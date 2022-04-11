# Discord Bot

# imports
import os
import pickle
import sqlite3
import threading
import zipfile
import json
import discord
import requests

# from imports
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# file imports
import class_json
import embed
import server_application

# from file imports
from data import token, my_api_key, root, icon_root
from manifest_vendor import vendor_dic
from manifest import item_dic

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

prefix = '-'

intents = discord.Intents.all()
myBot = discord.Client(intents=intents)
bot = commands.Bot(prefix)
slash = SlashCommand(myBot, sync_commands=True)
access_token = 'Bearer '

hawkmoon = 3164616407

app = server_application.app


# run the app (the server) which is in server_application.py
def run_flask():
    app.run(port=8000, ssl_context=('cert/cert.pem', 'cert/priv_key.pem'))


# test
@myBot.event
async def on_message(msg):
    if msg.content.startswith("salut"):
        await msg.channel.send("salu")
    if msg.content.startswith("test"):
        r = requests.get('https://127.0.0.1:8000/', verify=False)
        # print(r.json())


# Launch the bot
# Start a new thread and launch the server on localhost:8000 on this thread
# Maybe change later ton only get the access token on request
@myBot.event
async def on_ready():
    threading.Thread(target=run_flask).start()
    await myBot.change_presence(activity=discord.Game(name="Ratio", type=discord.ActivityType.listening))
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


# Get Xur data
# \param bungie_name: The bungie name of someone from whom we are getting the data
# later have only my character set by default in order to only have the command w/0 arguments
@slash.slash(name="Banshee",
             description="Get Banshee's items")
async def banshee(msg: SlashContext):
    await msg.defer()
    # message = await msg.send("Banshee-44's Inventory:", delete_after=1)
    banshee_hash, banshee_large_icon, banshee_original_icon = get_gunsmith()
    me = server_application.me

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    banshee_path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[0]) + '/Vendors/' + str(banshee_hash) + '/?components=402'
    print('path:', banshee_path)
    r = requests.get(banshee_path, headers=header)
    resp = r.json()

    item_list = []
    for item in resp['Response']['sales']['data'].items():
        for key in item:
            if type(key) != str:
                print(key)
                item_list.append(key['itemHash'])

    item_dictionary = item_dic()
    items = []

    for item in item_dictionary['DestinyInventoryItemDefinition']:
        for item_l in item_list:
            if item['hash'] == item_l and (item['itemType'] == 3 or item['itemType'] == 26):
                i = (item['displayProperties']['name'], item['itemType'])
                items.append(i)

    res = "Banshee-44's items:\n"
    for item in items:
        res += item[0] + " " + str(item[1]) + "\n"

    res = embed.gunsmith_embed(items, banshee_large_icon, banshee_original_icon)
    await msg.send(embed=res)


# Get gunsmith's (Banshee-44) hash
def get_gunsmith():
    name = 'Banshee-44'
    data = vendor_dic()
    banshee_h = None
    large_icon_url = ''
    original_icon_url = ''
    for vendor, data in data['DestinyVendorDefinition'].items():
        if name == data['displayProperties']['name']:
            banshee_h = vendor
            large_icon_url = icon_root + data['displayProperties']['largeIcon']
            original_icon_url = icon_root + data['displayProperties']['originalIcon']
    return banshee_h, large_icon_url, original_icon_url


# Run the discord bot
myBot.run(token)
