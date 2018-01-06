# implement the randomizer in python
# https://github.com/tewtal/itemrandomizerweb/blob/master/ItemRandomizer/Randomizers.fs

from dotnet_random import Random

# https://msdn.microsoft.com/en-us/visualfsharpdocs/conceptual/microsoft.fsharp.collections-namespace-%5bfsharp%5d
class Map:
    @staticmethod
    def toList(map):
        # returns a list of all key/value pairs in the mapping.
        # the returned list is ordered by the keys of the map.
        return [(index, map[index]) for index in sorted(map)]

class Array:
    @staticmethod
    def toList(array):
        # builds a list from the given array
        return array

    @staticmethod
    # Array.iteri (fun i _ -> swap a i (rnd.Next(i, Array.length a))) a
    def iteri(fun, array):
        # applies the given function to each element of the array.
        # the integer passed to the function indicates the index of element.
        # done in place.
        for i in range(len(array)):
            array[i] = fun(i, array[i])

class List:
    @staticmethod
    def length(list):
        # gets the number of items contained in the list
        return len(list)

    @staticmethod
    def exists(fun, list):
        # tests if any element of the list satisfies the given predicate
        # TODO::use next to avoid executing fun on all the list
        return True in [fun(elem) for elem in list]

    @staticmethod
    def filter(fun, list):
        # returns a new collection containing only the elements of the collection
        # for which the given predicate returns true
        return [elem for elem in list if fun(list) is True]

    @staticmethod
    def find(fun, list):
        # returns the first element for which the given function returns true
        # raise: StopIteration
        return next(iter([elem for elem in list if fun(elem) is True]))

    @staticmethod
    def sortBy(fun, list):
        # sorts the given list using keys given by the given projection
        return sorted(list, key=fun)

    @staticmethod
    def append(list1, list2):
        # returns a new list that contains the elements of the first
        # list followed by elements of the second
        return list1 + list2

    @staticmethod
    def head(list):
        # returns the first element of the list
        # raise: IndexError
        return list[0]

    @staticmethod
    def toArray(list):
        return list

    @staticmethod
    def item(index, list):
        # gets the element of the list at the given position
        return list[index]

    @staticmethod
    def map(fun, list):
        # creates a new collection whose elements are the results of
        # applying the given function to each of the elements of the collection
        return [fun(elem) for elem in list]

class Items:

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
    @staticmethod
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
    @staticmethod
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
            return Items.addAmmo(rnd, Items.addItem(item, itemPool))

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
    @staticmethod
    def getItemPool(rnd):
        itemPool = Items.addItem('Reserve', Items.Items)
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

class TournamentLocations:
    # Functions to check if we have a specific item
    def haveItem(items, itemType):
        return List.exists(lambda item: item["Type"] == itemType, items)
    
    def itemCount(items, itemType):
        return List.length(List.filter(lambda item: item["Type"] == itemType, items))

    def energyReserveCount(items):
        return itemCount(items, "ETank") + itemCount(items, "Reserve")

    def heatProof(items):
        return haveItem(items, "Varia")

    # Combined checks to see if we can perform an action needed to access locations
    def canHellRun(items):
        return (energyReserveCount(items) >= 3 or
                heatProof(items))

    def canFly(items):
        return (haveItem(items, "Morph") and haveItem(items, "Bomb")) or haveItem(items, "SpaceJump")
    def canUseBombs(items):
        return haveItem(items, "Morph") and haveItem(items, "Bomb")

    def canOpenRedDoors(items):
        return haveItem(items, "Missile") or haveItem(items, "Super")
    def canOpenGreenDoors(items):
        return haveItem(items, "Super")
    def canOpenYellowDoors(items):
        return haveItem(items, "Morph") and haveItem(items, "PowerBomb")
    def canUsePowerBombs():
        return canOpenYellowDoors()

    let canDestroyBombWalls items =
        (haveItem items Morph &&
            (haveItem items Bomb ||
             haveItem items PowerBomb)) ||
        haveItem items ScrewAttack
    
    let canCrystalFlash items = 
        itemCount items Missile >= 2 &&
        itemCount items Super >= 2 &&
        itemCount items PowerBomb >= 3
    
    let canEnterAndLeaveGauntlet items =
        (canFly items || haveItem items HiJump || haveItem items SpeedBooster) &&
        (canUseBombs items || 
         (canUsePowerBombs items && itemCount items PowerBomb >= 2) || 
         haveItem items ScrewAttack ||
         (haveItem items SpeedBooster && canUsePowerBombs items && (energyReserveCount items >= 2)))
    
    let canPassBombPassages items =
        canUseBombs items || 
        canUsePowerBombs items
    
    let canAccessRedBrinstar items =
        haveItem items Super && 
            ((canDestroyBombWalls items && haveItem items Morph) || 
             canUsePowerBombs items)
    
    let canAccessKraid items = 
        canAccessRedBrinstar items &&
        canPassBombPassages items
    
    let canAccessWs items = 
        canUsePowerBombs items && 
        haveItem items Super
    
    let canAccessHeatedNorfair items =
        canAccessRedBrinstar items &&
             (canHellRun items)
    
    let canAccessCrocomire items =
        canAccessHeatedNorfair items ||
            (canAccessKraid items &&
             canUsePowerBombs items &&
             haveItem items SpeedBooster &&
             (energyReserveCount items >= 2))
    
    let canAccessLowerNorfair items = 
        canAccessHeatedNorfair items &&
        canUsePowerBombs items &&
        haveItem items Varia &&
            (haveItem items HiJump ||
             haveItem items Gravity)
    
    let canPassWorstRoom items =
        canAccessLowerNorfair items &&
            (canFly items ||
             haveItem items Ice ||
             haveItem items HiJump)

    let canAccessOuterMaridia items = 
        canAccessRedBrinstar items &&
        canUsePowerBombs items &&
            (haveItem items Gravity ||
             (haveItem items HiJump && haveItem items Ice))
    
    let canAccessInnerMaridia items = 
        canAccessRedBrinstar items &&
        canUsePowerBombs items &&
        haveItem items Gravity
    
    let canDoSuitlessMaridia items = 
         (haveItem items HiJump && haveItem items Ice && haveItem items Grapple)    

    let canDefeatBotwoon items = 
        canAccessInnerMaridia items &&
        (haveItem items Ice || haveItem items SpeedBooster)

    let canDefeatDraygon items = 
        canDefeatBotwoon items && haveItem items Gravity;

    // Item Locations
    let AllLocations = 
        [
            {
                Area = Crateria;
                Name = "Power Bomb (Crateria surface)";
                Class = Minor;
                Address = 0x781CC;
                Visibility = Visible;
                Available = fun items ->
                    canUsePowerBombs items &&
                    (haveItem items SpeedBooster || canFly items);
            };
            {
                Area = Crateria;
                Name = "Missile (outside Wrecked Ship bottom)";
                Class = Minor;
                Address = 0x781E8;
                Visibility = Visible;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = Crateria;
                Name = "Missile (outside Wrecked Ship top)";
                Class = Minor;
                Address = 0x781EE;
                Visibility = Hidden;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = Crateria;
                Name = "Missile (outside Wrecked Ship middle)";
                Class = Minor;
                Address = 0x781F4;
                Visibility = Visible;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = Crateria;
                Name = "Missile (Crateria moat)";
                Class = Minor
                Address = 0x78248;
                Visibility = Visible;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = Crateria;
                Name = "Energy Tank, Gauntlet";
                Class = Major;
                Address = 0x78264;
                Visibility = Visible;
                Available = fun items -> canEnterAndLeaveGauntlet items;
            };
            {
                Area = Crateria;
                Name = "Missile (Crateria bottom)";
                Class = Minor;
                Address = 0x783EE;
                Visibility = Visible;
                Available = fun items -> canDestroyBombWalls items;
            };
            {
                Area = Crateria;
                Name = "Bomb";
                Address = 0x78404;
                Class = Major;
                Visibility = Chozo;
                Available = fun items -> haveItem items Morph && canOpenRedDoors items;
            };
            {
                Area = Crateria;
                Name = "Energy Tank, Terminator";
                Class = Major;
                Address = 0x78432;
                Visibility = Visible;
                Available = fun items -> canDestroyBombWalls items || haveItem items SpeedBooster
            };
            {
                Area = Crateria;
                Name = "Missile (Crateria gauntlet right)";
                Class = Minor;
                Address = 0x78464;
                Visibility = Visible;
                Available = fun items -> canEnterAndLeaveGauntlet items && canPassBombPassages items;
            };
            {
                Area = Crateria;
                Name = "Missile (Crateria gauntlet left)";
                Class = Minor;
                Address = 0x7846A;
                Visibility = Visible;
                Available = fun items -> canEnterAndLeaveGauntlet items && canPassBombPassages items;
            };
            {
                Area = Crateria;
                Name = "Super Missile (Crateria)";
                Class = Minor;
                Address = 0x78478;                
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items && 
                                         haveItem items SpeedBooster && 
                                         (haveItem items ETank || haveItem items Varia || haveItem items Gravity)
            };
            {
                Area = Crateria;
                Name = "Missile (Crateria middle)";
                Class = Minor;
                Address = 0x78486;
                Visibility = Visible;
                Available = fun items -> canPassBombPassages items;
            };
            {
                Area = Brinstar;
                Name = "Power Bomb (green Brinstar bottom)";
                Class = Minor;
                Address = 0x784AC;
                Visibility = Chozo;
                Available = fun items -> canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Super Missile (pink Brinstar)";
                Class = Minor;
                Address = 0x784E4;
                Visibility = Chozo;
                Available = fun items -> canPassBombPassages items && haveItem items Super;
            };
            {
                Area = Brinstar;
                Name = "Missile (green Brinstar below super missile)";
                Class = Minor;
                Address = 0x78518;
                Visibility = Visible;
                Available = fun items -> canPassBombPassages items && canOpenRedDoors items;
            };
            {
                Area = Brinstar;
                Name = "Super Missile (green Brinstar top)";
                Class = Minor;
                Address = 0x7851E;
                Visibility = Visible;
                Available = fun items -> (haveItem items SpeedBooster || canDestroyBombWalls items) && canOpenRedDoors items && (haveItem items Morph || haveItem items SpeedBooster);
            };
            {
                Area = Brinstar;
                Name = "Reserve Tank, Brinstar";
                Class = Major;
                Address = 0x7852C;
                Visibility = Chozo;
                Available = fun items -> (haveItem items SpeedBooster || canDestroyBombWalls items) && canOpenRedDoors items && (haveItem items Morph || haveItem items SpeedBooster);
            };
            {
                Area = Brinstar;
                Name = "Missile (green Brinstar behind missile)";
                Class = Minor;
                Address = 0x78532;
                Visibility = Hidden;
                Available = fun items -> canPassBombPassages items && canOpenRedDoors items;
            };
            {
                Area = Brinstar;
                Name = "Missile (green Brinstar behind reserve tank)";
                Class = Minor;
                Address = 0x78538;
                Visibility = Visible;
                Available = fun items -> canDestroyBombWalls items && canOpenRedDoors items && haveItem items Morph;
            };
            {
                Area = Brinstar;
                Name = "Missile (pink Brinstar top)";
                Class = Minor;
                Address = 0x78608;
                Visibility = Visible;
                Available = fun items -> (canDestroyBombWalls items && canOpenRedDoors items) ||
                                         canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Missile (pink Brinstar bottom)";
                Class = Minor;
                Address = 0x7860E;
                Visibility = Visible;
                Available = fun items -> (canDestroyBombWalls items && canOpenRedDoors items) ||
                                         canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Charge Beam";
                Class = Major;
                Address = 0x78614;
                Visibility = Chozo;
                Available = fun items -> (canPassBombPassages items && canOpenRedDoors items) ||
                                         canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Power Bomb (pink Brinstar)";
                Class = Minor;
                Address = 0x7865C;
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items && haveItem items Super;
            };
            {
                Area = Brinstar;
                Name = "Missile (green Brinstar pipe)";
                Class = Minor;
                Address = 0x78676;
                Visibility = Visible;
                Available = fun items -> (canPassBombPassages items && canOpenGreenDoors items) || canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Morphing Ball";
                Class = Major;
                Address = 0x786DE;
                Visibility = Visible;
                Available = fun items -> true;
            };
            {
                Area = Brinstar;
                Name = "Power Bomb (blue Brinstar)";
                Class = Minor;
                Address = 0x7874C;
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Missile (blue Brinstar middle)";
                Address = 0x78798;
                Class = Minor;
                Visibility = Visible;
                Available = fun items -> haveItem items Morph;
            };
            {
                Area = Brinstar;
                Name = "Energy Tank, Brinstar Ceiling";
                Class = Major;
                Address = 0x7879E;
                Visibility = Hidden;
                Available = fun items -> true;
            };
            {
                Area = Brinstar;
                Name = "Energy Tank, Etecoons";
                Class = Major;
                Address = 0x787C2;
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Super Missile (green Brinstar bottom)";
                Class = Minor;
                Address = 0x787D0;
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items && canOpenGreenDoors items;
            };
            {
                Area = Brinstar;
                Name = "Energy Tank, Waterway";
                Class = Major;
                Address = 0x787FA;
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items && canOpenRedDoors items && haveItem items SpeedBooster;
            };
            {
                Area = Brinstar;
                Name = "Missile (blue Brinstar bottom)";
                Class = Minor;
                Address = 0x78802;
                Visibility = Chozo;
                Available = fun items -> haveItem items Morph;
            };
            {
                Area = Brinstar;
                Name = "Energy Tank, Brinstar Gate";
                Class = Major;
                Address = 0x78824;
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items &&
                                         (haveItem items Wave || (haveItem items Super && haveItem items HiJump));
            };
            {
                Area = Brinstar;
                Name = "Missile (blue Brinstar top)";
                Class = Minor;
                Address = 0x78836;
                Visibility = Visible;
                Available = fun items -> canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Missile (blue Brinstar behind missile)";
                Class = Minor;
                Address = 0x7883C;
                Visibility = Hidden;
                Available = fun items -> canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "X-Ray Scope";
                Class = Major;
                Address = 0x78876;
                Visibility = Chozo;
                Available = fun items ->canAccessRedBrinstar items && 
                                        canUsePowerBombs items &&
                                        (haveItem items Grapple ||
                                         haveItem items SpaceJump ||
                                         (haveItem items Varia && energyReserveCount items >= 4) ||
                                         (energyReserveCount items >= 6))
                            
            };
            {
                Area = Brinstar;
                Name = "Power Bomb (red Brinstar sidehopper room)";
                Class = Minor;
                Address = 0x788CA;
                Visibility = Visible;
                Available = fun items -> canAccessRedBrinstar items && canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Power Bomb (red Brinstar spike room)";
                Class = Minor;
                Address = 0x7890E;
                Visibility = Chozo;
                Available = fun items -> canAccessRedBrinstar items && canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Missile (red Brinstar spike room)";
                Class = Minor;
                Address = 0x78914;
                Visibility = Visible;
                Available = fun items -> canAccessRedBrinstar items && canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Spazer";
                Class = Major;
                Address = 0x7896E;
                Visibility = Chozo;
                Available = fun items -> canAccessRedBrinstar items;
            };
            {
                Area = Brinstar;
                Name = "Energy Tank, Kraid";
                Class = Major;
                Address = 0x7899C;
                Visibility = Hidden;
                Available = fun items -> canAccessKraid items;
            };
            {
                Area = Brinstar;
                Name = "Missile (Kraid)";
                Class = Minor;
                Address = 0x789EC;
                Visibility = Hidden;
                Available = fun items -> canAccessKraid items && canUsePowerBombs items;
            };
            {
                Area = Brinstar;
                Name = "Varia Suit";
                Class = Major;
                Address = 0x78ACA;
                Visibility = Chozo;
                Available = fun items -> canAccessKraid items;
            };
            {
                Area = Norfair;
                Name = "Missile (lava room)";
                Class = Minor;
                Address = 0x78AE4;
                Visibility = Hidden;
                Available = fun items -> canAccessHeatedNorfair items;
            };
            {
                Area = Norfair;
                Name = "Ice Beam";
                Class = Major;
                Address = 0x78B24;
                Visibility = Chozo;
                Available = fun items -> canAccessKraid items &&
                                         (heatProof items || energyReserveCount items >= 2);
            };
            {
                Area = Norfair;
                Name = "Missile (below Ice Beam)";
                Class = Minor;
                Address = 0x78B46;
                Visibility = Hidden;
                Available = fun items -> canAccessKraid items && 
                                         canUsePowerBombs items && 
                                         canHellRun items;                                         
            };
            {
                Area = Norfair;
                Name = "Energy Tank, Crocomire";
                Class = Major;
                Address = 0x78BA4;
                Visibility = Visible;
                Available = fun items -> canAccessCrocomire items;
            };
            {
                Area = Norfair;
                Name = "Hi-Jump Boots";
                Class = Major;
                Address = 0x78BAC;
                Visibility = Chozo;
                Available = fun items -> canAccessRedBrinstar items;
            };
            {
                Area = Norfair;
                Name = "Missile (above Crocomire)";
                Class = Minor;
                Address = 0x78BC0;
                Visibility = Visible;
                Available = fun items -> canAccessCrocomire items &&
                                            (canFly items || 
                                             haveItem items Grapple ||
                                             (haveItem items HiJump && haveItem items SpeedBooster))
            };
            {
                Area = Norfair;
                Name = "Missile (Hi-Jump Boots)";
                Class = Minor;
                Address = 0x78BE6;
                Visibility = Visible;
                Available = fun items -> canAccessRedBrinstar items;
            };
            {
                Area = Norfair;
                Name = "Energy Tank (Hi-Jump Boots)";
                Class = Minor;
                Address = 0x78BEC;
                Visibility = Visible;
                Available = fun items -> canAccessRedBrinstar items;
            };
            {
                Area = Norfair;
                Name = "Power Bomb (Crocomire)";
                Class = Minor;
                Address = 0x78C04;
                Visibility = Visible;
                Available = fun items -> canAccessCrocomire items;
            };
            {
                Area = Norfair;
                Name = "Missile (below Crocomire)";
                Class = Minor;
                Address = 0x78C14;
                Visibility = Visible;
                Available = fun items -> canAccessCrocomire items;
            };
            {
                Area = Norfair;
                Name = "Missile (Grapple Beam)";
                Class = Minor;
                Address = 0x78C2A;
                Visibility = Visible;
                Available = fun items -> canAccessCrocomire items &&
                                            (canFly items ||
                                             haveItem items Grapple ||
                                             haveItem items SpeedBooster);
            };
            {
                Area = Norfair;
                Name = "Grapple Beam";
                Class = Major;
                Address = 0x78C36;
                Visibility = Chozo;
                Available = fun items -> canAccessCrocomire items &&
                                            (canFly items ||
                                             haveItem items Ice ||
                                             haveItem items SpeedBooster);
            };
            {
                Area = Norfair;
                Name = "Reserve Tank, Norfair";
                Class = Major;
                Address = 0x78C3E;
                Visibility = Chozo;
                Available = fun items -> canAccessHeatedNorfair items &&
                                            (canFly items ||
                                             haveItem items Grapple ||
                                             haveItem items HiJump);
            };
            {
                Area = Norfair;
                Name = "Missile (Norfair Reserve Tank)";
                Class = Minor;
                Address = 0x78C44;
                Visibility = Hidden;
                Available = fun items -> canAccessHeatedNorfair items &&
                                            (canFly items ||
                                             haveItem items Grapple ||
                                             haveItem items HiJump);
            };
            {
                Area = Norfair;
                Name = "Missile (bubble Norfair green door)";
                Class = Minor;
                Address = 0x78C52;
                Visibility = Visible;
                Available = fun items -> canAccessHeatedNorfair items &&
                                            (canFly items ||
                                             haveItem items Grapple ||
                                             haveItem items HiJump);
            };
            {
                Area = Norfair;
                Name = "Missile (bubble Norfair)";
                Class = Minor;
                Address = 0x78C66;
                Visibility = Visible;
                Available = fun items -> canAccessHeatedNorfair items;
            };
            {
                Area = Norfair;
                Name = "Missile (Speed Booster)";
                Class = Minor;
                Address = 0x78C74;
                Visibility = Hidden;
                Available = fun items -> canAccessHeatedNorfair items;
            };
            {
                Area = Norfair;
                Name = "Speed Booster";
                Class = Major;
                Address = 0x78C82;
                Visibility = Chozo;
                Available = fun items -> canAccessHeatedNorfair items;
            };
            {
                Area = Norfair;
                Name = "Missile (Wave Beam)";
                Class = Minor;
                Address = 0x78CBC;
                Visibility = Visible;
                Available = fun items -> canAccessHeatedNorfair items;
            };
            {
                Area = Norfair;
                Name = "Wave Beam";
                Class = Major;
                Address = 0x78CCA;
                Visibility = Chozo;
                Available = fun items -> canAccessHeatedNorfair items;
            };
            {
                Area = LowerNorfair;
                Name = "Missile (Gold Torizo)";
                Class = Minor;
                Address = 0x78E6E;
                Visibility = Visible;
                Available = fun items -> canAccessLowerNorfair items && haveItem items SpaceJump;
            };
            {
                Area = LowerNorfair;
                Name = "Super Missile (Gold Torizo)";
                Class = Minor;
                Address = 0x78E74;
                Visibility = Hidden;
                Available = fun items -> canAccessLowerNorfair items;
            };
            {
                Area = LowerNorfair;
                Name = "Missile (Mickey Mouse room)";
                Class = Minor;
                Address = 0x78F30;
                Visibility = Visible;
                Available = fun items -> canPassWorstRoom items;
            };
            {
                Area = LowerNorfair;
                Name = "Missile (lower Norfair above fire flea room)";
                Class = Minor;
                Address = 0x78FCA;
                Visibility = Visible;
                Available = fun items -> canPassWorstRoom items;
            };
            {
                Area = LowerNorfair;
                Name = "Power Bomb (lower Norfair above fire flea room)";
                Class = Minor;
                Address = 0x78FD2;
                Visibility = Visible;
                Available = fun items -> canPassWorstRoom items;
            };
            {
                Area = LowerNorfair;
                Name = "Power Bomb (Power Bombs of shame)";
                Class = Minor;
                Address = 0x790C0;
                Visibility = Visible;
                Available = fun items -> canPassWorstRoom items;
            };
            {
                Area = LowerNorfair;
                Name = "Missile (lower Norfair near Wave Beam)";
                Class = Minor;
                Address = 0x79100;
                Visibility = Visible;
                Available = fun items -> canPassWorstRoom items;
            };
            {
                Area = LowerNorfair;
                Name = "Energy Tank, Ridley";
                Class = Major;
                Address = 0x79108;
                Visibility = Hidden;
                Available = fun items -> canPassWorstRoom items;
            };
            {
                Area = LowerNorfair;
                Name = "Screw Attack";
                Class = Major;
                Address = 0x79110;
                Visibility = Chozo;
                Available = fun items -> canAccessLowerNorfair items;
            };
            {
                Area = LowerNorfair;
                Name = "Energy Tank, Firefleas";
                Class = Major;
                Address = 0x79184;
                Visibility = Visible;
                Available = fun items -> canPassWorstRoom items;
            };
            {
                Area = WreckedShip;
                Name = "Missile (Wrecked Ship middle)";
                Class = Minor;
                Address = 0x7C265;
                Visibility = Visible;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = WreckedShip;
                Name = "Reserve Tank, Wrecked Ship";
                Class = Major;
                Address = 0x7C2E9;
                Visibility = Chozo;
                Available = fun items -> canAccessWs items &&
                                         haveItem items SpeedBooster &&
                                         (haveItem items Varia || energyReserveCount items >= 1);
            };
            {
                Area = WreckedShip;
                Name = "Missile (Gravity Suit)";
                Class = Minor;
                Address = 0x7C2EF;
                Visibility = Visible;
                Available = fun items -> canAccessWs items &&
                                         (haveItem items Varia || energyReserveCount items >= 1);
            };
            {
                Area = WreckedShip;
                Name = "Missile (Wrecked Ship top)";
                Class = Minor;
                Address = 0x7C319;
                Visibility = Visible;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = WreckedShip;
                Name = "Energy Tank, Wrecked Ship";
                Class = Major;
                Address = 0x7C337;
                Visibility = Visible;
                Available = fun items -> canAccessWs items &&
                                            (haveItem items Bomb ||
                                             haveItem items PowerBomb ||
                                             haveItem items HiJump ||
                                             haveItem items SpaceJump ||
                                             haveItem items SpeedBooster ||
                                             haveItem items SpringBall);
            };
            {
                Area = WreckedShip;
                Name = "Super Missile (Wrecked Ship left)";
                Class = Minor;
                Address = 0x7C357;
                Visibility = Visible;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = WreckedShip;
                Name = "Right Super, Wrecked Ship";
                Class = Major;
                Address = 0x7C365;
                Visibility = Visible;
                Available = fun items -> canAccessWs items;
            };
            {
                Area = WreckedShip;
                Name = "Gravity Suit";
                Class = Major;
                Address = 0x7C36D;
                Visibility = Chozo;
                Available = fun items -> canAccessWs items &&
                                         (haveItem items Varia || energyReserveCount items >= 1);
            };
            {
                Area = Maridia;
                Name = "Missile (green Maridia shinespark)";
                Class = Minor;
                Address = 0x7C437;
                Visibility = Visible;
                Available = fun items -> canAccessRedBrinstar items &&
                                         canUsePowerBombs items &&
                                         haveItem items Gravity &&
                                         haveItem items SpeedBooster;
            };
            {
                Area = Maridia;
                Name = "Super Missile (green Maridia)";
                Class = Minor;
                Address = 0x7C43D;
                Visibility = Visible;
                Available = fun items -> canAccessOuterMaridia items;
            };
            {
                Area = Maridia;
                Name = "Energy Tank, Mama turtle";
                Class = Major;
                Address = 0x7C47D;
                Visibility = Visible;
                Available = fun items -> canAccessOuterMaridia items &&
                                            (canFly items ||
                                             haveItem items SpeedBooster ||
                                             haveItem items Grapple);
            };
            {
                Area = Maridia;
                Name = "Missile (green Maridia tatori)";
                Class = Minor;
                Address = 0x7C483;
                Visibility = Hidden;
                Available = fun items -> canAccessOuterMaridia items;
            };
            {
                Area = Maridia;
                Name = "Super Missile (yellow Maridia)";
                Class = Minor;
                Address = 0x7C4AF;
                Visibility = Visible;
                Available = fun items -> canAccessInnerMaridia items;
            };
            {
                Area = Maridia;
                Name = "Missile (yellow Maridia super missile)";
                Class = Minor;
                Address = 0x7C4B5;
                Visibility = Visible;
                Available = fun items -> canAccessInnerMaridia items;
            };
            {
                Area = Maridia;
                Name = "Missile (yellow Maridia false wall)";
                Class = Minor;
                Address = 0x7C533;
                Visibility = Visible;
                Available = fun items -> canAccessInnerMaridia items;
            };
            {
                Area = Maridia;
                Name = "Plasma Beam";
                Class = Major;
                Address = 0x7C559;
                Visibility = Chozo;
                Available = fun items -> canDefeatDraygon items &&
                                         (haveItem items SpeedBooster ||
                                            (haveItem items Charge ||
                                             haveItem items ScrewAttack) &&
                                            (canFly items || haveItem items HiJump));
            };
            {
                Area = Maridia;
                Name = "Missile (left Maridia sand pit room)";
                Class = Minor;
                Address = 0x7C5DD;
                Visibility = Visible;
                Available = fun items -> canAccessInnerMaridia items;
            };
            {
                Area = Maridia;
                Name = "Reserve Tank, Maridia";
                Class = Major;
                Address = 0x7C5E3;
                Visibility = Chozo;
                Available = fun items -> (canAccessOuterMaridia items && (canDoSuitlessMaridia items || haveItem items Gravity));
            };
            {
                Area = Maridia;
                Name = "Missile (right Maridia sand pit room)";
                Class = Minor;
                Address = 0x7C5EB;
                Visibility = Visible;
                Available = fun items -> canAccessInnerMaridia items;
            };
            {
                Area = Maridia;
                Name = "Power Bomb (right Maridia sand pit room)";
                Class = Minor;
                Address = 0x7C5F1;
                Visibility = Visible;
                Available = fun items -> canAccessOuterMaridia items &&
                                         haveItem items Gravity;
            };
            {
                Area = Maridia;
                Name = "Missile (pink Maridia)";
                Address = 0x7C603;
                Class = Minor;
                Visibility = Visible;
                Available = fun items -> canAccessOuterMaridia items &&
                                         haveItem items Gravity;
            };
            {
                Area = Maridia;
                Name = "Super Missile (pink Maridia)";
                Class = Minor;
                Address = 0x7C609;
                Visibility = Visible;
                Available = fun items -> canAccessOuterMaridia items &&
                                         haveItem items Gravity;
            };
            {
                Area = Maridia;
                Name = "Spring Ball";
                Class = Major;
                Address = 0x7C6E5;
                Visibility = Chozo;
                Available = fun items -> canAccessInnerMaridia items &&                                         
                                         (haveItem items Ice || (haveItem items Grapple && (canFly items || haveItem items HiJump)));
            };
            {
                Area = Maridia;
                Name = "Missile (Draygon)";
                Class = Minor;
                Address = 0x7C74D;
                Visibility = Hidden;
                Available = fun items -> canDefeatBotwoon items;
            };
            {
                Area = Maridia;
                Name = "Energy Tank, Botwoon";
                Class = Major;
                Address = 0x7C755;
                Visibility = Visible;
                Available = fun items -> canDefeatBotwoon items ||
                                         (canAccessOuterMaridia items && canDoSuitlessMaridia items);
            };
            {
                Area = Maridia;
                Name = "Space Jump";
                Class = Major;
                Address = 0x7C7A7;
                Visibility = Chozo;
                Available = fun items -> canDefeatDraygon items;
            }
        ];


class NewRandomizer:
    
    #let unusedLocation (location:Location) itemLocations =
    #    not (List.exists (fun itemLocation -> itemLocation.Location.Address = location.Address) itemLocations)
    @staticmethod
    def unusedLocation(location, itemLocations):
        return not List.exists(lambda itemLoc: itemLoc["Location"]["Address"] == location["Address"], itemLocations)

    #let currentLocations items itemLocations locationPool =
    #    List.filter (fun location -> location.Available items && unusedLocation location itemLocations ) locationPool
    @staticmethod
    def currentLocations(items, itemLocations, locationPool):
        return List.filter(lambda loc: loc["Available"](items) and unusedLocation(loc, itemLocations), locationPool)

    #let canPlaceAtLocation (item:Item) (location:Location) =
    #    location.Class = item.Class &&
    #    (match item.Type with
    #    | Gravity -> (not (location.Area = Crateria || location.Area = Brinstar)) || location.Name = "X-Ray Scope" || location.Name = "Energy Tank, Waterway"
    #    | Varia -> (not (location.Area = LowerNorfair || location.Area = Crateria || location.Name = "Morphing Ball" || location.Name = "Missile (blue Brinstar middle)" || location.Name = "Energy Tank, Brinstar Ceiling"))
    #    | SpeedBooster -> not (location.Name = "Morphing Ball" || location.Name = "Missile (blue Brinstar middle)" || location.Name = "Energy Tank, Brinstar Ceiling")
    #    | ScrewAttack -> not (location.Name = "Morphing Ball" || location.Name = "Missile (blue Brinstar middle)" || location.Name = "Energy Tank, Brinstar Ceiling")
    #    | _ -> true)
    @staticmethod
    def canPlaceAtLocation(item, location):
        matchingClass = (location["Class"] == item["Class"])
        if matchingClass is False:
            return False

        if item["Type"] == "Gravity":
            return ((not (location["Area"] == "Crateria" or location["Area"] == "Brinstar")) 
                    or location["Name"] == "X-Ray Scope" or location["Name"] == "Energy Tank, Waterway")
        elif item["Type"] == "Varia":
            return (not (location["Area"] == "LowerNorfair"
                          or location["Area"] == "Crateria"
                          or location["Name"] == "Morphing Ball"
                          or location["Name"] == "Missile (blue Brinstar middle)"
                          or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        elif item["Type"] == "SpeedBooster":
            return (not (location["Name"] == "Morphing Ball"
                         or location["Name"] == "Missile (blue Brinstar middle)"
                         or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        elif item["Type"] == "ScrewAttack":
            return (not (location["Name"] == "Morphing Ball"
                         or location["Name"] == "Missile (blue Brinstar middle)"
                         or location["Name"] == "Energy Tank, Brinstar Ceiling"))
        else:
            return True

    #let canPlaceItem (item:Item) itemLocations =
    #    List.exists (fun location -> canPlaceAtLocation item location) itemLocations
    @staticmethod
    def canPlaceItem(item, itemLocations):
        return List.exists(lambda loc: NewRandomizer.canPlaceAtLocation(item, loc), itemLocations)

    #let checkItem item items (itemLocations:ItemLocation list) locationPool =
    #    let oldLocations = (currentLocations items itemLocations locationPool)
    #    let newLocations = (currentLocations (item :: items) itemLocations locationPool)
    #    let newLocationsHasMajor = List.exists (fun l -> l.Class = Major) newLocations
    #    canPlaceItem item oldLocations && newLocationsHasMajor && (List.length newLocations) > (List.length oldLocations)
    @staticmethod
    def checkItem(item, items, itemLocations, locationPool):
        oldLocations = NewRandomizer.currentLocations(items, itemLocations, locationPool)
        newLocations = NewRandomizer.currentLocations([item] + items, itemLocations, locationPool)
        newLocationsHasMajor = List.exists(lambda l: l["Class"] == 'Major', newLocations)
        return (NewRandomizer.canPlaceItem(item, oldLocations)
                and newLocationsHasMajor
                and List.length(newLocations) > List.length(oldLocations))

    #let possibleItems items itemLocations itemPool locationPool =
    #    List.filter (fun item -> checkItem item items itemLocations locationPool) itemPool
    @staticmethod
    def possibleItems(items, itemLocations, itemPool, locationPool):
        return List.filter(lambda item: NewRandomizer.checkItem(item, items, itemLocations, locationPool), itemPool)

    #let rec removeItem itemType itemPool =
    #    match itemPool with
    #    | head :: tail -> if head.Type = itemType then tail else head :: removeItem itemType tail
    #    | [] -> itemPool
    @staticmethod
    def removeItem(itemType, itemPool):
        if len(itemPool) == 0:
            return itemPool
        else:
            head = itemPool[0]
            tail = itemPool[1:]
            if head["Type"] == itemType:
                return tail
            else:
                return head + NewRandomizer.removeItem(itemType, tail)

    #let placeItem (rnd:Random) (items:Item list) (itemPool:Item list) locations =
    #    let item = match List.length items with
    #               | 0 ->
    #                      if (List.exists (fun i -> i.Type = ScrewAttack) itemPool) then (List.find (fun i -> i.Type = ScrewAttack) itemPool)
    #                      elif (List.exists (fun i -> i.Type = SpeedBooster) itemPool) then (List.find (fun i -> i.Type = SpeedBooster) itemPool)
    #                      else List.item (rnd.Next (List.length itemPool)) itemPool
    #               | _ -> List.item (rnd.Next (List.length items)) items
    #
    #    let availableLocations = List.filter (fun location -> canPlaceAtLocation item location) locations
    #    { Item = item; Location = (List.item (rnd.Next (List.length availableLocations)) availableLocations) }
    @staticmethod
    def placeItem(rnd, items, itemPool, locations):
        itemsLen = List.length(items)
        if itemsLen == 0:
            if List.exists(lambda i: i["Type"] == "ScrewAttack", itemPool):
                item = List.find(lambda i: i["Type"] == "ScrewAttack", itemPool)
            elif List.exists(lambda i: i["Type"] == "SpeedBooster", itemPool):
                item = List.find(lambda i: i["Type"] == "SpeedBooster", itemPool)
            else:
                item = List.item(rnd.Next(0, List.length(itemPool)), itemPool)
        else:
            item = List.item(rnd.Next(0, List.length(items)), items)

        availableLocations = List.filter(lambda loc: NewRandomizer.canPlaceAtLocation(item, loc), locations)
        return {'Item': item, 'Locations': List.item(rnd.Next(0, List.length(availableLocations)), availableLocations)}

    #let placeSpecificItem (rnd:Random) item (itemPool:Item list) locations =
    #    let availableLocations = List.filter (fun location -> canPlaceAtLocation item location) locations
    #    { Item = item; Location = (List.item (rnd.Next (List.length availableLocations)) availableLocations) }
    @staticmethod
    def placeSpecificItem(rnd, item, itemPool, locations):
        availableLocations = List.filter(lambda loc: NewRandomizer.canPlaceAtLocation(item, loc), locations)
        return {'Item': item, 'Location': List.item(rnd.Next(0, List.length(availableLocations)), availableLocations)}

    #let placeSpecificItemAtLocation item location =
    #    { Item = item; Location = location }
    @staticmethod
    def placeSpecificItemAtLocation(item, location):
        return {'Item': item, 'Location': location}
    
    #let getEmptyLocations itemLocations (locationPool:Location list) =
    #    List.filter (fun (l:Location) -> unusedLocation l itemLocations) locationPool
    @staticmethod
    def getEmptyLocations(itemLocations, locationPool):
        return List.filter(lambda l: NewRandomizer.unusedLocation(l, itemLocations), locationPool)

    #let getItem itemType =
    #    List.find (fun i -> i.Type = itemType) Items.Items
    @staticmethod
    def getItem(itemType):
        return List.find(lambda i: i["Type"] == itemType, Items.Items)

    #let getAssumedItems item prefilledItems itemLocations itemPool =
    #    let items = removeItem item.Type itemPool
    #    let items = List.append items prefilledItems
    #    let accessibleItems = List.map (fun i -> i.Item) (List.filter (fun il -> (il.Location.Available items) && (not (List.exists (fun k -> k.Type = il.Item.Type) prefilledItems))) itemLocations)
    #    List.append items accessibleItems
    @staticmethod
    def getAssumedItems(item, prefilledItems, itemLocations, itemPool):
        items = NewRandomizer.removeItem(item["Type"], itemPool)
        items = List.append(items, prefilledItems)
        accessibleItems = List.map(lambda i: i.Item, List.filter(lambda il: il["Location"]["Available"](items) and not List.exists(lambda k: k["Type"] == il["Item"]["Type"], prefilledItems), itemLocations))
        return List.append(items, accessibleItems)

    #let rec generateAssumedItems prefilledItems items (itemLocations:ItemLocation list) (itemPool:Item list) locationPool =
    #    if not (List.exists (fun (l:Item) -> l.Category = Progression) itemPool) then
    #        (items, itemLocations, itemPool)
    #    else
    #        match itemPool with
    #        | [] -> (items, itemLocations, itemPool)
    #        | _ ->
    #            let item = List.head (List.filter (fun (i:Item) -> i.Category = Progression) itemPool)
    #            let assumedItems = getAssumedItems item prefilledItems itemLocations itemPool
    #            let availableLocations = List.filter (fun l -> l.Available assumedItems && canPlaceAtLocation item l) (getEmptyLocations itemLocations locationPool)
    #            let fillLocation = List.head availableLocations
    #
    #            let itemLocation = placeSpecificItemAtLocation item fillLocation
    #            generateAssumedItems prefilledItems (itemLocation.Item :: items) (itemLocation :: itemLocations) (removeItem itemLocation.Item.Type itemPool) locationPool
    @staticmethod
    def generateAssumedItems(prefilledItems, items, itemLocations, itemPool, locationPool):
        if not List.exists(lambda l: l["Category"] == "Progression", itemPool):
            return (items, itemLocations, itemPool)
        else:
            if len(itemPool) == 0:
                return (items, itemLocations, itemPool)
            else:
                item = List.head(List.filter(lambda i: i["Category"] == "Progression", itemPool))
                assumedItems = NewRandomizer.getAssumedItems(item, prefilledItems, itemLocations, itemPool)
                availableLocations = List.filter(lambda l: l["Available"](assumedItems) and NewRandomizer.canPlaceAtLocation(item, l), NewRandomizer.getEmptyLocations(itemLocations, locationPool))
                fillLocation = List.head(availableLocations)

                itemLocation = NewRandomizer.placeSpecificItemAtLocation(item, fillLocation)
                return NewRandomizer.generateAssumedItems(prefilledItems,
                                                          [itemLocation.Item] + items,
                                                          [itemLocation] + itemLocations,
                                                          NewRandomizer.removeItem(itemLocation["Item"]["Type"], itemPool),
                                                          locationPool)

    #let swap (a: _[]) x y =
    #    let tmp = a.[x]
    #    a.[x] <- a.[y]
    #    a.[y] <- tmp
    @staticmethod
    def swap(list, x, y):
        list[x], list[y] = list[y], list[x]
    
    #let shuffle (rnd:Random) a =
    #    Array.iteri (fun i _ -> swap a i (rnd.Next(i, Array.length a))) a
    @staticmethod
    def shuffle(rnd, a):
        Array.iteri(lambda i, _: swap(a, i, rnd.Next(i, Array.length(a))), a)

    #let rec generateMoreItems rnd items itemLocations itemPool locationPool =
    #    match itemPool with
    #    | [] -> itemLocations
    #    | _ ->
    #        let itemLocation = placeItem rnd (possibleItems items itemLocations itemPool locationPool) itemPool (currentLocations items itemLocations locationPool)
    #        generateMoreItems rnd (itemLocation.Item :: items) (itemLocation :: itemLocations) (removeItem itemLocation.Item.Type itemPool) locationPool
    @staticmethod
    def generateMoreItems(rnd, items, itemLocations, itemPool, locationPool):
        if len(itemPool) == 0:
            return itemLocations

        itemLocation = NewRandomizer.placeItem(rnd,
                                               NewRandomizer.possibleItems(items, itemLocations, itemPool, locationPool),
                                               itemPool,
                                               NewRandomizer.currentLocations(items, itemLocations, locationPool))
        return NewRandomizer.generateMoreItems(rnd,
                                               itemLocation["Item"] + items,
                                               itemLocation + itemLocations,
                                               NewRandomizer.removeItem(itemLocation["Item"]["Type"], itemPool),
                                               locationPool)

    #let rec getWeightedLocations (locationPool:Location list) num (locations:Map<int, Location>) =
    #    match locationPool with
    #    | [] -> List.map (fun (k,v) -> v) (List.sortBy (fun (k,v) -> k) (Map.toList locations))
    #    | loc :: tail ->
    #        let weight = num - (match loc.Area with
    #                            | Brinstar -> 0
    #                            | Crateria -> 0
    #                            | LowerNorfair -> 11
    #                            | Maridia -> 0
    #                            | Norfair -> 0
    #                            | WreckedShip -> 12)
    #        let locations = locations.Add(weight, loc)
    #        getWeightedLocations (List.filter (fun l -> l.Address <> loc.Address) locationPool) (num + 10) locations
    @staticmethod
    def getWeightedLocations(locationPool, num, locations):
        if len(locationPool) == 0:
            # TODO::Map.toList has already sorted by the keys
            return List.map(lambda (k, v): v, List.sortBy(lambda (k, v): k, Map.toList(locations)))

        loc = locationPool[0]
        tail = locationPool[1:]

        weigths = {'Brinstar': 0, 'Crateria': 0, 'LowerNorfair': 11, 'Maridia': 0, 'Norfair': 0, 'WreckedShip': 12}

        weigth = num - weigths[loc['Area']]
        locations = locations[weigth] = loc
        # TODO::why filter and not just use tail ?
        return NewRandomizer.getWeightedLocations(List.filter(lambda l: l["Address"] != loc["Address"], locationPool), num + 10, locations)

    #let prefill (rnd:Random) (itemType:ItemType) (items:Item list byref) (itemLocations:ItemLocation list byref) (itemPool:Item list byref) (locationPool: Location list) =
    #    let item = List.find (fun i -> i.Type = itemType) Items.Items
    #    let cl = List.filter (fun l -> l.Class = item.Class && canPlaceAtLocation item l) (currentLocations items itemLocations locationPool)
    #    let itemLocation = placeSpecificItemAtLocation item (List.item (rnd.Next (List.length cl)) cl)
    #    items <- itemLocation.Item :: items
    #    itemPool <- removeItem itemLocation.Item.Type itemPool
    #    itemLocations <- itemLocation :: itemLocations
    @staticmethod
    def prefill(rnd, itemType, items, itemLocations, itemPool, locationPool):
        # update parameters items, itemLocations, itemPool
        item = List.find(lambda i: i["Type"] == itemType, Items.Items)
        cl = List.filter(lambda l: l["Class"] == item["Class"] and NewRandomizer.canPlaceAtLocation(item, l), NewRandomizer.currentLocations(items, itemLocations, locationPool))
        itemLocation = NewRandomizer.placeSpecificItemAtLocation(item, List.item(rnd.Next(0, List.length(cl)), cl))
        items = [itemLocation.Item] + items
        itemPool = NewRandomizer.removeItem(itemLocation["Item"]["Type"], itemPool)
        itemLocations = [itemLocation] + itemLocations

    #let generateItems (rnd:Random) (items:Item list) (itemLocations:ItemLocation list) (itemPool:Item list) (locationPool:Location list) =
    #    let mutable newItems = items
    #    let mutable newItemLocations = itemLocations
    #    let mutable newItemPool = itemPool
    #
    #    // Place Morph at one of the earliest locations so that it's always accessible
    #    prefill rnd Morph &newItems &newItemLocations &newItemPool locationPool
    #
    #    // Place either a super or a missile to open up BT's location
    #    match rnd.Next(2) with
    #    | 0 -> prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
    #    | _ -> prefill rnd Super &newItems &newItemLocations &newItemPool locationPool
    #
    #    // Next step is to place items that opens up access to breaking bomb blocks
    #    // by placing either Screw/Speed/Bomb or just a PB pack early.
    #    // One PB pack will be placed after filling with other items so that there's at least on accessible
    #    match rnd.Next(13) with
    #    | 0 ->                          prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
    #                                    prefill rnd ScrewAttack &newItems &newItemLocations &newItemPool locationPool
    #                                    prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
    #    | 1 ->                          prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
    #                                    prefill rnd SpeedBooster &newItems &newItemLocations &newItemPool locationPool
    #                                    prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
    #    | 2 ->                          prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
    #                                    prefill rnd Bomb &newItems &newItemLocations &newItemPool locationPool
    #                                    prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
    #    | _ ->                          prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
    #
    #    // Place a super if it's not already placed
    #    if not (List.exists (fun i -> i.Type = Super) newItems) then
    #        prefill rnd Super &newItems &newItemLocations &newItemPool locationPool
    #
    #    // Save the prefilled items into a new list to be used later
    #    let prefilledItems = newItems
    #
    #    // Shuffle the locations randomly, then adjust the order slightly based on weighting per area
    #    let mutable shuffledLocations = List.toArray (List.filter (fun l -> l.Class = Major) locationPool)
    #    shuffle rnd shuffledLocations
    #    let weightedLocations = getWeightedLocations (Array.toList shuffledLocations) 100 Map.empty
    #
    #    // Shuffle the item pool
    #    let mutable shuffledItemsArr = List.toArray newItemPool
    #    shuffle rnd shuffledItemsArr
    #    let shuffledItems = Array.toList shuffledItemsArr
    #
    #    // Always start with placing a suit (this helps getting maximum spread of suit locations)
    #    let firstItem = match rnd.Next(2) with
    #                    | 0 -> List.find (fun i -> i.Type = Varia) shuffledItems
    #                    | _ -> List.find (fun i -> i.Type = Gravity) shuffledItems
    #
    #    let shuffledItems = firstItem :: List.filter (fun i -> i.Type <> firstItem.Type) shuffledItems
    #
    #    // Place the rest of progression items randomly
    #    let (progressItems, progressItemLocations, progressItemPool) = generateAssumedItems prefilledItems newItems newItemLocations shuffledItems weightedLocations
    #
    #    // All progression items are placed and every other location in the game should now be accessible
    #    // so place the rest of the items randomly using the regular placement method
    #    generateMoreItems rnd progressItems progressItemLocations progressItemPool locationPool

    #let generateItems (rnd:Random) (items:Item list) (itemLocations:ItemLocation list) (itemPool:Item list) (locationPool:Location list) =
    # called with: generateItems(rnd, [], [], (Items.getItemPool rnd), locationPool)
    @staticmethod
    def generateItems(rnd, items, itemLocations, itemPool, locationPool):
        newItems = items
        newItemLocations = itemLocations
        newItemPool = itemPool

        # Place Morph at one of the earliest locations so that it's always accessible
        NewRandomizer.prefill(rnd, "Morph", newItems, newItemLocations, newItemPool, locationPool)

        # Place either a super or a missile to open up BT's location 
        if rnd.Next(0, 2) == 0:
            NewRandomizer.prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
        else:
            NewRandomizer.prefill(rnd, "Super", newItems, newItemLocations, newItemPool, locationPool)

        # Next step is to place items that opens up access to breaking bomb blocks
        # by placing either Screw/Speed/Bomb or just a PB pack early.
        # One PB pack will be placed after filling with other items so that there's at least on accessible
        random = rnd.Next(0, 13)
        if random == 0:
            NewRandomizer.prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
            NewRandomizer.prefill(rnd, "ScrewAttack", newItems, newItemLocations, newItemPool, locationPool)
            NewRandomizer.prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)
        elif random == 1:
            NewRandomizer.prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
            NewRandomizer.prefill(rnd, "SpeedBooster", newItems, newItemLocations, newItemPool, locationPool)
            NewRandomizer.prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)
        elif random == 2:
            NewRandomizer.prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
            NewRandomizer.prefill(rnd, "Bomb", newItems, newItemLocations, newItemPool, locationPool)
            NewRandomizer.prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)
        else:
            NewRandomizer.prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)

        # Place a super if it's not already placed
        if not List.exists(lambda i: i["Type"] == "Super", newItems):
            NewRandomizer.prefill(rnd, "Super", newItems, newItemLocations, newItemPool, locationPool)

        # Save the prefilled items into a new list to be used later
        prefilledItems = newItems

        # Shuffle the locations randomly, then adjust the order slightly based on weighting per area
        shuffledLocations = List.toArray(List.filter(lambda l: l["Class"] == "Major", locationPool))
        NewRandomizer.shuffle(rnd, shuffledLocations)
        weightedLocations = NewRandomizer.getWeightedLocations(Array.toList(shuffledLocations), 100, {})

        # Shuffle the item pool
        shuffledItemsArr = List.toArray(newItemPool)
        NewRandomizer.shuffle(rnd, shuffledItemsArr)
        shuffledItems = Array.toList(shuffledItemsArr)

        # Always start with placing a suit (this helps getting maximum spread of suit locations)
        if rnd.Next(0, 2) == 0:
            firstItem = List.find(lambda i: i["Type"] == "Varia", shuffledItems)
        else:
            firstItem = List.find(lambda i: i["Type"] == "Gravity", shuffledItems)

        shuffledItems = [firstItem] + List.filter(lambda i: i["Type"] != firstItem["Type"], shuffledItems)

        # Place the rest of progression items randomly
        (progressItems, progressItemLocations, progressItemPool) = NewRandomizer.generateAssumedItems(prefilledItems, newItems, newItemLocations, shuffledItems, weightedLocations)

        # All progression items are placed and every other location in the game should now be accessible
        # so place the rest of the items randomly using the regular placement method
        return generateMoreItems(rnd, progressItems, progressItemLocations, progressItemPool, locationPool)

if __name__ == "__main__":

    #let rnd = Random(seed)
    #let itemLocations = writeSpoiler seed spoiler fileName (randomizer rnd [] [] (Items.getItemPool rnd) locationPool)
    #writeRomSpoiler data (List.sortBy (fun il -> il.Item.Type) (List.filter (fun il -> il.Item.Class = Major && il.Item.Type <> ETank && il.Item.Type <> Reserve) itemLocations)) 0x2f5240 |> ignore
    #//writeItemNames data Items.Items |> ignore
    #writeLocations data itemLocations        

    locationPool = []
    seed = 42
    rnd = Random(seed)
    NewRandomizer.generateItems(rnd, [], [], Items.getItemPool(rnd), locationPool)
