# Discord-Bot
Discord bot in Python
Every secret token or just some usefull data is in data.py (not in this repository for obvious reasons).
-> contains API key, discord application token, Destiny 2 API root, every membership_id, membership_type and character_id of my bungie account, a global variable to stock the current authorization token.

## V 1.0
- Launch server in localhost:8000 (still have to launch it manually and be connected to a bungie account).
- Get the manifest and create 2 dictionary (one for DestinyInventoryItemDefinition (every item in the game) and DestinyVendorDefinition (every vendor in the game) to be able to parse data about those entities when receiving requests.
- /banshee command: return every weapons and mods that Banshee-44 (Gunsmith) is currently selling.
