#!/usr/bin/python3
import sys, argparse

from solver.standardSolver import StandardSolver
from solver.conf import Conf
import utils.log

def standardSolver(args):
    if args.romFileName is None:
        print("Parameter --romFileName mandatory when not in interactive mode")
        sys.exit(1)

    if args.difficultyTarget is None:
        difficultyTarget = Conf.difficultyTarget
    else:
        difficultyTarget = args.difficultyTarget

    if args.pickupStrategy is None:
        pickupStrategy = Conf.itemsPickup
    else:
        pickupStrategy = args.pickupStrategy

    # itemsForbidden is like that: [['Varia'], ['Reserve'], ['Gravity']], fix it
    args.itemsForbidden = [item[0] for item in args.itemsForbidden]

    solver = StandardSolver(args.romFileName, args.presetFileName, difficultyTarget,
                            pickupStrategy, args.itemsForbidden, type=args.type,
                            firstItemsLog=args.firstItemsLog, extStatsFilename=args.extStatsFilename,
                            extStatsStep=args.extStatsStep,
                            displayGeneratedPath=args.displayGeneratedPath,
                            outputFileName=args.output, magic=args.raceMagic,
                            checkDuplicateMajor=args.checkDuplicateMajor, vcr=args.vcr,
                            runtimeLimit_s=args.runtimeLimit_s)

    solver.solveRom()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Solver")
    parser.add_argument('--romFileName', '-r', help="the input rom", nargs='?',
                        default=None, dest="romFileName")
    parser.add_argument('--preset', '-p', help="the preset file", nargs='?',
                        default=None, dest='presetFileName')
    parser.add_argument('--difficultyTarget', '-t',
                        help="the difficulty target that the solver will aim for",
                        dest='difficultyTarget', nargs='?', default=None, type=int)
    parser.add_argument('--pickupStrategy', '-s', help="Pickup strategy for the Solver",
                        dest='pickupStrategy', nargs='?', default=None,
                        choices=['all', 'any'])
    parser.add_argument('--itemsForbidden', '-f', help="Item not picked up during solving",
                        dest='itemsForbidden', nargs='+', default=[], action='append')

    parser.add_argument('--type', '-y', help="web or console", dest='type', nargs='?',
                        default='console', choices=['web', 'console'])
    parser.add_argument('--checkDuplicateMajor', dest="checkDuplicateMajor", action='store_true',
                        help="print a warning if the same major is collected more than once")
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--firstItemsLog', '-1',
                        help="path to file where for each item type the first time it was found and where will be written (spoilers!)",
                        nargs='?', default=None, type=str, dest='firstItemsLog')
    parser.add_argument('--ext_stats', help="Generate extended stats",
                        nargs='?', default=None, dest='extStatsFilename')
    parser.add_argument('--ext_stats_step', help="what extended stats to generate",
                        nargs='?', default=None, dest='extStatsStep', type=int)
    parser.add_argument('--displayGeneratedPath', '-g', help="display the generated path (spoilers!)",
                        dest='displayGeneratedPath', action='store_true')
    parser.add_argument('--race', help="Race mode magic number", dest='raceMagic', type=int)
    parser.add_argument('--vcr', help="Generate VCR output file", dest='vcr', action='store_true')
    # standard/interactive, web site
    parser.add_argument('--output', '-o', help="When called from the website, contains the result of the solver",
                        dest='output', nargs='?', default=None)
    parser.add_argument('--runtime',
                        help="Maximum runtime limit in seconds. If 0 or negative, no runtime limit.",
                        dest='runtimeLimit_s', nargs='?', default=0, type=int)

    args = parser.parse_args()

    if args.presetFileName is None:
        args.presetFileName = 'standard_presets/regular.json'

    utils.log.init(args.debug)

    standardSolver(args)
