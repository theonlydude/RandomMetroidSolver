import sys, json, os

from solver.commonSolver import CommonSolver
from logic.smbool import SMBool
from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.helpers import Pickup
from rom.rompatcher import RomPatcher
from rom.rom_patches import RomPatches
from graph.graph_locations import locations as graphLocations
from graph.graph import AccessGraphSolver as AccessGraph
from graph.graph_access import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, accessPoints, GraphUtils
from utils.utils import removeChars
from solver.conf import Conf
from utils.parameters import hard, infinity
from solver.solverState import SolverState
from solver.comeback import ComeBack
from rando.ItemLocContainer import ItemLocation
from utils.doorsmanager import DoorsManager
import utils.log

class InteractiveSolver(CommonSolver):
    def __init__(self, output):
        self.interactive = True
        self.errorMsg = ""
        self.checkDuplicateMajor = False
        self.vcr = None
        self.log = utils.log.get('Solver')

        self.outputFileName = output
        self.firstLogFile = None
        self.locations = graphLocations

        (self.locsAddressName, self.locsWeb2Internal) = self.initLocsAddressName()
        self.transWeb2Internal = self.initTransitionsName()

        Conf.difficultyTarget = infinity

        # no time limitation
        self.runtimeLimit_s = 0

    def initLocsAddressName(self):
        addressName = {}
        web2Internal = {}
        for loc in graphLocations:
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

        state.toJson(self.outputFileName)

    def initialize(self, mode, rom, presetFileName, magic, fill, startAP):
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

        self.loadRom(rom, interactive=True, magic=magic, startAP=startAP)
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
                    if self.mode in ['plando', 'seedless', 'race', 'debug']:
                        if params['loc'] != None:
                            if self.mode == 'plando':
                                self.setItemAt(params['loc'], params['item'], params['hide'])
                            else:
                                self.setItemAt(params['loc'], params.get('item', 'Nothing'), False)
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
            if lastVisited.difficulty.difficulty == -1:
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
            if lastVisited.difficulty == False:
                # if the loc is still sequence break, put it back as sequence break
                lastVisited.difficulty = SMBool(True, -1)

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
        for ap in accessPoints:
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
            "forbiddenItems": parameters["forbiddenItems"]
        }

        plandoCurrentJson = json.dumps(plandoCurrent)

        pythonExec = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)
        params = [
            pythonExec,  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
            '--runtime', '10',
            '--param', self.presetFileName,
            '--output', self.outputFileName,
            '--plandoRando', plandoCurrentJson,
            '--progressionSpeed', 'speedrun',
            '--minorQty', parameters["minorQty"],
            '--maxDifficulty', 'hardcore',
            '--energyQty', parameters["energyQty"],
            '--startAP', self.startAP
        ]

        import subprocess
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
            magic = random.randint(1, 0xffff)
        else:
            magic = None
        romPatcher = RomPatcher(magic=magic, plando=True)
        patches = ['credits_varia.ips', 'tracking.ips', "Escape_Animals_Disable"]
        if DoorsManager.isRandom():
            patches += RomPatcher.IPSPatches['DoorsColors']
            patches.append("Enable_Backup_Saves")
        if magic != None:
            patches.insert(0, 'race_mode.ips')
            patches.append('race_mode_credits.ips')
        romPatcher.addIPSPatches(patches)

        plms = []
        if self.areaRando == True or self.bossRando == True or self.escapeRando == True:
            doors = GraphUtils.getDoorConnections(AccessGraph(accessPoints, self.fillGraph()), self.areaRando, self.bossRando, self.escapeRando, False)
            romPatcher.writeDoorConnections(doors)
            if magic == None:
                doorsPtrs = GraphUtils.getAps2DoorsPtrs()
                romPatcher.writePlandoTransitions(self.curGraphTransitions, doorsPtrs,
                                                  len(vanillaBossesTransitions) + len(vanillaTransitions))
            if self.escapeRando == True and escapeTimer != None:
                # convert from '03:00' to number of seconds
                escapeTimer = int(escapeTimer[0:2]) * 60 + int(escapeTimer[3:5])
                romPatcher.applyEscapeAttributes({'Timer': escapeTimer, 'Animals': None}, plms)

        # write plm table & random doors
        romPatcher.writePlmTable(plms, self.areaRando, self.bossRando, self.startAP)

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

        romPatcher.commitIPS()
        romPatcher.end()

        data = romPatcher.romFile.data
        preset = os.path.splitext(os.path.basename(self.presetFileName))[0]
        seedCode = 'FX'
        if self.bossRando == True:
            seedCode = 'B'+seedCode
        if self.areaRando == True:
            seedCode = 'A'+seedCode
        from time import gmtime, strftime
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
            if loc.Name == locName:
                return loc
        raise Exception("Location '{}' not found".format(locName))

    def pickItemAt(self, locName):
        # collect new item at newLoc
        loc = self.getWebLoc(locName)
        if loc.difficulty is None or loc.difficulty == False:
            # sequence break
            loc.difficulty = SMBool(True, -1)
        if loc.accessPoint is None:
            # take first ap of the loc
            loc.accessPoint = list(loc.AccessFrom)[0]
        self.collectMajor(loc)

    def setItemAt(self, locName, itemName, hide):
        # set itemName at locName

        loc = self.getWebLoc(locName)
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

        self.collectMajor(loc, itemName)

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
        self.collectedItems[index] = itemName

        loc.itemName = itemName

        # major item can be set multiple times in plando mode
        count = self.collectedItems.count(oldItemName)
        isCount = self.smbm.isCountItem(oldItemName)

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
        self.lastAP = self.startAP
        self.lastArea = self.startArea
        self.majorLocations = self.locations
        if reload == True:
            for loc in self.majorLocations:
                loc.difficulty = None
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
            loc.difficulty = None

    def getDiffThreshold(self):
        # in interactive solver we don't have the max difficulty parameter
        epsilon = 0.001
        return hard - epsilon
