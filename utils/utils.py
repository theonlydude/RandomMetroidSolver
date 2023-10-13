import os, json, sys, re, random

from utils.parameters import Knows, Settings, Controller, isKnows, isSettings, isButton
from utils.parameters import easy, medium, hard, harder, hardcore, mania
from logic.smbool import SMBool

def getPythonExec():
    try:
        from utils.python_exec import pythonExec
    except:
        pythonExec = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)
    return pythonExec

def isStdPreset(preset):
    return preset in ['newbie', 'casual', 'regular', 'veteran', 'expert', 'master', 'samus', 'solution', 'Season_Races', 'SMRAT2021', 'Torneio_SGPT3']

def getPresetDir(preset):
    if isStdPreset(preset):
        return 'standard_presets'
    else:
        return 'community_presets'

def removeChars(string, toRemove):
    return re.sub('[{}]+'.format(toRemove), '', string)

def range_union(ranges):
    ret = []
    for rg in sorted([[r.start, r.stop] for r in ranges]):
        begin, end = rg[0], rg[-1]
        if ret and ret[-1][1] > begin:
            ret[-1][1] = max(ret[-1][1], end)
        else:
            ret.append([begin, end])
    return [range(r[0], r[1]) for r in ret]

# https://github.com/robotools/fontParts/commit/7cb561033929cfb4a723d274672e7257f5e68237
def normalizeRounding(n):
    # Normalizes rounding as Python 2 and Python 3 handing the rounding of halves (0.5, 1.5, etc) differently.
    # This normalizes rounding to be the same in both environments.
    if round(0.5) != 1 and n % 1 == .5 and not int(n) % 2:
        return int((round(n) + (abs(n) / n) * 1))
    else:
        return int(round(n))

# gauss random in [0, r] range
# the higher the slope, the less probable extreme values are.
def randGaussBounds(r, slope=5):
    r = float(r)
    n = normalizeRounding(random.gauss(r/2, r/slope))
    if n < 0:
        n = 0
    if n > r:
        n = int(r)
    return n

# from a relative weight dictionary, gives a normalized range dictionary
# example :
# { 'a' : 10, 'b' : 17, 'c' : 3 } => {'c': 0.1, 'a':0.4333333, 'b':1 }
def getRangeDict(weightDict):
    total = float(sum(weightDict.values()))
    rangeDict = {}
    current = 0.0
    for k in sorted(weightDict, key=weightDict.get):
        w = float(weightDict[k]) / total
        current += w
        rangeDict[k] = current

    return rangeDict

def chooseFromRange(rangeDict):
    r = random.random()
    val = None
    for v in sorted(rangeDict, key=rangeDict.get):
        val = v
        if r < rangeDict[v]:
            return v
    return val

class PresetLoader(object):
    @staticmethod
    def factory(params):
        # can be a json, a python file or a dict with the parameters
        if type(params) == str:
            ext = os.path.splitext(params)
            if ext[1].lower() == '.json':
                return PresetLoaderJson(params)
            else:
                raise Exception("PresetLoader: wrong parameters file type: {}".format(ext[1]))
        elif type(params) is dict:
            return PresetLoaderDict(params)
        else:
            raise Exception("wrong parameters input, is neither a string nor a json file name: {}::{}".format(params, type(params)))

    def __init__(self):
        if 'Knows' not in self.params:
            self.params['Knows'] = {}
        if 'Settings' not in self.params:
            self.params['Settings'] = {}
        if 'Controller' not in self.params:
            self.params['Controller'] = {}
        self.params['score'] = self.computeScore()

    def load(self):
        # update the parameters in the parameters classes: Knows, Settings

        # Knows
        for param in self.params['Knows']:
            if isKnows(param) and hasattr(Knows, param):
                setattr(Knows, param, SMBool(self.params['Knows'][param][0],
                                             self.params['Knows'][param][1],
                                             ['{}'.format(param)]))
        # Settings
        ## hard rooms
        for hardRoom in ['X-Ray', 'Gauntlet']:
            if hardRoom in self.params['Settings']:
                Settings.hardRooms[hardRoom] = Settings.hardRoomsPresets[hardRoom][self.params['Settings'][hardRoom]]

        ## bosses
        for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
            if boss in self.params['Settings']:
                Settings.bossesDifficulty[boss] = Settings.bossesDifficultyPresets[boss][self.params['Settings'][boss]]

        ## hellruns
        for hellRun in ['Ice', 'MainUpperNorfair', 'LowerNorfair']:
            if hellRun in self.params['Settings']:
                Settings.hellRuns[hellRun] = Settings.hellRunPresets[hellRun][self.params['Settings'][hellRun]]

        # Controller
        for button in self.params['Controller']:
            if isButton(button):
                setattr(Controller, button, self.params['Controller'][button])

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.params, jsonFile)

    def printToScreen(self):
        print("self.params: {}".format(self.params))

        print("loaded knows: ")
        for knows in Knows.__dict__:
            if isKnows(knows):
                print("{}: {}".format(knows, Knows.__dict__[knows]))
        print("loaded settings:")
        for setting in Settings.__dict__:
            if isSettings(setting):
                print("{}: {}".format(setting, Settings.__dict__[setting]))
        print("loaded controller:")
        for button in Controller.__dict__:
            if isButton(button):
                print("{}: {}".format(button, Controller.__dict__[button]))
        print("loaded score: {}".format(self.params['score']))

    def computeScore(self):
        # the more techniques you know and the smaller the difficulty of the techniques, the higher the score
        diff2score = {
            easy: 6,
            medium: 5,
            hard: 4,
            harder: 3,
            hardcore: 2,
            mania: 1
        }

        boss2score = {
            "He's annoying": 1,
            'A lot of trouble': 1,
            "I'm scared!": 1,
            "It can get ugly": 1,
            'Default': 2,
            'Quick Kill': 3,
            'Used to it': 3,
            'Is this really the last boss?': 3,
            'No problemo': 4,
            'Piece of cake': 4,
            'Nice cutscene bro': 4
        }

        hellrun2score = {
            'No thanks': 0,
            'Solution': 0,
            'Gimme energy': 2,
            'Default': 4,
            'Bring the heat': 6,
            'I run RBO': 8
        }

        hellrunLN2score = {
            'Default': 0,
            'Solution': 0,
            'Bring the heat': 6,
            'I run RBO': 12
        }

        xray2score = {
            'Aarghh': 0,
            'Solution': 0,
            "I don't like spikes": 1,
            'Default': 2,
            "I don't mind spikes": 3,
            'D-Boost master': 4
        }

        gauntlet2score = {
            'Aarghh': 0,
            "I don't like acid": 1,
            'Default': 2
        }

        score = 0

        # knows
        for know in Knows.__dict__:
            if isKnows(know):
                if know in self.params['Knows']:
                    if self.params['Knows'][know][0] == True:
                        score += diff2score[self.params['Knows'][know][1]]
                else:
                    # if old preset with not all the knows, use default values for the know
                    if Knows.__dict__[know].bool == True:
                        score += diff2score[Knows.__dict__[know].difficulty]

        # hard rooms
        hardRoom = 'X-Ray'
        if hardRoom in self.params['Settings']:
            score += xray2score[self.params['Settings'][hardRoom]]

        hardRoom = 'Gauntlet'
        if hardRoom in self.params['Settings']:
            score += gauntlet2score[self.params['Settings'][hardRoom]]

        # bosses
        for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
            if boss in self.params['Settings']:
                score += boss2score[self.params['Settings'][boss]]

        # hellruns
        for hellRun in ['Ice', 'MainUpperNorfair']:
            if hellRun in self.params['Settings']:
                score += hellrun2score[self.params['Settings'][hellRun]]

        hellRun = 'LowerNorfair'
        if hellRun in self.params['Settings']:
            score += hellrunLN2score[self.params['Settings'][hellRun]]

        return score

class PresetLoaderJson(PresetLoader):
    # when called from the test suite
    def __init__(self, jsonFileName):
        with open(jsonFileName) as jsonFile:
            self.params = json.load(jsonFile)
        super(PresetLoaderJson, self).__init__()

class PresetLoaderDict(PresetLoader):
    # when called from the website
    def __init__(self, params):
        self.params = params
        super(PresetLoaderDict, self).__init__()

def getDefaultMultiValues():
    from graph.graph_utils import GraphUtils
    from utils.objectives import Objectives
    from logic.logic import Logic
    # assume vanilla logic for default multi values
    Logic.factory('vanilla')
    defaultMultiValues = {
        'startLocation': GraphUtils.getStartAccessPointNames(),
        'majorsSplit': ['Full', 'FullWithHUD', 'Major', 'Chozo', 'Scavenger'],
        'progressionSpeed': ['slowest', 'slow', 'medium', 'fast', 'fastest', 'basic', 'VARIAble', 'speedrun'],
        'progressionDifficulty': ['easier', 'normal', 'harder'],
        'morphPlacement': ['early', 'late', 'normal'],
        'energyQty': ['ultra sparse', 'sparse', 'medium', 'vanilla'],
        'gravityBehaviour': ['Vanilla', 'Balanced', 'Progressive'],
        'areaRandomization': ['off', 'full', 'light'],
        'objective': Objectives.getAllGoals(exclude=True),
        'tourian': ['Vanilla', 'Fast', 'Disabled'],
        'logic': ['vanilla', 'mirror'],
    }
    return defaultMultiValues

# from web to cli
def convertParam(randoParams, param, inverse=False):
    value = randoParams.get(param, "off" if inverse == False else "on")
    if value == "on":
        return True if inverse == False else False
    elif value == "off":
        return False if inverse == False else True
    elif value == "random":
        return "random"
    raise Exception("invalid value for parameter {}".format(param))

def to_comma_string(value):
    if isinstance(value, list):
        return ','.join(value)
    return value

def loadRandoPreset(randoPreset, args):
    # load the rando preset json file and add the parameters inside it to the args parser
    with open(randoPreset) as randoPresetFile:
        randoParams = json.load(randoPresetFile)

    # use default params as base
    defaultParams = getRandomizerDefaultParameters()
    defaultParams.update(randoParams)
    randoParams = defaultParams

    if randoParams.get("logic") is not None:
        args.logic = randoParams["logic"]

    if randoParams.get("seed") is not None:
        args.seed = int(randoParams["seed"])

    if randoParams.get("animals", "off") == "on":
        args.animals = True
    if randoParams.get("variaTweaks", "on") == "off":
        args.noVariaTweaks = True
    variaTweaksCustom = randoParams.get("variaTweaksCustom")
    if variaTweaksCustom is None or len(variaTweaksCustom) == 0:
        args.variaTweaksCustom = None
    else:
        args.variaTweaksCustom = to_comma_string(variaTweaksCustom)
    if randoParams.get("maxDifficulty", "infinity") != "infinity":
        args.maxDifficulty = randoParams["maxDifficulty"]
    if randoParams.get("suitsRestriction", "off") != "off":
        if randoParams["suitsRestriction"] == "on":
            args.suitsRestriction = True
        else:
            args.suitsRestriction = "random"
    if randoParams.get("hideItems", "off") != "off":
        if randoParams["hideItems"] == "on":
            args.hideItems = True
        else:
            args.hideItems = "random"
    if randoParams.get("strictMinors", "off") != "off":
        if randoParams["strictMinors"] == "on":
            args.strictMinors = True
        else:
            args.strictMinors = "random"

    if randoParams.get("layoutPatches", "on") == "off":
        args.noLayout = True
    layoutCustom = randoParams.get("layoutCustom")
    if layoutCustom is None or len(layoutCustom) == 0:
        args.layoutCustom = None
    else:
        args.layoutCustom = to_comma_string(layoutCustom)
    if "gravityBehaviour" in randoParams:
        args.gravityBehaviour = randoParams["gravityBehaviour"]
    if randoParams.get("nerfedCharge", "off") == "on":
        args.nerfedCharge = True
    if randoParams.get("revealMap", "on") == "on":
        args.revealMap = True

    args.areaRandomization = randoParams["areaRandomization"]
    if args.areaRandomization == "on":
        # DEPRECATED previously areaRandomization was on/off, now it's off, full, or light
        args.areaRandomization == "full"
    if args.areaRandomization != "off":
        args.areaLayoutBase = convertParam(randoParams, "areaLayout", inverse=True)
    areaLayoutCustom = randoParams.get("areaLayoutCustom")
    if areaLayoutCustom is None or len(areaLayoutCustom) == 0:
        args.areaLayoutCustom = None
    else:
        args.areaLayoutCustom = to_comma_string(areaLayoutCustom)
    args.escapeRando = convertParam(randoParams, "escapeRando")
    if args.escapeRando == True:
        args.noRemoveEscapeEnemies = convertParam(randoParams, "removeEscapeEnemies", inverse=True)

    args.doorsColorsRando = convertParam(randoParams, "doorsColorsRando")
    args.allowGreyDoors = convertParam(randoParams, "allowGreyDoors")
    args.bosses = convertParam(randoParams, "bossRandomization")

    if randoParams.get("funCombat", "off") != "off":
        if randoParams["funCombat"] == "on":
            args.superFun.append("Combat")
        else:
            args.superFun.append("CombatRandom")
    if randoParams.get("funMovement", "off") != "off":
        if randoParams["funMovement"] == "on":
            args.superFun.append("Movement")
        else:
            args.superFun.append("MovementRandom")
    if randoParams.get("funSuits", "off") != "off":
        if randoParams["funSuits"] == "on":
            args.superFun.append("Suits")
        else:
            args.superFun.append("SuitsRandom")

    ipsPatches = ["itemsounds", "spinjumprestart", "rando_speed", "elevators_speed", "fast_doors", "refill_before_save", "relaxed_round_robin_cf", "better_reserves"]
    for patch in ipsPatches:
        if randoParams.get(patch, "off") == "on":
            args.patches.append(patch + '.ips')

    patches = ["No_Music", "Infinite_Space_Jump"]
    for patch in patches:
        if randoParams.get(patch, "off") == "on":
            args.patches.append(patch)

    if randoParams.get("hud", "off") == "on":
        args.hud = True

    if "morphPlacement" in randoParams:
        args.morphPlacement = randoParams["morphPlacement"]
    if "majorsSplit" in randoParams:
        args.majorsSplit = randoParams["majorsSplit"]
        if randoParams["majorsSplit"] == "Scavenger":
            if "scavNumLocs" in randoParams:
                if randoParams["scavNumLocs"] == "random":
                    args.scavNumLocs = 0
                else:
                    args.scavNumLocs = randoParams["scavNumLocs"]
            if "scavRandomized" in randoParams:
                args.scavRandomized = randoParams["scavRandomized"] == "on"
    if "startLocation" in randoParams:
        args.startLocation = randoParams["startLocation"]
    if "progressionDifficulty" in randoParams:
        args.progressionDifficulty = randoParams["progressionDifficulty"]

    if "progressionSpeed" in randoParams:
        args.progressionSpeed = randoParams["progressionSpeed"]

    if "missileQty" in randoParams:
        if randoParams["missileQty"] == "random":
            args.missileQty = 0
        else:
            args.missileQty = randoParams["missileQty"]
    if "superQty" in randoParams:
        if randoParams["superQty"] == "random":
            args.superQty = 0
        else:
            args.superQty = randoParams["superQty"]
    if "powerBombQty" in randoParams:
        if randoParams["powerBombQty"] == "random":
            args.powerBombQty = 0
        else:
            args.powerBombQty = randoParams["powerBombQty"]
    if "minorQty" in randoParams:
        if randoParams["minorQty"] == "random":
            args.minorQty = 0
        else:
            args.minorQty = randoParams["minorQty"]
    if "energyQty" in randoParams:
        args.energyQty = randoParams["energyQty"]

    if randoParams.get("objectiveRandom", "false") == "true":
        nbObjective = randoParams.get("nbObjective", 4)
        args.objective = [nbObjective]
    elif "objective" in randoParams:
        args.objective = randoParams["objective"]
    if randoParams.get("nbObjectivesRequired", "off") != "off":
        if randoParams["nbObjectivesRequired"] == "random":
            args.nbObjectivesRequired = 0
        else:
            args.nbObjectivesRequired = randoParams["nbObjectivesRequired"]
    args.hiddenObjectives = convertParam(randoParams, "hiddenObjectives")
    args.distributeObjectives = convertParam(randoParams, "distributeObjectives")

    if "tourian" in randoParams:
        args.tourian = randoParams["tourian"]

    if randoParams.get("minimizer", "off") == "on" and "minimizerQty" in randoParams:
        args.minimizerN = randoParams["minimizerQty"]

    defaultMultiValues = getDefaultMultiValues()
    multiElems = ["majorsSplit", "startLocation", "energyQty", "morphPlacement", "progressionDifficulty", "progressionSpeed", "gravityBehaviour", "objective", "areaRandomization", "logic"]
    for multiElem in multiElems:
        if multiElem+'MultiSelect' in randoParams:
            setattr(args, multiElem+'List', ','.join(randoParams[multiElem+'MultiSelect']))
        else:
            setattr(args, multiElem+'List', ','.join(defaultMultiValues[multiElem]))

    return randoParams.get("preset")

def getRandomizerDefaultParameters():
    defaultParams = {}
    defaultMultiValues = getDefaultMultiValues()

    defaultParams['logic'] = "vanilla"
    defaultParams['logicMultiSelect'] = defaultMultiValues['logic']
    defaultParams['complexity'] = "simple"
    defaultParams['preset'] = 'regular'
    defaultParams['randoPreset'] = ""
    defaultParams['raceMode'] = "off"
    defaultParams['majorsSplit'] = "Full"
    defaultParams['majorsSplitMultiSelect'] = defaultMultiValues['majorsSplit']
    defaultParams['scavNumLocs'] = "10"
    defaultParams['scavRandomized'] = "off"
    defaultParams['startLocation'] = "Landing Site"
    defaultParams['startLocationMultiSelect'] = defaultMultiValues['startLocation']
    defaultParams['maxDifficulty'] = 'hardcore'
    defaultParams['progressionSpeed'] = "medium"
    defaultParams['progressionSpeedMultiSelect'] = defaultMultiValues['progressionSpeed']
    defaultParams['progressionDifficulty'] = 'normal'
    defaultParams['progressionDifficultyMultiSelect'] = defaultMultiValues['progressionDifficulty']
    defaultParams['morphPlacement'] = "early"
    defaultParams['morphPlacementMultiSelect'] = defaultMultiValues['morphPlacement']
    defaultParams['suitsRestriction'] = "on"
    defaultParams['hideItems'] = "off"
    defaultParams['strictMinors'] = "off"
    defaultParams['missileQty'] = "3"
    defaultParams['superQty'] = "2"
    defaultParams['powerBombQty'] = "1"
    defaultParams['minorQty'] = "100"
    defaultParams['energyQty'] = "vanilla"
    defaultParams['energyQtyMultiSelect'] = defaultMultiValues['energyQty']
    defaultParams['objectiveRandom'] = "off"
    defaultParams['nbObjective'] = "4"
    defaultParams['objective'] = ["kill all G4"]
    defaultParams['objectiveMultiSelect'] = defaultMultiValues['objective']
    defaultParams['nbObjectivesRequired'] = "off"
    defaultParams['hiddenObjectives'] = "off"
    defaultParams['distributeObjectives'] = "off"
    defaultParams['tourian'] = "Vanilla"
    defaultParams['tourianMultiSelect'] = defaultMultiValues['tourian']
    defaultParams['areaRandomization'] = "off"
    defaultParams['areaRandomizationMultiSelect'] = defaultMultiValues['areaRandomization']
    defaultParams['areaLayout'] = "off"
    defaultParams['areaLayoutCustom'] = []
    defaultParams['doorsColorsRando'] = "off"
    defaultParams['allowGreyDoors'] = "off"
    defaultParams['escapeRando'] = "off"
    defaultParams['removeEscapeEnemies'] = "off"
    defaultParams['bossRandomization'] = "off"
    defaultParams['minimizer'] = "off"
    defaultParams['minimizerQty'] = "45"
    defaultParams['funCombat'] = "off"
    defaultParams['funMovement'] = "off"
    defaultParams['funSuits'] = "off"
    defaultParams['layoutPatches'] = "on"
    defaultParams['layoutCustom'] = []
    defaultParams['variaTweaks'] = "on"
    defaultParams['variaTweaksCustom'] = []
    defaultParams['gravityBehaviour'] = "Balanced"
    defaultParams['gravityBehaviourMultiSelect'] = defaultMultiValues['gravityBehaviour']
    defaultParams['nerfedCharge'] = "off"
    defaultParams['revealMap'] = "on"
    defaultParams['relaxed_round_robin_cf'] = "off"
    defaultParams['itemsounds'] = "on"
    defaultParams['elevators_speed'] = "on"
    defaultParams['fast_doors'] = "on"
    defaultParams['spinjumprestart'] = "off"
    defaultParams['rando_speed'] = "off"
    defaultParams['Infinite_Space_Jump'] = "off"
    defaultParams['refill_before_save'] = "off"
    defaultParams['hud'] = "off"
    defaultParams['animals'] = "off"
    defaultParams['No_Music'] = "off"
    defaultParams['random_music'] = "off"

    return defaultParams

def fixEnergy(items):
    # display number of energy used
    energies = [i for i in items if i.find('ETank') != -1]
    if len(energies) > 0:
        (maxETank, maxReserve, maxEnergy) = (0, 0, 0)
        for energy in energies:
            nETank = int(energy[0:energy.find('-ETank')])
            if energy.find('-Reserve') != -1:
                nReserve = int(energy[energy.find(' - ')+len(' - '):energy.find('-Reserve')])
            else:
                nReserve = 0
            nEnergy = nETank + nReserve
            if nEnergy > maxEnergy:
                maxEnergy = nEnergy
                maxETank = nETank
                maxReserve = nReserve
            items.remove(energy)
        items.append('{}-ETank'.format(maxETank))
        if maxReserve > 0:
            items.append('{}-Reserve'.format(maxReserve))

    # keep biggest crystal flash
    cfs = [i for i in items if i.find('CrystalFlash') != -1]
    if len(cfs) > 1:
        maxCf = 0
        for cf in cfs:
            nCf = int(cf[0:cf.find('-CrystalFlash')])
            if nCf > maxCf:
                maxCf = nCf
            items.remove(cf)
        items.append('{}-CrystalFlash'.format(maxCf))
    return items

def dumpErrorMsg(outFileName, msg):
    print("DIAG: " + msg)
    if outFileName is not None:
        with open(outFileName, 'w') as jsonFile:
            json.dump({"errorMsg": msg}, jsonFile)
