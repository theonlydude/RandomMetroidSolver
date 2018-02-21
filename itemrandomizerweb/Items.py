from itemrandomizerweb.stdlib import List
import struct

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

def toByteArray(itemCode):
    return (struct.pack('B', itemCode & 0xff), struct.pack('B', itemCode >> 8))

def getItemTypeCode(item, itemVisibility):
    if itemVisibility == 'Visible':
        modifier = 0
    elif itemVisibility == 'Chozo':
        modifier = 84
    elif itemVisibility == 'Hidden':
        modifier = 168

    itemCode = item['Code'] + modifier
    return toByteArray(itemCode)

def addItem(itemType, itemPool):
    return [List.find(lambda item: item["Type"] == itemType, Items)] + itemPool

def addAmmo(rnd, itemPool):
    if List.length(itemPool) == 100:
        return itemPool
    else:
        rand = rnd.Next(0, 7)
        if rand in [0, 1, 2]:
            item = 'Missile'
        elif rand in [3, 4, 5]:
            item = 'Super'
        else:
            item = 'PowerBomb'
        return addAmmo(rnd, addItem(item, itemPool))

def getItemPool(rnd):
    itemPool = addItem('Reserve', Items)
    itemPool = addItem('Reserve', itemPool)
    itemPool = addItem('Reserve', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('ETank', itemPool)
    itemPool = addItem('Missile', itemPool)
    itemPool = addItem('Super', itemPool)
    itemPool = addAmmo(rnd, itemPool)
    return itemPool
