from itemrandomizerweb.stdlib import List
import struct
import random

# https://github.com/tewtal/itemrandomizerweb/blob/master/ItemRandomizer/Items.fs
Items = [
    {
        'Type': 'ETank',
        'Category': 'Misc',
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
        'Category': 'Misc',
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
        'Category': 'Misc',
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
    'Category': 'Ammo',
    'Class': 'Minor',
    'Code': 0xeedb,
    'Name': "Nothing",
    'Message': 0x0
}
NoEnergy = {
    'Type': 'NoEnergy',
    'Category': 'Misc',
    'Class': 'Major',
    'Code': 0xeedb,
    'Name': "No Energy",
    'Message': 0x0
}

def toByteArray(itemCode):
    return (struct.pack('B', itemCode & 0xff), struct.pack('B', itemCode >> 8))

def getItemTypeCode(item, itemVisibility, returnsInt=False):
    if itemVisibility == 'Visible':
        modifier = 0
    elif itemVisibility == 'Chozo':
        modifier = 84
    elif itemVisibility == 'Hidden':
        modifier = 168

    itemCode = item['Code'] + modifier
    if returnsInt is True:
        return (itemCode & 0xff, itemCode >> 8)
    else:
        return toByteArray(itemCode)

def addItem(itemType, itemPool):
    return [List.find(lambda item: item["Type"] == itemType, Items)] + itemPool

def addAmmo(itemPool, qty):
    # always add enough minors to pass zebetites (1100 damages) and mother brain 1 (3000 damages)
    # ie: 1 missiles and 1 supper, and 2 (supers or missiles)
    for i in range(2):
        if random.random() < 0.5:
            itemPool = addItem('Missile', itemPool)
        else:
            itemPool = addItem('Super', itemPool)

    # there's 66 minors locations, 5 minors items are already in the pool
    minorLocations = ((66 - 5) * qty['minors']) / 100
    maxItems = len(itemPool) + minorLocations

    # we won't generate all the minors, add the nothing item
    if qty['minors'] != 100:
        Items.append(Nothing)

    # depending on quantity, compute thresholds
    sumQty = float(qty['missile'] + qty['super'] + qty['powerBomb'])
    missileThreshold = qty['missile'] / sumQty
    superThreshold = qty['super'] / sumQty
    powerBombThreshold = qty['powerBomb'] / sumQty

    while len(itemPool) < maxItems:
        rand = random.random()
        if rand <= missileThreshold:
            item = 'Missile'
        elif rand <= superThreshold:
            item = 'Super'
        else:
            item = 'PowerBomb'

        itemPool = addItem(item, itemPool)

    for i in range(100 - maxItems):
        itemPool = addItem('Nothing', itemPool)

    return itemPool

def getItemPool(qty):
    if qty['energy'] == 'sparse':
        # 5 (there's always a reserve and an etank added by the first call to addItem with Items as parameter)
        if random.random() < 0.5:
            itemPool = addItem('Reserve', Items)
        else:
            itemPool = addItem('ETank', Items)
        itemPool = addItem('ETank', itemPool)
        itemPool = addItem('ETank', itemPool)

        # complete up to 18 energies with nothing item
        Items.append(NoEnergy)
        for i in range(13):
            itemPool = addItem('NoEnergy', itemPool)
    elif qty['energy'] == 'medium':
        # 11
        itemPool = addItem('ETank', Items)
        for i in range(3):
            if random.random() < 0.5:
                itemPool = addItem('Reserve', itemPool)
            else:
                itemPool = addItem('ETank', itemPool)

        for i in range(5):
            itemPool = addItem('ETank', itemPool)

        Items.append(NoEnergy)
        for i in range(7):
            itemPool = addItem('NoEnergy', itemPool)
    else:
        # 18
        itemPool = addItem('Reserve', Items)
        for i in range(2):
            itemPool = addItem('Reserve', itemPool)
        for i in range(13):
            itemPool = addItem('ETank', itemPool)

    itemPool = addAmmo(itemPool, qty)

    return itemPool
