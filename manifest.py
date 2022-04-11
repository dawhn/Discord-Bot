import json
import os
import pickle
import requests
import sqlite3
import zipfile

import data
from data import my_api_key


def get_manifest():
    manifest_url = 'https://www.bungie.net/Platform/Destiny2/Manifest/'

    # get the manifest location from the json
    headers = {"X-API-Key": my_api_key,
               "Authorization": 'Bearer ' + data.auth_token}
    r = requests.get(manifest_url, headers=headers)
    manifest = r.json()
    mani_url = 'https://www.bungie.net'+manifest['Response']['mobileWorldContentPaths']['en']

    # Download the file, write it to 'MANZIP'
    r = requests.get(mani_url, headers=headers)
    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    # Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    print(name[0])
    os.replace(name[0], 'Manifest.content')
    print('Unzipped!')


hashes = {
    # 'DestinyActivityDefinition': 'activityHash',
    # 'DestinyActivityTypeDefinition': 'activityTypeHash',
    # 'DestinyClassDefinition': 'classHash',
    # 'DestinyGenderDefinition': 'genderHash',
    # 'DestinyInventoryBucketDefinition': 'bucketHash',
    'DestinyInventoryItemDefinition': 'itemHash'
    '''DestinyProgressionDefinition': 'progressionHash',
    'DestinyRaceDefinition': 'raceHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyUnlockFlagDefinition': 'flagHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyDirectorBookDefinition': 'bookHash',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyDestinationDefinition': 'destinationHash',
    'DestinyPlaceDefinition': 'placeHash',
    'DestinyActivityBundleDefinition': 'bundleHash',
    'DestinyStatGroupDefinition': 'statGroupHash',
    'DestinySpecialEventDefinition': 'eventHash',
    'DestinyFactionDefinition': 'factionHash',
    'DestinyVendorCategoryDefinition': 'categoryHash',
    'DestinyEnemyRaceDefinition': 'raceHash',
    'DestinyScriptedSkullDefinition': 'skullHash',
    'DestinyGrimoireCardDefinition': 'cardId'''
}

'''hashes_trunc = {
    'DestinyInventoryItemDefinition': 'itemHash',
    'DestinyTalentGridDefinition': 'gridHash',
    'DestinyHistoricalStatsDefinition': 'statId',
    'DestinyStatDefinition': 'statHash',
    'DestinySandboxPerkDefinition': 'perkHash',
    'DestinyStatGroupDefinition': 'statGroupHash'
}'''


def build_dict(hash_dict):
    # connect to the manifest
    con = sqlite3.connect('manifest.content')
    print('Connected')
    # create a cursor object
    cur = con.cursor()

    all_data = {}
    # for every table name in the dictionary
    for table_name in hash_dict.keys():
        # get a list of all the jsons from the table
        cur.execute('SELECT json from '+table_name)
        print('Generating '+table_name+' dictionary....')

        # this returns a list of tuples: the first item in each tuple is our json
        items = cur.fetchall()

        # create a list of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        all_data[table_name] = item_jsons
        # create a dictionary with the hashes as keys
        # and the jsons as values
        '''item_dict = {}
        hash = hash_dict[table_name]
        for item in item_jsons:
            item_dict[item[hash]] = item

        # add that dictionary to our all_data using the name of the table
        # as a key.
        all_data[table_name] = item_dict'''

    return all_data


def item_dic():
    # check if pickle exists, if not create one.
    if not os.path.isfile(r'manifest_item.pickle'):
        get_manifest()
        all_data = build_dict(hashes)
        with open('manifest_item.pickle', 'wb') as data:
            pickle.dump(all_data, data)
            print("'manifest_item.pickle' created!\nDONE!")
    else:
        print("'manifest_item.pickle' Exists")
    with open('manifest_item.pickle', 'rb') as data:
        all_data = pickle.load(data)
    return all_data

# print(all_data)
'''hash = 1274330687
all_data = item_dic()
ghorn = all_data['DestinyInventoryItemDefinition'][hash]

print('Name: '+ghorn['itemName'])
print('Type: '+ghorn['itemTypeName'])
print('Tier: '+ghorn['tierTypeName'])
print(ghorn['itemDescription'])'''