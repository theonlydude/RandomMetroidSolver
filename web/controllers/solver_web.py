# -*- coding: utf-8 -*-

import sys, os.path

path = os.path.expanduser('~/RandomMetroidSolver')
if os.path.exists(path) and path not in sys.path:
    sys.path.append(path)

import datetime, os, hashlib, json, subprocess, tempfile, glob, random, re, math, string, base64, urllib.parse, uuid
from datetime import datetime
import urllib.parse

# to solve the rom
from utils.parameters import easy, medium, hard, harder, hardcore, mania, diff4solver
from utils.parameters import Knows, Settings, Controller, isKnows, isButton
from solver.conf import Conf
from utils.parameters import diff2text, text2diff
from utils.utils import PresetLoader, removeChars, getDefaultMultiValues
from utils.db import DB
from graph.graph_access import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, accessPoints, GraphUtils
from utils.utils import isStdPreset, getRandomizerDefaultParameters, getPresetDir
from graph.graph_locations import locations
from logic.smboolmanager import SMBoolManager
from rom.romreader import RomReader
from rom.rom_patches import RomPatches
from rom.ips import IPS_Patch
from randomizer import energyQties, progDiffs, morphPlacements, majorsSplits, speeds
from utils.doorsmanager import DoorsManager

# discord webhook for plandorepo
try:
    from webhook import webhookUrl
    from discord_webhook import DiscordWebhook, DiscordEmbed
    webhookAvailable = True
except:
    webhookAvailable = False

# put an expiration date to the default cookie to have it kept between browser restart
response.cookies['session_id_solver']['expires'] = 31 * 24 * 3600

localIpsDir = 'varia_repository'

# use the correct one
pythonExec = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)

maxPresets = 4096
def maxPresetsReach():
    # to prevent a spammer to create presets in a loop and fill the fs
    return len(os.listdir('community_presets')) >= maxPresets

def loadPreset():
    # load conf from session if available
    loaded = False

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

def completePreset(params):
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

def loadPresetsList():
    files = sorted(os.listdir('community_presets'), key=lambda v: v.upper())
    stdPresets = ['newbie', 'casual', 'regular', 'veteran', 'expert', 'master']
    tourPresets = ['Season_Races', 'Playoff_Races', 'Playoff_Races_Chozo', 'SMRAT2021']
    comPresets = [os.path.splitext(file)[0] for file in files if file != '.git']
    return (stdPresets, tourPresets, comPresets)

def loadRandoPresetsList():
    tourPresets = ['Season_Races', 'Season_Races_Chozo', 'Playoff_Races', 'Playoff_Races_Chozo', 'SMRAT2021', 'VARIA_Weekly']
    files = sorted(os.listdir('rando_presets'), key=lambda v: v.upper())
    randoPresets = [os.path.splitext(file)[0] for file in files]
    randoPresets = [preset for preset in randoPresets if preset not in tourPresets]

    return (randoPresets, tourPresets)

def validatePresetsParams(action):
    if action == 'Create':
        preset = request.vars.presetCreate
    else:
        preset = request.vars.preset

    if IS_NOT_EMPTY()(preset)[1] is not None:
        return (False, "Preset name is empty")
    if IS_ALPHANUMERIC()(preset)[1] is not None:
        return (False, "Preset name must be alphanumeric: {}".format(preset))
    if IS_LENGTH(32)(preset)[1] is not None:
        return (False, "Preset name must be max 32 chars: {}".format(preset))

    if action in ['Create', 'Update']:
        if IS_NOT_EMPTY()(request.vars.password)[1] is not None:
            return (False, "Password is empty")
        if IS_ALPHANUMERIC()(request.vars.password)[1] is not None:
            return (False, "Password must be alphanumeric")
        if IS_LENGTH(32)(request.vars.password)[1] is not None:
            return (False, "Password must be max 32 chars")

        # check that there's not two buttons for the same action
        map = {}
        for button in Controller.__dict__:
            if isButton(button):
                value = request.vars[button]
                if button == "Moonwalk":
                    if value not in [None, 'on']:
                        return (False, "Invalid value for Moonwalk: {}".format(value))
                else:
                    if value is None:
                        return (False, "Button {} not set".format(button))
                    else:
                        if value in map:
                            return (False, "Action {} set for two buttons: {} and {}".format(value, button, map[value]))
                        map[value] = button

    if request.vars.currenttab not in ['Global', 'Techniques1', 'Techniques2', 'Techniques3', 'Techniques4', 'Techniques5', 'Techniques6', 'Techniques7', 'Techniques8', 'Mapping']:
        return (False, "Wrong value for current tab: [{}]".format(request.vars.currenttab))

    return (True, None)

def getSkillLevelBarData(preset):
    result = {'standards': {}}
    result['name'] = preset
    try:
        params = PresetLoader.factory('{}/{}.json'.format(getPresetDir(preset), preset)).params
        result['custom'] = (preset, params['score'])
        # add stats on the preset
        result['knowsKnown'] = len([know for know in params['Knows'] if params['Knows'][know][0] == True])
    except:
        result['custom'] = (preset, 'N/A')
        result['knowsKnown'] = 'N/A'

    # get score of standard presets
    for preset in ['newbie', 'casual', 'regular', 'veteran', 'expert', 'master', 'samus']:
        score = PresetLoader.factory('{}/{}.json'.format(getPresetDir(preset), preset)).params['score']
        result['standards'][preset] = score

    db = DB()
    result['generatedSeeds'] = db.getGeneratedSeeds(result['custom'][0])
    result['lastAction'] = db.getPresetLastActionDate(result['custom'][0])
    db.close()

    # TODO: normalize result (or not ?)
    return result

def initPresetsSession():
    if session.presets is None:
        session.presets = {}

        session.presets['preset'] = 'regular'
        session.presets['presetDict'] = None
        session.presets['currentTab'] = 'Global'

def updatePresetsSession():
    if request.vars.action == 'Create':
        session.presets['preset'] = request.vars.presetCreate
    elif request.vars.preset == None:
        session.presets['preset'] = 'regular'
    else:
        session.presets['preset'] = request.vars.preset

def computeGauntlet(sm, bomb, addVaria):
    result = {}

    for key in Settings.hardRoomsPresets['Gauntlet']:
        Settings.hardRooms['Gauntlet'] = Settings.hardRoomsPresets['Gauntlet'][key]
        sm.resetItems()
        if addVaria == True:
            sm.addItem('Varia')
        sm.addItem(bomb)

        result[key] = {easy: -1, medium: -1, hard: -1, harder: -1, hardcore: -1, mania: -1}

        for i in range(18):
            ret = sm.energyReserveCountOkHardRoom('Gauntlet', 0.51 if bomb == 'Bomb' else 1.0)

            if ret.bool == True:
                nEtank = 0
                for item in ret.items:
                    if item.find('ETank') != -1:
                        nEtank = int(item[0:item.find('-ETank')])
                        break
                result[key][ret.difficulty] = nEtank

            sm.addItem('ETank')

    return result

def computeXray(sm, addVaria):
    result = {}

    for key in Settings.hardRoomsPresets['X-Ray']:
        if key == 'Solution':
            continue
        Settings.hardRooms['X-Ray'] = Settings.hardRoomsPresets['X-Ray'][key]
        sm.resetItems()
        if addVaria == True:
            sm.addItem('Varia')

        result[key] = {easy: -1, medium: -1, hard: -1, harder: -1, hardcore: -1, mania: -1}

        for i in range(18):
            ret = sm.energyReserveCountOkHardRoom('X-Ray')

            if ret.bool == True:
                nEtank = 0
                for item in ret.items:
                    if item.find('ETank') != -1:
                        nEtank = int(item[0:item.find('-ETank')])
                        break
                result[key][ret.difficulty] = nEtank

            sm.addItem('ETank')

    return result

def computeHardRooms(hardRooms):
    # add gravity patch (as we add it by default in the randomizer)
    RomPatches.ActivePatches.append(RomPatches.NoGravityEnvProtection)

    sm = SMBoolManager()

    # xray
    xray = {}
    xray['Suitless'] = computeXray(sm, False)
    xray['Varia'] = computeXray(sm, True)
    hardRooms['X-Ray'] = xray

    # gauntlet
    gauntlet = {}
    gauntlet['SuitlessBomb'] = computeGauntlet(sm, 'Bomb', False)
    gauntlet['SuitlessPowerBomb'] = computeGauntlet(sm, 'PowerBomb', False)
    gauntlet['VariaBomb'] = computeGauntlet(sm, 'Bomb', True)
    gauntlet['VariaPowerBomb'] = computeGauntlet(sm, 'PowerBomb', True)
    hardRooms['Gauntlet'] = gauntlet

    return hardRooms

def addCF(sm, count):
    sm.addItem('Morph')
    sm.addItem('PowerBomb')

    for i in range(count):
        sm.addItem('Missile')
        sm.addItem('Missile')
        sm.addItem('Super')
        sm.addItem('Super')
        sm.addItem('PowerBomb')
        sm.addItem('PowerBomb')

def computeHellruns(hellRuns):
    sm = SMBoolManager()
    for hellRun in ['Ice', 'MainUpperNorfair']:
        hellRuns[hellRun] = {}

        for (actualHellRun, params) in Settings.hellRunsTable[hellRun].items():
            hellRuns[hellRun][actualHellRun] = {}
            for (key, difficulties) in Settings.hellRunPresets[hellRun].items():
                if key == 'Solution':
                    continue
                Settings.hellRuns[hellRun] = difficulties
                hellRuns[hellRun][actualHellRun][key] = {easy: -1, medium: -1, hard: -1, harder: -1, hardcore: -1, mania: -1}
                if difficulties == None:
                    continue

                sm.resetItems()
                for etank in range(19):
                    ret = sm.canHellRun(**params)

                    if ret.bool == True:
                        nEtank = 0
                        for item in ret.items:
                            if item.find('ETank') != -1:
                                nEtank = int(item[0:item.find('-ETank')])
                                break
                        hellRuns[hellRun][actualHellRun][key][ret.difficulty] = nEtank

                    sm.addItem('ETank')

    hellRun = 'LowerNorfair'
    hellRuns[hellRun] = {}
    hellRuns[hellRun]["NoScrew"] = computeLNHellRun(sm, False)
    hellRuns[hellRun]["Screw"] = computeLNHellRun(sm, True)

def getNearestDifficulty(difficulty):
    epsilon = 0.001
    if difficulty < medium - epsilon:
        return easy
    elif difficulty < hard - epsilon:
        return medium
    elif difficulty < harder - epsilon:
        return hard
    elif difficulty < hardcore - epsilon:
        return harder
    elif difficulty < mania - epsilon:
        return hardcore
    else:
        return mania

def computeLNHellRun(sm, addScrew):
    result = {}
    hellRun = 'LowerNorfair'
    for (actualHellRun, params) in Settings.hellRunsTable[hellRun].items():
        result[actualHellRun] = {}
        for (key, difficulties) in Settings.hellRunPresets[hellRun].items():
            if key == 'Solution':
                continue
            Settings.hellRuns[hellRun] = difficulties
            result[actualHellRun][key] = {'ETank': {easy: -1, medium: -1, hard: -1, harder: -1, hardcore: -1, mania: -1}, 'CF': {easy: -1, medium: -1, hard: -1, harder: -1, hardcore: -1, mania: -1}}
            if difficulties == None:
                continue

            for cf in range(3, 0, -1):
                sm.resetItems()
                if addScrew == True:
                    sm.addItem('ScrewAttack')
                addCF(sm, cf)
                for etank in range(19):
                    ret = sm.canHellRun(**params)

                    if ret.bool == True:
                        nEtank = 0
                        for item in ret.items:
                            if item.find('ETank') != -1:
                                nEtank = int(item[0:item.find('-ETank')])
                                break
                        result[actualHellRun][key]['ETank'][getNearestDifficulty(ret.difficulty)] = nEtank
                        result[actualHellRun][key]['CF'][getNearestDifficulty(ret.difficulty)] = cf

                    sm.addItem('ETank')
    return result

def presets():
    initPresetsSession()

    # use web2py builtin cache to avoid recomputing the hardrooms requirements
    hardRooms = cache.ram('hardRooms', lambda:dict(), time_expire=None)
    if len(hardRooms) == 0:
        computeHardRooms(hardRooms)

    hellRuns = cache.ram('hellRuns', lambda:dict(), time_expire=None)
    if len(hellRuns) == 0:
        computeHellruns(hellRuns)

    if request.vars.action is not None:
        (ok, msg) = validatePresetsParams(request.vars.action)
        if not ok:
            session.flash = msg
            redirect(URL(r=request, f='presets'))
        else:
            session.presets['currentTab'] = request.vars.currenttab

        if request.vars.action == 'Create':
            preset = request.vars.presetCreate
        else:
            preset = request.vars.preset

    # in web2py.js, in disableElement, remove 'working...' to have action with correct value
    if request.vars.action == 'Load':
        # check that the presets file exists
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if os.path.isfile(fullPath):
            # load it
            try:
                params = PresetLoader.factory(fullPath).params
                updatePresetsSession()
                session.presets["presetDict"] = None
            except Exception as e:
                session.flash = "L:Error loading the preset {}: {}".format(preset, e)
        else:
            session.flash = "Presets file not found: {}".format(fullPath)
        redirect(URL(r=request, f='presets'))

    elif request.vars.action in ['Update', 'Create']:
        # check if the presets file already exists
        password = request.vars['password']
        password = password.encode('utf-8')
        passwordSHA256 = hashlib.sha256(password).hexdigest()
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if os.path.isfile(fullPath):
            # load it
            end = False
            try:
                oldParams = PresetLoader.factory(fullPath).params
            except Exception as e:
                session.flash = "UC:Error loading the preset {}: {}".format(preset, e)
                end = True
            if end == True:
                redirect(URL(r=request, f='presets'))

            # check if password match
            if 'password' in oldParams and passwordSHA256 == oldParams['password']:
                # update the presets file
                paramsDict = genJsonFromParams(request.vars)
                paramsDict['password'] = passwordSHA256
                try:
                    PresetLoader.factory(paramsDict).dump(fullPath)
                    db = DB()
                    db.addPresetAction(preset, 'update')
                    db.close()
                    updatePresetsSession()
                    session.flash = "Preset {} updated".format(preset)
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
                    db = DB()
                    db.addPresetAction(preset, 'create')
                    db.close()
                    updatePresetsSession()
                    session.flash = "Preset {} created".format(preset)
                except Exception as e:
                    session.flash = "Error writing the preset {}: {}".format(preset, e)
                redirect(URL(r=request, f='presets'))
            else:
                session.flash = "Sorry, maximum number of presets reached, can't add more"
                redirect(URL(r=request, f='presets'))

    # set title
    response.title = 'Super Metroid VARIA Presets'

    # load conf from session if available
    error = False
    try:
        params = loadPreset()
    except Exception as e:
        session.presets['preset'] = 'regular'
        session.flash = "S:Error loading the preset: {}".format(e)
        error = True
    if error == True:
        redirect(URL(r=request, f='presets'))

    # load presets list
    (stdPresets, tourPresets, comPresets) = loadPresetsList()

    # add missing knows/settings
    completePreset(params)

    # compute score for skill bar
    skillBarData = getSkillLevelBarData(session.presets['preset'])

    # send values to view
    return dict(desc=Knows.desc, difficulties=diff2text,
                categories=Knows.categories, settings=params['Settings'], knows=params['Knows'],
                easy=easy, medium=medium, hard=hard, harder=harder, hardcore=hardcore, mania=mania,
                controller=params['Controller'], stdPresets=stdPresets, tourPresets=tourPresets,
                comPresets=comPresets, skillBarData=skillBarData, hardRooms=hardRooms, hellRuns=hellRuns)

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
        roms = ['{}.sfc'.format(file) for file in filtered]

    return roms

def getLastSolvedROM():
    if session.solver['romFile'] is not None:
        return '{}.sfc'.format(session.solver['romFile'])
    else:
        return None

def genPathTable(locations, displayAPs=True):
    if locations is None or len(locations) == 0:
        return None

    lastAP = None
    pathTable = """
<table class="full">
  <colgroup>
    <col class="locName" /><col class="area" /><col class="subarea" /><col class="item" /><col class="difficulty" /><col class="knowsUsed" /><col class="itemsUsed" />
  </colgroup>
  <tr>
    <th>Location Name</th><th>Area</th><th>SubArea</th><th>Item</th><th>Difficulty</th><th>Techniques used</th><th>Items used</th>
  </tr>
"""

    currentSuit = 'Power'
    for location, area, subarea, item, locDiff, locTechniques, locItems, pathDiff, pathTechniques, pathItems, path, _class in locations:
        if path is not None:
            lastAP = path[-1]
            if displayAPs == True and not (len(path) == 1 and path[0] == lastAP):
                pathTable += """<tr class="grey"><td colspan="3">{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n""".format(" -&gt; ".join(path), """<img alt="samus" class="imageItem" src="/solver/static/images/samus_run_{}.gif" title="samus" />""".format(currentSuit), getDiffImg(pathDiff), getTechniques(pathTechniques), getItems(pathItems))

        (name, room) = location

        # not picked up items start with an '-'
        if item[0] != '-':
            pathTable += """
<tr class="{}">
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
""".format(item, getRoomLink(name, room), getAreaLink(area), getSubArea(subarea),
           getBossImg(name) if "Boss" in _class else getItemImg(item), getDiffImg(locDiff),
           getTechniques(locTechniques), getItems(locItems))

            if item == 'Varia' and currentSuit == 'Power':
                currentSuit = 'Varia'
            elif item == 'Gravity':
                currentSuit = 'Gravity'

    pathTable += "</table>"

    return pathTable

def getItems(items):
    ret = ""
    for item in items:
        if item[0] >= '0' and item[0] <= '9':
            # for etanks and reserves
            count = item[:item.find('-')]
            item = item[item.find('-')+1:]
            ret += "<span>{}-{}</span>".format(count, getItemImg(item, True))
        else:
            ret += getItemImg(item, True)
    return ret

def getTechniques(techniques):
    ret = ""
    for tech in techniques:
        if tech in Knows.desc and Knows.desc[tech]['href'] != None:
            ret += """ <a class="marginKnows" href="{}" target="_blank">{}</a>""".format(Knows.desc[tech]['href'], tech)
        else:
            ret += """ {}""".format(tech)
    return ret

def getRoomLink(name, room):
    roomUrl = room.replace(' ', '_').replace("'", '%27')
    roomImg = room.replace(' ', '').replace('-', '').replace("'", '')
    return """<a target="_blank" href="https://wiki.supermetroid.run/{}" data-thumbnail-src="/solver/static/images/{}.png" class="room">{}</a>""".format(roomUrl, roomImg, name)

def getAreaLink(name):
    if name == "WreckedShip":
        url = "Wrecked_Ship"
    elif name == "LowerNorfair":
        url = "Norfair"
    else:
        url = name

    return """<a target="_blank" href="https://metroid.fandom.com/wiki/{}" data-thumbnail-src="/solver/static/images/{}.png" class="area">{}</a>""".format(url, name, name)

def getSubArea(subarea):
    img = subarea.replace(' ', '')
    if img in ["Kraid", "Tourian"]:
        # kraid is already the image for kraid boss
        img += "SubArea"
    return """<span data-thumbnail-src="/solver/static/images/{}.png" class="subarea">{}</span>""".format(img, subarea)

def getBossImg(boss):
    return """<img alt="{}" class="imageBoss" src="/solver/static/images/{}.png" title="{}" />""".format(boss, boss.replace(' ', ''), boss)

def getItemImg(item, small=False):
    if small == True:
        _class = "imageItems"
    else:
        _class = "imageItem"
    return """<img alt="{}" class="{}" src="/solver/static/images/{}.png" title="{}" />""".format(item, _class, item, item)

def getDiffImg(diff):
    diffName = diff4solver(float(diff))

    return """<img alt="{}" class="imageItem" src="/solver/static/images/marker_{}.png" title="{}" />""".format(diffName, diffName, diffName)

def prepareResult():
    if session.solver['result'] is not None:
        result = session.solver['result']

        if result['difficulty'] == -1:
            result['resultText'] = "The ROM \"{}\" is not finishable with the known techniques".format(result['randomizedRom'])
        else:
            if result['itemsOk'] is False:
                result['resultText'] = "The ROM \"{}\" is finishable but not all the requested items can be picked up with the known techniques. Estimated difficulty is: ".format(result['randomizedRom'])
            else:
                result['resultText'] = "The ROM \"{}\" estimated difficulty is: ".format(result['randomizedRom'])

        # add generated path (spoiler !)
        result['pathTable'] = genPathTable(result['generatedPath'])
        result['pathremainTry'] = genPathTable(result['remainTry'])
        result['pathremainMajors'] = genPathTable(result['remainMajors'], False)
        result['pathremainMinors'] = genPathTable(result['remainMinors'], False)
        result['pathskippedMajors'] = genPathTable(result['skippedMajors'], False)
        result['pathunavailMajors'] = genPathTable(result['unavailMajors'], False)

        # display the result only once
        session.solver['result'] = None
    else:
        result = None

    return result

def validateSolverParams():
    for param in ['difficultyTarget', 'pickupStrategy', 'complexity']:
        if request.vars[param] is None:
            return (False, "Missing parameter {}".format(param))

    if request.vars.preset == None:
        return (False, "Missing parameter preset")
    preset = request.vars.preset

    if IS_ALPHANUMERIC()(preset)[1] is not None:
        return (False, "Wrong value for preset, must be alphanumeric")

    if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
        return (False, "Wrong length for preset, name must be between 1 and 32 characters")

    # check that preset exists
    fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
    if not os.path.isfile(fullPath):
        return (False, "Unknown preset: {}".format(preset))

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
        if IS_LENGTH(maxsize=255, minsize=1)(request.vars.romFile)[1] is not None:
            return (False, "Wrong length for romFile, name must be between 1 and 256 characters: {}".format(request.vars.romFile))

    if request.vars.romJson is not None and len(request.vars.romJson) > 0:
        try:
            json.loads(request.vars.romJson)
        except:
            return (False, "Wrong value for romJson, must be a JSON string: [{}]".format(request.vars.romJson))

    if request.vars.uploadFile is not None:
        if type(request.vars.uploadFile) == str:
            if IS_MATCH('[a-zA-Z0-9_\.() ,\-]*', strict=True)(request.vars.uploadFile)[1] is not None:
                return (False, "Wrong value for uploadFile, must be a valid file name: {}".format(request.vars.uploadFile))

            if IS_LENGTH(maxsize=256, minsize=1)(request.vars.uploadFile)[1] is not None:
                return (False, "Wrong length for uploadFile, name must be between 1 and 255 characters")

    return (True, None)

def generateJsonROM(romJsonStr):
    tempRomJson = json.loads(romJsonStr)
    romFileName = tempRomJson["romFileName"]
    (base, ext) = os.path.splitext(romFileName)
    jsonRomFileName = 'roms/{}.json'.format(base)
    del tempRomJson["romFileName"]

    with open(jsonRomFileName, 'w') as jsonFile:
        json.dump(tempRomJson, jsonFile)

    return (base, jsonRomFileName)

def solver():
    # init session
    initSolverSession()

    if request.vars.action == 'Solve':
        (ok, msg) = validateSolverParams()
        if not ok:
            session.flash = msg
            redirect(URL(r=request, f='solver'))

        updateSolverSession()

        preset = request.vars.preset

        # new uploaded rom ?
        error = False
        if request.vars['romJson'] != '':
            try:
                (base, jsonRomFileName) = generateJsonROM(request.vars['romJson'])
                session.solver['romFile'] = base
                if base not in session.solver['romFiles']:
                    session.solver['romFiles'].append(base)
            except Exception as e:
                print("Error loading the ROM file, exception: {}".format(e))
                session.flash = "Error loading the json ROM file"
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
                try:
                    (ok, result) = computeDifficulty(jsonRomFileName, preset)
                    if not ok:
                        session.flash = result
                        redirect(URL(r=request, f='solver'))
                    session.solver['result'] = result
                except Exception as e:
                    print("Error loading the ROM file, exception: {}".format(e))
                    session.flash = "Error loading the ROM file"

        redirect(URL(r=request, f='solver'))

    # display result
    result = prepareResult()

    # set title
    response.title = 'Super Metroid VARIA Solver'

    ROMs = getROMsList()

    # last solved ROM
    lastRomFile = getLastSolvedROM()

    # load presets list
    (stdPresets, tourPresets, comPresets) = loadPresetsList()

    # generate list of addresses to read in the ROM
    addresses = getAddressesToRead()

    # send values to view
    return dict(desc=Knows.desc, stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets, roms=ROMs,
                lastRomFile=lastRomFile, difficulties=diff2text, categories=Knows.categories,
                result=result, addresses=addresses,
                easy=easy, medium=medium, hard=hard, harder=harder, hardcore=hardcore, mania=mania)

def getAddressesToRead(plando=False):
    addresses = {"locations": [], "patches": [], "transitions": [], "misc": [], "ranges": []}

    # locations
    for loc in locations:
        addresses["locations"].append(loc.Address)

    # patches
    for (patch, values) in RomReader.patches.items():
        addresses["patches"].append(values["address"])

    # transitions
    for ap in accessPoints:
        if ap.Internal == True:
            continue
        addresses["transitions"].append(0x10000 | ap.ExitInfo['DoorPtr'])

    # misc
    # majors split
    addresses["misc"].append(0x17B6C)
    # escape timer
    addresses["misc"].append(0x1E21)
    addresses["misc"].append(0x1E22)
    # nothing id
    addresses["misc"].append(0x17B6D)
    # start ap
    addresses["misc"].append(0x10F200)
    addresses["misc"].append(0x10F201)
    # random doors
    addresses["misc"] += DoorsManager.getAddressesToRead()

    # ranges [low, high]
    ## doorasm
    addresses["ranges"] += [0x7EB00, 0x7ee60]
    # for next release doorasm addresses will be relocated
    maxDoorAsmPatchLen = 22
    addresses["ranges"] += [0x7F800, 0x7F800+(maxDoorAsmPatchLen * len([ap for ap in accessPoints if ap.Internal == False]))]

    if plando == True:
        # plando addresses
        addresses["ranges"] += [0x2F6000, 0x2F6100]
        # plando transitions (4 bytes per transitions, ap#/2 transitions)
        addresses["ranges"] += [0x2F6100, 0x2F6100+((len(addresses["transitions"])/2) * 4)]

    return addresses

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
                if button == "Moonwalk":
                    if value != None and value == "on":
                        paramsDict['Controller'][button] = True
                    else:
                        paramsDict['Controller'][button] = False
                else:
                    paramsDict['Controller'][button] = value

    return paramsDict

def computeDifficulty(jsonRomFileName, preset):
    randomizedRom = os.path.basename(jsonRomFileName.replace('json', 'sfc'))

    presetFileName = "{}/{}.json".format(getPresetDir(preset), preset)
    (fd, jsonFileName) = tempfile.mkstemp()

    db = DB()
    id = db.initSolver()

    params = [
        pythonExec,  os.path.expanduser("~/RandomMetroidSolver/solver.py"),
        '-r', str(jsonRomFileName),
        '--preset', presetFileName,
        '--difficultyTarget', str(session.solver['difficultyTarget']),
        '--pickupStrategy', session.solver['pickupStrategy'],
        '--type', 'web',
        '--output', jsonFileName
    ]

    for item in session.solver['itemsForbidden']:
        params += ['--itemsForbidden', item]

    db.addSolverParams(id, randomizedRom, preset, session.solver['difficultyTarget'],
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

    db.addSolverResult(id, ret, duration, result)
    db.close()

    os.close(fd)
    os.remove(jsonFileName)

    return (ret == 0, result)

def infos():
    # set title
    response.title = 'Super Metroid VARIA Randomizer and Solver'

    return dict()

def initRandomizerSession():
    if session.randomizer is None:
        session.randomizer = getRandomizerDefaultParameters()

def getCurrentMultiValues():
    defaultMultiValues = getDefaultMultiValues()
    for key in defaultMultiValues:
        keyMulti = key + 'MultiSelect'
        if keyMulti in session.randomizer:
            defaultMultiValues[key] = session.randomizer[keyMulti]
    return defaultMultiValues

def randomizer():
    response.title = 'Super Metroid VARIA Randomizer'

    initRandomizerSession()

    (stdPresets, tourPresets, comPresets) = loadPresetsList()
    (randoPresets, tourRandoPresets) = loadRandoPresetsList()
    # add empty entry for default value
    randoPresets.append("")

    randoPresetsDesc = {
        "all_random": "all the parameters set to random",
        "Chozo_Speedrun": "speedrun progression speed with Chozo split",
        "default": "VARIA randomizer default settings",
        "doors_long": "be prepared to hunt for beams and ammo to open doors",
        "doors_short": "uses Chozo/speedrun settings for a quicker door color rando",
        "free": "easiest possible settings",
        "hardway2hell": "harder highway2hell",
        "haste": "inspired by DASH randomizer with Nerfed Charge / Progressive Suits",
        "highway2hell": "favors suitless seeds",
        "minimizer":"Typical 'boss rush' settings with random start and nerfed charge",
        "minimizer_hardcore":"Have fun 'rushing' bosses with no equipment on a tiny map",
        "minimizer_maximizer":"No longer a boss rush",
        "quite_random": "randomizes a few significant settings to have various seeds",
        "stupid_hard": "hardest possible settings",
        "surprise": "quite_random with Area/Boss/Doors/Start settings randomized",
        "vanilla": "closest possible to vanilla Super Metroid",
        "way_of_chozo": "chozo split with boss randomization",
        "where_am_i": "Area mode with random start location and early morph",
        "where_is_morph": "Area mode with late Morph",
        "Season_Races": "rando league races (Majors/Minors split)",
        "Season_Races_Chozo": "rando league races (Chozo split)",
        "Playoff_Races": "rando league races during playoff (Majors/Minors split)",
        "Playoff_Races_Chozo": "rando league races during playoff (Chozo split)",
        "SMRAT2021": "Super Metroid Randomizer Accessible Tournament 2021",
        "VARIA_Weekly": "Casual logic community races"
    }

    startAPs = GraphUtils.getStartAccessPointNamesCategory()
    startAPs = [OPTGROUP(_label="Standard", *startAPs["regular"]),
                OPTGROUP(_label="Custom", *startAPs["custom"]),
                OPTGROUP(_label="Custom (Area rando only)", *startAPs["area"])]

    # get multi
    currentMultiValues = getCurrentMultiValues()
    defaultMultiValues = getDefaultMultiValues()

    return dict(stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets,
                randoPresets=randoPresets, tourRandoPresets=tourRandoPresets, randoPresetsDesc=randoPresetsDesc,
                startAPs=startAPs, currentMultiValues=currentMultiValues, defaultMultiValues=defaultMultiValues,
                maxsize=sys.maxsize)

def raiseHttp(code, msg, isJson=False):
    #print("raiseHttp: code {} msg {} isJson {}".format(code, msg, isJson))
    if isJson is True:
        msg = json.dumps(msg)

    raise HTTP(code, msg)

def getInt(param, isJson=False):
    try:
        return int(request.vars[param])
    except:
        raiseHttp(400, "Wrong value for {}, must be an int".format(param), isJson)

def getFloat(param, isJson=False):
    try:
        return float(request.vars[param])
    except:
        raiseHttp(400, "Wrong value for {}, must be a float".format(param), isJson)

def validateWebServiceParams(switchs, quantities, multis, others, isJson=False):
    parameters = switchs + quantities + multis + others

    for param in parameters:
        if request.vars[param] is None:
            raiseHttp(400, "Missing parameter: {}".format(param), isJson)

    # switchs
    for switch in switchs:
        if request.vars[switch] not in ['on', 'off', 'random']:
            raiseHttp(400, "Wrong value for {}, authorized values: on/off".format(switch), isJson)

    # quantities
    for qty in quantities:
        if request.vars[qty] == 'random':
            continue
        if qty == 'minimizerQty':
            if request.vars.minimizer == 'on':
                qtyInt = getInt(qty, isJson)
                if qtyInt < 30 or qtyInt > 100:
                    raiseHttp(400, "Wrong value for {}, must be between 30 and 100".format(qty), isJson)
        else:
            qtyFloat = getFloat(qty, isJson)
            if qtyFloat < 1.0 or qtyFloat > 9.0:
                raiseHttp(400, "Wrong value for {}, must be between 1 and 9".format(qty), isJson)

    # multis
    defaultMultiValues = getDefaultMultiValues()

    for param in multis:
        paramMulti = param+"MultiSelect"
        value = request.vars[param]
        if value == 'random':
            if request.vars[paramMulti] is not None:
                # get multi values
                for value in request.vars[paramMulti].split(','):
                    # check multi values
                    if value not in defaultMultiValues[param]:
                        raiseHttp(400, "Wrong value for {}, authorized values: {}".format(param, defaultMultiValues[param]), isJson)
        else:
            # check value
            if value not in defaultMultiValues[param]:
                raiseHttp(400, "Wrong value for {}, authorized values: {}".format(param, defaultMultiValues[param]), isJson)

    # others
    if request.vars.minorQty not in ['random', None]:
        minorQtyInt = getInt('minorQty', isJson)
        if minorQtyInt < 7 or minorQtyInt > 100:
            raiseHttp(400, "Wrong value for minorQty, must be between 7 and 100", isJson)

    if 'gravityBehaviour' in others:
        if request.vars.gravityBehaviour not in ['Balanced', 'Progressive', 'Vanilla']:
            raiseHttp(400, "Wrong value for gravityBehaviour", isJson)

    if 'complexity' in others:
        if request.vars['complexity'] not in ['simple', 'medium', 'advanced']:
            raiseHttp(400, "Wrong value for complexity, authorized values simple/medium/advanced", isJson)

    if 'paramsFileTarget' in others:
        try:
            json.loads(request.vars.paramsFileTarget)
        except:
            raiseHttp(400, "Wrong value for paramsFileTarget, must be a JSON string", isJson)

    if 'seed' in others:
        seedInt = getInt('seed', isJson)
        if seedInt < 0 or seedInt > sys.maxsize:
            raiseHttp(400, "Wrong value for seed", isJson)

    preset = request.vars.preset
    if preset != None:
        if IS_ALPHANUMERIC()(preset)[1] is not None:
            raiseHttp(400, "Wrong value for preset, must be alphanumeric", isJson)

        if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
            raiseHttp(400, "Wrong length for preset, name must be between 1 and 32 characters", isJson)

        # check that preset exists
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if not os.path.isfile(fullPath):
            raiseHttp(400, "Unknown preset", isJson)

    randoPreset = request.vars.randoPreset
    if randoPreset != None and len(randoPreset) > 0:
        if IS_ALPHANUMERIC()(randoPreset)[1] is not None:
            raiseHttp(400, "Wrong value for randoPreset, must be alphanumeric", isJson)

        if IS_LENGTH(maxsize=32, minsize=1)(randoPreset)[1] is not None:
            raiseHttp(400, "Wrong length for randoPreset, name must be between 1 and 32 characters", isJson)

        # check that randoPreset exists
        fullPath = 'rando_presets/{}.json'.format(randoPreset)
        if not os.path.isfile(fullPath):
            raiseHttp(400, "Unknown randoPreset", isJson)

    # check race mode
    if 'raceMode' in request.vars:
        if request.vars.raceMode not in ['on', 'off']:
            raiseHttp(400, "Wrong value for race mode, must on/off", isJson)

    # check seed key
    if 'seedKey' in request.vars:
        if IS_MATCH('^[0-9a-z-]*$')(request.vars.seedKey)[1] is not None:
            raiseHttp(400, "Seed key can only contain [0-9a-z-]", isJson)
        if IS_LENGTH(maxsize=36, minsize=36)(request.vars.seedKey)[1] is not None:
            raiseHttp(400, "Seed key must be 36 chars long", isJson)

def sessionWebService():
    # web service to update the session
    switchs = ['suitsRestriction', 'hideItems', 'strictMinors',
               'areaRandomization', 'areaLayout', 'lightAreaRandomization',
               'doorsColorsRando', 'allowGreyDoors', 'escapeRando', 'removeEscapeEnemies',
               'bossRandomization', 'minimizer', 'minimizerTourian',
               'funCombat', 'funMovement', 'funSuits',
               'layoutPatches', 'variaTweaks', 'nerfedCharge',
               'itemsounds', 'elevators_doors_speed', 'spinjumprestart',
               'rando_speed', 'animals', 'No_Music', 'random_music',
               'Infinite_Space_Jump', 'refill_before_save']
    quantities = ['missileQty', 'superQty', 'powerBombQty', 'minimizerQty']
    multis = ['majorsSplit', 'progressionSpeed', 'progressionDifficulty',
              'morphPlacement', 'energyQty', 'startLocation']
    others = ['complexity', 'preset', 'randoPreset', 'maxDifficulty', 'minorQty', 'gravityBehaviour']
    validateWebServiceParams(switchs, quantities, multis, others)

    if session.randomizer is None:
        session.randomizer = {}

    session.randomizer['complexity'] = request.vars.complexity
    session.randomizer['preset'] = request.vars.preset
    # after selecting a rando preset and changing an option users can end up
    # generating a seed with the rando preset selected but not with all
    # the options set with the rando preset, so always empty the rando preset
    session.randomizer['randoPreset'] = ""
    session.randomizer['maxDifficulty'] = request.vars.maxDifficulty
    session.randomizer['suitsRestriction'] = request.vars.suitsRestriction
    session.randomizer['hideItems'] = request.vars.hideItems
    session.randomizer['strictMinors'] = request.vars.strictMinors
    session.randomizer['missileQty'] = request.vars.missileQty
    session.randomizer['superQty'] = request.vars.superQty
    session.randomizer['powerBombQty'] = request.vars.powerBombQty
    session.randomizer['minorQty'] = request.vars.minorQty
    session.randomizer['areaRandomization'] = request.vars.areaRandomization
    session.randomizer['areaLayout'] = request.vars.areaLayout
    session.randomizer['lightAreaRandomization'] = request.vars.lightAreaRandomization
    session.randomizer['doorsColorsRando'] = request.vars.doorsColorsRando
    session.randomizer['allowGreyDoors'] = request.vars.allowGreyDoors
    session.randomizer['escapeRando'] = request.vars.escapeRando
    session.randomizer['removeEscapeEnemies'] = request.vars.removeEscapeEnemies
    session.randomizer['bossRandomization'] = request.vars.bossRandomization
    session.randomizer['minimizer'] = request.vars.minimizer
    session.randomizer['minimizerQty'] = request.vars.minimizerQty
    session.randomizer['minimizerTourian'] = request.vars.minimizerTourian
    session.randomizer['funCombat'] = request.vars.funCombat
    session.randomizer['funMovement'] = request.vars.funMovement
    session.randomizer['funSuits'] = request.vars.funSuits
    session.randomizer['layoutPatches'] = request.vars.layoutPatches
    session.randomizer['variaTweaks'] = request.vars.variaTweaks
    session.randomizer['gravityBehaviour'] = request.vars.gravityBehaviour
    session.randomizer['nerfedCharge'] = request.vars.nerfedCharge
    session.randomizer['itemsounds'] = request.vars.itemsounds
    session.randomizer['elevators_doors_speed'] = request.vars.elevators_doors_speed
    session.randomizer['spinjumprestart'] = request.vars.spinjumprestart
    session.randomizer['rando_speed'] = request.vars.rando_speed
    session.randomizer['animals'] = request.vars.animals
    session.randomizer['No_Music'] = request.vars.No_Music
    session.randomizer['random_music'] = request.vars.random_music
    session.randomizer['Infinite_Space_Jump'] = request.vars.Infinite_Space_Jump
    session.randomizer['refill_before_save'] = request.vars.refill_before_save

    multis = ['majorsSplit', 'progressionSpeed', 'progressionDifficulty',
              'morphPlacement', 'energyQty', 'startLocation']
    for multi in multis:
        session.randomizer[multi] = request.vars[multi]
        if request.vars[multi] == 'random':
            session.randomizer[multi+"MultiSelect"] = request.vars[multi+"MultiSelect"].split(',')

    # to create a new rando preset, uncomment next lines
    #with open('rando_presets/new.json', 'w') as jsonFile:
    #    json.dump(session.randomizer, jsonFile)

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

    session.forget(response)

    # set header to authorize cross domain AJAX
    response.headers['Access-Control-Allow-Origin'] = '*'

    # check validity of all parameters
    switchs = ['suitsRestriction', 'hideItems', 'strictMinors',
               'areaRandomization', 'areaLayout', 'lightAreaRandomization',
               'doorsColorsRando', 'allowGreyDoors', 'escapeRando', 'removeEscapeEnemies',
               'bossRandomization', 'minimizer', 'minimizerTourian',
               'funCombat', 'funMovement', 'funSuits',
               'layoutPatches', 'variaTweaks', 'nerfedCharge',
               'itemsounds', 'elevators_doors_speed', 'spinjumprestart',
               'rando_speed', 'animals', 'No_Music', 'random_music',
               'Infinite_Space_Jump', 'refill_before_save']
    quantities = ['missileQty', 'superQty', 'powerBombQty', 'minimizerQty']
    multis = ['majorsSplit', 'progressionSpeed', 'progressionDifficulty',
              'morphPlacement', 'energyQty', 'startLocation']
    others = ['complexity', 'paramsFileTarget', 'seed', 'preset', 'gravityBehaviour', 'maxDifficulty']
    validateWebServiceParams(switchs, quantities, multis, others, isJson=True)

    # randomize
    db = DB()
    id = db.initRando()

    # race mode
    useRace = False
    if request.vars.raceMode == 'on':
        magic = getMagic()
        useRace = True

    (fd1, presetFileName) = tempfile.mkstemp()
    presetFileName += '.json'
    (fd2, jsonFileName) = tempfile.mkstemp()

    print("randomizerWebService, params validated")
    for var in request.vars:
        print("{}: {}".format(var, request.vars[var]))

    with open(presetFileName, 'w') as presetFile:
        presetFile.write(request.vars.paramsFileTarget)

    if request.vars.seed == '0':
        request.vars.seed = str(random.randrange(sys.maxsize))

    preset = request.vars.preset

    params = [pythonExec,  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
              '--runtime', '20',
              '--seed', request.vars.seed,
              '--output', jsonFileName,
              '--param', presetFileName,
              '--preset', preset]
    params += ['--missileQty', request.vars.missileQty if request.vars.missileQty != 'random' else '0',
               '--superQty', request.vars.superQty if request.vars.superQty != 'random' else '0',
               '--powerBombQty', request.vars.powerBombQty if request.vars.powerBombQty != 'random' else '0',
               '--minorQty', request.vars.minorQty if request.vars.minorQty != 'random' else '0']

    for multi in multis:
        params += ["--{}".format(multi), request.vars[multi]]
        if request.vars[multi] == 'random':
            params += ["--{}List".format(multi), request.vars[multi+"MultiSelect"]]

    if request.vars.maxDifficulty != 'no difficulty cap':
        params.append('--maxDifficulty')
        params.append(request.vars.maxDifficulty)

    if useRace == True:
        params += ['--race', str(magic)]

    if request.vars.nerfedCharge == 'on':
        params.append('--nerfedCharge')

    if request.vars.itemsounds == 'on':
        params += ['-c', 'itemsounds.ips']
    if request.vars.elevators_doors_speed == 'on':
        params += ['-c', 'elevators_doors_speed.ips']
    if request.vars.spinjumprestart == 'on':
        params += ['-c', 'spinjumprestart.ips']
    if request.vars.rando_speed == 'on':
        params += ['-c', 'rando_speed.ips']
    if request.vars.No_Music == 'on':
        params += ['-c', 'No_Music']
    if request.vars.random_music == 'on':
        params += ['-c', 'random_music.ips']
    if request.vars.Infinite_Space_Jump == 'on':
        params += ['-c', 'Infinite_Space_Jump']
    if request.vars.refill_before_save == 'on':
        params += ['-c', 'refill_before_save.ips']

    if request.vars.animals == 'on':
        params.append('--animals')
    if request.vars.variaTweaks == 'off':
        params.append('--novariatweaks')

    def addParamRandom(id, params):
        if request.vars[id] in ['on', 'random']:
            params.append('--{}'.format(id))
        if request.vars[id] == 'random':
            params.append('random')

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


    if request.vars.gravityBehaviour == 'Vanilla':
        params.append('--nogravheat')
    elif request.vars.gravityBehaviour == 'Progressive':
        params.append('--progressiveSuits')

    if request.vars.areaRandomization == 'on':
        params.append('--area')
        if request.vars.areaLayout == 'off':
            params.append('--areaLayoutBase')
        if request.vars.lightAreaRandomization == 'on':
            params.append('--lightArea')
    elif request.vars.areaRandomization == 'random':
        params += ['--area', 'random']

    if request.vars.doorsColorsRando == 'on':
        params.append('--doorsColorsRando')
    elif request.vars.doorsColorsRando == 'random':
        params += ['--doorsColorsRando', 'random']
    if request.vars.allowGreyDoors == 'on':
        params.append('--allowGreyDoors')

    if request.vars.escapeRando == 'on':
        params.append('--escapeRando')
        if request.vars.removeEscapeEnemies == 'off':
            params.append('--noRemoveEscapeEnemies')
    elif request.vars.escapeRando == 'random':
        params += ['--escapeRando', 'random']

    if request.vars.bossRandomization == 'on':
        params.append('--bosses')
    elif request.vars.bossRandomization == 'random':
        params += ['--bosses', 'random']

    if request.vars.minimizer == 'on':
        params += ['--minimizer', request.vars.minimizerQty]
    if request.vars.minimizerTourian == 'on':
        params.append('--minimizerTourian')

    # load content of preset to get controller mapping
    try:
        controlMapping = PresetLoader.factory(presetFileName).params['Controller']
    except Exception as e:
        os.close(fd1)
        os.remove(presetFileName)
        os.close(fd2)
        os.remove(jsonFileName)
        raise HTTP(400, json.dumps("randomizerWebService: can't load the preset"))

    (custom, controlParam) = getCustomMapping(controlMapping)
    if custom == True:
        params += ['--controls', controlParam]
        if "Moonwalk" in controlMapping and controlMapping["Moonwalk"] == True:
            params.append('--moonwalk')

    db.addRandoParams(id, request.vars)

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
            if msg[0] == '\n':
                msg = msg[1:]
            locsItems['errorMsg'] = msg.replace('\n', '<br/>')

        db.addRandoResult(id, ret, duration, msg)

        if "forcedArgs" in locsItems:
            db.updateRandoParams(id, locsItems["forcedArgs"])

        # store ips in local directory
        guid = str(uuid.uuid4())
        if storeLocalIps(guid, locsItems["fileName"], locsItems["ips"]):
            db.addRandoUploadResult(id, guid, locsItems["fileName"])
            locsItems['seedKey'] = guid
        db.close()

        os.close(fd1)
        os.remove(presetFileName)
        os.close(fd2)
        os.remove(jsonFileName)

        return json.dumps(locsItems)
    else:
        # extract error from json
        try:
            with open(jsonFileName) as jsonFile:
                msg = json.load(jsonFile)['errorMsg']
                if msg[0] == '\n':
                    msg = msg[1:]
                    msg = msg.replace('\n', '<br/>')
        except:
            msg = "randomizerWebService: something wrong happened"

        db.addRandoResult(id, ret, duration, msg)
        db.close()

        os.close(fd1)
        os.remove(presetFileName)
        os.close(fd2)
        os.remove(jsonFileName)
        raise HTTP(400, json.dumps(msg))

def storeLocalIps(key, fileName, ipsData):
    try:
        ipsDir = os.path.join(localIpsDir, str(key))
        os.makedirs(ipsDir, mode=0o755, exist_ok=True)

        # extract ipsData
        ips = base64.b64decode(ipsData)

        # write ips as key/fileName.ips
        ipsFileName = fileName.replace('sfc', 'ips')
        ipsLocal = os.path.join(ipsDir, ipsFileName)
        with open(ipsLocal, 'wb') as f:
            f.write(ips)

        return True
    except:
        return False

def presetWebService():
    # web service to get the content of the preset file
    if request.vars.preset == None:
        raiseHttp(400, "Missing parameter preset")
    preset = request.vars.preset

    if IS_ALPHANUMERIC()(preset)[1] is not None:
        raise HTTP(400, "Preset name must be alphanumeric")

    if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
        raise HTTP(400, "Preset name must be between 1 and 32 characters")

    print("presetWebService: preset={}".format(preset))

    fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)

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
        raise HTTP(400, "Preset not found")

def randoPresetWebService():
    # web service to get the content of the rando preset file
    if request.vars.randoPreset == None:
        raiseHttp(400, "Missing parameter rando preset")
    preset = request.vars.randoPreset

    if IS_ALPHANUMERIC()(preset)[1] is not None:
        raise HTTP(400, "Preset name must be alphanumeric")

    if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
        raise HTTP(400, "Preset name must be between 1 and 32 characters")

    if request.vars.origin not in ["extStats", "randomizer"]:
        raise HTTP(400, "Unknown origin")

    print("randoPresetWebService: preset={}".format(preset))

    fullPath = 'rando_presets/{}.json'.format(preset)

    # check that the presets file exists
    if os.path.isfile(fullPath):
        # load it
        try:
            # can be called from randomizer and extended stats pages
            updateSession = request.vars.origin == "randomizer"

            params = loadRandoPreset(fullPath, updateSession)
            params = json.dumps(params)
            return params
        except Exception as e:
            raise HTTP(400, "Can't load the rando preset")
    else:
        raise HTTP(400, "Rando preset not found")

def loadRandoPreset(presetFullPath, updateSession):
    with open(presetFullPath) as jsonFile:
        randoPreset = json.load(jsonFile)

    # update session
    if updateSession == True:
        for key in randoPreset:
            session.randomizer[key] = randoPreset[key]

    return randoPreset

def home():
    # set title
    response.title = 'Super Metroid VARIA Randomizer, Solver and Trackers'

    return dict()

def addError(state, params, tmpErr):
    errDir = os.path.expanduser("~/web2py/applications/solver/errors")
    if os.path.isdir(errDir):
        errFile = '{}.{}.{}'.format(request.client, datetime.now().strftime('%Y-%m-%d.%H-%M-%S'), str(uuid.uuid4()))
        errFile = os.path.join(errDir, errFile)
        with open(state) as f:
            stateContent = f.read()
        with open(tmpErr) as f:
            errContent = f.read()
        with open(errFile, 'w') as f:
            f.write(str(params)+'\n')
            f.write(str(stateContent)+'\n')
            f.write(errContent)

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

def getFsUsage():
    fsData = os.statvfs('/home')
    percent = round(100 - (100.0 * fsData.f_bavail / fsData.f_blocks), 2)
    if percent < 80:
        return ('OK', percent)
    elif percent < 95:
        return ('WARNING', percent)
    else:
        return ('CRITICAL', percent)

def randoParamsWebService():
    # get a json string of the randomizer parameters for a given seed
    if request.vars.seed == None:
        raiseHttp(400, "Missing parameter seed", False)

    seed = getInt('seed', False)
    if seed < 0 or seed > 9999999:
        raiseHttp(400, "Wrong value for seed, must be between 0 and 9999999", False)

    db = DB()
    (seed, params) = db.getRandomizerSeedParams(seed)
    db.close()

    return json.dumps({"seed": seed, "params": params})

def stats():
    response.title = 'Super Metroid VARIA Randomizer and Solver usage statistics'

    db = DB()
    weeks = 1

    solverPresets = db.getSolverPresets(weeks)
    randomizerPresets = db.getRandomizerPresets(weeks)

    solverDurations = db.getSolverDurations(weeks)
    randomizerDurations = db.getRandomizerDurations(weeks)

    solverData = db.getSolverData(weeks)
    randomizerData = db.getRandomizerData(weeks)

    isolver = db.getISolver(weeks)
    isolverData = db.getISolverData(weeks)

    errors = getErrors()

    db.close()

    (fsStatus, fsPercent) = getFsUsage()

    return dict(solverPresets=solverPresets, randomizerPresets=randomizerPresets,
                solverDurations=solverDurations, randomizerDurations=randomizerDurations,
                solverData=solverData, randomizerData=randomizerData,
                isolver=isolver, isolverData=isolverData, errors=errors,
                fsStatus=fsStatus, fsPercent=fsPercent)

def transition2isolver(transition):
    transition = str(transition)
    return transition[0].lower() + removeChars(transition[1:], " ,()-")

def tracker():
    response.title = 'Super Metroid VARIA Areas and Items Tracker'

    # init session
    if session.tracker is None:
        session.tracker = {}

        session.tracker["state"] = {}
        session.tracker["preset"] = "regular"
        session.tracker["seed"] = None
        session.tracker["startLocation"] = "Landing Site"

        # set to False in tracker.html
        session.tracker["firstTime"] = True

    # load presets list
    (stdPresets, tourPresets, comPresets) = loadPresetsList()

    # access points
    vanillaAPs = []
    for (src, dest) in vanillaTransitions:
        vanillaAPs += [transition2isolver(src), transition2isolver(dest)]

    vanillaBossesAPs = []
    for (src, dest) in vanillaBossesTransitions:
        vanillaBossesAPs += [transition2isolver(src), transition2isolver(dest)]

    escapeAPs = []
    for (src, dest) in vanillaEscapeTransitions:
        escapeAPs += [transition2isolver(src), transition2isolver(dest)]

    # generate list of addresses to read in the ROM
    addresses = getAddressesToRead()

    startAPs = GraphUtils.getStartAccessPointNamesCategory()
    startAPs = [OPTGROUP(_label="Standard", *startAPs["regular"]),
                OPTGROUP(_label="Custom", *startAPs["custom"]),
                OPTGROUP(_label="Custom (Area rando only)", *startAPs["area"])]

    return dict(stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets,
                vanillaAPs=vanillaAPs, vanillaBossesAPs=vanillaBossesAPs, escapeAPs=escapeAPs,
                curSession=session.tracker, addresses=addresses, startAPs=startAPs)

def plando():
    response.title = 'Super Metroid VARIA Areas and Items Plandomizer'

    # init session
    if session.plando is None:
        session.plando = {}

        session.plando["state"] = {}
        session.plando["preset"] = "regular"
        session.plando["seed"] = None
        session.plando["startLocation"] = "Landing Site"

        # rando params
        session.plando["rando"] = {}

        # set to False in plando.html
        session.plando["firstTime"] = True

    # load presets list
    (stdPresets, tourPresets, comPresets) = loadPresetsList()

    # access points
    vanillaAPs = []
    for (src, dest) in vanillaTransitions:
        vanillaAPs += [transition2isolver(src), transition2isolver(dest)]

    vanillaBossesAPs = []
    for (src, dest) in vanillaBossesTransitions:
        vanillaBossesAPs += [transition2isolver(src), transition2isolver(dest)]

    escapeAPs = []
    for (src, dest) in vanillaEscapeTransitions:
        escapeAPs += [transition2isolver(src), transition2isolver(dest)]

    # generate list of addresses to read in the ROM
    addresses = getAddressesToRead(plando=True)

    startAPs = GraphUtils.getStartAccessPointNamesCategory()
    startAPs = [OPTGROUP(_label="Standard", *startAPs["regular"]),
                OPTGROUP(_label="Custom", *startAPs["custom"]),
                OPTGROUP(_label="Custom (Area rando only)", *startAPs["area"])]

    return dict(stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets,
                vanillaAPs=vanillaAPs, vanillaBossesAPs=vanillaBossesAPs, escapeAPs=escapeAPs,
                curSession=session.plando, addresses=addresses, startAPs=startAPs)

class WS(object):
    @staticmethod
    def factory():
        scope = request.vars.scope
        if scope not in ["area", "item", "common", "door"]:
            raiseHttp(400, "Unknown scope, must be area/item/common/door", True)

        action = request.vars.action
        if action not in ['add', 'remove', 'toggle', 'clear', 'init', 'get', 'save', 'replace', 'randomize']:
            raiseHttp(400, "Unknown action, must be add/remove/toggle/clear/init/get/save/randomize", True)

        mode = request.vars.mode
        if mode not in ["standard", "seedless", "plando", "race", "debug"]:
            raiseHttp(400, "Unknown mode, must be standard/seedless/plando/race/debug", True)

        try:
            WSClass = globals()["WS_{}_{}".format(scope, action)]
            return WSClass(mode)
        except Exception as e:
            raiseHttp(400, "{}".format(e.body if "body" in e.__dict__ else e).replace('"', ''), True)

    def __init__(self, mode):
        self.mode = mode
        if self.mode in ["plando", "debug"]:
            if session.plando is None:
                raiseHttp(400, "No session found for the Plandomizer Web service", True)
            self.session = session.plando
        else:
            if session.tracker is None:
                raiseHttp(400, "No session found for the Tracker Web service", True)
            self.session = session.tracker

    def validate(self):
        if self.session is None:
            raiseHttp(400, "No session found for the Tracker", True)

        if request.vars.action == None:
            raiseHttp(400, "Missing parameter action", True)
        action = request.vars.action

        if action not in ['init', 'add', 'remove', 'clear', 'get', 'save', 'replace', 'randomize', 'toggle']:
            raiseHttp(400, "Unknown action, must be init/add/remove/toggle/clear/get/save/randomize", True)

        if request.vars.escapeTimer != None:
            if re.match("[0-9][0-9]:[0-9][0-9]", request.vars.escapeTimer) == None:
                raiseHttp(400, "Wrong escape timer value")

    def validatePoint(self, point):
        if request.vars[point] == None:
            raiseHttp(400, "Missing parameter {}".format(point), True)

        pointValue = request.vars[point]

        if pointValue not in ['lowerMushroomsLeft', 'moatRight', 'greenPiratesShaftBottomRight',
                              'keyhunterRoomBottom', 'morphBallRoomLeft', 'greenBrinstarElevator',
                              'greenHillZoneTopRight', 'noobBridgeRight', 'westOceanLeft', 'crabMazeLeft',
                              'lavaDiveRight', 'threeMuskateersRoomLeft', 'warehouseZeelaRoomLeft',
                              'warehouseEntranceLeft', 'warehouseEntranceRight', 'singleChamberTopRight',
                              'kronicBoostRoomBottomLeft', 'mainStreetBottom', 'crabHoleBottomLeft', 'leCoudeRight',
                              'redFishRoomLeft', 'redTowerTopLeft', 'caterpillarRoomTopRight', 'redBrinstarElevator',
                              'eastTunnelRight', 'eastTunnelTopRight', 'glassTunnelTop', 'goldenFour',
                              'ridleyRoomOut', 'ridleyRoomIn', 'kraidRoomOut', 'kraidRoomIn',
                              'draygonRoomOut', 'draygonRoomIn', 'phantoonRoomOut', 'phantoonRoomIn',
                              'tourianEscapeRoom4TopRight', 'climbBottomLeft', 'greenBrinstarMainShaftTopLeft',
                              'basementLeft', 'businessCenterMidLeft', 'crabHoleBottomRight', 'crocomireRoomTop',
                              'crocomireSpeedwayBottom', 'crabShaftRight', 'aqueductTopLeft']:
            raiseHttp(400, "Wrong value for {}".format(point), True)

    def action(self):
        pass

    def locName4isolver(self, locName):
        # remove space and special characters
        # sed -e 's+ ++g' -e 's+,++g' -e 's+(++g' -e 's+)++g' -e 's+-++g'
        locName = str(locName)
        return locName[0].lower() + removeChars(locName[1:], " ,()-")

    def returnState(self):
        if len(self.session["state"]) > 0:
            state = self.session["state"]
            #print("state returned to frontend: availWeb {}, visWeb {}".format(state["availableLocationsWeb"], state["visitedLocationsWeb"]))
            return json.dumps({
                # item tracker
                "availableLocations": state["availableLocationsWeb"],
                "visitedLocations": state["visitedLocationsWeb"],
                "collectedItems": state["collectedItems"],
                # compatibility with existing sessions
                "remainLocations": state["remainLocationsWeb"] if "remainLocationsWeb" in state else [],
                "lastAP": self.locName4isolver(state["lastAP"]),

                # area tracker
                "lines": state["linesWeb"],
                "linesSeq": state["linesSeqWeb"],
                "allTransitions": state["allTransitions"],

                # infos on seed
                "mode": state["mode"],
                "areaRando": state["areaRando"],
                "bossRando": state["bossRando"],
                "hasMixedTransitions": state["hasMixedTransitions"],
                "escapeRando": state["escapeRando"],
                "escapeTimer": state["escapeTimer"],
                "seed": state["seed"],
                "preset": os.path.basename(os.path.splitext(state["presetFileName"])[0]),
                "errorMsg": state["errorMsg"],
                "last": state["last"],
                "innerTransitions": state["innerTransitions"],
                "doors": state["doors"],
                "doorsRando": state["doorsRando"]
            })
        else:
            raiseHttp(200, "OK", True)

    def callSolverAction(self, scope, action, parameters):
        # check that we have a state in the session
        if "state" not in self.session:
            raiseHttp(400, "Missing Solver state in the session", True)

        (fd1, jsonInFileName) = tempfile.mkstemp()
        (fd2, jsonOutFileName) = tempfile.mkstemp()
        (fd3, errFile) = tempfile.mkstemp()
        params = [
            pythonExec,  os.path.expanduser("~/RandomMetroidSolver/solver.py"),
            '--interactive',
            '--state',  jsonInFileName,
            '--output', jsonOutFileName,
            '--action', action,
            '--mode', self.mode,
            '--scope', scope
        ]
        if action in ['add', 'replace']:
            if scope == 'item':
                if 'loc' in parameters:
                    params += ['--loc', parameters["loc"]]
                if self.mode != 'standard':
                    params += ['--item', parameters["item"]]
                    if parameters['hide'] == True:
                        params.append('--hide')
            elif scope == 'area':
                params += ['--startPoint', parameters["startPoint"],
                           '--endPoint', parameters["endPoint"]]
            elif scope == 'door':
                params += ['--doorName', parameters["doorName"],
                           '--newColor', parameters["newColor"]]
        elif action == 'remove' and scope == 'item':
            if 'loc' in parameters:
                params += ['--loc', parameters["loc"]]
            elif 'count' in parameters:
                params += ['--count', str(parameters["count"])]
            else:
                params += ['--item', str(parameters["item"])]
        elif action == 'toggle':
            if scope == 'item':
                params += ['--item', parameters['item']]
            elif scope == 'door':
                params += ['--doorName', parameters["doorName"]]
        elif action == 'remove' and scope == 'area' and "startPoint" in parameters:
            params += ['--startPoint', parameters["startPoint"]]
        elif action == 'save' and scope == 'common':
            if parameters['lock'] == True:
                params.append('--lock')
            if 'escapeTimer' in parameters:
                params += ['--escapeTimer', parameters['escapeTimer']]
        elif action == 'randomize':
            params += ['--minorQty', parameters["minorQty"],
                       '--energyQty', parameters["energyQty"]
            ]
            if "forbiddenItems" in parameters:
                params += ['--forbiddenItems', parameters["forbiddenItems"]]

        # dump state as input
        with open(jsonInFileName, 'w') as jsonFile:
            json.dump(self.session["state"], jsonFile)

        print("before calling isolver: {}".format(params))
        start = datetime.now()
        ret = subprocess.call(params, stderr=fd3)
        end = datetime.now()
        duration = (end - start).total_seconds()
        print("ret: {}, duration: {}s".format(ret, duration))

        if ret == 0:
            with open(jsonOutFileName) as jsonFile:
                state = json.load(jsonFile)
            os.close(fd1)
            os.remove(jsonInFileName)
            os.close(fd2)
            os.remove(jsonOutFileName)
            os.close(fd3)
            os.remove(errFile)
            if action == 'save':
                return json.dumps(state)
            else:
                # save the escape timer at every step to avoid loosing its value
                if request.vars.escapeTimer != None:
                    state["escapeTimer"] = request.vars.escapeTimer

                self.session["state"] = state
                return self.returnState()
        else:
            msg = "Something wrong happened while iteratively solving the ROM"
            try:
                addError(jsonInFileName, params, errFile)
                with open(jsonOutFileName, 'r') as jsonFile:
                    data = json.load(jsonFile)
                    if "errorMsg" in data:
                        msg = data["errorMsg"]
            except Exception as e:
                # happen when jsonOutFileName is empty
                pass
            os.close(fd1)
            os.remove(jsonInFileName)
            os.close(fd2)
            os.remove(jsonOutFileName)
            os.close(fd3)
            os.remove(errFile)
            raiseHttp(400, msg, True)

class WS_common_init(WS):
    def validate(self):
        super(WS_common_init, self).validate()

        if request.vars.scope != 'common':
            raiseHttp(400, "Unknown scope, must be common", True)

        # preset
        preset = request.vars.preset
        if request == None:
            raiseHttp(400, "Missing parameter preset", True)
        if IS_NOT_EMPTY()(preset)[1] is not None:
            raiseHttp(400, "Preset name is empty", True)
        if IS_ALPHANUMERIC()(preset)[1] is not None:
            raiseHttp(400, "Preset name must be alphanumeric", True)
        if IS_LENGTH(32)(preset)[1] is not None:
            raiseHttp(400, "Preset name must be max 32 chars", True)
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if not os.path.isfile(fullPath):
            raiseHttp(400, "Unknown preset", True)

        if request.vars.mode != 'seedless':
            # ROM (only through file API)
            if request.vars.romJson is None or len(request.vars.romJson) == 0:
                raiseHttp(400, "Missing ROM to solve", True)
            try:
                json.loads(request.vars.romJson)
            except:
                raiseHttp(400, "Wrong value for romJson, must be a JSON string")

            # ROM file name
            uploadFile = request.vars.fileName
            if uploadFile is None:
                raiseHttp(400, "Missing ROM file name", True)
            if IS_NOT_EMPTY()(uploadFile)[1] is not None:
                raiseHttp(400, "File name is empty", True)
            if IS_LENGTH(maxsize=255, minsize=1)(uploadFile)[1] is not None:
                raiseHttp(400, "Wrong length for ROM file name, name must be between 1 and 255 characters", True)

        if request.vars.startLocation != None:
            if request.vars.startLocation not in GraphUtils.getStartAccessPointNames():
                raiseHttp(400, "Wrong value for startLocation", True)

    def action(self):
        mode = request.vars.mode
        if mode != 'seedless':
            try:
                (base, jsonRomFileName) = generateJsonROM(request.vars.romJson)
            except Exception as e:
                raiseHttp(400, "Can't load JSON ROM: {}".format(e), True)
            seed = base + '.sfc'
            startLocation = None
        else:
            seed = 'seedless'
            jsonRomFileName = None
            startLocation = request.vars.startLocation

        preset = request.vars.preset
        presetFileName = '{}/{}.json'.format(getPresetDir(preset), preset)

        self.session["seed"] = seed
        self.session["preset"] = preset
        self.session["mode"] = mode
        self.session["startLocation"] = startLocation if startLocation != None else "Landing Site"

        fill = request.vars.fill == "true"

        return self.callSolverInit(jsonRomFileName, presetFileName, preset, seed, mode, fill, startLocation)

    def callSolverInit(self, jsonRomFileName, presetFileName, preset, romFileName, mode, fill, startLocation):
        (fd, jsonOutFileName) = tempfile.mkstemp()
        params = [
            pythonExec,  os.path.expanduser("~/RandomMetroidSolver/solver.py"),
            '--preset', presetFileName,
            '--output', jsonOutFileName,
            '--action', "init",
            '--interactive',
            '--mode', mode,
            '--scope', 'common'
        ]

        if mode != "seedless":
            params += ['-r', str(jsonRomFileName)]

        if fill == True:
            params.append('--fill')

        if startLocation != None:
            params += ['--startAP', startLocation]

        print("before calling isolver: {}".format(params))
        start = datetime.now()
        ret = subprocess.call(params)
        end = datetime.now()
        duration = (end - start).total_seconds()
        print("ret: {}, duration: {}s".format(ret, duration))

        if ret == 0:
            db = DB()
            db.addISolver(preset, romFileName)
            db.close()

            with open(jsonOutFileName) as jsonFile:
                state = json.load(jsonFile)
            os.close(fd)
            os.remove(jsonOutFileName)
            self.session["state"] = state
            return self.returnState()
        else:
            os.close(fd)
            os.remove(jsonOutFileName)
            raiseHttp(400, "Something wrong happened while initializing the ISolver", True)

class WS_common_get(WS):
    def validate(self):
        super(WS_common_get, self).validate()

    def action(self):
        return self.returnState()

class WS_common_save(WS):
    def validate(self):
        super(WS_common_save, self).validate()

        if request.vars.lock == None:
            raiseHttp(400, "Missing parameter lock", True)

        if request.vars.lock not in ["save", "lock"]:
            raiseHttp(400, "Wrong value for lock, authorized values: save/lock", True)

    def action(self):
        if self.session["mode"] != "plando":
            raiseHttp(400, "Save can only be use in plando mode", True)

        params = {'lock': request.vars.lock == "lock"}
        if request.vars.escapeTimer != None:
            params['escapeTimer'] = request.vars.escapeTimer

        return self.callSolverAction("common", "save", params)

class WS_common_randomize(WS):
    def validate(self):
        super(WS_common_randomize, self).validate()

        minorQtyInt = getInt('minorQty', True)
        if minorQtyInt < 7 or minorQtyInt > 100:
            raiseHttp(400, "Wrong value for minorQty, must be between 7 and 100", True)
        if request.vars.energyQty not in ["sparse", "medium", "vanilla"]:
            raiseHttp(400, "Wrong value for energyQty", True)
        if request.vars.forbiddenItems != '':
            forbiddenItems = request.vars.forbiddenItems.split(',')
            validItems = set(["Charge", "Ice", "Wave", "Spazer", "Plasma", "Varia", "Gravity", "Morph", "Bomb", "SpringBall", "ScrewAttack", "HiJump", "SpaceJump", "SpeedBooster", "Grapple", "XRayScope", "ETank", "Reserve", "Missile", "Super", "PowerBomb"])
            for item in forbiddenItems:
                if item not in validItems:
                    raiseHttp(400, "Wrong value for forbidden items", True)

    def action(self):
        if self.session["mode"] != "plando":
            raiseHttp(400, "Randomize can only be use in plando mode", True)

        params = {}
        for elem in "minorQty", "energyQty":
            params[elem] = request.vars[elem]
        if request.vars.forbiddenItems != '':
            params["forbiddenItems"] = request.vars.forbiddenItems

        self.session["rando"] = params

        return self.callSolverAction("common", "randomize", params)

class WS_area_add(WS):
    def validate(self):
        super(WS_area_add, self).validate()

        # startPoint and endPoint
        self.validatePoint("startPoint")
        self.validatePoint("endPoint")

        if len(self.session["state"]) == 0:
            raiseHttp(400, "ISolver state is empty", True)

    def action(self):
        return self.callSolverAction("area", "add", {"startPoint": request.vars.startPoint,
                                                     "endPoint": request.vars.endPoint})

class WS_area_remove(WS):
    def validate(self):
        if request.vars["startPoint"] != None:
            self.validatePoint("startPoint")

        super(WS_area_remove, self).validate()

    def action(self):
        parameters = {}
        if request.vars["startPoint"] != None:
            parameters["startPoint"] = request.vars.startPoint

        return self.callSolverAction("area", "remove", parameters)

class WS_area_clear(WS):
    def validate(self):
        super(WS_area_clear, self).validate()

    def action(self):
        return self.callSolverAction("area", "clear", {})

validItemsList = [None, 'ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack', 'Nothing', 'NoEnergy', 'Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']
validLocsList = ['EnergyTankGauntlet', 'Bomb', 'EnergyTankTerminator', 'ReserveTankBrinstar', 'ChargeBeam', 'MorphingBall', 'EnergyTankBrinstarCeiling', 'EnergyTankEtecoons', 'EnergyTankWaterway', 'EnergyTankBrinstarGate', 'XRayScope', 'Spazer', 'EnergyTankKraid', 'VariaSuit', 'IceBeam', 'EnergyTankCrocomire', 'HiJumpBoots', 'GrappleBeam', 'ReserveTankNorfair', 'SpeedBooster', 'WaveBeam', 'EnergyTankRidley', 'ScrewAttack', 'EnergyTankFirefleas', 'ReserveTankWreckedShip', 'EnergyTankWreckedShip', 'RightSuperWreckedShip', 'GravitySuit', 'EnergyTankMamaturtle', 'PlasmaBeam', 'ReserveTankMaridia', 'SpringBall', 'EnergyTankBotwoon', 'SpaceJump', 'PowerBombCrateriasurface', 'MissileoutsideWreckedShipbottom', 'MissileoutsideWreckedShiptop', 'MissileoutsideWreckedShipmiddle', 'MissileCrateriamoat', 'MissileCrateriabottom', 'MissileCrateriagauntletright', 'MissileCrateriagauntletleft', 'SuperMissileCrateria', 'MissileCrateriamiddle', 'PowerBombgreenBrinstarbottom', 'SuperMissilepinkBrinstar', 'MissilegreenBrinstarbelowsupermissile', 'SuperMissilegreenBrinstartop', 'MissilegreenBrinstarbehindmissile', 'MissilegreenBrinstarbehindreservetank', 'MissilepinkBrinstartop', 'MissilepinkBrinstarbottom', 'PowerBombpinkBrinstar', 'MissilegreenBrinstarpipe', 'PowerBombblueBrinstar', 'MissileblueBrinstarmiddle', 'SuperMissilegreenBrinstarbottom', 'MissileblueBrinstarbottom', 'MissileblueBrinstartop', 'MissileblueBrinstarbehindmissile', 'PowerBombredBrinstarsidehopperroom', 'PowerBombredBrinstarspikeroom', 'MissileredBrinstarspikeroom', 'MissileKraid', 'Missilelavaroom', 'MissilebelowIceBeam', 'MissileaboveCrocomire', 'MissileHiJumpBoots', 'EnergyTankHiJumpBoots', 'PowerBombCrocomire', 'MissilebelowCrocomire', 'MissileGrappleBeam', 'MissileNorfairReserveTank', 'MissilebubbleNorfairgreendoor', 'MissilebubbleNorfair', 'MissileSpeedBooster', 'MissileWaveBeam', 'MissileGoldTorizo', 'SuperMissileGoldTorizo', 'MissileMickeyMouseroom', 'MissilelowerNorfairabovefireflearoom', 'PowerBomblowerNorfairabovefireflearoom', 'PowerBombPowerBombsofshame', 'MissilelowerNorfairnearWaveBeam', 'MissileWreckedShipmiddle', 'MissileGravitySuit', 'MissileWreckedShiptop', 'SuperMissileWreckedShipleft', 'MissilegreenMaridiashinespark', 'SuperMissilegreenMaridia', 'MissilegreenMaridiatatori', 'SuperMissileyellowMaridia', 'MissileyellowMaridiasupermissile', 'MissileyellowMaridiafalsewall', 'MissileleftMaridiasandpitroom', 'MissilerightMaridiasandpitroom', 'PowerBombrightMaridiasandpitroom', 'MissilepinkMaridia', 'SuperMissilepinkMaridia', 'MissileDraygon', 'Kraid', 'Ridley', 'Phantoon', 'Draygon', 'MotherBrain']

def name4isolver(locName):
    # remove space and special characters
    # sed -e 's+ ++g' -e 's+,++g' -e 's+(++g' -e 's+)++g' -e 's+-++g'
    return removeChars(locName, " ,()-")

class WS_item_add(WS):
    def validate(self):
        super(WS_item_add, self).validate()

        # new location
        if request.vars.locName != None:
            locName = name4isolver(request.vars.locName)

            if locName not in validLocsList:
                raiseHttp(400, "Unknown location name", True)

            request.vars.locName = locName

        itemName = request.vars.itemName
        if itemName == "NoEnergy":
            itemName = "Nothing"

        if itemName not in validItemsList:
            raiseHttp(400, "Unknown item name", True)


    def action(self):
        item = request.vars.itemName
        locName = request.vars.locName

        # items used only in the randomizer that we get in vcr mode
        if item in ["NoEnergy", None]:
            item = 'Nothing'

        # in seedless mode we have to had boss items instead of nothing
        if request.vars.mode in ["seedless", "race", "debug"]:
            if locName in ['Kraid', 'Ridley', 'Phantoon', 'Draygon', 'MotherBrain']:
                item = locName

        params = {"item": item, "hide": request.vars.hide == "true"}
        if locName != None:
            params['loc'] = locName
        return self.callSolverAction("item", "add", params)

class WS_item_replace(WS_item_add):
    def validate(self):
        super(WS_item_replace, self).validate()

    def action(self):
        return self.callSolverAction("item", "replace", {"loc": request.vars.locName, "item": request.vars.itemName, "hide": request.vars.hide == "true"})

class WS_item_toggle(WS_item_add):
    def validate(self):
        super(WS_item_toggle, self).validate()

        if request.vars.itemName not in validItemsList:
            raiseHttp(400, "Unknown item name", True)

    def action(self):
        return self.callSolverAction("item", "toggle", {"item": request.vars.itemName})

class WS_item_remove(WS):
    def validate(self):
        super(WS_item_remove, self).validate()

        if request.vars.itemName not in validItemsList:
            raiseHttp(400, "Unknown item name", True)

        self.itemName = request.vars.itemName
        if self.itemName == None:
            if request.vars.count != None:
                self.count = getInt("count", True)
                if self.count > 105 or self.count < 1:
                    raiseHttp(400, "Wrong value for count, must be in [1-105] ", True)
            else:
                self.count = 1
        else:
            self.count = -1

        self.locName = request.vars.locName
        if self.locName != None:
            self.locName = name4isolver(self.locName)

            if self.locName not in validLocsList:
                raiseHttp(400, "Unknown location name", True)

    def action(self):
        if self.locName != None:
            return self.callSolverAction("item", "remove", {"loc": self.locName})
        else:
            if self.itemName != None:
                return self.callSolverAction("item", "remove", {"item": self.itemName})
            else:
                return self.callSolverAction("item", "remove", {"count": self.count})

class WS_item_clear(WS):
    def validate(self):
        super(WS_item_clear, self).validate()

    def action(self):
        return self.callSolverAction("item", "clear", {})

class WS_door_replace(WS):
    def validate(self):
        super(WS_door_replace, self).validate()

        self.doorName = request.vars.doorName
        if self.doorName not in DoorsManager.doors.keys():
            raiseHttp(400, "Wrong value for doorName", True)
        self.newColor = request.vars.newColor
        if self.newColor not in ["red", "green", "yellow", "grey", "wave", "spazer", "plasma", "ice"]:
            raiseHttp(400, "Wrong value for newColor", True)

    def action(self):
        return self.callSolverAction("door", "replace", {"doorName": self.doorName, "newColor": self.newColor})

class WS_door_toggle(WS):
    def validate(self):
        super(WS_door_toggle, self).validate()

        self.doorName = request.vars.doorName
        if self.doorName not in DoorsManager.doors.keys():
            raiseHttp(400, "Wrong value for doorName", True)

    def action(self):
        return self.callSolverAction("door", "toggle", {"doorName": self.doorName})

def trackerWebService():
    # unified web service for item/area trackers
    print("trackerWebService called")

    ws = WS.factory()
    ws.validate()
    ret = ws.action()

    if ret == None:
        # return something
        raiseHttp(200, "OK", True)
    else:
        return ret

# race mode
def getMagic():
    return random.randint(1, 0xffff)

def initCustomizerSession():
    if session.customizer == None:
        session.customizer = {}

        session.customizer['colorsRandomization'] = "off"
        session.customizer['suitsPalettes'] = "on"
        session.customizer['beamsPalettes'] = "on"
        session.customizer['tilesPalettes'] = "on"
        session.customizer['enemiesPalettes'] = "on"
        session.customizer['bossesPalettes'] = "on"
        session.customizer['minDegree'] = -15
        session.customizer['maxDegree'] = 15
        session.customizer['invert'] = "on"
        session.customizer['globalShift'] = "on"
        session.customizer['customSpriteEnable'] = "off"
        session.customizer['customSprite'] = "samus"
        session.customizer['customItemsEnable'] = "off"
        session.customizer['customShipEnable'] = "off"
        session.customizer['customShip'] = "Red-M0nk3ySMShip1"
        session.customizer['itemsounds'] = "off"
        session.customizer['spinjumprestart'] = "off"
        session.customizer['rando_speed'] = "off"
        session.customizer['elevators_doors_speed'] = "off"
        session.customizer['No_Music'] = "off"
        session.customizer['random_music'] = "off"
        session.customizer['Infinite_Space_Jump'] = "off"
        session.customizer['refill_before_save'] = "off"
        session.customizer['AimAnyButton'] = "off"
        session.customizer['max_ammo_display'] = "off"
        session.customizer['supermetroid_msu1'] = "off"
        session.customizer['remove_itemsounds'] = "off"
        session.customizer['remove_spinjumprestart'] = "off"

customSprites = {
    'samus': {"index":0, "name": "Samus", "desc": "Samus, with a distinct animation for Screw Attack without Space Jump and a new Crystal Flash animation", "author": "Artheau and Feesh", "group": "Samus"},
    'samus_backwards': {"index":1, "name": "Samus (backwards)", "desc": "Samus, flipped horizontally", "author": "TarThoron", "group": "Samus"},
    'samus_upside_down': {"index":2, "name": "Samus (upside down)", "desc": "Samus, flipped vertically", "author": "TarThoron", "group": "Samus"},
    'samus_upside_down_and_backwards': {"index":3, "name": "Samus (180°)", "desc": "Samus, flpped both horizontally and vertically", "author": "TarThoron", "group": "Samus"},
    'fusion_green_varia': {"index":4, "name": "Fusion", "desc": "Samus resprite inspired by Metroid Fusion (green Varia Suit)", "author": "Gala", "group": "Samus"},
    'fusion_orange_varia': {"index":5, "name": "Fusion", "desc": "Samus resprite inspired by Metroid Fusion (orange Varia Suit)", "author": "Gala", "group": "Samus"},
    'dark_samus': {"index":6, "name": "Dark Samus", "desc": "Samus recolor inspired by the Dark Samus character", "author": "TarThoron", "group": "Samus"},
    'hack_ancient_chozo': {"index":7, "name": "Chozo", "desc": "Samus, from Ancient Chozo hack", "author": "Albert V and Physix", "group": "Samus"},
    'hack_ascent': {"index":8, "name": "Ascent", "desc": "Samus, from Ascent hack", "author": "Benox50", "group": "Samus"},
    'hack_decision': {"index":9, "name": "Decision", "desc": "Samus, from Decision hack", "author": "JoshShoeWah", "group": "Samus"},
    'hack_escape2': {"index":10, "name": "Escape II", "desc": "Samus, from Escape II hack", "author": "Hiroishi", "group": "Samus"},
    'hack_hyper': {"index":11, "name": "Hyper", "desc": "Samus, from Hyper Metroid hack", "author": "RealRed", "group": "Samus"},
    'hack_nature': {"index":12, "name": "Nature", "desc": "Samus, from Nature hack", "author": "Jefe962", "group": "Samus"},
    'hack_opposition': {"index":13, "name": "Opposition", "desc": "Space Pirate themed suit for Samus, from Opposition hack", "author": "mccad00", "group": "Samus"},
    'hack_phazon': {"index":14, "name": "Phazon", "desc": "Samus, from Phazon hack", "author": "A_red_monk_called_Key", "group": "Samus"},
    'hack_redesign': {"index":15, "name": "Redesign", "desc": "Samus, from Redesign hack", "author": "Drewseph", "group": "Samus"},
    'hack_szm': {"index":16, "name": "SZM", "desc": "Samus, from Super Zero Mission hack", "author": "SBniconico", "group": "Samus"},
    'hitbox_helper': {"index":17, "name": "Hitbox", "desc": "Samus, with her actual hitbox on top", "author": "Artheau and Komaru", "group": "Samus"},
    'bailey': {"index":18, "name": "Bailey", "desc": "Justin Bailey, aka Samus in an 80s swimsuit", "author": "Auximines", "group": "Custom"},
    'alucard': {"index":19, "name": "Alucard", "desc": "Alucard from Castlevania Symphony Of The Night", "author": "Nintoaster", "group": "Custom"},
    'megaman': {"index":20, "name": "Megaman", "desc": "Megaman X!", "author": "Artheau", "group": "Custom"},
    'link': {"index":21, "name": "Link", "desc": "Sorry Link, your game is in another randomizer!", "author": "RonnSama", "group": "Custom"},
    'fed_trooper': {"index":22, "name": "GF Trooper", "desc": "A Galactic Federation trooper", "author": "Physix", "group": "Custom"},
    'super_controid': {"index":23, "name": "Contra", "desc": "Badass soldier from Contra III", "author": "Nintoaster", "group": "Custom"},
    'mario_8bit': {"index":24, "name": "Mario (NES)", "desc": "One of the bros", "author": "TarThoron", "group": "Custom"},
    'mario_8bit_modern': {"index":25, "name": "Mario (Alt)", "desc": "One of the bros, with a more modern palette", "author": "TarThoron", "group": "Custom"},
    'luigi': {"index":26, "name": "Luigi", "desc": "The other bro", "author": "RonnSama", "group": "Custom"},
    'diddy_kong': {"index":27, "name": "Diddy Kong", "desc": "Diddy Kong from Donkey Kong Country", "author": "Di10", "group": "Custom"},
    'marga': {"index":28, "name": "Margatroid", "desc": "Alice Margatroid from the Touhou Project", "author": "Plan", "group": "Custom"},
    'sprite_can': {"index":29, "name": "Sprite", "desc": "A ... Sprite ... ", "author": "TarThoron", "group": "Custom"},
    'win95_cursor': {"index":30, "name": "Win95 Cursor", "desc": "A classic Windows cursor...", "author": "PlaguedOne", "group": "Custom"}
}

customShips = {
    'Red-M0nk3ySMShip1': {"index":0, "name": "Red-M0nk3ySMShip1", "desc": "From MetConst", "author": "Red-M0nk3y"},
    'Red-M0nk3ySMShip2': {"index":1, "name": "Red-M0nk3ySMShip2", "desc": "From MetConst", "author": "Red-M0nk3y"},
    'Red-M0nk3ySMShip3': {"index":2, "name": "Red-M0nk3ySMShip3", "desc": "From MetConst", "author": "Red-M0nk3y"},
    'Red-M0nk3ySMShip4': {"index":3, "name": "Red-M0nk3ySMShip4", "desc": "From MetConst", "author": "Red-M0nk3y"},
    'Red-M0nk3ySMShip5': {"index":4, "name": "Red-M0nk3ySMShip5", "desc": "From MetConst", "author": "Red-M0nk3y"},
    'opposition_ship': {"index":5, "name": "Opposition Ship", "desc": "From Opposition Hack", "author": "mccad00"},
    'mario_ship': {"index":6, "name": "Mario Ship", "desc": "For Mario and Luigi sprites", "author": "mccad00"}
}

def customizer():
    response.title = 'Super Metroid VARIA Seeds Customizer'

    initCustomizerSession()

    url = request.env.request_uri.split('/')
    msg = ""
    seedInfo = None
    seedParams = None
    if len(url) > 0 and url[-1] != 'customizer':
        # a seed unique key was passed as parameter
        key = url[-1]

        # decode url
        key = urllib.parse.unquote(key)

        # sanity check
        if IS_MATCH('^[0-9a-z-]*$')(key)[1] is not None:
            msg = "Seed key can only contain [0-9a-z-]"
        elif IS_LENGTH(maxsize=36, minsize=36)(key)[1] is not None:
            msg = "Seed key must be 36 chars long"
        else:
            db = DB()
            seedInfo = db.getSeedInfo(key)
            db.close()
            if seedInfo == None or len(seedInfo) == 0:
                msg = "Seed {} not found".format(key)
                seedInfo = None
            else:
                # get a dict with seed info and another one with seed parameters
                info = {}
                seedParams = {}
                infoKeys = ['time', 'filename', 'preset', 'runtime', 'complexity', 'upload_status', 'seed', 'raceMode']
                for (k, value) in seedInfo:
                    if k in infoKeys:
                        info[k] = value
                    else:
                        seedParams[k] = value
                seedInfo = info
                seedInfo['key'] = key

                # if new parameters have been added since the seed creation, add them with value "n/a"
                defaultParams = getRandomizerDefaultParameters()
                for k in defaultParams:
                    if k not in infoKeys and k not in seedParams:
                        seedParams[k] = "n/a"

                # check that the seed ips is available
                if seedInfo["upload_status"] not in ['pending', 'uploaded', 'local']:
                    msg = "Seed {} not available".format(key)
                    seedInfo = None
                    seedParams = None
                # accessing the url tell us to store the ips for more than 7 days
                elif seedInfo["upload_status"] == 'local':
                    db = DB()
                    db.updateSeedUploadStatus(key, 'pending')
                    db.close()

    return dict(customSprites=customSprites, customShips=customShips,
                seedInfo=seedInfo, seedParams=seedParams, msg=msg)

def customWebService():
    print("customWebService")

    # check validity of all parameters
    switchs = ['itemsounds', 'spinjumprestart', 'rando_speed', 'elevators_doors_speed', 'No_Music', 'random_music',
               'AimAnyButton', 'max_ammo_display', 'supermetroid_msu1', 'Infinite_Space_Jump', 'refill_before_save',
               'customSpriteEnable', 'customItemsEnable', 'customShipEnable', 'remove_itemsounds', 'remove_elevators_doors_speed']
    others = ['colorsRandomization', 'suitsPalettes', 'beamsPalettes', 'tilesPalettes', 'enemiesPalettes',
              'bossesPalettes', 'minDegree', 'maxDegree', 'invert']
    validateWebServiceParams(switchs, [], [], others, isJson=True)
    if request.vars.customSpriteEnable == 'on':
        if request.vars.customSprite not in customSprites:
            raiseHttp(400, "Wrong value for customSprite", True)
    if request.vars.customShipEnable == 'on':
        if request.vars.customShip not in customShips:
            raiseHttp(400, "Wrong value for customShip", True)

    if session.customizer == None:
        session.customizer = {}

    # update session
    session.customizer['colorsRandomization'] = request.vars.colorsRandomization
    session.customizer['suitsPalettes'] = request.vars.suitsPalettes
    session.customizer['beamsPalettes'] = request.vars.beamsPalettes
    session.customizer['tilesPalettes'] = request.vars.tilesPalettes
    session.customizer['enemiesPalettes'] = request.vars.enemiesPalettes
    session.customizer['bossesPalettes'] = request.vars.bossesPalettes
    session.customizer['minDegree'] = request.vars.minDegree
    session.customizer['maxDegree'] = request.vars.maxDegree
    session.customizer['invert'] = request.vars.invert
    session.customizer['globalShift'] = request.vars.globalShift
    session.customizer['customSpriteEnable'] = request.vars.customSpriteEnable
    session.customizer['customSprite'] = request.vars.customSprite
    session.customizer['customItemsEnable'] = request.vars.customItemsEnable
    session.customizer['customShipEnable'] = request.vars.customShipEnable
    session.customizer['customShip'] = request.vars.customShip
    session.customizer['itemsounds'] = request.vars.itemsounds
    session.customizer['spinjumprestart'] = request.vars.spinjumprestart
    session.customizer['rando_speed'] = request.vars.rando_speed
    session.customizer['elevators_doors_speed'] = request.vars.elevators_doors_speed
    session.customizer['No_Music'] = request.vars.No_Music
    session.customizer['random_music'] = request.vars.random_music
    session.customizer['Infinite_Space_Jump'] = request.vars.Infinite_Space_Jump
    session.customizer['refill_before_save'] = request.vars.refill_before_save
    session.customizer['AimAnyButton'] = request.vars.AimAnyButton
    session.customizer['max_ammo_display'] = request.vars.max_ammo_display
    session.customizer['supermetroid_msu1'] = request.vars.supermetroid_msu1
    session.customizer['remove_itemsounds'] = request.vars.remove_itemsounds
    session.customizer['remove_elevators_doors_speed'] = request.vars.remove_elevators_doors_speed

    # when beam doors patch is detected, don't randomize blue door palette
    no_blue_door_palette = request.vars.no_blue_door_palette

    # call the randomizer
    (fd, jsonFileName) = tempfile.mkstemp()
    params = [pythonExec,  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
              '--output', jsonFileName, '--patchOnly']

    if request.vars.itemsounds == 'on':
        params += ['-c', 'itemsounds.ips']
    if request.vars.elevators_doors_speed == 'on':
        params += ['-c', 'elevators_doors_speed.ips']
    if request.vars.spinjumprestart == 'on':
        params += ['-c', 'spinjumprestart.ips']
    if request.vars.rando_speed == 'on':
        params += ['-c', 'rando_speed.ips']
    if request.vars.No_Music == 'on':
        params += ['-c', 'No_Music']
    if request.vars.random_music == 'on':
        params += ['-c', 'random_music.ips']
    if request.vars.AimAnyButton == 'on':
        params += ['-c', 'AimAnyButton.ips']
    if request.vars.max_ammo_display == 'on':
        params += ['-c', 'max_ammo_display.ips']
    if request.vars.supermetroid_msu1 == 'on':
        params += ['-c', 'supermetroid_msu1.ips']
    if request.vars.Infinite_Space_Jump == 'on':
        params += ['-c', 'Infinite_Space_Jump']
    if request.vars.refill_before_save == 'on':
        params += ['-c', 'refill_before_save.ips']
    if request.vars.remove_itemsounds == 'on':
        params += ['-c', 'remove_itemsounds.ips']
    if request.vars.remove_elevators_doors_speed == 'on':
        params += ['-c', 'remove_elevators_doors_speed.ips']

    if request.vars.colorsRandomization == 'on':
        params.append('--palette')
        if request.vars.suitsPalettes == 'off':
            params.append('--no_shift_suit_palettes')
        if request.vars.beamsPalettes == 'off':
            params.append('--no_shift_beam_palettes')
        if request.vars.tilesPalettes == 'off':
            params.append('--no_shift_tileset_palette')
        if request.vars.enemiesPalettes == 'off':
            params.append('--no_shift_enemy_palettes')
        if request.vars.bossesPalettes == 'off':
            params.append('--no_shift_boss_palettes')
        if request.vars.globalShift == 'off':
            params.append('--no_global_shift')
            params.append('--individual_suit_shift')
            params.append('--individual_tileset_shift')
            params.append('--no_match_ship_and_power')
        params += ['--min_degree', request.vars.minDegree, '--max_degree', request.vars.maxDegree]
        if request.vars.invert == 'on':
            params.append('--invert')
        if no_blue_door_palette == 'on':
            params.append('--no_blue_door_palette')

    if request.vars.customSpriteEnable == 'on':
        params += ['--sprite', "{}.ips".format(request.vars.customSprite)]
        if request.vars.customItemsEnable == 'on':
            params.append('--customItemNames')
    if request.vars.customShipEnable == 'on':
        params += ['--ship', "{}.ips".format(request.vars.customShip)]
    if request.vars.seedKey != None:
        db = DB()
        seedIpsInfo = db.getSeedIpsInfo(request.vars.seedKey)
        print("seedIpsInfo: {}".format(seedIpsInfo))
        db.close()
        if seedIpsInfo == None or len(seedIpsInfo) == 0:
            raise HTTP(400, json.dumps("Can't get seed info"))
        (uploadStatus, fileName) = seedIpsInfo[0]
        if uploadStatus not in ['local', 'pending', 'uploaded']:
            raise HTTP(400, json.dumps("Seed is not available"))

        ipsFileName = os.path.join(localIpsDir, request.vars.seedKey, fileName.replace('sfc', 'ips'))
        params += ['--seedIps', ipsFileName]

    print("before calling: {}".format(params))
    start = datetime.now()
    ret = subprocess.call(params)
    end = datetime.now()
    duration = (end - start).total_seconds()
    print("ret: {}, duration: {}s".format(ret, duration))

    if ret == 0:
        with open(jsonFileName) as jsonFile:
            data = json.load(jsonFile)

        os.close(fd)
        os.remove(jsonFileName)

        return json.dumps(data)
    else:
        # extract error from json
        try:
            with open(jsonFileName) as jsonFile:
                msg = json.load(jsonFile)['errorMsg']
        except:
            msg = "customizerWebService: something wrong happened"

        os.close(fd)
        os.remove(jsonFileName)
        raise HTTP(400, json.dumps(msg))

def initExtStatsSession():
    if session.extStats == None:
        session.extStats = {}
        session.extStats['preset'] = 'regular'
        session.extStats['randoPreset'] = 'default'

def updateExtStatsSession():
    if session.extStats is None:
        session.extStats = {}

    session.extStats['preset'] = request.vars.preset
    session.extStats['randoPreset'] = request.vars.randoPreset

def validateExtStatsParams():
    for (preset, directory) in [("preset", "standard_presets"), ("randoPreset", "rando_presets")]:
        if request.vars[preset] == None:
            return (False, "Missing parameter preset")
        preset = request.vars[preset]

        if IS_ALPHANUMERIC()(preset)[1] is not None:
            return (False, "Wrong value for preset, must be alphanumeric")

        if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
            return (False, "Wrong length for preset, name must be between 1 and 32 characters")

        # check that preset exists
        fullPath = '{}/{}.json'.format(directory, preset)
        if not os.path.isfile(fullPath):
            return (False, "Unknown preset: {}".format(preset))

    return (True, None)

def extStats():
    response.title = 'Super Metroid VARIA Randomizer statistics'

    initExtStatsSession()

    if request.vars.action == 'Load':
        (ok, msg) = validateExtStatsParams()
        if not ok:
            session.flash = msg
            redirect(URL(r=request, f='extStats'))

        updateExtStatsSession()

        skillPreset = request.vars.preset
        randoPreset = request.vars.randoPreset

        # load rando preset to get majors split
        fullPath = 'rando_presets/{}.json'.format(randoPreset)
        if not os.path.isfile(fullPath):
            raise HTTP(400, "Unknown rando preset: {}".format(e))
        try:
            with open(fullPath) as jsonFile:
                randoPresetContent = json.load(jsonFile)
        except Exception as e:
            raise HTTP(400, "Can't load the rando preset: {}".format(e))
        majorsSplit = randoPresetContent["majorsSplit"]

        # load skill preset
        fullPath = '{}/{}.json'.format(getPresetDir(skillPreset), skillPreset)
        try:
            skillPresetContent = PresetLoader.factory(fullPath).params
            completePreset(skillPresetContent)
        except Exception as e:
            raise HTTP(400, "Error loading the skill preset: {}".format(e))

        db = DB()
        (itemsStats, techniquesStats, difficulties, solverStatsRaw) = db.getExtStat(skillPreset, randoPreset)
        db.close()

        solverStats = {}
        if "avgLocs" in solverStatsRaw:
            solverStats["avgLocs"] = transformStats(solverStatsRaw["avgLocs"])
            solverStats["avgLocs"].insert(0, ['Available locations', 'Percentage'])
        if "open14" in solverStatsRaw:
            open14 = transformStats(solverStatsRaw["open14"])
            open24 = transformStats(solverStatsRaw["open24"])
            open34 = transformStats(solverStatsRaw["open34"])
            open44 = transformStats(solverStatsRaw["open44"])
            solverStats["open"] = zipStats([open14, open24, open34, open44])
            solverStats["open"].insert(0, ['Collected items', '1/4 locations available', '2/4 locations available', '3/4 locations available', '4/4 locations available'])

        # check that all items are present in the stats:
        nbItems = 19
        nbLocs = 105
        if itemsStats != None and len(itemsStats) > 0 and len(itemsStats) != nbItems:
            for i, item in enumerate(['Bomb', 'Charge', 'Grapple', 'Gravity', 'HiJump', 'Ice', 'Missile', 'Morph',
                                      'Plasma', 'PowerBomb', 'ScrewAttack', 'SpaceJump', 'Spazer', 'SpeedBooster',
                                      'SpringBall', 'Super', 'Varia', 'Wave', 'XRayScope']):
                if itemsStats[i][1] != item:
                    itemsStats.insert(i, [itemsStats[0][0], item] + [0]*nbLocs)
    else:
        itemsStats = None
        techniquesStats = None
        difficulties = None
        solverStats = None
        skillPresetContent = None
        majorsSplit = None

    (randoPresets, tourRandoPresets) = loadRandoPresetsList()
    # remove random presets those statistics are useless
    randoPresets.remove("all_random")
    randoPresets.remove("quite_random")
    (stdPresets, tourPresets, comPresets) = loadPresetsList()

    return dict(stdPresets=stdPresets, tourPresets=tourPresets,
                randoPresets=randoPresets, tourRandoPresets=tourRandoPresets,
                itemsStats=itemsStats, techniquesStats=techniquesStats,
                categories=Knows.categories, knowsDesc=Knows.desc, skillPresetContent=skillPresetContent,
                locations=locations, majorsSplit=majorsSplit, difficulties=difficulties, solverStats=solverStats)

def transformStats(stats, maxRange=106):
    # input a list [(x, value), (x, value), ..., (x, value)]
    # ouput a list with (x, 0) for missing x values
    if len(stats) > 0:
        (curX, curValue) = stats.pop(0)
    else:
        (curX, curValue) = (maxRange-1, 0)
    out = []
    for i in range(1, maxRange):
        if i < curX:
            out.append([i, 0])
        else:
            out.append([curX, float(curValue)])
            if len(stats) > 0:
                (curX, curValue) = stats.pop(0)
            else:
                (curX, curValue) = (maxRange-1, 0)
    return out

def zipStats(stats):
    out = []
    for i in range(len(stats[0])):
        line = [i+1]
        for s in stats:
            line.append(s[i][1])
        out.append(line)
    return out

def initProgSpeedStatsSession():
    if session.progSpeedStats == None:
        session.progSpeedStats = {}
        session.progSpeedStats['majorsSplit'] = 'Major'

def updateProgSpeedStatsSession():
    if session.progSpeedStats is None:
        session.progSpeedStats = {}

    session.progSpeedStats['majorsSplit'] = request.vars.majorsSplit

def validateProgSpeedStatsParams():
    if request.vars.majorsSplit not in ['Full', 'Major']:
            return (False, "Wrong value for majorsSplit, authorized values Full/Major")

    return (True, None)

def progSpeedStats():
    response.title = 'Super Metroid VARIA Randomizer progression speed statistics'

    initProgSpeedStatsSession()

    if request.vars.action == 'Load':
        (ok, msg) = validateProgSpeedStatsParams()
        if not ok:
            session.flash = msg
            redirect(URL(r=request, f='progSpeedStats'))

        updateProgSpeedStatsSession()

        skillPreset = "Season_Races"
        randoPreset = "Season_Races"
        majorsSplit = request.vars.majorsSplit

        db = DB()
        progSpeedStatsRaw = {}
        progSpeedStats = {}
        progSpeedStats["open14"] = {}
        progSpeedStats["open24"] = {}
        progSpeedStats["open34"] = {}
        progSpeedStats["open44"] = {}
        progSpeeds = ['speedrun', 'slowest', 'slow', 'medium', 'fast', 'fastest', 'basic', 'variable', 'total']
        realProgSpeeds = []
        realProgSpeedsName = []
        for progSpeed in progSpeeds:
            curRandoPreset = "{}_{}_{}".format(randoPreset, majorsSplit, progSpeed)
            progSpeedStatsRaw[progSpeed] = db.getProgSpeedStat(skillPreset, curRandoPreset)

            if len(progSpeedStatsRaw[progSpeed]) != 0:
                progSpeedStats[progSpeed] = {}
                progSpeedStats[progSpeed]["avgLocs"] = transformStats(progSpeedStatsRaw[progSpeed]["avgLocs"], 50)
                open14 = transformStats(progSpeedStatsRaw[progSpeed]["open14"])
                open24 = transformStats(progSpeedStatsRaw[progSpeed]["open24"])
                open34 = transformStats(progSpeedStatsRaw[progSpeed]["open34"])
                open44 = transformStats(progSpeedStatsRaw[progSpeed]["open44"])
                progSpeedStats[progSpeed]["open"] = zipStats([open14, open24, open34, open44])
                progSpeedStats[progSpeed]["open"].insert(0, ['Collected items', '1/4 locations available', '2/4 locations available', '3/4 locations available', '4/4 locations available'])

                progSpeedStats["open14"][progSpeed] = open14
                progSpeedStats["open24"][progSpeed] = open24
                progSpeedStats["open34"][progSpeed] = open34
                progSpeedStats["open44"][progSpeed] = open44

                realProgSpeeds.append(progSpeed)
                if progSpeed == 'total':
                    realProgSpeedsName.append('total_rando')
                else:
                    realProgSpeedsName.append(progSpeed)
        db.close()

        # avg locs
        if len(realProgSpeeds) > 0:
            progSpeedStats['avgLocs'] = zipStats([progSpeedStats[progSpeed]["avgLocs"] for progSpeed in realProgSpeeds])
            progSpeedStats["avgLocs"].insert(0, ['Available locations']+realProgSpeedsName)

        # prog items
        if len(progSpeedStats["open14"]) > 0:
            progSpeedStats["open14"] = zipStats([progSpeedStats["open14"][progSpeed] for progSpeed in realProgSpeeds])
            progSpeedStats["open14"].insert(0, ['Collected items']+realProgSpeedsName)
            progSpeedStats["open24"] = zipStats([progSpeedStats["open24"][progSpeed] for progSpeed in realProgSpeeds])
            progSpeedStats["open24"].insert(0, ['Collected items']+realProgSpeedsName)
            progSpeedStats["open34"] = zipStats([progSpeedStats["open34"][progSpeed] for progSpeed in realProgSpeeds])
            progSpeedStats["open34"].insert(0, ['Collected items']+realProgSpeedsName)
            progSpeedStats["open44"] = zipStats([progSpeedStats["open44"][progSpeed] for progSpeed in realProgSpeeds])
            progSpeedStats["open44"].insert(0, ['Collected items']+realProgSpeedsName)
    else:
        progSpeedStats = None

    majorsSplit = ['Major', 'Full']

    return dict(majorsSplit=majorsSplit, progSpeedStats=progSpeedStats)

ipsBasePath = "plandository/"
def plandorepo():
    response.title = 'Super Metroid VARIA Plandository'

    db = DB()
    url = request.env.request_uri.split('/')
    msg = ""
    plandos = []
    expand = True
    if len(url) > 0 and url[-1] != 'plandorepo':
        # a plando name was passed as parameter
        plandoName = url[-1]

        # decode url
        plandoName = urllib.parse.unquote(plandoName)

        # sanity check
        if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
            msg = "Plando name can only contain [a-zA-Z0-9 -_]"
        else:
            plandos = db.getPlando(plandoName)
            if plandos == None or len(plandos) == 0:
                msg = "Plando not found"
    if len(plandos) == 0:
        # get plando list
        plandos = db.getPlandos()
        expand = False

    db.close()

    return dict(plandos=plandos, msg=msg, expand=expand, math=math, re=re)

def plandoRateWebService():
    print("plandoRateWebService")

    if request.vars.plando == None:
        raiseHttp(400, "Missing parameter plando")
    plando = request.vars.plando

    if request.vars.rate == None:
        raiseHttp(400, "Missing parameter rate")
    rate = request.vars.rate

    if IS_LENGTH(maxsize=32, minsize=1)(plando)[1] is not None:
        raise HTTP(400, "Plando name must be between 1 and 32 characters")

    if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plando)[1] is not None:
        raise HTTP(400, "Plando name can only contain [a-zA-Z0-9 -_]")

    if IS_INT_IN_RANGE(1, 6)(rate)[1] is not None:
        raise HTTP(400, "Rate name must be between 1 and 5")
    rate = int(rate)
    ip = request.client

    db = DB()
    db.addRating(plando, rate, ip)
    newRate = db.getPlandoRate(plando)
    db.close()
    if newRate == None:
        raiseHttp(400, "Can't get new rate")
    newCount = newRate[0][0]
    newRate = float(newRate[0][1])
    data = {
        "msg": "",
        "purePlandoName": re.sub('[\W_]+', '', plando),
        "rate": newRate,
        "count": newCount
    }
    return json.dumps(data)

def downloadPlandoWebService():
    if request.vars.plando == None:
        raiseHttp(400, "Missing parameter plando")
    plandoName = request.vars.plando

    if IS_LENGTH(maxsize=32, minsize=1)(plandoName)[1] is not None:
        raise HTTP(400, "Plando name must be between 1 and 32 characters")

    if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
        raise HTTP(400, "Plando name can only contain [a-zA-Z0-9 -_]")

    ipsFileName = os.path.join(ipsBasePath, "{}.ips".format(plandoName))
    with open(ipsFileName, 'rb') as ipsFile:
        ipsData = ipsFile.read()

    db = DB()
    maxSize = db.getPlandoIpsMaxSize(plandoName)
    db.increaseDownloadCount(plandoName)
    db.close()

    data = {
        "ips": base64.b64encode(ipsData).decode(),
        "fileName": "{}.sfc".format(plandoName),
        "maxSize": maxSize
    }

    return json.dumps(data)

def removeHtmlTags(text):
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # also double the ' for db insertion
    return text.replace("'", "''")

def generateUpdateKey():
    # 8 chars string
    stringLength = 8
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def handleIps(plandoName, romDataJson):
    romDataJson = request.vars.romData
    romDataRaw = json.loads(romDataJson)
    # everything is string in json, cast to int
    romData = {}
    for addr in romDataRaw:
        romData[int(addr)] = int(romDataRaw[addr])

    # dict: address -> value, transform it dict: address -> [values]
    ipsData = {}
    prevAddr = -0xff
    curRecord = []
    curRecordAddr = -1
    for addr in sorted(romData):
        if addr == prevAddr + 1:
            curRecord.append(romData[addr])
        else:
            if len(curRecord) > 0:
                # save current record
                ipsData[curRecordAddr] = bytearray(curRecord)
            # start a new one
            curRecordAddr = addr
            curRecord = [romData[addr]]
        prevAddr = addr
    # save last record
    ipsData[curRecordAddr] = bytearray(curRecord)

    # generate ips using the records
    ipsPatch = IPS_Patch(ipsData)
    maxSize = ipsPatch.max_size

    # store ips in the repository
    ipsPatch.save(os.path.join(ipsBasePath, "{}.ips".format(plandoName)))

    return maxSize

def uploadPlandoWebService():
    print("uploadPlandoWebService")

    db = DB()
    count = db.getPlandoCount()
    plandoLimit = 2048
    if count == None or count[0][0] >= plandoLimit:
        db.close()
        raise HTTP(400, "Maximum number of plandos reach: {}".format(plandoLimit))
    db.close()

    for param in ["author", "plandoName", "longDesc", "preset", "romData"]:
        if request.vars[param] == None:
            raiseHttp(400, "Missing parameter {}".format(param))

    for param in ["author", "plandoName", "preset"]:
        if IS_LENGTH(maxsize=32, minsize=1)(request.vars[param])[1] is not None:
            raise HTTP(400, "{} must be between 1 and 32 characters".format(param))

    for param in ["longDesc"]:
        if IS_LENGTH(maxsize=2048, minsize=1)(request.vars[param])[1] is not None:
            raise HTTP(400, "{} must be between 1 and 2048 characters".format(param))

    plandoName = request.vars.plandoName
    if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
        raise HTTP(400, "Plando name can only contain [a-zA-Z0-9 -_]")

    # check if plando doesn't already exist
    db = DB()
    check = db.checkPlando(plandoName)
    db.close()

    if check is not None and len(check) > 0 and check[0][0] == plandoName:
        raise HTTP(400, "Can't create plando, a plando with the same name already exists")

    author = request.vars.author
    longDesc = removeHtmlTags(request.vars.longDesc)
    preset = request.vars.preset

    maxSize = handleIps(plandoName, request.vars.romData)

    updateKey = generateUpdateKey()

    db = DB()
    db.insertPlando((plandoName, author, longDesc, preset, updateKey, maxSize))
    db.close()

    if webhookAvailable:
        plandoWebhook(plandoName, author, preset, longDesc)

    return json.dumps(updateKey)

def plandoWebhook(plandoName, author, preset, longDesc):
    webhook = DiscordWebhook(url=webhookUrl, username="Plandository")

    embed = DiscordEmbed(title=plandoName, description="New {} plando by {}".format(preset, author), color=242424)

    # there's a limit for discord for the size of an embed field
    embedLimit = 512
    if len(longDesc) > embedLimit:
        longDesc = longDesc[:embedLimit]+"..."
    embed.add_embed_field(name="description", value=longDesc, inline=False)

    permalink = getPermalink(plandoName)
    embed.add_embed_field(name="permalink", value=permalink)
    webhook.add_embed(embed)

    try:
        response = webhook.execute()
    except:
        pass

def getPermalink(plandoName):
    return "http://{}/plandorepo/{}".format(request.env.HTTP_HOST, urllib.parse.quote(plandoName))

def deletePlandoWebService():
    for param in ["plandoName", "plandoKey"]:
        if request.vars[param] == None:
            raiseHttp(400, "Missing parameter {}".format(param))

    plandoName = request.vars.plandoName
    plandoKey = request.vars.plandoKey

    if IS_LENGTH(maxsize=32, minsize=1)(plandoName)[1] is not None:
        raise HTTP(400, "Plando name must be between 1 and 32 characters")
    if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
        raise HTTP(400, "Plando name can only contain [a-zA-Z0-9 -_]")

    if IS_LENGTH(maxsize=8, minsize=1)(plandoKey)[1] is not None:
        raise HTTP(400, "Plando key must be between 1 and 8 characters")
    if IS_MATCH('^[a-zA-Z0-9]*$')(plandoKey)[1] is not None:
        raise HTTP(400, "Plando key can only contain [a-zA-Z0-9]")

    db = DB()
    valid = db.isValidPlandoKey(plandoName, plandoKey)
    if valid == None or len(valid) == 0:
        db.close()
        raise HTTP(400, "Plando key mismatch")
    db.deletePlandoRating(plandoName)
    db.deletePlando(plandoName)
    db.close()

    return json.dumps("Plando {} deleted".format(plandoName))

def updatePlandoWebService():
    print("updatePlandoWebService")

    for param in ["author", "plandoName", "longDesc", "preset", "plandoKey"]:
        if request.vars[param] == None:
            raiseHttp(400, "Missing parameter {}".format(param))

    for param in ["author", "plandoName", "preset"]:
        if IS_LENGTH(maxsize=32, minsize=1)(request.vars[param])[1] is not None:
            raise HTTP(400, "{} must be between 1 and 32 characters".format(param))

    for param in ["plandoKey"]:
        if IS_LENGTH(maxsize=8, minsize=1)(request.vars[param])[1] is not None:
            raise HTTP(400, "{} must be between 1 and 8 characters".format(param))

    for param in ["longDesc"]:
        if IS_LENGTH(maxsize=2048, minsize=1)(request.vars[param])[1] is not None:
            raise HTTP(400, "{} must be between 1 and 2048 characters".format(param))

    plandoName = request.vars.plandoName
    if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
        raise HTTP(400, "Plando name can only contain [a-zA-Z0-9 -_]")

    author = request.vars.author
    longDesc = removeHtmlTags(request.vars.longDesc)
    preset = request.vars.preset
    plandoKey = request.vars.plandoKey

    # check update key
    db = DB()
    valid = db.isValidPlandoKey(plandoName, plandoKey)
    if valid == None or len(valid) == 0:
        db.close()
        raise HTTP(400, "Plando key mismatch")

    if request.vars.romData != None:
        print("updatePlandoWebService: update ips")
        maxSize = handleIps(plandoName, request.vars.romData)
        db.updatePlandoAll((author, longDesc, preset, maxSize, plandoName))
    else:
        db.updatePlandoMeta((author, longDesc, preset, plandoName))

    db.close()

    return json.dumps("Plando {} updated succesfully.".format(plandoName))
