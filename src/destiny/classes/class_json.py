# Definitions of all classes to deserialize json response

# imports
import re
from typing import Optional

import discord
import requests
import src.destiny.embed as embed

# from imports
from enum import Enum

from src.destiny import server_application
from src.data import root, my_api_key

access_token = "Bearer "


class Vendors:
    """
    Build a classes Vendor from a response to a requesy
    """

    def __init__(self, response):
        self.status = response.status_code
        self.url = response.url
        self.error_code = None
        self.error_status = None
        self.message = None
        self.data = None
        self.vendor_hash = None
        self.exception = None
        if self.status == 200:
            res = response.json()
            self.error_code = res['ErrorCode']
            self.error_status = res['ErrorStatus']
            self.message = res['Message']
            if self.error_code == 1:
                try:
                    self.data = res['Response']
                    self.vendor_hash = res['Response']['vendors']['data']
                except Exception as ex:
                    print("Vendors classes: 200 status and error_code 1 but there were no res['Response']")
                    print("Exception: {0}.\nType: {1}".format(ex, ex.__class__.__name__))
                    self.exception = ex.__class__.__name__
            else:
                print("No data returned for url: {0} with error code: {1}", self.url, self.error_code)
        else:
            print("Request failed for url: {0} with status: {1}", self.url, self.status)

    def __repr__(self):
        disp_header = f"<{self.__class__.__name__} instance>\n\n"
        disp_vendor_hash = f".vendor_hash: {str(self.vendor_hash)}\n"
        disp_url = f".url: {str(self.url)}\n"
        disp_msg = f".message: {str(self.message)}\n"
        disp_status = f".status: {str(self.status)}\n"
        disp_error_code = f".error_code: {str(self.error_code)}\n"
        disp_error_status = f".error_status: {str(self.error_status)}\n"
        disp_exception = f".exception: {str(self.exception)}\n"
        return disp_header + disp_vendor_hash + disp_url + disp_msg + disp_status + disp_error_code + disp_error_status + \
               disp_exception


class Player:
    """
    Build a class player from a response to a request
    """

    status = 0

    def __init__(self, response):
        self.status = response.status_code
        self.url = response.url
        self.error_code = None
        self.error_status = None
        self.message = None
        self.exception = None
        self.characters_ids = []
        self.membership_id = None
        self.membership_type = None

        # Data about the user
        self.name = None
        self.name_code = None
        self.membership_types = []
        self.membership_ids = []
        if self.status == 200:
            res = response.json()
            self.error_code = res['ErrorCode']
            self.error_status = res['ErrorStatus']
            self.message = res['Message']
            if self.error_code == 1:
                try:
                    self.name = res['Response'][0]['bungieGlobalDisplayName']
                    self.name_code = res['Response'][0]['bungieGlobalDisplayNameCode']
                    for item in res['Response']:
                        self.membership_ids.insert(0, item['membershipId'])
                    for item in res['Response'][0]['applicableMembershipTypes']:
                        self.membership_types.insert(0, item)
                    self.membership_types = res['Response'][0]['applicableMembershipTypes']
                except Exception as ex:
                    print("Player 200 status and error_code 1 but no data to retrieve for fields")
                    print("Exception: {0}.\nType: {1}".format(ex, ex.__class__.__name__))
                    self.exception = ex.__class__.__name__
            else:
                print("No data returned for url: {0} with error code: {1}", self.url, self.error_code)
                self.exception = "Wrong error code"
        else:
            print("Request failed for url: {0} with status: {1}", self.url, self.status)
            self.exception = "Wrong status code"

    def __repr__(self):
        disp_header = "<" + self.__class__.__name__ + " instance>\n\n"
        disp_name = ".name: " + str(self.name) + "\n"
        disp_name_code = ".name_code: " + str(self.name_code) + "\n"
        disp_membership_types = ".membership_types: "
        if self.membership_types:
            for member in self.membership_types:
                disp_membership_types += str(member) + " "
        disp_membership_types += "\n"
        disp_membership_id = ".membership_ids: " + str(self.membership_ids) + "\n"

        disp_url = ".url: " + str(self.url) + "\n"
        disp_msg = ".message: " + str(self.message) + "\n"
        disp_status = ".status: " + str(self.status) + "\n"
        disp_error_code = ".error_code: " + str(self.error_code) + "\n"
        disp_error_status = ".error_status: " + str(self.error_status) + "\n"
        disp_exception = ".exception: " + str(self.exception) + "\n"
        return disp_header + disp_name + disp_name_code + disp_membership_types + disp_membership_id + disp_url + \
               disp_msg + disp_status + disp_error_code + disp_error_status + disp_exception


def player(bungie_name: str) -> Optional[Player]:
    """
    Get player data by searching the player with its bungie name
    @param bungie_name: bungie name of the player
    @return: an object Player
    """

    if not re.match('^[\w]*#[0-9]{4}$', bungie_name):
        print("No match")
        # raise WrongBungieNameError
    me = server_application.me
    server_application.get_stored_informations(me)
    data = bungie_name.split("#")
    url = f"{root}SearchDestinyPlayerByBungieName/all/"
    # url = root + 'SearchDestinyPlayerByBungieName/' + 'all' + '/'
    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    body = {"displayName": data[0], "displayNameCode": data[1]}
    response = requests.post(url, headers=header, json=body)
    p = Player(response)
    if p.status != 200 or p.error_code != 1 or p.exception is not None:
        return None
    resp = None
    for i in range(len(p.membership_ids)):
        url_char = f"{root}{str(p.membership_types[i])}/Profile/{str(p.membership_ids[i])}/?components=200"
        # url_char = root + str(p.membership_types[i]) + '/Profile/' + str(p.membership_ids[i]) + '/?components=200'
        r = requests.get(url_char, headers=header)
        resp = r.json()
        if 'Response' in resp:
            p.membership_id = p.membership_ids[i]
            p.membership_type = p.membership_types[i]
            break
    if resp is not None:
        for char_id, char in resp['Response']['characters']['data'].items():
            p.characters_ids.append(char_id)
    return p


def get_all_deleted_char(p: Player):
    """
    Get all the deleted characters (which might hold some adat about the player's activity history) and add them to the
    characters_ids attribute of the parameter p
    @param p: the current player of classes Player
    """

    me = server_application.me
    server_application.get_stored_informations(me)
    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    # player_char_url = root + str(p.membership_type) + '/Account/' + str(p.membership_id) + '/Stats/?groups=0'
    player_char_url = f"{root}{str(p.membership_type)}/Account/{str(p.membership_id)}/Stats/?groups=0"
    r = requests.get(url=player_char_url, headers=header)
    resp = r.json()
    for character in resp['Response']['characters']:
        if character['deleted']:
            p.characters_ids.append(character['characterId'])


class ActivityType(Enum):
    RAID = 0,
    PVE = 1,
    PVP = 2,
    GAMBIT = 3,
    UNDEFINED = 4


def parse_type(s: str):
    if s == "Raid":
        return ActivityType.RAID
    if s == "PVE":
        return ActivityType.PVE
    if s == "PVP":
        return ActivityType.PVP
    if s == "Gambit":
        return ActivityType.GAMBIT


class Activity:
    """
    Build a class activity
    """

    def __init__(self, name: str, desc: str, schedule: str, type_: str, author: str, id):
        self.name = name
        self.desc = desc
        self.schedule = schedule
        self.type_ = parse_type(type_)
        self.author = author
        self.accepted = [author]
        self.maybe = []
        self.author_id = id

    def activity_image(self):
        if self.type_ == ActivityType.RAID:
            return "https://media.discordapp.net/attachments/965358071914332253/974771059712725092/Raid.png"
        if self.type_ == ActivityType.PVE:
            return "https://media.discordapp.net/attachments/965358071914332253/974771014519099452/f2154b781b36b19760efcb23695c66fe.png"
        if self.type_ == ActivityType.PVP:
            return "https://media.discordapp.net/attachments/965358071914332253/974771015081148536/cc8e6eea2300a1e27832d52e9453a227.png"
        if self.type_ == ActivityType.GAMBIT:
            return "https://media.discordapp.net/attachments/965358071914332253/974771014774968370/fc31e8ede7cc15908d6e2dfac25d78ff.png"

    def activity_color(self):
        if self.type_ == ActivityType.RAID:
            return discord.Color.light_gray()
        if self.type_ == ActivityType.PVE:
            return discord.Color.blue()
        if self.type_ == ActivityType.PVP:
            return discord.Color.red()
        if self.type_ == ActivityType.GAMBIT:
            return discord.Color.green()

    def add_player(self, name: str, type_: str):
        if name in self.accepted:
            self.accepted.remove(name)
        elif type_ == "Register":
            self.accepted.append(name)
        if name in self.maybe:
            self.maybe.remove(name)
        elif type_ == "Maybe":
            self.maybe.append(name)

    def to_embed(self):
        embed = discord.Embed(
            title="**" + self.name + "**",
            description=self.desc,
            color=self.activity_color()
        )
        accepted = ""
        maybe = ""
        if len(self.accepted) == 0:
            accepted = '\u200b'
        else:
            for player in self.accepted:
                accepted += "> " + player + "\n"
        if len(self.maybe) == 0:
            maybe = '\u200b'
        else:
            for player in self.maybe:
                maybe += "> " + player + "\n"
        embed.set_thumbnail(url=self.activity_image())
        embed.add_field(name="**Schedule:**", value=self.schedule, inline=False)
        embed.add_field(name="**Registered:**", value=accepted)
        embed.add_field(name="**Maybe:**", value=maybe)
        embed.set_footer(text="Request made by " + self.author)

        return embed


class ActivityStats:
    """
    Build a class regrouping stats of a player activities
    """

    def __init__(self, p: Player, raid_data, dungeon_data, gm_data):
        self.player = p
        self.raid_data = raid_data
        self.dungeon_data = dungeon_data
        self.gm_data = gm_data
        self.dungeon_data.sort()
        self.raid_data.sort()
        self.raid_embed = embed.raid_stats_embed(self.raid_data, p.name)
        self.dungeon_embed = embed.dungeon_stats_embed(self.dungeon_data, p.name)
        self.gm_embed = embed.gm_stats_embed(self.gm_data, p.name)
        self.data_embed = [self.raid_embed, self.dungeon_embed, self.gm_embed]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.player.name}>"


class PlayerEquipment:
    """
    Build a class regrouping weapons and armors of a player
    """

    def __init__(self, p: Player, weapons, armors, others):
        self.player = p
        self.weapons = weapons
        self.armors = armors
        self.mods = others


class Weapon:
    """
    Build a class representating a Destiny 2 weapon
    """

    def __init__(self, name: str, icon: str):
        self.perk_1 = None
        self.perk_2 = None
        self.shader = None
        self.mod = None
        self.name = name
        self.icon = icon
        self.perks = []

    def __repr__(self):
        return f"<Weapon {self.name}>"


class Armor:
    """
    Build a class representating a Destiny 2 armor
    """

    def __init__(self, name: str, icon: str):
        self.shader = None
        self.perks = []
        self.name = name
        self.icon = icon

    def __repr__(self):
        return f"<Armor {self.name}>"


class Perk:
    """
    Build a class representating a Destiny 2 perk
    """

    def __init__(self, name: str, icon: str = "", description: str = ""):
        self.name = name
        self.icon = icon
        self.description = description

    def __repr__(self):
        return f"<Perk {self.name}: {self.description}>"


class ActivityHash:
    vow_hash = 1441982566
    vog_hash = 3881495763
    gos_hash = 2497200493
    dsc_hash = 910380154
    kf_hash = 1374392663
    ron_hash = 1191701339
