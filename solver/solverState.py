import os, json

from logic.logic import Logic
from solver.conf import RomConf, InteractiveSolverConf
from solver.container import SolverContainer
from logic.smbool import SMBool
from rom.rom_patches import RomPatches
from utils.utils import removeChars, fixEnergy, transition2isolver
from utils.parameters import diff4solver
from utils.doorsmanager import DoorsManager
from rom.rom_patches import RomPatches
from graph.graph_utils import getAccessPoint

class SolverState(object):
    def set(self, state):
        self.state = state

    def get(self):
        return self.state

    def fromSolver(self, solver):
        self.state = {}

        ################################################
        # data to save the solver state

        ## string. it technically depends on the rom conf but we need it first hand to load the logic
        self.state["logic"] = solver.logic

        # dict with all the conf read from the rom
        self.state["romConf"] = solver.romConf.getState()
        self.state["conf"] = solver.conf.getState()

        # list of active patches
        self.state["patches"] = RomPatches.ActivePatches

        # graph: list [(ap1, ap2), ...]
        self.state["curGraphTransitions"] = solver.curGraphTransitions

        # locations container
        self.state["container"] = solver.container.getState()

        # doors colors: dict {name: (color, facing, hidden)}
        self.state["doors"] = DoorsManager.serialize()

        # custom objectives
        self.state["objectives"] = solver.objectives.getState()
        self.state["totalItemsCount"] = solver.objectives.getTotalItemsCount()


        #############################################
        # data to send to web front
        self.state["web"] = {}

        # item tracker
        self.state["web"]["availableLocations"] = solver.container.availableLocationsWeb()
        self.state["web"]["visitedLocations"] = solver.container.visitedLocationsWeb()
        self.state["web"]["collectedItems"] = solver.container.collectedItems()
        self.state["web"]["remainLocations"] = solver.container.remainLocationsWeb()
        self.state["web"]["lastAP"] = solver.container.lastAP()
        self.state["web"]["last"] = solver.container.lastWeb()

        # area tracker
        (self.state["web"]["linesWeb"],
         self.state["web"]["linesSeqWeb"]) = self.getLinesWeb(solver.curGraphTransitions)
        self.state["web"]["allTransitions"] = len(solver.curGraphTransitions) == len(solver.romConf.areaTransitions) + len(solver.romConf.bossTransitions) + len(solver.romConf.escapeTransition)
        # roomsVisibility: array of string ['landingSiteSvg', 'MissileCrateriamoatSvg']
        self.state["web"]["roomsVisibility"] = self.getRoomsVisibility(solver, solver.areaGraph, solver.smbm)

        # infos on seed
        self.state["web"]["logic"] = solver.logic
        self.state["web"]["mode"] = solver.conf.mode
        self.state["web"]["seed"] = solver.conf.romFileName
        self.state["web"]["preset"] = os.path.basename(os.path.splitext(solver.conf.presetFileName)[0]),
        self.state["web"]["majorsSplit"] = solver.romConf.masterMajorsSplit
        self.state["web"]["areaRando"] = solver.romConf.areaRando
        self.state["web"]["bossRando"] = solver.romConf.bossRando
        self.state["web"]["hasMixedTransitions"] = solver.romConf.hasMixedTransitions
        self.state["web"]["escapeRando"] = solver.romConf.escapeRando
        self.state["web"]["escapeTimer"] = solver.romConf.escapeTimer
        self.state["web"]["hasNothing"] = solver.romConf.hasNothing
        self.state["web"]["tourian"] = solver.romConf.tourian
        self.state["web"]["plandoScavengerOrder"] = solver.romConf.plandoScavengerOrder
        self.state["web"]["objectivesHidden"] = solver.romConf.objectivesHidden
        self.state["web"]["eventsBitMasks"] = solver.romConf.eventsBitMasks

        # doors
        self.state["web"]["doors"] = self.state["doors"]
        self.state["web"]["doorsRando"] = solver.romConf.doorsRando
        self.state["web"]["allDoorsRevealed"] = DoorsManager.allDoorsRevealed()

        # completed objectives
        self.state["web"]["newlyCompletedObjectives"] = solver.newlyCompletedObjectives
        self.state["web"]["objectives"] = self.state["objectives"]

        # error to display to user
        self.state["web"]["errorMsg"] = solver.errorMsg

        # store the inner graph transitions to display in vcr
        self.state["web"]["innerTransitions"] = self.getInnerTransitions(solver.areaGraph.availAccessPoints,
                                                                         solver.curGraphTransitions)

    def toSolver(self, solver):
        solver.logic = self.state["logic"]

        # rom and solver conf
        solver.romConf = RomConf()
        solver.romConf.setState(self.state["romConf"])
        solver.conf = InteractiveSolverConf(**self.state["conf"])

        # active patches
        RomPatches.ActivePatches = self.state["patches"]

        # current graph
        solver.curGraphTransitions = self.state["curGraphTransitions"]

        # location container
        # logic is already loaded
        solver.container = SolverContainer(Logic.locations(), solver.conf, solver.romConf)
        solver.romConf.postSetState(solver.container)
        solver.container.setState(self.state["container"], solver.smbm)

        # doors
        DoorsManager.unserialize(self.state["doors"])

        # custom objectives
        solver.objectives.setState(self.state["objectives"], tourianRequired=solver.romConf.tourian != 'Disabled')
        solver.objectives.setTotalItemsCount(self.state["totalItemsCount"])


    #############################################
    # data for web front compute helpers
    def getRoomsVisibility(self, solver, areaGraph, sm):
        # add graph access points
        roomsVisibility = set([transition2isolver(ap.Name)+'Svg' for ap in solver.areaGraph.availAccessPoints])
        # add available locations
        roomsVisibility.update([loc+'Svg' for loc, data in self.state["web"]["availableLocations"].items() if data["difficulty"] != "break"])
        # add visited locations
        roomsVisibility.update([loc+'Svg' for loc, data in self.state["web"]["visitedLocations"].items() if 'accessPoint' in data and data['accessPoint']+'Svg' in roomsVisibility])
        # add special rooms that have conditions to traverse them but no item in them,
        # so we need to know if they are visible or not
        if 'crocomireRoomTopSvg' in roomsVisibility and sm.enoughStuffCroc():
            roomsVisibility.add('CrocomireSvg')
        if 'greenBrinstarElevatorSvg' in roomsVisibility and sm.traverse('MainShaftBottomRight'):
            roomsVisibility.add('DachoraRoomLeftSvg')
        if 'bigPinkSvg' in roomsVisibility and sm.canPassDachoraRoom():
            roomsVisibility.add('DachoraRoomCenterSvg')
        if ('redBrinstarElevatorSvg' in roomsVisibility and sm.wor(RomPatches.has(RomPatches.HellwayBlueDoor), sm.traverse('RedTowerElevatorLeft'))) or ('redTowerTopLeftSvg' in roomsVisibility and sm.canClimbRedTower()):
            roomsVisibility.add('HellwaySvg')
        if 'businessCenterSvg' in roomsVisibility and sm.haveItem('SpeedBooster'):
            roomsVisibility.add('FrogSpeedwayCenterSvg')
        if 'crabShaftLeftSvg' in roomsVisibility or 'redFishRoomLeftSvg' in roomsVisibility or ('mainStreetBottomSvg' in roomsVisibility and sm.canDoOuterMaridia()):
            roomsVisibility.add('westMaridiaSvg')
        if 'mainStreetBottomSvg' in roomsVisibility and sm.canTraverseCrabTunnelLeftToRight():
            roomsVisibility.add('CrabTunnelSvg')
        if 'SpaceJumpSvg' in roomsVisibility and ('colosseumTopRightSvg' in roomsVisibility or 'leCoudeRightSvg' in roomsVisibility):
            roomsVisibility.add('CacatacAlleySvg')

        return list(roomsVisibility)

    def getInnerTransitions(self, availAccessPoints, curGraphTransitions):
        innerTransitions = []
        if self.state["conf"]["debug"]:
            for (apDst, dataSrc) in availAccessPoints.items():
                if dataSrc['from'] is None:
                    continue
                src = dataSrc['from'].Name
                dst = apDst.Name
                if [src, dst] in curGraphTransitions or [dst, src] in curGraphTransitions:
                    continue
                src = transition2isolver(src)
                dst = transition2isolver(dst)
                innerTransitions.append([src, dst, diff4solver(dataSrc['difficulty'].difficulty)])
        return innerTransitions

    def getLinesWeb(self, transitions):
        lines = {}
        linesSeq = []
        for (start, end) in transitions:
            startWeb = transition2isolver(start)
            endWeb = transition2isolver(end)
            lines[startWeb] = endWeb
            lines[endWeb] = startWeb
            linesSeq.append((startWeb, endWeb))
        return (lines, linesSeq)
