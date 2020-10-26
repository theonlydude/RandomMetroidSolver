try:
    import networkx as nx
    from networkx.drawing.nx_agraph import write_dot
except:
    print("missing networkx package, install it: pip3.7 install networkx --user")
    import sys
    sys.exit(1)

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
        # be more generous with only boss left steps in minisolver
        self.miniSolver = MiniSolver(startAP, graph, restrictions, 10)
        self.can100percent = False
        self.earlyGame = False

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
            self.log.debug("{}: {}".format(msg, [(it.Type, data['availLocsWoItemLen'], len(data['possibleLocs'])) for (it, data) in itemLocDict.items()]))
            for it, data in itemLocDict.items():
                locs = data['possibleLocs']
                self.log.debug("  {}: {}".format(it.Type, [loc.Name for loc in locs] if len(locs) < 5 else len(locs)))

    def computePriority(self, itemLocDict, step):
        # build a dependency graph of the items/locations to help priorize some locations and some items.
        for it, data in itemLocDict.items():
            data["newPossibleLocs"] = set()

        # keep only items where we still have step available locs after placing the item
        if step > 0:
            validItems = set([it for it, data in itemLocDict.items() if data['availLocsWoItemLen'] == step])
            self.log.debug("validItems: {}".format([it.Type for it in validItems]))
        else:
            validItems = set([it for it in itemLocDict.keys()])

        # for a node N and its parent P we add an edge to the graph if at least one possible location for item N
        # is in the locations which won't be available after placing item P (ie. we have to place N before P
        # to not have inaccessible locations)
        self.log.debug("begin graph construction")
        itemGraph = nx.DiGraph()
        for P, dataP in itemLocDict.items():
            for N, dataN in itemLocDict.items():
                if dataN["possibleLocs"].intersection(dataP["noLongerAvailLocsWoItem"]):
                    itemGraph.add_edge(P, N)
                    self.log.debug("add edge {} -> {}".format(P.Type, N.Type))

        write_dot(itemGraph, "grid{}.dot".format(step))

        # keep only the leafs (ie. nodes without transitions starting from them)
        leafs = [N for N in itemGraph.nodes() if itemGraph.out_degree(N) == 0]
        self.log.debug("leafs: {}".format([it.Type for it in leafs]))

        postNokPriority = 100 # have to be big, it's top priority to fill it else it will never be filled
        defaultPriority = 1

        # keep intersection of all possible locations which are in parent no longer avail locations
        priorityLocations = defaultdict(int)
        priorityLocationsItems = defaultdict(set)
        for P, N in itemGraph.edges():
            if N not in leafs or N not in validItems:
                self.log.debug("N {} not in leafs or not in validItems".format(N.Type))
                continue
            self.log.debug("handle N {} priority".format(N.Type))
            newPossibleLocs = itemLocDict[P]["noLongerAvailLocsWoItem"].intersection(itemLocDict[N]["possibleLocs"])
            # increase priority each time a location has to be filled to unlock an item
            for loc in newPossibleLocs:
                self.log.debug("increase N {} Loc {} priority".format(N.Type, loc.Name))
                priorityLocations[loc] += defaultPriority
                priorityLocationsItems[loc].add(N)
            itemLocDict[N]["newPossibleLocs"].update(newPossibleLocs)
        for it, data in itemLocDict.items():
            if it not in leafs or N not in validItems:
                continue
            data["possibleLocs"] = data["newPossibleLocs"]

        for it, data in itemLocDict.items():
            for loc in data["locsPostNokWoItem"]:
                self.log.debug("loc post nok wo {}: {}".format(it.Type, loc.Name))
                priorityLocations[loc] += postNokPriority
                for it2, data in itemLocDict.items():
                    if loc in data["possibleLocs"]:
                        priorityLocationsItems[loc].add(it2)

        return priorityLocations, priorityLocationsItems

    def step(self, onlyBossCheck=False):
        self.log.debug("------------------------------------------------")
        self.log.debug("is earlyGame: {}".format(self.earlyGame))

        if self.can100percentReverse():
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
            itemLoc = ItemThenLocChoice.chooseItemLoc(self.choice, itemLocDict, False)
            assert itemLoc is not None
            self.log.debug("can100percent, fill with no logic")
            self.ap = self.services.collect(self.ap, self.container, itemLoc)
            return True

        # check only boss left
        self.onlyBossLeftLocations = self.services.getOnlyBossLeftLocationReverse(self.startAP, self.container)

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
        itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.ap, self.container, assumedItems, maxDiff)

        # debug display
        self.displayItemLocDict("before", itemLocDict)

        # don't filter items based on availLocsWoItemLen
        if self.earlyGame:
            step = -1

        # keep only priority locations, locations that need to be filled to allow placement of an item
        # which will make other locations unreachable
        priorityLocations, priorityLocationsItems = self.computePriority(itemLocDict, step)

        if not priorityLocations:
            self.log.debug("no priority locations")
            # no more constraints between items.
            # choose between items with the highest number of available locs after.
            maxAvailLocs = -1
            for it, data in itemLocDict.items():
                if data["availLocsWoItemLen"] > maxAvailLocs:
                    maxAvailLocs = data["availLocsWoItemLen"]
            items = [it for it, data in itemLocDict.items() if data["availLocsWoItemLen"] == maxAvailLocs]

            item = random.choice(items)
            locations = list(itemLocDict[item]['possibleLocs'])
            self.log.debug("item chosen: {} - available locs: {}".format(item.Type, len(locations)))

            itemLoc = self.choice.chooseItemLoc({item: locations}, False)
            if itemLoc is None:
                self.log.debug("No remaining location for item {}".format(item.Type))
                self.alreadyTriedItems[step].add(item)
                return True
            self.log.debug("loc chosen: {}, difficulty: {}".format(itemLoc.Location.Name, itemLoc.Location.difficulty))
        else:
            self.log.debug("priority locations")
#        if not itemLocDict:
#            if not self.earlyGame:
#                self.log.debug("no longer enforce that enough locs are available")
#                self.earlyGame = True
#                return True
#            else:
#                self.errorMsg = "No item with {} available locs after".format(step)
#                self.log.debug(self.errorMsg)
#                return False

            # first choose the location, then the item, the more priority on a loc the higher chance to choose it
            locsChoice = [loc for loc, count in priorityLocations.items() for i in range(count)]

            loc = random.choice(locsChoice)

            # choose item
            itemsChoice = list(priorityLocationsItems[loc])

            item = random.choice(itemsChoice)
            self.log.debug("loc chosen: {}, difficulty: {} - available items: {}".format(loc.Name, loc.difficulty, len(itemsChoice)))
            self.log.debug("item chosen: {}".format(item.Type))

            itemLoc = ItemLocation(item, loc)

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
