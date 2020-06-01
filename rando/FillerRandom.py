
import random, sys, copy

from rando.Filler import Filler
from rando.Choice import ItemThenLocChoice
from rando.MiniSolver import MiniSolver
from solver import RandoSolver
from parameters import infinity
from helpers import diffValue2txt

# simple, uses mini solver only
class FillerRandom(Filler):
    def __init__(self, startAP, graph, restrictions, container, diffSteps=0):
        super(FillerRandom, self).__init__(startAP, graph, restrictions, container)
        self.miniSolver = MiniSolver(startAP, graph, restrictions)
        self.diffSteps = diffSteps
        self.beatableBackup = None

    def initFiller(self):
        super(FillerRandom, self).initFiller()
        self.log.debug("initFiller. maxDiff="+str(self.settings.maxDiff))
        self.baseItemLocs = self.container.itemLocations[:]
        self.baseItemPool = self.container.itemPool[:]
        self.baseUnusedLocations = self.container.unusedLocations[:]

    def resetContainer(self):
        # avoid costly deep copies of locations
        self.container.itemLocations = self.baseItemLocs[:]
        self.container.itemPool = self.baseItemPool[:]
        self.container.unusedLocations = self.baseUnusedLocations[:]

    def isBeatable(self, maxDiff=None):
        return self.miniSolver.isBeatable(self.container.itemLocations, maxDiff=maxDiff)

    def step(self):
        # here a step is not an item collection but a whole fill attempt
        while not self.container.isPoolEmpty():
            item = random.choice(self.container.itemPool)
            locs = [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocation(item, loc, self.container)]
            if len(locs) == 0:
                self.resetContainer()
                continue
            loc = random.choice(locs)
            itemLoc = {'Item':item, 'Location':loc}
            self.container.collect(itemLoc, pickup=False)
        # pool is exhausted, use mini solver to see if it is beatable
        if self.isBeatable():
            sys.stdout.write('o')
            sys.stdout.flush()
        else:
            if self.diffSteps > 0 and self.settings.maxDiff < infinity:
                if self.nSteps < self.diffSteps:
                    couldBeBeatable = self.isBeatable(maxDiff=infinity)
                    if couldBeBeatable:
                        difficulty = max([il['Location']['difficulty'].difficulty for il in self.container.itemLocations])
                        if self.beatableBackup is None or difficulty < self.beatableBackup[1]:
                            self.beatableBackup = (self.container.itemLocations, difficulty)
                elif self.beatableBackup is not None:
                    self.container.itemLocations = self.beatableBackup[0]
                    difficulty = self.beatableBackup[1]
                    self.errorMsg += "Could not find a solution compatible with max difficulty. Estimated seed difficulty: "+diffValue2txt(difficulty)
                    sys.stdout.write('O')
                    sys.stdout.flush()
                    return True
                else:
                    return False
            # reset container to force a retry
            self.resetContainer()
            if self.nSteps % 100 == 0 and self.nSteps > 0:
                sys.stdout.write('x')
                sys.stdout.flush()
        return True

# no logic random fill with one item placement per step. intended for incremental filling,
# so does not copy initial container before filling.
class FillerRandomItems(Filler):
    def __init__(self, startAP, graph, restrictions, container, steps=0):
        super(FillerRandomItems, self).__init__(startAP, graph, restrictions, container)
        self.steps = steps

    def initContainer(self):
        self.container = self.baseContainer

    def generateItems(self, condition=None, vcr=None):
        if condition is None and self.steps > 0:
            condition = self.createStepCountCondition(self.steps)
        return super(FillerRandomItems, self).generateItems(condition, vcr)

    def step(self):
        item = random.choice(self.container.itemPool)
        locs = [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocation(item, loc, self.container)]
        loc = random.choice(locs)
        itemLoc = {'Item':item, 'Location':loc}
        self.container.collect(itemLoc, pickup=False)
        sys.stdout.write('.')
        sys.stdout.flush()
        return True

# actual random filler will real solver on top of mini
class FillerRandomSpeedrun(FillerRandom):
    def __init__(self, startAP, graph, restrictions, container, diffSteps=0):
        super(FillerRandomSpeedrun, self).__init__(startAP, graph, restrictions, container)

    def isBeatable(self, maxDiff=None):
        miniOk = self.miniSolver.isBeatable(self.container.itemLocations, maxDiff=maxDiff)
        if miniOk == False:
            return False
        print("seed validated by mini solver after {} tries in {}ms".format(self.nSteps, int(self.runtime_s*1000)))
        graphLocations = self.container.getLocsForSolver()
        solver = RandoSolver(self.restrictions.split, self.startAP, self.graph, graphLocations)
        if(solver.solveRom() == -1):
            print("ERROR: unsolvable seed with real solver")
            return False

        print("seed validated by real solver")
        return True
