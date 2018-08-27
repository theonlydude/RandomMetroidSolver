# -*- coding: utf-8 -*-

import sys, os.path
path = os.path.expanduser('~/RandomMetroidSolver')
if os.path.exists(path) and path not in sys.path:
    sys.path.append(path)

import datetime, os, hashlib, json, subprocess, tempfile, glob, random
from datetime import datetime
from collections import OrderedDict

# to solve the rom
from parameters import easy, medium, hard, harder, hardcore, mania
from parameters import Knows, Settings, Controller, isKnows, isButton
from solver import Conf
from parameters import diff2text, text2diff
from graph_locations import locations as graphLocations
from solver import Solver, DifficultyDisplayer
from rom import RomLoader
from utils import PresetLoader
import db

def maxPresetsReach():
    # to prevent a spammer to create presets in a loop and fill the fs
    return len(os.listdir('community_presets')) >= 2048

def isStdPreset(preset):
    return preset in ['noob', 'casual', 'regular', 'veteran', 'speedrunner', 'master', 'samus', 'solution']

def getPresetDir(preset):
    if isStdPreset(preset):
        return 'standard_presets'
    else:
        return 'community_presets'

def loadPreset():
    # load conf from session if available
    loaded = False
    if session.presets['preset'] is None:
        # default preset
        session.presets['preset'] = 'regular'

    if request.vars.action is not None:
        # press solve, load or save button
        if request.vars.action in ['Update', 'Create']:
            # store the changes in case the form won't be accepted
            presetDict = genJsonFromParams(request.vars)
            session.presets['presetDict'] = presetDict
            params = PresetLoader.factory(presetDict).params
            loaded = True
        elif request.vars.action in ['Load']:
            # nothing to load, we'll load the new params file with the load form code
            pass
    else:
        # no forms button pressed
        if session.presets['presetDict'] is not None:
            params = PresetLoader.factory(session.presets['presetDict']).params
            loaded = True

    if not loaded:
        params = PresetLoader.factory('{}/{}.json'.format(getPresetDir(session.presets['preset']), session.presets['preset'])).params

    return params

def loadPresetsList():
    files = sorted(os.listdir('community_presets'), key=lambda v: v.upper())
    stdPresets = ['noob', 'casual', 'regular', 'veteran', 'speedrunner', 'master', 'samus']
    comPresets = [os.path.splitext(file)[0] for file in files]
    return stdPresets + comPresets

def validatePresetsParams(action):
    if action == 'Create':
        if IS_NOT_EMPTY()(request.vars.password)[1] is not None:
            return (False, "Password is empty")
        if IS_ALPHANUMERIC()(request.vars.password)[1] is not None:
            return (False, "Password must be alphanumeric")
        if IS_LENGTH(32)(request.vars.password)[1] is not None:
            return (False, "Password must be max 32 chars")
        if IS_NOT_EMPTY()(request.vars.presetCreate)[1] is not None:
            return (False, "Preset name is empty")
        if IS_ALPHANUMERIC()(request.vars.presetCreate)[1] is not None:
            return (False, "Preset name must be alphanumeric")
        if IS_LENGTH(32)(request.vars.presetCreate)[1] is not None:
            return (False, "Preset name must be max 32 chars")
    elif action == 'Update':
        if IS_ALPHANUMERIC()(request.vars.presetUpdate)[1] is not None:
            return (False, "Preset name must be alphanumeric")
        if IS_LENGTH(32)(request.vars.presetUpdate)[1] is not None:
            return (False, "Preset name must be max 32 chars")
    elif action == 'Load':
        if IS_ALPHANUMERIC()(request.vars.presetLoad)[1] is not None:
            return (False, "Preset name must be alphanumeric")
        if IS_LENGTH(32)(request.vars.presetLoad)[1] is not None:
            return (False, "Preset name must be max 32 chars")

    if action in ['Create', 'Update']:
        # check that there's not two buttons for the same action
        map = {}
        for button in Controller.__dict__:
            if isButton(button):
                value = request.vars[button]
                if value is None:
                    return (False, "Button {} not set".format(button))
                else:
                    if value in map:
                        return (False, "Action {} set for two buttons: {} and {}".format(value, button, map[value]))
                    map[value] = button

    if request.vars.currenttab not in ['Global', 'Techniques1', 'Techniques2', 'Techniques3', 'Techniques4', 'Techniques5', 'Techniques6', 'Techniques7', 'Mapping']:
        return (False, "Wrong value for current tab: [{}]".format(request.vars.currenttab))

    return (True, None)

def initPresetsSession():
    if session.presets is None:
        session.presets = {}

        session.presets['preset'] = 'regular'
        session.presets['presetDict'] = None
        session.presets['currentTab'] = 'Global'

def presets():
    initPresetsSession()

    if request.vars.action is not None:
        (ok, msg) = validatePresetsParams(request.vars.action)
        if not ok:
            session.flash = msg
            redirect(URL(r=request, f='presets'))
        else:
            session.presets['currentTab'] = request.vars.currenttab

    # in web2py.js, in disableElement, remove 'working...' to have action with correct value
    if request.vars.action == 'Load':
        # check that the presets file exists
        presetName = request.vars['presetLoad']
        fullPath = '{}/{}.json'.format(getPresetDir(presetName), presetName)
        if os.path.isfile(fullPath):
            # load it
            try:
                params = PresetLoader.factory(fullPath).params
                session.presets['preset'] = presetName
                session.presets["presetDict"] = None
            except Exception as e:
                session.flash = "Error loading the preset {}: {}".format(presetName, e)
        else:
            session.flash = "Presets file not found"
        redirect(URL(r=request, f='presets'))

    elif request.vars.action in ['Update', 'Create']:
        # update or creation ?
        if request.vars.action == 'Create':
            preset = request.vars['presetCreate']
        else:
            preset = request.vars['presetUpdate']

        # check if the presets file already exists
        password = request.vars['password']
        password = password.encode('utf-8')
        passwordSHA256 = hashlib.sha256(password).hexdigest()
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if os.path.isfile(fullPath):
            # load it
            try:
                oldParams = PresetLoader.factory(fullPath).params
            except Exception as e:
                session.flash = "Error loading the preset {}: {}".format(preset, e)
                redirect(URL(r=request, f='presets'))

            # check if password match
            if 'password' in oldParams and passwordSHA256 == oldParams['password']:
                # update the presets file
                paramsDict = genJsonFromParams(request.vars)
                paramsDict['password'] = passwordSHA256
                try:
                    PresetLoader.factory(paramsDict).dump(fullPath)
                    session.presets["preset"] = preset
                    session.flash = "Preset {} updated".format(preset)
                    redirect(URL(r=request, f='presets'))
                except Exception as e:
                    session.flash = "Error writing the preset {}: {}".format(preset, e)
                    redirect(URL(r=request, f='presets'))
            else:
                session.flash = "Password mismatch with existing presets file {}".format(preset)
                redirect(URL(r=request, f='presets'))

        else:
            # check that there's no more than 2K presets (there's less than 2K sm rando players in the world)
            if not maxPresetsReach():
                # write the presets file
                paramsDict = genJsonFromParams(request.vars)
                paramsDict['password'] = passwordSHA256
                try:
                    PresetLoader.factory(paramsDict).dump(fullPath)
                    session.presets["preset"] = preset
                    session.flash = "Preset {} created".format(preset)
                    redirect(URL(r=request, f='presets'))
                except Exception as e:
                    session.flash = "Error writing the preset {}: {}".format(preset, e)
                    redirect(URL(r=request, f='presets'))
            else:
                session.flash = "Sorry, there's already 2048 presets on the website, can't add more"
                redirect(URL(r=request, f='presets'))

    # set title
    response.title = 'Super Metroid VARIA Presets'

    # load conf from session if available
    try:
        params = loadPreset()
    except Exception as e:
        session.presets['preset'] = 'regular'
        session.flash = "Error loading the preset: {}".format(e)
        redirect(URL(r=request, f='presets'))

    # load presets list
    presets = loadPresetsList()

    # add missing knows
    for know in Knows.__dict__:
        if isKnows(know):
            if know not in params['Knows'].keys():
                params['Knows'][know] = Knows.__dict__[know]

    # add missing settings
    for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
        if boss not in params['Settings']:
            params['Settings'][boss] = 'Default'
    for hellrun in ['Ice', 'MainUpperNorfair', 'LowerNorfair']:
        if hellrun not in params['Settings']:
            params['Settings'][hellrun] = 'Default'
    for hardroom in ['X-Ray', 'Gauntlet']:
        if hardroom not in params['Settings']:
            params['Settings'][hardroom] = 'Default'

    # add missing controller buttons
    for button in Controller.__dict__:
        if isButton(button):
            if button not in params['Controller'].keys():
                params['Controller'][button] = Controller.__dict__[button]

    # send values to view
    return dict(desc=Knows.desc, difficulties=diff2text,
                categories=Knows.categories, settings=params['Settings'], knows=params['Knows'],
                easy=easy, medium=medium, hard=hard, harder=harder, hardcore=hardcore, mania=mania,
                controller=params['Controller'], presets=presets)

def initSolverSession():
    if session.solver is None:
        session.solver = {}

        session.solver['preset'] = 'regular'
        session.solver['difficultyTarget'] = Conf.difficultyTarget
        session.solver['pickupStrategy'] = Conf.itemsPickup
        session.solver['itemsForbidden'] = []
        session.solver['romFiles'] = []
        session.solver['romFile'] = None
        session.solver['result'] = None
        session.solver['complexity'] = 'simple'

def updateSolverSession():
    if session.solver is None:
        session.solver = {}

    session.solver['preset'] = request.vars.preset
    session.solver['difficultyTarget'] = text2diff[request.vars.difficultyTarget]
    session.solver['pickupStrategy'] = request.vars.pickupStrategy
    session.solver['complexity'] = request.vars.complexity

    itemsForbidden = []
    for item in ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
        boolvar = request.vars[item+"_bool"]
        if boolvar is not None:
            itemsForbidden.append(item)

    session.solver['itemsForbidden'] = itemsForbidden

def getROMsList():
    # filter the displayed roms to display only the ones uploaded in this session
    if session.solver['romFiles'] is None:
        session.solver['romFiles'] = []
        roms = []
    elif len(session.solver['romFiles']) == 0:
        roms = []
    else:
        files = sorted(os.listdir('roms'))
        bases = [os.path.splitext(file)[0] for file in files]
        filtered = [base for base in bases if base in session.solver['romFiles']]
        roms = [file+'.sfc' for file in filtered]

    return roms

def getLastSolvedROM():
    if session.solver['romFile'] is not None:
        return session.solver['romFile'] + '.sfc'
    else:
        return None

def genPathTable(locations, displayAPs=True):
    if locations is None or len(locations) == 0:
        return None

    lastAP = None
    pathTable = TABLE(COLGROUP(COL(_class="locName"), COL(_class="area"), COL(_class="subarea"), COL(_class="item"),
                               COL(_class="difficulty"), COL(_class="knowsUsed"), COL(_class="itemsUsed")),
                      TR(TH("Location Name"), TH("Area"), TH("SubArea"), TH("Item"),
                         TH("Difficulty"), TH("Techniques used"), TH("Items used")),
                      _class="full")
    for location, area, subarea, item, diff, techniques, items, path in locations:
        if path is not None:
            lastAP = path[-1]
            if displayAPs == True and not (len(path) == 1 and path[0] == lastAP):
                pathTable.append(TR(TD("Path"),
                                    TD(" -> ".join(path), _colspan="6"),
                                    _class="grey"))

        # not picked up items start with an '-'
        if item[0] != '-':
            pathTable.append(TR(A(location[0],
                                  _href="https://wiki.supermetroid.run/{}".format(location[1].replace(' ', '_').replace("'", '%27'))),
                                  area, subarea, item, diff, techniques, items, _class=item))
        else:
            pathTable.append(TR(A(location[0],
                                  _href="https://wiki.supermetroid.run/{}".format(location[1].replace(' ', '_').replace("'", '%27'))),
                                area, subarea, DIV(item, _class='linethrough'),
                                diff, techniques, items, _class=item))

    return pathTable

def prepareResult():
    if session.solver['result'] is not None:
        result = session.solver['result']

        if session.solver['result']['difficulty'] == -1:
            result['resultText'] = "The ROM \"{}\" is not finishable with the known techniques".format(session.solver['result']['randomizedRom'])
        else:
            if session.solver['result']['itemsOk'] is False:
                result['resultText'] = "The ROM \"{}\" is finishable but not all the requested items can be picked up with the known techniques. Estimated difficulty is: ".format(session.solver['result']['randomizedRom'])
            else:
                result['resultText'] = "The ROM \"{}\" estimated difficulty is: ".format(session.solver['result']['randomizedRom'])

        # add generated path (spoiler !)
        result['pathTable'] = genPathTable(session.solver['result']['generatedPath'])
        result['pathremainTry'] = genPathTable(session.solver['result']['remainTry'])
        result['pathremainMajors'] = genPathTable(session.solver['result']['remainMajors'], False)
        result['pathremainMinors'] = genPathTable(session.solver['result']['remainMinors'], False)
        result['pathskippedMajors'] = genPathTable(session.solver['result']['skippedMajors'], False)
        result['pathunavailMajors'] = genPathTable(session.solver['result']['unavailMajors'], False)

        # display the result only once
        session.solver['result'] = None
    else:
        result = None

    return result

def validateSolverParams():
    for param in ['preset', 'difficultyTarget', 'pickupStrategy', 'complexity']:
        if request.vars[param] is None:
            return (False, "Missing parameter {}".format(param))

    session.solver['preset'] = request.vars.preset

    difficultyTargetChoices = ["easy", "medium", "hard", "very hard", "hardcore", "mania"]
    if request.vars.difficultyTarget not in difficultyTargetChoices:
        return (False, "Wrong value for difficultyTarget: {}, authorized values: {}".format(request.vars.difficultyTarget, difficultyTargetChoices))

    pickupStrategyChoices = ["all", "minimal", "any"]
    if request.vars.pickupStrategy not in pickupStrategyChoices:
        return (False, "Wrong value for pickupStrategy: {}, authorized values: {}".format(request.vars.pickupStrategy, pickupStrategyChoice))

    complexityChoices = ["simple", "advanced"]
    if request.vars.complexity not in complexityChoices:
        return (False, "Wrong value for complexity: {}, authorized values: {}".format(request.vars.complexity, complexityChoices))

    itemsForbidden = []
    for item in ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
        boolvar = request.vars[item+"_bool"]
        if boolvar is not None:
            if boolvar != 'on':
                return (False, "Wrong value for {}: {}, authorized values: on/off".format(item, boolvar))

    if request.vars.romJson is None and request.vars.uploadFile is None and request.vars.romFile is None:
        return (False, "Missing ROM to solve")


    if request.vars.romFile is not None:
        if IS_MATCH('[a-zA-Z0-9_\.]*')(request.vars.romFile)[1] is not None:
            return (False, "Wrong value for romFile, must be valid file name: {}".format(request.vars.romFile))

        if IS_LENGTH(maxsize=256, minsize=1)(request.vars.romFile)[1] is not None:
            return (False, "Wrong length for romFile, name must be between 1 and 256 characters: {}".format(request.vars.romFile))

    if request.vars.romJson is not None and len(request.vars.romJson) > 0:
        try:
            json.loads(request.vars.romJson)
        except:
            return (False, "Wrong value for romJson, must be a JSON string: [{}]".format(request.vars.romJson))

    if request.vars.uploadFile is not None:
        if type(request.vars.uploadFile) == str:
            if IS_MATCH('[a-zA-Z0-9_\.]*')(request.vars.uploadFile)[1] is not None:
                return (False, "Wrong value for uploadFile, must be a valid file name: {}".format(request.vars.uploadFile))

            if IS_LENGTH(maxsize=256, minsize=1)(request.vars.uploadFile)[1] is not None:
                return (False, "Wrong length for uploadFile, name must be between 1 and 256 characters: {}".format(request.vars.uploadFile))
        else:
            # the file uploaded. TODO: how to check it ?
            pass

    return (True, None)

def solver():
    # init session
    initSolverSession()

    ROMs = getROMsList()

    # last solved ROM
    lastRomFile = getLastSolvedROM()

    # load presets list
    presets = loadPresetsList()

    if request.vars.action == 'Solve':
        (ok, msg) = validateSolverParams()
        if not ok:
            session.flash = msg
            redirect(URL(r=request, f='solver'))

        updateSolverSession()

        # new uploaded rom ?
        error = False
        if request.vars['romJson'] != '':
            try:
                tempRomJson = json.loads(request.vars['romJson'])
                romFileName = tempRomJson["romFileName"]
                (base, ext) = os.path.splitext(romFileName)
                jsonRomFileName = 'roms/' + base + '.json'
                del tempRomJson["romFileName"]

                # json keys are strings
                romDict = {}
                for address in tempRomJson:
                    romDict[int(address)] = tempRomJson[address]

                romLoader = RomLoader.factory(romDict)
                romLoader.assignItems(graphLocations)
                romLoader.dump(jsonRomFileName)

                session.solver['romFile'] = base
                if base not in session.solver['romFiles']:
                    session.solver['romFiles'].append(base)
            except Exception as e:
                print("Error loading the ROM file {}, exception: {}".format(romFileName, e))
                session.flash = "Error loading the json ROM file"
                error = True

        # no file: type(request.vars['uploadFile'])=[<type 'str'>]
        # file:    type(request.vars['uploadFile'])=[<type 'instance'>]
        elif request.vars['uploadFile'] is not None and type(request.vars['uploadFile']) != str:
            uploadFileName = request.vars['uploadFile'].filename
            uploadFileContent = request.vars['uploadFile'].file

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
                    romLoader.assignItems(graphLocations)
                    romLoader.dump(jsonRomFileName)

                    os.remove(tempRomFile)

                    session.solver['romFile'] = base
                    if base not in session.solver['romFiles']:
                        session.solver['romFiles'].append(base)
                except Exception as e:
                    print("Error loading the ROM file {}, exception: {}".format(uploadFileName, e))
                    session.flash = "Error loading the ROM file"
                    error = True

        elif request.vars['romFile'] is not None and len(request.vars['romFile']) != 0:
            session.solver['romFile'] = os.path.splitext(request.vars['romFile'])[0]
            jsonRomFileName = 'roms/' + session.solver['romFile'] + '.json'
        else:
            session.flash = "No rom file selected for upload"
            error = True

        if not error:
            # check that the json file exists
            if not os.path.isfile(jsonRomFileName):
                session.flash = "Missing json ROM file on the server"
            else:
                (ok, result) = computeDifficulty(jsonRomFileName)
                if not ok:
                    session.flash = result
                    redirect(URL(r=request, f='solver'))
                session.solver['result'] = result

        redirect(URL(r=request, f='solver'))

    # display result
    result = prepareResult()

    # set title
    response.title = 'Super Metroid VARIA Solver'

    # send values to view
    return dict(desc=Knows.desc, presets=presets, roms=ROMs, lastRomFile=lastRomFile,
                difficulties=diff2text, categories=Knows.categories,
                result=result,
                easy=easy, medium=medium, hard=hard, harder=harder, hardcore=hardcore, mania=mania)

def genJsonFromParams(vars):
    paramsDict = {'Knows': {}, 'Settings': {}, 'Controller': {}}

    # Knows
    for var in Knows.__dict__:
        if isKnows(var):
            boolVar = vars[var+"_bool"]
            if boolVar is None:
                paramsDict['Knows'][var] = [False, 0]
            else:
                diffVar = vars[var+"_diff"]
                if diffVar is not None:
                    paramsDict['Knows'][var] = [True, text2diff[diffVar]]

    # Settings
    for hellRun in ['Ice', 'MainUpperNorfair', 'LowerNorfair']:
        value = vars[hellRun]
        if value is not None:
            paramsDict['Settings'][hellRun] = value

    for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
        value = vars[boss]
        if value is not None:
            paramsDict['Settings'][boss] = value

    for room in ['X-Ray', 'Gauntlet']:
        value = vars[room]
        if value is not None:
            paramsDict['Settings'][room] = value

    # Controller
    for button in Controller.__dict__:
        if isButton(button):
            value = vars[button]
            if value is None:
                paramsDict['Controller'][button] = Controller.__dict__[button]
            else:
                paramsDict['Controller'][button] = value

    return paramsDict

def computeDifficulty(jsonRomFileName):
    randomizedRom = os.path.basename(jsonRomFileName.replace('json', 'sfc'))

    presetFileName = "{}/{}.json".format(getPresetDir(session.solver['preset']), session.solver['preset'])
    jsonFileName = tempfile.mkstemp()[1]

    DB = db.DB()
    id = DB.initSolver()

    params = [
        'python2',  os.path.expanduser("~/RandomMetroidSolver/solver.py"),
        str(jsonRomFileName),
        '--preset', presetFileName,
        '--difficultyTarget', str(session.solver['difficultyTarget']),
        '--pickupStrategy', session.solver['pickupStrategy'],
        '--type', 'web',
        '--output', jsonFileName
    ]

    for item in session.solver['itemsForbidden']:
        params += ['--itemsForbidden', item]

    DB.addSolverParams(id, randomizedRom, session.solver['preset'], session.solver['difficultyTarget'],
                       session.solver['pickupStrategy'], session.solver['itemsForbidden'])

    print("before calling solver: {}".format(params))
    start = datetime.now()
    ret = subprocess.call(params)
    end = datetime.now()
    duration = (end - start).total_seconds()
    print("ret: {}, duration: {}s".format(ret, duration))

    if ret == 0:
        with open(jsonFileName) as jsonFile:
            result = json.load(jsonFile)
    else:
        result = "Solver: something wrong happened while solving the ROM"

    DB.addSolverResult(id, ret, duration, result)
    DB.close()

    os.remove(jsonFileName)

    return (ret == 0, result)

def infos():
    # set title
    response.title = 'Super Metroid VARIA Randomizer and Solver'

    return dict()

patches = [
    # name, desc, default on, visible on medium
    ('skip_intro', "Skip text intro (start at Ceres Station) (by Smiley)", False, False),
    ('skip_ceres', "Skip text intro and Ceres station (start at Landing Site) (by Total)", True, False),
    ('itemsounds', "Remove fanfare when picking up an item (by Scyzer)", True, True),
    ('spinjumprestart', "Allows Samus to start spinning in mid air after jumping or falling (by Kejardon)", False, True),
    ('elevators_doors_speed', 'Accelerate doors and elevators transitions (by Rakki & Lioran)', True, True),
    ('animals', "Save the animals surprise (by Foosda)", False, False),
    ('No_Music', "Disable background music (by Kejardon)", False, True)
]

def initRandomizerSession():
    if session.randomizer is None:
        session.randomizer = {}

        session.randomizer['maxDifficulty'] = 'hardcore'
        session.randomizer['paramsFile'] = 'regular'
        for patch in patches:
            if patch[2] == True:
                session.randomizer[patch[0]] = "on"
            else:
                session.randomizer[patch[0]] = "off"
        session.randomizer['missileQty'] = "3"
        session.randomizer['superQty'] = "2"
        session.randomizer['powerBombQty'] = "1"
        session.randomizer['minorQty'] = "100"
        session.randomizer['energyQty'] = "vanilla"
        session.randomizer['progressionSpeed'] = "medium"
        session.randomizer['spreadItems'] = "on"
        session.randomizer['fullRandomization'] = "on"
        session.randomizer['suitsRestriction'] = "on"
        session.randomizer['morphPlacement'] = "early"
        session.randomizer['funCombat'] = "off"
        session.randomizer['funMovement'] = "off"
        session.randomizer['funSuits'] = "off"
        session.randomizer['layoutPatches'] = "on"
        session.randomizer['progressionDifficulty'] = 'normal'
        session.randomizer['areaRandomization'] = "off"
        session.randomizer['complexity'] = "simple"
        session.randomizer['areaLayout'] = "off"
        session.randomizer['variaTweaks'] = "on"
        session.randomizer['hideItems'] = "off"
        session.randomizer['strictMinors'] = "off"

def randomizer():
    response.title = 'Super Metroid VARIA Randomizer'

    initRandomizerSession()

    presets = loadPresetsList()

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

    def getFloat(param):
        try:
            return float(request.vars[param])
        except:
            raiseHttp(400, "Wrong value for {}: {}, must be a float".format(param, request.vars[param]), isJson)

    for qty in quantities:
        if request.vars[qty] == 'random':
            continue
        qtyFloat = getFloat(qty)
        if qtyFloat < 1.0 or qtyFloat > 9.0:
            raiseHttp(400, json.dumps("Wrong value for {}: {}, must be between 1 and 9".format(qty, request.vars[qty])), isJson)

    if 'seed' in others:
        seedInt = getInt('seed')
        if seedInt < 0 or seedInt > 9999999:
            raiseHttp(400, "Wrong value for seed: {}, must be between 0 and 9999999".format(request.vars[seed]), isJson)

    if request.vars['maxDifficulty'] is not None:
        if request.vars.maxDifficulty not in ['no difficulty cap', 'easy', 'medium', 'hard', 'harder', 'hardcore', 'mania', 'random']:
            raiseHttp(400, "Wrong value for difficulty_target, authorized values: no difficulty cap/easy/medium/hard/harder/hardcore/mania", isJson)

    if IS_ALPHANUMERIC()(request.vars.paramsFile)[1] is not None:
        raiseHttp(400, "Wrong value for paramsFile, must be alphanumeric", isJson)

    if IS_LENGTH(maxsize=32, minsize=1)(request.vars.paramsFile)[1] is not None:
        raiseHttp(400, "Wrong length for paramsFile, name must be between 1 and 32 characters", isJson)

    if request.vars.minorQty != 'random':
        minorQtyInt = getInt('minorQty')
        if minorQtyInt < 1 or minorQtyInt > 100:
            raiseHttp(400, "Wrong value for minorQty, must be between 1 and 100", isJson)

    if 'energyQty' in others:
        if request.vars.energyQty not in ['sparse', 'medium', 'vanilla', 'random']:
            raiseHttp(400, "Wrong value for energyQty: authorized values: sparse/medium/vanilla", isJson)

    if 'paramsFileTarget' in others:
        try:
            json.loads(request.vars.paramsFileTarget)
        except:
            raiseHttp(400, "Wrong value for paramsFileTarget, must be a JSON string", isJson)

    for check in ['spreadItems', 'fullRandomization', 'suitsRestriction', 'layoutPatches', 'noGravHeat', 'areaRandomization', 'hideItems', 'strictMinors']:
        if check in others:
            if request.vars[check] not in ['on', 'off', 'random']:
                raiseHttp(400, "Wrong value for {}: {}, authorized values: on/off".format(check, request.vars[check]), isJson)

    if 'morphPlacement' in others:
        if request.vars['morphPlacement'] not in ['early', 'late', 'normal', 'random']:
            raiseHttp(400, "Wrong value for morphPlacement: {}, authorized values early/late/normal".format(request.vars['morphPlacement']), isJson)

    if 'progressionSpeed' in others:
        if request.vars['progressionSpeed'] not in ['slowest', 'slow', 'medium', 'fast', 'fastest', 'random', 'basic']:
            raiseHttp(400, "Wrong value for progressionSpeed: {}, authorized values slowest/slow/medium/fast/fastest/basic".format(request.vars['progressionSpeed']), isJson)

    if 'progressionDifficulty' in others:
        if request.vars['progressionDifficulty'] not in ['easier', 'normal', 'harder', 'random']:
            raiseHttp(400, "Wrong value for progressionDifficulty: {}, authorized values easier/normal/harder".format(request.vars['progressionDifficulty']), isJson)

    if 'complexity' in others:
        if request.vars['complexity'] not in ['simple', 'medium', 'advanced']:
            raiseHttp(400, "Wrong value for complexity: {}, authorized values simple/medium/advanced".format(request.vars['complexity']), isJson)

def sessionWebService():
    # web service to update the session
    patchs = ['itemsounds', 'No_Music',
              'spinjumprestart', 'elevators_doors_speed',
              'skip_intro', 'skip_ceres', 'animals', 'areaLayout', 'variaTweaks']
    quantities = ['missileQty', 'superQty', 'powerBombQty']
    others = ['paramsFile', 'minorQty', 'energyQty', 'maxDifficulty',
              'progressionSpeed', 'spreadItems', 'fullRandomization', 'suitsRestriction',
              'funCombat', 'funMovement', 'funSuits', 'layoutPatches',
              'noGravHeat', 'progressionDifficulty', 'morphPlacement',
              'areaRandomization', 'complexity', 'hideItems', 'strictMinors']
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
    session.randomizer['progressionSpeed'] = request.vars.progressionSpeed
    session.randomizer['spreadItems'] = request.vars.spreadItems
    session.randomizer['fullRandomization'] = request.vars.fullRandomization
    session.randomizer['suitsRestriction'] = request.vars.suitsRestriction
    session.randomizer['morphPlacement'] = request.vars.morphPlacement
    session.randomizer['funCombat'] = request.vars.funCombat
    session.randomizer['funMovement'] = request.vars.funMovement
    session.randomizer['funSuits'] = request.vars.funSuits
    session.randomizer['layoutPatches'] = request.vars.layoutPatches
    session.randomizer['noGravHeat'] = request.vars.noGravHeat
    session.randomizer['progressionDifficulty'] = request.vars.progressionDifficulty
    session.randomizer['areaRandomization'] = request.vars.areaRandomization
    session.randomizer['complexity'] = request.vars.complexity
    session.randomizer['areaLayout'] = request.vars.areaLayout
    session.randomizer['variaTweaks'] = request.vars.variaTweaks
    session.randomizer['hideItems'] = request.vars.hideItems
    session.randomizer['strictMinors'] = request.vars.strictMinors

def getCustomMapping(controlMapping):
    if len(controlMapping) == 0:
        return (False, None)

    inv = {}
    for button in controlMapping:
        inv[controlMapping[button]] = button

    return (True, "{},{},{},{},{},{},{}".format(inv["Shoot"], inv["Jump"], inv["Dash"], inv["Item Select"], inv["Item Cancel"], inv["Angle Up"], inv["Angle Down"]))

def randomizerWebService():
    # web service to compute a new random (returns json string)
    print("randomizerWebService")

    # set header to authorize cross domain AJAX
    response.headers['Access-Control-Allow-Origin'] = '*'

    # check validity of all parameters
    patchs = ['itemsounds', 'spinjumprestart', 'elevators_doors_speed', 'skip_intro',
              'skip_ceres', 'areaLayout', 'variaTweaks', 'No_Music']
    quantities = ['missileQty', 'superQty', 'powerBombQty']
    others = ['seed', 'paramsFile', 'paramsFileTarget', 'minorQty', 'energyQty',
              'maxDifficulty', 'progressionSpeed', 'spreadItems', 'fullRandomization',
              'suitsRestriction', 'morphPlacement', 'funCombat', 'funMovement', 'funSuits',
              'layoutPatches', 'noGravHeat', 'progressionDifficulty', 'areaRandomization',
              'hideItems', 'strictMinors', 'complexity']
    validateWebServiceParams(patchs, quantities, others, isJson=True)

    # randomize
    DB = db.DB()
    id = DB.initRando()

    presetFileName = tempfile.mkstemp()[1] + '.json'
    jsonFileName = tempfile.mkstemp()[1]

    print("randomizerWebService, params validated")
    for var in request.vars:
        print("{}: {}".format(var, request.vars[var]))

    with open(presetFileName, 'w') as presetFile:
        presetFile.write(request.vars.paramsFileTarget)

    seed = request.vars.seed
    if seed == '0':
        seed = str(random.randint(0, 9999999))

    params = ['python2',  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
              '--seed', seed,
              '--output', jsonFileName,
              '--param', presetFileName,
              '--preset', request.vars.paramsFile,
              '--progressionSpeed', request.vars.progressionSpeed,
              '--progressionDifficulty', request.vars.progressionDifficulty,
              '--morphPlacement', request.vars.morphPlacement]
    params += ['--missileQty', request.vars.missileQty if request.vars.missileQty != 'random' else '0',
               '--superQty', request.vars.superQty if request.vars.superQty != 'random' else '0',
               '--powerBombQty', request.vars.powerBombQty if request.vars.powerBombQty != 'random' else '0',
               '--minorQty', request.vars.minorQty if request.vars.minorQty != 'random' else '0',
               '--energyQty', request.vars.energyQty]

    for patch in patches:
        if request.vars[patch[0]] == 'on':
            if patch[0] in ['animals', 'areaLayout', 'variaTweaks']:
                continue
            params.append('-c')
            if patch[0] == 'No_Music':
                params.append(patch[0])
            else:
                params.append(patch[0] + '.ips')
    if request.vars.animals == 'on':
        params.append('--animals')
    if request.vars.areaLayout == 'off':
        params.append('--areaLayoutBase')
    if request.vars.variaTweaks == 'off':
        params.append('--novariatweaks')

    if request.vars.maxDifficulty != 'no difficulty cap':
        params.append('--maxDifficulty')
        params.append(request.vars.maxDifficulty)

    def addParamRandom(id, params):
        if request.vars[id] in ['on', 'random']:
            params.append('--{}'.format(id))
        if request.vars[id] == 'random':
            params.append('random')

    addParamRandom('fullRandomization', params)
    addParamRandom('spreadItems', params)
    addParamRandom('suitsRestriction', params)
    addParamRandom('hideItems', params)
    addParamRandom('strictMinors', params)

    def addSuperFun(id, params):
        fun = id[len('fun'):]
        if request.vars[id] == 'on':
            params += ['--superFun', fun]
        elif request.vars[id] == 'random':
            params += ['--superFun', "{}Random".format(fun)]

    addSuperFun('funCombat', params)
    addSuperFun('funMovement', params)
    addSuperFun('funSuits', params)

    if request.vars.layoutPatches == 'off':
        params.append('--nolayout')
    if request.vars.noGravHeat == 'off':
        params.append('--nogravheat')

    if request.vars.areaRandomization == 'on':
        params.append('--area')

    # load content of preset to get controller mapping
    try:
        controlMapping = PresetLoader.factory(presetFileName).params['Controller']
    except Exception as e:
        os.remove(jsonFileName)
        os.remove(presetFileName)
        raise HTTP(400, json.dumps("randomizerWebService: can't load the preset"))

    (custom, controlParam) = getCustomMapping(controlMapping)
    if custom == True:
        params += ['--controls', controlParam]

    DB.addRandoParams(id, params + ['--complexity', request.vars.complexity])

    print("before calling: {}".format(params))
    start = datetime.now()
    ret = subprocess.call(params)
    end = datetime.now()
    duration = (end - start).total_seconds()
    print("ret: {}, duration: {}s".format(ret, duration))

    if ret == 0:
        with open(jsonFileName) as jsonFile:
            locsItems = json.load(jsonFile)

        # check if an info message has been returned
        msg = ''
        if len(locsItems['errorMsg']) > 0:
            msg = locsItems['errorMsg']

        DB.addRandoResult(id, ret, duration, msg)
        DB.close()

        os.remove(jsonFileName)
        os.remove(presetFileName)
        return json.dumps(locsItems)
    else:
        # extract error from json
        try:
            with open(jsonFileName) as jsonFile:
                msg = json.load(jsonFile)['errorMsg']
        except:
            msg = "randomizerWebService: something wrong happened"

        DB.addRandoResult(id, ret, duration, msg)
        DB.close()

        os.remove(jsonFileName)
        os.remove(presetFileName)
        raise HTTP(400, json.dumps(msg))

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

    fullPath = '{}/{}.json'.format(getPresetDir(paramsFile), paramsFile)

    # check that the presets file exists
    if os.path.isfile(fullPath):
        # load it
        try:
            params = PresetLoader.factory(fullPath).params
        except Exception as e:
            raise HTTP(400, "Can't load the preset")
        params = json.dumps(params)
        return params
    else:
        raise HTTP(400, "Preset '{}' not found".format(fullPath))

def home():
    # set title
    response.title = 'Super Metroid VARIA Randomizer and Solver'

    return dict()

def getErrors():
    # check dir exists
    errDir = os.path.expanduser("~/web2py/applications/solver/errors")
    if os.path.isdir(errDir):
        # list error files
        errFiles = glob.glob(os.path.join(errDir, "*"))

        # sort by date
        errFiles.sort(key=os.path.getmtime)
        errFiles = [os.path.basename(f) for f in errFiles]
        return errFiles
    else:
        return []

def stats():
    response.title = 'Super Metroid VARIA Randomizer and Solver statistics'

    DB = db.DB()
    weeks = 1

    solverPresets = DB.getSolverPresets(weeks)
    randomizerPresets = DB.getRandomizerPresets(weeks)

    solverDurations = DB.getSolverDurations(weeks)
    randomizerDurations = DB.getRandomizerDurations(weeks)

    solverData = DB.getSolverData(weeks)
    randomizerData = DB.getRandomizerData(weeks)

    errors = getErrors()

    return dict(solverPresets=solverPresets, randomizerPresets=randomizerPresets,
                solverDurations=solverDurations, randomizerDurations=randomizerDurations,
                solverData=solverData, randomizerData=randomizerData, errors=errors)
