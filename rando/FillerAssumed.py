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
                self.log.debug("  {}: {}".format(it.Type, [loc.Name for loc in locs] if len(locs) <= 5 else len(locs)))

    def computePriority(self, itemLocDict, step, maxDiff):
        # build a dependency graph of the items/locations to help priorize some locations and some items.
        for it, data in itemLocDict.items():
            data["newPossibleLocs"] = {}

        self.log.debug("begin graph construction")
        itemGraph = nx.DiGraph()

        if self.earlyGame:
            validItems = set([it for it in itemLocDict.keys()])
        else:
            # we only place items which won't make some locs unavailable
            validItems = set([it for it, data in itemLocDict.items() if not data['noLongerAvailLocsWoItem']])
        self.log.debug("validItems: {}".format([it.Type for it in validItems]))

        # add valid items to the graph
        for it in validItems:
            itemGraph.add_node(it)

        # for a node N and its parent P we add an edge to the graph if at least one possible location for item N
        # is in the locations which won't be available after placing item P (ie. we have to place N before P
        # to not have inaccessible locations)
        for P, dataP in itemLocDict.items():
            for N, dataN in itemLocDict.items():
                if dataN["possibleLocs"].intersection(dataP["noLongerAvailLocsWoItem"]):
                    itemGraph.add_edge(P, N)
                    #self.log.debug("add edge {} -> {}".format(P.Type, N.Type))

        #write_dot(itemGraph, "grid{}.dot".format(step))

        if self.earlyGame:
            leafs = validItems
        else:
            # keep only the leafs (ie. nodes without transitions starting from them)
            leafs = set([N for N in itemGraph.nodes() if itemGraph.out_degree(N) == 0 and N in validItems])
        self.log.debug("leafs: {}".format([it.Type for it in leafs]))

        extraPriority = 100 # have to be big, it's top priority to fill it else it will never be filled
        defaultPriority = 1

        # keep intersection of all possible locations which are in parent no longer avail locations
        priorityLocations = defaultdict(int)
        priorityLocationsItems = defaultdict(set)
        for N in leafs:
            for P in itemGraph.predecessors(N):
                #self.log.debug("handle P {} -> N {} priority".format(P.Type, N.Type))
                newPossibleLocs = itemLocDict[P]["noLongerAvailLocsWoItem"].intersection(itemLocDict[N]["possibleLocs"])
                # increase priority each time a location has to be filled to unlock an item
                for loc in newPossibleLocs:
                    #self.log.debug("increase N {} Loc {} priority".format(N.Type, loc.Name))
                    priorityLocations[loc] += defaultPriority
                    priorityLocationsItems[loc].add(N)
                itemLocDict[N]["newPossibleLocs"][P] = newPossibleLocs

        # if locs max priority > 1 remove locs from the item with the biggest noLongerAvailLocsWoItem
        # which are only no longer without this item (because of morph which has almost all locations no longer available)
        removeLowestPriority = False
        for priority in priorityLocations.values():
            if priority > 1:
                removeLowestPriority = True
                break

        if removeLowestPriority:
            # get item with biggest noLongerAvailLocsWoItem
            itemToRemove = None
            noLongerAvailLocsWoItemCount = -1
            for it, data in itemLocDict.items():
                if noLongerAvailLocsWoItemCount < len(data['noLongerAvailLocsWoItem']):
                    itemToRemove = it
                    noLongerAvailLocsWoItemCount = len(data['noLongerAvailLocsWoItem'])
            assert itemToRemove is not None
            self.log.debug("ignore noLongerAvailLocsWoItem for item {}".format(itemToRemove.Type))
            noLongerAvailLocsWoItem = itemLocDict[itemToRemove]['noLongerAvailLocsWoItem']
            for it1, data in itemLocDict.items():
                # don't update nodes with no parents (could be bosses)
                if len(data['newPossibleLocs']) > 0:
                    data['possibleLocs'] = set()
                    for it2, locs in data['newPossibleLocs'].items():
                        if it2 != itemToRemove:
                            data['possibleLocs'].update(locs)
                    # all the possible locs where from item to remove parent
                    if len(data['possibleLocs']) == 0:
                        data['possibleLocs'] = data['newPossibleLocs'][itemToRemove]

        self.log.debug("possible items: {}".format([it.Type for it in itemLocDict.keys() if it in leafs and it in validItems]))

        # check if a loc must be filled or else it'll be no longer available
        extraPriorityLocations = []
        for it, data in itemLocDict.items():
            if it not in validItems:
                continue
            for loc in data["locsPostNokWoItem"]+data["locsNokWoDoubleItem"]:
                self.log.debug("loc post nok wo OR double {}: {}".format(it.Type, loc.Name))
                self.log.debug("possible items for loc: {}".format([i.Type for i in priorityLocationsItems[loc]]))
                validItemsForLoc = leafs.intersection(priorityLocationsItems[loc])
                self.log.debug("valid items for loc: {}".format([i.Type for i in validItemsForLoc]))
                if validItemsForLoc:
                    priorityLocations[loc] += extraPriority
                    extraPriorityLocations.append(loc)
                    for it2, data2 in itemLocDict.items():
                        if loc in data2["possibleLocs"] and it2 in leafs:
                            priorityLocationsItems[loc].add(it2)
                    # if more than one loc has its postavailable nok without this item, remove item
                    if len(data['locsPostNokWoItem']) > 1 and it in priorityLocationsItems[loc]:
                        self.log.debug("more than one loc post nok wo {}, remove it for this loc items".format(it.Type))
                        priorityLocationsItems[loc].remove(it)

        # for each leaf item1, for each item2 with only one possible location,
        # check that item2 location is still available without item1 and item2.
        oneLocationItemsLocs = [(it, data['possibleLocs']) for it, data in itemLocDict.items() if len(data['possibleLocs']) == 1]
        removeFromLeafs = set()
        for leafItem in leafs:
            for oneLocItem, oneLoc in oneLocationItemsLocs:
                if leafItem == oneLocItem:
                    continue
                oneLoc = list(oneLoc)[0]
                if not self.services.locStillOkWoBothItems(leafItem, oneLocItem, self.startAP, self.ap, oneLoc, self.container, self.container.itemPool, maxDiff):
                    # if one loc item is in leaf, increase its location priority, else remove leaf item from leafs
                    self.log.debug("found loc unavailable wo both items, leaf: {} one loc item: {}, loc: {}".format(leafItem.Type, oneLocItem.Type, oneLoc.Name))
                    if oneLocItem in leafs:
                        self.log.debug("priorize loc: {}".format(oneLoc.Name))
                        priorityLocations[loc] += extraPriority
                    else:
                        self.log.debug("remove leaf item from leafs: {}".format(leafItem.Type))
                        removeFromLeafs.add(leafItem)
        if removeFromLeafs:
            leafs -= removeFromLeafs

        # for each leaf item1, for each item2 with only one possible location,
        # check if item2 only loc is in item1 possible locs, if so remove it
        for leafItem in leafs:
            for oneLocItem, oneLoc in oneLocationItemsLocs:
                if leafItem == oneLocItem:
                    continue
                self.log.debug("leaf: {} one: {} loc: {}".format(leafItem.Type, oneLocItem.Type, oneLoc))
                oneLoc = list(oneLoc)[0]
                if oneLoc in itemLocDict[leafItem]['possibleLocs']:
                    self.log.debug("remove loc {} from {} as it only loc for {}".format(oneLoc.Name, leafItem.Type, oneLocItem.Type))
                    priorityLocations[loc] += extraPriority
                    itemLocDict[leafItem]['possibleLocs'].remove(oneLoc)
                    if leafItem in priorityLocationsItems[loc]:
                        priorityLocationsItems[loc].remove(leafItem)

        return {it: data for it, data in itemLocDict.items() if it in leafs and it in validItems}, extraPriorityLocations, priorityLocations, priorityLocationsItems

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
        itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.ap, self.container, assumedItems, maxDiff)

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
            #assert len(allPossibleLocs) == len(self.container.unusedLocations)

        # keep only priority locations, locations that need to be filled to allow placement of an item
        # which will make other locations unreachable
        newItemLocDict, extraPriorityLocations, priorityLocations, priorityLocationsItems = self.computePriority(itemLocDict, step, maxDiff)
        possibleTypes = set([it.Type for it in newItemLocDict.keys()])

        if extraPriorityLocations:
            loc = random.choice(sorted(extraPriorityLocations))
            itemsChoice = sorted(list(priorityLocationsItems[loc]))

            item = random.choice(itemsChoice)
            self.log.debug("priority loc chosen: {}, difficulty: {} - available items: {}".format(loc.Name, loc.difficulty, len(itemsChoice)))
            self.log.debug("item chosen: {}".format(item.Type))

            itemLoc = ItemLocation(item, loc)
        else:
            possibleItems = sorted([it for it in assumedItems if it.Type in possibleTypes])
            self.log.debug("all possible items: {} {}".format(len(possibleItems), getItemListStr(possibleItems)))
            if not possibleItems:
                if self.earlyGame:
                    self.log.debug("even without constraints we're stucked")
                    return False
                else:
                    self.earlyGame = True
                    self.log.debug("no more possible items with all the constraints, remove them and retry")
                    return True

            # if an item is now available and wasn't before prioritize it (to avoid too many suits early)
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
                self.log.debug("choose in newAvailableItems: {}".format(self.newAvailableItems))
                itemType = random.choice(sorted(list(self.newAvailableItems)))
                self.newAvailableItems.remove(itemType)
                for it, data in newItemLocDict.items():
                    if it.Type == itemType:
                        item = it
                        locations = data['possibleLocs']
                        break
            else:
                item = random.choice(possibleItems)
                # not very pythonic
                for it, data in newItemLocDict.items():
                    if it.Type == item.Type:
                        locations = list(data['possibleLocs'])
                        break
            self.log.debug("item chosen: {} - available locs before prio: {}".format(item.Type, [(loc.Name, priorityLocations[loc]) for loc in locations] if len(locations) < 5 else len(locations)))
            maxPriority = -1
            for loc in locations:
                if priorityLocations[loc] > maxPriority:
                    maxPriority = priorityLocations[loc]
            locations = [loc for loc in locations if priorityLocations[loc] == maxPriority]
            self.log.debug("item chosen: {} - available locs after prio: {}".format(item.Type, [(loc.Name, priorityLocations[loc]) for loc in locations] if len(locations) < 5 else len(locations)))

            itemLoc = self.choice.chooseItemLoc({item: locations}, False)
            self.log.debug("loc chosen: {}".format(itemLoc.Location.Name))

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
