#!/usr/bin/python

# https://itemrando.supermetroid.run/randomize

import sys, math, logging, argparse, re, json, os, subprocess

# the difficulties for each technics
from parameters import Knows, Settings, isKnows, isSettings
from parameters import easy, medium, hard, harder, hardcore, mania, god, samus, impossibru, infinity, diff2text

# the helper functions
from smbool import SMBool
from smboolmanager import SMBoolManager
from helpers import Pickup, Bosses
from rom import RomType, RomLoader
from graph_locations import locations as graphLocations
from graph import AccessGraph
from graph_access import vanillaTransitions, accessPoints
from utils import PresetLoader

class Conf:
    # ROM type, between :
    # - Total_TX/FX/CX/X/HX : Total's randomizer seeds, Tournament/Full/Casual/Normal/Hard
    # - Dessy : Dessyreqt randomizer seeds
    # - Vanilla : original game
    romType = 'Total_TX'

    # keep getting majors of at most this difficulty before going for minors or changing area
    difficultyTarget = medium

    # display the generated path (spoilers!)
    displayGeneratedPath = False

    # choose how many items are required (possible value: minimal/all/any)
    itemsPickup = 'minimal'

    # the list of items to not pick up
    itemsForbidden = []

class Solver:
    # given a rom and parameters returns the estimated difficulty

    def __init__(self, rom, presetFileName, difficultyTarget, pickupStrategy, itemsForbidden=[], type='console', debug=False, firstItemsLog=None, displayGeneratedPath=False, output=None):
        if debug == True:
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('Solver')

        self.setConf(difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath)

        self.firstLogFile = None
        if firstItemsLog is not None:
            self.firstLogFile = open(firstItemsLog, 'w')
            self.firstLogFile.write('Item;Location;Area\n')

        # can be called from command line (console) or from web site (web)
        self.type = type

        self.locations = graphLocations
        self.smbm = SMBoolManager.factory('all', cache=False)

        if presetFileName is not None:
            self.loadPreset(presetFileName)

        self.loadRom(rom)

        self.pickup = Pickup(Conf.itemsPickup)

        Bosses.reset()

    def setConf(self, difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath):
        Conf.difficultyTarget = difficultyTarget
        Conf.itemsPickup = pickupStrategy
        Conf.displayGeneratedPath = displayGeneratedPath
        Conf.itemsForbidden = itemsForbidden

    def loadRom(self, rom):
        # TODO: with the new ROM json format, rewrite this
        guessed = RomType.guess(rom)
        if guessed is not None:
            Conf.romType = guessed

        # TODO::the patches are not yet loaded in the romLoader, decouplate the locations/items assigment
        # and reading the patchs/transitions info
        self.romLoader = RomLoader.factory(rom)
        self.romLoader.assignItems(self.locations)
        (self.fullRando, self.areaRando) = RomType.apply(Conf.romType, self.romLoader.patches)

        print("ROM {} Type: {}, Patches present: {}, Area Rando: {}".format(rom, Conf.romType, self.romLoader.patches, (self.areaRando == True)))

        graphTransitions = self.romLoader.getTransitions()
        if graphTransitions is None:
            graphTransitions = vanillaTransitions

        self.areaGraph = AccessGraph(accessPoints, graphTransitions)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("Display items at locations:")
            for location in self.locations:
                self.log.debug('{:>50}: {:>16}'.format(location["Name"], location['itemName']))

    def loadPreset(self, presetFileName):
        presetLoader = PresetLoader.factory(presetFileName)
        presetLoader.load()
        self.smbm.createKnowsFunctions()

        if self.log.getEffectiveLevel() == logging.DEBUG:
            presetLoader.printToScreen()

    def solveRom(self):
        self.lastLoc = 'Landing Site'

        (difficulty, itemsOk) = self.computeDifficulty()
        if self.firstLogFile is not None:
            self.firstLogFile.close()

        if self.type == 'console':
            # print generated path
            if Conf.displayGeneratedPath == True:
                self.printPath("Generated path:", self.visitedLocations)
                # if we've aborted, display remaining majors
                if difficulty == -1 or itemsOk == False:
                    self.printPath("Remaining major locations:", self.majorLocations)
                    self.printPath("Remaining minor locations:", self.minorLocations)

            # display difficulty scale
            self.displayDifficulty(difficulty)

        return (difficulty, itemsOk)

    def displayDifficulty(self, difficulty):
        if difficulty >= 0:
            text = DifficultyDisplayer(difficulty).scale()
            print("Estimated difficulty: {}".format(text))
        else:
            print("Aborted run, can't finish the game with the given prerequisites")

    def getDiffThreshold(self):
        target = Conf.difficultyTarget
        threshold = target
        epsilon = 0.001
        if target <= easy:
            threshold = medium - epsilon
        elif target <= medium:
            threshold = hard - epsilon
        elif target <= hard:
            threshold = harder - epsilon
        elif target <= harder:
            threshold = hardcore - epsilon
        elif target <= hardcore:
            threshold = mania - epsilon

        return threshold

    def computeDifficulty(self):
        # loop on the available locations depending on the collected items.
        # before getting a new item, loop on all of them and get their difficulty,
        # the next collected item is the one with the smallest difficulty,
        # if equality between major and minor, take major first.

        if not self.fullRando:
            self.majorLocations = [loc for loc in self.locations if loc["Class"] == "Major"]
            self.minorLocations = [loc for loc in self.locations if loc["Class"] == "Minor"]
        else:
            self.majorLocations = self.locations[:] # copy
            self.minorLocations = self.majorLocations

        self.visitedLocations = []
        self.collectedItems = []

        # with the knowsXXX conditions some roms can be unbeatable, so we have to detect it
        previous = -1
        current = 0

        self.log.debug("{}: available major: {}, available minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        isEndPossible = False
        endDifficulty = mania
        area = 'Crateria Landing Site'
        diffThreshold = self.getDiffThreshold()
        while True:
            # actual while condition
            hasEnoughMinors = self.pickup.enoughMinors(self.smbm, self.minorLocations)
            hasEnoughMajors = self.pickup.enoughMajors(self.smbm, self.majorLocations)
            hasEnoughItems = hasEnoughMajors and hasEnoughMinors
            canEndGame = self.canEndGame()
            (isEndPossible, endDifficulty) = (canEndGame.bool, canEndGame.difficulty)
            if isEndPossible and hasEnoughItems and endDifficulty <= diffThreshold:
                self.log.debug("END")
                break

            #self.log.debug(str(self.collectedItems))
            self.log.debug("Current Area : " + area)

            # check if we have collected an item in the last loop
            current = len(self.collectedItems)
            if current == previous:
                if not isEndPossible:
                    self.log.debug("STUCK ALL")
                else:
                    self.log.debug("HARD END")
                break
            previous = current

            # compute the difficulty of all the locations
            self.computeLocationsDifficulty(self.majorLocations)
            self.computeLocationsDifficulty(self.minorLocations)

            # keep only the available locations
            majorAvailable = [loc for loc in self.majorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]
            minorAvailable = [loc for loc in self.minorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]

            # check if we're stuck
            if len(majorAvailable) == 0 and len(minorAvailable) == 0:
                if not isEndPossible:
                    self.log.debug("STUCK MAJORS and MINORS")
                else:
                    self.log.debug("HARD END")
                break

            # sort them on difficulty and proximity
            majorAvailable = self.getAvailableItemsList(majorAvailable, area, diffThreshold, hasEnoughMajors)
            minorAvailable = self.getAvailableItemsList(minorAvailable, area, diffThreshold, hasEnoughMinors)

            # first take major items of acceptable difficulty in the current area
            if (len(majorAvailable) > 0
                and majorAvailable[0]['SolveArea'] == area
                and majorAvailable[0]['difficulty'].difficulty <= diffThreshold):
                self.collectMajor(majorAvailable.pop(0))
                continue
            # next item decision
            if len(minorAvailable) == 0 and len(majorAvailable) > 0:
                self.log.debug('MAJOR')
                area = self.collectMajor(majorAvailable.pop(0))
            elif len(majorAvailable) == 0 and len(minorAvailable) > 0:
                # we don't check for hasEnoughMinors here, because we would be stuck, so pickup
                # what we can and hope it gets better
                self.log.debug('MINOR')
                area = self.collectMinor(minorAvailable.pop(0))
            elif len(majorAvailable) > 0 and len(minorAvailable) > 0:
                self.log.debug('BOTH|M=' + majorAvailable[0]['Name'] + ', m=' + minorAvailable[0]['Name'])
                # if both are available, decide based on area and difficulty
                nextMajDifficulty = majorAvailable[0]['difficulty'].difficulty
                nextMinArea = minorAvailable[0]['SolveArea']
                nextMinDifficulty = minorAvailable[0]['difficulty'].difficulty
                nextMajComeBack = majorAvailable[0]['comeBack']
                nextMinComeBack = minorAvailable[0]['comeBack']
                nextMajDistance = majorAvailable[0]['distance']
                nextMinDistance = minorAvailable[0]['distance']

                self.log.debug("diff area back dist - diff area back dist")
                self.log.debug("maj: {} '{}' {} {}, min: {} '{}' {} {}".format(nextMajDifficulty, majorAvailable[0]['SolveArea'], nextMajComeBack, nextMajDistance, nextMinDifficulty, nextMinArea, nextMinComeBack, nextMinDistance))

                # first take item from loc where you can come back
                if nextMajComeBack != nextMinComeBack:
                    self.log.debug("!= combeback")
                    if nextMajComeBack == True:
                        area = self.collectMajor(majorAvailable.pop(0))
                    else:
                        area = self.collectMinor(minorAvailable.pop(0))
                # take the closer one
                elif nextMajDistance != nextMinDistance:
                    self.log.debug("!= distance")
                    if nextMajDistance < nextMinDistance:
                        area = self.collectMajor(majorAvailable.pop(0))
                    else:
                        area = self.collectMinor(minorAvailable.pop(0))
                # if not all the minors type are collected, start with minors
                elif nextMinDifficulty <= diffThreshold and not self.haveAllMinorTypes():
                    self.log.debug("not all minors types")
                    area = self.collectMinor(minorAvailable.pop(0))
                elif nextMinArea == area and nextMinDifficulty <= diffThreshold and not hasEnoughMinors:
                    self.log.debug("not enough minors")
                    area = self.collectMinor(minorAvailable.pop(0))
                # difficulty over area (this is a difficulty estimator,
                # not a speedrunning simulator)
                elif nextMinDifficulty < nextMajDifficulty and not hasEnoughMinors:
                    self.log.debug("min easier and not enough minors")
                    area = self.collectMinor(minorAvailable.pop(0))
                else:
                    self.log.debug("maj easier")
                    area = self.collectMajor(majorAvailable.pop(0))
        # main loop end
        if isEndPossible:
            self.visitedLocations.append({
                'item' : 'The End',
                'itemName' : 'The End',
                'Name' : 'The End',
                'Area' : 'The End',
                'SolveArea' : 'The End',
                'Room': 'Mother Brain Room',
                'distance': 0,
                'difficulty' : SMBool(True, endDifficulty)
            })

        # compute difficulty value
        (difficulty, itemsOk) = self.computeDifficultyValue()

        self.log.debug("difficulty={}".format(difficulty))
        self.log.debug("itemsOk={}".format(itemsOk))
        self.log.debug("{}: remaining major: {}, remaining minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        self.log.debug("remaining majors:")
        for loc in self.majorLocations:
            self.log.debug("{} ({})".format(loc['Name'], loc['itemName']))

        self.log.debug("bosses: {}".format(Bosses.golden4Dead))

        return (difficulty, itemsOk)

    def computeLocationsDifficulty(self, locations):
        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.lastLoc)
        # check post available functions too
        for loc in locations:
            if 'PostAvailable' in loc:
                self.smbm.addItem(loc['itemName'])
                postAvailable = loc['PostAvailable'](self.smbm)
                self.smbm.removeItem(loc['itemName'])
                loc['difficulty'] = self.smbm.wand(loc['difficulty'], postAvailable)
            # also check if we can come back to landing site from the location
            if loc['difficulty'].bool == True:
                loc['comeBack'] = self.areaGraph.canAccess(self.smbm, loc['accessPoint'], 'Landing Site', infinity, loc['itemName'])

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("available locs:")
            for loc in locations:
                if loc['difficulty'].bool == True:
                    self.log.debug("{}: {}".format(loc['Name'], loc['difficulty']))

    def computeDifficultyValue(self):
        if not self.canEndGame().bool:
            # we have aborted
            return (-1, False)
        else:
            # return the maximum difficulty
            difficultyMax = 0
            for loc in self.visitedLocations:
                difficultyMax = max(difficultyMax, loc['difficulty'].difficulty)
            difficulty = difficultyMax

            # check if we have taken all the requested items
            if (self.pickup.enoughMinors(self.smbm, self.minorLocations)
                and self.pickup.enoughMajors(self.smbm, self.majorLocations)):
                return (difficulty, True)
            else:
                # can finish but can't take all the requested items
                return (difficulty, False)

    def getPath(self, locations):
        out = []
        for loc in locations:
            out.append([(loc['Name'], loc['Room']), loc['Area'], loc['SolveArea'], loc['itemName'],
                        '{0:.2f}'.format(loc['difficulty'].difficulty),
                        ', '.join(sorted(loc['difficulty'].knows)),
                        ', '.join(sorted(list(set(loc['difficulty'].items))))])

        return out

    def getKnowsUsed(self):
        knowsUsed = []
        for loc in self.visitedLocations:
            knowsUsed += loc['difficulty'].knows

        # get unique knows
        knowsUsed = len(list(set(knowsUsed)))

        # get total of known knows
        knowsKnown = len([knows for  knows in Knows.__dict__ if isKnows(knows) and getattr(Knows, knows)[0] == True])
        knowsKnown += len([hellRun for hellRun in Settings.hellRuns if Settings.hellRuns[hellRun] is not None])

        return (knowsUsed, knowsKnown)

    def printPath(self, message, locations):
        print(message)
        print('{:>50} {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'.format("Location Name", "Area", "Sub Area", "Distance", "Item", "Difficulty", "Knows used", "Items used"))
        print('-'*150)
        lastAP = None
        for loc in locations:
            if 'path' in loc:
                path = [ap.Name for ap in loc['path']]
                lastAP = path[-1]
                if not (len(path) == 1 and path[0] == lastAP):
                    path = " -> ".join(path)
                    print('{:>50}: {}'.format('Access points gone through', path))
            print('{:>50}: {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'.format(loc['Name'],
                                                                           loc['Area'],
                                                                           loc['SolveArea'],
                                                                           loc['distance'] if 'distance' in loc else 'nc',
                                                                           loc['itemName'],
                                                                           round(loc['difficulty'].difficulty, 2) if 'difficulty' in loc else 'nc',
                                                                           sorted(loc['difficulty'].knows) if 'difficulty' in loc else 'nc',
                                                                           list(set(loc['difficulty'].items)) if 'difficulty' in loc else 'nc'))

    def collectMajor(self, loc):
        self.majorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc)
        return area

    def collectMinor(self, loc):
        self.minorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc)
        return area

    def collectItem(self, loc):
        item = loc["itemName"]
        isNew = item not in self.collectedItems
        if item not in Conf.itemsForbidden:
            self.collectedItems.append(item)
            self.smbm.addItem(item)
        else:
            # update the name of the item
            item = "-{}-".format(item)
            loc["itemName"] = item
            self.collectedItems.append(item)
            # we still need the boss difficulty
            if 'Pickup' not in loc:
                loc["difficulty"] = SMBool(False)
        if 'Pickup' in loc:
            loc['Pickup']()
        if isNew is True and self.firstLogFile is not None:
            self.firstLogFile.write("{};{};{}\n".format(item, loc['Name'], loc['SolveArea']))

        self.log.debug("collectItem: {} at {}".format(item, loc['Name']))

        # last loc is used as root node for the graph
        self.lastLoc = loc['accessPoint']

        return loc['SolveArea']

    def haveAllMinorTypes(self):
        # the first minor of each type can be seen as a major, so check for them first before going to far in zebes
        hasPB = 'PowerBomb' in self.collectedItems
        hasSuper = 'Super' in self.collectedItems
        hasMissile = 'Missile' in self.collectedItems
        return (hasPB and hasSuper and hasMissile)

    def canEndGame(self):
        # to finish the game you must :
        # - beat golden 4 : we force pickup of the 4 items
        #   behind the bosses to ensure that
        # - defeat metroids
        # - destroy/skip the zebetites
        # - beat Mother Brain
        return self.smbm.wand(Bosses.allBossesDead(self.smbm), self.smbm.enoughStuffTourian())

    def getAvailableItemsList(self, locations, area, threshold, enough):
        # locations without distance are not available
        locations = [loc for loc in locations if 'distance' in loc]

        around = [loc for loc in locations if (loc['SolveArea'] == area or loc['distance'] < 3) and loc['difficulty'].difficulty <= threshold and not Bosses.areaBossDead(area) and 'comeBack' in loc and loc['comeBack'] == True]
        # usually pickup action means beating a boss, so do that first if possible
        around.sort(key=lambda loc: (0 if 'Pickup' in loc
                                     else 1,
                                     0 if 'comeBack' in loc and loc['comeBack'] == True
                                     else 1,
                                     0 if loc['SolveArea'] == area and loc['difficulty'].difficulty <= threshold
                                     else 1,
                                     loc['distance'] if loc['difficulty'].difficulty <= threshold
                                     else 100000,
                                     loc['difficulty'].difficulty))

        outside = [loc for loc in locations if not loc in around]
        self.log.debug("around1 = " + str([(loc['Name'], loc['difficulty'], loc['distance'], loc['comeBack'], loc['SolveArea']) for loc in around]))
        self.log.debug("outside1 = " + str([(loc['Name'], loc['difficulty'], loc['distance'], loc['comeBack'], loc['SolveArea']) for loc in outside]))
        # we want to sort the outside locations by putting the ones is the same
        # area first if we don't have enough items,
        # then we sort the remaining areas starting whith boss dead status
        outside.sort(key=lambda loc: (0 if loc['SolveArea'] == area and loc['difficulty'].difficulty <= threshold
                                      else 1,
                                      0 if 'comeBack' in loc and loc['comeBack'] == True
                                      else 1,
                                      loc['distance'] if loc['difficulty'].difficulty <= threshold
                                      else 100000,
                                      loc['difficulty'].difficulty if not Bosses.areaBossDead(loc['Area'])
                                                                      and loc['difficulty'].difficulty <= threshold
                                                                      and 'Pickup' in loc
                                      else 100000,
                                      loc['difficulty'].difficulty if not Bosses.areaBossDead(loc['Area'])
                                                                      and loc['difficulty'].difficulty <= threshold
                                      else 100000,
                                      loc['difficulty'].difficulty))
        self.log.debug("around2 = " + str([(loc['Name'], loc['difficulty'], loc['distance'], loc['comeBack'], loc['SolveArea']) for loc in around]))
        self.log.debug("outside2 = " + str([(loc['Name'], loc['difficulty'], loc['distance'], loc['comeBack'], loc['SolveArea']) for loc in outside]))

        return around + outside

class DifficultyDisplayer:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def scale(self):
        if self.difficulty >= impossibru:
            return "IMPOSSIBRU!"
        else:
            previous = 0
            for d in sorted(diff2text):
                if self.difficulty >= d:
                    previous = d
                else:
                    displayString = diff2text[previous]
                    displayString += ' '
                    scale = d - previous
                    pos = int(self.difficulty - previous)
                    displayString += '-' * pos
                    displayString += '^'
                    displayString += '-' * (scale - pos)
                    displayString += ' '
                    displayString += diff2text[d]
                    break

            return displayString

    def percent(self):
        # return the difficulty as a percent
        if self.difficulty == -1:
            return -1
        elif self.difficulty in [0, easy]:
            return 0
        elif self.difficulty >= mania:
            return 100

        difficultiesPercent = {
            easy: 0,
            medium: 20,
            hard: 40,
            harder: 60,
            hardcore: 80,
            mania: 100
        }

        difficulty = self.difficulty

        lower = 0
        percent = 100
        for upper in sorted(diff2text):
            if self.difficulty >= upper:
                lower = upper
            else:
                lowerPercent = difficultiesPercent[lower]
                upperPercent = difficultiesPercent[upper]

                a = (upperPercent-lowerPercent)/float(upper-lower)
                b = lowerPercent - a * lower

                percent = int(difficulty * a + b)
                break

        return percent

def guessRomType(filename):
    match = re.findall(r'VARIA_Randomizer_[A]?[F]?X\d+', filename)
    if len(match) > 0:
        if match[0][17] == 'A' and match[0][18] == 'F':
            return "VARIA Area Full"
        elif match[0][17] == 'A' and match[0][18] == 'X':
            return "VARIA Area Classic"
        elif match[0][17] == 'F':
            return "VARIA Full"
        elif match[0][17] == 'X':
            return "VARIA Classic"

    match = re.findall(r'[CTFH]?X\d+', filename)
    if len(match) > 0:
        if match[0][0] == 'C':
            return "Total Casual"
        elif match[0][0] == 'T':
            return "Total Tournament"
        elif match[0][0] == 'F':
            return "Total Full"
        elif match[0][0] == 'H':
            return "Total Hard"
        elif match[0][0] == 'X':
            return "Total Normal"

    match = re.findall(r'[CMS]?\d+', filename)
    if len(match) > 0:
        if match[0][0] == 'C':
            return "Dessy Casual"
        elif match[0][0] == 'M':
            return "Dessy Masochist"
        elif match[0][0] == 'S':
            return "Dessy Speedrunner"

    match = re.findall(r'Super[ _]*Metroid', filename)
    if len(match) > 0:
        return "Vanilla"

    # default to TX
    return "Total Tournament"

def generatePng(dotFileName):
    # use dot to generate the graph's image .png
    # use convert to generate the thumbnail
    # dotFileName: the /directory/image.dot
    # the png and thumbnails are generated in the same directory as the dot

    splited = os.path.splitext(dotFileName)
    pngFileName = splited[0] + '.png'
    pngThumbFileName = splited[0] + '_thumbnail.png'

    # dot -Tpng VARIA_Randomizer_AFX5399_noob.dot -oVARIA_Randomizer_AFX5399_noob.png
    params = ['dot', '-Tpng', dotFileName, '-o'+pngFileName]
    ret = subprocess.call(params)
    if ret != 0:
        print("Error calling dot {}: {}".format(params, ret))
        return (None, None)

    params = ['convert', pngFileName, '-resize', '1024', pngThumbFileName]
    ret = subprocess.call(params)
    if ret != 0:
        print("Error calling convert {}: {}".format(params, ret))
        os.remove(pngFileName)
        return (None, None)

    return (pngFileName, pngThumbFileName)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Solver")
    parser.add_argument('romFileName', help="the input rom")
    parser.add_argument('--preset', '-p', help="the preset file", nargs='?',
                        default=None, dest='presetFileName')

    parser.add_argument('--difficultyTarget', '-t',
                        help="the difficulty target that the solver will aim for",
                        dest='difficultyTarget', nargs='?', default=None, type=int)
    parser.add_argument('--pickupStrategy', '-s', help="Pickup strategy for the Solver",
                        dest='pickupStrategy', nargs='?', default=None)
    parser.add_argument('--itemsForbidden', '-f', help="Item not picked up during solving",
                        dest='itemsForbidden', nargs='+', default=[], action='append')

    parser.add_argument('--type', '-y', help="web or console", dest='type', nargs='?',
                        default='console', choices=['web', 'console'])
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--firstItemsLog', '-1',
                        help="path to file where for each item type the first time it was found and where will be written (spoilers!)",
                        nargs='?', default=None, type=str, dest='firstItemsLog')
    parser.add_argument('--displayGeneratedPath', '-g', help="display the generated path (spoilers!)",
                        dest='displayGeneratedPath', action='store_true')
    parser.add_argument('--output', '-o', help="When called from the website, contains the result of the solver",
                        dest='output', nargs='?', default=None)

    args = parser.parse_args()

    if args.presetFileName is None:
        args.presetFileName = 'regular'

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

    solver = Solver(args.romFileName, args.presetFileName, difficultyTarget,
                    pickupStrategy, args.itemsForbidden, type=args.type, debug=args.debug,
                    firstItemsLog=args.firstItemsLog, displayGeneratedPath=args.displayGeneratedPath,
                    output=args.output)

    (difficulty, itemsOk) = solver.solveRom()
    (used, total) = solver.getKnowsUsed()

    if args.output is None:
        print("({}, {}): diff : {}".format(difficulty, itemsOk, args.romFileName))
        print("{}/{}: knows Used : {}".format(used, total, args.romFileName))
        if difficulty >= 0:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        if solver.areaRando == True:
            dotFileName = os.path.basename(os.path.splitext(args.romFileName)[0])+'.json'
            dotFileName = os.path.join(os.path.expanduser('~/web2py/applications/solver/static/graph'), dotFileName)
            solver.areaGraph.toDot(dotFileName)
            (pngFileName, pngThumbFileName) = generatePng(dotFileName)
            if pngFileName is not None and pngThumbFileName is not None:
                pngFileName = os.path.basename(pngFileName)
                pngThumbFileName = os.path.basename(pngThumbFileName)
        else:
            pngFileName = None
            pngThumbFileName = None

        randomizedRom=args.romFileName
        diffPercent = DifficultyDisplayer(difficulty).percent()
        generatedPath = solver.getPath(solver.visitedLocations)
        romType = guessRomType(randomizedRom)

        result = dict(randomizedRom=randomizedRom, difficulty=difficulty,
                      generatedPath=generatedPath, diffPercent=diffPercent,
                      knowsUsed=(used, total), itemsOk=itemsOk, romType=romType,
                      pngFileName=pngFileName, pngThumbFileName=pngThumbFileName)

        with open(args.output, 'w') as jsonFile:
            json.dump(result, jsonFile)
