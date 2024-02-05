import time, copy

from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.helpers import Pickup
from graph.graph_utils import getAccessPoint
from solver.conf import RandoSolverConf
from solver.comeback import ComeBack
from solver.standardSolver import StandardSolver
from solver.out import Out
from solver.runtimeLimiter import runtimeLimiter
from utils.parameters import easy
from utils.objectives import Objectives
import utils.log

class RandoSolver(StandardSolver):
    def __init__(self, majorsSplit, startLocation, areaGraph, locations, vcr=None):
        self.log = utils.log.get('Solver')

        self.conf = RandoSolverConf()

        # optional modules
        self.modules = []
        if vcr is not None:
            from solver.modules import ModuleVCR
            self.modules.append(ModuleVCR(vcr=vcr))

        self.output = Out.factory('rando', self)

        # create a copy of locations as solver can add gunship or update mother brain functions
        self.locations = copy.deepcopy(locations)
        self.smbm = SMBoolManager()
        self.pickup = Pickup(self.conf.pickupStrategy)
        self.comeBack = ComeBack(self)

        # load ROM info, patches are already loaded by the rando. get the graph from the rando too
        self.conf.majorsSplit = majorsSplit
        self.conf.startLocation = startLocation
        self.conf.startArea = getAccessPoint(startLocation).Start['solveArea']
        self.areaGraph = areaGraph
        self.escapeTransition = []

        self.objectives = Objectives()

        # limit to a few seconds to avoid cases with a lot of rewinds which could last for minutes
        self.runtimeLimiter = RuntimeLimiter(5)

    def propagateDifficulties(self, container):
        # as the rando solver works on a copy of the rando locations we have to propagate
        # locations difficulties computed by the solver back to the rando
        for loc in self.container.visitedLocations():
            if loc.itemName == "Gunship":
                continue
            itemLoc = container.getItemLoc(loc)

            # update difficulty for non restricted locations
            if not itemLoc.Location.restricted:
                itemLoc.Location.difficulty = loc.difficulty
