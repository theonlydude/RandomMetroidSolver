#!/usr/bin/python

import sys, math, argparse, re, json, os, subprocess, logging, random
from time import gmtime, strftime

# the difficulties for each technics
from parameters import Knows, Settings, isKnows, isSettings
from parameters import easy, medium, hard, harder, hardcore, mania, god, samus, impossibru, infinity, diff2text

# the helper functions
from smbool import SMBool
from smboolmanager import SMBoolManager
from helpers import Pickup, Bosses
from rom import RomLoader, RomPatcher, RomReader
from itemrandomizerweb.Items import ItemManager
from graph_locations import locations as graphLocations
from graph import AccessGraph
from graph_access import vanillaTransitions, accessPoints, getDoorConnections, getTransitions, vanillaBossesTransitions, getAps2DoorsPtrs
from utils import PresetLoader
from vcr import VCR
import log, db

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
    def __init__(self, debug=False):
        self.debug = debug

    def fromSolver(self, solver):
        self.state = {}
        # string
        self.state["majorsSplit"] = solver.majorsSplit
        # bool
        self.state["areaRando"] = solver.areaRando
        # bool
        self.state["bossRando"] = solver.bossRando
        # dict of raw patches
        self.state["patches"] = solver.patches
        # dict {locName: {itemName: "xxx", "accessPoint": "xxx"}, ...}
        self.state["locsData"] = self.getLocsData(solver.locations)
        # list [(ap1, ap2), (ap3, ap4), ...]
        self.state["areaTransitions"] = solver.areaTransitions
        # list [(ap1, ap2), (ap3, ap4), ...]
        self.state["bossTransitions"] = solver.bossTransitions
        # list [(ap1, ap2), ...]
        self.state["curGraphTransitions"] = solver.curGraphTransitions
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
        # dict {locNameWeb: {infos}, ...}
        self.state["remainLocationsWeb"] = self.getRemainLocationsWeb(solver.majorLocations)
        # string: standard/seedless/plando
        self.state["mode"] = solver.mode
        # string:
        self.state["seed"] = solver.seed
        # dict {point: point, ...} / array of startPoints
        (self.state["linesWeb"], self.state["linesSeqWeb"]) = self.getLinesWeb(solver.curGraphTransitions)
        # bool
        self.state["allTransitions"] = len(solver.curGraphTransitions) == len(solver.areaTransitions) + len(solver.bossTransitions)
        self.state["errorMsg"] = solver.errorMsg
        if len(solver.visitedLocations) > 0:
            self.state["last"] = {"loc": solver.visitedLocations[-1]["Name"],
                                  "item": solver.visitedLocations[-1]["itemName"]}
        else:
            self.state["last"] = ""

    def toSolver(self, solver):
        if 'majorsSplit' in self.state:
            solver.majorsSplit = self.state["majorsSplit"]
        else:
            # compatibility with existing sessions
            if self.state['fullRando'] == True:
                solver.majorsSplit = 'Full'
            else:
                solver.majorsSplit = 'Major'
        solver.areaRando = self.state["areaRando"]
        solver.bossRando = self.state["bossRando"]
        solver.patches = self.setPatches(self.state["patches"])
        self.setLocsData(solver.locations)
        solver.areaTransitions = self.state["areaTransitions"]
        solver.bossTransitions = self.state["bossTransitions"]
        solver.curGraphTransitions = self.state["curGraphTransitions"]
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
        solver.mode = self.state["mode"]
        solver.seed = self.state["seed"]

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
        if difficulty == -1:
            return "break"
        elif difficulty < medium:
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

    def name4isolver(self, locName):
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

    def transition2isolver(self, transition):
        transition = str(transition)
        return transition[0].lower()+transition[1:].translate(None, " ,()-")

    def getAvailableLocationsWeb(self, locations):
        ret = {}
        for loc in locations:
            if "difficulty" in loc and loc["difficulty"].bool == True:
                diff = loc["difficulty"]
                locName = self.name4isolver(loc["Name"])
                ret[locName] = {"difficulty": self.diff4isolver(diff.difficulty),
                                "knows": self.knows2isolver(diff.knows),
                                "items": list(set(diff.items)),
                                "item": loc["itemName"],
                                "name": loc["Name"]}
                if "comeBack" in loc:
                    ret[locName]["comeBack"] = loc["comeBack"]
                # for debug purpose
                if self.debug == True:
                    if "path" in loc:
                        ret[locName]["path"] = [a.Name for a in loc["path"]]
                    if "distance" in loc:
                        ret[locName]["distance"] = loc["distance"]
        return ret

    def getRemainLocationsWeb(self, locations):
        ret = {}
        for loc in locations:
            if "difficulty" not in loc or ("difficulty" in loc and loc["difficulty"].bool == False):
                locName = self.name4isolver(loc["Name"])
                ret[locName] = {"item": loc["itemName"],
                                "name": loc["Name"],
                                "knows": ["Sequence Break"],
                                "items": []}
                if self.debug == True:
                    if "difficulty" in loc:
                        ret[locName]["difficulty"] = str(loc["difficulty"])
                    if "distance" in loc:
                        ret[locName]["distance"] = loc["distance"]
        return ret

    def getLinesWeb(self, transitions):
        lines = {}
        linesSeq = []
        for (start, end) in transitions:
            startWeb = self.transition2isolver(start)
            endWeb = self.transition2isolver(end)
            lines[startWeb] = endWeb
            lines[endWeb] = startWeb
            linesSeq.append((startWeb, endWeb))
        return (lines, linesSeq)

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
#            if key in ["availableLocationsWeb", "visitedLocationsWeb", "collectedItems", "availableLocations", "visitedLocations"]:
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
    def loadRom(self, rom, interactive=False, magic=None):
        if rom == None:
            self.romFileName = 'seedless'
            self.majorsSplit = 'Full'
            self.areaRando = True
            self.bossRando = True
            self.patches = RomReader.getDefaultPatches()
            RomLoader.factory(self.patches).loadPatches()
            # in seedless load all the vanilla transitions
            self.areaTransitions = vanillaTransitions[:]
            self.bossTransitions = vanillaBossesTransitions[:]
            self.curGraphTransitions = self.bossTransitions + self.areaTransitions
            for loc in self.locations:
                loc['itemName'] = 'Nothing'
        else:
            self.romFileName = rom
            self.romLoader = RomLoader.factory(rom, magic)
            self.majorsSplit = self.romLoader.assignItems(self.locations)
            (self.areaRando, self.bossRando) = self.romLoader.loadPatches()

            if interactive == False:
                self.patches = self.romLoader.getPatches()
            else:
                self.patches = self.romLoader.getRawPatches()
            print("ROM {} majors: {} area: {} boss: {} patches: {}".format(rom, self.majorsSplit, self.areaRando, self.bossRando, self.patches))

            (self.areaTransitions, self.bossTransitions) = self.romLoader.getTransitions()
            if interactive == True and self.debug == False:
                # in interactive area mode we build the graph as we play along
                if self.areaRando == True and self.bossRando == True:
                    self.curGraphTransitions = []
                elif self.areaRando == True:
                    self.curGraphTransitions = self.bossTransitions[:]
                elif self.bossRando == True:
                    self.curGraphTransitions = self.areaTransitions[:]
                else:
                    self.curGraphTransitions = self.bossTransitions + self.areaTransitions
            else:
                self.curGraphTransitions = self.bossTransitions + self.areaTransitions

        self.areaGraph = AccessGraph(accessPoints, self.curGraphTransitions)

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

    def getLoc(self, locName):
        for loc in self.locations:
            if loc['Name'] == locName:
                return loc

    def computeLocationsDifficulty(self, locations):
        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.lastLoc)
        # check post available functions too
        for loc in locations:
            if loc['difficulty'].bool == True:
                if 'PostAvailable' in loc:
                    # in plando mode we can have the same major multiple times
                    already = self.smbm.haveItem(loc['itemName'])
                    isCount = self.smbm.isCountItem(loc['itemName'])

                    self.smbm.addItem(loc['itemName'])
                    postAvailable = loc['PostAvailable'](self.smbm)

                    if not already or isCount == True:
                        self.smbm.removeItem(loc['itemName'])

                    loc['difficulty'] = self.smbm.wand(loc['difficulty'], postAvailable)

                # also check if we can come back to landing site from the location
                loc['comeBack'] = self.areaGraph.canAccess(self.smbm, loc['accessPoint'], self.lastLoc, infinity, loc['itemName'])

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("available locs:")
            for loc in locations:
                if loc['difficulty'].bool == True:
                    self.log.debug("{}: {}".format(loc['Name'], loc['difficulty']))

    def collectMajor(self, loc, itemName=None):
        self.majorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc, itemName)
        return area

    def collectMinor(self, loc):
        self.minorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc)
        return area

    def collectItem(self, loc, item=None):
        if item == None:
            item = loc["itemName"]

        if self.vcr != None:
            self.vcr.addLocation(loc['Name'], item)

        if self.firstLogFile is not None:
            if item not in self.collectedItems:
                self.firstLogFile.write("{};{};{};{}\n".format(item, loc['Name'], loc['Area'], loc['GraphArea']))

        if item not in Conf.itemsForbidden:
            self.collectedItems.append(item)
            if self.checkDuplicateMajor == True:
                if item not in ['Nothing', 'NoEnergy', 'Missile', 'Super', 'PowerBomb', 'ETank', 'Reserve']:
                    if self.smbm.haveItem(item):
                        print("WARNING: {} has already been picked up".format(item))

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

        self.log.debug("collectItem: {} at {}".format(item, loc['Name']))

        # last loc is used as root node for the graph
        self.lastLoc = loc['accessPoint']

        return loc['SolveArea']

    def cancelLastItems(self, count):
        if self.vcr != None:
            self.vcr.addRollback(count)

        for _ in range(count):
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
            if item != self.collectedItems[-1]:
                raise Exception("Item of last collected loc {}: {} is different from last collected item: {}".format(loc["Name"], item, self.collectedItems[-1]))

            self.collectedItems.pop()

            # if multiple majors in plando mode, remove it from smbm only when it's the last occurence of it
            if self.smbm.isCountItem(item):
                self.smbm.removeItem(item)
            else:
                if item not in self.collectedItems:
                    self.smbm.removeItem(item)

    def getAvailableItemsList(self, locations, area, threshold):
        # locations without distance are not available
        locations = [loc for loc in locations if 'distance' in loc]

        if len(locations) == 0:
            return []

        around = [loc for loc in locations if ((loc['SolveArea'] == area or loc['distance'] < 3)
                                               and loc['difficulty'].difficulty <= threshold
                                               and not Bosses.areaBossDead(area)
                                               and 'comeBack' in loc and loc['comeBack'] == True)]
        outside = [loc for loc in locations if not loc in around]

        self.log.debug("around1 = {}".format([(loc['Name'], loc['difficulty'], loc['distance'], loc['comeBack'], loc['SolveArea']) for loc in around]))
        self.log.debug("outside1 = {}".format([(loc['Name'], loc['difficulty'], loc['distance'], loc['comeBack'], loc['SolveArea']) for loc in outside]))

        around.sort(key=lambda loc: (
            # locs in the same area
            0 if loc['SolveArea'] == area
            else 1,
            # nearest locs
            loc['distance'],
            # beating a boss
            0 if 'Pickup' in loc
            else 1,
            # easiest first
            loc['difficulty'].difficulty
            )
        )

        # we want to sort the outside locations by putting the ones is the same area first
        # then we sort the remaining areas starting whith boss dead status
        outside.sort(key=lambda loc: (
            # no come back heuristic
            loc["areaWeight"] if "areaWeight" in loc
            else 0,
            # first loc where we can come back
            0 if 'comeBack' in loc and loc['comeBack'] == True
            else 1,
            # first locs in the same area
            0 if loc['SolveArea'] == area and loc['difficulty'].difficulty <= threshold
            else 1,
            # first nearest locs
            loc['distance'] if loc['difficulty'].difficulty <= threshold
            else 100000,
            # beating a boss
            loc['difficulty'].difficulty if (not Bosses.areaBossDead(loc['Area'])
                                             and loc['difficulty'].difficulty <= threshold
                                             and 'Pickup' in loc)
            else 100000,
            # areas with boss still alive
            loc['difficulty'].difficulty if (not Bosses.areaBossDead(loc['Area'])
                                             and loc['difficulty'].difficulty <= threshold)
            else 100000,
            loc['difficulty'].difficulty))

        # display the criterias used for sorting
        self.log.debug("around2: {}".format([(loc['Name'], 0 if loc['SolveArea'] == area else 1, loc['distance'], 0 if 'Pickup' in loc else 1, loc['difficulty'].difficulty) for loc in around]))
        self.log.debug("outside2: (threshold: {}) name, areaWeight, comeBack, area, distance, boss, boss in area, difficulty".format(threshold))
        self.log.debug("outside2: {}".format([(loc['Name'], loc["areaWeight"] if "areaWeight" in loc else 0, 0 if 'comeBack' in loc and loc['comeBack'] == True else 1, 0 if loc['SolveArea'] == area and loc['difficulty'].difficulty <= threshold else 1, loc['distance'] if loc['difficulty'].difficulty <= threshold else 100000, loc['difficulty'].difficulty if (not Bosses.areaBossDead(loc['Area']) and loc['difficulty'].difficulty <= threshold and 'Pickup' in loc) else 100000, loc['difficulty'].difficulty if (not Bosses.areaBossDead(loc['Area']) and loc['difficulty'].difficulty <= threshold) else 100000, loc['difficulty'].difficulty) for loc in outside]))

        return around + outside

    def nextDecision(self, majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold, area):
        # first take major items of acceptable difficulty in the current area
        if (len(majorsAvailable) > 0
            and majorsAvailable[0]['SolveArea'] == area
            and majorsAvailable[0]['difficulty'].difficulty <= diffThreshold
            and majorsAvailable[0]['comeBack'] == True):
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
            # if both are available, decide based on area, difficulty and comeBack
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
                # if not all the minors type are collected, start with minors
                elif nextMinDifficulty <= diffThreshold and not self.haveAllMinorTypes():
                    self.log.debug("not all minors types")
                    return self.collectMinor(minorsAvailable.pop(0))
                elif nextMinArea == area and nextMinDifficulty <= diffThreshold:
                    self.log.debug("not enough minors")
                    return self.collectMinor(minorsAvailable.pop(0))
                # difficulty over area (this is a difficulty estimator, not a speedrunning simulator)
                elif nextMinDifficulty <= diffThreshold and nextMajDistance <= diffThreshold:
                    # take the closer one
                    if nextMajDistance != nextMinDistance:
                        self.log.debug("!= distance")
                        if nextMajDistance < nextMinDistance:
                            return self.collectMajor(majorsAvailable.pop(0))
                        else:
                            return self.collectMinor(minorsAvailable.pop(0))
                    # take the easier
                    elif nextMinDifficulty < nextMajDifficulty:
                        self.log.debug("min easier and not enough minors")
                        return self.collectMinor(minorsAvailable.pop(0))
                    elif nextMajDifficulty < nextMinDifficulty:
                        self.log.debug("maj easier")
                        return self.collectMajor(majorsAvailable.pop(0))
                    # same difficulty and distance for minor and major, take major first
                    else:
                        return self.collectMajor(majorsAvailable.pop(0))
                elif nextMinDifficulty > diffThreshold and nextMajDistance > diffThreshold:
                    # take the easier
                    if nextMinDifficulty < nextMajDifficulty:
                        self.log.debug("min easier and not enough minors")
                        return self.collectMinor(minorsAvailable.pop(0))
                    elif nextMajDifficulty < nextMinDifficulty:
                        self.log.debug("maj easier")
                        return self.collectMajor(majorsAvailable.pop(0))
                    # take the closer one
                    elif nextMajDistance != nextMinDistance:
                        self.log.debug("!= distance")
                        if nextMajDistance < nextMinDistance:
                            return self.collectMajor(majorsAvailable.pop(0))
                        else:
                            return self.collectMinor(minorsAvailable.pop(0))
                    # same difficulty and distance for minor and major, take major first
                    else:
                        return self.collectMajor(majorsAvailable.pop(0))
                else:
                    if nextMinDifficulty < nextMajDifficulty:
                        self.log.debug("min easier and not enough minors")
                        return self.collectMinor(minorsAvailable.pop(0))
                    else:
                        self.log.debug("maj easier")
                        return self.collectMajor(majorsAvailable.pop(0))

        raise Exception("Can't take a decision")

    def checkMB(self, mbLoc):
        # add mother brain loc and check if it's accessible
        self.majorLocations.append(mbLoc)
        self.computeLocationsDifficulty(self.majorLocations)
        if mbLoc["difficulty"] == True:
            self.log.debug("MB loc accessible")
            self.collectMajor(mbLoc)
            return True
        else:
            self.log.debug("MB loc not accessible")
            self.majorLocations.remove(mbLoc)
            return False

    def computeDifficulty(self):
        # loop on the available locations depending on the collected items.
        # before getting a new item, loop on all of them and get their difficulty,
        # the next collected item is the one with the smallest difficulty,
        # if equality between major and minor, take major first.

        # remove mother brain location (there items pickup conditions on top of going to mother brain location)
        mbLoc = self.getLoc('Mother Brain')
        self.locations.remove(mbLoc)

        if self.majorsSplit == 'Major':
            self.majorLocations = [loc for loc in self.locations if "Major" in loc["Class"] or "Boss" in loc["Class"]]
            self.minorLocations = [loc for loc in self.locations if "Minor" in loc["Class"]]
        elif self.majorsSplit == 'Chozo':
            self.majorLocations = [loc for loc in self.locations if "Chozo" in loc["Class"] or "Boss" in loc["Class"]]
            self.minorLocations = [loc for loc in self.locations if "Chozo" not in loc["Class"] and "Boss" not in loc["Class"]]
        else:
            # Full
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
                if self.checkMB(mbLoc):
                    self.log.debug("END")
                    break
                else:
                    self.log.debug("canEnd but MB loc not accessible")

            #self.log.debug(str(self.collectedItems))
            self.log.debug("Current Area : " + area)

            # check if we have collected an item in the last loop
            current = len(self.collectedItems)
            if current == previous:
                if not isEndPossible:
                    self.log.debug("STUCK ALL")
                    if self.comeBack.rewind(len(self.collectedItems)) == True:
                        # rewind ok
                        previous = len(self.collectedItems) - 1
                        continue
                    else:
                        # we're really stucked
                        self.log.debug("STUCK CAN'T REWIND")
                        break
                else:
                    self.log.debug("HARD END 1")
                    self.checkMB(mbLoc)
                    break
            previous = current

            # compute the difficulty of all the locations
            self.computeLocationsDifficulty(self.majorLocations)
            if self.majorsSplit != 'Full':
                self.computeLocationsDifficulty(self.minorLocations)

            # keep only the available locations
            majorsAvailable = [loc for loc in self.majorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]
            minorsAvailable = [loc for loc in self.minorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]

            # check if we're stuck
            if len(majorsAvailable) == 0 and len(minorsAvailable) == 0:
                if not isEndPossible:
                    self.log.debug("STUCK MAJORS and MINORS")
                    if self.comeBack.rewind(len(self.collectedItems)) == True:
                        previous = len(self.collectedItems) - 1
                        continue
                    else:
                        # we're really stucked
                        self.log.debug("STUCK CAN'T REWIND")
                        break
                else:
                    self.log.debug("HARD END 2")
                    self.checkMB(mbLoc)
                    break

            # handle no comeback heuristic
            if self.majorsSplit == 'Full':
                locs = majorsAvailable
            else:
                locs = majorsAvailable+minorsAvailable
            rewindRequired = self.comeBack.handleNoComeBack(locs, len(self.collectedItems))
            if rewindRequired == True:
                if self.comeBack.rewind(len(self.collectedItems)) == True:
                    previous = len(self.collectedItems) - 1
                    continue
                else:
                    # we're really stucked
                    self.log.debug("STUCK CAN'T REWIND")
                    break

            # sort them on difficulty and proximity
            majorsAvailable = self.getAvailableItemsList(majorsAvailable, area, diffThreshold)
            if self.majorsSplit == 'Full':
                minorsAvailable = majorsAvailable
            else:
                minorsAvailable = self.getAvailableItemsList(minorsAvailable, area, diffThreshold)

            self.comeBack.cleanNoComeBack(locs)

            # choose one to pick up
            area = self.nextDecision(majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold, area)

        # compute difficulty value
        (difficulty, itemsOk) = self.computeDifficultyValue()

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("difficulty={}".format(difficulty))
            self.log.debug("itemsOk={}".format(itemsOk))
            self.log.debug("{}: remaining major: {}, remaining minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

            self.log.debug("remaining majors:")
            for loc in self.majorLocations:
                self.log.debug("{} ({})".format(loc['Name'], loc['itemName']))

            self.log.debug("bosses: {}".format(Bosses.golden4Dead))

        return (difficulty, itemsOk)

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

class InteractiveSolver(CommonSolver):
    def __init__(self, output):
        self.errorMsg = ""
        self.checkDuplicateMajor = False
        self.vcr = None
        self.log = log.get('Solver')

        self.outputFileName = output
        self.firstLogFile = None
        self.locations = graphLocations

        (self.locsAddressName, self.locsWeb2Internal) = self.initLocsAddressName()
        self.transWeb2Internal = self.initTransitionsName()

    def initLocsAddressName(self):
        addressName = {}
        web2Internal = {}
        for loc in graphLocations:
            webName = self.locNameInternal2Web(loc["Name"])
            addressName[loc["Address"] % 0x10000] = webName
            web2Internal[webName] = loc["Name"]
        return (addressName, web2Internal)

    def initTransitionsName(self):
        web2Internal = {}
        for (startPoint, endPoint) in vanillaTransitions + vanillaBossesTransitions:
            for point in [startPoint, endPoint]:
                web2Internal[self.apNameInternal2Web(point)] = point
        return web2Internal

    def dumpState(self):
        state = SolverState(self.debug)
        state.fromSolver(self)
        state.toJson(self.outputFileName)

    def initialize(self, mode, rom, presetFileName, magic, debug, fill):
        # load rom and preset, return first state
        self.debug = debug
        self.mode = mode
        if self.mode != "seedless":
            self.seed = os.path.basename(os.path.splitext(rom)[0])+'.sfc'
        else:
            self.seed = "seedless"

        self.smbm = SMBoolManager()

        self.presetFileName = presetFileName
        self.loadPreset(self.presetFileName)

        self.loadRom(rom, interactive=True, magic=magic)
        if self.mode == 'plando':
            # in plando always consider that we're doing full
            self.majorsSplit = 'Full'

        self.clearItems()

        # in debug mode don't load plando locs/transitions
        if self.mode == 'plando' and self.debug == False:
            if fill == True:
                # load the source seed transitions and items/locations
                self.curGraphTransitions = self.bossTransitions + self.areaTransitions
                self.areaGraph = AccessGraph(accessPoints, self.curGraphTransitions)
                self.fillPlandoLocs()
            else:
                if self.areaRando == True:
                    plandoTrans = self.loadPlandoTransitions()
                    if len(plandoTrans) > 0:
                        self.curGraphTransitions = plandoTrans
                    self.areaGraph = AccessGraph(accessPoints, self.curGraphTransitions)

                self.loadPlandoLocs()

        # compute new available locations
        self.computeLocationsDifficulty(self.majorLocations)

        self.dumpState()

    def iterate(self, stateJson, scope, action, params):
        self.debug = params["debug"]
        self.smbm = SMBoolManager()

        state = SolverState()
        state.fromJson(stateJson)
        state.toSolver(self)

        RomLoader.factory(self.patches).loadPatches()

        self.loadPreset(self.presetFileName)

        # add already collected items to smbm
        self.smbm.addItems(self.collectedItems)

        if scope == 'item':
            if action == 'clear':
                self.clearItems(True)
            else:
                if action == 'add':
                    if self.mode == 'plando' or self.mode == 'seedless':
                        self.setItemAt(params['loc'], params['item'])
                    else:
                        # pickup item at locName
                        self.pickItemAt(params['loc'])
                elif action == 'remove':
                    # remove last collected item
                    self.cancelLastItems(params['count'])
                elif action == 'replace':
                    self.replaceItemAt(params['loc'], params['item'])
        elif scope == 'area':
            if action == 'clear':
                self.clearTransitions()
            else:
                if action == 'add':
                    startPoint = params['startPoint']
                    endPoint = params['endPoint']
                    self.addTransition(self.transWeb2Internal[startPoint], self.transWeb2Internal[endPoint])
                elif action == 'remove':
                    # remove last transition
                    self.cancelLastTransition()

        self.areaGraph = AccessGraph(accessPoints, self.curGraphTransitions)

        if scope == 'common':
            if action == 'save':
                return self.savePlando(params['lock'])
            elif action == 'randomize':
                self.randoPlando(params)

        # compute new available locations
        self.clearLocs(self.majorLocations)
        self.computeLocationsDifficulty(self.majorLocations)

        # return them
        self.dumpState()

    def getLocNameFromAddress(self, address):
        return self.locsAddressName[address]

    def loadPlandoTransitions(self):
        transitionsAddr = self.romLoader.getPlandoTransitions(len(vanillaBossesTransitions) + len(vanillaTransitions))
        return getTransitions(transitionsAddr)

    def loadPlandoLocs(self):
        # get the addresses of the already filled locs, with the correct order
        addresses = self.romLoader.getPlandoAddresses()

        # create a copy of the locations to avoid removing locs from self.locations
        self.majorLocations = self.locations[:]

        for address in addresses:
            # TODO::compute only the difficulty of the current loc
            self.computeLocationsDifficulty(self.majorLocations)

            locName = self.getLocNameFromAddress(address)
            self.pickItemAt(locName)

    def fillPlandoLocs(self):
        self.pickup = Pickup("all")
        self.comeBack = ComeBack(self)

        # backup
        locationsBck = self.locations[:]

        self.lastLoc = 'Landing Site'
        (self.difficulty, self.itemsOk) = self.computeDifficulty()

        if self.itemsOk == False:
            # add remaining locs as sequence break
            for loc in self.majorLocations[:]:
                loc["difficulty"] = SMBool(True, -1)
                if "accessPoint" not in loc:
                    # take first ap of the loc
                    loc["accessPoint"] = loc["AccessFrom"].keys()[0]
                self.collectMajor(loc)

        self.locations = locationsBck

    def fillGraph(self):
        # add self looping transitions on unused acces points
        usedAPs = {}
        for (src, dst) in self.curGraphTransitions:
            usedAPs[src] = True
            usedAPs[dst] = True

        singleAPs = []
        for ap in accessPoints:
            if ap.Internal == True:
                continue

            if ap.Name not in usedAPs:
                singleAPs.append(ap.Name)

        transitions = self.curGraphTransitions[:]
        for apName in singleAPs:
            transitions.append((apName, apName))

        return AccessGraph(accessPoints, transitions)

    def randoPlando(self, parameters):
        # if all the locations are visited, do nothing
        if len(self.majorLocations) == 0:
            return

        plandoLocsItems = {}
        for loc in self.visitedLocations:
            if "Boss" in loc["Class"]:
                plandoLocsItems[loc["Name"]] = "Boss"
            else:
                plandoLocsItems[loc["Name"]] = loc["itemName"]

        # add active patches
        patches = {
            0x7F1F:   {'value': 0xB6, 'name': "startCeres"},
            0x7F17:   {'value': 0xB6, 'name': "startLS"},
            0x21BD80: {'value': 0xD5, 'name': "layout"},
            0x06e37d: {'value': 0x01, 'name': "gravityNoHeatProtection"},
            0x7CC4D:  {'value': 0x37, 'name': "variaTweaks"},
            0x22D564: {'value': 0xF2, 'name': "area"},
            0x252FA7: {'value': 0xF8, 'name': "areaLayout"}
        }

        activePatches = []
        for address in self.patches:
            if address in patches:
                if self.patches[address] == patches[address]["value"]:
                    activePatches.append(patches[address]["name"])

        plandoCurrent = {
            "locsItems": plandoLocsItems,
            "transitions": self.curGraphTransitions,
            "patches": activePatches
        }

        plandoCurrentJson = json.dumps(plandoCurrent)

        params = [
            'python2',  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
            '--runtime', '10',
            '--param', self.presetFileName,
            '--output', self.outputFileName,
            '--plandoRando', plandoCurrentJson,
            '--progressionSpeed', parameters["progressionSpeed"],
            '--minorQty', parameters["minorQty"],
            '--maxDifficulty', 'hardcore',
            '--energyQty', parameters["energyQty"]
        ]

        subprocess.call(params)

        with open(self.outputFileName, 'r') as jsonFile:
            data = json.load(jsonFile)

        self.errorMsg = data["errorMsg"]

        # load the locations
        if "itemLocs" in data:
            self.clearItems(reload=True)
            itemsLocs = data["itemLocs"]

            # create a copy because we need self.locations to be full, else the state will be empty
            self.majorLocations = self.locations[:]

            for itemLoc in itemsLocs:
                locName = itemLoc["Location"]["Name"]
                loc = self.getLoc(locName)
                difficulty = itemLoc["Location"]["difficulty"]
                smbool = SMBool(difficulty["bool"], difficulty["difficulty"], difficulty["knows"], difficulty["items"])
                loc["difficulty"] = smbool
                itemName = itemLoc["Item"]["Type"]
                if itemName == "Boss":
                    itemName = "Nothing"
                loc["itemName"] = itemName
                loc["accessPoint"] = itemLoc["Location"]["accessPoint"]
                self.collectMajor(loc)

    def savePlando(self, lock):
        # store filled locations addresses in the ROM for next creating session
        locsItems = {}
        itemLocs = []
        for loc in self.visitedLocations:
            locsItems[loc["Name"]] = loc["itemName"]
        for loc in self.locations:
            if loc["Name"] in locsItems:
                itemLocs.append({'Location': loc, 'Item': ItemManager.getItem(locsItems[loc["Name"]])})
            else:
                # put nothing items in unused locations
                itemLocs.append({'Location': loc, 'Item': ItemManager.getItem("Nothing")})

        # patch the ROM
        if lock == True:
            magic = random.randint(1, 0xffff)
        else:
            magic = None
        romPatcher = RomPatcher(magic=magic, plando=True)
        patches = ['credits_varia.ips', 'tracking.ips']
        if magic != None:
            patches.insert(0, 'race_mode.ips')
        romPatcher.addIPSPatches(patches)
        romPatcher.commitIPS()
        romPatcher.writeItemsLocs(itemLocs)
        romPatcher.writeItemsNumber()
        romPatcher.writeSpoiler(itemLocs)
        class FakeRandoSettings:
            def __init__(self):
                self.qty = {'energy': 'plando'}
                self.progSpeed = 'plando'
                self.progDiff = 'plando'
                self.restrictions = {'Suits': False, 'Morph': 'plando'}
                self.superFun = {}
        randoSettings = FakeRandoSettings()
        romPatcher.writeRandoSettings(randoSettings, itemLocs)
        if magic != None:
            romPatcher.writeMagic()
        else:
            romPatcher.writePlandoAddresses(self.visitedLocations)
            if self.areaRando == True:
                doors = getDoorConnections(self.fillGraph(), self.areaRando, self.bossRando)
                romPatcher.writeDoorConnections(doors)
                doorsPtrs = getAps2DoorsPtrs()
                romPatcher.writePlandoTransitions(self.curGraphTransitions, doorsPtrs,
                                                  len(vanillaBossesTransitions) + len(vanillaTransitions))
        romPatcher.end()

        data = romPatcher.romFile.data
        preset = os.path.splitext(os.path.basename(self.presetFileName))[0]
        seedCode = 'FX'
        if self.bossRando == True:
            seedCode = 'B'+seedCode
        if self.areaRando == True:
            seedCode = 'A'+seedCode
        fileName = 'VARIA_Plandomizer_{}{}_{}.sfc'.format(seedCode, strftime("%Y%m%d%H%M%S", gmtime()), preset)
        data["fileName"] = fileName
        # error msg in json to be displayed by the web site
        data["errorMsg"] = ""
        with open(self.outputFileName, 'w') as jsonFile:
            json.dump(data, jsonFile)

    def locNameInternal2Web(self, locName):
        return locName.translate(None, " ,()-")

    def locNameWeb2Internal(self, locNameWeb):
        return self.locsWeb2Internal[locNameWeb]

    def apNameInternal2Web(self, apName):
        return apName[0].lower()+apName[1:].translate(None, " ")

    def getWebLoc(self, locNameWeb):
        locName = self.locNameWeb2Internal(locNameWeb)
        for loc in self.locations:
            if loc["Name"] == locName:
                return loc
        raise Exception("Location '{}' not found".format(locName))

    def pickItemAt(self, locName):
        # collect new item at newLoc
        loc = self.getWebLoc(locName)
        if "difficulty" not in loc or loc["difficulty"] == False:
            # sequence break
            loc["difficulty"] = SMBool(True, -1)
        if "accessPoint" not in loc:
            # take first ap of the loc
            loc["accessPoint"] = loc["AccessFrom"].keys()[0]
        self.collectMajor(loc)

    def setItemAt(self, locName, itemName):
        # set itemName at locName
        loc = self.getWebLoc(locName)
        # plando mode
        loc["itemName"] = itemName

        if "difficulty" not in loc:
            # sequence break
            loc["difficulty"] = SMBool(True, -1)
        if "accessPoint" not in loc:
            # take first ap of the loc
            loc["accessPoint"] = loc["AccessFrom"].keys()[0]

        self.collectMajor(loc, itemName)

    def replaceItemAt(self, locName, itemName):
        # replace itemName at locName
        loc = self.getWebLoc(locName)
        oldItemName = loc["itemName"]
        loc["itemName"] = itemName

        # major item can be set multiple times in plando mode
        count = self.collectedItems.count(oldItemName)
        isCount = self.smbm.isCountItem(oldItemName)

        # replace item at the old item spot in collectedItems
        index = next(i for i, vloc in enumerate(self.visitedLocations) if vloc['Name'] == loc['Name'])
        self.collectedItems[index] = itemName

        # update smbm if count item or major was only there once
        if isCount == True or count == 1:
            self.smbm.removeItem(oldItemName)

        self.smbm.addItem(itemName)

    def clearItems(self, reload=False):
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

    def addTransition(self, startPoint, endPoint):
        # already check in controller if transition is valid for seed
        self.curGraphTransitions.append((startPoint, endPoint))

    def cancelLastTransition(self):
        if self.areaRando == True and self.bossRando == True:
            if len(self.curGraphTransitions) > 0:
                self.curGraphTransitions.pop()
        elif self.areaRando == True:
            if len(self.curGraphTransitions) > len(self.bossTransitions):
                self.curGraphTransitions.pop()
        elif self.bossRando == True:
            if len(self.curGraphTransitions) > len(self.areaTransitions):
                self.curGraphTransitions.pop()

    def clearTransitions(self):
        if self.areaRando == True and self.bossRando == True:
            self.curGraphTransitions = []
        elif self.areaRando == True:
            self.curGraphTransitions = self.bossTransitions[:]
        elif self.bossRando == True:
            self.curGraphTransitions = self.areaTransitions[:]
        else:
            self.curGraphTransitions = self.bossTransitions + self.areaTransitions

    def clearLocs(self, locs):
        for loc in locs:
            if 'difficulty' in loc:
                del loc['difficulty']

    def getDiffThreshold(self):
        # in interactive solver we don't have the max difficulty parameter
        epsilon = 0.001
        return hard - epsilon

class StandardSolver(CommonSolver):
    # given a rom and parameters returns the estimated difficulty

    def __init__(self, rom, presetFileName, difficultyTarget, pickupStrategy, itemsForbidden=[], type='console',
                 firstItemsLog=None, extStatsFilename=None, displayGeneratedPath=False, outputFileName=None,
                 magic=None, checkDuplicateMajor=False, vcr=False):
        self.checkDuplicateMajor = checkDuplicateMajor
        self.vcr = VCR(rom, 'solver') if vcr == True else None

        self.log = log.get('Solver')

        self.setConf(difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath)

        self.firstLogFile = None
        if firstItemsLog is not None:
            self.firstLogFile = open(firstItemsLog, 'w')
            self.firstLogFile.write('Item;Location;Area\n')

        self.extStatsFilename = extStatsFilename

        # can be called from command line (console) or from web site (web)
        self.type = type
        self.output = Out.factory(self.type, self)
        self.outputFileName = outputFileName

        self.locations = graphLocations
        self.smbm = SMBoolManager()

        self.presetFileName = presetFileName
        self.loadPreset(self.presetFileName)

        self.loadRom(rom, magic=magic)

        self.pickup = Pickup(Conf.itemsPickup)

        self.comeBack = ComeBack(self)

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

        (self.knowsUsed, self.knowsKnown, knowsUsedList) = self.getKnowsUsed()

        if self.vcr != None:
            self.vcr.dump()

        if self.extStatsFilename != None:
            with open(self.extStatsFilename, 'a') as extStatsFile:
                db.DB.dumpExtStatsSolver(self.difficulty, knowsUsedList, extStatsFile)

        self.output.out()

    def getRemainMajors(self):
        return [loc for loc in self.majorLocations if loc['difficulty'].bool == False and loc['itemName'] not in ['Nothing', 'NoEnergy']]

    def getRemainMinors(self):
        if self.majorsSplit == 'Full':
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

    def getKnowsUsed(self):
        knowsUsed = []
        for loc in self.visitedLocations:
            knowsUsed += loc['difficulty'].knows

        # get unique knows
        knowsUsed = list(set(knowsUsed))
        knowsUsedCount = len(knowsUsed)

        # get total of known knows
        knowsKnownCount = len([knows for  knows in Knows.__dict__ if isKnows(knows) and getattr(Knows, knows)[0] == True])
        knowsKnownCount += len([hellRun for hellRun in Settings.hellRuns if Settings.hellRuns[hellRun] is not None])

        return (knowsUsedCount, knowsKnownCount, knowsUsed)

    def tryRemainingLocs(self):
        # use preset which knows every techniques to test the remaining locs to
        # find which technique could allow to continue the seed
        locations = self.majorLocations if self.majorsSplit == 'Full' else self.majorLocations + self.minorLocations

        presetFileName = os.path.expanduser('~/RandomMetroidSolver/standard_presets/solution.json')
        presetLoader = PresetLoader.factory(presetFileName)
        presetLoader.load()
        self.smbm.createKnowsFunctions()

        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.lastLoc)

        return [loc for loc in locations if loc['difficulty'].bool == True]

class ComeBack(object):
    # object to handle the decision to choose the next area when all locations have the "no comeback" flag.
    # handle rewinding to try the next area in case of a stuck.
    # one ComebackStep object is created each time we have to use the no comeback heuristic b, used for rewinding.
    def __init__(self, solver):
        self.comeBackSteps = []
        # used to rewind
        self.solver = solver
        self.log = log.get('Rewind')

    def handleNoComeBack(self, locations, cur):
        # return true if a rewind is required
        graphAreas = {}
        for loc in locations:
            if "comeBack" not in loc:
                return False
            if loc["comeBack"] == True:
                return False
            if loc["GraphArea"] in graphAreas:
                graphAreas[loc["GraphArea"]] += 1
            else:
                graphAreas[loc["GraphArea"]] = 1

        if len(graphAreas) == 1:
            return False

        self.log.debug("WARNING: use no come back heuristic for {} locs in {} graph areas".format(len(locations), len(graphAreas)))

        # check if we can use existing step
        if len(self.comeBackSteps) > 0:
            lastStep = self.comeBackSteps[-1]
            if lastStep.cur == cur:
                self.log.debug("Use last step at {}".format(cur))
                return lastStep.next(locations)

        # create a step
        self.log.debug("Create new step at {}".format(cur))
        step = ComeBackStep(graphAreas, cur)
        self.comeBackSteps.append(step)
        return step.next(locations)

    def cleanNoComeBack(self, locations):
        for loc in locations:
            if "areaWeight" in loc:
                del loc["areaWeight"]

    def rewind(self, cur):
        # come back to the previous step
        # if no more rewinds available: tell we're stuck by returning False
        if len(self.comeBackSteps) == 0:
            self.log.debug("No more steps to rewind")
            return False

        self.log.debug("Start rewind, current: {}".format(cur))

        lastStep = self.comeBackSteps[-1]
        if lastStep.cur == cur:
            # need to go up one more time
            self.comeBackSteps.pop()

            if len(self.comeBackSteps) == 0:
                self.log.debug("No more steps to rewind")
                return False

            lastStep = self.comeBackSteps[-1]
            self.log.debug("Rewind previous step at {}".format(lastStep.cur))

        count = cur - lastStep.cur
        self.solver.cancelLastItems(count)
        self.log.debug("Rewind {} items to {}".format(count, lastStep.cur))
        return True

class ComeBackStep(object):
    # one case of no come back decision
    def __init__(self, graphAreas, cur):
        self.visitedGraphAreas = []
        self.graphAreas = graphAreas
        self.cur = cur

    def next(self, locations):
        # use next available area, if all areas has been visited return True (stuck), else False
        if len(self.visitedGraphAreas) == len(self.graphAreas):
            return True

        # get area with max available locs
        maxAreaWeigth = 0
        maxAreaName = ""
        for graphArea in self.graphAreas:
            if graphArea in self.visitedGraphAreas:
                continue
            else:
                if self.graphAreas[graphArea] > maxAreaWeigth:
                    maxAreaWeigth = self.graphAreas[graphArea]
                    maxAreaName = graphArea
        self.visitedGraphAreas.append(maxAreaName)

        retGraphAreas = {}
        for graphArea in self.graphAreas:
            if graphArea == maxAreaName:
                retGraphAreas[graphArea] = 1
            else:
                retGraphAreas[graphArea] = 10000

        # update locs
        for loc in locations:
            loc["areaWeight"] = retGraphAreas[loc["GraphArea"]]

        return False

class Out(object):
    @staticmethod
    def factory(output, solver):
        if output == 'web':
            return OutWeb(solver)
        elif output == 'console':
            return OutConsole(solver)
        else:
            raise Exception("Wrong output type for the Solver: {}".format(output))

    def fixEnergy(self, items):
        # display number of energy used
        energies = [i for i in items if i.find('ETank') != -1]
        if len(energies) > 0:
            (maxETank, maxReserve, maxEnergy) = (0, 0, 0)
            for energy in energies:
                nETank = int(energy[0:energy.find('-ETank')])
                if energy.find('-Reserve') != -1:
                    nReserve = int(energy[energy.find(' - ')+len(' - '):energy.find('-Reserve')])
                else:
                    nReserve = 0
                nEnergy = nETank + nReserve
                if nEnergy > maxEnergy:
                    maxEnergy = nEnergy
                    maxETank = nETank
                    maxReserve = nReserve
                items.remove(energy)
            items.append('{}-ETank'.format(maxETank))
            if maxReserve > 0:
                items.append('{}-Reserve'.format(maxReserve))

class OutWeb(Out):
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
            self.fixEnergy(loc['difficulty'].items)

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
        # requires that graphviz is installed

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

class OutConsole(Out):
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
        print('{} {:>48} {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'.format("Z", "Location Name", "Area", "Sub Area", "Distance", "Item", "Difficulty", "Knows used", "Items used"))
        print('-'*150)
        lastAP = None
        for loc in locations:
            if displayAPs == True and 'path' in loc:
                path = [ap.Name for ap in loc['path']]
                lastAP = path[-1]
                if not (len(path) == 1 and path[0] == lastAP):
                    path = " -> ".join(path)
                    print('{:>50}: {}'.format('Path', path))
            line = '{} {:>48}: {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'

            self.fixEnergy(loc['difficulty'].items)

            print(line.format('Z' if 'Chozo' in loc['Class'] else ' ',
                              loc['Name'],
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
    # to init, requires interactive/romFileName/presetFileName/output parameters in standard/plando mode
    # to init, requires interactive/presetFileName/output parameters in seedless mode
    # to iterate, requires interactive/state/[loc]/[item]/action/output parameters in item scope
    # to iterate, requires interactive/state/[startPoint]/[endPoint]/action/output parameters in area scope
    if args.action == 'init':
        # init
        if args.mode != 'seedless' and args.romFileName == None:
            print("Missing romFileName parameter for {} mode".format(args.mode))
            sys.exit(1)

        if args.presetFileName == None or args.output == None:
            print("Missing preset or output parameter")
            sys.exit(1)

        solver = InteractiveSolver(args.output)
        solver.initialize(args.mode, args.romFileName, args.presetFileName, magic=args.raceMagic, debug=args.vcr, fill=args.fill)
    else:
        # iterate
        params = {}
        if args.scope == 'common':
            if args.action == "save":
                params["lock"] = args.lock
            elif args.action == "randomize":
                params["progressionSpeed"] = args.progressionSpeed
                params["minorQty"] = args.minorQty
                params["energyQty"] = args.energyQty
        elif args.scope == 'item':
            if args.state == None or args.action == None or args.output == None:
                print("Missing state/action/output parameter")
                sys.exit(1)
            if args.action in ["add", "replace"]:
                if args.loc == None:
                    print("Missing loc parameter when using action add for item")
                    sys.exit(1)
                if args.mode != 'standard':
                    if args.item == None:
                        print("Missing item parameter when using action add in plando/suitless mode")
                        sys.exit(1)
                params = {'loc': args.loc, 'item': args.item}
            elif args.action == "remove":
                params = {'count': args.count}
        elif args.scope == 'area':
            if args.state == None or args.action == None or args.output == None:
                print("Missing state/action/output parameter")
                sys.exit(1)
            if args.action == "add":
                if args.startPoint == None or args.endPoint == None:
                    print("Missing start or end point parameter when using action add for item")
                    sys.exit(1)
                params = {'startPoint': args.startPoint, 'endPoint': args.endPoint}
        params["debug"] = args.vcr

        solver = InteractiveSolver(args.output)
        solver.iterate(args.state, args.scope, args.action, params)

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
                            displayGeneratedPath=args.displayGeneratedPath,
                            outputFileName=args.output, magic=args.raceMagic,
                            checkDuplicateMajor=args.checkDuplicateMajor, vcr=args.vcr)

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
    parser.add_argument('--checkDuplicateMajor', dest="checkDuplicateMajor", action='store_true',
                        help="print a warning if the same major is collected more than once")
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--firstItemsLog', '-1',
                        help="path to file where for each item type the first time it was found and where will be written (spoilers!)",
                        nargs='?', default=None, type=str, dest='firstItemsLog')
    parser.add_argument('--ext_stats', help="Generate extended stats",
                        nargs='?', default=None, dest='extStatsFilename')
    parser.add_argument('--displayGeneratedPath', '-g', help="display the generated path (spoilers!)",
                        dest='displayGeneratedPath', action='store_true')
    parser.add_argument('--race', help="Race mode magic number", dest='raceMagic', type=int)
    parser.add_argument('--vcr', help="Generate VCR output file (in isolver it means debug mode: load all the transitions/add path info for locs)", dest='vcr', action='store_true')
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
                        dest="action", nargs="?", default=None, choices=['init', 'add', 'remove', 'clear', 'get', 'save', 'replace', 'randomize'])
    parser.add_argument('--item', help="Name of the item to place in plando mode (used in interactive mode)",
                        dest="item", nargs='?', default=None)
    parser.add_argument('--startPoint', help="The start AP to connect (used in interactive mode)",
                        dest="startPoint", nargs='?', default=None)
    parser.add_argument('--endPoint', help="The destination AP to connect (used in interactive mode)",
                        dest="endPoint", nargs='?', default=None)

    parser.add_argument('--mode', help="Solver mode: standard/seedless/plando (used in interactive mode)",
                        dest="mode", nargs="?", default=None, choices=['standard', 'seedless', 'plando'])
    parser.add_argument('--scope', help="Scope for the action: common/area/item (used in interactive mode)",
                        dest="scope", nargs="?", default=None, choices=['common', 'area', 'item'])
    parser.add_argument('--count', help="Number of item rollback (used in interactive mode)",
                        dest="count", type=int)
    parser.add_argument('--lock', help="lock the plando seed (used in interactive mode)",
                        dest="lock", action='store_true')
    parser.add_argument('--fill', help="in plando load all the source seed locations/transitions as a base (used in interactive mode)",
                        dest="fill", action='store_true')
    parser.add_argument('--progressionSpeed', help="rando plando (used in interactive mode)",
                        dest="progressionSpeed", nargs="?", default=None, choices=["slowest", "slow", "medium", "fast", "fastest", "basic", "VARIAble"])
    parser.add_argument('--minorQty', help="rando plando  (used in interactive mode)",
                        dest="minorQty", nargs="?", default=None, choices=[str(i) for i in range(0,101)])
    parser.add_argument('--energyQty', help="rando plando  (used in interactive mode)",
                        dest="energyQty", nargs="?", default=None, choices=["sparse", "medium", "vanilla"])

    args = parser.parse_args()

    if args.presetFileName is None:
        args.presetFileName = 'standard_presets/regular.json'

    if args.raceMagic != None:
        if args.raceMagic <= 0 or args.raceMagic >= 0x10000:
            print "Invalid magic"
            sys.exit(-1)

    if args.count != None:
        if args.count < 1 or args.count > 0x80:
            print "Invalid count"
            sys.exit(-1)

    log.init(args.debug)

    if args.interactive == True:
        interactiveSolver(args)
    else:
        standardSolver(args)
