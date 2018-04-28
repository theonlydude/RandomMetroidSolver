from smbool import SMBool

# the different difficulties available
easy = 1
medium = 5
hard = 10
harder = 25
hardcore = 50
mania = 100
god = mania*2
samus = god*2

diff2text = {
    0: 'baby',
    easy: 'easy',
    medium: 'medium',
    hard: 'hard',
    harder: 'very hard',
    hardcore: 'hardcore',
    mania: 'mania',
    god: 'god',
    samus: 'samus'
}

text2diff = {
    'baby': 0,
    'easy': easy,
    'medium': medium,
    'hard': hard,
    'harder': harder,
    'very hard': harder,
    'hardcore': hardcore,
    'mania': mania,
    'god': god,
    'samus': samus
}

def isConf(conf):
    return conf[0:len('__')] != '__'

class Conf:
    # ROM type, between :
    # - Total_TX/FX/CX/X/HX : Total's randomizer seeds, Tournament/Full/Casual/Normal/Hard
    # - Dessy : Dessyreqt randomizer seeds
    # - Vanilla : original game
    romType='Total_TX'
    # if true, will override seed type if ROM filename follows default filename patterns
    # from given rando
    guessRomType=True

    # keep getting majors of at most this difficulty before going for minors or changing area
    difficultyTarget=medium

    # display the generated path (spoilers!)
    displayGeneratedPath=False

    # choose how many items are required
    majorsPickup = 'minimal'
    #majorsPickup = 'all'
    #majorsPickup = 'any'
    minorsPickup = {
       'Missile' : 10,
       'Super' : 5,
       'PowerBomb' : 2
    }
    #minorsPickup = 'all'
    #minorsPickup = 'any'

    # the list of items to not pick up
    itemsForbidden = []

def isKnows(knows):
    return knows[0:len('__')] != '__' and knows[0] == knows[0].upper()

def staticConstructor(Class):
    Class.renameKnows(Class)
    return Class

@staticConstructor
class Knows:
    # the different technics to know (cf. http://deanyd.net/sm/index.php?title=Item_Randomizer)
    # and the personnal perceived difficulty.
    # False means: I can't do this technic or I don't know it.

    # store the descriptions used by the website along side the definition of the knows
    desc = {}

    # used across the game
    WallJump = SMBool(True, easy, ['WallJump'])
    desc['WallJump'] = {'display': 'Wall Jump',
                        'title': 'Kick-jump from wall: wall to wall, single wall climb, wall jump to instant morph',
                        'href': 'https://wiki.supermetroid.run/Walljump',
                        'rooms': [],
                        'readonly' : True}

    ShineSpark = SMBool(True, easy, ['ShineSpark'])
    desc['ShineSpark'] = {'display': 'Shinespark',
                          'title': 'With Speed Booster, press down to activate Shinespark. Then launch it in every possible direction, from ground or mid-air',
                          'href': 'https://wiki.supermetroid.run/Shinespark',
                          'rooms': [],
                          'readonly' : True}

    MidAirMorph = SMBool(True, easy, ['MidAirMorph'])
    desc['MidAirMorph'] = {'display': 'Mid-air Morph',
                           'title': 'Activate Morph Ball while jumping straight up (keep jump pressed) to reach high places in Morph Ball form without bomb jumping',
                           'href': None,
                           'rooms': [],
                           'readonly' : True}

    Mockball = SMBool(True, easy, ['Mockball'])
    desc['Mockball'] = {'display': 'Mockball',
                        'title': 'Morph from runing without loosing momentum to get Early Super and Ice Beam',
                        'href': 'https://wiki.supermetroid.run/index.php?title=Mockball',
                        'rooms': ['Early Supers Room', 'Ice Beam Gate Room']}

    SimpleShortCharge = SMBool(True, easy, ['SimpleShortCharge'])
    desc['SimpleShortCharge'] = {'display': 'Simple Short Charge',
                                 'title': 'Activate SpeedBooster faster for Waterway ETank without gravity, and Wrecked Ship access',
                                 'href': 'https://wiki.supermetroid.run/index.php?title=Quick_charge',
                                 'rooms': ['Parlor and Alcatraz', 'Waterway Energy Tank Room',
                                           'Landing Site', 'Crateria Keyhunter Room']}

    InfiniteBombJump = SMBool(True, medium, ['InfiniteBombJump'])
    desc['InfiniteBombJump'] = {'display': 'Infinite Bomb-Jump',
                                'title': 'To access certain locations without Hi-Jump or Space-Jump',
                                'href': 'https://www.youtube.com/watch?v=Qfmcm7hkXP4',
                                'rooms': ['Blue Brinstar Energy Tank Room', 'Post Crocomire Jump Room', 'Bubble Mountain', 'Screw Attack Room', 'Mama Turtle Room', 'Plasma Room', "Draygon's Room", 'Landing Site', 'Crocomire Escape', 'Post Crocomire Farming Room', 'Post Crocomire Jump Room', 'Warehouse Entrance', 'The Worst Room In The Game', 'Mt. Everest']}

    GreenGateGlitch = SMBool(True, medium, ['GreenGateGlitch'])
    desc['GreenGateGlitch'] = {'display': 'Green Gate Glitch',
                               'title': 'Open gates from other side to access Screw Attack and Crocomire',
                               'href': 'https://wiki.supermetroid.run/index.php?title=Gate_Glitch',
                               'rooms': ['Grapple Tutorial Room 3',
                                         'Fast Ripper Room',
                                         'Upper Norfair Farming Room']}

    ShortCharge = SMBool(False, 0, ['ShortCharge'])
    desc['ShortCharge'] = {'display': 'Short Charge',
                           'title': 'Activate SpeedBooster really fast, to kill draygon for example',
                           'href': 'https://wiki.supermetroid.run/index.php?title=Short_Charge',
                           'rooms': ['Plasma Room',
                                     'Crateria Super Room',
                                     "Draygon's Room"]}

    GravityJump = SMBool(True, hard, ['GravityJump'])
    desc['GravityJump'] = {'display': 'Gravity-Jump',
                           'title': "Super Hi-Jumps in water/lava using game's bug",
                           'href': 'https://wiki.supermetroid.run/index.php?title=14%25#Gravity_Jump',
                           'rooms': ["Draygon's Room",
                                     'The Moat',
                                     'Lava Dive Room',
                                     'Mt. Everest']}

    SpringBallJump = SMBool(True, hard, ['SpringBallJump'])
    desc['SpringBallJump'] = {'display': 'SpringBall-Jump',
                              'title': 'Do a SpringBall Jump from a jump to Access to Wrecked Ship Etank without anything else, Suitless Maridia navigation',
                              'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw&t=49s',
                              'rooms': ['Main Street',
                                        'Sponge Bath',
                                        'Mama Turtle Room',
                                        'The Precious Room']}

    SpringBallJumpFromWall = SMBool(True, harder, ['SpringBallJumpFromWall'])
    desc['SpringBallJumpFromWall'] = {'display': 'SpringBall-Jump from wall',
                                      'title': 'Do a SpringBall jump after a Wall jump to exit Screw Attack area, climb Worst Room without Hi-Jump',
                                      'href': None,
                                      'rooms': ['Screw Attack Room',
                                                'The Worst Room In The Game',
                                                'Bubble Mountain']}

    GetAroundWallJump = SMBool(True, hard, ['GetAroundWallJump'])
    desc['GetAroundWallJump'] = {'display': 'Get around Wall-Jump',
                                 'title': 'Tricky Wall-Jumps where you have to get around the platform you want to Wall-Jump on (access Norfair Reserve, go through Worst Room in the game, exit Plasma Room)',
                                 'href': 'https://www.youtube.com/watch?v=2GPx-6ARSIw&t=137s',
                                 'rooms': ['The Worst Room In The Game',
                                           'Bubble Mountain', 'Plasma Room']}

    # bosses
    DraygonGrappleKill = SMBool(True, medium, ['DraygonGrappleKill'])
    desc['DraygonGrappleKill'] = {'display': 'Draygon Grapple Kill',
                                  'title': 'Instant kill on Draygon with electric grapple',
                                  'href': 'https://www.youtube.com/watch?v=gcemRrXqCbE',
                                  'rooms': ["Draygon's Room"]}

    MicrowaveDraygon = SMBool(True, easy, ['MicrowaveDraygon'])
    desc['MicrowaveDraygon'] = {'display': 'Microwave Draygon',
                                'title': 'Charge/Plasma/X-Ray glitch on Draygon',
                                'href': 'https://www.youtube.com/watch?v=tj0VybUH6ZY',
                                'rooms': ["Draygon's Room"]}

    MicrowavePhantoon = SMBool(True, medium, ['MicrowavePhantoon'])
    desc['MicrowavePhantoon'] = {'display': 'Microwave Phantoon',
                                 'title': 'Same as Draygon, with a few missiles to start',
                                 'href': None,
                                 'rooms': ["Phantoon's Room"]}

    # End Game
    IceZebSkip = SMBool(False, 0, ['IceZebSkip'])
    desc['IceZebSkip'] = {'display': 'Ice Zeb Skip',
                          'title': 'Skip the Zebetites with Ice beam',
                          'href': 'https://www.youtube.com/watch?v=GBXi3MSpGZg',
                          'rooms': ['Mother Brain Room']}

    SpeedZebSkip = SMBool(False, 0, ['SpeedZebSkip'])
    desc['SpeedZebSkip'] = {'display': 'Speed Zeb Skip',
                            'title': 'Skip the Zebetites with a shinespark',
                            'href': 'https://www.youtube.com/watch?v=jEAgdWQ9kLQ',
                            'rooms': ['Mother Brain Room']}
    # underwater grav-less
    GravLessLevel0 = SMBool(True, easy, ['GravLessLevel0'])
    desc['GravLessLevel0'] = {'display': 'Level 0',
                              'title': 'Use crouch jump and downgrab to get out of ponds of water',
                              'href': None,
                              'rooms': [], # TODO spiky death, before Billy Mays, others?
                              'readonly' : True}

    SuitlessOuterMaridia = SMBool(True, hardcore, ['SuitlessOuterMaridia']) # keep SuitlessOuterMaridia as name for existing presets compatibility
    desc['SuitlessOuterMaridia'] = {'display': 'Level 1',
                                    'title': 'Level 0 + make your way underwater with Hi-Jump and Ice, freezing crabs and fishes. Access Botwoon with grapple.',
                                    'href': 'https://www.youtube.com/watch?v=c2xoPigezvM',
                                    'rooms': ['Main Street', 'Mt. Everest', 'Crab Shaft',
                                              'Aqueduct', 'Botwoon Hallway']} # TODO add forgotten highway rooms, crab hole

    GravLessLevel2 = SMBool(False, 0, ['GravLessLevel2'])
    desc['GravLessLevel2'] = {'display': 'Level 2',
                              'title': "Level 1 + access Draygon's lair and do the Draygon fight (exiting Draygon are separate techniques)",
                              'href': None,
                              'rooms': []} # TODO

    SuitlessSandpit = SMBool(False, 0, ['SuitlessSandpit']) # keep SuitlessSandpit as name for existing presets compatibility
    desc['SuitlessSandpit'] = {'display': 'Level 3',
                               'title': 'Level 2 and : no problem getting out of sand suitless, traverse mini-draygons area, wall jumps to access items in the left sand pit, access missile location in the right sand pit.',
                               'href': 'https://www.youtube.com/watch?v=1M2TiEVwH2I',
                               'rooms': ['West Sand Hole', 'East Sand Hole']} # TODO add mini-draygons rooms


    # Area difficulties

    # Brinstar
    CeilingDBoost = SMBool(True, easy, ['CeilingDBoost'])
    desc['CeilingDBoost'] = {'display': 'Ceiling Damage Boost',
                          'title': 'Hit an enemy at the right time to get the item in Blue Brinstar Ceiling',
                          'href': 'https://www.metroid2002.com/3/early_items_blue_brinstar_energy_tank.php',
                          'rooms': ['Blue Brinstar Energy Tank Room']}

    AlcatrazEscape = SMBool(True, harder, ['AlcatrazEscape'])
    desc['AlcatrazEscape'] = {'display': 'Alcatraz Escape',
                              'title': 'Escape from Bomb area using its entrance tunnel',
                              'href': 'https://www.youtube.com/watch?v=XSBeLJJafjY',
                              'rooms': ['Parlor and Alcatraz']}

    ReverseGateGlitch = SMBool(True, medium, ['ReverseGateGlitch'])
    desc['ReverseGateGlitch'] = {'display': 'Reverse Gate Glitch',
                                 'title': 'Open wave gate in Pink Brinstar from bottom left corner with Hi-Jump',
                                 'href': 'https://www.youtube.com/watch?v=cykJDBBSBrc',
                                 'rooms': ['Pink Brinstar Hopper Room']}

    ReverseGateGlitchHiJumpLess = SMBool(False, 0, ['ReverseGateGlitchHiJumpLess'])
    desc['ReverseGateGlitchHiJumpLess'] = {'display': 'Reverse Gate Glitch w/o Hi-Jump',
                                           'title': 'Open wave gate in Pink Brinstar from bottom left corner without Hi-Jump',
                                           'href': None,
                                           'rooms': ['Pink Brinstar Hopper Room']}

    EarlyKraid = SMBool(True, easy, ['EarlyKraid'])
    desc['EarlyKraid'] = {'display': 'Early Kraid',
                          'title': 'Access Kraid area by Wall-Jumping',
                          'href': 'https://www.youtube.com/watch?v=rHMHqTHHqHs',
                          'rooms': ['Warehouse Entrance']}

    XrayDboost = SMBool(False, 0, ['XrayDboost'])
    desc['XrayDboost'] = {'display': 'X-Ray Damage Boost',
                          'title': 'Get to X-Ray location without Space-Jump or Grapple',
                          'href': 'https://www.youtube.com/watch?v=2GPx-6ARSIw&t=162s',
                          'rooms': ['Red Brinstar Fireflea Room']}

    RedTowerClimb = SMBool(True, harder, ['RedTowerClimb'])
    desc['RedTowerClimb'] = {'display': 'Red Tower Climb',
                             'title': 'Climb Red Tower without Ice or Space-Jump',
                             'href': 'https://www.youtube.com/watch?v=g3goe6PZ4o0',
                             'rooms': ['Red Tower']}

    # Gauntlet
    HiJumpLessGauntletAccess = SMBool(False, 0, ['HiJumpLessGauntletAccess'])
    desc['HiJumpLessGauntletAccess'] = {'display': 'Gauntlet Access w/o Hi-Jump',
                                        'title': 'Access Gauntlet area using really tricky Wall-Jumps',
                                        'href': 'https://www.youtube.com/watch?v=uVU2X-egOTI&t=25s',
                                        'rooms': ['Landing Site']}

    HiJumpGauntletAccess = SMBool(True, harder, ['HiJumpGauntletAccess'])
    desc['HiJumpGauntletAccess'] = {'display': 'Hi-Jump Gauntlet Access',
                                    'title': 'Access Gauntlet area using tricky Wall-Jumps',
                                    'href': 'https://www.youtube.com/watch?v=2a6mf-kB60U',
                                    'rooms': ['Landing Site']}

    # Lower Norfair
    LavaDive = SMBool(True, harder, ['LavaDive'])
    desc['LavaDive'] = {'display': 'Lava Dive',
                        'title': 'Enter Lower Norfair with Varia and Hi-Jump',
                        'href': 'https://www.youtube.com/watch?v=pdyBy_54dB0',
                        'rooms': ['Lava Dive Room']}

    LavaDiveNoHiJump = SMBool(False, 0, ['LavaDiveNoHiJump'])
    desc['LavaDiveNoHiJump'] = {'display': 'Hi-Jump less Lava Dive',
                                'title': 'Enter Lower Norfair with just the Varia suit',
                                'href': 'https://www.youtube.com/watch?v=pdyBy_54dB0',
                                'rooms': ['Lava Dive Room']}

    WorstRoomIceCharge = SMBool(True, mania, ['WorstRoomIceCharge'])
    desc['WorstRoomIceCharge'] = {'display': 'Worst Room Ice and Charge',
                                  'title': 'Go through Worst Room In The Game JUST by freezing pirates',
                                  'href': 'https://www.youtube.com/watch?v=AYK7LREbLI8',
                                  'rooms': ['The Worst Room In The Game']}

    ScrewAttackExit = SMBool(True, medium, ['ScrewAttackExit'])
    desc['ScrewAttackExit'] = {'display': 'Screw Attack Exit',
                               'title': 'Gain momentum from Golden Torizo Energy Recharge room, then Wall-Jump in Screw Attack room',
                               'href': None,
                               'rooms': ['Screw Attack Room']}

    # wrecked ship
    ContinuousWallJump = SMBool(False, 0, ['ContinuousWallJump'])
    desc['ContinuousWallJump'] = {'display': 'Continuous Wall-Jump',
                                  'title': 'Get over the Moat using CWJ',
                                  'href': 'https://www.youtube.com/watch?v=4HVhTwwax6g',
                                  'rooms': ['The Moat']}

    DiagonalBombJump = SMBool(True, mania, ['DiagonalBombJump'])
    desc['DiagonalBombJump'] = {'display': 'Diagonal Bomb-Jump',
                                'title': 'Get over The Moat using Bomb-Jumps',
                                'href': 'https://www.youtube.com/watch?v=9Q8WGKCVb40',
                                'rooms': ['The Moat']}

    MockballWs = SMBool(True, hardcore, ['MockballWs'])
    desc['MockballWs'] = {'display': 'Mockball Wrecked Ship',
                          'title': 'Get over the moat using Mockball and Spring Ball',
                          'href': 'https://www.youtube.com/watch?v=WYxtRF--834',
                          'rooms': ['The Moat']}

    # wrecked ship etank access ("sponge bath" room)
    SpongeBathBombJump = SMBool(True, mania, ['SpongeBathBombJump'])
    desc['SpongeBathBombJump'] = {'display': 'SpongeBath Bomb-Jump',
                                  'title': 'Get through Sponge Bath room with Bomb-Jumps',
                                  'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw',
                                  'rooms': ['Sponge Bath']}

    SpongeBathHiJump = SMBool(True, easy, ['SpongeBathHiJump'])
    desc['SpongeBathHiJump'] = {'display': 'SpongeBath Hi-Jump',
                                'title': 'Get through sponge bath room with Hi-Jump and Wall-Jumps',
                                'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw',
                                'rooms': ['Sponge Bath']}

    SpongeBathSpeed = SMBool(True, medium, ['SpongeBathSpeed'])
    desc['SpongeBathSpeed'] = {'display': 'SpongeBath Speed',
                               'title': 'Get through sponge bath room with Speed Boster and Wall-Jumps',
                               'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw',
                               'rooms': ['Sponge Bath']}

    # Maridia
    # Suitless
    TediousMountEverest = SMBool(False, 0, ['TediousMountEverest'])
    desc['TediousMountEverest'] = {'display': 'Mt. Everest without anything',
                                    'title': 'Make your way through Mt. Everest with nothing but Ice (and Hi-Jump when suitless)',
                                    'href': 'https://www.youtube.com/watch?v=chFbX9rRV_k&t=123s',
                                    'rooms': ['Mt. Everest']}

    # Suitless Draygon
    DraygonRoomGrappleExit = SMBool(False, 0, ['DraygonRoomGrappleExit'])
    desc['DraygonRoomGrappleExit'] = {'display': 'Exit Draygon room with the Grapple',
                                      'title': 'Use Grapple to bounce them morph and demorph up to the platform',
                                      'href': 'https://www.youtube.com/watch?v=i2OGuFpcfiw&t=154s',
                                      'rooms': ["Draygon's Room"]}

    DraygonRoomCrystalFlash = SMBool(False, 0, ['DraygonRoomCrystalFlash'])
    desc['DraygonRoomCrystalFlash'] = {'display': 'Exit Draygon room or precious room with a shine spark',
                                       'title': 'Doing a Crystal flash and being grabbed by Draygon gives a free shine spark',
                                       'href': 'https://www.youtube.com/watch?v=hrHHfvGD3wo&t=625s',
                                       'rooms': ["Draygon's Room"]}

    PreciousRoomXRayExit = SMBool(False, 0, ['PreciousRoomXRayExit'])
    desc['PreciousRoomXRayExit'] = {'display': 'Exit the Precious room with an Xray glitch',
                                    'title': 'Use an XrayScope glitch to climb out of the Precious room',
                                    'href': 'https://www.youtube.com/watch?v=i2OGuFpcfiw&t=160s',
                                    'rooms': ['The Precious Room']}

    # clips
    MochtroidClip = SMBool(True, medium, ['MochtroidClip'])
    desc['MochtroidClip'] = {'display': 'Mochtroid Clip',
                             'title': 'Get to Botwoon with Ice Beam',
                             'href': 'https://wiki.supermetroid.run/index.php?title=14%25#Mochtroid_Clip',
                             'rooms': ['Botwoon Hallway']}

    PuyoClip = SMBool(False, 0, ['PuyoClip'])
    desc['PuyoClip'] = {'display': 'Puyo Clip',
                        'title': 'Get to Spring Ball with Gravity Suit and Ice Beam',
                        'href': 'https://www.youtube.com/watch?v=e5ZH_9paSLw',
                        'rooms': ['Pants Room']}

    SuitlessPuyoClip = SMBool(False, 0, ['SuitlessPuyoClip'])
    desc['SuitlessPuyoClip'] = {'display': 'Suitless Puyo Clip',
                                'title': 'Do the Puyo clip with Hi Jump and without Gravity',
                                'href': '',
                                'rooms': ['Pants Room']}

    # plasma room
    KillPlasmaPiratesWithSpark = SMBool(False, 0, ['KillPlasmaPiratesWithSpark'])
    desc['KillPlasmaPiratesWithSpark'] = {'display': 'Kill Plasma Pirates with Spark',
                                          'title': 'Use shinesparks to kill the pirates in Plasma Beam room',
                                          'href': None,
                                          'rooms': ['Plasma Room']}

    KillPlasmaPiratesWithCharge = SMBool(True, hard, ['KillPlasmaPiratesWithCharge'])
    desc['KillPlasmaPiratesWithCharge'] = {'display': 'Kill Plasma Pirates with Charge',
                                           'title': 'Use pseudo-screw to kill the pirates in Plasma Beam room',
                                           'href': None,
                                           'rooms': ['Plasma Room']}

    categories = [{'knows': ['WallJump', 'ShineSpark', 'MidAirMorph',
                             'Mockball', 'SimpleShortCharge', 'InfiniteBombJump', 'GreenGateGlitch',
                             'ShortCharge', 'GravityJump', 'SpringBallJump',
                             'SpringBallJumpFromWall', 'GetAroundWallJump'],
                   'title': 'Used across the game'},
                  {'knows': ['DraygonGrappleKill', 'MicrowaveDraygon', 'MicrowavePhantoon'],
                   'title': 'Bosses'},
                  {'knows': ['IceZebSkip', 'SpeedZebSkip'],
                   'title': 'End Game'},
                  {'knows': ['GravLessLevel0', 'SuitlessOuterMaridia', 'GravLessLevel2', 'SuitlessSandpit'],
                   'title': 'Underwater movement without Gravity Suit'},
                  {'knows': ['CeilingDBoost', 'AlcatrazEscape', 'ReverseGateGlitch',
                             'ReverseGateGlitchHiJumpLess', 'EarlyKraid', 'XrayDboost', 'RedTowerClimb'],
                   'title': 'Brinstar'},
                  {'knows': ['HiJumpLessGauntletAccess', 'HiJumpGauntletAccess'],
                   'title': 'Gauntlet'},
                  {'knows': ['LavaDive', 'LavaDiveNoHiJump', 'ScrewAttackExit', 'WorstRoomIceCharge'],
                   'title': 'Lower Norfair'},
                  {'knows': ['ContinuousWallJump', 'DiagonalBombJump', 'MockballWs'],
                   'title': 'Wrecked Ship'},
                  {'knows': ['SpongeBathBombJump', 'SpongeBathHiJump', 'SpongeBathSpeed'],
                   'title': 'Wrecked Ship Etank'},
                  {'knows': ['MochtroidClip', 'PuyoClip'],
                   'title': 'Maridia Clips'},
                  {'knows': ['KillPlasmaPiratesWithSpark', 'KillPlasmaPiratesWithCharge'],
                   'title': 'Maridia Plasma Room'},
                  {'knows': ['TediousMountEverest', 'SuitlessPuyoClip',
                             'DraygonRoomGrappleExit', 'DraygonRoomCrystalFlash', 'PreciousRoomXRayExit'],
                   'title': 'Maridia without Gravity Suit'}]

    newNames = {
        'SuitlessOuterMaridia' : 'GravLessLevel1',
        'SuitlessSandpit' : 'GravLessLevel3'
    }

    @staticmethod
    def renameKnows(Class):
        # handle renamed knows
        for old,new in Class.newNames.iteritems():
            if not hasattr(Class, new):
                setattr(Class, new, getattr(Class, old))


def isSettings(settings):
    return settings[0:len('__')] != '__'

class Settings:
    # boss difficulty tables :
    #
    # key is boss name. value is a dictionary where you define:
    #
    # 1. Rate : the rate of time in which you can land shots. For example
    # : 0.5 means you can land shots half the time in the boss (30secs in
    # a given minute). It represents a combination of the fraction of the
    # time you can hit the boss and your general accuracy against the boss.
    # If no information is given here, the fight will be
    # considered to be 2 minutes, regardless of anything else.
    #
    # 2. Energy : a dictionary where key is etanks+reserves you have,
    # value is estimated difficulty *for a 2-minute fight*, with Varia
    # suit only.
    # If not defined, the one below will be chosen, or the minimum one if
    # no below entry is defined. You can give any difficulty number
    # instead of the fixed values defined above.
    #
    # Actual difficulty calculation will also take into account estimated
    # fight duration. Difficulty will be multiplied with the ratio against
    # 2-minutes value entered here. The ammo margin will also be
    # considered if you do not have charge.
    #
    # If not enough info is provided here, base difficulty will be medium.

    # logic behind the presets : the ones where you find the boss difficult are
    # calibrated to give 'hard' in vanilla situations, the default are calibrated
    # to give 'medium' in vanilla situations, just above gives 'easy' in vanilla
    # situations, and top settings basically discards the boss except for extreme
    # situations (very low energy or firepower)
    bossesDifficultyPresets = {
        'Kraid' : {
            "He's annoying" : {
                'Rate' : 0.0075,
                'Energy' : {
                    0.5 : hard,
                    1 : medium,
                    2 : easy
                }
            },
            'Default' : {
                'Rate' : 0.015,
                'Energy' : {
                    0.5 : hard,
                    1.5 : medium,
                    2.5 : easy
                }
            },
            'Quick Kill' : {
                'Rate' : 1,
                'Energy' : {
                    0.5 : easy
                }
            }
        },
        'Phantoon' : {
            'A lot of trouble' : {
                'Rate' : 0.01,
                'Energy' : {
                    1 : mania,
                    3 : hardcore,
                    4 : harder,
                    5 : hard,
                    7 : medium,
                    10 : easy
                }
            },
            'Default' : {
                'Rate' : 0.015,
                'Energy' : {
                    1 : mania,
                    2 : hardcore,
                    4 : harder,
                    5 : hard,
                    6 : medium,
                    10 : easy
                }
            },
            'Used to it' : {
                'Rate' : 0.02,
                'Energy' : {
                    1 : (hardcore + mania)/2,
                    2 : harder,
                    2.5 : hard,
                    4 : medium,
                    6 : easy
                }
            },
            'No problemo' : {
                'Rate' : 0.02,
                'Energy' : {
                    1 : hard,
                    2 : medium,
                    3 : easy
                }
            }
        },
        'Draygon' : {
            'A lot of trouble' : {
                'Rate' : 0.025,
                'Energy' : {
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    11 : hard,
                    14 : medium,
                    20 : easy
                },
            },
            'Default' : {
                'Rate' : 0.05,
                'Energy' : {
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    11 : hard,
                    14 : medium,
                    20 : easy
                },
            },
            'Used to it' : {
                'Rate' : 0.06,
                'Energy' : {
                    1 : mania,
                    4 : hardcore,
                    6 : harder,
                    8 : hard,
                    11 : medium,
                    14 : easy
                },
            },
            'No problemo' : {
                'Rate' : 0.08,
                'Energy' : {
                    1 : mania,
                    4 : hardcore,
                    5 : harder,
                    6 : hard,
                    8 : medium,
                    12 : easy
                },
            }
        },
        'Ridley' : {
            "I'm scared!" : {
                'Rate' : 0.047,
                'Energy' : {
                    1 : mania,
                    7 : hardcore,
                    11 : harder,
                    14 : hard,
                    20 : medium
                },
            },
            'Default' : {
                'Rate' : 0.12,
                'Energy' : {
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    12 : hard,
                    20 : medium,
                    36 : easy
                },
            },
            'Used to it' : {
                'Rate' : 0.16,
                'Energy' : {
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    10 : hard,
                    14 : medium,
                    20 : easy
                },
            },
            'Piece of cake' : {
                'Rate' : 0.3,
                'Energy' : {
                    1 : mania,
                    3 : hardcore,
                    4 : harder,
                    6 : hard,
                    8 : medium,
                    10 : easy
                }
            }
        },
        'MotherBrain' : {
            "It can get ugly" : {
                'Rate' : 0.18,
                'Energy' : {
                    4 : mania, # less than 4 is actually impossible
                    8 : hardcore,
                    12 : harder,
                    16 : hard,
                    24 : medium,
                    32 : easy
                }
            },
            'Default' : {
                'Rate' : 0.25,
                'Energy' : {
                    4 : mania, # less than 4 is actually impossible
                    8 : hardcore,
                    12 : harder,
                    16 : hard,
                    20 : medium,
                    24 : easy
                }
            },
            'Is this really the last boss?': {
                'Rate' : 0.5,
                'Energy' : {
                    4 : mania, # less than 4 is actually impossible
                    6 : hardcore,
                    8 : harder,
                    12 : hard,
                    14 : medium,
                    20 : easy
                }
            },
            'Nice cutscene bro' : {
                'Rate' : 0.6,
                'Energy' : {
                    4 : hard, # less than 4 is actually impossible
                    8 : medium,
                    12 : easy
                }
            }
        }
    }

    bossesDifficulty = {
        'Kraid' : bossesDifficultyPresets['Kraid']['Default'],
        'Phantoon' : bossesDifficultyPresets['Phantoon']['Default'],
        'Draygon' : bossesDifficultyPresets['Draygon']['Default'],
        'Ridley' : bossesDifficultyPresets['Ridley']['Default'],
        'MotherBrain' : bossesDifficultyPresets['MotherBrain']['Default']
    }

    # hell run table
    # set entry to None to disable
    hellRunPresets = {
        'Ice' : {
            'No thanks' : None,
            # get comfortable before going in
            'Gimme energy' : [(4, hardcore), (5, harder), (6, hard), (10, medium)],
            # balanced setting
            'Default' : [(2, hardcore), (3, hard), (4, medium)],
            # you don't mind doing hell runs at all
            'Bring the heat' : [(2, hard), (3, medium)],
            # RBO runner
            'I run RBO' : [(2, medium), (3, easy)]
        },
        'MainUpperNorfair' : {
            'No thanks' : None,
            'Gimme energy' : [(4, mania), (6, hardcore), (8, harder), (10, hard), (14, medium)],
            'Default' : [(3, mania), (5, hardcore), (6, hard), (9, medium)],
            'Bring the heat' : [(3, hardcore), (4, hard), (5, medium), (7, easy)],
            'I run RBO' : [(3, harder), (4, hard), (5, medium), (6, easy)]
        },
        'LowerNorfair' : {
            'Default' : None,
            'Bring the heat' : [(9, mania), (12, hardcore), (14, harder), (18, hard)],
            'I run RBO' : [(7, mania), (9, hardcore), (11, harder), (14, hard), (18, medium)]
        }
    }

    hellRuns = {
        # Ice Beam hell run
        'Ice' : hellRunPresets['Ice']['Default'],
        # rest of upper norfair
        'MainUpperNorfair' : hellRunPresets['MainUpperNorfair']['Default'],
        'LowerNorfair' : hellRunPresets['LowerNorfair']['Default']
    }

    hardRoomsPresets = {
        'X-Ray' : {
            'Default' : [(6, hard), (8, medium), (10, easy)],
            "I don't like spikes" : [(8, hard), (10, medium), (14, easy)],
            'Aarghh' : [(10, hard), (14, medium)]
        },
        'Gauntlet' : {
            'Default' : [(0, harder), (1, hard), (3, medium), (6, easy)],
            "I don't like acid" : [(1, harder), (2, hard), (5, medium), (10, easy)],
            'Aarghh' : [(5, hard), (10, medium)]
        }
    }

    hardRooms = {
        'X-Ray' : hardRoomsPresets['X-Ray']['Default'],
        'Gauntlet' : hardRoomsPresets['Gauntlet']['Default']
    }

    # various settings used in difficulty computation
    algoSettings = {
        # Boss Fights

        # number of missiles fired per second during boss battles
        # (used along with Rate)
        'missilesPerSecond' : 3,
        # number of supers fired per second during boss battles
        # (used along with Rate)
        'supersPerSecond' : 1.85,
        # number of power bombs fired per second during boss battles
        # (used along with Rate)
        'powerBombsPerSecond' : 0.33,
        # number of charged shots per second (at most 1)
        'chargedShotsPerSecond' : 0.75,
        # firepower grabbed by picking up drops during boss battles
        # in missiles per minute (1 super = 3 missiles)
        'missileDropsPerMinute' : 12,
        # if no charge beam, amount of ammo margin to consider the boss
        # fight as 'normal' (1.5 = 50% more for instance)
        # boss fight difficulty will be linearly increased between this value
        # and 1
        'ammoMarginIfNoCharge' : 1.5,
        # divide the difficulty by this amount if charge or screw attack
        'phantoonFlamesAvoidBonus' : 1.2,
        # multiply the difficulty by this amount if no charge and few missiles
        'phantoonLowMissileMalus' : 1.2,
        # multiply the difficulty by this amount if you have to fight with water physics
        'draygonNoGravityMalus' : 2.0
    }
