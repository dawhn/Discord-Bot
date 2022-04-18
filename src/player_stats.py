# File containing every functions that are necessary to retrieve data about a player

import server_application
import class_json
import requests

from data import root, my_api_key
from manifest_vendor import activity_dic

access_token = 'Bearer '


# Get Player data
# By searching player with its bungie name
def player(bungie_name: str) -> class_json.Player:
    me = server_application.me
    data = bungie_name.split("#")
    url = root + 'SearchDestinyPlayerByBungieName/' + 'all' + '/'
    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    body = {"displayName": data[0], "displayNameCode": data[1]}
    response = requests.post(url, headers=header, json=body)
    p = class_json.Player(response)
    if p.status != 200 or p.error_code != 1 or p.exception is not None:
        return None
    url_char = root + str(p.membership_types[1]) + '/Profile/' + str(p.membership_ids[1]) + '/?components=200'
    r = requests.get(url_char, headers=header)
    resp = r.json()
    for char_id, char in resp['Response']['characters']['data'].items():
        p.characters_ids.append(char_id)
    return p


# First, get the deleted characters (that might hold some data about raid history)
# For each character (deleted or not) get its raid history and parse each raid into a list with a count
# match each raid with its name and return the list
def get_all_raids(p: class_json.Player):
    me = server_application.me
    list_activity = []

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}
    test_url = root + str(p.membership_types[1]) + '/Account/' + str(p.membership_ids[1]) + '/Stats/?groups=0'
    r = requests.get(test_url, headers=header)
    resp = r.json()
    for character in resp['Response']['characters']:
        if character['deleted']:
            p.characters_ids.append(character['characterId'])

    for i in range(len(p.membership_types)):
        membership_id = p.membership_ids[i]
        membership_type = p.membership_types[i]
        for char_id in p.characters_ids:

            count = 250
            page = 0
            while True:
                path = root + str(membership_type) + '/Account/' + str(membership_id) + '/Character/' \
                       + str(char_id) + '/Stats/Activities/?count=' + str(count) + '&mode=4' + '&page=' + str(page)
                r = requests.get(path, headers=header)

                resp = r.json()
                if resp['ErrorCode'] == 1 and 'activities' in resp['Response']:
                    for elem in resp['Response']['activities']:
                        hash_activity = elem['activityDetails']['directorActivityHash']
                        if 'displayValue' in elem['values']['completed']['basic']: # 'displayValue' in elem['values']['completionReason']['basic']:
                            # completed = elem['values']['completionReason']['basic']['displayValue']
                            completed2 = elem['values']['completed']['basic']['displayValue']
                            if completed2 != 'Yes': # completed != 'Objective Completed':
                                continue

                            found = False
                            for activity in list_activity:
                                if activity[0] == hash_activity:
                                    activity[1] += 1
                                    found = True
                            if not found:
                                list_activity.append([hash_activity, 1])
                    count = len(resp['Response']['activities'])
                if 'activities' not in resp['Response']:
                    count = 0
                if count != 250:
                    break
                page += 1

    activity_dictionary = activity_dic()
    for act in list_activity:
        for hash_activity, activity in activity_dictionary['DestinyActivityDefinition'].items():
            if act[0] == hash_activity:
                name = activity['displayProperties']['name']
                split = name.split(':')
                if len(split) > 1:
                    if split[0] == 'Last Wish':
                        act.append(split[0])
                    else:
                        act.append(activity['displayProperties']['name'])
                else:
                    act.append(activity['displayProperties']['name'])
    res = []
    for act in list_activity:
        found = False
        for el in res:
            if el[0] == act[2]:
                el[1] += act[1]
                found = True
        if not found:
            res.append([act[2], act[1]])

    return res
