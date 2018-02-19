#!/usr/bin/python

from itemrandomizerweb.stdlib import Random
from itemrandomizerweb import Items
#import TournamentLocations
from NewRandomizer import NewRandomizer
from tournament_locations import locations
from helpers import canEnterAndLeaveGauntlet, wand, wor, haveItem, canOpenRedDoors
from helpers import canPassBombPassages, canDestroyBombWalls, canUsePowerBombs, SMBool
from helpers import canFly, canAccessRedBrinstar, energyReserveCountOk, canAccessKraid
from helpers import Bosses, enoughStuffsKraid, heatProof, energyReserveCountOk
from helpers import energyReserveCountOkHellRun, canAccessCrocomire, canAccessHeatedNorfair
from helpers import canPassWorstRoom, enoughStuffsRidley, canAccessLowerNorfair
from helpers import canAccessWs, enoughStuffsPhantoon, enoughStuffsDraygon
from helpers import canAccessOuterMaridia, canDefeatDraygon, canPassMtEverest
from helpers import canAccessInnerMaridia, canFlyDiagonally, canDefeatBotwoon
from helpers import canCrystalFlash, canOpenGreenDoors, canHellRun

if __name__ == "__main__":

    #let rnd = Random(seed)
    #let itemLocations = writeSpoiler seed spoiler fileName (randomizer rnd [] [] (Items.getItemPool rnd) locationPool)
    #writeRomSpoiler data (List.sortBy (fun il -> il.Item.Type) (List.filter (fun il -> il.Item.Class = Major && il.Item.Type <> ETank && il.Item.Type <> Reserve) itemLocations)) 0x2f5240 |> ignore
    #//writeItemNames data Items.Items |> ignore
    #writeLocations data itemLocations        

    #locationPool = TournamentLocations.AllLocations
    seed = 9876543
    locationPool = locations

    randomizer = NewRandomizer(seed)
    itemLocs = randomizer.generateItems([], [])

    # transform itemLocs in our usual dict(location, item)
    locsItems = {}
    for itemLoc in itemLocs:
        locsItems[itemLoc["Location"]["Name"]] = itemLoc["Item"]["Type"]

    #print(locsItems)

    for loc in locsItems:
        print('{:>50}: {:>16} '.format(loc, locsItems[loc]))
