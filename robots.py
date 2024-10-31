all_actions = [
    'NavigateToLocation',
    'ScanObject',
    'GraspObject',
    'ReleaseObject',
    'TurnSwitchOn',
    'TurnSwitchOff',
    'Unscrew',
    'Screw',
    'CleanSurface',
    'PaintSurface'
]

#Screw/Unscrew
robot1 = {
    'id': 'robot1',
    'actions': [
        'NavigateToLocation',
        'ScanObject',
        'GraspObject',
        'ReleaseObject',
        'Unscrew',
        'Screw'
    ],  
    'size': {'width': 700, 'height': 1900},
    'max_reach_height': 2500
}

#only Screw
robot2 = {
    'id': 'robot2',
    'actions': [
        'NavigateToLocation',
        'ScanObject',
        'GraspObject',
        'ReleaseObject',
        'Screw'
    ],  
    'size': {'width': 800, 'height': 2100},
    'max_reach_height': 3000
}

#only testing
robot3 = {
    'id': 'robot3',
    'actions': [
        'NavigateToLocation',
        'TurnSwitchOn',
        'TurnSwitchOff',
    ],  
    'size': {'width': 900, 'height': 2200},
    'max_reach_height': 3500
}

#only grasp/release
robot4 = {
    'id': 'robot4',
    'actions': [
        'NavigateToLocation',
        'GraspObject',
        'ReleaseObject'
    ],
    'size': {'width': 1600, 'height': 2400},
    'max_reach_height': 3700
}

#only clean
robot5 = {
    'id': 'robot5',
    'actions': [
        'NavigateToLocation',
        'GraspObject',
        'ReleaseObject',
        'CleanSurface'
    ],
    'size': {'width': 1400, 'height': 2000},
    'max_reach_height': 2800
}

#clean and paint
robot6 = {
    'id': 'robot6',
    'actions': [
        'NavigateToLocation',
        'GraspObject',
        'ReleaseObject',
        'CleanSurface',
        'PaintSurface'
    ],
    'size': {'width': 750, 'height': 2050},
    'max_reach_height': 2300
}

#ALL
robot7 = {
    'id': 'robot7',
    'actions': [
        'NavigateToLocation',
        'ScanObject',
        'GraspObject',
        'ReleaseObject',
        'TurnSwitchOn',
        'TurnSwitchOff',
        'Unscrew',
        'Screw',
        'CleanSurface',
        'PaintSurface'
    ],
    'size': {'width': 800, 'height': 2000},
    'max_reach_height': 2200
}

#without scanning
robot8 = {
    'id': 'robot8',
    'actions': [
        'NavigateToLocation',
        'GraspObject',
        'ReleaseObject',
        'TurnSwitchOn',
        'TurnSwitchOff',
        'Unscrew',
        'Screw',
        'CleanSurface',
        'PaintSurface'
    ],
    'size': {'width': 700, 'height': 1950},
    'max_reach_height': 2600
}

#without grasp/release
robot9 = {
    'id': 'robot9',
    'actions': [
        'NavigateToLocation',
        'ScanObject',
        'TurnSwitchOn',
        'TurnSwitchOff',
        'Unscrew',
        'Screw',
        'CleanSurface',
        'PaintSurface'
    ],
    'size': {'width': 1700, 'height': 2500},
    'max_reach_height': 3200
}

#without screw/unscrew
robot10 = {
    'id': 'robot10',
    'actions': [
        'NavigateToLocation',
        'ScanObject',
        'GraspObject',
        'ReleaseObject',
        'TurnSwitchOn',
        'TurnSwitchOff',
        'CleanSurface',
        'PaintSurface'
    ],
    'size': {'width': 500, 'height': 1800},
    'max_reach_height': 4000
}

robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9, robot10]
