# File containing every functions that are necessary to create every needed embed for the bot

# imports
import datetime
import discord

# from file imports
from api import perks_data, images
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
    legendary_weapons = []
    exotic_weapons = []
    legendary_armor = []
    exotic_armor = []
    for item in items:
        if item[1] == 3:
            if item[2] == 6:
                exotic_weapons.append(f"> - {item[0]}\n")
            if item[2] == 5:
                legendary_weapons.append(f"> - {item[0]}\n")
        if item[1] == 2:
            if item[2] == 6:
                exotic_armor.append(f"> - {item[0]}\n")
            if item[2] == 5:
                legendary_armor.append(f"> - {item[0]}\n")
    embed.add_field(name="<:exotic_weapon:963119052019077180> __Exotic Weapons__", value=''.join(exotic_weapons),
                    inline=True)
    embed.add_field(name="<:exotic_armor:963113323501584384> __Exotic Armors__", value=''.join(exotic_armor),
                    inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="<:legendary_weapon:963081886295547915> __Legendary Weapons__",
                    value=''.join(legendary_weapons), inline=True)
    embed.add_field(name="<:legendary_armor:963113337384738826> __Legendary Armors__", value=''.join(legendary_armor),
                    inline=True)
    embed.set_footer(text="Dawhn#5398",
                     icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

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
    legendary_weapons = []
    exotic_weapons = []
    exotic_armor = []

    # For each weapon (exotic and legendary), parse their type and perks
    # Add both these elements and their corresponding emoji to wether exotic or legendary weapon field
    for item in items_perks:
        if item[len(item) - 2] == 3:
            if item[len(item) - 1] == 6:
                exotic_weapons.append(f"> - **{item[1]}**\n")
                exotic_weapons.append(f"> - {item[2]}\n")
                exotic_weapons.append(f"> ")
                for i in range(3, len(item) - 2):
                    for perk_name in all_perks:
                        if perk_name == item[i]:
                            exotic_weapons.append(f"{all_perks[perk_name]} ")
                exotic_weapons.append("\n\n\n")
            if item[len(item) - 1] == 5:
                legendary_weapons.append(f"> - **{item[1]}**\n")
                legendary_weapons.append(f"> - **{item[3]} {item[2]}**\n")
                legendary_weapons.append("> ")
                for i in range(3, len(item) - 2):
                    for perk_name in all_perks:
                        if perk_name == item[i]:
                            legendary_weapons.append(f"{all_perks[perk_name]} ")
                legendary_weapons.append("\n\n")

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
                        exotic_armor.append(f"> - **{item[0]}**\n")
                        exotic_armor.append(f"> {perks_data.all_perks[max_[0]]} {str(max_[1])}")
                        exotic_armor.append(f" | {perks_data.all_perks[max2[0]]} {str(max2[1])}")
                exotic_armor.append("\n\n")

    # Add the exotic armor slot to the exotic weapons field to make it inline with the legendary weapons
    exotic_weapons.append("<:exotic_armor:963113323501584384> __**Exotic Armors**__\n")
    exotic_weapons.extend(exotic_armor)

    embed.add_field(name="<:exotic_weapon:963119052019077180> __Exotic Weapons__", value=''.join(exotic_weapons),
                    inline=True)
    embed.add_field(name="<:legendary_weapon:963081886295547915> __Legendary Weapons__",
                    value=''.join(legendary_weapons), inline=True)
    embed.add_field(name="Xur's destination:", value=name_destinations[index], inline=False)
    embed.set_footer(text="Dawhn#5398",
                     icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

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
    weapons = []
    mods = []
    for item in items:
        if item[1] == 3:
            weapons.append(f"> - {item[0]}\n")
        else:
            mods.append(f"> - {item[0]}\n")
    embed.add_field(name="<:weapon:963081886295547915> __Weapons__", value=''.join(weapons), inline=True)
    embed.add_field(name="<:empty_socket:963080068362551306> __Mods__ ", value=''.join(mods), inline=True)
    embed.set_footer(text="Dawhn#5398",
                     icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

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
    weapons = []
    for item in items:
        weapons.append(f"> - {item[1]}\n")
        weapons.append(f"> {str(item[3])} {str(item[2])}\n")
        weapons.append("> ")
        for i in range(3, len(item)):
            for perk_name in all_perks:
                if perk_name == item[i]:
                    weapons.append(f"{all_perks[perk_name]} ")
            # weapons += item[i] + " "
        weapons += '\n\n'
    embed.add_field(name="<:weapon:963081886295547915> __Weapons__", value=''.join(weapons), inline=True)
    embed.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    return embed


def raid_stats_embed(raid: [], bungie_name: str):
    """
    Create and return an embed about the player's raid clears
    :param raid: list of raids alongside their number of clear
    :param bungie_name: the bungie name of a player
    :return: an embed containing every raid that the player has done with its number of clear
    """

    name = []
    count = []
    for activity in raid:
        name.append(f"> {activity[0]}\n")
        count.append(f"> {str(activity[1])}\n")
    embed = discord.Embed(
        title=f"**{bungie_name}**",
        description=f"Summary of {bungie_name}'s raid",
        color=discord.Color.dark_purple()
    )
    embed.add_field(name="__Raid__", value=''.join(name))
    embed.add_field(name="__Clears__", value=''.join(count))
    embed.set_image(url='https://media.discordapp.net/attachments/963544576193355837/964988469296369694/unknown.png')
    embed.set_footer(text="Dawhn#5398",
                     icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    return embed


def dungeon_stats_embed(dungeon: [], bungie_name: str):
    """
    Create and return an embed about the player's raid clears
    :param dungeon: list of dungeons alongside their number of clear
    :param bungie_name: the bungie name of a player
    :return: an embed containing every dungeon that the player has done with its number of clear
    """

    name = []
    count = []
    for activity in dungeon:
        name.append(f"> {activity[0]}\n")
        count.append(f"{str(activity[1])}\n")

    embed = discord.Embed(
        title=f"**{bungie_name}**",
        description=f"Summary of {bungie_name}'s raid",
        color=discord.Color.blurple()
    )
    embed.add_field(name="__Dungeon__", value=''.join(name))
    embed.add_field(name="__Clears__", value=''.join(count))
    embed.set_image(url='https://media.discordapp.net/attachments/963544576193355837/964988469296369694/unknown.png')
    embed.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    return embed


def gm_stats_embed(gm: [], bungie_name: str):
    """
    Create and return an embed about the player's raid clears
    :param gm: list of grandmaster nightfalls alongside their number of clear
    :param bungie_name: the bungie name of a player
    :return: an embed containing every grandmaster nightfall that the player has done with its number of clear
    """

    name = []
    count = []
    for activity in gm:
        type_, name_ = activity[0].split(':')
        name.append(f"> {name_}\n")
        count.append(f"{str(activity[1])}\n")

    embed = discord.Embed(
        title=f"**{bungie_name}**",
        descritpion=f"Summary of {bungie_name}'s Grandmaster Nightfalls",
        color=discord.Color.dark_blue()
    )

    embed.add_field(name="__Grandmaster__", value=''.join(name))
    embed.add_field(name="__Clears__", value=''.join(count))
    embed.set_image(url="https://media.discordapp.net/attachments/963544576193355837/967190183512518666/unknown.png"
                        "?width=1189&height=600")
    embed.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")
    return embed


def weekly_embed(weekly):
    nf_embed = discord.Embed(
        title=f"Weekly rotating Nightfall:\n\n**__{weekly.nf}__**",
        color=discord.Color.dark_blue()
    )
    nf_embed.set_thumbnail(url="https://media.discordapp.net/attachments/963544576193355837/974334243952025700/unknown.png")
    if weekly.double_rewards is not None:
        nf_embed.add_field(name="Double Nightfall rewards", value="All Nightfall loot drops are doubled.")
    nf_embed.set_image(url=images.strikes[weekly.nf])
    if weekly.boost:
        val = ""
        for i in weekly.boost:
            if "Double Vanguard Rank" in i:
                val = i
        if val != "":
            nf_embed.add_field(name=val, value="\u200b")
    nf_embed.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    raid_embed = discord.Embed(
        title="**__Weekly raid challenges__**",
        color=discord.Color.light_grey()
    )
    raid_embed.set_thumbnail(url="https://media.discordapp.net/attachments/963544576193355837/974334633175023656/unknown.png")
    raid_embed.set_image(url="https://media.discordapp.net/attachments/963544576193355837/964988469296369694/unknown.png?width=1117&height=571")
    count = 0
    for name, challenges in weekly.challenges.items():
        value = []
        if challenges:
            for challenge in challenges:
                value += f"{challenge[0]}\n"
            if count == 2:
                raid_embed.add_field(name="\u200b", value="\u200b", inline=False)
                raid_embed.add_field(name=name, value=''.join(value))
            else:
                raid_embed.add_field(name=name, value=''.join(value))
        count += 1
    raid_embed.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    detailed_raids = []
    for name, challenges in weekly.challenges.items():
        str_chall = []
        for challenge in challenges:
            str_chall.append(f"{challenge[0]} ({challenge[1]}): {challenge[2]}")
        emb = discord.Embed(
            title=f"**__Weekly {name} challenges__**",
            color=discord.Color.light_grey(),
            description="\n".join(str_chall)
        )
        emb.set_thumbnail(url="https://media.discordapp.net/attachments/963544576193355837/974334633175023656/unknown.png")
        emb.set_image(url="https://media.discordapp.net/attachments/963544576193355837/964988469296369694/unknown.png?width=1117&height=571")
        emb.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")
        detailed_raids.append(emb)

    hunt_embed = discord.Embed(
        title="Weekly rotating empire hunt:\n**__" + weekly.empire_hunt + "__**\n ",
        color=discord.Color.dark_blue()
    )
    hunt_embed.set_thumbnail(url="https://media.discordapp.net/attachments/963544576193355837/974335301994577940/unknown.png")
    val = []
    for hunt in weekly.nightmares_hunt:
        val.append(f"{hunt}\n")
    hunt_embed.add_field(name="Weekly rotating Nightmare Hunts:", value=''.join(val))
    hunt_embed.set_image(url=images.empire_hunt[f"Empire Hunt: {weekly.empire_hunt}"])
    hunt_embed.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    campaign_embed = discord.Embed(
        title=f"Weekly rotating campaign mission:\n\nThe Witch Queen: **__{weekly.lf_mission}__**\nLightfall: **__{weekly.wq_mission}__**",
        color=discord.Color.green()
    )

    campaign_embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/963544576193355837/974335270084300962/unknown.png")
    campaign_embed.set_image(url=images.lf_campaign[weekly.lf_mission])
    campaign_embed.set_footer(text="Dawhn#5398",
                        icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    pvp_embed = discord.Embed(
        title=f"Weekly rotating PvP mode:\n**__{weekly.pvp_modes[0]}__**",
        color=discord.Color.red()
    )
    if weekly.boost:
        val = ""
        for i in weekly.boost:
            if "Double Crucible Rank" in i:
                val = i
        if val != "":
            pvp_embed.add_field(name=val, value="\u200b", inline=False)

    pvp_embed.set_thumbnail(url="https://media.discordapp.net/attachments/963544576193355837/974334493458563140/unknown.png")
    for elem in weekly.pvp_modes:
        if elem == 'Iron Banner':
            pvp_embed.add_field(name="Iron Banner", value="This week is Iron Banner, no Trials of Osiris this weekend !", inline=False)
        else:
            pvp_embed.add_field(name=elem, value="\u200b", inline=False)
    pvp_embed.set_image(url="https://media.discordapp.net/attachments/963544576193355837/974339110791680001/unknown.png?width=1117&height=559")
    pvp_embed.set_footer(text="Dawhn#5398", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    return nf_embed, raid_embed, hunt_embed, campaign_embed, pvp_embed, detailed_raids


def automatic_weekly_embed(weekly):
    today = datetime.date.today()
    month = today.strftime("%b")
    day_b = today.strftime("%d")
    end = datetime.date.today() + datetime.timedelta(days=7)
    day_e = end.strftime("%d")
    embed = discord.Embed(
        title="**Weekly Reset**",
        description=f"{month} {day_b} - {day_e}"
    )

    if weekly.boost:
        val = ""
        for i in weekly.boost:
            if "Double Nightfall Rewards" in i:
                val = i
        if val != "":
            embed.add_field(name=val, value="\u200b")
    # if len(stats[3]) > 1:
    #     embed.add_field(name="Iron Banner", value="This week is Iron Banner, no Trials of Osiris this weekend !")

    embed.add_field(name="__**Weekly Nightfall**__", value=weekly.nf)

    raid_ = []
    for raid in weekly.challenges:
        raid_.append(f"{raid[1]}: {raid[0]}\n")
    embed.add_field(name="__**Weekly Raid challenges**__", value=''.join(raid_), inline=False)

    hunt_ = []
    for hunt in weekly.nightmares_hunt:
        hunt_.append(f"{hunt}\n")
    hunt_.append(f"Empire Hunt: {weekly.empire_hunt}")
    embed.add_field(name="__**Weekly Hunts**__", value=''.join(hunt_))

    embed.add_field(name="__**Weekly Witch Queen campaign**__", value=weekly.wq_mission)

    embed.add_field(name="__**Weekly PVP mode**__", value=" ".join(weekly.pvp_modes))
    embed.set_footer(text="**Dawhn#5398**", icon_url="https://media.discordapp.net/attachments/963544576193355837/977572811612774440/unknown.png")

    return embed
