import sys, os, json

from rom.rom import snes_to_pc
from rom.romreader import RomReader
from rom.addresses import Addresses
from utils.doorsmanager import DoorsManager
from utils.utils import getDefaultMultiValues, getPresetDir, removeChars
from utils.parameters import Knows, isKnows, Controller, isButton
from utils.objectives import Objectives
from logic.logic import Logic
from rom.flavor import RomFlavor

from gluon.validators import IS_ALPHANUMERIC, IS_LENGTH, IS_MATCH
from gluon.http import HTTP

localIpsDir = 'varia_repository'

def loadPresetsList(cache, emptyFirst=False):
    # use a cache to avoid reading the files everytime
    presets = cache.ram('skillPresets', lambda:dict(), time_expire=None)
    if presets and not emptyFirst:
        return (presets['stdPresets'], presets['tourPresets'], presets['comPresets'])

    if emptyFirst:
        # we empty the cache by calling it with None as 2nd param
        cache.ram('skillPresets', None)
        presets = cache.ram('skillPresets', lambda:dict(), time_expire=None)

    files = sorted(os.listdir('community_presets'), key=lambda v: v.upper())
    stdPresets = ['newbie', 'casual', 'regular', 'veteran', 'expert', 'master']
    tourPresets = ['Season_Races', 'SMRAT2021', 'Torneio_SGPT3']
    comPresets = [os.path.splitext(file)[0] for file in files if file != '.git']

    presets['stdPresets'] = stdPresets
    presets['tourPresets'] = tourPresets
    presets['comPresets'] = comPresets

    return (presets['stdPresets'], presets['tourPresets'], presets['comPresets'])

def loadRandoPresetsList(cache, filter=False):
    presets = cache.ram('randoPresets', lambda:dict(), time_expire=None)
    if not presets:
        tourPresets = ['Season_Races', 'SMRAT2021', 'VARIA_Weekly',
                       'RLS4W2', 'RLS4W3', 'RLS4W4', 'RLS4W5', 'RLS4W7',
                       'Torneio_SGPT3_stage1', 'Torneio_SGPT3_stage2',
                       'SGLive2022_Game_1', 'SGLive2022_Game_2', 'SGLive2022_Game_3', 'Boyz_League_SM_Rando']
        files = sorted(os.listdir('rando_presets'), key=lambda v: v.upper())
        randoPresets = [os.path.splitext(file)[0] for file in files]
        randoPresets = [preset for preset in randoPresets if preset not in tourPresets]

        presets['randoPresets'] = randoPresets
        presets['tourPresets'] = tourPresets

    randoPresets = presets['randoPresets']
    tourPresets = presets['tourPresets']

    if filter:
        # remove rando presets with no stats
        randoPresets = [preset for preset in randoPresets if preset not in ['all_random', 'minimizer_hardcore', 'minimizer', 'minimizer_maximizer', 'quite_random']]
    else:
        # create a copy to not modify cached one later
        randoPresets = randoPresets[:]

    return (randoPresets, tourPresets)

def getAddressesToRead(cache):
    addresses = cache.ram('addresses', lambda:dict(), time_expire=None)
    if addresses:
        return addresses

    addresses["locations"] = []
    addresses["patches"] = []
    addresses["transitions"] = []
    addresses["misc"] = []
    addresses["ranges"] = []

    for logic in ['vanilla', 'mirror']:
        Logic.factory(logic)
        RomFlavor.factory()

        # locations
        for loc in Logic.locations:
            addresses["locations"].append(loc.Address)

        # doors
        addresses["misc"] += DoorsManager.getAddressesToRead()

        # transitions
        for ap in Logic.accessPoints:
            if ap.Internal == True:
                continue
            addresses["transitions"].append(0x10000 | ap.ExitInfo['DoorPtr'])

        maxDoorAsmPatchLen = 22
        customDoorsAsm = Addresses.getOne('customDoorsAsm')
        addresses["ranges"] += [customDoorsAsm, customDoorsAsm+(maxDoorAsmPatchLen * len([ap for ap in Logic.accessPoints if ap.Internal == False]))]

    # patches
    for (_class, patches) in RomReader.patches.items():
        for patch, values in patches.items():
            addresses["patches"].append(values["address"])

    # flavor patches
    for patch, values in RomReader.flavorPatches.items():
        addresses["patches"].append(values["address"])

    # misc
    # majors split
    addresses["misc"] += Addresses.getWeb('majorsSplit')
    # escape timer
    addresses["misc"] += Addresses.getWeb('escapeTimer')
    # start ap
    addresses["misc"] += Addresses.getWeb('startAP')
    # objectives
    addresses["misc"] += Objectives.getAddressesToRead()

    # ranges [low, high]
    ## old doorasm for old seeds
    addresses["ranges"] += [snes_to_pc(0x8feb00), snes_to_pc(0x8fee60)]
    # split locs
    addresses["ranges"] += Addresses.getRange('locIdsByArea')
    addresses["ranges"] += Addresses.getRange('scavengerOrder')
    # plando addresses
    addresses["ranges"] += Addresses.getRange('plandoAddresses')
    # plando transitions (4 bytes per transitions, ap#/2 transitions)
    plandoTransitions = Addresses.getOne('plandoTransitions')
    addresses["ranges"] += [plandoTransitions, plandoTransitions+((len(addresses["transitions"])/2) * 4)]
    # starting etanks added in the customizer
    addresses["misc"] += Addresses.getWeb('additionalETanks')
    # events array for autotracker
    addresses["ranges"] += Addresses.getRange('objectiveEventsArray')

    return addresses

# if we have an internal parameter value different from its display value
displayNames = {
    "FullWithHUD": "Full Countdown",
    "harder": "very hard",
    "infinity": "no difficulty cap"
}

def updateParameterDisplay(value):
    for internal, display in displayNames.items():
        if internal in value:
            value = value.replace(internal, display)
    return value

def raiseHttp(code, msg, isJson=False):
    #print("raiseHttp: code {} msg {} isJson {}".format(code, msg, isJson))
    if isJson is True:
        msg = json.dumps(msg)

    raise HTTP(code, msg)

def getInt(request, param, isJson=False):
    try:
        return int(request.vars[param])
    except:
        raiseHttp(400, "Wrong value for {}, must be an int".format(param), isJson)

def getFloat(request, param, isJson=False):
    try:
        return float(request.vars[param])
    except:
        raiseHttp(400, "Wrong value for {}, must be a float".format(param), isJson)

def validateWebServiceParams(request, switchs, quantities, multis, others, isJson=False):
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
                qtyInt = getInt(request, qty, isJson)
                if qtyInt < 30 or qtyInt > 100:
                    raiseHttp(400, "Wrong value for {}, must be between 30 and 100".format(qty), isJson)
        elif qty == 'scavNumLocs':
            if request.vars.majorsSplit == 'Scavenger':
                qtyInt = getInt(request, qty, isJson)
                if qtyInt < 4 or qtyInt > 17:
                    raiseHttp(400, "Wrong value for {}, must be between 4 and 16".format(qty), isJson)
        else:
            qtyFloat = getFloat(request, qty, isJson)
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
        minorQtyInt = getInt(request, 'minorQty', isJson)
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
        seedInt = getInt(request, 'seed', isJson)
        if seedInt < 0 or seedInt > sys.maxsize:
            raiseHttp(400, "Wrong value for seed", isJson)

    if 'objective' in others:
        value = request.vars.objectiveRandom
        if not request.vars.objectiveRandom in ['true', 'false']:
            raiseHttp(400, "objectiveRandom must be either true or false", isJson)

        objective = request.vars.objective.split(',')
        authorizedObjectives = defaultMultiValues['objective'] + ['nothing']
        for value in objective:
            if value not in authorizedObjectives:
                raiseHttp(400, "Wrong value for objective", isJson)


        if request.vars.objectiveRandom == 'true':
            nbObjective = request.vars.nbObjective
            if nbObjective.isdigit():
                if not int(nbObjective) in range(6):
                    raiseHttp(400, "Number of objectives must be 0-5", isJson)
            elif nbObjective != "random":
                raiseHttp(400, "Number of objectives must be 0-5 or \"random\"", isJson)
        else:
            if len(objective) > 5:
                raiseHttp(400, "You cannot choose more than 5 objectives", isJson)


    if 'minDegree' in others:
        minDegree = getInt(request, 'minDegree', isJson)
        if minDegree < -180 or minDegree > 180:
            raiseHttp(400, "Wrong value for minDegree", isJson)

    if 'maxDegree' in others:
        maxDegree = getInt(request, 'maxDegree', isJson)
        if maxDegree < -180 or maxDegree > 180:
            raiseHttp(400, "Wrong value for maxDegree", isJson)

    if 'hellrun_rate' in others and request.vars.hellrun_rate != 'off':
        hellrun_rate = getInt(request, 'hellrun_rate', isJson)
        if hellrun_rate < 0 or hellrun_rate > 400:
            raiseHttp(400, "Wrong value for hellrun_rate", isJson)

    if 'etanks' in others and request.vars.etanks != 'off':
        etanks = getInt(request, 'etanks', isJson)
        if etanks < 0 or etanks > 14:
            raiseHttp(400, "Wrong value for etanks", isJson)

    if 'maxDifficulty' in others:
        if request.vars.maxDifficulty not in ['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania', 'infinity', 'random']:
            raiseHttp(400, "Wrong value for max difficulty", isJson)

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

    if 'nbObjectivesRequired' in others:
        if request.vars.nbObjectivesRequired not in ("off", "random", range(1, 32)):
            raiseHttp(400, "Wrong value for nbObjectivesRequired", isJson)

def getCustomMapping(controlMapping):
    if len(controlMapping) == 0:
        return (False, None)

    inv = {}
    for button in controlMapping:
        inv[controlMapping[button]] = button

    return (True, "{},{},{},{},{},{},{}".format(inv["Shoot"], inv["Jump"], inv["Dash"], inv["Item Select"], inv["Item Cancel"], inv["Angle Up"], inv["Angle Down"]))

def completePreset(params):
    # add missing knows
    for know in Knows.__dict__:
        if isKnows(know):
            if know not in params['Knows'].keys():
                params['Knows'][know] = Knows.__dict__[know].toPreset()

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

def transition2isolver(transition):
    transition = str(transition)
    return transition[0].lower() + removeChars(transition[1:], " ,()-")

def locName4isolver(locName):
    # remove space and special characters
    # sed -e 's+ ++g' -e 's+,++g' -e 's+(++g' -e 's+)++g' -e 's+-++g'
    locName = str(locName)
    return locName[0].lower() + removeChars(locName[1:], " ,()-")

def generateJsonROM(romJsonStr):
    tempRomJson = json.loads(romJsonStr)
    romFileName = tempRomJson["romFileName"]
    (base, ext) = os.path.splitext(romFileName)
    jsonRomFileName = 'roms/{}.json'.format(base)
    del tempRomJson["romFileName"]

    with open(jsonRomFileName, 'w') as jsonFile:
        json.dump(tempRomJson, jsonFile)

    return (base, jsonRomFileName)

def get_app_files():
    with open('applications/solver/static/client/manifest.json', 'r') as manifest:
        data = json.loads(manifest.read())
    js = [k for k in data.keys() if k.endswith('.js')]
    css = [k for k in data.keys() if k.endswith('.css')]
    fa = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css"
    return '\n'.join([
        f'<link href="{fa}" rel="stylesheet" />',
        *[f'<script src="{data[f]}"></script>' for f in js],
        *[f'<link href="{data[f]}" rel="stylesheet" />' for f in css],
    ])
