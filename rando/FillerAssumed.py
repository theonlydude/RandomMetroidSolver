import random, logging, time
from collections import defaultdict

from rando.Filler import Filler
from rando.FillerRandom import FillerRandomItems, FrontFillerKickstart, FrontFillerNoCopy
from utils.parameters import infinity
from rando.Choice import ItemThenLocChoice
from graph.graph_access import GraphUtils
from rando.RandoServices import ComebackCheckType
from rando.ItemLocContainer import ItemLocation, getItemListStr

class AssumedFiller(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate=infinity):
        super(AssumedFiller, self).__init__(startAP, graph, restrictions, container, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)

    def initFiller(self):
        super(AssumedFiller, self).initFiller()
        
        # first collect mother brain
        self.ap = 'Golden Four'
        for (boss, bossLocName) in [('MotherBrain', 'Mother Brain')]:
            bossItem = self.container.getItems(lambda it: it.Type == boss)
            bossLoc = self.container.getLocs(lambda loc: loc.Name == bossLocName)
            self.collect(ItemLocation(bossItem[0], bossLoc[0]))

        self.alreadyTriedItems = defaultdict(set)

        # TODO::choose morph loc first to forbid other items in it. TODO::handle early/late morph
        #firstItemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.container, assumedItems, alreadyPlacedItems)

    def step(self, onlyBossCheck=False):
        assumedItems = self.container.itemPool

        step = len(assumedItems)

        self.log.debug("remaining assumed items: {}: {}".format(self.nSteps, getItemListStr(assumedItems)))
        self.log.debug("start ap: {}".format(self.ap))

        # compute available locs without each item type
        itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.ap, self.container, assumedItems)
        # check if all items have no locs
        if len([item for item, locs in itemLocDict.items() if len(locs) > 0]) == 0:
            self.errorMsg = "Stuck, no item with possible loc"
            return False

        # debug display
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("before: {}".format([(it.Type, len(locs)) for (it, locs) in itemLocDict.items()]))
            for it, locs in itemLocDict.items():
                self.log.debug("{}: {}".format(it.Type, [loc.Name for loc in locs] if len(locs) < 5 else len(locs)))

        # keep only items with the max number of available locs and bosses
        maxLocsLen = -1
        for it, locs in itemLocDict.items():
            if len(locs) > maxLocsLen:
                maxLocsLen = len(locs)
        itemLocDict = {it: locs for it, locs in itemLocDict.items() if it.Category == 'Boss' or len(locs) == maxLocsLen}

        # debug display
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("after filter: {}".format([(it.Type, len(locs)) for (it, locs) in itemLocDict.items()]))
            for it, locs in itemLocDict.items():
                self.log.debug("{}: {}".format(it.Type, [loc.Name for loc in locs] if len(locs) < 5 else len(locs)))

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
        self.log.debug("loc chosen: {}".format(itemLoc.Location.Name))

        # check if a boss can't be placed after this items
        assumedItems.remove(item)
        # use chosen loc ap to check if an item can't be placed afterward
        ap = itemLoc.Location.accessPoint
        self.log.debug("middle ap: {}".format(ap))
        itemLocDictAfter = self.services.getPossiblePlacementsWithoutItem(ap, self.container, assumedItems)
        assumedItems.append(item)

        self.log.debug("after: {}".format([(it.Type, len(locs)) for (it, locs) in itemLocDictAfter.items()]))
        zeroLocsItemFound = False
        for it, locs in itemLocDictAfter.items():
            if it.Category == 'Boss' and len(locs) == 0:
                self.log.debug("step: {} - zeroLocsItemFound for {} after placing {} !!".format(self.nSteps, it.Type, item.Type))
                self.alreadyTriedItems[step].add(item)
                zeroLocsItemFound = True
                break

        if zeroLocsItemFound:
            return True

        self.collect(itemLoc)
        self.log.debug("end ap: {}".format(self.ap))

        return True
