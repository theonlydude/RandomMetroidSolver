from NewRandomizer import NewRandomizer
from stdlib import Map, Array, List, Random
import Items
import random

class DefaultRandomizer(NewRandomizer):
    def __init__(self, seed, difficultyTarget, locations):
        super(DefaultRandomizer, self).__init__(seed, difficultyTarget, locations)

    def placeItem(self, items, itemPool, locations):
        # 
        #
        # items: possible items to place
        # itemPool: 
        # locations: locations available
        #
        # returns a dict with the item and the location

        itemsLen = len(items)
        if itemsLen == 0:
            item = List.item(random.randint(0, len(itemPool)-1), itemPool)
        else:
            item = List.item(random.randint(0, len(items)-1), items)

        availableLocations = List.filter(lambda loc: self.canPlaceAtLocation(item, loc), locations)
        location = List.item(random.randint(0, len(availableLocations)-1), availableLocations)

        self.usedLocations += [location]
        i=0
        for loc in self.unusedLocations:
            if loc == location:
                self.unusedLocations = self.unusedLocations[0:i] + self.unusedLocations[i+1:]
            i+=1

        if 'Pickup' in location:
            location['Pickup']()

        return {'Item': item, 'Location': location}

    def generateItems(self, items, itemLocations):
        while len(self.itemPool) > 0:
            curLocs = self.currentLocations(items)
            posItems = self.possibleItems(curLocs, items, itemLocations, self.itemPool, self.locationPool)

            itemLocation = self.placeItem(posItems, self.itemPool, curLocs)

            items = [itemLocation['Item']] + items
            itemLocations += [itemLocation]
            self.itemPool = self.removeItem(itemLocation['Item']['Type'], self.itemPool)

        return itemLocations
