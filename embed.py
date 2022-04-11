import datetime

import discord


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
    # embed.set_author(name='Banshee', url=icon_url, icon_url=icon_url)
    embed.add_field(name="<:weapon:963081886295547915> __Weapons__", value=weapons, inline=True)
    embed.add_field(name="<:empty_socket:963080068362551306> __Mods__ ", value=mods, inline=True)
    today = datetime.datetime.now()
    date = today.strftime("%d/%m/%Y")
    embed.set_footer(text=date)

    return embed
