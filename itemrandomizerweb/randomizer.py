#!/usr/bin/python

from stdlib import Map, Array, List, Random
import Items
import TournamentLocations
import NewRandomizer

if __name__ == "__main__":

    #let rnd = Random(seed)
    #let itemLocations = writeSpoiler seed spoiler fileName (randomizer rnd [] [] (Items.getItemPool rnd) locationPool)
    #writeRomSpoiler data (List.sortBy (fun il -> il.Item.Type) (List.filter (fun il -> il.Item.Class = Major && il.Item.Type <> ETank && il.Item.Type <> Reserve) itemLocations)) 0x2f5240 |> ignore
    #//writeItemNames data Items.Items |> ignore
    #writeLocations data itemLocations        

    locationPool = TournamentLocations.AllLocations
    seed = 6869602
    rnd = Random(seed)
    itemLocs = NewRandomizer.generateItems(rnd, [], [], Items.getItemPool(rnd), locationPool)

    for itemLoc in itemLocs:
        item = itemLoc["Item"]["Type"]
        loc = itemLoc["Location"]["Name"]
        area = itemLoc["Location"]["Area"]
        print('{:>50}: {:>12} {:>16} '.format(loc, area, item))
