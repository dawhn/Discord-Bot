# imports
import time
import logging

# from imports
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, create_select, \
    create_select_option
from discord_slash.utils.manage_commands import create_option

# file imports
import api_requests
import player_stats
import automatic_commands
import embed
import server_application

# from file imports
from data import myBot
from discord_features import check_xur

slash = SlashCommand(myBot, sync_commands=True)


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
    logging.info("/banshee command send")
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
    logging.info("/xur command send")
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
    @param msg: Slash command message send by a user
    @param bungie_name: parameter of the slash command, correspond to a bungie name (has the format name#number)
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
    logging.info("/stats command send")
    while 1:
        inter = await wait_for_component(myBot, components=[action_row])
        pos = int(inter.values[0])
        await inter.edit_origin(embed=data_embed[pos], components=[action_row])


@slash.slash(name="Weekly",
             description="Information about this week")
async def weekly(msg: SlashContext):
    """
    Get weekly data
    Stocked on automatic_commands.weekly_embeds to avoid repetitive requests
    @param msg: Slash command message send by a user
    """

    await msg.defer()
    me = server_application.me
    if time.time() > me.token['access_expires']:
        api_requests.refresh_token()
    embeds = automatic_commands.weekly_embeds
    style = ButtonStyle.blue
    button_nf = [create_button(style=style, label="Nightfalls")]
    button_raid = [create_button(style=style, label="Raids")]
    button_hunt = [create_button(style=style, label="Hunts")]
    button_wq = [create_button(style=style, label="Witch Queen")]
    button_pvp = [create_button(style=style, label="PVP")]

    action_row = [create_actionrow(*button_nf, *button_raid, *button_hunt, *button_wq, *button_pvp)]

    select = create_select(
        options=[
            create_select_option("Vow of the Disciple", value='0'),
            create_select_option("Vault of Glass", value="1"),
            create_select_option("Garden of Salvation", value="2"),
            create_select_option("Deep Stone Crypt", value="3")
        ],
        placeholder="Choose a raid for details"
    )

    pos = 0
    d_pos = 0
    await msg.send(embed=embeds[pos], components=action_row)
    logging.info("/weekly command send")
    while 1:
        inter = await wait_for_component(myBot, components=action_row)
        if inter.values is None:
            if inter.component['label'] == 'Nightfalls':
                pos = 0
                d_pos = 0
                style = ButtonStyle.blue
            if inter.component['label'] == 'Raids':
                pos = 1
                d_pos = 0
                style = ButtonStyle.gray
            if inter.component['label'] == 'Hunts':
                pos = 2
                d_pos = 0
                style = ButtonStyle.blue
            if inter.component['label'] == 'Witch Queen':
                pos = 3
                d_pos = 0
                style = ButtonStyle.green
            if inter.component['label'] == 'PVP':
                pos = 4
                d_pos = 0
                style = ButtonStyle.red
        else:
            d_pos = int(inter.values[0])

        button_nf = [create_button(style=style, label="Nightfalls")]
        button_raid = [create_button(style=style, label="Raids")]
        button_hunt = [create_button(style=style, label="Hunts")]
        button_wq = [create_button(style=style, label="Witch Queen")]
        button_pvp = [create_button(style=style, label="PVP")]


        action_row = [create_actionrow(*button_nf, *button_raid, *button_hunt, *button_wq, *button_pvp)]
        if pos == 1:
            action_row.append(create_actionrow(select))
        if d_pos == 0:
            await inter.edit_origin(embed=embeds[pos], components=action_row)
        else:
            await inter.edit_origin(embed=embeds[5][d_pos], components=action_row)

# activity demand like echo eternel bot (with buttons