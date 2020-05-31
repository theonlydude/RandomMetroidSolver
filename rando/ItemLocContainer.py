
import copy, log

from smboolmanager import SMBoolManager
from collections import Counter

def getItemListStr(items):
    return str(dict(Counter([item['Type'] for item in items])))

def getLocListStr(locs):
    return str([loc['Name'] for loc in locs])

def getItemLocStr(itemLoc):
    return itemLoc['Item']['Type'] + " at " + itemLoc['Location']['Name']

def getItemLocationsStr(itemLocations):
    return str([getItemLocStr(il) for il in itemLocations])

class ItemLocContainer(object):
    def __init__(self, sm, itemPool, locations):
        self.sm = sm
        self.itemLocations = []
        self.unusedLocations = locations
        self.currentItems = []
        self.itemPool = itemPool
        self.itemPoolBackup = None
        self.unrestrictedItems = set()
        self.log = log.get('ItemLocContainer')
        self.checkConsistency()

    def checkConsistency(self):
        assert len(self.unusedLocations) == len(self.itemPool), "Item/Locs count mismatch"

    def __eq__(self, rhs):
        eq = self.currentItems == rhs.currentItems
        eq &= getLocListStr(self.unusedLocations) == getLocListStr(rhs.unusedLocations)
        eq &= self.itemPool == rhs.itemPool
        eq &= getItemLocationsStr(self.itemLocations) == getItemLocationsStr(rhs.itemLocations)

        return eq

    def __copy__(self):
        locs = [copy.deepcopy(loc) for loc in self.unusedLocations]
        ret = ItemLocContainer(SMBoolManager(),
                               self.itemPool[:],
                               locs)
        ret.currentItems = self.currentItems[:]
        ret.unrestrictedItems = copy.copy(self.unrestrictedItems)
        for il in self.itemLocations:
            ilCpy = {
                'Item': il['Item'],
                'Location': copy.deepcopy(il['Location'])
            }
            ret.itemLocations.append(ilCpy)
        ret.sm.addItems([item['Type'] for item in ret.currentItems])
        # we don't copy restriction state on purpose
        return ret

    def slice(self, itemPoolCond, locPoolCond):
        assert self.itemPoolBackup is None, "Cannot slice a constrained container"
        locs = self.getLocs(locPoolCond)
        items = self.getItems(itemPoolCond)
        cont = ItemLocContainer(self.sm, items, locs)
        cont.currentItems = self.currentItems
        cont.itemLocations = self.itemLocations
        return copy.copy(cont)

    def transferCollected(self, dest):
        dest.currentItems = self.currentItems[:]
        dest.sm = SMBoolManager()
        dest.sm.addItems([item['Type'] for item in dest.currentItems])
        dest.itemLocations = copy.copy(self.itemLocations)
        dest.unrestrictedItems = copy.copy(self.unrestrictedItems)

    def resetCollected(self):
        self.currentItems = []
        self.itemLocations = []
        self.unrestrictedItems = set()
        self.sm.resetItems()

    def dump(self):
        return "ItemPool(%d): %s\nLocPool(%d): %s\nCollected: %s" % (len(self.itemPool), getItemListStr(self.itemPool), len(self.unusedLocations), getLocListStr(self.unusedLocations), getItemListStr(self.currentItems))

    # temporarily restrict item pool to items fulfilling predicate
    def restrictItemPool(self, predicate):
        assert self.itemPoolBackup is None, "Item pool already restricted"
        self.itemPoolBackup = self.itemPool
        self.itemPool = [item for item in self.itemPoolBackup if predicate(item)]
        self.log.debug("restrictItemPool: "+getItemListStr(self.itemPool))

    # remove a placed restriction
    def unrestrictItemPool(self):
        assert self.itemPoolBackup is not None, "No pool restriction to remove"
        self.itemPool = self.itemPoolBackup
        self.itemPoolBackup = None
        self.log.debug("unrestrictItemPool: "+getItemListStr(self.itemPool))

    def extractLocs(self, locs):
        ret = []
        for loc in locs:
            ret.append(next(l for l in self.unusedLocations if l['Name'] == loc['Name']))
        return ret

    def removeLocation(self, location):
        if location in self.unusedLocations:
            self.unusedLocations.remove(location)
        else:
            self.unusedLocations.remove(next(loc for loc in self.unusedLocations if loc['Name'] == location['Name']))

    def removeItem(self, item):
        self.itemPool.remove(item)
        if self.itemPoolBackup is not None:
            self.itemPoolBackup.remove(item)
    
    def collect(self, itemLocation, pickup=True):
        item = itemLocation['Item']
        location = itemLocation['Location']
        if 'restricted' not in location or location['restricted'] == False:
            self.unrestrictedItems.add(item['Type'])
        if pickup == True:
            self.currentItems.append(item)
            self.sm.addItem(item['Type'])
        self.removeLocation(location)
        self.itemLocations.append(itemLocation)
        self.removeItem(item)

    def isPoolEmpty(self):
        return len(self.itemPool) == 0

    def getNextItemInPool(self, t):
        return next((item for item in self.itemPool if item['Type'] == t), None)

    def getNextItemInPoolMatching(self, predicate):
        return next((item for item in self.itemPool if predicate(item) == True), None)

    def hasItemTypeInPool(self, t):
        return any(item['Type'] == t for item in self.itemPool)

    def hasItemInPool(self, predicate):
        return any(predicate(item) == True for item in self.itemPool)

    def hasItemCategoryInPool(self, cat):
        return any(item['Category'] == cat for item in self.itemPool)

    def getNextItemInPoolFromCategory(self, cat):
        return next((item for item in self.itemPool if item['Category'] == cat), None)

    def getAllItemsInPoolFromCategory(self, cat):
        return [item for item in self.itemPool if item['Category'] == cat]

    def countItemTypeInPool(self, t):
        return sum(1 for item in self.itemPool if item['Type'] == t)

    def countItems(self, predicate):
        return sum(1 for item in self.itemPool if predicate(item) == True)

    def getPoolDict(self):
        poolDict = {}
        for item in self.itemPool:
            if item['Type'] not in poolDict:
                poolDict[item['Type']] = []
            poolDict[item['Type']].append(item)
        return poolDict

    def getLocs(self, predicate):
        return [loc for loc in self.unusedLocations if predicate(loc) == True]

    def getItems(self, predicate):
        return [item for item in self.itemPool if predicate(item) == True]

    def getUsedLocs(self, predicate):
        return [il['Location'] for il in self.itemLocations if predicate(il['Location']) == True]

    def getCollectedItems(self, predicate):
        return [item for item in self.currentItems if predicate(item) == True]

    def hasUnrestrictedLocWithItemType(self, itemType):
        return itemType in self.unrestrictedItems
