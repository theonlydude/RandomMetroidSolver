
import log, copy, time

from cache import RequestCache
from rando.RandoServices import RandoServices
from rando.Choice import ItemThenLocChoice
from rando.RandoServices import ComebackCheckType
from parameters import infinity
from helpers import diffValue2txt
from graph_access import GraphUtils

class Filler(object):
    def __init__(self, startAP, graph, restrictions, emptyContainer):
        self.startAP = startAP
        self.cache = RequestCache()
        self.graph = graph
        self.services = RandoServices(graph, restrictions, self.cache)
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.runtimeLimit_s = self.settings.runtimeLimit_s
        self.baseContainer = emptyContainer
        self.maxDiff = self.settings.maxDiff
        self.log = log.get('Filler')

    # reinit algo state
    def initFiller(self):
        self.ap = self.startAP
        self.initContainer()
        self.nSteps = 0
        self.errorMsg = ""
        self.settings.maxDiff = self.maxDiff
        self.runtime_s = 0

    def initContainer(self):
        self.container = copy.copy(self.baseContainer)

    def itemPoolCondition(self):
        return not self.container.isPoolEmpty()

    def createStepCountCondition(self, n):
        return lambda: self.nSteps < n

    # shall return (stuck, itemLoc dict list, progression itemLoc dict list)
    def generateItems(self, condition=None, vcr=None):
        self.vcr = vcr
        self.initFiller()
        if condition is None:
            condition = self.itemPoolCondition
        isStuck = False
        startDate = time.process_time()
        while condition() and not isStuck and self.runtime_s <= self.runtimeLimit_s:
            isStuck = not self.step()
            if not isStuck:
                self.nSteps += 1
            self.runtime_s = time.process_time() - startDate
        if condition():
            isStuck = True
            if self.runtime_s > self.runtimeLimit_s:
                self.errorMsg = "Exceeded time limit of "+str(self.runtimeLimit_s) +" seconds"
            else:
                self.errorMsg = "STUCK !\n"+self.container.dump()
        else:
            # check if some locations are above max diff and add relevant message
            locs = self.container.getUsedLocs(lambda loc: loc['difficulty'].difficulty > self.maxDiff)
            aboveMaxDiffStr = '[ ' + ' ; '.join([loc['Name'] + ': ' + diffValue2txt(loc['difficulty'].difficulty) for loc in locs]) + ' ]'
            if aboveMaxDiffStr != '[  ]':
                self.errorMsg += "Maximum difficulty could not be applied everywhere. Affected locations: {}".format(aboveMaxDiffStr)
            isStuck = False
        print('\n%d step(s)' % self.nSteps)
        if self.vcr != None:
            self.vcr.dump()
        return (isStuck, self.container.itemLocations, self.getProgressionItemLocations())

    def collect(self, itemLoc):
        location = itemLoc['Location']
        item = itemLoc['Item']
        self.ap = self.services.collect(self.ap, self.container, itemLoc)
        if self.vcr is not None:
            self.vcr.addLocation(location['Name'], item['Type'])

    def getProgressionItemLocations(self):
        return []

    # return True if ok, False if stuck
    def step(self):
        pass

# very simple front fill algorithm with no rollback and no "softlock checks" (== dessy algorithm)
class FrontFiller(Filler):
    def __init__(self, startAP, graph, restrictions, emptyContainer):
        super(FrontFiller, self).__init__(startAP, graph, restrictions, emptyContainer)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)

    def isEarlyGame(self):
        n = 2 if self.stdStart else 3
        return len(self.container.currentItems) <= n

    # one item/loc per step
    def step(self, onlyBossCheck=False):
        self.cache.reset()
        if not self.services.canEndGame(self.container):
            comebackCheck = ComebackCheckType.ComebackWithoutItem if not self.isEarlyGame() else ComebackCheckType.NoCheck
            (itemLocDict, isProg) = self.services.getPossiblePlacements(self.ap, self.container, comebackCheck)
        else:
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
        itemLoc = self.choice.chooseItemLoc(itemLocDict, isProg)
        if itemLoc is None:
            if onlyBossCheck == False and self.services.onlyBossesLeft(self.ap, self.container):
                self.settings.maxDiff = infinity
                return self.step(onlyBossCheck=True)
            return False
        self.collect(itemLoc)
        return True
