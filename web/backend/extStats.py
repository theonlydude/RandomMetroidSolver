import os, json

from web.backend.utils import raiseHttp, completePreset, transformStats, zipStats
from web.backend.utils import loadPresetsList, loadRandoPresetsList
from utils.utils import getPresetDir, PresetLoader
from utils.parameters import Knows
from graph.vanilla.graph_locations import locations
from utils.db import DB

from gluon.validators import IS_LENGTH, IS_ALPHANUMERIC
from gluon.http import redirect
from gluon.html import URL

class ExtStats(object):
    def __init__(self, session, request, cache):
        self.session = session
        self.request = request
        self.cache = cache

        self.vars = self.request.vars

    def run(self):
        self.initExtStatsSession()

        if self.vars.action == 'Load':
            (ok, msg) = self.validateExtStatsParams()
            if not ok:
                self.session.flash = msg
                redirect(URL(r=self.request, f='extStats'))

            self.updateExtStatsSession()

            skillPreset = self.vars.preset
            randoPreset = self.vars.randoPreset

            # load rando preset to get majors split
            fullPath = 'rando_presets/{}.json'.format(randoPreset)
            if not os.path.isfile(fullPath):
                raiseHttp(400, "Unknown rando preset: {}".format(e))
            try:
                with open(fullPath) as jsonFile:
                    randoPresetContent = json.load(jsonFile)
            except Exception as e:
                raiseHttp(400, "Can't load the rando preset: {}".format(e))
            majorsSplit = randoPresetContent.get("majorsSplit", "Full")

            # load skill preset
            fullPath = '{}/{}.json'.format(getPresetDir(skillPreset), skillPreset)
            try:
                skillPresetContent = PresetLoader.factory(fullPath).params
                completePreset(skillPresetContent)
            except Exception as e:
                raiseHttp(400, "Error loading the skill preset: {}".format(e))

            with DB() as db:
                (itemsStats, techniquesStats, difficulties, solverStatsRaw) = db.getExtStat(skillPreset, randoPreset)

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
            nbLocs = 109
            if itemsStats and len(itemsStats) != nbItems:
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

        (randoPresets, tourRandoPresets) = loadRandoPresetsList(self.cache, filter=True)
        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)

        return dict(stdPresets=stdPresets, tourPresets=tourPresets,
                    randoPresets=randoPresets, tourRandoPresets=tourRandoPresets,
                    itemsStats=itemsStats, techniquesStats=techniquesStats,
                    categories=Knows.categories, knowsDesc=Knows.desc, skillPresetContent=skillPresetContent,
                    locations=locations, majorsSplit=majorsSplit, difficulties=difficulties, solverStats=solverStats)

    def initExtStatsSession(self):
        if self.session.extStats is None:
            self.session.extStats = {
                'preset': 'regular',
                'randoPreset': 'default'
            }

    def updateExtStatsSession(self):
        if self.session.extStats is None:
            self.session.extStats = {}

        self.session.extStats['preset'] = self.vars.preset
        self.session.extStats['randoPreset'] = self.vars.randoPreset

    def validateExtStatsParams(self):
        for (preset, directory) in [("preset", "standard_presets"), ("randoPreset", "rando_presets")]:
            if self.vars[preset] == None:
                return (False, "Missing parameter preset")
            preset = self.vars[preset]

            if IS_ALPHANUMERIC()(preset)[1] is not None:
                return (False, "Wrong value for preset, must be alphanumeric")

            if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
                return (False, "Wrong length for preset, name must be between 1 and 32 characters")

            # check that preset exists
            fullPath = '{}/{}.json'.format(directory, preset)
            if not os.path.isfile(fullPath):
                return (False, "Unknown preset: {}".format(preset))

        return (True, None)
