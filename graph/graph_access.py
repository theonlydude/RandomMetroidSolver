import copy
import random
from graph.graph import AccessPoint, AccessGraph
from graph.graph_locations import locations
from utils.parameters import Knows, Settings
from rom.rom_patches import RomPatches
from logic.smbool import SMBool
from logic.helpers import Bosses
from logic.cache import Cache
import utils.log

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
        'Keyhunter Room Bottom': lambda sm: sm.traverse('LandingSiteRight'),
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
       start={'spawn': 0x0006, 'solveArea': "Crateria Gauntlet", 'save':"Save_Gauntlet", 'forcedEarlyMorph':True}),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': Cache.ldeco('LML_LS', lambda sm: sm.wand(sm.canPassTerminatorBombWall(False), sm.canPassCrateriaGreenPirates())),
        'Green Pirates Shaft Bottom Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9969, "area": 0x0, 'songs':[0x997a]},
       exitInfo = {'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x36, 'SamusY':0x88, 'song': 0x9},
       dotOrientation = 'nw'),
    AccessPoint('Green Pirates Shaft Bottom Right', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: SMBool(True)
    }, traverse = lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                    sm.traverse('GreenPiratesShaftBottomRight')),
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
        'Moat Right': lambda sm: sm.wand(sm.traverse('KihunterRight'),
                                         sm.canPassMoat()),
        'Landing Site': lambda sm: SMBool(True)
    }, traverse = lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                    sm.traverse('KihunterBottom')),
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
    # Escape APs
    AccessPoint('Climb Bottom Left', 'Crateria', {
        'Landing Site': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x96ba, "area": 0x0},
       exitInfo = {'DoorPtr':0x8b6e, 'direction': 0x5, "cap": (0x2e, 0x16), "bitFlag": 0x0,
                   "screen": (0x2, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x888},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Flyway Right', 'Crateria', {},
       roomInfo = {'RoomPtr':0x9879, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bc2, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000,
                   "exitAsmPtr": 0xf030}, # setup_next_escape in rando_escape.asm
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True),
    AccessPoint('Bomb Torizo Room Left', 'Crateria', {},
       roomInfo = {'RoomPtr':0x9804, "area": 0x0},
       exitInfo = {'DoorPtr':0x8baa, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0xb8},
       escape = True),
    ### Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator', 'GreenPinkBrinstar', {
        'Big Pink': Cache.ldeco('GBE_BP',
                                lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                                          sm.canDestroyBombWalls()),
                                                   sm.traverse('MainShaftBottomRight'))),
        'Etecoons Bottom': lambda sm: sm.canAccessEtecoons()
    }, roomInfo = {'RoomPtr':0x9938, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x88},
       start = {'spawn': 0x0108, 'doors':[0x1f, 0x21, 0x26], 'patches':[RomPatches.BrinReserveBlueDoors], 'solveArea': "Green Brinstar"}, # XXX test if it would be better in brin reserve room with custom save
       dotOrientation = 'ne'),
    AccessPoint('Big Pink', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                        sm.traverse('BigPinkBottomRight')),
        'Green Brinstar Elevator': lambda sm: sm.wor(sm.haveItem('SpeedBooster'),
                                                     sm.canDestroyBombWalls())
    }, internal=True, start={'spawn': 0x0100, 'solveArea': "Pink Brinstar"}),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: SMBool(True),
        'Big Pink': lambda sm: sm.haveItem('Morph')
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('GreenHillZoneTopRight')),
       roomInfo = {'RoomPtr':0x9e52, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': Cache.ldeco('NBR_GHZTR',
                                                 lambda sm: sm.wor(sm.haveItem('Wave'),
                                                                   sm.wor(sm.canBlueGateGlitch(),
                                                                          RomPatches.has(RomPatches.AreaRandoGatesOther))))
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('NoobBridgeRight')),
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
              'save':"Save_Etecoons" ,'solveArea': "Green Brinstar", 'forcedEarlyMorph':True}),
    AccessPoint('Etecoons Bottom', 'GreenPinkBrinstar', {
        'Etecoons Supers': lambda sm: sm.wor(RomPatches.has(RomPatches.EtecoonSupersBlueDoor),
                                             sm.traverse('EtecoonEnergyTankLeft')),
        'Green Brinstar Elevator': lambda sm: sm.canUsePowerBombs()
    }, internal=True),
    ### Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: sm.traverse('WestOceanRight')
    }, roomInfo = {'RoomPtr':0x93fe, "area": 0x0},
       exitInfo = {'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Wrecked Ship Main', 'WreckedShip', {
        'West Ocean Left': lambda sm: SMBool(True),
        'Wrecked Ship Back': Cache.ldeco('WSM_WSB',
                                         lambda sm: sm.wor(sm.wand(Bosses.bossDead(sm, 'Phantoon'),
                                                                   sm.canPassSpongeBath()),
                                                           sm.wand(sm.wnot(Bosses.bossDead(sm, 'Phantoon')),
                                                                   RomPatches.has(RomPatches.SpongeBathBlueDoor)))),
        'PhantoonRoomOut': lambda sm: sm.wand(sm.traverse('WreckedShipMainShaftBottom'), sm.canPassBombPassages())
    }, internal=True,
       start={'spawn':0x0300,
              'doors':[0x83,0x8b], 'patches':[RomPatches.SpongeBathBlueDoor, RomPatches.WsEtankBlueDoor],
              'solveArea': "WreckedShip Main",
              'needsPreRando':True}),
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
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 's'),
    AccessPoint('PhantoonRoomIn', 'WreckedShip', {},
       boss = True,
       roomInfo = {'RoomPtr':0xcd13, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2c4, 'direction': 0x5, "cap": (0x4e, 0x6), "bitFlag": 0x0,
                   "screen": (0x4, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe1fe,
                   "exitAsmPtr": 0xf7f0},
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
        'Screw Attack Bottom': Cache.ldeco('LNE_SAB',
                                           lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                              sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.canGreenGateGlitch(),
                                                              sm.canDestroyBombWalls())),
        'Firefleas': Cache.ldeco('LNE_F',
                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.canPassWorstRoom(),
                                                    sm.canUsePowerBombs()))
    }, internal=True),
    AccessPoint('LN Above GT', 'LowerNorfair', {
        'Screw Attack Bottom': Cache.ldeco('LNAGT_SAB',
                                           lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.enoughStuffGT()))
    }, internal=True),
    AccessPoint('Screw Attack Bottom', 'LowerNorfair', {
        'LN Entrance': Cache.ldeco('SAB_LNE',
                                   lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canExitScrewAttackArea(),
                                                      sm.haveItem('Super'),
                                                      sm.canUsePowerBombs()))
    }, internal=True),
    AccessPoint('Firefleas', 'LowerNorfair', {
        'LN Entrance': Cache.ldeco('F_LNE',
                                   lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canPassAmphitheaterReverse(),
                                                      sm.canPassWorstRoomPirates(),
                                                      sm.canUsePowerBombs())),
        'Three Muskateers Room Left': Cache.ldeco('F_TMRL',
                                                  lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                                     sm.haveItem('Morph'),
                                                                     # check for only 3 ki hunters this way
                                                                     sm.canPassRedKiHunters())),
        'Ridley Zone': Cache.ldeco('F_RZ',
                                   lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.traverse('WastelandLeft'),
                                                      sm.traverse('RedKihunterShaftBottom'),
                                                      sm.canUsePowerBombs(),
                                                      sm.wand(sm.canGetBackFromRidleyZone(),
                                                              sm.canPassRedKiHunters(),
                                                              sm.canPassWastelandDessgeegas(),
                                                              sm.canPassNinjaPirates()))),
        'Screw Attack Bottom': Cache.ldeco('F_SAB',
                                           lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.canPassAmphitheaterReverse(),
                                                              sm.canDestroyBombWalls(),
                                                              sm.canGreenGateGlitch())),
        'Firefleas Top': Cache.ldeco('F_FT',
                                     lambda sm: sm.wand(sm.canPassBombPassages(),
                                                        sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])))
    }, internal=True),
    AccessPoint('Firefleas Top', 'LowerNorfair', {
        # this weird condition basically says: "if we start here, give heat protection"
        'Firefleas': lambda sm: sm.wor(sm.wnot(RomPatches.has(RomPatches.LowerNorfairPBRoomHeatDisable)),
                                       sm.heatProof())
    }, internal=True,
       start={'spawn':0x0207,
              'rom_patches': ['LN_PB_Heat_Disable', 'LN_Firefleas_Remove_Fune','firefleas_shot_block.ips'],
              'patches':[RomPatches.LowerNorfairPBRoomHeatDisable, RomPatches.FirefleasRemoveFune],
              'knows': ["FirefleasWalljump"],
              'save': "Save_Firefleas", 'needsPreRando': True,
              'solveArea': "Lower Norfair After Amphitheater",
              'forcedEarlyMorph':True}),
    AccessPoint('Ridley Zone', 'LowerNorfair', {
        'Firefleas': Cache.ldeco('RZ_F',
                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.canUsePowerBombs(),
                                                    sm.wand(sm.canGetBackFromRidleyZone(),
                                                            sm.canPassWastelandDessgeegas(),
                                                            sm.canPassRedKiHunters()))),
        'RidleyRoomOut': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
    }, internal=True),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Firefleas': Cache.ldeco('TMRL_F',
                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.haveItem('Morph'),
                                                    sm.canPassThreeMuskateers()))
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
       traverse=Cache.ldeco('RRO_T',
                            lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                               sm.canOpenEyeDoors())),
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
       roomInfo = {'RoomPtr':0xa56b, "area": 0x1,
                   # put red brin song in both pre-kraid rooms,
                   # (vanilla music only makes sense if kraid is
                   #  vanilla)
                   "songs":[0xa57c,0xa537,0xa551]},
       exitInfo = {'DoorPtr':0x91b6, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x1cd, 'SamusY':0x188, 'song':0x12},
       traverse=lambda sm: sm.canOpenEyeDoors(),
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
        'Cathedral': lambda sm: sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles']['mult']),
        'Bubble Mountain': Cache.ldeco('BC_BM',
                                       lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                                                 sm.canPassBombPassages()),
                                                         # go through cathedral
                                                         sm.wand(sm.traverse('CathedralRight'),
                                                                 sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Bubble']['mult'])))),
        'Crocomire Speedway Bottom': Cache.ldeco('BC_CSB',
                                                 lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                                                           sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Croc via Frog w/Wave' if sm.haveItem('Wave') else 'Norfair Entrance -> Croc via Frog']),
                                                                           sm.wor(sm.canBlueGateGlitch(),
                                                                                  sm.haveItem('Wave'))),
                                                                   # below ice
                                                                   sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                                                           sm.haveItem('SpeedBooster'),
                                                                           sm.canUsePowerBombs(),
                                                                           sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Croc via Ice'])))),
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn':0x0208, 'doors':[0x4d], 'patches':[RomPatches.HiJumpAreaBlueDoor], 'solveArea': "Norfair Entrance", 'needsPreRando':True}),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Bubble Mountain Top': Cache.ldeco('SCTR_BBT',
                                           lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                              sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']))),
        'Kronic Boost Room Bottom Left': Cache.ldeco('SCTR_KBRNL',
                                                     lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                                        sm.haveItem('Morph'),
                                                                        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Kronic Boost Room'])))
    },  roomInfo = {'RoomPtr':0xad5e, "area": 0x2},
        exitInfo = {'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                    "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
        entryInfo = {'SamusX':0x5cf, 'SamusY':0x88},
        dotOrientation = 'ne'),
    AccessPoint('Cathedral', 'Norfair', {
        'Business Center': lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles']),
        'Bubble Mountain': lambda sm: sm.wand(sm.traverse('CathedralRight'),
                                             sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles']))
    }, internal=True),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
        'Single Chamber Top Right': Cache.ldeco('KBRBL_SCTR',
                                                lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Kronic Boost Room']),
                                                                   sm.canDestroyBombWalls(),
                                                                   sm.haveItem('Morph'),
                                                                   RomPatches.has(RomPatches.SingleChamberNoCrumble))),
        'Bubble Mountain': Cache.ldeco('KBRBL_BM',
                                       lambda sm: sm.wand(sm.canPassBombPassages(),
                                                          sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']))),
        'Bubble Mountain Top': Cache.ldeco('KBRBL_BMT',
                                           lambda sm: sm.wand(sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room -> Bubble Mountain Top']))), # go all the way around
        'Crocomire Speedway Bottom': Cache.ldeco('KBRBL_CSB',
                                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                                    sm.wor(sm.haveItem('Wave'),
                                                                           sm.canBlueGateGlitch()))),
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('KronicBoostBottomLeft')),
       roomInfo = {'RoomPtr':0xae74, "area": 0x2, 'songs':[0xae85]},
       exitInfo = {'DoorPtr':0x967e, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x288, 'song': 0x15},
       dotOrientation = 'se'),
    AccessPoint('Crocomire Speedway Bottom', 'Norfair', {
        'Business Center': Cache.ldeco('CSB_BC',
                                       lambda sm: sm.wor(sm.wand(sm.canPassFrogSpeedwayRightToLeft(),
                                                                 sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Norfair Entrance'])),
                                                         sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Norfair Entrance']),
                                                                 sm.canGrappleEscape(),
                                                                 sm.haveItem('Super')))),
        'Bubble Mountain': Cache.ldeco('CSB_BM',
                                       lambda sm: sm.wand(sm.canPassBombPassages(),
                                                          sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Bubble Mountain']))),
        'Kronic Boost Room Bottom Left': Cache.ldeco('CSB_KBRBL',
                                                     lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                                        sm.haveItem('Morph')))
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.CrocBlueDoors), sm.traverse('CrocomireSpeedwayBottom')),
       roomInfo = {'RoomPtr':0xa923, "area": 0x2},
       exitInfo = {'DoorPtr':0x93d2, 'direction': 0x6, "cap": (0x36, 0x2), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xc57, 'SamusY':0x2b8},
       dotOrientation = 'se'),
    AccessPoint('Bubble Mountain', 'Norfair', {
        # bottom left door -> frog speed way OR exit cathedral
        'Business Center': Cache.ldeco('BM_BC',
                                       lambda sm: sm.wor(sm.wand(sm.canPassBombPassages(),
                                                                 sm.canPassFrogSpeedwayRightToLeft()),
                                                         sm.canExitCathedral())),
        'Bubble Mountain Top': lambda sm: sm.canClimbBubbleMountain(),
        'Kronic Boost Room Bottom Left': Cache.ldeco('BM_KBRBL',
                                                     lambda sm: sm.wor(sm.wand(sm.canPassBombPassages(),
                                                                               sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room'])),
                                                                       sm.wand(sm.haveItem('Morph'),
                                                                               sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room wo/Bomb'])))), # go all the way around
        'Crocomire Speedway Bottom': Cache.ldeco('BM_CSB',
                                                 lambda sm: sm.wand(sm.canPassBombPassages(),
                                                                    sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Croc']),
                                                                    sm.wor(sm.canBlueGateGlitch(),
                                                                           sm.haveItem('Wave')))),
        'Cathedral': lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles']),
    }, internal=True,
       start={'spawn':0x0201, 'doors':[0x54,0x55], 'patches':[RomPatches.SpeedAreaBlueDoors], 'knows':['BubbleMountainWallJump'], 'solveArea': "Bubble Norfair Bottom"}),
    AccessPoint('Bubble Mountain Top', 'Norfair', {
        'Single Chamber Top Right': Cache.ldeco('BMT_SCTR',
                                                lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']),
                                                                   sm.canDestroyBombWalls(),
                                                                   sm.haveItem('Morph'),
                                                                   RomPatches.has(RomPatches.SingleChamberNoCrumble))),
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
    ### Croc
    AccessPoint('Crocomire Room Top', 'Crocomire', {
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.CrocBlueDoors), sm.enoughStuffCroc()),
       roomInfo = {'RoomPtr':0xa98d, "area": 0x2, 'songs':[0xa9bd]},
       exitInfo = {'DoorPtr':0x93ea, 'direction': 0x7, "cap": (0xc6, 0x2d), "bitFlag": 0x0,
                   "screen": (0xc, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0x0000,
                   "exitAsmPtr": 0xf7f0},
       entryInfo = {'SamusX':0x383, 'SamusY':0x98, 'song': 0x15},
       dotOrientation = 'se'),
    ### West Maridia
    AccessPoint('Main Street Bottom', 'WestMaridia', {
        'Red Fish Room Left': lambda sm: sm.wand(sm.canGoUpMtEverest(),
                                                 sm.haveItem('Morph')),
        'Crab Hole Bottom Left': Cache.ldeco('MSB_CHBL',
                                             lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                sm.traverse('MainStreetBottomRight'),
                                                                sm.wor(sm.haveItem('Super'),
                                                                       RomPatches.has(RomPatches.AreaRandoGatesOther)))),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco('MSB_OB',
                                    lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                       sm.traverse('MainStreetBottomRight'),
                                                       sm.wor(sm.haveItem('Super'),
                                                              RomPatches.has(RomPatches.AreaRandoGatesOther)),
                                                       sm.canTraverseWestSandHallLeftToRight())),
        'Crab Shaft Left': lambda sm: sm.canPassMtEverest()
    }, roomInfo = {'RoomPtr':0xcfc9, "area": 0x4},
       exitInfo = {'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8},
       dotOrientation = 's'),
    AccessPoint('Mama Turtle', 'WestMaridia', {
        'Main Street Bottom': lambda sm: sm.canJumpUnderwater()
    }, internal=True,
       start = {'spawn': 0x0406, 'solveArea': "Maridia Green", 'save':"Save_Mama",
                'patches':[RomPatches.MamaTurtleBlueDoor],
                'rom_patches':['mama_save.ips'], 'doors': [0x8e]}),
    AccessPoint('Crab Hole Bottom Left', 'WestMaridia', {
        'Main Street Bottom': Cache.ldeco('CHBL_MSB',
                                          lambda sm: sm.wand(sm.canExitCrabHole(),
                                                             sm.wor(sm.canGreenGateGlitch(),
                                                                    RomPatches.has(RomPatches.AreaRandoGatesOther)))),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco('CHBL_OB',
                                    lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                       sm.canExitCrabHole(),
                                                       sm.canTraverseWestSandHallLeftToRight()))
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa510, 'direction': 0x5,
                   "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                   "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x28, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('Red Fish Room Left', 'WestMaridia', {
        'Main Street Bottom': lambda sm: sm.haveItem('Morph') # just go down
    }, roomInfo = {'RoomPtr':0xd104, "area": 0x4},
       exitInfo = {'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                   "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'w'),
    AccessPoint('Crab Shaft Left', 'WestMaridia', {
        'Main Street Bottom': lambda sm: SMBool(True), # fall down
        'Beach': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                   sm.canDoSuitlessOuterMaridia()),
        'Crab Shaft Right': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Watering Hole', 'WestMaridia', {
        'Beach': lambda sm: sm.haveItem('Morph'),
        'Watering Hole Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start = {'spawn': 0x0407, 'solveArea': "Maridia Pink Bottom", 'save':"Save_Watering_Hole",
                'patches':[RomPatches.MaridiaTubeOpened], 'rom_patches':['wh_open_tube.ips'],
                'forcedEarlyMorph':True}),
    AccessPoint('Watering Hole Bottom', 'WestMaridia', {
        'Watering Hole': lambda sm: sm.canJumpUnderwater()
    }, internal=True),
    AccessPoint('Beach', 'WestMaridia', {
        'Crab Shaft Left': lambda sm: SMBool(True), # fall down
        'Watering Hole': Cache.ldeco('B_WH',
                                     lambda sm: sm.wand(sm.wor(sm.canPassBombPassages(),
                                                               sm.canUseSpringBall()),
                                                        sm.wor(sm.haveItem('Gravity'),
                                                               sm.canDoSuitlessOuterMaridia())))
    }, internal=True),
    AccessPoint('Crab Shaft Right', 'WestMaridia', {
        'Crab Shaft Left': lambda sm: sm.canJumpUnderwater()
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.CrabShaftBlueDoor),
                                  sm.traverse('CrabShaftRight')),
       roomInfo = {'RoomPtr':0xd1a3, "area": 0x4},
       exitInfo = {'DoorPtr':0xa4c8, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x1ca, 'SamusY':0x388},
       dotOrientation = 'e'),
    # escape APs
    AccessPoint('Crab Hole Bottom Right', 'WestMaridia', {
        'Crab Hole Bottom Left': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa51c, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd7, 'SamusY':0x188},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Maridia Map Room', 'WestMaridia', {
    }, roomInfo = {'RoomPtr':0xd3b6, "area": 0x4},
       exitInfo = {'DoorPtr':0xa5e8, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### East Maridia
    AccessPoint('Aqueduct Top Left', 'EastMaridia', {
        'Aqueduct Bottom': lambda sm: sm.canUsePowerBombs()
    }, roomInfo = {'RoomPtr':0xd5a7, "area": 0x4},
       exitInfo = {'DoorPtr':0xa708, 'direction': 0x5, "cap": (0x1e, 0x36), "bitFlag": 0x0,
                   "screen": (0x1, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe398},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       dotOrientation = 'w'),
    AccessPoint('Aqueduct Bottom', 'EastMaridia', {
        'Aqueduct Top Left': lambda sm: sm.wand(sm.canDestroyBombWallsUnderwater(), # top left bomb blocks
                                                sm.canJumpUnderwater()),
        'Post Botwoon': lambda sm: sm.wand(sm.canJumpUnderwater(),
                                           sm.canDefeatBotwoon()), # includes botwoon hallway conditions
        'Left Sandpit': lambda sm: sm.canAccessSandPits(),
        'Right Sandpit': lambda sm: sm.canAccessSandPits(),
        'Aqueduct': Cache.ldeco('AB_A',
                                lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                                          sm.wand(sm.knowsSnailClip(),
                                                                  sm.haveItem('Morph'))),
                                                   sm.haveItem('Gravity')))
    }, internal=True),
    AccessPoint('Aqueduct', 'EastMaridia', {
        'Aqueduct Bottom': lambda sm: SMBool(True) # go down
    }, internal=True,
       start = {'spawn': 0x0405, 'solveArea': "Maridia Pink Bottom", 'save':"Save_Aqueduct",
                'doors': [0x96]}),
    AccessPoint('Post Botwoon', 'EastMaridia', {
        'Aqueduct Bottom': lambda sm: sm.wor(sm.wand(sm.canJumpUnderwater(), # can't access the sand pits from the right side of the room
                                                     sm.haveItem('Morph')),
                                             sm.wand(sm.haveItem('Gravity'),
                                                     sm.haveItem('SpeedBooster'))),
        'Colosseum Top Right': lambda sm: sm.canBotwoonExitToColosseum(),
        'Toilet Top': lambda sm: sm.wand(sm.canReachCacatacAlleyFromBotowoon(),
                                         sm.canPassCacatacAlley())
    }, internal=True),
    AccessPoint('West Sand Hall Left', 'EastMaridia', {
        # XXX there might be some tech to do this suitless, but HJ+ice is not enough
        'Oasis Bottom': lambda sm: sm.haveItem('Gravity'),
        'Aqueduct Bottom': lambda sm: RomPatches.has(RomPatches.MaridiaSandWarp),
        # this goes directly to WestMaridia
        'Main Street Bottom': Cache.ldeco('WSHL_MSB',
                                          lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                             sm.wor(sm.canGreenGateGlitch(),
                                                                    RomPatches.has(RomPatches.AreaRandoGatesOther)))),
        # this goes directly to WestMaridia
        'Crab Hole Bottom Left': Cache.ldeco('WSHL_CHBL',
                                             lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                                sm.haveItem('Morph')))
    }, internal=True),
    AccessPoint('Left Sandpit', 'EastMaridia', {
        'West Sand Hall Left': lambda sm: sm.canAccessSandPits(),
        'Oasis Bottom': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Oasis Bottom', 'EastMaridia', {
        'Toilet Top': lambda sm: sm.wand(sm.traverse('OasisTop'), sm.canDestroyBombWallsUnderwater()),
        'West Sand Hall Left': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Right Sandpit', 'EastMaridia', {
        'Oasis Bottom': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Le Coude Right', 'EastMaridia', {
        'Toilet Top': lambda sm: SMBool(True)
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('LeCoudeBottom')),
       roomInfo = {'RoomPtr':0x95a8, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd1, 'SamusY':0x88},
       dotOrientation = 'ne'),
    AccessPoint('Toilet Top', 'EastMaridia', {
        'Oasis Bottom': lambda sm: sm.wand(sm.traverse('PlasmaSparkBottom'), sm.canDestroyBombWallsUnderwater()),
        'Le Coude Right': lambda sm: SMBool(True),
        'Precious Room Top': Cache.ldeco('TT_PRT',
                                         lambda sm: sm.wand(Bosses.bossDead(sm, 'Draygon'),
                                                            # suitless could be possible with this but unreasonable: https://youtu.be/rtLwytH-u8o
                                                            sm.haveItem('Gravity'),
                                                            sm.traverse('ColosseumBottomRight')))
    }, internal=True),
    AccessPoint('Colosseum Top Right', 'EastMaridia', {
        'Post Botwoon': lambda sm: sm.canColosseumToBotwoonExit(),
        'Precious Room Top': lambda sm: sm.traverse('ColosseumBottomRight'), # go down
    }, internal = True),
    AccessPoint('Precious Room Top', 'EastMaridia', {
        'Colosseum Top Right': lambda sm: sm.canClimbColosseum(),
        'DraygonRoomOut': lambda sm: SMBool(True) # go down
    }, internal = True),
    # boss APs
    AccessPoint('DraygonRoomOut', 'EastMaridia', {
        'Precious Room Top': lambda sm: sm.canExitPreciousRoom()
    }, boss = True,
       roomInfo = {'RoomPtr':0xd78f, "area": 0x4, "songs":[0xd7a5]},
       exitInfo = {'DoorPtr':0xa840, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288, 'song':0x1b},
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 'e'),
    AccessPoint('DraygonRoomIn', 'EastMaridia', {
        'Draygon Room Bottom': Cache.ldeco('DRI_DRB',
                                           lambda sm: sm.wor(Bosses.bossDead(sm, "Draygon"),
                                                             sm.wand(sm.canFightDraygon(),
                                                                     sm.enoughStuffsDraygon())))
    }, boss = True,
       roomInfo = {'RoomPtr':0xda60, "area": 0x4},
       exitInfo = {'DoorPtr':0xa96c, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe3d9,
                   "exitAsmPtr": 0xf7f0},
       entryInfo = {'SamusX':0x1c8, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Draygon Room Bottom', 'EastMaridia', {
       'DraygonRoomIn': lambda sm: sm.wand(Bosses.bossDead(sm, 'Draygon'), sm.canExitDraygon())
    }, internal = True),
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
                                                 sm.traverse('RedTowerElevatorLeft'))
    }, roomInfo = {'RoomPtr':0xa322, "area": 0x1},
       exitInfo = {'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf},
       entryInfo = {'SamusX':0x2cd, 'SamusY':0x388},
       dotOrientation = 'ne'),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: sm.canPassRedTowerToMaridiaNode(),
        'Red Tower Top Left': lambda sm: sm.wor(RomPatches.has(RomPatches.HellwayBlueDoor), sm.traverse('RedTowerElevatorLeft'))
    }, traverse=lambda sm:sm.wor(RomPatches.has(RomPatches.RedTowerBlueDoors), sm.traverse('RedBrinstarElevatorTop')),
       roomInfo = {'RoomPtr':0x962a, "area": 0x0},
       exitInfo = {'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1},
       entryInfo = {'SamusX':0x80, 'SamusY':0x58},
       start={'spawn':0x010a, 'doors':[0x3c], 'patches':[RomPatches.HellwayBlueDoor], 'solveArea': "Red Brinstar Top", 'areaMode':True},
       dotOrientation = 'n'),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda sm: SMBool(True), # handled by room traverse function
        'Glass Tunnel Top': Cache.ldeco('ETR_GTT',
                                        lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                           sm.wor(sm.haveItem('Gravity'),
                                                                  sm.haveItem('HiJump')))),
        'Red Tower Top Left': lambda sm: sm.canClimbBottomRedTower()
    }, roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa384, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xce, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoGatesBase),
                                               sm.haveItem('Super'))
    }, traverse=lambda sm: RomPatches.has(RomPatches.AreaRandoGatesBase),
       roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0x3c6, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
                                               sm.canUsePowerBombs())
    }, traverse=Cache.ldeco('GTT_T',
                            lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
                                                      sm.haveItem('HiJump')),
                                               sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
                                                      sm.canUsePowerBombs()))),
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
    ('Crocomire Speedway Bottom', 'Crocomire Room Top'),
    ('Three Muskateers Room Left', 'Single Chamber Top Right'),
    ('Warehouse Entrance Left', 'East Tunnel Right'),
    ('East Tunnel Top Right', 'Crab Hole Bottom Left'),
    ('Caterpillar Room Top Right', 'Red Fish Room Left'),
    ('Glass Tunnel Top', 'Main Street Bottom'),
    ('Green Pirates Shaft Bottom Right', 'Golden Four'),
    ('Warehouse Entrance Right', 'Warehouse Zeela Room Left'),
    ('Crab Shaft Right', 'Aqueduct Top Left')
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

vanillaEscapeAnimalsTransitions = [
    ('Flyway Right 0', 'Bomb Torizo Room Left'),
    ('Flyway Right 1', 'Bomb Torizo Room Left'),
    ('Flyway Right 2', 'Bomb Torizo Room Left'),
    ('Flyway Right 3', 'Bomb Torizo Room Left'),
    ('Bomb Torizo Room Left Animals', 'Flyway Right')
]

escapeSource = 'Tourian Escape Room 4 Top Right'
escapeTargets = ['Green Brinstar Main Shaft Top Left', 'Basement Left', 'Business Center Mid Left', 'Crab Hole Bottom Right']


def getAccessPoint(apName, apList=None):
    if apList is None:
        apList = accessPoints
    return next(ap for ap in apList if ap.Name == apName)

class GraphUtils:
    log = utils.log.get('GraphUtils')

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

    def getPossibleStartAPs(areaMode, maxDiff, morphPlacement):
        ret = []
        refused = {}
        allStartAPs = GraphUtils.getStartAccessPointNames()
        for apName in allStartAPs:
            start = getAccessPoint(apName).Start
            ok = True
            cause = ""
            if 'knows' in start:
                for k in start['knows']:
                    if not Knows.knows(k, maxDiff):
                        ok = False
                        cause += Knows.desc[k]['display']+" is not known. "
                        break
            if 'areaMode' in start and start['areaMode'] != areaMode:
                ok = False
                cause += "Start location available only with area randomization enabled. "
            if 'forcedEarlyMorph' in start and start['forcedEarlyMorph'] == True and morphPlacement == 'late':
                ok = False
                cause += "Start location unavailable with late morph placement. "
            if ok:
                ret.append(apName)
            else:
                refused[apName] = cause
        return ret, refused

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

    def createAreaTransitions(lightAreaRando=False):
        if lightAreaRando:
            return GraphUtils.createLightAreaTransitions()
        else:
            return GraphUtils.createRegularAreaTransitions()

    def createRegularAreaTransitions(apList=None, apPred=None):
        if apList is None:
            apList = accessPoints
        if apPred is None:
            apPred = lambda ap: ap.isArea()
        tFrom = []
        tTo = []
        apNames = [ap.Name for ap in apList if apPred(ap) == True]
        transitions = []

        def findTo(trFrom):
            ap = getAccessPoint(trFrom, apList)
            fromArea = ap.GraphArea
            targets = [apName for apName in apNames if apName not in tTo and getAccessPoint(apName, apList).GraphArea != fromArea]
            if len(targets) == 0: # fallback if no area transition is found
                targets = [apName for apName in apNames if apName != ap.Name]
                if len(targets) == 0: # extreme fallback: loop on itself
                    targets = [ap.Name]
            return random.choice(targets)

        def addTransition(src, dst):
            tFrom.append(src)
            tTo.append(dst)

        while len(apNames) > 0:
            sources = [apName for apName in apNames if apName not in tFrom]
            src = random.choice(sources)
            dst = findTo(src)
            transitions.append((src, dst))
            addTransition(src, dst)
            addTransition(dst, src)
            toRemove = [apName for apName in apNames if apName in tFrom and apName in tTo]
            for apName in toRemove:
                apNames.remove(apName)
        return transitions

    def getAPs(apPredicate, apList=None):
        if apList is None:
            apList = accessPoints
        return [ap for ap in apList if apPredicate(ap) == True]

    def loopUnusedTransitions(transitions, apList=None):
        if apList is None:
            apList = accessPoints
        usedAPs = set()
        for (src,dst) in transitions:
            usedAPs.add(getAccessPoint(src, apList))
            usedAPs.add(getAccessPoint(dst, apList))
        unusedAPs = [ap for ap in apList if not ap.isInternal() and ap not in usedAPs]
        for ap in unusedAPs:
            transitions.append((ap.Name, ap.Name))

    def createMinimizerTransitions(startApName, locLimit):
        if startApName == 'Ceres':
            startApName = 'Landing Site'
        startAp = getAccessPoint(startApName)
        def getNLocs(locsPredicate, locList=None):
            if locList is None:
                locList = locations
            # leave out bosses and count post boss locs systematically
            return len([loc for loc in locList if locsPredicate(loc) == True and not loc.SolveArea.endswith(" Boss") and not loc.isBoss()])
        availAreas = list(sorted({ap.GraphArea for ap in accessPoints if ap.GraphArea != startAp.GraphArea and getNLocs(lambda loc: loc.GraphArea == ap.GraphArea) > 0}))
        areas = [startAp.GraphArea]
        GraphUtils.log.debug("availAreas: {}".format(availAreas))
        GraphUtils.log.debug("areas: {}".format(areas))
        inBossCheck = lambda ap: ap.Boss and ap.Name.endswith("In")
        nLocs = 0
        transitions = []
        usedAPs = []
        trLimit = 5
        locLimit -= 3 # 3 "post boss" locs will always be available, and are filtered out in getNLocs
        def openTransitions():
            nonlocal areas, inBossCheck, usedAPs
            return GraphUtils.getAPs(lambda ap: ap.GraphArea in areas and not ap.isInternal() and not inBossCheck(ap) and not ap in usedAPs)
        while nLocs < locLimit or len(openTransitions()) < trLimit:
            GraphUtils.log.debug("openTransitions="+str([ap.Name for ap in openTransitions()]))
            fromAreas = availAreas
            if nLocs >= locLimit:
                GraphUtils.log.debug("not enough open transitions")
                # we just need transitions, avoid adding a huge area
                fromAreas = []
                n = trLimit - len(openTransitions())
                while len(fromAreas) == 0:
                    fromAreas = [area for area in availAreas if len(GraphUtils.getAPs(lambda ap: not ap.isInternal())) > n]
                    n -= 1
                minLocs = min([getNLocs(lambda loc: loc.GraphArea == area) for area in fromAreas])
                fromAreas = [area for area in fromAreas if getNLocs(lambda loc: loc.GraphArea == area) == minLocs]
            elif len(openTransitions()) <= 1: # dont' get stuck by adding dead ends
                fromAreas = [area for area in fromAreas if len(GraphUtils.getAPs(lambda ap: ap.GraphArea == area and not ap.isInternal())) > 1]
            nextArea = random.choice(fromAreas)
            GraphUtils.log.debug("nextArea="+str(nextArea))
            apCheck = lambda ap: not ap.isInternal() and not inBossCheck(ap) and ap not in usedAPs
            possibleSources = GraphUtils.getAPs(lambda ap: ap.GraphArea in areas and apCheck(ap))
            possibleTargets = GraphUtils.getAPs(lambda ap: ap.GraphArea == nextArea and apCheck(ap))
            src = random.choice(possibleSources)
            dst = random.choice(possibleTargets)
            usedAPs += [src,dst]
            GraphUtils.log.debug("add transition: (src: {}, dst: {})".format(src.Name, dst.Name))
            transitions.append((src.Name,dst.Name))
            availAreas.remove(nextArea)
            areas.append(nextArea)
            GraphUtils.log.debug("areas: {}".format(areas))
            nLocs = getNLocs(lambda loc:loc.GraphArea in areas)
            GraphUtils.log.debug("nLocs: {}".format(nLocs))
        # we picked the areas, add transitions (bosses and tourian first)
        sourceAPs = openTransitions()
        random.shuffle(sourceAPs)
        targetAPs = GraphUtils.getAPs(lambda ap: (inBossCheck(ap) or ap.Name == "Golden Four") and not ap in usedAPs)
        random.shuffle(targetAPs)
        assert len(sourceAPs) >= len(targetAPs), "Minimizer: less source than target APs"
        while len(targetAPs) > 0:
            transitions.append((sourceAPs.pop().Name, targetAPs.pop().Name))
        transitions += GraphUtils.createRegularAreaTransitions(sourceAPs, lambda ap: not ap.isInternal())
        GraphUtils.log.debug("FINAL MINIMIZER transitions: {}".format(transitions))
        GraphUtils.loopUnusedTransitions(transitions)
        GraphUtils.log.debug("FINAL MINIMIZER nLocs: "+str(nLocs+3))
        GraphUtils.log.debug("FINAL MINIMIZER areas: "+str(areas))
        return transitions

    def createLightAreaTransitions():
        # group APs by area
        aps = {}
        totalCount = 0
        for ap in accessPoints:
            if not ap.isArea():
                continue
            if not ap.GraphArea in aps:
                aps[ap.GraphArea] = {'totalCount': 0, 'transCount': {}, 'apNames': []}
            aps[ap.GraphArea]['apNames'].append(ap.Name)
        # count number of vanilla transitions between each area
        for (srcName, destName) in vanillaTransitions:
            srcAP = getAccessPoint(srcName)
            destAP = getAccessPoint(destName)
            aps[srcAP.GraphArea]['transCount'][destAP.GraphArea] = aps[srcAP.GraphArea]['transCount'].get(destAP.GraphArea, 0) + 1
            aps[srcAP.GraphArea]['totalCount'] += 1
            aps[destAP.GraphArea]['transCount'][srcAP.GraphArea] = aps[destAP.GraphArea]['transCount'].get(srcAP.GraphArea, 0) + 1
            aps[destAP.GraphArea]['totalCount'] += 1
            totalCount += 1

        transitions = []
        while totalCount > 0:
            # choose transition
            srcArea = random.choice(list(aps.keys()))
            srcName = random.choice(aps[srcArea]['apNames'])
            src = getAccessPoint(srcName)
            destArea = random.choice(list(aps[src.GraphArea]['transCount'].keys()))
            destName = random.choice(aps[destArea]['apNames'])
            transitions.append((srcName, destName))

            # update counts
            totalCount -= 1
            aps[srcArea]['totalCount'] -= 1
            aps[destArea]['totalCount'] -= 1
            aps[srcArea]['transCount'][destArea] -= 1
            if aps[srcArea]['transCount'][destArea] == 0:
                del aps[srcArea]['transCount'][destArea]
            aps[destArea]['transCount'][srcArea] -= 1
            if aps[destArea]['transCount'][srcArea] == 0:
                del aps[destArea]['transCount'][srcArea]
            aps[srcArea]['apNames'].remove(srcName)
            aps[destArea]['apNames'].remove(destName)

            if aps[srcArea]['totalCount'] == 0:
                del aps[srcArea]
            if aps[destArea]['totalCount'] == 0:
                del aps[destArea]

        return transitions

    def getVanillaExit(apName):
        allVanillaTransitions = vanillaTransitions + vanillaBossesTransitions + vanillaEscapeTransitions
        for (src,dst) in allVanillaTransitions:
            if apName == src:
                return dst
            if apName == dst:
                return src
        return None

    def isEscapeAnimals(apName):
        return 'Flyway Right' in apName or 'Bomb Torizo Room Left' in apName

    # gets dict like
    # (RoomPtr, (vanilla entry screen X, vanilla entry screen Y)): AP
    def getRooms():
        rooms = {}
        for ap in accessPoints:
            if ap.Internal == True:
                continue
            # special ap for random escape animals surprise
            if GraphUtils.isEscapeAnimals(ap.Name):
                continue

            roomPtr = ap.RoomInfo['RoomPtr']

            vanillaExitName = GraphUtils.getVanillaExit(ap.Name)
            # special ap for random escape animals surprise
            if GraphUtils.isEscapeAnimals(vanillaExitName):
                continue

            connAP = getAccessPoint(vanillaExitName)
            entryInfo = connAP.ExitInfo
            rooms[(roomPtr, entryInfo['screen'], entryInfo['direction'])] = ap
            rooms[(roomPtr, entryInfo['screen'], (ap.EntryInfo['SamusX'], ap.EntryInfo['SamusY']))] = ap
            # for boss rando with incompatible ridley transition, also register this one
            if ap.Name == 'RidleyRoomIn':
                rooms[(roomPtr, (0x0, 0x1), 0x5)] = ap
                rooms[(roomPtr, (0x0, 0x1), (0xbf, 0x198))] = ap

        return rooms

    def escapeAnimalsTransitions(graph, possibleTargets, firstEscape):
        n = len(possibleTargets)
        assert n < 4, "Invalid possibleTargets list: " + str(possibleTargets)
        # first get our list of 4 entries for escape patch
        if n >= 1:
            # get actual animals: pick one of the remaining targets
            animalsAccess = possibleTargets.pop()
            graph.EscapeAttributes['Animals'] = animalsAccess
            # we now have at most 2 targets left, fill up to fill cycling 4 targets for animals suprise
            possibleTargets.append('Climb Bottom Left')
            possibleTargets.append(firstEscape)
            poss = possibleTargets[:]
            while len(possibleTargets) < 4:
                possibleTargets.append(poss.pop(random.randint(0, len(poss)-1)))
        else:
            # failsafe: if not enough targets left, abort and do vanilla animals
            animalsAccess = 'Flyway Right'
            possibleTargets = ['Bomb Torizo Room Left'] * 4
        assert len(possibleTargets) == 4, "Invalid possibleTargets list: " + str(possibleTargets)
        # actually add the 4 connections for successive escapes challenge
        basePtr = 0xADAC
        btDoor = getAccessPoint('Flyway Right')
        for i in range(len(possibleTargets)):
            ap = copy.copy(btDoor)
            ap.Name += " " + str(i)
            ap.ExitInfo['DoorPtr'] = basePtr + i*24
            graph.addAccessPoint(ap)
            target = possibleTargets[i]
            graph.addTransition(ap.Name, target)
        # add the connection for animals access
        bt = getAccessPoint('Bomb Torizo Room Left')
        btCpy = copy.copy(bt)
        btCpy.Name += " Animals"
        btCpy.ExitInfo['DoorPtr'] = 0xAE00
        graph.addAccessPoint(btCpy)
        graph.addTransition(animalsAccess, btCpy.Name)

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

    def getDoorConnections(graph, areas=True, bosses=False,
                           escape=True, escapeAnimals=True):
        transitions = []
        if areas:
            transitions += vanillaTransitions
        if bosses:
            transitions += vanillaBossesTransitions
        if escape:
            transitions += vanillaEscapeTransitions
            if escapeAnimals:
                transitions += vanillaEscapeAnimalsTransitions
        for srcName, dstName in transitions:
            src = graph.accessPoints[srcName]
            dst = graph.accessPoints[dstName]
            dst.EntryInfo.update(src.ExitInfo)
            src.EntryInfo.update(dst.ExitInfo)
        connections = []
        for src, dst in graph.InterAreaTransitions:
            if not (escape and src.Escape and dst.Escape):
                # area only
                if not bosses and src.Boss:
                    continue
                # boss only
                if not areas and not src.Boss:
                    continue
                # no random escape
                if not escape and src.Escape:
                    continue

            conn = {}
            conn['ID'] = str(src) + ' -> ' + str(dst)
            # remove duplicates (loop transitions)
            if any(c['ID'] == conn['ID'] for c in connections):
                continue
#            print(conn['ID'])
            # where to write
            conn['DoorPtr'] = src.ExitInfo['DoorPtr']
            # door properties
            conn['RoomPtr'] = dst.RoomInfo['RoomPtr']
            conn['doorAsmPtr'] = dst.EntryInfo['doorAsmPtr']
            if 'exitAsmPtr' in src.ExitInfo:
                conn['exitAsmPtr'] = src.ExitInfo['exitAsmPtr']
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

    def hasMixedTransitions(areaTransitions, bossTransitions):
        vanillaAPs = []
        for (src, dest) in vanillaTransitions:
            vanillaAPs += [src, dest]

        vanillaBossesAPs = []
        for (src, dest) in vanillaBossesTransitions:
            vanillaBossesAPs += [src, dest]

        for (src, dest) in areaTransitions:
            if src in vanillaBossesAPs or dest in vanillaBossesAPs:
                return True

        for (src, dest) in bossTransitions:
            if src in vanillaAPs or dest in vanillaAPs:
                return True

        return False
