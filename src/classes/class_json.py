# Definitions of all classes to deserialize json response

# imports
import discord

# from imports
from enum import Enum


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
        disp_header = "<" + self.__class__.__name__ + " instance>\n\n"
        disp_vendor_hash = ".vendor_hash: " + str(self.vendor_hash) + "\n"
        disp_url = ".url: " + str(self.url) + "\n"
        disp_msg = ".message: " + str(self.message) + "\n"
        disp_status = ".status: " + str(self.status) + "\n"
        disp_error_code = ".error_code: " + str(self.error_code) + "\n"
        disp_error_status = ".error_status: " + str(self.error_status) + "\n"
        disp_exception = ".exception: " + str(self.exception) + "\n"
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
        disp_membership_id = ".membership_id: " + str(self.membership_ids) + "\n"

        disp_url = ".url: " + str(self.url) + "\n"
        disp_msg = ".message: " + str(self.message) + "\n"
        disp_status = ".status: " + str(self.status) + "\n"
        disp_error_code = ".error_code: " + str(self.error_code) + "\n"
        disp_error_status = ".error_status: " + str(self.error_status) + "\n"
        disp_exception = ".exception: " + str(self.exception) + "\n"
        return disp_header + disp_name + disp_name_code + disp_membership_types + disp_membership_id + disp_url + \
               disp_msg + disp_status + disp_error_code + disp_error_status + disp_exception


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
