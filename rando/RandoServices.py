
import log

class ItemWrapper(object): # to put items in dictionaries
    def __init__(self, item):
        self.item = item
        item['Wrapper'] = self

class RandoServices(object):
    def __init__(self, graph, restrictions):
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.areaGraph = areaGraph
        self.log = log.get('RandoServices')

    def updateAP(self, ap, container, itemLoc):
        # walk the graph to update AP
        self.currentLocations(ap, container)
        return itemLoc['Location']['accessPoint']

    def currentLocations(self, ap, container, item=None, post=False, diff=None):
        sm = container.smbm
        if diff is None:
            diff = self.settings.difficultyTarget
        itemType = None
        if item is not None:
            itemType = item['Type']
            sm.addItem(itemType)
        ret = sorted(self.getAvailLocs(container.locs, ap, diff),
                     key=lambda loc: loc['Name'])
        if post is True:
            ret = [loc for loc in ret if self.locPostAvailable(sm, loc, itemType)]
        if item is not None:
            sm.removeItem(itemType)

        return ret

    def locPostAvailable(self, sm, loc, item):
        if not 'PostAvailable' in loc:
            return True
        result = sm.eval(loc['PostAvailable'], item)
        return result.bool == True and result.difficulty <= self.settings.difficultyTarget
    
    def getAvailLocs(self, locs, ap, diff):
        return self.areaGraph.getAvailableLocations(locs,
                                                    self.smbm,
                                                    diff,
                                                    ap)

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
        sm = container.smbm
        if item is not None:
            itemType = item['Type']
            sm.addItem(itemType)
        nodes = sorted(self.areaGraph.getAvailableAccessPoints(self.areaGraph.accessPoints[ap],
                                                               sm, self.settings.difficultyTarget),
                       key=lambda ap: ap.Name)
        if item is not None:
            sm.removeItem(itemType)

        return nodes

    # FIXME no proba adjust here, just raw check
    def isSoftlockPossible(self, sm, ap, item, loc, justComeback):
        # disable check for early game and MB
        if loc['Name'] == 'Bomb' or loc['Name'] == 'Mother Brain':
            return False
        isPickup = 'Pickup' in loc
        if isPickup:
            loc['Pickup']()
        # if the loc forces us to go to an area we can't come back from
        comeBack = loc['accessPoint'] == ap or \
            self.areaGraph.canAccess(sm, loc['accessPoint'], ap, self.settings.difficultyTarget, item['Type'])
        if isPickup:
            loc['Unpickup']()
        if not comeBack:
            self.log.debug("KO come back from " + loc['accessPoint'] + " to " + self.curAccessPoint + " when trying to place " + item['Type'] + " at " + loc['Name'])
            return True
        else:
            self.log.debug("OK come back from " + loc['accessPoint'] + " to " + self.curAccessPoint + " when trying to place " + item['Type'] + " at " + loc['Name'])
        if not justComeback:
            # we know that loc is avail and post avail with the item
            # if it is not post avail without it, then the item prevents the
            # possible softlock
            if not self.locPostAvailable(sm, loc, None):
                return True
            # item allows us to come back from a softlock possible zone
            comeBackWithout = self.areaGraph.canAccess(sm, loc['accessPoint'],
                                                       ap,
                                                       self.settings.difficultyTarget,
                                                       None)
            if not comeBackWithout:
                return True

        return False
