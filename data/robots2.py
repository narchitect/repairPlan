actions = [
    {"action": "loadArm", "parameters": ["equipment", "material=None"]},
    {"action": "unloadArm", "parameters": []},
    {"action": "pickUp", "parameters": ["element_id"], "preconditions": ["equipment == 'gripper'"]},
    {"action": "putDown", "parameters": ["element_id"], "preconditions": ["equipment == 'gripper'"]},
    {"action": "placeInTrashBag", "parameters": ["element_id"], "preconditions": ["equipment == 'gripper'"]},
    {"action": "spraySurface", "parameters": ["element_id"], "preconditions": ["equipment == 'sprayGun'", "material != None"]},
    {"action": "wipeSurface", "parameters": ["element_id"], "preconditions": ["equipment == 'wiper'", "surfaceIsWet == true"]},
    {"action": "smoothSurface", "parameters": ["element_id"], "preconditions": ["equipment == 'scraper'"]},
]

equipments = [
    "sprayGun",
    "brush",
    "wiper",
    "scraper",
    "gripper",
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
        "gripper",
        "vacuum"
    ],
    "materials": [
        "cleaning Solution",
        "disinfectant",
        "paint",
        "filler"
    ],
    "size": {"width": 700, "height": 1500}, 
    "max_reach_height": 2000,
    "camera": {"height": 1500, "FOV": 90}

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
        "gripper",
        "vacuum"
    ],
    "materials": [
        "cleaning Solution",
        "disinfectant",
        "paint",
        "filler"
    ],
    "size": {"width": 850, "height": 1700},  
    "max_reach_height": 3700,  
    "camera": {"height": 1500, "FOV": 90}
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
    ],
    "size": {"width": 1600, "height": 2000}, 
    "max_reach_height": 3700,
    "camera": {"height": 1200, "FOV": 90}  
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
    "size": {"width": 700, "height": 1600}, 
    "max_reach_height": 3700,
    "camera": {"height": 1600, "FOV": 90}
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
    "size": {"width": 700, "height": 1600},  
    "max_reach_height": 3700,  
    "camera": {"height": 1800, "FOV": 90}
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
    "size": {"width": 700, "height": 1600}, 
    "max_reach_height": 3700,
    "camera": {"height": 1700, "FOV": 90}  
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
    "size": {"width": 700, "height": 1600},  
    "max_reach_height": 2000,
    "camera": {"height": 1500, "FOV": 90}
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
    "size": {"width": 700, "height": 1600}, 
    "max_reach_height": 3700,
    "camera": {"height": 1700, "FOV": 90}  
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
    "size": {"width": 700, "height": 1600},  
    "max_reach_height": 3700, 
    "camera": {"height": 1500, "FOV": 90}
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
    "size": {"width": 700, "height": 1600},  
    "max_reach_height": 2000, 
    "camera": {"height": 1300, "FOV": 90}
}

robots_withoutConfig = {
        "robots": [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10],
        "robot_storage": {
            "room_id": 1
        }
}
robots_withConfig = {
        "robot_configs": {
            "actions": actions,
            "equipments": equipments,
            "materials": materials,
        },
        "robot_storage": {
            "room_id": 46
        },
        "robots": [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10],
    }

robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10]

# print(robots_withConfig["robot_storage"])



