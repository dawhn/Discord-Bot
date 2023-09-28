# imports
from enum import Enum


class WqMission(Enum):
    ARRIVAL = "The Arrival"
    INVESTIGATION = "The Investigation"
    GHOSTS = "The Ghosts"
    COMMUNION = "The Communion"
    MIRROR = "The Mirror"
    CUNNING = "The Cunning"
    LAST_CHANCE = "The Last Chance"
    RITUAL = "The Ritual"

    def __str__(self):
        return self.value


class LfMission(Enum):
    FIRST_CONTACT = "First Contact"
    UNDER_SIEGE = "Under Siege"
    DOWNFALL = "Downfall"
    BREAKNECK = "Breakneck"
    ON_THE_VERGE = "On the Verge"
    NO_TIME_LEFT = "No Time Left"
    HEADLONG = "Headlong"
    DESPERATE_MEASURES = "Desperate Measures"

    def __str__(self):
        return self.value


class WeeklyEmbed:

    def __init__(self, empire_hunt: str, nightmares_hunt: list, wq_mission: str, lf_mission: str):
        self.empire_hunt = empire_hunt
        self.nightmares_hunt = nightmares_hunt
        self.wq_mission = wq_mission
        self.lf_mission = lf_mission
        self.boost = []
        self.challenges = None
        self.nf = None
        self.double_rewards = None
        self.pvp_modes = None

    def __str__(self):
        return f"Weekly:"\
               f"Empire Hunt: {self.empire_hunt}\n" \
               f"Nightmares Hunt: {self.nightmares_hunt}\n" \
               f"WQ Mission: {self.wq_mission}\n" \
               f"LF Mission: {self.lf_mission}\n" \
               f"Boost: {self.boost}\n" \
               f"Challenges: {self.challenges}\n" \
               f"NF: {self.nf}\n" \
               f"Double Rewards: {self.double_rewards}\n" \
               f"PVP Modes: {self.pvp_modes}"
