from utils.objectives import Objectives
import utils.log

class SolverContainer(object):
    # store solver steps
    def __init__(self, locations, conf, romConf):
        self.log = utils.log.get('SolverContainer')
        self.conf = conf
        self.romConf = romConf

        self.steps = []

        self.locations = locations
        self.locationsDict = {loc.Name: loc for loc in locations}

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

    def rollback(self, count, smbm):
        self.log.debug("rollback {} steps".format(count))
        # cancel count steps
        for _ in range(count):
            if self.steps:
                step = self.steps.pop()
                step.rollback(self, smbm)

    def lastAP(self):
        if self.steps:
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

    def completeObjective(self, objectiveName, ap, area, paths):
        # add one objective to steps
        Objectives.setGoalCompleted(objectiveName, True)
        step = SolverStepObjective(objectiveName, ap, area, paths)
        self.steps.append(step)

    def currentStep(self):
        return len(self.steps)

    def getLoc(self, locName):
        return self.locationsDict[locName]

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
        # return list of collected items
        return [step.itemName for step in self.steps if self.isStepLocation(step)]

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

class SolverStep(object):
    # instead of using several objects to keep visited locations, visited items, visited APs, completed objectives,
    # we put all these into a solver step object
    pass

class SolverStepLocation(SolverStep):
    def __init__(self, location, itemName, _class):
        self.log = utils.log.get('SolverStepLocation')
        self.location = location
        self.itemName = itemName
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

        # if multiple majors in plando mode, remove it from smbm only when it's the last occurence of it
        if smbm.isCountItem(item):
            smbm.removeItem(item)
        else:
            if item not in container.collectedItems():
                smbm.removeItem(item)

class SolverStepObjective(SolverStep):
    def __init__(self, objectiveName, lastAP, lastArea, paths):
        self.log = utils.log.get('SolverStepObjective')
        self.objectiveName = objectiveName
        self.lastAP = lastAP
        self.lastArea = lastArea
        self.APs = set(self.lastAP)
        self.paths = paths
        if self.paths is not None:
            pathAPs = [ap.Name for path in self.paths for ap in path.path]
            self.log.debug("add visited path APs: {} for objective {}".format(pathAPs, objectiveName))
            self.APs.update(pathAPs)

    def rollback(self, container, smbm):
        self.log.debug("rollback objective {}".format(self.objectiveName))
        Objectives.setGoalCompleted(self.objectiveName, False)
