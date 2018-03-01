import random
import Items
from stdlib import Map, Array, List, Random

class Randomizer(object):
    @staticmethod
    def factory(algo, seed, difficultyTarget, locations, sampleSize=1):
        if algo == 'Total_Tournament':
            from NewRandomizer import NewRandomizer
            return NewRandomizer(seed, difficultyTarget, locations)
        elif algo == 'Total_Full':
            from FullRandomizer import FullRandomizer
            return FullRandomizer(seed, difficultyTarget, locations)
        elif algo == 'Total_Casual' or algo == 'Total_Normal':
            from DefaultRandomizer import DefaultRandomizer
            return DefaultRandomizer(seed, difficultyTarget, locations, sampleSize)
        elif algo == 'Total_Hard':
            from SparseRandomizer import SparseRandomizer
            return SparseRandomizer(seed, difficultyTarget, locations)
        else:
            print("ERROR: unknown algo: {}".format(algo))
            return None

    def __init__(self, seed, difficultyTarget, locations, sampleSize=1):
        self.rnd = Random(seed)
        random.seed(seed)

        self.itemPool = Items.getItemPool(self.rnd)
        self.difficultyTarget = difficultyTarget
        self.locationPool = locations
        self.sampleSize = sampleSize
        self.chosenLocation = None
        
        # list of locations not already used
        self.unusedLocations = locations
        # list of locations already used
        self.usedLocations = []
        # list of {'Item': item, 'Location': location}, the items assigned to a location
        self.itemLocations = []

    def locAvailable(self, loc, items):
        result = loc["Available"](items)
        return result.bool is True and result.difficulty <= self.difficultyTarget

    def locPostAvailable(self, loc, items):
        if not 'PostAvailable' in loc:
            return True
        result = loc["PostAvailable"](items)
#        print("POST " + str(result.bool))
        return result.bool is True and result.difficulty <= self.difficultyTarget

    def currentLocations(self, items):
        # loop on all the location pool and check if the loc is not already used and if the available function is true
        # 
        # items: list of items, each item is a dict
        # itemLocations: list of dict with the current association of (item - location)
        # locationPool: list of the 100 locations
        #
        # return: list of locations

        # keep only the item type, it's too slow otherwise
        items = [item["Type"] for item in items]
        avail = lambda loc: self.locAvailable(loc, items)
        
        return List.filter(avail, self.unusedLocations)

    def canPlaceItem(self, item, itemLocations):
        # for an item check if a least one location can accept it, without checking
        # the available functions
        #
        # item: dict of an item
        # itemLocations: list of locations
        #
        # return bool
        return List.exists(lambda loc: self.canPlaceAtLocation(item, loc), itemLocations)

    def possibleItems(self, curLocs, items, itemLocations, itemPool, locationPool):
        # loop on all the items in the item pool of not already place items and return those that can be 
        #
        # items: list of items already placed
        # itemLocations: list of dict with the current association of (item - location)
        # itemPool: list of the items not already placed
        # locationPool: list of the 100 locations
        #
        # return list of items eligible for next placement
        result = []
        random.shuffle(itemPool)
        for item in itemPool:
            if self.checkItem(curLocs, item, items, itemLocations, locationPool):
                result.append(item)
                if len(result) >= self.sampleSize:
                    break
        return result

    def removeItem(self, itemType, itemPool):
        # recursive loop on the item pool to remove the first occurence of the item
        #
        # itemType: the name of the item to remove
        # itemPool: the items not already placed
        #
        # return the itemPool without one itemType
        i=0
        for item in itemPool:
            if item['Type'] == itemType:
                return itemPool[0:i] + itemPool[i+1:]
            i+=1

        return itemPool

    def chooseItem(self, items):
        return items[random.randint(0, len(items)-1)]
    
    def getItemToPlace(self, items, itemPool):
        itemsLen = len(items)
        if itemsLen == 0:
            if List.exists(lambda i: i["Type"] == "ScrewAttack", itemPool):
                item = List.find(lambda i: i["Type"] == "ScrewAttack", itemPool)
            elif List.exists(lambda i: i["Type"] == "SpeedBooster", itemPool):
                item = List.find(lambda i: i["Type"] == "SpeedBooster", itemPool)
            else:
                item = List.item(random.randint(0, len(itemPool)-1), itemPool)
        else:
            item = self.chooseItem(items)

        return item

    def chooseLocation(self, availableLocations):
        return availableLocations[random.randint(0, len(availableLocations)-1)]
    
    def placeItem(self, items, itemPool, locations):
        # 
        #
        # items: possible items to place
        # itemPool: 
        # locations: locations available
        #
        # returns a dict with the item and the location
        item = self.getItemToPlace(items, itemPool)
        currentItems = [i["Type"] for i in self.currentItems]
        currentItems.append(item['Type'])
        availableLocations = List.filter(lambda loc: self.canPlaceAtLocation(item, loc) and self.locPostAvailable(loc, currentItems), locations)
        if len(availableLocations) == 0:
            self.failItems.append(item)
            return None
        location = self.chooseLocation(availableLocations)

        self.usedLocations += [location]
        i=0
        for loc in self.unusedLocations:
            if loc == location:
                self.unusedLocations = self.unusedLocations[0:i] + self.unusedLocations[i+1:]
            i+=1

        if 'Pickup' in location:
            location['Pickup']()
            
        return {'Item': item, 'Location': location}

    def checkItem(self, curLocs, item, items, itemLocations, locationPool):
        # get the list of unused locations accessible with the given items (old),
        # the list of unused locations accessible with the given items and the new item (new).
        # check that there's a major location in the new list for next iteration of placement.
        # check that there's more 
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
        newLocationsHasMajor = List.exists(lambda l: l["Class"] == 'Major', newLocations)

        return newLocationsHasMajor and len(newLocations) > len(oldLocations)
    
    def canPlaceAtLocation(self, item, location):
        # check item class and location class, then for special items restrict some locations/areas
        #
        # item: dict of an item
        # location: dict of a location

        matchingClass = (location["Class"] == item["Class"])
        if matchingClass is False:
            return False

        if item["Type"] == "Gravity":
            return ((not (location["Area"] == "Crateria" or location["Area"] == "Brinstar"))
                    or location["Name"] == "X-Ray Scope" or location["Name"] == "Energy Tank, Waterway")
        elif item["Type"] == "Varia":
            return (not (location["Area"] == "LowerNorfair"
                         or location["Area"] == "Crateria"
                         or location["Name"] == "Morphing Ball"
                         or location["Name"] == "Missile (blue Brinstar middle)"
                         or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        elif item["Type"] == "SpeedBooster":
            return (not (location["Name"] == "Morphing Ball"
                         or location["Name"] == "Missile (blue Brinstar middle)"
                         or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        elif item["Type"] == "ScrewAttack":
            return (not (location["Name"] == "Morphing Ball"
                         or location["Name"] == "Missile (blue Brinstar middle)"
                         or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        else:
            return True
