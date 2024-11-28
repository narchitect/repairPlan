# Robot State
robot_state = {
    "equipment": None,
    "material": None,
    "lastAction": None
}

# Equipments
equipments = [
    "sprayGun",
    "wiper",
    "scraper",
    "gripper",
    "roller"
]

# Materials
materials = [
    "paint",
    "disinfectant",
    "cleaningSolution"
]

# Actions
actions = [
    {
        "action": "loadEquipment",
        "parameters": ["equipment", "material=None"],
        "preconditions": [
            "equipment == None",
            "material != None if equipment == sprayGun else True"
        ],
        "effects": [
            "robot_state[equipment] = equipment",
            "robot_state[material] = material"
        ]
    },
    {
        "action": "unloadEquipment",
        "parameters": [],
        "preconditions": ["robot_state[equipment] != None"],
        "effects": [
            "robot_state[equipment] = None",
            "robot_state[material] = None"
        ]
    },
    {
        "action": "scanTrashes",
        "parameters": ["surface_id"],
        "preconditions": ["robot_state[equipment] == None", "element_type == floor"],
        "effects": [
            "robot_state[lastAction] = scanTrashes"
        ]
    },
    {
        "action": "collectTrashes",
        "parameters": [],
        "preconditions": [
            "robot_state[equipment] == gripper",
            "robot_state[lastAction] == scanTrashes"
        ],
        "effects": [
            "robot_state[lastAction] = collectTrashes"
        ]
    },
    {
        "action": "placeInTrashBag",
        "parameters": [],
        "preconditions": [
            "robot_state[equipment] == gripper",
            "robot_state[lastAction] == collectTrashes"
        ],
        "effects": [
            "robot_state[lastAction] = placeInTrashBag"
        ]
    },
    {
        "action": "spraySurface",
        "parameters": ["surface_id"],
        "preconditions": [
            "robot_state[equipment] == sprayGun",
            "robot_state[material] != None"
        ],
        "effects": [
            "robot_state[surfaceIsWet][surface_id] = True",
            "robot_state[lastAction] = spraySurface"
        ]
    },
    {
        "action": "wipeSurface",
        "parameters": ["surface_id"],
        "preconditions": [
            "robot_state[equipment] == wiper",
            "robot_state[surfaceIsWet].get(surface_id, False) == True"
        ],
        "effects": [
            "robot_state[surfaceIsWet][surface_id] = False",
            "robot_state[lastAction] = wipeSurface"
        ]
    },
    {
        "action": "rollSurface",
        "parameters": ["surface_id"],
        "preconditions": [
            "robot_state[equipment] == roller"
        ],
        "effects": [
            "robot_state[lastAction] = rollSurface"
        ]
    },
    {
        "action": "polishSurface",
        "parameters": ["surface_id"],
        "preconditions": [
            "robot_state[equipment] == scraper"
        ],
        "effects": [
            "robot_state[lastAction] = polishSurface"
        ]
    }
]


robots = [
    {
        "id": 1,
        "actions": [
            "loadArm",
            "unloadArm",
            "spraySurface",
            "wipeSurface"
        ],
        "equipments": [
            "sprayGun",
            "wiper"
        ],
        "materials": [
            "cleaningSolution"
        ],
        "max_reach_height": 3000,
        "camera": {"FOV": 90}
    },
    {
        "id": 2,
        "actions": [
            "loadArm",
            "unloadArm",
            "spraySurface",
            "wipeSurface"
        ],
        "equipments": [
            "sprayGun",
            "wiper"
        ],
        "materials": [
            "disinfectant"
        ],
        "max_reach_height": 3000,
        "camera": {"FOV": 90}
    },
    {
        "id": 3,
        "actions": [
            "loadArm",
            "unloadArm",
            "spraySurface",
            "rollSurface"
        ],
        "equipments": [
            "sprayGun",
            "roller"
        ],
        "materials": [
            "paint"
        ],
        "max_reach_height": 3000,
        "camera": {"FOV": 90}
    },
    {
        "id": 4,
        "actions": [
            "loadArm",
            "unloadArm",
            "spraySurface",
            "polishSurface"
        ],
        "equipments": [
            "sprayGun",
            "scraper"
        ],
        "materials": [
            "filler"
        ],
        "max_reach_height": 3000,
        "camera": {"FOV": 90}
    },
    {
        "id": 5,
        "actions": [
            "scanTrashes",
            "loadArm",
            "unloadArm",
            "collectTrashes",
            "placeInTrashBag"
        ],
        "equipments": [
            "gripper"
        ],
        "materials": [],
        "max_reach_height": 1000,
        "camera": {"FOV": 90}
    },
    {
        "id": 6,
        "actions": [
            "loadArm",
            "unloadArm",
            "spraySurface",
            "polishSurface"
        ],
        "equipments": [
            "sprayGun",
            "scraper"
        ],
        "materials": [
            "filler"
        ],
        "max_reach_height": 3700,
        "camera": {"FOV": 90}
    },
    {
        "id": 7,
        "actions": [
            "loadArm",
            "unloadArm",
            "spraySurface",
            "rollSurface"
        ],
        "equipments": [
            "sprayGun",
            "roller"
        ],
        "materials": [
            "paint"
        ],
        "max_reach_height": 3700,
        "camera": {"FOV": 90}
    },
    {
        "id": 8,
        "actions": [
            "scanTrashes",
            "loadArm",
            "unloadArm",
            "collectTrashes",
            "placeInTrashBag",
            "spraySurface",
            "rollSurface"
        ],
        "equipments": [
            "gripper",
            "sprayGun",
            "roller"
        ],
        "materials": [
            "paint"
        ],
        "max_reach_height": 3000,
        "camera": {"FOV": 90}
    },
    {
        "id": 9,
        "actions": [
            "loadArm",
            "unloadArm",
            "spraySurface",
            "polishSurface",
            "rollSurface"
        ],
        "equipments": [
            "sprayGun",
            "scraper",
            "roller"
        ],
        "materials": [
            "filler",
            "paint"
        ],
        "max_reach_height": 3000,
        "camera": {"FOV": 90}
    },
        {
            "id": 10,
            "actions": [
                "loadArm",
                "unloadArm",
                "spraySurface",
                "wipeSurface"
            ],
            "equipments": [
                "sprayGun",
                "wiper"
            ],
            "materials": [
                "disinfectant",
                "cleaningSolution"
            ],
            "max_reach_height": 3000,
            "camera": {"FOV": 90}
        }
    ]


robots_withoutConfig = {
        "robots": robots,
        "robot_storage": {
            "room_id": 46
        }
}
robots_withConfig = {
        "robot_specifications": {
            "robot_type": "one-arm robot",
            "actions": actions,
            "equipments": equipments,
            "materials": materials,
        },
        "robot_storage": {
            "room_id": 46
        },
        "robots": robots,
    }




