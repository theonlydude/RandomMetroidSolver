from Randomizer import Randomizer
from stdlib import Map, Array, List, Random
import Items
import random

class FullRandomizer(Randomizer):
    def __init__(self, seed, difficultyTarget, locations):
        self.rnd = Random(seed)
        random.seed(seed)

        self.itemPool = Items.getItemPool(self.rnd)
        self.locationPool = locations

        # list of locations not already used
        self.unusedLocations = locations
        # list of locations already used
        self.usedLocations = []
        # list of {'Item': item, 'Location': location}, the items assigned to a location
        self.itemLocations = []

    def canPlaceAtLocation(self, item, location):
        return True

    def checkItem(self, curLocs, item, items, itemLocations, locationPool):
        # 
        #
        # item: dict of the item to check
        # items: list of items already placed
        # itemLocations: list of dict with the current association of (item - location)
        # locationPool: list of the 100 locations
        #
        # return bool
        oldLocations = curLocs
        canPlaceIt = self.canPlaceItem(item, oldLocations)
        if canPlaceIt is False:
            return False

        newLocations = self.currentLocations([item] + items)
        return len(newLocations) > len(oldLocations)

    def filterCurLocations(self, item, curLocations):
        return List.filter(lambda l: self.canPlaceAtLocation(item, l), curLocations)

    def shuffleLocations(self):
        shuffledLocations = self.unusedLocations[:]
        random.shuffle(shuffledLocations)
        return shuffledLocations
