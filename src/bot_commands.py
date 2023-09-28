from discord_slash.utils.manage_commands import create_option, create_choice

import data
from discord_slash import SlashCommand, SlashContext

import destiny.destiny_commands as destiny_commands
import poe.poe_commands as poe_commands

slash = SlashCommand(data.myBot, sync_commands=True)


@slash.slash(name="Banshee",
             description="Get Banshee's sales inventory")
async def banshee(msg: SlashContext):
    await destiny_commands.banshee(msg)


@slash.slash(name="Xur",
             description="Get Xur's sales inventory")
async def xur(msg: SlashContext):
    await destiny_commands.xur(msg)


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
    await destiny_commands.stats(msg, bungie_name)


@slash.slash(name="Weekly",
             description="Information about this week")
async def weekly(msg: SlashContext):
    await destiny_commands.weekly(msg)


@slash.slash(name="Activity",
             description="Get player stats",
             options=[
                 create_option(
                     name="activity_type",
                     description="Which type of activity (Raid, PVE, PVP, Gambit)",
                     required=True,
                     option_type=3,
                     choices=[
                         create_choice(name="Raid", value="Raid"),
                         create_choice(name="PVE", value="PVE"),
                         create_choice(name="PVP", value="PVP"),
                         create_choice(name="Gambit", value="Gambit")
                     ]
                 ),
                 create_option(
                     name="name",
                     description="Name of your activity",
                     required=True,
                     option_type=3
                 ),
                 create_option(
                     name="description",
                     description="Description of your activity",
                     required=True,
                     option_type=3
                 ),
                 create_option(
                     name="schedule",
                     description="Schedule of your activity",
                     required=True,
                     option_type=3
                 )
             ])
async def activity(msg: SlashContext, activity_type: str, name: str, description: str, schedule: str):
    await destiny_commands.activity(msg, activity_type, name, description, schedule)


@slash.slash(name="Loadout",
             description="Get player loadout",
             options=[
                 create_option(
                     name="bungie_name",
                     description="Bungie name of the player",
                     required=True,
                     option_type=3
                 )
             ])
async def loadout(msg: SlashContext, bungie_name: str):
    await destiny_commands.loadout(msg, bungie_name)


@slash.slash(name="Character",
             description="Get your character's information's in the current league",
             options=[
                 create_option(
                     name="character_name",
                     description="The name of the character",
                     required=True,
                     option_type=3,
                     choices=[
                         create_choice(name="Dawhnts", value="Dawhnts")
                     ]
                 )
             ])
async def character(ctx: SlashContext, character_name: str):
    await poe_commands.character(ctx, character_name)


@slash.slash(name="Equipment",
             description="Get your character's equipment in the current league",
             options=[
                create_option(
                    name="character_name",
                    description="The name of the character",
                    required=True,
                    option_type=3,
                    choices=[
                        create_choice(name="Dawhnts", value="Dawhnts")
                    ]
                )
             ])
async def equipment(ctx: SlashContext, character_name: str):
    await poe_commands.equipment(ctx, character_name)
