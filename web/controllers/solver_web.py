# -*- coding: utf-8 -*-

import sys, os.path
path = os.path.expanduser('~/RandomMetroidSolver')
if os.path.exists(path) and path not in sys.path:
    sys.path.append(path)

import datetime, os, hashlib, json

# to solve the rom
from parameters import easy, medium, hard, harder, hardcore, mania, Conf, Knows, Settings, isKnows
import tournament_locations
from solver import Solver, ParamsLoader, DifficultyDisplayer, RomLoader

difficulties = {
    0: 'mania',
    easy : 'easy',
    medium : 'medium',
    hard : 'hard',
    harder : 'very hard',
    hardcore : 'hardcore',
    mania : 'mania'
}

difficulties2 = {
    'easy' : easy,
    'medium' : medium,
    'hard' : hard,
    'harder' : harder,
    'very hard': harder,
    'hardcore' : hardcore,
    'mania' : mania
}

def solver():
    # load conf from session if available
    loaded = False
    if session.paramsFile is None:
        # default preset
        session.paramsFile = 'regular'

    if request.post_vars._formname is not None:
        # press solve, load or save button
        if request.post_vars._formname in ['saveform', 'mainform']:
            # store the changes in case the form won't be accepted
            paramsDict = generate_json_from_parameters(request.post_vars,
                                                       hidden=(request.post_vars._formname == 'saveform'))
            session.paramsDict = paramsDict
            params = ParamsLoader.factory(session.paramsDict).params
            loaded = True
        elif request.post_vars._formname in ['loadform']:
            # nothing to load, we'll load the new params file with the load form code
            pass
    else:
        # no forms button pressed
        if session.paramsDict is not None:
            params = ParamsLoader.factory(session.paramsDict).params
            loaded = True

    if not loaded:
        params = ParamsLoader.factory('diff_presets/{}.json'.format(session.paramsFile)).params

    # filter the displayed roms to display only the ones uploaded in this session
    if session.romFiles is None:
        session.romFiles = []
        roms = []
    elif len(session.romFiles) == 0:
        roms = []
    else:
        files = sorted(os.listdir('roms'))
        bases = [os.path.splitext(file)[0] for file in files]
        filtered = [base for base in bases if base in session.romFiles]
        roms = [file+'.sfc' for file in filtered]

    # main form
    mainForm = FORM(TABLE(TR("Already uploaded rom in this session: ",
                             SELECT(*roms, **dict(_name="romFile", value=session.romFile+'.sfc' if session.romFile is not None else None))),
                          TR("Randomized Super Metroid rom: ",
                             INPUT(_type="file", _name="uploadFile", _id="uploadFile"))),
                          INPUT(_type="submit",_value="Compute difficulty"),
                          INPUT(_type="text", _name="json", _id="json", _style='display:none'),
                    _id="mainform", _name="mainform", _onsubmit="doSubmit();")

    if mainForm.process(formname='mainform').accepted:
        # new uploaded rom ?
        error = False
        if mainForm.vars['json'] != '':
            try:
                tempRomJson = json.loads(mainForm.vars['json'])
                romFileName = tempRomJson["romFileName"]
                (base, ext) = os.path.splitext(romFileName)
                jsonRomFileName = 'roms/' + base + '.json'
                del tempRomJson["romFileName"]

                # json keys are strings
                romJson = {}
                for address in tempRomJson:
                    romJson[int(address)] = tempRomJson[address]

                romLoader = RomLoader.factory(romJson)
                romLoader.assignItems(tournament_locations.locations)
                romLoader.dump(jsonRomFileName)

                session.romFile = base
                if base not in session.romFiles:
                    session.romFiles.append(base)
            except:
                response.flash = "Error loading the rom file"
                error = True

        # python3:
        # no file: type(mainForm.vars['uploadFile'])=[<class 'str'>]
        # file:    type(mainForm.vars['uploadFile'])=[<class 'cgi.FieldStorage'>]
        # python2:
        # no file: type(mainForm.vars['uploadFile'])=[<type 'str'>]
        # file:    type(mainForm.vars['uploadFile'])=[<type 'instance'>]
        elif mainForm.vars['uploadFile'] is not None and type(mainForm.vars['uploadFile']) != str:
            uploadFileName = mainForm.vars['uploadFile'].filename
            uploadFileContent = mainForm.vars['uploadFile'].file

            (base, ext) = os.path.splitext(uploadFileName)
            jsonRomFileName = 'roms/' + base + '.json'

            if ext not in ['.sfc', '.smc']:
                response.flash = "Rom file must be .sfc or .smc"
                error = True
            else:
                # try loading it and create a json from it
                try:
                    tempRomFile = 'roms/' + base + '.sfc'
                    with open(tempRomFile, 'wb') as tempRom:
                        tempRom.write(uploadFileContent.read())

                    romLoader = RomLoader.factory(tempRomFile)
                    romLoader.assignItems(tournament_locations.locations)
                    romLoader.dump(jsonRomFileName)

                    os.remove(tempRomFile)

                    session.romFile = base
                    if base not in session.romFiles:
                        session.romFiles.append(base)
                except:
                    response.flash = "Error loading the rom file"
                    error = True

        elif len(mainForm.vars['romFile']) != 0:
            session.romFile = os.path.splitext(mainForm.vars['romFile'])[0]
            jsonRomFileName = 'roms/' + session.romFile + '.json'

        else:
            response.flash = "No rom file selected for upload"
            error = True

        if not error:
            # check that the json file exists
            if not os.path.isfile(jsonRomFileName):
                response.flash = "Missing json rom file on the server"
            else:
                session.result = compute_difficulty(jsonRomFileName, request.post_vars)
                redirect(URL(r=request, f='solver'))

    # load form
    files = sorted(os.listdir('diff_presets'))
    presets = [os.path.splitext(file)[0] for file in files]

    loadForm = FORM("Choose an available preset: ",
                    SELECT(*presets, **dict(_name="paramsFile", value=session.paramsFile, _onchange="this.form.submit()")),
                    _id="loadform", _name="loadform")

    if loadForm.process(formname='loadform').accepted:
        # check that the presets file exists
        paramsFile = loadForm.vars['paramsFile']
        fullPath = 'diff_presets/{}.json'.format(paramsFile)
        if os.path.isfile(fullPath):
            # load it
            params = ParamsLoader.factory(fullPath).params
            session.paramsFile = paramsFile
            # params changed, no longer display the old result to avoid confusion
            session.result = None
            session.paramsDict = None
            redirect(URL(r=request, f='solver'))
        else:
            response.flash = "Presets file not found"

    # save form
    saveTable = TABLE(TR("Update an existing preset:",
                         SELECT(*presets, **dict(_name="paramsFile", value=session.paramsFile))),
                      TR("Create a new preset:",
                         INPUT(_type="text",
                               _name="saveFile",
                               requires=[IS_ALPHANUMERIC(error_message='Preset name must be alphanumeric and max 32 chars'),
                                         IS_LENGTH(32)])),
                      TR("Password:",
                         INPUT(_type="text",
                               _name="password",
                               requires=[IS_NOT_EMPTY(),
                                         IS_ALPHANUMERIC(error_message='Password must be alphanumeric and max 32 chars'), 
                                         IS_LENGTH(32)])))
    saveTable.append(TR(INPUT(_type="submit",_value="Save presets")))
    saveForm = FORM(saveTable, _id="saveform", _name="saveform")

    if saveForm.process(formname='saveform').accepted:
        # update or creation ?
        saveFile = saveForm.vars['saveFile']
        if saveFile == "":
            saveFile = saveForm.vars['paramsFile']

        # check if the presets file already exists
        password = saveForm.vars['password']
        password = password.encode('utf-8')
        passwordSHA256 = hashlib.sha256(password).hexdigest()
        fullPath = 'diff_presets/{}.json'.format(saveFile)
        if os.path.isfile(fullPath):
            # load it
            oldParams = ParamsLoader.factory(fullPath).params

            # check if password match
            if 'password' in oldParams and passwordSHA256 == oldParams['password']:
                # update the presets file
                paramsDict = generate_json_from_parameters(request.post_vars, hidden=True)
                paramsDict['password'] = passwordSHA256
                ParamsLoader.factory(paramsDict).dump(fullPath)
                session.paramsFile = saveFile
                redirect(URL(r=request, f='solver'))
            else:
                response.flash = "Password mismatch with existing presets file {}".format(saveFile)

        else:
            # write the presets file
            paramsDict = generate_json_from_parameters(request.post_vars, hidden=True)
            paramsDict['password'] = passwordSHA256
            ParamsLoader.factory(paramsDict).dump(fullPath)
            session.paramsFile = saveFile
            redirect(URL(r=request, f='solver'))

    # conf parameters
    conf = {}
    if 'difficultyTarget' in params['Conf']:
        conf["target"] = params['Conf']['difficultyTarget']
    else:
        conf["target"] = Conf.difficultyTarget
    if 'majorsPickup' in params['Conf']:
        conf["pickup"] = params['Conf']['majorsPickup']
    else:
        conf["pickup"] = Conf.majorsPickup

    # display result
    if session.result is not None:
        if session.result['difficulty'] == -1:
            resultText = "The rom \"{}\" is not finishable with the known technics".format(session.result['randomizedRom'])
        else:
            resultText = "The rom \"{}\" estimated difficulty is: ".format(session.result['randomizedRom'])

        difficulty = session.result['difficulty']
        diffPercent = session.result['diffPercent']

        # add generated path (spoiler !)
        pathTable = TABLE(TR(TH("Location Name"), TH("Area"), TH("Item"), TH("Difficulty"), TH("Techniques used")))
        for location, area, item, diff, techniques in session.result['generatedPath']:
            pathTable.append(TR(location, area, item, diff, techniques))

        knowsUsed = session.result['knowsUsed']

        # display the result only once
        session.result = None
    else:
        resultText = None
        difficulty = None
        diffPercent = None
        pathTable = None
        knowsUsed = None

    # set title
    response.title = 'Super Metroid Item Randomizer Solver'
    response.menu = [['Super Metroid Item Randomizer Solver', False, '#'],
                     ['Solve!', True, URL(f='solver')],
                     ['Information & Contact', False, URL(f='infos')]]

    # add missing knows
    for know in Knows.__dict__:
        if isKnows(know):
            if know not in params['Knows'].keys():
                params['Knows'][know] = Knows.__dict__[know]

    # send values to view
    return dict(mainForm=mainForm, loadForm=loadForm, saveForm=saveForm,
                desc=Knows.desc,
                difficulties=difficulties,
                categories=Knows.categories,
                knows=params['Knows'], conf=conf, knowsUsed=knowsUsed,
                resultText=resultText, pathTable=pathTable,
                difficulty=difficulty, diffPercent=diffPercent,
                easy=easy,medium=medium,hard=hard,harder=harder,hardcore=hardcore,mania=mania)

def generate_json_from_parameters(vars, hidden):
    if hidden is True:
        hidden = "_hidden"
    else:
        hidden = ""
    paramsDict = {'Conf': {}, 'Settings': {}, 'Knows': {}}
    for var in Knows.__dict__:
        # print("var={}".format(var))
        if isKnows(var):
            boolVar = vars[var+"_bool"+hidden]
            # print("{} = {}".format(var+"_bool"+hidden, boolVar))
            if boolVar is None:
                paramsDict['Knows'][var] = [False, 0]
            else:
                paramsDict['Knows'][var] = [True, difficulties2[vars[var+"_diff"+hidden]]]
            # print("{}: {}".format(var, paramsDict['Knows'][var]))

    diffTarget = vars["difficulty_target"+hidden]
    #print("diffTarget={}".format(diffTarget))
    if diffTarget is not None:
        paramsDict['Conf']['difficultyTarget'] = difficulties2[diffTarget]
        #print("paramsDict['Conf']['difficultyTarget']={}".format(paramsDict['Conf']['difficultyTarget']))

    pickupStrategy = vars["pickup_strategy"+hidden]
    if pickupStrategy is not None:
        if pickupStrategy == 'all':
            paramsDict['Conf']['majorsPickup'] = 'all'
            paramsDict['Conf']['minorsPickup'] = 'all'
        elif pickupStrategy == 'any':
            paramsDict['Conf']['majorsPickup'] = 'any'
            paramsDict['Conf']['minorsPickup'] = 'any'
        else:
            paramsDict['Conf']['majorsPickup'] = 'minimal'
            paramsDict['Conf']['minorsPickup'] = {'Missile' : 10, 'Super' : 5, 'PowerBomb' : 2}

    return paramsDict

def compute_difficulty(jsonRomFileName, post_vars):
    randomizedRom = os.path.basename(jsonRomFileName.replace('json', 'sfc'))

    # generate json from parameters
    paramsDict = generate_json_from_parameters(post_vars, hidden=False)
    session.paramsDict = paramsDict

    # call solver
    solver = Solver(type='web', rom=jsonRomFileName, params=[paramsDict])
    difficulty = solver.solveRom()
    diffPercent = DifficultyDisplayer(difficulty).percent()

    generatedPath = solver.getPath(solver.visitedLocations)

    # the different knows used during the rom
    knowsUsed = solver.getKnowsUsed()
    used = len(knowsUsed)

    # the number of knows set to True
    total = len([param for param in paramsDict['Knows'] if paramsDict['Knows'][param][0] is True])

    return dict(randomizedRom=randomizedRom, difficulty=difficulty,
                generatedPath=generatedPath, diffPercent=diffPercent,
                knowsUsed=(used, total))

def infos():
    # set title
    response.title = 'Super Metroid Item Randomizer Solver'
    response.menu = [['Super Metroid Item Randomizer Solver', False, '#'],
                     ['Solve!', False, URL(f='solver')],
                     ['Information & Contact', True, URL(f='infos')]]

    return dict()
