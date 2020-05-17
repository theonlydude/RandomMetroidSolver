
import copy
from smboolmanager import SMBoolManager

class ItemLocContainer(object):
    def __init__(self, smbm, itemPool, locations):
        self.smbm = smbm
        self.itemLocations = []
        self.unusedLocations = locations
        self.currentItems = []
        self.itemPool = itemPool

    def __copy__(self):
        locs = [copy.deepcopy(loc) for loc in self.unusedLocations]
        sm = SMBoolManager()        
        ret = ItemLocContainer(sm,
                               self.itemPool[:],
                               locs)
        ret.currentItems = self.currentItems[:]
        for il in self.itemLocations:
            ilCpy = {
                'Item': il['Item'],
                'Location': copy.deepcopy(il['Location'])
            }
            ret.itemLocations.append(ilCpy)
        ret.smbm.addItems([item['Type'] for item in ret.currentItems])
        return ret

    def collect(self, itemLocation, pickup=True):
        item = itemLocation['Item']
        location = itemLocation['Location']
        if pickup == True:
            if 'Pickup' in location:
                location['Pickup']()
            self.currentItems.append(item)
            self.smbm.addItem(item['Type'])
        self.unusedLocations.remove(location)
        self.itemLocations.append(itemLocation)
        self.itemPool.remove(getNextItemInPool(item['Type']))

    def getNextItemInPool(self, t):
        return next(item for item in self.itemPool if item['Type'] == t, None)

    def hasItemType(self, t):
        return any(item['Type'] == t for item in self.itemPool)

    def hasItemCategory(self, cat):
        return any(item['Category'] == cat for item in self.itemPool)

    def getNextItemInPoolFromCategory(self, cat):
        return next(item for item in self.itemPool if item['Category'] == cat, None)

    def countItemTypeInPool(self, t):
        return len([item for item in self.itemPool if item['Type'] == t])

    def getPoolDict(self):
        poolDict = {}
        for item in self.itemPool:
            if item['Type'] not in poolDict:
                poolDict[item['Type']] = []
            poolDict[item['Type']].append(item)
        return poolDict
