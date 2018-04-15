# -*- coding: utf-8 -*-

import sys, os.path
path = os.path.expanduser('~/RandomMetroidSolver')
if os.path.exists(path) and path not in sys.path:
    sys.path.append(path)

import datetime, os, hashlib, json, re, subprocess, tempfile
from collections import OrderedDict

# to solve the rom
from parameters import easy, medium, hard, harder, hardcore, mania, Conf, Knows, Settings, isKnows
from parameters import diff2text, text2diff
import tournament_locations
from solver import Solver, ParamsLoader, DifficultyDisplayer, RomLoader

romTypes = OrderedDict([('VARIA Classic', 'VARIA_X'), ('VARIA Full', 'VARIA_FX'),
                        ('Total Casual', 'Total_CX'), ('Total Normal', 'Total_X'),
                        ('Total Hard', 'Total_HX'), ('Total Tournament', 'Total_TX'),
                        ('Total Full', 'Total_FX'), ('Dessy Casual', 'Dessy'),
                        ('Dessy Speedrunner', 'Dessy'), ('Dessy Masochist', 'Dessy'),
                        ('Vanilla', 'Vanilla')])

def guessRomType(filename):
    match = re.findall(r'VARIA_Randomizer_[F]?X\d+', filename)
    if len(match) > 0:
        if match[0][18] == 'F':
            return "VARIA Full"
        elif match[0][18] == 'X':
            return "VARIA Classic"

    match = re.findall(r'[CTFH]?X\d+', filename)
    if len(match) > 0:
        if match[0][0] == 'C':
            return "Total Casual"
        elif match[0][0] == 'T':
            return "Total Tournament"
        elif match[0][0] == 'F':
            return "Total Full"
        elif match[0][0] == 'H':
            return "Total Hard"
        elif match[0][0] == 'X':
            return "Total Normal"

    match = re.findall(r'[CMS]?\d+', filename)
    if len(match) > 0:
        if match[0][0] == 'C':
            return "Dessy Casual"
        elif match[0][0] == 'M':
            return "Dessy Masochist"
        elif match[0][0] == 'S':
            return "Dessy Speedrunner"

    match = re.findall(r'Super[ _]*Metroid', filename)
    if len(match) > 0:
        return "Vanilla"

    # default to TX
    return "Total Tournament"

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
    if session.romFile is not None:
        romFile = session.romFile+'.sfc'
        romType = guessRomType(romFile)
    else:
        romFile = None
        romType = 'Total Tournament'

    mainForm = FORM(TABLE(TR("Randomized Super Metroid ROM: ",
                             INPUT(_type="file", _name="uploadFile", _id="uploadFile")),
                          TR("Already uploaded rom in this session: ",
                             SELECT(*roms, **dict(_name="romFile",
                                                  _id="romFile",
                                                  value=romFile,
                                                  _class="filldropdown",
                                                  _onchange="changeRomType()"))),
                          TR("ROM type: ", SELECT(*romTypes.keys(),
                                                  _name="romType",
                                                  _id="romType",
                                                  value=romType,
                                                  _class="filldropdown"))),
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
                romDict = {}
                for address in tempRomJson:
                    romDict[int(address)] = tempRomJson[address]

                romLoader = RomLoader.factory(romDict)
                romLoader.assignItems(tournament_locations.locations)
                romLoader.dump(jsonRomFileName)

                session.romFile = base
                if base not in session.romFiles:
                    session.romFiles.append(base)
            except Exception as e:
                print("Error loading the rom file {}, exception: {}".format(romFileName, e))
                session.flash = "Error loading the ROM file"
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
                session.flash = "Rom file must be .sfc or .smc"
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
                except Exception as e:
                    print("Error loading the rom file {}, exception: {}".format(uploadFileName, e))
                    session.flash = "Error loading the ROM file"
                    error = True

        elif len(mainForm.vars['romFile']) != 0:
            session.romFile = os.path.splitext(mainForm.vars['romFile'])[0]
            jsonRomFileName = 'roms/' + session.romFile + '.json'
        else:
            session.flash = "No rom file selected for upload"
            error = True

        if not error:
            # check that the json file exists
            if not os.path.isfile(jsonRomFileName):
                session.flash = "Missing json rom file on the server"
            else:
                session.result = compute_difficulty(jsonRomFileName, request.post_vars)

        redirect(URL(r=request, f='solver'))

    # load form
    files = sorted(os.listdir('diff_presets'))
    presets = [os.path.splitext(file)[0] for file in files]

    loadForm = FORM(TABLE(COLGROUP(COL(_class="quarter"), COL(_class="half"), COL(_class="quarter")),
                          TR("Load preset: ",
                             SELECT(*presets,
                                    **dict(_name="paramsFile",
                                           value=session.paramsFile,
                                           _onchange="this.form.submit()",
                                           _class="filldropdown")),
                             INPUT(_type="submit",_value="Load", _class="full")),
                          _class="threequarter"),
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
            session.flash = "Presets file not found"

    # save form
    saveTable = TABLE(COLGROUP(COL(_class="quarter"), COL(_class="half"), COL(_class="quarter")),
                      TR("Update preset:",
                         SELECT(*presets, **dict(_name="paramsFile",
                                                 value=session.paramsFile,
                                                 _class="filldropdown")),
                         INPUT(_type="button",_value="Update", _class="full", _onclick="askPassword()")),
                      TR("New preset:",
                         INPUT(_type="text",
                               _name="saveFile",
                               requires=[IS_ALPHANUMERIC(error_message='Preset name must be alphanumeric and max 32 chars'),
                                         IS_LENGTH(32)],
                               _class="full"),
                         INPUT(_type="button",_value="Create", _class="full", _onclick="askPassword()")),
                      TR(INPUT(_type="text",
                               _name="password", _id="password",
                               requires=[IS_NOT_EMPTY(),
                                         IS_ALPHANUMERIC(error_message='Password must be alphanumeric and max 32 chars'), 
                                         IS_LENGTH(32)],
                               _style='display:none')),
                      _class="threequarter")
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
                session.flash = "Preset {} updated".format(saveFile)
                redirect(URL(r=request, f='solver'))
            else:
                session.flash = "Password mismatch with existing presets file {}".format(saveFile)
                redirect(URL(r=request, f='solver'))

        else:
            # write the presets file
            paramsDict = generate_json_from_parameters(request.post_vars, hidden=True)
            paramsDict['password'] = passwordSHA256
            ParamsLoader.factory(paramsDict).dump(fullPath)
            session.paramsFile = saveFile
            session.flash = "Preset {} created".format(saveFile)
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
    if 'itemsForbidden' in params['Conf']:
        conf["itemsForbidden"] = params['Conf']['itemsForbidden']
    else:
        conf["itemsForbidden"] = []

    # display result
    if session.result is not None:
        if session.result['difficulty'] == -1:
            resultText = "The rom \"{}\" is not finishable with the known technics".format(session.result['randomizedRom'])
        else:
            if session.result['itemsOk'] is False:
                resultText = "The rom \"{}\" is finishable but not all the requested items can be picked up with the known technics. Estimated difficulty is: ".format(session.result['randomizedRom'])
            else:
                resultText = "The rom \"{}\" estimated difficulty is: ".format(session.result['randomizedRom'])

        difficulty = session.result['difficulty']
        diffPercent = session.result['diffPercent']

        # add generated path (spoiler !)
        pathTable = TABLE(TR(TH("Location Name"), TH("Area"), TH("Item"), TH("Difficulty"),
                             TH("Techniques used"), TH("Items used")))
        for location, area, item, diff, techniques, items in session.result['generatedPath']:
            # not picked up items start with an '-'
            if item[0] != '-':
                pathTable.append(TR(A(location[0],
                                      _href="https://wiki.supermetroid.run/{}".format(location[1].replace(' ', '_').replace("'", '%27'))),
                                      area, item, diff, techniques, items))
            else:
                pathTable.append(TR(A(location[0],
                                      _href="https://wiki.supermetroid.run/{}".format(location[1].replace(' ', '_').replace("'", '%27'))),
                                    area, DIV(item, _class='linethrough'),
                                    diff, techniques, items))

        knowsUsed = session.result['knowsUsed']
        itemsOk = session.result['itemsOk']

        # display the result only once
        session.result = None
    else:
        resultText = None
        difficulty = None
        diffPercent = None
        pathTable = None
        knowsUsed = None
        itemsOk = None

    # set title
    response.title = 'Super Metroid Item Randomizer Solver'

    # add missing knows
    for know in Knows.__dict__:
        if isKnows(know):
            if know not in params['Knows'].keys():
                params['Knows'][know] = Knows.__dict__[know]

    # add missing settings
    for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
        if boss not in params['Settings']['bossesDifficulty']:
            params['Settings']['bossesDifficulty'][boss] = Settings.bossesDifficulty[boss]
        if boss not in params['Settings']:
            params['Settings'][boss] = 'Default'
    for hellrun in ['Ice', 'MainUpperNorfair', 'LowerNorfair']:
        if hellrun not in params['Settings']['hellRuns']:
            params['Settings']['hellRuns'][hellrun] = Settings.hellRuns[hellrun]
        if hellrun not in params['Settings']:
            params['Settings'][hellrun] = 'Default'

    # send values to view
    return dict(mainForm=mainForm, loadForm=loadForm, saveForm=saveForm,
                desc=Knows.desc,
                difficulties=diff2text,
                categories=Knows.categories, settings=params['Settings'],
                knows=params['Knows'], conf=conf, knowsUsed=knowsUsed,
                resultText=resultText, pathTable=pathTable,
                difficulty=difficulty, itemsOk=itemsOk, diffPercent=diffPercent,
                easy=easy,medium=medium,hard=hard,harder=harder,hardcore=hardcore,mania=mania)

def generate_json_from_parameters(vars, hidden):
    if hidden is True:
        hidden = "_hidden"
    else:
        hidden = ""

    paramsDict = {'Knows': {}, 'Conf': {}, 'Settings': {'hellRuns': {}, 'bossesDifficulty': {}}}

    # Knows
    for var in Knows.__dict__:
        if isKnows(var):
            boolVar = vars[var+"_bool"+hidden]
            if boolVar is None:
                paramsDict['Knows'][var] = [False, 0]
            else:
                diffVar = vars[var+"_diff"+hidden]
                if diffVar is not None:
                    paramsDict['Knows'][var] = [True, text2diff[diffVar]]

    # Conf
    diffTarget = vars["difficulty_target"+hidden]
    if diffTarget is not None:
        paramsDict['Conf']['difficultyTarget'] = text2diff[diffTarget]

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

    itemsForbidden = []
    for item in ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
        boolvar = vars[item+"_bool"+hidden]
        if boolvar is not None:
            itemsForbidden.append(item)

    paramsDict['Conf']['itemsForbidden'] = itemsForbidden

    if vars['romType'] is not None:
        paramsDict['Conf']['romType'] = romTypes[vars['romType']]

    # Settings
    for hellRun in ['Ice', 'MainUpperNorfair', 'LowerNorfair']:
        value = vars[hellRun+hidden]
        if value is not None:
            paramsDict['Settings']['hellRuns'][hellRun] = Settings.hellRunPresets[hellRun][value]
            paramsDict['Settings'][hellRun] = value

    for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
        value = vars[boss+hidden]
        if value is not None:
            paramsDict['Settings']['bossesDifficulty'][boss] = Settings.bossesDifficultyPresets[boss][value]
            paramsDict['Settings'][boss] = value

    return paramsDict

def compute_difficulty(jsonRomFileName, post_vars):
    randomizedRom = os.path.basename(jsonRomFileName.replace('json', 'sfc'))

    # generate json from parameters
    paramsDict = generate_json_from_parameters(post_vars, hidden=False)
    session.paramsDict = paramsDict

    # call solver
    solver = Solver(type='web', rom=jsonRomFileName, params=[paramsDict])
    (difficulty, itemsOk) = solver.solveRom()
    diffPercent = DifficultyDisplayer(difficulty).percent()

    generatedPath = solver.getPath(solver.visitedLocations)

    # the different knows used during the rom
    knowsUsed = solver.getKnowsUsed()
    used = len(knowsUsed)

    # the number of knows set to True
    total = len([param for param in paramsDict['Knows'] if paramsDict['Knows'][param][0] is True])
    if 'hellRuns' in paramsDict['Settings']:
        total += len([hellRun for hellRun in paramsDict['Settings']['hellRuns'] if paramsDict['Settings']['hellRuns'][hellRun] is not None])

    return dict(randomizedRom=randomizedRom, difficulty=difficulty,
                generatedPath=generatedPath, diffPercent=diffPercent,
                knowsUsed=(used, total), itemsOk=itemsOk)

def infos():
    # set title
    response.title = 'Super Metroid Item Randomizer Solver'

    return dict()

patches = [
    ("Removes_Gravity_Suit_heat_protection", "Remove gravity suit heat protection (by Total)"),
    ('skip_intro', "Skip text intro (start at Ceres Station) (by Smiley)"),
    ('skip_ceres', "Skip text intro and Ceres station (start at Landing Site) (by Total)"),
    ('AimAnyButton', "Allows the aim buttons to be assigned to any button (by Kejardon)"),
    ('itemsounds', "Remove fanfare when picking up an item (by Scyzer)"),
    ('spinjumprestart', "Allows Samus to start spinning in mid air after jumping or falling (by Kejardon)"),
    ('elevators_doors_speed', 'Accelerate doors and elevators transitions (by Rakki & Lioran)'),
    ('supermetroid_msu1', "Play music with MSU1 chip on SD2SNES (by DarkShock)"),
    ('max_ammo_display', "Max Ammo Display (by Personitis) (incompatible with MSU1 patch)"),
    ('animals', "Save the animals surprise (by Foosda)")
]

def randomizer():
    response.title = 'Super Metroid VARIA Randomizer'

    if session.randomizer is None:
        session.randomizer = {}

        session.randomizer['maxDifficulty'] = 'hard'
        session.randomizer['paramsFile'] = 'regular'
        for patch in patches:
            session.randomizer[patch[0]] = "on"
        session.randomizer['supermetroid_msu1'] = "off"
        session.randomizer['spinjumprestart'] = "off"
        session.randomizer['skip_intro'] = "off"
        session.randomizer['animals'] = "off"
        session.randomizer['missileQty'] = "3"
        session.randomizer['superQty'] = "3"
        session.randomizer['powerBombQty'] = "1"
        session.randomizer['minorQty'] = "100"
        session.randomizer['energyQty'] = "vanilla"
        session.randomizer['useMaxDiff'] = "off"
        session.randomizer['progressionSpeed'] = "medium"
        session.randomizer['spreadItems'] = "on"
        session.randomizer['fullRandomization'] = "off"
        session.randomizer['suitsRestriction'] = "on"
        session.randomizer['speedScrewRestriction'] = "on"
        session.randomizer['funCombat'] = "off"
        session.randomizer['funMovement'] = "off"
        session.randomizer['funSuits'] = "off"
        session.randomizer['layoutPatches'] = "on"

    # put standard presets first
    stdPresets = ['noob', 'regular', 'veteran', 'speedrunner']
    files = sorted(os.listdir('diff_presets'))
    presets = [os.path.splitext(file)[0] for file in files]
    for preset in stdPresets:
        presets.remove(preset)
    presets = stdPresets + presets

    return dict(presets=presets, patches=patches)

def raiseHttp(code, msg, isJson=False):
    print("raiseHttp: code {} msg {} isJson {}".format(code, msg, isJson))
    if isJson is True:
        msg = json.dumps(msg)

    raise HTTP(code, msg)

def validateWebServiceParams(patchs, quantities, others, isJson=False):
    parameters = patchs + quantities + others

    for param in parameters:
        if request.vars[param] is None:
            raiseHttp(400, "Missing parameter: {}".format(param), isJson)

    for patch in patchs:
        if request.vars[patch] not in ['on', 'off']:
            raiseHttp(400, "Wrong value for {}: {}, authorized values: on/off".format(patch, request.vars[patch]), isJson)

    if request.vars['skip_intro'] == request.vars['skip_ceres']:
        raiseHttp(400, "You must choose one and only one patch for skipping the intro/Ceres station")

    def getInt(param):
        try:
            return int(request.vars[param])
        except:
            raiseHttp(400, "Wrong value for {}: {}, must be an int".format(param, request.vars[param]), isJson)

    for qty in quantities:
        qtyInt = getInt(qty)
        if qtyInt not in range(1, 10):
            raiseHttp(400, json.dumps("Wrong value for {}: {}, must be between 1 and 9".format(qty, request.vars[qty])), isJson)

    if 'seed' in others:
        seedInt = getInt('seed')
        if seedInt < 0 or seedInt > 9999999:
            raiseHttp(400, "Wrong value for seed: {}, must be between 0 and 9999999".format(request.vars[seed]), isJson)

    if request.vars['maxDifficulty'] is not None:
        if request.vars.maxDifficulty not in ['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania']:
            raiseHttp(400, "Wrong value for difficulty_target, authorized values: easy/medium/hard/harder/hardcore/mania", isJson)

    if IS_ALPHANUMERIC()(request.vars.paramsFile)[1] is not None:
        raiseHttp(400, "Wrong value for paramsFile, must be alphanumeric", isJson)

    if IS_LENGTH(maxsize=32, minsize=1)(request.vars.paramsFile)[1] is not None:
        raiseHttp(400, "Wrong length for paramsFile, name must be between 1 and 32 characters", isJson)

    minorQtyInt = getInt('minorQty')
    if minorQtyInt < 1 or minorQtyInt > 100:
        raiseHttp(400, "Wrong value for minorQty, must be between 1 and 100", isJson)

    if 'energyQty' in others:
        if request.vars.energyQty not in ['sparse', 'medium', 'vanilla']:
            raiseHttp(400, "Wrong value for energyQty: authorized values: sparse/medium/vanilla", isJson)

    if 'paramsFileTarget' in others:
        try:
            json.loads(request.vars.paramsFileTarget)
        except:
            raiseHttp(400, "Wrong value for paramsFileTarget, must be a JSON string", isJson)

    for check in ['useMaxDiff', 'spreadItems', 'fullRandomization', 'suitsRestriction', 'speedScrewRestriction', 'layoutPatches']:
        if check in others:
            if request.vars[check] not in ['on', 'off']:
                raiseHttp(400, "Wrong value for {}: {}, authorized values: on/off".format(check, request.vars[check]), isJson)

    if 'progressionSpeed' in others:
        if request.vars['progressionSpeed'] not in ['random', 'slowest', 'slow', 'medium', 'fast', 'fastest']:
            raiseHttp(400, "Wrong value for progressionSpeed: {}, authorized values random/slowest/slow/medium/fast/fastest".format(request.vars['progressionSpeed']), isJson)

def sessionWebService():
    # web service to update the session
    patchs = ['Removes_Gravity_Suit_heat_protection', 'AimAnyButton', 'itemsounds',
              'spinjumprestart', 'supermetroid_msu1', 'max_ammo_display', 'elevators_doors_speed',
              'skip_intro', 'skip_ceres', 'animals']
    quantities = ['missileQty', 'superQty', 'powerBombQty']
    others = ['paramsFile', 'minorQty', 'energyQty', 'useMaxDiff', 'maxDifficulty',
              'progressionSpeed', 'spreadItems', 'fullRandomization', 'suitsRestriction',
              'speedScrewRestriction', 'funCombat', 'funMovement', 'funSuits', 'layoutPatches']
    validateWebServiceParams(patchs, quantities, others)

    if session.randomizer is None:
        session.randomizer = {}

    session.randomizer['maxDifficulty'] = request.vars.maxDifficulty
    session.randomizer['paramsFile'] = request.vars.paramsFile
    for patch in patches:
        session.randomizer[patch[0]] = request.vars[patch[0]]
    session.randomizer['missileQty'] = request.vars.missileQty
    session.randomizer['superQty'] = request.vars.superQty
    session.randomizer['powerBombQty'] = request.vars.powerBombQty
    session.randomizer['minorQty'] = request.vars.minorQty
    session.randomizer['energyQty'] = request.vars.energyQty
    session.randomizer['useMaxDiff'] = request.vars.useMaxDiff
    session.randomizer['progressionSpeed'] = request.vars.progressionSpeed
    session.randomizer['spreadItems'] = request.vars.spreadItems
    session.randomizer['fullRandomization'] = request.vars.fullRandomization
    session.randomizer['suitsRestriction'] = request.vars.suitsRestriction
    session.randomizer['speedScrewRestriction'] = request.vars.speedScrewRestriction
    session.randomizer['funCombat'] = request.vars.funCombat
    session.randomizer['funMovement'] = request.vars.funMovement
    session.randomizer['funSuits'] = request.vars.funSuits
    session.randomizer['layoutPatches'] = request.vars.layoutPatches

def randomizerWebService():
    # web service to compute a new random (returns json string)
    print("randomizerWebService")

    # set header to authorize cross domain AJAX
    response.headers['Access-Control-Allow-Origin'] = '*'

    # check validity of all parameters
    patchs = ['Removes_Gravity_Suit_heat_protection', 'AimAnyButton', 'itemsounds',
              'spinjumprestart', 'supermetroid_msu1', 'max_ammo_display', 'elevators_doors_speed',
              'skip_intro', 'skip_ceres']
    quantities = ['missileQty', 'superQty', 'powerBombQty']
    others = ['seed', 'paramsFile', 'paramsFileTarget', 'minorQty', 'energyQty', 'useMaxDiff',
              'maxDifficulty', 'progressionSpeed', 'spreadItems', 'fullRandomization',
              'suitsRestriction', 'speedScrewRestriction', 'funCombat', 'funMovement', 'funSuits',
              'layoutPatches']
    validateWebServiceParams(patchs, quantities, others, isJson=True)

    # randomize
    presetFileName = tempfile.mkstemp()[1] + '.json'
    jsonFileName = tempfile.mkstemp()[1]

    print("randomizerWebService, params validated")
    for var in request.vars:
        print("{}: {}".format(var, request.vars[var]))

    with open(presetFileName, 'w') as presetFile:
        presetFile.write(request.vars.paramsFileTarget)

    params = ['python2',  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
              '--seed', request.vars.seed,
              '--output', jsonFileName, '--param', presetFileName,
              '--preset', request.vars.paramsFile,
              '--missileQty', request.vars.missileQty,
              '--superQty', request.vars.superQty,
              '--powerBombQty', request.vars.powerBombQty,
              '--minorQty', request.vars.minorQty,
              '--energyQty', request.vars.energyQty,
              '--progressionSpeed', request.vars.progressionSpeed]
    for patch in patches:
        if request.vars[patch[0]] == 'on':
            if patch[0] == 'animals':
                continue
            params.append('-c')
            if patch[0] != 'Removes_Gravity_Suit_heat_protection':
                params.append(patch[0] + '.ips')
            else:
                params.append(patch[0])
    if request.vars.animals == 'on':
        params.append('--animals')
    if request.vars.useMaxDiff == 'on':
        params.append('--maxDifficulty')
        params.append(request.vars.maxDifficulty)
    if request.vars.spreadItems == 'on':
        params.append('--spreadItems')
    if request.vars.fullRandomization == 'on':
        params.append('--fullRandomization')
    if request.vars.suitsRestriction == 'on':
        params.append('--suitsRestriction')
    if request.vars.speedScrewRestriction == 'on':
        params.append('--speedScrewRestriction')
    if request.vars.funCombat == 'on':
        params.append('--superFun')
        params.append('Combat')
    if request.vars.funMovement == 'on':
        params.append('--superFun')
        params.append('Movement')
    if request.vars.funSuits == 'on':
        params.append('--superFun')
        params.append('Suits')
    if request.vars.layoutPatches == 'off':
        params.append('--nolayout')

    ret = subprocess.call(params)

    if ret == 0:
        with open(jsonFileName) as jsonFile:
            locsItems = json.load(jsonFile)

        os.remove(jsonFileName)
        os.remove(presetFileName)
        return json.dumps(locsItems)
    else:
        os.remove(jsonFileName)
        os.remove(presetFileName)
        raise HTTP(400, json.dumps("randomizerWebService: something wrong happened"))

def presetWebService():
    # web service to get the content of the preset file
    if request.vars.paramsFile is None:
        raise HTTP(400, "Missing paramsFile parameter")

    paramsFile = request.vars.paramsFile

    if IS_ALPHANUMERIC()(paramsFile)[1] is not None:
        raise HTTP(400, "Preset name must be alphanumeric")

    if IS_LENGTH(maxsize=32, minsize=1)(paramsFile)[1] is not None:
        raise HTTP(400, "Preset name must be between 1 and 32 characters")

    print("presetWebService: paramsFile={}".format(paramsFile))

    fullPath = 'diff_presets/{}.json'.format(paramsFile)

    # check that the presets file exists
    if os.path.isfile(fullPath):
        # load it
        params = ParamsLoader.factory(fullPath).params
        params = json.dumps(params)
        return params
    else:
        raise HTTP(400, "Preset not found")
