import random, logging, time
from collections import defaultdict

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
            self.log.debug("validateSeed: real solver validation failed")
            return False
        else:
            return True

    def GetReachableLocationsAssumed(self, locations, owneditems):
        # Find items within already filled locations
        newitems = self.ItemSearch(locations, owneditems)
        combined = owneditems[:]
        while len(newitems) > 0:
            self.log.debug("GetReachableLocationsAssumed new items: {}".format([item.Type for item in newitems]))
            combined += newitems
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
            return [loc for loc in locs if self.restrictions.canPlaceAtLocation(item, loc, self.container)]

    def allLocationsWithoutItem(self, locations, item, owneditems):
        self.log.debug("allLocationsWithoutItem {}".format(item.Type))
        owneditems = [it for it in owneditems if it != item]

        # check that we can access the locations without the item,
        return self.GetReachableLocationsAssumed(locations, owneditems)

    def getPossiblePlacementsWithoutItem(self, locations, items):
        distinctItems = {item.Type: item for item in items}
        itemLocDict = {item: self.allLocationsWithoutItem(locations, item, items) for itemType, item in distinctItems.items()}
        return itemLocDict

    def chooseItem(self, locations, owneditems):
        # for each item choose randomly between the ones with the most available locations
        itemLocDict = self.getPossiblePlacementsWithoutItem(locations, owneditems)

        maxLocs = -1
        maxItems = []
        for item, locs in itemLocDict.items():
            nbLocs = len(locs)
            if nbLocs > maxLocs:
                maxItems = [item]
                maxLocs = nbLocs
            elif nbLocs == maxLocs:
                maxItems.append(item)
        if maxItems:
            self.log.debug("chooseItem: maxItems: {} maxLocs: {} {}".format(maxLocs, len(maxItems), [item.Type for item in maxItems]))
            random.shuffle(maxItems)
            item = maxItems[0]
            owneditems.remove(item)
            return item
        else:
            self.log.debug("chooseItem maxItems is empty")
            return None

    def chooseLocation(self, locations):
        # for each reachable location check how many different items are required to access it,
        # choose location with the most prerequisites first
        maxItems = -1
        maxLocs = []
        for loc in locations:
            items = loc.difficulty.items
            nbItems = len(items)
            if nbItems > maxItems:
                maxLocs = [loc]
                maxItems = nbItems
            elif nbItems == maxItems:
                maxLocs.append(loc)
        if maxLocs:
            self.log.debug("chooseLocation: maxItems: {} maxLocs: {} {}".format(maxItems, len(maxLocs), [loc.Name for loc in maxLocs]))
            random.shuffle(maxLocs)
            return maxLocs[0]
        else:
            self.log.debug("chooseLocation maxLocs is empty")
            return None

    def step(self, onlyBossCheck=False):
        # start with all the items
        owneditems = self.container.itemPool[:]
        locations = self.container.unusedLocations[:]
        for loc in locations:
            loc.item = None
        reachable = self.GetReachableLocationsAssumed(locations, owneditems)
        reachablelocations = self.GetAllEmptyLocations(reachable)
        random.shuffle(owneditems)
        while len(owneditems) > 0:
            item = self.chooseItem(locations, owneditems)
            if item is None:
                self.log.debug("item is empty")
                # return true to try again
                self.container.resetCollected(reassignItemLocs=True)
                return True

            self.log.debug("item choosen: {}".format(item.Type))
            random.shuffle(owneditems)
            # Recalculate reachable locations now that less items are owned
            reachable = self.GetReachableLocationsAssumed(locations, owneditems)
            # Get empty locations which are reachable
            reachablelocations = self.GetAllEmptyLocations(reachable, item)
            self.log.debug("reachablelocations for item {}: {}".format(item.Type, len(reachablelocations)))
            location = self.chooseLocation(reachablelocations)
            if location is None:
                self.log.debug("reachablelocations is empty")
                # return true to try again
                self.container.resetCollected(reassignItemLocs=True)
                return True

            # Place random item in random location
            itemLoc = ItemLocation(item, location)
            self.log.debug("try to collect {} at {}".format(item.Type, location.Name))
            self.collect(itemLoc)
            location.item = item

        return self.validateSeed()
