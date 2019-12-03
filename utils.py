import os, json, sys, re, random

from parameters import Knows, Settings, Controller, isKnows, isSettings, isButton
from parameters import easy, medium, hard, harder, hardcore, mania
from smbool import SMBool

def isStdPreset(preset):
    return preset in ['noob', 'casual', 'regular', 'veteran', 'speedrunner', 'master', 'samus', 'solution', 'Season_Races', 'SMRAT2020']

def removeChars(string, toRemove):
    return re.sub('[{}]+'.format(toRemove), '', string)

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
    for k in sorted(weightDict, key=lambda kv: (kv[1], kv[0])):
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

if sys.version_info.major == 2:
    def isString(string):
        return type(string) in [str, unicode]
else:
    def isString(string):
        return type(string) == str

class PresetLoader(object):
    @staticmethod
    def factory(params):
        # can be a json, a python file or a dict with the parameters
        if isString(params):
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

def loadRandoPreset(randoPreset, args):
    # load the rando preset json file and add the parameters inside it to the args parser
    with open(randoPreset) as randoPresetFile:
        randoParams = json.load(randoPresetFile)

    if "animals" in randoParams and randoParams["animals"] == "on":
        args.animals = True
    if "areaLayout" in randoParams and randoParams["areaLayout"] == "off":
        args.areaLayoutBase = True
    if "variaTweaks" in randoParams and randoParams["variaTweaks"] == "off":
        args.noVariaTweaks = True
    if "maxDifficulty" in randoParams and randoParams["maxDifficulty"] != "no difficulty cap":
        args.maxDifficulty = randoParams["maxDifficulty"]
    if "suitsRestriction" in randoParams and randoParams["suitsRestriction"] != "off":
        if randoParams["suitsRestriction"] == "on":
            args.suitsRestriction = True
        else:
            args.suitsRestriction = "random"
    if "hideItems" in randoParams and randoParams["hideItems"] != "off":
        if randoParams["hideItems"] == "on":
            args.hideItems = True
        else:
            args.hideItems = "random"
    if "strictMinors" in randoParams and randoParams["strictMinors"] != "off":
        if randoParams["strictMinors"] == "on":
            args.strictMinors = True
        else:
            args.strictMinors = "random"

    if "layoutPatches" in randoParams and randoParams["layoutPatches"] == "off":
        args.noLayout = True
    if "noGravHeat" in randoParams and randoParams["noGravHeat"] == "off":
        args.noGravHeat = True

    if "areaRandomization" in randoParams and randoParams["areaRandomization"] == "on":
        args.area = True
    if "bossRandomization" in randoParams and randoParams["bossRandomization"] == "on":
        args.bosses = True

    if "funCombat" in randoParams and randoParams["funCombat"] != "off":
        if randoParams["funCombat"] == "on":
            args.superFun.append("Combat")
        else:
            args.superFun.append("CombatRandom")
    if "funMovement" in randoParams and randoParams["funMovement"] != "off":
        if randoParams["funMovement"] == "on":
            args.superFun.append("Movement")
        else:
            args.superFun.append("MovementRandom")
    if "funSuits" in randoParams and randoParams["funSuits"] != "off":
        if randoParams["funSuits"] == "on":
            args.superFun.append("Suits")
        else:
            args.superFun.append("SuitsRandom")

    patches = ["skip_intro", "skip_ceres", "itemsounds", "spinjumprestart", "rando_speed", "elevators_doors_speed"]

    for patch in patches:
        if patch in randoParams and randoParams[patch] == "on":
            args.patches.append(patch + '.ips')
    if "No_Music" in randoParams and randoParams["No_Music"] == "on":
        args.patches.append("No_Music")

    if "morphPlacement" in randoParams:
        args.morphPlacement = randoParams["morphPlacement"]
    if "majorsSplit" in randoParams:
        args.majorsSplit = randoParams["majorsSplit"]
    if "progressionDifficulty" in randoParams:
        args.progressionDifficulty = randoParams["progressionDifficulty"]

    if "progressionSpeed" in randoParams:
        if type(randoParams["progressionSpeed"]) == list:
            args.progressionSpeed = ",".join(randoParams["progressionSpeed"])
        else:
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
