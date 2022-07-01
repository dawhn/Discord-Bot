# Discord-Bot
Project: Discord bot in Python 

Every secret token or just some usefull data is in data.py (not in this repository for obvious reasons).  
-> contains API key, discord application token, Destiny 2 API root, every membership_id, membership_type and character_id of my bungie account, a global variable to stock the current authorization token.

## V 1.0
- Launch server in localhost:8000 (still have to launch it manually and be connected to a bungie account).
- Get the manifest and create 2 dictionary (one for DestinyInventoryItemDefinition (every item in the game) and DestinyVendorDefinition (every vendor in the game) to be able to parse data about those entities when receiving requests.
- /banshee command: return every weapon and mods that Banshee-44 (Gunsmith) is currently selling.
- /xur command: return every weapon and armors that Xur is currently selling.

### V 1.1
- Added buttons on /banshee and /xur to switch from general view to detailed view (and vice-versa) about the vendor's sales.
- /banshee: Added perks name for each item sold by banshee in the detailed window.

### V 1.2
- /xur: added items details (now show all weapons main perks and exotic armor first and second highests stat aswell as xur current location, reflected by the picture and the text in the bottom).
- Added emoji corresponding to each perk and stat (not complete) and replace perks name by their emoji on /banshee to make it clearer for the reader.
- /stats command: return number of clear for each raid done by one account (only works with my account for now).

### V 1.3
- /stats: added select button to chose between Raids, Dungeons and Grandmaster Nightfalls for the requested account.
- Added refresh_url root to the local server. Which allow to retrieve the access token without requiring to get the authorization code again. It is checked automatically when calling an API endpoint.
- Now only have to authorize the application once. When it is done, access_token and refresh_token with both their expiration date are stored in data.csv which can on the next launch of the bot be retrieved and keep on working without needing to authorize the application again.

### V 1.4
- Added selection of default channel for each guild (server). On launch or on server join, the bot will ask for a channel tag by a user (can be anyone for now) and save that id in a .csv to be able to retreive it later to send automatic message.
- Send an automatic message on all servers containing Xur's information at its reset (Friday at 7PM CEST)
- Send an automatic message on all servers containing Banshee-44's information at its reset (Tuesday at 7PM CEST)

### V 1.5
- Fixed when a server is already joined but no default channel has been sent (ask again for a channel and add it to the existing csv).
- /weekly command: return useful information about weekly reset (weekly Nightfall, weekly raid challenges, weekly hunts, weekly Witch queen campaign mission, weekly pvp gamemode and weekly rank boost).
- This command returns an embed that has many buttons to switch view between all possible information and when on the raid view has a select menu to chose details about a specific raid.
- Removed /banshee information on weekly reset on Tuesday and added /weekly information instead.
- Delayed automatic information on Tuesday / Friday reset from 19:00 to 19:02 CEST in order to make sure the update on the API has been concluded
- Changed from 19:02 CEST to 17:02 UTC to make it easier for different timezone

### V 1.6
- Added /activity command, allow to create an activity amongst different activity types.
- Can personnalized many aspect of the activity to matcht the author's willing.
- Anyone can Register by clicking the register button and remove itself from the registration by clicking again on the Register button
- Same goes for the Maybe button
- Only the activity's author or an admin can delete the activity, anyone else will receive a hidden message telling them they cannot.
- Changed automatic weekly to not have any buttons (in order to allow anyone to have the information they are looking for)
- Begined changed to create a backend server as well as a fronted in JavaScript which will allow to create a cleaner representation of the data.