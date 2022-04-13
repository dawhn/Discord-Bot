# Discord Bot

# imports
import os
import pickle
import sqlite3
import threading
import zipfile
import json
import discord
import discord_slash.utils.manage_components
import requests

# from imports
from discord.ext import commands
# from discord_ui import Button
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# from discord_components import Button, DiscordComponents, Select

# file imports
import class_json
import embed
import server_application

# from file imports
from data import token, my_api_key, root, icon_root
from manifest_vendor import vendor_dic, item_dic, location_dic, perk_dic

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

prefix = ''
vendor_embeds = []

intents = discord.Intents.all()
myBot = discord.Client(intents=intents)
bot = commands.Bot(prefix)
slash = SlashCommand(myBot, sync_commands=True)
access_token = 'Bearer '
app = server_application.app


# run the app (the server) which is in server_application.py
def run_flask():
    app.run(port=8000, ssl_context=('../cert/cert.pem', '../cert/priv_key.pem'))


# test
@myBot.event
async def on_message(msg):
    if msg.content.startswith("salut"):
        await msg.channel.send("salu")
    if msg.content.startswith("test"):
        r = requests.get('https://127.0.0.1:8000/', verify=False)


# Launch the bot
# Start a new thread and launch the server on localhost:8000 on this new thread
# TODO: Launch a single request with arguments to automatically connect with my Bungie account in order to avoid
# TODO: the manual connection every launch or every hour later
@myBot.event
async def on_ready():
    threading.Thread(target=run_flask).start()
    await myBot.change_presence(activity=discord.Game(name="Ratio", type=discord.ActivityType.listening))
    me = server_application.me
    while me.token == {}:
        me = server_application.me
        continue
    item_dic()
    vendor_dic()
    location_dic()
    vendor_embeds.append(sales_vendor('Banshee-44'))
    # xur_embeds.append(sales_vendor('Xûr'))
    print('Logged in as')
    print(myBot.user.name + '\n')


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
    return p


# Get Banshee-44 sales data
# Already stocked locally on vendor_embeds to avoid recurrent requests
# Create 2 button (one for general view and one for detailed one)
# Infinite loop to be able to swap view at anytime
# No need to multithread discord can handle it many times and still do everything else although infinite loop ???
@slash.slash(name="Banshee",
             description="Get Banshee's sales inventory")
async def banshee(msg):
    await msg.defer()
    pos = 0
    button_details = [create_button(style=ButtonStyle.green, label="Click for details")]
    button_general = [create_button(style=ButtonStyle.red, label="Come back to general view")]
    action_row = [create_actionrow(*button_details), create_actionrow(*button_general)]
    await msg.send(embed=vendor_embeds[0][pos], components=[action_row[pos]])
    while 1:
        inter = await wait_for_component(myBot, components=[action_row[pos]])
        pos = (pos + 1) % 2
        await inter.edit_origin(embed=vendor_embeds[0][pos], components=[action_row[pos]])


# Get Xur sales data
# Already stocked locally on vendor_embeds to avoid recurrent requests
# Create 2 button (one for general view and one for detailed one)
# Infinite loop to be able to swap view at anytime
# No need to multithread discord can handle it many times and still do everything else although infinite loop ???
@slash.slash(name="Xur",
             description="Get Xur's sales inventory")
async def xur(msg: SlashContext):
    await msg.defer()
    pos = 0
    button_details = [create_button(style=ButtonStyle.green, label="Click for details")]
    button_general = [create_button(style=ButtonStyle.red, label="Come back to general view")]
    action_row = [create_actionrow(*button_details), create_actionrow(*button_general)]
    await msg.send(embed=vendor_embeds[1][pos], components=[action_row[pos]])
    while 1:
        inter = await wait_for_component(myBot, components=[action_row[pos]])
        pos = (pos + 1) % 2
        await inter.edit_origin(embed=vendor_embeds[1][pos], components=[action_row[pos]])


# Build 2 embed and return them:
# - First one is general with overall informations about the vendor sales
# - Second one is more specific (with perks, locations ...)
def sales_vendor(name: str):
    vendor_hash, large_icon, original_icon, destinations = get_vendor(name)
    me = server_application.me

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[0]) + '/Vendors/' + str(vendor_hash) + '/?components=402'

    r = requests.get(path, headers=header)
    resp = r.json()

    item_list = []
    items_number = []
    for item in resp['Response']['sales']['data'].items():
        for key in item:
            if type(key) != str:
                item_list.append((key['itemHash'], key['vendorItemIndex']))

    item_dictionary = item_dic()
    items = []

    for item in item_dictionary['DestinyInventoryItemDefinition']:
        for item_l in item_list:
            if item['hash'] == item_l[0] and (item['itemType'] == 3 or item['itemType'] == 26 or item['itemType'] == 2):
                if item['itemType'] == 3:
                    items_number.append((item['displayProperties']['name'], item_l[1]))
                i = (item['displayProperties']['name'], item['itemType'], item['inventory']['tierType'])
                items.append(i)

    details = get_details(vendor_hash, original_icon, destinations, name, items, items_number)
    if name == 'Banshee-44':
        return embed.gunsmith_embed(items, large_icon, original_icon), details
    if name == 'Xûr':
        return embed.xur_embed(items, large_icon, original_icon), details


# Get all perks for each item sold by the vendor
# return a list containing all items with their perk sold by the vendor
def get_items_perks(vendor_hash: str, items: [()]):
    me = server_application.me
    perk_dictionary = perk_dic()

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}
    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[0]) + '/Vendors/' + str(vendor_hash) + '/?components=302'
    r = requests.get(path, headers=header)
    resp = r.json()
    perks = resp['Response']['itemComponents']['perks']['data'].items()

    items_perks = []
    for item in items:
        items_perks.append([item[1], item[0]])

    for perk in perks:
        i = 0
        curr = -1
        for item in items_perks:
            if str(item[0]) == perk[0]:
                curr = i
            i += 1
        if curr == -1:
            continue
        for perk_ in perk[1]['perks']:
            perk_hash = perk_['perkHash']
            for hash_perk, item in perk_dictionary['DestinySandBoxPerkDefinition'].items():
                if hash_perk == perk_hash:
                    if 'name' in item['displayProperties']:
                        items_perks[curr].append(item['displayProperties']['name'])

    return items_perks


# get the details of the current vendor (change depending which vendor we are on)
# return an emebed message containing these details
def get_details(vendor_hash, original_icon: str, destinations: [], name: str, items: [], items_number: [()]):
    items_perks = get_items_perks(vendor_hash, items_number)
    destination, index = get_destination(vendor_hash, destinations)
    if name == 'Banshee-44':
        return embed.gunsmith_detail_embed(items_perks, original_icon)
    if name == 'Xûr':
        return embed.xur_detail_embed(items, original_icon, index)


# get the destination of the current vendor amongst every destination he can be in (might not work for xur)
def get_destination(vendor_hash: str, destinations: []):
    me = server_application.me

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[0]) + '/Vendors/' + str(vendor_hash) + '/?components=400'

    r = requests.get(path, headers=header)
    resp = r.json()

    location_index = resp['Response']['vendor']['data']['vendorLocationIndex']

    location_dictionary = location_dic()
    actual_dest = destinations[location_index]

    for destination_hash, destination in location_dictionary['DestinyDestinationDefinition'].items():
        if actual_dest == destination_hash:
            return destination, location_index


# Get vendor hash, large_icon and original_icon
def get_vendor(name: str):
    data = vendor_dic()
    vendor_hash = None
    large_icon_url = ''
    original_icon_url = ''
    destinations = []
    for vendor, data_ in data['DestinyVendorDefinition'].items():
        if name == data_['displayProperties']['name']:
            vendor_hash = vendor
            if 'displayProperties' in data_:
                large_icon_url = icon_root + data_['displayProperties']['largeIcon']
                if 'mapIcon' in data_['displayProperties']:
                    original_icon_url = icon_root + data_['displayProperties']['mapIcon']
            if 'locations' in data_:
                for location in data_['locations']:
                    destinations.append(location['destinationHash'])
            if name == 'Xûr':
                break
    return vendor_hash, large_icon_url, original_icon_url, destinations


# Run the discord bot
myBot.run(token)
