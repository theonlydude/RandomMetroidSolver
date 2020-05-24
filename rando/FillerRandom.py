
import random, sys, copy

from rando.Filler import Filler
from rando.Choice import ItemThenLocChoice
from rando.MiniSolver import MiniSolver
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
            locs = [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocation(item, loc)]
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
            if self.diffSteps > 0:
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
            sys.stdout.write('x')
            sys.stdout.flush()
        return True

# TODO actual random filler will real solver instead of just mini: make it a subclass and change isBeatable method

