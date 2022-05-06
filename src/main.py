# Discord Bot main file

# imports
import threading
import time
import pandas as pd
import requests
import discord

# from imports
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, create_select, \
    create_select_option
from discord_slash.utils.manage_commands import create_option
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# file imports
import api_requests
import player_stats
import automatic_commands
import embed
import server_application

# from file imports
from data import token, myBot
from manifest import vendor_dic, item_dic, location_dic
from discord_features import check_default_channels, check_xur

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

bot = commands.Bot('')
slash = SlashCommand(myBot, sync_commands=True)
access_token = 'Bearer '
app = server_application.app


def run_flask():
    """
    # run the app (the server) which is in server_application.py
    """

    app.run(port=8000, ssl_context=('../cert/cert.pem', '../cert/priv_key.pem'))


# test
@myBot.event
async def on_message(msg):
    if msg.content.startswith("salut"):
        await msg.channel.send("salu")
    if msg.content.startswith("test"):
        for guild in myBot.guilds:
            print(guild)


@myBot.event
async def on_ready():
    """
    Launch the bot
    Start a new thread and launch the server on localhost:8000 on this new thread
    """

    threading.Thread(target=run_flask).start()
    await myBot.change_presence(activity=discord.Game(name="Ratio", type=discord.ActivityType.listening))
    if not server_application.get_stored_informations():
        # if data is not stored in the csv file, get the data by connecting to the server and bungie.net
        me = server_application.me
        print("Connect to https://127.0.0.1:8000/ to authorize the app and get the access_token")
        while me.token == {}:
            me = server_application.me
            continue
        # create CSV file and write it to store it and reused it next time the bot logs in
        data_ = {'access_token': [me.token['access_token']],
                 'access_expires': [me.token['access_expires']],
                 'refresh_token': [me.token['refresh_token']],
                 'refresh_expires': [me.token['refresh_expires']]}
        df = pd.DataFrame(data_)
        df.to_csv('../data.csv')

    item_dic()
    vendor_dic()
    location_dic()
    automatic_commands.vendor_embeds.append(api_requests.sales_vendor('Banshee-44'))
    await check_default_channels()
    automatic_commands.resets.start()
    print('Logged in as')
    print(myBot.user.name + '\n')


@slash.slash(name="Banshee",
             description="Get Banshee's sales inventory")
async def banshee(msg):
    """
    Get Banshee-44 sales data.
    Already stocked locally on vendor_embeds to avoid recurrent requests.
    Create 2 button (one for general view and one for detailed one).
    Infinite loop to be able to swap view at anytime
    :param msg: Slash command message send by a user.
    """

    await msg.defer()
    pos = 0
    button_details = [create_button(style=ButtonStyle.green, label="Click for details")]
    button_general = [create_button(style=ButtonStyle.red, label="Come back to general view")]
    action_row = [create_actionrow(*button_details), create_actionrow(*button_general)]
    await msg.send(embed=automatic_commands.vendor_embeds[0][pos], components=[action_row[pos]])
    while 1:
        inter = await wait_for_component(myBot, components=[action_row[pos]])
        pos = (pos + 1) % 2
        await inter.edit_origin(embed=automatic_commands.vendor_embeds[0][pos], components=[action_row[pos]])


@slash.slash(name="Xur",
             description="Get Xur's sales inventory")
async def xur(msg: SlashContext):
    """
    Get Xur sales data.
    Already stocked locally on vendor_embeds to avoid recurrent requests.
    Create 2 button (one for general view and one for detailed one).
    Infinite loop to be able to swap view at anytime
    :param msg: Slash command message send by a user.
    """

    if not check_xur():
        await msg.send("Stay tunned until Friday 7 PM to know about xur's information ")
        return
    await msg.defer()
    if len(automatic_commands.vendor_embeds) == 1:
        automatic_commands.xur_load(True)
    pos = 0
    button_details = [create_button(style=ButtonStyle.green, label="Click for details")]
    button_general = [create_button(style=ButtonStyle.red, label="Come back to general view")]
    action_row = [create_actionrow(*button_details), create_actionrow(*button_general)]
    await msg.send(embed=automatic_commands.vendor_embeds[1][pos], components=[action_row[pos]])
    while 1:
        inter = await wait_for_component(myBot, components=[action_row[pos]])
        pos = (pos + 1) % 2
        await inter.edit_origin(embed=automatic_commands.vendor_embeds[1][pos], components=[action_row[pos]])


@slash.slash(name="Stats",
             description="Get player stats",
             options=[
                 create_option(
                     name="bungie_name",
                     description="Bungie name of the player",
                     required=True,
                     option_type=3
                 )
             ])
async def stats(msg: SlashContext, bungie_name: str):
    """
    Get player's data
    For now, only player's raid, dungeon and grandmaster nightfall data is retrieved
    :param msg: Slash command message send by a user
    :param bungie_name: parameter of the slash command, correspond to a bungie name (has the format name#number)
    """

    await msg.defer()
    me = server_application.me
    if time.time() > me.token['refresh_expires']:
        print("REFRESH CODE EXPIRE ONE YEAR AS PASSED")
    if time.time() > me.token['access_expires']:
        api_requests.refresh_token()
    p = player_stats.player(bungie_name)

    raid_data = player_stats.get_all_raids(p)
    dungeon_data = player_stats.get_all_dungeons(p)
    gm_data = player_stats.get_all_gms(p)
    dungeon_data.sort()
    raid_data.sort()
    raid_embed = embed.raid_stats_embed(raid_data, bungie_name)
    dungeon_embed = embed.dungeon_stats_embed(dungeon_data, bungie_name)
    gm_embed = embed.gm_stats_embed(gm_data, bungie_name)
    data_embed = [raid_embed, dungeon_embed, gm_embed]

    select = create_select(
        options=[
            create_select_option("Raid", value='0'),
            create_select_option("Dungeon", value="1"),
            create_select_option("Grandmaster", value="2")
        ],
        placeholder="Choose your option"
    )
    action_row = create_actionrow(select)
    await msg.send(embed=data_embed[0], components=[action_row])
    while 1:
        inter = await wait_for_component(myBot, components=[action_row])
        pos = int(inter.values[0])
        await inter.edit_origin(embed=data_embed[pos], components=[action_row])


# Run the disc bot
myBot.run(token)
