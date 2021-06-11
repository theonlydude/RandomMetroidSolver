import random, sys, copy, logging, time

from rando.Filler import Filler
from rando.ItemLocContainer import getLocListStr
from solver.randoSolver import RandoSolver
from utils.parameters import easy, medium, hard, harder, hardcore, mania, infinity


class ScavengerSolver(RandoSolver):
    def __init__(self, startAP, areaGraph, locations, scavLocs, maxDiff, progDiff, vcr):
        super(ScavengerSolver, self).__init__("Full", startAP, areaGraph, locations)
        self.remainingScavLocs = scavLocs
        self.maxDiff = maxDiff
        self.progDiff = progDiff
        self.threshold = self.getThreshold()
        self.scavOrder = []
        self.vcr = vcr

    def getThreshold(self):
        if self.maxDiff >= mania:
            return harder
        else:
            return hard

    def pickupScav(self, nextScav):
        self.scavOrder.append(nextScav)
        self.remainingScavLocs.remove(nextScav)
        self.log.debug("pickupScav: {}".format(nextScav.Name))

    def chooseNextScavLoc(self, scavAvailable):
        harder = [loc for loc in scavAvailable if loc.difficulty.difficulty >= self.threshold]
        easier = [loc for loc in scavAvailable if loc.difficulty.difficulty < self.threshold]
        if harder and self.progDiff == "harder":
            return random.choice(harder)
        elif easier and self.progDiff == "easier":
            return random.choice(easier)
        else:
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
            self.log.debug("scavAvailable: "+getLocListStr(scavAvailable))
            nextScav = self.chooseNextScavLoc(scavAvailable)
            self.pickupScav(nextScav)
            return self.collectMajor(nextScav)
        else:
            # fallback to base solver behaviour to handle comeback etc
            loc = super(ScavengerSolver, self).nextDecision(majorsAvailable, majorsAvailable, hasEnoughMinors, diffThreshold) # not a typo, the args are the same, and we overwrote minorsAvailable
            if loc is not None and loc in self.remainingScavLocs:
                self.pickupScav(loc)
            return loc

    def cancelLastItems(self, count):
        # remove locs from scavOrder
        a=len(self.visitedLocations)-count
        for loc in self.visitedLocations[a:]:
            if loc in self.scavOrder:
                self.scavOrder.remove(loc)
                self.remainingScavLocs.append(loc)
                self.log.debug("cancel scav loc: {}".format(loc.Name))

        # call base func
        super(ScavengerSolver, self).cancelLastItems(count)

class FillerScavenger(Filler):
    def __init__(self, startAP, graph, restrictions, fullContainer, endDate=infinity):
        super(FillerScavenger, self).__init__(startAP, graph, restrictions, fullContainer, endDate)
        self.remainingScavLocs = restrictions.scavLocs[:]
        self.log.debug("FillerScavenger ctor. scavLocs="+getLocListStr(self.remainingScavLocs))

    def initContainer(self):
        self.container = self.baseContainer
        self.log.debug("FillerScavenger. container="+self.container.dump())

    def initFiller(self):
        super(FillerScavenger, self).initFiller()
        locs = self.container.getLocsForSolver()
        self.solver = ScavengerSolver(self.startAP, self.graph, locs, self.remainingScavLocs, self.maxDiff, self.settings.progDiff, self.vcr)

    def itemPoolCondition(self):
        return len(self.remainingScavLocs) > 0

    def step(self):
        self.solver.solveRom()
        self.container.cleanLocsAfterSolver()
        if self.itemPoolCondition():
            return False
        return True

    def getProgressionItemLocations(self):
        self.log.debug("Final Scavenger list: {}".format(getLocListStr(self.solver.scavOrder)))
        return [self.container.getItemLoc(loc) for loc in self.solver.scavOrder]
