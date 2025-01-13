# account_goals.py

COMBAT_MILESTONES = {
    1: {"Attack": 30, "Strength": 30, "Defence": 30},
    2: {"Attack": 40, "Strength": 40, "Defence": 40},
    3: {"Attack": 60, "Strength": 60, "Defence": 60},
    4: {"Attack": 70, "Strength": 70, "Defence": 70},
}

TOTAL_LEVEL_MILESTONES = {
    1: 500,
    2: 750,
    3: 1000,
    4: 1250,
    5: 1500,
}

LEVEL_TIME_RANGES = {
    (1, 30): (30, 90),     # Levels 1-30: 30-90 minutes
    (31, 60): (60, 180),   # Levels 31-60: 1-3 hours
    (61, 80): (120, 240),  # Levels 61-80: 2-4 hours
    (81, 99): (240, 480),  # Levels 81-99: 4-8 hours
}

QUEST_MILESTONES = {
    "earlyCombatXP": [
        "Waterfall Quest",
        "Fight Arena",
        "Tree Gnome Village",
        "The Grand Tree",
        "Vampyre Slayer",
        "Mountain Daughter"
    ],
    "earlyMagicXP": [
        "Witch's Potion",
        "Imp Catcher",
        "Rune Mysteries"
    ],
    "earlyRangedXP": [
        "Big Chompy Bird Hunting"
    ],
    "earlyAgilityXP": [
        "The Tourist Trap",
        "Recruitment Drive"
    ],
    "earlyThievingXP": [
        "Biohazard"
    ],
    # Add more milestones as needed
}

SKILL_MILESTONES = {
    "Agility": {
        30: "Varrock Rooftop Course",
        50: "Falador Rooftop Course",
        70: "Pollnivneach Rooftop Course",
        90: "Ardougne Rooftop Course"
    },
    "Attack": {
        40: "Unlock Rune weapons",
        60: "Unlock Dragon Scimitar",
        70: "Unlock Abyssal Whip",
        75: "Unlock Abyssal Tentacle"
    },
    "Construction": {
        33: "Oak Larders",
        50: "Portal Chamber",
        83: "Ornate Jewellery Box"
    },
    "Cooking": {
        35: "Jugs of Wine"
    },
    "Crafting": {
        57: "Unpowered Orbs"
    },
    "Defence": {
        30: "Adamant Armour",
        40: "Rune Armour",
        60: "Dragon Platebody",
        70: "Barrows Armour"
    },
    "Farming": {
        34: "Tithe Farm"
    },
    "Firemaking": {
        50: "Wintertodt"
    },
    "Fishing": {
        40: "Fly Fishing",
        50: "Lobsters",
        62: "Monkfish",
        76: "Sharks"
    },
    "Fletching": {
        30: "Maple Longbows",
        55: "Broad Bolts",
        85: "Dragon Darts"
    },
    "Herblore": {
        38: "Prayer Potions",
        45: "Super Attack/Strength/Defence",
        66: "Super Restore",
        81: "Saradomin Brew",
        90: "Super Combat Potion"
    },
    "Hunter": {
        43: "Falconry",
        60: "Red Chinchompas",
        73: "Black Chinchompas",
        80: "Herbiboar"
    },
    "Magic": {
        37: "Varrock Teleport",
        45: "Camelot Teleport",
        55: "High Alchemy",
        70: "Mage Arena 1",
        75: "Mage Arena 2",
        96: "Ice Barrage"
    },
    "Mining": {
        30: "Iron Ore",
        60: "Volcanic Mine",
        85: "Runite Ore"
    },
    "Prayer": {
        43: "Protect from Melee/Missiles",
        70: "Piety",
        77: "Rigour/Augury"
    },
    "Ranged": {
        50: "Magic Shortbow",
        75: "Toxic Blowpipe"
    },
    "Runecrafting": {
        44: "Nature Runes",
        77: "Blood Runes",
        91: "Double Nature Runes"
    },
    "Slayer": {
        55: "Broad Bolts",
        75: "Slayer Helmet (i)",
        85: "Abyssal Whip",
        93: "Trident of the Seas/Swamp"
    },
    "Smithing": {
        40: "Gold Bars (Blast Furnace)",
        85: "Rune Platebody",
        88: "Runite Limbs",
        99: "Max Cape"
    },
    "Strength": {
        40: "Unlock Rune weapons",
        60: "Unlock Dragon weapons",
        70: "Unlock Godswords",
    },
    "Thieving": {
        25: "Fruit Stalls",
        38: "Blackjacking (requires Rogue Trader miniquest)",
        55: "Pyramid Plunder"
    },
    "Woodcutting": {
        35: "Willow Trees",
        60: "Yew Trees",
        75: "Magic Trees",
        90: "Redwood Trees"
    }
}