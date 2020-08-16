from utils import randGaussBounds, getRangeDict, chooseFromRange
import log, logging, copy, random

class Item:
    __slots__ = ( 'Category', 'Class', 'Name', 'Code', 'Type' )

    def __init__(self, Category, Class, Name, Type, Code=None):
        self.Category = Category
        self.Class = Class
        self.Code = Code
        self.Name = Name
        self.Type = Type

    def withClass(self, Class):
        return Item(self.Category, Class, self.Name, self.Type, self.Code)

    def __eq__(self, other):
        # used to remove an item from a list
        return self.Type == other.Type and self.Class == other.Class

    def __hash__(self):
        # as we define __eq__ we have to also define __hash__ to use items as dictionnary keys
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        return id(self)

    def __repr__(self):
      return "Item({}, {}, {}, {}, {})".format(self.Category,
          self.Class, self.Code, self.Name, self.Type)

class ItemManager:
    Items = {
        'ETank': Item(
            Category='Energy',
            Class='Major',
            Code=0xeed7,
            Name="Energy Tank",
            Type='ETank',
        ),
        'Missile': Item(
            Category='Ammo',
            Class='Minor',
            Code=0xeedb,
            Name="Missile",
            Type='Missile',
        ),
        'Super': Item(
            Category='Ammo',
            Class='Minor',
            Code=0xeedf,
            Name="Super Missile",
            Type='Super',
        ),
        'PowerBomb': Item(
            Category='Ammo',
            Class='Minor',
            Code=0xeee3,
            Name="Power Bomb",
            Type='PowerBomb',
        ),
        'Bomb': Item(
            Category='Progression',
            Class='Major',
            Code=0xeee7,
            Name="Bomb",
            Type='Bomb',
        ),
        'Charge': Item(
            Category='Beam',
            Class='Major',
            Code=0xeeeb,
            Name="Charge Beam",
            Type='Charge',
        ),
        'Ice': Item(
            Category='Progression',
            Class='Major',
            Code=0xeeef,
            Name="Ice Beam",
            Type='Ice',
        ),
        'HiJump': Item(
            Category='Progression',
            Class='Major',
            Code=0xeef3,
            Name="Hi-Jump Boots",
            Type='HiJump',
        ),
        'SpeedBooster': Item(
            Category='Progression',
            Class='Major',
            Code=0xeef7,
            Name="Speed Booster",
            Type='SpeedBooster',
        ),
        'Wave': Item(
            Category='Beam',
            Class='Major',
            Code=0xeefb,
            Name="Wave Beam",
            Type='Wave',
        ),
        'Spazer': Item(
            Category='Beam',
            Class='Major',
            Code=0xeeff,
            Name="Spazer",
            Type='Spazer',
        ),
        'SpringBall': Item(
            Category='Misc',
            Class='Major',
            Code=0xef03,
            Name="Spring Ball",
            Type='SpringBall',
        ),
        'Varia': Item(
            Category='Progression',
            Class='Major',
            Code=0xef07,
            Name="Varia Suit",
            Type='Varia',
        ),
        'Plasma': Item(
            Category='Beam',
            Class='Major',
            Code=0xef13,
            Name="Plasma Beam",
            Type='Plasma',

        ),
        'Grapple': Item(
            Category='Progression',
            Class='Major',
            Code=0xef17,
            Name="Grappling Beam",
            Type='Grapple',
        ),
        'Morph': Item(
            Category='Progression',
            Class='Major',
            Code=0xef23,
            Name="Morph Ball",
            Type='Morph',
        ),
        'Reserve': Item(
            Category='Energy',
            Class='Major',
            Code=0xef27,
            Name="Reserve Tank",
            Type='Reserve',
        ),
        'Gravity': Item(
            Category='Progression',
            Class='Major',
            Code=0xef0b,
            Name="Gravity Suit",
            Type='Gravity',
        ),
        'XRayScope': Item(
            Category='Misc',
            Class='Major',
            Code=0xef0f,
            Name="X-Ray Scope",
            Type='XRayScope',
        ),
        'SpaceJump': Item(
            Category='Progression',
            Class='Major',
            Code=0xef1b,
            Name="Space Jump",
            Type='SpaceJump',
        ),
        'ScrewAttack': Item(
            Category='Misc',
            Class='Major',
            Code=0xef1f,
            Name="Screw Attack",
            Type='ScrewAttack',
        ),
        'Nothing': Item(
            Category='Nothing',
            Class='Minor',
            Code=0xeedb,
            Name="Nothing",
            Type='Nothing',
        ),
        'NoEnergy': Item(
            Category='Nothing',
            Class='Major',
            Code=0xeedb,
            Name="No Energy",
            Type='NoEnergy',
        ),
        'Kraid': Item(
            Category='Boss',
            Class='Boss',
            Name="Kraid",
            Type='Kraid',
        ),
        'Phantoon': Item(
            Category='Boss',
            Class='Boss',
            Name="Phantoon",
            Type='Phantoon'
        ),
        'Draygon': Item(
            Category='Boss',
            Class='Boss',
            Name="Draygon",
            Type='Draygon',
        ),
        'Ridley': Item(
            Category='Boss',
            Class='Boss',
            Name="Ridley",
            Type='Ridley',
        ),
        'MotherBrain': Item(
            Category='Boss',
            Class='Boss',
            Name="Mother Brain",
            Type='MotherBrain',
        ),
    }

    for itemType, item in Items.items():
      if item.Type != itemType:
        raise RuntimeError("Wrong item type for {} (expected {})".format(item, itemType))

    @staticmethod
    def isBeam(item):
        return item.Category == 'Beam' or item.Type == 'Ice'

    BeamBits = {
        'Wave'   : 0x1,
        'Ice'    : 0x2,
        'Spazer' : 0x4,
        'Plasma' : 0x8,
        'Charge' : 0x1000
    }

    ItemBits = {
        'Varia'        : 0x1,
        'SpringBall'   : 0x2,
        'Morph'        : 0x4,
        'ScrewAttack'  : 0x8,
        'Gravity'      : 0x20,
        'HiJump'       : 0x100,
        'SpaceJump'    : 0x200,
        'Bomb'         : 0x1000,
        'SpeedBooster' : 0x2000,
        'Grapple'      : 0x4000,
        'XRayScope'    : 0x8000
    }

    @staticmethod
    def getItemTypeCode(item, itemVisibility):
        if itemVisibility == 'Visible':
            modifier = 0
        elif itemVisibility == 'Chozo':
            modifier = 84
        elif itemVisibility == 'Hidden':
            modifier = 168

        itemCode = item.Code + modifier
        return itemCode

    def __init__(self, majorsSplit, qty, sm):
        self.qty = qty
        self.sm = sm
        self.majorsSplit = majorsSplit
        self.majorClass = 'Chozo' if majorsSplit == 'Chozo' else 'Major'
        self.itemPool = []

    def newItemPool(self, addBosses=True):
        self.itemPool = []
        if addBosses == True:
            # for the bosses
            for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
                self.addMinor(boss)

    def getItemPool(self):
        return self.itemPool

    def setItemPool(self, pool):
        self.itemPool = pool

    def addItem(self, itemType, itemClass=None):
        self.itemPool.append(ItemManager.getItem(itemType, itemClass))

    def addMinor(self, minorType):
        self.addItem(minorType, 'Minor')

    # remove from pool an item of given type. item type has to be in original Items list.
    def removeItem(self, itemType):
        for idx, item in enumerate(self.itemPool):
            if item.Type == itemType:
                self.itemPool = self.itemPool[0:idx] + self.itemPool[idx+1:]
                return item

    def removeForbiddenItems(self, forbiddenItems):
        # the pool is the one managed by the Randomizer
        for itemType in forbiddenItems:
            self.removeItem(itemType)
            self.addItem('NoEnergy', self.majorClass)
        return self.itemPool

    @staticmethod
    def getItem(itemType, itemClass=None):
        if itemClass is None:
            return copy.copy(ItemManager.Items[itemType])
        else:
            return ItemManager.Items[itemType].withClass(itemClass)

    def createItemPool(self, exclude=None):
        itemPoolGenerator = ItemPoolGenerator.factory(self.majorsSplit, self, self.qty, self.sm, exclude)
        self.itemPool = itemPoolGenerator.getItemPool()

    @staticmethod
    def getProgTypes():
        return [item for item in ItemManager.Items if ItemManager.Items[item].Category == 'Progression']

    def hasItemInPoolCount(self, itemName, count):
        return len([item for item in self.itemPool if item.Type == itemName]) >= count

class ItemPoolGenerator(object):
    @staticmethod
    def factory(majorsSplit, itemManager, qty, sm, exclude):
        if majorsSplit == 'Chozo':
            return ItemPoolGeneratorChozo(itemManager, qty, sm)
        elif majorsSplit == 'Plando':
            return ItemPoolGeneratorPlando(itemManager, qty, sm, exclude)
        else:
            return ItemPoolGeneratorMajors(itemManager, qty, sm)

    def __init__(self, itemManager, qty, sm):
        self.itemManager = itemManager
        self.qty = qty
        self.sm = sm
        self.maxItems = 105 # 100 item locs and 5 bosses
        self.log = log.get('ItemPool')

    # add ammo given quantity settings
    def addAmmo(self):
        nbMinorsAlready = 5
        # always add enough minors to pass zebetites (1100 damages) and mother brain 1 (3000 damages)
        # accounting for missile refill. so 15-10, or 10-10 if ice zeb skip is known (Ice is always in item pool)
        if not self.sm.knowsIceZebSkip():
            self.log.debug("Add missile because ice zeb skip is not known")
            self.itemManager.addMinor('Missile')
            nbMinorsAlready += 1
        minorLocations = max(0, 0.66*self.qty['minors'] - nbMinorsAlready) # 0.66 because of 66 minors and qty/100
        self.log.debug("minorLocations: {}".format(minorLocations))
        # we have to remove the minors already added
        maxItems = len(self.itemManager.getItemPool()) + int(minorLocations)
        self.log.debug("maxItems: {}".format(maxItems))
        ammoQty = self.qty['ammo']
        if not self.qty['strictMinors']:
            rangeDict = getRangeDict(ammoQty)
            self.log.debug("rangeDict: {}".format(rangeDict))
            while len(self.itemManager.getItemPool()) < maxItems:
                item = chooseFromRange(rangeDict)
                self.itemManager.addMinor(item)
        else:
            minorsTypes = ['Missile', 'Super', 'PowerBomb']
            totalProps = sum(ammoQty[m] for m in minorsTypes)
            minorsByProp = sorted(minorsTypes, key=lambda m: ammoQty[m])
            # in python3 the result is a float
            totalMinorLocations = int(66 * self.qty['minors'] / 100)
            self.log.debug("totalProps: {}".format(totalProps))
            self.log.debug("totalMinorLocations: {}".format(totalMinorLocations))
            def ammoCount(ammo):
                return float(len([item for item in self.itemManager.getItemPool() if item.Type == ammo]))
            def targetRatio(ammo):
                return round(float(ammoQty[ammo])/totalProps, 3)
            def cmpRatio(ammo, ratio):
                thisAmmo = ammoCount(ammo)
                thisRatio = round(thisAmmo/totalMinorLocations, 3)
                nextRatio = round((thisAmmo + 1)/totalMinorLocations, 3)
                self.log.debug("{} current, next/target ratio: {}, {}/{}".format(ammo, thisRatio, nextRatio, ratio))
                return abs(nextRatio - ratio) < abs(thisRatio - ratio)
            def fillAmmoType(ammo, checkRatio=True):
                ratio = targetRatio(ammo)
                self.log.debug("{}: target ratio: {}".format(ammo, ratio))
                while len(self.itemManager.getItemPool()) < maxItems and (not checkRatio or cmpRatio(ammo, ratio)):
                    self.log.debug("Add {}".format(ammo))
                    self.itemManager.addMinor(ammo)
            for m in minorsByProp:
                fillAmmoType(m)
            # now that the ratios have been matched as exactly as possible, we distribute the error
            def getError(m, countOffset=0):
                return abs((ammoCount(m)+countOffset)/totalMinorLocations - targetRatio(m))
            while len(self.itemManager.getItemPool()) < maxItems:
                minNextError = 1000
                chosenAmmo = None
                for m in minorsByProp:
                    nextError = getError(m, 1)
                    if nextError < minNextError:
                        minNextError = nextError
                        chosenAmmo = m
                self.itemManager.addMinor(chosenAmmo)
        # fill up the rest with blank items
        for i in range(self.maxItems - maxItems):
            self.itemManager.addMinor('Nothing')

class ItemPoolGeneratorChozo(ItemPoolGenerator):
    def addEnergy(self):
        total = 18
        energyQty = self.qty['energy']
        if energyQty == 'ultra sparse':
            # 0-1, remove reserve tank and two etanks, check if it also remove the last etank
            self.itemManager.removeItem('Reserve')
            self.itemManager.addItem('NoEnergy', 'Chozo')
            self.itemManager.removeItem('ETank')
            self.itemManager.addItem('NoEnergy', 'Chozo')
            self.itemManager.removeItem('ETank')
            self.itemManager.addItem('NoEnergy', 'Chozo')
            if random.random() < 0.5:
                # no etank nor reserve
                self.itemManager.removeItem('ETank')
                self.itemManager.addItem('NoEnergy', 'Chozo')
            elif random.random() < 0.5:
                # replace only etank with reserve
                self.itemManager.removeItem('ETank')
                self.itemManager.addItem('Reserve', 'Chozo')

            # complete up to 18 energies with nothing item
            alreadyInPool = 4
            for i in range(total - alreadyInPool):
                self.itemManager.addItem('Nothing', 'Minor')
        elif energyQty == 'sparse':
            # 4-6
            # already 3E and 1R
            alreadyInPool = 4
            rest = randGaussBounds(2, 5)
            if rest >= 1:
                if random.random() < 0.5:
                    self.itemManager.addItem('Reserve', 'Minor')
                else:
                    self.itemManager.addItem('ETank', 'Minor')
            for i in range(rest-1):
                self.itemManager.addItem('ETank', 'Minor')
            # complete up to 18 energies with nothing item
            for i in range(total - alreadyInPool - rest):
                self.itemManager.addItem('Nothing', 'Minor')
        elif energyQty == 'medium':
            # 8-12
            # add up to 3 Reserves or ETanks (cannot add more than 3 reserves)
            for i in range(3):
                if random.random() < 0.5:
                    self.itemManager.addItem('Reserve', 'Minor')
                else:
                    self.itemManager.addItem('ETank', 'Minor')
            # 7 already in the pool (3 E, 1 R, + the previous 3)
            alreadyInPool = 7
            rest = 1 + randGaussBounds(4, 3.7)
            for i in range(rest):
                self.itemManager.addItem('ETank', 'Minor')
            # fill the rest with NoEnergy
            for i in range(total - alreadyInPool - rest):
                self.itemManager.addItem('Nothing', 'Minor')
        else:
            # add the vanilla 3 reserves and 13 Etanks
            for i in range(3):
                self.itemManager.addItem('Reserve', 'Minor')
            for i in range(11):
                self.itemManager.addItem('ETank', 'Minor')

    def getItemPool(self):
        self.itemManager.newItemPool()
        # 25 locs: 16 majors, 3 etanks, 1 reserve, 2 missile, 2 supers, 1 pb
        for itemType in ['ETank', 'ETank', 'ETank', 'Reserve', 'Missile', 'Missile', 'Super', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
            self.itemManager.addItem(itemType, 'Chozo')

        self.addEnergy()
        self.addAmmo()

        return self.itemManager.getItemPool()

class ItemPoolGeneratorMajors(ItemPoolGenerator):
    def addEnergy(self):
        total = 18
        energyQty = self.qty['energy']
        if energyQty == 'ultra sparse':
            # 0-1, add up to one energy (etank or reserve)
            self.itemManager.removeItem('Reserve')
            self.itemManager.removeItem('ETank')
            self.itemManager.addItem('NoEnergy')
            if random.random() < 0.5:
                # no energy at all
                self.itemManager.addItem('NoEnergy')
            else:
                if random.random() < 0.5:
                    self.itemManager.addItem('ETank')
                else:
                    self.itemManager.addItem('Reserve')

            # complete up to 18 energies with nothing item
            alreadyInPool = 2
            for i in range(total - alreadyInPool):
                self.itemManager.addItem('NoEnergy')

        elif energyQty == 'sparse':
            # 4-6
            if random.random() < 0.5:
                self.itemManager.addItem('Reserve')
            else:
                self.itemManager.addItem('ETank')
            # 3 in the pool (1 E, 1 R + the previous one)
            alreadyInPool = 3
            rest = 1 + randGaussBounds(2, 5)
            for i in range(rest):
                self.itemManager.addItem('ETank')
            # complete up to 18 energies with nothing item
            for i in range(total - alreadyInPool - rest):
                self.itemManager.addItem('NoEnergy')

        elif energyQty == 'medium':
            # 8-12
            # add up to 3 Reserves or ETanks (cannot add more than 3 reserves)
            for i in range(3):
                if random.random() < 0.5:
                    self.itemManager.addItem('Reserve')
                else:
                    self.itemManager.addItem('ETank')
            # 5 already in the pool (1 E, 1 R, + the previous 3)
            alreadyInPool = 5
            rest = 3 + randGaussBounds(4, 3.7)
            for i in range(rest):
                self.itemManager.addItem('ETank')
            # fill the rest with NoEnergy
            for i in range(total - alreadyInPool - rest):
                self.itemManager.addItem('NoEnergy')
        else:
            # add the vanilla 3 reserves and 13 Etanks
            for i in range(3):
                self.itemManager.addItem('Reserve')
            for i in range(13):
                self.itemManager.addItem('ETank')

    def getItemPool(self):
        self.itemManager.newItemPool()

        for itemType in ['ETank', 'Reserve', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
            self.itemManager.addItem(itemType, 'Major')
        for itemType in ['Missile', 'Missile', 'Super', 'Super', 'PowerBomb']:
            self.itemManager.addItem(itemType, 'Minor')

        self.addEnergy()
        self.addAmmo()

        return self.itemManager.getItemPool()

class ItemPoolGeneratorPlando(ItemPoolGenerator):
    def __init__(self, itemManager, qty, sm, exclude):
        super(ItemPoolGeneratorPlando, self).__init__(itemManager, qty, sm)
        # dict of 'itemType: count' of items already added in the plando.
        # also a 'total: count' with the total number of items already added in the plando.
        self.exclude = exclude

    def getItemPool(self):
        self.itemManager.newItemPool(addBosses=False)

        # add the already placed items by the plando
        for item in self.exclude:
            if item == 'total':
                continue
            itemClass = 'Major'
            if item in ['Missile', 'Super', 'PowerBomb', 'Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
                itemClass = 'Minor'
            for i in range(self.exclude[item]):
                self.itemManager.addItem(item, itemClass)

        remain = 105 - self.exclude['total']
        self.log.debug("Plando: remain start: {}".format(remain))
        if remain > 0:
            # add missing bosses
            for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
                if boss not in self.exclude or self.exclude[boss] == 0:
                    self.itemManager.addItem(boss, 'Minor')
                    self.exclude[boss] = 1
                    remain -= 1

            self.log.debug("Plando: remain after bosses: {}".format(remain))
            if remain < 0:
                raise Exception("Too many items already placed by the plando: can't add the remaining bosses")

            # add missing majors
            majors = []
            for itemType in ['Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
                if itemType not in self.exclude or self.exclude[itemType] == 0:
                    self.itemManager.addItem(itemType, 'Major')
                    self.exclude[itemType] = 1
                    majors.append(itemType)
                    remain -= 1

            self.log.debug("Plando: remain after majors: {}".format(remain))
            if remain < 0:
                raise Exception("Too many items already placed by the plando: can't add the remaining majors: {}".format(', '.join(majors)))

            # add minimum minors to finish the game
            for (itemType, minimum) in [('Missile', 3), ('Super', 2), ('PowerBomb', 1)]:
                if itemType not in self.exclude:
                    self.exclude[itemType] = 0
                while self.exclude[itemType] < minimum:
                    self.itemManager.addItem(itemType, 'Minor')
                    self.exclude[itemType] += 1
                    remain -= 1

            self.log.debug("Plando: remain after minimum minors: {}".format(remain))
            if remain < 0:
                raise Exception("Too many items already placed by the plando: can't add the minimum minors to finish the game")

            # add energy
            energyQty = self.qty['energy']
            limits = {
                "sparse": [('ETank', 4), ('Reserve', 1)],
                "medium": [('ETank', 8), ('Reserve', 2)],
                "vanilla": [('ETank', 14), ('Reserve', 4)]
            }
            for (itemType, minimum) in limits[energyQty]:
                if itemType not in self.exclude:
                    self.exclude[itemType] = 0
                while self.exclude[itemType] < minimum:
                    self.itemManager.addItem(itemType, 'Major')
                    self.exclude[itemType] += 1
                    remain -= 1

            self.log.debug("Plando: remain after energy: {}".format(remain))
            if remain < 0:
                raise Exception("Too many items already placed by the plando: can't add energy")

            # add ammo
            nbMinorsAlready = self.exclude['Missile'] + self.exclude['Super'] + self.exclude['PowerBomb']
            minorLocations = max(0, 0.66*self.qty['minors'] - nbMinorsAlready)
            maxItems = len(self.itemManager.getItemPool()) + int(minorLocations)
            rangeDict = getRangeDict(self.qty['ammo'])
            while len(self.itemManager.getItemPool()) < maxItems and remain > 0:
                item = chooseFromRange(rangeDict)
                self.itemManager.addMinor(item)
                remain -= 1

            self.log.debug("Plando: remain after ammo: {}".format(remain))

            # add nothing
            while remain > 0:
                self.itemManager.addMinor('Nothing')
                remain -= 1

            self.log.debug("Plando: remain after nothing: {}".format(remain))

        return self.itemManager.getItemPool()
