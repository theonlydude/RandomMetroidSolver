# -*- coding: utf-8 -*-

import datetime, os.path

from parameters import *
from helpers import *
from tournament_locations import *
from solver import *
from get_random_rom import *

difficulties = {
    0: 'mania',
    easy : 'easy',
    medium : 'medium',
    hard : 'hard',
    harder : 'harder',
    hardcore : 'hardcore',
    mania : 'mania'
}

difficulties2 = {
    'easy' : easy,
    'medium' : medium,
    'hard' : hard,
    'harder' : harder,
    'hardcore' : hardcore,
    'mania' : mania
}

desc = {'Mockball': {'display': 'Mockball',
                     'title': 'Early super and ice beam',
                     'href': 'http://deanyd.net/sm/index.php?title=Mockball'},
        'SimpleShortCharge': {'display': 'Simple Short Charge',
                              'title': 'Waterway ETank without gravity, and Wrecked Ship access',
                              'href': 'http://deanyd.net/sm/index.php?title=Quick_charge'},
        'InfiniteBombJump': {'display': 'Infinite Bomb Jump',
                             'title': 'To access certain locations without high jump or space jump',
                             'href': 'https://www.youtube.com/watch?v=Qfmcm7hkXP4'},
        'GreenGateGlitch': {'display': 'Green Gate Glitch',
                            'title': 'To access screw attack and crocomire',
                            'href': 'http://deanyd.net/sm/index.php?title=Gate_Glitch'},
        'ShortCharge': {'display': 'Short Charge',
                        'title': 'To kill draygon',
                        'href': 'http://deanyd.net/sm/index.php?title=Short_Charge'},
        'GravityJump': {'display': 'Gravity Jump',
                        'title': 'n/a',
                        'href': 'http://deanyd.net/sm/index.php?title=14%25#Gravity_Jump'},
        'SpringBallJump': {'display': 'Spring Ball Jump',
                           'title': 'Access to wrecked ship etank without anything else and suitless maridia navigation',
                           'href': None},
        'DraygonGrappleKill': {'display': 'Draygon Grapple Kill', 'title': 'n/a', 'href': None},
        'MicrowaveDraygon': {'display': 'Microwave Draygon', 'title': 'n/a', 'href': None},
        'MicrowavePhantoon': {'display': 'Microwave Phantoon', 'title': 'n/a', 'href': None},
        'IceZebSkip': {'display': 'Ice Zeb Skip', 'title': 'n/a', 'href': None},
        'SpeedZebSkip': {'display': 'Speed Zeb Skip', 'title': 'n/a', 'href': None},
        'CeilingDBoost': {'display': 'Ceiling Damage Boost', 'title': 'n/a', 'href': None},
        'AlcatrazEscape': {'display': 'Alcatraz Escape', 'title': 'n/a', 'href': 'https://www.youtube.com/watch?v=XSBeLJJafjY'},
        'ReverseGateGlitch': {'display': 'Reverse Gate Glitch', 'title': 'n/a', 'href': None},
        'EarlyKraid': {'display': 'Early Kraid', 'title': 'n/a', 'href': None},
        'XrayDboost': {'display': 'Xray Damage Boost', 'title': 'n/a', 'href': None},
        'RedTowerClimb': {'display': 'Red Tower Climb', 'title': 'n/a', 'href': None},
        'HiJumpGauntletAccess': {'display': 'Hi-Jump Gauntlet Access', 'title': 'n/a', 'href': None},
        'GauntletWithBombs': {'display': 'Gauntlet With Bombs', 'title': 'n/a', 'href': None},
        'GauntletWithPowerBombs': {'display': 'Gauntlet With Power-Bombs', 'title': 'n/a', 'href': None},
        'GauntletEntrySpark': {'display': 'Gauntlet Entry Spark', 'title': 'n/a', 'href': None},
        'NorfairReserveHiJump': {'display': 'Norfair Reserve Hi-Jump', 'title': 'n/a', 'href': None},
        'WaveBeamWallJump': {'display': 'Wave-Beam Wall-Jump', 'title': 'n/a', 'href': None},
        'ClimbToGrappleWithIce': {'display': 'Climb to Grapple With Ice', 'title': 'n/a', 'href': None},
        'LavaDive': {'display': 'Lava Dive', 'title': 'n/a', 'href': None},
        'WorstRoomIceCharge': {'display': 'Worst Room Ice and Charge', 'title': 'n/a', 'href': None},
        'WorstRoomHiJump': {'display': 'Worst Room Hi-Jump', 'title': 'n/a', 'href': None},
        'ContinuousWallJump': {'display': 'Continuous Wall-Jump', 'title': 'n/a', 'href': None},
        'DiagonalBombJump': {'display': 'Diagonal Bomb-Jump', 'title': 'n/a', 'href': None},
        'MockballWs': {'display': 'Mockball Wrecked Ship', 'title': 'n/a', 'href': None},
        'SpongeBathBombJump': {'display': 'SpongeBath Bomb-Jump', 'title': 'n/a', 'href': None},
        'SpongeBathHiJump': {'display': 'SpongeBath Hi-Jump', 'title': 'n/a', 'href': None},
        'SpongeBathSpeed': {'display': 'SpongeBath Speed', 'title': 'n/a', 'href': None},
        'SuitlessOuterMaridia': {'display': 'Suitless Outer Maridia', 'title': 'n/a', 'href': None},
        'SuitlessOuterMaridiaNoGuns': {'display': 'Suitless Outer Maridia with no Guns', 'title': 'n/a', 'href': None},
        'MochtroidClip': {'display': 'Mochtroid Clip', 'title': 'n/a', 'href': None},
        'PuyoClip': {'display': 'Puyo Clip', 'title': 'n/a', 'href': None},
        'KillPlasmaPiratesWithSpark': {'display': 'Kill Plasma Pirates with Spark', 'title': 'n/a', 'href': None},
        'KillPlasmaPiratesWithCharge': {'display': 'Kill Plasma Pirates with Charge', 'title': 'n/a', 'href': None},
        'ExitPlasmaRoomHiJump': {'display': 'Exit Plasma room Hi-Jump', 'title': 'n/a', 'href': None},
        'SuitlessSandpit': {'display': 'Suitless Sandpit', 'title': 'n/a', 'href': None}
}

usedAcrossTheGame = ['Mockball', 'SimpleShortCharge', 'InfiniteBombJump', 'GreenGateGlitch', 'ShortCharge', 'GravityJump', 'SpringBallJump']
bosses = ['DraygonGrappleKill', 'MicrowaveDraygon', 'MicrowavePhantoon']
endGame = ['IceZebSkip', 'SpeedZebSkip']
brinstar = ['CeilingDBoost', 'AlcatrazEscape', 'ReverseGateGlitch', 'EarlyKraid', 'XrayDboost', 'RedTowerClimb']
gauntlet = ['HiJumpGauntletAccess', 'GauntletWithBombs', 'GauntletWithPowerBombs', 'GauntletEntrySpark']
upperNorfair = ['NorfairReserveHiJump', 'WaveBeamWallJump', 'ClimbToGrappleWithIce']
lowerNorfair = ['LavaDive', 'WorstRoomIceCharge', 'WorstRoomHiJump']
wreckedShip = ['ContinuousWallJump', 'DiagonalBombJump', 'MockballWs']
wreckedShipEtank = ['SpongeBathBombJump', 'SpongeBathHiJump', 'SpongeBathSpeed']
maridiaSuitless = ['SuitlessOuterMaridia', 'SuitlessOuterMaridiaNoGuns']
maridiaClips = ['MochtroidClip', 'PuyoClip']
maridiaPlasmaRoom = ['KillPlasmaPiratesWithSpark', 'KillPlasmaPiratesWithCharge', 'ExitPlasmaRoomHiJump']
maridiaSandpit = ['SuitlessSandpit']

categories = [{'knows': usedAcrossTheGame, 'title': 'Used across the game'},
              {'knows': bosses, 'title': 'Bosses'},
              {'knows': endGame, 'title': 'End Game'},
              {'knows': brinstar, 'title': 'Brinstar'},
              {'knows': gauntlet, 'title': 'Gauntlet'},
              {'knows': upperNorfair, 'title': 'Upper Norfair'},
              {'knows': lowerNorfair, 'title': 'Lower Norfair'},
              {'knows': wreckedShip, 'title': 'Wrecked Ship'},
              {'knows': wreckedShipEtank, 'title': 'Wrecked Ship Etank'},
              {'knows': maridiaSuitless, 'title': 'Maridia Suitless'},
              {'knows': maridiaClips, 'title': 'Maridia Clips'},
              {'knows': maridiaPlasmaRoom, 'title': 'Maridia Plasma Room'},
              {'knows': maridiaSandpit, 'title': 'Maridia Sandpit'}]

def solver():
    print("")
    print("")
    print("")


#    ,
#                  TR("difficulty_target:",
#                     SELECT('easy', 'medium', 'hard', 'harder', 'hardcore', 'mania',
#                            _name="difficulty_target",
#                            requires=IS_IN_SET(['easy', 'medium', 'hard',
#                                                'harder', 'hardcore', 'mania']),
#                            value=difficulties[Conf.difficultyTarget])))

    if session.paramsFile is not None:
        paramsFile = session.paramsFile
        print("Use {} params from session".format(paramsFile))
    else:
        paramsFile = 'regular'

    # load the presets
    params = ParamsLoader.factory('diff_presets/{}.json'.format(paramsFile)).params

#    # get the knowsXXX from the session if available
#    if session.paramsClass is not None and session.paramsDict is not None:
#        print("Use parameters from {}".format(session.lastUsed))
#        if session.paramsClass == 'noob':
#            print('use noob params from session')
#            params['noob']['Knows'] = session.paramsDict['Knows']
#        elif session.paramsClass == 'regular':
#            print('use regular params from session')
#            params['regular']['Knows'] = session.paramsDict['Knows']
#        elif session.paramsClass == 'veteran':
#            print('use veteran params from session')
#            params['veteran']['Knows'] = session.paramsDict['Knows']


    print("paramsFile={}".format(paramsFile))

    # main form
    mainTable = TABLE(TR("Tournament Rom seed: TX",
                         INPUT(_type="text",
                               _name="seed",
                               requires=IS_INT_IN_RANGE(0, 9999999, error_message = 'Seed is a number between 0 and 9999999'),
                               default=1234567)))
    mainTable.append(TR(INPUT(_type="submit",_value="Compute difficulty")))
    mainForm = FORM(mainTable, _id="mainform")

    if mainForm.accepts(request, session):
        response.flash="main form accepted"
        session.vars = mainForm.vars
        session.post_vars = request.post_vars
        redirect(URL(r=request, f='compute_difficulty'))
    elif mainForm.errors:
        response.flash="Seed number is invalid"


    # load form
    loadTable = TABLE(TR("Choose an available preset:", SELECT()))
    loadTable.append(TR(INPUT(_type="submit",_value="Load presets")))
    loadForm = FORM(loadTable, _id="loadform")

    if loadForm.accepts(request, session):
        response.flash="load form accepted"
        # check that the presets file exists
        paramsFile = mainForm.vars['paramsFile']
        fullPath = 'diff_presets/{}.json'.format(paramsFile)
        if os.path.isfile(fullPath):
            # load it

            session.paramsFile = paramsFile
        else:
            response.flash = "Presets file not found"

    elif mainForm.errors:
        response.flash="Invalid presets"


    # save form
    saveTable = TABLE(TR("Name of the preset:",
                         INPUT(_type="text",
                               _name="saveFile",
                               requires=[IS_NOT_EMPTY(),
                                         IS_ALPHANUMERIC(error_message='Preset name must be alphanumeric and max 32 chars'), 
                                         IS_LENGTH(32)])),
                      TR("Password:",
                         INPUT(_type="text",
                               _name="password",
                               requires=[IS_NOT_EMPTY(),
                                         IS_ALPHANUMERIC(error_message='Password must be alphanumeric and max 32 chars'), 
                                         IS_LENGTH(32)])))
    saveTable.append(TR(INPUT(_type="submit",_value="Save presets")))
    saveForm = FORM(saveTable, _id="loadform")


    # send values to view
    return dict(mainForm=mainForm, loadForm=loadForm, saveForm=saveForm,
                desc=desc,
                difficulties=difficulties,
                categories=categories,
                knows=params['Knows'],
                easy=easy,medium=medium,hard=hard,harder=harder,hardcore=hardcore,mania=mania)

def compute_difficulty():
    originalRom = '/home/dude/supermetroid_random/Super_Metroid_JU.smc'
    seed = session.vars['seed']

    # during development don't ask the same seed over and over again 
    #randomizedRom = getRandomizedRom(originalRom, seed)
    randomizedRom = 'TX6869602.sfc'

    # randomized rom is downloaded in "/home/dude/download/web2py"

    # generate json from parameters
    print("load from session:")
    print("session.vars={}".format(session.vars))
    print("session.post_vars={}".format(session.post_vars))
    paramsDict = {'Conf': {}, 'Settings': {}, 'Knows': {}}
    for var in Knows.__dict__:
        print("var={}".format(var))
        if var[0:len('__')] != '__':
            boolVar = session.post_vars[var+"_bool"]
            print("{} = {}".format(var+"_bool", boolVar))
            if boolVar is None:
                paramsDict['Knows'][var] = [False, 0]
            else:
                paramsDict['Knows'][var] = [True, difficulties2[session.post_vars[var+"_diff"]]]
            print("{}: {}".format(var, paramsDict['Knows'][var]))

    # store paramsDict in the session
    session.paramsDict = paramsDict
    session.paramsClass = session.vars['paramsClass']
    session.lastUsed = datetime.datetime.now()

    # call solver
    solver = Solver(type='web', rom=randomizedRom, params=[paramsDict])
    difficulty = solver.solveRom()
    text = DifficultyDisplayer(difficulty).scale()

    path = None
    if Conf.displayGeneratedPath is True and difficulty >= 0:
        path = solver.visitedLocations

    return dict(randomizedRom=randomizedRom, difficulty=difficulty, text=text, path=path)
