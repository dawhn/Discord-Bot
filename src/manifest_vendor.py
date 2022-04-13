import json
import os
import pickle
import sqlite3
import zipfile
import requests

import data
from data import my_api_key, token, root


hash_vendor = {
    'DestinyVendorDefinition': 'hash',
}

hash_location = {
    'DestinyLocationDefinition': 'index',
    'DestinyDestinationDefinition': 'hash'
}

hash_item = {
    'DestinyInventoryItemDefinition': 'hash',
}

hash_perk = {
    'DestinySandBoxPerkDefinition': 'hash'
}


# get the manifest and build Manifest.content (containing all the data of the manifest)
def get_manifest():
    headers = {"X-API-Key": my_api_key,
               "Authorization": 'Bearer ' + data.auth_token}
    url = root + 'Manifest/'
    r = requests.get(url, headers=headers)
    manifest = r.json()
    manifest_url = 'https://www.bungie.net' + manifest['Response']['mobileWorldContentPaths']['en']
    r = requests.get(manifest_url, headers=headers)

    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print('Downloaded')

    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    print(name[0])
    os.replace(name[0], '../pickle/Manifest.content')
    os.remove('MANZIP')
    print('Unzipped')


# Build the dictionary of all the vendors (CF DestinyVendorDefinition)
def build_dict(hash_dict):
    # connect to the manifest
    con = sqlite3.connect('../pickle/manifest.content')
    print('Connected')
    # create a cursor object
    cur = con.cursor()

    all_data = {}
    # for every table name in the dictionary
    for table_name in hash_dict.keys():
        # get a list of all the jsons from the table
        cur.execute('SELECT json from ' + table_name)
        print('Generating ' + table_name + ' dictionary....')

        # this returns a list of tuples: the first item in each tuple is our json
        vendors = cur.fetchall()

        # create a list of jsons
        vendor_jsons = [json.loads(vendor[0]) for vendor in vendors]

        # create a dictionary with the hashes as keys
        # and the jsons as values
        if table_name == 'DestinyInventoryItemDefinition':
            all_data[table_name] = vendor_jsons
            return all_data
        vendor_dict = {}
        hash = hash_dict[table_name]
        for vendor in vendor_jsons:
            vendor_dict[vendor[hash]] = vendor
        # add that dictionary to our all_data using the name of the table
        # as a key.
        all_data[table_name] = vendor_dict

    print('Dictionary Generated!')
    return all_data


# Build the vendor dictionary and create manifest.pick if it doesn't exist and returns the dicctionary
def vendor_dic():
    if not os.path.isfile(r'../pickle/manifest_vendor.pickle'):
        get_manifest()
        all_data = build_dict(hash_vendor)
        with open('../pickle/manifest_vendor.pickle', 'wb') as data:
            pickle.dump(all_data, data)
            print("'manifest_vendor.pickel' Created")
    else:
        print("'manifest_vendor.pickle' Exists")
    with open('../pickle/manifest_vendor.pickle', 'rb') as data:
        all_data = pickle.load(data)
    return all_data


def item_dic():
    # check if pickle exists, if not create one.
    if not os.path.isfile(r'../pickle/manifest_item.pickle'):
        get_manifest()
        all_data = build_dict(hash_item)
        with open('../pickle/manifest_item.pickle', 'wb') as data:
            pickle.dump(all_data, data)
            print("'manifest_item.pickle' Created")
    else:
        print("'manifest_item.pickle' Exists")
    with open('../pickle/manifest_item.pickle', 'rb') as data:
        all_data = pickle.load(data)
    return all_data


def perk_dic():
    if not os.path.isfile(r'../pickle/manifest_perk.pickle'):
        get_manifest()
        all_data = build_dict(hash_perk)
        with open('../pickle/manifest_perk.pickle', 'wb') as data:
            pickle.dump(all_data, data)
            print("'manifest_perk.pickle' Created")
    else:
        print("'manifest_perk.pickle' Exists")
    with open('../pickle/manifest_perk.pickle', 'rb') as data:
        all_data = pickle.load(data)
    return all_data


def location_dic():
    # check if pickle exists, if not create one.
    if not os.path.isfile(r'../pickle/manifest_location.pickle'):
        get_manifest()
        all_data = build_dict(hash_location)
        with open('../pickle/manifest_location.pickle', 'wb') as data:
            pickle.dump(all_data, data)
            print("'manifest_location.pickle' Created")
    else:
        print("'manifest_location.pickle' Exists")
    with open('../pickle/manifest_location.pickle', 'rb') as data:
        all_data = pickle.load(data)
    return all_data