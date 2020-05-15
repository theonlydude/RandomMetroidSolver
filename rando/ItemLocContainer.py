


class ItemLocContainer(object):
    def __init__(self, smbm, itemPool, locations):
        self.smbm = smbm
        self.itemLocations = []
        self.unusedLocations = locations
        self.currentItems = []
        self.itemPool = itemPool

    def __copy__(self):
        return ItemLocContainer(self.smbm,
                                self.itemPool[:],
                                [copy.deepcopy(loc) for loc in self.locations])

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
        return next(item for item in self.itemPool if item['Type'] == t)

    def hasItemType(self, t):
        return any(item['Type'] == t for item in self.itemPool)

    def countItemTypeInPool(self, t):
        return len([item for item in self.itemPool if item['Type'] == t])
