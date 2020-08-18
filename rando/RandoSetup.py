import copy, log, random

from utils import randGaussBounds
from smbool import SMBool
from smboolmanager import SMBoolManager
from helpers import Bosses
from graph_access import getAccessPoint, GraphUtils
from rando.Filler import FrontFiller
from rando.ItemLocContainer import ItemLocContainer, getLocListStr
from rando.Chozo import isChozoItem
from parameters import infinity

# checks init conditions for the randomizer: processes super fun settings, graph, start location, special restrictions
# the entry point is createItemLocContainer
class RandoSetup(object):
    def __init__(self, graphSettings, locations, services):
        self.sm = SMBoolManager()
        self.settings = services.settings
        self.graphSettings = graphSettings
        self.startAP = graphSettings.startAP
        self.superFun = self.settings.superFun
        self.container = None
        self.services = services
        self.restrictions = services.restrictions
        self.areaGraph = services.areaGraph
        self.allLocations = locations
        self.locations = self.areaGraph.getAccessibleLocations(locations, self.startAP)
#        print("nLocs Setup: "+str(len(self.locations)))
        self.itemManager = self.settings.getItemManager(self.sm, len(self.locations))
        self.forbiddenItems = []
        self.restrictedLocs = []
        self.lastRestricted = []
        self.bossesLocs = sorted(['Draygon', 'Kraid', 'Ridley', 'Phantoon', 'Mother Brain'])
        self.suits = ['Varia', 'Gravity']
        # organized by priority
        self.movementItems = ['SpaceJump', 'HiJump', 'SpeedBooster', 'Bomb', 'Grapple', 'SpringBall']
        # organized by priority
        self.combatItems = ['ScrewAttack', 'Plasma', 'Wave', 'Spazer']
        # OMG
        self.bossChecks = {
            'Kraid' : self.sm.enoughStuffsKraid,
            'Phantoon' : self.sm.enoughStuffsPhantoon,
            'Draygon' : self.sm.enoughStuffsDraygon,
            'Ridley' : self.sm.enoughStuffsRidley,
            'Mother Brain': self.sm.enoughStuffsMotherbrain
        }
        self.okay = lambda: SMBool(True, 0)
        exclude = self.settings.getExcludeItems(self.locations)
        # we have to use item manager only once, otherwise pool will change
        self.itemManager.createItemPool(exclude)
        self.basePool = self.itemManager.getItemPool()[:]
        self.log = log.get('RandoSetup')
        if len(locations) != len(self.locations):
            self.log.debug("inaccessible locations :"+getLocListStr([loc for loc in locations if loc not in self.locations]))

    # processes everything and returns an ItemLocContainer, or None if failed (invalid init conditions/settings)
    def createItemLocContainer(self):
        self.getForbidden()
        if not self.checkPool():
            self.log.debug("createItemLocContainer: checkPool fail")
            return None
        self.container = ItemLocContainer(self.sm, self.getItemPool(), self.locations)
        if self.restrictions.isLateMorph():
            self.restrictions.lateMorphInit(self.startAP, self.container, self.services)
            isStdStart = GraphUtils.isStandardStart(self.startAP)
            # ensure we have an area layout that can put morph outside start area
            # TODO::allow for custom start which doesn't require morph early
            if self.graphSettings.areaRando and isStdStart and not self.restrictions.suitsRestrictions and self.restrictions.lateMorphForbiddenArea is None:
                self.container = None
                self.log.debug("createItemLocContainer: checkLateMorph fail")
                return None
        # checkStart needs the container
        if not self.checkStart():
            self.container = None
            self.log.debug("createItemLocContainer: checkStart fail")
            return None
        # add placement restriction helpers for random fill
        if self.settings.progSpeed == 'speedrun':
            itemTypes = {item.Type for item in self.container.itemPool if item.Category not in ['Energy', 'Nothing', 'Boss']}
            itemTypes.remove('Missile')
            items = [self.container.getNextItemInPool(itemType) for itemType in itemTypes]
            restrictionDict = {}
            for item in items:
                itemType = item.Type
                poss = self.services.possibleLocations(item, self.startAP, self.container)
                for loc in poss:
                    if loc.GraphArea not in restrictionDict:
                        restrictionDict[loc.GraphArea] = {}
                    if itemType not in restrictionDict[loc.GraphArea]:
                        restrictionDict[loc.GraphArea][itemType] = set()
                    restrictionDict[loc.GraphArea][itemType].add(loc.Name)
            if self.restrictions.isEarlyMorph() and GraphUtils.isStandardStart(self.startAP):
                morphLocs = ['Morphing Ball']
                if self.restrictions.split in ['Full', 'Major']:
                    dboost = self.sm.knowsCeilingDBoost()
                    if dboost.bool == True and dboost.difficulty <= self.settings.maxDiff:
                        morphLocs += ['Energy Tank, Brinstar Ceiling']
                for area, locDict in restrictionDict.items():
                    if area == 'Crateria':
                        locDict['Morph'] = set(morphLocs)
                    elif 'Morph' in locDict:
                        del locDict['Morph']
            self.restrictions.addPlacementRestrictions(restrictionDict)
        self.fillRestrictedLocations()
        self.settings.collectAlreadyPlacedItemLocations(self.container)
        return self.container

    # fill up unreachable locations with "junk" to maximize the chance of the ROM
    # to be finishable
    def fillRestrictedLocations(self):
        majorRestrictedLocs = [loc for loc in self.restrictedLocs if self.restrictions.isLocMajor(loc)]
        otherRestrictedLocs = [loc for loc in self.restrictedLocs if loc not in majorRestrictedLocs]
        def getItemPredicateMajor(itemType):
            return lambda item: item.Type == itemType and self.restrictions.isItemMajor(item)
        def getItemPredicateMinor(itemType):
            return lambda item: item.Type == itemType and self.restrictions.isItemMinor(item)
        def fill(locs, getPred):
            self.log.debug("fillRestrictedLocations. locs="+getLocListStr(locs))
            for loc in locs:
                loc.restricted = True
                itemLocation = {'Location' : loc}
                if self.container.hasItemInPool(getPred('Nothing')):
                    itemLocation['Item'] = self.container.getNextItemInPoolMatching(getPred('Nothing'))
                elif self.container.hasItemInPool(getPred('NoEnergy')):
                    itemLocation['Item'] = self.container.getNextItemInPoolMatching(getPred('NoEnergy'))
                elif self.container.countItems(getPred('Missile')) > 3:
                    itemLocation['Item'] = self.container.getNextItemInPoolMatching(getPred('Missile'))
                elif self.container.countItems(getPred('Super')) > 2:
                    itemLocation['Item'] = self.container.getNextItemInPoolMatching(getPred('Super'))
                elif self.container.countItems(getPred('PowerBomb')) > 1:
                    itemLocation['Item'] = self.container.getNextItemInPoolMatching(getPred('PowerBomb'))
                elif self.container.countItems(getPred('Reserve')) > 1:
                    itemLocation['Item'] = self.container.getNextItemInPoolMatching(getPred('Reserve'))
                elif self.container.countItems(getPred('ETank')) > 3:
                    itemLocation['Item'] = self.container.getNextItemInPoolMatching(getPred('ETank'))
                else:
                    raise RuntimeError("Cannot fill restricted locations")
                self.log.debug("Fill: {} at {}".format(itemLocation['Item'].Type, itemLocation['Location'].Name))
                self.container.collect(itemLocation, False)
        fill(majorRestrictedLocs, getItemPredicateMajor)
        fill(otherRestrictedLocs, getItemPredicateMinor)

    def getItemPool(self, forbidden=[]):
        self.itemManager.setItemPool(self.basePool[:]) # reuse base pool to have constant base item set
        return self.itemManager.removeForbiddenItems(self.forbiddenItems + forbidden)

    # if needed, do a simplified "pre-randomization" of a few items to check start AP/area layout validity
    def checkStart(self):
        ap = getAccessPoint(self.startAP)
        if not self.graphSettings.areaRando or ap.Start is None or \
           (('needsPreRando' not in ap.Start or not ap.Start['needsPreRando']) and\
            ('areaMode' not in ap.Start or not ap.Start['areaMode'])):
            return True
        self.log.debug("********* PRE RANDO START")
        container = copy.copy(self.container)
        filler = FrontFiller(self.startAP, self.areaGraph, self.restrictions, container)
        condition = filler.createStepCountCondition(4)
        (isStuck, itemLocations, progItems) = filler.generateItems(condition)
        self.log.debug("********* PRE RANDO END")
        return not isStuck and len(self.services.currentLocations(filler.ap, filler.container)) > 0

    def checkPool(self, forbidden=None):
        self.log.debug("checkPool. forbidden=" + str(forbidden) + ", self.forbiddenItems=" + str(self.forbiddenItems))
        if self.graphSettings.minimizerN is None and len(self.allLocations) > len(self.locations):
            # invalid graph with looped areas
            return False
        ret = True
        if forbidden is not None:
            pool = self.getItemPool(forbidden)
        else:
            pool = self.getItemPool()
        # get restricted locs
        totalAvailLocs = []
        comeBack = {}
        try:
            container = ItemLocContainer(self.sm, pool, self.locations)
        except AssertionError as e:
            # invalid graph altogether
            self.log.debug("checkPool: AssertionError when creating ItemLocContainer: {}".format(e))
            return False
        # restrict item pool in chozo: game should be finishable with chozo items only
        contPool = []
        if self.restrictions.isChozo():
            container.restrictItemPool(isChozoItem)
            missile = container.getNextItemInPool('Missile')
            if missile is not None:
                # add missile (if zeb skip not known)
                contPool.append(missile)
        contPool += [item for item in pool if item in container.itemPool]
        # give us everything and beat every boss to see what we can access
        self.disableBossChecks()
        self.sm.resetItems()
        self.sm.addItems([item.Type for item in contPool]) # will add bosses as well
        poolDict = container.getPoolDict()
        self.log.debug('pool={}'.format(sorted([(t, len(poolDict[t])) for t in poolDict])))
        locs = self.services.currentLocations(self.startAP, container, post=True)
        self.areaGraph.useCache(True)
        for loc in locs:
            ap = loc.accessPoint
            if ap not in comeBack:
                # we chose Golden Four because it is always there.
                # Start APs might not have comeback transitions
                # possible start AP issues are handled in checkStart
                comeBack[ap] = self.areaGraph.canAccess(self.sm, ap, 'Golden Four', self.settings.maxDiff)
            if comeBack[ap]:
                totalAvailLocs.append(loc)
        self.areaGraph.useCache(False)
        self.lastRestricted = [loc for loc in self.locations if loc not in totalAvailLocs]
        self.log.debug("restricted=" + str([loc.Name for loc in self.lastRestricted]))

        # check if all inter-area APs can reach each other
        interAPs = [ap for ap in self.areaGraph.getAccessibleAccessPoints(self.startAP) if not ap.isInternal() and not ap.isLoop()]
        for startAp in interAPs:
            availAccessPoints = self.areaGraph.getAvailableAccessPoints(startAp, self.sm, self.settings.maxDiff)
            for ap in interAPs:
                if not ap in availAccessPoints:
                    ret = False
                    self.log.debug("unavail AP: " + ap.Name + ", from " + startAp.Name)

        # cleanup
        self.sm.resetItems()
        self.restoreBossChecks()
        # check if we can reach/beat all bosses
        if ret:
            for loc in self.lastRestricted:
                if loc.Name in self.bossesLocs:
                    ret = False
                    self.log.debug("unavail Boss: " + loc.Name)
            if ret:
                # revive bosses
                self.sm.addItems([item.Type for item in contPool if item.Category != 'Boss'])
                maxDiff = self.settings.maxDiff
                # see if phantoon doesn't block himself, and if we can reach draygon if she's alive
                ret = self.areaGraph.canAccess(self.sm, self.startAP, 'PhantoonRoomIn', maxDiff)\
                      and self.areaGraph.canAccess(self.sm, self.startAP, 'DraygonRoomIn', maxDiff)
                if ret:
                    # see if we can beat bosses with this equipment (infinity as max diff for a "onlyBossesLeft" type check
                    beatableBosses = sorted([loc.Name for loc in self.services.currentLocations(self.startAP, container, diff=infinity) if "Boss" in loc.Class])
                    self.log.debug("checkPool. beatableBosses="+str(beatableBosses))
                    ret = beatableBosses == Bosses.Golden4()
                    if ret:
                        # check that we can then kill mother brain
                        self.sm.addItems(Bosses.Golden4())
                        beatableMotherBrain = [loc.Name for loc in self.services.currentLocations(self.startAP, container, diff=infinity) if loc.Name == 'Mother Brain']
                        ret = len(beatableMotherBrain) > 0
                        self.log.debug("checkPool. beatable Mother Brain={}".format(ret))
                else:
                    self.log.debug('checkPool. locked by Phantoon or Draygon')
                self.log.debug('checkPool. boss access sanity check: '+str(ret))

        if self.restrictions.isChozo():
            # last check for chozo locations: don't put more restricted chozo locations than removed chozo items
            # (we cannot rely on removing ammo/energy in fillRestrictedLocations since it is already the bare minimum in chozo pool)
            # FIXME something to do there for ultra sparse, it gives us up to 3 more spots for nothing items
            restrictedLocs = self.restrictedLocs + [loc for loc in self.lastRestricted if loc not in self.restrictedLocs]
            nRestrictedChozo = sum(1 for loc in restrictedLocs if 'Chozo' in loc.Class)
            nNothingChozo = sum(1 for item in pool if 'Chozo' in item.Class and item.Category == 'Nothing')
            ret &= nRestrictedChozo <= nNothingChozo
            self.log.debug('checkPool. nRestrictedChozo='+str(nRestrictedChozo)+', nNothingChozo='+str(nNothingChozo))
        self.log.debug('checkPool. result: '+str(ret))
        return ret

    def disableBossChecks(self):
        self.sm.enoughStuffsKraid = self.okay
        self.sm.enoughStuffsPhantoon = self.okay
        self.sm.enoughStuffsDraygon = self.okay
        self.sm.enoughStuffsRidley = self.okay
        def mbCheck():
            (possible, energyDiff) = self.sm.mbEtankCheck()
            if possible == True:
                return self.okay()
            return SMBool(False)
        self.sm.enoughStuffsMotherbrain = mbCheck

    def restoreBossChecks(self):
        self.sm.enoughStuffsKraid = self.bossChecks['Kraid']
        self.sm.enoughStuffsPhantoon = self.bossChecks['Phantoon']
        self.sm.enoughStuffsDraygon = self.bossChecks['Draygon']
        self.sm.enoughStuffsRidley = self.bossChecks['Ridley']
        self.sm.enoughStuffsMotherbrain = self.bossChecks['Mother Brain']

    def addRestricted(self):
        self.checkPool()
        for r in self.lastRestricted:
            if r not in self.restrictedLocs:
                self.restrictedLocs.append(r)

    def getForbiddenItemsFromList(self, itemList):
        self.log.debug('getForbiddenItemsFromList: ' + str(itemList))
        remove = []
        n = randGaussBounds(len(itemList))
        for i in range(n):
            idx = random.randint(0, len(itemList) - 1)
            item = itemList.pop(idx)
            if item is not None:
                remove.append(item)
        return remove

    def addForbidden(self, removable):
        forb = None
        # it can take several tries if some item combination removal
        # forbids access to more stuff than each individually
        tries = 0
        while forb is None and tries < 100:
            forb = self.getForbiddenItemsFromList(removable[:])
            self.log.debug("addForbidden. forb="+str(forb))
            if self.checkPool(forb) == False:
                forb = None
            tries += 1
        if forb is None:
            # we couldn't find a combination, just pick an item
            firstItem = next((itemType for itemType in removable if itemType is not None), None)
            if firstItem is not None:
                forb = [firstItem]
            else:
                forb = []
        self.forbiddenItems += forb
        self.checkPool()
        self.addRestricted()
        return len(forb)

    def getForbiddenSuits(self):
        self.log.debug("getForbiddenSuits BEGIN. forbidden="+str(self.forbiddenItems)+",ap="+self.startAP)
        removableSuits = [suit for suit in self.suits if self.checkPool([suit])]
        if 'Varia' in removableSuits and self.startAP in ['Bubble Mountain', 'Firefleas Top']:
            # Varia has to be first item there, and checkPool can't detect it
            removableSuits.remove('Varia')
        self.log.debug("getForbiddenSuits removable="+str(removableSuits))
        if len(removableSuits) > 0:
            # remove at least one
            if self.addForbidden(removableSuits) == 0:
                self.forbiddenItems.append(removableSuits.pop())
                self.checkPool()
                self.addRestricted()
        else:
            self.superFun.remove('Suits')
            self.errorMsgs.append("Super Fun : Could not remove any suit")
        self.log.debug("getForbiddenSuits END. forbidden="+str(self.forbiddenItems))

    def getForbiddenMovement(self):
        self.log.debug("getForbiddenMovement BEGIN. forbidden="+str(self.forbiddenItems))
        removableMovement = [mvt for mvt in self.movementItems if self.checkPool([mvt])]
        self.log.debug("getForbiddenMovement removable="+str(removableMovement))
        if len(removableMovement) > 0:
            # remove at least the most important
            self.forbiddenItems.append(removableMovement.pop(0))
            self.addForbidden(removableMovement + [None])
        else:
            self.superFun.remove('Movement')
            self.errorMsgs.append('Super Fun : Could not remove any movement item')
        self.log.debug("getForbiddenMovement END. forbidden="+str(self.forbiddenItems))

    def getForbiddenCombat(self):
        self.log.debug("getForbiddenCombat BEGIN. forbidden="+str(self.forbiddenItems))
        removableCombat = [cbt for cbt in self.combatItems if self.checkPool([cbt])]
        self.log.debug("getForbiddenCombat removable="+str(removableCombat))
        if len(removableCombat) > 0:
            fake = [] # placeholders to avoid tricking the gaussian into removing too much stuff
            if len(removableCombat) > 0:
                # remove at least one if possible (will be screw or plasma)
                self.forbiddenItems.append(removableCombat.pop(0))
                fake.append(None)
            # if plasma is still available, remove it as well if we can
            if len(removableCombat) > 0 and removableCombat[0] == 'Plasma' and self.checkPool([removableCombat[0]]):
                self.forbiddenItems.append(removableCombat.pop(0))
                fake.append(None)
            self.addForbidden(removableCombat + fake)
        else:
            self.superFun.remove('Combat')
            self.errorMsgs.append('Super Fun : Could not remove any combat item')
        self.log.debug("getForbiddenCombat END. forbidden="+str(self.forbiddenItems))

    def getForbidden(self):
        self.forbiddenItems = []
        self.restrictedLocs = []
        self.errorMsgs = []
        if 'Suits' in self.superFun: # impact on movement item
            self.getForbiddenSuits()
        if 'Movement' in self.superFun:
            self.getForbiddenMovement()
        if 'Combat' in self.superFun:
            self.getForbiddenCombat()
        # if no super fun, check that there's no restricted locations (for ultra sparse)
        if len(self.superFun) == 0:
            self.addRestricted()
        self.log.debug("forbiddenItems: {}".format(self.forbiddenItems))
        self.log.debug("restrictedLocs: {}".format([loc.Name for loc in self.restrictedLocs]))
