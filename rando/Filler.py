
import log, copy, time

from cache import RequestCache
from rando.RandoServices import RandoServices
from rando.Choice import ItemThenLocChoice
from parameters import infinity
from helpers import diffValue2txt

class Filler(object):
    def __init__(self, startAP, graph, restrictions, emptyContainer):
        self.startAP = startAP
        self.cache = RequestCache()
        self.services = RandoServices(graph, restrictions, self.cache)
        self.settings = restrictions.settings
        self.runtimeLimit_s = self.settings.runtimeLimit_s
        self.baseContainer = emptyContainer
        self.errorMsg = ""
        self.log = log.get('Filler')

    # reinit algo state
    def initFiller(self):
        self.ap = self.startAP
        self.container = copy.copy(self.baseContainer)
        self.nSteps = 0

    def itemPoolCondition(self):
        return not self.container.isPoolEmpty()

    def createStepCountCondition(self, n):
        return lambda: self.nSteps < n

    # shall return (stuck, itemLoc dict list, progression itemLoc dict list)
    def generateItems(self, condition=None):
        self.initFiller()
        if condition is None:
            condition = self.itemPoolCondition
        runtime_s = 0
        isStuck = False
        startDate = time.process_time()
        maxDiff = self.settings.maxDiff
        while condition() and not isStuck and runtime_s <= self.runtimeLimit_s:
            isStuck = not self.step()
            if not isStuck:
                self.nSteps += 1
            runtime_s = time.process_time() - startDate
        if condition():
            isStuck = True
            if runtime_s > self.runtimeLimit_s:
                self.errorMsg = "Exceeded time limit of "+str(self.runtimeLimit_s) +" seconds"
            else:
                self.errorMsg = "STUCK !\n"+self.container.dump()
        else:
            # check if some locations are above max diff and add relevant message
            locs = self.container.getUsedLocs(lambda loc: loc['difficulty'].difficulty > maxDiff)
            aboveMaxDiffStr = '[ ' + ' ; '.join([loc['Name'] + ': ' + diffValue2txt(loc['difficulty'].difficulty) for loc in locs]) + ' ]'
            if aboveMaxDiffStr != '[  ]':
                self.errorMsg += "Maximum difficulty could not be applied everywhere. Affected locations: {}".format(aboveMaxDiffStr)
            isStuck = False
        print('')
        return (isStuck, self.container.itemLocations, self.getProgressionItemLocations())

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

    # one item/loc per step
    def step(self, onlyBossCheck=False):
        self.cache.reset()
        if not self.services.canEndGame(self.container):
            (itemLocDict, isProg) = self.services.getPossiblePlacements(self.ap, self.container, False)
        else:
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
        itemLoc = self.choice.chooseItemLoc(itemLocDict, isProg)
        if itemLoc is None:
            if onlyBossCheck == False and self.services.onlyBossesLeft(self.ap, self.container):
                self.settings.maxDiff = infinity
                return self.step(onlyBossCheck=True)
            return False
        self.ap = self.services.collect(self.ap, self.container, itemLoc)
        return True
