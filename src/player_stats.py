# File containing every functions that are necessary to retrieve data about a player

# imports
import requests

# file imports
import server_application

# from file imports
from classes import class_json
from data import root, my_api_key
from manifest import activity_dic

access_token = 'Bearer '


def player(bungie_name: str) -> class_json.Player:
    """
    Get player data by searching the player with its bungie name
    :param bungie_name: bungie name of the player
    :return: an object class_json.Player
    """

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


def get_all_deleted_char(p: class_json.Player):
    """
    Get all the deleted characters (which might hold some adat about the player's activity history) and add them to the
    characters_ids attribute of the parameter p
    :param p: the current player of classes class_json.Player
    """

    me = server_application.me
    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    player_char_url = root + str(p.membership_types[1]) + '/Account/' + str(p.membership_ids[1]) + '/Stats/?groups=0'
    r = requests.get(url=player_char_url, headers=header)
    resp = r.json()
    for character in resp['Response']['characters']:
        if character['deleted']:
            p.characters_ids.append(character['characterId'])


def get_all_activity(p: class_json.Player, mode: int):
    """
    For each character gets id history based on which mode is passed as a parameter
    :param p: the current player of classes class_json.Player
    :param mode: type of activity to send to the request
    :return: a list of all activities of the current mode with the number of clear for each
    """

    me = server_application.me
    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}
    get_all_deleted_char(p)
    list_activity = []
    for i in range(len(p.membership_types)):
        membership_id = p.membership_ids[i]
        membership_type = p.membership_types[i]
        for char_id in p.characters_ids:

            count = 250
            page = 0
            while True:
                path = root + str(membership_type) + '/Account/' + str(membership_id) + '/Character/' \
                       + str(char_id) + '/Stats/Activities/?count=' + str(count) + '&mode=' + str(
                    mode) + '&page=' + str(page)
                r = requests.get(path, headers=header)

                resp = r.json()
                if resp['ErrorCode'] == 1 and 'activities' in resp['Response']:
                    for elem in resp['Response']['activities']:
                        hash_activity = elem['activityDetails']['directorActivityHash']
                        if 'displayValue' in elem['values']['completed']['basic']:
                            completed2 = elem['values']['completed']['basic']['displayValue']
                            stop = False
                            # if mode == 82 or mode == 46:
                            completed = elem['values']['completionReason']['basic']['displayValue']
                            if completed != 'Objective Completed':
                                stop = True
                            if completed2 != 'Yes' or stop:
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
    return list_activity


def parse_activity(p: class_json.Player, mode: int):
    """
    Match each activity with its corresponding name
    :param p: the current player of classes class_json.Player
    :param mode: type of activity to send to the request
    :return: a list of all activities of the current mode with their name and the number of clear for each
    """

    list_activity = get_all_activity(p=p, mode=mode)

    activity_dictionary = activity_dic()
    for act in list_activity:
        for hash_activity, activity in activity_dictionary['DestinyActivityDefinition'].items():
            if act[0] == hash_activity:
                name = activity['displayProperties']['name']
                if name == 'Nightfall: The Ordeal: Grandmaster' or name == 'Nightfall: Grandmaster':
                    name = 'Nightfall Grandmaster: '
                    name += activity['displayProperties']['description']
                stop = False
                if mode == 46:
                    if 'Grandmaster' not in name:
                        # list_activity.remove(act)
                        stop = True
                if not stop:
                    split = name.split(':')
                    if len(split) > 2:
                        if 'Grandmaster' in split[1]:
                            name = 'Nightfall Grandmaster:' + split[2]
                            act.append(name)
                    elif len(split) > 1:
                        if split[0] == 'Last Wish':
                            act.append(split[0])
                        else:
                            act.append(name)
                    else:
                        act.append(name)
                else:
                    break
    res = []
    for act in list_activity:
        if len(act) == 3:
            found = False
            for el in res:
                if el[0] == act[2]:
                    el[1] += act[1]
                    found = True
            if not found:
                res.append([act[2], act[1]])
    return res


def get_all_raids(p: class_json.Player):
    """
    Get all raids for the current player p
    :param p: the current player of classes class_json.Player
    :return: a list of all raids with their name and the number of clear for each
    """

    return parse_activity(p=p, mode=4)


def get_all_dungeons(p: class_json.Player):
    """
    Get all dungeons for the current player p
    :param p: the current player of classes class_json.Player
    :return: a list of all dungeons with their name and the number of clear for each
    """

    return parse_activity(p=p, mode=82)


def get_all_gms(p: class_json.Player):
    """
    Get all grandmaster nightfalls for the current player p
    :param p: the current player of classes class_json.Player
    :return: a list of all grandmaster nightfalls with their name and the number of clear for each
    """

    return parse_activity(p=p, mode=46)
