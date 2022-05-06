# File containing every functions that are necessary to create every needed embed for the bot

# imports
import datetime
import discord

# from file imports
from api import perks_data
from api.perks_data import all_perks

tower_jpg = 'https://cdn.discordapp.com/attachments/963544576193355837/963546618475479060/tower.jpg'
nessus_jpg = 'https://cdn.discordapp.com/attachments/963544576193355837/963546607725461534/nessus.jpg'
edz_jpg = 'https://cdn.discordapp.com/attachments/963544576193355837/963546597134835812/edz.jpg'
image_destinations = [tower_jpg, edz_jpg, nessus_jpg]  # change order matching xur's order
name_destinations = ['The Tower, Hangar', 'EDZ, Winding Cove', 'Nessus, Watcher\'s Grave']


def xur_embed(items: [()], icon_url: str, original_icon_url: str):
    """
    Create and return an embed about xur
    :param items: list of weapons and armors sold by xur
    :param icon_url: url of xur's icon
    :param original_icon_url: url of xur's original icon
    :return: an embed containing general information about xur
    """

    embed = discord.Embed(
        title="Xûr",
        description="This week's item sold by Xûr",
        color=discord.Color.dark_gray()
    )
    embed.set_image(url=icon_url)
    embed.set_thumbnail(url=original_icon_url)
    legendary_weapons = ""
    exotic_weapons = ""
    legendary_armor = ""
    exotic_armor = ""
    for item in items:
        if item[1] == 3:
            if item[2] == 6:
                exotic_weapons += '> - ' + item[0] + '\n'
            if item[2] == 5:
                legendary_weapons += '> - ' + item[0] + '\n'
        if item[1] == 2:
            if item[2] == 6:
                exotic_armor += '> - ' + item[0] + '\n'
            if item[2] == 5:
                legendary_armor += '> - ' + item[0] + '\n'
    embed.add_field(name="<:exotic_weapon:963119052019077180> __Exotic Weapons__", value=exotic_weapons, inline=True)
    embed.add_field(name="<:exotic_armor:963113323501584384> __Exotic Armors__", value=exotic_armor, inline=True)
    embed.add_field(name="➖➖➖➖➖➖➖➖➖➖", value="➖➖➖➖➖➖➖➖➖➖", inline=False)
    embed.add_field(name="<:legendary_weapon:963081886295547915> __Legendary Weapons__", value=legendary_weapons,
                    inline=True)
    embed.add_field(name="<:legendary_armor:963113337384738826> __Legendary Armors__", value=legendary_armor,
                    inline=True)
    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed


def xur_detail_embed(items: [()], index: int, items_perks: [()], stats: [()]):
    """
    Create and return an embed about xur's detailed sold
    :param items: list of exotic weapons, exotic armors and legendary weapons sold by xur
    :param index: index of the current location of xur (0 = tower, 1 = edz, 2 = nessus)
    :param items_perks: list of perks of each weapon sold by xur
    :param stats: list of stats of each armor sold by xur
    :return: an embed containing detailed information about xur
    """

    embed = discord.Embed(
        title="Xûr",
        description="This week's item sold by Xûr with perks",
        color=discord.Color.dark_gray()
    )
    for item in items:
        for perk_item in items_perks:
            if item[0] == perk_item[1]:
                perk_item.append(item[1])
                perk_item.append(item[2])
    embed.set_image(url=image_destinations[index])
    legendary_weapons = ""
    exotic_weapons = ""
    exotic_armor = ""

    # For each weapon (exotic and legendary), parse their type and perks
    # Add both these elements and their corresponding emoji to wether exotic or legendary weapon field
    for item in items_perks:
        if item[len(item) - 2] == 3:
            if item[len(item) - 1] == 6:
                exotic_weapons += '> - **' + item[1] + '**\n'
                exotic_weapons += '> ' + item[2] + '\n'
                exotic_weapons += '> '
                for i in range(3, len(item) - 2):
                    for perk_name in all_perks:
                        if perk_name == item[i]:
                            exotic_weapons += all_perks[perk_name] + " "
                exotic_weapons += '\n\n\n'
            if item[len(item) - 1] == 5:
                legendary_weapons += '> - **' + item[1] + '**\n'
                legendary_weapons += '> ' + item[3] + ' ' + item[2] + '\n'
                legendary_weapons += '> '
                for i in range(3, len(item) - 2):
                    for perk_name in all_perks:
                        if perk_name == item[i]:
                            legendary_weapons += all_perks[perk_name] + " "
                legendary_weapons += '\n\n'

    # Parse every exotic armor and check for the 2 biggest value.
    # Add both these value and their corresponding emoji to the exotic_armor field
    for item in items:
        if item[1] == 2:
            if item[2] == 6:
                for stat_item in stats:
                    if stat_item[0] == item[0]:
                        max_ = None
                        max2 = None
                        for i in range(1, len(stat_item)):
                            if not max_:
                                max_ = stat_item[i]
                            if not max2 and stat_item[i][1] < max_[1]:
                                max2 = stat_item[i]
                            if stat_item[i][1] >= max_[1]:
                                max2 = max_
                                max_ = stat_item[i]
                            elif stat_item[i][1] > max2[1]:
                                max2 = stat_item[i]
                        exotic_armor += '> - **' + item[0] + '**\n'
                        exotic_armor += '> ' + perks_data.all_perks[max_[0]] + ' ' + str(max_[1])
                        exotic_armor += ' | ' + perks_data.all_perks[max2[0]] + ' ' + str(max2[1])
                exotic_armor += '\n\n'

    # Add the exotic armor slot to the exotic weapons field to make it inline with the legendary weapons
    exotic_weapons += "<:exotic_armor:963113323501584384> __**Exotic Armors**__\n"
    exotic_weapons += exotic_armor

    embed.add_field(name="<:exotic_weapon:963119052019077180> __Exotic Weapons__", value=exotic_weapons, inline=True)
    embed.add_field(name="<:legendary_weapon:963081886295547915> __Legendary Weapons__", value=legendary_weapons,
                    inline=True)
    footer = 'Xur is at ' + name_destinations[index]
    embed.set_footer(text=footer)

    return embed


def gunsmith_embed(items: [()], icon_url: str, original_icon_url: str):
    """
    Create and return an embed about banshee-44
    :param items: list of weapons and mods sold by banshee-44
    :param icon_url: url of banshee-44's icon
    :param original_icon_url: url of banshee-44's original icon
    :return: an embed containing general information about banshee-44
    """

    embed = discord.Embed(
        title="Banshee-44",
        description="Today's item sold by Banshee-44",
        color=discord.Color.light_gray()
    )
    # banshee's picture url
    embed.set_image(url=icon_url)
    embed.set_thumbnail(url=original_icon_url)
    weapons = ""
    mods = ""
    for item in items:
        if item[1] == 3:
            weapons += '> - ' + item[0] + '\n'
        else:
            mods += '> - ' + item[0] + '\n'
    embed.add_field(name="<:weapon:963081886295547915> __Weapons__", value=weapons, inline=True)
    embed.add_field(name="<:empty_socket:963080068362551306> __Mods__ ", value=mods, inline=True)
    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed


def gunsmith_detail_embed(items: [()], original_icon_url):
    """
    Create and return an embed about banshee-44's detailed sold
    :param items: list of weapons alongside their perks sold by banshee-44
    :param original_icon_url: url of banshee-44's original icon
    :return: an embed containing detailed information about banshee-44
    """

    embed = discord.Embed(
        title="Banshee-44",
        description="Today's items sold by Banshee-44 with perks",
        color=discord.Color.light_gray()
    )
    embed.set_image(url=tower_jpg)
    embed.set_thumbnail(url=original_icon_url)
    weapons = ""
    for item in items:
        weapons += '> - ' + item[1] + '\n'
        weapons += '> ' + str(item[3]) + ' ' + str(item[2]) + '\n'
        weapons += '> '
        for i in range(3, len(item)):
            for perk_name in all_perks:
                if perk_name == item[i]:
                    weapons += all_perks[perk_name] + " "
            # weapons += item[i] + " "
        weapons += '\n\n'
    embed.add_field(name="<:weapon:963081886295547915> __Weapons__", value=weapons, inline=True)
    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed


def raid_stats_embed(raid: [], bungie_name: str):
    """
    Create and return an embed about the player's raid clears
    :param raid: list of raids alongside their number of clear
    :param bungie_name: the bungie name of a player
    :return: an embed containing every raid that the player has done with its number of clear
    """

    name = ""
    count = ""
    for activity in raid:
        name += '> ' + activity[0] + '\n'
        count += str(activity[1]) + '\n'
    name_, id_ = bungie_name.split('#')
    embed = discord.Embed(
        title="**" + bungie_name + "**",
        description="Summary of " + name_ + "'s raid",
        color=discord.Color.dark_purple()
    )
    embed.add_field(name="__Raid__", value=name)
    embed.add_field(name="__Clears__", value=count)
    embed.set_image(url='https://media.discordapp.net/attachments/963544576193355837/964988469296369694/unknown.png')

    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed


def dungeon_stats_embed(dungeon: [], bungie_name: str):
    """
    Create and return an embed about the player's raid clears
    :param dungeon: list of dungeons alongside their number of clear
    :param bungie_name: the bungie name of a player
    :return: an embed containing every dungeon that the player has done with its number of clear
    """

    name = ""
    count = ""
    for activity in dungeon:
        name += '> ' + activity[0] + '\n'
        count += str(activity[1]) + '\n'

    name_, id_ = bungie_name.split('#')
    embed = discord.Embed(
        title="**" + bungie_name + "**",
        description="Summary of " + name_ + "'s raid",
        color=discord.Color.blurple()
    )
    embed.add_field(name="__Dungeon__", value=name)
    embed.add_field(name="__Clears__", value=count)
    embed.set_image(url='https://media.discordapp.net/attachments/963544576193355837/964988469296369694/unknown.png')

    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed


def gm_stats_embed(gm: [], bungie_name: str):
    """
    Create and return an embed about the player's raid clears
    :param gm: list of grandmaster nightfalls alongside their number of clear
    :param bungie_name: the bungie name of a player
    :return: an embed containing every grandmaster nightfall that the player has done with its number of clear
    """

    name = ""
    count = ""
    for activity in gm:
        type_, name_ = activity[0].split(':')
        name += '> ' + name_ + '\n'
        count += str(activity[1]) + '\n'

    name_, _ = bungie_name.split('#')
    embed = discord.Embed(
        title="**" + bungie_name + "**",
        descritpion="Summary of " + name_ + "'s Grandmaster Nightfalls",
        color=discord.Color.dark_blue()
    )

    embed.add_field(name="__Grandmaster__", value=name)
    embed.add_field(name="__Clears__", value=count)
    embed.set_image(url="https://media.discordapp.net/attachments/963544576193355837/967190183512518666/unknown.png"
                        "?width=1189&height=600")

    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed
