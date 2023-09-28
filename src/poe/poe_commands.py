import json

from discord_slash import SlashContext

from data import poe_profile
from poe.classes import embed


async def character(ctx: SlashContext, character_name: str):
    """
    Get the information's of a character
    :param ctx: The context of the command
    :param character_name: The name of the character
    :return: A message with the information's of the character
    """

    await ctx.defer()
    char = poe_profile.get_character(character_name)
    if not char:
        await ctx.send("Character not found")
        return

    await ctx.send(f"Character found: {char.name}\n```\n{char}\n```")


async def equipment(ctx: SlashContext, character_name: str):
    """"
    Get the equipment of a character
    :param ctx: The context of the command
    :param character_name: The name of the character
    :return: A message with the equipment of the character
    """

    await ctx.defer()
    char = poe_profile.get_character(character_name)
    if not char:
        await ctx.send("Character not found")
        return

    i = 0
    embeds = embed.equiped_embed(char.equipment)
    for emb in embeds:
        await ctx.send(embed=emb)


