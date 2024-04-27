import sys, json, os, tempfile

from solver.commonSolver import CommonSolver
from solver.solverState import SolverState
from solver.comeback import ComeBack
from solver.conf import InteractiveSolverConf
from solver.runtimeLimiter import RuntimeLimiter
from solver.container import SolverContainer
from logic.logic import Logic
from logic.smbool import SMBool
from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.helpers import Pickup
from rom.rompatcher import RomPatcher
from rom.rom_patches import RomPatches
from rom.flavor import RomFlavor
from rando.ItemLocContainer import ItemLocation
from graph.graph import AccessGraphSolver as AccessGraph
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, GraphUtils
from graph.location import define_location
from graph.vanilla.map_tiles import areaAccessPoints as vanilla_areaAccessPoints, bossAccessPoints as vanilla_bossAccessPoints, escapeAccessPoints as vanilla_escapeAccessPoints, itemLocations as vanilla_itemLocations, doors as vanilla_doors
from graph.mirror.map_tiles import areaAccessPoints as mirror_areaAccessPoints, bossAccessPoints as mirror_bossAccessPoints, escapeAccessPoints as mirror_escapeAccessPoints, itemLocations as mirror_itemLocations, doors as mirror_doors
from utils.utils import removeChars
from utils.parameters import easy, hard, infinity
from utils.doorsmanager import DoorsManager
from utils.objectives import Objectives
import utils.log

class InteractiveSolver(CommonSolver):
    def __init__(self, logic):
        self.modules = []
        self.interactive = True
        self.errorMsg = ""
        self.log = utils.log.get('Solver')

        self.logic = logic
        Logic.factory(self.logic, new=True)
        RomFlavor.factory()

        (self.locsAddressName, self.locsWeb2Internal) = self.initLocsAddressName()
        self.transWeb2Internal = self.initTransitionsName()

        self.objectives = Objectives(reset=True)

    def initLocsAddressName(self):
        addressName = {}
        web2Internal = {}
        for loc in Logic.locations():
            webName = self.locNameInternal2Web(loc.Name)
            addressName[loc.Address % 0x10000] = webName
            web2Internal[webName] = loc.Name
        return (addressName, web2Internal)

    def initTransitionsName(self):
        web2Internal = {}
        for (startPoint, endPoint) in vanillaTransitions + vanillaBossesTransitions + vanillaEscapeTransitions:
            for point in [startPoint, endPoint]:
                web2Internal[self.apNameInternal2Web(point)] = point
        return web2Internal

    def dumpState(self):
        state = SolverState()
        state.fromSolver(self)
        return state.get()

    def initialize(self, mode, romData, romFileName, presetFileName, fill, extraSettings):
        # load rom and preset, return first state
        self.conf = InteractiveSolverConf(mode=mode, romFileName=romFileName, presetFileName=presetFileName)

        self.smbm = SMBoolManager()

        self.loadPreset(self.conf.presetFileName)

        self.romConf = self.loadRom(romData, extraSettings=extraSettings)
        # in plando/tracker always consider that we're doing full
        self.romConf.majorsSplit = 'Full'

        # hide doors
        DoorsManager.initTracker(self.romConf.doorsRando and self.conf.mode in ['standard', 'race'])

        self.container = SolverContainer(Logic.locations(), self.conf, self.romConf)
        self.clearItems()

        # in debug mode don't load plando locs/transitions
        if self.conf.mode == 'plando' and not self.conf.debug:
            if fill is True:
                # load the source seed transitions and items/locations
                self.curGraphTransitions = self.romConf.bossTransitions + self.romConf.areaTransitions + self.romConf.escapeTransition
                self.buildGraph(self.romConf)
                self.fillPlandoLocs()
            else:
                if self.romConf.areaRando == True or self.romConf.bossRando == True:
                    plandoTrans = self.loadPlandoTransitions()
                    if len(plandoTrans) > 0:
                        self.curGraphTransitions = plandoTrans
                    self.buildGraph(self.romConf)

                self.loadPlandoLocs()

        # if tourian is disabled remove mother brain location
        if self.romConf.tourian == 'Disabled':
            self.container.removeTrackerLocation('Mother Brain')

        # compute new available locations
        self.computeLocationsDifficulty(self.container.majorLocations, startDiff=easy)
        self.checkGoals()

        return self.dumpState()

    def iterate(self, instate, scope, action, params):
        self.debug = params["debug"]
        self.smbm = SMBoolManager()

        state = SolverState()
        state.set(instate)
        state.toSolver(self)
        self.objectives.setSolverMode(self, self.romConf)

        # set mother brain access func for solver
        if self.romConf.tourian != 'Disabled':
            mbLoc = self.container.getLoc('Mother Brain')
            assert mbLoc is not None, "Mother Brain loc is None !"
            mbLoc.AccessFrom['Golden Four'] = self.getMotherBrainAccess()

        # save current AP
        previousAP = self.container.lastAP()

        self.loadPreset(self.conf.presetFileName)

        # add already collected items to smbm
        self.smbm.addItems(self.container.collectedItems())
        # always reset autotracker to false, then set it in importDump when importing autotracker state
        self.conf.autotracker = False

        if scope == 'item':
            if action == 'clear':
                self.clearItems(True)
            else:
                if action == 'add':
                    if self.conf.mode in ['plando', 'seedless', 'race', 'debug']:
                        if 'loc' in params:
                            if self.conf.mode == 'plando':
                                self.setItemAt(params['loc'], params['item'], params['hide'])
                            else:
                                itemName = params.get('item', 'Nothing')
                                if itemName is None:
                                    itemName = 'Nothing'
                                self.setItemAt(params['loc'], itemName, False)
                        else:
                            self.increaseItem(params['item'])
                    else:
                        # pickup item at locName
                        self.pickItemAt(params['loc'])
                elif action == 'remove':
                    if 'loc' in params:
                        self.removeItemAt(params['loc'])
                    elif 'count' in params:
                        # remove last collected item
                        self.rollbackTracker(params['count'])
                    else:
                        self.decreaseItem(params['item'])
                elif action == 'replace':
                    self.replaceItemAt(params['loc'], params['item'], params['hide'])
                elif action == 'toggle':
                    self.toggleItem(params['item'])
                elif action == 'upload_scav':
                    self.updatePlandoScavengerOrder(params['plandoScavengerOrder'])
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
        elif scope == 'door':
            if action == 'replace':
                doorName = params['doorName']
                newColor = params['newColor']
                DoorsManager.setColor(doorName, newColor)
            elif action == 'toggle':
                doorName = params['doorName']
                DoorsManager.switchVisibility(doorName)
            elif action == 'clear':
                DoorsManager.initTracker(self.romConf.doorsRando and self.conf.mode in ['standard', 'race'])
        elif scope == 'dump':
            if action == 'import':
                self.importDump(params["dump"])

        self.buildGraph(self.romConf)

        if scope == 'common':
            if action == 'save':
                return self.savePlando(params['lock'], params['escapeTimer'])
            elif action == 'randomize':
                self.randoPlando(params)

        # autotracker handles objectives
        if not self.conf.autotracker:
            self.checkGoals()

        # compute new available locations
        self.container.resetLocsDifficulty()
        self.computeLocationsDifficulty(self.container.majorLocations, startDiff=easy)

        # return them
        return self.dumpState()

    def checkGoals(self):
        # check if objectives can be completed
        self.newlyCompletedObjectives = []
        goals = self.objectives.checkGoals(self.smbm, self.container.lastAP())
        self.log.debug("objectives: {}".format(goals))
        for goalName, canClear in goals.items():
            if canClear:
                self.log.debug("objective possible: {}".format(goalName))
                goalObj = self.objectives.goals[goalName]
                requiredAPs, requiredLocs = goalObj.objCompletedFuncVisit(self.container.lastAP())
                visitedLocNames = set([loc.Name for loc in self.container.visitedLocations()])
                self.log.debug(f"remaining required locs: {[loc for loc in requiredLocs if loc not in visitedLocNames]}")
                # in tracker mode only check for required visited locations as we don't want to change user
                # current access point as it won't match with where he is in game.
                # as a result some objectives will be validated in the tracker before they are in game by the user,
                # it can be seen as a hint to the player that he should be able to complete the objective.
                if set(requiredLocs).issubset(visitedLocNames):
                    self.log.debug("complete objective {}".format(goalName))
                    self.container.completeObjective(goalName, self.container.lastAP(), self.container.lastArea(), None)
                    self.objectives.setGoalCompleted(goalName, True)
                    self.newlyCompletedObjectives.append("Completed objective: {}".format(goalName))
            else:
                self.log.debug("objective not possible: {}".format(goalName))

    def getLocNameFromAddress(self, address):
        return self.locsAddressName[address]

    def loadPlandoTransitions(self):
        # add escape transition
        transitionsAddr = self.romLoader.getPlandoTransitions(len(vanillaBossesTransitions) + len(vanillaTransitions) + 1)
        return GraphUtils.getTransitions(transitionsAddr)

    def loadPlandoLocs(self):
        # get the addresses of the already filled locs, with the correct order
        addresses = self.romLoader.getPlandoAddresses()

        # TODO::use container
        # create a copy of the locations to avoid removing locs from self.locations
        self.majorLocations = self.locations[:]

        for address in addresses:
            # TODO::compute only the difficulty of the current loc
            self.computeLocationsDifficulty(self.container.majorLocations)

            locName = self.getLocNameFromAddress(address)
            self.pickItemAt(locName)

    def fillPlandoLocs(self):
        self.pickup = Pickup("all")
        self.comeBack = ComeBack(self)

        # no time limitation
        self.runtimeLimiter = RuntimeLimiter(-1)

        # TODO::use container
        # backup
        locationsBck = self.locations[:]

        (self.difficulty, self.itemsOk) = self.computeDifficulty()

        # if last location is the gunship remove it as it's not handled by the tracker
        if any(loc.Name == 'Gunship' for loc in self.container.visitedLocations()):
            self.container.rollbackTracker(1, self.smbm)

        if self.itemsOk == False:
            # add remaining locs as sequence break
            for loc in self.container.majorLocations[:]:
                loc.difficulty = SMBool(True, -1)
                if loc.accessPoint is not None:
                    # take first ap of the loc
                    loc.accessPoint = list(loc.AccessFrom)[0]
                self.collectMajor(loc)

        self.locations = locationsBck

    def fillGraph(self):
        # add self looping transitions on unused acces points
        usedAPs = {}
        for (src, dst) in self.curGraphTransitions:
            usedAPs[src] = True
            usedAPs[dst] = True

        singleAPs = []
        for ap in Logic.accessPoints():
            if ap.isInternal() == True:
                continue

            if ap.Name not in usedAPs:
                singleAPs.append(ap.Name)

        transitions = self.curGraphTransitions[:]
        for apName in singleAPs:
            transitions.append((apName, apName))

        return transitions

    def randoPlando(self, parameters):
        # if all the locations are visited, do nothing
        if len(self.container.majorLocations) == 0:
            return

        plandoLocsItems = {}
        for loc in self.container.visitedLocations():
            plandoLocsItems[loc.Name] = loc.itemName

        plandoCurrent = {
            "locsItems": plandoLocsItems,
            "transitions": self.fillGraph(),
            "patches": RomPatches.ActivePatches,
            "doors": DoorsManager.serialize(),
            "forbiddenItems": parameters.get("forbiddenItems", []),
            "objectives": self.objectives.getGoalsList(),
            "tourian": self.romConf.tourian
        }

        plandoCurrentJson = json.dumps(plandoCurrent)

        (fd, jsonOutFileName) = tempfile.mkstemp()
        os.close(fd)

        from utils.utils import getPythonExec
        params = [
            getPythonExec(),  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
            '--runtime', '10',
            '--param', self.conf.presetFileName,
            '--output', jsonOutFileName,
            '--plandoRando', plandoCurrentJson,
            '--progressionSpeed', 'speedrun',
            '--minorQty', parameters["minorQty"],
            '--maxDifficulty', 'hardcore',
            '--energyQty', parameters["energyQty"],
            '--startLocation', self.romConf.startLocation
        ]

        import subprocess
        subprocess.call(params)

        with open(jsonOutFileName, 'r') as jsonFile:
            data = json.load(jsonFile)
        os.remove(jsonOutFileName)

        self.errorMsg = data["errorMsg"]

        # load the locations
        if "itemLocs" in data:
            self.clearItems(reload=True)
            itemsLocs = data["itemLocs"]

            # create a copy because we need self.locations to be full, else the state will be empty
            # TODO::is it still required ?
            #self.majorLocations = self.locations[:]

            # if tourian is disabled remove mother brain from itemsLocs if the rando added it
            if self.romConf.tourian == 'Disabled':
                if itemsLocs and itemsLocs[-1]["Location"]["Name"] == "Mother Brain":
                    itemsLocs.pop()

            for itemLoc in itemsLocs:
                locName = itemLoc["Location"]["Name"]
                loc = self.container.getLoc(locName)
                # we can have locations from non connected areas
                if "difficulty" in itemLoc["Location"]:
                    difficulty = itemLoc["Location"]["difficulty"]
                    smbool = SMBool(difficulty["bool"], difficulty["difficulty"], difficulty["knows"], difficulty["items"])
                    loc.difficulty = smbool
                    itemName = itemLoc["Item"]["Type"]
                    loc.itemName = itemName
                    loc.accessPoint = itemLoc["Location"]["accessPoint"]
                    self.collectMajor(loc)

    def savePlando(self, lock, escapeTimer):
        # store filled locations addresses in the ROM for next creating session
        errorMsg = ""
        from rando.Items import ItemManager
        locsItems = {}
        itemLocs = []
        for loc in self.container.visitedLocations():
            locsItems[loc.Name] = loc.itemName
        for loc in self.container.locations:
            if loc.Name in locsItems:
                itemLocs.append(ItemLocation(ItemManager.getItem(loc.itemName), loc))
            else:
                # put nothing items in unused locations
                itemLocs.append(ItemLocation(ItemManager.getItem("Nothing"), loc))

        # patch the ROM
        if lock is True:
            import random
            magic = random.randint(1, sys.maxsize)
        else:
            magic = None

        # plando is considered Full
        majorsSplit = self.romConf.masterMajorsSplit if self.romConf.masterMajorsSplit in ["FullWithHUD", "Scavenger"] else "Full"
        class FakeRandoSettings:
            def __init__(self):
                self.qty = {'energy': 'plando'}
                self.progSpeed = 'plando'
                self.progDiff = 'plando'
                self.restrictions = {'Suits': False, 'Morph': 'plando'}
                self.superFun = {}
        randoSettings = FakeRandoSettings()

        escapeAttr = None
        if self.romConf.escapeRando is True and escapeTimer != None:
            # convert from '03:00' to number of seconds
            escapeTimer = int(escapeTimer[0:2]) * 60 + int(escapeTimer[3:5])
            escapeAttr = {'Timer': escapeTimer, 'Animals': None, 'patches': []}

        progItemLocs = []
        if majorsSplit == "Scavenger":
            if not self.romConf.plandoScavengerOrder:
                return {"errorMsg": "Scavenger Hunt is empty, fill it before saving"}
            for locName in self.romConf.plandoScavengerOrder:
                loc = self.container.getLoc(locName)
                if locName in locsItems:
                    item = ItemManager.getItem(loc.itemName)
                else:
                    item = ItemManager.getItem("Nothing")
                    errorMsg = "Nothing at a Scavenger location, seed is unfinishable"
                progItemLocs.append(ItemLocation(Location=loc, Item=item))

        if RomPatches.ProgressiveSuits in RomPatches.ActivePatches:
            suitsMode = "Progressive"
        elif RomPatches.NoGravityEnvProtection in RomPatches.ActivePatches:
            suitsMode = "Balanced"
        else:
            suitsMode = "Vanilla"

        patches = ["Escape_Animals_Disable"]

        doors = GraphUtils.getDoorConnections(AccessGraph(Logic.accessPoints(), self.fillGraph()),
                                              self.romConf.areaRando, self.romConf.bossRando,
                                              self.romConf.escapeRando, False)

        from utils.version import displayedVersion
        from rom.rom_patches import groups, getPatchSet

        # individual layout/tweak patch handling
        layoutCustom = []
        areaLayoutCustom = []
        variaTweaksCustom = []
        def fillCustom(grp, custom):
            # FIXME would be better if we actually read patches from ROM? or access read patches?
            # because here we could miss individual layout patches with no logic impact
            for patchSet in groups[grp]:
                if all(rp in RomPatches.ActivePatches for rp in getPatchSet(patchSet, RomFlavor.flavor).get('logic', [])):
                    custom.append(patchSet)
        fillCustom('layout', layoutCustom)
        fillCustom('areaLayout', areaLayoutCustom)
        fillCustom('variaTweaks', variaTweaksCustom)
        patcherSettings = {
            "isPlando": True,
            "majorsSplit": majorsSplit,
            "startLocation": self.romConf.startLocation,
            "optionalPatches": patches,
            "layout": len(layoutCustom) > 0,
            "layoutCustom": layoutCustom,
            "suitsMode": suitsMode,
            "area": self.romConf.areaRando,
            "boss": self.romConf.bossRando,
            "areaLayout": len(areaLayoutCustom) > 0,
            "areaLayoutCustom": areaLayoutCustom,
            "escapeAttr": escapeAttr,
            "variaTweaks": len(variaTweaksCustom) > 0,
            "variaTweaksCustom": variaTweaksCustom,
            "nerfedCharge": RomPatches.NerfedCharge in RomPatches.ActivePatches,
            "nerfedRainbowBeam": RomPatches.NerfedRainbowBeam in RomPatches.ActivePatches,
            # these settings are kept to False or None to keep what's in base ROM
            "ctrlDict": None,
            "moonWalk": False,
            "debug": False,
            ##
            "revealMap": self.romConf.revealMap,
            "escapeRandoRemoveEnemies": self.romConf.escapeRandoRemoveEnemies,
            "minimizerN": 100 if RomPatches.NoGadoras in RomPatches.ActivePatches else None,
            "tourian": self.romConf.tourian,
            "doorsColorsRando": DoorsManager.isRandom(),
            "vanillaObjectives": self.objectives.isVanilla(),
            "seed": None,
            "randoSettings": randoSettings,
            "doors": doors,
            "displayedVersion": displayedVersion,
            "itemLocs": itemLocs,
            "progItemLocs": progItemLocs,
            "plando": {
                "graphTrans": self.curGraphTransitions,
                "maxTransitions": len(vanillaBossesTransitions) + len(vanillaTransitions),
                "visitedLocations": self.container.visitedLocations(),
                "additionalETanks": self.romConf.additionalETanks
            }
        }

        romPatcher = RomPatcher(settings=patcherSettings, magic=magic)
        romPatcher.patchRom()

        data = romPatcher.romFile.data
        preset = os.path.splitext(os.path.basename(self.conf.presetFileName))[0]
        seedCode = 'FX'
        if self.romConf.bossRando:
            seedCode = 'B'+seedCode
        if DoorsManager.isRandom():
            seedCode = 'D'+seedCode
        if self.romConf.areaRando:
            seedCode = 'A'+seedCode
        from time import gmtime, strftime
        fileName = 'VARIA_Plandomizer_{}{}_{}.sfc'.format(seedCode, strftime("%Y%m%d%H%M%S", gmtime()), preset)
        data["fileName"] = fileName
        # error msg in json to be displayed by the web site
        data["errorMsg"] = errorMsg

        return data

    def locNameInternal2Web(self, locName):
        return removeChars(locName, " ,()-")

    def locNameWeb2Internal(self, locNameWeb):
        return self.locsWeb2Internal[locNameWeb]

    def apNameInternal2Web(self, apName):
        return apName[0].lower() + removeChars(apName[1:], " ")

    def getWebLoc(self, locNameWeb):
        locName = self.locNameWeb2Internal(locNameWeb)
        return self.container.getLoc(locName)

    def pickItemAt(self, locNameWeb):
        # collect new item at newLoc
        loc = self.getWebLoc(locNameWeb)

        # check that location has not already been visited
        if loc in self.container.visitedLocations():
            self.errorMsg = "Location '{}' has already been visited".format(loc.Name)
            return

        if loc.difficulty is None or not loc.difficulty:
            # sequence break
            loc.difficulty = SMBool(True, -1)
        if loc.accessPoint is None:
            # take first ap of the loc
            loc.accessPoint = list(loc.AccessFrom)[0]
        self.collectMajor(loc)

    def setItemAt(self, locNameWeb, itemName, hide):
        # set itemName at locName

        loc = self.getWebLoc(locNameWeb)

        # check if location has not already been visited
        if loc in self.container.visitedLocations():
            self.errorMsg = "Location {} has already been visited".format(loc.Name)
            return

        # plando mode
        loc.itemName = itemName

        if loc.difficulty is None:
            # sequence break
            loc.difficulty = SMBool(True, -1)
        if loc.accessPoint is None:
            # take first ap of the loc
            loc.accessPoint = list(loc.AccessFrom)[0]

        if hide is True:
            loc.Visibility = 'Hidden'

        if loc in self.container.majorLocations:
            self.collectMajor(loc, itemName=itemName)

    def replaceItemAt(self, locNameWeb, itemName, hide):
        # replace itemName at locName
        loc = self.getWebLoc(locNameWeb)
        oldItemName = loc.itemName

        # check that location not already been visited
        if loc not in self.container.visitedLocations():
            self.errorMsg = "Location {} has not been visited".format(loc.Name)
            return

        # major item can be set multiple times in plando mode
        count = self.container.collectedItems().count(oldItemName)
        isCount = self.smbm.isCountItem(oldItemName)

        # update item after we check the count
        loc.itemName = itemName

        # update smbm if count item or major was only there once
        if isCount is True or count == 1:
            self.smbm.removeItem(oldItemName)

        if hide is True:
            loc.Visibility = 'Hidden'
        elif loc.CanHidden is True and loc.Visibility == 'Hidden':
            # the loc was previously hidden, set it back to visible
            loc.Visibility = 'Visible'

        self.smbm.addItem(itemName)

    def removeItemAt(self, locNameWeb):
        loc = self.getWebLoc(locNameWeb)

        if loc not in self.container.visitedLocations():
            self.errorMsg = "Location '{}' has not been visited".format(loc.Name)
            return

        # removeItemAt is only used from the tracker, so all the locs are in majorLocations
        self.container.cancelTrackerLocation(loc, self.smbm)

        # in autotracker items are read from memory
        if self.conf.autotracker:
            return

        # item
        item = loc.itemName

        # if multiple majors in plando mode, remove it from smbm only when it's the last occurence of it
        if self.smbm.isCountItem(item):
            self.smbm.removeItem(item)
        else:
            if item not in self.container.collectedItems():
                self.smbm.removeItem(item)

    def rollbackTracker(self, count):
        self.container.rollbackTracker(count, self.smbm)

    def increaseItem(self, item):
        self.container.increaseInventoryItem(item)
        self.smbm.addItem(item)

    def decreaseItem(self, item):
        if self.container.hasItemInInventory(item):
            self.container.decreaseInventoryItem(item)
            self.smbm.removeItem(item)

    def toggleItem(self, item):
        # add or remove a major item
        if self.container.hasItemInInventory(item):
            self.container.decreaseInventoryItem(item)
            self.smbm.removeItem(item)
        else:
            self.container.increaseInventoryItem(item)
            self.smbm.addItem(item)

    def clearItems(self, reload=False):
        self.container.reset(reload)
        self.smbm.resetItems()
        self.objectives.resetCompletedGoals()

    def updatePlandoScavengerOrder(self, plandoScavengerOrder):
        self.romConf.plandoScavengerOrder = plandoScavengerOrder

    def addTransition(self, startPoint, endPoint):
        # already check in controller if transition is valid for seed
        self.curGraphTransitions.append((startPoint, endPoint))

    def cancelLastTransition(self):
        if self.romConf.areaRando == True and self.romConf.bossRando == True:
            if len(self.curGraphTransitions) > 0:
                self.curGraphTransitions.pop()
        elif self.romConf.areaRando == True:
            if len(self.curGraphTransitions) > len(self.romConf.bossTransitions) + (1 if self.romConf.escapeRando == False else 0):
                self.curGraphTransitions.pop()
        elif self.romConf.bossRando == True:
            print("len cur graph: {} len area: {} len escape: {} len sum: {}".format(len(self.curGraphTransitions), len(self.romConf.areaTransitions), 1 if self.romConf.escapeRando == False else 0, len(self.romConf.areaTransitions) + (1 if self.romConf.escapeRando == False else 0)))
            if len(self.curGraphTransitions) > len(self.romConf.areaTransitions) + (1 if self.romConf.escapeRando == False else 0):
                self.curGraphTransitions.pop()
        elif self.romConf.escapeRando == True:
            if len(self.curGraphTransitions) > len(self.romConf.areaTransitions) + len(self.romConf.bossTransitions):
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
        if self.romConf.areaRando == True and self.romConf.bossRando == True and self.romConf.escapeRando == True:
            if len(self.curGraphTransitions) == 0:
                return
        elif self.romConf.areaRando == True and self.romConf.escapeRando == False:
            if len(self.curGraphTransitions) == len(self.romConf.bossTransitions) + len(self.romConf.escapeTransition):
                return
            elif [startPoint, endPoint] in self.romConf.bossTransitions or [endPoint, startPoint] in self.romConf.bossTransitions:
                return
            elif [startPoint, endPoint] in self.romConf.escapeTransition or [endPoint, startPoint] in self.romConf.escapeTransition:
                return
        elif self.romConf.bossRando == True and self.romConf.escapeRando == False:
            if len(self.curGraphTransitions) == len(self.romConf.areaTransitions) + len(self.romConf.escapeTransition):
                return
            elif [startPoint, endPoint] in self.romConf.areaTransitions or [endPoint, startPoint] in self.romConf.areaTransitions:
                return
            elif [startPoint, endPoint] in self.romConf.escapeTransition or [endPoint, startPoint] in self.romConf.escapeTransition:
                return
        elif self.romConf.areaRando == True and self.romConf.escapeRando == True:
            if len(self.curGraphTransitions) == len(self.romConf.bossTransitions):
                return
            elif [startPoint, endPoint] in self.romConf.bossTransitions or [endPoint, startPoint] in self.romConf.bossTransitions:
                return
        elif self.romConf.bossRando == True and self.romConf.escapeRando == True:
            if len(self.curGraphTransitions) == len(self.romConf.areaTransitions):
                return
            elif [startPoint, endPoint] in self.romConf.areaTransitions or [endPoint, startPoint] in self.romConf.areaTransitions:
                return
        elif self.romConf.escapeRando == True and self.romConf.areaRando == False and self.romConf.bossRando == False:
            if len(self.curGraphTransitions) == len(self.romConf.areaTransitions) + len(self.romConf.bossTransitions):
                return
            elif [startPoint, endPoint] in self.romConf.areaTransitions or [endPoint, startPoint] in self.romConf.areaTransitions:
                return
            elif [startPoint, endPoint] in self.romConf.bossTransitions or [endPoint, startPoint] in self.romConf.bossTransitions:
                return

        # remove transition
        self.curGraphTransitions.pop(i)

    def clearTransitions(self):
        if self.romConf.areaRando == True and self.romConf.bossRando == True:
            self.curGraphTransitions = []
        elif self.romConf.areaRando == True:
            self.curGraphTransitions = self.romConf.bossTransitions[:]
        elif self.romConf.bossRando == True:
            self.curGraphTransitions = self.romConf.areaTransitions[:]
        else:
            self.curGraphTransitions = self.romConf.bossTransitions + self.romConf.areaTransitions

        if self.romConf.escapeRando == False:
            self.curGraphTransitions += self.romConf.escapeTransition

    def getDiffThreshold(self):
        # in interactive solver we don't have the max difficulty parameter
        epsilon = 0.001
        return hard - epsilon

    # byteIndex is area index
    bossBitMasks = {
        "Kraid": {"byteIndex": 0x01, "bitMask": 0x01},
        "Ridley": {"byteIndex": 0x02, "bitMask": 0x01},
        "Phantoon": {"byteIndex": 0x03, "bitMask": 0x01},
        "Draygon": {"byteIndex": 0x04, "bitMask": 0x01},
        "Mother Brain": {"byteIndex": 0x05, "bitMask": 0x02},
        "Spore Spawn": {"byteIndex": 0x01, "bitMask": 0x02},
        "Crocomire": {"byteIndex": 0x02, "bitMask": 0x02},
        "Botwoon": {"byteIndex": 0x04, "bitMask": 0x02},
        "Golden Torizo": {"byteIndex": 0x02, "bitMask": 0x04}
    }

    eventsBitMasks = {}

    inventoryBitMasks = {
        'Varia': {"byteIndex": 0x0, "bitMask": 0x1},
        'SpringBall': {"byteIndex": 0x0, "bitMask": 0x2},
        'Morph': {"byteIndex": 0x0, "bitMask": 0x4},
        'ScrewAttack': {"byteIndex": 0x0, "bitMask": 0x8},
        'Gravity': {"byteIndex": 0x0, "bitMask": 0x20},
        'HiJump': {"byteIndex": 0x1, "bitMask": 0x1},
        'SpaceJump': {"byteIndex": 0x1, "bitMask": 0x2 },
        'Bomb': {"byteIndex": 0x1, "bitMask": 0x10},
        'SpeedBooster': {"byteIndex": 0x1, "bitMask": 0x20},
        'Grapple': {"byteIndex": 0x1, "bitMask": 0x40},
        'XRayScope': {"byteIndex": 0x1, "bitMask": 0x80},
        'Wave': {"byteIndex": 0x4, "bitMask": 0x1},
        'Ice': {"byteIndex": 0x4, "bitMask": 0x2},
        'Spazer': {"byteIndex": 0x4, "bitMask": 0x4},
        'Plasma': {"byteIndex": 0x4, "bitMask": 0x8},
        'Charge': {"byteIndex": 0x5, "bitMask": 0x10},
        'ETank': {"byteIndex": 0x6},
        'Missile': {"byteIndex": 0xA},
        'Super': {"byteIndex": 0xE},
        'PowerBomb': {"byteIndex": 0x12},
        'Reserve': {"byteIndex": 0x16},
    }

    areaAccessPoints = {
        "vanilla": vanilla_areaAccessPoints,
        "mirror": mirror_areaAccessPoints
    }

    bossAccessPoints = {
        "vanilla": vanilla_bossAccessPoints,
        "mirror": mirror_bossAccessPoints
    }

    escapeAccessPoints = {
        "vanilla": vanilla_escapeAccessPoints,
        "mirror": mirror_escapeAccessPoints
    }

    nothingScreens = {
        "vanilla": vanilla_itemLocations,
        "mirror": mirror_itemLocations
    }

    doorsScreen = {
        "vanilla": vanilla_doors,
        "mirror": mirror_doors
    }

    mapOffsetEnum = {
        "Crateria": 0,
        "Brinstar": 0x100,
        "Norfair": 0x200,
        "WreckedShip": 0x300,
        "Maridia": 0x400,
        "Tourian": 0x500
    }

    def importDump(self, dumpData):
        # to not update inventory when adding/removing locations
        self.conf.autotracker = True

        # first update current access point
        self.container.updateOverrideAP(dumpData["newAP"])

        dataEnum = {
            "state": '1',
            "map": '2',
            "curMap": '3',
            "samus": '4',
            "items": '5',
            "boss": '6',
            "events": '7',
            "inventory": '8',
        }

        currentState = dumpData["currentState"]
        bosses = []

        # add locations after having added new items to inventory to avoid seq break locations
        locationsToAdd = []

        for dataType, offset in dumpData["stateDataOffsets"].items():
            if dataType == dataEnum["items"]:
                # get item data, loop on all locations to check if they have been visited
                for loc in self.container.locations:
                    # loc id is used to index in the items data, boss locations don't have an Id.
                    # for scav hunt ridley loc now have an id, so also check if loc is a boss loc.
                    if loc.Id is None or loc.isBoss():
                        continue
                    # nothing locs are handled later
                    if loc.itemName == 'Nothing':
                        continue
                    byteIndex = loc.Id >> 3
                    bitMask = 0x01 << (loc.Id & 7)
                    if currentState[offset + byteIndex] & bitMask != 0:
                        if loc not in self.container.visitedLocations():
                            locationsToAdd.append(self.locNameInternal2Web(loc.Name))
                    else:
                        if loc in self.container.visitedLocations():
                            # TODO::loc not removed
                            self.removeItemAt(self.locNameInternal2Web(loc.Name))
            elif dataType == dataEnum["boss"]:
                for boss, bossData in self.bossBitMasks.items():
                    byteIndex = bossData["byteIndex"]
                    bitMask = bossData["bitMask"]
                    loc = self.container.getLoc(boss)
                    if currentState[offset + byteIndex] & bitMask != 0:
                        # as we clear collected items we have to add bosses back.
                        # some bosses have a space in their names, remove it.
                        bosses.append(boss.replace(' ', ''))

                        # in tourian disabled mother brain is not available, but it gets auto killed during escape
                        if loc not in self.container.visitedLocations() and loc in self.container.majorLocations:
                            locationsToAdd.append(self.locNameInternal2Web(loc.Name))
                    else:
                        if loc in self.container.visitedLocations():
                            self.removeItemAt(self.locNameInternal2Web(loc.Name))

            # Inventory
            elif dataType == dataEnum["inventory"]:
                # Clear collected items if loading from game state.
                self.container.resetInventoryItems()
                self.smbm.resetItems()

                # put back bosses
                for boss in bosses:
                    self.container.increaseInventoryItem(boss)
                    self.smbm.addItem(boss)

                for item, itemData in self.inventoryBitMasks.items():
                    byteIndex = itemData["byteIndex"]
                    loc = offset + byteIndex
                    # For two byte values, read little endian value.
                    if item in ("ETank", "Reserve", "Missile", "Super", "PowerBomb"):
                        val = currentState[loc] + (currentState[loc + 1] * 256)
                    else:
                        val = currentState[loc]

                    if item == "ETank":
                        tanks = int((val - 99) / 100)
                        for _ in range(tanks):
                            self.container.increaseInventoryItem(item)
                            self.smbm.addItem(item)
                    elif item == "Reserve":
                        tanks = int(val / 100)
                        for _ in range(tanks):
                            self.container.increaseInventoryItem(item)
                            self.smbm.addItem(item)
                    elif item in ("Missile", "Super", "PowerBomb"):
                        packs = int(val / 5)
                        for _ in range(packs):
                            self.container.increaseInventoryItem(item)
                            self.smbm.addItem(item)
                    else:
                        bitMask = itemData["bitMask"]
                        if val & bitMask != 0:
                            self.container.increaseInventoryItem(item)
                            self.smbm.addItem(item)

            elif dataType == dataEnum["map"]:
                if self.romConf.areaRando or self.romConf.bossRando or self.romConf.escapeRando:
                    availAPs = set()
                    for apName, apData in self.areaAccessPoints[self.logic].items():
                        if self.isElemAvailable(currentState, offset, apData):
                            availAPs.add(apName)
                    for apName, apData in self.bossAccessPoints[self.logic].items():
                        if self.isElemAvailable(currentState, offset, apData):
                            availAPs.add(apName)
                    for apName, apData in self.escapeAccessPoints[self.logic].items():
                        if self.isElemAvailable(currentState, offset, apData):
                            availAPs.add(apName)

                    # static transitions
                    if self.romConf.areaRando == True and self.romConf.bossRando == True:
                        staticTransitions = []
                        possibleTransitions = self.romConf.bossTransitions + self.romConf.areaTransitions
                    elif self.romConf.areaRando == True:
                        staticTransitions = self.romConf.bossTransitions[:]
                        possibleTransitions = self.romConf.areaTransitions[:]
                    elif self.romConf.bossRando == True:
                        staticTransitions = self.romConf.areaTransitions[:]
                        possibleTransitions = self.romConf.bossTransitions[:]
                    else:
                        staticTransitions = self.romConf.bossTransitions + self.romConf.areaTransitions
                        possibleTransitions = []
                    if self.romConf.escapeRando == False:
                        staticTransitions += self.romConf.escapeTransition
                    else:
                        possibleTransitions += self.romConf.escapeTransition

                    # remove static transitions from current transitions
                    dynamicTransitions = self.curGraphTransitions[:]
                    for transition in self.curGraphTransitions:
                        if transition in staticTransitions:
                            dynamicTransitions.remove(transition)

                    # remove dynamic transitions not visited
                    for transition in dynamicTransitions:
                        if transition[0] not in availAPs and transition[1] not in availAPs:
                            self.curGraphTransitions.remove(transition)

                    # for fast check of current transitions
                    fastTransCheck = {}
                    for transition in self.curGraphTransitions:
                        fastTransCheck[transition[0]] = transition[1]
                        fastTransCheck[transition[1]] = transition[0]

                    # add new transitions
                    for transition in possibleTransitions:
                        start = transition[0]
                        end = transition[1]
                        # available transition
                        if start in availAPs and end in availAPs:
                            # transition not already in current transitions
                            if start not in fastTransCheck and end not in fastTransCheck:
                                self.curGraphTransitions.append(transition)

                if self.romConf.hasNothing:
                    # get locs with nothing
                    locsNothing = [loc for loc in self.container.locations if loc.itemName == 'Nothing']
                    for loc in locsNothing:
                        locData = self.nothingScreens[self.logic][loc.Name]
                        if self.isElemAvailable(currentState, offset, locData):
                            # nothing has been seen, check if loc is already visited
                            if not loc in self.container.visitedLocations():
                                # visit it
                                locationsToAdd.append(self.locNameInternal2Web(loc.Name))
                        else:
                            # nothing not yet seed, check if loc is already visited
                            if loc in self.container.visitedLocations():
                                # unvisit it
                                self.removeItemAt(self.locNameInternal2Web(loc.Name))
                if self.romConf.doorsRando:
                    # get currently hidden / revealed doors names in sets
                    (hiddenDoors, revealedDoor) = DoorsManager.getDoorsState()
                    for doorName in hiddenDoors:
                        # check if door is still hidden
                        doorData = self.doorsScreen[self.logic][doorName]
                        if self.isElemAvailable(currentState, offset, doorData):
                            DoorsManager.switchVisibility(doorName)
                    for doorName in revealedDoor:
                        # check if door is still visible
                        doorData = self.doorsScreen[self.logic][doorName]
                        if not self.isElemAvailable(currentState, offset, doorData):
                            DoorsManager.switchVisibility(doorName)
            elif dataType == dataEnum["events"]:
                self.newlyCompletedObjectives = []
                goalsList = self.objectives.getGoalsList()
                objectivesState = self.objectives.getState()
                goalsCompleted = objectivesState["goals"]
                goalsCompleted = list(goalsCompleted.values())
                for i, (event, eventData) in enumerate(self.romConf.eventsBitMasks.items()):
                    assert i == event, "{}th event has code {} instead of {}".format(i, event, i)
                    if i >= len(goalsList):
                        continue
                    byteIndex = eventData["byteIndex"]
                    bitMask = eventData["bitMask"]
                    goalName = goalsList[i]
                    goalCompleted = goalsCompleted[i]
                    if currentState[offset + byteIndex] & bitMask != 0:
                        # set goal completed
                        if not goalCompleted:
                            self.objectives.setGoalCompleted(goalName, True)
                            self.newlyCompletedObjectives.append("Completed objective: {}".format(goalName))
                    else:
                        # set goal uncompleted
                        if goalCompleted:
                            self.objectives.setGoalCompleted(goalName, False)

                if self.romConf.objectivesHiddenOption:
                    # also check objectives revealed event
                    # !VARIA_event_base #= $0080
                    # !objectives_revealed_event #= !VARIA_event_base+33
                    VARIA_event_base = 0x80
                    objectives_revealed_event = VARIA_event_base+33
                    byteIndex = objectives_revealed_event >> 3
                    bitMask = 1 << (objectives_revealed_event & 7)
                    self.romConf.objectivesHidden = not bool(currentState[offset + byteIndex] & bitMask)

        if locationsToAdd:
            # recompute locations availability with the new inventory
            self.buildGraph(self.romConf)
            self.container.resetLocsDifficulty()
            self.computeLocationsDifficulty(self.container.majorLocations, startDiff=easy)

            for locNameWeb in locationsToAdd:
                self.pickItemAt(locNameWeb)

    def isElemAvailable(self, currentState, offset, apData):
        byteIndex = apData["byteIndex"]
        bitMask = apData["bitMask"]
        return currentState[offset + byteIndex + self.mapOffsetEnum[apData["area"]]] & bitMask != 0
