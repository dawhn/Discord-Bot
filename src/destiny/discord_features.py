# File containing every function that are necessary to make automatic features on disc servers

# imports
import datetime
import logging
import os

import pandas as pd

# from imports
from data import myBot
from os import path


def check_xur():
    """
    Check if xur is present or not
    :return: True if xur is present, False otherwise
    """

    if (datetime.datetime.now(datetime.timezone.utc).weekday() < 1 or datetime.datetime.now(datetime.timezone.utc).weekday() > 4 or
            (datetime.datetime.now(datetime.timezone.utc).weekday() == 1 and datetime.datetime.now(datetime.timezone.utc).hour < 17) or
            (datetime.datetime.now(datetime.timezone.utc).weekday() == 4 and datetime.datetime.now(datetime.timezone.utc).hour >= 17)):
        return True
    return False


async def add_channel(guild) -> pd.DataFrame:
    """
    Add the guild (server) to ../guilds.csv and ask in the new server for a default channel then store it with its name
    :param guild: the guild to add
    :return: DataFrame object containing all servers and their respective default channel
    """

    if not path.exists('../guilds.csv'):
        register_guilds()
    data = pd.read_csv('../guilds.csv')
    data = data.iloc[:, 1:]

    await guild.text_channels[0].send(
        'Please tag the name of the channel (should start by a #) that you want your default channel to be')
    channel = await myBot.wait_for('message', check=check_author)
    while not is_good_channel(channel):
        await guild.text_channels[0].send("2. Please send the correct tag, should be the same format as: "
                                          "'#general'")
        channel = await myBot.wait_for('message', check=check_author)
    channel = int(channel.content[2:-1])
    new_row = pd.DataFrame([[guild.name, str(channel)]], columns=['name', 'channel'])
    data = data.append(new_row, ignore_index=True)
    print('data after: ', data)
    return data


@myBot.event
async def on_guild_join(guild):
    """
    When joining a guild (server) call a function to add the server to ../guilds.csv
    :param guild: the guild joined
    """

    await guild.text_channels[0].send('Hello {}'.format(guild.name))
    data: pd.DataFrame = await add_channel(guild)
    data.to_csv('../guilds.csv')


def is_good_channel(msg):
    """
    Check if the message has the right format to be a channel tag (<#...>)
    :param msg: the message where the channel tag should be
    :return: True if it has the right format, False otherwise
    """

    if msg.author == myBot.user:
        return False
    if not msg.content.startswith('<#'):
        return False
    return True


def check_author(msg):
    """
    Check if the author of the message is the bot
    :param msg: the message to test
    :return: True if author is not myBot, False otherwise
    """

    if msg.author == myBot.user:
        return False
    return True


def register_guilds():
    """
    For each guild (server) that the bot is in, store their name in ../guilds.csv
    """

    guilds = []
    for guild in myBot.guilds:
        guilds.append([guild.name, None])
    df = pd.DataFrame(guilds, columns=['name', 'channel'])
    df.to_csv('../guilds.csv')


async def check_default_channels():
    """
    On launch, check if every server as its default channel setup.
    - Yes: do nothing
    - No: send a message to the first text channel of the server to ask for a default channel. Wait for a valid name and
          store it
    :return:
    """

    if not path.exists('../guilds.csv'):
        register_guilds()
    data = pd.read_csv('../guilds.csv')
    data = data.iloc[:, 1:]
    logging.info('Server list:\n\t' + data.to_string().replace('\n', '\n\t'))

    for guild in myBot.guilds:
        found = False
        for d in data.iterrows():
            if guild.name == d[1]['name']:
                found = True
                if pd.isna(d[1]['channel']):
                    await guild.text_channels[0].send('Please tag the name of the channel (should start by a #) that '
                                                      'you want your default channel to be')
                    channel = await myBot.wait_for('message', check=check_author)
                    while not is_good_channel(channel):
                        await guild.text_channels[0].send("1. Please send the correct tag, should be the same format "
                                                          "as: '#general'")
                        channel = await myBot.wait_for('message', check=check_author)
                    channel = int(channel.content[2:-1])
                    new_val = pd.Series(str(channel), name='channel', index=[d[0]])
                    data.update(new_val)
                    print(data)

        if not found:
            await guild.text_channels[0].send(
                'Please tag the name of the channel (should start by a #) that you want your default channel to be')
            channel = await myBot.wait_for('message', check=check_author)
            while not is_good_channel(channel):
                await guild.text_channels[0].send("2. Please send the correct tag, should be the same format as: "
                                                  "'#general'")
                channel = await myBot.wait_for('message', check=check_author)
            channel = int(channel.content[2:-1])
            new_row = pd.DataFrame([[guild.name, str(channel)]], columns=['name', 'channel'])
            data = data.append(new_row)
            print(data)
    data.to_csv('../guilds.csv')
