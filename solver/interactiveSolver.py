import sys, json, os, tempfile

from solver.commonSolver import CommonSolver
from logic.smbool import SMBool
from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.helpers import Pickup
from rom.rompatcher import RomPatcher
from rom.rom_patches import RomPatches
from rom.flavor import RomFlavor
from graph.graph import AccessGraphSolver as AccessGraph
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, GraphUtils
from graph.location import define_location
from utils.utils import removeChars
from solver.conf import Conf
from utils.parameters import hard, infinity
from solver.solverState import SolverState
from solver.comeback import ComeBack
from rando.ItemLocContainer import ItemLocation
from utils.doorsmanager import DoorsManager
from logic.logic import Logic
from utils.objectives import Objectives
from graph.vanilla.map_tiles import areaAccessPoints as vanilla_areaAccessPoints, bossAccessPoints as vanilla_bossAccessPoints, escapeAccessPoints as vanilla_escapeAccessPoints, itemLocations as vanilla_itemLocations, doors as vanilla_doors
from graph.mirror.map_tiles import areaAccessPoints as mirror_areaAccessPoints, bossAccessPoints as mirror_bossAccessPoints, escapeAccessPoints as mirror_escapeAccessPoints, itemLocations as mirror_itemLocations, doors as mirror_doors
import utils.log

class InteractiveSolver(CommonSolver):
    def __init__(self, shm, logic):
        self.interactive = True
        self.errorMsg = ""
        self.checkDuplicateMajor = False
        self.vcr = None
        self.log = utils.log.get('Solver')

        # only available since python 3.8, so import it here to keep >= 3.6 compatibility for CLI
        from utils.shm import SHM
        self.shm = SHM(shm)
        self.firstLogFile = None

        self.logic = logic
        Logic.factory(self.logic)
        RomFlavor.factory()
        self.locations = Logic.locations

        (self.locsAddressName, self.locsWeb2Internal) = self.initLocsAddressName()
        self.transWeb2Internal = self.initTransitionsName()

        Conf.difficultyTarget = infinity

        self.objectives = Objectives()

        # no time limitation
        self.runtimeLimit_s = 0

        # used by auto tracker to know how many locs have changed
        self.locDelta = 0

    def initLocsAddressName(self):
        addressName = {}
        web2Internal = {}
        for loc in Logic.locations:
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
        state = SolverState(self.debug)
        state.fromSolver(self)

        self.shm.writeMsgJson(state.get())
        self.shm.finish(False)

    def initialize(self, mode, rom, presetFileName, magic, fill, startLocation):
        # load rom and preset, return first state
        self.debug = mode == "debug"
        self.mode = mode
        if self.mode != "seedless":
            self.seed = os.path.basename(os.path.splitext(rom)[0])+'.sfc'
        else:
            self.seed = "seedless"

        self.smbm = SMBoolManager()

        self.presetFileName = presetFileName
        self.loadPreset(self.presetFileName)

        self.loadRom(rom, interactive=True, magic=magic, startLocation=startLocation)
        # in plando/tracker always consider that we're doing full
        self.majorsSplit = 'Full'

        # hide doors
        if self.doorsRando and mode in ['standard', 'race']:
            DoorsManager.initTracker()

        self.clearItems()

        # in debug mode don't load plando locs/transitions
        if self.mode == 'plando' and self.debug == False:
            if fill == True:
                # load the source seed transitions and items/locations
                self.curGraphTransitions = self.bossTransitions + self.areaTransitions + self.escapeTransition
                self.buildGraph()
                self.fillPlandoLocs()
            else:
                if self.areaRando == True or self.bossRando == True:
                    plandoTrans = self.loadPlandoTransitions()
                    if len(plandoTrans) > 0:
                        self.curGraphTransitions = plandoTrans
                    self.buildGraph()

                self.loadPlandoLocs()

        # if tourian is disabled remove mother brain location
        if self.tourian == 'Disabled':
            mbLoc = self.getLoc('Mother Brain')
            self.locations.remove(mbLoc)

        # compute new available locations
        self.computeLocationsDifficulty(self.majorLocations)
        self.checkGoals()

        self.dumpState()

    def iterate(self, scope, action, params):
        self.debug = params["debug"]
        self.smbm = SMBoolManager()

        state = SolverState()
        state.set(self.shm.readMsgJson())
        state.toSolver(self)
        self.objectives.setSolverMode(self)

        # save current AP
        previousAP = self.lastAP

        self.loadPreset(self.presetFileName)

        # add already collected items to smbm
        self.smbm.addItems(self.collectedItems)

        if scope == 'item':
            if action == 'clear':
                self.clearItems(True)
            else:
                if action == 'add':
                    if self.mode in ['plando', 'seedless', 'race', 'debug']:
                        if params['loc'] != None:
                            if self.mode == 'plando':
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
                        self.cancelLastItems(params['count'])
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
                DoorsManager.initTracker()
        elif scope == 'dump':
            if action == 'import':
                self.importDump(params["dump"])

        self.buildGraph()

        if scope == 'common':
            if action == 'save':
                return self.savePlando(params['lock'], params['escapeTimer'])
            elif action == 'randomize':
                self.randoPlando(params)

        rewindLimit = self.locDelta if scope == 'dump' and self.locDelta > 0 else 1
        lastVisitedLocs = []
        # if last loc added was a sequence break, recompute its difficulty,
        # as it may be available with the newly placed item.
        # generalize it for auto-tracker where we can add more than one loc at once.
        if len(self.visitedLocations) > 0:
            for i in range(1, rewindLimit+1):
                if i > len(self.visitedLocations):
                    break
                else:
                    loc = self.visitedLocations[-i]
                    # check that the ap of the loc is available from the previous ap,
                    # else it may set loc diff to easy
                    if (loc.difficulty.difficulty == -1 and
                        loc.accessPoint is not None and
                        self.areaGraph.canAccess(self.smbm, previousAP, loc.accessPoint, Conf.difficultyTarget)):
                        lastVisitedLocs.append(loc)

            for loc in lastVisitedLocs:
                self.visitedLocations.remove(loc)
                self.majorLocations.append(loc)

        # compute new available locations
        self.clearLocs(self.majorLocations)
        self.computeLocationsDifficulty(self.majorLocations)

        while True:
            remainLocs = []
            okLocs = []

            for loc in lastVisitedLocs:
                if loc.difficulty == False:
                    remainLocs.append(loc)
                else:
                    okLocs.append(loc)

            if len(remainLocs) == len(lastVisitedLocs):
                # all remaining locs are seq break
                for loc in lastVisitedLocs:
                    self.majorLocations.remove(loc)
                    self.visitedLocations.append(loc)
                    if loc.difficulty == False:
                        # if the loc is still sequence break, put it back as sequence break
                        loc.difficulty = SMBool(True, -1)
                break
            else:
                # add available locs
                for loc in okLocs:
                    lastVisitedLocs.remove(loc)
                    self.majorLocations.remove(loc)
                    self.visitedLocations.append(loc)

            # compute again
            self.clearLocs(self.majorLocations)
            self.computeLocationsDifficulty(self.majorLocations)

        # autotracker handles objectives
        if not (scope == 'dump' and action == 'import'):
            self.checkGoals()

        # return them
        self.dumpState()

    def checkGoals(self):
        # check if objectives can be completed
        self.newlyCompletedObjectives = []
        goals = self.objectives.checkGoals(self.smbm, self.lastAP)
        for goalName, canClear in goals.items():
            if canClear:
                self.objectives.setGoalCompleted(goalName, True)
                self.newlyCompletedObjectives.append("Completed objective: {}".format(goalName))

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
        locationsBck = self.locations[:]

        self.lastAP = self.startLocation
        self.lastArea = self.startArea
        (self.difficulty, self.itemsOk) = self.computeDifficulty()

        if self.itemsOk == False:
            # add remaining locs as sequence break
            for loc in self.majorLocations[:]:
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
        for ap in Logic.accessPoints:
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
        if len(self.majorLocations) == 0:
            return

        plandoLocsItems = {}
        for loc in self.visitedLocations:
            plandoLocsItems[loc.Name] = loc.itemName

        plandoCurrent = {
            "locsItems": plandoLocsItems,
            "transitions": self.fillGraph(),
            "patches": RomPatches.ActivePatches,
            "doors": DoorsManager.serialize(),
            "forbiddenItems": parameters["forbiddenItems"],
            "objectives": self.objectives.getGoalsList(),
            "tourian": self.tourian
        }

        plandoCurrentJson = json.dumps(plandoCurrent)

        (fd, jsonOutFileName) = tempfile.mkstemp()
        os.close(fd)

        from utils.utils import getPythonExec
        params = [
            getPythonExec(),  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
            '--runtime', '10',
            '--param', self.presetFileName,
            '--output', jsonOutFileName,
            '--plandoRando', plandoCurrentJson,
            '--progressionSpeed', 'speedrun',
            '--minorQty', parameters["minorQty"],
            '--maxDifficulty', 'hardcore',
            '--energyQty', parameters["energyQty"],
            '--startLocation', self.startLocation
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
            self.majorLocations = self.locations[:]

            # if tourian is disabled remove mother brain from itemsLocs if the rando added it
            if self.tourian == 'Disabled':
                if itemsLocs and itemsLocs[-1]["Location"]["Name"] == "Mother Brain":
                    itemsLocs.pop()

            for itemLoc in itemsLocs:
                locName = itemLoc["Location"]["Name"]
                loc = self.getLoc(locName)
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
        for loc in self.visitedLocations:
            locsItems[loc.Name] = loc.itemName
        for loc in self.locations:
            if loc.Name in locsItems:
                itemLocs.append(ItemLocation(ItemManager.getItem(loc.itemName), loc))
            else:
                # put nothing items in unused locations
                itemLocs.append(ItemLocation(ItemManager.getItem("Nothing"), loc))

        # patch the ROM
        if lock == True:
            import random
            magic = random.randint(1, sys.maxsize)
        else:
            magic = None

        # plando is considered Full
        majorsSplit = self.masterMajorsSplit if self.masterMajorsSplit in ["FullWithHUD", "Scavenger"] else "Full"
        class FakeRandoSettings:
            def __init__(self):
                self.qty = {'energy': 'plando'}
                self.progSpeed = 'plando'
                self.progDiff = 'plando'
                self.restrictions = {'Suits': False, 'Morph': 'plando'}
                self.superFun = {}
        randoSettings = FakeRandoSettings()

        escapeAttr = None
        if self.escapeRando == True and escapeTimer != None:
            # convert from '03:00' to number of seconds
            escapeTimer = int(escapeTimer[0:2]) * 60 + int(escapeTimer[3:5])
            escapeAttr = {'Timer': escapeTimer, 'Animals': None, 'patches': []}

        progItemLocs = []
        if majorsSplit == "Scavenger":
            def getLoc(locName):
                for loc in self.locations:
                    if loc.Name == locName:
                        return loc
            for locName in self.plandoScavengerOrder:
                loc = getLoc(locName)
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

        doors = GraphUtils.getDoorConnections(AccessGraph(Logic.accessPoints, self.fillGraph()), self.areaRando,
                                              self.bossRando, self.escapeRando, False)

        from utils.version import displayedVersion

        patcherSettings = {
            "isPlando": True,
            "majorsSplit": majorsSplit,
            "startLocation": self.startLocation,
            "optionalPatches": patches,
            "layout": RomPatches.MoatShotBlock in RomPatches.ActivePatches,
            "suitsMode": suitsMode,
            "area": self.areaRando,
            "boss": self.bossRando,
            "areaLayout": RomPatches.AreaRandoGatesOther in RomPatches.ActivePatches,
            "escapeAttr": escapeAttr,
            # these settings are kept to False or None to keep what's in base ROM
            "variaTweaks": False,
            "nerfedCharge": False,
            "nerfedRainbowBeam": False,
            "revealMap": False,
            "escapeRandoRemoveEnemies": None,
            "ctrlDict": None,
            "moonWalk": False,
            "debug": False,
            ##
            "minimizerN": 100 if RomPatches.NoGadoras in RomPatches.ActivePatches else None,
            "tourian": self.tourian,
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
                "visitedLocations": self.visitedLocations,
                "additionalETanks": self.additionalETanks
            }
        }

        romPatcher = RomPatcher(settings=patcherSettings, magic=magic)
        romPatcher.patchRom()

        data = romPatcher.romFile.data
        preset = os.path.splitext(os.path.basename(self.presetFileName))[0]
        seedCode = 'FX'
        if self.bossRando == True:
            seedCode = 'B'+seedCode
        if DoorsManager.isRandom():
            seedCode = 'D'+seedCode
        if self.areaRando == True:
            seedCode = 'A'+seedCode
        from time import gmtime, strftime
        fileName = 'VARIA_Plandomizer_{}{}_{}.sfc'.format(seedCode, strftime("%Y%m%d%H%M%S", gmtime()), preset)
        data["fileName"] = fileName
        # error msg in json to be displayed by the web site
        data["errorMsg"] = errorMsg

        self.shm.writeMsgJson(data)
        self.shm.finish(False)

    def locNameInternal2Web(self, locName):
        return removeChars(locName, " ,()-")

    def locNameWeb2Internal(self, locNameWeb):
        return self.locsWeb2Internal[locNameWeb]

    def apNameInternal2Web(self, apName):
        return apName[0].lower() + removeChars(apName[1:], " ")

    def getWebLoc(self, locNameWeb):
        locName = self.locNameWeb2Internal(locNameWeb)
        for loc in self.locations:
            if loc.Name == locName:
                return loc
        raise Exception("Location '{}' not found".format(locName))

    def pickItemAt(self, locName, autotracker=False):
        # collect new item at newLoc
        loc = self.getWebLoc(locName)

        # check that location has not already been visited
        if loc in self.visitedLocations:
            self.errorMsg = "Location '{}' has already been visited".format(loc.Name)
            return

        if loc.difficulty is None or loc.difficulty == False:
            # sequence break
            loc.difficulty = SMBool(True, -1)
        if loc.accessPoint is None:
            # take first ap of the loc
            loc.accessPoint = list(loc.AccessFrom)[0]
        self.collectMajor(loc, autotracker=autotracker)

    def setItemAt(self, locName, itemName, hide):
        # set itemName at locName

        loc = self.getWebLoc(locName)

        # check if location has not already been visited
        if loc in self.visitedLocations:
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

        if hide == True:
            loc.Visibility = 'Hidden'

        if loc in self.majorLocations:
            self.collectMajor(loc, itemName=itemName)

    def replaceItemAt(self, locName, itemName, hide):
        # replace itemName at locName
        loc = self.getWebLoc(locName)
        oldItemName = loc.itemName

        # replace item at the old item spot in collectedItems
        try:
            index = next(i for i, vloc in enumerate(self.visitedLocations) if vloc.Name == loc.Name)
        except Exception as e:
            self.errorMsg = "Empty location {}".format(locName)
            return

        # major item can be set multiple times in plando mode
        count = self.collectedItems.count(oldItemName)
        isCount = self.smbm.isCountItem(oldItemName)

        # update item in collected items after we check the count
        self.collectedItems[index] = itemName
        loc.itemName = itemName

        # update smbm if count item or major was only there once
        if isCount == True or count == 1:
            self.smbm.removeItem(oldItemName)

        if hide == True:
            loc.Visibility = 'Hidden'
        elif loc.CanHidden == True and loc.Visibility == 'Hidden':
            # the loc was previously hidden, set it back to visible
            loc.Visibility = 'Visible'

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
        self.lastAP = self.startLocation
        self.lastArea = self.startArea
        self.majorLocations = self.locations
        if reload == True:
            for loc in self.majorLocations:
                loc.difficulty = None
        self.smbm.resetItems()
        self.objectives.resetGoals()

    def updatePlandoScavengerOrder(self, plandoScavengerOrder):
        self.plandoScavengerOrder = plandoScavengerOrder

    def addTransition(self, startPoint, endPoint):
        # already check in controller if transition is valid for seed
        self.curGraphTransitions.append((startPoint, endPoint))

    def cancelLastTransition(self):
        if self.areaRando == True and self.bossRando == True:
            if len(self.curGraphTransitions) > 0:
                self.curGraphTransitions.pop()
        elif self.areaRando == True:
            if len(self.curGraphTransitions) > len(self.bossTransitions) + (1 if self.escapeRando == False else 0):
                self.curGraphTransitions.pop()
        elif self.bossRando == True:
            print("len cur graph: {} len area: {} len escape: {} len sum: {}".format(len(self.curGraphTransitions), len(self.areaTransitions), 1 if self.escapeRando == False else 0, len(self.areaTransitions) + (1 if self.escapeRando == False else 0)))
            if len(self.curGraphTransitions) > len(self.areaTransitions) + (1 if self.escapeRando == False else 0):
                self.curGraphTransitions.pop()
        elif self.escapeRando == True:
            if len(self.curGraphTransitions) > len(self.areaTransitions) + len(self.bossTransitions):
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
        if self.areaRando == True and self.bossRando == True and self.escapeRando == True:
            if len(self.curGraphTransitions) == 0:
                return
        elif self.areaRando == True and self.escapeRando == False:
            if len(self.curGraphTransitions) == len(self.bossTransitions) + len(self.escapeTransition):
                return
            elif [startPoint, endPoint] in self.bossTransitions or [endPoint, startPoint] in self.bossTransitions:
                return
            elif [startPoint, endPoint] in self.escapeTransition or [endPoint, startPoint] in self.escapeTransition:
                return
        elif self.bossRando == True and self.escapeRando == False:
            if len(self.curGraphTransitions) == len(self.areaTransitions) + len(self.escapeTransition):
                return
            elif [startPoint, endPoint] in self.areaTransitions or [endPoint, startPoint] in self.areaTransitions:
                return
            elif [startPoint, endPoint] in self.escapeTransition or [endPoint, startPoint] in self.escapeTransition:
                return
        elif self.areaRando == True and self.escapeRando == True:
            if len(self.curGraphTransitions) == len(self.bossTransitions):
                return
            elif [startPoint, endPoint] in self.bossTransitions or [endPoint, startPoint] in self.bossTransitions:
                return
        elif self.bossRando == True and self.escapeRando == True:
            if len(self.curGraphTransitions) == len(self.areaTransitions):
                return
            elif [startPoint, endPoint] in self.areaTransitions or [endPoint, startPoint] in self.areaTransitions:
                return
        elif self.escapeRando == True and self.areaRando == False and self.bossRando == False:
            if len(self.curGraphTransitions) == len(self.areaTransitions) + len(self.bossTransitions):
                return
            elif [startPoint, endPoint] in self.areaTransitions or [endPoint, startPoint] in self.areaTransitions:
                return
            elif [startPoint, endPoint] in self.bossTransitions or [endPoint, startPoint] in self.bossTransitions:
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

        if self.escapeRando == False:
            self.curGraphTransitions += self.escapeTransition

    def clearLocs(self, locs):
        for loc in locs:
            loc.difficulty = None

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

    def importDump(self, shmName):
        from utils.shm import SHM
        shm = SHM(shmName)
        dumpData = shm.readMsgJson()
        shm.finish(False)

        # first update current access point
        self.lastAP = dumpData["newAP"]

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
        self.locDelta = 0
        bosses = []

        for dataType, offset in dumpData["stateDataOffsets"].items():
            if dataType == dataEnum["items"]:
                # get item data, loop on all locations to check if they have been visited
                for loc in self.locations:
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
                        if loc not in self.visitedLocations:
                            self.pickItemAt(self.locNameInternal2Web(loc.Name), autotracker=True)
                            self.locDelta += 1
                    else:
                        if loc in self.visitedLocations:
                            self.removeItemAt(self.locNameInternal2Web(loc.Name), autotracker=True)
            elif dataType == dataEnum["boss"]:
                for boss, bossData in self.bossBitMasks.items():
                    byteIndex = bossData["byteIndex"]
                    bitMask = bossData["bitMask"]
                    loc = self.getLoc(boss)
                    if currentState[offset + byteIndex] & bitMask != 0:
                        # as we clear collected items we have to add bosses back.
                        # some bosses have a space in their names, remove it.
                        bosses.append(boss.replace(' ', ''))

                        # in tourian disabled mother brain is not available, but it gets auto killed during escape
                        if loc not in self.visitedLocations and loc in self.majorLocations:
                            self.pickItemAt(self.locNameInternal2Web(loc.Name), autotracker=True)
                            self.locDelta += 1
                    else:
                        if loc in self.visitedLocations:
                            self.removeItemAt(self.locNameInternal2Web(loc.Name), autotracker=True)

            # Inventory
            elif dataType == dataEnum["inventory"]:
                # Clear collected items if loading from game state.
                self.collectedItems.clear()
                self.smbm.resetItems()

                # put back bosses
                for boss in bosses:
                    self.collectedItems.append(boss)
                    self.smbm.addItem(boss)

                for item, itemData in self.inventoryBitMasks.items():
                    if item not in Conf.itemsForbidden:
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
                                self.collectedItems.append(item)
                                self.smbm.addItem(item)
                        elif item == "Reserve":
                            tanks = int(val / 100)
                            for _ in range(tanks):
                                self.collectedItems.append(item)
                                self.smbm.addItem(item)
                        elif item in ("Missile", "Super", "PowerBomb"):
                            packs = int(val / 5)
                            for _ in range(packs):
                                self.collectedItems.append(item)
                                self.smbm.addItem(item)
                        else:
                            bitMask = itemData["bitMask"]
                            if val & bitMask != 0:
                                self.collectedItems.append(item)
                                self.smbm.addItem(item)

            elif dataType == dataEnum["map"]:
                if self.areaRando or self.bossRando or self.escapeRando:
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
                    if self.areaRando == True and self.bossRando == True:
                        staticTransitions = []
                        possibleTransitions = self.bossTransitions + self.areaTransitions
                    elif self.areaRando == True:
                        staticTransitions = self.bossTransitions[:]
                        possibleTransitions = self.areaTransitions[:]
                    elif self.bossRando == True:
                        staticTransitions = self.areaTransitions[:]
                        possibleTransitions = self.bossTransitions[:]
                    else:
                        staticTransitions = self.bossTransitions + self.areaTransitions
                        possibleTransitions = []
                    if self.escapeRando == False:
                        staticTransitions += self.escapeTransition
                    else:
                        possibleTransitions += self.escapeTransition

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

                if self.hasNothing:
                    # get locs with nothing
                    locsNothing = [loc for loc in self.locations if loc.itemName == 'Nothing']
                    for loc in locsNothing:
                        locData = self.nothingScreens[self.logic][loc.Name]
                        if self.isElemAvailable(currentState, offset, locData):
                            # nothing has been seen, check if loc is already visited
                            if not loc in self.visitedLocations:
                                # visit it
                                self.pickItemAt(self.locNameInternal2Web(loc.Name))
                                self.locDelta += 1
                        else:
                            # nothing not yet seed, check if loc is already visited
                            if loc in self.visitedLocations:
                                # unvisit it
                                self.removeItemAt(self.locNameInternal2Web(loc.Name))
                if self.doorsRando:
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
                goalsCompleted = self.objectives.getState()
                goalsCompleted = list(goalsCompleted.values())
                for i, (event, eventData) in enumerate(self.eventsBitMasks.items()):
                    assert str(i) == event, "{}th event has code {} instead of {}".format(i, event, i)
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

                if self.objectivesHiddenOption:
                    # also check objectives revealed event
                    # !VARIA_event_base #= $0080
                    # !objectives_revealed_event #= !VARIA_event_base+33
                    VARIA_event_base = 0x80
                    objectives_revealed_event = VARIA_event_base+33
                    byteIndex = objectives_revealed_event >> 3
                    bitMask = 1 << (objectives_revealed_event & 7)
                    self.objectivesHidden = not bool(currentState[offset + byteIndex] & bitMask)

    def isElemAvailable(self, currentState, offset, apData):
        byteIndex = apData["byteIndex"]
        bitMask = apData["bitMask"]
        return currentState[offset + byteIndex + self.mapOffsetEnum[apData["area"]]] & bitMask != 0
