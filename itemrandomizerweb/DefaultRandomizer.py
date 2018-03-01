from Randomizer import Randomizer
from stdlib import Map, Array, List, Random
import Items
import random
import sys

class DefaultRandomizer(Randomizer):
    def __init__(self, seed, difficultyTarget, locations, qty, sampleSize, choose, restrictions):
        super(DefaultRandomizer, self).__init__(seed, difficultyTarget, locations, qty, sampleSize, choose, restrictions)
    
    def generateItems(self):
        items = []
        itemLocations = []
        self.currentItems = items
        while len(self.itemPool) > 0:
            curLocs = self.currentLocations(items)
            itemLocation = None
            self.failItems = []
            while itemLocation is None:
                posItems = self.possibleItems(curLocs, items, itemLocations, self.itemPool, self.locationPool)
                itemLocation = self.placeItem(posItems, self.itemPool, curLocs)
                if len(self.failItems) >= len(posItems):
                    break
            if itemLocation is None:
                return None
#            print(str(len(self.currentItems) + 1) + ':' + itemLocation['Item']['Type'] + ' at ' + itemLocation['Location']['Name'])
            sys.stdout.write('.')
            sys.stdout.flush()
            items.append(itemLocation['Item'])
            itemLocations.append(itemLocation)
            self.itemPool = self.removeItem(itemLocation['Item']['Type'], self.itemPool)
        print("")
            
        return itemLocations
