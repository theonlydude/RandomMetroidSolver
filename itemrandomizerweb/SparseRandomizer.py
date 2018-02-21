from NewRandomizer import NewRandomizer
from stdlib import Map, Array, List, Random
import Items
import random

class SparseRandomizer(NewRandomizer):
    def __init__(self, seed, difficultyTarget, locations):
        super(SparseRandomizer, self).__init__(seed, difficultyTarget, locations)

    def canPlaceAtLocation(self, item, location):
        # check item class and location class, then for special items restrict some locations/areas
        #
        # item: dict of an item
        # location: dict of a location

        matchingClass = (location["Class"] == item["Class"])
        if matchingClass is False:
            return False

        if item["Type"] == "Gravity":
            return ((not (location["Area"] == "Crateria" or location["Area"] == "Brinstar"))
                    or location["Name"] == "X-Ray Scope" or location["Name"] == "Energy Tank, Waterway")
        elif item["Type"] == "Varia":
            return not (location["Area"] == "Crateria")
        else:
            return True

    def checkItem(self, curLocs, item, items, itemLocations, locationPool):
        # get the list of unused locations accessible with the given items (old),
        # the list of unused locations accessible with the given items and the new item (new).
        # check that there's a major location in the new list for next iteration of placement.
        # check that there's more 
        #
        # item: dict of the item to check
        # items: list of items already placed
        # itemLocations: list of dict with the current association of (item - location)
        # locationPool: list of the 100 locations
        #
        # return bool
        oldLocations = curLocs
        canPlaceIt = self.canPlaceItem(item, oldLocations)
        if canPlaceIt is False:
            return False

        newLocations = self.currentLocations([item] + items)
        newLocationsHasMajor = List.exists(lambda l: l["Class"] == 'Major', newLocations)

        return newLocationsHasMajor and len(newLocations) > len(oldLocations)




        let newLocationsHasMajor = List.exists (fun (l:Location) -> l.Class = Major && not (List.exists (fun (ol:Location) -> ol.Address = l.Address) oldLocations)) newLocations

        canPlaceItem item oldLocations && (newLocationsHasMajor || item.Class = Major) && (List.length newLocations) > (List.length oldLocations)

    new
    let checkFillerItem item items (itemLocations:ItemLocation list) locationPool =
        let oldLocations = (currentLocations items itemLocations locationPool)
        canPlaceItem item oldLocations

    new
    let getNewLocations item items (itemLocations:ItemLocation list) locationPool =
        let oldLocations = (currentLocations items itemLocations locationPool)
        let newLocations = (currentLocations (item :: items) itemLocations locationPool)
        match item.Type with 
        | Varia -> (((List.length newLocations) - (List.length oldLocations)) + 1) * 3
        | Gravity -> (((List.length newLocations) - (List.length oldLocations)) + 1) * 4
        | Super -> ((List.length newLocations) - (List.length oldLocations)) + 1
        | PowerBomb -> ((List.length newLocations) - (List.length oldLocations)) + 2
        | _ -> ((List.length newLocations) - (List.length oldLocations))

    diff
    let possibleItems items itemLocations itemPool locationPool =
        List.sortBy (fun item -> getNewLocations item items itemLocations locationPool) (List.filter (fun item -> checkItem item items itemLocations locationPool) itemPool)

    new
    let possibleFillerItems items itemLocations itemPool locationPool =
        List.filter (fun item -> checkFillerItem item items itemLocations locationPool) itemPool


    diff
    let placeItem (rnd:Random) (items:Item list) (itemPool:Item list) locations =
        let item = (match List.length items with
                    | 0 -> List.item (rnd.Next (List.length itemPool)) itemPool
                    | _ -> List.item (((rnd.Next (List.length items))+1)/2) items)
    
        let availableLocations = List.filter (fun location -> canPlaceAtLocation item location) locations

        { Item = item; Location = (List.item (rnd.Next (List.length availableLocations)) availableLocations) }

    new
    let placeFiller (rnd:Random) (items:Item list) (itemPool:Item list) (itemLocations:ItemLocation list) locations =
        let sortedList = List.sortBy (fun (i:Item) -> getNewLocations i items itemLocations locations) items
        let item = sortedList.Head
        
        let availableLocations = List.filter (fun location -> canPlaceAtLocation item location) locations
        { Item = item; Location = (List.item (rnd.Next (List.length availableLocations)) availableLocations) }

    new
    let rec fillItems rnd items itemLocations itemPool locationPool =
        let initialLocations = (currentLocations items itemLocations locationPool)
        let possibleItems = (possibleFillerItems items itemLocations itemPool locationPool)
        match List.length possibleItems with
            | 0 -> (items, itemLocations, itemPool)
            | _ ->
                let itemLocation = placeFiller rnd possibleItems itemPool itemLocations initialLocations
                fillItems rnd (itemLocation.Item :: items) (itemLocation :: itemLocations) (removeItem itemLocation.Item.Type itemPool) locationPool 


    diff
    let rec generateItems rnd items itemLocations itemPool locationPool =
        match itemPool with
        | [] -> itemLocations
        | _ ->
            // First we get a random item that will advance the progress
            let initialLocations = (currentLocations items itemLocations locationPool)
            let itemLocation = placeItem rnd (possibleItems items itemLocations itemPool locationPool) itemPool initialLocations

            // Now fill all other spots with "trash"
            let fillLocations = List.filter (fun (l:Location) -> l.Address <> itemLocation.Location.Address) initialLocations
            let (newItems, newItemLocations, newItemPool) = fillItems rnd (itemLocation.Item :: items) (itemLocation :: itemLocations) (removeItem itemLocation.Item.Type itemPool) fillLocations
            
            generateItems rnd newItems newItemLocations newItemPool locationPool
