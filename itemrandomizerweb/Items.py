from stdlib import List

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
        'Type': 'XRay',
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

#let toByteArray itemCode = [|byte(itemCode &&& 0xFF); byte(itemCode >>> 8)|]

#let getItemTypeCode item itemVisibility =
#    let modifier =
#        match itemVisibility with
#        | Visible -> 0
#        | Chozo -> 0x54
#        | Hidden -> 0xA8
#
#    let itemCode = (item.Code + modifier)
#    toByteArray itemCode

#let addItem (itemType:ItemType) (itemPool:Item list) =
#    (List.find (fun item -> item.Type = itemType) Items) :: itemPool
def addItem(itemType, itemPool):
    return [List.find(lambda item: item["Type"] == itemType, Items.Items)] + itemPool

#let rec addAmmo (rnd:System.Random) (itemPool:Item list) =
#    match List.length itemPool with
#    | 100 -> itemPool
#    | _ -> addAmmo rnd (addItem (match rnd.Next(7) with
#                                 | 0 | 1 | 2 -> Missile
#                                 | 3 | 4 | 5 -> Super
#                                 | _ -> PowerBomb)
#                                 itemPool)
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

#let getItemPool rnd =
#    Items
#    |> addItem Reserve
#    |> addItem Reserve
#    |> addItem Reserve
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem ETank
#    |> addItem Missile
#    |> addItem Super
#    |> addAmmo rnd
def getItemPool(rnd):
    itemPool = Items.addItem('Reserve', Items)
    itemPool = Items.addItem('Reserve', itemPool)
    itemPool = Items.addItem('Reserve', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('ETank', itemPool)
    itemPool = Items.addItem('Missile', itemPool)
    itemPool = Items.addItem('Super', itemPool)
    itemPool = Items.addAmmo(rnd, itemPool)
    return itemPool
