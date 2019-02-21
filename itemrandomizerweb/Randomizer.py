import sys, random, time
from itemrandomizerweb.Items import ItemManager
from parameters import Knows, Settings, samus, infinity
from itemrandomizerweb.stdlib import List
from smbool import SMBool
from helpers import Bosses, diffValue2txt
from utils import randGaussBounds, getRangeDict, chooseFromRange
from graph import AccessGraph
from graph_access import accessPoints
from smboolmanager import SMBoolManager
from vcr import VCR
import log, logging

progSpeeds = ['slowest', 'slow', 'medium', 'fast', 'fastest', 'basic']

class RandoSettings(object):
    # maxDiff : max diff
    # progSpeed : slowest, slow, medium, fast, fastest, basic
    # progDiff : easier, normal, harder
    # qty : dictionary telling how many tanks and ammo will be distributed. keys are:
    #       'ammo': a dict with 'Missile', 'Super', 'PowerBomb' keys. relative weight of ammo distribution (ex:3/3/1)
    #       'energy' : can be 'sparse' (4-6 tanks), 'medium' (8-12 tanks), 'vanilla' (14 Etanks, 4 reserves)
    #       'minors' : percentage of ammo to distribute. 100 being vanilla
    # restrictions : item placement restrictions dict. values are booleans. keys :
    #                'Suits' : no suits early game
    #                'Morph' : Morph ball placement.
    #                          early to get it in the first two rooms.
    #                          late to get it after the beginning of the game (crateria/blue brinstar)
    #                          random for morph to be placed randomly.
    #                'MajorMinor' : if 'Major', will put major items in major locations, and minor items
    #                               in minor locations
    #                               if 'Chozo', will put major items in chozo locations, and minor items in others
    #                               if 'Full', no restriction
    # superFun : super fun settings list. can contain 'Movement', 'Combat', 'Suits'. Will remove random items
    # of the relevant categorie(s). This can easily cause aborted seeds, so some basic checks will be performed
    # beforehand to know whether an item can indeed be removed.
    # runtimeLimit_s : maximum runtime limit in seconds for generateItems functions. If <= 0, will be unlimited.
    def __init__(self, maxDiff, progSpeed, progDiff, qty, restrictions, superFun, runtimeLimit_s, vcr):
        self.progSpeed = progSpeed
        self.progDiff = progDiff
        self.maxDiff = maxDiff
        self.qty = qty
        self.restrictions = restrictions
        self.superFun = superFun
        self.runtimeLimit_s = runtimeLimit_s
        if self.runtimeLimit_s <= 0:
            self.runtimeLimit_s = sys.maxint
        self.vcr = vcr

    def getChooseLocs(self):
        return self.getChooseLocDict(self.progDiff)

    def getChooseItems(self, progSpeed=None):
        if progSpeed is None:
            progSpeed = self.progSpeed
        return self.getChooseItemDict(progSpeed)

    def getSpreadFactor(self, progSpeed):
        if progSpeed == 'slowest':
            return 0.9
        elif progSpeed == 'slow':
            return 0.7
        elif progSpeed == 'medium':
            return 0.4
        elif progSpeed == 'fast':
            return 0.1
        return 0

    def getChooseLocDict(self, progDiff):
        if progDiff == 'normal':
            return {
                'Random' : 1,
                'MinDiff' : 0,
                'MaxDiff' : 0
            }
        elif progDiff == 'easier':
            return {
                'Random' : 2,
                'MinDiff' : 1,
                'MaxDiff' : 0
            }
        elif progDiff == 'harder':
            return {
                'Random' : 2,
                'MinDiff' : 0,
                'MaxDiff' : 1
            }

    def getChooseItemDict(self, progSpeed):
        if progSpeed == 'slowest':
            return {
                'MinProgression' : 1,
                'Random' : 2,
                'MaxProgression' : 0
            }
        elif progSpeed == 'slow':
            return {
                'MinProgression' : 25,
                'Random' : 75,
                'MaxProgression' : 0
            }
        elif progSpeed == 'medium' or progSpeed == 'basic':
            return {
                'MinProgression' : 0,
                'Random' : 1,
                'MaxProgression' : 0
            }
        elif progSpeed == 'fast':
            return {
                'MinProgression' : 0,
                'Random' : 75,
                'MaxProgression' : 25
            }
        elif progSpeed == 'fastest':
            return {
                'MinProgression' : 0,
                'Random' : 2,
                'MaxProgression' : 1
            }

    def getPossibleSoftlockProb(self, progSpeed):
        if progSpeed == 'slowest':
            return 1
        if progSpeed == 'slow':
            return 0.66
        if progSpeed == 'medium':
            return 0.33
        if progSpeed == 'fast':
            return 0.1
        if progSpeed == 'fastest' or progSpeed == 'basic':
            return 0

    def getMinorHelpProb(self, progSpeed):
        if self.restrictions['MajorMinor'] != 'Major':
            return 0
        if progSpeed == 'slowest':
            return 0.16
        elif progSpeed == 'slow':
            return 0.33
        elif progSpeed == 'medium':
            return 0.5
        return 1

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
        return [] # basic speed

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
        elif progSpeed == 'basic':
            itemLimit = 0
        if self.restrictions['MajorMinor'] == 'Chozo':
            itemLimit /= 4
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
        elif progSpeed == 'basic':
            # locLimit is irrelevant for basic speed, as itemLimit is 0,
            # but we define it for chozo 2nd phase algorithm
            locLimit = 105
        return locLimit

# dat class name
class SuperFunProvider(object):
    # give the rando since we have to access services from it
    def __init__(self, superFun, itemManager, rando):
        self.superFun = superFun
        self.itemManager = itemManager
        self.rando = rando
        self.locations = rando.unusedLocations
        self.sm = self.rando.smbm
        self.areaGraph = self.rando.areaGraph
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
        self.log = log.get('SuperFun')

    def getItemPool(self, forbidden=[]):
        self.itemManager.setItemPool(self.basePool[:]) # reuse base pool to have constant base item set
        return self.itemManager.removeForbiddenItems(self.forbiddenItems + forbidden)

    def checkPool(self, forbidden=None):
        self.log.debug("forbidden=" + str(forbidden))
        ret = True
        if forbidden is not None:
            pool = self.getItemPool([forbidden])
        else:
            pool = self.getItemPool()
        self.log.debug('pool='+str(sorted([i['Type'] for i in pool])))
        # give us everything and beat every boss to see what we can access
        self.disableBossChecks()
        self.sm.resetItems()
        self.sm.addItems([item['Type'] for item in pool])
        for boss in self.bossChecks:
            Bosses.beatBoss(boss)
        # get restricted locs
        totalAvailLocs = [loc for loc in self.rando.currentLocations(post=True)]
        self.lastRestricted = [loc for loc in self.locations if loc not in totalAvailLocs]
        self.log.debug("restricted=" + str([loc['Name'] for loc in self.lastRestricted]))

        # check if we can reach all APs
        landingSite = self.areaGraph.accessPoints['Landing Site']
        availAccessPoints = self.areaGraph.getAvailableAccessPoints(landingSite, self.sm, self.rando.difficultyTarget)
        for apName, ap in self.areaGraph.accessPoints.iteritems():
            if not ap in availAccessPoints:
                ret = False
                self.log.debug("unavail AP: " + apName)

        # check if we can reach all bosses
        if ret:
            for loc in self.lastRestricted:
                if loc['Name'] in self.bossesLocs:
                    ret = False
                    self.log.debug("unavail Boss: " + loc['Name'])

        # cleanup
        self.sm.resetItems()
        Bosses.reset()
        self.restoreBossChecks()

        return ret

    def disableBossChecks(self):
        self.sm.enoughStuffsKraid = self.okay
        self.sm.enoughStuffsPhantoon = self.okay
        self.sm.enoughStuffsDraygon = self.okay
        self.sm.enoughStuffsRidley = self.okay
        self.sm.enoughStuffsMotherbrain = self.okay

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
        remove = []
        n = randGaussBounds(len(itemList))
        for i in range(n):
            idx = random.randint(0, len(itemList) - 1)
            item = itemList.pop(idx)
            if item is not None:
                remove.append(item)
        return remove

    def addForbidden(self, removable):
        forb = self.getForbiddenItemsFromList(removable)
        self.forbiddenItems += forb
        self.checkPool()
        self.addRestricted()
        return len(forb)

    def getForbiddenSuits(self):
        self.log.debug("getForbiddenSuits BEGIN. forbidden="+str(self.forbiddenItems))
        removableSuits = [suit for suit in self.suits if self.checkPool(suit)]
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
        removableMovement = [mvt for mvt in self.movementItems if self.checkPool(mvt)]
        if len(removableMovement) > 0:
            # remove at least the most important
            self.forbiddenItems.append(removableMovement.pop(0))
            self.addForbidden(removableMovement + [None])
        else:
            self.errorMsgs.append('Could not remove any movement item')
        self.log.debug("getForbiddenMovement END. forbidden="+str(self.forbiddenItems))

    def getForbiddenCombat(self):
        self.log.debug("getForbiddenCombat BEGIN. forbidden="+str(self.forbiddenItems))
        removableCombat = [cbt for cbt in self.combatItems if self.checkPool(cbt)]
        if len(removableCombat) > 0:
            fake = [None, None] # placeholders to avoid tricking the gaussian into removing too much stuff
            # do not remove screw if morph placement is late FIXME : this is nasty, but is due to simplistice morph placement restriction implementation
            if self.rando.restrictions['Morph'] == 'late':
                removableCombat.pop(0)
                fake.pop()
            if len(removableCombat) > 0:
                # remove at least one if possible (will be screw or plasma)
                self.forbiddenItems.append(removableCombat.pop(0))
            # if plasma is still available, remove it as well
            if len(removableCombat) > 0 and removableCombat[0] == 'Plasma':
                self.forbiddenItems.append(removableCombat.pop(0))
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

# current state of randomizer algorithm. can be saved and restored at any point.
# useful to rollback state when algorithm is stuck
class RandoState(object):
    # get state from randomizer object
    # rando: Randomizer instance
    # curLocs: current accessible locations at the time
    def __init__(self, rando, curLocs):
        self.unusedLocations = rando.unusedLocations[:]
        self.itemPool = rando.itemPool[:]
        self.chozoItemPool = rando.chozoItemPool[:]
        self.nonChozoItemPool = rando.nonChozoItemPool[:]
        self.curAccessPoint = rando.curAccessPoint
        self.currentItems = rando.currentItems[:]
        self.itemLocations = rando.itemLocations[:]
        self.states = rando.states[:]
        self.progressionItemLocs = rando.progressionItemLocs[:]
        self.progressionStatesIndices = rando.progressionStatesIndices[:]
        self.hadChozoLeft = rando.hadChozoLeft
        self.bosses = [boss for boss in Bosses.golden4Dead if Bosses.golden4Dead[boss] == True]
        self.curLocs = curLocs

    # apply this state to a randomizer object
    def apply(self, rando):
        rando.unusedLocations = self.unusedLocations[:]
        rando.currentItems = self.currentItems[:]
        rando.itemLocations = self.itemLocations[:]
        rando.setCurAccessPoint(self.curAccessPoint)
        rando.states = self.states[:]
        rando.itemPool = self.itemPool[:]
        rando.chozoItemPool = self.chozoItemPool[:]
        rando.nonChozoItemPool = self.nonChozoItemPool[:]
        rando.progressionStatesIndices = self.progressionStatesIndices[:]
        rando.progressionItemLocs = self.progressionItemLocs[:]
        rando.hadChozoLeft = self.hadChozoLeft
        rando.smbm.resetItems()
        rando.smbm.addItems([item['Type'] for item in self.currentItems])
        Bosses.reset()
        for boss in self.bosses:
            Bosses.beatBoss(boss)
        rando.resetCache()

# randomizer algorithm main class. generateItems method will generate a complete seed, or fail (depending on settings) 
class Randomizer(object):
    # locations : items locations
    # settings : RandoSettings instance
    def __init__(self, locations, settings, seedName, graphTransitions, bidir=True, dotDir=None):
        self.errorMsg = ''
        # create graph
        dotFile = None
        if dotDir is not None:
            dotFile = dotDir + '/' + seedName + ".dot"
        self.areaGraph = AccessGraph(accessPoints, graphTransitions, bidir, dotFile)
        # process settings
        self.log = log.get('Rando')

        self.settings = settings
        self.chooseItemFuncs = {
            'Random' : self.chooseItemRandom,
            'MinProgression' : self.chooseItemMinProgression,
            'MaxProgression' : self.chooseItemMaxProgression
        }
        self.chooseLocFuncs = {
            'Random' : self.chooseLocationRandom,
            'MinDiff' : self.chooseLocationMinDiff,
            'MaxDiff' : self.chooseLocationMaxDiff
        }
        self.chooseLocRanges = getRangeDict(settings.getChooseLocs())
        self.restrictions = settings.restrictions
        self.difficultyTarget = settings.maxDiff
        self.runtimeLimit_s = settings.runtimeLimit_s
        # init everything
        self.smbm = SMBoolManager()
        self.unusedLocations = locations
        # collected items
        self.currentItems = []
        # items, locs and area caches
        self.resetCache()
        # start at landing site
        self.curAccessPoint = None
        self.curLocs = None
        self.setCurAccessPoint()
        # states saved at each item collection
        self.states = []
        # indices in states list that mark a progression item collection
        self.progressionStatesIndices = []
        self.progressionItemLocs = []
        # progression items tried for a given rollback point
        self.rollbackItemsTried = {}
        # handle super fun settings
        self.itemPool = None
        itemManager = ItemManager(self.restrictions['MajorMinor'], settings.qty, self.smbm)
        fun = SuperFunProvider(settings.superFun, itemManager, self)
        fun.getForbidden()
        # check if we can reach everything
        self.log.debug("LAST CHECKPOOL")
        if not fun.checkPool():
            raise RuntimeError('Invalid transitions')
        # store unapplied super fun messages
        if len(fun.errorMsgs) > 0:
            self.errorMsg += "Super Fun: " + ', '.join(fun.errorMsgs) + ' '
        self.itemPool = fun.getItemPool()
        self.chozoItemPool = []
        self.nonChozoItemPool = []
        # temporarily swap item pool in chozo mode, until all chozo item are placed in chozo locs
        if self.restrictions['MajorMinor'] == 'Chozo':
            self.chozoItemPool = [item for item in self.itemPool if item['Class'] == 'Chozo' or item['Name'] == 'Boss']
            self.nonChozoItemPool = [item for item in self.itemPool if item not in self.chozoItemPool] # this will be swapped back
            self.log.debug('pools. c=%d, n=%d, t=%d' % (len(self.chozoItemPool), len(self.nonChozoItemPool), len(self.itemPool)))
            self.itemPool = self.chozoItemPool
        self.restrictedLocations = fun.restrictedLocs
        self.vcr = VCR(seedName, 'rando') if settings.vcr == True else None

    def resetCache(self):
        self.nonProgTypesCache = []
        self.progTypesCache = []
        self.curLocs = None
        self.curAccessPoints = None

    # with the new chozo split the tests change, a loc can have one or two classes, an item just one
    def isLocMajor(self, loc):
        return self.restrictions['MajorMinor'] == "Full" or self.restrictions['MajorMinor'] in loc['Class']

    def isLocMinor(self, loc):
        return self.restrictions['MajorMinor'] == "Full" or self.restrictions['MajorMinor'] not in loc['Class']

    def isItemMajor(self, item):
        if self.restrictions['MajorMinor'] == "Full":
            return False
        else:
            return item['Class'] == self.restrictions['MajorMinor']

    def isItemMinor(self, item):
        return item['Class'] == "Minor"

    def isItemLocMatching(self, loc, item):
        if self.restrictions['MajorMinor'] in loc['Class']:
            return item['Class'] == self.restrictions['MajorMinor']
        else:
            return item['Class'] == "Minor"

    # determine randomizer parameters, either statically (all speeds but variable), or dynamically (variable speed)
    def determineParameters(self):
        speed = self.settings.progSpeed
        if speed == 'variable':
            speed = progSpeeds[random.randint(0, len(progSpeeds)-1)]
        self.spreadProb = self.settings.getSpreadFactor(speed)
        self.minorHelpProb = self.settings.getMinorHelpProb(speed)
        self.chooseItemRanges = getRangeDict(self.settings.getChooseItems(speed))
        self.itemLimit = self.settings.getItemLimit(speed)
        self.locLimit = self.settings.getLocLimit(speed)
        self.progressionItemTypes = self.settings.getProgressionItemTypes(speed)
        self.possibleSoftlockProb = self.settings.getPossibleSoftlockProb(speed)

    def setCurAccessPoint(self, ap='Landing Site'):
        if ap != self.curAccessPoint:
            self.curAccessPoint = ap
            self.log.debug('current AP: {}'.format(ap))

    def locPostAvailable(self, loc, item):
        if not 'PostAvailable' in loc:
            return True
        result = self.smbm.eval(loc['PostAvailable'], item)
        return result.bool == True and result.difficulty <= self.difficultyTarget

    def getAvailLocs(self, locs, ap):
        availLocs = self.areaGraph.getAvailableLocations(locs,
                                                         self.smbm,
                                                         self.difficultyTarget,
                                                         ap)
        if self.restrictions['MajorMinor'] != 'Chozo' or self.difficultyTarget == infinity or not self.isChozoLeft():
            return availLocs
        # in chozo mode, we disable diff check for bosses/hardrooms/hellruns
        availLocsInf = self.areaGraph.getAvailableLocations(locs,
                                                            self.smbm,
                                                            infinity,
                                                            ap)
        def isAvail(loc):
            if 'Boss' in loc['Class']:
                return True
            for k in loc['difficulty'].knows:
                try:
                    diff = getattr(Knows, k)
                    if diff.difficulty > self.difficultyTarget:
                        return False
                except AttributeError:
                    # hard room/hell run
                    pass
            return True

        for loc in availLocsInf:
            if loc not in availLocs and isAvail(loc):
                availLocs.append(loc)

        return availLocs

    # get available locations, given current items, and an optional additional item.
    # uses graph method to get avail locs.
    # item : optional additional item, or None
    # locs : base locations list. If None, self.unusedLocations will be used.
    # ap : access point name. if None, self.curAccessPoint will be used
    # post : if True, will also check post availability. Default is False. 
    # return available locations list.
    def currentLocations(self, item=None, locs=None, ap=None, post=False):
        isSimpleCall = item is None and locs is None and ap is None and post == False
        if self.curLocs is not None and isSimpleCall:
            return self.curLocs
        itemType = None
        if locs is None:
            locs = self.unusedLocations
        if item is not None:
            itemType = item['Type']
            self.smbm.addItem(itemType)
        if ap is None:
            ap = self.curAccessPoint
        ret = sorted(self.getAvailLocs(locs, ap),
                     key=lambda loc: loc['Name'])
        if post is True:
            ret = [loc for loc in ret if self.locPostAvailable(loc, itemType)]
        if item is not None:
            self.smbm.removeItem(itemType)
        if isSimpleCall:
            self.curLocs = ret

        return ret

    def currentAccessPoints(self, item=None, ap=None):
        isSimpleCall = item is None and (ap is None or ap == self.curAccessPoint)
        if self.curAccessPoints is not None and isSimpleCall:
            return self.curAccessPoints
        if item is not None:
            itemType = item['Type']
            self.smbm.addItem(itemType)
        if ap is None:
            ap = self.curAccessPoint
        nodes = sorted(self.areaGraph.getAvailableAccessPoints(self.areaGraph.accessPoints[ap],
                                                               self.smbm, self.difficultyTarget),
                       key=lambda ap: ap.Name)
        if item is not None:
            self.smbm.removeItem(itemType)
        if isSimpleCall:
            self.curAccessPoints = nodes

        return nodes

    # for an item check if a least one location can accept it, given the current
    # placement restrictions
    #
    # item: dict of an item
    # locs: list of locations
    #
    # return bool
    def canPlaceItem(self, item, locs):
        return List.exists(lambda loc: self.canPlaceAtLocation(item, loc), locs)

    # organize an item pool in a type-indexed dictionary
    def getPoolDict(self, pool):
        poolDict = {}
        for item in pool:
            if item['Type'] not in poolDict:
                poolDict[item['Type']] = []
            poolDict[item['Type']].append(item)
        return poolDict

    # loop on all the items in the item pool of not already placed
    # items and return those that open up new locations.
    #
    # curLocs: accessible locations
    # itemPool: list of the items not already placed
    #
    # return list of items eligible for next placement
    def possibleItems(self, curLocs, itemPool):
        result = []
        poolDict = self.getPoolDict(itemPool)
        for itemType,items in poolDict.iteritems():
            if self.checkItem(items[0]):
                for item in items:
                    result.append(item)
        random.shuffle(result)
        return result

    # removes an item of given type from the pool.
    def removeItem(self, itemType, pool=None):
        if pool is None:
            pool = self.itemPool
        item = self.getNextItemInPool(itemType, pool)
        pool.remove(item)

    # get choose function from a weighted dict
    def getChooseFunc(self, rangeDict, funcDict):
        v = chooseFromRange(rangeDict)

        return funcDict[v]

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
        self.log.debug("RANDOM")
        self.log.debug("chooseLocationRandom: {}".format([l['Name'] for l in availableLocations]))
        return availableLocations[random.randint(0, len(availableLocations)-1)]

    def getLocDiff(self, loc):
        # avail difficulty already stored by graph algorithm        
        return loc['difficulty']

    def fillLocsDiff(self, locs):
        for loc in locs:
            if 'PostAvailable' in loc:
                loc['difficulty'] = self.smbm.wand(self.getLocDiff(loc), self.smbm.eval(loc['PostAvailable']))

    def chooseLocationMaxDiff(self, availableLocations, item):
        self.log.debug("MAX")
        self.fillLocsDiff(availableLocations)
        self.log.debug("chooseLocationMaxDiff: {}".format([(l['Name'], l['difficulty']) for l in availableLocations]))
        return max(availableLocations, key=lambda loc:loc['difficulty'].difficulty)

    def chooseLocationMinDiff(self, availableLocations, item):
        self.log.debug("MIN")
        self.fillLocsDiff(availableLocations)
        self.log.debug("chooseLocationMinDiff: {}".format([(l['Name'], l['difficulty']) for l in availableLocations]))
        return min(availableLocations, key=lambda loc:loc['difficulty'].difficulty)

    def areaDistanceProp(self, loc, otherLocs, prop):
        areas = [l[prop] for l in otherLocs]
        cnt = areas.count(loc[prop])
        d = None
        if cnt == 0:
            d = 2
        else:
            d = 1.0/cnt
        return d

    # gives a general "distance" of a particular location compared to other locations
    def areaDistance(self, loc, otherLocs):
        return self.areaDistanceProp(loc, otherLocs, 'Area')

    def getLocsSpreadProgression(self, availableLocations):
        progLocs = [il['Location'] for il in self.progressionItemLocs if self.restrictions["MajorMinor"] == il['Item']['Class'] and il['Item']['Category'] != "Energy"]
        distances = [self.areaDistance(loc, progLocs) for loc in availableLocations]
        maxDist = max(distances)
        indices = [index for index, d in enumerate(distances) if d == maxDist]
        locs = [availableLocations[i] for i in indices]

        return locs

    def hasItemType(self, t):
        return self.hasItemTypeInPool(t, self.currentItems)

    def hasItemTypeInPool(self, t, pool=None):
        if pool is None:
            pool = self.itemPool
        return any(item['Type'] == t for item in pool)

    def isJunk(self, item):
        if item['Type'] in ['Nothing', 'NoEnergy']:
            return True
    
    def isProgItemNow(self, item):
        if self.isJunk(item):
            return False
        if item['Type'] in self.progTypesCache:
            return True
        if item['Type'] in self.nonProgTypesCache:
            return False
        isProg = self.checkItem(item)
        if isProg == False and item['Type'] not in self.nonProgTypesCache:
            self.nonProgTypesCache.append(item['Type'])
        elif isProg == True and item['Type'] not in self.progTypesCache:
            self.progTypesCache.append(item['Type'])
        return isProg

    def isProgItem(self, item):
        if self.isJunk(item):
            return False
        if item['Type'] in self.progressionItemTypes:
            return True
        return self.isProgItemNow(item)

    def chooseLocation(self, availableLocations, item):
        locs = availableLocations
        isProg = self.isProgItem(item)
        if isProg == True and random.random() < self.spreadProb:
            locs = self.getLocsSpreadProgression(availableLocations)
        random.shuffle(locs)
        self.log.debug("chooseLocation isProg: {}".format(isProg))
        if isProg == True:
            return self.getChooseFunc(self.chooseLocRanges, self.chooseLocFuncs)(locs, item)
        else:
            # choose randomly if non-progression
            return self.chooseLocationRandom(locs, item)

    # items: possible items to place that will open up new paths, or an empty list
    # itemPool: non-placed items
    #
    # return if items is non-empty, item to place based on choose
    # function. if items is empty, a random non-placed item.
    def getItemToPlace(self, items, itemPool):
        itemsLen = len(items)
        if itemsLen == 0:
            fixedPool = [item for item in itemPool if item not in self.failItems]
            item = List.item(random.randint(0, len(fixedPool)-1), fixedPool)
        else:
            item = self.chooseItem(items)
        return item

    # items: possible items to place that will open up new paths, or an empty list
    # itemPool: non-placed items
    # locations: locations available
    #
    # returns a dict with the item and the location
    def placeItem(self, items, itemPool, locations):
        item = self.getItemToPlace(items, itemPool)
        locations = [loc for loc in locations if self.locPostAvailable(loc, item['Type'])]
        # if a loc is available we trigger pick up action, to make more locs available afterwards
        for loc in locations:
            if 'Pickup' in loc:
                self.log.debug("PICKUP call for: {}".format(loc['Name']))
                loc['Pickup']()
        availableLocations = List.filter(lambda loc: self.canPlaceAtLocation(item, loc, checkSoftlock=True), locations)
        if len(availableLocations) == 0:
            if not item in self.failItems:
                self.failItems.append(item)
            return None
        self.log.debug("placeItem: availLocs={}".format([l['Name'] for l in availableLocations]))
        location = self.chooseLocation(availableLocations, item)

        return {'Item': item, 'Location': location}

    # checks if an item opens up new locations.
    # curLocs : currently available locations
    # item : item to check
    #
    # return bool
    def checkItem(self, item):
        # no need to test nothing items
        if item['Category'] == 'Nothing':
            return False
        oldLocations = self.currentLocations()
        canPlaceIt = self.canPlaceItem(item, oldLocations)
        if canPlaceIt == False:
            return False
        newLocations = [loc for loc in self.currentLocations(item) if loc not in oldLocations]
        ret = len(newLocations) > 0
        if ret == True and self.restrictions["MajorMinor"] != "Full":
            ret = List.exists(lambda l: self.restrictions["MajorMinor"] in l["Class"], newLocations)
            if ret == False and self.restrictions["MajorMinor"] == "Major":
                # in major/minor split, still consider minor locs as progression if not all types are distributed
                ret = not self.hasItemType('Missile') or not self.hasItemType('Super') or not self.hasItemType('PowerBomb')

        return ret

    @staticmethod
    def isInBlueBrinstar(location):
        return location["Name"] in ["Morphing Ball",
                                    "Missile (blue Brinstar middle)",
                                    "Energy Tank, Brinstar Ceiling",
                                    "Power Bomb (blue Brinstar)",
                                    "Missile (blue Brinstar bottom)",
                                    "Missile (blue Brinstar top)",
                                    "Missile (blue Brinstar behind missile)"]

    @staticmethod
    def isSuit(item):
        return item['Type'] in ['Gravity', 'Varia']

    @staticmethod
    def isSpeedScrew(item):
        return item['Type'] in ['SpeedBooster', 'ScrewAttack']

    @staticmethod
    def isMorph(item):
        return item['Type'] == 'Morph'
    
    def suitsRestrictionsImpl(self, item, location):
        if item["Type"] == "Gravity":
            return ((not (location["Area"] == "Crateria" or location["Area"] == "Brinstar"))
                    or location["Name"] == "X-Ray Scope" or location["Name"] == "Energy Tank, Waterway")
        elif item["Type"] == "Varia":
            return not (location["Area"] == "Crateria" or Randomizer.isInBlueBrinstar(location))

        return True

    def speedScrewRestrictionImpl(self, item, location):
        return not Randomizer.isInBlueBrinstar(location)

    def morphPlacementImpl(self, item, location):
        return location['GraphArea'] != 'Crateria'

    # is softlock possible from the player POV when checking the loc?
    # usually these locs are checked last when playing, so placing
    # an important item there has an impact on progression speed
    def isSoftlockPossible(self, item, loc):
        if loc['Name'] == 'Bomb':
            # disable check for bombs as it is the beginning
            return False
        # if the loc forces us to go to an area we can't come back from
        comeBack = self.areaGraph.canAccess(self.smbm, loc['accessPoint'], self.curAccessPoint, self.difficultyTarget, item['Type'])
        if not comeBack:
            return True
        if self.isProgItemNow(item) and random.random() >= self.possibleSoftlockProb: # depends on prog speed
            # we know that loc is avail and post avail with the item
            # if it is not post avail without it, then the item prevents the
            # possible softlock
            if not self.locPostAvailable(loc, None):
                return True
            # item allows us to come back from a softlock possible zone
            comeBackWithout = self.areaGraph.canAccess(self.smbm, loc['accessPoint'], self.curAccessPoint, self.difficultyTarget, None)
            if not comeBackWithout:
                return True

        return False

    def isChozoLeft(self):
        return self.itemPool is not None and any(item['Class'] == 'Chozo' or item['Name'] == 'Boss' for item in self.itemPool)

    def locClassCheck(self, item, location):
        # in chozo mode, place chozo items first so the seed is
        # theoretically finishable without checking any other location
        if self.restrictions['MajorMinor'] == 'Chozo':
            if self.isChozoLeft():
                return 'Chozo' == item['Class'] and 'Chozo' in location['Class']
            else:
                return True

        if self.restrictions['MajorMinor'] != "Full":
            return self.isItemLocMatching(location, item)

        return True

    # check if an item can be placed at a location, given restrictions
    # settings.
    def canPlaceAtLocation(self, item, location, checkSoftlock=False):
        if item['Type'] == 'Boss':
            return 'Boss' in location['Class']

        if 'Boss' in location['Class']:
            return item['Type'] == 'Boss'

        if not self.locClassCheck(item, location):
            return False

        if self.restrictions['Suits'] == True and Randomizer.isSuit(item):
            return self.suitsRestrictionsImpl(item, location)

        if self.restrictions['Morph'] == 'early' and Randomizer.isSpeedScrew(item):
            return self.speedScrewRestrictionImpl(item, location)

        if self.restrictions['Morph'] == 'late' and Randomizer.isMorph(item):
            return self.morphPlacementImpl(item, location)

        if checkSoftlock == True:
            return not self.isSoftlockPossible(item, location)

        return True

    # from current accessible locations and an item pool, generate an item/loc dict.
    # return item/loc, or None if stuck
    def generateItem(self, curLocs, pool):
        itemLocation = None
        self.failItems = []
        posItems = self.possibleItems(curLocs, pool)
        self.log.debug("posItems: {}".format([i['Name'] for i in posItems]))
        if len(posItems) > 0:
            # if posItems is not empty, only those in posItems will be tried (see placeItem)
            nPool = len(set([item['Type'] for item in posItems]))
        else:
            # if posItems is empty, all items in the pool will be tried (see placeItem)
            nPool = len(set([item['Type'] for item in pool]))
        while itemLocation is None and len(self.failItems) < nPool:
            self.log.debug("P " + str(len(posItems)) + ", F " + str(len(self.failItems)) + " / " + str(nPool))
            itemLocation = self.placeItem(posItems, pool, curLocs)
        return itemLocation

    def appendCurrentState(self, curLocs):
        curState = RandoState(self, curLocs)
        self.log.debug('appendCurrentState ' + str(curState) + ' at ' + str(len(self.states)))
        self.states.append(curState)
        curState.states.append(curState)

    # actually get an item/loc.
    # itemLocation: item/loc to get
    # collect: actually collect item. defaults to True. use False for unreachable items.
    # pool : base item pool. If None (default), uses self.itemPool.
    # showDot : if True (default), outputs a dot on stdout
    def getItem(self, itemLocation, collect=True, pool=None, showDot=True):
        if pool is None:
            pool = self.itemPool
        if showDot == True:
            sys.stdout.write('.')
            sys.stdout.flush()
        item = itemLocation['Item']
        location = itemLocation['Location']
        curLocs = None
        isProg = self.isProgItemNow(item)
        if collect == True:
            # walk the graph one last time to get proper access point and store with the state
            curLocs = self.currentLocations(item)
            self.log.debug("getItem: loc: {} ap: {}".format(location['Name'], location['accessPoint']))
            self.setCurAccessPoint(location['accessPoint'])
            self.currentItems.append(item)
            self.smbm.addItem(item['Type'])

            if self.vcr != None:
                self.vcr.addLocation(location['Name'], item['Type'])

        self.unusedLocations.remove(location)
        self.itemLocations.append(itemLocation)
        if curLocs != None:
            self.log.debug("PLACEMENT {}: {} at {} diff: {}, locs: {}".format(len(self.currentItems), item['Type'], location['Name'], location['difficulty'], len(curLocs)-1))
            self.log.debug("Path: {}".format([ap.Name for ap in location['path']]))
        self.removeItem(item['Type'], pool)
        if collect == True:
            if isProg == True:
                n = len(self.states)
                self.log.debug("prog indice="+str(n))
                self.progressionStatesIndices.append(n)
                self.progressionItemLocs.append(itemLocation)
            if location in curLocs:
                curLocs.remove(location)
            self.resetCache()
            self.appendCurrentState(curLocs)

    # check if remaining locations pool is conform to rando settings when filling up
    # with non-progression items
    def checkLocPool(self):
 #       self.log.debug("checkLocPool {}".format([it['Name'] for it in self.itemPool]))
        progItems = [item for item in self.itemPool if self.isProgItem(item)]
        self.log.debug("progItems {}".format([it['Name'] for it in progItems]))
 #       self.log.debug("curItems {}".format([it['Name'] for it in self.currentItems]))
        if len(progItems) == 0 or self.locLimit <= 0:
            return True
        isMinorProg = any(self.isItemMinor(item) for item in progItems)
        isMajorProg = any(self.isItemMajor(item) for item in progItems)
        accessibleLocations = []
#        self.log.debug("unusedLocs: {}".format([loc['Name'] for loc in self.unusedLocations]))
        locs = self.currentLocations()
        for loc in locs:
            majAvail = self.isLocMajor(loc)
            minAvail = self.isLocMinor(loc)
            if ((isMajorProg and majAvail) or (isMinorProg and minAvail)) \
               and self.locPostAvailable(loc, None):
                accessibleLocations.append(loc)
        self.log.debug("accesLoc {}".format([loc['Name'] for loc in accessibleLocations]))
        if len(accessibleLocations) <= self.locLimit:
            sys.stdout.write('|')
            sys.stdout.flush()
            return False
        # check that there is room left in all main areas
        room = {'Brinstar' : 0, 'Norfair' : 0, 'WreckedShip' : 0, 'LowerNorfair' : 0, 'Maridia' : 0 }
        for loc in self.unusedLocations:
            majAvail = self.isLocMajor(loc)
            minAvail = self.isLocMinor(loc)
            if loc['Area'] in room and ((isMajorProg and majAvail) or (isMinorProg and minAvail)):
                room[loc['Area']] += 1
        for r in room.values():
            if r > 0 and r <= self.locLimit:
                sys.stdout.write('|')
                sys.stdout.flush()
                return False
        return True

    def getNonProgItemPool(self, basePool=None):
        if basePool is None:
            basePool = self.itemPool
        pool = [item for item in basePool if not self.isProgItem(item)]

        # enabled only in major/minor split, and depends on prog speed
        if random.random() < self.minorHelpProb:
            helpfulMinors = [item for item in basePool if item['Class'] == 'Minor' and not self.hasItemTypeInPool(item['Type'], pool)]
            if len(helpfulMinors) > 0:
                pool.append(helpfulMinors[random.randint(0, len(helpfulMinors)-1)])
        # don't hold energy back for certain settings
        if (self.restrictions['MajorMinor'] == 'Chozo' or (self.restrictions['MajorMinor'] == 'Major' and self.settings.qty['energy'] == 'vanilla'))\
            and not any(item['Category'] == 'Energy' for item in pool):
            pool += [item for item in basePool if item['Category'] == 'Energy']
        return pool

    # return True if stuck, False if not
    def fillNonProgressionItems(self):
        if self.itemLimit <= 0:
            return False
        pool = self.getNonProgItemPool()
        poolTypes = list(set([item['Type'] for item in pool]))
        self.log.debug("fillNonProgressionItems poolset=" + str(poolTypes))
        poolWasEmpty = len(pool) == 0 or poolTypes == ['Boss']
        itemLocation = None
        nItems = 0
        locPoolOk = True
        self.log.debug("NON-PROG")
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
                self.log.debug("fillNonProgressionItems: {} at {}".format(itemLocation['Item']['Name'], itemLocation['Location']['Name']))
                self.getItem(itemLocation)
                pool = [item for item in self.itemPool if not self.isProgItem(item)]
            locPoolOk = self.checkLocPool()
        isStuck = not poolWasEmpty and itemLocation is None
        return isStuck

    # return True if stuck, False if not
    def getItemFromStandardPool(self):
        curLocs = self.currentLocations()
        self.log.debug("getItemFromStandardPool: I:{} L:{}".format([i['Name'] for i in self.itemPool],[l['Name'] for l in curLocs if self.restrictions['MajorMinor'] != 'Chozo' or not self.isChozoLeft() or 'Chozo' in l['Class']]))
        itemLocation = self.generateItem(curLocs, self.itemPool)
        isStuck = itemLocation is None
        if not isStuck:
            sys.stdout.write('-')
            sys.stdout.flush()
            self.log.debug("getItemFromStandardPool: {} at {}".format(itemLocation['Item']['Name'], itemLocation['Location']['Name']))
            self.getItem(itemLocation)
        return isStuck

    def initRollbackPoints(self):
        minRollbackPoint = 0
        maxRollbackPoint = len(self.states) - 1
        if len(self.progressionStatesIndices) > 0:
            minRollbackPoint = self.progressionStatesIndices[-1]
        self.log.debug('initRollbackPoints: min=' + str(minRollbackPoint) + ", max=" + str(maxRollbackPoint))
        return minRollbackPoint, maxRollbackPoint

    def initRollback(self):
        self.states.pop() # last state is current state, so it's useless
        self.log.debug('initRollback: progressionStatesIndices 1=' + str(self.progressionStatesIndices))
        if len(self.progressionStatesIndices) > 0 and self.progressionStatesIndices[-1] == len(self.states):
            # the state we just removed was a progression state (highly unlikely, but let's be safe)
            self.progressionStatesIndices.pop()
        self.log.debug('initRollback: progressionStatesIndices 2=' + str(self.progressionStatesIndices))

    def getSituationId(self):
        progItems = str(sorted([il['Item']['Type'] for il in self.progressionItemLocs]))
        position = str(sorted([ap.Name for ap in self.currentAccessPoints()]))
        return progItems+'/'+position

    def hasTried(self, itemLoc):
        # disable tried check if we don't have morph+unlocking ammo
        sm = self.smbm
        if sm.canUsePowerBombs().bool == False or sm.canOpenGreenDoors().bool == False:
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
        nItemsAtStart = len(self.currentItems)
        nStatesAtStart = len(self.states)
        self.log.debug("rollback BEGIN: nItems={}, nStates={}".format(len(self.currentItems), nStatesAtStart))
        self.initRollback()
        if len(self.states) == 0:
            self.initState.apply(self)
            self.log.debug("rollback END initState apply, nCurLocs="+str(len(self.currentLocations())))
            return None
        # to stay consistent in case no solution is found as states list was popped in init
        ret = None
        fallbackState = self.states[-1]
        # we can be in a 'fake rollback' situation where we rollback
        # just after non prog phase without checking normal items first (we
        # do this for more randomness, to avoid placing items in postavail locs
        # like spospo etc. too often).
        # if so, we won't go back further a prog item if first rollback fails
        # (fallback state will be applied instead)
        isFakeRollback = self.generateItem(self.currentLocations(), self.itemPool) is not None
        i = 0
        possibleStates = []
        while i >= 0 and len(possibleStates) == 0:
            states = self.states[:]
            minRollbackPoint, maxRollbackPoint = self.initRollbackPoints()
            i = maxRollbackPoint
            while i >= minRollbackPoint and len(possibleStates) < 3:
                state = states[i]
                state.apply(self)
                posItems = self.possibleItems(state.curLocs, self.itemPool)
                if len(posItems) > 0: # new locs can be opened
#                    self.log.debug([item['Type'] for item in posItems])
#                    self.log.debug([loc['Name'] for loc in state.curLocs])
                    itemLoc = self.generateItem(state.curLocs, self.itemPool)
                    if itemLoc is not None and (isFakeRollback == True or not self.hasTried(itemLoc)):
                        possibleStates.append((state, itemLoc))
                i -= 1
            # nothing, let's rollback further a progression item
            if len(possibleStates) == 0 and i >= 0:
                if isFakeRollback == False:
                    sys.stdout.write('!')
                    sys.stdout.flush()
                    self.progressionStatesIndices.pop()
                else:
                    break
        if len(possibleStates) > 0:
            (state, itemLoc) = possibleStates[random.randint(0, len(possibleStates)-1)]
            self.updateRollbackItemsTried(itemLoc)
            state.apply(self)
            ret = itemLoc

            if self.vcr != None:
                self.vcr.addRollback(nItemsAtStart - len(self.currentItems))
        else:
            # we end up here if rollback failed or fake rollback was asked
            self.log.debug('fallbackState apply')
            fallbackState.apply(self)
        sys.stdout.write('<'*(nStatesAtStart - len(self.states)))
        sys.stdout.flush()
        self.log.debug("rollback END: {}".format(len(self.currentItems)))
        return ret

    # check if bosses are blocking the last remaining locations
    def onlyBossesLeft(self, bossesKilled):
        self.log.debug('onlyBossesLeft, diff=' + str(self.difficultyTarget))
        prevLocs = self.currentLocations(post=True)
        # fake kill all bosses and see if we can access the rest of the game
        Bosses.reset()
        for boss in ['Kraid', 'Phantoon', 'Ridley', 'Draygon']:
            Bosses.beatBoss(boss)
        # get bosses locations and newly accessible locations (for bosses that open up locs)
        newLocs = self.currentLocations(post=True)
        locs = newLocs + [loc for loc in self.unusedLocations if 'Boss' in loc['Class'] and not loc in newLocs]
        ret = (len(locs) > len(prevLocs) and len(locs) == len(self.unusedLocations))
        # restore currently killed bosses
        Bosses.reset()
        for boss in bossesKilled:
            Bosses.beatBoss(boss)
        if ret == True and self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("onlyBossesLeft openedLocs: {}".format([loc['Name'] for loc in locs if loc not in prevLocs]))
            self.log.debug("current AP: {}".format(self.curAccessPoint))
            nodes = self.currentAccessPoints()
            self.log.debug("avail APs: {}".format([ap.Name for ap in nodes]))
            self.log.debug("curLocs: {}".format([loc['Name'] for loc in self.curLocs]))
        return ret

    # when max diff was stepped up due to boss fights, get a string that
    # tells locations above initial target and associated difficulties
    def getAboveMaxDiffLocsStr(self, maxDiff):
        locs = [il['Location'] for il in self.itemLocations if il['Location']['difficulty'].difficulty > maxDiff]
        return '[ ' + ' ; '.join([loc['Name'] + ': ' + diffValue2txt(loc['difficulty'].difficulty) for loc in locs]) + ' ]'

    # if not all items could be placed (the player cannot finish the seed 100%),
    # check if we can still finish the game (the player can finish the seed any%)
    def canEndGame(self):
        return not any(loc['Name'] == 'Mother Brain' for loc in self.unusedLocations)
        # itemTypes = [item['Type'] for item in self.currentItems]
        # return self.smbm.wand(Bosses.allBossesDead(self.smbm), self.smbm.enoughStuffTourian())

    def getNextItemInPool(self, t, pool=None):
        if pool is None:
            pool = self.itemPool
        return next(item for item in pool if item['Type'] == t)

    # fill up unreachable locations with "junk" to maximize the chance of the ROM
    # to be finishable
    def fillRestrictedLocations(self):
        isChozo = self.restrictions['MajorMinor'] == 'Chozo'
        for loc in self.restrictedLocations:
            isMajor = self.isLocMajor(loc)
            isMinor = self.isLocMinor(loc)
            if isChozo:
                if isMajor: # chozo loc
                    self.itemPool = self.chozoItemPool
                else:
                    self.itemPool = self.nonChozoItemPool
            itemLocation = {'Location' : loc}
            if isMinor and self.hasItemTypeInPool('Nothing'):
                itemLocation['Item'] = self.getNextItemInPool('Nothing')
            elif isMajor and self.hasItemTypeInPool('NoEnergy'):
                itemLocation['Item'] = self.getNextItemInPool('NoEnergy')
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
            self.log.debug("Fill: {} at {}".format(itemLocation['Item']['Type'], itemLocation['Location']['Name']))
            self.getItem(itemLocation, False)

        if isChozo:
            self.itemPool = self.chozoItemPool

    def getCurrentState(self):
        return self.states[-1]

    def chozoFill(self):
        # 2nd phase fill-up :
        # try to enforce max diff, with items compatible with prog speed
        curState = RandoState(self, self.currentLocations())
        allItemLocs = []
        states = [self.states[i] for i in self.progressionStatesIndices]
        self.log.debug("chozoFill, progs=" + str(self.progressionStatesIndices))
        for state in states:
            def chooseItem(pool):
                # choose item in the pool that brings the most collected locs to < diffTarget
                random.shuffle(pool)
                ret = None
                collectedLocs = [il['Location'] for il in self.itemLocations]
                def getAboveDiffLocs(locs):
                    return [loc for loc in locs if loc['difficulty'].difficulty > self.difficultyTarget]
                minLeftAbove = len(getAboveDiffLocs(collectedLocs))
                self.log.debug('minLeftAbove=' + str(minLeftAbove))
                if minLeftAbove == 0:
                    return pool[0]
                checkPool = []
                for item in pool:
                    if not any(i for i in checkPool if i['Type'] == item['Type']):
                        checkPool.append(item)
                for item in checkPool:
                    curLocs = self.currentLocations(item, collectedLocs)
                    n = len(getAboveDiffLocs(curLocs))
                    if n < minLeftAbove:
                        minLeftAbove = n
                        self.log.debug('item ' + item['Type'] + ' lowers minLeftAbove to ' + str(minLeftAbove))
                        ret = item
                if ret is None:
                    ret = pool[0]
                return ret
            def getLocs(locs):
                return [loc for loc in locs if 'Chozo' not in loc['Class'] and 'Boss' not in loc['Class']]
            def fillup(n, pool):
                self.log.debug('fillup-n=' + str(n) + ', pool_types=' + str(list(set([item['Type'] for item in pool]))))
                itemLocs = []
                for i in range(n):
                    curLocs = getLocs(self.currentLocations(ap='Landing Site'))
                    item = chooseItem(pool)
                    loc = curLocs[random.randint(0, len(curLocs)-1)]
                    il = {'Item':item, 'Location':loc}
                    self.log.debug('fillup ' + item['Type'] + ' at ' + loc['Name'])
                    self.getItem(il, pool=self.nonChozoItemPool)
                    itemLocs.append(il)
                    pool.remove(item)
                return itemLocs
            def updateCurrentState(itemLocs, curLocs, curState):
                self.log.debug('updateCurrentState BEGIN')
                curState.apply(self)
                for il in itemLocs:
                    self.getItem(il, showDot=False)
                    allItemLocs.append(il)
                self.log.debug('updateCurrentState END')
            # restore state to this point + all item locs we already put in the fillup
            state.apply(self)
            self.log.debug('state ' + str(state) + ' apply, nCurLocs='+str(len(self.currentLocations())))
            self.log.debug('collected1=' + str(list(set([i['Item']['Type'] for i in self.itemLocations]))))
            for il in allItemLocs:
                self.getItem(il, pool=self.nonChozoItemPool, showDot=False)
            # fill-up
            self.determineParameters()
            self.log.debug('collected2=' + str(list(set([i['Item']['Type'] for i in self.itemLocations]))))
            nonProg = self.getNonProgItemPool(self.nonChozoItemPool)
            lim = self.locLimit
            if lim < 0:
                lim = 0
            nLocsNonProg = len(getLocs(self.currentLocations())) - lim
            itemLocs = []
            if len(nonProg) > 0 and nLocsNonProg > 0:
                self.log.debug('nonProg fillup cur=' + str(len(self.currentLocations())) + ', nLocs=' + str(nLocsNonProg))
                itemLocs += fillup(min(nLocsNonProg, len(nonProg)), nonProg)
            allItems = self.nonChozoItemPool[:]
            nLocs = len(getLocs(self.currentLocations()))
            if len(allItems) > 0 and nLocs > 0:
                self.log.debug('allItems fillup cur=' + str(len(self.currentLocations())) + ', nLocs=' + str(nLocsNonProg))
                itemLocs += fillup(min(nLocs, len(allItems)), allItems)
            updateCurrentState(itemLocs, self.currentLocations(), curState)
            curState = RandoState(self, self.currentLocations())

    def chozoCheck(self):
        if self.restrictions['MajorMinor'] == 'Chozo':
            if not self.isChozoLeft() and self.hadChozoLeft:
                # filled all chozo locs, go back to normal placement
                self.log.debug('CHOZO SWAP')
                self.itemPool = self.nonChozoItemPool
                if self.prevDiffTarget is not None:
                    self.difficultyTarget = self.prevDiffTarget
                self.chozoFill()
            self.hadChozoLeft = self.isChozoLeft()

    # only function to use (once) from outside of the Randomizer class.
    # returns a list of item/location dicts with 'Item' and 'Location' as keys.
    def generateItems(self):
        stuck = False
        self.itemLocations = []
        isStuck = False
        # if major items are removed from the pool (super fun setting), fill not accessible locations with
        # items that are as useless as possible
        self.fillRestrictedLocations()
        self.curLocs = self.currentLocations()
        self.curAccessPoints = self.currentAccessPoints()
        self.hadChozoLeft = self.isChozoLeft()
        self.initState = RandoState(self, self.currentLocations())
        self.log.debug("{} items in pool".format(len(self.itemPool)))
        runtime_s = 0
        startDate = time.clock()
        self.prevDiffTarget = None
        while len(self.itemPool) > 0 and not isStuck and runtime_s <= self.runtimeLimit_s:
            # dynamic params determination (useful for variable speed)
            self.determineParameters()
            # fill up with non-progression stuff
            isStuck = self.fillNonProgressionItems()
            self.log.debug("non prog stuck = " + str(isStuck))
            self.chozoCheck()
            if len(self.itemPool) > 0:
                # collect an item with standard pool
                if not isStuck:
                    isStuck = self.getItemFromStandardPool()
                if isStuck:
                    # if we're stuck, check if only bosses locations are left (bosses difficulty settings problems)
                    onlyBosses = self.onlyBossesLeft(self.getCurrentState().bosses)
                    if not onlyBosses:
                        # check that we're actually stuck
                        nCurLocs = len(self.currentLocations())
                        nLocsLeft = len(self.unusedLocations)
                        itemLoc = None
                        # self.log.debug("nCurLocs={}, nLocsLeft={}".format(nCurLocs, nLocsLeft))
                        # self.log.debug("curLocs: {}".format([loc['Name'] for loc in self.states[-1].curLocs]))
                        # self.log.debug("unused: {}".format([loc['Name'] for loc in self.unusedLocations]))
                        if nCurLocs < nLocsLeft:
                            # stuck, rollback to make progress if we can't access everything yet
                            itemLoc = self.rollback()
                        if itemLoc is not None:
                            self.getItem(itemLoc)
                            isStuck = False
                        else:
                            isStuck = self.getItemFromStandardPool()
                    else:
                        # stuck by boss fights. disable max difficulty (warn the user afterwards)
                        if self.prevDiffTarget is None:
                            self.log.debug('RAISE MAX DIFF')
                            self.log.debug("aboveDiff: {}".format([loc['Name'] for loc in self.getCurrentState().curLocs if loc['difficulty'].difficulty > self.difficultyTarget]))
                            self.prevDiffTarget = self.difficultyTarget
                            self.difficultyTarget = infinity
                            self.resetCache()
                        isStuck = False
            self.chozoCheck()
            runtime_s = time.clock() - startDate
        self.log.debug("{} remaining items in pool".format(len(self.itemPool)))
        self.log.debug("nStates="+str(len(self.states)))
        self.log.debug('unusedLocs='+str([loc['Name'] for loc in self.unusedLocations]))
        if len(self.itemPool) > 0:
            # we could not place all items, check if we can finish the game
            if self.canEndGame():
                # seed is finishable, place randomly all remaining items
                while len(self.itemPool) > 0:
                    item = self.itemPool[0]
                    possibleLocs = [loc for loc in self.unusedLocations if self.canPlaceAtLocation(item, loc)]
                    self.log.debug("last fill item = " + item['Type'] + "/" + item['Class'] + ", locs = " + str([loc['Name'] for loc in possibleLocs]))
                    itemLocation = {
                        'Item' : item,
                        'Location' : possibleLocs[random.randint(0, len(possibleLocs) - 1)]
                    }
                    self.log.debug("last Fill: {} at {}".format(itemLocation['Item']['Type'], itemLocation['Location']['Name']))
                    self.getItem(itemLocation, False)
                self.chozoCheck()
            else:
                print("\nSTUCK ! ")
                print("REM LOCS = "  + str([loc['Name'] for loc in self.unusedLocations]))
                print("REM ITEMS = "  + str([item['Type'] for item in self.itemPool]))
                self.errorMsg += "Stuck because of navigation. Retry, and disable either super fun settings/late morph ball/suits restriction if the problem happens again."
                stuck = True
        if not stuck:
            maxDiff = self.prevDiffTarget
            if maxDiff is None:
                maxDiff = self.difficultyTarget
            locsDiffs = self.getAboveMaxDiffLocsStr(maxDiff)
            if locsDiffs != '[  ]':
                self.errorMsg += "Maximum difficulty could not be applied everywhere. Affected locations: {}".format(locsDiffs)
        if len(self.errorMsg) > 0:
            print("\nDIAG: {}".format(self.errorMsg))
        print("")

        if self.vcr != None:
            self.vcr.dump()

        return (stuck, self.itemLocations)
