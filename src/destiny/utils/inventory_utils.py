from destiny.classes.class_json import Weapon, Armor, Player, Perk
from src.data import root, my_api_key
from src.destiny.manifest import item_dic

import src.destiny.server_application as server_application
import requests

access_token = "Bearer "


def get_inventory(p: Player):
    """Request player's inventory and get its weapons / armors / others

    @param p: the current player of the class Player
    @return:
    """

    me = server_application.me
    header = {"X-API-KEY": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    item_dict = item_dic()
    for char_id in p.characters_ids:
        char_path = f"{root}{str(p.membership_type)}/Profile/{str(p.membership_id)}/Character/{char_id}/?components=200,205,305,302"
        r = requests.get(char_path, headers=header)
        resp = r.json()

        weapons = []
        armors = []
        others = []

        if resp['ErrorCode'] == 1:
            for equipment in resp['Response']['equipment']['data']['items']:
                eq = [item['displayProperties'] for item
                      in item_dict['DestinyInventoryItemDefinition']
                      if item['hash'] == equipment['itemHash']]
                eq = eq[0]
                if len(weapons) < 3:
                    weapons.append(Weapon(eq['name'], eq['icon']))
                elif len(armors) < 5:
                    armors.append(Armor(eq["name"], eq["icon"]))
                else:
                    others.extend(eq)

            for i, (plug, list_plugs) in enumerate(resp['Response']['itemComponents']['sockets']['data'].items()):
                print(f"new item: {plug}")
                if i < 3:
                    curr_item = weapons[i]
                elif i < 8:
                    curr_item = armors[i - 3]
                else:
                    break

                for item_perk in list_plugs['sockets']:
                    if 'plugHash' not in item_perk:
                        continue
                    print(item_perk['plugHash'])

                    curr = next((obj for obj in item_dict['DestinyInventoryItemDefinition'] if
                                 obj['hash'] == item_perk['plugHash']), None)
                    try:
                        perk = Perk(curr['displayProperties']['name'], curr['displayProperties']['icon'],
                                    curr['displayProperties']['description'])
                        if "Tracker" in perk.name or "Masterwork" in perk.name or "Upgrade" in perk.name:
                            continue
                        if perk.description and "shader" in perk.description or "Shader" in perk.name:
                            curr_item.shader = perk
                        elif perk.description and ("ornament" in perk.description or "Ornament" in perk.name):
                            curr_item.ornament = perk
                        elif curr["itemTypeDisplayName"] == "Weapon Mod" or "Catalyst" in perk.name or "Mod" in perk.name:
                            curr_item.mod = perk
                        else:
                            curr_item.perks.append(perk)
                    except KeyError as exception:
                        pass

            return weapons, armors, others
