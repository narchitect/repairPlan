actions = [
    {"action": "loadArm", "parameters": ["equipment", "material=None"], "preconditions": ["if equipment == 'sprayGun' and material != None"]},
    {"action": "unloadArm", "parameters": []},
    {"action": "collectTrashes", "parameters": [], "preconditions": ["equipment == 'gripper'", "action='scanTrashes'"]},
    {"action": "scanTrashes", "parameters": ["surface_id"], "preconditions": ["equipment == None", "element_type == 'floor'"]},
    {"action": "placeInTrashBag", "parameters": [], "preconditions": ["equipment == 'gripper'", "action='collectTrashes'"]},
    {"action": "spraySurface", "parameters": ["surface_id"], "preconditions": ["equipment == 'sprayGun'", "material != None"]},
    {"action": "wipeSurface", "parameters": ["surface_id"], "preconditions": ["equipment == 'wiper'", "surfaceIsWet == true"]},
    {"action": "spreadPaint", "parameters": ["surface_id"], "preconditions": ["equipment == 'roller'", "previous_action='spraySurface'", "material == 'paint'"]},
    {"action": "spreadFiller", "parameters": ["surface_id"], "preconditions": ["equipment == 'scrapper'", "previous_action='spraySurface'", "material == 'filler'"]},
]

equipments = [
    "sprayGun",
    "wiper",
    "scraper",
    "gripper",
]

materials = [
    "cleaningSolution",
    "disinfectant",
    "paint",
    "filler"
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
            "spreadPaint"
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
            "spreadFiller"
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
            "spreadFiller"
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
            "spreadPaint"
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
            "spreadPaint"
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
            "spreadFiller",
            "spreadPaint"
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




