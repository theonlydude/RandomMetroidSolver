from graph.graph import AccessPoint
from utils.parameters import Settings
from rom.rom_patches import RomPatches
from logic.smbool import SMBool
from logic.helpers import Bosses
from logic.cache import Cache

# all access points and traverse functions
accessPoints = [
    ### Ceres Station
    AccessPoint('Ceres', 'Ceres', 'Ceres', {
        'Landing Site': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0xfffe, 'doors':[0x32], 'patches':[RomPatches.BlueBrinstarBlueDoor], 'solveArea': "Crateria Landing Site"}),
    ### Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', 'Crateria Landing Site', {
        'Lower Mushrooms Left': Cache.ldeco(lambda sm: sm.wand(sm.canPassTerminatorBombWall(),
                                                               sm.canPassCrateriaGreenPirates())),
        'Keyhunter Room Bottom': Cache.ldeco(lambda sm: sm.traverse('LandingSiteRight')),
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True),
        'Gauntlet Top': lambda sm: sm.canDoGauntletFromLandingSite()
    }, internal=True,
       start={'spawn': 0x0000, 'doors':[0x32], 'patches':[RomPatches.BlueBrinstarBlueDoor], 'solveArea': "Crateria Landing Site"}),
    AccessPoint('Blue Brinstar Elevator Bottom', 'Crateria', 'Blue Brinstar', {
        'Morph Ball Room Left': lambda sm: sm.canUsePowerBombs(),
        'Landing Site': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Gauntlet Top', 'Crateria', 'Crateria Gauntlet', {
        'Green Pirates Shaft Bottom Right': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'), sm.canPassCrateriaGreenPirates()))
    }, internal=True,
       start={'spawn': 0x0006, 'solveArea': "Crateria Gauntlet", 'save':"Save_Gauntlet", 'forcedEarlyMorph':True}),
    AccessPoint('Lower Mushrooms Left', 'Crateria', 'Crateria Terminator', {
        'Landing Site': Cache.ldeco(lambda sm: sm.wand(sm.canPassTerminatorBombWall(False),
                                                       sm.canPassCrateriaGreenPirates())),
        'Green Pirates Shaft Bottom Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9969, "area": 0x0, 'songs':[0x997a]},
       exitInfo = {'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x36, 'SamusY':0x88, 'song': 0x9},
       dotOrientation = 'nw'),
    AccessPoint('Green Pirates Shaft Bottom Right', 'Crateria', 'Crateria Terminator', {
        'Lower Mushrooms Left': lambda sm: SMBool(True)
    }, traverse = Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                                sm.traverse('GreenPiratesShaftBottomRight'))),
       roomInfo = {'RoomPtr':0x99bd, "area": 0x0, 'songs':[0x99ce]},
       exitInfo = {'DoorPtr':0x8c52, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x688, 'song': 0x9},
       dotOrientation = 'e'),
    AccessPoint('Moat Right', 'Crateria', 'Crateria Moat', {
        'Moat Left': lambda sm: sm.canPassMoatReverse()
    }, roomInfo = {'RoomPtr':0x95ff, "area": 0x0, 'songs':[0x9610]},
       exitInfo = {'DoorPtr':0x8aea, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1cf, 'SamusY':0x88, 'song': 0xc},
       dotOrientation = 'ne'),
    AccessPoint('Moat Left', 'Crateria', 'Crateria Moat', {
        'Keyhunter Room Bottom': lambda sm: SMBool(True),
        'Moat Right': lambda sm: sm.canPassMoatFromMoat()
    }, internal=True),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', 'Crateria Landing Site', {
        'Moat Left': Cache.ldeco(lambda sm: sm.traverse('KihunterRight')),
        'Moat Right': Cache.ldeco(lambda sm: sm.wand(sm.traverse('KihunterRight'), sm.canPassMoat())),
        'Landing Site': lambda sm: SMBool(True)
    }, traverse = Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                                sm.traverse('KihunterBottom'))),
       roomInfo = { 'RoomPtr':0x948c, "area": 0x0, 'songs':[0x949d] },
       exitInfo = {'DoorPtr':0x8a42, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14c, 'SamusY':0x2b8, 'song': 0xc},
       dotOrientation = 'se'),
    AccessPoint('Morph Ball Room Left', 'Crateria', 'Blue Brinstar', {
        'Blue Brinstar Elevator Bottom': lambda sm: sm.canUsePowerBombs()
    }, roomInfo = { 'RoomPtr':0x9e9f, "area": 0x1},
       exitInfo = {'DoorPtr':0x8e9e, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288},
       dotOrientation = 'sw'),
    # Escape APs
    AccessPoint('Climb Bottom Left', 'Crateria', 'Crateria Landing Site', {
        'Landing Site': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x96ba, "area": 0x0},
       exitInfo = {'DoorPtr':0x8b6e, 'direction': 0x5, "cap": (0x2e, 0x16), "bitFlag": 0x0,
                   "screen": (0x2, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x888},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Flyway Right', 'Crateria', 'Crateria Bombs', {},
       roomInfo = {'RoomPtr':0x9879, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bc2, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000,
                   "exitAsm": "rando_escape_common_setup_next_escape"},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True),
    AccessPoint('Bomb Torizo Room Left', 'Crateria', 'Crateria Bombs', {},
       roomInfo = {'RoomPtr':0x9804, "area": 0x0},
       exitInfo = {'DoorPtr':0x8baa, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0xb8},
       escape = True),
    ### Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator', 'GreenPinkBrinstar', 'Green Brinstar', {
        'Big Pink': Cache.ldeco(lambda sm: sm.wand(sm.canPassDachoraRoom(),
                                                   sm.traverse('MainShaftBottomRight'))),
        'Etecoons Bottom': lambda sm: sm.canAccessEtecoons()
    }, roomInfo = {'RoomPtr':0x9938, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x88},
       start = {
           'spawn': 0x0108, 'doors':[0x1f, 0x21, 0x26],
           'patches':[RomPatches.BrinReserveBlueDoors],
           'layout': ['early_super_bridge'],
           'solveArea': "Green Brinstar"
       },
       dotOrientation = 'ne'),
    AccessPoint('Big Pink', 'GreenPinkBrinstar', 'Pink Brinstar', {
        'Green Hill Zone Top Right': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                    sm.traverse('BigPinkBottomRight'))),
        'Green Brinstar Elevator': lambda sm: sm.canPassDachoraRoom()
    }, internal=True, start={'spawn': 0x0100, 'layout': ['spospo_save'], 'solveArea': "Pink Brinstar"}),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', 'Brinstar Hills', {
        'Noob Bridge Right': lambda sm: SMBool(True),
        'Big Pink': Cache.ldeco(lambda sm: sm.haveItem('Morph'))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('GreenHillZoneTopRight'))),
       roomInfo = {'RoomPtr':0x9e52, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', 'Brinstar Hills', {
        'Green Hill Zone Top Right': Cache.ldeco(lambda sm: sm.wor(sm.haveItem('Wave'),
                                                                   sm.wor(RomPatches.has(RomPatches.GreenHillsGateRemoved),
                                                                          sm.canBlueGateGlitch())))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('NoobBridgeRight'))),
       roomInfo = {'RoomPtr':0x9fba, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8f0a, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x5ce, 'SamusY':0x88},
       dotOrientation = 'se'),
    AccessPoint('Green Brinstar Main Shaft Top Left', 'GreenPinkBrinstar', 'Green Brinstar', {
        'Green Brinstar Elevator': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9ad9, "area": 0x1},
       exitInfo = {'DoorPtr':0x8cb2, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Brinstar Pre-Map Room Right', 'GreenPinkBrinstar', 'Green Brinstar', {
    }, roomInfo = {'RoomPtr':0x9b9d, "area": 0x1},
       exitInfo = {'DoorPtr':0x8d42, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Etecoons Supers', 'GreenPinkBrinstar', 'Green Brinstar', {
        'Etecoons Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0x0107, 'doors':[0x34], 'patches':[RomPatches.EtecoonSupersBlueDoor],
              'save':"Save_Etecoons" ,'solveArea': "Green Brinstar",
              'forcedEarlyMorph':True, 'needsPreRando': True}),
    AccessPoint('Etecoons Bottom', 'GreenPinkBrinstar', 'Green Brinstar', {
        'Etecoons Supers': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.EtecoonSupersBlueDoor),
                                                         sm.traverse('EtecoonEnergyTankLeft'))),
        'Green Brinstar Elevator': lambda sm: sm.canUsePowerBombs()
    }, internal=True),
    ### Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', 'WreckedShip Bottom', {
        'Wrecked Ship Main': Cache.ldeco(lambda sm: sm.traverse('WestOceanRight'))
    }, roomInfo = {'RoomPtr':0x93fe, "area": 0x0},
       exitInfo = {'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Wrecked Ship Main', 'WreckedShip', 'WreckedShip Main', {
        'West Ocean Left': lambda sm: SMBool(True),
        'Wrecked Ship Back': Cache.ldeco(lambda sm: sm.wor(sm.wand(Bosses.bossDead(sm, 'Phantoon'),
                                                                   sm.canPassSpongeBath()),
                                                           sm.wand(sm.wnot(Bosses.bossDead(sm, 'Phantoon')),
                                                                   RomPatches.has(RomPatches.SpongeBathBlueDoor)))),
        'PhantoonRoomOut': Cache.ldeco(lambda sm: sm.wand(sm.traverse('WreckedShipMainShaftBottom'), sm.canPassBombPassages())),
        'Bowling': Cache.ldeco(lambda sm: sm.wand(sm.canMorphJump(),
                                                  sm.canPassBowling()))
    }, internal=True,
       start={'spawn':0x0300,
              'doors':[0x83,0x8b], 'patches':[RomPatches.SpongeBathBlueDoor, RomPatches.WsEtankBlueDoor],
              'variaTweaks': ['WS_Etank'],
              'solveArea': "WreckedShip Main",
              'needsPreRando':True}),
    AccessPoint('Wrecked Ship Back', 'WreckedShip', 'WreckedShip Back', {
        'Wrecked Ship Main': lambda sm: SMBool(True),
        'Crab Maze Left': Cache.ldeco(lambda sm: sm.wand(sm.canPassForgottenHighway(True), sm.haveItem('Morph')))
    }, internal=True),
    AccessPoint('Bowling', 'WreckedShip', 'WreckedShip Gravity', {
        'West Ocean Left': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Crab Maze Left', 'WreckedShip', 'WreckedShip Back', {
        'Wrecked Ship Back': Cache.ldeco(lambda sm: sm.wand(sm.canPassForgottenHighway(False), sm.haveItem('Morph')))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors),
                                              sm.traverse('LeCoudeBottom'))), # it is not exactly coude's door
                                                                              # but it's equivalent in vanilla anyway
       roomInfo = {'RoomPtr':0x957d, "area": 0x0, 'songs':[0x958e]},
       exitInfo = {'DoorPtr':0x8aae, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188, 'song': 0xc},
       dotOrientation = 'e'),
    AccessPoint('PhantoonRoomOut', 'WreckedShip', 'Phantoon Boss', {
        'Wrecked Ship Main': lambda sm: sm.canPassBombPassages()
    }, boss = True,
       roomInfo = {'RoomPtr':0xcc6f, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2ac, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x49f, 'SamusY':0xb8},
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 's'),
    AccessPoint('PhantoonRoomIn', 'WreckedShip', 'Phantoon Boss', {},
       boss = True,
       roomInfo = {'RoomPtr':0xcd13, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2c4, 'direction': 0x5, "cap": (0x4e, 0x6), "bitFlag": 0x0,
                   "screen": (0x4, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe1fe,
                   "exitAsm": "door_transition_boss_exit_fix"},
       entryInfo = {'SamusX':0x2e, 'SamusY':0xb8},
       dotOrientation = 's'),
    AccessPoint('Basement Left', 'WreckedShip', 'WreckedShip Main', {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xcc6f, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2a0, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2e, 'SamusY':0x88},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Wrecked Ship Map Room', 'WreckedShip', 'WreckedShip Main', {
    }, roomInfo = {'RoomPtr':0xcccb, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2b8, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', 'Lower Norfair Screw Attack', {
        'LN Entrance': lambda sm: sm.canPassLavaPit()
    }, roomInfo = {'RoomPtr':0xaf14, "area": 0x2, 'songs':[0xaf25]},
       exitInfo = {'DoorPtr':0x96d2, 'direction': 0x4, "cap": (0x11, 0x26), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x3d0, 'SamusY':0x88, 'song': 0x15},
       dotOrientation = 'w'),
    AccessPoint('LN Entrance', 'LowerNorfair', 'Lower Norfair Screw Attack', {
        'Lava Dive Right': lambda sm: sm.canPassLavaPitReverse(),
        'LN Above GT': Cache.ldeco(lambda sm: sm.wand(sm.wor(sm.wnot(RomPatches.has(RomPatches.DreadMode)),
                                                             sm.haveItem("SpaceJump"), sm.haveItem("ScrewAttack"),
                                                             sm.canShortCharge()),
                                                      sm.canPassLowerNorfairChozo())),
        'Screw Attack Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                              sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.canGreenGateGlitch(),
                                                              sm.canDestroyBombWalls())),
        'Worst Room Top': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                         sm.canPassWorstRoom(),
                                                         sm.wand(sm.canUsePowerBombs(),
                                                                 sm.wor(sm.wnot(RomPatches.has(RomPatches.DreadMode)),
                                                                        sm.canSimpleShortCharge(), # spark from ripper room
                                                                        sm.haveItem("ScrewAttack")))))
    }, internal=True),
    AccessPoint('LN Above GT', 'LowerNorfair', 'Lower Norfair Screw Attack', {
        'LN Entrance': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canPassBombPassages())),
        'Screw Attack Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.enoughStuffGT()))
    }, internal=True),
    AccessPoint('Screw Attack Bottom', 'LowerNorfair', 'Lower Norfair Screw Attack', {
        'LN Entrance': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canExitScrewAttackArea(),
                                                      sm.haveItem('Super'),
                                                      sm.canUsePowerBombs()))
    }, internal=True),
    AccessPoint('Worst Room Top', 'LowerNorfair', 'Lower Norfair Before Amphitheater', {
        'Firefleas': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
        'LN Entrance': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canPassWorstRoomPirates(),
                                                      sm.canUsePowerBombs(),
                                                      sm.wor(sm.wnot(RomPatches.has(RomPatches.DreadMode)),
                                                             sm.haveItem("ScrewAttack"))))
    }, internal=True),
    AccessPoint('Firefleas', 'LowerNorfair', 'Lower Norfair After Amphitheater', {
        'Worst Room Top': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                         sm.canPassAmphitheaterReverse())),
        'Three Muskateers Room Left': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                                     sm.haveItem('Morph'),
                                                                     # check for only 3 ki hunters this way
                                                                     sm.canPassRedKiHunterStairs())),
        'Ridley Zone': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.traverse('WastelandLeft'),
                                                      sm.traverse('RedKihunterShaftBottom'),
                                                      sm.canGetBackFromRidleyZone(),
                                                      sm.canPassRedKiHunterStairs(),
                                                      sm.canPassWastelandDessgeegas(),
                                                      sm.canPassNinjaPirates())),
        'Screw Attack Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.canPassAmphitheaterReverse(),
                                                              sm.canDestroyBombWalls(),
                                                              sm.wor(sm.wnot(RomPatches.has(RomPatches.DreadMode)), sm.haveItem("ScrewAttack")),
                                                              sm.canGreenGateGlitch())),
        'Firefleas Top': Cache.ldeco(lambda sm: sm.wand(sm.canPassBombPassages(),
                                                        sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])))
    }, internal=True),
    AccessPoint('Firefleas Top', 'LowerNorfair', 'Lower Norfair After Amphitheater', {
        # this weird condition basically says: "if we start here, give heat protection"
        'Firefleas': Cache.ldeco(lambda sm: sm.wor(sm.wnot(RomPatches.has(RomPatches.LowerNorfairPBRoomHeatDisable)),
                                                   sm.heatProof()))
    }, internal=True,
       start={'spawn':0x0207,
              'rom_patches': ['LN_PB_Heat_Disable', 'LN_Firefleas_Remove_Fune','firefleas_shot_block.ips'],
              'patches':[RomPatches.LowerNorfairPBRoomHeatDisable, RomPatches.FirefleasRemoveFune],
              'knows': ["FirefleasWalljump"],
              'save': "Save_Firefleas", 'needsPreRando': True,
              'solveArea': "Lower Norfair After Amphitheater",
              'forcedEarlyMorph':True}),
    AccessPoint('Ridley Zone', 'LowerNorfair', 'Lower Norfair Wasteland', {
        'Firefleas': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.canGetBackFromRidleyZone(),
                                                    sm.canPassWastelandDessgeegas(),
                                                    sm.canPassRedKiHunterStairs())),
        'RidleyRoomOut': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])),
        'Wasteland': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.canGetBackFromRidleyZone(),
                                                    sm.canPassWastelandDessgeegas()))
    }, internal=True),
    AccessPoint('Wasteland', 'LowerNorfair', 'Lower Norfair Wasteland', {
        # no transition to firefleas to exclude pb of shame location when starting at firefleas top
        'Ridley Zone': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.traverse('WastelandLeft'),
                                                      sm.canGetBackFromRidleyZone(),
                                                      sm.canPassWastelandDessgeegas(),
                                                      sm.canPassNinjaPirates()))
    }, internal=True),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', 'Lower Norfair After Amphitheater', {
        'Firefleas': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.haveItem('Morph'),
                                                    sm.canPassThreeMuskateers()))
    }, roomInfo = {'RoomPtr':0xb656, "area": 0x2},
       exitInfo = {'DoorPtr':0x9a4a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x88},
       dotOrientation = 'n'),
    AccessPoint('RidleyRoomOut', 'LowerNorfair', 'Ridley Boss', {
        'Ridley Zone': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']))
    }, boss = True,
       roomInfo = {'RoomPtr':0xb37a, "area": 0x2},
       exitInfo = {'DoorPtr':0x98ca, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x2e, 'SamusY':0x98},
       traverse=Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                               sm.canOpenEyeDoors())),
       dotOrientation = 'e'),
    AccessPoint('RidleyRoomIn', 'LowerNorfair', 'Ridley Boss', {},
       boss = True,
       roomInfo = {'RoomPtr':0xb32e, "area": 0x2},
       exitInfo = {'DoorPtr':0x98be, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0xbf, 'SamusY':0x198}, # on Ridley's platform. entry screen has to be changed (see getDoorConnections)
       dotOrientation = 'e'),
    ### Kraid
    AccessPoint('Warehouse Zeela Room Left', 'Kraid', 'Kraid', {
        'KraidRoomOut': lambda sm: sm.canPassBombPassages()
    }, roomInfo = {'RoomPtr': 0xa471, "area": 0x1, 'songs':[0xa482]},
       exitInfo = {'DoorPtr': 0x913e, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbd3f},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88, 'song':0x12},
       dotOrientation = 'w'),
    AccessPoint('KraidRoomOut', 'Kraid', 'Kraid Boss', {
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
    AccessPoint('KraidRoomIn', 'Kraid', 'Kraid Boss', {},
       boss = True,
       roomInfo = {'RoomPtr':0xa59f, "area": 0x1},
       exitInfo = {'DoorPtr':0x91ce, 'direction': 0x5, "cap": (0x1e, 0x16), "bitFlag": 0x0,
                   "screen": (0x1, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0,
                   "exitAsm": "door_transition_kraid_exit_fix"},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       dotOrientation = 'e'),
    ### Norfair
    AccessPoint('Warehouse Entrance Left', 'Norfair', 'Norfair Entrance', {
        'Warehouse Entrance Right': lambda sm: sm.canAccessKraidsLair(),
        'Business Center': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr':0x922e, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x40,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdd1},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'sw'),
    AccessPoint('Warehouse Entrance Right', 'Norfair', 'Norfair Entrance', {
        'Warehouse Entrance Left': Cache.ldeco(lambda sm: sm.haveItem('Super'))
    }, roomInfo = {'RoomPtr': 0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr': 0x923a, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX': 0x2c7, 'SamusY': 0x98},
       dotOrientation = 'nw'),
    AccessPoint('Business Center', 'Norfair', 'Norfair Entrance', {
        'Cathedral': Cache.ldeco(lambda sm: sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles']['mult'])),
        'Bubble Mountain': Cache.ldeco(# go through cathedral
                                       lambda sm: sm.wand(sm.traverse('CathedralRight'),
                                                          sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Bubble']['mult']))),
        'Bubble Mountain Bottom': lambda sm: sm.canPassFrogSpeedwayLeftToRight(),
        'Crocomire Speedway Bottom': Cache.ldeco(lambda sm: sm.wor(sm.wand(sm.canPassFrogSpeedwayLeftToRight(),
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
       start={
           'spawn':0x0208, 'doors':[0x4d],
           'patches':[RomPatches.HiJumpAreaBlueDoor],
           'layout': ['high_jump', 'nova_boost_platform'],
           'solveArea': "Norfair Entrance", 'needsPreRando':True
       }
    ),
    AccessPoint('Single Chamber Top Right', 'Norfair', 'Bubble Norfair Wave', {
        'Bubble Mountain Top': Cache.ldeco(lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                              sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain'])))
    },  roomInfo = {'RoomPtr':0xad5e, "area": 0x2},
        exitInfo = {'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                    "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
        entryInfo = {'SamusX':0x5cf, 'SamusY':0x88},
        dotOrientation = 'ne'),
    AccessPoint('Cathedral', 'Norfair', 'Norfair Cathedral', {
        'Business Center': Cache.ldeco(lambda sm: sm.canExitCathedral(Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles'])),
        'Bubble Mountain': Cache.ldeco(lambda sm: sm.wand(sm.traverse('CathedralRight'),
                                                          sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles'])))
    }, internal=True),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', 'Bubble Norfair Wave', {
        'Bubble Mountain Bottom': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain'])),
        'Bubble Mountain Top': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room -> Bubble Mountain Top']))), # go all the way around
        'Crocomire Speedway Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                                    sm.wor(sm.haveItem('Wave'),
                                                                           sm.canBlueGateGlitch()))),
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('KronicBoostBottomLeft'))),
       roomInfo = {'RoomPtr':0xae74, "area": 0x2, 'songs':[0xae85]},
       exitInfo = {'DoorPtr':0x967e, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x288, 'song': 0x15},
       dotOrientation = 'se'),
    AccessPoint('Crocomire Speedway Bottom', 'Norfair', 'Norfair Grapple Escape', {
        'Grapple Escape': lambda sm: sm.canGrappleEscape(),
        'Business Center': Cache.ldeco(lambda sm: sm.wand(sm.canPassFrogSpeedwayRightToLeft(),
                                                          sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Norfair Entrance']))),
        'Bubble Mountain Bottom': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Bubble Mountain'])),
        'Kronic Boost Room Bottom Left': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                                        sm.haveItem('Morph')))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.CrocBlueDoors), sm.traverse('CrocomireSpeedwayBottom'))),
       roomInfo = {'RoomPtr':0xa923, "area": 0x2},
       exitInfo = {'DoorPtr':0x93d2, 'direction': 0x6, "cap": (0x36, 0x2), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xc57, 'SamusY':0x2b8},
       dotOrientation = 'se'),
    AccessPoint('Grapple Escape', 'Norfair', 'Norfair Grapple Escape', {
        'Business Center': lambda sm: sm.haveItem('Super'),
        'Crocomire Speedway Bottom': lambda sm: sm.canHellRunBackFromGrappleEscape()
    }, internal=True),
    AccessPoint('Bubble Mountain', 'Norfair', 'Bubble Norfair Bottom', {
        'Business Center': lambda sm: sm.canExitCathedral(Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Entrance']),
        'Bubble Mountain Top': lambda sm: sm.canClimbBubbleMountain(),
        'Cathedral': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles'])),
        'Bubble Mountain Bottom': lambda sm: sm.canPassBombPassages()
    }, internal=True,
       start={
           'spawn':0x0201, 'doors':[0x54,0x55],
           'patches':[RomPatches.SpeedAreaBlueDoors],
           'knows':['BubbleMountainWallJump'],
           'layout': ['nova_boost_platform'],
           'areaLayout': ['area_layout_ln_exit'],
           'solveArea': "Bubble Norfair Bottom"
       }
    ),
    AccessPoint('Bubble Mountain Top', 'Norfair', 'Bubble Norfair Speed', {
        'Kronic Boost Room Bottom Left': Cache.ldeco(# go all the way around
                                                     lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room wo/Bomb']))),
        'Single Chamber Top Right': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']),
                                                                   sm.canDestroyBombWalls(),
                                                                   sm.haveItem('Morph'),
                                                                   RomPatches.has(RomPatches.SingleChamberNoCrumble))),
        'Bubble Mountain': lambda sm: SMBool(True),
        # all the way around
        'Bubble Mountain Bottom': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                 sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble Top <-> Bubble Bottom'])))
    }, internal=True),
    AccessPoint('Bubble Mountain Bottom', 'Norfair', 'Bubble Norfair Bottom', {
        'Bubble Mountain': lambda sm: sm.canPassBombPassages(),
        'Crocomire Speedway Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Croc']),
                                                                    sm.wor(sm.canBlueGateGlitch(),
                                                                           sm.haveItem('Wave')))),
        'Kronic Boost Room Bottom Left': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room'])),
        'Business Center': lambda sm: sm.canPassFrogSpeedwayRightToLeft(),
        # all the way around
        'Bubble Mountain Top': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble Top <-> Bubble Bottom'])))
    }, internal=True),
    AccessPoint('Business Center Mid Left', 'Norfair', 'Norfair Entrance', {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa7de, "area": 0x2},
       exitInfo = {'DoorPtr':0x9306, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Norfair Map Room', 'Norfair', 'Norfair Entrance', {
    }, roomInfo = {'RoomPtr':0xb0b4, "area": 0x2},
       exitInfo = {'DoorPtr':0x97c2, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### Croc
    AccessPoint('Crocomire Room Top', 'Crocomire', 'Crocomire', {
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.CrocBlueDoors), sm.enoughStuffCroc())),
       roomInfo = {'RoomPtr':0xa98d, "area": 0x2, 'songs':[0xa9bd]},
       exitInfo = {'DoorPtr':0x93ea, 'direction': 0x7, "cap": (0xc6, 0x2d), "bitFlag": 0x0,
                   "screen": (0xc, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0x0000,
                   "exitAsm": "door_transition_boss_exit_fix"},
       entryInfo = {'SamusX':0x383, 'SamusY':0x98, 'song': 0x15},
       dotOrientation = 'se'),
    ### West Maridia
    AccessPoint('Main Street Bottom', 'WestMaridia', 'Maridia Green', {
        'Red Fish Room Bottom': lambda sm: sm.canGoUpMtEverest(),
        'Crab Hole Bottom Left': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                sm.canTraverseCrabTunnelLeftToRight())),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                       sm.traverse('MainStreetBottomRight'),
                                                       sm.wor(RomPatches.has(RomPatches.CrabTunnelGreenGateRemoved),
                                                              sm.haveItem('Super')),
                                                       sm.canTraverseWestSandHallLeftToRight())),
        'Crab Shaft Left': lambda sm: sm.canPassMtEverest(),
        "Mama Turtle": lambda sm: sm.canAccessMamaTurtleFromMainStreet()
    }, roomInfo = {'RoomPtr':0xcfc9, "area": 0x4},
       exitInfo = {'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8},
       dotOrientation = 's'),
    AccessPoint('Mama Turtle', 'WestMaridia', 'Maridia Green', {
        'Main Street Bottom': lambda sm: sm.canJumpUnderwater()
    }, internal=True,
       start = {'spawn': 0x0406, 'solveArea': "Maridia Green",
                'save':"Save_Mama", 'needsPreRando':True,
                'patches':[RomPatches.MamaTurtleBlueDoor],
                'areaLayout': ['area_layout_crab_hole', 'area_rando_gate_crab_tunnel'],
                'rom_patches':['mama_save.ips'], 'doors': [0x8e]}),
    AccessPoint('Crab Hole Bottom Left', 'WestMaridia', 'Maridia Green', {
        'Main Street Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canExitCrabHole(),
                                                             sm.wor(RomPatches.has(RomPatches.CrabTunnelGreenGateRemoved),
                                                                    sm.canGreenGateGlitch()))),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                       sm.canExitCrabHole(),
                                                       sm.canTraverseWestSandHallLeftToRight()))
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa510, 'direction': 0x5,
                   "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                   "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x28, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('Red Fish Room Left', 'WestMaridia', 'Maridia Green', {
        'Red Fish Room Bottom': Cache.ldeco(lambda sm: sm.haveItem('Morph')) # just go down
    }, roomInfo = {'RoomPtr':0xd104, "area": 0x4},
       exitInfo = {'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                   "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'w'),
    AccessPoint('Red Fish Room Bottom', 'WestMaridia', 'Maridia Green', {
        'Main Street Bottom': lambda sm: SMBool(True), # just go down
        'Red Fish Room Left': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                             sm.canJumpUnderwater()))
    }, internal=True),
    # TODO::maridia pink bottom is in east maridia now
    AccessPoint('Crab Shaft Left', 'WestMaridia', 'Maridia Pink Bottom', {
        'Main Street Bottom': lambda sm: SMBool(True), # fall down
        'Beach': lambda sm: sm.canDoOuterMaridia(),
        'Crab Shaft Right': lambda sm: SMBool(True)
    }, internal=True),
    # TODO::maridia pink bottom is in east maridia now
    AccessPoint('Watering Hole', 'WestMaridia', 'Maridia Pink Bottom', {
        'Beach': lambda sm: sm.haveItem('Morph'),
        'Watering Hole Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start = {'spawn': 0x0407, 'solveArea': "Maridia Pink Bottom", 'save':"Save_Watering_Hole",
                'patches':[RomPatches.MaridiaTubeOpened], 'rom_patches':['wh_open_tube.ips'],
                'areaLayout': ['area_layout_crab_hole', 'area_rando_gate_crab_tunnel'],
                'forcedEarlyMorph':True}),
    # TODO::maridia pink bottom is in east maridia now
    AccessPoint('Watering Hole Bottom', 'WestMaridia', 'Maridia Pink Bottom', {
        'Watering Hole': lambda sm: sm.canJumpUnderwater()
    }, internal=True),
    # TODO::maridia pink bottom is in east maridia now
    AccessPoint('Beach', 'WestMaridia', 'Maridia Pink Bottom', {
        'Crab Shaft Left': lambda sm: SMBool(True), # fall down
        'Watering Hole': Cache.ldeco(lambda sm: sm.wor(sm.wand(sm.wor(sm.canPassBombPassages(),
                                                                      sm.canUseSpringBall()),
                                                               sm.canDoOuterMaridia()),
                                                       sm.wand(sm.haveItem('Gravity'),
                                                               sm.haveItem('Morph'),
                                                               sm.knowsBomblessWateringHoleAccess())))
    }, internal=True),
    # TODO::maridia pink bottom is in east maridia now
    AccessPoint('Crab Shaft Right', 'WestMaridia', 'Maridia Pink Bottom', {
        'Crab Shaft Left': lambda sm: sm.canJumpUnderwater()
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.CrabShaftBlueDoor),
                                              sm.traverse('CrabShaftRight'))),
       roomInfo = {'RoomPtr':0xd1a3, "area": 0x4},
       exitInfo = {'DoorPtr':0xa4c8, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x1ca, 'SamusY':0x388},
       dotOrientation = 'e'),
    # escape APs
    AccessPoint('Crab Hole Bottom Right', 'WestMaridia', 'Maridia Green', {
        'Crab Hole Bottom Left': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa51c, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd7, 'SamusY':0x188},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Maridia Map Room', 'WestMaridia', 'Maridia Green', {
    }, roomInfo = {'RoomPtr':0xd3b6, "area": 0x4},
       exitInfo = {'DoorPtr':0xa5e8, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### East Maridia
    AccessPoint('Aqueduct Top Left', 'EastMaridia', 'Maridia Pink Bottom', {
        'Aqueduct Bottom': lambda sm: sm.wor(sm.wand(RomPatches.has(RomPatches.AqueductBombBlocks),
                                                     sm.canDestroyBombWallsUnderwater()),
                                             sm.canUsePowerBombs())
    }, roomInfo = {'RoomPtr':0xd5a7, "area": 0x4},
       exitInfo = {'DoorPtr':0xa708, 'direction': 0x5, "cap": (0x1e, 0x36), "bitFlag": 0x0,
                   "screen": (0x1, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe398},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       dotOrientation = 'w'),
    AccessPoint('Aqueduct Bottom', 'EastMaridia', 'Maridia Pink Bottom', {
        'Aqueduct Top Left': Cache.ldeco(lambda sm: sm.wor(sm.wand(sm.canDestroyBombWallsUnderwater(), # top left bomb blocks
                                                                   sm.canJumpUnderwater()),
                                                           # same requirements as aq items: spark from bottom or snail clip
                                                           sm.wand(RomPatches.has(RomPatches.AqueductBombBlocks),
                                                                   sm.canAccessAqueductItemsFromBottom()))),
        'Post Botwoon': Cache.ldeco(lambda sm: sm.wand(sm.canJumpUnderwater(),
                                                       sm.canPassBotwoonHallway(),
                                                       sm.haveItem('Botwoon'))),
        'Left Sandpit': lambda sm: sm.canAccessSandPits(),
        'Right Sandpit': lambda sm: sm.canAccessSandPits(),
        'Aqueduct': lambda sm: sm.canAccessAqueductItemsFromBottom()
    }, internal=True),
    AccessPoint('Aqueduct', 'EastMaridia', 'Maridia Pink Bottom', {
        'Aqueduct Bottom': lambda sm: SMBool(True) # go down
    }, internal=True,
       start = {'spawn': 0x0405, 'solveArea': "Maridia Pink Bottom",
                'save':"Save_Aqueduct", 'needsPreRando':True,
                'areaLayout': ['aqueduct_bomb_blocks'],
                'doors': [0x96]}),
    AccessPoint('Post Botwoon', 'EastMaridia', 'Maridia Pink Top', {
        'Aqueduct Bottom': Cache.ldeco(lambda sm: sm.wor(sm.wand(sm.canJumpUnderwater(), # can't access the sand pits from the right side of the room
                                                                 sm.haveItem('Morph')),
                                                         sm.wand(sm.haveItem('Gravity'),
                                                                 sm.haveItem('SpeedBooster')))),
        'Colosseum Top Right': lambda sm: sm.canBotwoonExitToColosseum(),
        'Toilet Top': Cache.ldeco(lambda sm: sm.wand(sm.canReachCacatacAlleyFromBotowoon(),
                                                     sm.canPassCacatacAlleyEastToWest()))
    }, internal=True),
    AccessPoint('West Sand Hall Left', 'EastMaridia', 'Maridia Sandpits', {
        # XXX there might be some tech to do this suitless, but HJ+ice is not enough
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.haveItem('Gravity')),
        'Aqueduct Bottom': Cache.ldeco(lambda sm: RomPatches.has(RomPatches.MaridiaSandWarp)),
        # this goes directly to WestMaridia
        'Main Street Bottom': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                             sm.wor(RomPatches.has(RomPatches.CrabTunnelGreenGateRemoved),
                                                                    sm.canGreenGateGlitch()))),
        # this goes directly to WestMaridia
        'Crab Hole Bottom Left': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                                                                sm.haveItem('Morph')))
    }, internal=True),
    AccessPoint('Left Sandpit', 'EastMaridia', 'Left Sandpit', {
        'West Sand Hall Left': lambda sm: sm.canAccessSandPits(),
        'Oasis Bottom': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Oasis Bottom', 'EastMaridia', 'Maridia Sandpits', {
        'Toilet Top': Cache.ldeco(lambda sm: sm.wand(sm.traverse('OasisTop'), sm.canDestroyBombWallsUnderwater())),
        'West Sand Hall Left': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Right Sandpit', 'EastMaridia', 'Right Sandpit', {
        'Oasis Bottom': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Le Coude Right', 'EastMaridia', 'Maridia Forgotten Highway', {
        'Toilet Top': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x95a8, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd1, 'SamusY':0x88},
       dotOrientation = 'ne'),
    AccessPoint('Toilet Top', 'EastMaridia', 'Maridia Forgotten Highway', {
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.wand(sm.traverse('PlasmaSparkBottom'), sm.canDestroyBombWallsUnderwater())),
        'Le Coude Right': lambda sm: SMBool(True),
        'Post Botwoon': lambda sm: sm.canPassCacatacAlleyWestToEast()
    }, internal=True),
    AccessPoint('Colosseum Top Right', 'EastMaridia', 'Maridia Pink Top', {
        'Post Botwoon': lambda sm: sm.canColosseumToBotwoonExit(),
        'Precious Room Top': Cache.ldeco(lambda sm: sm.traverse('ColosseumBottomRight')), # go down
    }, internal = True),
    AccessPoint('Precious Room Top', 'EastMaridia', 'Maridia Pink Top', {
        'Colosseum Top Right': lambda sm: sm.canClimbColosseum(),
        'DraygonRoomOut': lambda sm: SMBool(True) # go down
    }, internal = True),
    # boss APs
    AccessPoint('DraygonRoomOut', 'EastMaridia', 'Draygon Boss', {
        'Precious Room Top': lambda sm: sm.canExitPreciousRoom()
    }, boss = True,
       roomInfo = {'RoomPtr':0xd78f, "area": 0x4, "songs":[0xd7a5]},
       exitInfo = {'DoorPtr':0xa840, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288, 'song':0x1b},
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 'e'),
    AccessPoint('DraygonRoomIn', 'EastMaridia', 'Draygon Boss', {
        'Draygon Room Bottom': Cache.ldeco(lambda sm: sm.wor(Bosses.bossDead(sm, "Draygon"),
                                                             sm.wand(sm.canFightDraygon(),
                                                                     sm.enoughStuffsDraygon())))
    }, boss = True,
       roomInfo = {'RoomPtr':0xda60, "area": 0x4},
       exitInfo = {'DoorPtr':0xa96c, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe3d9,
                   "exitAsm": "door_transition_boss_exit_fix"},
       entryInfo = {'SamusX':0x1c8, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Draygon Room Bottom', 'EastMaridia', 'Draygon Boss', {
       'DraygonRoomIn': Cache.ldeco(lambda sm: sm.wand(Bosses.bossDead(sm, 'Draygon'), sm.canExitDraygon()))
    }, internal = True),
    ### Red Brinstar. Main nodes: Red Tower Top Left, East Tunnel Right
    AccessPoint('Red Tower Top Left', 'RedBrinstar', 'Red Brinstar Middle', {
        # go up
        'Red Brinstar Elevator': lambda sm: sm.canClimbRedTower(),
        'Caterpillar Room Top Right': Cache.ldeco(lambda sm: sm.wand(sm.canPassRedTowerToMaridiaNode(),
                                                                     sm.canClimbRedTower())),
        # go down
        'East Tunnel Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa253, "area": 0x1},
       exitInfo = {'DoorPtr':0x902a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2f, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', 'Red Brinstar Top', {
        'Red Brinstar Elevator': lambda sm: sm.canPassMaridiaToRedTowerNode()
    }, roomInfo = {'RoomPtr':0xa322, "area": 0x1},
       exitInfo = {'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf},
       entryInfo = {'SamusX':0x2cd, 'SamusY':0x388},
       dotOrientation = 'ne'),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', 'Red Brinstar Top', {
        'Caterpillar Room Top Right': lambda sm: sm.canPassRedTowerToMaridiaNode(),
        'Red Tower Top Left': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.HellwayBlueDoor), sm.traverse('RedTowerElevatorLeft')))
    }, traverse=Cache.ldeco(lambda sm:sm.wor(RomPatches.has(RomPatches.RedTowerBlueDoors), sm.traverse('RedBrinstarElevatorTop'))),
       roomInfo = {'RoomPtr':0x962a, "area": 0x0},
       exitInfo = {'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1},
       entryInfo = {'SamusX':0x80, 'SamusY':0x58},
       start={
           'spawn':0x010a, 'doors':[0x3c, 0x3d],
           'patches':[RomPatches.HellwayBlueDoor, RomPatches.AlphaPowerBombBlueDoor],
           'areaLayout': ['area_rando_gate_caterpillar', 'area_rando_gate_east_tunnel'],
           'layout': ['red_tower'],
           'solveArea': "Red Brinstar Top", 'areaMode':True
       },
       dotOrientation = 'n'),
    AccessPoint('East Tunnel Right', 'RedBrinstar', 'Red Brinstar Bottom', {
        'East Tunnel Top Right': lambda sm: SMBool(True), # handled by room traverse function
        'Glass Tunnel Top': Cache.ldeco(lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                           sm.wor(sm.haveItem('Gravity'),
                                                                  sm.haveItem('HiJump'),
                                                                  sm.knowsTubeGravityJump()))),
        'Red Tower Top Left': lambda sm: sm.canClimbBottomRedTower()
    }, roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa384, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xce, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', 'Red Brinstar Bottom', {
        'East Tunnel Right': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.EastTunnelGreenGateRemoved),
                                                           sm.haveItem('Super')))
    }, traverse=Cache.ldeco(lambda sm: RomPatches.has(RomPatches.EastTunnelGreenGateRemoved)),
       roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0x3c6, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', 'Red Brinstar Bottom', {
        'East Tunnel Right': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
                                                           sm.canUsePowerBombs(),
                                                           sm.wand(sm.haveItem('Morph'),
                                                                   sm.knowsTubeClip())))
    }, traverse=Cache.ldeco(lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
                                                      sm.haveItem('HiJump')),
                                               sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
                                                      sm.canUsePowerBombs()))),
       roomInfo = {'RoomPtr':0xcefb, "area": 0x4},
       exitInfo = {'DoorPtr':0xa330, 'direction': 0x7, "cap": (0x16, 0x7d), "bitFlag": 0x0,
                   "screen": (0x1, 0x7), "distanceToSpawn": 0x200, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x81, 'SamusY':0x78},
       dotOrientation = 's'),
    ### Tourian
    AccessPoint('Golden Four', 'Tourian', 'Tourian', {},
       roomInfo = {'RoomPtr':0xa5ed, "area": 0x0},
       exitInfo = {'DoorPtr':0x91e6, 'direction': 0x5, "cap": (0xe, 0x66), "bitFlag": 0x0,
                   "screen": (0x0, 0x6), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       start={
           'spawn':0x0007,
           'solveArea': "Tourian", "save": "Save_G4", 'areaMode':True,
           'layout': ['red_tower'],
           'areaLayout': ['area_rando_gate_caterpillar', 'area_rando_gate_east_tunnel']
       },
       dotOrientation = 'w'),
    AccessPoint('Tourian Escape Room 4 Top Right', 'Tourian', 'Tourian', {},
       roomInfo = {'RoomPtr':0xdede, "area": 0x5},
       exitInfo = {'DoorPtr':0xab34, 'direction': 0x4, "cap": (0x1, 0x86), "bitFlag": 0x40,
                   "screen": (0x0, 0x8), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe4cf},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne')
]

accessPointsDict = {ap.Name:ap for ap in accessPoints}
