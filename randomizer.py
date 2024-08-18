#!/usr/bin/python3

import argparse, os.path, json, sys, shutil, random

from rando.RandoSettings import RandoSettings, GraphSettings
from rando.RandoExec import RandoExec
from graph.graph_utils import GraphUtils, getAccessPoint
from utils.parameters import easy, medium, hard, harder, hardcore, mania, infinity, text2diff, appDir
from rom.rom_patches import RomPatches, getPatchSet, getPatchSetsFromPatcherSettings, getPatchDescriptions
from rom.rompatcher import RomPatcher
from rom.flavor import RomFlavor
from utils.utils import PresetLoader, loadRandoPreset, getDefaultMultiValues, getPresetDir
from utils.version import displayedVersion
from utils.doorsmanager import DoorsManager
from logic.logic import Logic
from utils.objectives import Objectives
from utils.utils import dumpErrorMsg

import utils.log
import utils.db as db

# use vanilla logic to get default start locations
Logic.factory('vanilla')
defaultMultiValues = getDefaultMultiValues()
speeds = defaultMultiValues['progressionSpeed']
energyQties = defaultMultiValues['energyQty']
progDiffs = defaultMultiValues['progressionDifficulty']
morphPlacements = defaultMultiValues['morphPlacement']
majorsSplits = defaultMultiValues['majorsSplit']
gravityBehaviours = defaultMultiValues['gravityBehaviour']
objectives = defaultMultiValues['objective']
tourians = defaultMultiValues['tourian']
areaRandomizations = defaultMultiValues['areaRandomization']
startLocations = defaultMultiValues['startLocation']
logics = defaultMultiValues['logic']

def randomMulti(args, param, defaultMultiValues):
    value = args[param]

    isRandom = False
    if value == "random":
        isRandom = True
        choices = defaultMultiValues
        if args[param+"List"] is not None:
            # use provided list
            choices = [choice for choice in args[param+"List"].split(',') if choice in defaultMultiValues]
        value = random.choice(choices)

    return (isRandom, value)

def dumpErrorMsgs(outFileName, msgs):
    dumpErrorMsg(outFileName, joinErrorMsgs(msgs))

def joinErrorMsgs(msgs):
    return '\n'.join(msgs)

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 9.0:
        raise argparse.ArgumentTypeError("%r not in range [1.0, 9.0]"%(x,))
    return x

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VARIA Randomizer")
    parser.add_argument('--param', '-p', help="the input parameters",
                        default=None, dest='paramsFileName')
    parser.add_argument('--dir',
                        help="output directory for ROM and dot files",
                        dest='directory', nargs='?', default='.')
    parser.add_argument('--dot',
                        help="generate dot file with area graph",
                        action='store_true',dest='dot', default=False)
    parser.add_argument('--areaRandomization', help="area mode",
                        dest='areaRandomization', nargs='?', const=True, choices=["random"]+areaRandomizations, default='off')
    parser.add_argument('--areaRandomizationList', help="list to choose from when random",
                        dest='areaRandomizationList', nargs='?', default=None)
    parser.add_argument('--areaLayoutBase',
                        help="use simple layout patch for area mode", action='store_true',
                        dest='areaLayoutBase', default=False)
    parser.add_argument('--areaLayoutCustom',
                        help="Customize area layout patches. Comma-separated values of patch IDs",
                        nargs='?', dest='areaLayoutCustom', default=None)
    parser.add_argument('--escapeRando',
                        help="Randomize the escape sequence",
                        dest='escapeRando', nargs='?', const=True, default=False)
    parser.add_argument('--noRemoveEscapeEnemies',
                        help="Do not remove enemies during escape sequence", action='store_true',
                        dest='noRemoveEscapeEnemies', default=False)
    parser.add_argument('--bosses', help="randomize bosses",
                        dest='bosses', nargs='?', const=True, default=False)
    parser.add_argument('--minimizer', help="minimizer mode: area and boss mixed together. arg is number of non boss locations",
                        dest='minimizerN', nargs='?', const=35, default=None,
                        choices=[str(i) for i in range(30,101)]+["random"])
    parser.add_argument('--startLocation', help="Name of the Access Point to start from",
                        dest='startLocation', nargs='?', default="Landing Site",
                        choices=['random'] + startLocations)
    parser.add_argument('--startLocationList', help="list to choose from when random",
                        dest='startLocationList', nargs='?', default=None)
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug',
                        action='store_true')
    parser.add_argument('--maxDifficulty', '-t',
                        help="the maximum difficulty generated seed will be for given parameters",
                        dest='maxDifficulty', nargs='?', default='infinity',
                        choices=['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania', 'infinity', 'random'])
    parser.add_argument('--minDifficulty',
                        help="the minimum difficulty generated seed will be for given parameters (speedrun prog speed required)",
                        dest='minDifficulty', nargs='?', default=None,
                        choices=['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania'])
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
                        choices=['itemsounds.ips', 'random_music.ips',
                                 'fast_doors.ips', 'elevators_speed.ips',
                                 'spinjumprestart.ips', 'rando_speed.ips', 'No_Music', 'AimAnyButton.ips',
                                 'max_ammo_display.ips', 'supermetroid_msu1.ips', 'Infinite_Space_Jump',
                                 'refill_before_save.ips', 'relaxed_round_robin_cf.ips', 'better_reserves.ips'])
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
    parser.add_argument('--energyQtyList', help="list to choose from when random",
                        dest='energyQtyList', nargs='?', default=None)
    parser.add_argument('--strictMinors',
                        help="minors quantities values will be strictly followed instead of being probabilities",
                        dest='strictMinors', nargs='?', const=True, default=False)
    parser.add_argument('--majorsSplit',
                        help="how to split majors/minors: Full, FullWithHUD, Major, Chozo, Scavenger",
                        dest='majorsSplit', nargs='?', choices=majorsSplits + ['random'], default='Full')
    parser.add_argument('--majorsSplitList', help="list to choose from when random",
                        dest='majorsSplitList', nargs='?', default=None)
    parser.add_argument('--scavNumLocs',
                        help="For Scavenger split, number of major locations in the mandatory route",
                        dest='scavNumLocs', nargs='?', default=10,
                        choices=["0"]+[str(i) for i in range(4,18)])
    parser.add_argument('--scavRandomized',
                        help="For Scavenger split, decide whether mandatory major locs will have non-vanilla items",
                        dest='scavRandomized', nargs='?', const=True, default=False)
    parser.add_argument('--suitsRestriction',
                        help="no suits in early game",
                        dest='suitsRestriction', nargs='?', const=True, default=False)
    parser.add_argument('--morphPlacement',
                        help="morph placement",
                        dest='morphPlacement', nargs='?', default='early',
                        choices=morphPlacements + ['random'])
    parser.add_argument('--morphPlacementList', help="list to choose from when random",
                        dest='morphPlacementList', nargs='?', default=None)
    parser.add_argument('--hideItems', help="Like in dessy's rando hide half of the items",
                        dest="hideItems", nargs='?', const=True, default=False)
    parser.add_argument('--progressionSpeed', '-i',
                        help="progression speed, from " + str(speeds) + ". 'random' picks a random speed from these. Pick a random speed from a subset using comma-separated values, like 'slow,medium,fast'.",
                        dest='progressionSpeed', nargs='?', default='medium', choices=speeds+['random'])
    parser.add_argument('--progressionSpeedList', help="list to choose from when random",
                        dest='progressionSpeedList', nargs='?', default=None)
    parser.add_argument('--progressionDifficulty',
                        help="",
                        dest='progressionDifficulty', nargs='?', default='normal',
                        choices=progDiffs + ['random'])
    parser.add_argument('--progressionDifficultyList', help="list to choose from when random",
                        dest='progressionDifficultyList', nargs='?', default=None)
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
    parser.add_argument('--layoutCustom',
                        help="Customize anti-softlock layout patches. Comma-separated values of patch IDs",
                        nargs='?', dest='layoutCustom', default=None)
    parser.add_argument('--gravityBehaviour',
                        help="varia/gravity suits behaviour",
                        dest='gravityBehaviour', nargs='?', default='Balanced', choices=gravityBehaviours+['random'])
    parser.add_argument('--gravityBehaviourList', help="list to choose from when random",
                        dest='gravityBehaviourList', nargs='?', default=None)
    parser.add_argument('--revealMap',
                        help="reveal all map at game start",
                        dest='revealMap', action='store_true', default=False)
    parser.add_argument('--nerfedCharge',
                        help="apply nerfed charge patch",
                        dest='nerfedCharge', action='store_true', default=False)
    parser.add_argument('--novariatweaks',
                        help="do not include VARIA randomizer tweaks",
                        dest='noVariaTweaks', action='store_true', default=False)
    parser.add_argument('--variaTweaksCustom',
                        help="Customize VARIA tweaks patches. Comma-separated values of patch IDs",
                        nargs='?', dest='variaTweaksCustom', default=None)
    parser.add_argument('--controls',
                        help="specify controls, comma-separated, in that order: Shoot,Jump,Dash,ItemSelect,ItemCancel,AngleUp,AngleDown. Possible values: A,B,X,Y,L,R,Select,None",
                        dest='controls')
    parser.add_argument('--moonwalk',
                        help="Enables moonwalk by default",
                        dest='moonWalk', action='store_true', default=False)
    parser.add_argument('--runtime',
                        help="Maximum runtime limit in seconds. If 0 or negative, no runtime limit. Default is 30.",
                        dest='runtimeLimit_s', nargs='?', default=30, type=int)
    parser.add_argument('--race', help="Race mode magic number", dest='raceMagic',
                        type=int)
    parser.add_argument('--vcr', help="Generate VCR output file", dest='vcr', action='store_true')
    parser.add_argument('--ext_stats', help="dump extended stats SQL", nargs='?', default=None, dest='extStatsFilename')
    parser.add_argument('--randoPreset', help="rando preset file", dest="randoPreset", nargs='?', default=None)
    parser.add_argument('--fakeRandoPreset', help="for prog speed stats", dest="fakeRandoPreset", nargs='?', default=None)
    parser.add_argument('--plandoRando', help="json string with already placed items/locs", dest="plandoRando",
                        nargs='?', default=None)
    parser.add_argument('--jm,', help="display data used by jm for its stats", dest='jm', action='store_true', default=False)
    parser.add_argument('--doorsColorsRando', help='randomize color of colored doors', dest='doorsColorsRando',
                        nargs='?', const=True, default=False)
    parser.add_argument('--allowGreyDoors', help='add grey color in doors colors pool', dest='allowGreyDoors',
                        nargs='?', const=True, default=False)
    parser.add_argument('--logic', help='logic to use', dest='logic', nargs='?', const=True, default="vanilla", choices=logics+['random'])
    parser.add_argument('--logicList', help="list to choose from when randomizing logic",
                        dest='logicList', nargs='?', default=None)
    parser.add_argument('--hud', help='Enable VARIA hud', dest='hud',
                        nargs='?', const=True, default=False)
    parser.add_argument('--music',
                        help="JSON file for music replacement mapping",
                        dest='music', nargs='?', default=None)
    parser.add_argument('--objective',
                        help="objectives to open G4",
                        dest='objective', nargs='?', default=[], action='append',
                        choices=Objectives.getAllGoals()+["random"]+[str(i) for i in range(Objectives.maxActiveGoals+1)])
    parser.add_argument('--nbObjectivesRequired',
                        help="Maximum required objectives. Set to 0 for random between 1 and total number of objectives.",
                        dest='nbObjectivesRequired', nargs='?', default=None, type=int)
    parser.add_argument('--hiddenObjectives', help="don't reveal objectives until reaching a particular room depending on tourian setting", dest='hiddenObjectives',
                        nargs='?', const=True, default=False)
    parser.add_argument('--distributeObjectives', help="Distribute random objectives evenly across categories", dest='distributeObjectives',
                        nargs='?', const=True, default=False)
    parser.add_argument('--objectiveList', help="list to choose from when random",
                        dest='objectiveList', nargs='?', default=None)
    parser.add_argument('--tourian', help="Tourian mode",
                        dest='tourian', nargs='?', default='Vanilla',
                        choices=tourians+['random'])
    parser.add_argument('--tourianList', help="list to choose from when random",
                        dest='tourianList', nargs='?', default=None)
    # parse args
    args = parser.parse_args()

    if args.output is None and args.rom is None:
        print("Need --output or --rom parameter")
        sys.exit(-1)
    elif args.output is not None and args.rom is not None:
        print("Can't have both --output and --rom parameters")
        sys.exit(-1)

    if args.plandoRando is not None and args.output is None:
        print("plandoRando param requires output param")
        sys.exit(-1)

    utils.log.init(args.debug)
    logger = utils.log.get('Rando')

    # service to force an argument value and notify it
    argDict = vars(args)
    forcedArgs = {}
    optErrMsgs = [ ]
    def forceArg(arg, value, msg, altValue=None, webArg=None, webValue=None):
        okValues = [value]
        if altValue is not None:
            okValues.append(altValue)

        if argDict[arg] not in okValues:
            argDict[arg] = value
            forcedArgs[webArg if webArg is not None else arg] = webValue if webValue is not None else value
            optErrMsgs.append(msg)

    def forceLayoutArgs(forcedLayout):
        def mergeCustomLayout(arg, forced):
            if arg is None:
                return forced, forced
            p = arg.split(',')
            return sorted(list(set(p + forced))), sorted(list(set(forced) - set(p)))
        def getForcedText(forced):
            return ', '.join(getPatchDescriptions(forced, RomFlavor.flavor))
        if forcedLayout['layout'] and (args.noLayout or args.layoutCustom is not None):
            forceArg('noLayout', False, "'Anti-softlock layout patches' forced to on", webValue='on')
            forced = forcedLayout['layout']
            custom, actuallyForced = mergeCustomLayout(args.layoutCustom, forced)
            if len(actuallyForced) > 0:
                forceArg("layoutCustom", ','.join(custom), f"Forced layout patches: {getForcedText(actuallyForced)}", webValue=custom)
        if args.areaRandomization != 'off' and forcedLayout['areaLayout'] and (args.areaLayoutBase or args.areaLayoutCustom is not None):
            forceArg('areaLayoutBase', False, "'Additional layout patches for easier navigation' forced to on", webValue='on')
            forced = forcedLayout['areaLayout']
            custom, actuallyForced = mergeCustomLayout(args.areaLayoutCustom, forced)
            if len(actuallyForced) > 0:
                forceArg("areaLayoutCustom", ','.join(custom), f"Forced area layout patches: {getForcedText(actuallyForced)}", webValue=custom)
        if forcedLayout['variaTweaks'] and (args.noVariaTweaks or args.variaTweaksCustom is not None):
            forceArg('noVariaTweaks', False, "'VARIA tweaks' forced to on", webValue='on')
            forced = forcedLayout['variaTweaks']
            custom, actuallyForced = mergeCustomLayout(args.variaTweaksCustom, forced)
            if len(actuallyForced) > 0:
                forceArg('variaTweaksCustom', ','.join(custom), f"Forced VARIA tweaks: {getForcedText(actuallyForced)}", webValue=custom)

    # if rando preset given, load it first
    if args.randoPreset is not None:
        preset = loadRandoPreset(args.randoPreset, args)
        # use the skill preset from the rando preset
        if preset is not None and args.paramsFileName is None:
            args.paramsFileName = '{}/{}/{}.json'.format(appDir, getPresetDir(preset), preset)

    # if diff preset given, load it
    if args.paramsFileName is not None:
        PresetLoader.factory(args.paramsFileName).load()
        preset = os.path.splitext(os.path.basename(args.paramsFileName))[0]

        if args.preset is not None:
            preset = args.preset
    else:
        preset = 'default'

    logger.debug("skill preset: {}".format(preset))

    # initialize random seed
    if args.seed == 0:
        # if no seed given, choose one
        seed = random.randrange(sys.maxsize)
    else:
        seed = args.seed
    logger.debug("seed: {}".format(seed))

    seed4rand = seed
    if args.raceMagic is not None:
        seed4rand = seed ^ args.raceMagic
    random.seed(seed4rand)

    # handle random parameters with dynamic pool of values
    (_, progSpeed) = randomMulti(args.__dict__, "progressionSpeed", speeds)
    (_, progDiff) = randomMulti(args.__dict__, "progressionDifficulty", progDiffs)
    (majorsSplitRandom, args.majorsSplit) = randomMulti(args.__dict__, "majorsSplit", majorsSplits)
    (_, gravityBehaviour) = randomMulti(args.__dict__, "gravityBehaviour", gravityBehaviours)
    (_, args.tourian) = randomMulti(args.__dict__, "tourian", tourians)
    (areaRandom, args.areaRandomization) = randomMulti(args.__dict__, "areaRandomization", areaRandomizations)
    (logicRandom, args.logic) = randomMulti(args.__dict__, "logic", logics)
    areaRandomization = args.areaRandomization in ['light', 'full']
    lightArea = args.areaRandomization == 'light'

    # logic can be set in rando preset
    Logic.factory(args.logic)
    RomFlavor.factory()

    # if no max diff, set it very high
    if args.maxDifficulty == 'random':
        diffs = ['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania']
        maxDifficulty = text2diff[random.choice(diffs)]
    else:
        maxDifficulty = text2diff[args.maxDifficulty]
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
    logger.debug("maxDifficulty: {}".format(maxDifficulty))

    if args.minDifficulty:
        minDifficulty = text2diff[args.minDifficulty]
        if progSpeed != "speedrun":
            optErrMsgs.append("Minimum difficulty setting ignored, as prog speed is not speedrun")
    else:
        minDifficulty = 0

    # minimizer
    if areaRandomization == True and args.bosses == True and args.minimizerN is not None:
        if args.minimizerN == "random":
            minimizerN = random.randint(30, 60)
            logger.debug("minimizerN: {}".format(minimizerN))
        else:
            minimizerN = int(args.minimizerN)
        if minimizerN < 100:
            forceArg('majorsSplit', 'Full', "'Majors Split' forced to Full. Use 100 locations on your minimizer to use a non-Full split.", altValue='FullWithHUD')
    else:
        minimizerN = None
    logger.debug(f"majorsSplit: {args.majorsSplit}")

    # door color rando
    doorsColorsRandom = False
    if args.doorsColorsRando == 'random':
        doorsColorsRandom = True
        args.doorsColorsRando = bool(random.getrandbits(1))
    logger.debug("doorsColorsRando: {}".format(args.doorsColorsRando))

    # boss rando
    bossesRandom = False
    if args.bosses == 'random':
        bossesRandom = True
        args.bosses = bool(random.getrandbits(1))
    logger.debug("bosses: {}".format(args.bosses))

    # escape rando
    if args.escapeRando == 'random':
        args.escapeRando = bool(random.getrandbits(1))
    logger.debug("escapeRando: {}".format(args.escapeRando))

    # settings constraints
    if args.suitsRestriction != False and minimizerN is not None:
        forceArg('suitsRestriction', False, "'Suits restriction' forced to off", webValue='off')

    if args.suitsRestriction == 'random':
        if args.morphPlacement == 'late' and areaRandomization == True:
            forceArg('suitsRestriction', False, "'Suits restriction' forced to off", webValue='off')
        else:
            args.suitsRestriction = bool(random.getrandbits(1))
    logger.debug("suitsRestriction: {}".format(args.suitsRestriction))

    if args.hideItems == 'random':
        args.hideItems = bool(random.getrandbits(1))

    if args.morphPlacement == 'random':
        if args.morphPlacementList is not None:
            morphPlacements = args.morphPlacementList.split(',')
        args.morphPlacement = random.choice(morphPlacements)
    # Scavenger Hunt constraints
    if args.majorsSplit == 'Scavenger':
        forceArg('progressionSpeed', 'speedrun', "'Progression speed' forced to speedrun")
        progSpeed = "speedrun"
        forceArg('hud', True, "'VARIA HUD' forced to on", webValue='on')
        if not GraphUtils.isStandardStart(args.startLocation):
            forceArg('startLocation', "Landing Site", "Start Location forced to Landing Site because of Scavenger mode")
        if args.morphPlacement == 'late':
            forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal instead of late")
    # use escape rando for auto escape trigger
    if args.tourian == 'Disabled':
        forceArg('escapeRando', True, "'Escape randomization' forced to on", webValue='on')
        forceArg('noRemoveEscapeEnemies', True, "Enemies enabled during escape sequence", webArg='removeEscapeEnemies', webValue='off')
    # random fill makes certain options unavailable
    if (progSpeed == 'speedrun' or progSpeed == 'basic') and args.majorsSplit != 'Scavenger':
        forceArg('progressionDifficulty', 'normal', "'Progression difficulty' forced to normal")
        progDiff = args.progressionDifficulty
    logger.debug("progressionDifficulty: {}".format(progDiff))

    if args.strictMinors == 'random':
        args.strictMinors = bool(random.getrandbits(1))

    # in plando rando we know that the start ap is ok
    if not GraphUtils.isStandardStart(args.startLocation) and args.plandoRando is None:
        if args.majorsSplit in ['Major', "Chozo"]:
            forceArg('hud', True, "'VARIA HUD' forced to on", webValue='on')
        forceArg('suitsRestriction', False, "'Suits restriction' forced to off", webValue='off')
        possibleStartAPs, reasons = GraphUtils.getPossibleStartAPs(areaRandomization, maxDifficulty, args.morphPlacement)
        if args.startLocation == 'random':
            if args.startLocationList is not None:
                startLocationList = args.startLocationList.split(',')
                # intersection between user whishes and reality
                possibleStartAPs = sorted(list(set(possibleStartAPs).intersection(set(startLocationList))))
                if len(possibleStartAPs) == 0:
                    optErrMsgs += ["%s : %s" % (apName, cause) for apName, cause in reasons.items() if apName in startLocationList]
                    optErrMsgs.append('Invalid start locations list with your settings.')
                    dumpErrorMsgs(args.output, optErrMsgs)
                    sys.exit(-1)
            args.startLocation = random.choice(possibleStartAPs)
        elif args.startLocation not in possibleStartAPs:
            optErrMsgs.append('Invalid start location: {}.  {}'.format(args.startLocation, reasons[args.startLocation]))
            optErrMsgs.append('Possible start locations with these settings: {}'.format(possibleStartAPs))
            dumpErrorMsgs(args.output, optErrMsgs)
            sys.exit(-1)
        forcedLayout = GraphUtils.getForcedLayoutPatches(args.startLocation)
        forceLayoutArgs(forcedLayout)

    ap = getAccessPoint(args.startLocation)
    if 'forcedEarlyMorph' in ap.Start and ap.Start['forcedEarlyMorph'] == True:
        forceArg('morphPlacement', 'early', "'Morph Placement' forced to early for custom start location")
    else:
        if progSpeed == 'speedrun':
            if args.morphPlacement == 'late':
                forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal instead of late")
            elif (not GraphUtils.isStandardStart(args.startLocation)) and args.morphPlacement != 'normal':
                forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal for custom start location")
        if args.majorsSplit == 'Chozo' and args.morphPlacement == "late":
            forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal for Chozo")

    print("SEED: " + str(seed))

    # fill restrictions dict
    restrictions = { 'Suits' : args.suitsRestriction, 'Morph' : args.morphPlacement, "doors": "normal" if not args.doorsColorsRando else "late" }
    restrictions['MajorMinor'] = 'Full' if args.majorsSplit == 'FullWithHUD' else args.majorsSplit
    if restrictions["MajorMinor"] == "Scavenger":
        scavNumLocs = int(args.scavNumLocs)
        if scavNumLocs == 0:
            scavNumLocs = random.randint(4,16)
        restrictions["ScavengerParams"] = {'numLocs':scavNumLocs, 'vanillaItems':not args.scavRandomized}
    restrictions["EscapeTrigger"] = args.tourian == 'Disabled'

    # determine output file name
    seedCode = 'X'
    if majorsSplitRandom == False:
        if restrictions['MajorMinor'] == 'Full':
            seedCode = 'FX'
        elif restrictions['MajorMinor'] == 'Chozo':
            seedCode = 'ZX'
        elif restrictions['MajorMinor'] == 'Major':
            seedCode = 'MX'
        elif restrictions['MajorMinor'] == 'Scavenger':
            seedCode = 'SX'
    if args.bosses == True and bossesRandom == False:
        seedCode = 'B'+seedCode
    if args.doorsColorsRando == True and doorsColorsRandom == False:
        seedCode = 'D'+seedCode
    if areaRandomization == True and areaRandom == False:
        seedCode = 'A'+seedCode
    logicCode = ""
    if logicRandom == False:
        if args.logic == "vanilla":
            logicCode = "Randomizer_"
        elif args.logic == "mirror":
            logicCode = "Mirrortroid_"
        else:
            raise ValueError("Invalid logic name "+args.logic)
    # output ROM name
    fileName = "VARIA_{}{}{}_{}".format(logicCode, seedCode, seed, preset)
    if args.progressionSpeed != "random":
        fileName += "_" + args.progressionSpeed
    seedName = fileName
    if args.directory != '.':
        fileName = args.directory + '/' + fileName

    # settings processing
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
        if args.energyQtyList is not None:
            energyQties = args.energyQtyList.split(',')
        energyQty = random.choice(energyQties)
    qty = {'energy': energyQty,
           'minors': minorQty,
           'ammo': { 'Missile': missileQty,
                     'Super': superQty,
                     'PowerBomb': powerBombQty },
           'strictMinors' : args.strictMinors }
    logger.debug("quantities: {}".format(qty))

    if len(args.superFun) > 0:
        superFun = []
        for fun in args.superFun:
            if fun.find('Random') != -1:
                if bool(random.getrandbits(1)) == True:
                    superFun.append(fun[0:fun.find('Random')])
            else:
                superFun.append(fun)
        args.superFun = superFun
    logger.debug("superFun: {}".format(args.superFun))

    # controls
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

    # plando rando
    plandoSettings = None
    if args.plandoRando is not None:
        plandoRando = json.loads(args.plandoRando)
        forceArg('progressionSpeed', 'speedrun', "'Progression Speed' forced to speedrun")
        progSpeed = 'speedrun'
        forceArg('majorsSplit', 'Full', "'Majors Split' forced to Full")
        forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal")
        forceArg('progressionDifficulty', 'normal', "'Progression difficulty' forced to normal")
        progDiff = 'normal'
        RomPatches.ActivePatches = plandoRando["patches"]
        DoorsManager.unserialize(plandoRando["doors"])
        plandoSettings = {"locsItems": plandoRando['locsItems'], "forbiddenItems": plandoRando['forbiddenItems']}
    randoSettings = RandoSettings(maxDifficulty, progSpeed, progDiff, qty,
                                  restrictions, args.superFun, args.runtimeLimit_s,
                                  plandoSettings, minDifficulty)

    # area rando
    dotFile = None
    if areaRandomization == True:
        if args.dot == True:
            dotFile = args.directory + '/' + seedName + '.dot'
    graphSettings = GraphSettings(args.startLocation, areaRandomization, lightArea, args.bosses,
                                  args.escapeRando, minimizerN, dotFile,
                                  args.doorsColorsRando, args.allowGreyDoors, args.tourian,
                                  plandoRando["transitions"] if plandoSettings is not None else None)

    # objectives
    if plandoSettings is None:
        objectivesManager = Objectives(args.tourian != 'Disabled', randoSettings)
        Objectives.startAP = args.startLocation
        addedObjectives = 0
        if args.majorsSplit == "Scavenger":
            objectivesManager.setScavengerHunt()
            addedObjectives = 1

        if args.objective:
            try:
                nbObjectives = int(args.objective[0])
            except:
                nbObjectives = 0 if "random" in args.objective else None
            if nbObjectives is not None:
                availableObjectives = args.objectiveList.split(',') if args.objectiveList is not None else objectives
                if nbObjectives == 0:
                    nbObjectives = Objectives.getNbRandomObjectives(len(availableObjectives))
                objectivesManager.setRandom(nbObjectives, availableObjectives, distribute=args.distributeObjectives)
                if Objectives.nbActiveGoals < nbObjectives:
                    optErrMsgs.append(f"Could not reach {nbObjectives} possible objectives: only {Objectives.nbActiveGoals} available")
            else:
                maxActiveGoals = Objectives.maxActiveGoals - addedObjectives
                if len(args.objective) > maxActiveGoals:
                    args.objective = args.objective[0:maxActiveGoals]
                for goal in args.objective:
                    objectivesManager.addGoal(goal)
                # ignore these settings if objectives are not randomized
                args.hiddenObjectives = False
                args.distributeObjectives = False
            if args.nbObjectivesRequired is not None:
                nbReq = int(args.nbObjectivesRequired)
                if nbReq == 0:
                    nbReq = Objectives.getNbRandomRequiredObjectives()
            else:
                objectivesManager.expandGoals()
                nbReq = Objectives.nbActiveGoals
            objectivesManager.setNbRequiredGoals(nbReq)
            if Objectives.nbRequiredGoals < nbReq:
                optErrMsgs.append(f"Required objectives limited to {Objectives.nbRequiredGoals} instead of {nbReq}")
            Objectives.hidden = args.hiddenObjectives
        else:
            if not (args.majorsSplit == "Scavenger" and args.tourian == 'Disabled'):
                objectivesManager.setVanilla()
        goals = Objectives.activeGoals
        if len(goals) == 0:
            objectivesManager.addGoal('nothing')
        if any(goal for goal in goals if goal.area is not None and goal.gtype == "items"):
            forceArg('hud', True, "'VARIA HUD' forced to on", webValue='on')
        if any(goal for goal in goals if goal.gtype == "map"):
            forceArg('revealMap', True, "'Reveal Map' forced to on", webValue='on')
    else:
        args.tourian = plandoRando["tourian"]
        objectivesManager = Objectives(args.tourian != 'Disabled')
        for goal in plandoRando["objectives"]:
            objectivesManager.addGoal(goal)

    # choose on animal patch (only for vanilla flavor)
    if args.animals == True:
        if args.logic != "vanilla":
            optErrMsgs.append("Ignored animals surprise because of non vanilla ROM flavor")
        else:
            animalsPatches = ['animal_enemies.ips', 'animals.ips', 'draygonimals.ips', 'escapimals.ips',
                              'gameend.ips', 'grey_door_animals.ips', 'low_timer.ips', 'metalimals.ips',
                              'phantoonimals.ips', 'ridleyimals.ips']
            if args.escapeRando == False:
                args.patches.append(random.choice(animalsPatches))
                args.patches.append("Escape_Animals_Change_Event")
            else:
                optErrMsgs.append("Ignored animals surprise because of escape randomization")

    # generate patcher settings and extract patch sets to apply logic patches before randomization
    # will be completed later by items, area connections, escape...
    patcherSettings = {
        "isPlando": False,
        "majorsSplit": args.majorsSplit,
        "startLocation": args.startLocation,
        "optionalPatches": args.patches,
        "layout": not args.noLayout,
        "layoutCustom": None if args.layoutCustom is None else args.layoutCustom.split(','),
        "suitsMode": gravityBehaviour,
        "area": areaRandomization,
        "boss": args.bosses,
        "areaLayout": areaRandomization == True and not args.areaLayoutBase,
        "areaLayoutCustom": None if args.areaLayoutCustom is None else args.areaLayoutCustom.split(','),
        "variaTweaks": not args.noVariaTweaks,
        "variaTweaksCustom": None if args.variaTweaksCustom is None else args.variaTweaksCustom.split(','),
        "nerfedCharge": args.nerfedCharge,
        "nerfedRainbowBeam": energyQty == 'ultra sparse',
        "escapeAttr": None if args.escapeRando == False else True, # tmp value before actual attrs after randomization
        "escapeRandoRemoveEnemies": not args.noRemoveEscapeEnemies,
        "minimizerN": minimizerN,
        "tourian": args.tourian,
        "doorsColorsRando": args.doorsColorsRando,
        "vanillaObjectives": objectivesManager.isVanilla(),
        "ctrlDict": ctrlDict,
        "moonWalk": args.moonWalk,
        "seed": seed,
        "randoSettings": randoSettings,
        "displayedVersion": displayedVersion,
        "revealMap": args.revealMap,
        "hud": args.hud == True or args.majorsSplit == "FullWithHUD",
        "round_robin_cf": 'relaxed_round_robin_cf.ips' in args.patches, # will be applied twice but keep it like this for retrocompat
        "debug": args.debug
    }
    patchSets = [getPatchSet(patchSetName, RomFlavor.flavor) for patchSetName in getPatchSetsFromPatcherSettings(patcherSettings)]
    for patchSet in [p for p in patchSets if 'logic' in p]:
        RomPatches.ActivePatches += patchSet['logic']
    # these are dynamic
    RomPatches.ActivePatches += GraphUtils.getGraphPatches(args.startLocation)
    # this one isn't a simple patch but a ROM option
    if args.tourian == "Disabled":
        RomPatches.ActivePatches.append(RomPatches.NoTourian)

    # this operation needs logic patches
    if plandoSettings is None:
        DoorsManager.setDoorsColor()

    # print some parameters for jm's stats
    if args.jm == True or args.debug == True:
        print("logic:{}".format(args.logic))
        print("startLocation:{}".format(args.startLocation))
        print("progressionSpeed:{}".format(progSpeed))
        print("majorsSplit:{}".format(args.majorsSplit))
        print("morphPlacement:{}".format(args.morphPlacement))
        print("gravity:{}".format(gravityBehaviour))
        print("maxDifficulty:{}".format(maxDifficulty))
        print("tourian:{}".format(args.tourian))
        print("objectives:{}".format([g.name for g in Objectives.activeGoals]))
        print("energyQty:{}".format(energyQty))
        print("rom_patches: "+str(sorted(RomPatches.ActivePatches)))

    try:
        randoExec = RandoExec(seedName, args.vcr, randoSettings, graphSettings)
        (stuck, itemLocs, progItemLocs) = randoExec.randomize()
        patcherSettings['itemLocs'], patcherSettings['progItemLocs'] = itemLocs, progItemLocs
        # if we couldn't find an area layout then the escape graph is not created either
        # and getDoorConnections will crash if random escape is activated.
        if not stuck or args.vcr == True:
            patcherSettings['doors'] = GraphUtils.getDoorConnections(randoExec.areaGraph,
                                                                     areaRandomization, args.bosses,
                                                                     args.escapeRando if not stuck else False)
            patcherSettings['escapeAttr'] = randoExec.areaGraph.EscapeAttributes if args.escapeRando else None
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stdout)
        dumpErrorMsg(args.output, "Error: {}".format(e))
        sys.exit(-1)

    if stuck == True:
        dumpErrorMsg(args.output, randoExec.errorMsg)
        print("Can't generate " + fileName + " with the given parameters: {}".format(randoExec.errorMsg))
        # in vcr mode we still want the seed to be generated to analyze it
        if args.vcr == False:
            sys.exit(-1)

    randoExec.postProcessItemLocs(itemLocs, args.hideItems)

    # transform itemLocs in our usual dict(location, item), exclude minors, we'll get them with the solver
    locsItems = {}
    for itemLoc in itemLocs:
        locName = itemLoc.Location.Name
        itemType = itemLoc.Item.Type
        if args.debug == True:
            print("%s\t@%s\t%s" % (itemType, locName, str(itemLoc.Location.difficulty)))
        if itemType in ['Missile', 'Super', 'PowerBomb']:
            continue
        locsItems[locName] = itemType
    if args.debug == True:
        for loc in sorted(locsItems.keys()):
            print('{:>50}: {:>16} '.format(loc, locsItems[loc]))

    if plandoSettings is not None:
        with open(args.output, 'w') as jsonFile:
            json.dump({"itemLocs": [il.json() for il in itemLocs], "errorMsg": randoExec.errorMsg}, jsonFile)
        sys.exit(0)

    # generate extended stats
    if args.extStatsFilename is not None:
        with open(args.extStatsFilename, 'a') as extStatsFile:
            skillPreset = os.path.splitext(os.path.basename(args.paramsFileName))[0]
            if args.fakeRandoPreset is not None:
                randoPreset = args.fakeRandoPreset
            else:
                randoPreset = os.path.splitext(os.path.basename(args.randoPreset))[0]
            db.DB.dumpExtStatsItems(skillPreset, randoPreset, locsItems, extStatsFile)

    try:
        # args.rom is not None: generate local rom named filename.sfc with args.rom as source
        # args.output is not None: generate local json named args.output
        if args.rom is not None:
            # patch local rom
            romFileName = args.rom
            outFileName = fileName + '.sfc'
            shutil.copyfile(romFileName, outFileName)
            romPatcher = RomPatcher(settings=patcherSettings, romFileName=outFileName, magic=args.raceMagic)
        else:
            outFileName = args.output
            romPatcher = RomPatcher(settings=patcherSettings, magic=args.raceMagic)

        romPatcher.patchRom()

        if len(optErrMsgs) > 0:
            optErrMsgs.append(randoExec.errorMsg)
            msg = joinErrorMsgs(optErrMsgs)
        else:
            msg = randoExec.errorMsg

        if args.rom is None: # web mode
            data = romPatcher.romFile.data
            fileName = '{}.sfc'.format(fileName)
            data["fileName"] = fileName
            # error msg in json to be displayed by the web site
            data["errorMsg"] = msg
            # replaced parameters to update stats in database
            if len(forcedArgs) > 0:
                data["forcedArgs"] = forcedArgs
            with open(outFileName, 'w') as jsonFile:
                json.dump(data, jsonFile)
        else: # CLI mode
            if msg != "":
                print(msg)
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stdout)
        msg = "Error patching {}: ({}: {})".format(outFileName, type(e).__name__, e)
        dumpErrorMsg(args.output, msg)
        sys.exit(-1)

    if stuck == True:
        print("Rom generated for debug purpose: {}".format(fileName))
    else:
        print("Rom generated: {}".format(fileName))
