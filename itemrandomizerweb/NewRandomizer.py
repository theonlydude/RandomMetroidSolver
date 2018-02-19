from itemrandomizerweb.stdlib import Map, Array, List, Random
from itemrandomizerweb import Items
import random

# https://github.com/tewtal/itemrandomizerweb/blob/master/ItemRandomizer/Randomizers.fs

global space
space = 0
class NewRandomizer:
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

    def currentLocations(self, items):
        # loop on all the location pool and check if the loc is not already used and if the available function is true
        # 
        # items: list of items, each item is a dict
        # itemLocations: list of dict with the current association of (item - location)
        # locationPool: list of the 100 locations
        #
        # return: list of locations
        global space
        space += 1

        # keep only the item type, it's too slow otherwise
        items = [item["Type"] for item in items]

        cur = List.filter(lambda loc: loc["Available"](items)[0], self.unusedLocations)
        #notCur = List.filter(lambda loc: not loc["Available"](items)[0], self.unusedLocations)
        #used = self.usedLocations

        #print#" "*space + "currentLocations len(cur)={} len(notCur)={} len(used)={}".format(len(cur), len(notCur), len(used)))
        ##print#" "*space + "currentLocations notCur={}".format([loc['Name'] for loc in notCur]))

        space -= 1
        return cur

    def canPlaceAtLocation(self, item, location):
        # check item class and location class, then for special items restrict some locations/areas
        #
        # item: dict of an item
        # location: dict of a location
        global space
        space += 1

        matchingClass = (location["Class"] == item["Class"])
        if matchingClass is False:
            #print#" "*space + "canPlaceAtLocation {} at {}: {}".format(item['Type'], location['Name'], False))
            space -= 1
            return False

        if item["Type"] == "Gravity":
            result = ((not (location["Area"] == "Crateria" or location["Area"] == "Brinstar"))
                      or location["Name"] == "X-Ray Scope" or location["Name"] == "Energy Tank, Waterway")
        elif item["Type"] == "Varia":
            result = (not (location["Area"] == "LowerNorfair"
                           or location["Area"] == "Crateria"
                           or location["Name"] == "Morphing Ball"
                           or location["Name"] == "Missile (blue Brinstar middle)"
                           or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        elif item["Type"] == "SpeedBooster":
            result = (not (location["Name"] == "Morphing Ball"
                           or location["Name"] == "Missile (blue Brinstar middle)"
                           or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        elif item["Type"] == "ScrewAttack":
            result = (not (location["Name"] == "Morphing Ball"
                           or location["Name"] == "Missile (blue Brinstar middle)"
                           or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        else:
            result = True

        #print#" "*space + "canPlaceAtLocation {} at {}: {}".format(item['Type'], location['Name'], result))
        space -= 1
        return result

    def canPlaceItem(self, item, itemLocations):
        # for an item check if a least one location can accept it, without checking
        # the available functions
        #
        # item: dict of an item
        # itemLocations: list of locations
        #
        # return bool
        global space
        space += 1

        result = List.exists(lambda loc: self.canPlaceAtLocation(item, loc), itemLocations)
        #print#" "*space + "canPlaceItem {}: {}".format(item['Type'], result))
        space -= 1
        return result

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
        global space
        space += 1

        oldLocations = curLocs
        canPlaceIt = self.canPlaceItem(item, oldLocations)
        if canPlaceIt is False:
            return False

        newLocations = self.currentLocations([item] + items)
        newLocationsHasMajor = List.exists(lambda l: l["Class"] == 'Major', newLocations)

        result = (canPlaceIt
                  and newLocationsHasMajor
                  and len(newLocations) > len(oldLocations))
        #print#" "*space + "checkItem {}: can {} hasMajor {} (new {} > old {}): {}".format(item['Type'], canPlaceIt,
        #                                                                      newLocationsHasMajor,
        #                                                                      len(newLocations),
        #                                                                      len(oldLocations),
        #                                                                      result))
        space -= 1
        return result

    def possibleItems(self, curLocs, items, itemLocations, itemPool, locationPool):
        # loop on all the items in the item pool of not already place items and return those that can be 
        #
        # items: list of items already placed
        # itemLocations: list of dict with the current association of (item - location)
        # itemPool: list of the items not already placed
        # locationPool: list of the 100 locations
        #
        # return list of items eligible for next placement
        global space
        space += 1

        result = []
        random.shuffle(itemPool)
        for item in itemPool:
            if self.checkItem(curLocs, item, items, itemLocations, locationPool):
                result = [item]
                break
        #result = List.filter(lambda item: self.checkItem(curLocs, item, items, itemLocations, locationPool), itemPool)
        #print#" "*space + "possibleItems len eligible items {}".format(len(result)))
        space -= 1
        return result

    def removeItem(self, itemType, itemPool):
        # recursive loop on the item pool to remove the first occurence of the item
        #
        # itemType: the name of the item to remove
        # itemPool: the items not already placed
        #
        # return the itemPool without one itemType
        global space
        space += 1
        #print#" "*space + "removeItem {}".format(itemType))
        space -= 1

        i=0
        for item in itemPool:
            if item['Type'] == itemType:
                return itemPool[0:i] + itemPool[i+1:]
            i+=1

        return itemPool

    #    if len(itemPool) == 0:
    #        return itemPool
    #    else:
    #        head = itemPool[0]
    #        tail = itemPool[1:]
    #        if head["Type"] == itemType:
    #            return tail
    #        else:
    #            return [head] + removeItem(itemType, tail)

    def placeItem(self, items, itemPool, locations):
        # 
        #
        # items: possible items to place
        # itemPool: 
        # locations: locations available
        #
        # returns a dict with the item and the location
        global space
        space += 1

        #print#" "*space + "")
        #print#" "*space + "placeItem: items {}".format([item['Type'] for item in items]))
        #print#" "*space + "placeItem: itemPool {}".format([item['Type'] for item in itemPool]))
        #print#" "*space + "placeItem: locations {}".format([loc['Name'] for loc in locations]))

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
        #print#" "*space + "placeItem: {} in {}".format(item['Type'], [loc['Name'] for loc in availableLocations]))
        location = List.item(random.randint(0, len(availableLocations)-1), availableLocations)
        #print#" "*space + "placeItem: {} at {}".format(item['Type'], location['Name']))

        space -= 1

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
        global space
        space += 1

        #print#" "*space + "placeSpecificItemAtLocation::item={} location={} ({})".format(item['Type'], location['Name'], location['Area']))
        space -= 1

        self.usedLocations += [location]
        i=0
        for loc in self.unusedLocations:
            if loc == location:
                self.unusedLocations = self.unusedLocations[0:i] + self.unusedLocations[i+1:]
            i+=1

        if 'Pickup' in location:
            location['Pickup']()

        return {'Item': item, 'Location': location}

    def getEmptyLocations(self, itemLocations, locationPool):
        # loop on all the 100 locations in the location pool, and for each loop on
        # all locations already assigned in itemsLocations to see if the loc is in it
        #
        # itemLocations: list of dict of {item, location} of the already assigned items-locations
        # locationPool: the shuffled majors
        #
        # return a list of the empty locations
        global space
        space += 1

        ##print#" "*space + "getEmptyLocations itemLocations {} locationPool {}".format(len(itemLocations), len(locationPool)))
        #result = List.filter(lambda l: self.unusedLocation(l, itemLocations), locationPool)
        ##print#" "*space + "getEmptyLocations result: {}".format([loc['Name'] for loc in result]))
        space -= 1
        #return result
        return self.unusedLocations

    #    let getAssumedItems item prefilledItems itemLocations itemPool = 
    #        let items = removeItem item.Type itemPool
    #        let items = List.append items prefilledItems
    #        let accessibleItems = List.map (fun i -> i.Item) (List.filter (fun il -> (il.Location.Available items) && (not (List.exists (fun k -> k.Type = il.Item.Type) prefilledItems))) itemLocations)
    #        List.append items accessibleItems

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
        global space
        space += 1

        #print#" "*space + "getAssumedItems item {}".format(item['Type']))
        #print#" "*space + "getAssumedItems prefilledItems {}".format([it['Type'] for it in prefilledItems]))
        #print#" "*space + "getAssumedItems itemLocations {}".format([(il['Item']['Type'], il['Location']['Name']) for il in itemLocations]))
        #print#" "*space + "getAssumedItems itemPool {}".format([it['Type'] for it in itemPool]))

        # remove the item from the pool
        items = self.removeItem(item["Type"], itemPool)
        # add the item pool without the removed item and the prefilled items already set before generateAssumedItems
        items = List.append(items, prefilledItems)
        # keep only the type of the items (for our Available functions)
        items = [item["Type"] for item in items]
        #print#" "*space + "getAssumedItems items {}".format(items))

        # filter the items-locations already associated, keep only the ones accessible
        # with the items and the item of the itemlocation is not in the prefilled items

        # get the already associated locations/items accessible without the new item but with the items in the pool and the prefilled items
        # but not the locations where the prefilled items have been placed
        # => locations with progression items accessible with all the progression items and the preffiled items but not the current item
        filteredItemLocations = List.filter(lambda itLoc: (not List.exists(lambda preIt: preIt["Type"] == itLoc["Item"]["Type"], prefilledItems)
                                                           and itLoc["Location"]["Available"](items)[0]),
                                            itemLocations)
        #print#" "*space + "getAssumedItems filtered itemLoc {}".format([(il['Item']['Type'], il['Location']['Name']) for il in filteredItemLocations]))

        # progression items accessibles without the current item
        accessibleItems = List.map(lambda i: i["Item"]['Type'], filteredItemLocations)
        #print#" "*space + "getAssumedItems accessibleItems {}".format(accessibleItems))
        result = List.append(items, accessibleItems)
        #print#" "*space + "getAssumedItems result {}".format(result))
        space -= 1
        return result

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
        global space
        space += 1

        if len(itemPool) == 0:
            #print#" "*space + "generateAssumedItems:item pool is empty")
            #print#" "*space + "generateAssumedItems items={}".format([item['Type'] for item in items]))
            #print#" "*space + "generateAssumedItems itemLocations={}".format([(il['Item']['Type'], il['Location']['Name']) for il in itemLocations]))
            #print#" "*space + "generateAssumedItems itemPool={}".format(itemPool))
            space -= 1
            return (items, itemLocations, itemPool)
        else:
            # get next progression item from item pool
            item = itemPool[0]
            # get list of item types, the already placed items - current item + the item pool filtered to keep only items
            # at locations with progression items accessible with all the progression
            # items and the preffiled items but not the current item
            assumedItems = self.getAssumedItems(item, prefilledItems, itemLocations, itemPool)
            # get empty locations
            #emptyLocations = self.getEmptyLocations(itemLocations, locationPool)
            emptyLocations = self.unusedLocations

            # get first available location
            for loc in emptyLocations:
                if 'PostAvailable' in loc:
                    if (loc["Available"](assumedItems)[0] and 
                        loc['PostAvailable'](assumedItems + [item['Type']])[0] and
                        self.canPlaceAtLocation(item, loc)):
                        fillLocation = loc
                        break
                else:
                    if loc["Available"](assumedItems)[0] and self.canPlaceAtLocation(item, loc):
                        fillLocation = loc
                        break

            #print#" "*space + "generateAssumedItems::item={} location={} ({})".format(item['Type'], fillLocation['Name'], fillLocation['Area']))
            itemLocation = self.placeSpecificItemAtLocation(item, fillLocation)
            space -= 1
            return self.generateAssumedItems(prefilledItems,
                                             [itemLocation["Item"]] + items,
                                             [itemLocation] + itemLocations,
                                             self.removeItem(itemLocation["Item"]["Type"], itemPool),
                                             locationPool)

    def generateMoreItems(self, items, itemLocations, itemPool, locationPool):
        global space
        space += 1

        if len(itemPool) == 0:
            space -= 1
            return itemLocations

        #print#" "*space + "")

        curLocs = self.currentLocations(items)
        posItems = self.possibleItems(curLocs, items, itemLocations, itemPool, locationPool)

        #print#" "*space + "generateMoreItems len(itLocs)={}".format(len(itemLocations)))
        #print#" "*space + "generateMoreItems posItems({})={}".format(len(posItems), [i['Type'] for i in posItems]))
        #print#" "*space + "generateMoreItems curLocs({})={}".format(len(curLocs), [l['Name'] for l in curLocs]))

        itemLocation = self.placeItem(posItems, itemPool, curLocs)
        space -= 1
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
        global space
        space += 1

        if len(locationPool) == 0:
            # TODO::Map.toList has already sorted by the keys
            #print#" "*space + "getWeightedLocations: {}".format([(w_l[0], w_l[1]['Name']) for w_l in Map.toList(locations)]))
            return List.map(lambda k_v: k_v[1], List.sortBy(lambda k_v: k_v[0], Map.toList(locations)))

        loc = locationPool[0]
        tail = locationPool[1:]

        weigths = {'Brinstar': 0, 'Crateria': 0, 'LowerNorfair': 11, 'Maridia': 0, 'Norfair': 0, 'WreckedShip': 12}

        weigth = num - weigths[loc['Area']]
        locations[weigth] = loc
        space -= 1
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
        global space
        space += 1

        # get the dict of the item to place
        item = List.find(lambda i: i["Type"] == itemType, Items.Items)

        # get the locs not already used and accessible with the given items
        curLocations = self.currentLocations(items)

        # filter out the cur locs depending on the item to place
        cl = List.filter(lambda l: l["Class"] == item["Class"] and self.canPlaceAtLocation(item, l), curLocations)

        # place item at a random location among the avaible ones
        itemLocation = self.placeSpecificItemAtLocation(item, List.item(random.randint(0, len(cl)-1), cl))

        items = [itemLocation["Item"]] + items
        itemPool = self.removeItem(itemLocation["Item"]["Type"], itemPool)
        itemLocations = [itemLocation] + itemLocations
        #print#" "*space + "prefill set {} at {}".format(itemType, itemLocation['Location']['Name']))
        space -= 1
        return (items, itemLocations, itemPool)

    def generateItems(self, items, itemLocations):
        # main function
        #
        # items: empty list
        # itemLocations: empty list
        #
        # return 

        newItems = items
        newItemLocations = itemLocations
        newItemPool = self.itemPool

        # Place Morph at one of the earliest locations so that it's always accessible
        (newItems, newItemLocations, newItemPool) = self.prefill("Morph", newItems, newItemLocations, newItemPool, self.locationPool)
        #print#" "*space + "generateItems::morph::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

        # Place either a super or a missile to open up BT's location 
        if random.randint(0, 1) == 0:
            (newItems, newItemLocations, newItemPool) = self.prefill("Missile", newItems, newItemLocations, newItemPool, self.locationPool)
        else:
            (newItems, newItemLocations, newItemPool) = self.prefill("Super", newItems, newItemLocations, newItemPool, self.locationPool)
        #print#" "*space + "generateItems::missile::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

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
        #print#" "*space + "generateItems::break bomb block::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

        # Place a super if it's not already placed
        if not List.exists(lambda i: i["Type"] == "Super", newItems):
            (newItems, newItemLocations, newItemPool) = self.prefill("Super", newItems, newItemLocations, newItemPool, self.locationPool)
            #print#" "*space + "generateItems::super::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

        # Save the prefilled items into a new list to be used later
        prefilledItems = newItems

        # Shuffle the major locations randomly, then adjust the order slightly based on weighting per area
        shuffledLocations = List.toArray(List.filter(lambda l: l["Class"] == "Major", self.locationPool))
        random.shuffle(shuffledLocations)
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
        #print#" "*space + "generateItems progressItems {}".format([it['Type'] for it in progressItems]))
        #print#" "*space + "generateItems progressItemLocations {}".format([(il['Item']['Type'], il['Location']['Name']) for il in progressItemLocations]))
        #print#" "*space + "generateItems progressItemPool {}".format([it['Type'] for it in progressItemPool]))

        # All progression items are placed and every other location in the game should now be accessible
        # so place the rest of the items randomly using the regular placement method
        return self.generateMoreItems(progressItems, progressItemLocations, otherItemsPool, self.locationPool)
