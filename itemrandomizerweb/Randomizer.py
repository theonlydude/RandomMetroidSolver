import random
import Items
from stdlib import Map, Array, List, Random

class Randomizer(object):
    @staticmethod
    def factory(algo, seed, difficultyTarget, locations):
        if algo == 'Total_Tournament':
            from NewRandomizer import NewRandomizer
            return NewRandomizer(seed, difficultyTarget, locations)
        elif algo == 'Total_Full':
            from FullRandomizer import FullRandomizer
            return FullRandomizer(seed, difficultyTarget, locations)
        elif algo == 'Total_Casual' or algo == 'Total_Normal':
            from DefaultRandomizer import DefaultRandomizer
            return DefaultRandomizer(seed, difficultyTarget, locations)
        elif algo == 'Total_Hard':
            from SparseRandomizer import SparseRandomizer
            return SparseRandomizer(seed, difficultyTarget, locations)
        else:
            print("ERROR: unknown algo: {}".format(algo))
            return None

    def __init__(self, seed, difficultyTarget, locations):
        self.rnd = Random(seed)
        random.seed(seed)

        self.itemPool = Items.getItemPool(self.rnd)
        self.difficultyTarget = difficultyTarget
        self.locationPool = locations

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
        result = loc["PostAvailable"](items)
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

        return List.filter(lambda loc: self.locAvailable(loc, items), self.unusedLocations)

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
                result = [item]
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
            if List.exists(lambda i: i["Type"] == "ScrewAttack", itemPool):
                item = List.find(lambda i: i["Type"] == "ScrewAttack", itemPool)
            elif List.exists(lambda i: i["Type"] == "SpeedBooster", itemPool):
                item = List.find(lambda i: i["Type"] == "SpeedBooster", itemPool)
            else:
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

    def placeSpecificItemAtLocation(self, item, location):
        # returns a dict with the item and the location
        #
        # item: the item to place
        # location: the location where the item is placed
        #
        # returns a dict with the item and the location
        self.usedLocations += [location]
        i=0
        for loc in self.unusedLocations:
            if loc == location:
                self.unusedLocations = self.unusedLocations[0:i] + self.unusedLocations[i+1:]
            i+=1

        if 'Pickup' in location:
            location['Pickup']()

        return {'Item': item, 'Location': location}

    def getAssumedItems(self, item, prefilledItems, itemLocations, itemPool):
        # returns items, the prefilled items, minus the current item, plus the items in itemPool filtered
        # to keep only items at locations with progression items accessible with all the progression
        # items and the preffiled items but not the current item
        #
        # item: dict of an item
        # prefilledItems: list of dict of items, the items already placed
        # itemLocations: list of dict item-location already associated
        # itemPool: list of dict of items, the items available for placement (progression items)
        #
        # returns a list of item types

        # remove the item from the pool
        items = self.removeItem(item["Type"], itemPool)
        # add the item pool without the removed item and the prefilled items already set before generateAssumedItems
        items = List.append(items, prefilledItems)
        # keep only the type of the items (for our Available functions)
        items = [item["Type"] for item in items]

        # filter the items-locations already associated, keep only the ones accessible
        # with the items and the item of the itemlocation is not in the prefilled items

        # get the already associated locations/items accessible without the new item but with the items in the pool and the prefilled items
        # but not the locations where the prefilled items have been placed
        # => locations with progression items accessible with all the progression items and the preffiled items but not the current item
        filteredItemLocations = List.filter(lambda itLoc: (not List.exists(lambda preIt: preIt["Type"] == itLoc["Item"]["Type"], prefilledItems)
                                                           and self.locAvailable(itLoc["Location"], items)),
                                            itemLocations)

        # progression items accessibles without the current item
        accessibleItems = List.map(lambda i: i["Item"]['Type'], filteredItemLocations)

        return List.append(items, accessibleItems)

    def generateAssumedItems(self, prefilledItems, items, itemLocations, itemPool, locationPool):
        # place the progression items
        #
        # prefilledItems: list of items already placed
        # items: list of items already placed
        # itemLocations: list of dict item-location already associated
        # itemPool: available items to place
        # locationPool: randomized majors locations
        #
        # return ()
        if len(itemPool) == 0:
            return (items, itemLocations, itemPool)
        else:
            # get next progression item from item pool
            item = itemPool[0]
            # get list of item types, the already placed items - current item + the item pool filtered to keep only items
            # at locations with progression items accessible with all the progression
            # items and the preffiled items but not the current item
            assumedItems = self.getAssumedItems(item, prefilledItems, itemLocations, itemPool)
            # get empty locations
            emptyLocations = locationPool

            # get first available location
            for loc in emptyLocations:
                if 'PostAvailable' in loc:
                    if (self.locAvailable(loc, assumedItems) and
                        self.locPostAvailable(loc, assumedItems + [item['Type']]) and
                        self.canPlaceAtLocation(item, loc)):
                        fillLocation = loc
                        break
                else:
                    if self.locAvailable(loc, assumedItems) and self.canPlaceAtLocation(item, loc):
                        fillLocation = loc
                        break

            itemLocation = self.placeSpecificItemAtLocation(item, fillLocation)

            i=0
            for loc in locationPool:
                if loc == fillLocation:
                    locationPool = locationPool[0:i] + locationPool[i+1:]
                i+=1

            return self.generateAssumedItems(prefilledItems,
                                             [itemLocation["Item"]] + items,
                                             [itemLocation] + itemLocations,
                                             self.removeItem(itemLocation["Item"]["Type"], itemPool),
                                             locationPool)

    def generateMoreItems(self, items, itemLocations, itemPool, locationPool):
        if len(itemPool) == 0:
            return itemLocations

        curLocs = self.currentLocations(items)
        posItems = self.possibleItems(curLocs, items, itemLocations, itemPool, locationPool)

        itemLocation = self.placeItem(posItems, itemPool, curLocs)
        return self.generateMoreItems([itemLocation["Item"]] + items,
                                      [itemLocation] + itemLocations,
                                      self.removeItem(itemLocation["Item"]["Type"], itemPool),
                                      locationPool)

    def getWeightedLocations(self, locationPool, num, locations):
        # take the first location in the pool, set its weight
        # then recurse on itself with locationPool minus head, num+10 and locations plus weighted head
        #
        # locationPool: all majors locations shuffled, then head is removed
        # num: 100, then num+10
        # locations: empty dict, then dict of {weigth: location}
        #
        # returns list of locations sorted by weigth
        if len(locationPool) == 0:
            # TODO::Map.toList has already sorted by the keys
            #print#" "*space + "getWeightedLocations: {}".format([(w_l[0], w_l[1]['Name']) for w_l in Map.toList(locations)]))
            return List.map(lambda k_v: k_v[1], List.sortBy(lambda k_v: k_v[0], Map.toList(locations)))

        loc = locationPool[0]
        tail = locationPool[1:]

        weigths = {'Brinstar': 0, 'Crateria': 0, 'LowerNorfair': 11, 'Maridia': 0, 'Norfair': 0, 'WreckedShip': 12}

        weigth = num - weigths[loc['Area']]
        locations[weigth] = loc
        return self.getWeightedLocations(tail, num+10, locations)

    def prefill(self, itemType, items, itemLocations, itemPool, locationPool):
        # update parameters: items, itemLocations, itemPool
        #
        # rnd: random number generator
        # itemType: the item type to place
        # items: the items already placed (list of items dicts)
        # itemLocations: the already associated items-locations
        # itemPool: available items to place (list of items dicts)
        # locationPool: list of the 100 dict locations
        #
        # returns the updated lists of:
        #  -items already placed
        #  -the already associated items-locations
        #  -available items to place (list of items dicts)

        # get the dict of the item to place
        item = List.find(lambda i: i["Type"] == itemType, Items.Items)

        # get the locs not already used and accessible with the given items
        curLocations = self.currentLocations(items)

        # filter out the cur locs depending on the item to place
        cl = self.filterCurLocations(item, curLocations)

        # place item at a random location among the avaible ones
        itemLocation = self.placeSpecificItemAtLocation(item, List.item(random.randint(0, len(cl)-1), cl))

        items = [itemLocation["Item"]] + items
        itemPool = self.removeItem(itemLocation["Item"]["Type"], itemPool)
        itemLocations = [itemLocation] + itemLocations

        return (items, itemLocations, itemPool)

    def generateItems(self):
        # main function
        #
        # items: empty list
        # itemLocations: empty list
        #
        # return 

        newItems = []
        newItemLocations = []
        newItemPool = self.itemPool

        # Place Morph at one of the earliest locations so that it's always accessible
        (newItems, newItemLocations, newItemPool) = self.prefill("Morph", newItems, newItemLocations, newItemPool, self.locationPool)

        # Place either a super or a missile to open up BT's location 
        if random.randint(0, 1) == 0:
            (newItems, newItemLocations, newItemPool) = self.prefill("Missile", newItems, newItemLocations, newItemPool, self.locationPool)
        else:
            (newItems, newItemLocations, newItemPool) = self.prefill("Super", newItems, newItemLocations, newItemPool, self.locationPool)

        # Next step is to place items that opens up access to breaking bomb blocks
        # by placing either Screw/Speed/Bomb or just a PB pack early.
        # One PB pack will be placed after filling with other items so that there's at least on accessible
        rand = random.randint(0, 12)
        if rand == 0:
            (newItems, newItemLocations, newItemPool) = self.prefill("Missile", newItems, newItemLocations, newItemPool, self.locationPool)
            (newItems, newItemLocations, newItemPool) = self.prefill("ScrewAttack", newItems, newItemLocations, newItemPool, self.locationPool)
            (newItems, newItemLocations, newItemPool) = self.prefill("PowerBomb", newItems, newItemLocations, newItemPool, self.locationPool)
        elif rand == 1:
            (newItems, newItemLocations, newItemPool) = self.prefill("Missile", newItems, newItemLocations, newItemPool, self.locationPool)
            (newItems, newItemLocations, newItemPool) = self.prefill("SpeedBooster", newItems, newItemLocations, newItemPool, self.locationPool)
            (newItems, newItemLocations, newItemPool) = self.prefill("PowerBomb", newItems, newItemLocations, newItemPool, self.locationPool)
        elif rand == 2:
            (newItems, newItemLocations, newItemPool) = self.prefill("Missile", newItems, newItemLocations, newItemPool, self.locationPool)
            (newItems, newItemLocations, newItemPool) = self.prefill("Bomb", newItems, newItemLocations, newItemPool, self.locationPool)
            (newItems, newItemLocations, newItemPool) = self.prefill("PowerBomb", newItems, newItemLocations, newItemPool, self.locationPool)
        else:
            (newItems, newItemLocations, newItemPool) = self.prefill("PowerBomb", newItems, newItemLocations, newItemPool, self.locationPool)

        # Place a super if it's not already placed
        if not List.exists(lambda i: i["Type"] == "Super", newItems):
            (newItems, newItemLocations, newItemPool) = self.prefill("Super", newItems, newItemLocations, newItemPool, self.locationPool)

        # Save the prefilled items into a new list to be used later
        prefilledItems = newItems

        # Shuffle the locations randomly, then adjust the order slightly based on weighting per area
        shuffledLocations = self.shuffleLocations()
        weightedLocations = self.getWeightedLocations(Array.toList(shuffledLocations), 100, {})

        # Shuffle the item pool
        random.shuffle(newItemPool)

        # Always start with placing a suit (this helps getting maximum spread of suit locations)
        if random.randint(0, 1) == 0:
            firstItem = List.find(lambda i: i["Type"] == "Varia", newItemPool)
        else:
            firstItem = List.find(lambda i: i["Type"] == "Gravity", newItemPool)

        newItemPool = [firstItem] + List.filter(lambda i: i["Type"] != firstItem["Type"], newItemPool)

        progressionItemsPool = List.filter(lambda i: i["Category"] == 'Progression', newItemPool)
        otherItemsPool = List.filter(lambda i: i["Category"] != 'Progression', newItemPool)

        # Place the rest of progression items randomly
        (progressItems,
         progressItemLocations,
         progressItemPool) = self.generateAssumedItems(prefilledItems, newItems, newItemLocations,
                                                       progressionItemsPool, weightedLocations)

        # All progression items are placed and every other location in the game should now be accessible
        # so place the rest of the items randomly using the regular placement method
        return self.generateMoreItems(progressItems, progressItemLocations, otherItemsPool, self.locationPool)
