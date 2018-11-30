from parameters import Knows, Settings, easy, medium, hard, harder, hardcore, mania
from helpers import Bosses
from rom import RomPatches
from smbool import SMBool

# all the items locations with the prerequisites to access them
locations = [
###### MAJORS
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Gauntlet",
    'Name': "Energy Tank, Gauntlet",
    'Class': "Major",
    'CanHidden': False,
    'Address': 0x78264,
    'Visibility': "Visible",
    'Room': 'Gauntlet Energy Tank Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wor(sm.canEnterAndLeaveGauntlet(),
                                   sm.wand(sm.haveItem('SpeedBooster'),
                                           sm.knowsShortCharge(),
                                           sm.canEnterAndLeaveGauntletQty(1, 0))) # thanks ponk! https://youtu.be/jil5zTBCF1s
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Bombs",
    'Name': "Bomb",
    'Address': 0x78404,
    'Class': "Major",
    'CanHidden': True,
    'Visibility': "Chozo",
    'Room': 'Bomb Torizo Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.haveItem('Morph'),
                                    sm.canOpenRedDoors()),
    'PostAvailable': lambda sm: sm.wor(sm.knowsAlcatrazEscape(),
                                       sm.canPassBombPassages())
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Terminator",
    'Name': "Energy Tank, Terminator",
    'Class': "Major",
    'CanHidden': False,
    'Address': 0x78432,
    'Visibility': "Visible",
    'Room': 'Terminator Room',
    'AccessFrom' : {
        'Lower Mushrooms Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar Reserve",
    'Name': "Reserve Tank, Brinstar",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7852C,
    'Visibility': "Chozo",
    'Room': 'Brinstar Reserve Tank Room',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenRedDoors(),
                                    sm.wor(sm.wand(sm.knowsMockball(),
                                                   sm.haveItem('Morph')),
                                           sm.haveItem('SpeedBooster')))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Pink Brinstar",
    'Name': "Charge Beam",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78614,
    'Visibility': "Chozo",
    'Room': 'Big Pink',
    'AccessFrom' : {
        'Big Pink': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canPassBombPassages()
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'SolveArea': "Blue Brinstar",
    'Name': "Morphing Ball",
    'Class': "Major",
    'CanHidden': False,
    'Address': 0x786DE,
    'Visibility': "Visible",
    'Room': 'Morph Ball Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'SolveArea': "Blue Brinstar",
    'Name': "Energy Tank, Brinstar Ceiling",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7879E,
    'Visibility': "Hidden",
    'Room': 'Blue Brinstar Energy Tank Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: sm.wor(sm.canOpenRedDoors(), RomPatches.has(RomPatches.BlueBrinstarBlueDoor))
    },
    # EXPLAINED: to get this major item the different technics are:
    #  -can fly (continuous bomb jump or space jump)
    #  -have the high jump boots
    #  -freeze the Reo to jump on it
    #  -do a damage boost with one of the two Geemers
    'Available': lambda sm: sm.wor(sm.knowsCeilingDBoost(),
                                   sm.canFly(),
                                   sm.wor(sm.haveItem('HiJump'),
                                          sm.haveItem('Ice'),
                                          sm.wand(sm.haveItem('SpeedBooster'),
                                                  sm.wor(sm.knowsSimpleShortCharge(), sm.knowsShortCharge()))))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar",
    'Name': "Energy Tank, Etecoons",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x787C2,
    'Visibility': "Visible",
    'Room': 'Etecoon Energy Tank Room',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canAccessEtecoons(),
    'PostAvailable': lambda sm: sm.canUsePowerBombs()
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Pink Brinstar",
    'Name': "Energy Tank, Waterway",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x787FA,
    'Visibility': "Visible",
    'Room': 'Waterway Energy Tank Room',
    'AccessFrom' : {
        'Big Pink': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.canOpenRedDoors(),
                                    sm.haveItem('SpeedBooster'),
                                    sm.wor(sm.haveItem('Gravity'),
                                           sm.knowsSimpleShortCharge(), # from the blocks above the water
                                           sm.knowsShortCharge()))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Pink Brinstar",
    'Name': "Energy Tank, Brinstar Gate",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78824,
    'Visibility': "Visible",
    'Room': 'Hopper Energy Tank Room',
    'AccessFrom' : {
        'Big Pink': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.wor(sm.haveItem('Wave'),
                                           sm.wand(sm.haveItem('Super'),
                                                   sm.haveItem('HiJump'),
                                                   sm.knowsReverseGateGlitch()),
                                           sm.wand(sm.haveItem('Super'),
                                                   sm.knowsReverseGateGlitchHiJumpLess())))
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'SolveArea': "Red Brinstar",
    'Name': "X-Ray Scope",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78876,
    'Visibility': "Chozo",
    'Room': 'X-Ray Scope Room',
    'AccessFrom' : {
        'Red Tower Top Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.wor(sm.haveItem('Grapple'),
                                           sm.haveItem('SpaceJump'),
                                           sm.wand(sm.energyReserveCountOkHardRoom('X-Ray'),
                                                   sm.wor(sm.knowsXrayDboost(),
                                                          sm.haveItem('Ice'),
                                                          sm.wand(sm.canUseBombs(),
                                                                  sm.knowsInfiniteBombJump())))))
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'SolveArea': "Red Brinstar",
    'Name': "Spazer",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7896E,
    'Visibility': "Chozo",
    'Room': 'Spazer Room',
    'AccessFrom' : {
        'East Tunnel Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                    sm.wor(sm.canPassBombPassages(),
                                           sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.SpazerShotBlock))))
},
{
    'Area': "Brinstar",
    'GraphArea': "Kraid",
    'SolveArea': "Kraid",
    'Name': "Energy Tank, Kraid",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7899C,
    'Visibility': "Hidden",
    'Room': 'Warehouse Energy Tank Room',
    'AccessFrom' : {
        'Warehouse Zeela Room Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: Bosses.bossDead('Kraid')
},
{
    'Area': "Brinstar",
    'GraphArea': "Kraid",
    'SolveArea': "Kraid",
    'Name': "Varia Suit",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78ACA,
    'Visibility': "Chozo",
    'Room': 'Varia Suit Room',
    'AccessFrom' : {
        'Warehouse Zeela Room Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canPassBombPassages(),
                                    sm.enoughStuffsKraid()),
    'Pickup': lambda: Bosses.beatBoss('Kraid'),
    'Unpickup': lambda: Bosses.unbeatBoss('Kraid')
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Norfair Ice",
    'Name': "Ice Beam",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78B24,
    'Visibility': "Chozo",
    'Room': 'Ice Beam Room',
    'AccessFrom' : {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                    sm.canHellRun('Ice'),
                                    sm.canPassBombPassages(), # if you fail
                                    sm.wor(sm.wand(sm.haveItem('Morph'),
                                                   sm.knowsMockball()),
                                           sm.haveItem('SpeedBooster')))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Crocomire",
    'Name': "Energy Tank, Crocomire",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78BA4,
    'Visibility': "Visible",
    'Room': "Crocomire's Room",
    'AccessFrom' : {
        'Croc Zone': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.enoughStuffCroc(),
                                    sm.wor(sm.haveItem('Grapple'),
                                           sm.haveItem('SpaceJump'),
                                           sm.energyReserveCountOk(3/sm.getDmgReduction())))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Norfair Entrance",
    'Name': "Hi-Jump Boots",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78BAC,
    'Visibility': "Chozo",
    'Room': 'Hi Jump Boots Room',
    'AccessFrom' : {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenRedDoors(), sm.haveItem('Morph')),
    'PostAvailable': lambda sm: sm.wor(sm.canPassBombPassages(),
                                       sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.HiJumpShotBlock)))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Crocomire",
    'Name': "Grapple Beam",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78C36,
    'Visibility': "Chozo",
    'Room': 'Grapple Beam Room',
    'AccessFrom' : {
        'Croc Zone': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.enoughStuffCroc(),
                                    sm.wor(sm.wand(sm.haveItem('Morph'),
                                                   sm.canFly()),
                                           sm.wand(sm.haveItem('SpeedBooster'),
                                                   sm.wor(sm.knowsShortCharge(),
                                                          sm.canUsePowerBombs())),
                                           sm.wand(sm.haveItem('Morph'),
                                                   sm.haveItem('SpeedBooster'),
                                                   sm.haveItem('HiJump')), # jump from the yellow plateform ennemy
                                           sm.wand(sm.haveItem('Super'),
                                                   sm.knowsGreenGateGlitch())))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Reserve",
    'Name': "Reserve Tank, Norfair",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78C3E,
    'Visibility': "Chozo",
    'Room': 'Norfair Reserve Tank Room',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: sm.canHellRun('MainUpperNorfair'),
    },
    'Available': lambda sm: sm.wand(sm.haveItem('Morph'), sm.canEnterNorfairReserveArea())
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Speed",
    'Name': "Speed Booster",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78C82,
    'Visibility': "Chozo",
    'Room': 'Speed Booster Room',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: sm.canOpenGreenDoors()
    },
    'Available': lambda sm: sm.canHellRun('MainUpperNorfair')
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Wave",
    'Name': "Wave Beam",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x78CCA,
    'Visibility': "Chozo",
    'Room': 'Wave Beam Room',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: sm.canHellRun('MainUpperNorfair', 0.75)
    },
    'Available': lambda sm: sm.canOpenRedDoors(),
    'PostAvailable': lambda sm: sm.wor(sm.haveItem('Morph'), # exit through lower passage under the spikes
                                       sm.wand(sm.wor(sm.haveItem('SpaceJump'), # exit through blue gate
                                                      sm.haveItem('Grapple')),
                                               sm.wor(sm.wand(sm.knowsGreenGateGlitch(), sm.heatProof()), # hell run + green gate glitch is too much
                                                      sm.haveItem('Wave'))))
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair After Amphitheater",
    'Name': "Energy Tank, Ridley",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x79108,
    'Visibility': "Hidden",
    'Room': 'Ridley Tank Room',
    'AccessFrom' : {
        'Ridley Zone': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'), sm.enoughStuffsRidley()),
    'Pickup': lambda: Bosses.beatBoss('Ridley'),
    'Unpickup': lambda: Bosses.unbeatBoss('Ridley')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair Screw Attack",
    'Name': "Screw Attack",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x79110,
    'Visibility': "Chozo",
    'Room': 'Screw Attack Room',
    # everything is handled by the graph
    'AccessFrom' : {
        'Screw Attack Bottom': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair After Amphitheater",
    'Name': "Energy Tank, Firefleas",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x79184,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Fireflea Room',
    'AccessFrom' : {
        'Firefleas': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True),
    # avoid doing the super annoying wall jump in the dark...
    'PostAvailable': lambda sm: sm.wor(sm.haveItem('Ice'),
                                       sm.haveItem('HiJump'),
                                       sm.canFly(),
                                       sm.canSpringBallJump())
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Gravity",
    'Name': "Reserve Tank, Wrecked Ship",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C2E9,
    'Visibility': "Chozo",
    'Room': 'Bowling Alley',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.haveItem('SpeedBooster'),
                                    sm.canPassBowling())
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Back",
    'Name': "Energy Tank, Wrecked Ship",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C337,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship Energy Tank Room',
    'AccessFrom' : {
        'Wrecked Ship Back': lambda sm: sm.canOpenRedDoors()
    },
    'Available': lambda sm: sm.wor(Bosses.bossDead('Phantoon'),
                                   RomPatches.has(RomPatches.WsEtankPhantoonAlive))
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Main",
    'Name': "Right Super, Wrecked Ship",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C365,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship East Super Room',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenGreenDoors(), sm.enoughStuffsPhantoon(), sm.canPassBombPassages()),
    'Pickup': lambda: Bosses.beatBoss('Phantoon'),
    'Unpickup': lambda: Bosses.unbeatBoss('Phantoon')
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Gravity",
    'Name': "Gravity Suit",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C36D,
    'Visibility': "Chozo",
    'Room': 'Gravity Suit Room',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canPassBombPassages(),
                                    sm.canPassBowling())
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Green",
    'Name': "Energy Tank, Mama turtle",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C47D,
    'Visibility': "Visible",
    'Room': 'Mama Turtle Room',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.wor(sm.haveItem('Gravity'), sm.canDoSuitlessOuterMaridia())
    },
    'Available': lambda sm: sm.wand(sm.canOpenRedDoors(),
                                    sm.wor(sm.wor(sm.canFly(),
                                                  sm.wand(sm.haveItem('Gravity'),
                                                          sm.haveItem('SpeedBooster')),
                                                  sm.wand(sm.haveItem('HiJump'),
                                                          sm.haveItem('SpeedBooster'),
                                                          sm.knowsHiJumpMamaTurtle())),
                                           sm.wor(sm.wand(sm.canUseSpringBall(),
                                                          sm.wor(sm.wand(sm.haveItem('HiJump'),
                                                                         sm.knowsSpringBallJump()),
                                                                 sm.knowsSpringBallJumpFromWall())),
                                                  sm.haveItem('Grapple'))))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Forgotten Highway",
    'Name': "Plasma Beam",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C559,
    'Visibility': "Chozo",
    'Room': 'Plasma Room',
    'AccessFrom' : { # simple because if draygon is dead, you can get there
        'Main Street Bottom': lambda sm: SMBool(True), # green gate+toilet
        'Le Coude Right': lambda sm: SMBool(True)
    },
    # DONE: to leave the Plasma Beam room you have to kill the space pirates and return to the door
    # to unlock the door:
    #  -kill draygon
    # to kill the space pirates:
    #  -do short charges with speedbooster
    #  -use pseudo screw
    #  -have screw attack
    #  -have plasma beam
    # to go back to the door:
    #  -have high jump boots
    #  -can fly (space jump or infinite bomb jump)
    #  -use short charge with speedbooster
    'Available': lambda sm: Bosses.bossDead('Draygon'),
    'PostAvailable': lambda sm: sm.wand(sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                                                       sm.knowsShortCharge(),
                                                       sm.knowsKillPlasmaPiratesWithSpark()),
                                               sm.wand(sm.haveItem('Charge'),
                                                       sm.knowsKillPlasmaPiratesWithCharge()),
                                               sm.haveItem('ScrewAttack', difficulty=easy),
                                               sm.haveItem('Plasma', difficulty=easy)),
                                        sm.wor(sm.canFly(),
                                               sm.wand(sm.haveItem('HiJump'),
                                                       sm.knowsGetAroundWallJump()),
                                               sm.wand(sm.haveItem('SpeedBooster'),
                                                       sm.knowsShortCharge())))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Reserve Tank, Maridia",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C5E3,
    'Visibility': "Chozo",
    'Room': 'West Sand Hole',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessBotwoonFromMainStreet()
    },
    'Available': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                   sm.knowsGravLessLevel3()) # suitless maridia conditions are in canAccessBotwoonFromMainStreet
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Sandpits",
    'Name': "Spring Ball",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C6E5,
    'Visibility': "Chozo",
    'Room': 'Spring Ball Room',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.wor(sm.canOpenGreenDoors(), sm.wand(sm.canOpenRedDoors(), RomPatches.has(RomPatches.AreaRandoGatesOther))), # gate
        'Le Coude Right': lambda sm: sm.wand(sm.wor(sm.canOpenYellowDoors(), RomPatches.has(RomPatches.AreaRandoBlueDoors)),
                                             sm.canOpenGreenDoors(),
                                             sm.canDestroyBombWallsUnderwater()) # toilet
    },
    'Available': lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'), # access pants room
                                           sm.wand(sm.haveItem('HiJump'),
                                                   sm.haveItem('Ice'),
                                                   sm.knowsGravLessLevel3())),
                                    sm.wor(sm.wand(sm.haveItem('Ice'), # puyo clip
                                                   sm.wor(sm.wand(sm.haveItem('Gravity'),
                                                                  sm.knowsPuyoClip()),
                                                          sm.knowsSuitlessPuyoClip())),
                                           sm.wand(sm.haveItem('Grapple'), # go through grapple block
                                                   sm.haveItem('Gravity'),
                                                   sm.wor(sm.canFlyDiagonally(),
                                                          sm.haveItem('HiJump'),
                                                          sm.wand(sm.haveItem('Bomb'),
                                                                  sm.wor(sm.knowsAccessSpringBallWithBombJumps(),
                                                                         sm.wand(sm.haveItem('SpringBall'),
                                                                                 sm.knowsAccessSpringBallWithSpringBallBombJumps()))),
                                                          sm.wand(sm.haveItem('SpringBall'), sm.knowsAccessSpringBallWithSpringBallJump()))),
                                           sm.wand(sm.haveItem('XRayScope'), sm.knowsAccessSpringBallWithXRayClimb())), # XRay climb
                                    sm.haveItem('Morph')),
    'PostAvailable': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                       sm.canSpringBallJump())
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Top",
    'Name': "Energy Tank, Botwoon",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C755,
    'Visibility': "Visible",
    'Room': 'Botwoon Energy Tank Room',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canDefeatBotwoon()
    },
    'Available': lambda sm: sm.haveItem('Morph')
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Top",
    'Name': "Space Jump",
    'Class': "Major",
    'CanHidden': True,
    'Address': 0x7C7A7,
    'Visibility': "Chozo",
    'Room': 'Space Jump Room',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessDraygonFromMainStreet()
    },
    'Available': lambda sm: sm.enoughStuffsDraygon(),
    'Pickup': lambda: Bosses.beatBoss('Draygon'),
    'Unpickup': lambda: Bosses.unbeatBoss('Draygon'),
    # to get out of draygon room:
    #   with gravity but without highjump/bomb/space jump: gravity jump
    #   dessyreqt randomizer in machosist can have suitless draygon:
    #     to exit draygon room: grapple or crystal flash (for free shine spark)
    #     to exit precious room: spring ball jump, xray scope glitch or stored spark
    'PostAvailable': lambda sm: sm.wor(sm.wand(sm.haveItem('Gravity'),
                                               sm.wor(sm.canFly(),
                                                      sm.knowsGravityJump(),
                                                      sm.wand(sm.haveItem('HiJump'),
                                                              sm.haveItem('SpeedBooster')))),
                                       sm.wand(sm.wand(sm.canCrystalFlash(),
                                                       sm.knowsDraygonRoomCrystalFlash()),
                                               # use the spark either to exit draygon room or precious room
                                               sm.wor(sm.wand(sm.haveItem('Grapple'),
                                                              sm.knowsDraygonRoomGrappleExit()),
                                                      sm.wand(sm.haveItem('XRayScope'),
                                                              sm.knowsPreciousRoomXRayExit()),
                                                      sm.canSpringBallJump())),
                                       # spark-less exit (no CF)
                                       sm.wand(sm.wand(sm.haveItem('Grapple'),
                                                       sm.knowsDraygonRoomGrappleExit()),
                                               sm.wor(sm.wand(sm.haveItem('XRayScope'),
                                                              sm.knowsPreciousRoomXRayExit()),
                                                      sm.canSpringBallJump())))
},
###### MINORS
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Landing Site",
    'Name': "Power Bomb (Crateria surface)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x781CC,
    'Visibility': "Visible",
    'Room': 'Crateria Power Bomb Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.wor(sm.haveItem('SpeedBooster'),
                                           sm.canFly()))
},
{
    'Area': "Crateria",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Bottom",
    'Name': "Missile (outside Wrecked Ship bottom)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x781E8,
    'Visibility': "Visible",
    'Room': 'West Ocean',
    'AccessFrom' : {
        'West Ocean Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canPassBombPassages()
},
{
    'Area': "Crateria",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip",
    'Name': "Missile (outside Wrecked Ship top)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x781EE,
    'Visibility': "Hidden",
    'Room': 'West Ocean',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: Bosses.bossDead('Phantoon')
},
{
    'Area': "Crateria",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Top",
    'Name': "Missile (outside Wrecked Ship middle)",
    'CanHidden': True,
    'Class': "Minor",
    'Address': 0x781F4,
    'Visibility': "Visible",
    'Room': 'West Ocean',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.haveItem('Super'), sm.haveItem('Morph'), Bosses.bossDead('Phantoon'))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Landing Site",
    'Name': "Missile (Crateria moat)",
    'Class': "Minor",
    'CanHidden': False,
    'Address': 0x78248,
    'Visibility': "Visible",
    'Room': 'The Moat',
    'AccessFrom' : {
        'Keyhunter Room Bottom': lambda sm: sm.canOpenYellowDoors()
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Landing Site",
    'Name': "Missile (Crateria bottom)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x783EE,
    'Visibility': "Visible",
    'Room': 'Pit Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canDestroyBombWalls()
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Gauntlet",
    'Name': "Missile (Crateria gauntlet right)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78464,
    'Visibility': "Visible",
    'Room': 'Green Pirates Shaft',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                           sm.canPassBombPassages()),
                                   sm.wand(sm.knowsShortCharge(), # https://www.youtube.com/watch?v=JU6BFcjuR4c
                                           sm.haveItem('SpeedBooster'),
                                           sm.canUsePowerBombs(),
                                           sm.energyReserveCountOk(1)))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Gauntlet",
    'Name': "Missile (Crateria gauntlet left)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7846A,
    'Visibility': "Visible",
    'Room': 'Green Pirates Shaft',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                           sm.canPassBombPassages()),
                                   sm.wand(sm.knowsShortCharge(), # https://www.youtube.com/watch?v=JU6BFcjuR4c
                                           sm.haveItem('SpeedBooster'),
                                           sm.canUsePowerBombs(),
                                           sm.energyReserveCountOk(1)))
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Landing Site",
    'Name': "Super Missile (Crateria)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78478,
    'Visibility': "Visible",
    'Room': 'Crateria Super Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.haveItem('SpeedBooster'),
                                    # reserves are hard to trigger midspark when not having ETanks
                                    sm.wor(sm.wand(sm.energyReserveCountOk(2), SMBool(sm.haveItemCount('ETank', 1))), # need energy to get out
                                           sm.wand(SMBool(sm.haveItemCount('ETank', 1)),
                                                   sm.wor(sm.haveItem('Grapple'), # use grapple/space or dmg protection to get out
                                                          sm.haveItem('SpaceJump'),
                                                          sm.heatProof()))),
                                    sm.wor(sm.haveItem('Ice'),
                                           sm.knowsShortCharge(),
                                           sm.knowsSimpleShortCharge())) # there's also a dboost involved in simple short charge or you have to kill the yellow enemies with some power bombs
},
{
    'Area': "Crateria",
    'GraphArea': "Crateria",
    'SolveArea': "Crateria Landing Site",
    'Name': "Missile (Crateria middle)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78486,
    'Visibility': "Visible",
    'Room': 'The Final Missile',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canPassBombPassages()
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar",
    'Name': "Power Bomb (green Brinstar bottom)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x784AC,
    'Visibility': "Chozo",
    'Room': 'Green Brinstar Main Shaft',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canAccessEtecoons(),
    'PostAvailable': lambda sm: sm.canUsePowerBombs()
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Pink Brinstar",
    'Name': "Super Missile (pink Brinstar)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x784E4,
    'Visibility': "Chozo",
    'Room': 'Spore Spawn Super Room',
    'AccessFrom' : {
        'Big Pink': lambda sm: SMBool(True)
    },
    # either you go the back way, using a super and the camera glitch,
    # or just beat spore spawn (so no sm.knows() setting needed for the glitch)
    'Available': lambda sm: sm.canOpenRedDoors(),
    'PostAvailable': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                        sm.canPassBombPassages())
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar",
    'Name': "Missile (green Brinstar below super missile)",
    'Class': "Minor",
    'CanHidden': False,
    'Address': 0x78518,
    'Visibility': "Visible",
    'Room': 'Early Supers Room',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canOpenRedDoors(),
    'PostAvailable': lambda sm: sm.wor(sm.canPassBombPassages(),
                                       RomPatches.has(RomPatches.EarlySupersShotBlock))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar Reserve",
    'Name': "Super Missile (green Brinstar top)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7851E,
    'Visibility': "Visible",
    'Room': 'Early Supers Room',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenRedDoors(),
                                    sm.wor(sm.wand(sm.haveItem('Morph'), sm.knowsMockball()),
                                           sm.haveItem('SpeedBooster')))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar Reserve",
    'Name': "Missile (green Brinstar behind missile)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78532,
    'Visibility': "Hidden",
    'Room': 'Brinstar Reserve Tank Room',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.haveItem('Morph'),
                                    sm.wor(sm.knowsMockball(),
                                           sm.haveItem('SpeedBooster')),
                                    sm.canOpenRedDoors(),
                                    sm.wor(sm.canPassBombPassages(),
                                           sm.wand(sm.knowsRonPopeilScrew(),
                                                   sm.haveItem('ScrewAttack'))))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar Reserve",
    'Name': "Missile (green Brinstar behind reserve tank)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78538,
    'Visibility': "Visible",
    'Room': 'Brinstar Reserve Tank Room',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenRedDoors(),
                                    sm.haveItem('Morph'),
                                    sm.wor(sm.knowsMockball(),
                                           sm.haveItem('SpeedBooster')))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Pink Brinstar",
    'Name': "Missile (pink Brinstar top)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78608,
    'Visibility': "Visible",
    'Room': 'Big Pink',
    'AccessFrom' : {
        'Big Pink': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Pink Brinstar",
    'Name': "Missile (pink Brinstar bottom)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7860E,
    'Visibility': "Visible",
    'Room': 'Big Pink',
    'AccessFrom' : {
        'Big Pink': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Pink Brinstar",
    'Name': "Power Bomb (pink Brinstar)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7865C,
    'Visibility': "Visible",
    'Room': 'Pink Brinstar Power Bomb Room',
    'AccessFrom' : {
        'Big Pink': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.haveItem('Super'))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Brinstar Hills",
    'Name': "Missile (green Brinstar pipe)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78676,
    'Visibility': "Visible",
    'Room': 'Green Hill Zone',
    'AccessFrom' : {
        'Green Hill Zone Top Right': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.haveItem('Morph')
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'SolveArea': "Blue Brinstar",
    'Name': "Power Bomb (blue Brinstar)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7874C,
    'Visibility': "Visible",
    'Room': 'Morph Ball Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canUsePowerBombs()
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'SolveArea': "Blue Brinstar",
    'Name': "Missile (blue Brinstar middle)",
    'Address': 0x78798,
    'Class': "Minor",
    'CanHidden': True,
    'Visibility': "Visible",
    'Room': 'Blue Brinstar Energy Tank Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.wor(sm.haveItem('Morph'), RomPatches.has(RomPatches.BlueBrinstarMissile)),
                                    sm.wor(sm.canOpenRedDoors(),
                                           RomPatches.has(RomPatches.BlueBrinstarBlueDoor)))
},
{
    'Area': "Brinstar",
    'GraphArea': "GreenPinkBrinstar",
    'SolveArea': "Green Brinstar",
    'Name': "Super Missile (green Brinstar bottom)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x787D0,
    'Visibility': "Visible",
    'Room': 'Etecoon Super Room',
    'AccessFrom' : {
        'Green Brinstar Elevator Right': lambda sm: sm.canAccessEtecoons()
    },
    'Available': lambda sm: sm.canOpenGreenDoors(),
    'PostAvailable': lambda sm: sm.canUsePowerBombs()
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'SolveArea': "Blue Brinstar",
    'Name': "Missile (blue Brinstar bottom)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78802,
    'Visibility': "Chozo",
    'Room': 'First Missile Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.haveItem('Morph')
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'SolveArea': "Blue Brinstar",
    'Name': "Missile (blue Brinstar top)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78836,
    'Visibility': "Visible",
    'Room': 'Billy Mays Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canUsePowerBombs()
},
{
    'Area': "Brinstar",
    'GraphArea': "Crateria",
    'SolveArea': "Blue Brinstar",
    'Name': "Missile (blue Brinstar behind missile)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7883C,
    'Visibility': "Hidden",
    'Room': 'Billy Mays Room',
    'AccessFrom' : {
        'Landing Site': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canUsePowerBombs()
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'SolveArea': "Red Brinstar Top",
    'Name': "Power Bomb (red Brinstar sidehopper room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x788CA,
    'Visibility': "Visible",
    'Room': 'Beta Power Bomb Room',
    'AccessFrom' : {
        'Red Brinstar Elevator': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                    sm.canUsePowerBombs())
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'SolveArea': "Red Brinstar Top",
    'Name': "Power Bomb (red Brinstar spike room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7890E,
    'Visibility': "Chozo",
    'Room': 'Alpha Power Bomb Room',
    'AccessFrom' : {
        'Red Brinstar Elevator': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canOpenGreenDoors()
},
{
    'Area': "Brinstar",
    'GraphArea': "RedBrinstar",
    'SolveArea': "Red Brinstar Top",
    'Name': "Missile (red Brinstar spike room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78914,
    'Visibility': "Visible",
    'Room': 'Alpha Power Bomb Room',
    'AccessFrom' : {
        'Red Brinstar Elevator': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                    sm.canUsePowerBombs())
},
{
    'Area': "Brinstar",
    'GraphArea': "Kraid",
    'SolveArea': "Kraid",
    'Name': "Missile (Kraid)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x789EC,
    'Visibility': "Hidden",
    'Room': 'Warehouse Keyhunter Room',
    'AccessFrom' : {
        'Warehouse Zeela Room Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canUsePowerBombs()
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Norfair Entrance",
    'Name': "Missile (lava room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78AE4,
    'Visibility': "Hidden",
    'Room': 'Cathedral',
    'AccessFrom' : {
        'Warehouse Entrance Left': lambda sm: sm.canEnterCathedral(0.66),
        'Bubble Mountain': lambda sm: sm.canHellRun('MainUpperNorfair', 0.66)
    },
    'Available': lambda sm: sm.haveItem('Morph')
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Norfair Ice",
    'Name': "Missile (below Ice Beam)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78B46,
    'Visibility': "Hidden",
    'Room': 'Crumble Shaft',
    'AccessFrom' : {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                    sm.canUsePowerBombs(),
                                    sm.canHellRun('Ice'))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Norfair Grapple Escape",
    'Name': "Missile (above Crocomire)",
    'Class': "Minor",
    'CanHidden': False,
    'Address': 0x78BC0,
    'Visibility': "Visible",
    'Room': 'Crocomire Escape',
    'AccessFrom' : {
        'Croc Zone': lambda sm: sm.canHellRun('MainUpperNorfair')
    },
    'Available': lambda sm: sm.canGrappleEscape()
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Norfair Entrance",
    'Name': "Missile (Hi-Jump Boots)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78BE6,
    'Visibility': "Visible",
    'Room': 'Hi Jump Energy Tank Room',
    'AccessFrom' : {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenRedDoors(), sm.haveItem('Morph')),
    'PostAvailable': lambda sm: sm.wor(sm.canPassBombPassages(),
                                       sm.wand(RomPatches.has(RomPatches.HiJumpShotBlock), sm.haveItem('Morph')))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Norfair Entrance",
    'Name': "Energy Tank (Hi-Jump Boots)",
    'CanHidden': True,
    'Class': "Minor",
    'Address': 0x78BEC,
    'Visibility': "Visible",
    'Room': 'Hi Jump Energy Tank Room',
    'AccessFrom' : {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canOpenRedDoors()
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Crocomire",
    'Name': "Power Bomb (Crocomire)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78C04,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Power Bomb Room',
    'AccessFrom' : {
        'Croc Zone': lambda sm: sm.energyReserveCountOk(1)
    },
    'Available': lambda sm: sm.wand(sm.enoughStuffCroc(),
                                    sm.wor(sm.wor(sm.canFly(),
                                                  sm.haveItem('Grapple'),
                                                  sm.haveItem('SpeedBooster')), # spark from the room before
                                           sm.wor(sm.haveItem('HiJump'), # run and jump from yellow platform
                                                  sm.wand(sm.haveItem('Ice'),
                                                          sm.knowsCrocPBsIce()),
                                                  sm.knowsCrocPBsDBoost())))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Crocomire",
    'Name': "Missile (below Crocomire)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78C14,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Missile Room',
    'AccessFrom' : {
        'Croc Zone': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canOpenRedDoors(), sm.enoughStuffCroc(), sm.haveItem('Morph'))
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Crocomire",
    'Name': "Missile (Grapple Beam)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78C2A,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Jump Room',
    'AccessFrom' : {
        'Croc Zone': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.enoughStuffCroc(),
                                    sm.wor(sm.wor(sm.wand(sm.haveItem('Morph'), # from below
                                                          sm.canFly()),
                                                  sm.wand(sm.haveItem('SpeedBooster'),
                                                          sm.wor(sm.knowsShortCharge(),
                                                                 sm.canUsePowerBombs()))),
                                           sm.wand(sm.haveItem('Super'), # from grapple room
                                                   sm.knowsGreenGateGlitch(),
                                                   sm.wor(sm.canFly(),
                                                          sm.haveItem('Grapple'))))), # TODO::test if accessible with a spark, and how many etanks required
    'PostAvailable': lambda sm: sm.wor(sm.haveItem('Morph'), # normal exit
                                       sm.wor(sm.haveItem('SpaceJump'), # go back to grapple room
                                              sm.wand(sm.haveItem('SpeedBooster'), sm.haveItem('HiJump')))) # jump from the yellow plateform ennemy
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Reserve",
    'Name': "Missile (Norfair Reserve Tank)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78C44,
    'Visibility': "Hidden",
    'Room': 'Norfair Reserve Tank Room',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: sm.canHellRun('MainUpperNorfair')
    },
    'Available': lambda sm: sm.wand(sm.haveItem('Morph'), sm.canEnterNorfairReserveArea())
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Reserve",
    'Name': "Missile (bubble Norfair green door)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78C52,
    'Visibility': "Visible",
    'Room': 'Green Bubbles Missile Room',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: sm.canHellRun('MainUpperNorfair', 2)
    },
    'Available': lambda sm: sm.canEnterNorfairReserveArea()
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Bottom",
    'Name': "Missile (bubble Norfair)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78C66,
    'Visibility': "Visible",
    'Room': 'Bubble Mountain',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Speed",
    'Name': "Missile (Speed Booster)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78C74,
    'Visibility': "Hidden",
    'Room': 'Speed Booster Hall',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: sm.canOpenGreenDoors()
    },
    'Available': lambda sm: sm.canHellRun('MainUpperNorfair')
},
{
    'Area': "Norfair",
    'GraphArea': "Norfair",
    'SolveArea': "Bubble Norfair Wave",
    'Name': "Missile (Wave Beam)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78CBC,
    'Visibility': "Visible",
    'Room': 'Double Chamber',
    'AccessFrom' : {
        'Bubble Mountain': lambda sm: sm.canHellRun('MainUpperNorfair', 0.75)
    },
    'Available': lambda sm: sm.canOpenRedDoors()
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair Screw Attack",
    'Name': "Missile (Gold Torizo)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78E6E,
    'Visibility': "Visible",
    'Room': "Golden Torizo's Room",
    'AccessFrom' : {
        'LN Above GT': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canHellRun('LowerNorfair'),
    'PostAvailable': lambda sm: sm.enoughStuffGT()
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair Screw Attack",
    'Name': "Super Missile (Gold Torizo)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78E74,
    'Visibility': "Hidden",
    'Room': "Golden Torizo's Room",
    'AccessFrom' : {
        'Screw Attack Bottom': lambda sm: SMBool(True)
    },
    'Available': lambda sm: SMBool(True),
    'PostAvailable': lambda sm: sm.enoughStuffGT()
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair Before Amphitheater",
    'Name': "Missile (Mickey Mouse room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78F30,
    'Visibility': "Visible",
    'Room': 'Mickey Mouse Room',
    'AccessFrom' : {
        'LN Entrance': lambda sm: sm.wand(sm.canUsePowerBombs(), sm.canPassWorstRoom()),
    },
    'Available': lambda sm: sm.canHellRun('LowerNorfair')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair After Amphitheater",
    'Name': "Missile (lower Norfair above fire flea room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x78FCA,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Spring Ball Maze Room',
    'AccessFrom' : {
        'Firefleas': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canHellRun('LowerNorfair')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair After Amphitheater",
    'Name': "Power Bomb (lower Norfair above fire flea room)",
    'Class': "Minor",
    'CanHidden': False,
    'Address': 0x78FD2,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Escape Power Bomb Room',
    'AccessFrom' : {
        'Firefleas': lambda sm: sm.canPassBombPassages()
    },
    'Available': lambda sm: sm.canHellRun('LowerNorfair')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair After Amphitheater",
    'Name': "Power Bomb (Power Bombs of shame)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x790C0,
    'Visibility': "Visible",
    'Room': 'Wasteland',
    'AccessFrom' : {
        'Ridley Zone': lambda sm: sm.canUsePowerBombs()
    },
    'Available': lambda sm: sm.canHellRun('LowerNorfair')
},
{
    'Area': "LowerNorfair",
    'GraphArea': "LowerNorfair",
    'SolveArea': "Lower Norfair After Amphitheater",
    'Name': "Missile (lower Norfair near Wave Beam)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x79100,
    'Visibility': "Visible",
    'Room': "Three Muskateers' Room",
    'AccessFrom' : {
        'Three Muskateers Room Left': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                    sm.canPassBombPassages())
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Main",
    'Name': "Missile (Wrecked Ship middle)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C265,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship Main Shaft',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.canPassBombPassages()
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Gravity",
    'Name': "Missile (Gravity Suit)",
    'Class': "Minor",
    'CanHidden': False,
    'Address': 0x7C2EF,
    'Visibility': "Visible",
    'Room': 'Bowling Alley',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.canPassBowling(),
                                    sm.canPassBombPassages())
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Top",
    'Name': "Missile (Wrecked Ship top)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C319,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship East Missile Room',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: Bosses.bossDead('Phantoon')
},
{
    'Area': "WreckedShip",
    'GraphArea': "WreckedShip",
    'SolveArea': "WreckedShip Main",
    'Name': "Super Missile (Wrecked Ship left)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C357,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship West Super Room',
    'AccessFrom' : {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    'Available': lambda sm: Bosses.bossDead('Phantoon')
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Green",
    'Name': "Missile (green Maridia shinespark)",
    'Class': "Minor",
    'CanHidden': False,
    'Address': 0x7C437,
    'Visibility': "Visible",
    'Room': 'Main Street',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: SMBool(True)
    },
    'Available': lambda sm: sm.wand(sm.haveItem('Gravity'),
                                    sm.haveItem('SpeedBooster'),
                                    sm.wor(sm.wand(sm.canOpenGreenDoors(), # run from room on the right
                                                   SMBool(sm.haveItemCount('ETank', 1))), # etank for the spark since sparking from low ground
                                           sm.knowsSimpleShortCharge(), # run from above
                                           sm.knowsShortCharge())) # run from below and jump
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Green",
    'Name': "Super Missile (green Maridia)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C43D,
    'Visibility': "Visible",
    'Room': 'Main Street',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                                sm.canDoSuitlessOuterMaridia())
        # we could add eas access from red fish room here, but if you miss it you can't retry
    },
    'Available': lambda sm: sm.haveItem('Morph')
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Green",
    'Name': "Missile (green Maridia tatori)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C483,
    'Visibility': "Hidden",
    'Room': 'Mama Turtle Room',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                                sm.canDoSuitlessOuterMaridia())
    },
    'Available': lambda sm: sm.canOpenRedDoors()
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Super Missile (yellow Maridia)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C4AF,
    'Visibility': "Visible",
    'Room': 'Watering Hole',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canPassMtEverest()
    },
    'Available': lambda sm: sm.wor(sm.canPassBombPassages(),
                                   sm.canUseSpringBall())
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Missile (yellow Maridia super missile)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C4B5,
    'Visibility': "Visible",
    'Room': 'Watering Hole',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canPassMtEverest()
    },
    'Available': lambda sm: sm.wor(sm.canPassBombPassages(), sm.canUseSpringBall())
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Missile (yellow Maridia false wall)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C533,
    'Visibility': "Visible",
    'Room': 'Pseudo Plasma Spark Room',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canPassMtEverest()
    },
    'Available': lambda sm: SMBool(True)
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Missile (left Maridia sand pit room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C5DD,
    'Visibility': "Visible",
    'Room': 'West Sand Hole',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessBotwoonFromMainStreet()
    },
    'Available': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                   sm.knowsGravLessLevel3()) # suitless maridia conditions are in canPassMtEverest
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Missile (right Maridia sand pit room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C5EB,
    'Visibility': "Visible",
    'Room': 'East Sand Hole',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessBotwoonFromMainStreet()
    },
    'Available': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                   sm.knowsGravLessLevel3()) # suitless maridia conditions are in canPassMtEverest
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Power Bomb (right Maridia sand pit room)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C5F1,
    'Visibility': "Visible",
    'Room': 'East Sand Hole',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessBotwoonFromMainStreet()
    },
    'Available': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                   sm.wand(sm.knowsGravLessLevel3(),
                                           sm.canSpringBallJump())) # https://www.youtube.com/watch?v=7LYYxphRRT0
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Missile (pink Maridia)",
    'Address': 0x7C603,
    'Class': "Minor",
    'CanHidden': True,
    'Visibility': "Visible",
    'Room': 'Aqueduct',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessBotwoonFromMainStreet()
    },
    'Available': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                           sm.wand(sm.knowsSnailClip(), sm.haveItem('Morph'))),
                                    sm.haveItem('Gravity'))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Bottom",
    'Name': "Super Missile (pink Maridia)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C609,
    'Visibility': "Visible",
    'Room': 'Aqueduct',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessBotwoonFromMainStreet()
    },
    'Available': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                           sm.wand(sm.knowsSnailClip(), sm.haveItem('Morph'))),
                                    sm.haveItem('Gravity'))
},
{
    'Area': "Maridia",
    'GraphArea': "Maridia",
    'SolveArea': "Maridia Pink Top",
    'Name': "Missile (Draygon)",
    'Class': "Minor",
    'CanHidden': True,
    'Address': 0x7C74D,
    'Visibility': "Hidden",
    'Room': 'The Precious Room',
    'AccessFrom' : {
        'Main Street Bottom': lambda sm: sm.canAccessDraygonFromMainStreet()
    },
    'Available': lambda sm: SMBool(True)
}
]
