
from graph import AccessPoint
from parameters import Knows
from rom import RomPatches
from smbool import SMBool

# all access points and traverse functions
accessPoints = [
    # Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: sm.canPassTerminatorBombWall(),
        'Keyhunter Room Bottom': lambda sm: sm.canOpenGreenDoors(),
        'Morph Ball Room Left': lambda sm: sm.canUsePowerBombs()
    }, internal=True,
       shortName="C\\LANDING"),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canPassTerminatorBombWall(False),
        'Green Pirates Shaft Bottom Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9969, "area": 0x0},
       exitInfo = {'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x36, 'SamusY':0x88, 'song': 0x9},
       shortName="C\\MUSHROOMS"),
    AccessPoint('Green Pirates Shaft Bottom Right', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: SMBool(True)
    }, traverse = lambda sm: sm.canOpenRedDoors(),
       roomInfo = {'RoomPtr':0x99bd, "area": 0x0},
       # the doorAsmPtr 7FE00 is set by the g4_skip.ips patch, we have to call it
       exitInfo = {'DoorPtr':0x8c52, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xfe00},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x688, 'song': 0x9},
       shortName="C\\PIRATES"),
    AccessPoint('Moat Right', 'Crateria', {
        'Keyhunter Room Bottom': lambda sm: sm.canPassMoatReverse()
    }, roomInfo = {'RoomPtr':0x95ff, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aea, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1cf, 'SamusY':0x88, 'song': 0xc},
       shortName="C\\MOAT"),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Right': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                         sm.canPassMoat()),
        'Landing Site': lambda sm: SMBool(True)
    }, traverse = lambda sm: sm.canOpenYellowDoors(),
       roomInfo = { 'RoomPtr':0x948c, "area": 0x0 },
       exitInfo = {'DoorPtr':0x8a42, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14c, 'SamusY':0x2b8, 'song': 0xc},
       shortName="C\\KEYHUNTERS"),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canUsePowerBombs()
    }, roomInfo = { 'RoomPtr':0x9e9f, "area": 0x1},
       exitInfo = {'DoorPtr':0x8e9e, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288},
       shortName="C\\MORPH"),
    # Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator Right', 'GreenPinkBrinstar', {
        'Big Pink': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                              sm.canDestroyBombWalls()),
                                       sm.canOpenRedDoors())
    }, roomInfo = {'RoomPtr':0x9938, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x88},
       shortName="B\\GREEN ELEV."),
    AccessPoint('Big Pink', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                        sm.canOpenGreenDoors()),
        'Green Brinstar Elevator Right': lambda sm: sm.wor(sm.haveItem('SpeedBooster'),
                                                           sm.canDestroyBombWalls())
    }, internal=True),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: SMBool(True),
        'Big Pink': lambda sm: sm.haveItem('Morph')
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
       roomInfo = {'RoomPtr':0x9e52, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},
       shortName="B\\GREEN HILL"),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wor(sm.haveItem('Wave'),
                                                       sm.wor(sm.wand(sm.canOpenRedDoors(), # can do the glitch with either missile or supers
                                                                      sm.knowsGreenGateGlitch()),
                                                              RomPatches.has(RomPatches.AreaRandoGatesOther)))
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenGreenDoors()),
       roomInfo = {'RoomPtr':0x9fba, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8f0a, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x5ce, 'SamusY':0x88},
       shortName="B\\NOOB BRIDGE"),
    # Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Crab Maze Left': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                             sm.canPassSpongeBath(), # implies dead phantoon and pass bomb passages
                                             sm.canPassForgottenHighway(True))
    }, roomInfo = {'RoomPtr':0x93fe, "area": 0x0},
       exitInfo = {'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       shortName="W\\WEST OCEAN"),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        'West Ocean Left': lambda sm: sm.canPassForgottenHighway(False)
    }, roomInfo = {'RoomPtr':0x957d, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aae, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188, 'song': 0xc},
       shortName="W\\CRAB MAZE"),
    # Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', {
        'Three Muskateers Room Left': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                                         sm.canPassLavaPit(),
                                                         sm.canPassWorstRoom())
    }, roomInfo = {'RoomPtr':0xaf14, "area": 0x2},
       exitInfo = {'DoorPtr':0x96d2, 'direction': 0x4, "cap": (0x11, 0x26), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x3d0, 'SamusY':0x88, 'song': 0x15},
       shortName="LN\\LAVA DIVE"),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Lava Dive Right': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                              sm.canPassAmphitheaterReverse(),  # if this is OK, reverse lava pit will be too...
                                              sm.canUsePowerBombs())
    }, roomInfo = {'RoomPtr':0xb656, "area": 0x2},
       exitInfo = {'DoorPtr':0x9a4a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x88},
       shortName="LN\\THREE MUSK."),
    # Kraid
    AccessPoint('Warehouse Zeela Room Left', 'Kraid', {},
       roomInfo = {'RoomPtr': 0xa471, "area": 0x1},
       exitInfo = {'DoorPtr': 0x913e, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbd3f},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88, 'song':0x12},
       shortName="KRAID"
    ),
    # Norfair
    AccessPoint('Warehouse Entrance Left', 'Norfair', {
        'Bubble Mountain': lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                                     sm.canPassBombPassages()),
                                             # go through cathedral
                                             sm.wand(sm.canOpenGreenDoors(),
                                                     sm.canHellRun('MainUpperNorfair'),
                                                     sm.wor(RomPatches.has(RomPatches.CathedralEntranceWallJump),
                                                            sm.haveItem('HiJump'),
                                                            sm.canFly(),
                                                            sm.haveItem('SpeedBooster')))), # spark
        'Croc Zone': lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                               sm.canHellRun('MainUpperNorfair', 2),
                                               sm.wor(sm.wand(sm.canOpenRedDoors(), sm.knowsGreenGateGlitch()),
                                                      sm.haveItem('Wave')),
                                               sm.canOpenGreenDoors()),
                                       # below ice
                                       sm.wand(sm.canOpenGreenDoors(),
                                               sm.haveItem('SpeedBooster'),
                                               sm.canUsePowerBombs(),
                                               sm.canHellRun('Ice', 1.5))),
        'Warehouse Entrance Right': lambda sm: sm.canAccessKraidsLair()
    }, roomInfo = {'RoomPtr':0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr':0x922e, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x40,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdd1},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       shortName="N\\WAREHOUSE L"),
    AccessPoint('Warehouse Entrance Right', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.haveItem('Super')
    }, roomInfo = {'RoomPtr': 0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr': 0x923a, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX': 0x2c7, 'SamusY': 0x98},
       shortName="N\\WAREHOUSE R"),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Bubble Mountain': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                              sm.haveItem('Morph'),
                                              sm.canHellRun('MainUpperNorfair', 1.25)),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                            sm.haveItem('Morph'),
                                                            sm.canHellRun('MainUpperNorfair'))
    },  roomInfo = {'RoomPtr':0xad5e, "area": 0x2},
        exitInfo = {'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                    "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
        entryInfo = {'SamusX':0x5cf, 'SamusY':0x88},
        shortName="N\\SINGLE CHAMBER"),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.wand(sm.canHellRun('MainUpperNorfair'),
                                                       sm.canDestroyBombWalls(),
                                                       sm.haveItem('Morph'),
                                                       RomPatches.has(RomPatches.SingleChamberNoCrumble)),
        'Bubble Mountain': lambda sm: sm.wor(sm.wand(sm.canPassBombPassages(),
                                                     sm.canHellRun('MainUpperNorfair', 1.25)),
                                             sm.wand(sm.haveItem('Morph'),
                                                     sm.canHellRun('MainUpperNorfair', 0.5))), # go all the way around
        'Croc Zone': lambda sm: sm.wand(sm.canHellRun('MainUpperNorfair'), 
                                        sm.haveItem('Morph'),
                                        sm.wor(sm.haveItem('Wave'),
                                               sm.wand(sm.canOpenRedDoors(),
                                                       sm.knowsGreenGateGlitch()))),
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
       roomInfo = {'RoomPtr':0xae74, "area": 0x2},
       exitInfo = {'DoorPtr':0x967e, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x288, 'song': 0x15},
       shortName="N\\KRONIC BOOST"),
    AccessPoint('Croc Zone', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                                             sm.canHellRun('MainUpperNorfair', 2)),
                                                     sm.wand(sm.canHellRun('MainUpperNorfair', 1.25),
                                                             sm.canGrappleEscape(),
                                                             sm.haveItem('Super'))),
        'Bubble Mountain': lambda sm: sm.wand(sm.canPassBombPassages(),
                                              sm.canHellRun('MainUpperNorfair', 2)),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wand(sm.canHellRun('MainUpperNorfair'),
                                                            sm.haveItem('Morph'))
    }, internal=True),
    AccessPoint('Bubble Mountain', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.wand(sm.canPassBombPassages(), # to access bottom left door OR to exit cathedral
                                                      sm.wor(sm.haveItem('SpeedBooster'),
                                                             sm.canHellRun('MainUpperNorfair', 0.75))),
        'Single Chamber Top Right': lambda sm: sm.wand(sm.canHellRun('MainUpperNorfair', 1.25),
                                                       sm.canDestroyBombWalls(),
                                                       sm.haveItem('Morph'),
                                                       RomPatches.has(RomPatches.SingleChamberNoCrumble)),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wor(sm.wand(sm.canPassBombPassages(),
                                                                   sm.canHellRun('MainUpperNorfair', 1.25)),
                                                           sm.wand(sm.haveItem('Morph'),
                                                                   sm.canHellRun('MainUpperNorfair', 0.5))), # go all the way around
        'Croc Zone': lambda sm: sm.wand(sm.canPassBombPassages(),
                                        sm.canHellRun('MainUpperNorfair', 2),
                                        sm.wor(sm.wand(sm.canOpenRedDoors(), sm.knowsGreenGateGlitch()),
                                               sm.haveItem('Wave')),
                                        sm.canOpenGreenDoors())
    }, internal=True),
    # Maridia
    AccessPoint('Main Street Bottom', 'Maridia', {
        'Red Fish Room Left': lambda sm: sm.wand(sm.canGoUpMtEverest(),
                                                 sm.haveItem('Morph')),
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                    sm.wor(sm.canOpenGreenDoors(), # red door+green gate
                                                           sm.wand(sm.canOpenRedDoors(),
                                                                   RomPatches.has(RomPatches.AreaRandoGatesOther)))),
        'Le Coude Right': lambda sm: sm.wand(sm.canOpenGreenDoors(), # gate+door
                                             sm.wor(sm.haveItem('Gravity'),
                                                    sm.wand(sm.knowsGravLessLevel3(),
                                                            sm.haveItem('HiJump'),
                                                            sm.haveItem('Ice'))), # for the sand pits
                                             sm.canDestroyBombWallsUnderwater())
    }, roomInfo = {'RoomPtr':0xcfc9, "area": 0x4},
       exitInfo = {'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8},
       shortName="M\\MAIN STREET"),
    AccessPoint('Crab Hole Bottom Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.wand(sm.canExitCrabHole(),
                                                 sm.wor(sm.wand(sm.haveItem('Super'),
                                                                sm.knowsGreenGateGlitch()),
                                                        RomPatches.has(RomPatches.AreaRandoGatesOther))),
        'Le Coude Right': lambda sm: sm.wand(sm.canExitCrabHole(),
                                             sm.canOpenGreenDoors(), # toilet door
                                             sm.canDestroyBombWallsUnderwater(),
                                             sm.wor(sm.haveItem('Gravity'),
                                                    sm.wand(sm.knowsGravLessLevel3(),
                                                            sm.haveItem('HiJump'),
                                                            sm.haveItem('Ice')))) # for the sand pits
    },
       roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa510, 'direction': 0x5,
                   "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                   "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x28, 'SamusY':0x188},
       shortName="M\\CRAB HOLE"),
    AccessPoint('Le Coude Right', 'Maridia', {
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.wand(sm.wor(sm.canOpenYellowDoors(), RomPatches.has(RomPatches.AreaRandoBlueDoors)),
                                                            sm.wor(sm.haveItem('Gravity'),
                                                                   sm.wand(sm.knowsGravLessLevel3(),
                                                                           sm.haveItem('HiJump'),
                                                                           sm.haveItem('Ice')))), # for the sand pits
                                                    sm.wand(sm.canOpenGreenDoors(),
                                                            sm.canDestroyBombWallsUnderwater(),
                                                            sm.haveItem('Morph'))), # toilet door
        'Main Street Bottom': lambda sm: sm.wand(sm.wor(sm.canOpenYellowDoors(), RomPatches.has(RomPatches.AreaRandoBlueDoors)),
                                                 sm.canDestroyBombWallsUnderwater(),
                                                 sm.wand(sm.wor(sm.haveItem('Gravity'),
                                                                sm.wand(sm.knowsGravLessLevel3(),
                                                                        sm.haveItem('HiJump'),
                                                                        sm.haveItem('Ice'))), # for the sand pits
                                                         sm.canOpenGreenDoors(), # toilet door
                                                         sm.wor(RomPatches.has(RomPatches.AreaRandoGatesOther),
                                                                sm.knowsGreenGateGlitch()))),
    }, roomInfo = {'RoomPtr':0x95a8, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd1, 'SamusY':0x88},
       shortName="M\\COUDE"),
    AccessPoint('Red Fish Room Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.haveItem('Morph') # just go down
    },
       roomInfo = {'RoomPtr':0xd104, "area": 0x4},
       exitInfo = {'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                   "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       shortName="M\\RED FISH"),
    # Red Brinstar. Main nodes: Red Tower Top Left, East Tunnel Right
    AccessPoint('Red Tower Top Left', 'RedBrinstar', {
        # go up
        'Red Brinstar Elevator': lambda sm: sm.wand(sm.canClimbRedTower(),
                                                    sm.wor(sm.canOpenYellowDoors(),
                                                           RomPatches.has(RomPatches.RedTowerBlueDoors))),
        'Caterpillar Room Top Right': lambda sm: sm.wand(sm.canPassRedTowerToMaridiaNode(),
                                                         sm.canClimbRedTower()),
        # go down
        'East Tunnel Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa253, "area": 0x1},
       exitInfo = {'DoorPtr':0x902a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2f, 'SamusY':0x488},
       shortName="B\\RED TOWER"),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', {
        'Red Brinstar Elevator': lambda sm: sm.wand(sm.canPassMaridiaToRedTowerNode(),
                                                    sm.wor(sm.canUsePowerBombs(),
                                                           RomPatches.has(RomPatches.RedTowerBlueDoors))),
        'Red Tower Top Left': lambda sm: sm.wand(sm.canPassMaridiaToRedTowerNode(),
                                                 sm.canOpenYellowDoors())
    },
       roomInfo = {'RoomPtr':0xa322, "area": 0x1},
       exitInfo = {'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf},
       entryInfo = {'SamusX':0x2cd, 'SamusY':0x388},
       shortName="B\\TOP RED TOWER"),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: sm.canPassRedTowerToMaridiaNode(),
        'Red Tower Top Left': lambda sm: sm.canOpenYellowDoors()
    }, roomInfo = {'RoomPtr':0x962a, "area": 0x0},
       exitInfo = {'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1},
       entryInfo = {'SamusX':0x80, 'SamusY':0x58},
       shortName="B\\RED ELEV."),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda sm: SMBool(True), # handled by room traverse function
        'Glass Tunnel Top': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                               sm.wor(sm.haveItem('Gravity'),
                                                      sm.haveItem('HiJump'))),
        'Red Tower Top Left': lambda sm: sm.canClimbBottomRedTower()
    }, roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa384, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xce, 'SamusY':0x188},
       shortName="B\\EAST TUNNEL"),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoGatesBase),
                                               sm.canOpenGreenDoors())
    }, traverse=lambda sm: RomPatches.has(RomPatches.AreaRandoGatesBase),
       roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0x3c6, 'SamusY':0x88},
       shortName="B\\TOP EAST TUNNEL"),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.canUsePowerBombs()
    }, traverse=lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
                                          sm.haveItem('HiJump')),
                                   sm.canUsePowerBombs()),
       roomInfo = {'RoomPtr':0xcefb, "area": 0x4},
       exitInfo = {'DoorPtr':0xa330, 'direction': 0x7, "cap": (0x16, 0x7d), "bitFlag": 0x0,
                   "screen": (0x1, 0x7), "distanceToSpawn": 0x200, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x81, 'SamusY':0x78},
       shortName="B\\GLASS TUNNEL"),
    # Tourian
    AccessPoint('Statues Hallway Left', 'Tourian', {},
       roomInfo = {'RoomPtr':0xa5ed, "area": 0x0},
       exitInfo = {'DoorPtr':0x91e6, 'direction': 0x5, "cap": (0xe, 0x66), "bitFlag": 0x0,
                   "screen": (0x0, 0x6), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       shortName="TOURIAN"
    )
]

vanillaTransitions = [
    ('Lower Mushrooms Left', 'Green Brinstar Elevator Right'),
    ('Morph Ball Room Left', 'Green Hill Zone Top Right'),
    ('Moat Right', 'West Ocean Left'),
    ('Keyhunter Room Bottom', 'Red Brinstar Elevator'),
    ('Noob Bridge Right', 'Red Tower Top Left'),
    ('Crab Maze Left', 'Le Coude Right'),
    ('Kronic Boost Room Bottom Left', 'Lava Dive Right'),
    ('Three Muskateers Room Left', 'Single Chamber Top Right'),
    ('Warehouse Entrance Left', 'East Tunnel Right'),
    ('East Tunnel Top Right', 'Crab Hole Bottom Left'),
    ('Caterpillar Room Top Right', 'Red Fish Room Left'),
    ('Glass Tunnel Top', 'Main Street Bottom'),
    ('Green Pirates Shaft Bottom Right', 'Statues Hallway Left'),
    ('Warehouse Entrance Right', 'Warehouse Zeela Room Left')
]

def isVanillaTransitions(transitions):
    for src, dest in transitions:
        found = False
        for vsrc, vdest in vanillaTransitions:
            if (src == vsrc and dest == vdest) or (src == vdest and dest == vsrc):
                found = True
                break
        if found == False:
            return False
    return True

    # up: 0x3, 0x7
    # down: 0x2, 0x6
    # left: 0x1, 0x5
    # right: 0x0, 0x4

def isHorizontal(dir):
    return dir in [0x1, 0x5, 0x0, 0x4]

def removeCap(dir):
    if dir < 4:
        return dir
    return dir - 4

def getDirection(src, dst):
    exitDir = src.ExitInfo['direction']
    entryDir = dst.EntryInfo['direction']
    # compatible transition
    if exitDir == entryDir:
        return exitDir
    # if incompatible but horizontal we keep entry dir (looks more natural)
    if isHorizontal(exitDir) and isHorizontal(entryDir):
        return entryDir
    # otherwise keep exit direction and remove cap
    return removeCap(exitDir)

def getBitFlag(srcArea, dstArea, origFlag):
    flags = origFlag
    if srcArea == dstArea:
        flags &= 0xBF
    else:
        flags |= 0x40
    return flags

def getDoorConnections(graph):
    for srcName, dstName in vanillaTransitions:
        src = graph.accessPoints[srcName]
        dst = graph.accessPoints[dstName]
        dst.EntryInfo.update(src.ExitInfo)
        src.EntryInfo.update(dst.ExitInfo)
    connections = []
    for src, dst in graph.InterAreaTransitions:
        conn = {}
        conn['ID'] = str(src) + ' -> ' + str(dst)
        # where to write
        conn['DoorPtr'] = src.ExitInfo['DoorPtr']
        # door properties
        conn['RoomPtr'] = dst.RoomInfo['RoomPtr']
        conn['doorAsmPtr'] = dst.EntryInfo['doorAsmPtr']
        conn['direction'] = getDirection(src, dst)
        conn['bitFlag'] = getBitFlag(src.RoomInfo['area'], dst.RoomInfo['area'],
                                     dst.EntryInfo['bitFlag'])
        conn['cap'] = dst.EntryInfo['cap']
        conn['screen'] = dst.EntryInfo['screen']
        if conn['direction'] != src.ExitInfo['direction']: # incompatible transition
            conn['distanceToSpawn'] = 0
            conn['SamusX'] = dst.EntryInfo['SamusX']
            conn['SamusY'] = dst.EntryInfo['SamusY']
        else:
            conn['distanceToSpawn'] = dst.EntryInfo['distanceToSpawn']
        if 'song' in dst.EntryInfo:
            conn['song'] = dst.EntryInfo['song']
        connections.append(conn)
    return connections
