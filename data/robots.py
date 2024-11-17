actions = [
    "load<equipment>",
    "unload<equipment>",
    "pickUp<object>",
    "putDown<object>",
    "placeInTrashBag"
    "spray<object>",
    "wipeSurface<object>",
    "smoothSurface<object>",
]
equipments = [
    "sprayGun<object><material>",
    "brush",
    "wiper",
    "scraper",
    "gripper"
]

materials = [
    "cleaning Solution",
    "disinfectant",
    "paint",
    "filler"
]

robot1 = {
    "id": 1,
    "actions": [
        "pickUp",
        "putDown",
        "placeInTrashBag",
        "spray",
        "wipeSurface",
        "smoothSurface",
    ],
    "equipments": [
        "sprayGun",
        "brush",
        "wiper",
        "scraper",
        "gripper"
    ],
    "materials": [
        "cleaning Solution",
        "disinfectant",
        "paint",
        "filler"
    ],
    "size": {"width": 700, "height": 1500},  # Small size
    "max_reach_height": 2000  # Can reach up to 2 meters
}

robot2 = {
    "id": 2,
    "actions": [
        "pickUp",
        "putDown",
        "placeInTrashBag",
        "spray",
        "wipeSurface",
        "smoothSurface",
    ],
    "equipments": [
        "sprayGun",
        "brush",
        "wiper",
        "scraper",
        "gripper"
    ],
    "materials": [
        "cleaning Solution",
        "disinfectant",
        "paint",
        "filler"
    ],
    "size": {"width": 850, "height": 1700},  # Medium size
    "max_reach_height": 3000  # Can reach up to 3 meters
}


robot3 = {
    "id": 3,
    "actions": [
        "pickUp",
        "putDown",
        "placeInTrashBag",
        "spray",
        "wipeSurface",
        "smoothSurface",
    ],
    "equipments": [
        "sprayGun",
        "brush",
        "wiper",
        "scraper",
        "gripper"
    ],
    "materials": [
        "cleaning Solution",
        "disinfectant",
        "paint",
        "filler"
    ],
    "size": {"width": 1600, "height": 2000},  # Large size
    "max_reach_height": 3700  # Can reach up to ceiling height
}


robot4 = {
    "id": 4,
    "actions": [
        "pickUp",
        "putDown",
        "placeInTrashBag",
        "spray",
        "wipeSurface",
        "smoothSurface",
    ],
    "equipments": [
        "sprayGun",
        "brush",
        "wiper",
        "scraper",
        "gripper"
    ],
    "materials": [
        "cleaning Solution",
        "disinfectant",
        "paint",
        "filler"
    ],
    "size": {"width": 700, "height": 1600},  # Fits all doors
    "max_reach_height": 2000  # Limited reach
}

robot5 = {
    "id": 5,
    "actions": [
        "pickUp",
        "putDown",
        "placeInTrashBag",
        "spray",
        "wipeSurface",
        "smoothSurface",
    ],
    "equipments": [
        "sprayGun",
        "brush",
        "wiper",
        "scraper",
        "gripper"
    ],
    "materials": [
        "cleaning Solution",
        "disinfectant",
        "paint",
        "filler"
    ],
    "size": {"width": 700, "height": 1600},  # Fits all doors
    "max_reach_height": 3700  # Maximum reach
}


robot6 = {
    "id": 6,
    "actions": [
        "wipeSurface"
    ],
    "equipments": [
        "wiper"
    ],
    "materials": [
        "cleaning Solution"
    ],
    "size": {"width": 700, "height": 1600},  # Fits all doors
    "max_reach_height": 3700  # Can reach windows up to ceiling height
}


robot7 = {
    "id": 7,
    "actions": [
        "spray",
        "wipeSurface"
    ],
    "equipments": [
        "sprayGun",
        "wiper"
    ],
    "materials": [
        "disinfectant"
    ],
    "size": {"width": 700, "height": 1600},  # Fits all doors
    "max_reach_height": 2000  # Door handles are typically within 1m - 1.5m
}

robot8 = {
    "id": 8,
    "actions": [
        "spray"
    ],
    "equipments": [
        "sprayGun"
    ],
    "materials": [
        "paint"
    ],
    "size": {"width": 700, "height": 1600},  # Fits all doors
    "max_reach_height": 3700  # Can paint walls up to ceiling height
}


robot9 = {
    "id": 9,
    "actions": [
        "smoothSurface"
    ],
    "equipments": [
        "scraper",
        "brush"
    ],
    "materials": [
        "filler"
    ],
    "size": {"width": 700, "height": 1600},  # Fits all doors
    "max_reach_height": 3700  # Can reach cracks at any height
}

robot10 = {
    "id": 10,
    "actions": [
        "pickUp",
        "putDown",
        "placeInTrashBag"
    ],
    "equipments": [
        "gripper"
    ],
    "size": {"width": 700, "height": 1600},  # Fits all doors
    "max_reach_height": 2000  # Sufficient for ground-level trash collection
}

robots_withoutConfig = {
        "robots": [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10],
        "robot_storage_room_id": 1
}
robots_withConfig = {
        "robot_configs": {
            "actions": actions,
            "equipments": equipments,
            "materials": materials,
        },
        "robots": [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10],
    }

robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10]
robot_storage_id = 1



