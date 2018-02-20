#!/usr/bin/python

import argparse, random

from itemrandomizerweb.stdlib import Random
from itemrandomizerweb import Items
from itemrandomizerweb.Randomizer import Randomizer
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
from parameters import hard
from solver import ParamsLoader

if __name__ == "__main__":

    #let rnd = Random(seed)
    #let itemLocations = writeSpoiler seed spoiler fileName (randomizer rnd [] [] (Items.getItemPool rnd) locationPool)
    #writeRomSpoiler data (List.sortBy (fun il -> il.Item.Type) (List.filter (fun il -> il.Item.Class = Major && il.Item.Type <> ETank && il.Item.Type <> Reserve) itemLocations)) 0x2f5240 |> ignore
    #//writeItemNames data Items.Items |> ignore
    #writeLocations data itemLocations        

    parser = argparse.ArgumentParser(description="Random Metroid Randomizer")
    parser.add_argument('--param', '-p', help="the input parameters", nargs='+', default=None, dest='paramsFileName')

    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--difficultyTarget', '-t', help="the maximum difficulty target that the randomizer will use", dest='difficultyTarget', nargs='?', default=None, type=int)
    parser.add_argument('--seed', '-s', help="randomization seed to use", dest='seed', nargs='?', default=0, type=int)
    parser.add_argument('--algo', '-a', help="randomization algorithm to use", dest='algo', nargs='?', default=None)

    args = parser.parse_args()

    if args.paramsFileName is not None:
        ParamsLoader.factory(args.paramsFileName[0]).load()
    
    if args.seed == 0:
        seed = random.randint(0, 9999999)
    else:
        seed = args.seed

    print("seed={}".format(seed))

    if args.difficultyTarget is not None:
        difficultyTarget = args.difficultyTarget
    else:
        difficultyTarget = hard

    if args.algo is not None:
        algo = args.algo
    else:
        algo = 'Total_Tournament'

    locationPool = locations

    randomizer = Randomizer.factory(algo, seed, difficultyTarget, locations)
    itemLocs = randomizer.generateItems([], [])

    # transform itemLocs in our usual dict(location, item)
    locsItems = {}
    for itemLoc in itemLocs:
        locsItems[itemLoc["Location"]["Name"]] = itemLoc["Item"]["Type"]

    #print(locsItems)

    for loc in locsItems:
        print('{:>50}: {:>16} '.format(loc, locsItems[loc]))
