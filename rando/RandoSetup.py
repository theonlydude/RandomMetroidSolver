import copy, log
from helpers import Bosses

class RandoSetup(object):
    # give the rando since we have to access services from it
    def __init__(self, smbm, startAP, graph, locations, settings, services):
        self.sm = smbm
        self.startAP = startAP
        self.settings = settings
        self.itemManager = settings.getItemManager(smbm)
        self.superFun = settings.superFun
        self.container = None
        self.services = services
        self.locations = locations
        self.areaGraph = graph
        self.forbiddenItems = []
        self.restrictedLocs = []
        self.lastRestricted = []
        self.bossesLocs = ['Draygon', 'Kraid', 'Ridley', 'Phantoon', 'Mother Brain']
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
        self.itemManager.createItemPool() # we have to do this only once, otherwise pool will change
        self.basePool = self.itemManager.getItemPool()[:]
        self.log = log.get('RandoSetup')

    def createItemLocContainer(self):
        self.getForbidden()
        if not self.checkPool() or not self.checkStart():
            return None
        self.container = ItemLocContainer(self.sm, self.getItemPool(), self.locations)
        self.fillRestrictedLocations()
        return self.container

    # fill up unreachable locations with "junk" to maximize the chance of the ROM
    # to be finishable
    def fillRestrictedLocations(self):
#        isChozo = self.restrictions['MajorMinor'] == 'Chozo'
        for loc in self.restrictedLocations:
            isMajor = self.services.isLocMajor(loc)
            isMinor = self.services.isLocMinor(loc)
            # if isChozo:
            #     if isMajor: # chozo loc
            #         self.itemPool = self.chozoItemPool
            #     else:
            #         self.itemPool = self.nonChozoItemPool
            itemLocation = {'Location' : loc}
            if isMinor and self.container.hasItemTypeInPool('Nothing'):
                itemLocation['Item'] = self.container.getNextItemInPool('Nothing')
            elif isMajor and self.container.hasItemTypeInPool('NoEnergy'):
                itemLocation['Item'] = self.container.getNextItemInPool('NoEnergy')
            elif isMinor and self.container.countItemTypeInPool('Missile') > 3:
                itemLocation['Item'] = self.container.getNextItemInPool('Missile')
            elif isMinor and self.container.countItemTypeInPool('Super') > 2:
                itemLocation['Item'] = self.container.getNextItemInPool('Super')
            elif isMinor and self.container.countItemTypeInPool('PowerBomb') > 1:
                itemLocation['Item'] = self.container.getNextItemInPool('PowerBomb')
            elif isMajor and self.container.countItemTypeInPool('Reserve') > 1:
                itemLocation['Item'] = self.container.getNextItemInPool('Reserve')
            elif isMajor and self.container.countItemTypeInPool('ETank') > 3:
                itemLocation['Item'] = self.container.getNextItemInPool('ETank')
            else:
                raise RuntimeError("Cannot fill restricted locations")
            self.log.debug("Fill: {} at {}".format(itemLocation['Item']['Type'], itemLocation['Location']['Name']))
            self.container.collect(itemLocation, False)
        # if isChozo:
        #     self.itemPool = self.chozoItemPool
    
    def getItemPool(self, forbidden=[]):
        self.itemManager.setItemPool(self.basePool[:]) # reuse base pool to have constant base item set
        return self.itemManager.removeForbiddenItems(self.forbiddenItems + forbidden)

    # if needed, do a simplified "pre-randomization" of a few items to check start AP/area layout validity
    # very basic because we know we're in full randomization in cases the check can fail
    def checkStart(self):
        ap = getAccessPoint(self.startAP)
        if ap.Start is None or \
           (('needsPreRando' not in ap.Start or not ap.Start['needsPreRando']) and \
            ('areaMode' not in ap.Start or not ap.Start['areaMode'])):
            return True
        self.log.debug("********* PRE RANDO START")
        container = copy.copy(self.container)
        itemLoc = None
        startOk = True
#        self.rando.computeLateMorphLimit()
        self.sm.resetItems()
        curLocs = self.services.currentLocations(container=container)
#        state = RandoState(self.rando, curLocs)
#        self.rando.determineParameters()
        for i in range(4):
            # services need restrictions object
            itemLoc = self.services.generateItem(curLocs, container=container)
            if itemLoc is None:
                startOk = False
                break
            container.collect(itemLoc)
            curLocs = self.services.currentLocations(container=container)
#        state.apply(self.rando)
        self.log.debug("********* PRE RANDO END")

        return startOk

    def checkPool(self, forbidden=None):
        self.log.debug("checkPool. forbidden=" + str(forbidden) + ", self.forbiddenItems=" + str(self.forbiddenItems))
        ret = True
        if forbidden is not None:
            pool = self.getItemPool(forbidden)
        else:
            pool = self.getItemPool()
        # if self.isChozo:
        #     zeb = self.sm.knowsIceZebSkip()
        #     pool = [item for item in pool if item['Class'] == 'Chozo' or item['Name'] == 'Boss']
        #     # forces ice zeb skip in the knows to pass end game condition. this is ugly but valid,
        #     # as if zeb skip is not known, an extra missile pack is guaranteed to be added (it won't
        #     # be in a chozo location, but the game is still finishable)
        #     Knows.IceZebSkip = SMBool(True, 0, [])

        poolDict = self.services.getPoolDict(pool)
        self.log.debug('pool={}'.format(sorted([(t, len(poolDict[t])) for t in poolDict])))
        # give us everything and beat every boss to see what we can access
        self.disableBossChecks()
        self.sm.resetItems()
        self.sm.addItems([item['Type'] for item in pool])
        for boss in self.bossChecks:
            Bosses.beatBoss(boss)
        # get restricted locs
        totalAvailLocs = []
        comeBack = {}
        container = ItemLocContainer(self.sm, pool, self.locations)
        locs = self.services.currentLocations(container=container, post=True)
        for loc in locs:
            ap = loc['accessPoint']
            if ap not in comeBack:
                # we chose Landing Site because other start APs might not have comeback transitions
                # possible start AP issues are handled in checkStart
                comeBack[ap] = self.areaGraph.canAccess(self.sm, ap, 'Landing Site', self.rando.difficultyTarget)
            if comeBack[ap]:
                totalAvailLocs.append(loc)
        self.lastRestricted = [loc for loc in self.locations if loc not in totalAvailLocs]
        self.log.debug("restricted=" + str([loc['Name'] for loc in self.lastRestricted]))

        # check if we all inter-area APs reach each other
        interAPs = [ap for ap in self.areaGraph.accessPoints.values() if ap.isArea()]
        for startAp in interAPs:
            availAccessPoints = self.areaGraph.getAvailableAccessPoints(startAp, self.sm, self.rando.difficultyTarget)
            for ap in interAPs:
                if not ap in availAccessPoints:
                    ret = False
                    self.log.debug("unavail AP: " + ap.Name + ", from " + startAp.Name)

        # check if we can reach all bosses
        if ret:
            for loc in self.lastRestricted:
                if loc['Name'] in self.bossesLocs:
                    ret = False
                    self.log.debug("unavail Boss: " + loc['Name'])
            if ret:
                # revive bosses and see if phantoon doesn't block himself, and if we can reach draygon if she's alive
                Bosses.reset()
                # reset cache
                self.sm.resetItems()
                self.sm.addItems([item['Type'] for item in pool])
                maxDiff = self.settings.difficultyTarget
                ret = self.areaGraph.canAccess(self.sm, 'PhantoonRoomOut', 'PhantoonRoomIn', maxDiff)\
                      and self.areaGraph.canAccess(self.sm, 'Main Street Bottom', 'DraygonRoomIn', maxDiff)
                self.log.debug('checkPool. boss access sanity check: '+str(ret))

        # if self.isChozo:
        #     Knows.IceZebSkip = zeb
        #     # last check for chozo locations: don't put more restricted locations than removed chozo items (we cannot rely
        #     # on removing ammo/energy in fillRestrictedLocations since it is already the bare minimum in chozo pool)
        #     restrictedLocs = self.restrictedLocs + [loc for loc in self.lastRestricted if loc not in self.restrictedLocs]
        #     nRestrictedChozo = sum(1 for loc in restrictedLocs if 'Chozo' in loc['Class'])
        #     nNothingChozo = sum(1 for item in pool if 'Chozo' in item['Class'] and item['Category'] == 'Nothing')
        #     ret &= nRestrictedChozo <= nNothingChozo
        #     self.log.debug('checkPool. nRestrictedChozo='+str(nRestrictedChozo)+', nNothingChozo='+str(nNothingChozo))
        # cleanup
        self.sm.resetItems()
        Bosses.reset()
        self.restoreBossChecks()
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
        self.log.debug("getForbiddenSuits BEGIN. forbidden="+str(self.forbiddenItems)+",ap="+self.rando.curAccessPoint)
        removableSuits = [suit for suit in self.suits if self.checkPool([suit])]
        if 'Varia' in removableSuits and self.rando.curAccessPoint in ['Bubble Mountain', 'Firefleas Top']:
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
            self.errorMsgs.append("Could not remove any suit")
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
            self.errorMsgs.append('Could not remove any movement item')
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
            self.errorMsgs.append('Could not remove any combat item')
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

        self.log.debug("forbiddenItems: {}".format(self.forbiddenItems))
        self.log.debug("restrictedLocs: {}".format([loc['Name'] for loc in self.restrictedLocs]))
