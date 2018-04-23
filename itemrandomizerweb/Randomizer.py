import sys, random
from itemrandomizerweb import Items
from parameters import Knows, Settings, mania
from itemrandomizerweb.stdlib import List
from helpers import Bosses
from graph import AccessGraph
from smboolmanager import SMBoolManager

class RandoSettings(object):
    # maxDiff : max diff
    # progSpeed : slowest, slow, medium, fast, fastest
    # qty : dictionary telling how many tanks and ammo will be distributed. keys are:
    #       'missile', 'super', 'powerBomb' : relative weight of ammo distribution (ex:3/3/1)
    #       'energy' : can be 'sparse' (5 tanks), 'medium' (11 tanks), 'vanilla' (14 Etanks, 4 reserves)
    #       'minors' : percentage of ammo to distribute. 100 being vanilla
    # restrictions : item placement restrictions dict. values are booleans. keys :
    #                'Suits' : no suits early game
    #                'SpeedScrew' : no speed or screw in the very first rooms
    #                'MajorMinor' : if true, will put major items in major locations, and minor items
    #                               in minor locations
    # spreadProg : if true, will spread progression items
    # sampleSize : possible items sample size between 1 and 100. Has to be > 1 for choose dict to be relevant.
    # superFun : super fun settings list. can contain 'Movement', 'Combat', 'Suits'. Will remove random items
    # of the relevant categorie(s). This can easily cause aborted seeds, so some basic checks will be performed
    # beforehand to know whether an item can indeed be removed.
    def __init__(self, maxDiff, progSpeed, qty, restrictions, spreadProg, sampleSize, superFun):
        self.progSpeed = progSpeed
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
        self.locLimit = self.getLocLimit(progSpeed)
        self.forbiddenItems = self.getForbiddenItems(superFun)

    def getChooseItemDict(self, progSpeed):
        if progSpeed == 'slowest':
            return {
                'MinProgression' : 1,
                'Random' : 2,
                'MaxProgression' : 0
            }
        if progSpeed == 'slow':
            return {
                'MinProgression' : 25,
                'Random' : 75,
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
                'Random' : 75,
                'MaxProgression' : 25
            }
        if progSpeed == 'fastest':
            return {
                'MinProgression' : 0,
                'Random' : 2,
                'MaxProgression' : 1
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
        if progSpeed == 'slow':
            return progTypes
        else:
            progTypes.remove('Bomb')
            progTypes.remove('Grapple')
        if progSpeed == 'medium':
            return progTypes
        else:
            progTypes.remove('Ice')
            progTypes.remove('SpaceJump')
        if progSpeed == 'fast':
            return progTypes
        else:
            progTypes.remove('SpeedBooster')
        return progTypes # only morph, varia, gravity

    def getItemLimit(self, progSpeed):
        itemLimit = 100
        if progSpeed == 'slow':
            itemLimit = 20
        elif progSpeed == 'medium':
            itemLimit = 11
        elif progSpeed == 'fast':
            itemLimit = 5
        elif progSpeed == 'fastest':
            itemLimit = 1
        return itemLimit

    def getLocLimit(self, progSpeed):
        locLimit = -1
        if progSpeed == 'slow':
            locLimit = 1
        elif progSpeed == 'medium':
            locLimit = 2
        elif progSpeed == 'fast':
            locLimit = 3
        elif progSpeed == 'fastest':
            locLimit = 4
        return locLimit

    def getForbiddenItemsFromList(self, itemList):
        remove = []
        nItems = float(len(itemList))
        n = int(round(random.gauss(nItems/2, nItems/8), 0))
        if n < 0:
            n = 0
        if n > len(itemList):
            n = len(itemList)
        for i in range(n):
            idx = random.randint(0, len(itemList) - 1)
            remove.append(itemList.pop(idx))
        return remove

    def getForbiddenSuits(self, dontRemove):
        removable = []
        # can we remove gravity?
        if Knows.SuitlessOuterMaridia.bool or Knows.SuitlessOuterMaridiaNoGuns.bool:
            if Knows.DraygonRoomCrystalFlash.bool:
                if Knows.PreciousRoomXRayExit.bool:
                    removable.append('Gravity')
                elif Knows.DraygonRoomGrappleExit.bool and not Knows.SpringBallJump.bool:
                    removable.append('Gravity')
                    dontRemove.append('Grapple')
                elif not Knows.DraygonRoomGrappleExit.bool and Knows.SpringBallJump.bool:
                    removable.append('Gravity')
                    dontRemove.append('SpringBall')
                elif Knows.DraygonRoomGrappleExit.bool and Knows.SpringBallJump.bool:
                    if random.random() < 0.5:
                        dontRemove.append('SpringBall')
                    else:
                        dontRemove.append('Grapple')
                    removable.append('Gravity')
            elif Knows.DraygonRoomGrappleExit.bool:
                if Knows.PreciousRoomXRayExit.bool:
                    removable.append('Gravity')
                    dontRemove.append('Grapple')
                elif Knows.SpringBallJump.bool:
                    removable.append('Gravity')
                    dontRemove.append('Grapple')
                    dontRemove.append('SpringBall')
        # can we remove varia?
        if Settings.hellRuns['LowerNorfair'] is not None and self.qty['energy'] != 'sparse':
            removable.append('Varia')
        return removable

    def getForbiddenMovement(self, dontRemove):
        movementItems = ['SpaceJump', 'Bomb', 'HiJump', 'SpeedBooster', 'Grapple', 'SpringBall']        
        return [item for item in movementItems if not item in dontRemove]

    def getForbiddenCombat(self):
        combatItems = ['ScrewAttack', 'Wave', 'Spazer', 'Plasma']
        return combatItems
    
    def getForbiddenItems(self, superFun):
        remove = []
        dontRemove = []
        if 'Suits' in superFun: # impact on movement item
            removableSuits = self.getForbiddenSuits(dontRemove)
            remove += self.getForbiddenItemsFromList(removableSuits)
        if 'Movement' in superFun:
            removableMovement = self.getForbiddenMovement(dontRemove)
            remove += self.getForbiddenItemsFromList(removableMovement)
        if 'Combat' in superFun:
            removableCombat = self.getForbiddenCombat()
            remove += self.getForbiddenItemsFromList(removableCombat)
        return remove
        
class Randomizer(object):
    # locations : items locations
    # settings : RandoSettings instance
    def __init__(self, locations, settings, seedName, graphTransitions=None, bidir=True):
        # we assume that 'choose' dict is perfectly formed, that is all keys
        # below are defined in the appropriate weight dicts
        if graphTransitions is not None:
            self.currentLocations = self.currentLocationsGraph
            self.areaGraph = AccessGraph(graphTransitions, bidir, seedName + ".dot")
        else:
            self.currentLocations = self.currentLocationsAvailFunc
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
        self.itemPool = Items.getItemPool(settings.qty, settings.forbiddenItems)
        self.restrictedLocations = self.getRestrictedLocations(settings.forbiddenItems, locations)
        self.difficultyTarget = settings.maxDiff
        self.sampleSize = settings.sampleSize
        self.itemLimit = settings.itemLimit
        self.unusedLocations = locations
        self.locLimit = settings.locLimit
        self.usedLocations = []
        self.progressionItemLocs = []
        self.progressionItemTypes = settings.progressionItemTypes
        self.maxCancel = 1
        self.totalCancels = 0
        self.pickedUpLocs = []
        if self.difficultyTarget > mania:
            self.smbm = SMBoolManager.factory('bool')
        else:
            self.smbm = SMBoolManager.factory('diff')

    def getRestrictedLocations(self, forbiddenItems, locations):
        # list only absolutely unreachable locations, regardless of known techniques
        # TODO more accurate filtering
        restricted = []
        if 'SpeedBooster' in forbiddenItems:
            restricted += ["Energy Tank, Waterway", "Reserve Tank, Wrecked Ship",
                           "Super Missile (Crateria)", "Missile (green Maridia shinespark)",
                           "Missile (pink Maridia)", "Super Missile (pink Maridia)"]
        if 'Gravity' in forbiddenItems:
            restricted += ["Missile (pink Maridia)", "Super Missile (pink Maridia)",
                           "Missile (green Maridia shinespark)", "Power Bomb (right Maridia sand pit room)",
                           "Spring Ball" ]
        if 'SpaceJump' in forbiddenItems:
            restricted += ["Missile (Gold Torizo)"]

        restricted = sorted(list(set(restricted)))

        # add full locations
        restrictedFull = []
        for restrictLoc in restricted:
            for loc in locations:
                if loc['Name'] == restrictLoc:
                    restrictedFull.append(loc)
        return restrictedFull
        
    def locAvailable(self, loc):
        result = self.smbm.eval(loc['Available'])
        return result.bool == True and result.difficulty <= self.difficultyTarget

    def locPostAvailable(self, loc, item):
        if not 'PostAvailable' in loc:
            return True
        result = self.smbm.eval(loc['PostAvailable'], item)
#        print("POST " + str(result.bool))
        return result.bool == True and result.difficulty <= self.difficultyTarget

    def currentLocationsAvailFunc(self, item=None):
        # loop on all the location pool and check if the loc is not already used and if the available function is true
        # 
        # items: list of items, each item is a dict
        # itemLocations: list of dict with the current association of (item - location)
        #
        # return: list of locations

        if item is not None:
            self.smbm.addItem(item['Type'])

        avail = lambda loc: self.locAvailable(loc)
        ret = List.filter(avail, self.unusedLocations)

        if item is not None:
            self.smbm.removeItem(item['Type'])

        return ret

    def currentLocationsGraph(self, items):
        items = [item["Type"] for item in items]

        return self.areaGraph.getAvailableLocations(self.unusedLocations, items, self.difficultyTarget)

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
            newLocs = len(self.currentLocations(item))
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
            newLocs = len(self.currentLocations(item))
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
        progLocs = [il['Location'] for il in self.progressionItemLocs if il['Item']['Class'] == 'Major' and il['Item']['Category'] != "Energy"]
        distances = [self.areaDistance(loc, progLocs) for loc in availableLocations]
        maxDist = max(distances)
        indices = [index for index, d in enumerate(distances) if d == maxDist]
        locs = [availableLocations[i] for i in indices]

        return locs

    def hasItemType(self, t):
        return any(item['Type'] == t for item in self.currentItems)

    def hasItemTypeInPool(self, t):
        return any(item['Type'] == t for item in self.itemPool)
    
    def isProgItem(self, item):
        if item['Type'] in self.progressionItemTypes:
            return True
        if item['Type'] in self.nonProgTypesCache:
            return False
        if item['Type'] in self.progTypesCache:
            return True
        if not item in self.currentItems:
            isProg = len(self.currentLocations()) < len(self.currentLocations(item))
            if isProg == False and item['Type'] not in self.nonProgTypesCache:
                self.nonProgTypesCache.append(item['Type'])
            elif isProg == True and item['Type'] not in self.progTypesCache:
                self.progTypesCache.append(item['Type'])
            return isProg
        return False
    
    def chooseLocation(self, availableLocations, item):
        locs = availableLocations
        if self.isSpreadProgression == True and self.isProgItem(item):
            locs = self.getLocsSpreadProgression(availableLocations)
        random.shuffle(locs)
        return self.getChooseFunc(self.chooseLocRanges, self.chooseLocFuncs)(locs, item)
    
    def getItemToPlace(self, items, itemPool):        
        itemsLen = len(items)
        if itemsLen == 0:
            fixedPool = [item for item in itemPool if item not in self.failItems]
            item = List.item(random.randint(0, len(fixedPool)-1), fixedPool)
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
        availableLocations = List.filter(lambda loc: self.canPlaceAtLocation(item, loc) and self.locPostAvailable(loc, item['Type']), locations)
        # if a loc is available we trigger pick up action, to make more locs available afterwards
        for loc in availableLocations:
            if 'Pickup' in loc and not loc in self.pickedUpLocs:
                loc['Pickup']()
                self.pickedUpLocs.append(loc)
        if len(availableLocations) == 0:
            if not item in self.failItems:
                self.failItems.append(item)
            return None
        location = self.chooseLocation(availableLocations, item)
            
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
        if canPlaceIt == False:
            return False

        newLocations = self.currentLocations(item)
        if self.restrictions["MajorMinor"] == True:
            newLocationsHasMajor = List.exists(lambda l: l["Class"] == 'Major', newLocations)
        else:
            newLocationsHasMajor = True

        return newLocationsHasMajor and len(newLocations) > len(oldLocations)
    
    def canPlaceAtLocation(self, item, location):
        # check item class and location class, then for special items restrict some locations/areas
        #
        # item: dict of an item
        # location: dict of a location
        if self.restrictions['MajorMinor'] == True:
            matchingClass = (location["Class"] == item["Class"])
            if matchingClass == False:
                return False

        isInBlueBrinstar = location["Name"] in ["Morphing Ball",
                                                "Missile (blue Brinstar middle)",
                                                "Energy Tank, Brinstar Ceiling",
                                                "Power Bomb (blue Brinstar)",
                                                "Missile (blue Brinstar bottom)",
                                                "Missile (blue Brinstar top)",
                                                "Missile (blue Brinstar behind missile)"]
        
        if self.restrictions['Suits'] == True:
            if item["Type"] == "Gravity":
                return ((not (location["Area"] == "Crateria" or location["Area"] == "Brinstar"))
                        or location["Name"] == "X-Ray Scope" or location["Name"] == "Energy Tank, Waterway")
            elif item["Type"] == "Varia":
                return not (location["Area"] == "Crateria" or isInBlueBrinstar)
        if self.restrictions['SpeedScrew'] == True:
            if item["Type"] == "SpeedBooster":
                return not isInBlueBrinstar
            if item["Type"] == "ScrewAttack":
                return not (isInBlueBrinstar or location["Area"] == "Crateria") # screw attack this early is a bit too easy. plus, with MinProgression setting, ScrewAttack always ends up at Bomb
            
        return True

    def getItem(self, itemLocation, itemLocations, collect=True):
        sys.stdout.write('.')
        sys.stdout.flush()
        item = itemLocation['Item']
        location = itemLocation['Location']
        if self.isProgItem(item):
            self.progressionItemLocs.append(itemLocation)
            if item['Category'] == 'Energy':
                # if energy made us progress we must not cancel energy we already
                # have, so add the already collected energy to progression locations
                self.progressionItemLocs += [il for il in itemLocations if il['Item']['Category'] == 'Energy' and not il in self.progressionItemLocs]
        self.usedLocations.append(location)
        self.unusedLocations.remove(location)
        if collect == True:
            self.currentItems.append(item)
            self.smbm.addItem(item['Type'])
            self.nonProgTypesCache = []
            self.progTypesCache = []
        itemLocations.append(itemLocation)
#        print(str(len(self.currentItems)) + ':' + itemLocation['Item']['Type'] + ' at ' + itemLocation['Location']['Name'])
        self.itemPool = self.removeItem(item['Type'], self.itemPool)

    def generateItem(self, curLocs, pool):
        itemLocation = None
        self.failItems = []
        posItems = self.possibleItems(curLocs, self.currentItems, pool)
#        print(set([item['Type'] for item in posItems]))
        if len(posItems) > 0:
            # if posItems is not empty, only those in posItems will be tried (see placeItem)
            nPool = len(set([item['Type'] for item in posItems]))
        else:
            # if posItems is empty, all items in the pool will be tried (see placeItem)
            nPool = len(set([item['Type'] for item in pool]))
        while itemLocation is None and len(self.failItems) < nPool:
#            print("P " + str(len(posItems)) + ", F " + str(len(self.failItems)) + " / " + str(nPool))
            itemLocation = self.placeItem(posItems, pool, curLocs)
        return itemLocation

    def cancelItem(self, itemLocations, maxLen, posItems, force=False):
        # cancel an item that did not made progress
        # we know what items can unlock the situation (posItems)
        # so we know what location class we can cancel
        itemTypes = [item['Type'] for item in self.currentItems]
        onlyMajors = all(item['Class'] == 'Major' for item in posItems)
        onlyMinors = all(item['Class'] == 'Minor' for item in posItems)
        locList = []
        i = len(itemLocations) - 1
        maxLocs = self.maxCancel + 2
        while len(locList) < maxLocs and i >= (100 - maxLen):
            il = itemLocations[i]
            isMajor = il['Item']['Class'] == 'Major' or self.restrictions['MajorMinor'] == False
            isMinor = il['Item']['Class'] == 'Minor' or self.restrictions['MajorMinor'] == False
            if il['Item']['Category'] != 'Progression' \
               and il not in self.progressionItemLocs \
               and ((not onlyMinors and not onlyMajors and isMajor) or \
                    (onlyMinors and isMinor) or \
                    (onlyMajors and isMajor)):
               locList.append(il)
            i -= 1
        itemLoc = None
        if len(locList) > 0:
            itemLoc = locList[random.randint(0, len(locList) - 1)]
        if itemLoc is None:
            if not force:
                # cancel was requested (not forced) and is not possible
                sys.stdout.write('!')
                sys.stdout.flush()
                return False
            else:
                # forced cancel
                cancelFrom = [il for il in itemLocations if not il in self.progressionItemLocs]
                if len(cancelFrom) == 0:
                    cancelFrom = itemLocations
                itemLoc = cancelFrom[random.randint(0, len(cancelFrom) - 1)]
                if itemLoc in self.progressionItemLocs:
                    self.progressionItemLocs.remove(itemLoc)
        itemLocations.remove(itemLoc)
        item = itemLoc['Item']
        loc = itemLoc['Location']
        if item in self.currentItems:
            self.currentItems.remove(item)
            self.smbm.removeItem(item['Type'])
        self.itemPool.append(item)
        self.usedLocations.remove(loc)
        self.unusedLocations.append(loc)
        self.totalCancels += 1
#        print("Cancelled  " + item['Type'] + " at " + loc['Name'])
        sys.stdout.write('x')
        sys.stdout.flush()
        return True
        
    def checkLocPool(self):
        progItems = [item for item in self.itemPool if self.isProgItem(item)]
        if len(progItems) == 0:
            return True
        isMinorProg = any(item['Class'] == 'Minor' for item in progItems)
        isMajorProg = any(item['Class'] == 'Major' for item in progItems)
        # check that there is room left in all main areas
        room = {'Brinstar' : 0, 'Norfair' : 0, 'WreckedShip' : 0, 'LowerNorfair' : 0, 'Maridia' : 0 }
        for loc in self.unusedLocations: # TODO should be accessible locations
            majAvail = self.restrictions['MajorMinor'] == False or loc['Class'] == 'Major'
            minAvail = self.restrictions['MajorMinor'] == False or loc['Class'] == 'Minor'
            if loc['Area'] in room and ((isMajorProg and majAvail) or (isMinorProg and minAvail)):
                room[loc['Area']] += 1
        for r in room.values():
            if r > 0 and r <= self.locLimit:
                sys.stdout.write('|')
                sys.stdout.flush()
                return False
        return True

    def getNextItemInPool(self, t):
        return next(item for item in self.itemPool if item['Type'] == t)
    
    def fillRestrictedLocations(self, itemLocations):
        # fill up unreachable locations with "junk" to maximize the chance of the ROM
        # to be finishable
        for loc in self.restrictedLocations:
            isMajor = self.restrictions['MajorMinor'] == False or loc['Class'] == 'Major'
            isMinor = self.restrictions['MajorMinor'] == False or loc['Class'] == 'Minor'
            itemLocation = {'Location' : loc}
            if isMinor and self.hasItemTypeInPool('Nothing'):
                itemLocation['Item'] = self.getNextItemInPool('Nothing')
            elif isMajor and self.hasItemTypeInPool('NoEnergy'):
                itemLocation['Item'] = self.getNextItemInPool('NoEnergy')
            elif isMajor and self.hasItemTypeInPool('XRayScope'):
                itemLocation['Item'] = self.getNextItemInPool('XRayScope')
            elif isMinor and self.hasItemTypeInPool('Missile'):
                itemLocation['Item'] = self.getNextItemInPool('Missile')
            elif isMinor and self.hasItemTypeInPool('Super'):
                itemLocation['Item'] = self.getNextItemInPool('Super')
            elif isMinor and self.hasItemTypeInPool('PowerBomb'):
                itemLocation['Item'] = self.getNextItemInPool('PowerBomb')
            elif isMajor and self.hasItemTypeInPool('Reserve'):
                itemLocation['Item'] = self.getNextItemInPool('Reserve')
            elif isMajor and self.hasItemTypeInPool('ETank'):
                itemLocation['Item'] = self.getNextItemInPool('ETank')
            else:
                break
#            print("Fill : " + itemLocation['Item']['Type'] + " at " + itemLocation['Location']['Name'])
            self.getItem(itemLocation, itemLocations, False)

    def fillNonProgressionItems(self, itemLocations):
        pool = [item for item in self.itemPool if not self.isProgItem(item)]
        poolWasEmpty = len(pool) == 0
        itemLocation = None
        nItems = 0
        locPoolOk = True
#            print("NON-PROG")
        minLimit = self.itemLimit - int(self.itemLimit/5)
        maxLimit = self.itemLimit + int(self.itemLimit/5)
        itemLimit = random.randint(minLimit, maxLimit)
        while len(pool) > 0 and nItems < itemLimit and locPoolOk: 
            curLocs = self.currentLocations()
            itemLocation = self.generateItem(curLocs, pool)
            if itemLocation is None:
                break
            else:
                nItems += 1
                self.getItem(itemLocation, itemLocations)
                pool = self.removeItem(itemLocation['Item']['Type'], pool)
            locPoolOk = self.checkLocPool()
        isStuck = not poolWasEmpty and itemLocation is None
        return isStuck

    def getItemFromStandardPool(self, itemLocations, isStuck, maxLen):
#                print("REGULAR")
        # first, try to put an item from standard pool
#        print("PROG IN maxLen =  " + str(maxLen) + ", " + str([l['Name'] for l in self.currentLocations()]))
        curLocs = self.currentLocations()
        nLocsIn = len(curLocs)
        itemLocation = None
        nCancel = 0
        if not isStuck:
            itemLocation = self.generateItem(curLocs, self.itemPool)
        if itemLocation is None and self.totalCancels < 250:
            # we cannot place items anymore, cancel a bunch of our last decisions
            doCancel = True
            posItems = self.possibleItems(curLocs, self.currentItems, self.itemPool)
            while doCancel is True and len(itemLocations) > 0 and nCancel < self.maxCancel and len(self.itemPool) <= maxLen:
                doCancel = self.cancelItem(itemLocations, maxLen, posItems)
                if doCancel is True:
                    nCancel += 1
            if nLocsIn > 0 or nCancel > 0:
                curLocs = self.currentLocations()
                itemLocation = self.generateItem(curLocs, self.itemPool)
        else:
            sys.stdout.write('-')
            sys.stdout.flush()
        isStuck = itemLocation is None
        nFreed = 0
        if isStuck == False:
            if nCancel > 0:
                nFreed = nCancel - 1
            self.getItem(itemLocation, itemLocations)
        else:
            nFreed = nCancel
        curLocs = self.currentLocations()
        nLocsOut = len(curLocs)
        if nLocsOut - nFreed <= nLocsIn:
#            print("up")
            self.maxCancel += 1
        else:
#            print("one")
            self.maxCancel = 1
#        print("PROG OUT " + str([l['Name'] for l in curLocs]) + ", stuck? " + str(isStuck))
        return isStuck
    
    def generateItems(self):
        itemLocations = []
        self.currentItems = []
        self.smbm.resetItems()
        self.nonProgTypesCache = []
        self.progTypesCache = []
        isStuck = False
        # if major items are removed from the pool (super fun setting), fill not accessible locations with
        # items that are as useless as possible
        self.fillRestrictedLocations(itemLocations)
        maxLen = len(self.itemPool) # to prevent cancelling of these useless items/locations
        while len(self.itemPool) > 0 and not isStuck:
            # 1. fill up with non-progression stuff
            isStuck = self.fillNonProgressionItems(itemLocations)
            if len(self.itemPool) > 0:
                # 2. collect an item with standard pool that will unlock the situation
#                print("Full Pool " + str(len(self.itemPool)) + ", curLocs " + str([l['Name'] for l in self.currentLocations(self.currentItems)]))
                isStuck = self.getItemFromStandardPool(itemLocations, isStuck, maxLen)
                if isStuck == True:
                    # force item cancel if stuck as a last resort for early game corner cases
                    self.cancelItem(itemLocations, maxLen, [], force=True)
                    isStuck = self.getItemFromStandardPool(itemLocations, isStuck, maxLen)
        if len(self.itemPool) > 0:
            # we could not place all items, check if we can finish the game
            itemTypes = [item['Type'] for item in self.currentItems]
#            print(itemTypes)
            self.smbm.resetSMBool()
            self.smbm.wand(Bosses.allBossesDead(self.smbm), self.smbm.enoughStuffTourian())
            canEndGame = self.smbm.getSMBool()
#            print(canEndGame)
#            print(Bosses.golden4Dead)
            if canEndGame.bool == True and canEndGame.difficulty < self.difficultyTarget:
                # seed is finishable, place randomly all remaining items
                while len(self.itemPool) > 0:
                    itemLocation = {
                        'Item' : self.itemPool[0],
                        'Location' : self.unusedLocations[random.randint(0, len(self.unusedLocations) - 1)]
                    }
#                    print("Fill : " + itemLocation['Item']['Type'] + " at " + itemLocation['Location']['Name'])
                    self.getItem(itemLocation, itemLocations, False)
            else:
                print("\nSTUCK ! ")
                print("REM LOCS = "  + str([loc['Name'] for loc in self.unusedLocations]))
                print("REM ITEMS = "  + str([item['Type'] for item in self.itemPool]))
                return None
        print("")
        return itemLocations

