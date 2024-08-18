# optional modules
class SolverModule:
    def reset(self):
        pass

    def addStep(self, locations):
        pass

    def addLocation(self, locName, itemName):
        pass

    def addObjective(self, objectiveName):
        pass

    def addRollback(self, count):
        pass
        
    def dump(self):
        pass

# VCR debug
class ModuleVCR(SolverModule):
    def __init__(self, romFileName=None, vcr=None):
        from utils.vcr import VCR
        if vcr is None:
            self.vcr = VCR(romFileName, 'solver')
        else:
            self.vcr = vcr

    def reset(self):
        self.vcr.empty()

    def addLocation(self, locName, itemName):
        self.vcr.addLocation(locName, itemName)

    def addObjective(self, objectiveName):
        # TODO::remove objectives from VCR to generate VCR compatible with master branch
        # TODO::to be put back after tracker works again in this branch
        if False:
            self.vcr.addObjective(objectiveName)

    def addRollback(self, count):
        self.vcr.addRollback(count)
        
    def dump(self):
        self.vcr.dump()

# extended statistics compute
class ModuleExtStats(SolverModule):
    def __init__(self, solver, extStatsFilename, extStatsStep):
        self.solver = solver
        self.extStatsFilename = extStatsFilename
        self.extStatsStep = extStatsStep
        self.nbAvailLocs = []
        self.solverStats = {}

    def addStep(self, locations):
        self.nbAvailLocs.append(len(locations))

    def addObjective(self, objectiveName):
        self.nbAvailLocs.append(-1)

    def addRollback(self, count):
        self.nbAvailLocs = self.nbAvailLocs[:-count]
        
    def dump(self):
        self.computeExtStats()

        firstMinor = {'Missile': False, 'Super': False, 'PowerBomb': False}
        locsItems = {}
        for loc in self.solver.container.visitedLocations():
            if loc.itemName in firstMinor and firstMinor[loc.itemName] == False:
                locsItems[loc.Name] = loc.itemName
                firstMinor[loc.itemName] = True

        import utils.db as db
        with open(self.extStatsFilename, 'a') as extStatsFile:
            db.DB.dumpExtStatsSolver(self.solver.difficulty, self.solver.knowsUsedList, self.solverStats,
                                     locsItems, self.extStatsStep, extStatsFile)

    def computeExtStats(self):
        # avgLocs: avg number of available locs, the higher the value the more open is a seed
        # open[1-4]4: how many location you have to visit to open 1/4, 1/2, 3/4, all locations.
        #             gives intel about prog item repartition.

        # remove objective steps which have count == -1
        self.nbAvailLocs = [count for count in self.nbAvailLocs if count >= 0]
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

        self.solverStats['open14'] = open14 if open14 != -1 else 0
        self.solverStats['open24'] = open24 if open24 != -1 else 0
        self.solverStats['open34'] = open34 if open34 != -1 else 0
        self.solverStats['open44'] = open44 if open44 != -1 else 0

# log where for each item type the first time it was found and where will be written
class ModuleLogFirst(SolverModule):
    def __init__(self, solver, firstItemsLog):
        self.solver = solver
        self.firstLogFile = open(firstItemsLog, 'w')
        self.firstLogFile.write('Item;Location;Area;GraphArea\n')

    def addLocation(self, locName, itemName):
        if itemName not in self.solver.collectedItems():
            loc = self.solver.getLoc(locName)
            self.firstLogFile.write("{};{};{};{}\n".format(itemName, loc.Name, loc.Area, loc.GraphArea))

    def dump(self):
        self.firstLogFile.close()

# raise a warning if a duplicate major is collected
class ModuleCheckDupMajor(SolverModule):
    def __init__(self, solver):
        self.solver = solver

    def addLocation(self, locName, itemName):
        if itemName not in ['Nothing', 'NoEnergy', 'Missile', 'Super', 'PowerBomb', 'ETank', 'Reserve']:
            if self.solver.smbm.haveItem(itemName):
                print(f"WARNING: {itemName} has already been picked up")
