# File containing dictionaries about:
# - emoji and their corresponding name
# - Weapon type and their corrsponding number

all_perks = {
    "Mobility": "<:Mobility:965645304798011454>",
    "Resilience": "<:Resilience:965645305175478342>",
    "Recovery": "<:Recovery:965645441461022741>",
    "Discipline": "<:Discipline:965645305682997258>",
    "Intellect": "<:Intellect:965645305032876163>",
    "Strength": "<:Strength:965645305100001291>",
    "Unrelenting": "<:Unrelenting:963817505703473262>",
    "Killing Wind": "<:KillingWind:963817505548296222>",
    "Multikill Clip": "<:Multikillclip:963817505128857693>",
    "Under Pressure": "<:UnderPressure:963817505674129409>",
    "Frenzy": "<:Frenzy:963817505149845576> ",
    "Thresh": "<:Thresh:963817505615392859>",
    "Surrounded": "<:Surrounded:963817505611219064>",
    "Adrenaline Junkie": "<:AdrenalineJunkie:963817452637159464>",
    "Subsistence": "<:Subsistance:963817505581834280>",
    "Slideshot": "<:Slideshot:963817505581838436>",
    "Demolitionist": "<:Demolitionist:963817505162424431>",
    "Ambitious Assassin": "<:AmbitiousAssassin:965342322353139735>",
    "Quickdraw": "<:Quickdraw:965342322340532245>",
    "Feeding Frenzy": "<:FeedingFrenzy:965342322592206909>",
    "Whirlwind Blade": "<:WhirlwindBlade:965342322575429652>",
    "Explosive Light": "<:ExplosiveLight:965342322617384960>",
    "Omolon Fluid Dynamics": "<:OmolonFluidDynamics:965342322596401152>",
    "Auto-Loading Holster": "<:AutoLoadingHolster:965342322575425586>",
    "Hakke Breach Armaments": "<:HakkeBreachArmaments:965342322571214938>",
    "Lead from Gold": "<:LeadfromGold:965342322705440908>",
    "One-Two Punch": "<:OneTwoPunch:965342322592202772>",
    "Hip-Fire Grip": "<:HipFireGrip:965358334666485784>",
    "Wire Rifle": "<:WireRifle:965358207608447116>",
    "Swashbuckler": "<:Swashbuckler:965357951130931341>",
    "Blinding Grenades": "<:BlindingGrenades:965357951105761340>",
    "Wellspring": "<:Wellspring:965357951240007700>",
    "Zen Moment": "<:ZenMoment:965357951168688158>",
    "Rangefinder": "<:Rangefinder:965357951168708679>",
    "Paracausal Shot": "<:ParacausalShot:965357951114162187>",
    "Kill Clip": "<:KillClip:965357951130943488>",
    "Tracking Module": "<:TrackingModule:965357951202263140>",
    "Vorpal Weapon": "<:VorpalWeapon:965357951130935336>",
    "Cranial Spike": "<:CranialSpike:965357951265157200>",
    "Threat Detector": "<:ThreatDetector:965357951265144862>",
    "Harmony": "<:Harmony:965357950807969876>",
    "Moving Target": "<:MovingTarget:965358334842638356>",
    "One for All": "<:OneforAll:965358962679640164>",
    "High-Impact Reserves": "<:HighImpactReserves:967198786092941412>",
    "Genesis": "<:Genesis:967198785996488775>",
    "Underdog": "<:Underdog:967198786222981150>",
    "Tap the Trigger": "<:TaptheTrigger:967198785996472340>",
    "Dynamic Sway Reduction": "<:DynamicSwayReduction:967198786185224202>",
    "Relentless Strikes": "<:RelentlessStrikes:967198785971302511>",
    "Full Auto Trigger System": "<:FullAutoTriggerSystem:967198785790963794>",
    "Fourth Time's the Charm": "<:FourthTimestheCharm:967198786092949524>",
    "Flame Refraction": "<:FlameRefraction:967200463449632788>",
    "Prismatic Inferno": "<:PrismaticInferno:967201329011388446>",
    "Impulse Amplifier": "<:ImpulseAmplifier:968270202238292068>",
    "Osmosis": "<:Osmosis:968270201932095509>",
    "Veist Stinger": "<:VeistStinger:968270201940480030>",
    "Steady Hands": "<:SteadyHands:968270201982443602>"
}

DestinyItemSubType = {
    "None": 0,
    "AutoRifle": 6,
    "Shotgun": 7,
    "Machinegun": 8,
    "HandCannon": 9,
    "RocketLauncher": 10,
    "FusionRifle": 11,
    "SniperRifle": 12,
    "PulseRifle": 13,
    "ScoutRifle": 14,
    "Sidearm": 17,
    "Sword": 18,
    "Mask": 19,
    "Shader": 20,
    "Ornament": 21,
    "FusionRifleLine": 22,
    "GrenadeLauncher": 23,
    "SubmachineGun": 24,
    "TraceRifle": 25,
    "HelmetArmor": 26,
    "GauntletsArmor": 27,
    "ChestArmor": 28,
    "LegArmor": 29,
    "ClassArmor": 30,
    "Bow": 31,
    "DummyRepeatableBounty": 32,
    "Glaive": 33
}

DestinyChallenges = {
    # VOW challenges
    "Swift Destruction":
        [
            "Acquisition encounter", "All three Unstoppable Abominations must be killed within 5 seconds."
        ],
    "Base Information":
        [
            "Caretaker encounter", "You may only grab one symbol at a time."
        ],
    "Defenses Down":
        [
            "Exhibition encounter", "Each player may only kill one Taken knight."
        ],
    "Looping Catalyst":
        [
            "Rhulk encounter", "Your fireteam cannot lose the Leeching Essence buff."
        ],
    # VOG Challenges
    "Wait for It...":
        [
            "Confluxes encounter", "Only defeat Wyverns while they're sacrificing.", "Vision of Confluence"
        ],
    "The Only Oracle For You":
        [
            "Oracle encounter", "Each player may not destroy the same oracle twice.", "Praedyth's Revenge"
        ],
    "Out of Its Way":
        [
            "Templar encounter", "Defeat the Templar without allowing it to teleport.", "Fatebringer"
        ],
    "Strangers in Time":
        [
            "Gatekeepers encounter", "Defeat the Wyvern and Praetorian Minotaur enemies within 3 seconds of each other.", "Hezen Vengeance"
        ],
    "Ensemble's Refrain":
        [
            "Atheon encounter", "Each player may not destroy more than one oracle per oracle wave.", "Corrective Measure"
        ],
    # GOS Challenges
    "A Link to the Chain":
        [
            "First encounter", "All six fireteam members must replenish enlightment at the same time."
        ],
    "To the Top":
        [
            "Third encounter", "10 motes must be deposited at a time."
        ],
    "Zero to One Hundred":
        [
            "Fourth encounter", "Once you deposite motes, you have 10 seconds to fully fill the bank."
        ],
    "Leftovers":
        [
            "First encounter", "Do not kill any of the Cyclops in the room where the Consecrated Mind is depositing Voltaic Overflow charges."
        ],
    # DSC Challenges
    "Red Rover":
        [
            "First encounter", "All players have to be operator and shoot two pannels on lowe level (requires 3 phases)."
        ],
    "Copies of Copies":
        [
            "Second encounter", "Do not send any Replication debuff out of an airlock."
        ],
    "Of All Trades":
        [
            "Third encounter", "All players on the fireteam must do each role (operator, scanner, suppressor) once."
        ],
    "The Core Four":
        [
            "Fourth encounter", "Players must dunk all four cores each time you can destroy Taniks' orange generator."
        ],
    # KF Challenges
    "The Grass is Alwayes Greener":
        [
            "Totems encounter", "Players cannot take the same Brand type twice in a row."
        ],
    "Devious Thievery":
        [
            "Warpriest encounter", "Players must steal the Brand of the Initiate within a couple of seconds of taking the Brand Claimer buff."
        ],
    "Gaze Amaze":
        [
            "Golgoroth encounter", "Players must The gaze holder must tand in the Pool of Unclaimed Light when swapping the gaze."
        ],
    "Under Construction":
        [
            "Daughters encounter", "Players cannot stand on the same plate twice in a single phase."
        ],
    "Hands off":
        [
            "Oryx encounter", "Players must not kill the same Ogre or Light Eater Knight throughout the encounter."
        ],
    # RON Challenges
    "Illuminated Torment":
        [
            "Cataclysm encounter", "All Tormentors must be killed by someone with the Field of Light buff."
        ],
    "Crossfire":
        [
            "Scission encounter", "Players can only shoot the launcher cystals on the opposite side."
        ],
    "Cosmic Equilibrium":
        [
            "Macrocosm encounter", "Players must move all dark planets to the left side and all light planets to the right side."
        ],
    "All Hands":
        [
            "Nezarec encounter", "Players must complete a node on each side, light and dark (both sides must be completed around the same time)."
        ]
}