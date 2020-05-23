
import log, copy, random, sys, logging
from enum import Enum, unique
from parameters import infinity

class ItemWrapper(object): # to put items in dictionaries
    def __init__(self, item):
        self.item = item
        item['Wrapper'] = self

@unique
class ComebackCheckType(Enum):
    NoCheck = 1
    JustComeback = 2
    ComebackWithoutItem = 3

class RandoServices(object):
    def __init__(self, graph, restrictions, cache=None):
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.areaGraph = graph
        self.cache = cache
        self.log = log.get('RandoServices')

    def collect(self, ap, container, itemLoc):
        # walk the graph to update AP
        self.currentLocations(ap, container, itemLoc['Item'])
        container.collect(itemLoc)
        self.log.debug("COLLECT "+itemLoc['Item']['Type']+" at "+itemLoc['Location']['Name'])
        sys.stdout.write('.')
        sys.stdout.flush()
        return itemLoc['Location']['accessPoint']

    def currentLocations(self, ap, container, item=None, post=False, diff=None):
        if self.cache is not None:
            request = self.cache.request('currentLocations', ap, container, None if item is None else item['Type'], post, diff)
            ret = self.cache.get(request)
            if ret is not None:
                return ret
        sm = container.sm
        if diff is None:
            diff = self.settings.maxDiff
        itemType = None
        if item is not None:
            itemType = item['Type']
            sm.addItem(itemType)
        ret = sorted(self.getAvailLocs(container, ap, diff),
                     key=lambda loc: loc['Name'])
        if post is True:
            ret = [loc for loc in ret if self.locPostAvailable(sm, loc, itemType)]
        if item is not None:
            sm.removeItem(itemType)
        if self.cache is not None:
            self.cache.store(request, ret)
        return ret

    def locPostAvailable(self, sm, loc, item):
        if not 'PostAvailable' in loc:
            return True
        result = sm.eval(loc['PostAvailable'], item)
        return result.bool == True and result.difficulty <= self.settings.maxDiff
    
    def getAvailLocs(self, container, ap, diff):
        sm = container.sm
        locs = container.unusedLocations
        return self.areaGraph.getAvailableLocations(locs, sm, diff, ap)

        # if self.restrictions['MajorMinor'] != 'Chozo' or diff >= god or not self.isChozoLeft():
        #     return availLocs
        # # in chozo mode, we use high difficulty check for bosses/hardrooms/hellruns
        # availLocsInf = self.areaGraph.getAvailableLocations(locs,
        #                                                     self.smbm,
        #                                                     god,
        #                                                     ap)
        # def isAvail(loc):
        #     for k in loc['difficulty'].knows:
        #         try:
        #             smKnows = getattr(Knows, k)
        #             # filter out tricks above diff target except boss
        #             # knows, because boss fights can be performed
        #             # without the trick anyway.
        #             # this barely works, because it is possible for
        #             # standard fight diff to be above god.  it is
        #             # never totally impossible because there is no
        #             # Knows for Ridley, and other bosses give
        #             # drops. so only boss fights with diff above god
        #             # can slip in
        #             if smKnows.difficulty > diff and isBossKnows(k) is None:
        #                 return False
        #         except AttributeError:
        #             # hard room/hell run
        #             pass
        #     return True

        # for loc in availLocsInf:
        #     if loc not in availLocs and isAvail(loc):
        #         availLocs.append(loc)

        # return availLocs

    def currentAccessPoints(self, ap, container, item=None):
        if self.cache is not None:
            request = self.cache.request('currentAccessPoints', ap, container, None if item is None else item['Type'])
            ret = self.cache.get(request)
            if ret is not None:
                return ret
        sm = container.sm
        if item is not None:
            itemType = item['Type']
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
        # some specific checks
        if loc['Name'] == 'Bomb' or loc['Name'] == 'Mother Brain' or\
           (loc['Name'] in ['Draygon', 'Space Jump'] and sm.canExitDraygon()):
            return False
        # if the loc forces us to go to an area we can't come back from
        comeBack = loc['accessPoint'] == ap or \
            self.areaGraph.canAccess(sm, loc['accessPoint'], ap, self.settings.maxDiff, item['Type'] if item is not None else None)
        if not comeBack:
            self.log.debug("KO come back from " + loc['accessPoint'] + " to " + ap + " when trying to place " + item['Type'] + " at " + loc['Name'])
            return True
#        else:
#            self.log.debug("OK come back from " + loc['accessPoint'] + " to " + ap + " when trying to place " + item['Type'] + " at " + loc['Name'])
        if item is not None and comebackCheck == ComebackCheckType.ComebackWithoutItem and self.isProgression(item, ap, container):
            # we know that loc is avail and post avail with the item
            # if it is not post avail without it, then the item prevents the
            # possible softlock
            if not self.locPostAvailable(sm, loc, None):
                return True
            # item allows us to come back from a softlock possible zone
            comeBackWithout = self.areaGraph.canAccess(sm, loc['accessPoint'],
                                                       ap,
                                                       self.settings.maxDiff,
                                                       None)
            if not comeBackWithout:
                return True

        return False

    def fullComebackCheck(self, container, ap, item, loc, comebackCheck):
        sm = container.sm
        return self.locPostAvailable(sm, loc, item['Type'] if item is not None else None) and not self.isSoftlockPossible(container, ap, item, loc, comebackCheck)

    def isProgression(self, item, ap, container):
        sm = container.sm
        # no need to test nothing items
        if item['Category'] == 'Nothing' or item['Category'] == 'Boss':
            return False
        if self.cache is not None:
            request = self.cache.request('isProgression', item['Type'], ap, container)
            ret = self.cache.get(request)
            if ret is not None:
                return ret
        oldLocations = self.currentLocations(ap, container)
        ret = any(self.restrictions.canPlaceAtLocation(item, loc) for loc in oldLocations)
        if ret == True:
            newLocations = [loc for loc in self.currentLocations(ap, container, item) if loc not in oldLocations]
            ret = len(newLocations) > 0 and any(self.restrictions.isItemLocMatching(item, loc) for loc in newLocations)
            self.log.debug('checkItem. item=' + item['Type'] + ', newLocs=' + str([loc['Name'] for loc in newLocations]))
            if ret == False and len(newLocations) > 0 and self.restrictions.split == 'Major':
                # in major/minor split, still consider minor locs as
                # progression if not all types are distributed
                ret = not sm.haveItem('Missile').bool \
                      or not sm.haveItem('Super').bool \
                      or not sm.haveItem('PowerBomb').bool
        if self.cache is not None:
            self.cache.store(request, ret)
        return ret

    def getPossiblePlacements(self, ap, container, comebackCheck):
        curLocs = self.currentLocations(ap, container)
        self.log.debug('getPossiblePlacements. nCurLocs='+str(len(curLocs)))
        sm = container.sm
        poolDict = container.getPoolDict()
        itemLocDict = {}
        possibleProg = False
        nonProgList = None
        def getLocList(itemObj, baseList):
            nonlocal sm
            return [loc for loc in baseList if self.restrictions.canPlaceAtLocation(itemObj, loc) and self.fullComebackCheck(container, ap, itemObj, loc, comebackCheck)]
        def getNonProgLocList(itemObj):
            nonlocal nonProgList, sm
            if nonProgList is None:
                nonProgList = [loc for loc in self.currentLocations(ap, container) if self.fullComebackCheck(container, ap, itemObj, loc, comebackCheck)] # we don't care what the item is
                self.log.debug("nonProgLocList="+str([loc['Name'] for loc in nonProgList]))
            return [loc for loc in nonProgList if self.restrictions.canPlaceAtLocation(itemObj, loc)]
        # boss handling : check if we can kill a boss, if so return immediately
        hasBoss = container.hasItemCategoryInPool('Boss')
        bossLoc = None if not hasBoss else next((loc for loc in curLocs if 'Boss' in loc['Class'] and self.fullComebackCheck(container, ap, None, loc, comebackCheck)), None)
        if bossLoc is not None:
            bosses = container.getItems(lambda item: item['Name'] == bossLoc['Name'])
            assert len(bosses) == 1
            boss = bosses[0]
            itemLocDict[ItemWrapper(boss)] = [bossLoc]
            self.log.debug("getPossiblePlacements. boss: "+boss['Name'])
            return (itemLocDict, False)
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
            self.log.debug('getPossiblePlacements. itemType=' + itemType + ', curLocs='+str([loc['Name'] for loc in curLocs]))
            locations = getLocList(itemObj, curLocs) if prog else getNonProgLocList(itemObj)
            if len(locations) == 0:
                continue
            if prog and not possibleProg:
                possibleProg = True
                itemLocDict = {} # forget all the crap ones we stored just in case
            self.log.debug('getPossiblePlacements. itemType=' + itemType + ', locs='+str([loc['Name'] for loc in locations]))
            for item in items:
                itemLocDict[ItemWrapper(item)] = locations
        # special check for early morph
        if self.restrictions.isEarlyMorph() and len(curLocs) >= 2:
            morph = container.getNextItemInPool('Morph')
            if morph is not None:
                self.log.debug("getPossiblePlacements: early morph check - morph not placed yet")
            if morph is not None and not any(w.item['Type'] == morph['Type'] for w in itemLocDict):
                self.log.debug("getPossiblePlacements: early morph placement check")
                # we have to place morph early, it's still not placed, and not detected as placeable
                # let's see if we can place it anyway in the context of a combo
                morphLocs = getLocList(morph, curLocs)
                if len(morphLocs) > 0:
                    # copy our context to do some destructive checks
                    containerCpy = copy.copy(container)
                    # choose a morph item location in that context
                    morphItemLoc = {
                        'Item':morph,
                        'Location':random.choice(containerCpy.extractLocs(morphLocs))
                    }
                    # acquire morph in new context and see if we can still open new locs
                    newAP = self.collect(ap, container, morphItemLoc)
                    (ild, poss) = self.getPossiblePlacements(newAP, containerCpy, comebackCheck)
                    if poss:
                        # it's possible, add morph and its locations from our context
                        itemLocDict[ItemWrapper(morph)] = morphLocs
        if self.log.getEffectiveLevel() == logging.DEBUG:
            debugDict = {}
            for w, locList in itemLocDict.items():
                if w.item['Type'] not in debugDict:
                    debugDict[w.item['Type']] = [loc['Name'] for loc in locList]
            self.log.debug('itemLocDict='+str(debugDict))
            self.log.debug('possibleProg='+str(possibleProg))
        return (itemLocDict, possibleProg)

    def getPossiblePlacementsNoLogic(self, container):
        poolDict = container.getPoolDict()
        itemLocDict = {}
        def getLocList(itemObj, baseList):
            return [loc for loc in baseList if self.restrictions.canPlaceAtLocation(itemObj, loc)]
        for itemType,items in sorted(poolDict.items()):
            itemObj = items[0]
            locList = getLocList(itemObj, container.unusedLocations)
            for item in items:
                itemLocDict[ItemWrapper(item)] = locList
        return (itemLocDict, False)

    # check if bosses are blocking the last remaining locations.
    # accurate most of the time, still a heuristic
    def onlyBossesLeft(self, ap, container):
        if self.settings.maxDiff == infinity:
            return False
        self.log.debug('onlyBossesLeft, diff=' + str(self.settings.maxDiff))
        sm = container.sm
        bossesLeft = container.getAllItemsInPoolFromCategory('Boss')
        if len(bossesLeft) == 0:
            return False
        def getLocList():
            return [loc for loc in self.currentLocations(ap, container) if self.fullComebackCheck(container, ap, None, loc, True)]
        prevLocs = getLocList()
        # fake kill remaining bosses and see if we can access the rest of the game
        if self.cache is not None:
            self.cache.reset()
        for boss in bossesLeft:
            sm.addItem(boss['Type'])
        # get bosses locations and newly accessible locations (for bosses that open up locs)
        newLocs = getLocList()
        locs = newLocs + container.getLocs(lambda loc: 'Boss' in loc['Class'] and not loc in newLocs)
        ret = (len(locs) > len(prevLocs) and len(locs) == len(container.unusedLocations))
        # restore bosses killed state
        for boss in bossesLeft:
            sm.removeItem(boss['Type'])
        if self.cache is not None:
            self.cache.reset()
        self.log.debug("onlyBossesLeft? " +str(ret))
        return ret

    def canEndGame(self, container):
        return not any(loc['Name'] == 'Mother Brain' for loc in container.unusedLocations)
