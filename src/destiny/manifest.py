# File containing every functions that are necessary to create every dictionary needed based on the manifest

# imports
import json
import logging
import os
import pickle
import sqlite3
import zipfile
import requests

# from file imports
from data import my_api_key, root, auth_token


# Different category of the manifest with their main key
hash_vendor = {
    'DestinyVendorDefinition': 'hash',
}

hash_location = {
    'DestinyLocationDefinition': 'index',
    'DestinyDestinationDefinition': 'hash'
}

hash_item = {
    'DestinyInventoryItemDefinition': 'hash'
}

hash_sub_type = {
    'DestinyItemSubType': ''
}

hash_perk = {
    'DestinySandBoxPerkDefinition': 'hash',
    'DestinyStatDefinition': 'hash'
}

hash_activity = {
    'DestinyActivityDefinition': 'hash'
}

hash_activity_modifier = {
    'DestinyActivityModifierDefinition': 'hash'
}


def get_manifest():
    """
    Get the manifest and build 'Manifest.content' (containing all the data of the manifest)
    """

    headers = {"X-API-Key": my_api_key,
               "Authorization": 'Bearer ' + auth_token}
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
    print(os.getcwd())
    os.replace(name[0], 'destiny/pickle/Manifest.content')
    os.remove('MANZIP')
    print('Unzipped')


def build_dict(hash_dict):
    """
    Build the dictionary of all object passed as parameter
    :param hash_dict: the dictionary to get every information about all vendors
    :return: a dictionary with every hash : object as items
    """

    con = sqlite3.connect('destiny/pickle/Manifest.content')
    print('Connected')
    # create a cursor object
    cur = con.cursor()

    all_data = {}
    # for every table name in the dictionary
    for table_name in hash_dict.keys():
        # get a list of all the jsons from the table
        cur.execute('SELECT json from ' + table_name)
        logging.info('Generating %s dictionary...', table_name)

        # this returns a list of tuples: the first item in each tuple is our json
        vendors = cur.fetchall()

        # create a list of jsons
        vendor_jsons = [json.loads(vendor[0]) for vendor in vendors]

        # create a dictionary with the hashes as keys
        # and the jsons as values
        if table_name == 'DestinyInventoryItemDefinition' or table_name == 'DestinyItemSubType':
            all_data[table_name] = vendor_jsons
            return all_data
        vendor_dict = {}
        hash = hash_dict[table_name]
        for vendor in vendor_jsons:
            vendor_dict[vendor[hash]] = vendor
        # add that dictionary to our all_data using the name of the table
        # as a key.
        all_data[table_name] = vendor_dict

    logging.info('Dictionary Generated!')
    return all_data


def dic(path: str, hash_: dict):
    """
    Build the dictionary corresponding to the dictionary passed as parameter
    :param hash_: the current dictionary to build the object dictionary on
    :param path: the path to store the dictionary
    """

    if not os.path.isfile(path):
        get_manifest()
        all_data = build_dict(hash_)
        with open(path, 'wb') as data:
            pickle.dump(all_data, data)
            logging.info('%s Created', path)
    else:
        logging.info('%s Exists', path)
    with open(path, 'rb') as data:
        all_data = pickle.load(data)
    return all_data


def vendor_dic():
    """
    Build the vendor dictionary and create manifest_vendor.pickle if it doesn't exist
    :return: a dictionary with the information from the manifest about DestinyVendorDefinition
    """

    return dic(r'destiny/pickle/manifest_vendor.pickle', hash_vendor)


def item_dic():
    """
    Build the item dictionary and create manifest_item.pickle if it doesn't exist
    :return: a dictionary with the information from the manifest about DestinyInventoryItemDefinition
    """

    return dic(r'destiny/pickle/manifest_item.pickle', hash_item)


def perk_dic():
    """
    Build the perk dictionary and create manifest_perk.pickle if it doesn't exist
    :return: a dictionary with the information from the manifest about
    DestinySandBoxPerkDefinition and DestinySandBoxPerkDefinition
    """

    return dic(r'destiny/pickle/manifest_perk.pickle', hash_perk)


def location_dic():
    """
    Build the location dictionary and create manifest_perk.pickle if it doesn't exist
    :return: a dictionary with the information from the manifest about
    DestinyLocationDefinition and DestinyDestinationDefinition
    """

    return dic(r'destiny/pickle/manifest_location.pickle', hash_location)


def item_type():
    """
    Build the item_type dictionary and create manifest_perk.pickle if it doesn't exist
    :return: a dictionary with the information from the manifest about DestinyItemSubType
    """

    return dic(r'destiny/pickle/manifest_item_type.pickle', hash_sub_type)


def activity_dic():
    """
    Build the perk dictionary and create manifest_perk.pickle if it doesn't exist
    :return: a dictionary with the information from the manifest about DestinyActivityDefinition
    """

    return dic(r'destiny/pickle/manifest_activity.pickle', hash_activity)


def activity_modifier_dic():
    return dic(r'destiny/pickle/manifest_activity_modifier.pickle', hash_activity_modifier)
