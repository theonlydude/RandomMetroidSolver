#!/usr/bin/python3
import argparse

from solver.standardSolver import StandardSolver
import utils.log

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Solver")
    parser.add_argument('--romFileName', '-r', help="the input rom", required=True, dest="romFileName")
    parser.add_argument('--preset', '-p', help="the preset file", nargs='?',
                        default='standard_presets/regular.json', dest='presetFileName')
    parser.add_argument('--difficultyTarget', '-t',
                        help="the difficulty target that the solver will aim for",
                        dest='difficultyTarget', nargs='?', default=None, type=int)
    parser.add_argument('--pickupStrategy', '-s', help="Pickup strategy for the Solver",
                        dest='pickupStrategy', nargs='?', default=None,
                        choices=['all', 'any'])
    parser.add_argument('--itemsForbidden', '-f', help="Item not picked up during solving",
                        dest='itemsForbidden', nargs='+', default=[], action='extend')

    parser.add_argument('--type', '-y', help="web or console", dest='outputType', nargs='?',
                        default='console', choices=['web', 'console'])
    parser.add_argument('--checkDuplicateMajor', dest="checkDuplicateMajor", action='store_true',
                        help="print a warning if the same major is collected more than once")
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--firstItemsLog', '-1',
                        help="file name logging first item location (spoilers!)",
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
                        dest='outputFileName', nargs='?', default=None)
    parser.add_argument('--runtime',
                        help="Maximum runtime limit in seconds. If 0 or negative, no runtime limit.",
                        dest='runtimeLimit_s', nargs='?', default=0, type=int)

    args = parser.parse_args()
    utils.log.init(args.debug)

    solver = StandardSolver(args)
    solver.solveRom()
