
import utils.log, copy, random, sys, logging
from enum import Enum, unique
from utils.parameters import infinity
from rando.ItemLocContainer import getLocListStr, getItemListStr, ContainerSoftBackup, ItemLocation
from logic.helpers import Bosses

# used to specify whether we want to come back from locations
@unique
class ComebackCheckType(Enum):
    Undefined = 0
    # do not check whether we should come back
    NoCheck = 1
    # come back with the placed item
    JustComeback = 2
    # come back without the placed item
    ComebackWithoutItem = 3

# collection of stateless services to be used mainly by fillers
class RandoServices(object):
    def __init__(self, graph, restrictions, cache=None):
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.areaGraph = graph
        self.cache = cache
        self.log = utils.log.get('RandoServices')

    # collect an item/loc with logic in a container from a given AP
    # return new AP
    def collect(self, ap, container, itemLoc, pickup=True):
        if pickup == True:
            # walk the graph to update AP
            if self.cache:
                self.cache.reset()
            self.currentLocations(ap, container)
        container.collect(itemLoc, pickup=pickup)
        self.log.debug("COLLECT "+itemLoc.Item.Type+" at "+itemLoc.Location.Name)
        sys.stdout.write('.')
        sys.stdout.flush()
        return itemLoc.Location.accessPoint if pickup == True else ap

    def getPossiblePlacementsWithoutItem(self, startAP, ap, container, items, maxDiff):
        distinctItems = {item.Type: item for item in items}
        self.log.debug("getPossiblePlacementsWithoutItem, unusedLocations: {}".format(len(container.unusedLocations)))
        return {item: self.allLocationsWithoutItem(item, startAP, ap, container, items, maxDiff) for itemType, item in distinctItems.items()}

    def allLocationsWithoutItem(self, item, startAP, ap, container, items, maxDiff):
        container.sm.resetItems()
        items.remove(item)
        container.sm.addItems([it.Type for it in items])
        items.append(item)

        if self.cache:
            self.cache.reset()

        # check if bosses can be accessed and killed, if so add them to alreadyPlacedItems:
        sm = container.sm

        if item.Type != 'Kraid' and sm.enoughStuffsKraid() and self.areaGraph.canAccess(container.sm, ap, 'KraidRoomIn', self.settings.maxDiff):
            container.sm.addItem('Kraid')
        if item.Type != 'Phantoon' and sm.enoughStuffsPhantoon() and self.areaGraph.canAccess(container.sm, ap, 'PhantoonRoomIn', self.settings.maxDiff):
            container.sm.addItem('Phantoon')
        if item.Type != 'Ridley' and sm.enoughStuffsRidley() and self.areaGraph.canAccess(container.sm, ap, 'RidleyRoomIn', self.settings.maxDiff):
            container.sm.addItem('Ridley')
        if (item.Type != 'Draygon'
            and sm.wand(sm.canFightDraygon(),
                        sm.enoughStuffsDraygon(),
                        sm.canExitDraygon())
            and (ap == 'Draygon Room Bottom' # need draygon dead to exit draygon room bottom
                 or self.areaGraph.canAccess(sm, ap, 'DraygonRoomIn', self.settings.maxDiff))):
            container.sm.addItem('Draygon')

        # check that we can access the locations without the item,
        curLocs = set(self.currentLocations(startAP, container, post=False, diff=maxDiff))

        # check if item is need to postavail some locs
        curLocsPostAvail = set([loc for loc in curLocs if self.fullComebackCheck(container, ap, item, loc, None, checkSoftlock=False)])

        curLocsPostAvailWoItem = set([loc for loc in curLocs if self.fullComebackCheck(container, ap, None, loc, None, checkSoftlock=False)])

        locsPostNokWoItem = list(curLocsPostAvail - curLocsPostAvailWoItem)

        # filter locs where we can place the item
        curLocsCanPlace = set([loc for loc in curLocsPostAvail if self.restrictions.canPlaceAtLocation(item, loc, container)])

        assert len(curLocsCanPlace) > 0


        # if count item it could happen that we're one item before some locs get unavailable,
        # so test the possible locs again with two items removed.
        locsNokWoDoubleItem = []
        if container.sm.isCountItem(item.Type) and container.sm.haveItem(item.Type):
            self.log.debug("test double remove for {}".format(item.Type))
            container.sm.removeItem(item.Type)

            if self.cache:
                self.cache.reset()

            curLocsDouble = set(self.currentLocations(startAP, container, post=False, diff=maxDiff))
            locsNokWoDoubleItem = list(curLocs - curLocsDouble)

            #self.log.debug("curLocs:       {}".format(sorted([loc.Name for loc in curLocs])))
            #self.log.debug("curLocsDouble: {}".format(sorted([loc.Name for loc in curLocsDouble])))

            if locsNokWoDoubleItem:
                self.log.debug("detected nok locs without double {}: {}".format(item.Type, [loc.Name for loc in locsNokWoDoubleItem]))

        container.sm.resetItems()

        # return locations still available without the item, and the number of it
        # return the locations no longer available without the item
        # return the locs where post avail fails without the item
        # return the locs no longer available without two items (for count items)
        # return the list of locations that we can still reach without the item and where we can place the item.
        return {"availLocsWoItem": curLocs, "availLocsWoItemLen": len(curLocs),
                "noLongerAvailLocsWoItem": set(container.unusedLocations) - curLocs,
                "locsNokWoDoubleItem": locsNokWoDoubleItem,
                "locsPostNokWoItem": locsPostNokWoItem, "possibleLocs": curLocsCanPlace}

    # reverse only boss left locations for assumed fill
    def getOnlyBossLeftLocationReverse(self, startAP, container, earlyGame):
        if self.settings.maxDiff == infinity:
            return []

        # draygon diff is computed in its path, so don't give draygon item
        if self.cache: self.cache.reset()
        container.sm.resetItems()
        container.sm.addItems([it.Type for it in container.itemPool if it.Type != "Draygon"]+["Phantoon", "Ridley", "Kraid"])

        curLocsMaxDiff1 = set(self.currentLocations(startAP, container, post=True))
        curLocsInfinity1 = set(self.currentLocations(startAP, container, post=True, diff=infinity))
        onlyBossLeft1 = curLocsInfinity1 - curLocsMaxDiff1

        # give draygon for space jump location which requires it
        if self.cache: self.cache.reset()
        container.sm.resetItems()
        container.sm.addItems([it.Type for it in container.itemPool]+["Draygon", "Phantoon", "Ridley", "Kraid"])

        curLocsMaxDiff2 = set(self.currentLocations(startAP, container, post=True))
        curLocsInfinity2 = set(self.currentLocations(startAP, container, post=True, diff=infinity))
        onlyBossLeft2 = curLocsInfinity2 - curLocsMaxDiff2

        onlyBossLeft = onlyBossLeft1.union(onlyBossLeft2)

        if not earlyGame:
            allReachableLocs = curLocsInfinity1.union(curLocsInfinity2)
            allLocs = set(container.unusedLocations)
            self.log.debug("only boss left, reach all locs ?: {}/{}".format(len(allReachableLocs), len(allLocs)))
            self.log.debug("only boss left locs: {}".format([loc.Name for loc in list(onlyBossLeft)]))
            if len(allReachableLocs) != len(allLocs):
                self.log.debug("one or more locations are now non reachable, should not happen !")
                for loc in list(allLocs - allReachableLocs):
                    self.log.debug("unreachable loc: {}".format(loc))
            assert len(allReachableLocs) == len(allLocs)

        container.sm.resetItems()

        return {loc: loc.difficulty.difficulty for loc in list(onlyBossLeft)}

    # gives all the possible theoretical locations for a given item
    def possibleLocations(self, item, ap, emptyContainer, bossesKilled=True):
        assert len(emptyContainer.currentItems) == 0, "Invalid call to possibleLocations. emptyContainer had collected items"
        emptyContainer.sm.resetItems()
        self.log.debug('possibleLocations. item='+item.Type)
        if bossesKilled:
            itemLambda = lambda it: it.Type != item.Type
        else:
            itemLambda = lambda it: it.Type != item.Type and it.Category != 'Boss'
        allBut = emptyContainer.getItems(itemLambda)
        self.log.debug('possibleLocations. allBut='+getItemListStr(allBut))
        emptyContainer.sm.addItems([it.Type for it in allBut])
        ret = [loc for loc in self.currentLocations(ap, emptyContainer, post=True) if self.restrictions.canPlaceAtLocation(item, loc, emptyContainer)]
        self.log.debug('possibleLocations='+getLocListStr(ret))
        emptyContainer.sm.resetItems()
        return ret

    # gives current accessible locations within a container from an AP, given an optional item.
    # post: checks post available?
    # diff: max difficulty to use (None for max diff from settings)
    def currentLocations(self, ap, container, item=None, post=False, diff=None):
        if self.cache is not None:
            request = self.cache.request('currentLocations', ap, container, None if item is None else item.Type, post, diff)
            ret = self.cache.get(request)
            if ret is not None:
                return ret
        sm = container.sm
        if diff is None:
            diff = self.settings.maxDiff
        itemType = None
        if item is not None:
            itemType = item.Type
            sm.addItem(itemType)
        ret = sorted(self.getAvailLocs(container, ap, diff),
                     key=lambda loc: loc.Name)
        if post is True:
            ret = [loc for loc in ret if self.locPostAvailable(sm, loc, itemType)]
        if item is not None:
            sm.removeItem(itemType)
        if self.cache is not None:
            self.cache.store(request, ret)
        return ret

    def locPostAvailable(self, sm, loc, item):
        if loc.PostAvailable is None:
            return True
        result = sm.withItem(item, loc.PostAvailable) if item is not None else loc.PostAvailable(sm)
        return result.bool == True and result.difficulty <= self.settings.maxDiff

    def getAvailLocs(self, container, ap, diff):
        sm = container.sm
        locs = container.unusedLocations
        return self.areaGraph.getAvailableLocations(locs, sm, diff, ap)

    # gives current accessible APs within a container from an AP, given an optional item.
    def currentAccessPoints(self, ap, container, item=None):
        if self.cache is not None:
            request = self.cache.request('currentAccessPoints', ap, container, None if item is None else item.Type)
            ret = self.cache.get(request)
            if ret is not None:
                return ret
        sm = container.sm
        if item is not None:
            itemType = item.Type
            sm.addItem(itemType)
        nodes = sorted(self.areaGraph.getAvailableAccessPoints(self.areaGraph.accessPoints[ap],
                                                               sm, self.settings.maxDiff),
                       key=lambda ap: ap.Name)
        if item is not None:
            sm.removeItem(itemType)
        if self.cache is not None:
            self.cache.store(request, nodes)

        return nodes

    def isSoftlockPossible(self, container, ap, item, loc, comebackCheck):
        sm = container.sm
        # usually early game
        if comebackCheck == ComebackCheckType.NoCheck:
            return False
        # some specific early/late game checks
        if loc.Name == 'Bomb' or loc.Name == 'Mother Brain':
            return False
        # if the loc forces us to go to an area we can't come back from
        comeBack = loc.accessPoint == ap or \
            self.areaGraph.canAccess(sm, loc.accessPoint, ap, self.settings.maxDiff, item.Type if item is not None else None)
        if not comeBack:
            self.log.debug("KO come back from " + loc.accessPoint + " to " + ap + " when trying to place " + ("None" if item is None else item.Type) + " at " + loc.Name)
            return True
#        else:
#            self.log.debug("OK come back from " + loc.accessPoint + " to " + ap + " when trying to place " + item.Type + " at " + loc.Name)
        if item is not None and comebackCheck == ComebackCheckType.ComebackWithoutItem and self.isProgression(item, ap, container):
            # we know that loc is avail and post avail with the item
            # if it is not post avail without it, then the item prevents the
            # possible softlock
            if not self.locPostAvailable(sm, loc, None):
                return True
            # item allows us to come back from a softlock possible zone
            comeBackWithout = self.areaGraph.canAccess(sm, loc.accessPoint,
                                                       ap,
                                                       self.settings.maxDiff,
                                                       None)
            if not comeBackWithout:
                return True

        return False

    def fullComebackCheck(self, container, ap, item, loc, comebackCheck, checkSoftlock=True):
        sm = container.sm
        tmpItems = []
        # draygon special case: there are two locations, and we can
        # place one item, but we might need both the item and the boss
        # dead to get out
        if loc.SolveArea == "Draygon Boss" and Bosses.bossDead(sm, 'Draygon').bool == False:
            # temporary kill draygon
            tmpItems.append('Draygon')
        sm.addItems(tmpItems)
        ret = self.locPostAvailable(sm, loc, item.Type if item is not None else None)
        if checkSoftlock:
            ret &= not self.isSoftlockPossible(container, ap, item, loc, comebackCheck)
        for tmp in tmpItems:
            sm.removeItem(tmp)
        return ret

    def isProgression(self, item, ap, container):
        sm = container.sm
        # no need to test nothing items
        if item.Category == 'Nothing':
            return False
        if self.cache is not None:
            request = self.cache.request('isProgression', item.Type, ap, container)
            ret = self.cache.get(request)
            if ret is not None:
                return ret
        oldLocations = self.currentLocations(ap, container)
        ret = any(self.restrictions.canPlaceAtLocation(item, loc, container) for loc in oldLocations)
        if ret == True:
            newLocations = [loc for loc in self.currentLocations(ap, container, item) if loc not in oldLocations]
            ret = len(newLocations) > 0 and any(self.restrictions.isItemLocMatching(item, loc) for loc in newLocations)
            self.log.debug('isProgression. item=' + item.Type + ', newLocs=' + str([loc.Name for loc in newLocations]))
            if ret == False and len(newLocations) > 0 and self.restrictions.split == 'Major':
                # in major/minor split, still consider minor locs as
                # progression if not all types are distributed
                ret = not sm.haveItem('Missile').bool \
                      or not sm.haveItem('Super').bool \
                      or not sm.haveItem('PowerBomb').bool
        if self.cache is not None:
            self.cache.store(request, ret)
        return ret

    def getPlacementLocs(self, ap, container, comebackCheck, itemObj, locs):
        return [loc for loc in locs if (itemObj is None or self.restrictions.canPlaceAtLocation(itemObj, loc, container)) and self.fullComebackCheck(container, ap, itemObj, loc, comebackCheck)]

    def processEarlyMorph(self, ap, container, comebackCheck, itemLocDict, curLocs):
        morph = container.getNextItemInPool('Morph')
        if morph is not None:
            self.log.debug("processEarlyMorph. morph not placed yet")
            morphLocItem = next((item for item in itemLocDict if item.Type == morph.Type), None)
            if morphLocItem is not None:
                morphLocs = itemLocDict[morphLocItem]
                itemLocDict.clear()
                itemLocDict[morphLocItem] = morphLocs
            elif len(curLocs) >= 2:
                self.log.debug("processEarlyMorph. early morph placement check")
                # we have to place morph early, it's still not placed, and not detected as placeable
                # let's see if we can place it anyway in the context of a combo
                morphLocs = self.getPlacementLocs(ap, container, comebackCheck, morph, curLocs)
                if len(morphLocs) > 0:
                    # copy our context to do some destructive checks
                    containerCpy = copy.copy(container)
                    # choose a morph item location in that context
                    morphItemLoc = ItemLocation(
                        morph,
                        random.choice(containerCpy.extractLocs(morphLocs))
                    )
                    # acquire morph in new context and see if we can still open new locs
                    newAP = self.collect(ap, containerCpy, morphItemLoc)
                    (ild, poss) = self.getPossiblePlacements(newAP, containerCpy, comebackCheck)
                    if poss:
                        # it's possible, only offer morph as possibility
                        itemLocDict.clear()
                        itemLocDict[morph] = morphLocs

    def processLateMorph(self, container, itemLocDict):
        morphLocItem = next((item for item in itemLocDict if item.Type == 'Morph'), None)
        if morphLocItem is None or len(itemLocDict) == 1:
            # no morph, or it is the only possibility: nothing to do
            return
        morphLocs = self.restrictions.lateMorphCheck(container, itemLocDict[morphLocItem])
        if morphLocs is not None:
            itemLocDict[morphLocItem] = morphLocs
        else:
            del itemLocDict[morphLocItem]

    def processNoComeback(self, ap, container, itemLocDict):
        comebackDict = {}
        for item,locList in itemLocDict.items():
            comebackLocs = [loc for loc in locList if self.fullComebackCheck(container, ap, item, loc, ComebackCheckType.JustComeback)]
            if len(comebackLocs) > 0:
                comebackDict[item] = comebackLocs
        if len(comebackDict) > 0:
            itemLocDict.clear()
            itemLocDict.update(comebackDict)

    def processPlacementRestrictions(self, ap, container, comebackCheck, itemLocDict, curLocs):
        if self.restrictions.isEarlyMorph():
            self.processEarlyMorph(ap, container, comebackCheck, itemLocDict, curLocs)
        elif self.restrictions.isLateMorph():
            self.processLateMorph(container, itemLocDict)
        if comebackCheck == ComebackCheckType.NoCheck:
            self.processNoComeback(ap, container, itemLocDict)

    # main logic function to be used by fillers. gives possible locations for each item.
    # ap: AP to check from
    # container: our item/loc container
    # comebackCheck: how to check for comebacks (cf ComebackCheckType)
    # return a dictionary with Item instances as keys and locations lists as values
    def getPossiblePlacements(self, ap, container, comebackCheck):
        curLocs = self.currentLocations(ap, container)
        self.log.debug('getPossiblePlacements. nCurLocs='+str(len(curLocs)))
        self.log.debug('getPossiblePlacements. curLocs='+getLocListStr(curLocs))
        self.log.debug('getPossiblePlacements. comebackCheck='+str(comebackCheck))
        sm = container.sm
        poolDict = container.getPoolDict()
        itemLocDict = {}
        possibleProg = False
        nonProgList = None
        def getLocList(itemObj):
            nonlocal curLocs
            return self.getPlacementLocs(ap, container, comebackCheck, itemObj, curLocs)
        def getNonProgLocList():
            nonlocal nonProgList
            if nonProgList is None:
                nonProgList = [loc for loc in self.currentLocations(ap, container) if self.fullComebackCheck(container, ap, None, loc, comebackCheck)]
                self.log.debug("nonProgLocList="+str([loc.Name for loc in nonProgList]))
            return [loc for loc in nonProgList if self.restrictions.canPlaceAtLocation(itemObj, loc, container)]
        for itemType,items in sorted(poolDict.items()):
            itemObj = items[0]
            cont = True
            prog = False
            if self.isProgression(itemObj, ap, container):
                cont = False
                prog = True
            elif not possibleProg:
                cont = False
            if cont: # ignore non prog items if a prog item has already been found
                continue
            # check possible locations for this item type
#            self.log.debug('getPossiblePlacements. itemType=' + itemType + ', curLocs='+str([loc.Name for loc in curLocs]))
            locations = getLocList(itemObj) if prog else getNonProgLocList()
            if len(locations) == 0:
                continue
            if prog and not possibleProg:
                possibleProg = True
                itemLocDict = {} # forget all the crap ones we stored just in case
#            self.log.debug('getPossiblePlacements. itemType=' + itemType + ', locs='+str([loc.Name for loc in locations]))
            for item in items:
                itemLocDict[item] = locations
        self.processPlacementRestrictions(ap, container, comebackCheck, itemLocDict, curLocs)
        self.printItemLocDict(itemLocDict)
        self.log.debug('possibleProg='+str(possibleProg))
        return (itemLocDict, possibleProg)

    def printItemLocDict(self, itemLocDict):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            debugDict = {}
            for item, locList in itemLocDict.items():
                if item.Type not in debugDict:
                    debugDict[item.Type] = [loc.Name for loc in locList]
            self.log.debug('itemLocDict='+str(debugDict))

    # same as getPossiblePlacements, without any logic check
    def getPossiblePlacementsNoLogic(self, container):
        poolDict = container.getPoolDict()
        itemLocDict = {}
        def getLocList(itemObj, baseList):
            return [loc for loc in baseList if self.restrictions.canPlaceAtLocation(itemObj, loc, container)]
        for itemType,items in sorted(poolDict.items()):
            itemObj = items[0]
            locList = getLocList(itemObj, container.unusedLocations)
            for item in items:
                itemLocDict[item] = locList
        self.printItemLocDict(itemLocDict)
        return (itemLocDict, False)

    # check if bosses are blocking the last remaining locations.
    # accurate most of the time, still a heuristic
    def onlyBossesLeft(self, ap, container):
        if self.settings.maxDiff == infinity:
            return False
        self.log.debug('onlyBossesLeft, diff=' + str(self.settings.maxDiff) + ", ap="+ap)
        sm = container.sm
        bossesLeft = container.getAllItemsInPoolFromCategory('Boss')
        if len(bossesLeft) == 0:
            return False
        def getLocList():
            curLocs = self.currentLocations(ap, container)
            self.log.debug('onlyBossesLeft, curLocs=' + getLocListStr(curLocs))
            return self.getPlacementLocs(ap, container, ComebackCheckType.JustComeback, None, curLocs)
        prevLocs = getLocList()
        self.log.debug("onlyBossesLeft. prevLocs="+getLocListStr(prevLocs))
        # fake kill remaining bosses and see if we can access the rest of the game
        if self.cache is not None:
            self.cache.reset()
        for boss in bossesLeft:
            self.log.debug('onlyBossesLeft. kill '+boss.Name)
            sm.addItem(boss.Type)
        # get bosses locations and newly accessible locations (for bosses that open up locs)
        newLocs = getLocList()
        self.log.debug("onlyBossesLeft. newLocs="+getLocListStr(newLocs))
        locs = newLocs + container.getLocs(lambda loc: loc.isBoss() and not loc in newLocs)
        self.log.debug("onlyBossesLeft. locs="+getLocListStr(locs))
        ret = (len(locs) > len(prevLocs) and len(locs) == len(container.unusedLocations))
        # restore bosses killed state
        for boss in bossesLeft:
            self.log.debug('onlyBossesLeft. revive '+boss.Name)
            sm.removeItem(boss.Type)
        if self.cache is not None:
            self.cache.reset()
        self.log.debug("onlyBossesLeft? " +str(ret))
        return ret

    def canEndGame(self, container):
        return not any(loc.Name == 'Mother Brain' for loc in container.unusedLocations)

    def can100percent(self, ap, container):
        if not self.canEndGame(container):
            return False
        curLocs = self.currentLocations(ap, container, post=True)
        return len(curLocs) == len(container.unusedLocations)

    def getStartupProgItemsPairs(self, ap, container):
        self.log.debug("getStartupProgItemsPairs: kickstart")
        (itemLocDict, isProg) = self.getPossiblePlacements(ap, container, ComebackCheckType.NoCheck)

        # save container
        saveEmptyContainer = ContainerSoftBackup(container)

        # key is (item1, item2)
        pairItemLocDict = {}

        # keep only unique items in itemLocDict
        uniqItemLocDict = {}
        for item, locs in itemLocDict.items():
            if item.Type in ['NoEnergy', 'Nothing']:
                continue
            if item.Type not in [it.Type for it in uniqItemLocDict.keys()]:
                uniqItemLocDict[item] = locs
        if not uniqItemLocDict:
            return None

        if self.cache:
            self.cache.reset()
        curLocsBefore = self.currentLocations(ap, container)
        if not curLocsBefore:
            return None

        self.log.debug("search for progression with a second item")
        for item1, locs1 in uniqItemLocDict.items():
            # collect first item in first available location matching restrictions
            if self.cache:
                self.cache.reset()
            firstItemPlaced = False
            for loc in curLocsBefore:
                if self.restrictions.canPlaceAtLocation(item1, loc, container):
                    self.log.debug("getStartupProgItemsPairs. firstItemPlaced")
                    container.collect(ItemLocation(item1, loc))
                    firstItemPlaced = True
                    break
            if not firstItemPlaced:
                saveEmptyContainer.restore(container)
                continue

            saveAfterFirst = ContainerSoftBackup(container)

            curLocsAfterFirst = self.currentLocations(ap, container)
            if not curLocsAfterFirst:
                saveEmptyContainer.restore(container)
                continue

            for item2, locs2 in uniqItemLocDict.items():
                if item1.Type == item2.Type:
                    continue

                if (item1, item2) in pairItemLocDict.keys() or (item2, item1) in pairItemLocDict.keys():
                    continue

                # collect second item in first available location
                if self.cache:
                    self.cache.reset()
                secondItemPlaced = False
                for loc in curLocsAfterFirst:
                    if self.restrictions.canPlaceAtLocation(item2, loc, container):
                        container.collect(ItemLocation(item2, loc))
                        secondItemPlaced = True
                        break
                if not secondItemPlaced:
                    saveAfterFirst.restore(container)
                    continue

                curLocsAfterSecond = self.currentLocations(ap, container)
                if not curLocsAfterSecond:
                    saveAfterFirst.restore(container)
                    continue

                pairItemLocDict[(item1, item2)] = [curLocsBefore, curLocsAfterFirst, curLocsAfterSecond]
                saveAfterFirst.restore(container)

            saveEmptyContainer.restore(container)

        # check if a pair was found
        if len(pairItemLocDict) == 0:
            self.log.debug("no pair was found")
            return None
        else:
            if self.log.getEffectiveLevel() == logging.DEBUG:
                self.log.debug("pairItemLocDict:")
                for key, locs in pairItemLocDict.items():
                    self.log.debug("{}->{}: {}".format(key[0].Type, key[1].Type, [l['Name'] for l in locs[2]]))

            return pairItemLocDict
