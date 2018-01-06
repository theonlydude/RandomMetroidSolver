from stdlib import Map, Array, List, Random
import Items

# https://github.com/tewtal/itemrandomizerweb/blob/master/ItemRandomizer/Randomizers.fs

#let unusedLocation (location:Location) itemLocations =
#    not (List.exists (fun itemLocation -> itemLocation.Location.Address = location.Address) itemLocations)
def unusedLocation(location, itemLocations):
    return not List.exists(lambda itemLoc: itemLoc["Location"]["Address"] == location["Address"], itemLocations)

#let currentLocations items itemLocations locationPool =
#    List.filter (fun location -> location.Available items && unusedLocation location itemLocations ) locationPool
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
def canPlaceItem(item, itemLocations):
    return List.exists(lambda loc: canPlaceAtLocation(item, loc), itemLocations)

#let checkItem item items (itemLocations:ItemLocation list) locationPool =
#    let oldLocations = (currentLocations items itemLocations locationPool)
#    let newLocations = (currentLocations (item :: items) itemLocations locationPool)
#    let newLocationsHasMajor = List.exists (fun l -> l.Class = Major) newLocations
#    canPlaceItem item oldLocations && newLocationsHasMajor && (List.length newLocations) > (List.length oldLocations)
def checkItem(item, items, itemLocations, locationPool):
    oldLocations = currentLocations(items, itemLocations, locationPool)
    newLocations = currentLocations([item] + items, itemLocations, locationPool)
    newLocationsHasMajor = List.exists(lambda l: l["Class"] == 'Major', newLocations)
    return (canPlaceItem(item, oldLocations)
            and newLocationsHasMajor
            and List.length(newLocations) > List.length(oldLocations))

#let possibleItems items itemLocations itemPool locationPool =
#    List.filter (fun item -> checkItem item items itemLocations locationPool) itemPool
def possibleItems(items, itemLocations, itemPool, locationPool):
    return List.filter(lambda item: checkItem(item, items, itemLocations, locationPool), itemPool)

#let rec removeItem itemType itemPool =
#    match itemPool with
#    | head :: tail -> if head.Type = itemType then tail else head :: removeItem itemType tail
#    | [] -> itemPool
def removeItem(itemType, itemPool):
    if len(itemPool) == 0:
        return itemPool
    else:
        head = itemPool[0]
        tail = itemPool[1:]
        if head["Type"] == itemType:
            return tail
        else:
            return [head] + removeItem(itemType, tail)

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

    availableLocations = List.filter(lambda loc: canPlaceAtLocation(item, loc), locations)
    return {'Item': item, 'Location': List.item(rnd.Next(0, List.length(availableLocations)), availableLocations)}

#let placeSpecificItem (rnd:Random) item (itemPool:Item list) locations =
#    let availableLocations = List.filter (fun location -> canPlaceAtLocation item location) locations
#    { Item = item; Location = (List.item (rnd.Next (List.length availableLocations)) availableLocations) }
def placeSpecificItem(rnd, item, itemPool, locations):
    availableLocations = List.filter(lambda loc: canPlaceAtLocation(item, loc), locations)
    return {'Item': item, 'Location': List.item(rnd.Next(0, List.length(availableLocations)), availableLocations)}

#let placeSpecificItemAtLocation item location =
#    { Item = item; Location = location }
def placeSpecificItemAtLocation(item, location):
    return {'Item': item, 'Location': location}

#let getEmptyLocations itemLocations (locationPool:Location list) =
#    List.filter (fun (l:Location) -> unusedLocation l itemLocations) locationPool
def getEmptyLocations(itemLocations, locationPool):
    return List.filter(lambda l: unusedLocation(l, itemLocations), locationPool)

#let getItem itemType =
#    List.find (fun i -> i.Type = itemType) Items.Items
def getItem(itemType):
    return List.find(lambda i: i["Type"] == itemType, Items.Items)

#let getAssumedItems item prefilledItems itemLocations itemPool =
#    let items = removeItem item.Type itemPool
#    let items = List.append items prefilledItems
#    let accessibleItems = List.map (fun i -> i.Item) (List.filter (fun il -> (il.Location.Available items) && (not (List.exists (fun k -> k.Type = il.Item.Type) prefilledItems))) itemLocations)
#    List.append items accessibleItems
def getAssumedItems(item, prefilledItems, itemLocations, itemPool):
    items = removeItem(item["Type"], itemPool)
    items = List.append(items, prefilledItems)
    accessibleItems = List.map(lambda i: i["Item"], List.filter(lambda il: il["Location"]["Available"](items) and not List.exists(lambda k: k["Type"] == il["Item"]["Type"], prefilledItems), itemLocations))
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
def generateAssumedItems(prefilledItems, items, itemLocations, itemPool, locationPool):
    if not List.exists(lambda l: l["Category"] == "Progression", itemPool):
        return (items, itemLocations, itemPool)
    else:
        if len(itemPool) == 0:
            return (items, itemLocations, itemPool)
        else:
            item = List.head(List.filter(lambda i: i["Category"] == "Progression", itemPool))
            assumedItems = getAssumedItems(item, prefilledItems, itemLocations, itemPool)
            availableLocations = List.filter(lambda l: l["Available"](assumedItems) and canPlaceAtLocation(item, l), getEmptyLocations(itemLocations, locationPool))
            fillLocation = List.head(availableLocations)

            itemLocation = placeSpecificItemAtLocation(item, fillLocation)
            return generateAssumedItems(prefilledItems,
                                                      [itemLocation["Item"]] + items,
                                                      [itemLocation] + itemLocations,
                                                      removeItem(itemLocation["Item"]["Type"], itemPool),
                                                      locationPool)

#let swap (a: _[]) x y =
#    let tmp = a.[x]
#    a.[x] <- a.[y]
#    a.[y] <- tmp
def swap(list, x, y):
    list[x], list[y] = list[y], list[x]

#let shuffle (rnd:Random) a =
#    Array.iteri (fun i _ -> swap a i (rnd.Next(i, Array.length a))) a
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

    itemLocation = placeItem(rnd,
                             possibleItems(items, itemLocations, itemPool, locationPool),
                             itemPool,
                             currentLocations(items, itemLocations, locationPool))
    return generateMoreItems(rnd,
                             [itemLocation["Item"]] + items,
                             [itemLocation] + itemLocations,
                             removeItem(itemLocation["Item"]["Type"], itemPool),
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
def getWeightedLocations(locationPool, num, locations):
    if len(locationPool) == 0:
        # TODO::Map.toList has already sorted by the keys
        return List.map(lambda k_v: k_v[1], List.sortBy(lambda k_v: k_v[0], Map.toList(locations)))

    loc = locationPool[0]
    tail = locationPool[1:]

    weigths = {'Brinstar': 0, 'Crateria': 0, 'LowerNorfair': 11, 'Maridia': 0, 'Norfair': 0, 'WreckedShip': 12}

    weigth = num - weigths[loc['Area']]
    locations[weigth] = loc
    # TODO::why filter and not just use tail ?
    return getWeightedLocations(List.filter(lambda l: l["Address"] != loc["Address"], locationPool), num + 10, locations)

#let prefill (rnd:Random) (itemType:ItemType) (items:Item list byref) (itemLocations:ItemLocation list byref) (itemPool:Item list byref) (locationPool: Location list) =
#    let item = List.find (fun i -> i.Type = itemType) Items.Items
#    let cl = List.filter (fun l -> l.Class = item.Class && canPlaceAtLocation item l) (currentLocations items itemLocations locationPool)
#    let itemLocation = placeSpecificItemAtLocation item (List.item (rnd.Next (List.length cl)) cl)
#    items <- itemLocation.Item :: items
#    itemPool <- removeItem itemLocation.Item.Type itemPool
#    itemLocations <- itemLocation :: itemLocations
def prefill(rnd, itemType, items, itemLocations, itemPool, locationPool):
    # update parameters: items, itemLocations, itemPool
    item = List.find(lambda i: i["Type"] == itemType, Items.Items)
    cl = List.filter(lambda l: l["Class"] == item["Class"] and canPlaceAtLocation(item, l), currentLocations(items, itemLocations, locationPool))
    itemLocation = placeSpecificItemAtLocation(item, List.item(rnd.Next(0, List.length(cl)), cl))
    items = [itemLocation["Item"]] + items
    itemPool = removeItem(itemLocation["Item"]["Type"], itemPool)
    itemLocations = [itemLocation] + itemLocations
    return (items, itemLocations, itemPool)

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
def generateItems(rnd, items, itemLocations, itemPool, locationPool):
    newItems = items
    newItemLocations = itemLocations
    newItemPool = itemPool

    # Place Morph at one of the earliest locations so that it's always accessible
    #print("generateItems::begin::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))
    (newItems, newItemLocations, newItemPool) = prefill(rnd, "Morph", newItems, newItemLocations, newItemPool, locationPool)
    #print("generateItems::morph::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

    # Place either a super or a missile to open up BT's location 
    if rnd.Next(0, 2) == 0:
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
    else:
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "Super", newItems, newItemLocations, newItemPool, locationPool)
    #print("generateItems::missile::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

    # Next step is to place items that opens up access to breaking bomb blocks
    # by placing either Screw/Speed/Bomb or just a PB pack early.
    # One PB pack will be placed after filling with other items so that there's at least on accessible
    random = rnd.Next(0, 13)
    if random == 0:
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "ScrewAttack", newItems, newItemLocations, newItemPool, locationPool)
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)
    elif random == 1:
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "SpeedBooster", newItems, newItemLocations, newItemPool, locationPool)
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)
    elif random == 2:
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "Missile", newItems, newItemLocations, newItemPool, locationPool)
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "Bomb", newItems, newItemLocations, newItemPool, locationPool)
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)
    else:
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "PowerBomb", newItems, newItemLocations, newItemPool, locationPool)
    #print("generateItems::break bomb block::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

    # Place a super if it's not already placed
    if not List.exists(lambda i: i["Type"] == "Super", newItems):
        (newItems, newItemLocations, newItemPool) = prefill(rnd, "Super", newItems, newItemLocations, newItemPool, locationPool)
        #print("generateItems::super::newItems {}, newItemLocations {}, newItemPool {}".format(len(newItems), len(newItemLocations), len(newItemPool)))

    # Save the prefilled items into a new list to be used later
    prefilledItems = newItems

    # Shuffle the locations randomly, then adjust the order slightly based on weighting per area
    shuffledLocations = List.toArray(List.filter(lambda l: l["Class"] == "Major", locationPool))
    shuffle(rnd, shuffledLocations)
    weightedLocations = getWeightedLocations(Array.toList(shuffledLocations), 100, {})

    # Shuffle the item pool
    shuffledItemsArr = List.toArray(newItemPool)
    shuffle(rnd, shuffledItemsArr)
    shuffledItems = Array.toList(shuffledItemsArr)

    # Always start with placing a suit (this helps getting maximum spread of suit locations)
    if rnd.Next(0, 2) == 0:
        firstItem = List.find(lambda i: i["Type"] == "Varia", shuffledItems)
    else:
        firstItem = List.find(lambda i: i["Type"] == "Gravity", shuffledItems)

    shuffledItems = [firstItem] + List.filter(lambda i: i["Type"] != firstItem["Type"], shuffledItems)

    # Place the rest of progression items randomly
    (progressItems, progressItemLocations, progressItemPool) = generateAssumedItems(prefilledItems, newItems, newItemLocations, shuffledItems, weightedLocations)

    # All progression items are placed and every other location in the game should now be accessible
    # so place the rest of the items randomly using the regular placement method
    return generateMoreItems(rnd, progressItems, progressItemLocations, progressItemPool, locationPool)
