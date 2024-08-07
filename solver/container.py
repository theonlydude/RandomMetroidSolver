import logging
from utils.objectives import Objectives
from logic.smbool import SMBool
from graph.graph import Path
from graph.graph_utils import getAccessPoint
from utils.utils import transition2isolver, removeChars, fixEnergy
from utils.parameters import Knows, diff4solver
import utils.log

class SolverContainer(object):
    # store solver steps
    def __init__(self, locations, conf, romConf):
        self.log = utils.log.get('SolverContainer')
        self.conf = conf
        self.romConf = romConf

        self.locations = locations
        self.locationsDict = {loc.Name: loc for loc in locations}

        self.reset()

    def reset(self, reload=False):
        self.steps = []

        if self.romConf.majorsSplit == 'Major':
            self.majorLocations = [loc for loc in self.locations if loc.isMajor() or loc.isBoss()]
            self.minorLocations = [loc for loc in self.locations if loc.isMinor()]
        elif self.romConf.majorsSplit == 'Chozo':
            self.majorLocations = [loc for loc in self.locations if loc.isChozo() or loc.isBoss()]
            self.minorLocations = [loc for loc in self.locations if not loc.isChozo() and not loc.isBoss()]
        elif self.romConf.majorsSplit == 'Scavenger':
            self.majorLocations = [loc for loc in self.locations if loc.isScavenger() or loc.isBoss()]
            self.minorLocations = [loc for loc in self.locations if not loc.isScavenger() and not loc.isBoss()]
        else:
            # Full
            self.majorLocations = self.locations[:] # copy
            self.minorLocations = self.majorLocations

        # in seedless we can add items to the inventory, we need to keep track of them
        self.inventoryItems = []

        if reload:
            self.resetLocsDifficulty()

        # in auto tracker we can update samus current access point when she's travelling the map
        self.overrideAP = None

    def resetLocsDifficulty(self):
        for loc in self.majorLocations:
            loc.difficulty = None

    def rollback(self, count, smbm):
        self.log.debug("rollback {} steps".format(count))
        # cancel count steps
        for _ in range(count):
            if self.steps:
                step = self.steps.pop()
                step.rollback(self, smbm)
        self.overrideAP = None

    def rollbackTracker(self, count, smbm):
        # in tracker we cancel X item locations, so don't count objective steps
        self.log.debug("rollback {} steps for tracker".format(count))
        # cancel count steps
        cancelled = 0
        while self.steps and cancelled < count:
            step = self.steps.pop()
            if self.isStepLocation(step):
                cancelled += 1
            step.rollback(self, smbm)
        self.overrideAP = None

    def removeTrackerLocation(self, locName):
        # used in isolver to remove mother brain location
        loc = self.getLoc(locName)
        self.locations.remove(loc)
        del self.locationsDict[locName]

    def cancelTrackerLocation(self, location, smbm):
        # we cancel a location anywhere in the already collected locations list,
        # doing so could invalidate some objectives but we can't revalidate all of them,
        # so we are only checking if the location to cancel is the last location in the container,
        # if so use the rollbackTracker method which also cancels objectives added after the location.
        self.log.debug("cancelTrackerLocation {}".format(location.Name))
        for step in self.steps[::-1]:
            if self.isStepLocation(step):
                break
        if step.location == location:
            self.log.debug("cancelTrackerLocation location is last collected")
            self.rollbackTracker(1, smbm)
        else:
            for stepIndex, step in enumerate(self.steps):
                if self.isStepLocation(step) and step.location == location:
                    break

            self.log.debug("cancelTrackerLocation location is at index {}".format(stepIndex))

            # remove location step
            self.steps = self.steps[0:stepIndex] + self.steps[stepIndex+1:]
            # in tracker all locs are major
            self.majorLocations.append(location)

        self.debug()

        location.difficulty = None
        location.distance = None
        location.accessPoint = None
        location.path = None

    def updateOverrideAP(self, ap):
        if ap != self.lastAP():
            self.overrideAP = ap

    def lastAP(self):
        # autotracker current AP
        if self.overrideAP is not None:
            return self.overrideAP
        elif self.steps:
            return self.steps[-1].lastAP
        else:
            return self.romConf.startLocation

    def lastArea(self):
        if self.steps:
            return self.steps[-1].lastArea
        else:
            return self.romConf.startArea

    def collectMajor(self, location):
        self.log.debug("collect major at {}".format(location.Name))
        self.majorLocations.remove(location)

    def collectMinor(self, location):
        self.log.debug("collect minor at {}".format(location.Name))
        self.minorLocations.remove(location)

    def collectItem(self, location, itemName, _class):
        # add one item/loc to steps
        self.log.debug("collect item {} at {}".format(itemName, location.Name))
        step = SolverStepLocation(location, itemName, _class)
        self.steps.append(step)
        self.overrideAP = None

    def completeObjective(self, objectiveName, ap, area, paths):
        # add one objective to steps
        Objectives.setGoalCompleted(objectiveName, True)
        step = SolverStepObjective(objectiveName, ap, area, paths)
        self.steps.append(step)
        self.overrideAP = None

    def currentStep(self):
        return len(self.steps)

    def getLoc(self, locName):
        return self.locationsDict.get(locName)

    def isStepLocation(self, step):
        return type(step) == SolverStepLocation

    def isLocVisited(self, location):
        return any(step.location for step in self.steps if self.isStepLocation(step) and step.location == location)

    def visitedLocations(self):
        # return list of visited locs
        return [step.location for step in self.steps if self.isStepLocation(step)]

    def visitedAPs(self):
        # return set of visited APs
        return {ap for step in self.steps for ap in step.APs}

    def collectedItems(self):
        # return list of collected items.
        if self.conf.autotracker:
            # in autotracker returns only inventoryItems read from memory
            return self.inventoryItems
        else:
            return self.inventoryItems + [step.location.itemName for step in self.steps if self.isStepLocation(step)]

    def getMajorsAvailable(self):
        return [loc for loc in self.majorLocations if loc.difficulty is not None and loc.difficulty.bool == True]

    def getMinorsAvailable(self):
        return [loc for loc in self.minorLocations if loc.difficulty is not None and loc.difficulty.bool == True]

    def getAllLocs(self):
        if self.romConf.majorsSplit == 'Full':
            return self.majorLocations
        else:
            return self.majorLocations + self.minorLocations

    def updateEndGameLocation(self, gunship):
        # remove mother brain location and replace it with gunship loc
        mbLoc = self.getLoc('Mother Brain')
        self.majorLocations.remove(mbLoc)
        self.majorLocations.append(gunship)
        # TODO::remove mb loc from locationsDict and add gunship ?

    # manage seedless inventory
    def increaseInventoryItem(self, itemName):
        self.inventoryItems.append(itemName)

    def decreaseInventoryItem(self, itemName):
        self.inventoryItems.remove(itemName)

    def hasItemInInventory(self, itemName):
        return itemName in self.inventoryItems

    def resetInventoryItems(self):
        self.inventoryItems.clear()

    def debug(self):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("solver container content: inventory items: {}".format(self.inventoryItems))
            for step in self.steps:
                step.debug()

    # serialize the solver state for the tracker
    def getState(self):
        state = {}
        state["locsData"] = self.getLocsData()

        state["steps"] = [step.dump() for step in self.steps]
        # required in seedless mode
        state["inventoryItems"] = self.inventoryItems
        return state

    def setState(self, state, smbm):
        smbm.resetItems()
        self.inventoryItems = state["inventoryItems"]

        if self.conf.mode in ['seedless', 'race']:
            smbm.addItems(self.inventoryItems)

        self.setLocsData(state["locsData"])
        for step in state["steps"]:
            if step["type"] == "location":
                smbm.addItem(step["itemName"])
                loc = self.getLoc(step["locationName"])
                if step["_class"] == "major":
                    self.collectMajor(loc)
                else:
                    self.collectMinor(loc)
                self.steps.append(SolverStepLocation.restore(step, loc))
            else:
                Objectives.setGoalCompleted(step["objectiveName"], True)
                self.steps.append(SolverStepObjective.restore(step))

    def getLocsData(self):
        return {
            loc.Name: {
                'distance': loc.distance,
                'accessPoint': loc.accessPoint,
                'difficulty': (loc.difficulty.bool, loc.difficulty.difficulty, loc.difficulty.knows, loc.difficulty.items) if loc.difficulty is not None else None,
                'path': [ap.Name for ap in loc.path] if loc.path is not None else None,
                'pathDifficulty': (loc.pathDifficulty.bool, loc.pathDifficulty.difficulty, loc.pathDifficulty.knows, loc.pathDifficulty.items) if loc.pathDifficulty is not None else None,
                'locDifficulty': (loc.locDifficulty.bool, loc.locDifficulty.difficulty, loc.locDifficulty.knows, loc.locDifficulty.items) if loc.locDifficulty is not None else None,
                'itemName': loc.itemName,
                'comeBack': loc.comeBack,
                'areaWeight': loc.areaWeight,
                'mayNotComeback': loc.mayNotComeback
            } for loc in self.locations
        }

    def setLocsData(self, locsData):
        for locName, locData in locsData.items():
            loc = self.getLoc(locName)
            loc.distance = locData["distance"]
            loc.accessPoint = locData["accessPoint"]
            loc.difficulty = SMBool(locData["difficulty"][0], locData["difficulty"][1], locData["difficulty"][2], locData["difficulty"][3]) if locData["difficulty"] is not None else None
            loc.path = locData["path"] if locData["path"] is None else [getAccessPoint(ap) for ap in locData["path"]]
            loc.pathDifficulty = SMBool(locData["pathDifficulty"][0], locData["pathDifficulty"][1], locData["pathDifficulty"][2], locData["pathDifficulty"][3]) if locData["pathDifficulty"] is not None else None
            loc.locDifficulty = SMBool(locData["locDifficulty"][0], locData["locDifficulty"][1], locData["locDifficulty"][2], locData["locDifficulty"][3]) if locData["locDifficulty"] is not None else None
            loc.itemName = locData["itemName"]
            loc.comeBack = locData["comeBack"]
            loc.areaWeight = locData["areaWeight"]
            loc.mayNotComeback = locData["mayNotComeback"]

    # serialize data for front web
    def availableLocationsWeb(self):
        return self.getLocationsWeb(self.majorLocations, True)

    def visitedLocationsWeb(self):
        return self.getLocationsWeb(self.visitedLocations(), False)

    def name4isolver(self, locName):
        # remove space and special characters
        return removeChars(locName, " ,()-")

    def knows2isolver(self, knows):
        result = []
        for know in knows:
            if know in Knows.desc:
                result.append(Knows.desc[know]['display'])
            else:
                result.append(know)
        return list(set(result))

    def getLocationsWeb(self, locations, onlyAvailable):
        ret = {}
        for loc in locations:
            # in plando we can set items to seq break locations which have difficulty set to false,
            # so when iterating on visited locations we ignore location difficulty
            if (onlyAvailable and loc.difficulty is not None and loc.difficulty.bool) or not onlyAvailable:
                diff = loc.difficulty
                locName = self.name4isolver(loc.Name)
                # we have loc.comeBack which tells if you can comeback from loc access point to current player accesspoint.
                # we also have loc.mayNotComeback which tells if you may not be able to comeback from a loc to its access point.
                # we merge these two comebacks into one to display a '?' on a loc icon if you may not be able to come back from the loc to the current player access point.

                finalMayNotComeback = loc.mayNotComeback or (not loc.comeBack) if loc.comeBack is not None else loc.mayNotComeback
                ret[locName] = {"difficulty": diff4solver(diff.difficulty),
                                "knows": self.knows2isolver(diff.knows),
                                "items": fixEnergy(list(set(diff.items))),
                                "item": loc.itemName,
                                "name": loc.Name,
                                "canHidden": loc.CanHidden,
                                "visibility": loc.Visibility,
                                "major": loc.isClass(self.romConf.masterMajorsSplit),
                                "mayNotComeback": finalMayNotComeback}

                if loc.accessPoint is not None:
                    ret[locName]["accessPoint"] = transition2isolver(loc.accessPoint)
                    if loc.path is not None:
                        ret[locName]["path"] = [transition2isolver(a.Name) for a in loc.path]
                # for debug purpose
                if self.conf.debug == True:
                    if loc.distance is not None:
                        ret[locName]["distance"] = loc.distance
                    if loc.locDifficulty is not None:
                        lDiff = loc.locDifficulty
                        ret[locName]["locDifficulty"] = [diff4solver(lDiff.difficulty)[0], self.knows2isolver(lDiff.knows), list(set(lDiff.items))]
                    if loc.pathDifficulty is not None:
                        pDiff = loc.pathDifficulty
                        ret[locName]["pathDifficulty"] = [diff4solver(pDiff.difficulty)[0], self.knows2isolver(pDiff.knows), list(set(pDiff.items))]

        return ret

    def remainLocationsWeb(self):
        ret = {}
        for loc in self.majorLocations:
            if loc.difficulty is None or not loc.difficulty.bool:
                locName = self.name4isolver(loc.Name)
                ret[locName] = {"item": loc.itemName,
                                "name": loc.Name,
                                "knows": ["Sequence Break"],
                                "items": [],
                                "canHidden": loc.CanHidden,
                                "visibility": loc.Visibility,
                                "major": loc.isClass(self.romConf.masterMajorsSplit),
                                "mayNotComeback": False}
                if self.conf.debug == True:
                    if loc.difficulty is not None:
                        ret[locName]["difficulty"] = str(loc.difficulty)
                    if loc.distance is not None:
                        ret[locName]["distance"] = loc.distance
        return ret

    def lastWeb(self):
        visitedLocations = self.visitedLocations()
        if visitedLocations:
            return {
                "loc": visitedLocations[-1].Name,
                "item": visitedLocations[-1].itemName
            }
        return ""


class SolverStep(object):
    # instead of using several objects to keep visited locations, visited items, visited APs, completed objectives,
    # we put all these into a solver step object
    pass

class SolverStepLocation(SolverStep):
    def __init__(self, location, itemName, _class):
        self.log = utils.log.get('SolverStepLocation')
        self.location = location
        self.location.itemName = itemName
        self._class = _class
        if self.location.accessPoint is not None:
            self.lastAP = location.accessPoint
            self.log.debug("add visited access AP: ['{}'] for loc {}".format(location.accessPoint, location.Name))
        else:
            # when loading a plando we can load locations from non connected areas,
            # so they don't have an access point.
            self.lastAP = list(self.location.AccessFrom.keys())[0]
        self.lastArea = self.location.SolveArea
        self.APs = set(self.lastAP)

        # add location path APs in visited APs (used by explore objectives)
        if self.location.path is not None:
            pathAPs = [ap.Name for ap in self.location.path]
            self.log.debug("add visited path APs: {} for loc {}".format(pathAPs, self.location.Name))
            self.APs.update(pathAPs)

    def rollback(self, container, smbm):
        # delete location params which are set when the location is available
        self.location.difficulty = None
        self.location.distance = None
        self.location.accessPoint = None
        self.location.path = None

        # in plando we have to remove the last added item,
        # else it could be used in computing the postAvailable of a location
        item = self.location.itemName
        if container.conf.mode in ['plando', 'seedless', 'race', 'debug']:
            self.location.itemName = 'Nothing'

        if self._class == 'major':
            container.majorLocations.append(self.location)
        else:
            container.minorLocations.append(self.location)

        if not container.conf.autotracker:
            # if multiple majors in plando mode, remove it from smbm only when it's the last occurence of it
            if smbm.isCountItem(item):
                smbm.removeItem(item)
            else:
                if item not in container.collectedItems():
                    smbm.removeItem(item)

    def dump(self):
        return {
            "type": "location",
            "locationName": self.location.Name,
            "itemName": self.location.itemName,
            "_class": self._class,
        }

    @staticmethod
    def restore(dump, location):
        return SolverStepLocation(location, dump["itemName"], dump["_class"])

    def debug(self):
        self.log.debug("  step location: {}".format(self.location.Name))

class SolverStepObjective(SolverStep):
    def __init__(self, objectiveName, lastAP, lastArea, paths):
        self.log = utils.log.get('SolverStepObjective')
        self.objectiveName = objectiveName
        self.lastAP = lastAP
        self.lastArea = lastArea
        self.APs = set(self.lastAP)
        self.paths = paths if paths is not None else []
        if self.paths is not None:
            pathAPs = [ap.Name for path in self.paths for ap in path.path]
            self.log.debug("add visited path APs: {} for objective {}".format(pathAPs, objectiveName))
            self.APs.update(pathAPs)

    def rollback(self, container, smbm):
        self.log.debug("rollback objective {}".format(self.objectiveName))
        Objectives.setGoalCompleted(self.objectiveName, False)

    def dump(self):
        return {
            "type": "objective",
            "objectiveName": self.objectiveName,
            "lastAP": self.lastAP,
            "lastArea": self.lastArea,
            "paths": [{"path": [ap.Name for ap in path.path],
                       "pdiff": (path.pdiff.bool, path.pdiff.difficulty, path.pdiff.knows, path.pdiff.items),
                       "distance": path.distance} for path in self.paths]
        }

    @staticmethod
    def restore(dump):
        # rebuild paths
        paths = [Path([getAccessPoint(APName) for APName in path["path"]],
                      SMBool(path["pdiff"][1], path["pdiff"][1], path["pdiff"][2], path["pdiff"][3]),
                      path["distance"]) for path in dump["paths"]]

        # instanciate SolverStepObjective
        return SolverStepObjective(dump["objectiveName"], dump["lastAP"], dump["lastArea"], paths)

    def debug(self):
        self.log.debug("  step objective: {}".format(self.objectiveName))
