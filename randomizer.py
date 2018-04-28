#!/usr/bin/python

import argparse, random, os.path, json, sys, shutil

from itemrandomizerweb import Items
from itemrandomizerweb.Randomizer import Randomizer, RandoSettings
from itemrandomizerweb.AreaRandomizer import AreaRandomizer
from tournament_locations import locations as defaultLocations
from graph_locations import locations as graphLocations
from graph import vanillaTransitions
from parameters import Knows, easy, medium, hard, harder, hardcore, mania, text2diff, diff2text
from solver import ParamsLoader
from rom import RomPatcher, RomPatches

speeds = ['slowest', 'slow', 'medium', 'fast', 'fastest']
energyQties = ['sparse', 'medium', 'vanilla' ]
progDiffs = ['easier', 'random', 'harder']

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 9.0:
        raise argparse.ArgumentTypeError("%r not in range [1.0, 9.0]"%(x,))
    return x

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Randomizer")
    parser.add_argument('--param', '-p', help="the input parameters", nargs='+',
                        default=None, dest='paramsFileName')
    parser.add_argument('--dir',
                        help="output directory",
                        dest='directory', nargs='?', default='.')
    parser.add_argument('--graph',
                        help="experimental graph mode", action='store_true',
                        dest='graph', default=False)
    parser.add_argument('--area',
                        help="experimental area mode", action='store_true',
                        dest='area', default=False)
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
                        type=restricted_float)
    parser.add_argument('--superQty', '-q',
                        help="quantity of super missiles",
                        dest='superQty', nargs='?', default=3,
                        type=restricted_float)
    parser.add_argument('--powerBombQty', '-w',
                        help="quantity of power bombs",
                        dest='powerBombQty', nargs='?', default=1,
                        type=restricted_float)
    parser.add_argument('--minorQty', '-n',
                        help="quantity of minors",
                        dest='minorQty', nargs='?', default=100,
                        choices=[str(i) for i in range(0,101)])
    parser.add_argument('--energyQty', '-g',
                        help="quantity of ETanks/Reserve Tanks",
                        dest='energyQty', nargs='?', default='vanilla',
                        choices=energyQties + ['random'])
    parser.add_argument('--randomRestrictions',
                        help="Randomizes (and overrides) spreadItems, suitsRestriction and speedScrewRestriction", action='store_true',
                        dest='randomRestrictions', default=False)
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
    parser.add_argument('--progressionDifficulty',
                        help="",
                        dest='progressionDifficulty', nargs='?', default='random',
                        choices=progDiffs + ['random'])
    parser.add_argument('--superFun',
                        help="randomly remove major items from the pool for maximum enjoyment",
                        dest='superFun', nargs='?', default=[], action='append',
                        choices=['Movement', 'Combat', 'Suits', 'random'])
    parser.add_argument('--animals',
                        help="randomly change the save the animals room",
                        dest='animals', action='store_true', default=False)
    parser.add_argument('--nolayout',
                        help="do not include total randomizer layout patches",
                        dest='noLayout', action='store_true', default=False)
    parser.add_argument('--nogravheat',
                        help="do not include total randomizer suits patches",
                        dest='noGravHeat', action='store_true', default=False)

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

    # choose on animal patch
    if args.animals == True:
        animalsPatches = ['animal_enemies.ips', 'animals.ips', 'draygonimals.ips', 'escapimals.ips',
                          'gameend.ips', 'grey_door_animals.ips', 'low_timer.ips', 'metalimals.ips',
                          'phantoonimals.ips', 'ridleyimals.ips']
        args.patches.append(animalsPatches[random.randint(0, len(animalsPatches)-1)])

    # if random progression speed, choose one
    progSpeed = args.progressionSpeed
    if progSpeed == "random":
        progSpeed = speeds[random.randint(0, len(speeds)-1)]
    progDiff = args.progressionDifficulty

    print("SEED: " + str(seed))
#    print("progression speed: " + progSpeed)

    # if no max diff, set it very high
    if args.maxDifficulty:
        maxDifficulty = text2diff[args.maxDifficulty]
    else:
        maxDifficulty = float('inf')

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
    if not args.randomRestrictions:
        restrictions = { 'Suits' : args.suitsRestriction, 'SpeedScrew' : args.speedScrewRestriction, 'SpreadItems' : args.spreadItems }
    else:
        restrictions = { 'Suits' : bool(random.getrandbits(1)), 'SpeedScrew' : bool(random.getrandbits(1)), 'SpreadItems' : bool(random.getrandbits(1))}
    restrictions['MajorMinor'] = not args.fullRandomization
    seedCode = 'X'
    if restrictions['MajorMinor'] == False:
        seedCode = 'FX'

    # output ROM name
    fileName = 'VARIA_Randomizer_' + seedCode + str(seed) + '_' + preset
    if args.progressionSpeed != "random":
        fileName += "_" + args.progressionSpeed
    seedName = fileName
    if args.directory != '.':
        fileName = args.directory + '/' + fileName
    # check that one skip patch is set
    if 'skip_intro.ips' not in args.patches and 'skip_ceres.ips' not in args.patches:
        args.patches.append('skip_ceres.ips')

    if args.noLayout == True:
        RomPatches.ActivePatches = RomPatches.Total_Base
    else:
        RomPatches.ActivePatches = RomPatches.Total
    if args.noGravHeat == True:
        RomPatches.ActivePatches.remove(RomPatches.NoGravityEnvProtection)
    missileQty = float(args.missileQty)
    superQty = float(args.superQty)
    powerBombQty = float(args.powerBombQty)
    minorQty = int(args.minorQty)
    energyQty = args.energyQty
    if missileQty < 1:
        missileQty = random.randint(1, 9)
    if superQty < 1:
        superQty = random.randint(1, 9)
    if powerBombQty < 1:
        powerBombQty = random.randint(1, 9)
    if minorQty < 1:
        minorQty = random.randint(25, 100)
    if energyQty == 'random':
        energyQty = energyQties[random.randint(0, len(energyQties)-1)]
    qty = {'missile': missileQty, 'super': superQty,
           'powerBomb': powerBombQty, 'energy': energyQty,
           'minors': minorQty}
    if 'random' in args.superFun:
        args.superFun = []
        def addFun(fun):
            if bool(random.getrandbits(1)) == True:
                args.superFun.append(fun)
        addFun('Suits')
        addFun('Combat')
        addFun('Movement')
    # print("qty = " + str(qty))
    # print("restrictions = " + str(restrictions))
    # print("superFun = " + str(args.superFun))
    randoSettings = RandoSettings(maxDifficulty, progSpeed, progDiff, qty, restrictions, args.superFun)
    if args.area == True:
        randomizer = AreaRandomizer(graphLocations, randoSettings, seedName, dotDir=args.directory)
    elif args.graph == True:
        randomizer = Randomizer(graphLocations, randoSettings, seedName, vanillaTransitions)
    else:
        randomizer = Randomizer(defaultLocations, randoSettings, seedName)
    itemLocs = randomizer.generateItems()
    if itemLocs is None:
        print("Can't generate " + fileName + " with the given parameters, try increasing the difficulty target.")
        sys.exit(-1)

    # transform itemLocs in our usual dict(location, item)
    locsItems = {}
    for itemLoc in itemLocs:
        locsItems[itemLoc["Location"]["Name"]] = itemLoc["Item"]["Type"]

    if args.debug == True:
        for loc in locsItems:
            print('{:>50}: {:>16} '.format(loc, locsItems[loc]))

    if args.rom is not None:
        # patch local rom
        romFileName = args.rom
        fileName += '.sfc'

        try:
            shutil.copyfile(romFileName, fileName)

            RomPatcher.writeItemsLocs(fileName, itemLocs)
            RomPatcher.applyIPSPatches(fileName, args.patches, args.noLayout, args.noGravHeat)
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
            data.update(RomPatcher.applyIPSPatches(None, args.patches, args.noLayout, args.noGravHeat))
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
