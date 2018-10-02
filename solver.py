#!/usr/bin/python

import sys, math, argparse, re, json, os, subprocess, logging

# the difficulties for each technics
from parameters import Knows, Settings, isKnows, isSettings
from parameters import easy, medium, hard, harder, hardcore, mania, god, samus, impossibru, infinity, diff2text

# the helper functions
from smbool import SMBool
from smboolmanager import SMBoolManager
from helpers import Pickup, Bosses
from rom import RomLoader
from graph_locations import locations as graphLocations
from graph import AccessGraph
from graph_access import vanillaTransitions, accessPoints
from utils import PresetLoader
import log

class Conf:
    # keep getting majors of at most this difficulty before going for minors or changing area
    difficultyTarget = medium

    # display the generated path (spoilers!)
    displayGeneratedPath = False

    # choose how many items are required (possible value: minimal/all/any)
    itemsPickup = 'minimal'

    # the list of items to not pick up
    itemsForbidden = []

class SolverState(object):
    def fromSolver(self, solver):
        self.state = {}
        # bool
        self.state["fullRando"] = solver.fullRando
        # bool
        self.state["areaRando"] = solver.areaRando
        # dict of raw patches
        self.state["patches"] = solver.patches
        # dict {locName: {itemName: "xxx", "accessPoint": "xxx"}, ...}
        self.state["locsData"] = self.getLocsData(solver.locations)
        # list [(ap1, ap2), (ap3, ap4), ...]
        self.state["graphTransitions"] = solver.graphTransitions
        # preset file name
        self.state["presetFileName"] = solver.presetFileName
        ## items collected / locs visited / bosses killed
        # list [item1, item2, ...]
        self.state["collectedItems"] = solver.collectedItems
        # dict {locName: {index: 0, difficulty: (bool, diff, ...), ...} with index being the position of the loc in visitedLocations
        self.state["visitedLocations"] = self.getVisitedLocations(solver.visitedLocations)
        # dict {locName: (bool, diff, [know1, ...], [item1, ...]), ...}
        self.state["availableLocations"] = self.getAvailableLocations(solver.majorLocations)
        # string of last access point
        self.state["lastLoc"] = solver.lastLoc
        # list of killed bosses: ["boss1", "boss2"]
        self.state["bosses"] = [boss for boss in Bosses.golden4Dead if Bosses.golden4Dead[boss] == True]
        # dict {locNameWeb: {infos}, ...}
        self.state["availableLocationsWeb"] = self.getAvailableLocationsWeb(solver.majorLocations)
        # dict {locNameWeb: {infos}, ...}
        self.state["visitedLocationsWeb"] = self.getAvailableLocationsWeb(solver.visitedLocations)

    def toSolver(self, solver):
        solver.fullRando = self.state["fullRando"]
        solver.areaRando = self.state["areaRando"]
        solver.patches = self.setPatches(self.state["patches"])
        self.setLocsData(solver.locations)
        solver.graphTransitions = self.state["graphTransitions"]
        # preset
        solver.presetFileName = self.state["presetFileName"]
        # items collected / locs visited / bosses killed
        solver.collectedItems = self.state["collectedItems"]
        (solver.visitedLocations, solver.majorLocations) = self.setLocations(self.state["visitedLocations"],
                                                                             self.state["availableLocations"],
                                                                             solver.locations)
        solver.lastLoc = self.state["lastLoc"]
        Bosses.reset()
        for boss in self.state["bosses"]:
            Bosses.beatBoss(boss)
        solver.availableLocationsWeb = self.state["availableLocationsWeb"]

    def getLocsData(self, locations):
        ret = {}
        for loc in locations:
            ret[loc["Name"]] = {"itemName": loc["itemName"]}
            if "accessPoint" in loc:
                ret[loc["Name"]]["accessPoint"] = loc["accessPoint"]
        return ret

    def setLocsData(self, locations):
        for loc in locations:
            loc["itemName"] = self.state["locsData"][loc["Name"]]["itemName"]
            if "accessPoint" in self.state["locsData"][loc["Name"]]:
                loc["accessPoint"] = self.state["locsData"][loc["Name"]]["accessPoint"]

    def getVisitedLocations(self, visitedLocations):
        # need to keep the order (for cancelation)
        ret = {}
        i = 0
        for loc in visitedLocations:
            diff = loc["difficulty"]
            ret[loc["Name"]] = {"index": i, "difficulty": (diff.bool, diff.difficulty, diff.knows, diff.items)}
            i += 1
        return ret

    def setLocations(self, visitedLocations, availableLocations, locations):
        retVis = []
        retMaj = []
        for loc in locations:
            if loc["Name"] in visitedLocations:
                # visitedLocations contains an index
                diff = visitedLocations[loc["Name"]]["difficulty"]
                loc["difficulty"] = SMBool(diff[0], diff[1], diff[2], diff[3])
                retVis.append((visitedLocations[loc["Name"]]["index"], loc))
            else:
                if loc["Name"] in availableLocations:
                    diff = availableLocations[loc["Name"]]
                    loc["difficulty"] = SMBool(diff[0], diff[1], diff[2], diff[3])
                retMaj.append(loc)
        retVis.sort(key=lambda x: x[0])
        return ([loc for (i, loc) in retVis], retMaj)

    def diff4isolver(self, difficulty):
        if difficulty < medium:
            return "easy"
        elif difficulty < hard:
            return "medium"
        elif difficulty < harder:
            return "hard"
        elif difficulty < hardcore:
            return "harder"
        elif difficulty < mania:
            return "hardcore"
        else:
            return "mania"

    def locName4isolver(self, locName):
        # remove space and special characters
        # sed -e 's+ ++g' -e 's+,++g' -e 's+(++g' -e 's+)++g' -e 's+-++g'
        return locName.translate(None, " ,()-")

    def knows2isolver(self, knows):
        result = []
        for know in knows:
            if know in Knows.desc:
                result.append(Knows.desc[know]['display'])
            else:
                result.append(know)
        return list(set(result))

    def getAvailableLocationsWeb(self, locations):
        ret = {}
        for loc in locations:
            if "difficulty" in loc and loc["difficulty"].bool == True:
                diff = loc["difficulty"]
                locName = self.locName4isolver(loc["Name"])
                ret[locName] = {"difficulty": self.diff4isolver(diff.difficulty),
                                "knows": self.knows2isolver(diff.knows),
                                "items": list(set(diff.items)),
                                "item": loc["itemName"],
                                "name": loc["Name"]}
        return ret

    def getAvailableLocations(self, locations):
        ret = {}
        for loc in locations:
            if "difficulty" in loc and loc["difficulty"].bool == True:
                diff = loc["difficulty"]
                ret[loc["Name"]] = (diff.bool, diff.difficulty, diff.knows, diff.items)
        return ret

    def setPatches(self, patchesData):
        # json's dicts keys are strings
        ret = {}
        for address in patchesData:
            ret[int(address)] = patchesData[address]
        return ret

    def fromJson(self, stateJsonFileName):
        with open(stateJsonFileName, 'r') as jsonFile:
            self.state = json.load(jsonFile)
#        print("Loaded Json State:")
#        for key in self.state:
#            if key in ["availableLocationsWeb", "visitedLocationsWeb", "collectedItems", "visitedLocations"]:
#                print("{}: {}".format(key, self.state[key]))
#        print("")

    def toJson(self, outputFileName):
        with open(outputFileName, 'w') as jsonFile:
            json.dump(self.state, jsonFile)
#        print("Dumped Json State:")
#        for key in self.state:
#            if key in ["availableLocationsWeb", "visitedLocationsWeb", "collectedItems", "visitedLocations"]:
#                print("{}: {}".format(key, self.state[key]))
#        print("")

class CommonSolver(object):
    def loadRom(self, rom, interactive=False):
        self.romFileName = rom
        self.romLoader = RomLoader.factory(rom)
        self.fullRando = self.romLoader.assignItems(self.locations)
        self.areaRando = self.romLoader.loadPatches()

        if interactive == False:
            self.patches = self.romLoader.getPatches()
        else:
            self.patches = self.romLoader.getRawPatches()
        print("ROM {} full: {} area: {} patches: {}".format(rom, self.fullRando,
                                                            self.areaRando, self.patches))

        self.graphTransitions = self.romLoader.getTransitions()
        if self.graphTransitions is None:
            self.graphTransitions = vanillaTransitions

        self.areaGraph = AccessGraph(accessPoints, self.graphTransitions)

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
        if self.firstLogFile is not None:
            if item not in self.collectedItems:
                self.firstLogFile.write("{};{};{};{}\n".format(item, loc['Name'], loc['Area'], loc['GraphArea']))

        self.log.debug("collectItem: {} at {}".format(item, loc['Name']))

        # last loc is used as root node for the graph
        self.lastLoc = loc['accessPoint']

        return loc['SolveArea']

class InteractiveSolver(CommonSolver):
    def __init__(self, output):
        self.log = log.get('Solver')

        self.outputFileName = output
        self.firstLogFile = None

    def dumpState(self):
        state = SolverState()
        state.fromSolver(self)
        state.toJson(self.outputFileName)

    def initialize(self, rom, presetFileName):
        # load rom and preset, return first state
        self.locations = graphLocations
        self.smbm = SMBoolManager()

        self.presetFileName = presetFileName
        self.loadPreset(self.presetFileName)

        self.loadRom(rom, interactive=True)
        self.locations = self.addMotherBrainLoc(self.locations)

        self.clear()

        # compute new available locations
        self.computeLocationsDifficulty(self.majorLocations)

        self.dumpState()

    def iterate(self, stateJson, locName, action):
        self.locations = self.addMotherBrainLoc(graphLocations)
        self.smbm = SMBoolManager()

        state = SolverState()
        state.fromJson(stateJson)
        state.toSolver(self)

        RomLoader.factory(self.patches).loadPatches()

        self.loadPreset(self.presetFileName)
        self.areaGraph = AccessGraph(accessPoints, self.graphTransitions)

        if action == 'clear':
            self.clear(True)
        else:
            # add already collected items to smbm
            self.smbm.addItems(self.collectedItems)

            if action == 'add':
                # pickup item at locName
                self.pickItemAt(locName)
            elif action == 'remove':
                # remove last collected item
                self.cancelLast()

        # compute new available locations
        self.computeLocationsDifficulty(self.majorLocations)

        # return them
        self.dumpState()

    def getLoc(self, locName):
        for loc in self.majorLocations:
            if loc["Name"] == locName:
                return loc
        raise Exception("Location '{}' not found in remaining locations".format(locName))

    def pickItemAt(self, locName):
        # collect new item at newLoc
        if locName not in self.availableLocationsWeb:
            raise Exception("Location '{}' not found in available locations".format(locName))
        self.collectMajor(self.getLoc(self.availableLocationsWeb[locName]["name"]))

    def cancelLast(self):
        # loc
        if len(self.visitedLocations) == 0:
            return

        loc = self.visitedLocations.pop()
        self.majorLocations.append(loc)

        # pickup func
        if 'Unpickup' in loc:
            loc['Unpickup']()

        # access point
        if len(self.visitedLocations) == 0:
            self.lastLoc = "Landing Site"
        else:
            self.lastLoc = self.visitedLocations[-1]["accessPoint"]

        # item
        item = loc["itemName"]
        if item not in ["Nothing", "NoEnergy"]:
            if item != self.collectedItems[-1]:
                raise Exception("Item of last collected loc {}: {} is different from last collected item: {}".format(loc["Name"], item, self.collectedItems[-1]))
            self.smbm.removeItem(item)
            self.collectedItems.pop()

    def clear(self, reload=False):
        self.collectedItems = []
        self.visitedLocations = []
        self.lastLoc = 'Landing Site'
        self.majorLocations = self.locations
        if reload == True:
            for loc in self.majorLocations:
                if "difficulty" in loc:
                    del loc["difficulty"]
        Bosses.reset()
        self.smbm.resetItems()

    def addMotherBrainLoc(self, locations):
        # in the interactive solver mother brain is a new loc
        locations.append({
            'Area': "Tourian",
            'GraphArea': "Tourian",
            'SolveArea': "Tourian",
            'Name': "Mother Brain",
            'Visibility': "Visible",
            'Room': 'Mother Brain Room',
            'itemName': "Nothing",
            'AccessFrom' : {
                'Statues Hallway Left': lambda sm: SMBool(True)
            },
            'Available': lambda sm: sm.wand(Bosses.allBossesDead(sm), sm.enoughStuffTourian())
        })
        return locations

class StandardSolver(CommonSolver):
    # given a rom and parameters returns the estimated difficulty

    def __init__(self, rom, presetFileName, difficultyTarget, pickupStrategy, itemsForbidden=[], type='console', firstItemsLog=None, displayGeneratedPath=False, outputFileName=None):
        self.log = log.get('Solver')

        self.setConf(difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath)

        self.firstLogFile = None
        if firstItemsLog is not None:
            self.firstLogFile = open(firstItemsLog, 'w')
            self.firstLogFile.write('Item;Location;Area\n')

        # can be called from command line (console) or from web site (web)
        self.type = type
        self.output = Out.factory(self.type, self)
        self.outputFileName = outputFileName

        self.locations = graphLocations
        self.smbm = SMBoolManager()

        self.presetFileName = presetFileName
        self.loadPreset(self.presetFileName)

        self.loadRom(rom)

        self.pickup = Pickup(Conf.itemsPickup)

    def setConf(self, difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath):
        Conf.difficultyTarget = difficultyTarget
        Conf.itemsPickup = pickupStrategy
        Conf.displayGeneratedPath = displayGeneratedPath
        Conf.itemsForbidden = itemsForbidden

    def solveRom(self):
        self.lastLoc = 'Landing Site'

        (self.difficulty, self.itemsOk) = self.computeDifficulty()
        if self.firstLogFile is not None:
            self.firstLogFile.close()

        (self.knowsUsed, self.knowsKnown) = self.getKnowsUsed()

        self.output.out()

    def getRemainMajors(self):
        return [loc for loc in self.majorLocations if loc['difficulty'].bool == False and loc['itemName'] not in ['Nothing', 'NoEnergy']]

    def getRemainMinors(self):
        if self.fullRando == True:
            return None
        else:
            return [loc for loc in self.minorLocations if loc['difficulty'].bool == False and loc['itemName'] not in ['Nothing', 'NoEnergy']]

    def getSkippedMajors(self):
        return [loc for loc in self.majorLocations if loc['difficulty'].bool == True and loc['itemName'] not in ['Nothing', 'NoEnergy']]

    def getUnavailMajors(self):
        return [loc for loc in self.majorLocations if loc['difficulty'].bool == False and loc['itemName'] not in ['Nothing', 'NoEnergy']]


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
            if self.fullRando == False:
                self.computeLocationsDifficulty(self.minorLocations)

            # keep only the available locations
            majorsAvailable = [loc for loc in self.majorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]
            minorsAvailable = [loc for loc in self.minorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]

            # check if we're stuck
            if len(majorsAvailable) == 0 and len(minorsAvailable) == 0:
                if not isEndPossible:
                    self.log.debug("STUCK MAJORS and MINORS")
                else:
                    self.log.debug("HARD END")
                break

            # sort them on difficulty and proximity
            majorsAvailable = self.getAvailableItemsList(majorsAvailable, area, diffThreshold)
            if self.fullRando == True:
                minorsAvailable = majorsAvailable
            else:
                minorsAvailable = self.getAvailableItemsList(minorsAvailable, area, diffThreshold)

            # choose one to pick up
            area = self.nextDecision(majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold, area)

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

    def getAvailableItemsList(self, locations, area, threshold):
        # locations without distance are not available
        locations = [loc for loc in locations if 'distance' in loc]

        around = [loc for loc in locations if (loc['SolveArea'] == area or loc['distance'] < 3) and loc['difficulty'].difficulty <= threshold and not Bosses.areaBossDead(area) and 'comeBack' in loc and loc['comeBack'] == True]
        # pickup action means beating a boss, so do that first if possible
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

    def nextDecision(self, majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold, area):
        # first take major items of acceptable difficulty in the current area
        if (len(majorsAvailable) > 0
            and majorsAvailable[0]['SolveArea'] == area
            and majorsAvailable[0]['difficulty'].difficulty <= diffThreshold):
            return self.collectMajor(majorsAvailable.pop(0))
        # next item decision
        if len(minorsAvailable) == 0 and len(majorsAvailable) > 0:
            self.log.debug('MAJOR')
            return self.collectMajor(majorsAvailable.pop(0))
        elif len(majorsAvailable) == 0 and len(minorsAvailable) > 0:
            # we don't check for hasEnoughMinors here, because we would be stuck, so pickup
            # what we can and hope it gets better
            self.log.debug('MINOR')
            return self.collectMinor(minorsAvailable.pop(0))
        elif len(majorsAvailable) > 0 and len(minorsAvailable) > 0:
            self.log.debug('BOTH|M=' + majorsAvailable[0]['Name'] + ', m=' + minorsAvailable[0]['Name'])
            # if both are available, decide based on area and difficulty
            nextMajDifficulty = majorsAvailable[0]['difficulty'].difficulty
            nextMinArea = minorsAvailable[0]['SolveArea']
            nextMinDifficulty = minorsAvailable[0]['difficulty'].difficulty
            nextMajComeBack = majorsAvailable[0]['comeBack']
            nextMinComeBack = minorsAvailable[0]['comeBack']
            nextMajDistance = majorsAvailable[0]['distance']
            nextMinDistance = minorsAvailable[0]['distance']

            self.log.debug("diff area back dist - diff area back dist")
            self.log.debug("maj: {} '{}' {} {}, min: {} '{}' {} {}".format(nextMajDifficulty, majorsAvailable[0]['SolveArea'], nextMajComeBack, nextMajDistance, nextMinDifficulty, nextMinArea, nextMinComeBack, nextMinDistance))

            if hasEnoughMinors == True and self.haveAllMinorTypes() == True and self.smbm.haveItem('Charge'):
                # we have charge, no longer need minors
                return self.collectMajor(majorsAvailable.pop(0))
            else:
                # first take item from loc where you can come back
                if nextMajComeBack != nextMinComeBack:
                    self.log.debug("!= combeback")
                    if nextMajComeBack == True:
                        return self.collectMajor(majorsAvailable.pop(0))
                    else:
                        return self.collectMinor(minorsAvailable.pop(0))
                # take the closer one
                elif nextMajDistance != nextMinDistance:
                    self.log.debug("!= distance")
                    if nextMajDistance < nextMinDistance:
                        return self.collectMajor(majorsAvailable.pop(0))
                    else:
                        return self.collectMinor(minorsAvailable.pop(0))
                # if not all the minors type are collected, start with minors
                elif nextMinDifficulty <= diffThreshold and not self.haveAllMinorTypes():
                    self.log.debug("not all minors types")
                    return self.collectMinor(minorsAvailable.pop(0))
                elif nextMinArea == area and nextMinDifficulty <= diffThreshold:
                    self.log.debug("not enough minors")
                    return self.collectMinor(minorsAvailable.pop(0))
                # difficulty over area (this is a difficulty estimator,
                # not a speedrunning simulator)
                elif nextMinDifficulty < nextMajDifficulty:
                    self.log.debug("min easier and not enough minors")
                    return self.collectMinor(minorsAvailable.pop(0))
                else:
                    self.log.debug("maj easier")
                    return self.collectMajor(majorsAvailable.pop(0))

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

    def tryRemainingLocs(self):
        # use preset which knows every techniques to test the remaining locs to
        # find which technique could allow to continue the seed
        locations = self.majorLocations if self.fullRando == True else self.majorLocations + self.minorLocations

        presetFileName = os.path.expanduser('~/RandomMetroidSolver/standard_presets/solution.json')
        presetLoader = PresetLoader.factory(presetFileName)
        presetLoader.load()
        self.smbm.createKnowsFunctions()

        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.lastLoc)

        return [loc for loc in locations if loc['difficulty'].bool == True]

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

class Out(object):
    @staticmethod
    def factory(output, solver):
        if output == 'web':
            return OutWeb(solver)
        elif output == 'console':
            return OutConsole(solver)
        else:
            raise Exception("Wrong output type for the Solver: {}".format(output))

class OutWeb:
    def __init__(self, solver):
        self.solver = solver

    def out(self):
        s = self.solver
        if s.areaRando == True:
            dotFileName = os.path.basename(os.path.splitext(s.romFileName)[0])+'.json'
            dotFileName = os.path.join(os.path.expanduser('~/web2py/applications/solver/static/graph'), dotFileName)
            s.areaGraph.toDot(dotFileName)
            (pngFileName, pngThumbFileName) = self.generatePng(dotFileName)
            if pngFileName is not None and pngThumbFileName is not None:
                pngFileName = os.path.basename(pngFileName)
                pngThumbFileName = os.path.basename(pngThumbFileName)
        else:
            pngFileName = None
            pngThumbFileName = None

        randomizedRom = os.path.basename(os.path.splitext(s.romFileName)[0])+'.sfc'
        diffPercent = DifficultyDisplayer(s.difficulty).percent()
        generatedPath = self.getPath(s.visitedLocations)
        collectedItems = s.smbm.getItems()

        if s.difficulty == -1:
            remainTry = self.getPath(s.tryRemainingLocs())
            remainMajors = self.getPath(s.getRemainMajors())
            remainMinors = self.getPath(s.getRemainMinors())
            skippedMajors = None
            unavailMajors = None
        else:
            remainTry = None
            remainMajors = None
            remainMinors = None
            skippedMajors = self.getPath(s.getSkippedMajors())
            unavailMajors = self.getPath(s.getUnavailMajors())

        result = dict(randomizedRom=randomizedRom, difficulty=s.difficulty,
                      generatedPath=generatedPath, diffPercent=diffPercent,
                      knowsUsed=(s.knowsUsed, s.knowsKnown), itemsOk=s.itemsOk, patches=s.patches,
                      pngFileName=pngFileName, pngThumbFileName=pngThumbFileName,
                      remainTry=remainTry, remainMajors=remainMajors, remainMinors=remainMinors,
                      skippedMajors=skippedMajors, unavailMajors=unavailMajors,
                      collectedItems=collectedItems)

        with open(s.outputFileName, 'w') as jsonFile:
            json.dump(result, jsonFile)

    def getPath(self, locations):
        if locations is None:
            return None

        out = []
        for loc in locations:
            out.append([(loc['Name'], loc['Room']), loc['Area'], loc['SolveArea'], loc['itemName'],
                        '{0:.2f}'.format(loc['difficulty'].difficulty),
                        ', '.join(sorted(loc['difficulty'].knows)),
                        ', '.join(sorted(list(set(loc['difficulty'].items)))),
                        [ap.Name for ap in loc['path']] if 'path' in loc else None])

        return out

    def generatePng(self, dotFileName):
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

class OutConsole:
    def __init__(self, solver):
        self.solver = solver

    def out(self):
        s = self.solver
        self.displayOutput()

        print("({}, {}): diff : {}".format(s.difficulty, s.itemsOk, s.romFileName))
        print("{}/{}: knows Used : {}".format(s.knowsUsed, s.knowsKnown, s.romFileName))

        if s.difficulty >= 0:
            sys.exit(0)
        else:
            sys.exit(1)

    def printPath(self, message, locations, displayAPs=True):
        print("")
        print(message)
        print('{:>50} {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'.format("Location Name", "Area", "Sub Area", "Distance", "Item", "Difficulty", "Knows used", "Items used"))
        print('-'*150)
        lastAP = None
        for loc in locations:
            if displayAPs == True and 'path' in loc:
                path = [ap.Name for ap in loc['path']]
                lastAP = path[-1]
                if not (len(path) == 1 and path[0] == lastAP):
                    path = " -> ".join(path)
                    print('{:>50}: {}'.format('Path', path))
            print('{:>50}: {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'.format(loc['Name'],
                                                                           loc['Area'],
                                                                           loc['SolveArea'],
                                                                           loc['distance'] if 'distance' in loc else 'nc',
                                                                           loc['itemName'],
                                                                           round(loc['difficulty'].difficulty, 2) if 'difficulty' in loc else 'nc',
                                                                           sorted(loc['difficulty'].knows) if 'difficulty' in loc else 'nc',
                                                                           list(set(loc['difficulty'].items)) if 'difficulty' in loc else 'nc'))

    def displayOutput(self):
        s = self.solver

        # print generated path
        if Conf.displayGeneratedPath == True:
            self.printPath("Generated path ({}/101):".format(len(s.visitedLocations)), s.visitedLocations)

            # if we've aborted, display missing techniques and remaining locations
            if s.difficulty == -1:
                self.printPath("Next locs which could have been available if more techniques were known:", s.tryRemainingLocs())

                remainMajors = s.getRemainMajors()
                if len(remainMajors) > 0:
                    self.printPath("Remaining major locations:", remainMajors, displayAPs=False)

                remainMinors = s.getRemainMinors()
                if remainMinors is not None and len(remainMinors) > 0:
                    self.printPath("Remaining minor locations:", remainMinors, displayAPs=False)

            else:
                # if some locs are not picked up display those which are available
                # and those which are not
                skippedMajors = s.getSkippedMajors()
                if len(skippedMajors) > 0:
                    self.printPath("Skipped major locations:", skippedMajors, displayAPs=False)
                else:
                    print("No skipped major locations")

                unavailMajors = s.getUnavailMajors()
                if len(unavailMajors) > 0:
                    self.printPath("Unaccessible major locations:", unavailMajors, displayAPs=False)
                else:
                    print("No unaccessible major locations")

            items = s.smbm.getItems()
            print("ETank: {}, Reserve: {}, Missile: {}, Super: {}, PowerBomb: {}".format(items['ETank'], items['Reserve'], items['Missile'], items['Super'], items['PowerBomb']))
            print("Majors: {}".format(sorted([item for item in items if items[item] == True])))

        # display difficulty scale
        self.displayDifficulty(s.difficulty)

    def displayDifficulty(self, difficulty):
        if difficulty >= 0:
            text = DifficultyDisplayer(difficulty).scale()
            print("Estimated difficulty: {}".format(text))
        else:
            print("Aborted run, can't finish the game with the given prerequisites")

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

def interactiveSolver(args):
    # to init, requires interactive/romFileName/presetFileName/output parameters
    # to iterate, requires interactive/state/loc/action/output parameters
    if args.romFileName != None and args.presetFileName != None and args.output != None:
        # init
        solver = InteractiveSolver(args.output, args.debug)
        solver.initialize(args.romFileName, args.presetFileName)
    elif args.state != None and args.action != None and args.output != None:
        # iterate
        if args.action == "add" and args.loc == None:
            print("Missing loc parameter when using action add")
            sys.exit(1)

        solver = InteractiveSolver(args.output)
        solver.iterate(args.state, args.loc, args.action)
    else:
        print("Wrong parameters for interactive mode")
        sys.exit(1)

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
                            firstItemsLog=args.firstItemsLog,
                            displayGeneratedPath=args.displayGeneratedPath,
                            outputFileName=args.output)

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
                        choices=['minimal', 'all', 'any'])
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
    # standard/interactive, web site
    parser.add_argument('--output', '-o', help="When called from the website, contains the result of the solver",
                        dest='output', nargs='?', default=None)
    # interactive, web site
    parser.add_argument('--interactive', '-i', help="Activate interactive mode for the solver",
                        dest='interactive', action='store_true')
    parser.add_argument('--state', help="JSON file of the Solver state (used in interactive mode)",
                        dest="state", nargs='?', default=None)
    parser.add_argument('--loc', help="Name of the location to action on (used in interactive mode)",
                        dest="loc", nargs='?', default=None)
    parser.add_argument('--action', help="Pickup item at location, remove last pickedup location, clear all (used in interactive mode)",
                        dest="action", nargs="?", default=None, choices=['init', 'add', 'remove', 'clear', 'get'])

    args = parser.parse_args()

    if args.presetFileName is None:
        args.presetFileName = 'standard_presets/regular.json'

    log.init(args.debug)

    if args.interactive == True:
        interactiveSolver(args)
    else:
        standardSolver(args)
