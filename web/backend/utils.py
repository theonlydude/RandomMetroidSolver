import sys, os, json

from graph.vanilla.graph_locations import locations
from graph.vanilla.graph_access import accessPoints
from rom.romreader import RomReader
from utils.doorsmanager import DoorsManager
from utils.utils import getDefaultMultiValues, getPresetDir, removeChars
from utils.parameters import Knows, isKnows, Controller, isButton

from gluon.validators import IS_ALPHANUMERIC, IS_LENGTH, IS_MATCH
from gluon.http import HTTP

localIpsDir = 'varia_repository'

def loadPresetsList(cache):
    # use a cache to avoid reading the files everytime
    presets = cache.ram('skillPresets', lambda:dict(), time_expire=None)
    if presets:
        return presets.values()

    files = sorted(os.listdir('community_presets'), key=lambda v: v.upper())
    stdPresets = ['newbie', 'casual', 'regular', 'veteran', 'expert', 'master']
    tourPresets = ['Season_Races', 'SMRAT2021', 'Torneio_SGPT2']
    comPresets = [os.path.splitext(file)[0] for file in files if file != '.git']

    presets['stdPresets'] = stdPresets
    presets['tourPresets'] = tourPresets
    presets['comPresets'] = comPresets

    return presets.values()

def loadRandoPresetsList(cache, filter=False):
    presets = cache.ram('randoPresets', lambda:dict(), time_expire=None)
    if not presets:
        tourPresets = ['Season_Races', 'SMRAT2021', 'VARIA_Weekly',
                       'Torneio_SGPT3_stage1', 'Torneio_SGPT3_stage2',
                       'SGLive2022_Game_1', 'SGLive2022_Game_2', 'SGLive2022_Game_3']
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
    # split locs
    addresses["ranges"] += [0x10F550, 0x10F5D8]
    # scavenger hunt items list (16 prog items + hunt over + terminator, each is a word)
    scavengerListSize = 36
    addresses["ranges"] += [0x10F5D8, 0x10F5D8+scavengerListSize]
    if plando == True:
        # plando addresses
        addresses["ranges"] += [0x2F6000, 0x2F6100]
        # plando transitions (4 bytes per transitions, ap#/2 transitions)
        addresses["ranges"] += [0x2F6100, 0x2F6100+((len(addresses["transitions"])/2) * 4)]

    return addresses

# if we have an internal parameter value different from its display value
displayNames = {"FullWithHUD": "Full Countdown"}

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
