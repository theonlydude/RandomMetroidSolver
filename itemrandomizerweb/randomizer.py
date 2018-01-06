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
    seed = 42
    rnd = Random(seed)
    locs = NewRandomizer.generateItems(rnd, [], [], Items.getItemPool(rnd), locationPool)
    print("Generated locations: {}".format(locs))
