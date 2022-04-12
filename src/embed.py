import datetime

import discord


def xur_embed(items: [()], icon_url: str, original_icon_url: str):
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
    embed.add_field(name="<:legendary_weapon:963081886295547915> __Legendary Weapons__", value=legendary_weapons, inline=True)
    embed.add_field(name="<:legendary_armor:963113337384738826> __Legendary Armors__", value=legendary_weapons, inline=True)
    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed


def gunsmith_embed(items: [()], icon_url: str, original_icon_url: str):
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
