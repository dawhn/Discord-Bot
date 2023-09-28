from poe.classes.poe_class import Profile, Character, Stash

import http.client
import json

conn = http.client.HTTPSConnection("api.pathofexile.com")


def get_league(oauth_token: str):
    payload = ""
    headers = {
        'Authorization': f"Bearer {oauth_token}"
    }

    conn.request("GET", "/leagues", payload, headers)
    res = conn.getresponse()
    response = json.loads(res.read().decode("utf-8"))
    for league in response:
        if "Standard" not in league["id"] and "Hardcore" not in league["id"] and "Solo Self-Found" not in league["id"] and "Ruthless" not in league["id"]:
            return league["id"]
    return "Standard"


def get_profile(oauth_token: str, league: str):
    payload = ""
    headers = {
        'Authorization': f"Bearer {oauth_token}"
    }

    conn.request("GET", "/profile", payload, headers)
    res = conn.getresponse()
    prof = json.loads(res.read().decode("utf-8"))
    return Profile(prof, league)


def get_detail_character(oauth_token: str, char_name):
    payload = ""
    headers = {
        'Authorization': f"Bearer {oauth_token}"
    }

    conn.request("GET", f"/character/{char_name}", payload, headers)
    res = conn.getresponse()
    character_detail = json.loads(res.read().decode("utf-8"))
    return Character(character_detail["character"])


def get_character(oauth_token: str, profile: Profile):
    payload = ""
    headers = {
        'Authorization': f"Bearer {oauth_token}"
    }

    all_names = []

    conn.request("GET", "/character", payload, headers)
    res = conn.getresponse()
    characters = json.loads(res.read().decode("utf-8"))
    print(characters)
    for character in characters["characters"]:
        char_name = character["name"]
        char_league = character["league"]
        if char_league == profile.current_league:
            all_names.append(char_name)
            char = get_detail_character(oauth_token, char_name)
            profile.add_character(char)
    profile.character_names = all_names


def get_detail_stash(oauth_token: str, league: str, stash: Stash):
    payload = ""
    headers = {
        'Authorization': f"Bearer {oauth_token}"
    }

    conn.request("GET", f"/stash/{league}/{stash.id}", payload, headers)
    res = conn.getresponse()
    stash_detail = json.loads(res.read().decode("utf-8"))
    stash.details = stash_detail


def get_stash(oauth_token: str, league: str, profile: Profile):
    payload = ""
    headers = {
        'Authorization': f"Bearer {oauth_token}"
    }

    conn.request("GET", f"/stash/{league}", payload, headers)
    res = conn.getresponse()
    stashes = json.loads(res.read().decode("utf-8"))
    for stash in stashes["stashes"]:
        stash = Stash(stash)
        get_detail_stash(oauth_token, league, stash)
        profile.add_stash(stash)

    with open(f"profile.json", "w") as f:
        json.dump(profile, f, indent=4, default=lambda x: x.__dict__)

