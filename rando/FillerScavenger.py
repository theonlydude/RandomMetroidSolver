import random, sys, copy, logging, time

from rando.Filler import Filler
from rando.ItemLocContainer import getLocListStr
from solver.randoSolver import RandoSolver
from utils.parameters import infinity


class ScavengerSolver(RandoSolver):
    def __init__(self, startAP, areaGraph, locations, scavLocs, maxDiff):
        super(ScavengerSolver, self).__init__("Full", startAP, areaGraph, locations)
        self.remainingScavLocs = scavLocs
        self.maxDiff = maxDiff
        self.scavOrder = []

    def pickupScav(self, nextScav):
        self.scavOrder.append(nextScav)
        self.remainingScavLocs.remove(nextScav)

    def chooseNextScavLoc(self, scavAvailable):
        return random.choice(scavAvailable)

    def nextDecision(self, majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold):
        # since solver split is forced to Full, majorsAvailable=minorsAvailable
        # we don't care about hasEnoughMinors, we're gonna pick enough anyway
        # we can ignore diffThreshold as well, we have self.maxDiff
        scavAvailable = [loc for loc in majorsAvailable if loc in self.remainingScavLocs and loc.difficulty.difficulty < self.maxDiff and loc.comeBack == True]
        minorsAvailable = [loc for loc in majorsAvailable if loc not in self.remainingScavLocs and loc.difficulty.difficulty < self.maxDiff and loc.comeBack == True]
        if len(minorsAvailable) > 0:
            nextMinor = random.choice(minorsAvailable)
            return self.collectMajor(nextMinor)
        elif len(scavAvailable) > 0:
            nextScav = self.chooseNextScavLoc(scavAvailable)
            self.pickupScav(nextScav)
            return self.collectMajor(nextScav)
        else:
            # fallback to base solver behaviour to handle comeback etc
            loc = super(ScavengerSolver, self).nextDecision(majorsAvailable, majorsAvailable, hasEnoughMinors, diffThreshold) # not a typo, the args are the same, and we overwrote minorsAvailable            
            if loc is not None and loc in self.remainingScavLocs:
                self.pickupScav(loc)
            return loc

class FillerScavenger(Filler):
    def __init__(self, startAP, graph, restrictions, fullContainer, endDate=infinity):
        super(FillerScavenger, self).__init__(startAP, graph, restrictions, fullContainer, endDate)
        self.remainingScavLocs = restrictions.scavLocs[:]
        print("scavLocs="+getLocListStr(self.remainingScavLocs))

    def initContainer(self):
        self.container = self.baseContainer
        self.log.debug("FillerScavenger. container="+self.container.dump())

    def initFiller(self):
        super(FillerScavenger, self).initFiller()
        locs = self.container.getLocsForSolver()
        self.solver = ScavengerSolver(self.startAP, self.graph, locs, self.remainingScavLocs, self.maxDiff)

    def itemPoolCondition(self):
        return len(self.remainingScavLocs) > 0

    def step(self):
        self.solver.solveRom()
        self.container.cleanLocsAfterSolver()
        if self.itemPoolCondition():
            return False
        return True

    def getProgressionItemLocations(self):
        print(getLocListStr(self.solver.scavOrder))
        return [self.container.getItemLoc(loc) for loc in self.solver.scavOrder]
