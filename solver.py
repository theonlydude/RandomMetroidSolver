#!/usr/bin/python3

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
from rom_patches import RomPatches
from rando.Items import ItemManager
from graph_locations import locations as graphLocations
from graph import AccessGraph
from graph_access import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, accessPoints, GraphUtils, getAccessPoint
from utils import PresetLoader, removeChars
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
        # bool
        self.state["escapeRando"] = solver.escapeRando
        # string "03:00"
        self.state["escapeTimer"] = solver.escapeTimer
        # list of active patches
        self.state["patches"] = RomPatches.ActivePatches
        # start ap
        self.state["startAP"] = solver.startAP
        # start area
        self.state["startArea"] = solver.startArea
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
        self.state["lastAP"] = solver.lastAP
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
        solver.escapeRando = self.state["escapeRando"]
        solver.escapeTimer = self.state["escapeTimer"]
        RomPatches.ActivePatches = self.state["patches"]
        solver.startAP = self.state["startAP"]
        solver.startArea = self.state["startArea"]
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
        solver.lastAP = self.state["lastAP"]
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
            ret[loc["Name"]] = {"index": i,
                                "difficulty": (diff.bool, diff.difficulty, diff.knows, diff.items),
                                "Visibility": loc["Visibility"]}
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
                if "Visibility" in visitedLocations[loc["Name"]]:
                    loc["Visibility"] = visitedLocations[loc["Name"]]["Visibility"]
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
        return removeChars(locName, " ,()-")

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
        return transition[0].lower() + removeChars(transition[1:], " ,()-")

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
                                "name": loc["Name"],
                                "canHidden": loc["CanHidden"],
                                "visibility": loc["Visibility"]}
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
                                "items": [],
                                "canHidden": loc["CanHidden"],
                                "visibility": loc["Visibility"]}
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
    def loadRom(self, rom, interactive=False, magic=None, startAP=None):
        # startAP param is only use for seedless
        if rom == None:
            self.romFileName = 'seedless'
            self.majorsSplit = 'Full'
            self.areaRando = True
            self.bossRando = True
            self.escapeRando = False
            self.escapeTimer = "03:00"
            self.startAP = startAP
            RomPatches.setDefaultPatches(startAP)
            self.startArea = getAccessPoint(startAP).Start['solveArea']
            # in seedless load all the vanilla transitions
            self.areaTransitions = vanillaTransitions[:]
            self.bossTransitions = vanillaBossesTransitions[:]
            self.escapeTransition = [vanillaEscapeTransitions[0]]
            self.curGraphTransitions = self.bossTransitions + self.areaTransitions + self.escapeTransition
            for loc in self.locations:
                loc['itemName'] = 'Nothing'
        else:
            self.romFileName = rom
            self.romLoader = RomLoader.factory(rom, magic)
            self.romLoader.readNothingId()
            self.majorsSplit = self.romLoader.assignItems(self.locations)
            (self.startAP, self.startArea, startPatches) = self.romLoader.getStartAP()
            (self.areaRando, self.bossRando, self.escapeRando) = self.romLoader.loadPatches()
            RomPatches.ActivePatches += startPatches
            self.escapeTimer = self.romLoader.getEscapeTimer()

            if interactive == False:
                print("ROM {} majors: {} area: {} boss: {} escape: {} patches: {} activePatches: {}".format(rom, self.majorsSplit, self.areaRando, self.bossRando, self.escapeRando, sorted(self.romLoader.getPatches()), sorted(RomPatches.ActivePatches)))
            else:
                print("majors: {} area: {} boss: {} escape: {} activepatches: {}".format(self.majorsSplit, self.areaRando, self.bossRando, self.escapeRando, sorted(RomPatches.ActivePatches)))

            (self.areaTransitions, self.bossTransitions, self.escapeTransition) = self.romLoader.getTransitions()
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
                if self.escapeRando == False:
                    self.curGraphTransitions += self.escapeTransition
            else:
                self.curGraphTransitions = self.bossTransitions + self.areaTransitions + self.escapeTransition

        self.areaGraph = AccessGraph(accessPoints, self.curGraphTransitions)

        # store at each step how many locations are available
        self.nbAvailLocs = []

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

    def computeLocationsDifficulty(self, locations, phase="major"):
        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.lastAP)
        # check post available functions too
        for loc in locations:
            if loc['difficulty'].bool == True:
                if 'PostAvailable' in loc:
                    self.smbm.addItem(loc['itemName'])
                    postAvailable = loc['PostAvailable'](self.smbm)
                    self.smbm.removeItem(loc['itemName'])

                    loc['difficulty'] = self.smbm.wand(loc['difficulty'], postAvailable)

                # also check if we can come back to landing site from the location
                loc['comeBack'] = self.areaGraph.canAccess(self.smbm, loc['accessPoint'], self.lastAP, infinity, loc['itemName'])

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("available {} locs:".format(phase))
            for loc in locations:
                if loc['difficulty'].bool == True:
                    print("{:>48}: {:>8}".format(loc['Name'], round(loc['difficulty'].difficulty, 2)))

    def collectMajor(self, loc, itemName=None):
        self.majorLocations.remove(loc)
        self.visitedLocations.append(loc)
        self.collectItem(loc, itemName)

    def collectMinor(self, loc):
        self.minorLocations.remove(loc)
        self.visitedLocations.append(loc)
        self.collectItem(loc)

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

        if self.log.getEffectiveLevel() == logging.DEBUG:
            print("---------------------------------------------------------------")
            print("collectItem: {:<16} at {:<48}".format(item, loc['Name']))
            print("---------------------------------------------------------------")

        # last loc is used as root node for the graph
        self.lastAP = loc['accessPoint']
        self.lastArea = loc['SolveArea']

    def cancelLastItems(self, count):
        if self.vcr != None:
            self.vcr.addRollback(count)

        if self.interactive == False:
            self.nbAvailLocs = self.nbAvailLocs[:-count]

        for _ in range(count):
            if len(self.visitedLocations) == 0:
                return

            loc = self.visitedLocations.pop()
            if self.majorsSplit == 'Full':
                self.majorLocations.append(loc)
            else:
                if self.majorsSplit in loc['Class'] or 'Boss' in loc['Class']:
                    self.majorLocations.append(loc)
                else:
                    self.minorLocations.append(loc)

            # pickup func
            if 'Unpickup' in loc:
                loc['Unpickup']()

            # access point
            if len(self.visitedLocations) == 0:
                self.lastAP = self.startAP
                self.lastArea = self.startArea
            else:
                self.lastAP = self.visitedLocations[-1]["accessPoint"]
                self.lastArea = self.visitedLocations[-1]["SolveArea"]

            # delete location params which are set when the location is available
            if 'difficulty' in loc:
                del loc['difficulty']
            if 'distance' in loc:
                del loc['distance']
            if 'accessPoint' in loc:
                del loc['accessPoint']
            if 'path' in loc:
                del loc['path']

            # item
            item = loc["itemName"]
            if item != self.collectedItems[-1]:
                raise Exception("Item of last collected loc {}: {} is different from last collected item: {}".format(loc["Name"], item, self.collectedItems[-1]))

            # in plando we have to remove the last added item,
            # else it could be used in computing the postAvailable of a location
            if self.mode in ['plando', 'seedless']:
                loc["itemName"] = 'Nothing'

            self.collectedItems.pop()

            # if multiple majors in plando mode, remove it from smbm only when it's the last occurence of it
            if self.smbm.isCountItem(item):
                self.smbm.removeItem(item)
            else:
                if item not in self.collectedItems:
                    self.smbm.removeItem(item)

    def printLocs(self, locs, phase):
        if len(locs) > 0:
            print("{}:".format(phase))
            print('{:>48} {:>12} {:>8} {:>8} {:>34} {:>10}'.format("Location Name", "Difficulty", "Distance", "ComeBack", "SolveArea", "AreaWeight"))
            for loc in locs:
                print('{:>48} {:>12} {:>8} {:>8} {:>34} {:>10}'.
                      format(loc['Name'], round(loc['difficulty'][1], 2), round(loc['distance'], 2),
                             loc['comeBack'], loc['SolveArea'], loc['areaWeight'] if 'areaWeight' in loc else -1))

    def getAvailableItemsList(self, locations, threshold):
        # locations without distance are not available
        locations = [loc for loc in locations if 'distance' in loc]

        if len(locations) == 0:
            return []

        # add nocomeback locations which has been selected by the comeback step (areaWeight == 1)
        around = [loc for loc in locations if( ('areaWeight' in loc and loc['areaWeight'] == 1)
                                               or ((loc['SolveArea'] == self.lastArea or loc['distance'] < 3)
                                                   and loc['difficulty'].difficulty <= threshold
                                                   and not Bosses.areaBossDead(self.lastArea)
                                                   and 'comeBack' in loc and loc['comeBack'] == True) )]
        outside = [loc for loc in locations if not loc in around]

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.printLocs(around, "around1")
            self.printLocs(outside, "outside1")

        around.sort(key=lambda loc: (
            # locs in the same area
            0 if loc['SolveArea'] == self.lastArea
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

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.printLocs(around, "around2")

        # we want to sort the outside locations by putting the ones in the same area first,
        # then we sort the remaining areas starting whith boss dead status.
        # we also want to sort by range of difficulty and not only with the difficulty threshold.
        ranged = {
            "areaWeight": [],
            "easy": [],
            "medium": [],
            "hard": [],
            "harder": [],
            "hardcore": [],
            "mania": [],
            "noComeBack": []
        }
        for loc in outside:
            if "areaWeight" in loc:
                ranged["areaWeight"].append(loc)
            elif "comeBack" not in loc or loc['comeBack'] == False:
                ranged["noComeBack"].append(loc)
            else:
                difficulty = loc['difficulty'].difficulty
                if difficulty < medium:
                    ranged["easy"].append(loc)
                elif difficulty < hard:
                    ranged["medium"].append(loc)
                elif difficulty < harder:
                    ranged["hard"].append(loc)
                elif difficulty < hardcore:
                    ranged["harder"].append(loc)
                elif difficulty < mania:
                    ranged["hardcore"].append(loc)
                else:
                    ranged["mania"].append(loc)

        for key in ranged:
            ranged[key].sort(key=lambda loc: (
                # first locs in the same area
                0 if loc['SolveArea'] == self.lastArea else 1,
                # first nearest locs
                loc['distance'],
                # beating a boss
                loc['difficulty'].difficulty if (not Bosses.areaBossDead(loc['Area'])
                                                 and 'Pickup' in loc)
                else 100000,
                # areas with boss still alive
                loc['difficulty'].difficulty if (not Bosses.areaBossDead(loc['Area']))
                else 100000,
                loc['difficulty'].difficulty))


        if self.log.getEffectiveLevel() == logging.DEBUG:
            for key in ["areaWeight", "easy", "medium", "hard", "harder", "hardcore", "mania", "noComeBack"]:
                self.printLocs(ranged[key], "outside2:{}".format(key))

        outside = []
        for key in ["areaWeight", "easy", "medium", "hard", "harder", "hardcore", "mania", "noComeBack"]:
            outside += ranged[key]

        return around + outside

    def nextDecision(self, majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold):
        # first take major items of acceptable difficulty in the current area
        if (len(majorsAvailable) > 0
            and majorsAvailable[0]['SolveArea'] == self.lastArea
            and majorsAvailable[0]['difficulty'].difficulty <= diffThreshold
            and majorsAvailable[0]['comeBack'] == True):
            return self.collectMajor(majorsAvailable.pop(0))
        # next item decision
        elif len(minorsAvailable) == 0 and len(majorsAvailable) > 0:
            self.log.debug('MAJOR')
            return self.collectMajor(majorsAvailable.pop(0))
        elif len(majorsAvailable) == 0 and len(minorsAvailable) > 0:
            # we don't check for hasEnoughMinors here, because we would be stuck, so pickup
            # what we can and hope it gets better
            self.log.debug('MINOR')
            return self.collectMinor(minorsAvailable.pop(0))
        elif len(majorsAvailable) > 0 and len(minorsAvailable) > 0:
            self.log.debug('BOTH|M={}, m={}'.format(majorsAvailable[0]['Name'], minorsAvailable[0]['Name']))
            # if both are available, decide based on area, difficulty and comeBack
            nextMajDifficulty = majorsAvailable[0]['difficulty'].difficulty
            nextMinDifficulty = minorsAvailable[0]['difficulty'].difficulty
            nextMajArea = majorsAvailable[0]['SolveArea']
            nextMinArea = minorsAvailable[0]['SolveArea']
            nextMajComeBack = majorsAvailable[0]['comeBack']
            nextMinComeBack = minorsAvailable[0]['comeBack']
            nextMajDistance = majorsAvailable[0]['distance']
            nextMinDistance = minorsAvailable[0]['distance']
            nextMajAreaWeight = majorsAvailable[0]['areaWeight'] if "areaWeight" in majorsAvailable[0] else 10000
            nextMinAreaWeight = minorsAvailable[0]['areaWeight'] if "areaWeight" in minorsAvailable[0] else 10000

            if self.log.getEffectiveLevel() == logging.DEBUG:
                print("     : {:>4} {:>32} {:>4} {:>4} {:>6}".format("diff", "area", "back", "dist", "weight"))
                print("major: {:>4} {:>32} {:>4} {:>4} {:>6}".format(round(nextMajDifficulty, 2), nextMajArea, nextMajComeBack, round(nextMajDistance, 2), nextMajAreaWeight))
                print("minor: {:>4} {:>32} {:>4} {:>4} {:>6}".format(round(nextMinDifficulty, 2), nextMinArea, nextMinComeBack, round(nextMinDistance, 2), nextMinAreaWeight))

            if hasEnoughMinors == True and self.haveAllMinorTypes() == True and self.smbm.haveItem('Charge'):
                # we have charge, no longer need minors
                self.log.debug("we have charge, no longer need minors, take major")
                return self.collectMajor(majorsAvailable.pop(0))
            else:
                # first take item from loc where you can come back
                if nextMajComeBack != nextMinComeBack:
                    self.log.debug("maj/min != combeback")
                    if nextMajComeBack == True:
                        return self.collectMajor(majorsAvailable.pop(0))
                    else:
                        return self.collectMinor(minorsAvailable.pop(0))
                # respect areaweight first
                elif nextMajAreaWeight != nextMinAreaWeight:
                    self.log.debug("maj/min != area weight")
                    if nextMajAreaWeight < nextMinAreaWeight:
                        return self.collectMajor(majorsAvailable.pop(0))
                    else:
                        return self.collectMinor(minorsAvailable.pop(0))
                # difficulty over area (this is a difficulty estimator, not a speedrunning simulator)
                elif nextMinDifficulty <= diffThreshold and nextMajDifficulty <= diffThreshold:
                    # take the closer one
                    if nextMajDistance != nextMinDistance:
                        self.log.debug("!= distance and <= diffThreshold")
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
                # if not all the minors type are collected, start with minors
                elif nextMinDifficulty <= diffThreshold and not self.haveAllMinorTypes():
                    self.log.debug("not all minors types")
                    return self.collectMinor(minorsAvailable.pop(0))
                elif nextMinArea == self.lastArea and nextMinDifficulty <= diffThreshold:
                    self.log.debug("not enough minors")
                    return self.collectMinor(minorsAvailable.pop(0))
                elif nextMinDifficulty > diffThreshold and nextMajDifficulty > diffThreshold:
                    # take the easier
                    if nextMinDifficulty < nextMajDifficulty:
                        self.log.debug("min easier and not enough minors")
                        return self.collectMinor(minorsAvailable.pop(0))
                    elif nextMajDifficulty < nextMinDifficulty:
                        self.log.debug("maj easier")
                        return self.collectMajor(majorsAvailable.pop(0))
                    # take the closer one
                    elif nextMajDistance != nextMinDistance:
                        self.log.debug("!= distance and > diffThreshold")
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

        self.log.debug("{}: available major: {}, available minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        isEndPossible = False
        endDifficulty = mania
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

            self.log.debug("Current AP/Area: {}/{}".format(self.lastAP, self.lastArea))

            # compute the difficulty of all the locations
            self.computeLocationsDifficulty(self.majorLocations)
            if self.majorsSplit != 'Full':
                self.computeLocationsDifficulty(self.minorLocations, phase="minor")

            # keep only the available locations
            majorsAvailable = [loc for loc in self.majorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]
            minorsAvailable = [loc for loc in self.minorLocations if 'difficulty' in loc and loc["difficulty"].bool == True]

            if self.majorsSplit == 'Full':
                locs = majorsAvailable
            else:
                locs = majorsAvailable+minorsAvailable

            self.nbAvailLocs.append(len(locs))

            # check if we're stuck
            if len(majorsAvailable) == 0 and len(minorsAvailable) == 0:
                if not isEndPossible:
                    self.log.debug("STUCK MAJORS and MINORS")
                    if self.comeBack.rewind(len(self.collectedItems)) == True:
                        continue
                    else:
                        # we're really stucked
                        self.log.debug("STUCK CAN'T REWIND")
                        break
                else:
                    self.log.debug("HARD END 2")
                    self.checkMB(mbLoc)
                    break

            # handle no comeback locations
            rewindRequired = self.comeBack.handleNoComeBack(locs, len(self.collectedItems))
            if rewindRequired == True:
                if self.comeBack.rewind(len(self.collectedItems)) == True:
                    continue
                else:
                    # we're really stucked
                    self.log.debug("STUCK CAN'T REWIND")
                    break

            # sort them on difficulty and proximity
            self.log.debug("getAvailableItemsList majors")
            majorsAvailable = self.getAvailableItemsList(majorsAvailable, diffThreshold)
            if self.majorsSplit == 'Full':
                minorsAvailable = majorsAvailable
            else:
                self.log.debug("getAvailableItemsList minors")
                minorsAvailable = self.getAvailableItemsList(minorsAvailable, diffThreshold)

            # choose one to pick up
            self.nextDecision(majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold)

            self.comeBack.cleanNoComeBack(locs)

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
        self.interactive = True
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
        for (startPoint, endPoint) in vanillaTransitions + vanillaBossesTransitions + vanillaEscapeTransitions:
            for point in [startPoint, endPoint]:
                web2Internal[self.apNameInternal2Web(point)] = point
        return web2Internal

    def dumpState(self):
        state = SolverState(self.debug)
        state.fromSolver(self)
        state.toJson(self.outputFileName)

    def initialize(self, mode, rom, presetFileName, magic, debug, fill, startAP):
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

        self.loadRom(rom, interactive=True, magic=magic, startAP=startAP)
        if self.mode == 'plando':
            # in plando always consider that we're doing full
            self.majorsSplit = 'Full'

        self.clearItems()

        # in debug mode don't load plando locs/transitions
        if self.mode == 'plando' and self.debug == False:
            if fill == True:
                # load the source seed transitions and items/locations
                self.curGraphTransitions = self.bossTransitions + self.areaTransitions + self.escapeTransition
                self.areaGraph = AccessGraph(accessPoints, self.curGraphTransitions)
                self.fillPlandoLocs()
            else:
                if self.areaRando == True or self.bossRando == True:
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

        self.loadPreset(self.presetFileName)

        # add already collected items to smbm
        self.smbm.addItems(self.collectedItems)

        if scope == 'item':
            if action == 'clear':
                self.clearItems(True)
            else:
                if action == 'add':
                    if self.mode == 'plando' or self.mode == 'seedless':
                        if params['loc'] != None:
                            if self.mode == 'plando':
                                self.setItemAt(params['loc'], params['item'], params['hide'])
                            else:
                                self.setItemAt(params['loc'], 'Nothing', False)
                        else:
                            self.increaseItem(params['item'])
                    else:
                        # pickup item at locName
                        self.pickItemAt(params['loc'])
                elif action == 'remove':
                    if 'count' in params:
                        # remove last collected item
                        self.cancelLastItems(params['count'])
                    else:
                        self.decreaseItem(params['item'])
                elif action == 'replace':
                    self.replaceItemAt(params['loc'], params['item'], params['hide'])
                elif action == 'toggle':
                    self.toggleItem(params['item'])
        elif scope == 'area':
            if action == 'clear':
                self.clearTransitions()
            else:
                if action == 'add':
                    startPoint = params['startPoint']
                    endPoint = params['endPoint']
                    self.addTransition(self.transWeb2Internal[startPoint], self.transWeb2Internal[endPoint])
                elif action == 'remove':
                    if 'startPoint' in params:
                        self.cancelTransition(self.transWeb2Internal[params['startPoint']])
                    else:
                        # remove last transition
                        self.cancelLastTransition()

        self.areaGraph = AccessGraph(accessPoints, self.curGraphTransitions)

        if scope == 'common':
            if action == 'save':
                return self.savePlando(params['lock'], params['escapeTimer'])
            elif action == 'randomize':
                self.randoPlando(params)

        # if last loc added was a sequence break, recompute its difficulty,
        # as it may be available with the newly placed item.
        if len(self.visitedLocations) > 0:
            lastVisited = self.visitedLocations[-1]
            if lastVisited['difficulty'].difficulty == -1:
                self.visitedLocations.remove(lastVisited)
                self.majorLocations.append(lastVisited)
            else:
                lastVisited = None
        else:
            lastVisited = None

        # compute new available locations
        self.clearLocs(self.majorLocations)
        self.computeLocationsDifficulty(self.majorLocations)

        # put back last visited location
        if lastVisited != None:
            self.majorLocations.remove(lastVisited)
            self.visitedLocations.append(lastVisited)
            if lastVisited["difficulty"] == False:
                # if the loc is still sequence break, put it back as sequence break
                lastVisited["difficulty"] = SMBool(True, -1)

        # return them
        self.dumpState()

    def getLocNameFromAddress(self, address):
        return self.locsAddressName[address]

    def loadPlandoTransitions(self):
        # add escape transition
        transitionsAddr = self.romLoader.getPlandoTransitions(len(vanillaBossesTransitions) + len(vanillaTransitions) + 1)
        return GraphUtils.getTransitions(transitionsAddr)

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
        mbLoc = self.getLoc("Mother Brain")
        locationsBck = self.locations[:]

        self.lastAP = self.startAP
        self.lastArea = self.startArea
        (self.difficulty, self.itemsOk) = self.computeDifficulty()

        # put back mother brain location
        if mbLoc not in self.majorLocations and mbLoc not in self.visitedLocations:
            self.majorLocations.append(mbLoc)

        if self.itemsOk == False:
            # add remaining locs as sequence break
            for loc in self.majorLocations[:]:
                loc["difficulty"] = SMBool(True, -1)
                if "accessPoint" not in loc:
                    # take first ap of the loc
                    loc["accessPoint"] = list(loc["AccessFrom"])[0]
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
            if ap.isInternal() == True:
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

        plandoCurrent = {
            "locsItems": plandoLocsItems,
            "transitions": self.curGraphTransitions,
            "patches": RomPatches.ActivePatches
        }

        plandoCurrentJson = json.dumps(plandoCurrent)

        pythonExec = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)
        params = [
            pythonExec,  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
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

    def savePlando(self, lock, escapeTimer):
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
        patches = ['credits_varia.ips', 'tracking.ips', "Escape_Animals_Disable"]
        if magic != None:
            patches.insert(0, 'race_mode.ips')
            patches.append('race_mode_credits.ips')
        romPatcher.addIPSPatches(patches)
        romPatcher.setNothingId(self.startAP, itemLocs)
        romPatcher.writeItemsLocs(itemLocs)
        romPatcher.writeItemsNumber()
        romPatcher.writeSpoiler(itemLocs)
        romPatcher.writeNothingId()
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
        if self.areaRando == True or self.bossRando == True or self.escapeRando == True:
            doors = GraphUtils.getDoorConnections(self.fillGraph(), self.areaRando, self.bossRando, self.escapeRando, False)
            romPatcher.writeDoorConnections(doors)
            if magic == None:
                doorsPtrs = GraphUtils.getAps2DoorsPtrs()
                romPatcher.writePlandoTransitions(self.curGraphTransitions, doorsPtrs,
                                                  len(vanillaBossesTransitions) + len(vanillaTransitions))
            if self.escapeRando == True and escapeTimer != None:
                # convert from '03:00' to number of seconds
                escapeTimer = int(escapeTimer[0:2]) * 60 + int(escapeTimer[3:5])
                romPatcher.applyEscapeAttributes({'Timer': escapeTimer, 'Animals': None}, [])

        romPatcher.commitIPS()
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
        return removeChars(locName, " ,()-")

    def locNameWeb2Internal(self, locNameWeb):
        return self.locsWeb2Internal[locNameWeb]

    def apNameInternal2Web(self, apName):
        return apName[0].lower() + removeChars(apName[1:], " ")

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
            loc["accessPoint"] = list(loc["AccessFrom"])[0]
        self.collectMajor(loc)

    def setItemAt(self, locName, itemName, hide):
        # set itemName at locName

        loc = self.getWebLoc(locName)
        # plando mode
        loc["itemName"] = itemName

        if "difficulty" not in loc:
            # sequence break
            loc["difficulty"] = SMBool(True, -1)
        if "accessPoint" not in loc:
            # take first ap of the loc
            loc["accessPoint"] = list(loc["AccessFrom"])[0]

        if hide == True:
            loc["Visibility"] = 'Hidden'

        self.collectMajor(loc, itemName)

    def replaceItemAt(self, locName, itemName, hide):
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

        if hide == True:
            loc["Visibility"] = 'Hidden'
        elif loc['CanHidden'] == True and loc['Visibility'] == 'Hidden':
            # the loc was previously hidden, set it back to visible
            loc["Visibility"] = 'Visible'

        self.smbm.addItem(itemName)

    def increaseItem(self, item):
        # add item at begining of collectedItems to not mess with item removal when cancelling a location
        self.collectedItems.insert(0, item)
        self.smbm.addItem(item)

    def decreaseItem(self, item):
        if item in self.collectedItems:
            self.collectedItems.remove(item)
            self.smbm.removeItem(item)

    def toggleItem(self, item):
        # add or remove a major item
        if item in self.collectedItems:
            self.collectedItems.remove(item)
            self.smbm.removeItem(item)
        else:
            self.collectedItems.insert(0, item)
            self.smbm.addItem(item)

    def clearItems(self, reload=False):
        self.collectedItems = []
        self.visitedLocations = []
        self.lastAP = self.startAP
        self.lastArea = self.startArea
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

    def cancelTransition(self, startPoint):
        # get end point
        endPoint = None
        for (i, (start, end)) in enumerate(self.curGraphTransitions):
            if start == startPoint:
                endPoint = end
                break
            elif end == startPoint:
                endPoint = start
                break

        if endPoint == None:
            # shouldn't happen
            return

        # check that transition is cancelable
        if self.areaRando == True and self.bossRando == True:
            if len(self.curGraphTransitions) == 0:
                return
        elif self.areaRando == True:
            if len(self.curGraphTransitions) == len(self.bossTransitions):
                return
            elif [startPoint, endPoint] in self.bossTransitions or [endPoint, startPoint] in self.bossTransitions:
                return
        elif self.bossRando == True:
            if len(self.curGraphTransitions) == len(self.areaTransitions):
                return
            elif [startPoint, endPoint] in self.areaTransitions or [endPoint, startPoint] in self.areaTransitions:
                return

        # remove transition
        self.curGraphTransitions.pop(i)

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
                 firstItemsLog=None, extStatsFilename=None, extStatsStep=None, displayGeneratedPath=False,
                 outputFileName=None, magic=None, checkDuplicateMajor=False, vcr=False, plot=None):
        self.interactive = False
        self.checkDuplicateMajor = checkDuplicateMajor
        self.vcr = VCR(rom, 'solver') if vcr == True else None
        # for compatibility with some common methods of the interactive solver
        self.mode = 'standard'

        self.log = log.get('Solver')

        self.setConf(difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath)

        self.firstLogFile = None
        if firstItemsLog is not None:
            self.firstLogFile = open(firstItemsLog, 'w')
            self.firstLogFile.write('Item;Location;Area\n')

        self.extStatsFilename = extStatsFilename
        self.extStatsStep = extStatsStep
        self.plot = plot

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
        self.lastAP = self.startAP
        self.lastArea = self.startArea

        (self.difficulty, self.itemsOk) = self.computeDifficulty()
        if self.firstLogFile is not None:
            self.firstLogFile.close()

        (self.knowsUsed, self.knowsKnown, knowsUsedList) = self.getKnowsUsed()

        if self.vcr != None:
            self.vcr.dump()

        self.computeExtStats()

        if self.extStatsFilename != None:
            with open(self.extStatsFilename, 'a') as extStatsFile:
                db.DB.dumpExtStatsSolver(self.difficulty, knowsUsedList, self.solverStats, self.extStatsStep, extStatsFile)

        if self.plot != None:
            with open(self.plot, 'w') as outDataFile:
                for (i, number) in enumerate(self.nbAvailLocs):
                    outDataFile.write("{} {}\n".format(i, number))

        self.output.out()

    def computeExtStats(self):
        # avgLocs: avg number of available locs, the higher the value the more open is a seed
        # open[1-4]4: how many location you have to visit to open 1/4, 1/2, 3/4, all locations.
        #             gives intel about prog item repartition.
        self.solverStats = {}
        self.solverStats['avgLocs'] = int(sum(self.nbAvailLocs)/len(self.nbAvailLocs))

        derivative = []
        for i in range(len(self.nbAvailLocs)-1):
            d = self.nbAvailLocs[i+1] - self.nbAvailLocs[i]
            derivative.append(d)

        sumD = sum([d for d in derivative if d != -1])
        (sum14, sum24, sum34, sum44) = (sumD/4, sumD/2, sumD*3/4, sumD)
        (open14, open24, open34, open44) = (-1, -1, -1, -1)

        sumD = 0
        for (i, d) in enumerate(derivative, 1):
            if d == -1:
                continue
            sumD += d
            if sumD >= sum14 and open14 == -1:
                open14 = i
                continue
            if sumD >= sum24 and open24 == -1:
                open24 = i
                continue
            if sumD >= sum34 and open34 == -1:
                open34 = i
                continue
            if sumD >= sum44 and open44 == -1:
                open44 = i
                break

        self.solverStats['open14'] = open14
        self.solverStats['open24'] = open24
        self.solverStats['open34'] = open34
        self.solverStats['open44'] = open44

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
        knowsKnownCount = len([knows for  knows in Knows.__dict__ if isKnows(knows) and getattr(Knows, knows).bool == True])
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

        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.lastAP)

        return [loc for loc in locations if loc['difficulty'].bool == True]

class ComeBack(object):
    # object to handle the decision to choose the next area when all locations have the "no comeback" flag.
    # handle rewinding to try the next area in case of a stuck.
    # one ComebackStep object is created each time we have to use the no comeback heuristic, used for rewinding.
    def __init__(self, solver):
        self.comeBackSteps = []
        # used to rewind
        self.solver = solver
        self.log = log.get('Rewind')

    def handleNoComeBack(self, locations, cur):
        hasEnoughMinors = self.solver.pickup.enoughMinors(self.solver.smbm, self.solver.minorLocations)
        hasAllMinorTypes = self.solver.haveAllMinorTypes()
        hasCharge = self.solver.smbm.haveItem('Charge')
        noNeedMinors = hasEnoughMinors and hasAllMinorTypes and hasCharge

        # return True if a rewind is needed. choose the next area to use
        solveAreas = {}
        locsCount = 0
        for loc in locations:
            # filter minors locations when the solver no longer collect minors
            if (self.solver.majorsSplit != 'Full'
                and self.solver.majorsSplit not in loc['Class']
                and 'Boss' not in loc['Class']
                and noNeedMinors == True):
                continue
            if "comeBack" not in loc:
                return False
            if loc["comeBack"] == True:
                return False
            locsCount += 1
            if loc["SolveArea"] in solveAreas:
                solveAreas[loc["SolveArea"]] += 1
            else:
                solveAreas[loc["SolveArea"]] = 1

        # only minors locations, or just one major, no need for a rewind step
        if locsCount < 2:
            return False

        self.log.debug("WARNING: use no come back heuristic for {} locs in {} solve areas ({})".format(locsCount, len(solveAreas), solveAreas))

        # check if we can use an existing step
        if len(self.comeBackSteps) > 0:
            lastStep = self.comeBackSteps[-1]
            if lastStep.cur == cur:
                self.log.debug("Use last step at {}".format(cur))
                return lastStep.next(locations)
            else:
                self.log.debug("cur: {}, lastStep.cur: {}, don't use lastStep.next()".format(cur, lastStep.cur))

        if len(solveAreas) == 1:
            self.log.debug("handleNoComeBack: only one solve area")
            return False

        # create a step
        self.log.debug("Create new step at {}".format(cur))
        lastStep = ComeBackStep(solveAreas, cur)
        self.comeBackSteps.append(lastStep)
        return lastStep.next(locations)

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

        while len(self.comeBackSteps) > 0:
            lastStep = self.comeBackSteps[-1]
            if not lastStep.moreAvailable():
                self.log.debug("last step has been fully visited, go up one more time")
                self.comeBackSteps.pop()

                if len(self.comeBackSteps) == 0:
                    self.log.debug("No more steps to rewind")
                    return False

                self.log.debug("Rewind to previous step at {}".format(self.comeBackSteps[-1].cur))
            else:
                break

        count = cur - lastStep.cur
        if count == 0:
            self.log.debug("Can't rewind, it's buggy here !")
            return False
        self.solver.cancelLastItems(count)
        self.log.debug("Rewind {} items to {}".format(count, lastStep.cur))
        return True

class ComeBackStep(object):
    # one case of no come back decision
    def __init__(self, solveAreas, cur):
        self.visitedSolveAreas = []
        self.solveAreas = solveAreas
        self.cur = cur
        self.log = log.get('RewindStep')
        self.log.debug("create rewind step: {} {}".format(cur, solveAreas))

    def moreAvailable(self):
        self.log.debug("moreAvailable: cur: {} len(visited): {} len(areas): {}".format(self.cur, len(self.visitedSolveAreas), len(self.solveAreas)))
        return len(self.visitedSolveAreas) < len(self.solveAreas)

    def next(self, locations):
        # use next available area, if all areas have been visited return True (stuck), else False
        if not self.moreAvailable():
            self.log.debug("rewind: all areas have been visited, stuck")
            return True

        self.log.debug("rewind next, solveAreas: {} visitedSolveAreas: {}".format(self.solveAreas, self.visitedSolveAreas))

        # get area with max available locs
        maxAreaWeigth = 0
        maxAreaName = ""
        for solveArea in sorted(self.solveAreas):
            if solveArea in self.visitedSolveAreas:
                continue
            else:
                if self.solveAreas[solveArea] > maxAreaWeigth:
                    maxAreaWeigth = self.solveAreas[solveArea]
                    maxAreaName = solveArea
        self.visitedSolveAreas.append(maxAreaName)
        self.log.debug("rewind next area: {}".format(maxAreaName))

        outWeight = 10000
        retSolveAreas = {}
        for solveArea in self.solveAreas:
            if solveArea == maxAreaName:
                retSolveAreas[solveArea] = 1
            else:
                retSolveAreas[solveArea] = outWeight

        # update locs
        for loc in locations:
            solveArea = loc["SolveArea"]
            if solveArea in retSolveAreas:
                loc["areaWeight"] = retSolveAreas[loc["SolveArea"]]
                self.log.debug("rewind loc {} new areaWeight: {}".format(loc["Name"], loc["areaWeight"]))
            else:
                # can happen if going to the first area unlocks new areas,
                # or for minors locations when we no longer need minors.
                loc["areaWeight"] = outWeight
                self.log.debug("rewind loc {} from area {} not in original areas".format(loc["Name"], solveArea))

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
                      knowsUsed=(s.knowsUsed, s.knowsKnown), itemsOk=s.itemsOk, patches=s.romLoader.getPatches(),
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
                        sorted(loc['difficulty'].knows),
                        sorted(list(set(loc['difficulty'].items))),
                        [ap.Name for ap in loc['path']] if 'path' in loc else None,
                        loc['Class']])

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

        print("({}, {}): diff : {}".format(round(float(s.difficulty), 3), s.itemsOk, s.romFileName))
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
                              round(float(loc['difficulty'].difficulty), 2) if 'difficulty' in loc else 'nc',
                              sorted(loc['difficulty'].knows) if 'difficulty' in loc else 'nc',
                              sorted(list(set(loc['difficulty'].items))) if 'difficulty' in loc else 'nc'))

    def displayOutput(self):
        s = self.solver

        print("all patches: {}".format(s.romLoader.getAllPatches()))

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
        solver.initialize(args.mode, args.romFileName, args.presetFileName, magic=args.raceMagic, debug=args.vcr, fill=args.fill, startAP=args.startAP)
    else:
        # iterate
        params = {}
        if args.scope == 'common':
            if args.action == "save":
                params["lock"] = args.lock
                params["escapeTimer"] = args.escapeTimer
            elif args.action == "randomize":
                params["progressionSpeed"] = args.progressionSpeed
                params["minorQty"] = args.minorQty
                params["energyQty"] = args.energyQty
        elif args.scope == 'item':
            if args.state == None or args.action == None or args.output == None:
                print("Missing state/action/output parameter")
                sys.exit(1)
            if args.action in ["add", "replace"]:
                if args.mode != 'seedless' and args.loc == None:
                    print("Missing loc parameter when using action add for item")
                    sys.exit(1)
                if args.mode == 'plando':
                    if args.item == None:
                        print("Missing item parameter when using action add in plando/suitless mode")
                        sys.exit(1)
                params = {'loc': args.loc, 'item': args.item, 'hide': args.hide}
            elif args.action == "remove":
                if args.item != None:
                    params = {'item': args.item}
                else:
                    params = {'count': args.count}
            elif args.action == "toggle":
                params = {'item': args.item}
        elif args.scope == 'area':
            if args.state == None or args.action == None or args.output == None:
                print("Missing state/action/output parameter")
                sys.exit(1)
            if args.action == "add":
                if args.startPoint == None or args.endPoint == None:
                    print("Missing start or end point parameter when using action add for item")
                    sys.exit(1)
                params = {'startPoint': args.startPoint, 'endPoint': args.endPoint}
            if args.action == "remove" and args.startPoint != None:
                params = {'startPoint': args.startPoint}
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
                            extStatsStep=args.extStatsStep,
                            displayGeneratedPath=args.displayGeneratedPath,
                            outputFileName=args.output, magic=args.raceMagic,
                            checkDuplicateMajor=args.checkDuplicateMajor, vcr=args.vcr, plot=args.plot)

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
    parser.add_argument('--ext_stats_step', help="what extended stats to generate",
                        nargs='?', default=None, dest='extStatsStep', type=int)
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
                        dest="action", nargs="?", default=None, choices=['init', 'add', 'remove', 'clear', 'get', 'save', 'replace', 'randomize', 'toggle'])
    parser.add_argument('--item', help="Name of the item to place in plando mode (used in interactive mode)",
                        dest="item", nargs='?', default=None)
    parser.add_argument('--hide', help="Hide the item to place in plando mode (used in interactive mode)",
                        dest="hide", action='store_true')
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
    parser.add_argument('--escapeTimer', help="escape timer like 03:00", dest="escapeTimer", default=None)
    parser.add_argument('--fill', help="in plando load all the source seed locations/transitions as a base (used in interactive mode)",
                        dest="fill", action='store_true')
    parser.add_argument('--startAP', help="in plando/seedless: the start location", dest="startAP", default="Landing Site")
    parser.add_argument('--progressionSpeed', help="rando plando (used in interactive mode)",
                        dest="progressionSpeed", nargs="?", default=None, choices=["slowest", "slow", "medium", "fast", "fastest", "basic", "VARIAble"])
    parser.add_argument('--minorQty', help="rando plando  (used in interactive mode)",
                        dest="minorQty", nargs="?", default=None, choices=[str(i) for i in range(0,101)])
    parser.add_argument('--energyQty', help="rando plando  (used in interactive mode)",
                        dest="energyQty", nargs="?", default=None, choices=["sparse", "medium", "vanilla"])
    parser.add_argument('--plot', help="dump plot data in file specified", dest="plot", nargs="?", default=None)

    args = parser.parse_args()

    if args.presetFileName is None:
        args.presetFileName = 'standard_presets/regular.json'

    if args.raceMagic != None:
        if args.raceMagic <= 0 or args.raceMagic >= 0x10000:
            print("Invalid magic")
            sys.exit(-1)

    if args.count != None:
        if args.count < 1 or args.count > 0x80:
            print("Invalid count")
            sys.exit(-1)

    log.init(args.debug)

    if args.interactive == True:
        interactiveSolver(args)
    else:
        standardSolver(args)
