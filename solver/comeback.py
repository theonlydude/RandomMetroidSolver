import log

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
        # return True if a rewind is needed. choose the next area to use
        solveAreas = {}
        locsCount = 0
        majorNoComeBack = False
        for loc in locations:
            if self.solver.majorsSplit != 'Full':
                if self.solver.majorsSplit in loc.Class or "Boss" in loc.Class:
                    if loc.comeBack is None:
                        return False
                    elif loc.comeBack == True:
                        return False
                    else:
                        # when the solver decide to visit a major no come back locations
                        # when there's minors comeback locations available.
                        # create a rollback point just in case more minors where actually required to do a special tech.
                        majorNoComeBack = True
            else:
                if loc.comeBack is None:
                    return False
                if loc.comeBack == True:
                    return False
            locsCount += 1
            if loc.SolveArea in solveAreas:
                solveAreas[loc.SolveArea] += 1
            else:
                solveAreas[loc.SolveArea] = 1

        if majorNoComeBack == False and self.solver.majorsSplit != 'Full':
            return False

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
            elif self.reuseLastStep(lastStep, solveAreas):
                self.log.debug("Reuse last step at {}".format(lastStep.cur))
                if self.visitedAllLocsInArea(lastStep, locations):
                    return lastStep.next(locations)
                else:
                    self.log.debug("There's still locations in the current solve area, visit them first")
                    return False
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

    def reuseLastStep(self, lastStep, solveAreas):
        # reuse the last step if they share the same solve areas to avoid creating too many
        return sorted(lastStep.solveAreas.keys()) == sorted(solveAreas.keys())

    def visitedAllLocsInArea(self, lastStep, locations):
        for loc in locations:
            if loc.difficulty == True and loc.SolveArea == lastStep.curSolveArea:
                return False
        return True

    def cleanNoComeBack(self, locations):
        for loc in locations:
            loc.areaWeight = None

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
        self.curSolveArea = None
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
        self.curSolveArea = maxAreaName
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
            solveArea = loc.SolveArea
            if solveArea in retSolveAreas:
                loc.areaWeight = retSolveAreas[loc.SolveArea]
                self.log.debug("rewind loc {} new areaWeight: {}".format(loc.Name, loc.areaWeight))
            else:
                # can happen if going to the first area unlocks new areas,
                # or for minors locations when we no longer need minors.
                loc.areaWeight = outWeight
                self.log.debug("rewind loc {} from area {} not in original areas".format(loc.Name, solveArea))

        return False
