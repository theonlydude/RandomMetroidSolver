from Randomizer import Randomizer
from stdlib import Map, Array, List, Random
import Items
import random

class DefaultRandomizer(Randomizer):
    def __init__(self, seed, difficultyTarget, locations):
        super(DefaultRandomizer, self).__init__(seed, difficultyTarget, locations)

    def getItemToPlace(self, items, itemPool):        
        itemsLen = len(items)
        if itemsLen == 0:
            item = List.item(random.randint(0, len(itemPool)-1), itemPool)
        else:
            item = List.item(random.randint(0, len(items)-1), items)
        return item

    def generateItems(self):
        items = []
        itemLocations = []
        self.currentItems = items
        while len(self.itemPool) > 0:
            curLocs = self.currentLocations(items)
            itemLocation = None
            while itemLocation is None:
                posItems = self.possibleItems(curLocs, items, itemLocations, self.itemPool, self.locationPool)

                itemLocation = self.placeItem(posItems, self.itemPool, curLocs)
            print(str(len(self.currentItems) + 1) + ':' + itemLocation['Item']['Type'] + ' at ' + itemLocation['Location']['Name'])
            items.append(itemLocation['Item'])
            itemLocations.append(itemLocation)
            self.itemPool = self.removeItem(itemLocation['Item']['Type'], self.itemPool)

        return itemLocations
