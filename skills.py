# skills.py

SKILLS = {
    "agility": {
        "methods": {
            "default": {
                "1-10": {"name": "Gnome Stronghold Agility Course", "xp_per_hour": 8000, "requirements": {}},
                "10-20": {"name": "Draynor Village Rooftop Course", "xp_per_hour": 9000, "requirements": {"agility": 1}},
                "20-30": {"name": "Al Kharid Rooftop Course", "xp_per_hour": 9000, "requirements": {"agility": 20}},
                "30-40": {"name": "Varrock Rooftop Course", "xp_per_hour": 13000, "requirements": {"agility": 30}},
                "40-50": {"name": "Canifis Rooftop Course", "xp_per_hour": 19000, "requirements": {"agility": 40}},
                "50-60": {"name": "Seers' Village Rooftop Course", "xp_per_hour": 45000, "requirements": {"agility": 50}},
                "60-80": {"name": "Seers' Village Rooftop Course (with hard diary)", "xp_per_hour": 57000, "requirements": {"agility": 60, "quests": ["kandarin_hard"]}},
                "80-90": {"name": "Rellekka Rooftop Course", "xp_per_hour": 54000, "requirements": {"agility": 80}},
                "90-99": {"name": "Ardougne Rooftop Course", "xp_per_hour": 60000, "requirements": {"agility": 90}}
            },
            "gnome": {
                "1-99": {"name": "Gnome Stronghold Agility Course", "xp_per_hour": 8000, "requirements": {}}
            },
            "draynor": {
                "1-99": {"name": "Draynor Village Rooftop Course", "xp_per_hour": 9000, "requirements": {"agility": 1}}
            },
            "varrock": {
                "1-99": {"name": "Varrock Rooftop Course", "xp_per_hour": 13000, "requirements": {"agility": 30}}
            },
            "canifis": {
                "1-99": {"name": "Canifis Rooftop Course", "xp_per_hour": 19000, "requirements": {"agility": 40}}
            },
            "falador": {
                "1-99": {"name": "Falador Rooftop Course", "xp_per_hour": 45000, "requirements": {"agility": 50}}
            },
            "seers": {
                "1-99": {"name": "Seers' Village Rooftop Course", "xp_per_hour": 57000, "requirements": {"agility": 60}}
            },
            "polly": {
                "1-99": {"name": "Pollnivneach Rooftop Course", "xp_per_hour": 54000, "requirements": {"agility": 70}}
            },
            "relleka": {
                "1-99": {"name": "Rellekka Rooftop Course", "xp_per_hour": 60000, "requirements": {"agility": 80}}
            },
            "ardy": {
                "1-99": {"name": "Ardougne Rooftop Course", "xp_per_hour": 60000, "requirements": {"agility": 90}}
            }
        },
        "default_method": "default"
    },
    "construction": {
        "methods": {
            "default": {
                "1-33": {"name": "Crude Wooden Chairs", "xp_per_hour": 28000, "requirements": {}},
                "33-52": {"name": "Oak Larders", "xp_per_hour": 80000, "requirements": {"construction": 33}},
                "52-74": {"name": "Mahogany Tables", "xp_per_hour": 140000, "requirements": {"construction": 52}},
                "74-99": {"name": "Mahogany Tables", "xp_per_hour": 840000, "requirements": {"construction": 74}}
            }
        },
        "default_method": "default"
    },
    "cooking": {
        "methods": {
            "default": {
                "1-35": {"name": "Shrimps", "xp_per_hour": 10000, "requirements": {}},
                "35-99": {"name": "Karambwans", "xp_per_hour": 380000, "requirements": {"cooking": 35, "quests": ["tai_bwo_wannai_trio"]}}
            }
        },
        "default_method": "default"
    },
    "crafting": {
        "methods": {
            "default": {
                "1-54": {"name": "Gems", "xp_per_hour": 110000, "requirements": {}},
                "54-63": {"name": "Green Dragonhide Bodies", "xp_per_hour": 150000, "requirements": {"crafting": 54}},
                "63-99": {"name": "Air Battlestaves", "xp_per_hour": 220000, "requirements": {"crafting": 63, "magic": 66}}
            }
        },
        "default_method": "default"
    },
    "farming": {
        "methods": {
            "default": {
                "1-99": {"name": "Tree Runs", "xp_per_hour": 50000, "requirements": {}}
            }
        },
        "default_method": "default"
    },
    "firemaking": {
        "methods": {
            "default": {
                "1-50": {"name": "Normal Logs", "xp_per_hour": 40000, "requirements": {}},
                "50-99": {"name": "Wintertodt", "xp_per_hour": 300000, "requirements": {"firemaking": 50}}
            }
        },
        "default_method": "default"
    },
    "fishing": {
        "methods": {
            "default": {
                "1-20": {"name": "Shrimps", "xp_per_hour": 7000, "requirements": {}},
                "20-47": {"name": "Fly Fishing", "xp_per_hour": 35000, "requirements": {"fishing": 20}},
                "47-99": {"name": "Barbarian Fishing", "xp_per_hour": 80000, "requirements": {"fishing": 48, "strength": 15, "agility": 15}}
            }
        },
        "default_method": "default"
    },
    "fletching": {
        "methods": {
            "default": {
                "1-99": {"name": "Broad Bolts", "xp_per_hour": 900000, "requirements": {"fletching": 52, "slayer": 55}}
            }
        },
        "default_method": "default"
    },
    "herblore": {
        "methods": {
            "default": {
                "1-38": {"name": "Attack Potions", "xp_per_hour": 20000, "requirements": {}},
                "38-55": {"name": "Prayer Potions", "xp_per_hour": 150000, "requirements": {"herblore": 38}},
                "55-66": {"name": "Super Energy Potions", "xp_per_hour": 175000, "requirements": {"herblore": 52}},
                "66-72": {"name": "Super Restore Potions", "xp_per_hour": 200000, "requirements": {"herblore": 63}},
                "72-81": {"name": "Saradomin Brews", "xp_per_hour": 230000, "requirements": {"herblore": 81}},
                "81-99": {"name": "Super Combat Potions", "xp_per_hour": 250000, "requirements": {"herblore": 90}}
            }
        },
        "default_method": "default"
    },
    "hunter": {
        "methods": {
            "default": {
                "1-60": {"name": "Birdhouses", "xp_per_hour": 28000, "requirements": {}},
                "60-80": {"name": "Red Chinchompas", "xp_per_hour": 270000, "requirements": {"hunter": 60}},
                "80-99": {"name": "Black Chinchompas", "xp_per_hour": 330000, "requirements": {"hunter": 73}}
            }
        },
        "default_method": "default"
    },
    "mining": {
        "methods": {
            "default": {
                "1-60": {"name": "Iron Ore", "xp_per_hour": 65000, "requirements": {}},
                "60-99": {"name": "Volcanic Mine", "xp_per_hour": 70000, "requirements": {"mining": 50}}
            }
        },
        "default_method": "default"
    },
    "prayer": {
        "methods": {
            "default": {
                "1-99": {"name": "Superior Dragon Bones (Chaos Altar)", "xp_per_hour": 800000, "requirements": {}}
            }
        },
        "default_method": "default"
    },
    "runecrafting": {
        "methods": {
            "default": {
                "1-77": {"name": "Lava Runes", "xp_per_hour": 70000, "requirements": {}},
                "77-99": {"name": "Blood Runes", "xp_per_hour": 55000, "requirements": {"runecrafting": 77}}
            }
        },
        "default_method": "default"
    },
    "smithing": {
        "methods": {
            "default": {
                "1-40": {"name": "Bronze Bars (Blast Furnace)", "xp_per_hour": 30000, "requirements": {}},
                "40-99": {"name": "Gold Bars (Blast Furnace)", "xp_per_hour": 350000, "requirements": {"smithing": 40}}
            }
        },
        "default_method": "default"
    },
    "thieving": {
        "methods": {
            "default": {
                "1-55": {"name": "Ardougne Knights", "xp_per_hour": 80000, "requirements": {}},
                "55-99": {"name": "Pyramid Plunder", "xp_per_hour": 250000, "requirements": {"thieving": 55}}
            },
            "fruit": {
                "1-99": {"name": "Fruit Stalls", "xp_per_hour": 50000, "requirements": {"thieving": 25}}
            }
        },
        "default_method": "default"
    },
    "woodcutting": {
        "methods": {
            "default": {
                "1-60": {"name": "Teak Trees", "xp_per_hour": 80000, "requirements": {}},
                "60-99": {"name": "Sulliuscep Mushrooms", "xp_per_hour": 120000, "requirements": {"woodcutting": 65}}
            }
        },
        "default_method": "default"
    },
    "magic": {
        "methods": {
            "default": {
                "1-55": {"name": "Splashing", "xp_per_hour": 14000, "requirements": {}},
                "55-99": {"name": "High Alch", "xp_per_hour": 65000, "requirements": {"magic": 55}},
                "55-70": {"name": "Fire Bolt (NMZ)", "xp_per_hour": 159000, "requirements": {"magic": 55}},
                "70-99": {"name": "Fire Surge (NMZ)", "xp_per_hour": 238000, "requirements": {"magic": 70}}
            }
        },
        "default_method": "default"
    },
    "attack": {
        "methods": {
            "crab": {
                "1-99": {"name": "Sand Crabs", "xp_per_hour": 30000, "requirements": {}}
            },
            "nmz": {
                "1-99": {"name": "Nightmare Zone", "xp_per_hour": 100000, "requirements": {"attack": 60, "strength": 60}}
            },
            "rat": {
                "1-99": {"name": "Scurrius", "xp_per_hour": 45000, "requirements": {"attack": 50, "strength": 50}}
            },
            "slay": {
                "1-99": {"name": "Slayer", "xp_per_hour": 30000, "requirements": {}}
            }
        },
        "default_method": "crab"
    },
    "strength": {
        "methods": {
            "crab": {
                "1-99": {"name": "Sand Crabs", "xp_per_hour": 30000, "requirements": {}}
            },
            "nmz": {
                "1-99": {"name": "Nightmare Zone", "xp_per_hour": 100000, "requirements": {"attack": 60, "strength": 60}}
            },
            "rat": {
                "1-99": {"name": "Scurrius", "xp_per_hour": 45000, "requirements": {"attack": 50, "strength": 50}}
            },
            "slay": {
                "1-99": {"name": "Slayer", "xp_per_hour": 30000, "requirements": {}}
            }
        },
        "default_method": "crab"
    },
    "defence": {
        "methods": {
            "crab": {
                "1-99": {"name": "Sand Crabs", "xp_per_hour": 30000, "requirements": {}}
            },
            "nmz": {
                "1-99": {"name": "Nightmare Zone", "xp_per_hour": 100000, "requirements": {"attack": 60, "strength": 60}}
            },
            "rat": {
                "1-99": {"name": "Scurrius", "xp_per_hour": 45000, "requirements": {"attack": 50, "strength": 50}}
            },
            "slay": {
                "1-99": {"name": "Slayer", "xp_per_hour": 30000, "requirements": {}}
            }
        },
        "default_method": "crab"
    },
    "ranged": {
        "methods": {
            "crab": {
                "1-99": {"name": "Sand Crabs", "xp_per_hour": 30000, "requirements": {}}
            },
            "nmz": {
                "1-99": {"name": "Nightmare Zone", "xp_per_hour": 100000, "requirements": {"ranged": 50, "defence": 40}}
            },
            "rat": {
                "1-99": {"name": "Scurrius", "xp_per_hour": 45000, "requirements": {"ranged": 50, "defence": 40}}
            },
            "slay": {
                "1-99": {"name": "Slayer", "xp_per_hour": 30000, "requirements": {}}
            },
            "cannon": {
                "1-99": {"name": "Dwarf Cannon", "xp_per_hour": 60000, "requirements": {}}
            }
        },
        "default_method": "crab"
    },
    "longranged": {
        "methods": {
            "crab": {
                "1-99": {"name": "Sand Crabs", "xp_per_hour": 30000, "requirements": {}}
            },
            "rat": {
                "1-99": {"name": "Scurrius", "xp_per_hour": 45000, "requirements": {"ranged": 50, "defence": 40}}
            },
            "slay": {
                "1-99": {"name": "Slayer", "xp_per_hour": 30000, "requirements": {}}
            }
        },
        "default_method": "crab"
    }
}