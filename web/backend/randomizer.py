import sys, os, urllib, tempfile, random, subprocess, base64, json, uuid
from datetime import datetime

from web.backend.utils import loadPresetsList, loadRandoPresetsList, displayNames
from web.backend.utils import validateWebServiceParams, getCustomMapping, localIpsDir, raiseHttp, getInt
from utils.utils import getRandomizerDefaultParameters, getDefaultMultiValues, PresetLoader, getPresetDir, getPythonExec
from graph.graph_utils import GraphUtils
from utils.db import DB
from logic.logic import Logic
from utils.objectives import Objectives

from gluon.validators import IS_ALPHANUMERIC, IS_LENGTH, IS_MATCH
from gluon.html import OPTGROUP

class Randomizer(object):
    def __init__(self, session, request, response, cache):
        self.session = session
        self.request = request
        self.response = response
        self.cache = cache
        # required for GraphUtils access to access points
        Logic.factory('vanilla')

        self.vars = self.request.vars

    def run(self):
        self.initRandomizerSession()

        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)

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
            "hud": "Full rando with remaining major upgrades in the area shown in the HUD",
            "hud_hard": "Low resources and VARIA HUD enabled to help you track of actual items count",
            "hud_start": "Non-vanilla start with Major or Chozo split",
            "minimizer":"Typical 'boss rush' settings with random start and nerfed charge",
            "minimizer_hardcore":"Have fun 'rushing' bosses with no equipment on a tiny map",
            "minimizer_maximizer":"No longer a boss rush",
            "objectives_all_bosses":"Kill all bosses/minibosses",
            "objectives_clear_areas":"Clear 5 random areas and end with fast Tourian",
            "objectives_hard_heat":"All Norfair-related objectives, possibly without a suit",
            "objectives_hard_water":"All Maridia-related objectives, possibly without a suit",
            "objectives_long": "5 random long objectives and Vanilla Tourian",
            "objectives_memes":"Do all the memes and rush to the ship",
            "objectives_robots_notweaks":"Collect Bomb and Space Jump to activate the robots, then rush to the ship",
            "objectives_short": "3 random short objectives and Disabled Tourian",
            "quite_random": "randomizes a few significant settings to have various seeds",
            "scavenger_hard":"Pretty hostile Scavenger mode",
            "scavenger_random":"Randomize everything within Scavenger mode",
            "scavenger_speedrun":"Quickest Scavenger settings",
            "scavenger_vanilla_but_not":"Items are vanilla, but area and bosses are not",
            "stupid_hard": "hardest possible settings",
            "surprise": "quite_random with Area/Boss/Doors/Start settings randomized",
            "vanilla": "closest possible to vanilla Super Metroid",
            "way_of_chozo": "chozo split with boss randomization",
            "where_am_i": "Area mode with random start location and early morph",
            "where_is_morph": "Area mode with late Morph",
            "Season_Races": "rando league races (Majors/Minors split)",
            "Torneio_SGPT3_stage1": "SG Português Tournament 2022 group stage",
            "Torneio_SGPT3_stage2": "SG Português Tournament 2022 playoff stage",
            "SGLive2022_Game_1": "SGLive 2022 Randomizer Tournament race 1",
            "SGLive2022_Game_2": "SGLive 2022 Randomizer Tournament race 2",
            "SGLive2022_Game_3": "SGLive 2022 Randomizer Tournament race 3",
            "SMRAT2021": "Randomizer Accessible Tournament 2021",
            "VARIA_Weekly": "Casual logic community races",
            "Boyz_League_SM_Rando": "Boyz League Tournament",
            "RLS4W2": "Rando League Season 4 week 2",
            "RLS4W3": "Rando League Season 4 week 3",
            "RLS4W4": "Rando League Season 4 week 4",
            "RLS4W5": "Rando League Season 4 week 5",
            "RLS4W7": "Rando League Season 4 week 7",
            "RLS4GS": "Rando League Season 4 playoff GS",
            "RLS4P1": "Rando League Season 4 playoff 1",
            "RLS4P2": "Rando League Season 4 playoff 2",
        }

        randoPresetsCategories = {
            "Standard": ["", "default", "Chozo_Speedrun", "free", "haste", "vanilla"],
            "Hud": ["hud", "hud_hard", "hud_start"],
            "Scavenger": ["scavenger_hard", "scavenger_random", "scavenger_speedrun", "scavenger_vanilla_but_not"],
            "Area": ["way_of_chozo", "where_am_i", "where_is_morph"],
            "Doors": ["doors_long", "doors_short"],
            "Minimizer": ["minimizer", "minimizer_hardcore", "minimizer_maximizer"],
            "Objectives": ["objectives_all_bosses", "objectives_clear_areas", "objectives_memes", "objectives_short", "objectives_long", "objectives_robots_notweaks"],
            "Hard": ["hardway2hell", "highway2hell", "stupid_hard", "objectives_hard_heat", "objectives_hard_water"],
            "Random": ["all_random", "quite_random", "surprise"],
            "Tournament": ["Season_Races", "SMRAT2021", "VARIA_Weekly", "RLS4W2", "RLS4W3", "RLS4W4", "RLS4W5", "RLS4W7", "RLS4GS", "RLS4P1", "RLS4P2", "Torneio_SGPT3_stage1", "Torneio_SGPT3_stage2", "SGLive2022_Game_1", "SGLive2022_Game_2", "SGLive2022_Game_3", "Boyz_League_SM_Rando"]
        }

        startAPs = GraphUtils.getStartAccessPointNamesCategory()
        startAPs = [OPTGROUP(_label="Standard", *startAPs["regular"]),
                    OPTGROUP(_label="Custom", *startAPs["custom"]),
                    OPTGROUP(_label="Custom (Area rando only)", *startAPs["area"])]

        # get multi
        currentMultiValues = self.getCurrentMultiValues()
        defaultMultiValues = getDefaultMultiValues()

        # objectives self exclusions
        objectivesExclusions = Objectives.getExclusions()
        objectivesTypes = Objectives.getObjectivesTypes()
        objectivesSort = Objectives.getObjectivesSort()
        objectivesCategories = Objectives.getObjectivesCategories()

        # check if we have a guid in the url
        url = self.request.env.request_uri.split('/')
        if len(url) > 0 and url[-1] != 'randomizer':
            # a seed unique key was passed as parameter
            key = url[-1]

            # decode url
            key = urllib.parse.unquote(key)

            # sanity check
            if IS_MATCH('^[0-9a-z-]*$')(key)[1] is None and IS_LENGTH(maxsize=36, minsize=36)(key)[1] is None:
                with DB() as db:
                    seedInfo = db.getSeedInfo(key)
                if seedInfo is not None and len(seedInfo) > 0:
                    defaultParams = getRandomizerDefaultParameters()
                    defaultParams.update(seedInfo)
                    seedInfo = defaultParams

                    # check that the seed ips is available
                    if seedInfo["upload_status"] in ['pending', 'uploaded', 'local']:
                        # load parameters in session
                        for key, value in seedInfo.items():
                            if key in ["complexity", "randoPreset", "raceMode"]:
                                continue
                            elif key in defaultMultiValues:
                                keyMulti = key + 'MultiSelect'
                                if keyMulti in seedInfo:
                                    if key == 'objective' and value == 'nothing':
                                        self.session.randomizer[key] = ""
                                    else:
                                        self.session.randomizer[key] = seedInfo[key]
                                    valueMulti = seedInfo[keyMulti]
                                    if type(valueMulti) == str:
                                        valueMulti = valueMulti.split(',')
                                    self.session.randomizer[keyMulti] = valueMulti
                                    currentMultiValues[key] = valueMulti
                            elif key in self.session.randomizer and 'MultiSelect' not in key:
                                self.session.randomizer[key] = value

        return dict(stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets,
                    randoPresetsDesc=randoPresetsDesc, randoPresetsCategories=randoPresetsCategories,
                    startAPs=startAPs, currentMultiValues=currentMultiValues, defaultMultiValues=defaultMultiValues,
                    maxsize=sys.maxsize, displayNames=displayNames, objectivesExclusions=objectivesExclusions,
                    objectivesTypes=objectivesTypes, objectivesSort=objectivesSort,
                    objectivesCategories=objectivesCategories)

    def initRandomizerSession(self):
        if self.session.randomizer is None:
            self.session.randomizer = getRandomizerDefaultParameters()

    def getCurrentMultiValues(self):
        defaultMultiValues = getDefaultMultiValues()
        for key in defaultMultiValues:
            keyMulti = key + 'MultiSelect'
            if key == "objective":
                if key in self.session.randomizer:
                    defaultMultiValues[key] = self.session.randomizer[key]
                elif keyMulti in self.session.randomizer:
                    defaultMultiValues[key] = self.session.randomizer[keyMulti]
            else:
                if keyMulti in self.session.randomizer:
                    defaultMultiValues[key] = self.session.randomizer[keyMulti]
        return defaultMultiValues

    # race mode
    def getMagic(self):
        return random.randint(1, sys.maxsize)

    def storeLocalIps(self, key, fileName, ipsData):
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

    def webService(self):
        # web service to compute a new random (returns json string)
        print("randomizerWebService")

        # check validity of all parameters
        switchs = ['suitsRestriction', 'hideItems', 'strictMinors',
                   'areaLayout',
                   'doorsColorsRando', 'allowGreyDoors', 'escapeRando', 'removeEscapeEnemies',
                   'bossRandomization', 'minimizer',
                   'funCombat', 'funMovement', 'funSuits',
                   'layoutPatches', 'variaTweaks', 'nerfedCharge',
                   'itemsounds', 'elevators_speed', 'fast_doors', 'spinjumprestart',
                   'rando_speed', 'animals', 'No_Music', 'random_music',
                   'Infinite_Space_Jump', 'refill_before_save', 'hud', "scavRandomized",
                   'relaxed_round_robin_cf']
        quantities = ['missileQty', 'superQty', 'powerBombQty', 'minimizerQty', "scavNumLocs"]
        multis = ['majorsSplit', 'progressionSpeed', 'progressionDifficulty', 'tourian',
                  'morphPlacement', 'energyQty', 'startLocation', 'gravityBehaviour',
                  'areaRandomization']
        others = ['complexity', 'paramsFileTarget', 'seed', 'preset', 'maxDifficulty', 'objective']
        validateWebServiceParams(self.request, switchs, quantities, multis, others, isJson=True)

        # randomize
        db = DB()
        id = db.initRando()

        # race mode
        useRace = False
        if self.vars.raceMode == 'on':
            magic = self.getMagic()
            useRace = True

        (fd1, presetFileName) = tempfile.mkstemp()
        presetFileName += '.json'
        (fd2, jsonFileName) = tempfile.mkstemp()
        (fd3, jsonRandoPreset) = tempfile.mkstemp()

        print("randomizerWebService, params validated")
        for var in self.vars:
            print("{}: {}".format(var, self.vars[var]))

        with open(presetFileName, 'w') as presetFile:
            presetFile.write(self.vars.paramsFileTarget)

        if self.vars.seed == '0':
            self.vars.seed = str(random.randrange(sys.maxsize))

        preset = self.vars.preset

        params = [getPythonExec(),  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
                  '--runtime', '20',
                  '--output', jsonFileName,
                  '--param', presetFileName,
                  '--preset', preset]

        if useRace == True:
            params += ['--race', str(magic)]

        # load content of preset to get controller mapping
        try:
            controlMapping = PresetLoader.factory(presetFileName).params['Controller']
        except Exception as e:
            os.close(fd1)
            os.remove(presetFileName)
            os.close(fd2)
            os.remove(jsonFileName)
            os.close(fd3)
            os.remove(jsonRandoPreset)
            return json.dumps({"status": "NOK", "errorMsg": "randomizerWebService: can't load the preset"})

        (custom, controlParam) = getCustomMapping(controlMapping)
        if custom == True:
            params += ['--controls', controlParam]
            if "Moonwalk" in controlMapping and controlMapping["Moonwalk"] == True:
                params.append('--moonwalk')

        randoPresetDict = {var: self.vars[var] for var in self.vars if var != 'paramsFileTarget'}
        # set multi select as list as expected in a rando preset
        for var, value in randoPresetDict.items():
            if 'MultiSelect' in var:
                randoPresetDict[var] = value.split(',')

        if self.vars.objectiveRandom == 'true':
            randoPresetDict['objective'] = self.vars.nbObjective # 0-5 or "random"
            randoPresetDict['objectiveMultiSelect'] = self.vars.objective.split(',')
        else:
            randoPresetDict['objective'] = self.vars.objective.split(',')

        with open(jsonRandoPreset, 'w') as randoPresetFile:
            json.dump(randoPresetDict, randoPresetFile)
        params += ['--randoPreset', jsonRandoPreset]

        db.addRandoParams(id, self.vars)

        print("before calling: {}".format(' '.join(params)))
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
            if self.storeLocalIps(guid, locsItems["fileName"], locsItems["ips"]):
                db.addRandoUploadResult(id, guid, locsItems["fileName"])
                locsItems['seedKey'] = guid
                if self.vars.get('wantsCustomize') == 'true':
                    # don't send the ips if they requested a redirect to the customize page
                    locsItems.pop('ips')
            db.close()

            os.close(fd1)
            os.remove(presetFileName)
            os.close(fd2)
            os.remove(jsonFileName)
            os.close(fd3)
            os.remove(jsonRandoPreset)

            locsItems["status"] = "OK"
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
            os.close(fd3)
            os.remove(jsonRandoPreset)
            return json.dumps({"status": "NOK", "errorMsg": msg})

    def presetWebService(self):
        # web service to get the content of the preset file
        if self.vars.preset == None:
            raiseHttp(400, "Missing parameter preset")
        preset = self.vars.preset

        if IS_ALPHANUMERIC()(preset)[1] is not None:
            raiseHttp(400, "Preset name must be alphanumeric")

        if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
            raiseHttp(400, "Preset name must be between 1 and 32 characters")

        print("presetWebService: preset={}".format(preset))

        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)

        # check that the presets file exists
        if os.path.isfile(fullPath):
            # load it
            try:
                params = PresetLoader.factory(fullPath).params
            except Exception as e:
                raiseHttp(400, "Can't load the preset")
            params = json.dumps(params)
            return params
        else:
            raiseHttp(400, "Preset not found")

    def sessionWebService(self):
        # web service to update the session
        switchs = ['suitsRestriction', 'hideItems', 'strictMinors',
                   'areaLayout',
                   'doorsColorsRando', 'allowGreyDoors', 'escapeRando', 'removeEscapeEnemies',
                   'bossRandomization', 'minimizer',
                   'funCombat', 'funMovement', 'funSuits',
                   'layoutPatches', 'variaTweaks', 'nerfedCharge',
                   'itemsounds', 'elevators_speed', 'fast_doors', 'spinjumprestart',
                   'rando_speed', 'animals', 'No_Music', 'random_music',
                   'Infinite_Space_Jump', 'refill_before_save', 'hud', "scavRandomized",
                   'relaxed_round_robin_cf']
        quantities = ['missileQty', 'superQty', 'powerBombQty', 'minimizerQty', "scavNumLocs"]
        multis = ['majorsSplit', 'progressionSpeed', 'progressionDifficulty', 'tourian',
                  'morphPlacement', 'energyQty', 'startLocation', 'gravityBehaviour',
                  'areaRandomization']
        others = ['complexity', 'preset', 'randoPreset', 'maxDifficulty', 'minorQty', 'objective']
        validateWebServiceParams(self.request, switchs, quantities, multis, others)

        if self.session.randomizer is None:
            self.session.randomizer = {}

        self.session.randomizer['complexity'] = self.vars.complexity
        self.session.randomizer['preset'] = self.vars.preset
        # after selecting a rando preset and changing an option users can end up
        # generating a seed with the rando preset selected but not with all
        # the options set with the rando preset, so always empty the rando preset
        self.session.randomizer['randoPreset'] = ""
        self.session.randomizer['maxDifficulty'] = self.vars.maxDifficulty
        self.session.randomizer['suitsRestriction'] = self.vars.suitsRestriction
        self.session.randomizer['hideItems'] = self.vars.hideItems
        self.session.randomizer['strictMinors'] = self.vars.strictMinors
        self.session.randomizer['missileQty'] = self.vars.missileQty
        self.session.randomizer['superQty'] = self.vars.superQty
        self.session.randomizer['powerBombQty'] = self.vars.powerBombQty
        self.session.randomizer['minorQty'] = self.vars.minorQty
        self.session.randomizer['areaRandomization'] = self.vars.areaRandomization
        self.session.randomizer['areaLayout'] = self.vars.areaLayout
        self.session.randomizer['doorsColorsRando'] = self.vars.doorsColorsRando
        self.session.randomizer['allowGreyDoors'] = self.vars.allowGreyDoors
        self.session.randomizer['escapeRando'] = self.vars.escapeRando
        self.session.randomizer['removeEscapeEnemies'] = self.vars.removeEscapeEnemies
        self.session.randomizer['bossRandomization'] = self.vars.bossRandomization
        self.session.randomizer['minimizer'] = self.vars.minimizer
        self.session.randomizer['minimizerQty'] = self.vars.minimizerQty
        self.session.randomizer['funCombat'] = self.vars.funCombat
        self.session.randomizer['funMovement'] = self.vars.funMovement
        self.session.randomizer['funSuits'] = self.vars.funSuits
        self.session.randomizer['layoutPatches'] = self.vars.layoutPatches
        self.session.randomizer['variaTweaks'] = self.vars.variaTweaks
        self.session.randomizer['nerfedCharge'] = self.vars.nerfedCharge
        self.session.randomizer['relaxed_round_robin_cf'] = self.vars.relaxed_round_robin_cf
        self.session.randomizer['itemsounds'] = self.vars.itemsounds
        self.session.randomizer['elevators_speed'] = self.vars.elevators_speed
        self.session.randomizer['fast_doors'] = self.vars.fast_doors
        self.session.randomizer['spinjumprestart'] = self.vars.spinjumprestart
        self.session.randomizer['rando_speed'] = self.vars.rando_speed
        self.session.randomizer['animals'] = self.vars.animals
        self.session.randomizer['No_Music'] = self.vars.No_Music
        self.session.randomizer['random_music'] = self.vars.random_music
        self.session.randomizer['Infinite_Space_Jump'] = self.vars.Infinite_Space_Jump
        self.session.randomizer['refill_before_save'] = self.vars.refill_before_save
        self.session.randomizer['hud'] = self.vars.hud
        self.session.randomizer['scavNumLocs'] = self.vars.scavNumLocs
        self.session.randomizer['scavRandomized'] = self.vars.scavRandomized
        self.session.randomizer['tourian'] = self.vars.tourian

        # objective is a special multi select
        self.session.randomizer['objectiveRandom'] = self.vars.objectiveRandom
        if self.vars.objectiveRandom == 'true':
            self.session.randomizer['objectiveMultiSelect'] = self.vars.objective.split(',')
            self.session.randomizer['nbObjective'] = self.vars.nbObjective
        else:
            self.session.randomizer['objective'] = self.vars.objective.split(',')

        for multi in multis:
            self.session.randomizer[multi] = self.vars[multi]
            if self.vars[multi] == 'random':
                self.session.randomizer[multi+"MultiSelect"] = self.vars[multi+"MultiSelect"].split(',')

        # to create a new rando preset, uncomment next lines
        #with open('rando_presets/new.json', 'w') as jsonFile:
        #    json.dump(self.session.randomizer, jsonFile)

    def randoParamsWebService(self):
        # get a json string of the randomizer parameters for a given seed.
        # seed is the id in randomizer table, not actual seed number.
        if self.vars.seed == None:
            raiseHttp(400, "Missing parameter seed", True)

        seed = getInt(self.request, 'seed', False)
        if seed < 0 or seed > sys.maxsize:
            raiseHttp(400, "Wrong value for seed", True)

        with DB() as db:
            (seed, params) = db.getRandomizerSeedParams(seed)

        return json.dumps({"seed": seed, "params": params})

    def updateRandoSession(self, randoPreset):
        for key, value in randoPreset.items():
            self.session.randomizer[key] = value

    def loadRandoPreset(self, presetFullPath):
        with open(presetFullPath) as jsonFile:
            randoPreset = json.load(jsonFile)
        return randoPreset

    def randoPresetWebService(self):
        # web service to get the content of the rando preset file
        if self.vars.randoPreset == None:
            raiseHttp(400, "Missing parameter rando preset")
        preset = self.vars.randoPreset

        if IS_ALPHANUMERIC()(preset)[1] is not None:
            raiseHttp(400, "Preset name must be alphanumeric")

        if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
            raiseHttp(400, "Preset name must be between 1 and 32 characters")

        if self.vars.origin not in ["extStats", "randomizer"]:
            raiseHttp(400, "Unknown origin")

        print("randoPresetWebService: preset={}".format(preset))

        fullPath = 'rando_presets/{}.json'.format(preset)

        # check that the preset file exists
        if os.path.isfile(fullPath):
            # load it
            try:
                # can be called from randomizer and extended stats pages
                updateSession = self.vars.origin == "randomizer"

                params = self.loadRandoPreset(fullPath)

                # first load default preset to set all parameters to default values,
                # thus preventing parameters from previous loaded preset to stay when loading a new one,
                # (like comfort patches from the free preset).
                if updateSession and preset != 'default':
                    defaultParams = self.loadRandoPreset('rando_presets/default.json')
                    # don't reset skill preset
                    defaultParams.pop('preset', None)
                    defaultParams.update(params)
                    params = defaultParams

                if updateSession:
                    self.updateRandoSession(params)

                return json.dumps(params)
            except Exception as e:
                raiseHttp(400, "Can't load the rando preset: {}".format(e))
        else:
            raiseHttp(400, "Rando preset not found")
