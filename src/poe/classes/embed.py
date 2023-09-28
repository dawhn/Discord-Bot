import discord

from poe.classes.poe_class import Equipment, Item


def equiped_embed(items: Equipment):
    embeds = []
    for item in items.items:
        embed = discord.Embed(
            title=item.name,
            description=item.baseType,
            color=discord.Color.dark_gold())

        embed.set_image(url=item.icon)
        if item.implicitMods:
            for implicit in item.implicitMods:
                embed.add_field(name="Implicit", value=implicit)
        if item.explicitMods:
            for explicit in item.explicitMods:
                embed.add_field(name="Explicit", value=explicit)

        embeds.append(embed)

    return embeds
