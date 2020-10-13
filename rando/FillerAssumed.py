import random, logging, time

from rando.Filler import Filler
from rando.FillerRandom import FillerRandomItems, FrontFillerKickstart, FrontFillerNoCopy
from utils.parameters import infinity
from rando.Choice import ItemThenLocChoice
from graph.graph_access import GraphUtils
from rando.RandoServices import ComebackCheckType
from rando.ItemLocContainer import ItemLocation, getItemListStr

class ReverseFiller(Filler):
    def __init__(self, graphSettings, graph, restrictions, emptyContainer, endDate=infinity):
        super(ReverseFiller, self).__init__(graphSettings.startAP, graph, restrictions, emptyContainer, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        self.errorMsg = ""

    def generateItems(self, condition=None, vcr=None):
        self.vcr = vcr
        self.initFiller()

        # front fill until 1/3 of locations are available (like total)
        self.log.debug("initial front fill start")
        frontFiller = FrontFillerKickstart(self.startAP, self.graph, self.restrictions, self.container)
        condition = lambda: len(frontFiller.services.currentLocations(self.ap, self.container))+len(frontFiller.container.itemLocations) < len(frontFiller.container.unusedLocations)/3
        (stuck, itemLocations, progItems) = frontFiller.generateItems(condition, vcr=self.vcr)
        self.container = frontFiller.container
        if stuck:
            self.errorMsg = "Stuck during initial front fill: {}".format(frontFiller.errorMsg)
            return (stuck, self.container.itemLocations, self.getProgressionItemLocations())

        self.log.debug("available locs after initial frontfill: {}".format(len(self.services.currentLocations(self.startAP, self.container))))

        # assumed fill for important items
        if self.vcr is not None:
            self.vcr.beginAssumed()
        self.log.debug("assumed fill start")
        assumedFiller = AssumedFiller(self.startAP, self.graph, self.restrictions, self.container, self.endDate)
        (stuck, itemLocs, prog) = assumedFiller.generateItems(vcr=self.vcr)
        if self.vcr is not None:
            self.vcr.endAssumed()
        self.container = assumedFiller.container
        if stuck:
            self.errorMsg = "Stuck during assumed fill: {}".format(assumedFiller.errorMsg)
            return (stuck, self.container.itemLocations, self.getProgressionItemLocations())

        if assumedFiller.randomFillWithLogic:
            # random fill logic for remaining minors & major items we couldn't place during previous filler
            self.log.debug("final random fill logic start")
            frontFiller = FrontFillerNoCopy(self.startAP, self.graph, self.restrictions, self.container, self.endDate)
            (stuck, itemLocations, progItems) = frontFiller.generateItems(vcr=self.vcr)
            self.container = frontFiller.container
            if stuck:
                self.errorMsg = "Stuck during final random fill logic: {}".format(frontFiller.errorMsg)
        else:
            # random fill no logic for remaining minors
            self.log.debug("final random fill nologic start")
            randomFiller = FillerRandomItems(self.startAP, self.graph, self.restrictions, self.container, self.endDate)
            (stuck, itemLocs, prog) = randomFiller.generateItems(vcr=self.vcr)
            self.container = randomFiller.container
            if stuck:
                self.errorMsg = "Stuck during final random fill nologic: {}".format(randomFiller.errorMsg)

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

        alreadyPlacedItems = [il.Item for il in self.container.itemLocations if not il.Location.restricted]
        self.log.debug("alreadyPlacedItems: {}".format(getItemListStr(alreadyPlacedItems)))

        # store available aps, use them at the end to be able to connect frontfill end to assumed begining
        sm = self.container.sm
        sm.addItems([it.Type for it in alreadyPlacedItems])
        initialAPs = self.services.areaGraph.getAvailableAccessPoints(self.services.areaGraph.accessPoints[self.startAP], sm, self.services.settings.maxDiff)
        initialAPs = set([ap.Name for ap in initialAPs.keys()])
        sm.resetItems()
        self.log.debug("initial APs: {}".format(initialAPs))

        allItems = self.container.itemPool

        # first collect mother brain
        for (boss, bossLocName) in [('MotherBrain', 'Mother Brain')]:
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

        if self.log.getEffectiveLevel() == logging.DEBUG:
            for item in firstItemLocDict.keys():
                self.log.debug("first {} locs: {}".format(item.Type, len(firstItemLocDict[item])))

        # set start ap to mother brain as we're going in reverse from the end
        self.ap = 'Golden Four'

        self.nSteps = 1
        while len(assumedItems) > 0:
            self.nSteps += 1
            self.log.debug("remaining assumed items: {}: {}".format(self.nSteps, getItemListStr(assumedItems)))

            # compute available locs without each item type
            itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.ap, self.container, assumedItems, alreadyPlacedItems)
            # check if all items have no locs
            if len([item for item, locs in itemLocDict.items() if len(locs) > 0]) == 0:
                self.errorMsg = "Stuck, no item with possible loc"
                return (True, self.container.itemLocations, self.getProgressionItemLocations())

            self.log.debug("before: {}".format([(it.Type, len(locs)) for (it, locs) in itemLocDict.items()]))
            for it, locs in itemLocDict.items():
                self.log.debug("{}: {}".format(it.Type, [loc.Name for loc in locs] if len(locs) < 5 else len(locs)))

            item = random.choice(list(itemLocDict.keys()))
            locations = itemLocDict[item]
            self.log.debug("item choosen: {} - available locs: {}".format(item.Type, len(locations)))

            # keep only locations available from initial APs
            if len(assumedItems) == 1:
                locations = [loc for loc in locations if loc.accessPoint in initialAPs]
                self.log.debug("last item - filtered available locs: {}".format(len(locations)))
                if not locations:
                    self.errorMsg = "Stuck, can't join front filler end to assumed filler end"
                    return (True, self.container.itemLocations, self.getProgressionItemLocations())

            itemLoc = self.choice.chooseItemLoc({item: locations}, False)
            if itemLoc is None:
                self.log.debug("No remaining location for item {}".format(item.Type))
                continue
            self.log.debug("loc choosen: {}".format(itemLoc.Location.Name))

            # check if a boss can't be placed after this items
            assumedItems.remove(item)
            # use chosen loc ap to check if an item can't be placed afterward
            itemLocDictAfter = self.services.getPossiblePlacementsWithoutItem(itemLoc.Location.accessPoint, self.container, assumedItems, alreadyPlacedItems)
            assumedItems.append(item)

            self.log.debug("after: {}".format([(it.Type, len(locs)) for (it, locs) in itemLocDictAfter.items()]))
            zeroLocsItemFound = False
            for it, locs in itemLocDictAfter.items():
                if it.Category == 'Boss' and len(locs) == 0:
                    self.log.debug("step: {} - zeroLocsItemFound for {} after placing {} !!".format(self.nSteps, it.Type, item.Type))
                    zeroLocsItemFound = True
                    break

            if zeroLocsItemFound:
                continue

            self.collect(itemLoc)
            assumedItems.remove(item)

        # add collected assumed items to container's smbm for next filler
        self.container.sm.addItems([itemLoc.Item.Type for itemLoc in self.container.itemLocations])

        print('\n%d step(s) in %dms' % (self.nSteps, int((time.process_time()-self.startDate)*1000)))

        return (False, self.container.itemLocations, self.getProgressionItemLocations())
