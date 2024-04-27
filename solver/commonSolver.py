import logging, time

from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.smbool import SMBool, smboolFalse
from logic.helpers import Bosses
from rom.romloader import RomLoader
from rom.rom_patches import RomPatches, getPatchDescriptionsByGroup
from graph.graph import AccessGraphSolver as AccessGraph
from utils.utils import PresetLoader
from solver.conf import RomConf
from solver.container import SolverContainer
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, GraphUtils, getAccessPoint
from utils.parameters import easy, medium, hard, harder, hardcore, mania, infinity
from utils.doorsmanager import DoorsManager
from utils.objectives import Objectives
from logic.logic import Logic
from rom.flavor import RomFlavor
from graph.location import define_location

class CommonSolver(object):
    def loadRom(self, rom, extraSettings=None):
        # rom can be:
        #  None: for tracker seedless
        #  dict: for tracker
        #  json file name: for web solver
        #  sfc file name: for console solver
        romConf = RomConf()

        if rom is None:
            # seedless
            self.logic = Logic.implementation
            romConf.initSeedless(extraSettings)

            RomPatches.setDefaultPatches(romConf.startLocation)

            # in seedless load all the vanilla transitions
            self.curGraphTransitions = romConf.bossTransitions + romConf.areaTransitions + romConf.escapeTransition

            self.locations = Logic.locations()
            for loc in self.locations:
                loc.itemName = 'Nothing'

            # set doors related to default patches
            DoorsManager.setDoorsColor(seedless=romConf.doorsRando)

            self.objectives.setVanilla()
        else:
            self.romLoader = RomLoader.factory(rom, self.conf.magic)
            Logic.factory(self.romLoader.readLogic())
            self.logic = Logic.implementation
            if not self.conf.interactive:
                RomFlavor.factory()
            self.romLoader.loadSymbols()
            self.locations = Logic.locations()
            (romConf.majorsSplit, romConf.masterMajorsSplit) = self.romLoader.assignItems(self.locations)
            (romConf.startLocation, romConf.startArea, startPatches) = self.romLoader.getStartAP()
            if not GraphUtils.isStandardStart(romConf.startLocation) and romConf.majorsSplit != 'Full':
                # update major/chozo locs in non standard start
                self.romLoader.updateSplitLocs(romConf.majorsSplit, self.locations)
            (romConf.areaRando, romConf.bossRando, romConf.escapeRando,
             hasObjectives, romConf.tourian) = self.romLoader.loadPatches()
            RomPatches.ActivePatches += startPatches
            romConf.escapeTimer = self.romLoader.getEscapeTimer()
            romConf.doorsRando = self.romLoader.loadDoorsColor()
            romConf.hasNothing = self.checkLocsForNothing()
            if romConf.majorsSplit == 'Scavenger':
                romConf.scavengerOrder = self.romLoader.loadScavengerOrder(self.locations)
            if hasObjectives:
                self.romLoader.loadObjectives(self.objectives)
                if self.conf.interactive:
                    # this option wasn't available in previous release
                    if not Objectives.previousReleaseFallback:
                        romConf.objectivesHiddenOption = bool(self.romLoader.readOption("objectivesHidden"))
                        romConf.objectivesHidden = romConf.objectivesHiddenOption
                        # load event bit masks for auto tracker
                        romConf.eventsBitMasks = self.romLoader.loadEventBitMasks()
            else:
                if romConf.majorsSplit == "Scavenger":
                    # add scav hunt
                    self.objectives.setScavengerHunt()
                    self.objectives.tourianRequired = not self.romLoader.isEscapeTrigger()
                    if self.objectives.tourianRequired:
                        # add G4 on top of scav hunt
                        self.objectives.setVanilla()
                else:
                    # only G4
                    self.objectives.setVanilla()
            romConf.majorUpgrades = self.romLoader.loadMajorUpgrades()
            romConf.splitLocsByArea = self.romLoader.getSplitLocsByArea(self.locations)
            self.objectives.setSolverMode(self, romConf)
            if self.conf.mode == 'plando':
                romConf.additionalETanks = self.romLoader.getAdditionalEtanks()
                romConf.escapeRandoRemoveEnemies = bool(self.romLoader.readOption("escapeRandoRemoveEnemies"))
                romConf.revealMap = self.romLoader.hasPatch('revealMap')
            if self.conf.interactive:
                print("majors: {} area: {} boss: {} escape: {}".format(
                    romConf.majorsSplit, romConf.areaRando,
                    romConf.bossRando, romConf.escapeRando)
                )
            else:
                print("ROM {}\nmajors: {} area: {} boss: {} escape: {}\npatches: {}".format(
                    self.conf.romFileName, romConf.majorsSplit, romConf.areaRando,
                    romConf.bossRando, romConf.escapeRando, self.getPatchDescriptionsByGroup())
                )

            (romConf.areaTransitions, romConf.bossTransitions,
             romConf.escapeTransition, romConf.hasMixedTransitions) = self.romLoader.getTransitions(romConf.tourian)
            self.log.debug("area transitions: {}".format(romConf.areaTransitions))
            self.log.debug("boss transitions: {}".format(romConf.bossTransitions))
            self.log.debug("escape transitions: {}".format(romConf.escapeTransition))

            if self.conf.interactive and not self.conf.debug:
                # in interactive area mode we build the graph as we play along
                if romConf.areaRando and romConf.bossRando:
                    self.curGraphTransitions = []
                elif romConf.areaRando:
                    self.curGraphTransitions = romConf.bossTransitions[:]
                elif romConf.bossRando:
                    self.curGraphTransitions = romConf.areaTransitions[:]
                else:
                    self.curGraphTransitions = romConf.bossTransitions + romConf.areaTransitions
                if not romConf.escapeRando:
                    self.curGraphTransitions += romConf.escapeTransition
            else:
                self.curGraphTransitions = romConf.bossTransitions + romConf.areaTransitions + romConf.escapeTransition

        self.smbm = SMBoolManager()
        self.buildGraph(romConf)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("Display items at locations:")
            for loc in self.locations:
                self.log.debug('{:>50}: {:>16}'.format(loc.Name, loc.itemName))

        return romConf

    def getPatchDescriptionsByGroup(self):
        return getPatchDescriptionsByGroup(sorted(self.romLoader.getPatchIds()), RomFlavor.flavor)

    def buildGraph(self, romConf):
        # in crateria less seeds update escape AP traverse function to be only available during escape
        # to prevent crateria locations from being visited before escape
        if not self.conf.interactive:
            cbl = getAccessPoint("Climb Bottom Left")
            if romConf.tourian == 'Disabled':
                self.log.debug("update Climb Bottom Left traverse function in case of crateria less and tourian disabled")
                cbl.transitions['Landing Site'] = lambda sm: SMBool(Objectives.enoughGoalsCompleted())

            else:
                self.log.debug("update Climb Bottom Left traverse function in case of crateria less and tourian enabled")
                cbl.transitions['Landing Site'] = lambda sm: sm.wand(SMBool(Objectives.enoughGoalsCompleted()),
                                                                     sm.haveItem("MotherBrain"))

        self.areaGraph = AccessGraph(Logic.accessPoints(), self.curGraphTransitions)
        Objectives.setGraph(self.areaGraph, romConf.startLocation, infinity)

    def loadPreset(self, presetFileName):
        presetLoader = PresetLoader.factory(presetFileName)
        presetLoader.load()
        self.smbm.createKnowsFunctions()

        if self.log.getEffectiveLevel() == logging.DEBUG:
            presetLoader.printToScreen()

    def getNextDifficulty(self, difficulty):
        nextDiffs = {
            0: easy,
            easy: medium,
            medium: hard,
            hard: harder,
            harder: hardcore,
            hardcore: mania,
            mania: infinity
        }
        return nextDiffs[difficulty]

    def checkLocsForNothing(self):
        # for the auto tracker, need to know if we have to track nothing items
        return any(loc.itemName == "Nothing" for loc in self.locations)

    def computeLocationsDifficulty(self, locations, phase="major", startDiff=None):
        difficultyTarget = startDiff if startDiff is not None else self.conf.difficultyTarget
        nextLocations = locations

        # before looping on all diff targets, get only the available locations with diff target infinity
        if difficultyTarget != infinity:
            self.areaGraph.getAvailableLocations(nextLocations, self.smbm, infinity, self.container.lastAP())
            nextLocations = [loc for loc in nextLocations if loc.difficulty]

        while True:
            self.areaGraph.getAvailableLocations(nextLocations, self.smbm, difficultyTarget, self.container.lastAP())
            # check post available functions too
            for loc in nextLocations:
                loc.evalPostAvailable(self.smbm, self.conf.mode)

            self.areaGraph.useCache(True)
            # also check if we can come back to current AP from the location
            for loc in nextLocations:
                loc.evalComeBack(self.smbm, self.areaGraph, self.container.lastAP())
            self.areaGraph.useCache(False)

            nextLocations = [loc for loc in nextLocations if not loc.difficulty]
            if not nextLocations:
                break

            if difficultyTarget == infinity:
                # we've tested all the difficulties
                break

            # start a new loop with next difficulty
            difficultyTarget = self.getNextDifficulty(difficultyTarget)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("available {} locs:".format(phase))
            for loc in locations:
                if loc.difficulty.bool == True:
                    print("{:>48}: {:>8}".format(loc.Name, round(loc.difficulty.difficulty, 2)))
                    print("                                          smbool: {}".format(loc.difficulty))
                    print("                                            path: {}".format([ap.Name for ap in loc.path]))

    def collectMajor(self, loc, itemName=None):
        self.log.debug("collect major at {}".format(loc.Name))
        self.container.collectMajor(loc)
        self.collectItem(loc, 'major', itemName)
        return loc

    def collectMinor(self, loc):
        self.log.debug("collect minor at {}".format(loc.Name))
        self.container.collectMinor(loc)
        self.collectItem(loc, 'minor')
        return loc

    def collectItem(self, loc, _class, item=None):
        if item is None:
            item = loc.itemName

        for module in self.modules:
            module.addLocation(loc.Name, item)

        if item not in self.conf.itemsForbidden:
            # in autotracker items are read from memory
            if not self.conf.autotracker:
                self.smbm.addItem(item)
        else:
            # update the name of the item
            item = "-{}-".format(item)
            loc.itemName = item
            # we still need the boss difficulty
            if not loc.isBoss():
                loc.difficulty = smboolFalse
        self.container.collectItem(loc, item, _class)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            print("---------------------------------------------------------------")
            print("collectItem: {:<16} at {:<48} diff {}".format(item, loc.Name, loc.difficulty))
            print("---------------------------------------------------------------")

    def rollback(self, count):
        for module in self.modules:
            module.addRollback(count)

        self.container.rollback(count, self.smbm)

    def printLocs(self, locs, phase):
        if len(locs) > 0:
            print("{}:".format(phase))
            print('{:>48} {:>12} {:>8} {:>8} {:>34} {:>10}'.format("Location Name", "Difficulty", "Distance", "ComeBack", "SolveArea", "AreaWeight"))
            for loc in locs:
                print('{:>48} {:>12} {:>8} {:>8} {:>34} {:>10}'.
                      format(loc.Name, round(loc.difficulty[1], 2), round(loc.distance, 2),
                             loc.comeBack, loc.SolveArea, loc.areaWeight if loc.areaWeight is not None else -1))

    def getAvailableItemsList(self, locations, threshold):
        # locations without distance are not available
        locations = [loc for loc in locations if loc.distance is not None]

        if len(locations) == 0:
            return []

        mandatoryBosses = Objectives.getMandatoryBosses()

        # add nocomeback locations which has been selected by the comeback step (areaWeight == 1)
        around = [loc for loc in locations if( (loc.areaWeight is not None and loc.areaWeight == 1)
                                               or ((loc.SolveArea == self.container.lastArea() or loc.distance < 3)
                                                   and loc.difficulty.difficulty <= threshold
                                                   and (not Bosses.areaBossDead(self.smbm, self.container.lastArea())
                                                        and (self.container.lastArea() not in Bosses.areaBosses
                                                             or Bosses.areaBosses[self.container.lastArea()] in mandatoryBosses))
                                                   and loc.comeBack is not None and loc.comeBack == True)
                                               or (loc.Name == "Gunship") )]
        outside = [loc for loc in locations if not loc in around]

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.printLocs(around, "around1")
            self.printLocs(outside, "outside1")

        around.sort(key=lambda loc: (
            # end game loc
            0 if loc.Name == "Gunship" else 1,
            # locs in the same area
            0 if loc.SolveArea == self.container.lastArea() else 1,
            # nearest locs
            loc.distance,
            # beating a boss
            0 if loc.isBoss() else 1,
            # easiest first
            loc.difficulty.difficulty
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
            if loc.areaWeight is not None:
                ranged["areaWeight"].append(loc)
            elif loc.comeBack is None or loc.comeBack == False:
                ranged["noComeBack"].append(loc)
            else:
                difficulty = loc.difficulty.difficulty
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
                0 if loc.SolveArea == self.container.lastArea() else 1,
                # first nearest locs
                loc.distance,
                # beating a boss
                loc.difficulty.difficulty if (not Bosses.areaBossDead(self.smbm, loc.Area)
                                              and loc.isBoss())
                else 100000,
                # areas with boss still alive
                loc.difficulty.difficulty if (not Bosses.areaBossDead(self.smbm, loc.Area))
                else 100000,
                loc.difficulty.difficulty))


        if self.log.getEffectiveLevel() == logging.DEBUG:
            for key in ["areaWeight", "easy", "medium", "hard", "harder", "hardcore", "mania", "noComeBack"]:
                self.printLocs(ranged[key], "outside2:{}".format(key))

        outside = []
        for key in ["areaWeight", "easy", "medium", "hard", "harder", "hardcore", "mania", "noComeBack"]:
            outside += ranged[key]

        locs = around + outside

        # special case for newbie like presets and VARIA tweaks, when both Phantoon and WS Etank are available,
        # if phantoon is visited first then WS Etank is no longer available as newbie can't pass sponge bath.
        # do the switch only if phantoon and ws etank have the same comeback, in boss rando we can have
        # phantoon comeback and ws etank nocomeback and it would fail to solve in that case.
        if locs and locs[0].Name == 'Phantoon':
            for i, loc in enumerate(locs):
                if loc.Name == 'Energy Tank, Wrecked Ship' and locs[0].comeBack == loc.comeBack:
                    self.log.debug("switch Phantoon and WS Etank")
                    locs[i] = locs[0]
                    locs[0] = loc
                    break

        return locs

    def nextDecision(self, majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold):
        # first go back to gunship if available to end the run
        if (len(majorsAvailable) > 0
            and majorsAvailable[0].Name == "Gunship"):
            return self.collectMajor(majorsAvailable.pop(0))
        # next take major items of acceptable difficulty in the current area
        elif (len(majorsAvailable) > 0
            and majorsAvailable[0].SolveArea == self.container.lastArea()
            and majorsAvailable[0].difficulty.difficulty <= diffThreshold
            and majorsAvailable[0].comeBack == True):
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
            self.log.debug('BOTH|M={}, m={}'.format(majorsAvailable[0].Name, minorsAvailable[0].Name))
            # if both are available, decide based on area, difficulty and comeBack
            nextMajDifficulty = majorsAvailable[0].difficulty.difficulty
            nextMinDifficulty = minorsAvailable[0].difficulty.difficulty
            nextMajArea = majorsAvailable[0].SolveArea
            nextMinArea = minorsAvailable[0].SolveArea
            nextMajComeBack = majorsAvailable[0].comeBack
            nextMinComeBack = minorsAvailable[0].comeBack
            nextMajDistance = majorsAvailable[0].distance
            nextMinDistance = minorsAvailable[0].distance
            maxAreaWeigth = 10000
            nextMajAreaWeight = majorsAvailable[0].areaWeight if majorsAvailable[0].areaWeight is not None else maxAreaWeigth
            nextMinAreaWeight = minorsAvailable[0].areaWeight if minorsAvailable[0] .areaWeight is not None else maxAreaWeigth

            if self.log.getEffectiveLevel() == logging.DEBUG:
                print("     : {:>4} {:>32} {:>4} {:>4} {:>6}".format("diff", "area", "back", "dist", "weight"))
                print("major: {:>4} {:>32} {:>4} {:>4} {:>6}".format(round(nextMajDifficulty, 2), nextMajArea, nextMajComeBack, round(nextMajDistance, 2), nextMajAreaWeight))
                print("minor: {:>4} {:>32} {:>4} {:>4} {:>6}".format(round(nextMinDifficulty, 2), nextMinArea, nextMinComeBack, round(nextMinDistance, 2), nextMinAreaWeight))

            if hasEnoughMinors == True and self.haveAllMinorTypes() == True and self.smbm.haveItem('Charge') and nextMajAreaWeight != maxAreaWeigth:
                # we have charge, no longer need minors
                self.log.debug("we have charge, no longer need minors, take major")
                return self.collectMajor(majorsAvailable.pop(0))
            else:
                # respect areaweight first
                if nextMajAreaWeight != nextMinAreaWeight:
                    self.log.debug("maj/min != area weight")
                    if nextMajAreaWeight < nextMinAreaWeight:
                        return self.collectMajor(majorsAvailable.pop(0))
                    else:
                        return self.collectMinor(minorsAvailable.pop(0))
                # then take item from loc where you can come back
                elif nextMajComeBack != nextMinComeBack:
                    self.log.debug("maj/min != combeback")
                    if nextMajComeBack == True:
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
                elif nextMinArea == self.container.lastArea() and nextMinDifficulty <= diffThreshold:
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

    def canRelaxEnd(self):
        # sometimes you can't get all locations because of restricted locs, so allow to go to mother brain
        if self.endGameLoc.Name == 'Mother Brain' and self.conf.pickupStrategy == 'all':
            self.relaxedEndCheck = True
            self.computeLocationsDifficulty(self.container.majorLocations)
            self.relaxedEndCheck = False
            return self.endGameLoc.difficulty == True
        else:
            return False

    def getGunship(self):
        # add gunship location and try to go back to it
        solver = self
        def GunshipAccess(sm):
            nonlocal solver

            return SMBool(solver.objectives.enoughGoalsCompleted())

        def GunshipAvailable(_, sm):
            nonlocal solver

            if solver.relaxedEndCheck:
                return SMBool(True)
            else:
                hasEnoughMinors = solver.pickup.enoughMinors(sm, solver.container.minorLocations)
                hasEnoughMajors = solver.pickup.enoughMajors(sm, solver.container.majorLocations)
                hasEnoughItems = hasEnoughMajors and hasEnoughMinors
                return SMBool(hasEnoughItems)

        gunship = define_location(
            Area="Crateria",
            GraphArea="Crateria",
            SolveArea="Crateria Landing Site",
            Name="Gunship",
            # to display bigger gunship image in spoiler log
            Class=["Boss"],
            CanHidden=False,
            Address=-1,
            Id=None,
            Visibility="Hidden",
            Room='Landing Site',
            AccessFrom = {
                'Landing Site': GunshipAccess
            },
            Available = GunshipAvailable
        )
        gunship.itemName = 'Gunship'
        return gunship

    def getMotherBrainAccess(self):
        solver = self
        def MotherBrainAccess(sm):
            nonlocal solver

            return SMBool(solver.objectives.enoughGoalsCompleted())
        return MotherBrainAccess

    def getMotherBrainAvailable(self):
        solver = self
        def MotherBrainAvailable(sm):
            nonlocal solver

            tourian = sm.enoughStuffTourian()

            # can't check all locations
            if solver.relaxedEndCheck:
                return tourian
            else:
                hasEnoughMinors = solver.pickup.enoughMinors(sm, solver.container.minorLocations)
                hasEnoughMajors = solver.pickup.enoughMajors(sm, solver.container.majorLocations)
                hasEnoughItems = hasEnoughMajors and hasEnoughMinors
                return sm.wand(tourian, SMBool(hasEnoughItems))
        return MotherBrainAvailable

    def computeDifficulty(self):
        # loop on the available locations depending on the collected items.
        # before getting a new item, loop on all of them and get their difficulty,
        # the next collected item is the one with the smallest difficulty,
        # if equality between major and minor, take major first.

        self.container = SolverContainer(self.locations, self.conf, self.romConf)
        mbLoc = self.container.getLoc('Mother Brain')
        if self.objectives.tourianRequired:
            # update mother brain to handle all end game conditions, allow MB loc to access solver data
            mbLoc.AccessFrom['Golden Four'] = self.getMotherBrainAccess()
            mbLoc.Available = self.getMotherBrainAvailable()
            self.endGameLoc = mbLoc
            self.log.debug("tourian is required, end game location is mother brain")
        else:
            # remove mother brain location and replace it with gunship loc
            gunship = self.getGunship()
            self.container.updateEndGameLocation(gunship)
            self.endGameLoc = gunship
            self.log.debug("tourian is disabled, end game location is gunship")

        self.log.debug("{}: available major: {}, available minor: {}".format(
            self.conf.pickupStrategy, len(self.container.majorLocations), len(self.container.minorLocations))
        )

        endDifficulty = mania
        diffThreshold = self.getDiffThreshold()
        self.relaxedEndCheck = False
        self.aborted = False

        while not self.container.isLocVisited(self.endGameLoc):
            # check time limit
            if self.runtimeLimiter.expired():
                return (-1, False)

            self.log.debug("################################ new solver step ################################")
            self.log.debug("Current AP/Area: {}/{}".format(self.container.lastAP(), self.container.lastArea()))
            self.log.debug("Objectives: {}".format(self.objectives.getState()))
            if self.log.getEffectiveLevel() == logging.DEBUG:
                aps = self.areaGraph.getAvailableAccessPoints(getAccessPoint(self.container.lastAP()), self.smbm, infinity)
                aps = sorted([ap.Name for ap in aps])
                self.log.debug("APs: {}".format(aps))
            self.log.debug("SMBM: {}".format(self.smbm.getItems()))

            # check if a new objective can be completed
            goals = self.objectives.checkGoals(self.smbm, self.container.lastAP())
            if any([possible for possible in goals.values()]):
                completed = False
                for goalName, possible in goals.items():
                    if possible:
                        self.log.debug("objective possible: {}".format(goalName))
                        goalObj = self.objectives.goals[goalName]
                        requiredAPs, requiredLocs = goalObj.objCompletedFuncVisit(self.container.lastAP())
                        visitedLocNames = set([loc.Name for loc in self.container.visitedLocations()])
                        self.log.debug("remaining required APs: {}".format([ap for ap in requiredAPs if ap not in self.container.visitedAPs()]))
                        self.log.debug("remaining required locs: {}".format([loc for loc in requiredLocs if loc not in visitedLocNames]))
                        # first check required locs
                        if set(requiredLocs).issubset(visitedLocNames):
                            # extract missing APs and visit them to get objective path
                            missingAPs = set(requiredAPs) - self.container.visitedAPs()
                            paths = None
                            if missingAPs:
                                self.log.debug("try to access objective missing APs: {}".format(missingAPs))
                                paths = self.areaGraph.exploreAPs(self.smbm, self.container.lastAP(), missingAPs, infinity)
                                if not paths:
                                    self.log.debug("can't access missings APs for objective {}".format(goalName))
                                    continue

                            self.log.debug("complete objective {}".format(goalName))

                            # if some aps have been visited to complete the objectives,
                            #  use them to update last AP/Area
                            if paths is not None:
                                lastAP = paths[-1].path[-1]
                                objLastAP = lastAP.Name
                                objLastArea = lastAP.SolveArea
                            else:
                                objLastAP = self.container.lastAP()
                                objLastArea = self.container.lastArea()

                            self.container.completeObjective(goalName, objLastAP, objLastArea, paths)

                            for module in self.modules:
                                module.addObjective(goalName)

                            # TODO::always create a rollback point when completing an objective ?
                            #       it means that we have to priorize objective or location after a rollback (to
                            #       not complete the rollbacked objective right away),
                            #       so it's a big change... try with jm first to see if it happens

                            completed = True
                            break
                        else:
                            self.log.debug("objective missing aps: {}".format(
                                sorted(set(requiredAPs) - self.container.visitedAPs()))
                            )
                if completed:
                    continue
            else:
                self.log.debug("no possible objectives, remaining: {}".format(goals.keys()))

            # compute the difficulty of all the locations
            self.computeLocationsDifficulty(self.container.majorLocations)
            if self.romConf.majorsSplit != 'Full':
                self.computeLocationsDifficulty(self.container.minorLocations, phase="minor")

            # keep only the available locations
            majorsAvailable = self.container.getMajorsAvailable()
            minorsAvailable = self.container.getMinorsAvailable()

            allLocs = self.getAllLocs(majorsAvailable, minorsAvailable)
            for module in self.modules:
                module.addStep(allLocs)

            # remove next scavenger locs before checking if we're stuck
            if self.romConf.majorsSplit == 'Scavenger':
                majorsAvailable = self.filterScavengerLocs(majorsAvailable)

            # check if we're stuck
            if len(majorsAvailable) == 0 and len(minorsAvailable) == 0:
                self.log.debug("STUCK MAJORS and MINORS")

                if not self.endGameLoc.difficulty and self.canRelaxEnd():
                    self.log.debug("Can't collect 100% but Mother Brain is available in relax end")
                    majorsAvailable.append(self.endGameLoc)
                elif self.comeBack.rewind(self.container.currentStep()) == True:
                    self.log.debug("Rewind as we're stuck")
                    continue
                else:
                    # we're really stucked
                    self.log.debug("STUCK CAN'T REWIND")
                    self.aborted = True
                    break

            # handle no comeback locations
            rewindRequired = self.comeBack.handleNoComeBack(majorsAvailable, minorsAvailable,
                                                            self.container.currentStep())
            if rewindRequired == True:
                if self.comeBack.rewind(self.container.currentStep()) == True:
                    continue
                else:
                    # we're really stucked
                    self.log.debug("STUCK CAN'T REWIND")
                    self.aborted = True
                    break

            # sort them on difficulty and proximity
            self.log.debug("getAvailableItemsList majors")
            majorsAvailable = self.getAvailableItemsList(majorsAvailable, diffThreshold)
            if self.romConf.majorsSplit == 'Full':
                minorsAvailable = majorsAvailable
            else:
                self.log.debug("getAvailableItemsList minors")
                minorsAvailable = self.getAvailableItemsList(minorsAvailable, diffThreshold)

            # choose one to pick up
            hasEnoughMinors = self.pickup.enoughMinors(self.smbm, self.container.minorLocations)
            self.nextDecision(majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold)

            self.comeBack.cleanNoComeBack(self.getAllLocs(self.container.majorLocations,
                                                          self.container.minorLocations))

        if self.objectives.tourianRequired and not self.aborted and self.romConf.escapeTransition:
            # add gunship location to display escape in the spoiler log
            gunship = self.getGunship()
            self.container.majorLocations.append(gunship)
            # ignore items requirements now that mother brain is dead
            self.relaxedEndCheck = True
            # change current AP to escape AP
            self.container.updateOverrideAP(self.romConf.escapeTransition[0][1])
            self.computeLocationsDifficulty(self.container.majorLocations)
            majorsAvailable = self.container.getMajorsAvailable()
            if gunship in majorsAvailable:
                self.collectMajor(gunship)

        # compute difficulty value
        (difficulty, itemsOk) = self.computeDifficultyValue()

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("difficulty={}".format(difficulty))
            self.log.debug("itemsOk={}".format(itemsOk))
            self.log.debug("{}: remaining major: {}, remaining minor: {}, visited: {}".format(
                self.conf.pickupStrategy, len(self.container.majorLocations),
                len(self.container.minorLocations), len(self.container.visitedLocations())
            ))

            self.log.debug("remaining majors:")
            for loc in self.container.majorLocations:
                self.log.debug("{} ({})".format(loc.Name, loc.itemName))

            self.log.debug("bosses: {}".format([(boss, Bosses.bossDead(self.smbm, boss)) for boss in Bosses.Golden4()]))

        return (difficulty, itemsOk)

    def haveAllMinorTypes(self):
        # the first minor of each type can be seen as a major, so check for them first before going to far in zebes
        collectedItems = self.container.collectedItems()
        hasPB = 'PowerBomb' in collectedItems
        hasSuper = 'Super' in collectedItems
        hasMissile = 'Missile' in collectedItems
        return (hasPB and hasSuper and hasMissile)

    def getAllLocs(self, majorsAvailable, minorsAvailable):
        if self.romConf.majorsSplit == 'Full':
            return majorsAvailable
        else:
            return majorsAvailable+minorsAvailable

    def computeDifficultyValue(self):
        if self.aborted:
            # we have aborted
            return (-1, False)
        else:
            # return the maximum difficulty
            difficultyMax = 0
            for loc in self.container.visitedLocations():
                difficultyMax = max(difficultyMax, loc.difficulty.difficulty)
            difficulty = difficultyMax

            # check if we have taken all the requested items
            if (self.pickup.enoughMinors(self.smbm, self.container.minorLocations)
                and self.pickup.enoughMajors(self.smbm, self.container.majorLocations)):
                return (difficulty, True)
            else:
                # can finish but can't take all the requested items
                return (difficulty, False)

    def getScavengerHuntState(self):
        # check where we are in the scavenger hunt
        huntInProgress = False
        index = 0
        for index, loc in enumerate(self.romConf.scavengerOrder):
            if not self.container.isLocVisited(loc):
                huntInProgress = True
                break
        return (huntInProgress, index)

    def filterScavengerLocs(self, majorsAvailable):
        huntInProgress, index = self.getScavengerHuntState()
        if huntInProgress and index < len(self.romConf.scavengerOrder)-1:
            self.log.debug("Scavenger hunt in progress, {}/{}".format(index, len(self.romConf.scavengerOrder)-1))
            # remove all next locs in the hunt
            nextHuntLocs = self.romConf.scavengerOrder[index+1:]
            for loc in nextHuntLocs:
                self.log.debug("Scavenger hunt, try to remove loc {}".format(loc.Name))
                try:
                    majorsAvailable.remove(loc)
                except:
                    pass

        return majorsAvailable

    def scavengerHuntComplete(self, smbm=None, ap=None):
        if self.romConf.masterMajorsSplit != 'Scavenger':
            return SMBool(True)
        else:
            # check that last loc from the scavenger hunt list has been visited.
            # avoid crash in plando if the list is empty (it shouldn't)
            if self.romConf.scavengerOrder:
                lastLoc = self.romConf.scavengerOrder[-1]
                return SMBool(self.container.isLocVisited(lastLoc))
            return SMBool(False)

    def getPriorityArea(self):
        # if scav returns solve area of next loc in the hunt
        if self.romConf.majorsSplit != 'Scavenger':
            return None
        huntInProgress, index = self.getScavengerHuntState()
        if huntInProgress and index < len(self.romConf.scavengerOrder)-1:
            return self.romConf.scavengerOrder[index].SolveArea
        return None
