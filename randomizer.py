#!/usr/bin/python

import argparse, random, os.path, json, sys, shutil

from itemrandomizerweb.stdlib import Random
from itemrandomizerweb import Items
from itemrandomizerweb.Randomizer import Randomizer, RandoSettings
from tournament_locations import locations
from parameters import easy, medium, hard, harder, hardcore, mania, text2diff, diff2text
from solver import ParamsLoader
from rom import RomPatcher, RomPatches

speeds = ['slowest', 'slow', 'medium', 'fast', 'fastest']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Randomizer")
    parser.add_argument('--param', '-p', help="the input parameters", nargs='+',
                        default=None, dest='paramsFileName')
    parser.add_argument('--dir',
                        help="output directory",
                        dest='directory', nargs='?', default='.')
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug',
                        action='store_true')
    parser.add_argument('--maxDifficulty', '-t',
                        help="the maximum difficulty generated seed will be for given parameters",
                        dest='maxDifficulty', nargs='?', default=None,
                        choices=['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania'])
    parser.add_argument('--seed', '-s', help="randomization seed to use", dest='seed',
                        nargs='?', default=0, type=int)
    parser.add_argument('--rom', '-r',
                        help="the vanilia ROM",
                        dest='rom', nargs='?', default=None)
    parser.add_argument('--output',
                        help="to choose the name of the generated json (for the webservice)",
                        dest='output', nargs='?', default=None)
    parser.add_argument('--preset',
                        help="the name of the preset (for the webservice)",
                        dest='preset', nargs='?', default=None)
    parser.add_argument('--patch', '-c',
                        help="optional patches to add",
                        dest='patches', nargs='?', default=[], action='append',
                        choices=['AimAnyButton.ips', 'itemsounds.ips', 'max_ammo_display.ips',
                                 'spinjumprestart.ips', 'supermetroid_msu1.ips',
                                 'elevators_doors_speed.ips', 'skip_intro.ips', 'skip_ceres.ips'])
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
    parser.add_argument('--spreadItems',
                        help="spread progression items", action='store_true',
                        dest='spreadItems', default=False)
    parser.add_argument('--fullRandomization',
                        help="will place majors in all locations", action='store_true',
                        dest='fullRandomization', default=False)
    parser.add_argument('--suitsRestriction',
                        help="no suits in early game", action='store_true',
                        dest='suitsRestriction', default=False)
    parser.add_argument('--speedScrewRestriction',
                        help="no speed or screw in the very first rooms", action='store_true',
                        dest='speedScrewRestriction', default=False)
    parser.add_argument('--progressionSpeed', '-i',
                        help="",
                        dest='progressionSpeed', nargs='?', default='medium',
                        choices=speeds + ['random'])
    parser.add_argument('--superFun', 
                        help="randomly remove major items from the pool for maximum enjoyment",
                        dest='superFun', nargs='?', default=[], action='append',
                        choices=['Movement', 'Combat', 'Suits'])

    # parse args
    args = parser.parse_args()

    # if diff preset given, load it
    if args.paramsFileName is not None:
        ParamsLoader.factory(args.paramsFileName[0]).load()
        preset = os.path.splitext(os.path.basename(args.paramsFileName[0]))[0]

        if args.preset is not None:
            preset = args.preset
    else:
        preset = 'default'

    # if no seed given, choose one
    if args.seed == 0:
        seed = random.randint(0, 9999999)
    else:
        seed = args.seed
    random.seed(seed)

    # if random progression speed, choose one
    progSpeed = args.progressionSpeed
    if progSpeed == "random":
        progSpeed = speeds[random.randint(0, len(speeds)-1)]

    print("SEED: " + str(seed))
#    print("progression speed: " + progSpeed)

    # if no max diff, set it very high
    if args.maxDifficulty:
        maxDifficulty = text2diff[args.maxDifficulty]
    else:
        maxDifficulty = 100000

    # same as solver, increase max difficulty 
    threshold = maxDifficulty
    epsilon = 0.001
    if maxDifficulty <= easy:
        threshold = medium - epsilon
    elif maxDifficulty <= medium:
        threshold = hard - epsilon
    elif maxDifficulty <= hard:
        threshold = harder - epsilon
    elif maxDifficulty <= harder:
        threshold = hardcore - epsilon
    elif maxDifficulty <= hardcore:
        threshold = mania - epsilon
    maxDifficulty = threshold

    # fill restrictions dict
    restrictions = { 'Suits' : args.suitsRestriction, 'SpeedScrew' : args.speedScrewRestriction, 'MajorMinor' : not args.fullRandomization }
    seedCode = 'X'
    if restrictions['MajorMinor'] is False:
        seedCode = 'FX'

    # output ROM name
    fileName = 'VARIA_Randomizer_' + seedCode + str(seed) + '_' + preset
    if args.directory != '.':
        fileName = args.directory + '/' + fileName
    if args.progressionSpeed != "random":
        fileName += "_" + args.progressionSpeed
    # check that one skip patch is set
    if 'skip_intro.ips' not in args.patches and 'skip_ceres.ips' not in args.patches:
        args.patches.append('skip_ceres.ips')

    locationPool = locations

    RomPatches.ActivePatches = RomPatches.Total
    qty = {'missile': int(args.missileQty), 'super': int(args.superQty),
           'powerBomb': int(args.powerBombQty), 'energy': args.energyQty,
           'minors': int(args.minorQty)}
    sampleSize = 100
    randoSettings = RandoSettings(maxDifficulty, progSpeed, qty, restrictions, args.spreadItems, sampleSize, args.superFun)
    randomizer = Randomizer(locations, randoSettings)
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
