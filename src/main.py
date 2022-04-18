# Discord Bot

# imports
import threading
import discord
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
import embed
import player_stats
import server_application

# from file imports
from data import token, my_api_key, root, icon_root
from manifest_vendor import vendor_dic, item_dic, location_dic, perk_dic
from perks_data import DestinyItemSubType

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
# TODO: Do somthing with the refresh_token (might allow to not have to repeat the whole process again but skip parts)
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
    vendor_embeds.append(sales_vendor('Xûr'))
    print('Logged in as')
    print(myBot.user.name + '\n')


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


# Get player's data
# For now, only player's raid data is retrieved
@slash.slash(name="Stats",
             description="Get player stats")
async def stats(msg: SlashContext):
    await msg.defer()
    name = "Dawhn#0621"
    p = player_stats.player(name)
    raid_data = player_stats.get_all_raids(p)
    raid_data.sort()
    await msg.send(embed=embed.raid_stats_embed(raid_data, name))


# Build 2 embed and return them:
# - First one is general with overall information about the vendor sales
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
                    sub_type = item['itemSubType']
                    type_name = ''
                    for name_, type_id in DestinyItemSubType.items():
                        if sub_type == type_id:
                            type_name = name_
                    items_number.append((item['displayProperties']['name'], item_l[1], type_name))
                i = (item['displayProperties']['name'], item['itemType'], item['inventory']['tierType'], item_l[1])
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
        items_perks.append([item[1], item[0], item[2]])

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


# Get all stats for each armor sold by the vendor
def get_all_stats(vendor_hash: str, items: []):
    me = server_application.me
    perk_dictionary = perk_dic()
    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[0]) + '/Vendors/' + str(vendor_hash) + '/?components=304'

    r = requests.get(path, headers=header)
    resp = r.json()
    stats_ = resp['Response']['itemComponents']['stats']['data'].items()

    all_stats = []

    for stat in stats_:
        curr_stats = []
        found = False
        stop = False
        for hash_stat in stat[1]['stats']:
            for stat_hash, item_stat in perk_dictionary['DestinyStatDefinition'].items():
                if stat_hash == int(hash_stat):
                    name = item_stat['displayProperties']['name']
                    if name == 'Mobility' or name == 'Resilience' or name == 'Recovery' or name == 'Discipline' or \
                            name == 'Intellect' or name == 'Strength':
                        if not found:
                            item_name = ""
                            item_rarity = 0
                            for item in items:
                                if item[3] == int(stat[0]):
                                    item_name = item[0]
                                    item_rarity = item[2]
                            if item_rarity != 6:
                                stop = True
                            if not stop:
                                curr_stats.append(item_name)
                            # curr_stats.append(item_rarity)
                            found = True
                        if not stop:
                            if found and curr_stats[0] != '':
                                curr_stats.append((item_stat['displayProperties']['name'], stat[1]['stats'][hash_stat]['value']))
        if found and not stop:
            all_stats.append(curr_stats)
    return all_stats


# get the details of the current vendor (change depending which vendor we are on)
# return an emebed message containing these details
def get_details(vendor_hash, original_icon: str, destinations: [], name: str, items: [], items_number: [()]):
    items_perks = get_items_perks(vendor_hash, items_number)
    destination, index = get_destination(vendor_hash, destinations)
    if name == 'Banshee-44':
        return embed.gunsmith_detail_embed(items_perks, original_icon)
    if name == 'Xûr':
        stats_ = get_all_stats(vendor_hash, items)
        return embed.xur_detail_embed(items, original_icon, index, items_perks, stats_)


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
