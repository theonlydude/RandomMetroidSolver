
import random, sys, copy, logging

from rando.Filler import Filler, FrontFiller
from rando.Choice import ItemThenLocChoice
from rando.MiniSolver import MiniSolver
from rando.ItemLocContainer import ContainerSoftBackup
from rando.RandoServices import ComebackCheckType
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
        self.nFrontFillSteps = 0
        self.stepIncr = 1
        # based on runtime limit, help the random fill with up to three front fill steps
        self.runtimeSteps = [self.runtimeLimit_s/4, self.runtimeLimit_s/2, self.runtimeLimit_s*3/4, sys.maxsize]

    def initFiller(self):
        super(FillerRandom, self).initFiller()
        self.log.debug("initFiller. maxDiff="+str(self.settings.maxDiff))
        self.createBaseLists()

    def createBaseLists(self):
        self.baseContainer = ContainerSoftBackup(self.container)
        self.helpContainer = ContainerSoftBackup(self.container)

    def createHelpingBaseLists(self):
        self.helpContainer = ContainerSoftBackup(self.container)

    def resetContainer(self):
        self.baseContainer.restore(self.container, resetSM=True)

    def resetHelpingContainer(self):
        self.helpContainer.restore(self.container, resetSM=False)

    def isBeatable(self, maxDiff=None):
        return self.miniSolver.isBeatable(self.container.itemLocations, maxDiff=maxDiff)

    def getLocations(self, item):
        return [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocation(item, loc, self.container)]

    def step(self):
        # here a step is not an item collection but a whole fill attempt
        while not self.container.isPoolEmpty():
            item = random.choice(self.container.itemPool)
            locs = self.getLocations(item)
            if not locs:
                self.log.debug("FillerRandom: constraint collision during step {} for item {}".format(self.nSteps, item['Type']))
                self.resetHelpingContainer()
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
            self.resetHelpingContainer()
            if (self.nSteps + 1) % 100 == 0:
                sys.stdout.write('x')
                sys.stdout.flush()

            if self.runtime_s > self.runtimeSteps[self.nFrontFillSteps]:
                # store the step for debug purpose
                sys.stdout.write('n({})'.format(self.nSteps))
                sys.stdout.flush()
                # help the random fill with a bit of frontfill
                self.nFrontFillSteps += self.stepIncr
                self.createBaseLists(updateBase=False)

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

class FrontFillerNoCopy(FrontFiller):
    def __init__(self, startAP, graph, restrictions, container):
        super(FrontFillerNoCopy, self).__init__(startAP, graph, restrictions, container)

    def initContainer(self):
        self.container = self.baseContainer

class FrontFillerKickstart(FrontFiller):
    def __init__(self, startAP, graph, restrictions, emptyContainer):
        super(FrontFillerKickstart, self).__init__(startAP, graph, restrictions, emptyContainer)

    def initContainer(self):
        self.container = self.baseContainer

    # if during first step no item is a progression item, check all two items pairs instead of just one item
    def step(self, onlyBossCheck=False):
        if self.nSteps > 0:
            return super(FrontFillerKickstart, self).step(onlyBossCheck)

        (itemLocDict, isProg) = self.services.getPossiblePlacements(self.ap, self.container, ComebackCheckType.NoCheck)
        if isProg == True:
            self.log.debug("FrontFillerKickstart: found prog item")
            return super(FrontFillerKickstart, self).step(onlyBossCheck)

        self.log.debug("FrontFillerKickstart: no prog item found, kickstart")

        # save container
        saveEmptyContainer = ContainerSoftBackup(self.container)

        # key is (item1, item2)
        pairItemLocDict = {}

        # keep only unique items in itemLocDict
        uniqItemLocDict = {}
        for item, locs in itemLocDict.items():
            if item.item['Type'] in ['NoEnergy', 'Nothing']:
                continue
            if item.item['Type'] not in [it.item['Type'] for it in uniqItemLocDict.keys()]:
                uniqItemLocDict[item] = locs
        assert len(uniqItemLocDict) > 0

        curLocsBefore = self.services.currentLocations(self.ap, self.container)
        assert len(curLocsBefore) > 0

        self.log.debug("search for progression with a second item")
        for item1, locs1 in uniqItemLocDict.items():
            # collect first item in first available location
            self.cache.reset()
            self.container.collect({'Item': item1.item, 'Location': curLocsBefore[0]})
            saveAfterFirst = ContainerSoftBackup(self.container)

            curLocsAfterFirst = self.services.currentLocations(self.ap, self.container)
            if not curLocsAfterFirst:
                saveEmptyContainer.restore(self.container)
                continue

            for item2, locs2 in uniqItemLocDict.items():
                if item1.item['Type'] == item2.item['Type']:
                    continue

                if (item1, item2) in pairItemLocDict.keys() or (item2, item1) in pairItemLocDict.keys():
                    continue

                # collect second item in first available location
                self.cache.reset()
                self.container.collect({'Item': item2.item, 'Location': curLocsAfterFirst[0]})

                curLocsAfterSecond = self.services.currentLocations(self.ap, self.container)
                if not curLocsAfterSecond:
                    saveAfterFirst.restore(self.container)
                    continue

                pairItemLocDict[(item1, item2)] = [curLocsBefore, curLocsAfterFirst, curLocsAfterSecond]
                saveAfterFirst.restore(self.container)

            saveEmptyContainer.restore(self.container)

        # check if a pair was found
        if len(pairItemLocDict) == 0:
            self.log.debug("no pair was found")
            return super(FrontFillerKickstart, self).step(onlyBossCheck)

        # choose a pair of items which create progression
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("pairItemLocDict:")
            for key, locs in pairItemLocDict.items():
                self.log.debug("{}->{}: {}".format(key[0].item['Type'], key[1].item['Type'], [l['Name'] for l in locs[2]]))

        keys = list(pairItemLocDict.keys())
        key = random.choice(keys)

        # collect them
        availableLocs = pairItemLocDict[key]
        self.collect({'Item': key[0].item, 'Location': availableLocs[0][0]})
        self.collect({'Item': key[1].item, 'Location': availableLocs[1][0]})

        return True

# actual random filler will real solver on top of mini
class FillerRandomSpeedrun(FillerRandom):
    def __init__(self, graphSettings, graph, restrictions, container, diffSteps=0):
        super(FillerRandomSpeedrun, self).__init__(graphSettings.startAP, graph, restrictions, container)
        self.nFrontFillSteps = graphSettings.getRandomFillHelp()

    def initFiller(self):
        super(FillerRandomSpeedrun, self).initFiller()
        self.restrictions.precomputeRestrictions(self.container)

    # depending on the start location help the randomfill with a little bit of frontfill.
    # also if the randomfill can't find a solution, help him too with a little bit of frontfill.
    def createBaseLists(self, updateBase=True):
        if self.nFrontFillSteps > 0:
            if updateBase == False:
                super(FillerRandomSpeedrun, self).resetContainer()
            filler = FrontFillerKickstart(self.startAP, self.graph, self.restrictions, self.container)
            condition = filler.createStepCountCondition(self.nFrontFillSteps)
            (isStuck, itemLocations, progItems) = filler.generateItems(condition)
            # do not stop if we got stuck while trying to help the random fill
            if updateBase == True:
                assert not isStuck
            self.settings.runtimeLimit_s -= filler.runtime_s
            self.log.debug(self.container.dump())
        if updateBase == True:
            # our container is updated, we can create base lists
            super(FillerRandomSpeedrun, self).createBaseLists()
            # reset help steps to zero
            self.nFrontFillSteps = 0
        else:
            super(FillerRandomSpeedrun, self).createHelpingBaseLists()

    def getLocations(self, item):
        return [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocationFast(item['Type'], loc['Name'], self.container)]

    def isBeatable(self, maxDiff=None):
        miniOk = self.miniSolver.isBeatable(self.container.itemLocations, maxDiff=maxDiff)
        if miniOk == False:
            return False
        sys.stdout.write('s')
        graphLocations = self.container.getLocsForSolver()
        solver = RandoSolver(self.restrictions.split, self.startAP, self.graph, graphLocations)
        if(solver.solveRom() == -1):
            sys.stdout.write('X')
            sys.stdout.flush()
            return False
        sys.stdout.write('S({}/{}ms)'.format(self.nSteps+1, int(self.runtime_s*1000)))
        sys.stdout.flush()
        return True
