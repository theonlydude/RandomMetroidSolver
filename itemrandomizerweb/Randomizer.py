import sys, random
import Items
from stdlib import Map, Array, List, Random

class RandoSettings(object):
    # maxDiff : max diff
    # progSpeed : Slowest, Slow, Medium, Fast, Fastest
    # qty : dictionary telling how many tanks and ammo will be distributed. keys are:
    #       'missile', 'super', 'powerBomb' : relative weight of ammo distribution (ex:3/3/1)
    #       'energy' : can be 'sparse' (5 tanks), 'medium' (11 tanks), 'vanilla' (14 Etanks, 4 reserves)
    #       'minors' : percentage of ammo to distribute. 100 being vanilla
    # restrictions : item placement restrictions dict. values are booleans. keys :
    #                'Suits' : no suits early game
    #                'SpeedScrew' : no speed or screw in the very first rooms
    #                'MajorMinor' : if true, will put major items in major locations, and minor items
    #                               in minor locations
    # spreadProg : if true, will spread progrssion items
    # sampleSize : possible items sample size between 1 and 100. Has to be > 1 for choose dict to be relevant.
    def __init__(self, maxDiff, progSpeed, qty, restrictions, spreadProg, sampleSize):
        self.maxDiff = maxDiff
        self.qty = qty
        self.restrictions = restrictions
        self.isSpreadProgression = spreadProg
        self.sampleSize = sampleSize
        self.choose = {
            'Locations' : {
                'Random' : 1,
                'MinDiff' : 0,
                'MaxDiff' : 0
            },
            'Items' : self.getChooseItemDict(progSpeed)
        }
        self.progressionItemTypes = self.getProgressionItemTypes(progSpeed)
        self.itemLimit = self.getItemLimit(progSpeed)

    def getChooseItemDict(self, progSpeed):
        if progSpeed == 'slowest':
            return {
                'MinProgression' : 5,
                'Random' : 5,
                'MaxProgression' : 0
            }
        if progSpeed == 'slow':
            return {
                'MinProgression' : 2,
                'Random' : 8,
                'MaxProgression' : 0
            }
        if progSpeed == 'medium':
            return {
                'MinProgression' : 0,
                'Random' : 1,
                'MaxProgression' : 0
            }
        if progSpeed == 'fast':
            return {
                'MinProgression' : 0,
                'Random' : 8,
                'MaxProgression' : 2
            }
        if progSpeed == 'fastest':
            return {
                'MinProgression' : 0,
                'Random' : 5,
                'MaxProgression' : 5
            }            
        return None

    def getProgressionItemTypes(self, progSpeed):
        progTypes = [item['Type'] for item in Items.Items if item['Category'] == 'Progression']
        progTypes.append('Charge')
        if progSpeed == 'slowest':
            return progTypes
        else:
            progTypes.remove('HiJump')
            progTypes.remove('Charge')
            progTypes.remove('Bomb')
        if progSpeed == 'slow':
            return progTypes
        else:
            progTypes.remove('Grapple')
            progTypes.remove('Ice')
        if progSpeed == 'medium':
            return progTypes
        else:
            progTypes.remove('SpaceJump')
        if progSpeed == 'fast':
            return progTypes
        else:
            progTypes.remove('SpeedBooster')
        return progTypes # only morph, varia, gravity

    def getItemLimit(self, progSpeed):
        itemLimit = 100
        if progSpeed == 'medium':
            itemLimit = 25
        elif progSpeed == 'fast':
            itemLimit = 10
        elif progSpeed == 'fastest':
            itemLimit = 1
        return itemLimit
        
class Randomizer(object):
    # seed : rand seed
    # locations : items locations
    # settings : RandoSettings instance
    def __init__(self, seed, locations, settings):
        random.seed(seed)

        # we assume that 'choose' dict is perfectly formed, that is all keys
        # below are defined in the appropriate weight dicts
        self.isSpreadProgression = settings.isSpreadProgression
        self.choose = settings.choose
        self.chooseItemFuncs = {
            'Random' : self.chooseItemRandom,
            'MinProgression' : self.chooseItemMinProgression,
            'MaxProgression' : self.chooseItemMaxProgression
        }
        self.chooseItemRanges = self.getRangeDict(settings.choose['Items'])
        self.chooseLocFuncs = {
            'Random' : self.chooseLocationRandom,
            'MinDiff' : self.chooseLocationMinDiff,
            'MaxDiff' : self.chooseLocationMaxDiff
        }
        self.chooseLocRanges = self.getRangeDict(settings.choose['Locations'])
        self.restrictions = settings.restrictions
        self.itemPool = Items.getItemPool(settings.qty)
        self.difficultyTarget = settings.maxDiff
        self.sampleSize = settings.sampleSize
        self.itemLimit = settings.itemLimit
        self.unusedLocations = locations
        self.usedLocations = []
        self.progressionLocs = []
        self.progressionItemTypes = settings.progressionItemTypes

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

    def possibleItems(self, curLocs, items, itemPool):
        # loop on all the items in the item pool of not already place items and return those that can be 
        #
        # items: list of items already placed
        # itemLocations: list of dict with the current association of (item - location)
        # itemPool: list of the items not already placed
        #
        # return list of items eligible for next placement
        result = []
        random.shuffle(itemPool)
        for item in itemPool:
            if self.checkItem(curLocs, item, items):
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

    # from a relative weight dictionary, gives a normalized range dictionary
    # example :
    # { 'a' : 10, 'b' : 17, 'c' : 3 } => {'c': 0.1, 'a':0.4333333, 'b':1 }
    def getRangeDict(self, weightDict):
        total = float(sum(weightDict.values()))
        rangeDict = {}
        current = 0.0
        for k in sorted(weightDict, key=weightDict.get):
            w = float(weightDict[k]) / total
            current += w
            rangeDict[k] = current
            
        return rangeDict

    def getChooseFunc(self, rangeDict, funcDict):
        r = random.random()
        for v in sorted(rangeDict, key=rangeDict.get):
            f = funcDict[v]
            if r < rangeDict[v]:
                return f
        return f
    
    def chooseItemRandom(self, items):
        return items[random.randint(0, len(items)-1)]
    
    def chooseItemMinProgression(self, items):
        minNewLocs = 1000
        ret = None
        
        for item in items:
            if item in self.failItems:
                continue
            newLocs = len(self.currentLocations(self.currentItems + [item]))
            if newLocs < minNewLocs:
                minNewLocs = newLocs
                ret = item
        return ret

    def chooseItemMaxProgression(self, items):
        maxNewLocs = 0
        ret = None
        
        for item in items:
            if item in self.failItems:
                continue
            newLocs = len(self.currentLocations(self.currentItems + [item]))
            if newLocs > maxNewLocs:
                maxNewLocs = newLocs
                ret = item
        return ret 
    
    def chooseItem(self, items):
        random.shuffle(items)
        item = self.getChooseFunc(self.chooseItemRanges, self.chooseItemFuncs)(items)
        if item is None:
            item = self.chooseItemRandom(items)
        return item
        
    def chooseLocationRandom(self, availableLocations, item):
        return availableLocations[random.randint(0, len(availableLocations)-1)]

    def chooseLocationMaxDiff(self, availableLocations, item):
        return max(availableLocations, key=lambda loc:loc['Available'](self.currentItems).difficulty)

    def chooseLocationMinDiff(self, availableLocations, item):
        return min(availableLocations, key=lambda loc:loc['Available'](self.currentItems).difficulty)

    # gives a general "distance" of a particular location compared to other locations
    def areaDistance(self, loc, otherLocs):
        areas = [l['Area'] for l in otherLocs]
        cnt = areas.count(loc['Area'])
        d = None
        if cnt == 0:
            d = 2
        else:
            d = 1.0/cnt
        return d
    
    def getLocsSpreadProgression(self, availableLocations):
        distances = [self.areaDistance(loc, self.progressionLocs) for loc in availableLocations]
        maxDist = max(distances)
        indices = [index for index, d in enumerate(distances) if d == maxDist]        
        locs = [availableLocations[i] for i in indices]

        return locs

    def isProgItem(self, item):
        return item['Type'] in self.progressionItemTypes
    
    def chooseLocation(self, availableLocations, item):
        locs = availableLocations
        if self.isSpreadProgression is True and self.isProgItem(item):
            locs = self.getLocsSpreadProgression(availableLocations)
        random.shuffle(locs)
        return self.getChooseFunc(self.chooseLocRanges, self.chooseLocFuncs)(locs, item)
    
    def getItemToPlace(self, items, itemPool):        
        itemsLen = len(items)
        if itemsLen == 0:
#            print("EMPTY")
            item = List.item(random.randint(0, len(itemPool)-1), itemPool)
        else:
            item = self.chooseItem(items)
        return item

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
        location = self.chooseLocation(availableLocations, item)
        if self.isProgItem(item):
#            print("placing " + item['Type'])
            self.progressionLocs.append(location)
        
        self.usedLocations += [location]
        i=0
        for loc in self.unusedLocations:
            if loc == location:
                self.unusedLocations = self.unusedLocations[0:i] + self.unusedLocations[i+1:]
            i+=1

        if 'Pickup' in location:
            location['Pickup']()
            
        return {'Item': item, 'Location': location}

    def checkItem(self, curLocs, item, items):
        # get the list of unused locations accessible with the given items (old),
        # the list of unused locations accessible with the given items and the new item (new).
        # check that there's a major location in the new list for next iteration of placement.
        # check that there's more 
        #
        # item: dict of the item to check
        # items: list of items already placed
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
        if self.restrictions['MajorMinor'] is True:        
            matchingClass = (location["Class"] == item["Class"])
            if matchingClass is False:
                return False

        def isInBlueBrinstar(loc):
            return location["Name"] in ["Morphing Ball",
                                        "Missile (blue Brinstar middle)",
                                        "Energy Tank, Brinstar Ceiling",
                                        "Power Bomb (blue Brinstar)",
                                        "Missile (blue Brinstar bottom)",
                                        "Missile (blue Brinstar top)",
                                        "Missile (blue Brinstar behind missile)"]
            
        if self.restrictions['Suits'] is True:
            if item["Type"] == "Gravity":
                return ((not (location["Area"] == "Crateria" or location["Area"] == "Brinstar"))
                        or location["Name"] == "X-Ray Scope" or location["Name"] == "Energy Tank, Waterway")
            elif item["Type"] == "Varia":
                return not (location["Area"] == "Crateria" or isInBlueBrinstar(location))
        if self.restrictions['SpeedScrew'] is True:
            if item["Type"] == "SpeedBooster":
                return not isInBlueBrinstar(location)
            if item["Type"] == "ScrewAttack":
                return not (isInBlueBrinstar(location) or location["Area"] == "Crateria") # screw attack this early is a bit too easy. plus, with MinProgression setting, ScrewAttack always ends up at Bomb

        return True

    def getItem(self, itemLocation, itemLocations):
        sys.stdout.write('.')
        sys.stdout.flush()
        self.currentItems.append(itemLocation['Item'])
        itemLocations.append(itemLocation)
 #       print(str(len(self.currentItems)) + ':' + itemLocation['Item']['Type'] + ' at ' + itemLocation['Location']['Name'])
        self.itemPool = self.removeItem(itemLocation['Item']['Type'], self.itemPool)

    def generateItem(self, curLocs, pool):
        itemLocation = None
        while itemLocation is None:
            posItems = self.possibleItems(curLocs, self.currentItems, pool)
            #                print(str(len(posItems)) + " possible items")
            itemLocation = self.placeItem(posItems, pool, curLocs)
            if len(self.failItems) >= len(posItems):
                break
            if itemLocation is None:
                return None
        return itemLocation

    def cancelLastItem(self, itemLocations):
        itemLoc = itemLocations.pop()
        item = itemLoc['Item']
        loc = itemLoc['Location']
        self.currentItems.pop()
        self.itemPool.append(item)
        self.usedLocations.remove(loc)
        self.unusedLocations.append(loc)
#        print("Cancelled  " + item['Type'] + " at " + loc['Name'])
        sys.stdout.write('x')
        sys.stdout.flush()
        
    def checkLocPool(self):
        if self.isSpreadProgression is False:
            return True
        nProgs = len([item for item in self.itemPool if self.isProgItem(item)])
        if nProgs == 0:
            return True
        # check that there is room left in all main areas
        room = {'Brinstar' : 0, 'Norfair' : 0, 'WreckedShip' : 0, 'LowerNorfair' : 0, 'Maridia' : 0}
        for loc in self.unusedLocations:
            majAvail = self.restrictions['MajorMinor'] is False or loc['Class'] == 'Major'
            if majAvail and loc['Area'] in room:
                room[loc['Area']] += 1
        for r in room.values():
            if r > 0 and r <= 2:
                sys.stdout.write('|')
                sys.stdout.flush()
                return False
        return True
        
    
    def generateItems(self):
        itemLocations = []
        self.currentItems = []
        nLoops = 0
        while len(self.itemPool) > 0:
            # 1. fill up with non-progression stuff
            pool = [item for item in self.itemPool if not self.isProgItem(item)]
            poolWasEmpty = len(pool) == 0
            itemLocation = None
            nItems = 0
            locPoolOk = True
#            print("NON-PROG")
            while len(pool) > 0 and nItems < self.itemLimit and locPoolOk: 
#                print(str(len(pool)) + " " + str(len(self.itemPool)))
                curLocs = self.currentLocations(self.currentItems)
                self.failItems = []
                itemLocation = self.generateItem(curLocs, pool)
                if itemLocation is None:
                    break
                else:
                    nItems += 1
                    self.getItem(itemLocation, itemLocations)
                    pool = self.removeItem(itemLocation['Item']['Type'], pool)
                locPoolOk = self.checkLocPool()
            isStuck = not poolWasEmpty and itemLocation is None
            if len(self.itemPool) > 0:
                # 2. collect with standard pool
#                print("REGULAR")
                removed = True
                itemLocation = None
                self.failItems = []
                if not isStuck:
#                    print("PRECANCEL")
                    curLocs = self.currentLocations(self.currentItems)
                    itemLocation = self.generateItem(curLocs, self.itemPool)                    
                    isStuck = itemLocation is None
                while itemLocation is None and (removed is True or not isStuck):
                    # if we were stuck, cancel a bunch of our last decisions
                    curLocs = self.currentLocations(self.currentItems)
                    removed = False
                    doRemove = True
                    maxCancel = 3 # assume we can't get stuck by a combination of more than 3 items...
                    nCancel = 0
                    while isStuck and len(itemLocations) > 0 and doRemove and nCancel <= maxCancel:
                        self.cancelLastItem(itemLocations)
                        nCancel += 1
                        removed = True
                        # we can continue to cancel decisions if we don't regress
                        nextCur = self.currentLocations(self.currentItems[:-1])
                        doRemove = len(curLocs) == len(nextCur) or len(curLocs) == len(nextCur) - 1
                        if doRemove:
                            curLocs = nextCur
                    # proceed like normal
                    curLocs = self.currentLocations(self.currentItems)
                    itemLocation = self.generateItem(curLocs, self.itemPool)
                    if not isStuck and itemLocation is None:
                        # we weren't stuck before but we are now...cancel last item to survive this corner case
                        self.cancelLastItem(itemLocations)
                        
                if itemLocation is None: # actually stuck
                    print("STUCK !")
                    print("REM LOCS = "  + str([loc['Name'] for loc in self.unusedLocations]))
                    print("REM ITEMS = "  + str([item['Type'] for item in self.itemPool]))
                    return None
                self.getItem(itemLocation, itemLocations)
            nLoops += 1
            if nLoops > 500: # this is coming out of my ass
                print("")
                print(str(nLoops) + " LOOPS...TOO MUCH")
                print("REM LOCS = "  + str([loc['Name'] for loc in self.unusedLocations]))
                print("REM ITEMS = "  + str([item['Type'] for item in self.itemPool]))
                return None
        print("")

        return itemLocations

# IDEES :
# - changer les choose en parametres generaux Min/Max progression/difficulty
# * si max diff : impact sur le choix de l'item => prendre l'item qui diminue
# le moins la difficulte totale (ou max?) des currentLocations obtenues avec
# cet item.
# pb de la rigidite du choix : failItems devrait suffire

# chooseLocation :
# Placer en min/max diff n'a pas l'air d'avoir d'interet car ce n'est pas rempli dans
# l'ordre de toutes facons...

# protection tournoi/race :
# avoir un log public sur le site des dernieres seeds solvees avec nom de fichier+md5+preset.
