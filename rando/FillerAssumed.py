import random, logging, time
from collections import defaultdict

from rando.Filler import Filler
from rando.FillerRandom import FillerRandomItems, FrontFillerKickstart, FrontFillerNoCopy
from utils.parameters import infinity
from rando.Choice import ItemThenLocChoice
from graph.graph_access import GraphUtils
from rando.RandoServices import ComebackCheckType
from rando.ItemLocContainer import ItemLocation, getItemListStr, ContainerSoftBackup
from logic.smbool import SMBool
from logic.helpers import diffValue2txt
from rando.MiniSolver import MiniSolver
from solver.randoSolver import RandoSolver

class AssumedFiller(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate=infinity):
        super(AssumedFiller, self).__init__(startAP, graph, restrictions, container, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        self.miniSolver = MiniSolver(startAP, graph, restrictions)
        self.can100percent = False

    def initFiller(self):
        super(AssumedFiller, self).initFiller()
        
        assert len(self.container.itemPool) == len(self.container.unusedLocations)

        if self.vcr is not None:
            # give all items to vcr, like we do in assumed fill
            self.vcr.setFiller('reverse')
            self.vcr.addInitialItems([it.Type for it in self.container.itemPool])

        # first collect mother brain
        self.ap = 'Golden Four'
        for (boss, bossLocName) in [('MotherBrain', 'Mother Brain')]:
            bossItem = self.container.getItems(lambda it: it.Type == boss)
            bossLoc = self.container.getLocs(lambda loc: loc.Name == bossLocName)
            self.collect(ItemLocation(bossItem[0], bossLoc[0]))

        # check only boss left
        self.onlyBossLeftLocations = self.services.getOnlyBossLeftLocationReverse(self.startAP, self.container)
        if self.onlyBossLeftLocations:
            self.log.debug("only boss left locations: {}".format([loc.Name for loc in self.onlyBossLeftLocations]))
            self.errorMsg = "Maximum difficulty could not be applied everywhere. Affected locations: [ {} ]".format(' ; '.join(["{}: {}".format(loc.Name, diffValue2txt(loc.difficulty.difficulty)) for loc in self.onlyBossLeftLocations]))

        self.alreadyTriedItems = defaultdict(set)

        # get all aps accessible from start ap with no items
        self.firstAPs = [ap.Name for ap in self.graph.getAvailableAccessPoints(self.graph.accessPoints[self.startAP], self.container.sm, self.maxDiff)]

        self.log.debug("first APs: {}".format(self.firstAPs))
        # then all the locations linked to these first APs
        self.firstLocations = []
        for loc in self.container.unusedLocations:
            for ap in loc.AccessFrom.keys():
                if ap in self.firstAPs:
                    self.firstLocations.append(loc)
                    continue

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("first locations:")
            for loc in self.firstLocations:
                self.log.debug(loc.Name)

        # TODO::choose morph loc first to forbid other items in it. TODO::handle early/late morph
        #firstItemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.container, assumedItems, alreadyPlacedItems)

    def switchTwoItems(self, zeroItemLocDict, maxDiff):
        # we are stuck, all items have zero location available (zero_item).
        # we need to remove an already placed item.
        # so compute the locations available for each item using the already filled locations,
        # then test the filled locations accessible to get the most useless item,
        # remove it, then use minisolver to check that we can still reach all the other filled locations.
        # loop until mini solver is ok or we've tested all locations.

        # create a backup of the container
        containerBackup = ContainerSoftBackup(self.container)

        # set back all locations as unused, return a {loc: item}
        locsItem = self.container.restoreLocations()

        # compute available locations from start ap with all locations set as unused
        newItemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.ap, self.container, self.container.itemPool, maxDiff)

        # display new itemLoc dict
        self.displayItemLocDict("with all locs", newItemLocDict)

        if len(newItemLocDict) == 0:
            self.log.debug("No location available even after setting all locations as available")
            return False

        # get item with the less possible locations, it's the harder to place
        minLocsLen = infinity
        minItem = None
        for item, locs in newItemLocDict.items():
            if len(locs) < minLocsLen:
                minLocsLen = len(locs)
                minItem = item
        self.log.debug("switch: minItem: {}".format(minItem.Type))

        # get items in minItem locations
        oldItemsLocs = {locsItem[loc]: loc for loc in newItemLocDict[minItem] if loc in locsItem}
        oldItems = [it for it in oldItemsLocs.keys()]
        if self.log.getEffectiveLevel() == logging.DEBUG:
            for it, loc in oldItemsLocs.items():
                self.log.debug("minItem possible loc: {} with old item: {}".format(loc.Name, it.Type))

        # restore container
        containerBackup.restore(self.container)

        self.miniSolver.startAP = self.ap
        while True:
            containerBackup = ContainerSoftBackup(self.container)

            # get more disposable item
            if len(oldItems) > 1:
                uselessItem = oldItems[0]
                for it in oldItems[1:]:
                    uselessItem = self.getMoreUseless(uselessItem, it)
            elif len(oldItems) == 1:
                uselessItem = oldItems[0]
            else:
                self.log.debug("switch: no more available location that has already been used, really stucked")
                return False
            self.log.debug("switch: Useless item found: {}".format(uselessItem.Type))
            oldItems.remove(uselessItem)

            # get loc with the most useless item
            uselessLoc = oldItemsLocs[uselessItem]
            del oldItemsLocs[uselessItem]

            self.log.debug("switch: Useless associated location: {}".format(uselessLoc.Name))

            # uncollect uselessLoc: put back useless item in pool
            self.uncollect(uselessLoc)

            # collect minItem in uselessLoc
            self.log.debug("switch: collect {}@{}".format(minItem.Type, uselessLoc.Name))
            self.collect(ItemLocation(minItem, uselessLoc))

            # launch mini solver to check that all previously visited locations are still available
            startItems = [it.Type for it in self.container.itemPool]
            if self.miniSolver.isBeatable(self.container.itemLocations, self.maxDiff, startItems):
                self.log.debug("minisolver has validated the item switch")
                return True

            self.log.debug("minisolver nok, continue with next useless item")

            # restore container
            containerBackup.restore(self.container)

        return True

    def uncollect(self, loc):
        itemType = self.container.uncollect(loc)
        if self.vcr is not None:
            self.vcr.removeLocation(loc.Name, itemType)

    def getMoreUseless(self, item1, item2):
        # nothing < noenergy < missile < super < powerbomb < reserve < etank
        usefulness = {'Nothing': 0, 'NoEnergy': 1, 'Missile': 2, 'Super': 3, 'PowerBomb': 4, 'Reserve': 5, 'ETank': 6}

        if usefulness.get(item1.Type, infinity) < usefulness.get(item2.Type, infinity):
            return item1
        else:
            return item2

    def validateFill(self):
        self.log.debug("Final mini/real solver check to validate the fill")
        return self.can100percentReverse()

    def can100percentReverse(self):
        if self.can100percent:
            self.log.debug("can100percentReverse: already validated by real solver")
            return True
        # check that mini solver can beat the seed starting from start ap
        self.miniSolver.startAP = self.startAP
        if not self.miniSolver.isBeatable(self.container.itemLocations, self.maxDiff):
            return False
        self.log.debug("can100percentReverse: validated by mini solver")
        # do a full solver check
        graphLocations = self.container.getLocsForSolver()
        solver = RandoSolver(self.restrictions.split, self.startAP, self.graph, graphLocations)
        diff = solver.solveRom()
        self.container.cleanLocsAfterSolver()
        if diff == -1:
            self.log.debug("can100percentReverse: real solver validation failed")
            return False
        self.log.debug("can100percentReverse: validated by real solver")
        # don't do a real solver check each loop
        self.can100percent = True
        return True

    def displayItemLocDict(self, msg, itemLocDict):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("{}: {}".format(msg, [(it.Type, len(locs)) for (it, locs) in itemLocDict.items()]))
            for it, locs in itemLocDict.items():
                self.log.debug("{}: {}".format(it.Type, [loc.Name for loc in locs] if len(locs) < 5 else len(locs)))

    def step(self, onlyBossCheck=False):
        self.log.debug("------------------------------------------------")

        if self.can100percentReverse():
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
            itemLoc = ItemThenLocChoice.chooseItemLoc(self.choice, itemLocDict, False)
            assert itemLoc is not None
            self.log.debug("can100percent, fill with no logic")
            self.ap = self.services.collect(self.ap, self.container, itemLoc)
            return True

        assumedItems = self.container.itemPool

        step = len(assumedItems)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("remaining assumed items: {}".format(getItemListStr(assumedItems)))
            self.log.debug("remaining locations: {}".format(len(self.container.unusedLocations) if len(self.container.unusedLocations) > 5 else [loc.Name for loc in self.container.unusedLocations]))
            self.log.debug("start ap: {}".format(self.ap))

        if len(self.onlyBossLeftLocations) > 0:
            self.log.debug("onlyBossLeftLocations not empty: {}, set maxDiff to infinity".format([loc.Name for loc in self.onlyBossLeftLocations]))
            maxDiff = infinity
        else:
            self.log.debug("onlyBossLeftLocations empty, set maxDiff to {}".format(self.services.settings.maxDiff))
            maxDiff = self.maxDiff

        # compute available locs without each item type, check that we can come back to start ap
        itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.ap, self.container, assumedItems, maxDiff)
        # check if all items have no locs
        if len([item for item, locs in itemLocDict.items() if len(locs) > 0]) == 0:
            self.log.debug("all items have no locs, switch item")
            return self.switchTwoItems(itemLocDict, maxDiff)

        # debug display
        self.displayItemLocDict("before", itemLocDict)

        # TODO::check that it's correct
        # remove fist locations if too many remaining items
        if len(set([it.Type for it in assumedItems])) > len(self.firstLocations):
            for item, locs in itemLocDict.items():
                for loc in self.firstLocations:
                    if loc in locs:
                        locs.remove(loc)

        # TODO::check if we can do without that, or do better
        # keep only items with the max number of available locs and bosses
        maxLocsLen = -1
        for it, locs in itemLocDict.items():
            if len(locs) > maxLocsLen:
                maxLocsLen = len(locs)
        itemLocDict = {it: locs for it, locs in itemLocDict.items() if it.Category == 'Boss' or len(locs) == maxLocsLen}

        # debug display
        self.displayItemLocDict("after filter", itemLocDict)

        if len(self.alreadyTriedItems[step]) > 0:
            self.log.debug("self.alreadyTriedItems: {} / {}".format(len(self.alreadyTriedItems[step]), step))
            try:
                item = random.choice([it for it in itemLocDict.keys() if it not in self.alreadyTriedItems[step]])
            except IndexError:
                self.errorMsg = "Stucked after testing all items"
                return False
        else:
            item = random.choice(list(itemLocDict.keys()))
        locations = itemLocDict[item]
        self.log.debug("item chosen: {} - available locs: {}".format(item.Type, len(locations)))

        itemLoc = self.choice.chooseItemLoc({item: locations}, False)
        if itemLoc is None:
            self.log.debug("No remaining location for item {}".format(item.Type))
            self.alreadyTriedItems[step].add(item)
            return True
        self.log.debug("loc chosen: {}, difficulty: {}".format(itemLoc.Location.Name, itemLoc.Location.difficulty))

        # check if a boss can't be placed after this items
        assumedItems.remove(item)
        # use chosen loc ap to check if an item can't be placed afterward
        ap = itemLoc.Location.accessPoint
        self.log.debug("middle ap: {}".format(ap))
        itemLocDictAfter = self.services.getPossiblePlacementsWithoutItem(self.startAP, ap, self.container, assumedItems, maxDiff)
        assumedItems.append(item)

        # TODO::do we have to generalize that to every items and not only boss items ?
        self.displayItemLocDict("compute remaining without {}".format(item.Type), itemLocDictAfter)
        zeroLocsItemFound = False
        for it, locs in itemLocDictAfter.items():
            if it.Category == 'Boss' and len(locs) == 0:
                self.log.debug("step: {} - zeroLocsItemFound for {} after placing {} !!".format(self.nSteps, it.Type, item.Type))
                # if it's because of max diff, put back boss location in only boss left locations
                if maxDiff < infinity:
                    bossLoc = self.container.getLocs(lambda loc: loc.Name == it.Type)[0]
                    self.onlyBossLeftLocations.append(bossLoc)
                    self.errorMsg += " and {}".format(bossLoc.Name)
                    return True

                self.alreadyTriedItems[step].add(item)
                zeroLocsItemFound = True
                break

        if zeroLocsItemFound:
            return True

        self.collect(itemLoc)

        if itemLoc.Location in self.onlyBossLeftLocations:
            self.log.debug("Remove loc from onlyBossLeft locations")
            self.onlyBossLeftLocations.remove(itemLoc.Location)

        self.log.debug("end ap: {}".format(self.ap))

        return True
