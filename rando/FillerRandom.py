
import random, sys, copy

from rando.Filler import Filler
from rando.Choice import ItemThenLocChoice
from rando.MiniSolver import MiniSolver

# simple, uses mini solver only
class FillerRandom(Filler):
    def __init__(self, startAP, graph, restrictions, container):
        super(FillerRandom, self).__init__(startAP, graph, restrictions, container)
        self.solver = MiniSolver(startAP, graph, restrictions)

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

    def step(self):
        item = random.choice(self.container.itemPool)
        locs = [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocation(item, loc)]
        loc = random.choice(locs)
        itemLoc = {'Item':item, 'Location':loc}
        self.container.collect(itemLoc, pickup=False)
        if self.container.isPoolEmpty():
            # pool is exhausted, use mini solver to see if it is beatable
            if self.solver.isBeatable(self.container.itemLocations):
                sys.stdout.write('o')
                sys.stdout.flush()
            else:
                # reset container to force a retry
                self.resetContainer()
                sys.stdout.write('x')
                sys.stdout.flush()
        # never stuck, stop if we hit runtime limit only
        return True

# TODO actual random filler will real solver instead of just mini
