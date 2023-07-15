# File conatining every functions that are necessary to display and update vendor's data at their respective reset time

# imports
import datetime
import asyncio
import logging

import pandas as pd

# from imports
from discord.ext import tasks
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from promise import Promise

# file imports
import api_requests

# from file imports
from data import myBot
from discord_features import check_xur

vendor_embeds = []
weekly_embeds = []


@tasks.loop(hours=24)
async def resets():
    """
    Each day, schedule a call to a function that will update every vendor's sale
    """

    await auto()


@resets.before_loop
async def before_reset():
    """
    Loop before 7PM to make sure to the start time at 19:00 exactly
    Allow to start the bot whenever we want and still have the call to resets() to be at 7PM
    """

    hour = 17
    minute = 00
    await myBot.wait_until_ready()
    now = datetime.datetime.now(datetime.timezone.utc)
    future = datetime.datetime(now.year, now.month, now.day, hour, minute, tzinfo=datetime.timezone.utc)
    if now.hour >= hour and now.minute >= minute:
        future += datetime.timedelta(days=1)
    await asyncio.sleep((future - now).seconds)


async def auto():
    """
    For each server, get its default channel.
    Send Xur's data on Friday
    Send Banshee-44's data on Tuesday
    """

    chans = []
    df = pd.read_csv('../guilds.csv')
    for chan in df['channel']:
        new_chan = myBot.get_channel(int(chan))
        chans.append(new_chan)
    if check_xur():
        xur_load(False)
    if datetime.datetime.now(datetime.timezone.utc).weekday() == 1:
        banshee_load()
        weekly_load()

    async def auto_(channel):
        tasks_ = []
        if check_xur() and datetime.datetime.now(datetime.timezone.utc).weekday() == 4:
            tasks_.append(xur_auto(channel))
        if datetime.datetime.now(datetime.timezone.utc).weekday() == 1:
            tasks_.append(weekly_auto(channel))
        await Promise.all(tasks_)

    coros = [auto_(chan) for chan in chans]
    await asyncio.gather(*coros)


def xur_load(overload: bool):
    """
    Load Xur's data and add it to vendor_embeds
    @param overload: when True, allow to always append xur's data to vendor_embeds
    """

    if overload or len(vendor_embeds) == 1 or datetime.datetime.now(datetime.timezone.utc).weekday() == 4:
        logging.info('xur loaded')
        vendor_embeds.append(api_requests.sales_vendor('Xûr'))


def banshee_load():
    """
    Load Banshee-44's data and update it in vendor_embeds
    """

    if datetime.datetime.now(datetime.timezone.utc).weekday() == 1:
        logging.info('banshee loaded')
        vendor_embeds.pop()
        vendor_embeds[0] = api_requests.sales_vendor('Banshee-44')


def weekly_load():
    """
    Load weekly data and update weekly_embeds
    """
    if datetime.datetime.now(datetime.timezone.utc).weekday() == 1:
        logging.info('weekly loaded')
        global weekly_embeds
        weekly_embeds = api_requests.get_weekly()


async def xur_auto(chan):
    """
    Send an embed with xur's data and a button to switch between the general and detailed view
    @param chan: the channel to send the embed
    """

    pos = 0
    button_details = [create_button(style=ButtonStyle.green, label="Click for details")]
    button_general = [create_button(style=ButtonStyle.red, label="Come back to general view")]
    action_row = [create_actionrow(*button_details), create_actionrow(*button_general)]
    await chan.send(embed=vendor_embeds[1][pos], components=[action_row[pos]])
    while 1:
        inter = await wait_for_component(myBot, components=[action_row[pos]])
        pos = (pos + 1) % 2
        await inter.edit_origin(embed=vendor_embeds[1][pos], components=[action_row[pos]])


async def banshee_auto(chan):
    """
    Send an embed with banshee-44's data and a button to switch between the general and detailed view
    @param chan: the channel to send the embed
    """

    pos = 0
    button_details = [create_button(style=ButtonStyle.green, label="Click for details")]
    button_general = [create_button(style=ButtonStyle.red, label="Come back to general view")]
    action_row = [create_actionrow(*button_details), create_actionrow(*button_general)]
    await chan.send(embed=vendor_embeds[0][pos], components=[action_row[pos]])
    while 1:
        inter = await wait_for_component(myBot, components=[action_row[pos]])
        pos = (pos + 1) % 2
        await inter.edit_origin(embed=vendor_embeds[0][pos], components=[action_row[pos]])


async def weekly_auto(chan):
    """
    Send an embed with the weekly data.
    @param chan: the channel to send th embed
    """

    await chan.send(embed=weekly_embeds[1])
