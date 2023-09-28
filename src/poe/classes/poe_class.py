
class Profile:
    def __init__(self, response, league):
        for key in response:
            setattr(self, key, response[key])

        self.characters = []
        self.character_names = []
        self.stashes = []
        self.current_league = league

    def add_character(self, character):
        self.characters.append(character)

    def add_stash(self, stash):
        self.stashes.append(stash)

    def get_character(self, name):
        for character in self.characters:
            if character.name == name:
                return character
        return None


class Character:
    def __init__(self, response):
        self.name = response["name"]
        self.league = response["league"]
        self.class_ = response["class"]
        self.level = response["level"]
        # self.pantheon_major = response["pantheon_major"]
        # self.pantheon_minor = response["pantheon_minor"]
        # self.bandit_choice = response["bandit_choice"]

        self.equipment = Equipment(response["equipment"])
        self.inventory = Inventory(response["inventory"])

    def __str__(self):
        return "Class: " + str(self.class_) + "\nLevel: " + str(self.level)


class Equipment:
    def __init__(self, response):
        self.items = []
        for item in response:
            self.items.append(Item(item))


class Inventory:
    def __init__(self, response):
        self.items = []
        for item in response:
            self.items.append(Item(item))


class Item:
    def __init__(self, response):
        self.influences = response["influences"] if "influences" in response else None
        self.name = response["name"]
        self.baseType = response["baseType"]
        self.itemLvl = response["ilvl"]
        self.icon = response["icon"]
        self.implicitMods = response["implicitMods"] if "implicitMods" in response else None
        self.explicitMods = response["explicitMods"] if "explicitMods" in response else None
        self.craftedMods = response["craftedMods"] if "craftedMods" in response else None
        self.enchantMods = response["enchantMods"] if "enchantMods" in response else None
        self.corrupt = response["corrupted"] if "corrupted" in response else None
        self.flavourText = response["flavourText"] if "flavourText" in response else None

    def __str__(self):
        return str(self.name) + "\n" + "\n" + str(self.baseType) + "\n" + str(self.itemLvl) + \
            "\nImplicit: " + str(self.implicitMods) + "\nExplicit: " + str(self.explicitMods) + "\nCrafted: " +  \
            str(self.craftedMods) + "\nEnchant: " + str(self.craftedMods) + "\nCorrupt: " + str(self.corrupt) + "\n" + \
            str(self.flavourText)


class Passives:
    def __init__(self, response):
        for key in response:
            setattr(self, key, response[key])


class Stash:
    def __init__(self, response):
        for key in response:
            setattr(self, key, response[key])
        self.details = {}