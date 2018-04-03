from parameters import Knows, Settings, easy, medium, hard, harder, hardcore, mania
# the canXXX functions
from graph_helpers import canEnterAndLeaveGauntlet, wand, wor, haveItem, canOpenRedDoors
from graph_helpers import canPassBombPassages, canDestroyBombWalls, canUsePowerBombs, SMBool
from graph_helpers import canFly, energyReserveCountOk, canAccessKraidsLair
from graph_helpers import Bosses, enoughStuffsKraid, heatProof, energyReserveCountOk
from graph_helpers import energyReserveCountOkHellRun, canAccessCrocFromNorfairEntrance
from graph_helpers import canPassWorstRoom, enoughStuffsRidley, canPassLavaPit, canPassForgottenHighway
from graph_helpers import enoughStuffsPhantoon, enoughStuffsDraygon, canPassAmphitheaterReverse
from graph_helpers import canDoSuitlessOuterMaridia, canDefeatBotwoon, canPassMtEverest, canClimbRedTower
from graph_helpers import canFlyDiagonally, canAccessCrocFromMainUpperNorfair, enoughStuffCroc, canAccessHeatedNorfairFromEntrance
from graph_helpers import canCrystalFlash, canOpenGreenDoors, canOpenYellowDoors, canHellRun, canEnterNorfairReserveArea

from rom import RomPatches

# all the items locations with the prerequisites to access them
###### MAJORS
locations = [
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'Name': "Energy Tank, Gauntlet",
    'Class': "Major",
    'Address': 0x78264,
    'Visibility': "Visible",
    'Room': 'Gauntlet Energy Tank Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    # EXPLAINED: difficulty already handled in the canEnterAndLeaveGauntlet function
    'Available': lambda items: canEnterAndLeaveGauntlet(items)
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'Name': "Bomb",
    'Address': 0x78404,
    'Class': "Major",
    'Visibility': "Chozo",
    'Room': 'Bomb Torizo Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    # EXPLAINED: need to morph to enter Alcatraz. red door at Flyway.
    #            we may not have bombs or power bomb to get out of Alcatraz.    
    'Available': lambda items: wand(haveItem(items, 'Morph'),
                                    canOpenRedDoors(items)),
    'PostAvailable': lambda items: wor(Knows.AlcatrazEscape,
                                       canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'Name': "Energy Tank, Terminator",
    'Class': "Major",
    'Address': 0x78432,
    'Visibility': "Visible",
    'Room': 'Terminator Room',
    'AccessPoints' : {
        'Lower Mushrooms Left': lambda items: SMBool(True, 0)
    },
    'Available': lambda items: SMBool(True, 0)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'Name': "Reserve Tank, Brinstar",
    'Class': "Major",
    'Address': 0x7852C,
    'Visibility': "Chozo",
    'Room': 'Brinstar Reserve Tank Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: SMBool(True, 0)
    },
    # EXPLAINED: break the bomb wall at left of Parlor and Alcatraz,
    #            open red door at Green Brinstar Main Shaft,
    #            mock ball for early retreval or speed booster
    'Available': lambda items: wand(canOpenRedDoors(items),
                                    wor(wand(Knows.Mockball,
                                        haveItem(items, 'Morph')),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'Name': "Charge Beam",
    'Class': "Major",
    'Address': 0x78614,
    'Visibility': "Chozo",
    'Room': 'Big Pink',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: wand(canOpenRedDoors(items),
                                                            canDestroyBombWalls(items)),
        'Green Hill Zone Top Right': lambda items: haveItem(items, 'Morph')
    },
    # EXPLAINED: open red door at Green Brinstar Main Shaft (down right),
    #            break the bomb wall at left of Parlor and Alcatraz
    'Available': lambda items: canPassBombPassages(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'Name': "Morphing Ball",
    'Class': "Major",
    'Address': 0x786DE,
    'Visibility': "Visible",
    'Room': 'Morph Ball Room',
    'AccessPoints' : {
        'Landing Site': lambda items: SMBool(True, 0)
    },
    # EXPLAINED: no difficulty
    'Available': lambda items: SMBool(True, 0)
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'Name': "Energy Tank, Brinstar Ceiling",
    'Class': "Major",
    'Address': 0x7879E,
    'Visibility': "Hidden",
    'Room': 'Blue Brinstar Energy Tank Room',
    'AccessPoints' : {
        'Landing Site': lambda items: wor(canOpenRedDoors(items), RomPatches.has(RomPatches.BlueBrinstarBlueDoor))
    },
    # EXPLAINED: to get this major item the different technics are:
    #  -can fly (continuous bomb jump or space jump)
    #  -have the high jump boots
    #  -freeze the Reo to jump on it
    #  -do a damage boost with one of the two Geemers
    'Available': lambda items: wor(Knows.CeilingDBoost,
                                   canFly(items),
                                   haveItem(items, 'HiJump'),
                                   haveItem(items, 'Ice'))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'Name': "Energy Tank, Etecoons",
    'Class': "Major",
    'Address': 0x787C2,
    'Visibility': "Visible",
    'Room': 'Etecoon Energy Tank Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: SMBool(True, 0)
    },
    # EXPLAINED: break the bomb wall at left of Parlor and Alcatraz,
    #            power bomb down of Green Brinstar Main Shaft
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'Name': "Energy Tank, Waterway",
    'Class': "Major",
    'Address': 0x787FA,
    'Visibility': "Visible",
    'Room': 'Waterway Energy Tank Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: wand(canOpenRedDoors(items),
                                                            canDestroyBombWalls(items)),
        'Green Hill Zone Top Right': lambda items: haveItem(items, 'Morph')
    },
    # EXPLAINED: break the bomb wall at left of Parlor and Alcatraz with power bombs,
    #            open red door at Green Brinstar Main Shaft (down right),
    #            power bomb at bottom of Big Pink (Charge Beam),
    #            open red door leading to waterway,
    #            at waterway, either do:
    #  -with gravity do a speed charge
    #  -a simple short charge from the blocks above the water
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    canOpenRedDoors(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(haveItem(items, 'Gravity'),
                                        Knows.SimpleShortCharge))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'Name': "Energy Tank, Brinstar Gate",
    'Class': "Major",
    'Address': 0x78824,
    'Visibility': "Visible",
    'Room': 'Hopper Energy Tank Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: wand(canOpenRedDoors(items),
                                                            canDestroyBombWalls(items)),
        'Green Hill Zone Top Right': lambda items: haveItem(items, 'Morph')
    },
    # DONE: use Knows.ReverseGateGlitch
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    wor(haveItem(items, 'Wave'),
                                        wand(haveItem(items, 'Super'),
                                             haveItem(items, 'HiJump'),
                                             Knows.ReverseGateGlitch),
                                        wand(haveItem(items, 'Super'),
                                             Knows.ReverseGateGlitchHiJumpLess)))
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'Name': "X-Ray Scope",
    'Class': "Major",
    'Address': 0x78876,
    'Visibility': "Chozo",
    'Room': 'X-Ray Scope Room',
    'AccessPoints' : {
        'Red Tower Top Left': lambda items: SMBool(True, 0)
    },
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    wor(wor(haveItem(items, 'Grapple'),
                                            haveItem(items, 'SpaceJump'),
                                            wand(Knows.XrayDboost,
                                                 wor(wand(heatProof(items),
                                                          energyReserveCountOk(items, 3)),
                                                     energyReserveCountOk(items, 6))),
                                            wand(haveItem(items, 'Ice'),
                                                 wor(energyReserveCountOk(items, 6),
                                                     wand(heatProof(items),
                                                          energyReserveCountOk(items, 3))))),
                                        wand(haveItem(items, 'Bomb'),
                                             Knows.InfiniteBombJump,
                                             wor(energyReserveCountOk(items, 6),
                                                 wand(heatProof(items),
                                                      energyReserveCountOk(items, 3))))))
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'Name': "Spazer",
    'Class': "Major",
    'Address': 0x7896E,
    'Visibility': "Chozo",
    'Room': 'Spazer Room',
    'AccessPoints' : {
        'Red Tower Top Left': lambda items: SMBool(True, 0),
        'East Tunnel Right': lambda items: SMBool(True, 0)
    },
    # DONE: no difficulty
    'Available': lambda items: wand(canOpenGreenDoors(items),
                                    wor(canPassBombPassages(items), RomPatches.has(RomPatches.SpazerShotBlock)))
},
{
    'Area': "Brinstar",
    'GraphArea': "Norfair",
    'Name': "Energy Tank, Kraid",
    'Class': "Major",
    'Address': 0x7899C,
    'Visibility': "Hidden",
    'Room': 'Warehouse Energy Tank Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: SMBool(True, 0)
    },
    # DONE: no difficulty
    'Available': lambda items: wand(canAccessKraidsLair(items), Bosses.bossDead('Kraid'))
},
{
    'Area': "Brinstar",
    'GraphArea': "Norfair",
    'Name': "Varia Suit",
    'Class': "Major",
    'Address': 0x78ACA,
    'Visibility': "Chozo",
    'Room': 'Varia Suit Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: SMBool(True, 0)
    },
    # DONE: no difficulty
    'Available': lambda items: wand(canAccessKraidsLair(items),
                                    enoughStuffsKraid(items)),
    'Pickup': lambda: Bosses.beatBoss('Kraid')
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Ice Beam",
    'Class': "Major",
    'Address': 0x78B24,
    'Visibility': "Chozo",
    'Room': 'Ice Beam Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: SMBool(True, 0)
    },
    # DONE: harder without varia
    'Available': lambda items: wand(canOpenGreenDoors(items),
                                    canHellRun(items, 'Ice'),
                                    wor(wand(haveItem(items, 'Morph'),
                                             Knows.Mockball),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Energy Tank, Crocomire",
    'Class': "Major",
    'Address': 0x78BA4,
    'Visibility': "Visible",
    'Room': "Crocomire's Room",
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessCrocFromNorfairEntrance(items),
        'Single Chamber Top Right': lambda items: canAccessCrocFromMainUpperNorfair(items),
        'Kronic Boost Room Bottom Right': lambda items: canAccessCrocFromMainUpperNorfair(items)
    },
    'Available': lambda items: enoughStuffCroc(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Hi-Jump Boots",
    'Class': "Major",
    'Address': 0x78BAC,
    'Visibility': "Chozo",
    'Room': 'Hi Jump Boots Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: SMBool(True, 0)
    },
    # DONE: no difficulty
    'Available': lambda items: canOpenRedDoors(items),
    'PostAvailable': lambda items: wor(canPassBombPassages(items),
                                       RomPatches.has(RomPatches.HiJumpShotBlock))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Grapple Beam",
    'Class': "Major",
    'Address': 0x78C36,
    'Visibility': "Chozo",
    'Room': 'Grapple Beam Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessCrocFromNorfairEntrance(items),
        'Single Chamber Top Right': lambda items: canAccessCrocFromMainUpperNorfair(items),
        'Kronic Boost Room Bottom Right': lambda items: canAccessCrocFromMainUpperNorfair(items)
    },
    'Available': lambda items: wand(enoughStuffCroc(items),
                                    wor(canFly(items),
                                        haveItem(items, 'SpeedBooster'),
                                        Knows.GreenGateGlitch))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Reserve Tank, Norfair",
    'Class': "Major",
    'Address': 0x78C3E,
    'Visibility': "Chozo",
    'Room': 'Norfair Reserve Tank Room',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: canEnterNorfairReserveArea(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Speed Booster",
    'Class': "Major",
    'Address': 0x78C82,
    'Visibility': "Chozo",
    'Room': 'Speed Booster Room',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: canOpenGreenDoors(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Wave Beam",
    'Class': "Major",
    'Address': 0x78CCA,
    'Visibility': "Chozo",
    'Room': 'Wave Beam Room',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: canOpenRedDoors(items)
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Energy Tank, Ridley",
    'Class': "Major",
    'Address': 0x79108,
    'Visibility': "Hidden",
    'Room': 'Ridley Tank Room',
    'AccessPoints' : {
        'Lava Dive Right': lambda items: wand(canPassLavaPit(items),
                                              canPassWorstRoom(items),
                                              canOpenYellowDoors(item),
                                              canOpenGreenDoors(items)),
        'Three Muskateers Room Left': lambda items: wand(canOpenYellowDoors(item),
                                                         canOpenGreenDoors(items))
    },
    # DONE: already set in function
    'Available': lambda items: wand(canHellRun(items, 'LowerNorfair'), enoughStuffsRidley(items)),
    'Pickup': lambda: Bosses.beatBoss('Ridley')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Screw Attack",
    'Class': "Major",
    'Address': 0x79110,
    'Visibility': "Chozo",
    'Room': 'Screw Attack Room',
    'AccessPoints' : {
        'Lava Dive Right': lambda items: canPassLavaPit(items),
        'Three Muskateers Room Left': lambda items: canPassAmphitheaterReverse(items)
    },
    'Available': lambda items: wand(canHellRun(items, 'LowerNorfair'),
                                    wor(haveItem(items, 'SpaceJump'),
                                        Knows.GreenGateGlitch)),
    'PostAvailable': lambda items: wor(canFly(items),
                                       wand(haveItem(items, 'HiJump'),
                                            haveItem(items, 'ScrewAttack'),
                                            haveItem(items, 'SpeedBooster'),
                                            Knows.ScrewAttackExit),
                                       wand(haveItem(items, 'SpringBall'), Knows.SpringBallJumpFromWall))
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Energy Tank, Firefleas",
    'Class': "Major",
    'Address': 0x79184,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Fireflea Room',
    'AccessPoints' : {
        'Lava Dive Right': lambda items: wand(canHellRun(items, 'LowerNorfair'), canPassLavaPit(items), canPassWorstRoom(items)),
        'Three Muskateers Room Left': lambda items: canHellRun(items, 'LowerNorfair')
    },
    'Available': lambda items: SMBool(True, 0)
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Reserve Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C2E9,
    'Visibility': "Chozo",
    'Room': 'Bowling Alley',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(heatProof(items),
                                        energyReserveCountOk(items, 1)),
                                    Bosses.bossDead('Phantoon'))
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Energy Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C337,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship Energy Tank Room',
    'AccessPoints' : {
        'West Ocean Left': lambda items: wand(canOpenGreenDoors(items), canPassSpongeBath(items)),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: Bosses.bossDead('Phantoon')
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Right Super, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C365,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship East Super Room',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: wand(canOpenGreenDoors(items), enoughStuffsPhantoon(items), canPassBombPassages(items)),
    'Pickup': lambda: Bosses.beatBoss('Phantoon')
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Gravity Suit",
    'Class': "Major",
    'Address': 0x7C36D,
    'Visibility': "Chozo",
    'Room': 'Gravity Suit Room',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: wand(canPassBombPassages(items),
                                    Bosses.bossDead('Phantoon'),
                                    wor(heatProof(items),
                                        energyReserveCountOk(items, 1)))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Energy Tank, Mama turtle",
    'Class': "Major",
    'Address': 0x7C47D,
    'Visibility': "Visible",
    'Room': 'Mama Turtle Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wor(haveItem(items, 'Gravity'), canDoSuitlessOuterMaridia(items))
    },
    # DONE: difficulty already handled in canDoSuitlessOuterMaridia
    # to acces the ETank in higher part of the room:
    #  -use grapple to attach to the block
    #  -use speedbooster ??
    #  -can fly (space jump or infinite bomb jump)
    'Available': lambda items: wand(canOpenRedDoors(items),
                                    wor(canFly(items),
                                        wand(haveItem(items, 'Gravity'), haveItem(items, 'SpeedBooster')),
                                        wand(haveItem(items, 'HiJump'), haveItem(items, 'SpringBall'), Knows.SpringBallJump),
                                        haveItem(items, 'Grapple')))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Plasma Beam",
    'Class': "Major",
    'Address': 0x7C559,
    'Visibility': "Chozo",
    'Room': 'Plasma Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: canOpenGreenDoors(items), # green gate+toilet
        'Le Coude Right': lambda items: SMBool(True, 0)
    },
    # DONE: to leave the Plasma Beam room you have to kill the space pirates and return to the door
    # to unlock the door:
    #  -can access draygon room to kill him
    # to kill the space pirates:
    #  -do short charges with speedbooster
    #  -do beam charges with spin jump attacks
    #  -have screw attack
    #  -have plasma beam
    # to go back to the door:
    #  -have high jump boots
    #  -can fly (space jump or infinite bomb jump)
    #  -use short charge with speedbooster
    'Available': lambda items: Bosses.bossDead('Draygon'),
    'PostAvailable': lambda items: wand(wor(wand(haveItem(items, 'SpeedBooster'),
                                                 Knows.ShortCharge,
                                                 Knows.KillPlasmaPiratesWithSpark),
                                            wand(haveItem(items, 'Charge'),
                                                 Knows.KillPlasmaPiratesWithCharge),
                                            haveItem(items, 'ScrewAttack', difficulty=easy),
                                            haveItem(items, 'Plasma', difficulty=easy)),
                                        wor(canFly(items),
                                            wand(haveItem(items, 'HiJump'),
                                                 Knows.GetAroundWallJump),
                                            wand(haveItem(items, 'SpeedBooster'),
                                                 Knows.ShortCharge)))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Reserve Tank, Maridia",
    'Class': "Major",
    'Address': 0x7C5E3,
    'Visibility': "Chozo",
    'Room': 'West Sand Hole',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items),
                                                 canOpenGreenDoors(items),
                                                 canUsePowerBombs(items))
    },
    # DONE: this item can be taken without gravity, but it's super hard because of the quick sands...
    'Available': lambda items: wor(haveItem(items, 'Gravity'),
                                   Knows.SuitlessSandpit) # suitless maridia conditions are in canPassMtEverest
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Spring Ball",
    'Class': "Major",
    'Address': 0x7C6E5,
    'Visibility': "Chozo",
    'Room': 'Spring Ball Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: canOpenGreenDoors(items), # gate
        'Le Coude Right': lambda items: wand(canOpenYellowDoors(items),
                                             canOpenGreenDoors(items)), # toilet
    },
    # DONE: handle puyo clip and diagonal bomb jump
    # to access the spring ball you can either:
    #  -use the puyo clip with ice
    #  -use the grapple to destroy the block and then:
    #    -use high boots jump
    #    -fly (with space jump or diagonal bomb jump
    'Available': lambda items: wand(haveItem(items, 'Gravity'),
                                    wor(wand(haveItem(items, 'Ice'),
                                             Knows.PuyoClip),
                                        wand(haveItem(items, 'Grapple'),
                                             wor(canFlyDiagonally(items),
                                                 haveItem(items, 'HiJump')))))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Energy Tank, Botwoon",
    'Class': "Major",
    'Address': 0x7C755,
    'Visibility': "Visible",
    'Room': 'Botwoon Energy Tank Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: canPassMtEverest(items)
    },
    # DONE: difficulty already handled in the functions
    'Available': lambda items: canDefeatBotwoon(items)
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Space Jump",
    'Class': "Major",
    'Address': 0x7C7A7,
    'Visibility': "Chozo",
    'Room': 'Space Jump Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items), canDefeatBotwoon(items), canOpenGreenDoors(items))
    },
    # DONE: difficulty already handled in the function,
    # we need to have access to the boss and enough stuff to kill him.
    # to get out of draygon room:
    #   with gravity but without highjump/bomb/space jump: gravity jump
    #   dessyreqt randomizer in machosist can have suitless draygon:
    #     to exit draygon room: grapple or crystal flash (for free shine spark)
    #     to exit precious room: spring ball jump, xray scope glitch or stored spark
    'Available': lambda items: enoughStuffsDraygon(items),
    'Pickup': lambda: Bosses.beatBoss('Draygon'),
    'PostAvailable': lambda items: wor(wand(haveItem(items, 'Gravity'),
                                            wor(canFly(items),
                                                Knows.GravityJump,
                                                wand(haveItem(items, 'HiJump'),
                                                     haveItem(items, 'SpeedBooster')))),
                                       wand(wand(canCrystalFlash(items),
                                                 Knows.DraygonRoomCrystalFlash),
                                            # use the spark either to exit draygon room or precious room
                                            wor(wand(haveItem(items, 'Grapple'),
                                                     Knows.DraygonRoomGrappleExit),
                                                wand(haveItem(items, 'XRayScope'),
                                                     Knows.PreciousRoomXRayExit),
                                                wand(haveItem(items, 'SpringBall'),
                                                     Knows.SpringBallJump))),
                                       # spark-less exit (no CF)
                                       wand(wand(haveItem(items, 'Grapple'),
                                                 Knows.DraygonRoomGrappleExit),
                                            wor(wand(haveItem(items, 'XRayScope'),
                                                     Knows.PreciousRoomXRayExit),
                                                wand(haveItem(items, 'SpringBall'),
                                                     Knows.SpringBallJump))))
},
###### MINORS
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'Name': "Power Bomb (Crateria surface)",
    'Class': "Minor",
    'Address': 0x781CC,
    'Visibility': "Visible",
    'Room': 'Crateria Power Bomb Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    wor(haveItem(items, 'SpeedBooster'),
                                        canFly(items)))
},
{
    'Area': "Crateria",
    'GraphArea': "WreckedShip",
    'Name': "Missile (outside Wrecked Ship bottom)",
    'Class': "Minor",
    'Address': 0x781E8,
    'Visibility': "Visible",
    'Room': 'West Ocean',
    'AccessPoints' : {
        'West Ocean Left': lambda items: (True, 0),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: canPassBombPassages(items)
},
{
    'Area': "Crateria",
    'GraphArea': "WreckedShip",
    'Name': "Missile (outside Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x781EE,
    'Visibility': "Hidden",
    'Room': 'West Ocean',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: Bosses.bossDead('Phantoon')
},
{
    'Area': "Crateria",
    'GraphArea': "WreckedShip",
    'Name': "Missile (outside Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x781F4,
    'Visibility': "Visible",
    'Room': 'West Ocean',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: wand(canOpenGreenDoors(items), haveItem(items, 'Morph'), Bosses.bossDead('Phantoon'))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'Name': "Missile (Crateria moat)",
    'Class': "Minor",
    'Address': 0x78248,
    'Visibility': "Visible",
    'Room': 'The Moat',
    'AccessPoints' : {
        'Keyhunter Room Bottom': lambda items: canOpenYellowDoors(items)
    },
    # it's before actual wrecked ship access
    'Available': lambda items: (True, 0)
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'Name': "Missile (Crateria bottom)",
    'Class': "Minor",
    'Address': 0x783EE,
    'Visibility': "Visible",
    'Room': 'Pit Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: canDestroyBombWalls(items)
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",    
    'Name': "Missile (Crateria gauntlet right)",
    'Class': "Minor",
    'Address': 0x78464,
    'Visibility': "Visible",
    'Room': 'Green Pirates Shaft',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items),
                                    canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",    
    'Name': "Missile (Crateria gauntlet left)",
    'Class': "Minor",
    'Address': 0x7846A,
    'Visibility': "Visible",
    'Room': 'Green Pirates Shaft',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items),
                                    canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",    
    'Name': "Super Missile (Crateria)",
    'Class': "Minor",
    'Address': 0x78478,
    'Visibility': "Visible",
    'Room': 'Crateria Super Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(haveItem(items, 'Ice'),
                                        Knows.ShortCharge))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",    
    'Name': "Missile (Crateria middle)",
    'Class': "Minor",
    'Address': 0x78486,
    'Visibility': "Visible",
    'Room': 'The Final Missile',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: canPassBombPassages(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'Name': "Power Bomb (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x784AC,
    'Visibility': "Chozo",
    'Room': 'Green Brinstar Main Shaft',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: (True, 0)
    },
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Super Missile (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x784E4,
    'Visibility': "Chozo",
    'Room': 'Spore Spawn Super Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: wand(canOpenRedDoors(items),
                                                            canDestroyBombWalls(items)),
        'Green Hill Zone Top Right': lambda items: haveItem(items, 'Morph')
    },
    # either you go the back way, using a super and the camera glitch,
    # or just beat spore spawn (so no Knows* setting needed for the glitch)
    'Available': lambda items: wor(wand(canPassBombPassages(items),
                                        haveItem(items, 'Super')),
                                   SMBool(True, easy)),
    'PostAvailable': lambda items: wand(canOpenGreenDoors(items),
                                        canPassBombPassages(items))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Missile (green Brinstar below super missile)",
    'Class': "Minor",
    'Address': 0x78518,
    'Visibility': "Visible",
    'Room': 'Early Supers Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: (True, 0)
    },
    'Available': lambda items: canOpenRedDoors(items),
    'PostAvailable': lambda items: wor(canPassBombPassages(items),
                                       RomPatches.has(RomPatches.EarlySupersShotBlock))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Super Missile (green Brinstar top)",
    'Class': "Minor",
    'Address': 0x7851E,
    'Visibility': "Visible",
    'Room': 'Early Supers Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canOpenRedDoors(items),
                                    wor(wand(haveItem(items, 'Morph'), Knows.Mockball),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Missile (green Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x78532,
    'Visibility': "Hidden",
    'Room': 'Brinstar Reserve Tank Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canPassBombPassages(items),
                                    canOpenRedDoors(items),
                                    wor(wand(haveItem(items, 'Morph'), Knows.Mockball),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Missile (green Brinstar behind reserve tank)",
    'Class': "Minor",
    'Address': 0x78538,
    'Visibility': "Visible",
    'Room': 'Brinstar Reserve Tank Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canOpenRedDoors(items),
                                    haveItem(items, 'Morph'),
                                    wor(Knows.Mockball,
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Missile (pink Brinstar top)",
    'Class': "Minor",
    'Address': 0x78608,
    'Visibility': "Visible",
    'Room': 'Big Pink',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: wand(canOpenRedDoors(items),
                                                            canDestroyBombWalls(items)),
        'Green Hill Zone Top Right': lambda items: haveItem(items, 'Morph')
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Missile (pink Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x7860E,
    'Visibility': "Visible",
    'Room': 'Big Pink',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: wand(canOpenRedDoors(items),
                                                            canDestroyBombWalls(items)),
        'Green Hill Zone Top Right': lambda items: haveItem(items, 'Morph')
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Power Bomb (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x7865C,
    'Visibility': "Visible",
    'Room': 'Pink Brinstar Power Bomb Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: wand(canOpenRedDoors(items),
                                                            canDestroyBombWalls(items)),
        'Green Hill Zone Top Right': lambda items: haveItem(items, 'Morph')
    },
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    haveItem(items, 'Super'))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",    
    'Name': "Missile (green Brinstar pipe)",
    'Class': "Minor",
    'Address': 0x78676,
    'Visibility': "Visible",
    'Room': 'Green Hill Zone',
    'AccessPoints' : {
        'Green Hill Zone Top Right': lambda items: (True, 0)
    },
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'Name': "Power Bomb (blue Brinstar)",
    'Class': "Minor",
    'Address': 0x7874C,
    'Visibility': "Visible",
    'Room': 'Morph Ball Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",    
    'Name': "Missile (blue Brinstar middle)",
    'Address': 0x78798,
    'Class': "Minor",
    'Visibility': "Visible",
    'Room': 'Blue Brinstar Energy Tank Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: wand(wor(haveItem(items, 'Morph'), RomPatches.has(RomPatches.BlueBrinstarMissile)),
                                    wor(canOpenRedDoors(items),
                                        RomPatches.has(RomPatches.BlueBrinstarBlueDoor)))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'Name': "Super Missile (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x787D0,
    'Visibility': "Visible",
    'Room': 'Etecoon Super Room',
    'AccessPoints' : {
        'Green Brinstar Elevator Right': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    canOpenGreenDoors(items))
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'Name': "Missile (blue Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x78802,
    'Visibility': "Chozo",
    'Room': 'First Missile Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",    
    'Name': "Missile (blue Brinstar top)",
    'Class': "Minor",
    'Address': 0x78836,
    'Visibility': "Visible",
    'Room': 'Billy Mays Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'Name': "Missile (blue Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x7883C,
    'Visibility': "Hidden",
    'Room': 'Billy Mays Room',
    'AccessPoints' : {
        'Landing Site': lambda items: (True, 0)
    },
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'Name': "Power Bomb (red Brinstar sidehopper room)",
    'Class': "Minor",
    'Address': 0x788CA,
    'Visibility': "Visible",
    'Room': 'Beta Power Bomb Room',
    'AccessPoints' : {
        'Red Brinstar Elevator': lambda items: (True, 0),
        'Caterpillar Room Top Right': lambda items: (True, 0),
        'Red Tower Top Left': lambda items: canClimbRedTower(items)
    },
    'Available': lambda items: wand(canOpenGreenDoors(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'Name': "Power Bomb (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x7890E,
    'Visibility': "Chozo",
    'Room': 'Alpha Power Bomb Room',
    'AccessPoints' : {
        'Red Brinstar Elevator': lambda items: (True, 0),
        'Caterpillar Room Top Right': lambda items: (True, 0),
        'Red Tower Top Left': lambda items: canClimbRedTower(items)
    },
    'Available': lambda items: canOpenGreenDoors(items)
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'Name': "Missile (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x78914,
    'Visibility': "Visible",
    'Room': 'Alpha Power Bomb Room',
    'AccessPoints' : {
        'Red Brinstar Elevator': lambda items: (True, 0),
        'Caterpillar Room Top Right': lambda items: (True, 0),
        'Red Tower Top Left': lambda items: canClimbRedTower(items)
    },
    'Available': lambda items: wand(canOpenGreenDoors(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'GraphArea': "Norfair",
    'Name': "Missile (Kraid)",
    'Class': "Minor",
    'Address': 0x789EC,
    'Visibility': "Hidden",
    'Room': 'Warehouse Keyhunter Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessKraidsLair(items)
    },
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",    
    'Name': "Missile (lava room)",
    'Class': "Minor",
    'Address': 0x78AE4,
    'Visibility': "Hidden",
    'Room': 'Cathedral',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (below Ice Beam)",
    'Class': "Minor",
    'Address': 0x78B46,
    'Visibility': "Hidden",
    'Room': 'Crumble Shaft',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: (True, 0)
    },
    'Available': lambda items: wand(canOpenGreenDoors(items),
                                    canUsePowerBombs(items),
                                    canHellRun(items, 'Ice'))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (above Crocomire)",
    'Class': "Minor",
    'Address': 0x78BC0,
    'Visibility': "Visible",
    'Room': 'Crocomire Escape',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessCrocFromNorfairEntrance(items),
        'Single Chamber Top Right': lambda items: canAccessCrocFromMainUpperNorfair(items),
        'Kronic Boost Room Bottom Right': lambda items: canAccessCrocFromMainUpperNorfair(items)
    },
    'Available': lambda items: wor(canFly(items), haveItem(items, 'Grapple'),
                                   wand(haveItem(items, 'HiJump'),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (Hi-Jump Boots)",
    'Class': "Minor",
    'Address': 0x78BE6,
    'Visibility': "Visible",
    'Room': 'Hi Jump Energy Tank Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: (True, 0)
    },
    'Available': lambda items: (True, 0),
    'PostAvailable': lambda items: wor(canPassBombPassages(items),
                                       RomPatches.has(RomPatches.HiJumpShotBlock))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Energy Tank (Hi-Jump Boots)",
    'Class': "Minor",
    'Address': 0x78BEC,
    'Visibility': "Visible",
    'Room': 'Hi Jump Energy Tank Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: (True, 0)
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Power Bomb (Crocomire)",
    'Class': "Minor",
    'Address': 0x78C04,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Power Bomb Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessCrocFromNorfairEntrance(items),
        'Single Chamber Top Right': lambda items: canAccessCrocFromMainUpperNorfair(items),
        'Kronic Boost Room Bottom Right': lambda items: canAccessCrocFromMainUpperNorfair(items)
    },
    'Available': lambda items: wand(enoughStuffCroc(items),
                                    wor(canFly(items),
                                        haveItem(items, 'Grapple'),
                                        wand(haveItem(items, 'HiJump'),
                                             haveItem(items, 'SpeedBooster'))))

},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (below Crocomire)",
    'Class': "Minor",
    'Address': 0x78C14,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Missile Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessCrocFromNorfairEntrance(items),
        'Single Chamber Top Right': lambda items: canAccessCrocFromMainUpperNorfair(items),
        'Kronic Boost Room Bottom Right': lambda items: canAccessCrocFromMainUpperNorfair(items)
    },
    'Available': lambda items: enoughStuffCroc(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (Grapple Beam)",
    'Class': "Minor",
    'Address': 0x78C2A,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Jump Room',
    'AccessPoints' : {
        'Warehouse Entrance Left': lambda items: canAccessCrocFromNorfairEntrance(items),
        'Single Chamber Top Right': lambda items: canAccessCrocFromMainUpperNorfair(items),
        'Kronic Boost Room Bottom Right': lambda items: canAccessCrocFromMainUpperNorfair(items)
    },
    'Available': lambda items: wand(enoughStuffCroc(items),
                                    wor(canFly(items), haveItem(items, 'Grapple'),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (Norfair Reserve Tank)",
    'Class': "Minor",
    'Address': 0x78C44,
    'Visibility': "Hidden",
    'Room': 'Norfair Reserve Tank Room',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: canEnterNorfairReserveArea(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (bubble Norfair green door)",
    'Class': "Minor",
    'Address': 0x78C52,
    'Visibility': "Visible",
    'Room': 'Green Bubbles Missile Room',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: canEnterNorfairReserveArea(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (bubble Norfair)",
    'Class': "Minor",
    'Address': 0x78C66,
    'Visibility': "Visible",
    'Room': 'Bubble Mountain',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",    
    'Name': "Missile (Speed Booster)",
    'Class': "Minor",
    'Address': 0x78C74,
    'Visibility': "Hidden",
    'Room': 'Speed Booster Hall',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: canOpenGreenDoors(items)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'Name': "Missile (Wave Beam)",
    'Class': "Minor",
    'Address': 0x78CBC,
    'Visibility': "Visible",
    'Room': 'Double Chamber',
    'AccessPoints' : {
        'Single Chamber Top Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Warehouse Entrance Left': lambda items: canAccessHeatedNorfairFromEntrance(items)
    },
    'Available': lambda items: canOpenRedDoors(items)
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E6E,
    'Visibility': "Visible",
    'Room': "Golden Torizo's Room",
    'AccessPoints' : {
        'Lava Dive Right': lambda items: canPassLavaPit(items),
        'Three Muskateers Room Left': lambda items: canPassAmphitheaterReverse(items)
    },
    'Available': lambda items: wand(canHellRun(items, 'LowerNorfair'),
                                    haveItem(items, 'SpaceJump'))
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Super Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E74,
    'Visibility': "Hidden",
    'Room': "Golden Torizo's Room",
    'AccessPoints' : {
        'Lava Dive Right': lambda items: canPassLavaPit(items),
        'Three Muskateers Room Left': lambda items: canPassAmphitheaterReverse(items)
    },
    'Available': lambda items: wand(canHellRun(items, 'LowerNorfair'),
                                    wor(haveItem(items, 'SpaceJump'),
                                        Knows.GreenGateGlitch))
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Missile (Mickey Mouse room)",
    'Class': "Minor",
    'Address': 0x78F30,
    'Visibility': "Visible",
    'Room': 'Mickey Mouse Room',
    'AccessPoints' : {
        'Lava Dive Right': lambda items: wand(canPassLavaPit(items), canPassWorstRoom(items)),
        'Three Muskateers Room Left': lambda items: canPassAmphitheaterReverse(items)
    },
    'Available': lambda items: canHellRun(items, 'LowerNorfair')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Missile (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FCA,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Spring Ball Maze Room',
    'AccessPoints' : {
        'Lava Dive Right': lambda items: wand(canPassLavaPit(items), canPassWorstRoom(items)),
        'Three Muskateers Room Left': lambda items: SMBool(True, 0)
    },
    'Available': lambda items: canHellRun(items, 'LowerNorfair')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Power Bomb (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FD2,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Escape Power Bomb Room',
    'AccessPoints' : {
        'Lava Dive Right': lambda items: wand(canPassLavaPit(items), canPassWorstRoom(items)),
        'Three Muskateers Room Left': lambda items: SMBool(True, 0)
    },
    'Available': lambda items: wand(canHellRun(items, 'LowerNorfair'), haveItem(items, 'Morph'))
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Power Bomb (Power Bombs of shame)",
    'Class': "Minor",
    'Address': 0x790C0,
    'Visibility': "Visible",
    'Room': 'Wasteland',
    'AccessPoints' : {
        'Lava Dive Right': lambda items: wand(canPassLavaPit(items), canPassWorstRoom(items)),
        'Three Muskateers Room Left': lambda items: SMBool(True, 0)
    },
    'Available': lambda items: wand(canHellRun(items, 'LowerNorfair'),
                                    canOpenGreenDoors(items),
                                    canOpenYellowDoors(items))
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'Name': "Missile (lower Norfair near Wave Beam)",
    'Class': "Minor",
    'Address': 0x79100,
    'Visibility': "Visible",
    'Room': "Three Muskateers' Room",
    'AccessPoints' : {
        'Lava Dive Right': lambda items: wand(canPassLavaPit(items), canPassWorstRoom(items)),
        'Three Muskateers Room Left': lambda items: SMBool(True, 0)
    },
    'Available': lambda items: wand(canHellRun(items, 'LowerNorfair'),
                                    canPassBombPassages(items))
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Missile (Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x7C265,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship Main Shaft',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: canPassBombPassages(items)
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Missile (Gravity Suit)",
    'Class': "Minor",
    'Address': 0x7C2EF,
    'Visibility': "Visible",
    'Room': 'Bowling Alley',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: wand(wor(heatProof(items),
                                        energyReserveCountOk(items, 1)),
                                    Bosses.bossDead('Phantoon'),
                                    canPassBombPassages(items))
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Missile (Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x7C319,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship East Missile Room',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: Bosses.bossDead('Phantoon')
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'Name': "Super Missile (Wrecked Ship left)",
    'Class': "Minor",
    'Address': 0x7C357,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship West Super Room',
    'AccessPoints' : {
        'West Ocean Left': lambda items: canOpenGreenDoors(items),
        'Crab Maze Left': lambda items: canPassForgottenHighway(items, False)
    },
    'Available': lambda items: Bosses.bossDead('Phantoon')
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (green Maridia shinespark)",
    'Class': "Minor",
    'Address': 0x7C437,
    'Visibility': "Visible",
    'Room': 'Main Street',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: SMBool(True, 0)
    },
    'Available': lambda items: wand(haveItem(items, 'Gravity'),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(canOpenGreenDoors(items), # to run from room on the right
                                        Knows.SimpleShortCharge))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Super Missile (green Maridia)",
    'Class': "Minor",
    'Address': 0x7C43D,
    'Visibility': "Visible",
    'Room': 'Main Street',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wor(haveItem(items, 'Gravity'), canDoSuitlessOuterMaridia(items))
        # we could add eas access from red fish room here, but if you miss it you can't retry
    },
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (green Maridia tatori)",
    'Class': "Minor",
    'Address': 0x7C483,
    'Visibility': "Hidden",
    'Room': 'Mama Turtle Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wor(haveItem(items, 'Gravity'), canDoSuitlessOuterMaridia(items))
    },
    'Available': lambda items: canOpenRedDoors(items)
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Super Missile (yellow Maridia)",
    'Class': "Minor",
    'Address': 0x7C4AF,
    'Visibility': "Visible",
    'Room': 'Watering Hole',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: canPassMtEverest(items)
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (yellow Maridia super missile)",
    'Class': "Minor",
    'Address': 0x7C4B5,
    'Visibility': "Visible",
    'Room': 'Watering Hole',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: canPassMtEverest(items)
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (yellow Maridia false wall)",
    'Class': "Minor",
    'Address': 0x7C533,
    'Visibility': "Visible",
    'Room': 'Pseudo Plasma Spark Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: canPassMtEverest(items)
    },
    'Available': lambda items: (True, 0)
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (left Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5DD,
    'Visibility': "Visible",
    'Room': 'West Sand Hole',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items),
                                                 canOpenGreenDoors(items),
                                                 canUsePowerBombs(items))
    },
    # DONE: this item can be taken without gravity, but it's super hard because of the quick sands...
    'Available': lambda items: wor(haveItem(items, 'Gravity'),
                                   Knows.SuitlessSandpit) # suitless maridia conditions are in canPassMtEverest
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5EB,
    'Visibility': "Visible",
    'Room': 'East Sand Hole',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items),
                                                 canOpenGreenDoors(items),
                                                 canUsePowerBombs(items))
    },
    # DONE: this item can be taken without gravity, but it's super hard because of the quick sands...
    'Available': lambda items: wor(haveItem(items, 'Gravity'),
                                   Knows.SuitlessSandpit) # suitless maridia conditions are in canPassMtEverest
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Power Bomb (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5F1,
    'Visibility': "Visible",
    'Room': 'East Sand Hole',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items),
                                                 canOpenGreenDoors(items),
                                                 canUsePowerBombs(items))
    },
    'Available': lambda items: haveItem(items, 'Gravity')
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (pink Maridia)",
    'Address': 0x7C603,
    'Class': "Minor",
    'Visibility': "Visible",
    'Room': 'Aqueduct',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items),
                                                 canOpenGreenDoors(items),
                                                 canUsePowerBombs(items))
    },
    # DONE: this item can be taken without gravity, but it's super hard because of the quick sands...
    'Available': lambda items: wand(haveItem(items, 'SpeedBooster'), # TODO FLO find trick to get this without speed booster and add knows
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Super Missile (pink Maridia)",
    'Class': "Minor",
    'Address': 0x7C609,
    'Visibility': "Visible",
    'Room': 'Aqueduct',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items),
                                                 canOpenGreenDoors(items),
                                                 canUsePowerBombs(items))
    },
    'Available': lambda items: wand(haveItem(items, 'SpeedBooster'), # TODO FLO find trick to get this without speed booster and add knows
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'Name': "Missile (Draygon)",
    'Class': "Minor",
    'Address': 0x7C74D,
    'Visibility': "Hidden",
    'Room': 'The Precious Room',
    'AccessPoints' : {
        'Main Street Bottom': lambda items: wand(canPassMtEverest(items), canDefeatBotwoon(items), canOpenGreenDoors(items))
    },
    'Available': lambda items: (True, 0)
}
]
