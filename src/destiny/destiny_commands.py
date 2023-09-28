# imports
import time
import logging

# from imports
import discord
from discord_slash import SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, create_select, \
    create_select_option
from destiny.utils.activity_utils import get_all_gms, get_all_dungeons, get_all_raids
from destiny.utils.inventory_utils import get_inventory

# file imports
import destiny.api_requests as api_requests
import destiny.automatic_commands as automatic_commands
import destiny.server_application as server_application
import destiny.classes.class_json as class_json

# from file imports
from data import myBot, icon_root
from destiny.discord_features import check_xur


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
    p = class_json.player(bungie_name)

    raid_data = get_all_raids(p)
    dungeon_data = get_all_dungeons(p)
    gm_data = get_all_gms(p)
    activity_stats = class_json.ActivityStats(p, raid_data, dungeon_data, gm_data)

    select = create_select(
        options=[
            create_select_option("Raid", value='0'),
            create_select_option("Dungeon", value="1"),
            create_select_option("Grandmaster", value="2")
        ],
        placeholder="Choose your option"
    )
    action_row = create_actionrow(select)
    await msg.send(embed=activity_stats.data_embed[0], components=[action_row])
    logging.info("/stats command send")
    while 1:
        inter = await wait_for_component(myBot, components=[action_row])
        pos = int(inter.values[0])
        await inter.edit_origin(embed=activity_stats.data_embed[pos], components=[action_row])


async def weekly(msg: SlashContext):
    """
    Get weekly data
    Stocked on automatic_commands.weekly_embeds to avoid repetitive requests
    @param msg: Slash command message send by a user
    """

    # await msg.defer()
    auth = msg.author_id
    me = server_application.me
    if time.time() > me.token['access_expires']:
        api_requests.refresh_token()
    embeds = automatic_commands.weekly_embeds[0]
    style = ButtonStyle.blue
    button_nf = [create_button(style=style, label="Nightfalls")]
    button_raid = [create_button(style=style, label="Raids")]
    button_hunt = [create_button(style=style, label="Hunts")]
    button_campaign = [create_button(style=style, label="Campaign")]
    button_pvp = [create_button(style=style, label="PVP")]

    action_row = [create_actionrow(*button_nf, *button_raid, *button_hunt, *button_campaign, *button_pvp)]

    select = create_select(
        options=[
            create_select_option("Vow of the Disciple", value='0'),
            create_select_option("Vault of Glass", value="1"),
            create_select_option("Garden of Salvation", value="2"),
            create_select_option("Deep Stone Crypt", value="3"),
            create_select_option("Vow of the Disciple", value='4'),
            create_select_option("Root of the Nightmare", value="5")
        ],
        placeholder="Choose a raid for details"
    )

    pos = 0
    d_pos = 0
    await msg.send(embed=embeds[pos], components=action_row)
    logging.info("/weekly command send")
    while 1:
        inter = await wait_for_component(myBot, components=action_row)
        if inter.author.id != auth and not inter.author.guild_permissions.administrator:
            await inter.send('You cannot do that', hidden=True)
        else:
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
                if inter.component['label'] == 'Campaign':
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
            button_campaign = [create_button(style=style, label="Campaign")]
            button_pvp = [create_button(style=style, label="PVP")]

            action_row = [create_actionrow(*button_nf, *button_raid, *button_hunt, *button_campaign, *button_pvp)]
            if pos == 1:
                action_row.append(create_actionrow(select))
            if d_pos == 0:
                await inter.edit_origin(embed=embeds[pos], components=action_row)
            else:
                await inter.edit_origin(embed=embeds[5][d_pos], components=action_row)


async def activity(msg: SlashContext, activity_type: str, name: str, description: str, schedule: str):
    act = class_json.Activity(name, description, schedule, activity_type, msg.author.name, msg.author.id)
    button_yes = [create_button(style=ButtonStyle.green, label="Register")]
    button_maybe = [create_button(style=ButtonStyle.gray, label="Maybe")]
    button_destroy = [create_button(style=ButtonStyle.red, label="Cancel")]
    action_row = [create_actionrow(*button_yes, *button_maybe, *button_destroy)]
    await msg.send(embed=act.to_embed(), components=action_row)
    while 1:
        inter = await wait_for_component(myBot, components=action_row)
        if inter.component['label'] == 'Register':
            act.add_player(inter.author.name, 'Register')
        if inter.component['label'] == 'Maybe':
            act.add_player(inter.author.name, 'Maybe')
        if inter.component['label'] == 'Cancel':
            if inter.author.id == act.author_id or inter.author.guild_permissions.administrator:
                await inter.edit_origin(content="")
                await inter.origin_message.delete()
            else:
                await inter.send('You cannot do that', hidden=True)
        else:
            await inter.edit_origin(embed=act.to_embed(), components=action_row)


async def loadout(msg: SlashContext, bungie_name: str):
    """

    @param msg: Slash command message send by the user
    @param bungie_name: parameter of the slash command, correspond to a bungie name (has the format name#number)
    @return:
    """

    await msg.defer()
    me = server_application.me
    if time.time() > me.token['refresh_expires']:
        print("REFRESH CODE EXPIRE ONE YEAR AS PASSED")
    if time.time() > me.token['access_expires']:
        api_requests.refresh_token()
    p = class_json.player(bungie_name)

    weapons, armors, others = get_inventory(p)
    inventory = class_json.PlayerEquipment(p, weapons, armors, others)
    embs = []
    for weapon in weapons:
        emb = discord.Embed(title="test", url="https://example.org/")
        emb.add_field(value=weapon.shader, name="shader")
        emb.set_image(url=f"{icon_root}{weapon.icon}")
        embs.append(emb)

    embs2 = []
    for armor in armors:
        emb = discord.Embed(title="test", url="https://example.org/")
        emb.add_field(value=armor.shader, name="shader")
        emb.set_image(url=f"{icon_root}{armor.icon}")
        embs2.append(emb)

    await msg.send(embeds=embs)
    await msg.send(embeds=embs2)
