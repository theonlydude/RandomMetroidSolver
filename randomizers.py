# implement the randomizer in python
# https://github.com/tewtal/itemrandomizerweb/blob/master/ItemRandomizer/Randomizers.fs

class NewRandomizer:
    
    def unusedLocation(location, itemLocations):
        return not (True in [loc["Address"] == location["Address"] for loc in itemLocations])

    def currentLocations(items, itemLocations, locationPool):
        return [loc for loc in locationPool if loc["Available"](items) and unusedLocation(loc, itemLocations)]

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

    def canPlaceItem(item, itemLocations):
        return True in [canPlaceAtLocation(item, loc) for loc in itemLocations]

    def checkItem(item, items, itemLocations, locationPool):
        oldLocations = currentLocations(items, itemLocations, locationPool)
        newLocations = currentLocations([item] + items, itemLocations, locationPool)
        newLocationsHasMajor = (True in [loc["Class"] == "Major" for loc in newLocations])
        return (canPlaceItem(item, oldLocations)
                and newLocationsHasMajor
                and len(newLocations) > len(oldLocations))

    def possibleItems(items, itemLocations, itemPool, locationPool):
        return [item for item in itemPool if checkItem(item, items, itemLocations, locationPool)]
    
    def removeItem(itemType, itemPool):
        return [item for item in itemPool if item["Type"] != itemType]

    def placeItem(rnd, items, itemPool, locations):
        itemsLen = len(items)
        if itemsLen == 0:
            try:
                item = next(item for item in itemPool if item["Type"] == 'ScrewAttack')
            except StopIteration:
                try:
                    item = next(item for item in itemPool if item["Type"] == 'SpeedBooster')
                except StopIteration:
                    item = itemPool[rnd.Next(0, len(itemPool))]
        else:
            item = items[rnd.Next(0, itemsLen)]

        availableLocations = [loc for loc in locations if canPlaceAtLocation(item, loc)]
        return {'Item': item, 'Location': availableLocations[rnd.Next(0, len(availableLocations))]}

    def placeSpecificItem(rnd, item, itemPool, locations):
        availableLocations = [loc for loc in locations if canPlaceAtLocation(item, loc)]
        return {'Item': item, 'Location': availableLocations[rnd.Next(0, len(availableLocations))]}

    def placeSpecificItemAtLocation(item, location):
        return {'Item': item, 'Location': location}
    
    def getEmptyLocations(itemLocations, locationPool):
        return [loc for loc in locationPool if unusedLocation(loc, itemLocations)]

    def getItem(itemType):
        # TODO::what's Items.Items ??
        return [item for item in Items.Items if item["Type"] == itemType][0]

    let getAssumedItems item prefilledItems itemLocations itemPool = 
        let items = removeItem item.Type itemPool
        let items = List.append items prefilledItems
        let accessibleItems = List.map (fun i -> i.Item) (List.filter (fun il -> (il.Location.Available items) && (not (List.exists (fun k -> k.Type = il.Item.Type) prefilledItems))) itemLocations)
        List.append items accessibleItems
    def getAssumedItems(item, prefilledItems, itemLocations, itemPool):
        items = removeItem(item["Type"], itemPool)
        items = items + prefilledItems
        filteredLocations = [loc for loc in itemLocations if loc.Location["Available"](items) and ]
        #accessibleItems = [loc["Item"] for loc in itemLocations]
        return items + accessibleItems

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
            

    let swap (a: _[]) x y =
        let tmp = a.[x]
        a.[x] <- a.[y]
        a.[y] <- tmp
    
    let shuffle (rnd:Random) a =
        Array.iteri (fun i _ -> swap a i (rnd.Next(i, Array.length a))) a

    let rec generateMoreItems rnd items itemLocations itemPool locationPool =
        match itemPool with
        | [] -> itemLocations
        | _ ->            
            let itemLocation = placeItem rnd (possibleItems items itemLocations itemPool locationPool) itemPool (currentLocations items itemLocations locationPool)
            generateMoreItems rnd (itemLocation.Item :: items) (itemLocation :: itemLocations) (removeItem itemLocation.Item.Type itemPool) locationPool

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
    def prefill(rnd, itemType, items, itemLocations, itemPool, locationPool):
        item = 
        cl = 
        itemLocation = 
        return ([itemLocation.Item] + items, removeItem(itemLocation.Item.Type, itemPool), [itemLocation] + itemLocations)

    # called with: generateItems(rnd, [], [], (Items.getItemPool rnd), locationPool)
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
