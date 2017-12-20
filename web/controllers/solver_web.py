# -*- coding: utf-8 -*-

import datetime

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

desc = {'Mockball': {'title': 'Early super and ice beam',
                     'href': 'http://deanyd.net/sm/index.php?title=Mockball'},
        'SimpleShortCharge': {'title': 'Waterway ETank without gravity, and Wrecked Ship access',
                              'href': 'http://deanyd.net/sm/index.php?title=Quick_charge'},
        'InfiniteBombJump': {'title': 'To access certain locations without high jump or space jump',
                             'href': 'https://www.youtube.com/watch?v=Qfmcm7hkXP4'},
        'GreenGateGlitch': {'title': 'To access screw attack and crocomire',
                            'href': 'http://deanyd.net/sm/index.php?title=Gate_Glitch'},
        'ShortCharge': {'title': 'To kill draygon',
                        'href': 'http://deanyd.net/sm/index.php?title=Short_Charge'},
        'GravityJump': {'title': 'n/a',
                        'href': 'http://deanyd.net/sm/index.php?title=14%25#Gravity_Jump'},
        'SpringBallJump': {'title': 'Access to wrecked ship etank without anything else and suitless maridia navigation',
                           'href': None},
        'DraygonGrappleKill': {'title': 'n/a', 'href': None},
        'MicrowaveDraygon': {'title': 'n/a', 'href': None},
        'MicrowavePhantoon': {'title': 'n/a', 'href': None},
        'IceZebSkip': {'title': 'n/a', 'href': None},
        'SpeedZebSkip': {'title': 'n/a', 'href': None},
        'CeilingDBoost': {'title': 'n/a', 'href': None},
        'AlcatrazEscape': {'title': 'n/a', 'href': 'https://www.youtube.com/watch?v=XSBeLJJafjY'},
        'ReverseGateGlitch': {'title': 'n/a', 'href': None},
        'EarlyKraid': {'title': 'n/a', 'href': None},
        'XrayDboost': {'title': 'n/a', 'href': None},
        'RedTowerClimb': {'title': 'n/a', 'href': None},
        'HiJumpGauntletAccess': {'title': 'n/a', 'href': None},
        'GauntletWithBombs': {'title': 'n/a', 'href': None},
        'GauntletWithPowerBombs': {'title': 'n/a', 'href': None},
        'GauntletEntrySpark': {'title': 'n/a', 'href': None},
        'NorfairReserveHiJump': {'title': 'n/a', 'href': None},
        'WaveBeamWallJump': {'title': 'n/a', 'href': None},
        'ClimbToGrappleWithIce': {'title': 'n/a', 'href': None},
        'LavaDive': {'title': 'n/a', 'href': None},
        'WorstRoomIceCharge': {'title': 'n/a', 'href': None},
        'WorstRoomHiJump': {'title': 'n/a', 'href': None},
        'ContinuousWallJump': {'title': 'n/a', 'href': None},
        'DiagonalBombJump': {'title': 'n/a', 'href': None},
        'MockballWs': {'title': 'n/a', 'href': None},
        'SpongeBathBombJump': {'title': 'n/a', 'href': None},
        'SpongeBathHiJump': {'title': 'n/a', 'href': None},
        'SpongeBathSpeed': {'title': 'n/a', 'href': None},
        'SuitlessOuterMaridia': {'title': 'n/a', 'href': None},
        'SuitlessOuterMaridiaNoGuns': {'title': 'n/a', 'href': None},
        'MochtroidClip': {'title': 'n/a', 'href': None},
        'PuyoClip': {'title': 'n/a', 'href': None},
        'KillPlasmaPiratesWithSpark': {'title': 'n/a', 'href': None},
        'KillPlasmaPiratesWithCharge': {'title': 'n/a', 'href': None},
        'ExitPlasmaRoomHiJump': {'title': 'n/a', 'href': None},
        'SuitlessSandpit': {'title': 'n/a', 'href': None}
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

    table = TABLE(TR("Tournament Rom seed: TX", INPUT(_type="text",_name="seed",requires=IS_NOT_EMPTY(),default=1234567)))

#    ,
#                  TR("difficulty_target:",
#                     SELECT('easy', 'medium', 'hard', 'harder', 'hardcore', 'mania',
#                            _name="difficulty_target",
#                            requires=IS_IN_SET(['easy', 'medium', 'hard',
#                                                'harder', 'hardcore', 'mania']),
#                            value=difficulties[Conf.difficultyTarget])))

    if session.paramsClass is not None:
        paramsClass = session.paramsClass
        print("Use {} params from session".format(paramsClass))
    else:
        paramsClass = 'veteran'

    # load the presets
    params = {}
    params['noob'] = ParamsLoader.factory('diff_presets/noob.json').params
    params['regular'] = ParamsLoader.factory('diff_presets/flo.json').params
    params['veteran'] = ParamsLoader.factory('diff_presets/veteran.json').params

    # get the knowsXXX from the session if available
    if session.paramsClass is not None and session.paramsDict is not None:
        print("Use parameters from {}".format(session.lastUsed))
        if session.paramsClass == 'noob':
            print('use noob params from session')
            params['noob']['Knows'] = session.paramsDict['Knows']
        elif session.paramsClass == 'regular':
            print('use regular params from session')
            params['regular']['Knows'] = session.paramsDict['Knows']
        elif session.paramsClass == 'veteran':
            print('use veteran params from session')
            params['veteran']['Knows'] = session.paramsDict['Knows']


    table.append(TR("Parameters preset", SELECT('noob', 'regular', 'veteran', _name='paramsClass', value=paramsClass, onchange="showDiv(this)"), ""))

    print("paramsClass={}".format(paramsClass))

    table.append(TR(INPUT(_type="submit",_value="SUBMIT")))

    form=FORM(table, _id="mainform")

    if form.accepts(request,session):
        response.flash="form accepted"
        #print("request={}".format(request))
        session.vars = form.vars
        session.post_vars = request.post_vars
        redirect(URL(r=request, f='compute_difficulty'))
    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"

    return dict(form=form,
                desc=desc,
                difficulties=difficulties,
                categories=categories,
                knows=params[session.paramsClass]['Knows'],
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
