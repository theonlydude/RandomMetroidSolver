# implement the randomizer in python
# https://github.com/tewtal/itemrandomizerweb/blob/master/ItemRandomizer/Randomizers.fs

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
        return List.find(lambda item: item["Type"] == itemType, Items.Items) + itemPool

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
        return List.filter(lambda loc -> loc["Available"](items) and unusedLocation(loc, itemLocations), locationPool)

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
        filteredLocations = [loc for loc in itemLocations if loc.Location["Available"](items) and ]
        accessibleItems = List.map(lambda i: i.Item, List.filter(lambda il: il["Location"]["Available"](items) and not List.exists(lambda k: k["Type"] == il["Item"]["Type"], prefilledItems), itemLocations))
        return List.append(items, accessibleItems)

    let rec generateAssumedItems prefilledItems items (itemLocations:ItemLocation list) (itemPool:Item list) locationPool =
        if not (List.exists (fun (l:Item) -> l.Category = Progression) itemPool) then
            (items, itemLocations, itemPool)
        else
            match itemPool with
            | [] -> (items, itemLocations, itemPool)
            | _ ->
                let item = List.head (List.filter (fun (i:Item) -> i.Category = Progression) itemPool)
                let assumedItems = getAssumedItems item prefilledItems itemLocations itemPool
                let availableLocations = List.filter (fun l -> l.Available assumedItems && canPlaceAtLocation item l) (getEmptyLocations itemLocations locationPool)
                let fillLocation = List.head availableLocations

                let itemLocation = placeSpecificItemAtLocation item fillLocation
                generateAssumedItems prefilledItems (itemLocation.Item :: items) (itemLocation :: itemLocations) (removeItem itemLocation.Item.Type itemPool) locationPool
    @staticmethod
    def generateAssumedItems(prefilledItems, items, itemLocations, itemPool, locationPool):
        pass

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

    let rec getWeightedLocations (locationPool:Location list) num (locations:Map<int, Location>) =
        match locationPool with
        | [] -> List.map (fun (k,v) -> v) (List.sortBy (fun (k,v) -> k) (Map.toList locations))
        | loc :: tail ->
            let weight = num - (match loc.Area with
                                | Brinstar -> 0
                                | Crateria -> 0
                                | LowerNorfair -> 11
                                | Maridia -> 0
                                | Norfair -> 0
                                | WreckedShip -> 12)
            let locations = locations.Add(weight, loc)
            getWeightedLocations (List.filter (fun l -> l.Address <> loc.Address) locationPool) (num + 10) locations

    let prefill (rnd:Random) (itemType:ItemType) (items:Item list byref) (itemLocations:ItemLocation list byref) (itemPool:Item list byref) (locationPool: Location list) =
        let item = List.find (fun i -> i.Type = itemType) Items.Items
        let cl = List.filter (fun l -> l.Class = item.Class && canPlaceAtLocation item l) (currentLocations items itemLocations locationPool)
        let itemLocation = placeSpecificItemAtLocation item (List.item (rnd.Next (List.length cl)) cl)
        items <- itemLocation.Item :: items
        itemPool <- removeItem itemLocation.Item.Type itemPool
        itemLocations <- itemLocation :: itemLocations
    @staticmethod
    def prefill(rnd, itemType, items, itemLocations, itemPool, locationPool):
        item = 
        cl = 
        itemLocation = 
        return ([itemLocation.Item] + items, removeItem(itemLocation.Item.Type, itemPool), [itemLocation] + itemLocations)

    # called with: generateItems(rnd, [], [], (Items.getItemPool rnd), locationPool)
    @staticmethod
    def generateItems(rnd, items, itemLocations, itemPool, locationPool):
        #let generateItems (rnd:Random) (items:Item list) (itemLocations:ItemLocation list) (itemPool:Item list) (locationPool:Location list) =
        let mutable newItems = items
        let mutable newItemLocations = itemLocations
        let mutable newItemPool = itemPool

        # Place Morph at one of the earliest locations so that it's always accessible
        prefill(rnd, "Morph", &newItems, &newItemLocations, &newItemPool, locationPool)
        
        # Place either a super or a missile to open up BT's location 
        match rnd.Next(2) with
        | 0 -> prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
        | _ -> prefill rnd Super &newItems &newItemLocations &newItemPool locationPool

        # Next step is to place items that opens up access to breaking bomb blocks
        # by placing either Screw/Speed/Bomb or just a PB pack early.
        # One PB pack will be placed after filling with other items so that there's at least on accessible
        match rnd.Next(13) with
        | 0 ->                          prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
                                        prefill rnd ScrewAttack &newItems &newItemLocations &newItemPool locationPool
                                        prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
        | 1 ->                          prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
                                        prefill rnd SpeedBooster &newItems &newItemLocations &newItemPool locationPool
                                        prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
        | 2 ->                          prefill rnd Missile &newItems &newItemLocations &newItemPool locationPool
                                        prefill rnd Bomb &newItems &newItemLocations &newItemPool locationPool
                                        prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
        | _ ->                          prefill rnd PowerBomb &newItems &newItemLocations &newItemPool locationPool
        
        # Place a super if it's not already placed
        if not (List.exists (fun i -> i.Type = Super) newItems) then
            prefill rnd Super &newItems &newItemLocations &newItemPool locationPool
        
        # Save the prefilled items into a new list to be used later
        let prefilledItems = newItems

        # Shuffle the locations randomly, then adjust the order slightly based on weighting per area
        let mutable shuffledLocations = List.toArray (List.filter (fun l -> l.Class = Major) locationPool)
        shuffle rnd shuffledLocations
        let weightedLocations = getWeightedLocations (Array.toList shuffledLocations) 100 Map.empty

        # Shuffle the item pool
        let mutable shuffledItemsArr = List.toArray newItemPool
        shuffle rnd shuffledItemsArr
        let shuffledItems = Array.toList shuffledItemsArr

        # Always start with placing a suit (this helps getting maximum spread of suit locations)
        let firstItem = match rnd.Next(2) with
                        | 0 -> List.find (fun i -> i.Type = Varia) shuffledItems
                        | _ -> List.find (fun i -> i.Type = Gravity) shuffledItems

        let shuffledItems = firstItem :: List.filter (fun i -> i.Type <> firstItem.Type) shuffledItems

        # Place the rest of progression items randomly
        let (progressItems, progressItemLocations, progressItemPool) = generateAssumedItems prefilledItems newItems newItemLocations shuffledItems weightedLocations
        
        # All progression items are placed and every other location in the game should now be accessible
        # so place the rest of the items randomly using the regular placement method
        generateMoreItems rnd progressItems progressItemLocations progressItemPool locationPool
