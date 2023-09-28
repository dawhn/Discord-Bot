import json
from data import client_secret, client_id
from poe.api_requests import get_league, get_profile, get_stash, get_character
import http.client
import data


def get_oauth_token() -> str:
    conn = http.client.HTTPSConnection("www.pathofexile.com")

    payload = f"\n\t\"client_id\": \"{client_id}\",\n\t" \
              f"\"client_secret\": \"{client_secret}\",\n\t" \
              "\"grant_type\": \"client_credentials\",\n\t" \
              "\"scope\": \"account:profile account:stashes account:characters account:league_accounts " \
              "service:leagues service:leagues:ladder service:psapi\"\n "

    payload = "{" + payload + "}"

    headers = {
        'Content-Type': "application/json"
    }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    return json.loads(res.read().decode("utf-8"))['access_token']


def setup_profile():
    poe_token = get_oauth_token()
    league = get_league(poe_token)
    data.poe_profile = get_profile(poe_token, league)
    data.poe_names = [x.name for x in data.poe_profile.character_names]
    get_character(poe_token, data.poe_profile)
    get_stash(poe_token, league, data.poe_profile)


setup_profile()
