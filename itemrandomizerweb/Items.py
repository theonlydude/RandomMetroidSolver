from itemrandomizerweb.stdlib import List
from utils import randGaussBounds, getRangeDict, chooseFromRange
import log, logging

import struct, random, copy

class ItemManager:
    Items = {
        'ETank': {
            'Category': 'Energy',
            'Class': 'Major',
            'Code': 0xeed7,
            'Name': "Energy Tank"
        },
        'Missile': {
            'Category': 'Ammo',
            'Class': 'Minor',
            'Code': 0xeedb,
            'Name': "Missile"
        },
        'Super': {
            'Category': 'Ammo',
            'Class': 'Minor',
            'Code': 0xeedf,
            'Name': "Super Missile"
        },
        'PowerBomb': {
            'Category': 'Ammo',
            'Class': 'Minor',
            'Code': 0xeee3,
            'Name': "Power Bomb"
        },
        'Bomb': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xeee7,
            'Name': "Bomb"
        },
        'Charge': {
            'Category': 'Beam',
            'Class': 'Major',
            'Code': 0xeeeb,
            'Name': "Charge Beam"
        },
        'Ice': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xeeef,
            'Name': "Ice Beam"
        },
        'HiJump': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xeef3,
            'Name': "Hi-Jump Boots"
        },
        'SpeedBooster': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xeef7,
            'Name': "Speed Booster"
        },
        'Wave': {
            'Category': 'Beam',
            'Class': 'Major',
            'Code': 0xeefb,
            'Name': "Wave Beam"
        },
        'Spazer': {
            'Category': 'Beam',
            'Class': 'Major',
            'Code': 0xeeff,
            'Name': "Spazer"
        },
        'SpringBall': {
            'Category': 'Misc',
            'Class': 'Major',
            'Code': 0xef03,
            'Name': "Spring Ball"
        },
        'Varia': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xef07,
            'Name': "Varia Suit"
        },
        'Plasma': {
            'Category': 'Beam',
            'Class': 'Major',
            'Code': 0xef13,
            'Name': "Plasma Beam"

        },
        'Grapple': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xef17,
            'Name': "Grappling Beam"
        },
        'Morph': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xef23,
            'Name': "Morph Ball"
        },
        'Reserve': {
            'Category': 'Energy',
            'Class': 'Major',
            'Code': 0xef27,
            'Name': "Reserve Tank"
        },
        'Gravity': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xef0b,
            'Name': "Gravity Suit"
        },
        'XRayScope': {
            'Category': 'Misc',
            'Class': 'Major',
            'Code': 0xef0f,
            'Name': "X-Ray Scope"
        },
        'SpaceJump': {
            'Category': 'Progression',
            'Class': 'Major',
            'Code': 0xef1b,
            'Name': "Space Jump"
        },
        'ScrewAttack': {
            'Category': 'Misc',
            'Class': 'Major',
            'Code': 0xef1f,
            'Name': "Screw Attack"
        },
        'Nothing': {
            'Category': 'Nothing',
            'Class': 'Minor',
            'Code': 0xeedb,
            'Name': "Nothing"
        },
        'NoEnergy': {
            'Category': 'Nothing',
            'Class': 'Major',
            'Code': 0xeedb,
            'Name': "No Energy"
        },
        'Boss': {
            'Category': 'Nothing',
            'Class': 'Minor',
            'Code': 0xeedb,
            'Name': "Boss"
        }
    }

    @staticmethod
    def isBeam(item):
        return item['Category'] == 'Beam' or item['Type'] == 'Ice'

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

        itemCode = item['Code'] + modifier
        return itemCode

    def __init__(self, majorsSplit, qty, sm):
        self.qty = qty
        self.sm = sm
        self.majorsSplit = majorsSplit
        self.majorClass = 'Chozo' if majorsSplit == 'Chozo' else 'Major'
        self.itemPool = []

    def newItemPool(self):
        self.itemPool = []
        # for the bosses
        for i in range(5):
            self.addMinor('Boss')

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
            if item["Type"] == itemType:
                self.itemPool = self.itemPool[0:idx] + self.itemPool[idx+1:]
                break

    def removeForbiddenItems(self, forbiddenItems):
        # the pool is the one managed by the Randomizer
        for itemType in forbiddenItems:
            self.removeItem(itemType)
            self.addItem('NoEnergy', self.majorClass)
        return self.itemPool

    @staticmethod
    def getItem(itemType, itemClass=None):
        # TODO::use objects instead of dicts ?
        item = copy.copy(ItemManager.Items[itemType])
        if itemClass is not None:
            item['Class'] = itemClass
        item['Type'] = itemType
        return item

    def createItemPool(self):
        itemPoolGenerator = ItemPoolGenerator.factory(self.majorsSplit, self, self.qty, self.sm)
        self.itemPool = itemPoolGenerator.getItemPool()

    @staticmethod
    def getProgTypes():
        return [item for item in ItemManager.Items if ItemManager.Items[item]['Category'] == 'Progression']

class ItemPoolGenerator(object):
    @staticmethod
    def factory(majorsSplit, itemManager, qty, sm):
        if majorsSplit == 'Chozo':
            return ItemPoolGeneratorChozo(itemManager, qty, sm)
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
        # always add enough minors to pass zebetites (1100 damages) and mother brain 1 (3000 damages)
        # accounting for missile refill. so 15-10, or 10-10 if ice zeb skip is known (Ice is always in item pool)
        nbMinorsAlready = 5
        nbMinors = 66 - nbMinorsAlready # 66 minor locs, 5 already in the pool
        if not self.sm.knowsIceZebSkip():
            self.log.debug("Add missile because ice zeb skip is not known")
            self.itemManager.addMinor('Missile')
            nbMinors -= 1
            nbMinorsAlready += 1
        minorLocations = (nbMinors * self.qty['minors']) / 100
        self.log.debug("minorLocations: {}".format(minorLocations))
        # we have to remove the minors already added
        maxItems = len(self.itemManager.getItemPool()) + int(minorLocations) - nbMinorsAlready
        self.log.debug("maxItems: {}".format(maxItems))
        ammoQty = self.qty['ammo']
        if not self.qty['strictMinors']:
            rangeDict = getRangeDict(ammoQty)
            while len(self.itemManager.getItemPool()) < maxItems:
                item = chooseFromRange(rangeDict)
                self.itemManager.addMinor(item)
        else:
            totalProps = ammoQty['Missile'] + ammoQty['Super'] + ammoQty['PowerBomb']
            totalMinorLocations = 66 * self.qty['minors'] / 100
            self.log.debug("totalProps: {}".format(totalProps))
            self.log.debug("totalMinorLocations: {}".format(totalMinorLocations))
            def getRatio(ammo):
                thisAmmo = len([item for item in self.itemManager.getItemPool() if item['Type'] == ammo])
                ratio = float(thisAmmo)/totalMinorLocations
                self.log.debug("{} current ratio: {}".format(ammo, ratio))
                return ratio
            def fillAmmoType(ammo, checkRatio=True):
                ratio = float(ammoQty[ammo])/totalProps
                self.log.debug("{}: target ratio: {}".format(ammo, ratio))
                while len(self.itemManager.getItemPool()) < maxItems and (not checkRatio or getRatio(ammo) < ratio):
                    self.log.debug("Add {}".format(ammo))
                    self.itemManager.addMinor(ammo)
            fillAmmoType('Missile')
            fillAmmoType('Super')
            fillAmmoType('PowerBomb', False)

        for i in range(self.maxItems - maxItems):
            self.itemManager.addMinor('Nothing')

class ItemPoolGeneratorChozo(ItemPoolGenerator):
    def addEnergy(self):
        total = 18
        energyQty = self.qty['energy']
        if energyQty == 'sparse':
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
                self.itemManager.addItem('NoEnergy', 'Minor')
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
                self.itemManager.addItem('NoEnergy', 'Minor')
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
        if energyQty == 'sparse':
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
