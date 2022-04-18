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
- /xur: added items details (now show all weapons main perks and exotic armor first and second hight stat aswell as xur current location, reflected by the picture and the text in the bottom).
- Added emoji corresponding to each perk and stat (not complete) and replace perks name by their emoji on /banshee to make it clearer for the reader.
- /stats command: return number of clear for each raid done by one account (only works with my account for now).