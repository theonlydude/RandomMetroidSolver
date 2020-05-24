
import copy, random, sys

from rando.Filler import Filler
from rando.Choice import ItemThenLocChoiceProgSpeed
from rando.RandoServices import ComebackCheckType
from rando.Items import ItemManager
from parameters import infinity
from graph_access import GraphUtils, getAccessPoint

progSpeeds = ['slowest', 'slow', 'medium', 'fast', 'fastest']

# algo settings depending on prog speed, and unrelated to choice
class ProgSpeedParameters(object):
    def __init__(self, restrictions):
        self.restrictions = restrictions

    def getMinorHelpProb(self, progSpeed):
        if self.restrictions.split != 'Major':
            return 0
        if progSpeed == 'slowest':
            return 0.16
        elif progSpeed == 'slow':
            return 0.33
        elif progSpeed == 'medium':
            return 0.5
        return 1

    def getItemLimit(self, progSpeed):
        itemLimit = 105
        if progSpeed == 'slow':
            itemLimit = 21
        elif progSpeed == 'medium':
            itemLimit = 12
        elif progSpeed == 'fast':
            itemLimit = 5
        elif progSpeed == 'fastest':
            itemLimit = 1
        if self.restrictions.split == 'Chozo':
            itemLimit = int(itemLimit / 4)
        minLimit = itemLimit - int(itemLimit/5)
        maxLimit = itemLimit + int(itemLimit/5)
        if minLimit == maxLimit:
            itemLimit = minLimit
        else:
            itemLimit = random.randint(minLimit, maxLimit)
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

    def getProgressionItemTypes(self, progSpeed):
        progTypes = ItemManager.getProgTypes()
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
        if progSpeed == 'fastest':
            return progTypes # only morph, varia, gravity
        raise RuntimeError("Unknown prog speed " + progSpeed)

    def getPossibleSoftlockProb(self, progSpeed):
        if progSpeed == 'slowest':
            return 1
        if progSpeed == 'slow':
            return 0.66
        if progSpeed == 'medium':
            return 0.33
        if progSpeed == 'fast':
            return 0.1
        if progSpeed == 'fastest':
            return 0
        raise RuntimeError("Unknown prog speed " + progSpeed)

# algo state used for rollbacks
class FillerState(object):
    def __init__(self, filler):
        self.container = copy.copy(filler.container)
        self.ap = filler.ap
        self.states = filler.states[:]
        self.progressionItemLocs = filler.progressionItemLocs[:]
        self.progressionStatesIndices = filler.progressionStatesIndices[:]

    def apply(self, filler):
        filler.container = self.container
        filler.ap = self.ap
        filler.states = self.states
        filler.progressionItemLocs = self.progressionItemLocs
        filler.progressionStatesIndices = self.progressionStatesIndices
        filler.cache.reset()

    def __eq__(self, rhs):
        if rhs is None:
            return False
        eq = self.container == rhs.container
        eq &= self.ap == rhs.ap
        eq &= self.progressionStatesIndices == rhs.progressionStatesIndices
        return eq

class FillerProgSpeed(Filler):
    def __init__(self, graphSettings, areaGraph, restrictions, container):
        super(FillerProgSpeed, self).__init__(graphSettings.startAP, areaGraph, restrictions, container)
        distanceProp = 'GraphArea' if graphSettings.areaRando else 'Area'
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        self.choice = ItemThenLocChoiceProgSpeed(restrictions, distanceProp, self.services)
        self.progSpeedParams = ProgSpeedParameters(restrictions)

    def initFiller(self):
        super(FillerProgSpeed, self).initFiller()
        self.states = []
        self.progressionItemLocs = []
        self.progressionStatesIndices = []
        self.rollbackItemsTried = {}
        self.lastFallbackState = None
        self.initState = FillerState(self)

    def determineParameters(self):
        speed = self.settings.progSpeed
        if speed == 'variable':
            speed = random.choice(progSpeeds)
        self.choice.determineParameters(speed)
        self.minorHelpProb = self.progSpeedParams.getMinorHelpProb(speed)
        self.itemLimit = self.progSpeedParams.getItemLimit(speed)
        self.locLimit = self.progSpeedParams.getLocLimit(speed)
        self.possibleSoftlockProb = self.progSpeedParams.getPossibleSoftlockProb(speed)
        self.progressionItemTypes = self.progSpeedParams.getProgressionItemTypes(speed)
        if self.restrictions.isEarlyMorph() and 'Morph' in self.progressionItemTypes:
            self.progressionItemTypes.remove('Morph')
        collectedAmmo = self.container.getCollectedItems(lambda item: item['Category'] == 'Ammo')
        collectedAmmoTypes = set([item['Type'] for item in collectedAmmo])
        ammos = ['Missile', 'Super', 'PowerBomb']
        if 'Super' in collectedAmmoTypes:
            ammos.remove('Missile')
        self.progressionItemTypes += [ammoType for ammoType in ammos if ammoType not in collectedAmmoTypes]

    def chooseItemLoc(self, itemLocDict, possibleProg):
        return self.choice.chooseItemLoc(itemLocDict, possibleProg, self.progressionItemLocs, self.ap, self.container)

    def currentLocations(self, item=None):
        return self.services.currentLocations(self.ap, self.container, item=item)

    def getComebackCheck(self):
        if self.isEarlyGame():
            return ComebackCheckType.NoCheck
        if random.random() >= self.possibleSoftlockProb:
            return ComebackCheckType.ComebackWithoutItem
        return ComebackCheckType.JustComeback

    # from current accessible locations and an item pool, generate an item/loc dict.
    # return item/loc, or None if stuck
    def generateItem(self):        
        itemLocDict, possibleProg = self.services.getPossiblePlacements(self.ap, self.container, self.getComebackCheck())
        if self.isEarlyGame():
            # cheat a little bit if non-standard start: place early
            # progression away from crateria/blue brin if possible
            startAp = getAccessPoint(self.startAP)
            if startAp.GraphArea != "Crateria":
                newItemLocDict = {}
                for w, locs in itemLocDict.items():
                    filtered = [loc for loc in locs if loc['GraphArea'] != 'Crateria']
                    if len(filtered) > 0:
                        newItemLocDict[w] = filtered
                if len(newItemLocDict) > 0:
                    itemLocDict = newItemLocDict
        itemLoc = self.chooseItemLoc(itemLocDict, possibleProg)
        self.log.debug("generateItem. itemLoc="+("None" if itemLoc is None else itemLoc['Item']['Type']+"@"+itemLoc['Location']['Name']))
        return itemLoc

    def getCurrentState(self):
        return self.states[-1] if len(self.states) > 0 else self.initState
    
    def appendCurrentState(self):
        curState = FillerState(self)
        self.states.append(curState)
        curState.states.append(curState)

    def collect(self, itemLoc):
        item = itemLoc['Item']
        location = itemLoc['Location']
        isProg = self.services.isProgression(item, self.ap, self.container)
        self.ap = self.services.collect(self.ap, self.container, itemLoc)
        if isProg:
            n = len(self.states)
            self.log.debug("prog indice="+str(n))
            self.progressionStatesIndices.append(n)
            self.progressionItemLocs.append(itemLoc)
        self.appendCurrentState()
        self.cache.reset()

    def isProgItem(self, item):
        if item['Type'] in self.progressionItemTypes:
            return True
        return self.services.isProgression(item, self.ap, self.container)

    def isEarlyGame(self):
        return len(self.progressionStatesIndices) <= 2 if self.stdStart else len(self.progressionStatesIndices) <= 3

    # check if remaining locations pool is conform to rando settings when filling up
    # with non-progression items
    def checkLocPool(self):
        sm = self.container.sm
 #       self.log.debug("checkLocPool {}".format([it['Name'] for it in self.itemPool]))
        if self.locLimit <= 0:
            return True
        progItems = self.container.getItems(self.isProgItem)
        self.log.debug("checkLocPool. progItems {}".format([it['Name'] for it in progItems]))
 #       self.log.debug("curItems {}".format([it['Name'] for it in self.currentItems]))
        if len(progItems) == 0:
            return True
        isMinorProg = any(self.restrictions.isItemMinor(item) for item in progItems)
        isMajorProg = any(self.restrictions.isItemMajor(item) for item in progItems)
        accessibleLocations = []
#        self.log.debug("unusedLocs: {}".format([loc['Name'] for loc in self.unusedLocations]))
        locs = self.currentLocations()
        for loc in locs:
            majAvail = self.restrictions.isLocMajor(loc)
            minAvail = self.restrictions.isLocMinor(loc)
            if ((isMajorProg and majAvail) or (isMinorProg and minAvail)) \
               and self.services.locPostAvailable(sm, loc, None):
                accessibleLocations.append(loc)
        self.log.debug("accesLoc {}".format([loc['Name'] for loc in accessibleLocations]))
        if len(accessibleLocations) <= self.locLimit:
            sys.stdout.write('|')
            sys.stdout.flush()
            return False
        # check that there is room left in all main areas
        room = {'Brinstar' : 0, 'Norfair' : 0, 'WreckedShip' : 0, 'LowerNorfair' : 0, 'Maridia' : 0 }
        if not self.stdStart:
            room['Crateria'] = 0
        for loc in self.container.unusedLocations:
            majAvail = self.restrictions.isLocMajor(loc)
            minAvail = self.restrictions.isLocMinor(loc)
            if loc['Area'] in room and ((isMajorProg and majAvail) or (isMinorProg and minAvail)):
                room[loc['Area']] += 1
        for r in room.values():
            if r > 0 and r <= self.locLimit:
                sys.stdout.write('|')
                sys.stdout.flush()
                return False
        return True

    def addEnergyAsNonProg(self):
        return self.restrictions.split == 'Chozo'

    def nonProgItemCheck(self, item):
        return (item['Category'] == 'Energy' and self.addEnergyAsNonProg()) or (not self.stdStart and item['Category'] == 'Ammo') or (self.restrictions.isEarlyMorph() and item['Type'] == 'Morph') or not self.isProgItem(item)

    def getNonProgItemPoolRestriction(self):
        return self.nonProgItemCheck

    def pickHelpfulMinor(self, item):
        self.helpfulMinorPicked = not self.container.hasItemTypeInPool(item['Type'])
        return self.helpfulMinorPicked

    def getNonProgItemPoolRestrictionStart(self):
        self.helpfulMinorPicked = random.random() >= self.minorHelpProb
        return lambda item: (item['Category'] == 'Ammo' and not self.helpfulMinorPicked and self.pickHelpfulMinor(item)) or self.nonProgItemCheck(item)

    # return True if stuck, False if not
    def fillNonProgressionItems(self):
        if self.itemLimit <= 0:
            return False
        poolRestriction = self.getNonProgItemPoolRestrictionStart()
        self.container.restrictItemPool(poolRestriction)
        if self.container.isPoolEmpty():
            self.container.unrestrictItemPool()
            return False
        itemLocation = None
        nItems = 0
        locPoolOk = True
        self.log.debug("NON-PROG")
        while not self.container.isPoolEmpty() and nItems < self.itemLimit and locPoolOk:
            itemLocation = self.generateItem()
            if itemLocation is not None:
                nItems += 1
                self.log.debug("fillNonProgressionItems: {} at {}".format(itemLocation['Item']['Name'], itemLocation['Location']['Name']))
                # doing this first is actually important, as state is saved in collect
                self.container.unrestrictItemPool()
                self.collect(itemLocation)
                locPoolOk = self.checkLocPool()
                poolRestriction = self.getNonProgItemPoolRestriction()
                self.container.restrictItemPool(poolRestriction)
            else:
                break
        self.container.unrestrictItemPool()
        return itemLocation is None

    def getItemFromStandardPool(self):
        itemLoc = self.generateItem()
        isStuck = itemLoc is None
        if not isStuck:
            sys.stdout.write('-')
            sys.stdout.flush()
            self.collect(itemLoc)
        return isStuck

    def initRollbackPoints(self):
        minRollbackPoint = 0
        maxRollbackPoint = len(self.states) - 1
        if len(self.progressionStatesIndices) > 0:
            minRollbackPoint = self.progressionStatesIndices[-1]
        self.log.debug('initRollbackPoints: min=' + str(minRollbackPoint) + ", max=" + str(maxRollbackPoint))
        return minRollbackPoint, maxRollbackPoint

    def initRollback(self, isFakeRollback):
        self.log.debug('initRollback: progressionStatesIndices 1=' + str(self.progressionStatesIndices))
        if len(self.progressionStatesIndices) > 0 and self.progressionStatesIndices[-1] == len(self.states) - 1:
            if isFakeRollback == True: # in fake rollback case we refuse to remove any progression
                return
            # the state we are about to remove was a progression state
            self.progressionStatesIndices.pop()
        if len(self.states) > 0:
            self.states.pop() # remove current state, it's the one we're stuck in
        self.log.debug('initRollback: progressionStatesIndices 2=' + str(self.progressionStatesIndices))

    def getSituationId(self):
        progItems = str(sorted([il['Item']['Type'] for il in self.progressionItemLocs]))
        position = str(sorted([ap.Name for ap in self.services.currentAccessPoints(self.ap, self.container)]))
        return progItems+'/'+position

    def hasTried(self, itemLoc):
        if self.isEarlyGame():
            return False
        itemType = itemLoc['Item']['Type']
        situation = self.getSituationId()
        ret = False
        if situation in self.rollbackItemsTried:
            ret = itemType in self.rollbackItemsTried[situation]
            if ret:
                self.log.debug('has tried ' + itemType + ' in situation ' + situation)
        return ret

    def updateRollbackItemsTried(self, itemLoc):
        itemType = itemLoc['Item']['Type']
        situation = self.getSituationId()
        if situation not in self.rollbackItemsTried:
            self.rollbackItemsTried[situation] = []
        self.log.debug('adding ' + itemType + ' to situation ' + situation)
        self.rollbackItemsTried[situation].append(itemType)

    # goes back in the previous states to find one where
    # we can put a progression item
    def rollback(self):
        nItemsAtStart = len(self.container.currentItems)
        nStatesAtStart = len(self.states)
        self.log.debug("rollback BEGIN: nItems={}, nStates={}".format(nItemsAtStart, nStatesAtStart))
        currentState = self.getCurrentState()
        ret = None
        # we can be in a 'fake rollback' situation where we rollback
        # just after non prog phase without checking normal items first (we
        # do this for more randomness, to avoid placing items in postavail locs
        # like spospo etc. too often).
        # in this case, we won't remove any prog items since we're not actually
        # stuck
        if not self.isEarlyGame():
            ret = self.generateItem()
        isFakeRollback = ret is not None
        self.log.debug('isFakeRollback=' + str(isFakeRollback))
        self.initRollback(isFakeRollback)
        if len(self.states) == 0:
            self.initState.apply(self)
            self.log.debug("rollback END initState apply, nCurLocs="+str(len(self.currentLocations())))
            # if self.vcr != None:
            #     self.vcr.addRollback(nStatesAtStart)
            sys.stdout.write('<'*nStatesAtStart)
            sys.stdout.flush()
            return None
        # to stay consistent in case no solution is found as states list was popped in init
        fallbackState = self.getCurrentState()
        if fallbackState == self.lastFallbackState:
            # we're stuck there, rewind more in fallback
            fallbackState = self.states[-2] if len(self.states) > 1 else self.initState
        self.lastFallbackState = fallbackState
        i = 0
        possibleStates = []
        self.log.debug('rollback. nStates='+str(len(self.states)))
        while i >= 0 and len(possibleStates) == 0:
            states = self.states[:]
            minRollbackPoint, maxRollbackPoint = self.initRollbackPoints()
            i = maxRollbackPoint
            while i >= minRollbackPoint and len(possibleStates) < 3:
                state = states[i]
                state.apply(self)                
                itemLoc = self.generateItem()
                if itemLoc is not None and not self.hasTried(itemLoc) and self.services.isProgression(itemLoc['Item'], self.ap, self.container):
                    possibleStates.append((state, itemLoc))
                i -= 1
            # nothing, let's rollback further a progression item
            if len(possibleStates) == 0 and i >= 0:
                if len(self.progressionStatesIndices) > 0 and isFakeRollback == False:
                    sys.stdout.write('!')
                    sys.stdout.flush()
                    self.progressionStatesIndices.pop()
                else:
                    break
        if len(possibleStates) > 0:
            (state, itemLoc) = random.choice(possibleStates)
            self.updateRollbackItemsTried(itemLoc)
            state.apply(self)
            ret = itemLoc
            # if self.vcr != None:
            #     nRoll = nItemsAtStart - len(self.currentItems)
            #     if nRoll > 0:
            #         self.vcr.addRollback(nRoll)
        else:
            if isFakeRollback == False:
                self.log.debug('fallbackState apply')
                fallbackState.apply(self)
                # if self.vcr != None:
                #     self.vcr.addRollback(1)
            else:
                self.log.debug('currentState restore')
                currentState.apply(self)
        sys.stdout.write('<'*(nStatesAtStart - len(self.states)))
        sys.stdout.flush()
        self.log.debug("rollback END: {}".format(len(self.container.currentItems)))
        return ret

    def step(self, onlyBossCheck=False):
        self.cache.reset()
        if self.services.canEndGame(self.container) and self.settings.progSpeed not in ['slowest', 'slow']:
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
            itemLoc = self.chooseItemLoc(itemLocDict, False)
            assert itemLoc is not None
            self.ap = self.services.collect(self.ap, self.container, itemLoc)
            return True
        self.determineParameters()
        # fill up with non-progression stuff
        isStuck = self.fillNonProgressionItems()
        if not self.container.isPoolEmpty():
            if not isStuck:
                isStuck = self.getItemFromStandardPool()
            if isStuck:
                if onlyBossCheck == False and self.services.onlyBossesLeft(self.ap, self.container):
                    self.settings.maxDiff = infinity
                    return self.step(onlyBossCheck=True)
                if onlyBossCheck == True:
                    # we're stuck even after bumping diff.
                    # it was a onlyBossesLeft false positive, restore max diff
                    self.settings.maxDiff = self.maxDiff
                # check that we're actually stuck
                nCurLocs = len(self.currentLocations())
                nLocsLeft = len(self.container.unusedLocations)
                itemLoc = None
                if nCurLocs < nLocsLeft:
                    # stuck, rollback to make progress if we can't access everything yet
                    itemLoc = self.rollback()
                if itemLoc is not None:
                    self.collect(itemLoc)
                    isStuck = False
                else:
                    isStuck = self.getItemFromStandardPool()
        return not isStuck
