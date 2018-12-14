from itemrandomizerweb.stdlib import List
from utils import randGaussBounds, getRangeDict, chooseFromRange

import struct
import random

# base items list : one of each type. we'll use it for base item pool
# and add duplicate items for ammo/energy
Items = [
    {
        'Type': 'ETank',
        'Category': 'Energy',
        'Class': 'Major',
        'Code': 0xeed7,
        'Name': "Energy Tank",
        'Message': 0x2877f
    },
    {
        'Type': 'Missile',
        'Category': 'Ammo',
        'Class': 'Minor',
        'Code': 0xeedb,
        'Name': "Missile",
        'Message': 0x287bf
    },
    {
        'Type': 'Super',
        'Category': 'Ammo',
        'Class': 'Minor',
        'Code': 0xeedf,
        'Name': "Super Missile",
        'Message': 0x288bf
    },
    {
        'Type': 'PowerBomb',
        'Category': 'Ammo',
        'Class': 'Minor',
        'Code': 0xeee3,
        'Name': "Power Bomb",
        'Message': 0x289bf
    },
    {
        'Type': 'Bomb',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xeee7,
        'Name': "Bomb",
        'Message': 0x2907f
    },
    {
        'Type': 'Charge',
        'Category': 'Beam',
        'Class': 'Major',
        'Code': 0xeeeb,
        'Name': "Charge Beam",
        'Message': 0x28f3f
    },
    {
        'Type': 'Ice',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xeeef,
        'Name': "Ice Beam",
        'Message': 0x28f7f
    },
    {
        'Type': 'HiJump',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xeef3,
        'Name': "Hi-Jump Boots",
        'Message': 0x28dbf
    },
    {
        'Type': 'SpeedBooster',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xeef7,
        'Name': "Speed Booster",
        'Message': 0x28e3f
    },
    {
        'Type': 'Wave',
        'Category': 'Beam',
        'Class': 'Major',
        'Code': 0xeefb,
        'Name': "Wave Beam",
        'Message': 0x28fbf
    },
    {
        'Type': 'Spazer',
        'Category': 'Beam',
        'Class': 'Major',
        'Code': 0xeeff,
        'Name': "Spazer",
        'Message': 0x28fff
    },
    {
        'Type': 'SpringBall',
        'Category': 'Misc',
        'Class': 'Major',
        'Code': 0xef03,
        'Name': "Spring Ball",
        'Message': 0x28cff
    },
    {
        'Type': 'Varia',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xef07,
        'Name': "Varia Suit",
        'Message': 0x28cbf
    },
    {
        'Type': 'Plasma',
        'Category': 'Beam',
        'Class': 'Major',
        'Code': 0xef13,
        'Name': "Plasma Beam",
        'Message': 0x2903f
    },
    {
        'Type': 'Grapple',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xef17,
        'Name': "Grappling Beam",
        'Message': 0x28abf
    },
    {
        'Type': 'Morph',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xef23,
        'Name': "Morph Ball",
        'Message': 0x28d3f
    },
    {
        'Type': 'Reserve',
        'Category': 'Energy',
        'Class': 'Major',
        'Code': 0xef27,
        'Name': "Reserve Tank",
        'Message': 0x294ff
    },
    {
        'Type': 'Gravity',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xef0b,
        'Name': "Gravity Suit",
        'Message': 0x2953f
    },
    {
        'Type': 'XRayScope',
        'Category': 'Misc',
        'Class': 'Major',
        'Code': 0xef0f,
        'Name': "X-Ray Scope",
        'Message': 0x28bbf
    },
    {
        'Type': 'SpaceJump',
        'Category': 'Progression',
        'Class': 'Major',
        'Code': 0xef1b,
        'Name': "Space Jump",
        'Message': 0x28dff
    },
    {
        'Type': 'ScrewAttack',
        'Category': 'Misc',
        'Class': 'Major',
        'Code': 0xef1f,
        'Name': "Screw Attack",
        'Message': 0x28d7f
    }
]

Nothing = {
    'Type': 'Nothing',
    'Category': 'Nothing',
    'Class': 'Minor',
    'Code': 0xeedb,
    'Name': "Nothing",
    'Message': 0x0
}

NoEnergy = {
    'Type': 'NoEnergy',
    'Category': 'Nothing',
    'Class': 'Major',
    'Code': 0xeedb,
    'Name': "No Energy",
    'Message': 0x0
}

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

def getItemTypeCode(item, itemVisibility):
    if itemVisibility == 'Visible':
        modifier = 0
    elif itemVisibility == 'Chozo':
        modifier = 84
    elif itemVisibility == 'Hidden':
        modifier = 168

    itemCode = item['Code'] + modifier
    return itemCode

# add item from original item list (NoEnergy and Nothing items have to be added manually)
def addItem(itemType, itemPool):
    itemPool.append(List.find(lambda item: item["Type"] == itemType, Items))

# remove from pool an item of given type. item type has to be in original Items list.
def removeItem(itemType, itemPool):
    itemPool.remove(List.find(lambda item: item["Type"] == itemType, Items))

# add ammo given quantity settings
def addAmmo(qty, itemPool, sm):
    # always add enough minors to pass zebetites (1100 damages) and mother brain 1 (3000 damages)
    # accounting for missile refill. so 15-10, or 10-10 if ice zeb skip is known (Ice is always in item pool)
    addItem('Missile', itemPool)
    addItem('Super', itemPool)
    nbMinors = 66 - 5 # 66 minor locs, 3 already in the pool, + the 2 above
    if not sm.knowsIceZebSkip():
        addItem('Missile', itemPool)
        nbMinors -= 1
    minorLocations = (nbMinors * qty['minors']) / 100
    maxItems = len(itemPool) + int(minorLocations)
    ammoQty = qty['ammo']
    if not qty['strictMinors']:
        rangeDict = getRangeDict(ammoQty)
        while len(itemPool) < maxItems:
            item = chooseFromRange(rangeDict)
            addItem(item, itemPool)
    else:
        totalProps = ammoQty['Missile'] + ammoQty['Super'] + ammoQty['PowerBomb']
        totalMinorLocations = 66 * qty['minors'] / 100
        def getRatio(ammo):
            thisAmmo = len([item for item in itemPool if item['Type'] == ammo])
            return float(thisAmmo)/totalMinorLocations
        def fillAmmoType(ammo, checkRatio=True):
            ratio = float(ammoQty[ammo])/totalProps
            while len(itemPool) < maxItems and (not checkRatio or getRatio(ammo) < ratio):
                addItem(ammo, itemPool)
        fillAmmoType('Missile')
        fillAmmoType('Super')
        fillAmmoType('PowerBomb', False)

    for i in range(100 - maxItems):
        itemPool.append(Nothing)

    return itemPool

def removeForbiddenItems(forbiddenItems, itemPool):
    for item in forbiddenItems:
        removeItem(item, itemPool)
        itemPool.append(NoEnergy)
    return itemPool

def addEnergy(qty, itemPool):
    total = 18
    energyQty = qty['energy']
    if energyQty == 'sparse':
        # 4-6
        if random.random() < 0.5:
            addItem('Reserve', itemPool)
        else:
            addItem('ETank', itemPool)
        # 3 in the pool (1 E, 1 R + the previous one)
        alreadyInPool = 3
        rest = 1 + randGaussBounds(2, 5)
        for i in range(rest):
            addItem('ETank', itemPool)
        # complete up to 18 energies with nothing item
        for i in range(total - alreadyInPool - rest):
            itemPool.append(NoEnergy)
    elif qty['energy'] == 'medium':
        # 8-12
        # add up to 3 Reserves or ETanks (cannot add more than 3 reserves)
        for i in range(3):
            if random.random() < 0.5:
                addItem('Reserve', itemPool)
            else:
                addItem('ETank', itemPool)
        # 5 already in the pool (1 E, 1 R, + the previous 3)
        alreadyInPool = 5
        rest = 3 + randGaussBounds(4, 3.7)
        for i in range(rest):
            addItem('ETank', itemPool)
        # fill the rest with NoEnergy
        for i in range(total - alreadyInPool - rest):
            itemPool.append(NoEnergy)
    else:
        # add the vanilla 3 reserves and 13 Etanks
        for i in range(3):
            addItem('Reserve', itemPool)
        for i in range(13):
            addItem('ETank', itemPool)

def getItemPool(qty, sm):
    # copy original items list (does not contain the 'nothing' types)
    itemPool = Items[:]
    # always add energy before ammo, as addAmmo will fill up item pool
    addEnergy(qty, itemPool)
    addAmmo(qty, itemPool, sm)

    return itemPool
