import random, logging, time

from rando.Filler import Filler
from rando.FillerRandom import FillerRandomItems, FrontFillerKickstart, FrontFillerNoCopy
from rando.Choice import ItemThenLocChoice
from rando.RandoServices import ComebackCheckType
from rando.ItemLocContainer import ItemLocation, getItemListStr, ContainerSoftBackup
from rando.MiniSolver import MiniSolver
from rando.AssumedGraph import AssumedGraph
from utils.parameters import infinity
from graph.graph_access import GraphUtils
from logic.smbool import SMBool
from logic.helpers import diffValue2txt
from solver.randoSolver import RandoSolver

class AssumedFiller(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate=infinity):
        super(AssumedFiller, self).__init__(startAP, graph, restrictions, container, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        # be more generous with only boss left steps in minisolver
        self.miniSolver = MiniSolver(startAP, graph, restrictions, 10)
        self.can100percent = False
        self.earlyGame = False
        self.previousAvailableItemsTypes = set()
        self.newAvailableItems = set()

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

    def isMajor(self, obj):
        return (self.settings.restrictions['MajorMinor'] == 'Full'
                or self.settings.restrictions['MajorMinor'] in obj.Class)

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
            self.log.debug("{}: (it, stillAvail, possLocs) {}".format(msg, [(it.Type, data['availLocsWoItemLen'], len(data['possibleLocs'])) for (it, data) in itemLocDict.items()]))
            for it, data in itemLocDict.items():
                locs = data['possibleLocs']
                self.log.debug("  {} ({}): {}".format(it.Type, data['availLocsWoItemLen'], [loc.Name for loc in locs] if len(locs) <= 5 else len(locs)))

    def computePriority(self, itemLocDict):
        # build a dependency graph of the items/locations to help priorize some locations and some items.
        if self.earlyGame:
            validItems = set([it for it in itemLocDict.keys()])
        else:
            # we only place items which won't make some locs unavailable
            validItems = set([it for it, data in itemLocDict.items() if not data['noLongerAvailLocsWoItem']])
        self.log.debug("validItems: {}".format([it.Type for it in validItems]))

        graph = AssumedGraph(validItems)
        graph.build(itemLocDict, self.container)
        return graph.getLocationsItems()

    def displayNoLongerAvailLocsWoItem(self, itemLocDict):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("noLongerAvailLocsWoItem:")
            for it, data in itemLocDict.items():
                self.log.debug("{}: {}".format(it.Type, len(data['noLongerAvailLocsWoItem'])))

    def displayIfItemsHaveReduceNoLongerAvailLocsWoItem(self, loc, itemLocDict):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("reduced?:")
            found = False
            for it, data in itemLocDict.items():
                if loc in data['noLongerAvailLocsWoItem']:
                    found = True
                    self.log.debug("{} noLongerAvailLocsWoItem has been reduced by one".format(it.Type))
            if not found:
                self.log.debug("No item has noLongerAvailLocsWoItem reduced")

    def step(self, onlyBossCheck=False):
        self.log.debug("------------------------------------------------")
        self.log.debug("is earlyGame: {}".format(self.earlyGame))

        if self.can100percentReverse():
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
            itemLoc = ItemThenLocChoice.chooseItemLoc(self.choice, itemLocDict, False)
            assert itemLoc is not None
            self.log.debug("can100percent, fill with no logic: {}".format(itemLoc))
            self.ap = self.services.collect(self.ap, self.container, itemLoc)
            return True

        # check only boss left
        self.onlyBossLeftLocations = self.services.getOnlyBossLeftLocationReverse(self.startAP, self.container, self.earlyGame)

        assumedItems = self.container.itemPool
        step = len(assumedItems)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("remaining assumed items: {} - {}".format(step, getItemListStr(assumedItems)))
            self.log.debug("remaining locations: {}".format(len(self.container.unusedLocations) if len(self.container.unusedLocations) > 13 else [loc.Name for loc in self.container.unusedLocations]))
            self.log.debug("start ap: {}".format(self.ap))

        if len(self.onlyBossLeftLocations) > 0:
            self.log.debug("onlyBossLeftLocations not empty: {}, set maxDiff to infinity".format([loc.Name for loc in self.onlyBossLeftLocations]))
            maxDiff = infinity
        else:
            self.log.debug("onlyBossLeftLocations empty, set maxDiff to {}".format(self.services.settings.maxDiff))
            maxDiff = self.maxDiff

        # compute available locs without each item type from start ap
        itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.ap, self.container, assumedItems, maxDiff, self.earlyGame)

        # debug display
        self.displayItemLocDict("before", itemLocDict)

        if not self.earlyGame:
            # check that the union of all possible locs == unused locs
            allPossibleLocs = set()
            for it, data in itemLocDict.items():
                allPossibleLocs.update(data['possibleLocs'])
            self.log.debug("allPossibleLocs: {} unusedLocations: {}".format(len(allPossibleLocs), len(self.container.unusedLocations)))
            if len(allPossibleLocs) != len(self.container.unusedLocations):
                self.log.debug("lost locations: {}".format([loc.Name for loc in set(self.container.unusedLocations)-allPossibleLocs]))
                return False

        # keep only priority locations, locations that need to be filled to allow placement of an item
        # which will make other locations unreachable
        locItemDict = self.computePriority(itemLocDict)

        if not locItemDict:
            if self.earlyGame:
                self.log.debug("even without constraints we're stucked")
                return False
            else:
                self.earlyGame = True
                self.log.debug("no more possible locs/items with all the constraints, remove them and retry")
                return True

        # choose loc
        loc = random.choice(sorted(list(locItemDict.keys())))
        self.log.debug("loc chosen: {}".format(loc.Name))

        possibleTypes = set([item.Type for item in locItemDict[loc]])
        possibleItems = sorted([it for it in assumedItems if it.Type in possibleTypes])

        # if an item is now available and wasn't before prioritize it (to avoid too many suits early in game)
        if not self.previousAvailableItemsTypes:
            self.previousAvailableItemsTypes = possibleTypes
        self.log.debug("possibleTypes: {}".format(possibleTypes))
        self.log.debug("previousAvailableItemsTypes: {}".format(self.previousAvailableItemsTypes))
        self.log.debug("old newAvailableItems: {}".format(self.newAvailableItems))
        self.newAvailableItems.update(possibleTypes - self.previousAvailableItemsTypes)
        self.log.debug("new newAvailableItems: {}".format(self.newAvailableItems))
        # some items in newAvailableItems could no longer be in possibleItems
        # (if space jump was in it before speedbooster is placed, and once you place speedbooster
        #  some locs which were available with speedbooster require space jump)
        self.newAvailableItems = self.newAvailableItems.intersection(set(possibleItems))
        if self.newAvailableItems and random.random() > 0.5:
            self.log.debug("choose in newAvailableItems: {}".format([it.Type for it in self.newAvailableItems]))
            itemType = random.choice(sorted(list(self.newAvailableItems)))
            for item in assumedItems:
                if item.Type == itemType:
                    break
            self.newAvailableItems.remove(itemType)
            self.log.debug("item type chosen: {}".format(item.Type))
        else:
            item = random.choice(possibleItems)
            self.log.debug("item type chosen: {}".format(item.Type))

        itemLoc = ItemLocation(item, loc)

        self.previousAvailableItemsTypes = possibleTypes

        self.displayNoLongerAvailLocsWoItem(itemLocDict)
        self.displayIfItemsHaveReduceNoLongerAvailLocsWoItem(itemLoc.Location, itemLocDict)

        self.collect(itemLoc)

        loc = itemLoc.Location
        if loc in self.onlyBossLeftLocations:
            self.log.debug("Remove loc from onlyBossLeft locations")
            if len(self.errorMsg) == 0:
                self.errorMsg = "Maximum difficulty could not be applied everywhere. Affected locations: "
            self.errorMsg += " {}: {}".format(loc.Name, diffValue2txt(self.onlyBossLeftLocations[loc]))
            del self.onlyBossLeftLocations[loc]

        self.log.debug("end ap: {}".format(self.ap))

        return True
