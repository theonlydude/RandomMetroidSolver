
import copy
from smboolmanager import SMBoolManager

class ItemLocContainer(object):
    def __init__(self, sm, itemPool, locations):
        self.sm = sm
        self.itemLocations = []
        self.unusedLocations = locations
        self.currentItems = []
        self.itemPool = itemPool

    def __copy__(self):
        locs = [copy.deepcopy(loc) for loc in self.unusedLocations]
        ret = ItemLocContainer(SMBoolManager(),
                               self.itemPool[:],
                               locs)
        ret.currentItems = self.currentItems[:]
        for il in self.itemLocations:
            ilCpy = {
                'Item': il['Item'],
                'Location': copy.deepcopy(il['Location'])
            }
            ret.itemLocations.append(ilCpy)
        ret.sm.addItems([item['Type'] for item in ret.currentItems])
        return ret

    def extractLocs(self, locs):
        return [next(l in self.unusedLocations if l['Name'] == loc['Name']) for loc in locs]

    def collect(self, itemLocation, pickup=True):
        item = itemLocation['Item']
        location = itemLocation['Location']
        if pickup == True:
            self.currentItems.append(item)
            self.sm.addItem(item['Type'])
        self.unusedLocations.remove(location)
        self.itemLocations.append(itemLocation)
        self.itemPool.remove(self.getNextItemInPool(item['Type']))

    def isPoolEmpty(self):
        return len(self.itemPool) == 0
        
    def getNextItemInPool(self, t):
        return next(item for item in self.itemPool if item['Type'] == t, None)

    def hasItemTypeInPool(self, t):
        return any(item['Type'] == t for item in self.itemPool)

    def hasItemCategoryInPool(self, cat):
        return any(item['Category'] == cat for item in self.itemPool)

    def getNextItemInPoolFromCategory(self, cat):
        return next(item for item in self.itemPool if item['Category'] == cat, None)

    def getAllItemsInPoolFromCategory(self, cat):
        return [item for item in self.itemPool if item['Category'] == cat]
    
    def countItemTypeInPool(self, t):
        return len([item for item in self.itemPool if item['Type'] == t])

    def getPoolDict(self):
        poolDict = {}
        for item in self.itemPool:
            if item['Type'] not in poolDict:
                poolDict[item['Type']] = []
            poolDict[item['Type']].append(item)
        return poolDict

    def getLocs(self, predicate):
        return [loc for loc in self.unusedLocations if predicate(loc) == True]
