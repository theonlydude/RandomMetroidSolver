#!/usr/bin/python

import argparse, random, os.path, json, sys, shutil

from itemrandomizerweb.stdlib import Random
from itemrandomizerweb import Items
from itemrandomizerweb.Randomizer import Randomizer
from tournament_locations import locations
from parameters import easy, medium, hard, harder, hardcore, mania, text2diff, diff2text
from solver import ParamsLoader
from rom import RomPatcher, RomPatches

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Randomizer")
    parser.add_argument('--param', '-p', help="the input parameters", nargs='+',
                        default=None, dest='paramsFileName')

    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug',
                        action='store_true')
    parser.add_argument('--difficultyTarget', '-t',
                        help="the maximum difficulty target that the randomizer will use",
                        dest='difficultyTarget', nargs='?', default=None,
                        choices=['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania'])
    parser.add_argument('--seed', '-s', help="randomization seed to use", dest='seed',
                        nargs='?', default=0, type=int)
    parser.add_argument('--rom', '-r',
                        help="the vanilia ROM",
                        dest='rom', nargs='?', default=None)
    parser.add_argument('--output', '-o',
                        help="to choose the name of the generated json (for the webservice)",
                        dest='output', nargs='?', default=None)
    parser.add_argument('--preset', '-e',
                        help="the name of the preset (for the webservice)",
                        dest='preset', nargs='?', default=None)
    parser.add_argument('--patch', '-c',
                        help="optional patches to add",
                        dest='patches', nargs='?', default=[], action='append',
                        choices=['AimAnyButton.ips', 'itemsounds.ips', 'max_ammo_display.ips',
                                 'spinjumprestart.ips', 'supermetroid_msu1.ips'])
    parser.add_argument('--missileQty', '-m',
                        help="quantity of missiles",
                        dest='missileQty', nargs='?', default=3,
                        choices=[str(i) for i in range(1,10)])
    parser.add_argument('--superQty', '-q',
                        help="quantity of super missiles",
                        dest='superQty', nargs='?', default=3,
                        choices=[str(i) for i in range(1,10)])
    parser.add_argument('--powerBombQty', '-w',
                        help="quantity of power bombs",
                        dest='powerBombQty', nargs='?', default=1,
                        choices=[str(i) for i in range(1,10)])
    parser.add_argument('--minorQty', '-n',
                        help="quantity of minors",
                        dest='minorQty', nargs='?', default=100,
                        choices=[str(i) for i in range(1,101)])
    parser.add_argument('--energyQty', '-g',
                        help="quantity of ETanks/Reserve Tanks",
                        dest='energyQty', nargs='?', default='vanilla',
                        choices=['sparse', 'medium', 'vanilla'])
    parser.add_argument('--sampleSize', '-z',
                        help="Sample size to choose next item (lower is faster but less accurate)",
                        dest='sampleSize', nargs='?', default=100,
                        choices=[str(i) for i in range(1,101)])
    
    args = parser.parse_args()

    if args.paramsFileName is not None:
        ParamsLoader.factory(args.paramsFileName[0]).load()
        preset = os.path.splitext(os.path.basename(args.paramsFileName[0]))[0]

        if args.preset is not None:
            preset = args.preset
    else:
        preset = 'default'

    if args.seed == 0:
        seed = random.randint(0, 9999999)
    else:
        seed = args.seed

    print("SEED: " + str(seed))
        
    if args.difficultyTarget:
        difficultyTarget = text2diff[args.difficultyTarget]
    else:
        difficultyTarget = hard

    # same as solver
    threshold = difficultyTarget
    epsilon = 0.001
    if difficultyTarget <= easy:
        threshold = medium - epsilon
    elif difficultyTarget <= medium:
        threshold = hard - epsilon
    elif difficultyTarget <= hard:
        threshold = harder - epsilon
    elif difficultyTarget <= harder:
        threshold = hardcore - epsilon
    elif difficultyTarget <= hardcore:
        threshold = mania - epsilon
    difficultyTarget = threshold
        
    chooseItemWeights = { 'Random' : 1, 'MinProgression' : 0, 'MaxProgression' : 0 }
    chooseLocWeights = { 'Random' : 1, 'MinDiff' : 0, 'MaxDiff' : 0, 'SpreadProgression' : True }
    choose = { 'Items' : chooseItemWeights, 'Locations' : chooseLocWeights }
    restrictions = { 'Suits' : True, 'SpeedScrew' : True, 'MajorMinor' : True }
    seedCode = 'X'
    if restrictions['MajorMinor'] is False:
        seedCode = 'FX'
    fileName = 'Ouiche_Randomizer_' + seedCode + str(seed) + '_' + preset

    locationPool = locations

    RomPatches.ActivePatches = RomPatches.Total
    qty = {'missile': int(args.missileQty), 'super': int(args.superQty),
           'powerBomb': int(args.powerBombQty), 'energy': args.energyQty,
           'minors': int(args.minorQty)}
    randomizer = Randomizer(seed, difficultyTarget, locations, qty,
                            int(args.sampleSize), choose, restrictions)
    itemLocs = randomizer.generateItems()
    if itemLocs is None:
        print("Can't generate a randomized rom with the given parameters, try increasing the difficulty target.")
        sys.exit(-1)

    # transform itemLocs in our usual dict(location, item)
    locsItems = {}
    for itemLoc in itemLocs:
        locsItems[itemLoc["Location"]["Name"]] = itemLoc["Item"]["Type"]

    if args.debug is True:
        for loc in locsItems:
            print('{:>50}: {:>16} '.format(loc, locsItems[loc]))

    if args.rom is not None:
        # patch local rom
        romFileName = args.rom
        fileName += '.sfc'

        try:
            shutil.copyfile(romFileName, fileName)

            RomPatcher.writeItemsLocs(fileName, itemLocs)

            RomPatcher.applyIPSPatches(fileName, args.patches)

            RomPatcher.writeSeed(fileName, seed)

            RomPatcher.writeSpoiler(fileName, itemLocs)
        except Exception as e:
            print("Error patching {}. Is {} a valid ROM ? ({})".format(fileName, romFileName, e))
            sys.exit(-1)
    else:
        if args.output is not None:
            # web service
            data = {}

            data.update(RomPatcher.writeItemsLocs(None, itemLocs))
            data.update(RomPatcher.applyIPSPatches(None, args.patches))
            data.update(RomPatcher.writeSeed(None, seed))
            data.update(RomPatcher.writeSpoiler(None, itemLocs))

            fileName += '.sfc'
            data["fileName"] = fileName

            with open(args.output, 'w') as jsonFile:
                json.dump(data, jsonFile)
        else:
            # rom json
            fileName += '.json'
            with open(fileName, 'w') as jsonFile:
                json.dump(locsItems, jsonFile)

    print("Rom generated: {}".format(fileName))
