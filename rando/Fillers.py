
import log, copy, time
from RandoServices import RandoServices

class Filler(object):
    def __init__(self, graph, restrictions, emptyContainer):
        self.services = RandoServices(graph, restrictions)
        self.settings = restrictions.settings
        self.runtimeLimit_s = self.settings.runtimeLimit_s
        self.baseContainer = emptyContainer
        self.log = log.get('Filler')

    # reinit algo state
    def initFiller(self):
        self.container = copy.copy(self.baseContainer)

    # shall return (stuck, itemLoc dict list, progression itemLoc dict list)
    def generateItems(self):
        self.initFiller()
        runtime_s = 0
        isStuck = False
        startDate = time.process_time()
        while not self.container.isPoolEmpty() and not isStuck and runtime_s <= self.runtimeLimit_s:
            isStuck = not self.step()
            runtime_s = time.process_time() - startDate
        if not self.container.isPoolEmpty():
            isStuck = True
            if runtime_s > self.runtimeLimit_s:
                # TODO handle error messages
                pass
        return (isStuck, self.container.itemLocations, self.getProgressionItemLocations())

    def getProgressionItemLocations(self):
        return []

    # return True if ok, False if stuck
    def step(self):
        pass

# simple front fill algorithm with no rollback
class FrontFiller(Filler):
    def __init__(self, graph, restrictions, emptyContainer):
        super(BasicFiller, self).__init__(graph, restrictions, emptyContainer)

    def step(self):
        # TODO
        return False
