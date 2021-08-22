import random, logging, time

from rando.Filler import Filler
from rando.Choice import ItemThenLocChoice
from rando.ItemLocContainer import ItemLocation
from solver.randoSolver import RandoSolver
from graph.graph_utils import getAccessPoint
from utils.parameters import infinity

class AssumedFiller(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate=infinity):
        super(AssumedFiller, self).__init__(startAP, graph, restrictions, container, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.startGraphArea = getAccessPoint(self.startAP).GraphArea

    def initFiller(self):
        super(AssumedFiller, self).initFiller()
        assert len(self.container.itemPool) == len(self.container.unusedLocations)

        if self.vcr is not None:
            # give all items to vcr, like we do in assumed fill
            self.vcr.setFiller('reverse')
            self.vcr.addInitialItems([it.Type for it in self.container.itemPool])

        # first collect mother brain
        for (boss, bossLocName) in [('MotherBrain', 'Mother Brain')]:
            bossItem = self.container.getItems(lambda it: it.Type == boss)
            bossLoc = self.container.getLocs(lambda loc: loc.Name == bossLocName)
            self.collect(ItemLocation(bossItem[0], bossLoc[0]))

        # don't use rando cache as we manually handle sm items
        self.services.cache = None

    def validateSeed(self):
        # do a full solver check
        graphLocations = self.container.getLocsForSolver()
        solver = RandoSolver(self.restrictions.split, self.startAP, self.graph, graphLocations)
        diff = solver.solveRom()
        self.container.cleanLocsAfterSolver()
        if diff == -1:
            self.log.debug("can100percentReverse: real solver validation failed")
            return False
        else:
            return True

    def GetReachableLocationsAssumed(self, locations, owneditems):
        # Find items within R
        newitems = self.ItemSearch(locations, owneditems)
        # Copy list
        combined = owneditems[:]
        while len(newitems) > 0:
            self.log.debug("GetReachableLocationsAssumed new items: {}".format([item.Type for item in newitems]))
            # Add items to currently used items
            combined += newitems
            # Find items within R
            newitems = self.ItemSearch(locations, combined)
        # Use that combined list to find final search result
        return self.GetReachableLocations(locations, combined)

    def ItemSearch(self, locations, items):
        reachable = self.GetReachableLocations(locations, items)
        return [loc.item for loc in reachable if loc.item is not None and loc.item not in items]

    def GetReachableLocations(self, locations, items):
        sm = self.container.sm
        sm.resetItems()
        sm.addItems([item.Type for item in items])
        return self.services.areaGraph.getAvailableLocations(locations, sm, self.maxDiff, self.startAP)

    def GetAllEmptyLocations(self, reachable, item=None):
        locs = [loc for loc in reachable if loc.item is None]
        if item is None:
            return locs
        else:
            # keep only locations where the selected item can be placed
            locs = [loc for loc in locs if self.restrictions.canPlaceAtLocation(item, loc, self.container)]
            if item.Type == 'Morph' and self.restrictions.isEarlyMorph():
                locs = [loc for loc in locs if loc.GraphArea == self.startGraphArea]
            return locs

    def step(self, onlyBossCheck=False):
        # In contrast to other two algos, I is initialized to all items and itempool is empty
        owneditems = self.container.itemPool[:]
        locations = self.container.unusedLocations[:]
        # Initially R should equal all locations in the game
        for loc in locations:
            loc.item = None
        reachable = self.GetReachableLocationsAssumed(locations, owneditems)
        reachablelocations = self.GetAllEmptyLocations(reachable)
        random.shuffle(owneditems)
        while len(owneditems) > 0:
            # Pop random item from I, R will shrink
            item = owneditems.pop()
            self.log.debug("item choosen: {}".format(item.Type))
            random.shuffle(owneditems)
            # Recalculate R now that less items are owned
            reachable = self.GetReachableLocationsAssumed(locations, owneditems)
            # Get empty locations which are reachable
            reachablelocations = self.GetAllEmptyLocations(reachable, item)
            self.log.debug("reachablelocations for item {}: {}".format(item.Type, len(reachablelocations)))
            random.shuffle(reachablelocations)
            try:
                # Remove location from list
                location = reachablelocations.pop();
            except:
                # If this happens, means there are no reachable locations left and must return,
                # usually indicates uncompletable permutation
                self.log.debug("reachablelocations is empty")
                # return true to try again
                self.container.resetCollected(reassignItemLocs=True)
                return True
            # Place random item in random location
            itemLoc = ItemLocation(item, location)
            self.log.debug("try to collect {} at {}".format(item.Type, location.Name))
            self.collect(itemLoc)
            location.item = item

        # World has been filled with items, return
        if len(reachablelocations) > 0 or len(owneditems) > 0:
            print("STUCK: reachablelocations: {} owneditems: {}".format(len(reachablelocations), len(owneditems)))
            return False
        return self.validateSeed()

