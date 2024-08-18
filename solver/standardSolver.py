import os

from solver.commonSolver import CommonSolver
from solver.conf import StandardSolverConf
from solver.out import Out
from solver.comeback import ComeBack
from solver.runtimeLimiter import RuntimeLimiter
from logic.helpers import Pickup
from utils.utils import PresetLoader
from utils.parameters import infinity
from utils.parameters import Knows, isKnows, Settings, getDiffThreshold
from utils.objectives import Objectives
import utils.log

class StandardSolver(CommonSolver):
    # given a rom and parameters returns the estimated difficulty
    def __init__(self, args):
        self.log = utils.log.get('Solver')

        self.conf = StandardSolverConf(args)

        # add optional modules
        self.modules = []
        if args.firstItemsLog is not None:
            from solver.modules import ModuleLogFirst
            self.modules.append(ModuleLogFirst(self, args.firstItemsLog))
        if args.extStatsFilename is not None:
            from solver.modules import ModuleExtStats
            self.modules.append(ModuleExtStats(self, args.extStatsFilename, args.extStatsStep))
        if args.vcr is True:
            from solver.modules import ModuleVCR
            self.modules.append(ModuleVCR(romFileName=args.romFileName))
        if args.checkDuplicateMajor is True:
            from solver.modules import ModuleCheckDupMajor
            self.modules.append(ModuleCheckDupMajor(self))

        # can be called from command line (console) or from web site (web)
        self.output = Out.factory(args.outputType, self, args.outputFileName)

        self.objectives = Objectives()

        self.romConf = self.loadRom(args.romFileName)

        # if tourian is disabled force item pickup to any%
        if self.romConf.tourian == 'Disabled':
            self.conf.pickupStrategy = 'any'

        self.loadPreset(self.conf.presetFileName)

        self.pickup = Pickup(self.conf.pickupStrategy)

        self.comeBack = ComeBack(self)

        self.runtimeLimiter = RuntimeLimiter(args.runtimeLimit_s)

    def solveRom(self):
        (self.difficulty, self.itemsOk) = self.computeDifficulty()
        (self.knowsUsed, self.knowsKnown, self.knowsUsedList) = self.getKnowsUsed()

        # vcr / ext stats
        for module in self.modules:
            module.dump()

        # console or html output
        self.output.out()

        return self.difficulty

    def getRemainMajors(self):
        return [loc for loc in self.container.majorLocations if loc.difficulty.bool == False and loc.itemName not in ['Nothing', 'NoEnergy']]

    def getRemainMinors(self):
        if self.romConf.majorsSplit == 'Full':
            return None
        return [loc for loc in self.container.minorLocations if loc.difficulty.bool == False and loc.itemName not in ['Nothing', 'NoEnergy']]

    def getSkippedMajors(self):
        return [loc for loc in self.container.majorLocations if loc.difficulty.bool == True and loc.itemName not in ['Nothing', 'NoEnergy']]

    def getUnavailMajors(self):
        return [loc for loc in self.container.majorLocations if loc.difficulty.bool == False and loc.itemName not in ['Nothing', 'NoEnergy']]

    def getDiffThreshold(self):
        return getDiffThreshold(self.conf.difficultyTarget)

    def getKnowsUsed(self):
        knowsUsed = []
        for loc in self.container.visitedLocations():
            knowsUsed += loc.difficulty.knows

        # get unique knows
        knowsUsed = list(set(knowsUsed))
        knowsUsedCount = len(knowsUsed)

        # get total of known knows
        knowsKnownCount = len([knows for  knows in Knows.__dict__ if isKnows(knows) and getattr(Knows, knows).bool == True])
        knowsKnownCount += len([hellRun for hellRun in Settings.hellRuns if Settings.hellRuns[hellRun] is not None])

        return (knowsUsedCount, knowsKnownCount, knowsUsed)

    def tryRemainingLocs(self):
        # use preset which knows every techniques to test the remaining locs to
        # find which technique could allow to continue the seed
        locations = self.container.getAllLocs()

        # instanciate a new smbool manager to reset the cache
        from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
        self.smbm = SMBoolManager()
        presetFileName = os.path.expanduser('~/RandomMetroidSolver/standard_presets/solution.json')
        presetLoader = PresetLoader.factory(presetFileName)
        presetLoader.load()
        self.smbm.createKnowsFunctions()

        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.container.lastAP())

        return [loc for loc in locations if loc.difficulty.bool == True]
