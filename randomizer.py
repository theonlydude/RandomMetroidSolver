#!/usr/bin/python

import argparse, random, os.path, json, sys, shutil

from itemrandomizerweb import Items
from itemrandomizerweb.Randomizer import Randomizer, RandoSettings
from itemrandomizerweb.AreaRandomizer import AreaRandomizer
from graph_locations import locations as graphLocations
from graph_access import vanillaTransitions, getDoorConnections
from parameters import Knows, easy, medium, hard, harder, hardcore, mania, text2diff, diff2text
from utils import PresetLoader
from rom import RomPatcher, RomPatches, FakeROM
import log

speeds = ['slowest', 'slow', 'medium', 'fast', 'fastest', 'basic']
energyQties = ['sparse', 'medium', 'vanilla' ]
progDiffs = ['easier', 'normal', 'harder']
morphPlacements = ['early', 'late', 'normal']

def dumpErrorMsg(outFileName, msg):
    if outFileName is None:
        return
    with open(outFileName, 'w') as jsonFile:
        json.dump({"errorMsg": msg}, jsonFile)

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
                        help="output directory for ROM and dot files",
                        dest='directory', nargs='?', default='.')
    parser.add_argument('--dot',
                        help="generate dot file with area graph",
                        action='store_true',dest='dot', default=False)
    parser.add_argument('--area',
                        help="area mode", action='store_true',
                        dest='area', default=False)
    parser.add_argument('--areaLayoutBase',
                        help="use simple layout patch for area mode", action='store_true',
                        dest='areaLayoutBase', default=False)
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug',
                        action='store_true')
    parser.add_argument('--maxDifficulty', '-t',
                        help="the maximum difficulty generated seed will be for given parameters",
                        dest='maxDifficulty', nargs='?', default=None,
                        choices=['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania', 'random'])
    parser.add_argument('--seed', '-s', help="randomization seed to use", dest='seed',
                        nargs='?', default=0, type=int)
    parser.add_argument('--rom', '-r',
                        help="the vanilla ROM",
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
                        choices=['itemsounds.ips',
                                 'spinjumprestart.ips', 'No_Music',
                                 'elevators_doors_speed.ips', 'skip_intro.ips', 'skip_ceres.ips'])
    parser.add_argument('--missileQty', '-m',
                        help="quantity of missiles",
                        dest='missileQty', nargs='?', default=3,
                        type=restricted_float)
    parser.add_argument('--superQty', '-q',
                        help="quantity of super missiles",
                        dest='superQty', nargs='?', default=2,
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
    parser.add_argument('--strictMinors',
                        help="minors quantities values will be strictly followed instead of being probabilities",
                        dest='strictMinors', nargs='?', const=True, default=False)
    parser.add_argument('--fullRandomization',
                        help="will place majors in all locations",
                        dest='fullRandomization', nargs='?', const=True, default=False)
    parser.add_argument('--suitsRestriction',
                        help="no suits in early game",
                        dest='suitsRestriction', nargs='?', const=True, default=False)
    parser.add_argument('--morphPlacement',
                        help="morph placement",
                        dest='morphPlacement', nargs='?', default='early',
                        choices=morphPlacements + ['random'])
    parser.add_argument('--hideItems', help="Like in dessy's rando hide half of the items",
                        dest="hideItems", nargs='?', const=True, default=False)
    parser.add_argument('--progressionSpeed', '-i',
                        help="",
                        dest='progressionSpeed', nargs='?', default='medium',
                        choices=speeds + ['random'])
    parser.add_argument('--progressionDifficulty',
                        help="",
                        dest='progressionDifficulty', nargs='?', default='normal',
                        choices=progDiffs + ['random'])
    parser.add_argument('--superFun',
                        help="randomly remove major items from the pool for maximum enjoyment",
                        dest='superFun', nargs='?', default=[], action='append',
                        choices=['Movement', 'Combat', 'Suits', 'MovementRandom', 'CombatRandom', 'SuitsRandom'])
    parser.add_argument('--animals',
                        help="randomly change the save the animals room",
                        dest='animals', action='store_true', default=False)
    parser.add_argument('--nolayout',
                        help="do not include total randomizer layout patches",
                        dest='noLayout', action='store_true', default=False)
    parser.add_argument('--nogravheat',
                        help="do not include total randomizer suits patches",
                        dest='noGravHeat', action='store_true', default=False)
    parser.add_argument('--novariatweaks',
                        help="do not include VARIA randomizer tweaks",
                        dest='noVariaTweaks', action='store_true', default=False)
    parser.add_argument('--controls',
                        help="specify controls, comma-separated, in that order: Shoot,Jump,Dash,ItemSelect,ItemCancel,AngleUp,AngleDown. Possible values: A,B,X,Y,L,R,Select,None",
                        dest='controls')
    parser.add_argument('--runtime', help="Maximum runtime limit in seconds. If 0 or negative, no runtime limit. Default is 30.", dest='runtimeLimit_s',
                        nargs='?', default=30, type=int)
    parser.add_argument('--race', help="Race mode magic number", dest='raceMagic',
                        type=int, choices=range(0, 0x10000))

    # parse args
    args = parser.parse_args()

    if args.output is None and args.rom is None:
        print "Need --output or --rom parameter"
        sys.exit(-1)
    elif args.output is not None and args.rom is not None:
        print "Can't have both --output and --rom parameters"
        sys.exit(-1)

    # if diff preset given, load it
    if args.paramsFileName is not None:
        PresetLoader.factory(args.paramsFileName[0]).load()
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
    seed4rand = seed
    if args.raceMagic is not None:
        seed4rand = seed ^ args.raceMagic
    random.seed(seed4rand)

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
    # if random progression difficulty, choose one
    progDiff = args.progressionDifficulty
    if progDiff == "random":
        progDiff = progDiffs[random.randint(0, len(progDiffs)-1)]

    print("SEED: " + str(seed))
#    print("progression speed: " + progSpeed)

    # if no max diff, set it very high
    if args.maxDifficulty:
        if args.maxDifficulty == 'random':
            diffs = ['hard', 'harder', 'very hard', 'hardcore', 'mania']
            maxDifficulty = text2diff[diffs[random.randint(0, len(diffs)-1)]]
        else:
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

    if args.fullRandomization == 'random':
        args.fullRandomization = bool(random.getrandbits(1))
    if args.suitsRestriction == 'random':
        args.suitsRestriction = bool(random.getrandbits(1))
    if args.hideItems == 'random':
        args.hideItems = bool(random.getrandbits(1))
    if args.morphPlacement == 'random':
        args.morphPlacement = morphPlacements[random.randint(0, len(morphPlacements)-1)]
    if args.strictMinors == 'random':
        args.strictMinors = bool(random.getrandbits(1))

    # fill restrictions dict
    restrictions = { 'Suits' : args.suitsRestriction, 'Morph' : args.morphPlacement }
    restrictions['MajorMinor'] = not args.fullRandomization
    seedCode = 'X'
    if restrictions['MajorMinor'] == False:
        seedCode = 'FX'
    if args.area == True:
        seedCode = 'A'+seedCode

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
        RomPatches.ActivePatches = RomPatches.TotalBase
    else:
        RomPatches.ActivePatches = RomPatches.Total
    if args.noGravHeat == True:
        RomPatches.ActivePatches.remove(RomPatches.NoGravityEnvProtection)
    if args.noVariaTweaks == False:
        RomPatches.ActivePatches += RomPatches.VariaTweaks
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
    qty = {'energy': energyQty,
           'minors': minorQty,
           'ammo': { 'Missile': missileQty,
                     'Super': superQty,
                     'PowerBomb': powerBombQty },
           'strictMinors' : args.strictMinors }

    if len(args.superFun) > 0:
        superFun = []
        for fun in args.superFun:
            if fun.find('Random') != -1:
                if bool(random.getrandbits(1)) == True:
                    superFun.append(fun[0:fun.find('Random')])
            else:
                superFun.append(fun)
        args.superFun = superFun
    ctrlDict = None
    if args.controls:
        ctrlList = args.controls.split(',')
        if len(ctrlList) != 7:
            raise ValueError("Invalid control list size")
        ctrlKeys = ["Shot", "Jump", "Dash", "ItemSelect", "ItemCancel", "AngleUp", "AngleDown"]
        ctrlDict = {}
        i = 0
        for k in ctrlKeys:
            b = ctrlList[i]
            if b in RomPatcher.buttons:
                ctrlDict[k] = b
                i += 1
            else:
                raise ValueError("Invalid button name : " + str(b))

    # print("qty = " + str(qty))
    # print("restrictions = " + str(restrictions))
    # print("superFun = " + str(args.superFun))
    log.init(args.debug)
    randoSettings = RandoSettings(maxDifficulty, progSpeed, progDiff, qty, restrictions, args.superFun, args.runtimeLimit_s)
    if args.area == True:
        if args.dot == True:
            dotDir = args.directory
        else:
            dotDir = None
        try:
            randomizer = AreaRandomizer(graphLocations, randoSettings, seedName, dotDir=dotDir)
        except RuntimeError:
            msg = "Cannot generate area layout. Retry, and change the super fun settings if the problem happens again."
            dumpErrorMsg(args.output, msg)
            print("DIAG: {}".format(msg))
            sys.exit(-1)
        RomPatches.ActivePatches += RomPatches.AreaSet
        if args.areaLayoutBase == True:
            RomPatches.ActivePatches.remove(RomPatches.AreaRandoGatesOther)
        doors = getDoorConnections(randomizer.areaGraph)
    else:
        try:
            randomizer = Randomizer(graphLocations, randoSettings, seedName, vanillaTransitions)
        except RuntimeError:
            msg = "Locations unreachable detected with preset/super fun/max diff. Retry, and change the Super Fun settings and or Maximum difficulty if the problem happens again."
            dumpErrorMsg(args.output, msg)
            print("DIAG: {}".format(msg))
            sys.exit(-1)
    itemLocs = randomizer.generateItems()
    if itemLocs is None:
        dumpErrorMsg(args.output, randomizer.errorMsg)
        print("Can't generate " + fileName + " with the given parameters: {}".format(randomizer.errorMsg))
        sys.exit(-1)

    # hide some items like in dessy's
    if args.hideItems == True:
        for itemLoc in itemLocs:
            if (itemLoc['Item']['Type'] not in ['Nothing', 'NoEnergy']
                and itemLoc['Location']['CanHidden'] == True
                and itemLoc['Location']['Visibility'] == 'Visible'):
                if bool(random.getrandbits(1)) == True:
                    itemLoc['Location']['Visibility'] = 'Hidden'

    # transform itemLocs in our usual dict(location, item)
    locsItems = {}
    for itemLoc in itemLocs:
        locsItems[itemLoc["Location"]["Name"]] = itemLoc["Item"]["Type"]
    if args.debug == True:
        for loc in locsItems:
            print('{:>50}: {:>16} '.format(loc, locsItems[loc]))

    try:
        # args.rom is not None: generate local rom named filename.sfc with args.rom as source
        # args.output is not None: generate local json named args.output
        if args.rom is not None:
            # patch local rom
            romFileName = args.rom
            outFileName = fileName + '.sfc'
            shutil.copyfile(romFileName, outFileName)
            romPatcher = RomPatcher(outFileName, magic=args.raceMagic)
        else:
            outFileName = args.output
            romPatcher = RomPatcher(magic=args.raceMagic)

        romPatcher.writeItemsLocs(itemLocs)
        romPatcher.applyIPSPatches(args.patches, args.noLayout, args.noGravHeat, args.area, args.areaLayoutBase, args.noVariaTweaks)
        romPatcher.writeSeed(seed) # lol if race mode
        romPatcher.writeSpoiler(itemLocs)
        romPatcher.writeRandoSettings(randoSettings)
        if args.area == True:
            romPatcher.writeDoorConnections(doors)
        romPatcher.writeTransitionsCredits(randomizer.areaGraph.getCreditsTransitions())
        if ctrlDict is not None:
            romPatcher.writeControls(ctrlDict)
        romPatcher.writeMagic()
        romPatcher.end()

        if args.rom is None:
            data = romPatcher.romFile.data
            fileName += '.sfc'
            data["fileName"] = fileName
            # error msg in json to be displayed by the web site
            data["errorMsg"] = randomizer.errorMsg
            with open(outFileName, 'w') as jsonFile:
                json.dump(data, jsonFile)
    except Exception as e:
        msg = "Error patching {}: ({}: {})".format(outFileName, type(e).__name__, e)
        dumpErrorMsg(args.output, msg)
        print(msg)
        sys.exit(-1)

    print("Rom generated: {}".format(fileName))
