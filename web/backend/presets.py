import hashlib, json, os

from web.backend.utils import raiseHttp, loadPresetsList, completePreset
from utils.utils import getPresetDir, PresetLoader
from utils.parameters import Knows, isKnows, text2diff, Controller, isButton, Settings
from utils.parameters import easy, medium, hard, harder, hardcore, mania, diff2text
from logic.smboolmanager import SMBoolManager
from rom.rom_patches import RomPatches
from utils.db import DB
from logic.logic import Logic

from gluon.http import redirect
from gluon.html import URL
from gluon.validators import IS_NOT_EMPTY, IS_ALPHANUMERIC, IS_LENGTH

class Presets(object):
    def __init__(self, session, request, cache):
        self.session = session
        self.request = request
        self.cache = cache
        # to compute hardrooms/hellruns
        Logic.factory('vanilla')

        self.vars = self.request.vars

    def run(self):
        self.initPresetsSession()

        # use web2py builtin cache to avoid recomputing the hardrooms requirements
        hardRooms = self.cache.ram('hardRooms', lambda:dict(), time_expire=None)
        if len(hardRooms) == 0:
            self.computeHardRooms(hardRooms)

        hellRuns = self.cache.ram('hellRuns', lambda:dict(), time_expire=None)
        if len(hellRuns) == 0:
            self.computeHellruns(hellRuns)

        if self.vars.action is not None:
            (ok, msg) = self.validatePresetsParams(self.vars.action)
            if not ok:
                self.session.flash = msg
                redirect(URL(r=self.request, f='presets'))
            else:
                self.session.presets['currentTab'] = self.vars.currenttab

            preset = self.vars.preset

        # in web2py.js, in disableElement, remove 'working...' to have action with correct value.
        # called when using "What's in the logic for this skills preset ?" from another page.
        if self.vars.action == 'Load':
            # check that the presets file exists
            fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
            if os.path.isfile(fullPath):
                # load it
                try:
                    params = PresetLoader.factory(fullPath).params
                    self.updatePresetsSession()
                    self.session.presets["presetDict"] = None
                except Exception as e:
                    self.session.flash = "L:Error loading the preset {}: {}".format(preset, e)
            else:
                self.session.flash = "Presets file not found: {}".format(fullPath)
            redirect(URL(r=self.request, f='presets'))

        # load conf from session if available
        error = False
        try:
            params = self.loadPreset()
        except Exception as e:
            self.session.presets['preset'] = 'regular'
            self.session.flash = "S:Error loading the preset: {}".format(e)
            error = True
        if error == True:
            redirect(URL(r=self.request, f='presets'))

        # load presets list
        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)

        # add missing knows/settings
        completePreset(params)

        # compute score for skill bar
        skillBarData = self.getSkillLevelBarData(self.session.presets['preset'])

        # send values to view
        return dict(desc=Knows.desc, difficulties=diff2text,
                    categories=Knows.categories, settings=params['Settings'], knows=params['Knows'],
                    easy=easy, medium=medium, hard=hard, harder=harder, hardcore=hardcore, mania=mania,
                    controller=params['Controller'], stdPresets=stdPresets, tourPresets=tourPresets,
                    comPresets=comPresets, skillBarData=skillBarData, hardRooms=hardRooms, hellRuns=hellRuns)

    def maxPresetsReach(self):
        # to prevent a spammer to create presets in a loop and fill the fs
        maxPresets = 4096
        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)
        return len(comPresets) >= maxPresets

    def loadPreset(self):
        # load conf from session if available
        loaded = False

        if self.vars.action is not None:
            # press solve, load or save button
            if self.vars.action in ['Update', 'Create']:
                # store the changes in case the form won't be accepted
                presetDict = self.genJsonFromParams(self.vars)
                self.session.presets['presetDict'] = presetDict
                params = PresetLoader.factory(presetDict).params
                loaded = True
            elif self.vars.action in ['Load']:
                # nothing to load, we'll load the new params file with the load form code
                pass
        else:
            # no forms button pressed
            if self.session.presets['presetDict'] is not None:
                params = PresetLoader.factory(self.session.presets['presetDict']).params
                loaded = True

        if not loaded:
            presetPath = '{}/{}.json'.format(getPresetDir(self.session.presets['preset']),
                                             self.session.presets['preset'])
            params = PresetLoader.factory(presetPath).params

        return params

    def validatePresetsParams(self, action):
        if action == 'Create':
            preset = self.vars.presetCreate
        else:
            preset = self.vars.preset

        if IS_NOT_EMPTY()(preset)[1] is not None:
            return (False, "Preset name is empty")
        if IS_ALPHANUMERIC()(preset)[1] is not None:
            return (False, "Preset name must be alphanumeric")
        if IS_LENGTH(32)(preset)[1] is not None:
            return (False, "Preset name must be max 32 chars")

        if action in ['Create', 'Update']:
            if IS_NOT_EMPTY()(self.vars.password)[1] is not None:
                return (False, "Password is empty")
            if IS_ALPHANUMERIC()(self.vars.password)[1] is not None:
                return (False, "Password must be alphanumeric")
            if IS_LENGTH(32)(self.vars.password)[1] is not None:
                return (False, "Password must be max 32 chars")

            # check that there's not two buttons for the same action
            map = {}
            for button in Controller.__dict__:
                if isButton(button):
                    value = self.vars[button]
                    if button == "Moonwalk":
                        if value not in [None, 'on', 'off']:
                            return (False, "Invalid value for Moonwalk: {}".format(value))
                    else:
                        if value is None:
                            return (False, "Button {} not set".format(button))
                        else:
                            if value in map:
                                return (False, "Action {} set for two buttons: {} and {}".format(value, button, map[value]))
                            map[value] = button

        if self.vars.currenttab not in ['Global', 'Techniques1', 'Techniques2', 'Techniques3', 'Techniques4', 'Techniques5', 'Techniques6', 'Techniques7', 'Techniques8', 'Mapping']:
            return (False, "Wrong value for current tab: [{}]".format(self.vars.currenttab))

        return (True, None)

    def getSkillLevelBarData(self, preset):
        result = {
            'name': preset
        }
        try:
            params = PresetLoader.factory('{}/{}.json'.format(getPresetDir(preset), preset)).params
            result['custom'] = (preset, params['score'])
            # add stats on the preset
            result['knowsKnown'] = len([know for know in params['Knows'] if params['Knows'][know][0] == True])
        except:
            result['custom'] = (preset, 'N/A')
            result['knowsKnown'] = 'N/A'

        # get score of standard presets
        standardScores = self.cache.ram('standardScores', lambda:dict(), time_expire=None)
        if not standardScores:
            for preset in ['newbie', 'casual', 'regular', 'veteran', 'expert', 'master', 'samus']:
                score = PresetLoader.factory('{}/{}.json'.format(getPresetDir(preset), preset)).params['score']
                standardScores[preset] = score

        result['standards'] = standardScores

        with DB() as db:
            result['lastAction'] = db.getPresetLastActionDate(result['custom'][0])

        # TODO: normalize result (or not ?)
        return result

    def initPresetsSession(self):
        if self.session.presets is None:
            self.session.presets = {}

            self.session.presets['preset'] = 'regular'
            self.session.presets['presetDict'] = None
            self.session.presets['currentTab'] = 'Global'

    def updatePresetsSession(self):
        if self.vars.action == 'Create':
            self.session.presets['preset'] = self.vars.presetCreate
        elif self.vars.preset is None:
            self.session.presets['preset'] = 'regular'
        else:
            self.session.presets['preset'] = self.vars.preset

    def computeGauntlet(self, sm, bomb, addVaria):
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

    def computeXray(self, sm, addVaria):
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

    def computeHardRooms(self, hardRooms):
        # add gravity patch (as we add it by default in the randomizer)
        RomPatches.ActivePatches.append(RomPatches.NoGravityEnvProtection)

        sm = SMBoolManager()

        # xray
        xray = {}
        xray['Suitless'] = self.computeXray(sm, False)
        xray['Varia'] = self.computeXray(sm, True)
        hardRooms['X-Ray'] = xray

        # gauntlet
        gauntlet = {}
        gauntlet['SuitlessBomb'] = self.computeGauntlet(sm, 'Bomb', False)
        gauntlet['SuitlessPowerBomb'] = self.computeGauntlet(sm, 'PowerBomb', False)
        gauntlet['VariaBomb'] = self.computeGauntlet(sm, 'Bomb', True)
        gauntlet['VariaPowerBomb'] = self.computeGauntlet(sm, 'PowerBomb', True)
        hardRooms['Gauntlet'] = gauntlet

        return hardRooms

    def addCF(self, sm, count):
        sm.addItem('Morph')
        sm.addItem('PowerBomb')

        for i in range(count):
            sm.addItem('Missile')
            sm.addItem('Missile')
            sm.addItem('Super')
            sm.addItem('Super')
            sm.addItem('PowerBomb')
            sm.addItem('PowerBomb')

    def computeHellruns(self, hellRuns):
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
        hellRuns[hellRun]["NoScrew"] = self.computeLNHellRun(sm, False)
        hellRuns[hellRun]["Screw"] = self.computeLNHellRun(sm, True)

    def getNearestDifficulty(self, difficulty):
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

    def computeLNHellRun(self, sm, addScrew):
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
                    self.addCF(sm, cf)
                    for etank in range(19):
                        ret = sm.canHellRun(**params)

                        if ret.bool == True:
                            nEtank = 0
                            for item in ret.items:
                                if item.find('ETank') != -1:
                                    nEtank = int(item[0:item.find('-ETank')])
                                    break
                            result[actualHellRun][key]['ETank'][self.getNearestDifficulty(ret.difficulty)] = nEtank
                            result[actualHellRun][key]['CF'][self.getNearestDifficulty(ret.difficulty)] = cf

                        sm.addItem('ETank')
        return result

    def skillPresetActionWebService(self):
        print("skillPresetActionWebService call")

        if self.session.presets is None:
            self.session.presets = {}

        # for create/update, not load
        (ok, msg) = self.validatePresetsParams(self.vars.action)
        if not ok:
            raiseHttp(400, json.dumps(msg))
        else:
            self.session.presets['currentTab'] = self.vars.currenttab

        if self.vars.action == 'Create':
            preset = self.vars.presetCreate
        else:
            preset = self.vars.preset

        # check if the presets file already exists
        password = self.vars['password'] or ""
        password = password.encode('utf-8')
        passwordSHA256 = hashlib.sha256(password).hexdigest()
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if os.path.isfile(fullPath):
            if self.vars.action == 'load':
                self.session.presets['preset'] = self.vars.preset
                self.session.presets['currentTab'] = self.vars.currenttab
                skillBarData = self.getSkillLevelBarData(self.session.presets['preset'])
                out = PresetLoader.factory(fullPath).params
                # add missing knows/settings
                completePreset(out)
                out.pop('password', None)
                out['skillBarData']= skillBarData
                return json.dumps(out)
            # load it
            end = False
            try:
                oldParams = PresetLoader.factory(fullPath).params
            except Exception as e:
                msg = "UC:Error loading the preset {}: {}".format(preset, e)
                end = True
            if end == True:
                raiseHttp(400, json.dumps(msg))

            # check if password match
            if 'password' in oldParams and passwordSHA256 == oldParams['password']:
                # update the presets file
                paramsDict = self.genJsonFromParams(self.vars)
                paramsDict['password'] = passwordSHA256
                try:
                    PresetLoader.factory(paramsDict).dump(fullPath)
                    with DB() as db:
                        db.addPresetAction(preset, 'update')
                    self.updatePresetsSession()
                    msg = "Preset {} updated".format(preset)
                    return json.dumps(msg)
                except Exception as e:
                    msg = "Error writing the preset {}: {}".format(preset, e)
                    raiseHttp(400, json.dumps(msg))
            else:
                msg = "Password mismatch with existing presets file {}".format(preset)
                raiseHttp(400, json.dumps(msg))
        else:
            # prevent a malicious user from creating presets in a loop
            if not self.maxPresetsReach():
                # write the presets file
                paramsDict = self.genJsonFromParams(self.vars)
                paramsDict['password'] = passwordSHA256
                try:
                    PresetLoader.factory(paramsDict).dump(fullPath)
                    with DB() as db:
                        db.addPresetAction(preset, 'create')
                    self.updatePresetsSession()

                    # add new preset in cache
                    (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)
                    comPresets.append(preset)
                    comPresets.sort(key=lambda v: v.upper())

                    msg = "Preset {} created".format(preset)
                    return json.dumps(msg)
                except Exception as e:
                    msg = "Error writing the preset {}: {}".format(preset, e)
                    raiseHttp(400, json.dumps(msg))
                redirect(URL(r=self.request, f='presets'))
            else:
                msg = "Sorry, maximum number of presets reached, can't add more"
                raiseHttp(400, json.dumps(msg))

    def genJsonFromParams(self, vars):
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

    def skillPresetListWebService(self):
        # load presets list
        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)
        return json.dumps(stdPresets + tourPresets + comPresets)
