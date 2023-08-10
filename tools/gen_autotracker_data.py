#!/usr/bin/python3

import sys, os
from enum import IntEnum
from copy import copy

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))
sys.path.insert(0, os.path.dirname(sys.path[0]))

from logic.logic import Logic
from rom.flavor import RomFlavor
from rom.rom import RealROM, pc_to_snes, snes_to_pc
from rom.leveldata import Room
from utils.doorsmanager import DoorsManager, plmFacing
from graph.graph_utils import getAccessPoint, GraphUtils
from utils.utils import removeChars

# for vanilla the vanilla rom + area_ids
# for mirror the vanilla rom + mirror base patchs (in RomPatcher.IPSPatches['Logic']['mirror']) + area_ids

rom = RealROM(sys.argv[1])
logic = sys.argv[2]

Logic.factory(logic)
RomFlavor.factory()
locations = Logic.locations()

locationsDict = {pc_to_snes(loc.Address): loc for loc in locations}
locationsName = set([loc.Name for loc in locations])
accessPoints = Logic.accessPoints()
patchDict = RomFlavor.patchAccess.getDictPatches()
additionalPLMs = RomFlavor.patchAccess.getAdditionalPLMs()

# from vanilla area to varia area, matching the bounding box of varia area.
# offset in screens.
# offset is removed from position on vanilla map.
mapsOffsets = {
    "vanilla": {
        "Crateria": {
            # start of the varia map in the vanilla map
            "Crateria": (6, 0),
            # elevator to green brinstar
            # on crateria vanilla map: 6,8
            # on varia green bt map: 4,0
            "GreenBrinstar": (2, 8),
            # elevator to red brinstar
            # on crateria vanilla map: 34,7
            # on varia red bt map: 14,0
            "RedBrinstar": (20, 7),
            # wrecked ship east part
            # on crateria vanilla map: 49,0
            # on varia wreckedship map: 18,0
            "WreckedShip": (31, 0),
            # TODO::special case for 94fd too which has 4 empty screen on top ?
            # special case for west part
            # on crateria vanilla map: 38,0
            # on varia wreckedship map: 0,0
            "93fe": (38, 0),
            # elevator to east maridia
            # on crateria vanilla map: 53,9
            # on varia east maridia map: 16,0
            "EastMaridia": (37, 9),
            # G4 access
            # on crateria vanilla map: 12,8
            # on varia tourian map: 4,0
            "Tourian": (8, 8),
        },
        "Brinstar": {
            # on brinstar vanilla map: 5,0
            # on varia green bt map: 0,2
            "GreenBrinstar": (5,-2),
            # on brinstar vanilla map: 21,8
            # on varia crateria bt map: 11,27
            "Crateria": (10, -19),
            # on brinstar vanilla map: 35,7
            # on varia red bt map: 12,5
            "RedBrinstar": (23, 2),
            # on brinstar vanilla map: 43,18
            # on varia kraid's lair map: 0,0
            "KraidLair": (43, 18),
            # on brinstar vanilla map: 41,18
            # on varia norfair map: 8,0
            "UpperNorfair": (33, 18),
            # kraid
            # on brinstar vanilla map: 57,19
            # on varia kraid map: 2,1
            "a6e2": (55, 18),
            "a59f": (55, 18),
        },
        "Norfair": {
            # on norfair vanilla map: 2,0
            # on varia up norf map: 0,2
            "UpperNorfair": (2, -2),
            # on norfair vanilla map: 9,10
            # on varia croc map: 6,0
            "Crocomire": (3, 10),
            # on norfair vanilla map: 20,10
            # on varia lo norf map: 5,7
            "LowerNorfair": (15, 3),
            # ridley
            # on norfair vanilla map: 22,17
            # on varia ridley map: 0,1
            "b698": (22, 16),
            "b32e": (22, 16),
        },
        "WreckedShip": {
            # on wreckedship vanilla map: 10,10
            # on varia wreckedship map: 6,0
            "WreckedShip": (4, 10),
            # phantoon
            # on WS vanilla map: 19,19
            # on varia phantoon map: 0,0
            "cd13": (19, 19),
        },
        "Maridia": {
            # on maridia vanilla map: 10,18
            # on varia red bt map: 15,16
            "RedBrinstar": (-5, 2),
            # on maridia vanilla map: 10,9
            # on varia w maridia map: 0,5
            "WestMaridia": (10, 4),
            # on maridia vanilla map: 25,0
            # on varia e maridia map: 7,3
            "EastMaridia": (18, -3),
            # draygon
            # on maridia vanilla map: 38,10
            # on varia draygon map: 0,1
            "da60": (38, 9),
            "d9aa": (38, 9),
        },
        "Tourian": {
            # on tourian vanilla map: 20,9
            # on varia tourian map: 9,1
            "Tourian": (11, 8)
        },
        # not displayed on the tracker
        "Ceres": {
            "Ceres": (0, 0)
        },
    },
    "mirror": {
        "Crateria": {
            # start of the varia map in the vanilla mirrored map
            # on crateria vanilla map: 25
            # on varia crateria map: 0
            "Crateria": (25,0),
            # elevator to green brinstar
            # on crateria vanilla map: 56
            # on varia green bt map: 23
            "GreenBrinstar": (33, 8),
            # elevator to red brinstar
            # on crateria vanilla map: 28
            # on varia red bt map: 6
            "RedBrinstar": (22,7),
            # wrecked ship east part
            # on crateria vanilla map: 7
            # on varia wreckedship map: 1
            "WreckedShip": (6,0),
            # TODO::special case for 94fd too which has 4 empty screen on top ?
            # special case for west part
            # on crateria vanilla map: 17
            # on varia wreckedship map: 18
            "93fe": (-1,0),
            # elevator to east maridia
            # on crateria vanilla map: 10
            # on varia east maridia map: 8
            "EastMaridia": (2, 9),
            # G4 access
            # on crateria vanilla map: 45
            # on varia tourian map: 1
            "Tourian": (44,8),
        },
        "Brinstar": {
            # on brinstar vanilla map: 31
            # on varia green bt map: 0
            "GreenBrinstar": (31,-2),
            # on brinstar vanilla map: 31
            # on varia crateria bt map: 8
            "Crateria": (23,-19),
            # on brinstar vanilla map: 26
            # on varia red bt map: 6
            "RedBrinstar": (20, 2),
            # on brinstar vanilla map: 9
            # on varia kraid's lair map: 0
            "KraidLair": (9, 18),
            # on brinstar vanilla map: 22
            # on varia norfair map: 27
            "UpperNorfair": (-5, 18),
            # kraid
            # on brinstar vanilla map: 6,19
            # on varia kraid map: 0,1
            "a6e2": (6, 18),
            "a59f": (6, 18),
        },
        "Norfair": {
            # on norfair vanilla map: 25
            # on varia up norf map: 0
            "UpperNorfair": (25, -2),
            # on norfair vanilla map: 54
            # on varia croc map: 10
            "Crocomire": (44, 10),
            # on norfair vanilla map: 25
            # on varia lo norf map: 0
            "LowerNorfair": (25, 3),
            # ridley
            # on norfair vanilla map: 40,17
            # on varia ridley map: 1,1
            "b698": (39, 16),
            "b32e": (39, 16),
        },
        "WreckedShip": {
            # on wreckedship vanilla map: 33
            # on varia wreckedship map: 8
            "WreckedShip": (25, 10),
            # phantoon
            # on WS vanilla map: 35,19
            # on varia phantoon map: 0,0
            "cd13": (35, 19),
        },
        "Maridia": {
            # on maridia vanilla map: 55
            # on varia red bt map: 4
            "RedBrinstar": (51, 2),
            # on maridia vanilla map: 56
            # on varia w maridia map: 11
            "WestMaridia": (45, 4),
            # on maridia vanilla map: 24
            # on varia e maridia map: 0
            "EastMaridia": (24, -3),
            # draygon
            # on maridia vanilla map: 29,10
            # on varia draygon map: 2,1
            "da60": (27, 9),
            "d9aa": (27, 9),
        },
        "Tourian": {
            # on tourian vanilla map: 42
            # on varia tourian map: 0
            "Tourian": (42, 8),
            # TODO::special case for vanilla MB room and new MB room
        },
        "Ceres": {
            "Ceres": (0, 0)
        },
    }
}

# size in screens
variaMaps = {
    "Ceres": {
        "size": (-1, -1)
    },
    "Crateria": {
        "size": (31, 31)
    },
    "GreenBrinstar": {
        "size": (28, 16),
    },
    "RedBrinstar": {
        "size": (21, 18),
    },
    "WreckedShip": {
        "size": (26, 10),
    },
    "KraidLair": {
        "size": (15, 2),
    },
    "UpperNorfair": {
        "size": (36, 13),
    },
    "LowerNorfair": {
        "size": (23, 15),
    },
    "Crocomire": {
        "size": (17, 8),
    },
    "WestMaridia": {
        "size": (12, 14),
    },
    "EastMaridia": {
        "size": (25, 20),
    },
    "Tourian": {
        "size": (11, 14),
    },

    "Phantoon": {
        "size": (1, 1),
    },
    "Draygon": {
        "size": (3, 2),
    },
    "Kraid": {
        "size": (3, 2),
    },
    "Ridley": {
        "size": (2, 2),
    },
}

# each area map is 64x32 screens in game, in two 32x32 pages
# vanilla area id
class Area(IntEnum):
    Crateria = 0
    Brinstar = 1
    Norfair = 2
    WreckedShip = 3
    Maridia = 4
    Tourian = 5
    Ceres = 6
    Debug = 7

class VariaArea(IntEnum):
    Ceres = 0
    Crateria = 1
    GreenBrinstar = 2
    RedBrinstar = 3
    WreckedShip = 4
    KraidLair = 5
    UpperNorfair = 6
    Crocomire = 7
    LowerNorfair = 8
    WestMaridia = 9
    EastMaridia = 10
    Tourian = 11

vanillaMaps = {
    "Crateria": [[["____"]*32 for y in range(32)] for page in range(2)],
    "Brinstar": [[["____"]*32 for _ in range(32)] for __ in range(2)],
    "Norfair": [[["____"]*32 for _ in range(32)] for __ in range(2)],
    "WreckedShip": [[["____"]*32 for _ in range(32)] for __ in range(2)],
    "Maridia": [[["____"]*32 for _ in range(32)] for __ in range(2)],
    "Tourian": [[["____"]*32 for _ in range(32)] for __ in range(2)],
    "Ceres": [[["____"]*32 for _ in range(32)] for __ in range(2)],
}

# rooms positions on the map
jsrooms = {}
jsrooms['vanilla'] = {
    '91f8': {'name': 'Landing Site'},
    '92b3': {'name': 'Gauntlet Entrance'},
    '92fd': {'name': 'Parlor and Alcatraz'},
    '93aa': {'name': 'Crateria Power Bomb Room'},
    '93d5': {'name': '[Parlor Save Room]'},
    '93fe': {'name': 'West Ocean', 'graphArea': 'WreckedShip', 'nearestAP': 'westOceanLeft'},
    '9461': {'name': 'Bowling Alley Path'},
    '948c': {'name': 'Crateria Keyhunter Room', 'graphArea': 'Crateria', 'nearestAP': 'keyhunterRoomBottom'},
    '94cc': {'name': '[Elevator to Maridia]'},
    # but room starts 4 screens before on Y
    '94fd': {'name': 'East Ocean'},
    '9552': {'name': 'Forgotten Highway Kago Room'},
    '957d': {'name': 'Crab Maze', 'graphArea': 'WreckedShip', 'nearestAP': 'crabMazeLeft'},
    '95a8': {'name': '[Crab Maze to Elevator]', 'graphArea': 'EastMaridia', 'nearestAP': 'leCoudeRight'},
    '95d4': {'name': 'Crateria Tube'},
    '95ff': {'name': 'The Moat', 'graphArea': 'Crateria', 'nearestAP': 'moatRight'},
    '962a': {'name': '[Elevator to Red Brinstar]', 'graphArea': 'RedBrinstar', 'nearestAP': 'redBrinstarElevator'},
    '965b': {'name': 'Gauntlet Energy Tank Room'},
    '968f': {'name': '[West Ocean Geemer Corridor]'},
    '96ba': {'name': 'Climb'},
    '975c': {'name': 'Pit Room [Old Mother Brain Room]'},
    '97b5': {'name': '[Elevator to Blue Brinstar]'},
    '9804': {'name': 'Bomb Torizo Room'},
    '9879': {'name': 'Flyway'},
    '98e2': {'name': 'Pre-Map Flyway'},
    '990d': {'name': 'Terminator Room'},
    '9938': {'name': '[Elevator to Green Brinstar]', 'graphArea': 'GreenPinkBrinstar', 'nearestAP': 'greenBrinstarElevator'},
    '9969': {'name': 'Lower Mushrooms', 'graphArea': 'Crateria', 'nearestAP': 'lowerMushroomsLeft'},
    '9994': {'name': 'Crateria Map Room'},
    '99bd': {'name': 'Green Pirates Shaft', 'graphArea': 'Crateria', 'nearestAP': 'greenPiratesShaftBottomRight'},
    '99f9': {'name': 'Crateria Super Room'},
    '9a44': {'name': 'Final Missile Bombway'},
    '9a90': {'name': 'The Final Missile'},
    '9ad9': {'name': 'Green Brinstar Main Shaft [etecoon room]'},
    '9b5b': {'name': 'Spore Spawn Super Room'},
    '9b9d': {'name': 'Brinstar Pre-Map Room'},
    '9bc8': {'name': 'Early Supers Room'},
    '9c07': {'name': 'Brinstar Reserve Tank Room'},
    '9c35': {'name': 'Brinstar Map Room'},
    '9c5e': {'name': 'Green Brinstar Fireflea Room'},
    '9c89': {'name': '[Green Brinstar Missile Station]'},
    '9cb3': {'name': 'Dachora Room'},
    '9d19': {'name': 'Big Pink'},
    '9d9c': {'name': 'Spore Spawn Keyhunter Room'},
    '9dc7': {'name': 'Spore Spawn Room'},
    '9e11': {'name': 'Pink Brinstar Power Bomb Room'},
    '9e52': {'name': 'Green Hill Zone', 'graphArea': 'GreenPinkBrinstar', 'nearestAP': 'greenHillZoneTopRight'},
    '9e9f': {'name': 'Morph Ball Room', 'graphArea': 'Crateria', 'nearestAP': 'morphBallRoomLeft'},
    '9f11': {'name': 'Construction Zone'},
    '9f64': {'name': 'Blue Brinstar Energy Tank Room'},
    '9fba': {'name': 'Noob Bridge', 'graphArea': 'GreenPinkBrinstar', 'nearestAP': 'noobBridgeRight'},
    '9fe5': {'name': 'Green Brinstar Beetom Room'},
    'a011': {'name': 'Etecoon Energy Tank Room'},
    'a051': {'name': 'Etecoon Super Room'},
    'a07b': {'name': '[Dachora Room Energy Charge Station]'},
    'a0a4': {'name': 'Spore Spawn Farming Room'},
    'a0d2': {'name': 'Waterway Energy Tank Room'},
    'a107': {'name': 'First Missile Room'},
    'a130': {'name': 'Pink Brinstar Hopper Room'},
    'a15b': {'name': 'Hopper Energy Tank Room'},
    'a184': {'name': '[Spore Spawn Save Room]'},
    'a1ad': {'name': 'Blue Brinstar Boulder Room'},
    'a1d8': {'name': 'Blue Brinstar Double Missile Room'},
    'a201': {'name': '[Green Brinstar Main Shaft Save Room]'},
    'a22a': {'name': '[Etecoon Save Room]'},
    'a253': {'name': 'Red Tower', 'graphArea': 'RedBrinstar', 'nearestAP': 'redTowerTopLeft'},
    'a293': {'name': 'Red Brinstar Fireflea Room'},
    'a2ce': {'name': 'X-Ray Scope Room'},
    'a2f7': {'name': 'Hellway'},
    'a322': {'name': 'Caterpillar Room', 'graphArea': 'RedBrinstar', 'nearestAP': 'caterpillarRoomTopRight'},
    'a37c': {'name': 'Beta Power Bomb Room'},
    'a3ae': {'name': 'Alpha Power Bomb Room'},
    'a3dd': {'name': 'Bat Room'},
    'a408': {'name': 'Below Spazer'},
    'a447': {'name': 'Spazer Room'},
    'a471': {'name': 'Warehouse Zeela Room', 'graphArea': 'Kraid', 'nearestAP': 'warehouseZeelaRoomLeft'},
    'a4b1': {'name': 'Warehouse Energy Tank Room'},
    'a4da': {'name': 'Warehouse Keyhunter Room'},
    'a521': {'name': 'Baby Kraid Room'},
    'a56b': {'name': 'Kraid Eye Door Room', 'graphArea': 'Kraid', 'nearestAP': 'kraidRoomOut'},
    'a59f': {'name': 'Kraid Room'},
    'a5ed': {'name': 'Statues Hallway', 'graphArea': 'Tourian', 'nearestAP': 'goldenFour'},
    'a618': {'name': '[Red Tower Energy Charge Station]'},
    'a641': {'name': '[Kraid Recharge Station]'},
    'a66a': {'name': 'Statues Room'},
    'a6a1': {'name': 'Warehouse Entrance', 'graphArea': 'Norfair', 'nearestAP': 'MULTI',
             'screens': [['warehouseEntranceLeft', 'warehouseEntranceRight', 'warehouseEntranceRight'],
                         ['warehouseEntranceLeft', 'warehouseEntranceRight', 'warehouseEntranceRight']]},
    'a6e2': {'name': 'Varia Suit Room'},
    'a70b': {'name': '[Kraid Save Room]'},
    'a734': {'name': '[Caterpillar Save Room]'},
    'a75d': {'name': 'Ice Beam Acid Room'},
    'a788': {'name': 'Cathedral'},
    'a7b3': {'name': 'Cathedral Entrance'},
    'a7de': {'name': 'Business Center'},
    'a815': {'name': 'Ice Beam Gate Room'},
    'a865': {'name': 'Ice Beam Tutorial Room'},
    'a890': {'name': 'Ice Beam Room'},
    'a8b9': {'name': 'Ice Beam Snake Room'},
    'a8f8': {'name': 'Crumble Shaft'},
    'a923': {'name': 'Crocomire Speedway', 'graphArea': 'Norfair', 'nearestAP': 'crocomireSpeedwayBottom'},
    'a98d': {'name': 'Crocomire Room', 'graphArea': 'Crocomire', 'nearestAP': 'crocomireRoomTop'},
    'a9e5': {'name': 'Hi Jump Boots Room'},
    'aa0e': {'name': 'Crocomire Escape'},
    'aa41': {'name': 'Hi Jump Energy Tank Room'},
    'aa82': {'name': 'Post Crocomire Farming Room'},
    'aab5': {'name': '[Post Crocomire Save Room]'},
    'aade': {'name': 'Post Crocomire Power Bomb Room'},
    'ab07': {'name': 'Post Crocomire Shaft'},
    'ab3b': {'name': 'Post Crocomire Missile Room'},
    'ab64': {'name': 'Grapple Tutorial Room 3'},
    'ab8f': {'name': 'Post Crocomire Jump Room'},
    'abd2': {'name': 'Grapple Tutorial Room 2'},
    'ac00': {'name': 'Grapple Tutorial Room 1'},
    'ac2b': {'name': 'Grapple Beam Room'},
    'ac5a': {'name': 'Norfair Reserve Tank Room'},
    'ac83': {'name': 'Green Bubbles Missile Room'},
    'acb3': {'name': 'Bubble Mountain'},
    'acf0': {'name': 'Speed Booster Hall'},
    'ad1b': {'name': 'Speed Booster Room'},
    'ad5e': {'name': 'Single Chamber', 'graphArea': 'Norfair', 'nearestAP': 'singleChamberTopRight'},
    'adad': {'name': 'Double Chamber'},
    'adde': {'name': 'Wave Beam Room'},
    'ae07': {'name': 'Spiky Platforms Tunnel'},
    'ae32': {'name': 'Volcano Room'},
    'ae74': {'name': 'Kronic Boost Room', 'graphArea': 'Norfair', 'nearestAP': 'kronicBoostRoomBottomLeft'},
    'aeb4': {'name': 'Magdollite Tunnel'},
    'aedf': {'name': 'Purple Shaft'},
    'af14': {'name': 'Lava Dive Room', 'graphArea': 'LowerNorfair', 'nearestAP': 'lavaDiveRight'},
    'af3f': {'name': '[Elevator to Lower Norfair]'},
    'af72': {'name': 'Upper Norfair Farming Room'},
    'afa3': {'name': 'Rising Tide'},
    'afce': {'name': 'Acid Snakes Tunnel'},
    'affb': {'name': 'Spiky Acid Snakes Tunnel'},
    'b026': {'name': '[Crocomire Recharge Room]'},
    'b051': {'name': 'Purple Farming Room'},
    'b07a': {'name': 'Bat Cave'},
    'b0b4': {'name': 'Norfair Map Room'},
    'b0dd': {'name': '[Bubble Mountain Save Room]'},
    'b106': {'name': 'Frog Speedway'},
    'b139': {'name': 'Red Pirate Shaft'},
    'b167': {'name': '[Business Center Save Room]'},
    'b192': {'name': '[Crocomire Save Room]'},
    'b1bb': {'name': '[Elevator Save Room]'},
    'b1e5': {'name': 'Acid Statue Room'},
    'b236': {'name': 'Main Hall'},
    'b283': {'name': 'Golden Torizo Room'},
    'b2da': {'name': 'Fast Ripper Room'},
    'b305': {'name': '[Screw Attack Energy Charge Room]'},
    'b32e': {'name': 'Ridley Room'},
    'b37a': {'name': 'Lower Norfair Farming Room', 'graphArea': 'LowerNorfair', 'nearestAP': 'ridleyRoomOut'},
    'b3a5': {'name': 'Fast Pillars Setup Room'},
    'b40a': {'name': 'Mickey Mouse Room'},
    'b457': {'name': 'Pillar Room'},
    'b482': {'name': 'Plowerhouse Room'},
    'b4ad': {'name': 'The Worst Room In The Game'},
    'b4e5': {'name': 'Amphitheatre'},
    'b510': {'name': 'Lower Norfair Spring Ball Maze Room'},
    'b55a': {'name': 'Lower Norfair Escape Power Bomb Room'},
    'b585': {'name': 'Red Keyhunter Shaft'},
    'b5d5': {'name': 'Wasteland'},
    'b62b': {'name': 'Metal Pirates Room'},
    'b656': {'name': 'Three Muskateers Room', 'graphArea': 'LowerNorfair', 'nearestAP': 'threeMuskateersRoomLeft'},
    'b698': {'name': 'Ridley Tank Room'},
    'b6c1': {'name': 'Screw Attack Room'},
    'b6ee': {'name': 'Lower Norfair Fireflea Room'},
    'b741': {'name': '[Red Keyhunter Shaft Save Room]'},
    'c98e': {'name': 'Bowling Alley'},
    'ca08': {'name': 'Wrecked Ship Entrance'},
    'ca52': {'name': 'Attic'},
    'caae': {'name': 'Wrecked Ship East Missile Room'},
    'caf6': {'name': 'Wrecked Ship Main Shaft'},
    'cb8b': {'name': 'Spiky Death Room'},
    'cbd5': {'name': 'Electric Death Room'},
    'cc27': {'name': 'Wrecked Ship Energy Tank Room'},
    'cc6f': {'name': 'Basement', 'graphArea': 'WreckedShip', 'nearestAP': 'phantoonRoomOut'},
    'cccb': {'name': 'Wrecked Ship Map Room'},
    'cd13': {'name': 'Phantoon Room'},
    'cd5c': {'name': 'Sponge Bath'},
    'cda8': {'name': 'Wrecked Ship West Super Room'},
    'cdf1': {'name': 'Wrecked Ship East Super Room'},
    'ce40': {'name': 'Gravity Suit Room'},
    'ce8a': {'name': '[Wrecked Ship Save Room]'},
    'ced2': {'name': '[Glass Tunnel Save Room]'},
    'cefb': {'name': 'Glass Tunnel', 'graphArea': 'RedBrinstar', 'nearestAP': 'glassTunnelTop'},
    'cf54': {'name': 'West Tunnel'},
    'cf80': {'name': 'East Tunnel', 'graphArea': 'RedBrinstar', 'nearestAP': 'MULTI',
             'screens': [['eastTunnelTopRight', 'eastTunnelTopRight', 'eastTunnelTopRight', 'eastTunnelTopRight'],
                         ['eastTunnelRight',    'x',                  'x',                  'x']]},
    'cfc9': {'name': 'Main Street', 'graphArea': 'WestMaridia', 'nearestAP': 'mainStreetBottom'},
    'd017': {'name': 'Fish Tank'},
    'd055': {'name': 'Mama Turtle Room'},
    'd08a': {'name': 'Crab Tunnel'},
    'd0b9': {'name': 'Mt. Everest'},
    'd104': {'name': 'Red Fish Room', 'graphArea': 'WestMaridia', 'nearestAP': 'redFishRoomLeft'},
    'd13b': {'name': 'Watering Hole'},
    'd16d': {'name': 'Northwest Maridia Bug Room'},
    'd1a3': {'name': 'Crab Shaft', 'graphArea': 'WestMaridia', 'nearestAP': 'crabShaftRight'},
    'd1dd': {'name': 'Pseudo Plasma Spark Room'},
    'd21c': {'name': 'Crab Hole', 'graphArea': 'WestMaridia', 'nearestAP': 'crabHoleBottomLeft'},
    'd252': {'name': '[Tunnel to West Sand Hall]'},
    'd27e': {'name': 'Plasma Tutorial Room'},
    'd2aa': {'name': 'Plasma Room'},
    'd2d9': {'name': 'Thread The Needle Room'},
    'd30b': {'name': 'Maridia Elevator Room'},
    'd340': {'name': 'Plasma Spark Room'},
    'd387': {'name': 'Plasma Climb'},
    'd3b6': {'name': 'Maridia Map Room'},
    'd3df': {'name': '[Maridia Elevator Save Room]'},
    'd408': {'name': '[Vertical Tube]'},
    'd433': {'name': 'Bug Sand Hole'},
    'd461': {'name': 'West Sand Hall'},
    'd48e': {'name': 'Oasis'},
    'd4c2': {'name': 'East Sand Hall'},
    'd4ef': {'name': 'West Sand Hole'},
    'd51e': {'name': 'East Sand Hole'},
    'd54d': {'name': '[West Sand Fall]'},
    'd57a': {'name': '[East Sand Fall]'},
    'd5a7': {'name': 'Aqueduct', 'graphArea': 'EastMaridia', 'nearestAP': 'aqueductTopLeft'},
    'd5ec': {'name': 'Butterfly Room'},
    'd617': {'name': 'Botwoon Hallway'},
    'd646': {'name': 'Pants Room'},
    'd69a': {'name': '[Pants Room West half]'},
    'd6d0': {'name': 'Spring Ball Room'},
    'd6fd': {'name': 'Below Botwoon Energy Tank'},
    'd72a': {'name': 'Colosseum'},
    'd765': {'name': '[Aqueduct Save Room]'},
    'd78f': {'name': 'The Precious Room', 'graphArea': 'EastMaridia', 'nearestAP': 'draygonRoomOut'},
    'd7e4': {'name': 'Botwoon Energy Tank Room'},
    'd81a': {'name': '[Colosseum Save Room]'},
    'd845': {'name': '[Halfie Climb Missile Station]'},
    'd86e': {'name': '[Bug Sand Fall]'},
    'd898': {'name': '[Botwoon Sand Fall]'},
    'd8c5': {'name': 'Shaktool Room'},
    'd913': {'name': 'Halfie Climb Room'},
    'd95e': {'name': 'Botwoon Room'},
    'd9aa': {'name': 'Space Jump Room'},
    'd9d4': {'name': '[Colosseum Energy Charge Room]'},
    'd9fe': {'name': 'Cactus Alley [West]'},
    'da2b': {'name': 'Cactus Alley [East]'},
    'da60': {'name': 'Draygon Room'},
    'daae': {'name': 'Tourian First Room'},
    'dae1': {'name': 'Metroid Room 1'},
    'db31': {'name': 'Metroid Room 2'},
    'db7d': {'name': 'Metroid Room 3'},
    'dbcd': {'name': 'Metroid Room 4'},
    'dc19': {'name': 'Blue Hopper Room'},
    'dc65': {'name': 'Dust Torizo Room'},
    'dcb1': {'name': 'Big Boy Room'},
    'dcff': {'name': 'Seaweed Room'},
    'dd2e': {'name': 'Tourian Recharge Room'},
    'dd58': {'name': 'Mother Brain Room'},
    'ddc4': {'name': 'Tourian Eye Door Room'},
    'ddf3': {'name': 'Rinka Shaft'},
    'de23': {'name': '[Mother Brain Save Room]'},
    'de4d': {'name': 'Tourian Escape Room 1'},
    'de7a': {'name': 'Tourian Escape Room 2'},
    'dea7': {'name': 'Tourian Escape Room 3'},
    'dede': {'name': 'Tourian Escape Room 4'},
    'df1b': {'name': '[Tourian First Save Room]'},
    'df45': {'name': '[Ceres Elevator Room]'},
    'df8d': {'name': '[Ceres Jump Tutorial Room]'},
    'dfd7': {'name': '[Ceres Staircase Room]'},
    'e021': {'name': '[Ceres Dead Scientists Room]'},
    'e06b': {'name': '[Ceres Last Corridor]'},
    'e0b5': {'name': '[Ceres Ridley Room]'},
}
jsrooms["mirror"] = copy(jsrooms["vanilla"])
jsrooms["mirror"]['fd40'] = {'name': 'Mirrortroid Mother Brain Room'}

def getVariaArea(room):
    specificRooms = {
        "a6e2": "Kraid",
        "a59f": "Kraid",
        "b698": "Ridley",
        "b32e": "Ridley",
        "cd13": "Phantoon",
        "da60": "Draygon",
        "d9aa": "Draygon"
    }
    roomAddr = hex(pc_to_snes(room.dataAddr) & 0xffff)[2:]
    if roomAddr in specificRooms:
        return specificRooms[roomAddr]
    else:
        return VariaArea(room.variaArea).name

# loop on room, for each get it's area, map x/y, width/height, plms
# loop on plms to get doors/items
# for door get direction and screen x/y
# for item get screen x/y
rooms = {}
for roomAddrS in jsrooms[logic]:
    roomAddrS = int('0x8f'+roomAddrS, 16)
    roomAddrPC = snes_to_pc(roomAddrS)
    room = Room(rom, roomAddrPC)
    rooms[roomAddrS] = room

    # add room in map
    displayAddr = hex(roomAddrS & 0xffff)[2:]

    area = Area(room.area).name
    variaArea = getVariaArea(room)
    for y in range(room.height):
        for x in range(room.width):
            if room.mapX + x < 32:
                page = 0
            else:
                page = 1
            vanillaMaps[area][page][room.mapY + y][room.mapX + x - (0 if page == 0 else 32)] = displayAddr

    #print("room {} area: {} variaarea: {} room name: {}".format(hex(roomAddrS), area, variaArea, jsrooms[logic][hex(roomAddrS&0xffff)[2:]]['name']))

# display maps
#for vanillaArea in ['Crateria', 'Brinstar', 'Norfair', 'WreckedShip', 'Maridia', 'Tourian']:
#    print(vanillaArea)
#    for y in range(32):
#        print(vanillaMaps[vanillaArea][0][y] + vanillaMaps[vanillaArea][1][y])

# get for each room its position on the varia area maps
for roomShortAddr, data in jsrooms[logic].items():
    roomAddrS = 0x8f0000 + int('0x'+roomShortAddr, 16)
    room = rooms[roomAddrS]
    vanillaArea = Area(room.area).name
    variaArea = getVariaArea(room)
    (x, y) = (room.mapX, room.mapY)
    if roomShortAddr in mapsOffsets[logic][vanillaArea]:
        offsets = mapsOffsets[logic][vanillaArea][roomShortAddr]
    else:
        offsets = mapsOffsets[logic][vanillaArea][variaArea]
    x -= offsets[0]
    y -= offsets[1]
    data["left"] = x
    data["top"] = y
    data["vanillaArea"] = vanillaArea
    data["variaArea"] = variaArea

print("<"*32+"rooms positions on varia area maps for tracker.html:"+"<"*32)
print("rooms['{}']: {{".format(logic))
for addr, data in jsrooms[logic].items():
    print("    '{}': {},".format(addr, data))
print("};")
print(">"*32+"rooms positions on varia area maps for tracker.html "+">"*32)
print("")

# match room plm and loc address
items = {}
foundLocs = set()
for roomAddrS, room in rooms.items():
    for itemAddr in room.items:
        # old croc etank
        if itemAddr == 0x8f8ba4 and logic == 'mirror':
            continue
        loc = locationsDict[itemAddr]
        itemPlm = room.plms[itemAddr]
        items[itemAddr] = {'loc': loc, 'itemPlm': itemPlm, 'room': roomAddrS}
        foundLocs.add(loc.Name)

print("<"*32+" plm list:"+"<"*32)
for itemAddr, values in items.items():
    print("{}: room: {} loc: {} x: {} y: {}".format(hex(itemAddr), hex(values['room']) , values['loc'].Name, values['itemPlm'][1], values['itemPlm'][2]))

missingLocs = locationsName - foundLocs
print("missingLocs: {}".format(missingLocs))
print(">"*32+" plm list "+">"*32)
print("")

# match room plm and doors addresses
doorsDict = {door.address: door for door in DoorsManager.doors.values()}
doorsName = set([door.name for door in DoorsManager.doors.values()])

doors = {}
foundDoors = set()
for roomAddrS, room in rooms.items():
    for doorAddr in room.doors:
        # we don't have all doors in varia (like some grey doors in some states)
        if doorAddr not in doorsDict:
            continue
        door = doorsDict[doorAddr]
        doorPlm = room.plms[doorAddr]
        doors[doorAddr] = {'door': door, 'doorPlm': doorPlm, 'room': roomAddrS, 'facing': plmFacing[doorPlm[0]]}
        foundDoors.add(door.name)

print("<"*32+" door list:"+"<"*32)
for doorAddr, values in doors.items():
    print("{}: room: {} door: {} x: {} y: {} facing: {}".format(hex(doorAddr), hex(values['room']) , values['door'].name, values['doorPlm'][1], values['doorPlm'][2], values['facing']))

missingDoors = doorsName - foundDoors
print("missingDoors: {}".format(missingDoors))
print(">"*32+" door list "+">"*32)
print("")


# object in tiles coordinates in room
def getMapPos(roomPos, objPos):
    (roomX, roomY) = roomPos
    (objX, objY) = objPos
    x = roomX + objX // 0x10
    y = roomY + objY // 0x10
    byteIndex = (y + (x & 0x20)) * 4 + (x & 0x1F) // 8
    # first line of map is unused, so add 4 to ignore it (8 bytes per lines, but 4 in each page)
    byteIndex += 4
    bitMask = 0x80 >> (x & 7)
    return (byteIndex, bitMask)

print("<"*32+" for solver/interactivesolver.py:"+"<"*32)
print("    nothingScreens['{}'] = {{".format(logic))
for item in items.values():
    room = rooms[item['room']]
    roomX = room.mapX
    roomY = room.mapY
    itemPlm = item['itemPlm']
    itemX = itemPlm[1]
    itemY = itemPlm[2]
    (byteIndex, bitMask) = getMapPos((roomX, roomY), (itemX, itemY))

    # "Energy Tank, Gauntlet": {"byteIndex": 14, "bitMask": 64, "room": 0x965b, "area": "Crateria"},
    print('        "{}": {{"byteIndex": {}, "bitMask": {}, "room": {}, "area": "{}"}},'.format(
        item['loc'].Name, byteIndex, bitMask, hex(pc_to_snes(room.dataAddr) & 0xffff), Area(room.area).name))
print("    }")


print("    doorsScreen['{}'] = {{".format(logic))
for door in doors.values():
    doorObj = door['door']
    room = rooms[door['room']]
    roomX = room.mapX
    roomY = room.mapY
    doorPlm = door['doorPlm']
    doorX = doorPlm[1]
    doorY = doorPlm[2]
    (byteIndex, bitMask) = getMapPos((roomX, roomY), (doorX, doorY))

    # 'LandingSiteRight': {"byteIndex": 23, "bitMask": 1, "room": 0x91f8, "area": "Crateria"},
    print('        "{}": {{"byteIndex": {}, "bitMask": {}, "room": {}, "area": "{}"}},'.format(
        doorObj.name, byteIndex, bitMask, hex(pc_to_snes(room.dataAddr) & 0xffff), Area(room.area).name))
print("    }")

accessPointsIds = {
    "areaAccessPoints": [
        "Lower Mushrooms Left", 
        "Green Pirates Shaft Bottom Right", 
        "Moat Right", 
        "Keyhunter Room Bottom", 
        "Morph Ball Room Left", 
        "Green Brinstar Elevator", 
        "Green Hill Zone Top Right", 
        "Noob Bridge Right", 
        "West Ocean Left", 
        "Crab Maze Left", 
        "Lava Dive Right", 
        "Three Muskateers Room Left", 
        "Warehouse Zeela Room Left", 
        "Warehouse Entrance Left", 
        "Warehouse Entrance Right", 
        "Single Chamber Top Right", 
        "Kronic Boost Room Bottom Left", 
        "Crocomire Speedway Bottom", 
        "Crocomire Room Top", 
        "Main Street Bottom", 
        "Crab Hole Bottom Left", 
        "Red Fish Room Left", 
        "Crab Shaft Right", 
        "Aqueduct Top Left", 
        "Le Coude Right", 
        "Red Tower Top Left", 
        "Caterpillar Room Top Right", 
        "Red Brinstar Elevator", 
        "East Tunnel Right", 
        "East Tunnel Top Right", 
        "Glass Tunnel Top", 
        "Golden Four", 
    ],

    "bossAccessPoints": [
        "PhantoonRoomOut", 
        "PhantoonRoomIn", 
        "RidleyRoomOut", 
        "RidleyRoomIn", 
        "KraidRoomOut", 
        "KraidRoomIn", 
        "DraygonRoomOut", 
        "DraygonRoomIn", 
    ],

    "escapeAccessPoints": [
        'Tourian Escape Room 4 Top Right', 
        'Climb Bottom Left', 
        'Green Brinstar Main Shaft Top Left', 
        'Basement Left', 
        'Business Center Mid Left', 
        'Crab Hole Bottom Right', 
    ]
}

for aptype, aps in accessPointsIds.items():
    print("    {}['{}'] = {{".format(aptype, logic))
    for apName in aps:
        ap = getAccessPoint(apName)
        roomPtr = ap.RoomInfo['RoomPtr']

        blinking = 'Blinking[{}]'.format(apName)

        plm = None
        if blinking in additionalPLMs:
            plm = additionalPLMs[blinking]['plm_bytes_list'][0]
        elif blinking in patchDict:
            for addr, data in patchDict[blinking].items():
                if (pc_to_snes(addr) >> 16) == 0x8f:
                    plm = data
                    break

        room = rooms[0x8f0000 + roomPtr]
        roomX = room.mapX
        roomY = room.mapY
        if plm is not None:
            doorX = plm[2]
            doorY = plm[3]
        else:
            # most escape AP don't blink... so get data directly from access points
            oppositeApName = GraphUtils.getVanillaExit(apName)
            oppositeAp = getAccessPoint(oppositeApName)
            doorX = oppositeAp.ExitInfo['cap'][0]
            doorY = oppositeAp.ExitInfo['cap'][1]
        (byteIndex, bitMask) = getMapPos((roomX, roomY), (doorX, doorY))

        # "Lower Mushrooms Left": {"byteIndex": 36, "bitMask": 1, "room": 0x9969, "area": "Crateria"},
        print('        "{}": {{"byteIndex": {}, "bitMask": {}, "room": {}, "area": "{}"}},'.format(
            apName, byteIndex, bitMask, hex(roomPtr), Area(room.area).name))
    print("    }")
print(">"*32+" for solver/interactivesolver.py "+">"*32)


def name4isolver(name):
    # remove space and special characters
    return removeChars(name, " ,()-")

def transition2isolver(transition):
    transition = str(transition)
    return transition[0].lower() + removeChars(transition[1:], " ,()-")

def getScreen(roomPos, objPos):
    (roomX, roomY) = roomPos
    (objX, objY) = objPos
    x = roomX + objX // 0x10
    y = roomY + objY // 0x10
    return (x, y)

print("<"*32+" for autotracker:"+"<"*32)
print("locations['{}'] = {{".format(logic))
# items
for item in items.values():
    roomAddrS = item['room']
    shortRoomAddrS = hex(roomAddrS & 0xffff)[2:]
    room = rooms[item['room']]
    jsroom = jsrooms[logic][shortRoomAddrS]

    # room position on varia map
    (roomX, roomY) = (jsroom["left"], jsroom["top"])

    itemPlm = item['itemPlm']
    itemX = itemPlm[1]
    itemY = itemPlm[2]
    # position on varia map, in screen unit, from top,left of varia map
    (itemMapX, itemMapY) = getScreen((roomX, roomY), (itemX, itemY))

    name = name4isolver(item['loc'].Name)

    print('    "{}": {{"left": {}, "top": {}, "room": "{}", "variaArea": "{}"}},'.format(
        name, itemMapX, itemMapY, shortRoomAddrS, getVariaArea(room)))
# bosses/minibosses locations
bosses = {
    "vanilla": {
        "Kraid": (0.5, 0.5),
        "Phantoon": (0, 0),
        "Draygon": (1.5, 0.5),
        "Ridley": (1, 0.5),
        "MotherBrain": (2, 10),
        "SporeSpawn": (17, 5),
        "Botwoon": (6, 11),
        "GoldenTorizo": (4, 13),
        "Crocomire": (13, 0)
    },
    "mirror": {
        "Kraid": (1,5, 0.5),
        "Phantoon": (0, 0),
        "Draygon": (0.5, 0.5),
        "Ridley": (0, 0.5),
        "MotherBrain": (8, 10),
        "SporeSpawn": (10, 5),
        "Botwoon": (17, 11),
        "GoldenTorizo": (20, 13),
        "Crocomire": (5, 0)
    }
}
print('    "Kraid": {{"left": {}, "top": {}, "room": "a59f", "variaArea": "Kraid"}},'.format(bosses[logic]["Kraid"][0], bosses[logic]["Kraid"][1]))
print('    "Phantoon": {{"left": {}, "top": {}, "room": "cd13", "variaArea": "Phantoon"}},'.format(bosses[logic]["Phantoon"][0], bosses[logic]["Phantoon"][1]))
print('    "Draygon": {{"left": {}, "top": {}, "room": "da60", "variaArea": "Draygon"}},'.format(bosses[logic]["Draygon"][0], bosses[logic]["Draygon"][1]))
print('    "Ridley": {{"left": {}, "top": {}, "room": "b32e", "variaArea": "Ridley"}},'.format(bosses[logic]["Ridley"][0], bosses[logic]["Ridley"][1]))
if logic == "vanilla":
    print('    "MotherBrain": {{"left": {}, "top": {}, "room": "dd58", "variaArea": "Tourian"}},'.format(bosses[logic]["MotherBrain"][0], bosses[logic]["MotherBrain"][1]))
elif logic == "mirror":
    print('    "MotherBrain": {{"left": {}, "top": {}, "room": "fd40", "variaArea": "Tourian"}},'.format(bosses[logic]["MotherBrain"][0], bosses[logic]["MotherBrain"][1]))
print('    "SporeSpawn": {{"left": {}, "top": {}, "room": "9dc7", "variaArea": "GreenBrinstar"}},'.format(bosses[logic]["SporeSpawn"][0], bosses[logic]["SporeSpawn"][1]))
print('    "Botwoon": {{"left": {}, "top": {}, "room": "d95e", "variaArea": "EastMaridia"}},'.format(bosses[logic]["Botwoon"][0], bosses[logic]["Botwoon"][1]))
print('    "GoldenTorizo": {{"left": {}, "top": {}, "room": "b283", "variaArea": "LowerNorfair"}},'.format(bosses[logic]["GoldenTorizo"][0], bosses[logic]["GoldenTorizo"][1]))
print('    "Crocomire": {{"left": {}, "top": {}, "room": "a98d", "variaArea": "Crocomire"}},'.format(bosses[logic]["Crocomire"][0], bosses[logic]["Crocomire"][1]))

print('};')

# doors
print("doors['{}'] = {{".format(logic))
for door in doors.values():
    doorObj = door['door']
    room = rooms[door['room']]
    shortRoomAddrS = hex(room.dataAddr & 0xffff)[2:]
    jsroom = jsrooms[logic][shortRoomAddrS]

    # room position on varia map
    (roomX, roomY) = (jsroom["left"], jsroom["top"])

    doorPlm = door['doorPlm']
    doorX = doorPlm[1]
    doorY = doorPlm[2]
    (doorMapX, doorMapY) = getScreen((roomX, roomY), (doorX, doorY))

    print('    "{}": {{"left": {}, "top": {}, "facing": {}, "room": "{}", "variaArea": "{}"}},'.format(
        doorObj.name, doorMapX, doorMapY, doorObj.facing, shortRoomAddrS, getVariaArea(room)))
print("};")

# aps
print("aps['{}'] = {{".format(logic))
for aptype, aps in accessPointsIds.items():
    aptype = aptype[:-len("AccessPoints")]
    for apName in aps:
        name = transition2isolver(apName)
        ap = getAccessPoint(apName)
        roomPtr = ap.RoomInfo['RoomPtr']

        blinking = 'Blinking[{}]'.format(apName)

        room = rooms[0x8f0000 + roomPtr]
        jsroom = jsrooms[logic][hex(roomPtr)[2:]]

        (roomX, roomY) = (jsroom["left"], jsroom["top"])

        oppositeApName = GraphUtils.getVanillaExit(apName)
        oppositeAp = getAccessPoint(oppositeApName)
        doorX = oppositeAp.ExitInfo['cap'][0]
        doorY = oppositeAp.ExitInfo['cap'][1]
        # 0 = right, 1 = left, 2 = down, 3 = up.
        facing = oppositeAp.ExitInfo['direction'] & 0b11
        (apMapX, apMapY) = getScreen((roomX, roomY), (doorX, doorY))

        print('   "{}": {{"left": {}, "top": {}, "facing": {}, "room": "{}", "area": "{}", "type": "{}"}},'.format(
            name, apMapX, apMapY, facing, hex(roomPtr)[2:], getVariaArea(room), aptype))
print("};")

print(">"*32+" for autotracker "+">"*32)
