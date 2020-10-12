import random, logging
from collections import defaultdict

from rando.Filler import Filler
from rando.FillerRandom import FillerRandomItems, FrontFillerKickstart
from utils.parameters import infinity
from rando.Choice import ItemThenLocChoice
from graph.graph_access import GraphUtils
from rando.RandoServices import ComebackCheckType
from rando.ItemLocContainer import ItemLocation, getItemListStr
from utils.parameters import infinity

class ReverseFiller(Filler):
    def __init__(self, graphSettings, graph, restrictions, emptyContainer, endDate=infinity):
        super(ReverseFiller, self).__init__(graphSettings.startAP, graph, restrictions, emptyContainer, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        self.errorMsg = ""

    def generateItems(self, condition=None, vcr=None):
        self.vcr = vcr
        self.initFiller()

        # first between 2 and 3 steps of frontfill
        self.log.debug("initial front fill start")
        frontFiller = FrontFillerKickstart(self.startAP, self.graph, self.restrictions, self.container)
        # fill until 1/3 of locations are available (like total)
        condition = lambda: len(frontFiller.services.currentLocations(self.ap, self.container))+len(frontFiller.container.itemLocations) < len(frontFiller.container.unusedLocations)/3
        (stuck, itemLocations, progItems) = frontFiller.generateItems(condition)
        if stuck:
            self.errorMsg = "Stuck during initial front fill: {}".format(frontFiller.errorMsg)
            if self.vcr != None:
                self.vcr.dump(reverse=True)
            return (stuck, self.container.itemLocations, self.getProgressionItemLocations())

        self.log.debug("available locs after initial frontfill: {}".format(len(self.services.currentLocations(self.startAP, self.container))))

        # assumed fill for important items
        self.log.debug("assumed fill start")
        assumedFiller = AssumedFiller(self.startAP, self.graph, self.restrictions, self.container, self.endDate)
        (stuck, itemLocs, prog) = assumedFiller.generateItems(vcr=self.vcr)
        if stuck:
            self.errorMsg = "Stuck during assumed fill: {}".format(assumedFiller.errorMsg)
            if self.vcr != None:
                self.vcr.dump(reverse=True)
            return (stuck, self.container.itemLocations, self.getProgressionItemLocations())

        # random fill no logic for remaining minors
        self.log.debug("final random fill start")
        randomFiller = FillerRandomItems(self.startAP, self.graph, self.restrictions, self.container, self.endDate)
        (stuck, itemLocs, prog) = randomFiller.generateItems(vcr=self.vcr)
        if stuck:
            self.errorMsg = "Stuck during final random fill: {}".format(randomFiller.errorMsg)

        if self.vcr != None:
            self.vcr.dump(reverse=True)
        return (stuck, self.container.itemLocations, self.getProgressionItemLocations())

class AssumedFiller(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate=infinity):
        super(AssumedFiller, self).__init__(startAP, graph, restrictions, container, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        self.errorMsg = ""

    def generateItems(self, condition=None, vcr=None):
        self.vcr = vcr
        self.initFiller()

        alreadyPlacedItems = [il.Item for il in self.container.itemLocations]
        self.log.debug("alreadyPlacedItems: {}".format(getItemListStr(alreadyPlacedItems)))
        allItems = self.container.itemPool

        # first collect mother brain and G4
        for (boss, bossLocName) in [('MotherBrain', 'Mother Brain'), ('Kraid', 'Kraid'), ('Phantoon', 'Phantoon'), ('Draygon', 'Draygon'), ('Ridley', 'Ridley')]:
            bossItem = self.container.getItems(lambda it: it.Type == boss)
            bossLoc = self.container.getLocs(lambda loc: loc.Name == bossLocName)
            if len(bossItem) > 0 and len(bossLoc) > 0:
                self.collect(ItemLocation(bossItem[0], bossLoc[0]))

        # keep only important items in assumed fill
        assumedItems = []
        requiredCount = {'Missile': 2, 'Super': 1, 'PowerBomb': 2, 'ETank': 4}
        currentCount = {'Missile': 0, 'Super': 0, 'PowerBomb': 0, 'ETank': 0}
        for item in allItems:
            if item.Type in currentCount and currentCount[item.Type] < requiredCount[item.Type]:
                assumedItems.append(item)
                currentCount[item.Type] += 1
            elif item.Type in ['Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack', 'Kraid', 'Phantoon', 'Draygon', 'Ridley']:
                assumedItems.append(item)

        # TODO::choose morph loc first to forbid other items in it. TODO::handle early/late morph
        firstItemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.container, assumedItems, alreadyPlacedItems)

        # if some items can't be placed during assumed phase, put them in the 2nd phase
        self.randomFillWithLogic = False
        for item, locs in firstItemLocDict.items():
            if len(locs) == 0:
                assumedItems.remove(item)
                self.randomFillWithLogic = True
                self.log.debug("Move item {} to 2nd phase".format(item.Type))
                self.errorMsg = "Moving item to random fill phase is not implemented yet"
                return (True, self.container.itemLocations, self.getProgressionItemLocations())

        if self.log.getEffectiveLevel() == logging.DEBUG:
            for item in firstItemLocDict.keys():
                self.log.debug("first {} locs: {}".format(item.Type, len(firstItemLocDict[item])))

        # set start ap to mother brain as we're going in reverse from the end
        self.ap = 'Golden Four'

        while len(assumedItems) > 0:
            step = len(assumedItems)
            self.log.debug("remaining assumed items: {}: {}".format(step, getItemListStr(assumedItems)))

            # compute available locs without each item type
            itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.ap, self.container, assumedItems, alreadyPlacedItems)
            # check if all items have no locs
            if len([item for item, locs in itemLocDict.items() if len(locs) > 0]) == 0:
                self.errorMsg = "Stuck, no item with possible loc"
                if self.vcr != None:
                    self.vcr.dump(reverse=True)
                return (True, self.container.itemLocations, self.getProgressionItemLocations())

            self.log.debug("before: {}".format([(it.Type, len(locs)) for (it, locs) in itemLocDict.items()]))

            item = random.choice(list(itemLocDict.keys()))
            locations = itemLocDict[item]
            self.log.debug("item choosen: {} - available locs: {}".format(item.Type, len(locations)))

            itemLoc = self.choice.chooseItemLoc({item: locations}, False)
            if itemLoc is None:
                self.log.debug("No remaining location for item {}".format(item.Type))
                continue
            self.log.debug("loc choosen: {}".format(itemLoc.Location.Name))

            self.collect(itemLoc)
            assumedItems.remove(item)

        if self.vcr != None:
            self.vcr.dump(reverse=True)
        return (False, self.container.itemLocations, self.getProgressionItemLocations())
