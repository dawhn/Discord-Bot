# Discord Bot main file

# imports
import sys
import threading
import pandas as pd
import requests
import discord
import logging

# from imports
from discord.ext import commands
from discord_slash import SlashCommand
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# file imports
import api_requests
import automatic_commands
import server_application

# from file imports
from data import token, myBot
from bot_commands import slash
from manifest import vendor_dic, item_dic, location_dic
from discord_features import check_default_channels

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

bot = commands.Bot('')
access_token = 'Bearer '
app = server_application.app

# Logger setup
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('requests').setLevel(logging.ERROR)
logging.getLogger('flask').setLevel(logging.ERROR)


def run_flask():
    """
    # run the app (the server) which is in server_application.py
    """
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
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
    load()
    await check_default_channels()
    automatic_commands.resets.start()
    logging.info('Logged in as %s\n', myBot.user.name)


def load():
    """
    Load every data that is needed for automatics embed
    """

    automatic_commands.vendor_embeds.append(api_requests.sales_vendor('Banshee-44'))
    if automatic_commands.check_xur():
        automatic_commands.vendor_embeds.append(api_requests.sales_vendor('Xûr'))
    automatic_commands.weekly_embeds = api_requests.get_weekly()


# Run the disc bot
myBot.run(token)
