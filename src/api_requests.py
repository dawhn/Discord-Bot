# File containing every functions that are necessary to make API requests
import json
# imports
import time
import requests

# file imports
import embed
import server_application

# from file imports
from data import my_api_key, root, icon_root
from discord_features import check_xur
from manifest import vendor_dic, item_dic, location_dic, perk_dic, activity_dic, activity_modifier_dic
from api.perks_data import DestinyItemSubType, DestinyChallenges
from classes.class_embed import WeeklyEmbed, WqMission, LfMission
from classes.class_json import ActivityHash

access_token = 'Bearer '


def refresh_token():
    """
    Send a request to the server to refresh the access_token of the application
    """

    requests.get('https://127.0.0.1:8000/refresh_url', verify=False)


def sales_vendor(name: str):
    """
    Build 2 embed about the vendor, one containing general information, the other containing detailed informatio
    - First one is general with overall information about the vendor sales
    - Second is more specific and detailed with item perks, item stats and location
    @param name: name of the vendor
    @return: 2 embed one general, the other detailed
    """

    if name == 'Xûr':
        if not check_xur():
            print('wtf')
            return None
    me = server_application.me
    if time.time() > me.token['access_expires']:
        refresh_token()
    vendor_hash, large_icon, original_icon, destinations = get_vendor(name)
    if time.time() > me.token['access_expires']:
        print('refresh')
        refresh_token()

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[2]) + '/Vendors/' + str(vendor_hash) + '/?components=402'

    r = requests.get(path, headers=header)
    resp = r.json()
    if resp['ErrorCode'] != 1 or resp['ErrorStatus'] != 'Success':
        return None

    item_list = []
    items_number = []
    for item in resp['Response']['sales']['data'].items():
        for key in item:
            if type(key) != str:
                item_list.append((key['itemHash'], key['vendorItemIndex']))

    item_dictionary = item_dic()
    items = []

    for item in item_dictionary['DestinyInventoryItemDefinition']:
        for item_l in item_list:
            if item['hash'] == item_l[0] and (item['itemType'] == 3 or item['itemType'] == 26 or item['itemType'] == 2):
                if item['itemType'] == 3:
                    sub_type = item['itemSubType']
                    type_name = ''
                    for name_, type_id in DestinyItemSubType.items():
                        if sub_type == type_id:
                            type_name = name_
                    items_number.append((item['displayProperties']['name'], item_l[1], type_name))
                i = (item['displayProperties']['name'], item['itemType'], item['inventory']['tierType'], item_l[1])
                items.append(i)

    details = get_details(vendor_hash, original_icon, destinations, name, items, items_number)
    if name == 'Banshee-44':
        return embed.gunsmith_embed(items, large_icon, original_icon), details
    if name == 'Xûr':
        return embed.xur_embed(items, large_icon, original_icon), details


def get_details(vendor_hash, original_icon: str, destinations: [], name: str, items: [], items_number: [()]):
    """
    Get detailed information about a vendor
    @param vendor_hash: hash of the vendor
    @param original_icon: the original icon of the vendor
    @param destinations: all the possible destination of the vendor
    @param name: the name of the vendor
    @param items: list of items sold by the vendor (weapons, armors or mods with their item type)
    @param items_number: list of items sold by the vendor (only weapons and armors and contains the item archetype)
    @return: an embed message containing detailed information about the vendor
    """

    items_perks = get_items_perks(vendor_hash, items_number)
    destination, index = get_destination(vendor_hash, destinations)
    if name == 'Banshee-44':
        return embed.gunsmith_detail_embed(items_perks, original_icon)
    if name == 'Xûr':
        stats_ = get_all_stats(vendor_hash, items)
        return embed.xur_detail_embed(items, index, items_perks, stats_)


def get_items_perks(vendor_hash: str, items: [()]):
    """
    Get all perks for each item sold by the vendor
    @param vendor_hash: hash of the vendor
    @param items: list of all items sold by the vendor
    @return: a list containing all items with their respective perks sold by the vendor
    """

    me = server_application.me
    perk_dictionary = perk_dic()

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}
    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[2]) + '/Vendors/' + str(vendor_hash) + '/?components=302'
    r = requests.get(path, headers=header)
    resp = r.json()
    if resp['ErrorCode'] != 1 or resp['ErrorStatus'] != 'Success':
        return None
    perks = resp['Response']['itemComponents']['perks']['data'].items()

    items_perks = []
    for item in items:
        items_perks.append([item[1], item[0], item[2]])

    for perk in perks:
        i = 0
        curr = -1
        for item in items_perks:
            if str(item[0]) == perk[0]:
                curr = i
            i += 1
        if curr == -1:
            continue
        for perk_ in perk[1]['perks']:
            perk_hash = perk_['perkHash']
            for hash_perk, item in perk_dictionary['DestinySandBoxPerkDefinition'].items():
                if hash_perk == perk_hash:
                    if 'name' in item['displayProperties']:
                        items_perks[curr].append(item['displayProperties']['name'])

    return items_perks


def get_all_stats(vendor_hash: str, items: []):
    """
    Get all stats for each armor sold by the vendor
    @param vendor_hash: hash of the vendor
    @param items: list of all items sold by the vendor
    @return: a list of all items sold with their respective stats sold by the vendor
    """

    me = server_application.me
    perk_dictionary = perk_dic()
    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[2]) + '/Vendors/' + str(vendor_hash) + '/?components=304'

    r = requests.get(path, headers=header)
    resp = r.json()
    if resp['ErrorCode'] != 1 or resp['ErrorStatus'] != 'Success':
        return None
    stats_ = resp['Response']['itemComponents']['stats']['data'].items()

    all_stats = []

    for stat in stats_:
        curr_stats = []
        found = False
        stop = False
        for hash_stat in stat[1]['stats']:
            for stat_hash, item_stat in perk_dictionary['DestinyStatDefinition'].items():
                if stat_hash == int(hash_stat):
                    name = item_stat['displayProperties']['name']
                    if name == 'Mobility' or name == 'Resilience' or name == 'Recovery' or name == 'Discipline' or \
                            name == 'Intellect' or name == 'Strength':
                        if not found:
                            item_name = ""
                            item_rarity = 0
                            for item in items:
                                if item[3] == int(stat[0]):
                                    item_name = item[0]
                                    item_rarity = item[2]
                            if item_rarity != 6:
                                stop = True
                            if not stop:
                                curr_stats.append(item_name)
                            found = True
                        if not stop:
                            if found and curr_stats[0] != '':
                                curr_stats.append(
                                    (item_stat['displayProperties']['name'], stat[1]['stats'][hash_stat]['value']))
        if found and not stop:
            all_stats.append(curr_stats)
    return all_stats


def get_destination(vendor_hash: str, destinations: []):
    """
    Get the current location of the vendor
    @param vendor_hash: hash of the vendor to look for
    @param destinations: all the possible destinations of the vendor
    @return: the destination and the index of the destination in the list of all possible destinations
    """

    me = server_application.me

    header = {"X-API-Key": my_api_key,
              "Authorization": access_token + me.token['access_token']}

    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[2]) + '/Vendors/' + str(vendor_hash) + '/?components=400'

    r = requests.get(path, headers=header)
    resp = r.json()
    if resp['ErrorCode'] != 1 or resp['ErrorStatus'] != 'Success':
        return None

    location_index = resp['Response']['vendor']['data']['vendorLocationIndex']

    location_dictionary = location_dic()
    actual_dest = destinations[location_index]

    for destination_hash, destination in location_dictionary['DestinyDestinationDefinition'].items():
        if actual_dest == destination_hash:
            return destination, location_index


def get_vendor(name: str):
    """
    Get general information about a vendor
    @param name: name of the vendor
    @return: the vendor hash, its icon, its original icon, its detinations
    """

    data = vendor_dic()
    vendor_hash = None
    large_icon_url = ''
    original_icon_url = ''
    destinations = []
    for vendor, data_ in data['DestinyVendorDefinition'].items():
        if name == data_['displayProperties']['name']:
            vendor_hash = vendor
            if 'displayProperties' in data_:
                large_icon_url = icon_root + data_['displayProperties']['largeIcon']
                if 'mapIcon' in data_['displayProperties']:
                    original_icon_url = icon_root + data_['displayProperties']['mapIcon']
            if 'locations' in data_:
                for location in data_['locations']:
                    destinations.append(location['destinationHash'])
            if name == 'Xûr':
                break
    return vendor_hash, large_icon_url, original_icon_url, destinations


def get_weekly_activities(headers: dict):
    """
    Get the dictionary of activities based on activities
    @param headers: headers of the request
    @return: the dictionary of activities
    """

    me = server_application.me
    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[2]) + '/?components=204'
    r = requests.get(path, headers=headers)
    resp = r.json()
    if resp['ErrorCode'] != 1 or resp['ErrorStatus'] != 'Success':
        return None

    if 'activities' not in resp['Response']:
        return None

    activity_dictionary = activity_dic()
    name_activities = []

    for activity_hash in resp['Response']['activities']['data']['availableActivities']:
        hash = activity_hash['activityHash']

        for act_hash, activity_def in activity_dictionary['DestinyActivityDefinition'].items():
            if act_hash == hash:
                name_activities.append(activity_def['displayProperties']['name'])
    return resp, name_activities


def get_weekly_nf(activities: dict):
    """
    Get this week's Nightfall
    @param activities: dictionary containing all activities available
    @return: Nightfall name
    """

    activity_dictionary = activity_dic()
    act = None
    found = False
    for activity in activities['Response']['activities']['data']['availableActivities']:
        if 'recommendedLight' in activity:
            if activity['recommendedLight'] == 1840:
                for activity_hash, activity_def in activity_dictionary['DestinyActivityDefinition'].items():
                    if found:
                        break
                    if activity_hash == activity['activityHash'] and 'Nightfall' in activity_def['displayProperties']['name']:
                        act = activity_def
                        found = True
        if found:
            break
    return act['displayProperties']['description']


def get_weekly_challenges(activities: dict):
    """
    Get this week's raid challenges
    @param activities: dictionary containing all activities available
    @return: raid name, challenge name and challenge description
    """

    modifiers_vow = []
    modifiers_vog = []
    modifiers_gos = []
    modifiers_dsc = []
    modifiers_kf = []
    modifiers_ron = []
    activity_mod_dic = activity_modifier_dic()

    for activity in activities['Response']['activities']['data']['availableActivities']:
        match activity['activityHash']:
            case ActivityHash.vow_hash:
                modifiers_vow = activity['modifierHashes']
            case ActivityHash.vog_hash:
                modifiers_vog = activity['modifierHashes']
            case ActivityHash.gos_hash:
                modifiers_gos = activity['modifierHashes']
            case ActivityHash.dsc_hash:
                modifiers_dsc = activity['modifierHashes']
            case ActivityHash.kf_hash:
                modifiers_kf = activity['modifierHashes']
            case ActivityHash.ron_hash:
                modifiers_ron = activity['modifierHashes']
            case _:
                pass

    modifiers = [modifiers_vow, modifiers_vog, modifiers_gos, modifiers_dsc, modifiers_kf, modifiers_ron]
    raids = ["Vow of the disciple", "Vault of glass", "Garden of salvation", "Deep stone crypt", "King's Fall", "Root of Nightmares"]

    res = {}

    for i in range(len(modifiers)):
        challenges = []
        for modifier in modifiers[i]:
            for mod_hash, mod in activity_mod_dic['DestinyActivityModifierDefinition'].items():
                mod_name = mod['displayProperties']['name'][:9] if mod['displayProperties']['name'][10:] == 'Challenge' else mod['displayProperties']['name']
                if modifier == mod_hash and mod_name in DestinyChallenges:
                    challenge = [mod_name]
                    challenge.extend(DestinyChallenges[mod_name])
                    challenges.append(challenge)
        res[raids[i]] = challenges
    return res


def get_weekly_hunts(activities: dict):
    """
    Get this week's Empire and Nightmare hunts
    @param activities: dictionary containing all activities available
    @return: name of all available hunts
    """

    activity_dictionary = activity_dic()
    rotate = []
    for activity in activities['Response']['activities']['data']['availableActivities']:
        if 'recommendedLight' in activity:
            if activity['recommendedLight'] == 1840:
                for activity_hash, activity_def in activity_dictionary['DestinyActivityDefinition'].items():
                    if activity['activityHash'] == activity_hash:
                        name = activity_def['displayProperties']['name']
                        if 'Vow' not in name and 'Vault' not in name and 'Vox' not in name and 'Wellspring' not in name\
                                and 'Nightfall' not in name and 'Grasp' not in name:
                            name = activity_def['displayProperties']['name']
                            if 'Master' in name:
                                test = name.split(':')
                                name = ':'.join(test[0:len(test) - 1])
                            rotate.append(name)
    return rotate


def get_weekly_progression(headers: dict):
    """
    Get the dictionary of activities based on progression
    @param headers: headers of the request
    @return: the dictionary of activities
    """

    me = server_application.me
    path = root + str(me.membership_types[0]) + '/Profile/' + str(me.membership_ids[0]) + '/Character/' + str(
        me.character_ids[2]) + '/?components=202'
    r = requests.get(path, headers=headers)
    resp = r.json()
    if resp['ErrorCode'] != 1 or resp['ErrorStatus'] != 'Success':
        return None

    return resp


def get_rank_boost(activities: dict):
    """
    Get this week's rank boost
    @param activities: dictionary containing all activities available
    @return: the name of the boost and "Double Nightfall Drops" if it is active
    """

    boost = []
    double_rewards = ""
    for activity in activities['Response']['activities']['data']['availableActivities']:
        if 'modifierHashes' in activity:
            for modifier in activity['modifierHashes']:
                if modifier == 3874605433 and "Double Crucible Rank" not in boost:
                    boost.append("Double Crucible Rank")
                if modifier == 745014575 and "Double Vanguard Rank" not in boost:
                    boost.append("Double Vanguard Rank")
                if modifier == 3228023383 and "Double Gambit Rank" not in boost:
                    boost.append("Double Gambit Rank")
                if modifier == 1171597537:
                    double_rewards = "Double Nightfall Drops"
    return boost, double_rewards


def check_pvp_mode(hash_: str):
    """
    Check if the current has is a usual pvp gamemode
    @param hash_: the hash to test
    @return: True: is not a common gamemode, False otherwise
    """

    if hash_ == 1717505396 or hash_ == 1957660400 or hash_ == 1957660400 or hash_ == 1683791010 or hash_ == 3283279668 or hash_ == 2259621230:
        return False
    return True


def check_banner(activities: dict):
    """
    Check if the current hash is iron banner
    @param activities: the list of activities to check
    @return: True: is Iron Banner, False otherwise
    """

    if '4111516205' in activities['Response']['progressions']['data']['milestones']:
        return True
    return False


def get_weekly_pvp_mode(activities_name: dict):
    """
    Get this week's pvp mode
    @param activities_name: list containing all names of available activities
    @return: names of all pvp modes available
    """
    pvp_modes = []
    if "Momentum Control" in activities_name:
        pvp_modes.append("Momentum Control")
    if "Iron Banner" in activities_name:
        pvp_modes.append("Iron Banner")
    if "Mayhem" in activities_name:
        pvp_modes.append("Mayhem")
    if "Showdown" in activities_name:
        pvp_modes.append("Showdown")
    if "Trials of Osiris" in activities_name:
        pvp_modes.append("Trials of Osiris")
    if "Team Scorched" in activities_name:
        pvp_modes.append("Team Scorched")

    return pvp_modes


def get_weekly():
    """
    Get this week information
    @return: a list of embed containing nightfall, raid challenges, hunts, pvp mode, rank boost and double rewards
    """

    me = server_application.me
    headers = {"X-API-Key": my_api_key,
               "Authorization": access_token + me.token['access_token']}

    activities, name_activities = get_weekly_activities(headers)

    # Hunts
    empire_hunts: list = []
    nightmare_hunts: list = []
    for activity in name_activities:
        if "Empire Hunt" in activity and activity.split(": ")[1] not in empire_hunts:
            empire_hunts.append(activity.split(": ")[1])
        if "Nightmare Hunt" in activity and activity.split(": ")[1] not in nightmare_hunts:
            nightmare_hunts.append(activity.split(": ")[1])

    # Campaign missions
    lf_mission = [name.split(":")[0] for name in name_activities if "Master" in name and name.split(":")[0] in LfMission._value2member_map_][0]
    wq_mission = [name.split(":")[0] for name in name_activities if "Master" in name and name.split(":")[0] in WqMission._value2member_map_][0]

    weekly = WeeklyEmbed(empire_hunt=empire_hunts[0], nightmares_hunt=nightmare_hunts, wq_mission=wq_mission, lf_mission=lf_mission)

    # Nightfall
    nf = get_weekly_nf(activities)

    # Challenges
    challenges = get_weekly_challenges(activities)

    # Rank boost / Double rewards
    boost, double_rewards = get_rank_boost(activities)

    # PvP mode

    weekly.nf = nf
    weekly.challenges = challenges
    weekly.boost = boost
    weekly.double_rewards = double_rewards

    pvp_modes = get_weekly_pvp_mode(name_activities)
    weekly.pvp_modes = pvp_modes

    return embed.weekly_embed(weekly), embed.automatic_weekly_embed(weekly)
