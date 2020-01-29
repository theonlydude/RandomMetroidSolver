import copy
import random
from graph import AccessPoint
from parameters import Knows, Settings
from rom_patches import RomPatches
from smbool import SMBool
from helpers import Bosses

# all access points and traverse functions
accessPoints = [
    ### Ceres Station
    AccessPoint('Ceres', 'Ceres', {
        'Landing Site': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0xfffe, 'doors':[0x32], 'patches':[RomPatches.BlueBrinstarBlueDoor], 'solveArea': "Crateria Landing Site"}),
    ### Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: sm.canPassTerminatorBombWall(),
        'Keyhunter Room Bottom': lambda sm: sm.canOpenGreenDoors(),
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0x0000, 'doors':[0x32], 'patches':[RomPatches.BlueBrinstarBlueDoor], 'solveArea': "Crateria Landing Site"}),
    AccessPoint('Blue Brinstar Elevator Bottom', 'Crateria', {
        'Morph Ball Room Left': lambda sm: sm.canUsePowerBombs(),
        'Landing Site': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Gauntlet Top', 'Crateria', {
        'Green Pirates Shaft Bottom Right': lambda sm: sm.haveItem('Morph')
    }, internal=True,
       start={'spawn': 0x0006, 'solveArea': "Crateria Gauntlet", 'save':"Save_Gauntlet"}),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canPassTerminatorBombWall(False),
        'Green Pirates Shaft Bottom Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9969, "area": 0x0, 'songs':[0x997a]},
       exitInfo = {'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x36, 'SamusY':0x88, 'song': 0x9},
       dotOrientation = 'nw'),
    AccessPoint('Green Pirates Shaft Bottom Right', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: SMBool(True)
    }, traverse = lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                    sm.canOpenRedDoors()),
       roomInfo = {'RoomPtr':0x99bd, "area": 0x0, 'songs':[0x99ce]},
       # the doorAsmPtr 7FE00 is set by the g4_skip.ips patch, we have to call it
       exitInfo = {'DoorPtr':0x8c52, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xfe00},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x688, 'song': 0x9},
       dotOrientation = 'e'),
    AccessPoint('Moat Right', 'Crateria', {
        'Keyhunter Room Bottom': lambda sm: sm.canPassMoatReverse()
    }, roomInfo = {'RoomPtr':0x95ff, "area": 0x0, 'songs':[0x9610]},
       exitInfo = {'DoorPtr':0x8aea, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1cf, 'SamusY':0x88, 'song': 0xc},
       dotOrientation = 'ne'),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Right': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                         sm.canPassMoat()),
        'Landing Site': lambda sm: SMBool(True)
    }, traverse = lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                    sm.canOpenYellowDoors()),
       roomInfo = { 'RoomPtr':0x948c, "area": 0x0, 'songs':[0x949d] },
       exitInfo = {'DoorPtr':0x8a42, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14c, 'SamusY':0x2b8, 'song': 0xc},
       dotOrientation = 'se'),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
        'Blue Brinstar Elevator Bottom': lambda sm: sm.canUsePowerBombs()
    }, roomInfo = { 'RoomPtr':0x9e9f, "area": 0x1},
       exitInfo = {'DoorPtr':0x8e9e, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288},
       dotOrientation = 'sw'),
    AccessPoint('Climb Bottom Left', 'Crateria', {
        'Landing Site': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x96ba, "area": 0x0},
       exitInfo = {'DoorPtr':0x8b6e, 'direction': 0x5, "cap": (0x2e, 0x16), "bitFlag": 0x0,
                   "screen": (0x2, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x888},
       escape = True,
       dotOrientation = 'ne'),
    ### Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator', 'GreenPinkBrinstar', {
        'Big Pink': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                              sm.canDestroyBombWalls()),
                                       sm.canOpenRedDoors()),
        'Etecoons Bottom': lambda sm: sm.canAccessEtecoons()
    }, roomInfo = {'RoomPtr':0x9938, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x88},
       start = {'spawn': 0x0108, 'doors':[0x1f, 0x21, 0x26], 'patches':[RomPatches.BrinReserveBlueDoors], 'solveArea': "Green Brinstar"}, # XXX test if it would be better in brin reserve room with custom save
       dotOrientation = 'ne'),
    AccessPoint('Big Pink', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                        sm.canOpenGreenDoors()),
        'Green Brinstar Elevator': lambda sm: sm.wor(sm.haveItem('SpeedBooster'),
                                                           sm.canDestroyBombWalls())
    }, internal=True, start={'spawn': 0x0100, 'solveArea': "Pink Brinstar"}),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: SMBool(True),
        'Big Pink': lambda sm: sm.haveItem('Morph')
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
       roomInfo = {'RoomPtr':0x9e52, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},
       dotOrientation = 'e'),
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
       dotOrientation = 'se'),
    AccessPoint('Green Brinstar Main Shaft Top Left', 'GreenPinkBrinstar', {
        'Green Brinstar Elevator': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9ad9, "area": 0x1},
       exitInfo = {'DoorPtr':0x8cb2, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Brinstar Pre-Map Room Right', 'GreenPinkBrinstar', {
    }, roomInfo = {'RoomPtr':0x9b9d, "area": 0x1},
       exitInfo = {'DoorPtr':0x8d42, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Etecoons Supers', 'GreenPinkBrinstar', {
        'Etecoons Bottom': lambda sm: sm.haveItem('Morph')
    }, internal=True,
       start={'spawn': 0x0107, 'doors':[0x34], 'patches':[RomPatches.EtecoonSupersBlueDoor],
              'save':"Save_Etecoons" ,'solveArea': "Green Brinstar"}),
    AccessPoint('Etecoons Bottom', 'GreenPinkBrinstar', {
        'Etecoons Supers': lambda sm: sm.wor(RomPatches.has(RomPatches.EtecoonSupersBlueDoor),
                                             sm.canOpenGreenDoors()),
        'Green Brinstar Elevator': lambda sm: sm.canUsePowerBombs()
    }, internal=True),
    ### Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: sm.canOpenGreenDoors()
    }, roomInfo = {'RoomPtr':0x93fe, "area": 0x0},
       exitInfo = {'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Wrecked Ship Main', 'WreckedShip', {
        'West Ocean Left': lambda sm: SMBool(True),
        'Wrecked Ship Back': lambda sm: sm.wor(sm.wand(Bosses.bossDead('Phantoon'),
                                                       sm.canPassSpongeBath()),
                                               sm.wand(sm.wnot(Bosses.bossDead('Phantoon')),
                                                       RomPatches.has(RomPatches.SpongeBathBlueDoor))),
        'PhantoonRoomOut': lambda sm: sm.wand(sm.canOpenGreenDoors(), sm.canPassBombPassages())
    }, internal=True,
       start={'spawn':0x0300, 'doors':[0x83], 'patches':[RomPatches.SpongeBathBlueDoor], 'solveArea': "WreckedShip Main"}),
    AccessPoint('Wrecked Ship Back', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: SMBool(True),
        'Crab Maze Left': lambda sm: sm.canPassForgottenHighway(True)
    }, internal=True),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        'Wrecked Ship Back': lambda sm: sm.canPassForgottenHighway(False)
    }, roomInfo = {'RoomPtr':0x957d, "area": 0x0, 'songs':[0x958e]},
       exitInfo = {'DoorPtr':0x8aae, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188, 'song': 0xc},
       dotOrientation = 'e'),
    AccessPoint('PhantoonRoomOut', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: sm.canPassBombPassages()
    }, boss = True,
       roomInfo = {'RoomPtr':0xcc6f, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2ac, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x49f, 'SamusY':0xb8},
       traverse=lambda sm: sm.canOpenRedDoors(),
       dotOrientation = 's'),
    AccessPoint('PhantoonRoomIn', 'WreckedShip', {},
       boss = True,
       roomInfo = {'RoomPtr':0xcd13, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2c4, 'direction': 0x5, "cap": (0x4e, 0x6), "bitFlag": 0x0,
                   "screen": (0x4, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe1fe},
       entryInfo = {'SamusX':0x2e, 'SamusY':0xb8},
       dotOrientation = 's'),
    AccessPoint('Basement Left', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xcc6f, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2a0, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2e, 'SamusY':0x88},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Wrecked Ship Map Room', 'WreckedShip', {
    }, roomInfo = {'RoomPtr':0xcccb, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2b8, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', {
        'LN Entrance': lambda sm: sm.canPassLavaPit()
    }, roomInfo = {'RoomPtr':0xaf14, "area": 0x2, 'songs':[0xaf25]},
       exitInfo = {'DoorPtr':0x96d2, 'direction': 0x4, "cap": (0x11, 0x26), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x3d0, 'SamusY':0x88, 'song': 0x15},
       dotOrientation = 'w'),
    AccessPoint('LN Entrance', 'LowerNorfair', {
        'Lava Dive Right': lambda sm: sm.canPassLavaPitReverse(),
        'LN Above GT': lambda sm: sm.canPassLowerNorfairChozo(),
        'Screw Attack Bottom': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                  sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                  sm.wand(sm.haveItem('Super'), sm.knowsGreenGateGlitch()),
                                                  sm.canDestroyBombWalls()),
        'Firefleas': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                        sm.canPassWorstRoom(),
                                        sm.canUsePowerBombs())
    }, internal=True),
    AccessPoint('LN Above GT', 'LowerNorfair', {
        'Screw Attack Bottom': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                  sm.enoughStuffGT())
    }, internal=True),
    AccessPoint('Screw Attack Bottom', 'LowerNorfair', {
        'LN Entrance': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                          sm.canExitScrewAttackArea(),
                                          sm.haveItem('Super'))
    }, internal=True),
    AccessPoint('Firefleas', 'LowerNorfair', {
        'LN Entrance': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                          sm.canPassAmphitheaterReverse(),
                                          sm.canUsePowerBombs()),
        'Three Muskateers Room Left': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                         sm.haveItem('Morph'),
                                                         sm.canPassThreeMuskateers()),
        'Ridley Zone': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                          sm.canOpenGreenDoors(),
                                          sm.canOpenYellowDoors()),
        'Screw Attack Bottom': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                  sm.canPassAmphitheaterReverse(),
                                                  sm.canDestroyBombWalls(),
                                                  sm.wand(sm.haveItem('Super'), sm.knowsGreenGateGlitch()))
    }, internal=True),
    AccessPoint('Ridley Zone', 'LowerNorfair', {
        'Firefleas': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                        sm.canUsePowerBombs(),
                                        sm.wor(sm.haveItem('SpringBall'),
                                               sm.haveItem('Bomb'),
                                               SMBool(sm.haveItemCount('PowerBomb', 2)),
                                               sm.canShortCharge())), # speedball
        'RidleyRoomOut': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
    }, internal=True),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Firefleas': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                        sm.haveItem('Morph'),
                                        sm.canPassThreeMuskateers())
    }, roomInfo = {'RoomPtr':0xb656, "area": 0x2},
       exitInfo = {'DoorPtr':0x9a4a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x88},
       dotOrientation = 'n'),
    AccessPoint('RidleyRoomOut', 'LowerNorfair', {
        'Ridley Zone': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
    }, boss = True,
       roomInfo = {'RoomPtr':0xb37a, "area": 0x2},
       exitInfo = {'DoorPtr':0x98ca, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x2e, 'SamusY':0x98},
       traverse=lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']), sm.canOpenRedDoors()),
       dotOrientation = 'e'),
    AccessPoint('RidleyRoomIn', 'LowerNorfair', {},
       boss = True,
       roomInfo = {'RoomPtr':0xb32e, "area": 0x2},
       exitInfo = {'DoorPtr':0x98be, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0xbf, 'SamusY':0x198}, # on Ridley's platform. entry screen has to be changed (see getDoorConnections)
       dotOrientation = 'e'),
    ### Kraid
    AccessPoint('Warehouse Zeela Room Left', 'Kraid', {
        'KraidRoomOut': lambda sm: sm.canPassBombPassages()
    }, roomInfo = {'RoomPtr': 0xa471, "area": 0x1, 'songs':[0xa482]},
       exitInfo = {'DoorPtr': 0x913e, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbd3f},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88, 'song':0x12},
       dotOrientation = 'w'),
    AccessPoint('KraidRoomOut', 'Kraid', {
        'Warehouse Zeela Room Left': lambda sm: sm.canPassBombPassages()
    }, boss = True,
       roomInfo = {'RoomPtr':0xa56b, "area": 0x1},
       exitInfo = {'DoorPtr':0x91b6, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x1cd, 'SamusY':0x188},
       traverse=lambda sm: sm.canOpenRedDoors(),
       dotOrientation = 'e'),
    AccessPoint('KraidRoomIn', 'Kraid', {},
       boss = True,
       roomInfo = {'RoomPtr':0xa59f, "area": 0x1},
       exitInfo = {'DoorPtr':0x91ce, 'direction': 0x5, "cap": (0x1e, 0x16), "bitFlag": 0x0,
                   "screen": (0x1, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       dotOrientation = 'e'),
    ### Norfair
    AccessPoint('Warehouse Entrance Left', 'Norfair', {
        'Warehouse Entrance Right': lambda sm: sm.canAccessKraidsLair(),
        'Business Center': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr':0x922e, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x40,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdd1},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'sw'),
    AccessPoint('Warehouse Entrance Right', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.haveItem('Super')
    }, roomInfo = {'RoomPtr': 0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr': 0x923a, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX': 0x2c7, 'SamusY': 0x98},
       dotOrientation = 'nw'),
    AccessPoint('Business Center', 'Norfair', {
        'Bubble Mountain': lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                                     sm.canPassBombPassages()),
                                             # go through cathedral
                                             sm.wand(sm.canOpenGreenDoors(),
                                                     sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Bubble']['mult']))),
        'Croc Zone': lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                               sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Croc via Frog w/Wave' if sm.haveItem('Wave') else 'Norfair Entrance -> Croc via Frog']),
                                               sm.wor(sm.wand(sm.canOpenRedDoors(), sm.knowsGreenGateGlitch()),
                                                      sm.haveItem('Wave')),
                                               sm.canOpenGreenDoors()),
                                       # below ice
                                       sm.wand(sm.canOpenGreenDoors(),
                                               sm.haveItem('SpeedBooster'),
                                               sm.canUsePowerBombs(),
                                               sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Croc via Ice']))),
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn':0x0208, 'doors':[0x4d], 'patches':[RomPatches.HiJumpAreaBlueDoor], 'solveArea': "Norfair Entrance", 'needsPreRando':True}),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Bubble Mountain Top': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                  sm.haveItem('Morph'),
                                                  sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain'])),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                            sm.haveItem('Morph'),
                                                            sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Kronic Boost Room']))
    },  roomInfo = {'RoomPtr':0xad5e, "area": 0x2},
        exitInfo = {'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                    "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
        entryInfo = {'SamusX':0x5cf, 'SamusY':0x88},
        dotOrientation = 'ne'),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Kronic Boost Room']),
                                                       sm.canDestroyBombWalls(),
                                                       sm.haveItem('Morph'),
                                                       RomPatches.has(RomPatches.SingleChamberNoCrumble)),
        'Bubble Mountain': lambda sm: sm.wand(sm.canPassBombPassages(),
                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain'])),
        'Bubble Mountain Top': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                  sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room -> Bubble Mountain Top'])), # go all the way around
        'Croc Zone': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                        sm.wor(sm.haveItem('Wave'),
                                               sm.wand(sm.canOpenRedDoors(),
                                                       sm.knowsGreenGateGlitch()))),
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
       roomInfo = {'RoomPtr':0xae74, "area": 0x2, 'songs':[0xae85]},
       exitInfo = {'DoorPtr':0x967e, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x288, 'song': 0x15},
       dotOrientation = 'se'),
    AccessPoint('Croc Zone', 'Norfair', {
        'Business Center': lambda sm: sm.wor(sm.wand(sm.canPassFrogSpeedwayRightToLeft(),
                                                     sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Norfair Entrance'])),
                                             sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Norfair Entrance']),
                                                     sm.canGrappleEscape(),
                                                     sm.haveItem('Super'))),
        'Bubble Mountain': lambda sm: sm.wand(sm.canPassBombPassages(),
                                              sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Bubble Mountain'])),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                            sm.haveItem('Morph'))
    }, internal=True),
    AccessPoint('Bubble Mountain', 'Norfair', {
        # bottom left door -> frog speed way OR exit cathedral
        'Business Center': lambda sm: sm.wor(sm.wand(sm.canPassBombPassages(),
                                                     sm.canPassFrogSpeedwayRightToLeft()),
                                             sm.canExitCathedral()),
        'Bubble Mountain Top': lambda sm: sm.canClimbBubbleMountain(),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wor(sm.wand(sm.canPassBombPassages(),
                                                                   sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room'])),
                                                           sm.wand(sm.haveItem('Morph'),
                                                                   sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room wo/Bomb']))), # go all the way around
        'Croc Zone': lambda sm: sm.wand(sm.canPassBombPassages(),
                                        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Croc']),
                                        sm.wor(sm.wand(sm.canOpenRedDoors(), sm.knowsGreenGateGlitch()),
                                               sm.haveItem('Wave')),
                                        sm.canOpenGreenDoors())
    }, internal=True,
       start={'spawn':0x0201, 'doors':[0x54,0x55], 'patches':[RomPatches.SpeedAreaBlueDoors], 'knows':['BubbleMountainWallJump'], 'solveArea': "Bubble Norfair Bottom"}),
    AccessPoint('Bubble Mountain Top', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']),
                                                       sm.canDestroyBombWalls(),
                                                       sm.haveItem('Morph'),
                                                       RomPatches.has(RomPatches.SingleChamberNoCrumble)),
        'Bubble Mountain': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Business Center Mid Left', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa7de, "area": 0x2},
       exitInfo = {'DoorPtr':0x9306, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Norfair Map Room', 'Norfair', {
    }, roomInfo = {'RoomPtr':0xb0b4, "area": 0x2},
       exitInfo = {'DoorPtr':0x97c2, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### Maridia
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
                                             sm.canDestroyBombWallsUnderwater()),
        'Precious Room Top': lambda sm: sm.canAccessDraygonFromMainStreet()
    }, roomInfo = {'RoomPtr':0xcfc9, "area": 0x4},
       exitInfo = {'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8},
       dotOrientation = 's'),
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
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa510, 'direction': 0x5,
                   "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                   "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x28, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('Le Coude Right', 'Maridia', {
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.wand(sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
                                                            sm.wor(sm.haveItem('Gravity'),
                                                                   sm.wand(sm.knowsGravLessLevel3(),
                                                                           sm.haveItem('HiJump'),
                                                                           sm.haveItem('Ice')))), # for the sand pits
                                                    sm.wand(sm.canOpenGreenDoors(),
                                                            sm.canDestroyBombWallsUnderwater(),
                                                            sm.haveItem('Morph'))), # toilet door
        'Main Street Bottom': lambda sm: sm.wand(sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
                                                 sm.canDestroyBombWallsUnderwater(),
                                                 sm.wand(sm.wor(sm.haveItem('Gravity'),
                                                                sm.wand(sm.knowsGravLessLevel3(),
                                                                        sm.haveItem('HiJump'),
                                                                        sm.haveItem('Ice'))), # for the sand pits
                                                         sm.canOpenGreenDoors(), # toilet door
                                                         sm.wor(RomPatches.has(RomPatches.AreaRandoGatesOther),
                                                                sm.knowsGreenGateGlitch()))),
        'Precious Room Top': lambda sm: sm.wand(Bosses.bossDead('Draygon'),
                                                sm.haveItem('Gravity'), # suitless could be possible with this but unreasonable: https://youtu.be/rtLwytH-u8o 
                                                sm.canOpenGreenDoors())
    }, roomInfo = {'RoomPtr':0x95a8, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd1, 'SamusY':0x88},
       dotOrientation = 'ne'),
    AccessPoint('Red Fish Room Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.haveItem('Morph') # just go down
    }, roomInfo = {'RoomPtr':0xd104, "area": 0x4},
       exitInfo = {'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                   "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'w'),
    AccessPoint('Watering Hole', 'Maridia', {
        'Beach': lambda sm: sm.haveItem('Morph'),
        'Watering Hole Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start = {'spawn': 0x0407, 'solveArea': "Maridia Pink Bottom", 'save':"Save_Watering_Hole",
                'patches':[RomPatches.MaridiaTubeOpened], 'rom_patches':['wh_open_tube.ips']}),
    AccessPoint('Watering Hole Bottom', 'Maridia', {
        'Watering Hole': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                           sm.wand(sm.knowsGravLessLevel1(),
                                                   sm.haveItem('HiJump')))
    }, internal=True),
    AccessPoint('Beach', 'Maridia', {
        'Main Street Bottom': lambda sm: SMBool(True) # fall down
    }, internal=True),
    AccessPoint('Precious Room Top', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.wand(sm.canBotwoonExitToAndFromDraygon(),
                                                 sm.wor(sm.haveItem('Gravity'), # go down sand pits
                                                        sm.wand(sm.canDoSuitlessOuterMaridia(),
                                                                sm.wor(sm.wand(sm.haveItem('Ice'),# reverse pre-botwoon
                                                                               sm.knowsMochtroidClip(),
                                                                               sm.canDestroyBombWallsUnderwater()),
                                                                       sm.knowsGravLessLevel3())))), # sandpits
        'DraygonRoomOut': lambda sm: SMBool(True),
        'Le Coude Right': lambda sm: sm.wand(sm.canPassCacatacAlley(),
                                             sm.canBotwoonExitToAndFromDraygon())
    }, internal = True),
    AccessPoint('DraygonRoomOut', 'Maridia', {
        'Precious Room Top': lambda sm: sm.canExitPreciousRoom()
    }, boss = True,
       roomInfo = {'RoomPtr':0xd78f, "area": 0x4},
       exitInfo = {'DoorPtr':0xa840, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288},
       traverse=lambda sm: sm.canOpenRedDoors(),
       dotOrientation = 'e'),
    AccessPoint('DraygonRoomIn', 'Maridia', {},
       boss = True,
       roomInfo = {'RoomPtr':0xda60, "area": 0x4},
       exitInfo = {'DoorPtr':0xa96c, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe3d9},
       entryInfo = {'SamusX':0x1c8, 'SamusY':0x88},
       traverse = lambda sm: sm.canExitDraygon(),
       dotOrientation = 'e'),
    AccessPoint('Crab Hole Bottom Right', 'Maridia', {
        'Crab Hole Bottom Left': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa51c, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd7, 'SamusY':0x188},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Maridia Map Room', 'Maridia', {
    }, roomInfo = {'RoomPtr':0xd3b6, "area": 0x4},
       exitInfo = {'DoorPtr':0xa5e8, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### Red Brinstar. Main nodes: Red Tower Top Left, East Tunnel Right
    AccessPoint('Red Tower Top Left', 'RedBrinstar', {
        # go up
        'Red Brinstar Elevator': lambda sm: sm.canClimbRedTower(),
        'Caterpillar Room Top Right': lambda sm: sm.wand(sm.canPassRedTowerToMaridiaNode(),
                                                         sm.canClimbRedTower()),
        # go down
        'East Tunnel Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa253, "area": 0x1},
       exitInfo = {'DoorPtr':0x902a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2f, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', {
        'Red Brinstar Elevator': lambda sm: sm.canPassMaridiaToRedTowerNode(),
        'Red Tower Top Left': lambda sm: sm.wand(sm.canPassMaridiaToRedTowerNode(),
                                                 sm.canOpenYellowDoors())
    }, roomInfo = {'RoomPtr':0xa322, "area": 0x1},
       exitInfo = {'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf},
       entryInfo = {'SamusX':0x2cd, 'SamusY':0x388},
       dotOrientation = 'ne'),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: sm.canPassRedTowerToMaridiaNode(),
        'Red Tower Top Left': lambda sm: sm.wor(RomPatches.has(RomPatches.HellwayBlueDoor), sm.canOpenYellowDoors())
    }, traverse=lambda sm:sm.wor(RomPatches.has(RomPatches.RedTowerBlueDoors), sm.canOpenYellowDoors()),
       roomInfo = {'RoomPtr':0x962a, "area": 0x0},
       exitInfo = {'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1},
       entryInfo = {'SamusX':0x80, 'SamusY':0x58},
       start={'spawn':0x010a, 'doors':[0x3c], 'patches':[RomPatches.HellwayBlueDoor], 'solveArea': "Red Brinstar Top", 'areaMode':True},
       dotOrientation = 'n'),
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
       dotOrientation = 'se'),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoGatesBase),
                                               sm.canOpenGreenDoors())
    }, traverse=lambda sm: RomPatches.has(RomPatches.AreaRandoGatesBase),
       roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0x3c6, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
                                               sm.canUsePowerBombs())
    }, traverse=lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
                                          sm.haveItem('HiJump')),
                                   sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
                                          sm.canUsePowerBombs())),
       roomInfo = {'RoomPtr':0xcefb, "area": 0x4},
       exitInfo = {'DoorPtr':0xa330, 'direction': 0x7, "cap": (0x16, 0x7d), "bitFlag": 0x0,
                   "screen": (0x1, 0x7), "distanceToSpawn": 0x200, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x81, 'SamusY':0x78},
       dotOrientation = 's'),
    ### Tourian
    AccessPoint('Golden Four', 'Tourian', {},
       roomInfo = {'RoomPtr':0xa5ed, "area": 0x0},
       exitInfo = {'DoorPtr':0x91e6, 'direction': 0x5, "cap": (0xe, 0x66), "bitFlag": 0x0,
                   "screen": (0x0, 0x6), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       start={'spawn':0x0007, 'solveArea': "Tourian", "save": "Save_G4", 'areaMode':True},
       dotOrientation = 'w'),
    AccessPoint('Tourian Escape Room 4 Top Right', 'Tourian', {},
       roomInfo = {'RoomPtr':0xdede, "area": 0x5},
       exitInfo = {'DoorPtr':0xab34, 'direction': 0x4, "cap": (0x1, 0x86), "bitFlag": 0x40,
                   "screen": (0x0, 0x8), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe4cf},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
]

vanillaTransitions = [
    ('Lower Mushrooms Left', 'Green Brinstar Elevator'),
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
    ('Green Pirates Shaft Bottom Right', 'Golden Four'),
    ('Warehouse Entrance Right', 'Warehouse Zeela Room Left')
]

vanillaBossesTransitions = [
    ('KraidRoomOut', 'KraidRoomIn'),
    ('PhantoonRoomOut', 'PhantoonRoomIn'),
    ('DraygonRoomOut', 'DraygonRoomIn'),
    ('RidleyRoomOut', 'RidleyRoomIn')
]

# vanilla escape transition in first position
vanillaEscapeTransitions = [
    ('Tourian Escape Room 4 Top Right', 'Climb Bottom Left'),
    ('Brinstar Pre-Map Room Right', 'Green Brinstar Main Shaft Top Left'),
    ('Wrecked Ship Map Room', 'Basement Left'),
    ('Norfair Map Room', 'Business Center Mid Left'),
    ('Maridia Map Room', 'Crab Hole Bottom Right')
]

escapeSource = 'Tourian Escape Room 4 Top Right'
escapeTargets = ['Climb Bottom Left', 'Green Brinstar Main Shaft Top Left', 'Basement Left', 'Business Center Mid Left', 'Crab Hole Bottom Right']

def getAccessPoint(apName):
    return next(ap for ap in accessPoints if ap.Name == apName)

class GraphUtils:
    def getStartAccessPointNames():
        return [ap.Name for ap in accessPoints if ap.Start is not None]

    def getStartAccessPointNamesCategory():
        ret = {'regular': [], 'custom': [], 'area': []}
        for ap in accessPoints:
            if ap.Start == None:
                continue
            elif 'areaMode' in ap.Start and ap.Start['areaMode'] == True:
                ret['area'].append(ap.Name)
            elif GraphUtils.isStandardStart(ap.Name):
                ret['regular'].append(ap.Name)
            else:
                ret['custom'].append(ap.Name)
        return ret

    def isStandardStart(startApName):
        return startApName == 'Ceres' or startApName == 'Landing Site'

    def getPossibleStartAPs(areaMode, maxDiff):
        ret = []
        allStartAPs = GraphUtils.getStartAccessPointNames()
        for apName in allStartAPs:
            start = getAccessPoint(apName).Start
            ok = True
            if 'knows' in start:
                for k in start['knows']:
                    if not Knows.knows(k, maxDiff):
                        ok = False
                        break
            if 'areaMode' in start:
                ok &= start['areaMode'] == areaMode
            if ok:
                ret.append(apName)
        return ret

    def getGraphPatches(startApName):
        ap = getAccessPoint(startApName)
        return ap.Start['patches'] if 'patches' in ap.Start else []

    def createBossesTransitions():
        transitions = vanillaBossesTransitions
        def isVanilla():
            for t in vanillaBossesTransitions:
                if t not in transitions:
                    return False
            return True
        while isVanilla():
            transitions = []
            srcs = []
            dsts = []
            for (src,dst) in vanillaBossesTransitions:
                srcs.append(src)
                dsts.append(dst)
            while len(srcs) > 0:
                src = srcs.pop(random.randint(0,len(srcs)-1))
                dst = dsts.pop(random.randint(0,len(dsts)-1))
                transitions.append((src,dst))
        return transitions

    def createAreaTransitions(bidir=True):
        tFrom = []
        tTo = []
        apNames = [ap.Name for ap in accessPoints if ap.isArea()]
        transitions = []

        def findTo(trFrom):
            ap = getAccessPoint(trFrom)
            fromArea = ap.GraphArea
            targets = [apName for apName in apNames if apName not in tTo and getAccessPoint(apName).GraphArea != fromArea]
            if len(targets) == 0: # fallback if no area transition is found
                targets = [apName for apName in apNames if apName != ap.Name]
            return targets[random.randint(0, len(targets)-1)]

        def addTransition(src, dst):
            tFrom.append(src)
            tTo.append(dst)

        while len(apNames) > 0:
            sources = [apName for apName in apNames if apName not in tFrom]
            src = sources[random.randint(0, len(sources)-1)]
            dst = findTo(src)
            transitions.append((src, dst))
            addTransition(src, dst)
            if bidir is True:
                addTransition(dst, src)
            toRemove = [apName for apName in apNames if apName in tFrom and apName in tTo]
            for apName in toRemove:
                apNames.remove(apName)
        return transitions

    def createEscapeTransition():
        return (escapeSource, random.choice(escapeTargets))

    def getVanillaExit(apName):
        allVanillaTransitions = vanillaTransitions + vanillaBossesTransitions + vanillaEscapeTransitions
        for (src,dst) in allVanillaTransitions:
            if apName == src:
                return dst
            if apName == dst:
                return src
        return None

    # gets dict like
    # (RoomPtr, (vanilla entry screen X, vanilla entry screen Y)): AP
    def getRooms():
        rooms = {}
        for ap in accessPoints:
            if ap.Internal == True:
                continue
            roomPtr = ap.RoomInfo['RoomPtr']

            connAP = getAccessPoint(GraphUtils.getVanillaExit(ap.Name))
            entryInfo = connAP.ExitInfo
            rooms[(roomPtr, entryInfo['screen'], entryInfo['direction'])] = ap
            rooms[(roomPtr, entryInfo['screen'], (ap.EntryInfo['SamusX'], ap.EntryInfo['SamusY']))] = ap
            # for boss rando with incompatible ridley transition, also register this one
            if ap.Name == 'RidleyRoomIn':
                rooms[(roomPtr, (0x0, 0x1), 0x5)] = ap
                rooms[(roomPtr, (0x0, 0x1), (0xbf, 0x198))] = ap

        return rooms

    def isHorizontal(dir):
        # up: 0x3, 0x7
        # down: 0x2, 0x6
        # left: 0x1, 0x5
        # right: 0x0, 0x4
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
        if GraphUtils.isHorizontal(exitDir) and GraphUtils.isHorizontal(entryDir):
            return entryDir
        # otherwise keep exit direction and remove cap
        return GraphUtils.removeCap(exitDir)

    def getBitFlag(srcArea, dstArea, origFlag):
        flags = origFlag
        if srcArea == dstArea:
            flags &= 0xBF
        else:
            flags |= 0x40
        return flags

    def getDoorConnections(graph, areas=True, bosses=False, escape=True):
        transitions = []
        if areas:
            transitions += vanillaTransitions
        if bosses:
            transitions += vanillaBossesTransitions
        if escape:
            transitions += vanillaEscapeTransitions
        for srcName, dstName in transitions:
            src = graph.accessPoints[srcName]
            dst = graph.accessPoints[dstName]
            dst.EntryInfo.update(src.ExitInfo)
            src.EntryInfo.update(dst.ExitInfo)
        connections = []
        for src, dst in graph.InterAreaTransitions:
            # area only
            if not bosses and src.Boss:
                continue
            # boss only
            if not areas and not src.Boss:
                continue
            conn = {}
            conn['ID'] = str(src) + ' -> ' + str(dst)
            # remove duplicates (loop transitions)
            if any(c['ID'] == conn['ID'] for c in connections):
                continue
    #        print(conn['ID'])
            # where to write
            conn['DoorPtr'] = src.ExitInfo['DoorPtr']
            # door properties
            conn['RoomPtr'] = dst.RoomInfo['RoomPtr']
            conn['doorAsmPtr'] = dst.EntryInfo['doorAsmPtr']
            conn['direction'] = GraphUtils.getDirection(src, dst)
            conn['bitFlag'] = GraphUtils.getBitFlag(src.RoomInfo['area'], dst.RoomInfo['area'],
                                                    dst.EntryInfo['bitFlag'])
            conn['cap'] = dst.EntryInfo['cap']
            conn['screen'] = dst.EntryInfo['screen']
            if conn['direction'] != src.ExitInfo['direction']: # incompatible transition
                conn['distanceToSpawn'] = 0
                conn['SamusX'] = dst.EntryInfo['SamusX']
                conn['SamusY'] = dst.EntryInfo['SamusY']
                if dst.Name == 'RidleyRoomIn': # special case: spawn samus on ridley platform
                    conn['screen'] = (0x0, 0x1)
            else:
                conn['distanceToSpawn'] = dst.EntryInfo['distanceToSpawn']
            if 'song' in dst.EntryInfo:
                conn['song'] = dst.EntryInfo['song']
                conn['songs'] = dst.RoomInfo['songs']
            connections.append(conn)
        return connections

    def getDoorsPtrs2Aps():
        ret = {}
        for ap in accessPoints:
            if ap.Internal == True:
                continue
            ret[ap.ExitInfo["DoorPtr"]] = ap.Name
        return ret

    def getAps2DoorsPtrs():
        ret = {}
        for ap in accessPoints:
            if ap.Internal == True:
                continue
            ret[ap.Name] = ap.ExitInfo["DoorPtr"]
        return ret

    def getTransitions(addresses):
        # build address -> name dict
        doorsPtrs = GraphUtils.getDoorsPtrs2Aps()

        transitions = []
        # (src.ExitInfo['DoorPtr'], dst.ExitInfo['DoorPtr'])
        for (srcDoorPtr, destDoorPtr) in addresses:
            transitions.append((doorsPtrs[srcDoorPtr], doorsPtrs[destDoorPtr]))

        return transitions
