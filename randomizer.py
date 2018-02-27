#!/usr/bin/python

import argparse, random, os.path, json, sys

from itemrandomizerweb.stdlib import Random
from itemrandomizerweb import Items
from itemrandomizerweb.Randomizer import Randomizer
from tournament_locations import locations
from parameters import easy, medium, hard, harder, hardcore, mania, text2diff, diff2text
from solver import ParamsLoader
from rom import RomPatcher

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
    parser.add_argument('--algo', '-a', help="randomization algorithm to use",
                        dest='algo', nargs='?', default='Total_Tournament',
                        choices=['Total_Tournament', 'Total_Full', 'Total_Casual'])
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
                        dest='patches', nargs='+', default=[],
                        choices=['Max_Ammo_Display', 'MSU1_audio'])

    args = parser.parse_args()

    if args.paramsFileName is not None:
        ParamsLoader.factory(args.paramsFileName[0]).load()
        preset = os.path.splitext(os.path.basename(args.paramsFileName[0]))[0]
    elif args.preset is not None:
        preset = args.preset
        ParamsLoader.factory('diff_presets/' + preset + '.json').load()
    else:
        preset = 'default'

    if args.seed == 0:
        seed = random.randint(0, 9999999)
    else:
        seed = args.seed

    if args.difficultyTarget:
        difficultyTarget = text2diff[args.difficultyTarget]
    else:
        difficultyTarget = hard

    algo = args.algo

    algo2text = {
        'Total_Tournament': 'TX',
        'Total_Full': 'FX',
        'Total_Casual': 'CX',
        'Total_Normal': 'X',
        'Total_Hard': 'HX'}

    fileName = 'Ouiche Randomizer ' + algo2text[algo] + str(seed) + ' ' + preset + ' ' + diff2text[difficultyTarget]

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

    locationPool = locations

    try:
        randomizer = Randomizer.factory(algo, seed, difficultyTarget, locations)
        itemLocs = randomizer.generateItems()
    except:
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
        RomPatcher.patch(romFileName, fileName, itemLocs)

        difficulty = algo[algo.find('_')+1:]
        RomPatcher.applyIPSPatches(fileName, difficulty, args.patches)

        RomPatcher.writeSeed(fileName, seed)
    else:
        if args.output is not None:
            # web service
            locsItems = {}
            for itemLoc in itemLocs:
                itemCode = Items.getItemTypeCode(itemLoc['Item'],
                                                 itemLoc['Location']['Visibility'],
                                                 returnsInt = True)
                locsItems[itemLoc['Location']['Address']] = itemCode[0]
                locsItems[itemLoc['Location']['Address'] + 1] = itemCode[1]

            locsItems["fileName"] = fileName + '.sfc'

            #print("locsItems={}".format(locsItems))
            with open(args.output, 'w') as jsonFile:
                json.dump(locsItems, jsonFile)
        else:
            # rom json
            fileName += '.json'
            with open(fileName, 'w') as jsonFile:
                json.dump(locsItems, jsonFile)

    print("Rom generated: {}".format(fileName))
