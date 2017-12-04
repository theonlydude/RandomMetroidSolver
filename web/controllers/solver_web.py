# -*- coding: utf-8 -*-

import datetime

from parameters import *
from helpers import *
from tournament_locations import *
from solver import *
from get_random_rom import *

difficulties = {
    0: 'false',
    easy : 'easy',
    medium : 'medium',
    hard : 'hard',
    harder : 'harder',
    hardcore : 'hardcore',
    mania : 'mania'
}

difficulties2 = {
    'false': 0,
    'easy' : easy,
    'medium' : medium,
    'hard' : hard,
    'harder' : harder,
    'hardcore' : hardcore,
    'mania' : mania
}

tutorials = {
    'AlcatrazEscape': 'https://www.youtube.com/watch?v=XSBeLJJafjY'
}

def solver():
    print("")
    print("")
    print("")

    table = TABLE(TR("Tournament Rom seed:", INPUT(_type="text",_name="seed",requires=IS_NOT_EMPTY(),default=1234567)))

#    ,
#                  TR("difficulty_target:",
#                     SELECT('easy', 'medium', 'hard', 'harder', 'hardcore', 'mania',
#                            _name="difficulty_target",
#                            requires=IS_IN_SET(['easy', 'medium', 'hard',
#                                                'harder', 'hardcore', 'mania']),
#                            value=difficulties[Conf.difficultyTarget])))

    if session.paramsClass is not None:
        paramsClass = session.paramsClass
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
            params['noob']['Knows'] = session.paramsDict['Knows']
        elif session.paramsClass == 'regular':
            params['regular']['Knows'] = session.paramsDict['Knows']
        elif session.paramsClass == 'veteran':
            params['veteran']['Knows'] = session.paramsDict['Knows']


    table.append(TR("Parameters preset", SELECT('noob', 'regular', 'veteran', _name='paramsClass', value=paramsClass), ""))

    table.append(TR("", "Do I know the technic", "Difficulty of the technic"))

    print("paramsClass={}".format(paramsClass))

    for var in params[paramsClass]['Knows']:
        # check if a link to a tutorial exists
        if var in tutorials:
            text = DIV('{} ('.format(var), A('link', _href=tutorials[var]), ')')
        else:
            text = "{}: ".format(var)

        print("var={} value={}".format(var, params[paramsClass]['Knows'][var]))

        table.append(TR(text,
                        INPUT(_type='checkbox',
                              _name="{}_bool".format(var),
                              value=params[paramsClass]['Knows'][var][0]),
                        SELECT('false', 'easy', 'medium', 'hard', 'harder', 'hardcore', 'mania',
                               _name="{}_diff".format(var),
                               value=difficulties[params[paramsClass]['Knows'][var][1]])))

    print("apres for var in params")

    table.append(TR(INPUT(_type="submit",_value="SUBMIT")))

    form=FORM(table)

    if form.accepts(request,session):
        response.flash="form accepted"
        session.vars = form.vars
        redirect(URL(r=request, f='compute_difficulty'))
    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"
    return dict(form=form,vars=form.vars)

def compute_difficulty():
    originalRom = '/home/dude/supermetroid_random/Super_Metroid_JU.smc'
    seed = session.vars['seed']

    # during development don't ask the same seed over and over again 
    #randomizedRom = getRandomizedRom(originalRom, seed)
    randomizedRom = 'TX6869602.sfc'

    # randomized rom is downloaded in "/home/dude/download/web2py"

    # generate json from parameters
    print("load from session:")
    paramsDict = {'Conf': {}, 'Settings': {}, 'Knows': {}}
    for var in Knows.__dict__:
        if var[0:len('__')] != '__':
            paramsDict['Knows'][var] = [True if session.vars[var+"_bool"] == 'on' else False, difficulties2[session.vars[var+"_diff"]]]
            print("{}: {}".format(var, paramsDict['Knows'][var]))


    # store paramsDict in the session
    session.paramsDict = paramsDict
    session.paramsClass = session.vars['paramsClass']
    session.lastUsed = datetime.datetime.now()

    # call solver
    solver = Solver(type='web')
    solver.loadRom(randomizedRom)
    solver.loadParams(paramsDict)
    solver.postInit()
    difficulty = solver.solveRom()
    text = DifficultyDisplayer(difficulty).scale()

    path = None
    if Conf.displayGeneratedPath is True and difficulty >= 0:
        path = solver.visitedLocations

    return dict(vars=[randomizedRom, difficulty, text, path])
