import os, uuid, json, subprocess, tempfile, re
from datetime import datetime

from web.backend.utils import raiseHttp, locName4isolver, getInt
from graph.vanilla.graph_access import accessPoints
from graph.graph_utils import GraphUtils
from utils.utils import removeChars, getPresetDir, getPythonExec
from utils.doorsmanager import DoorsManager
from utils.db import DB
from solver.interactiveSolver import InteractiveSolver
from logic.logic import Logic

from gluon.validators import IS_ALPHANUMERIC, IS_LENGTH, IS_NOT_EMPTY

class WS(object):
    @staticmethod
    def factory(caller):
        scope = caller.request.vars.scope
        if scope not in ["area", "item", "common", "door", "dump"]:
            raiseHttp(400, "Unknown scope, must be area/item/common/door/dump", True)

        action = caller.request.vars.action
        if action not in ['add', 'remove', 'toggle', 'clear', 'init', 'get', 'save', 'replace', 'randomize', 'import', 'upload_scav']:
            raiseHttp(400, "Unknown action", True)

        mode = caller.request.vars.mode
        if mode not in ["standard", "seedless", "plando", "race", "debug"]:
            raiseHttp(400, "Unknown mode, must be standard/seedless/plando/race/debug", True)

        logic = caller.request.vars.logic
        if logic not in Logic.list():
            raiseHttp(400, "Unknown logic, must be vanilla/mirror", True)

        try:
            WSClass = globals()["WS_{}_{}".format(scope, action)]
            return WSClass(logic, mode, caller)
        except Exception as e:
            raiseHttp(400, "{}".format(e.body if "body" in e.__dict__ else e).replace('"', ''), True)

    def __init__(self, logic, mode, caller):
        self.logic = logic
        self.mode = mode
        self.caller = caller
        self.vars = self.caller.request.vars
        if self.mode in ["plando", "debug"]:
            if self.caller.session.plando is None:
                raiseHttp(400, "No session found for the Plandomizer Web service", True)
            self.session = self.caller.session.plando
        else:
            if self.caller.session.tracker is None:
                raiseHttp(400, "No session found for the Tracker Web service", True)
            self.session = self.caller.session.tracker

    def validate(self):
        if self.session is None:
            raiseHttp(400, "No session found for the Tracker", True)

        if self.vars.action == None:
            raiseHttp(400, "Missing parameter action", True)
        action = self.vars.action

        if self.vars.escapeTimer != None:
            if re.match("[0-9][0-9]:[0-9][0-9]", self.vars.escapeTimer) == None:
                raiseHttp(400, "Wrong escape timer value")

    def validatePoint(self, point):
        if self.vars[point] == None:
            raiseHttp(400, "Missing parameter {}".format(point), True)

        pointValue = self.vars[point]

        if pointValue not in ['lowerMushroomsLeft', 'moatRight', 'greenPiratesShaftBottomRight',
                              'keyhunterRoomBottom', 'morphBallRoomLeft', 'greenBrinstarElevator',
                              'greenHillZoneTopRight', 'noobBridgeRight', 'westOceanLeft', 'crabMazeLeft',
                              'lavaDiveRight', 'threeMuskateersRoomLeft', 'warehouseZeelaRoomLeft',
                              'warehouseEntranceLeft', 'warehouseEntranceRight', 'singleChamberTopRight',
                              'kronicBoostRoomBottomLeft', 'mainStreetBottom', 'crabHoleBottomLeft', 'leCoudeRight',
                              'redFishRoomLeft', 'redTowerTopLeft', 'caterpillarRoomTopRight', 'redBrinstarElevator',
                              'eastTunnelRight', 'eastTunnelTopRight', 'glassTunnelTop', 'goldenFour',
                              'ridleyRoomOut', 'ridleyRoomIn', 'kraidRoomOut', 'kraidRoomIn',
                              'draygonRoomOut', 'draygonRoomIn', 'phantoonRoomOut', 'phantoonRoomIn',
                              'tourianEscapeRoom4TopRight', 'climbBottomLeft', 'greenBrinstarMainShaftTopLeft',
                              'basementLeft', 'businessCenterMidLeft', 'crabHoleBottomRight', 'crocomireRoomTop',
                              'crocomireSpeedwayBottom', 'crabShaftRight', 'aqueductTopLeft']:
            raiseHttp(400, "Wrong value for {}".format(point), True)

    def action(self):
        pass

    def returnState(self):
        if self.session["state"]:
            state = self.session["state"]
            return json.dumps({
                # item tracker
                "availableLocations": state["availableLocationsWeb"],
                "visitedLocations": state["visitedLocationsWeb"],
                "collectedItems": state["collectedItems"],
                "remainLocations": state["remainLocationsWeb"],
                "lastAP": locName4isolver(state["lastAP"]),

                # area tracker
                "lines": state["linesWeb"],
                "linesSeq": state["linesSeqWeb"],
                "allTransitions": state["allTransitions"],
                "roomsVisibility": state["roomsVisibility"],

                # infos on seed
                "logic": state["logic"],
                "mode": state["mode"],
                "majorsSplit": state["masterMajorsSplit"],
                "areaRando": state["areaRando"],
                "bossRando": state["bossRando"],
                "hasMixedTransitions": state["hasMixedTransitions"],
                "escapeRando": state["escapeRando"],
                "escapeTimer": state["escapeTimer"],
                "seed": state["seed"],
                "preset": os.path.basename(os.path.splitext(state["presetFileName"])[0]),
                "errorMsg": state["errorMsg"],
                "last": state["last"],
                "innerTransitions": state["innerTransitions"],
                "hasNothing": state["hasNothing"],

                # doors
                "doors": state["doors"],
                "doorsRando": state["doorsRando"],
                "allDoorsRevealed": state["allDoorsRevealed"],

                # plando scav hunt
                "plandoScavengerOrder": state["plandoScavengerOrder"],

                # tourian
                "tourian": state["tourian"],

                # completed objectives
                "newlyCompletedObjectives": state["newlyCompletedObjectives"],
                "eventsBitMasks": state["eventsBitMasks"],
                "objectives": state["objectives"],
                "objectivesHidden": state["objectivesHidden"]
            })
        else:
            raiseHttp(200, "OK", True)

    def callSolverAction(self, scope, action, parameters):
        # check that we have a state in the session
        if "state" not in self.session:
            raiseHttp(400, "Missing Solver state in the session", True)

        parameters["debug"] = self.mode == 'debug'

        print("before calling isolver: {}".format(parameters))
        start = datetime.now()

        try:
            solver = InteractiveSolver(self.logic)
            state = solver.iterate(self.session["state"], scope, action, parameters)
        except Exception as e:
            msg = "Something wrong happened while iteratively solving the ROM: {}".format(e)
            print(msg)
            self.addError(parameters, msg)

            if action == 'randomize':
                with DB() as db:
                    end = datetime.now()
                    duration = (end - start).total_seconds() * 1000
                    db.addPlandoRando(-1, duration, msg)

            raiseHttp(400, msg, True)

        end = datetime.now()
        duration = (end - start).total_seconds() * 1000
        print("isolver duration: {}ms".format(duration))

        if action == 'save':
            return json.dumps(state)
        else:
            if action == 'randomize':
                with DB() as db:
                    db.addPlandoRando(0, duration, state.get("errorMsg", ""))

            # save the escape timer at every step to avoid loosing its value
            if self.vars.escapeTimer is not None:
                state["escapeTimer"] = self.vars.escapeTimer

            self.session["state"] = state
            return self.returnState()

    def addError(self, params, errContent):
        errDir = os.path.expanduser("~/web2py/applications/solver/errors")
        if os.path.isdir(errDir):
            import traceback
            errFile = '{}.{}.{}'.format(self.caller.request.client,
                                        datetime.now().strftime('%Y-%m-%d.%H-%M-%S'),
                                        str(uuid.uuid4()))
            errFile = os.path.join(errDir, errFile)
            errContent += "\n" + traceback.format_exc()
            with open(errFile, 'w') as f:
                f.write(str(params)+'\n')
                f.write(errContent)

    def name4isolver(self, locName):
        # remove space and special characters
        # sed -e 's+ ++g' -e 's+,++g' -e 's+(++g' -e 's+)++g' -e 's+-++g'
        return removeChars(locName, " ,()-")

class WS_common_init(WS):
    def validate(self):
        super(WS_common_init, self).validate()

        if self.vars.scope != 'common':
            raiseHttp(400, "Unknown scope, must be common", True)

        # preset
        preset = self.vars.preset
        if preset is None:
            raiseHttp(400, "Missing parameter preset", True)
        if IS_NOT_EMPTY()(preset)[1] is not None:
            raiseHttp(400, "Preset name is empty", True)
        if IS_ALPHANUMERIC()(preset)[1] is not None:
            raiseHttp(400, "Preset name must be alphanumeric", True)
        if IS_LENGTH(32)(preset)[1] is not None:
            raiseHttp(400, "Preset name must be max 32 chars", True)
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if not os.path.isfile(fullPath):
            raiseHttp(400, "Unknown preset", True)

        if self.vars.mode != 'seedless':
            # ROM (only through file API)
            if self.vars.romJson is None or len(self.vars.romJson) == 0:
                raiseHttp(400, "Missing ROM to solve", True)
            try:
                json.loads(self.vars.romJson)
            except:
                raiseHttp(400, "Wrong value for romJson, must be a JSON string")

        if self.vars.startLocation is not None:
            if self.vars.startLocation not in GraphUtils.getStartAccessPointNames(self.logic):
                raiseHttp(400, "Wrong value for startLocation", True)

    def action(self):
        mode = self.vars.mode
        logic = self.vars.logic
        if mode != 'seedless':
            tmpRomData = json.loads(self.vars.romJson)
            seed = tmpRomData["romFileName"]
            del tmpRomData["romFileName"]
            # in json keys are strings
            romData = {int(address): data for address, data in tmpRomData.items()}
            romData["romFileName"] = seed
            startLocation = None
        else:
            seed = 'seedless'
            romData = None
            startLocation = self.vars.startLocation

        preset = self.vars.preset
        presetFileName = '{}/{}.json'.format(getPresetDir(preset), preset)
        doorsRando = self.vars.doorsRando == 'true'

        self.session["logic"] = logic
        self.session["seed"] = seed
        self.session["preset"] = preset
        self.session["mode"] = mode
        self.session["startLocation"] = startLocation if startLocation != None else "Landing Site"

        fill = self.vars.fill == "true"

        return self.callSolverInit(romData, presetFileName, preset, seed, logic, mode, fill, startLocation, doorsRando)

    def callSolverInit(self, romData, presetFileName, preset, romFileName, logic, mode, fill, startLocation, doorsRando):

        extraSettings = {
            'startLocation': startLocation,
            'doorsRando': doorsRando,
        }

        printParams = {"mode": mode, "logic": logic, "preset": preset, "rom": romFileName}
        print("before init isolver: {}".format(printParams))
        start = datetime.now()

        try:
            solver = InteractiveSolver(self.logic)
            state = solver.initialize(mode, romData, romFileName, presetFileName, fill, extraSettings)
        except Exception as e:
            msg = "Something wrong happened during isolver init: {}".format(e)
            print(msg)
            self.addError(printParams, msg)
            raiseHttp(400, msg, True)

        end = datetime.now()
        duration = (end - start).total_seconds() * 1000
        print("isolver init duration: {}ms".format(duration))

        with DB() as db:
            db.addISolver(preset, 'plando' if mode == 'plando' else 'tracker', romFileName)

        self.session["state"] = state
        return self.returnState()

class WS_common_get(WS):
    def validate(self):
        super(WS_common_get, self).validate()

    def action(self):
        return self.returnState()

class WS_common_save(WS):
    def validate(self):
        super(WS_common_save, self).validate()

        if self.vars.lock == None:
            raiseHttp(400, "Missing parameter lock", True)

        if self.vars.lock not in ["save", "lock"]:
            raiseHttp(400, "Wrong value for lock, authorized values: save/lock", True)

    def action(self):
        if self.session["mode"] != "plando":
            raiseHttp(400, "Save can only be use in plando mode", True)

        params = {'lock': self.vars.lock == "lock"}
        params['escapeTimer'] = self.vars.escapeTimer if self.vars.escapeTimer is not None else '03:00'

        return self.callSolverAction("common", "save", params)

class WS_common_randomize(WS):
    def validate(self):
        super(WS_common_randomize, self).validate()

        minorQtyInt = getInt(self.caller.request, 'minorQty', True)
        if minorQtyInt < 7 or minorQtyInt > 100:
            raiseHttp(400, "Wrong value for minorQty, must be between 7 and 100", True)
        if self.vars.energyQty not in ["sparse", "medium", "vanilla"]:
            raiseHttp(400, "Wrong value for energyQty", True)
        if self.vars.forbiddenItems != '':
            forbiddenItems = self.vars.forbiddenItems.split(',')
            validItems = set(["Charge", "Ice", "Wave", "Spazer", "Plasma", "Varia", "Gravity", "Morph", "Bomb", "SpringBall", "ScrewAttack", "HiJump", "SpaceJump", "SpeedBooster", "Grapple", "XRayScope", "ETank", "Reserve", "Missile", "Super", "PowerBomb"])
            for item in forbiddenItems:
                if item not in validItems:
                    raiseHttp(400, "Wrong value for forbidden items", True)

    def action(self):
        if self.session["mode"] != "plando":
            raiseHttp(400, "Randomize can only be use in plando mode", True)

        params = {}
        for elem in "minorQty", "energyQty":
            params[elem] = self.vars[elem]
        if self.vars.forbiddenItems != '':
            params["forbiddenItems"] = self.vars.forbiddenItems.split(',')

        self.session["rando"] = params

        return self.callSolverAction("common", "randomize", params)

class WS_area_add(WS):
    def validate(self):
        super(WS_area_add, self).validate()

        # startPoint and endPoint
        self.validatePoint("startPoint")
        self.validatePoint("endPoint")

        if len(self.session["state"]) == 0:
            raiseHttp(400, "ISolver state is empty", True)

    def action(self):
        return self.callSolverAction("area", "add", {"startPoint": self.vars.startPoint,
                                                     "endPoint": self.vars.endPoint})

class WS_area_remove(WS):
    def validate(self):
        if self.vars["startPoint"] != None:
            self.validatePoint("startPoint")

        super(WS_area_remove, self).validate()

    def action(self):
        parameters = {}
        if self.vars["startPoint"] != None:
            parameters["startPoint"] = self.vars.startPoint

        return self.callSolverAction("area", "remove", parameters)

class WS_area_clear(WS):
    def validate(self):
        super(WS_area_clear, self).validate()

    def action(self):
        return self.callSolverAction("area", "clear", {})

validItemsList = [None, 'ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack', 'Nothing', 'NoEnergy', 'Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain', 'SporeSpawn', 'Crocomire', 'Botwoon', 'GoldenTorizo']
validLocsList = ['EnergyTankGauntlet', 'Bomb', 'EnergyTankTerminator', 'ReserveTankBrinstar', 'ChargeBeam', 'MorphingBall', 'EnergyTankBrinstarCeiling', 'EnergyTankEtecoons', 'EnergyTankWaterway', 'EnergyTankBrinstarGate', 'XRayScope', 'Spazer', 'EnergyTankKraid', 'VariaSuit', 'IceBeam', 'EnergyTankCrocomire', 'HiJumpBoots', 'GrappleBeam', 'ReserveTankNorfair', 'SpeedBooster', 'WaveBeam', 'EnergyTankRidley', 'ScrewAttack', 'EnergyTankFirefleas', 'ReserveTankWreckedShip', 'EnergyTankWreckedShip', 'RightSuperWreckedShip', 'GravitySuit', 'EnergyTankMamaturtle', 'PlasmaBeam', 'ReserveTankMaridia', 'SpringBall', 'EnergyTankBotwoon', 'SpaceJump', 'PowerBombCrateriasurface', 'MissileoutsideWreckedShipbottom', 'MissileoutsideWreckedShiptop', 'MissileoutsideWreckedShipmiddle', 'MissileCrateriamoat', 'MissileCrateriabottom', 'MissileCrateriagauntletright', 'MissileCrateriagauntletleft', 'SuperMissileCrateria', 'MissileCrateriamiddle', 'PowerBombgreenBrinstarbottom', 'SuperMissilepinkBrinstar', 'MissilegreenBrinstarbelowsupermissile', 'SuperMissilegreenBrinstartop', 'MissilegreenBrinstarbehindmissile', 'MissilegreenBrinstarbehindreservetank', 'MissilepinkBrinstartop', 'MissilepinkBrinstarbottom', 'PowerBombpinkBrinstar', 'MissilegreenBrinstarpipe', 'PowerBombblueBrinstar', 'MissileblueBrinstarmiddle', 'SuperMissilegreenBrinstarbottom', 'MissileblueBrinstarbottom', 'MissileblueBrinstartop', 'MissileblueBrinstarbehindmissile', 'PowerBombredBrinstarsidehopperroom', 'PowerBombredBrinstarspikeroom', 'MissileredBrinstarspikeroom', 'MissileKraid', 'Missilelavaroom', 'MissilebelowIceBeam', 'MissileaboveCrocomire', 'MissileHiJumpBoots', 'EnergyTankHiJumpBoots', 'PowerBombCrocomire', 'MissilebelowCrocomire', 'MissileGrappleBeam', 'MissileNorfairReserveTank', 'MissilebubbleNorfairgreendoor', 'MissilebubbleNorfair', 'MissileSpeedBooster', 'MissileWaveBeam', 'MissileGoldTorizo', 'SuperMissileGoldTorizo', 'MissileMickeyMouseroom', 'MissilelowerNorfairabovefireflearoom', 'PowerBomblowerNorfairabovefireflearoom', 'PowerBombPowerBombsofshame', 'MissilelowerNorfairnearWaveBeam', 'MissileWreckedShipmiddle', 'MissileGravitySuit', 'MissileWreckedShiptop', 'SuperMissileWreckedShipleft', 'MissilegreenMaridiashinespark', 'SuperMissilegreenMaridia', 'MissilegreenMaridiatatori', 'SuperMissileyellowMaridia', 'MissileyellowMaridiasupermissile', 'MissileyellowMaridiafalsewall', 'MissileleftMaridiasandpitroom', 'MissilerightMaridiasandpitroom', 'PowerBombrightMaridiasandpitroom', 'MissilepinkMaridia', 'SuperMissilepinkMaridia', 'MissileDraygon', 'Kraid', 'Ridley', 'Phantoon', 'Draygon', 'MotherBrain', 'SporeSpawn', 'Crocomire', 'Botwoon', 'GoldenTorizo']

class WS_item_add(WS):
    def validate(self):
        super(WS_item_add, self).validate()

        # new location
        if self.vars.locName != None:
            locName = self.name4isolver(self.vars.locName)

            if locName not in validLocsList:
                raiseHttp(400, "Unknown location name", True)

            self.vars.locName = locName

        itemName = self.vars.itemName
        if itemName == "NoEnergy":
            itemName = "Nothing"

        if itemName not in validItemsList:
            raiseHttp(400, "Unknown item name", True)


    def action(self):
        item = self.vars.itemName
        locName = self.vars.locName

        # items used only in the randomizer that we get in vcr mode
        if item in ["NoEnergy", None]:
            item = 'Nothing'

        # in seedless mode we have to had boss items instead of nothing
        if self.vars.mode in ["seedless", "race", "debug"]:
            if locName in ['Kraid', 'Ridley', 'Phantoon', 'Draygon', 'MotherBrain', 'SporeSpawn', 'Crocomire', 'Botwoon', 'GoldenTorizo']:
                item = locName

        params = {"item": item, "hide": self.vars.hide == "true"}
        if locName != None:
            params['loc'] = locName
        return self.callSolverAction("item", "add", params)

class WS_item_replace(WS_item_add):
    def validate(self):
        super(WS_item_replace, self).validate()

    def action(self):
        return self.callSolverAction("item", "replace", {"loc": self.vars.locName, "item": self.vars.itemName, "hide": self.vars.hide == "true"})

class WS_item_toggle(WS_item_add):
    def validate(self):
        super(WS_item_toggle, self).validate()

        if self.vars.itemName not in validItemsList:
            raiseHttp(400, "Unknown item name", True)

    def action(self):
        return self.callSolverAction("item", "toggle", {"item": self.vars.itemName})

class WS_item_remove(WS):
    def validate(self):
        super(WS_item_remove, self).validate()

        if self.vars.itemName not in validItemsList:
            raiseHttp(400, "Unknown item name", True)

        self.itemName = self.vars.itemName
        if self.itemName == None:
            if self.vars.count != None:
                self.count = getInt(self.caller.request, "count", True)
                if self.count > 109 or self.count < 1:
                    raiseHttp(400, "Wrong value for count, must be in [1-109] ", True)
            else:
                self.count = 1
        else:
            self.count = -1

        self.locName = self.vars.locName
        if self.locName != None:
            self.locName = self.name4isolver(self.locName)

            if self.locName not in validLocsList:
                raiseHttp(400, "Unknown location name", True)

    def action(self):
        if self.locName != None:
            return self.callSolverAction("item", "remove", {"loc": self.locName})
        else:
            if self.itemName != None:
                return self.callSolverAction("item", "remove", {"item": self.itemName})
            else:
                return self.callSolverAction("item", "remove", {"count": self.count})

class WS_item_clear(WS):
    def validate(self):
        super(WS_item_clear, self).validate()

    def action(self):
        return self.callSolverAction("item", "clear", {})

class WS_item_upload_scav(WS):
    def getScavLocs(self):
        scavLocs = self.caller.cache.ram('scavLocs', lambda:list(), time_expire=None)
        if len(scavLocs):
            return scavLocs
        else:
            from graph.vanilla.graph_locations import locations
            scavLocs = [loc.Name for loc in locations if loc.isScavenger()]
            return scavLocs

    def validate(self):
        super(WS_item_upload_scav, self).validate()

        self.params = {}
        if self.vars.plandoScavengerOrder is not None:
            scavLocs = self.getScavLocs()
            self.params["plandoScavengerOrder"] = self.vars.plandoScavengerOrder.split(',')
            for loc in self.params["plandoScavengerOrder"]:
                if loc not in scavLocs:
                    raiseHttp(400, "Unknown scavenger location: [{}]".format(loc), True)

    def action(self):
        return self.callSolverAction("item", "upload_scav", self.params)

class WS_door_replace(WS):
    def validate(self):
        super(WS_door_replace, self).validate()

        self.doorName = self.vars.doorName
        if self.doorName not in DoorsManager.doors.keys():
            raiseHttp(400, "Wrong value for doorName", True)
        self.newColor = self.vars.newColor
        if self.newColor not in ["red", "green", "yellow", "grey", "wave", "spazer", "plasma", "ice", "blue"]:
            raiseHttp(400, "Wrong value for newColor", True)

    def action(self):
        return self.callSolverAction("door", "replace", {"doorName": self.doorName, "newColor": self.newColor})

class WS_door_toggle(WS):
    def validate(self):
        super(WS_door_toggle, self).validate()

        self.doorName = self.vars.doorName
        if self.doorName not in DoorsManager.doors.keys():
            raiseHttp(400, "Wrong value for doorName", True)

    def action(self):
        return self.callSolverAction("door", "toggle", {"doorName": self.doorName})

class WS_door_clear(WS):
    def validate(self):
        super(WS_door_clear, self).validate()

    def action(self):
        return self.callSolverAction("door", "clear", {})

webAPs = {locName4isolver(ap.Name): ap.Name for ap in accessPoints}
class WS_dump_import(WS):
    def validate(self):
        super(WS_dump_import, self).validate()

        newAP = self.vars.newAP
        if newAP not in webAPs:
            raiseHttp(400, "Wrong AP", True)

        self.jsonData = {"stateDataOffsets": json.loads(self.vars.stateDataOffsets),
                         "currentState": json.loads(self.vars.currentState),
                         "newAP": webAPs[newAP]}
        if len(self.jsonData["currentState"]) > 1632 or len(self.jsonData["stateDataOffsets"]) > 5:
            raiseHttp(400, "Wrong state size", True)
        for key, value in self.jsonData["stateDataOffsets"].items():
            if len(key) > 1 or type(value) != int:
                raiseHttp(400, "Wrong state type", True)
        if any([d for d in self.jsonData["currentState"] if type(d) != int]):
            raiseHttp(400, "Wrong cur state type", True)

    def action(self):
        ret = self.callSolverAction("dump", "import", {"dump": self.jsonData})
        return ret
