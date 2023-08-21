import copy

from rom.compression import Compressor
from rom.rom import snes_to_pc
from rom.addresses import Addresses
from rom.rom_options import RomOptions
from rom.flavor import RomFlavor
from rom.ips import IPS_Patch
from patches.patchaccess import PatchAccess
from graph.graph_utils import GraphUtils, getAccessPoint, graphAreas
from logic.logic import Logic
from collections import defaultdict
from utils.objectives import Objectives
from utils.doorsmanager import DoorsManager
from rom.rom_patches import definitions as patches_definitions

class RomReader:
    nothings = ['0xbae9', '0xbaed']
    # read the items in the rom
    items = {
        # vanilla
        '0xeed7': {'name': 'ETank'},
        '0xeedb': {'name': 'Missile'},
        '0xeedf': {'name': 'Super'},
        '0xeee3': {'name': 'PowerBomb'},
        '0xeee7': {'name': 'Bomb'},
        '0xeeeb': {'name': 'Charge'},
        '0xeeef': {'name': 'Ice'},
        '0xeef3': {'name': 'HiJump'},
        '0xeef7': {'name': 'SpeedBooster'},
        '0xeefb': {'name': 'Wave'},
        '0xeeff': {'name': 'Spazer'},
        '0xef03': {'name': 'SpringBall'},
        '0xef07': {'name': 'Varia'},
        '0xef13': {'name': 'Plasma'},
        '0xef17': {'name': 'Grapple'},
        '0xef23': {'name': 'Morph'},
        '0xef27': {'name': 'Reserve'},
        '0xef0b': {'name': 'Gravity'},
        '0xef0f': {'name': 'XRayScope'},
        '0xef1b': {'name': 'SpaceJump'},
        '0xef1f': {'name': 'ScrewAttack'},
        # old rando "chozo" items
        '0xef2b': {'name': 'ETank'},
        '0xef2f': {'name': 'Missile'},
        '0xef33': {'name': 'Super'},
        '0xef37': {'name': 'PowerBomb'},
        '0xef3b': {'name': 'Bomb'},
        '0xef3f': {'name': 'Charge'},
        '0xef43': {'name': 'Ice'},
        '0xef47': {'name': 'HiJump'},
        '0xef4b': {'name': 'SpeedBooster'},
        '0xef4f': {'name': 'Wave'},
        '0xef53': {'name': 'Spazer'},
        '0xef57': {'name': 'SpringBall'},
        '0xef5b': {'name': 'Varia'},
        '0xef5f': {'name': 'Gravity'},
        '0xef63': {'name': 'XRayScope'},
        '0xef67': {'name': 'Plasma'},
        '0xef6b': {'name': 'Grapple'},
        '0xef6f': {'name': 'SpaceJump'},
        '0xef73': {'name': 'ScrewAttack'},
        '0xef77': {'name': 'Morph'},
        '0xef7b': {'name': 'Reserve'},
        # old rando "hidden" items
        '0xef7f': {'name': 'ETank'},
        '0xef83': {'name': 'Missile'},
        '0xef87': {'name': 'Super'},
        '0xef8b': {'name': 'PowerBomb'},
        '0xef8f': {'name': 'Bomb'},
        '0xef93': {'name': 'Charge'},
        '0xef97': {'name': 'Ice'},
        '0xef9b': {'name': 'HiJump'},
        '0xef9f': {'name': 'SpeedBooster'},
        '0xefa3': {'name': 'Wave'},
        '0xefa7': {'name': 'Spazer'},
        '0xefab': {'name': 'SpringBall'},
        '0xefaf': {'name': 'Varia'},
        '0xefb3': {'name': 'Gravity'},
        '0xefb7': {'name': 'XRayScope'},
        '0xefbb': {'name': 'Plasma'},
        '0xefbf': {'name': 'Grapple'},
        '0xefc3': {'name': 'SpaceJump'},
        '0xefc7': {'name': 'ScrewAttack'},
        '0xefcb': {'name': 'Morph'},
        '0xefcf': {'name': 'Reserve'},
        '0x0': {'name': 'Nothing'},
        '0xbae9': {'name': 'Nothing'}, # new visible/chozo Nothing
        '0xbaed': {'name': 'Nothing'}  # new hidden Nothing
    }

    patches = patches_definitions

    flavorPatches = {
        'mirror': patches_definitions["mirror"]["logic"]
    }

    # FIXME use symbols/names addresses here?
    allPatches = {
        'AimAnyButton': {'address': 0x175ca, 'value': 0x60, 'vanillaValue': 0xad},
        'animal_enemies': {'address': 0x78418, 'value': 0x3B, 'vanillaValue': 0x48},
        # all the modifications from animals are included in animal_enemies...
        #'animals': {'address': 0x7841D, 'value': 0x8C, 'vanillaValue': 0x18},
        'area_rando_blue_doors': {'address': 0x7823E, 'value': 0x3B, 'vanillaValue': 0x66},
        'area_rando_door_transition': {'address': 0x852BA, 'value': 0x20, 'vanillaValue': 0xad},
        'rando_escape': {'address': 0x15F38, 'value': 0x5C, 'vanillaValue': 0xbd},
        'area_rando_layout_base': {'address': 0x788A0, 'value': 0x2B, 'vanillaValue': 0x26},
        'area_rando_layout': {'address': 0x78666, 'value': 0x62, 'vanillaValue': 0x64},
        'bomb_torizo': {'address': 0x208A7, 'value': 0x20, 'vanillaValue': 0x0d},
        'brinstar_map_room': {'address': 0x784EC, 'value': 0x3B, 'vanillaValue': 0x42},
        'credits_varia': {'address': 0x44B, 'value': 0x5C, 'vanillaValue': 0xa2},
        'dachora': {'address': 0x22A173, 'value': 0xC9, 'vanillaValue': 0xc8},
        'draygonimals': {'address': 0x1ADAC, 'value': 0x60, 'vanillaValue': 0xff},
        'early_super_bridge': {'address': 0x22976B, 'value': 0xC7, 'vanillaValue': 0x43},
        'elevators_doors_speed': {'address': 0x2E9D, 'value': 0x08, 'vanillaValue': 0x04},
        'endingtotals': {'address': 0x208A0, 'value': 0x30, 'vanillaValue': 0x8e},
        'escapimals': {'address': 0x1ADAC, 'value': 0x4D, 'vanillaValue': 0xff},
        'g4_skip': {'address': 0x18C5D, 'value': 0xFE, 'vanillaValue': 0x00},
        'gameend': {'address': 0x18BCC, 'value': 0x20, 'vanillaValue': 0x00},
        'grey_door_animals': {'address': 0x21E186, 'value': 0x06, 'vanillaValue': 0x07},
        'high_jump': {'address': 0x23AA77, 'value': 0x04, 'vanillaValue': 0x05},
        'itemsounds': {'address': 0x16126, 'value': 0x22, 'vanillaValue': 0xa9},
        'ln_chozo_platform': {'address': 0x7CEB0, 'value': 0xC9, 'vanillaValue': 0xc7},
        'ln_chozo_sj_check_disable': {'address': 0x2518F, 'value': 0xEA, 'vanillaValue': 0xad},
        'low_timer': {'address': 0x18BCC, 'value': 0x20, 'vanillaValue': 0x00},
        'max_ammo_display': {'address': 0x19E1, 'value': 0xEA, 'vanillaValue': 0xad},
        'metalimals': {'address': 0x1ADAC, 'value': 0x2B, 'vanillaValue': 0xff},
        'moat': {'address': 0x21BD80, 'value': 0xD5, 'vanillaValue': 0x54},
        'nova_boost_platform': {'address': 0x236CC3, 'value': 0xDF, 'vanillaValue': 0x5f},
        'phantoonimals': {'address': 0x1ADAC, 'value': 0x13, 'vanillaValue': 0xff},
        'rando_speed': {'address': 0x7FDC, 'value': 0xB4, 'vanillaValue': 0x20},
        'red_tower': {'address': 0x2304F7, 'value': 0xC4, 'vanillaValue': 0x44},
        'ridleyimals': {'address': 0x1ADAC, 'value': 0x2E, 'vanillaValue': 0xff},
        'ridley_platform': {'address': 0x246C09, 'value': 0x00, 'vanillaValue': 0x02},
        'seed_display': {'address': 0x16CBB, 'value': 0x20, 'vanillaValue': 0xa2},
        'skip_ceres': {'address': 0x7F17, 'value': 0xB6, 'vanillaValue': 0xff},
        'skip_intro': {'address': 0x7F1F, 'value': 0xB6, 'vanillaValue': 0xff},
        'spazer': {'address': 0x23392B, 'value': 0xC5, 'vanillaValue': 0x45},
        'spinjumprestart': {'address': 0x8763A, 'value': 0xAD, 'vanillaValue': 0xff},
        'spospo_save': {'address': 0x785FC, 'value': 0x3B, 'vanillaValue': 0x03},
        'supermetroid_msu1': {'address': 0xF27, 'value': 0x20, 'vanillaValue': 0x8d},
        'tracking': {'address': 0x10CEA, 'value': 0x4C, 'vanillaValue': 0xee},
        'tracking_buggy_arm_pump': {'address': 0x8EB05, 'value': 0x4C, 'vanillaValue': 0x4D},
        'wake_zebes': {'address': 0x18EB5, 'value': 0xFF, 'vanillaValue': 0x00},
        'ws_etank': {'address': 0x7CC4D, 'value': 0x37, 'vanillaValue': 0x8f},
        'ws_save': {'address': 0x7CEB0, 'value': 0xC9, 'vanillaValue': 0xc7},
        'Removes_Gravity_Suit_heat_protection': {'address': 0x0869dd, 'value': 0x01, 'vanillaValue': 0x20},
        'progressive_suits': {'address': 0x869df, 'value': 0xF0, 'vanillaValue': 0xd0},
        'nerfed_charge': {'address': 0x83821, 'value': 0x80, 'vanillaValue': 0xd0},
        'Suit_acquisition_animation_skip': {'address': 0x020717, 'value': 0xea, 'vanillaValue': 0x22},
        'Fix_Morph_and_Missiles_Room_State': {'address': 0x07e655, 'value': 0xea, 'vanillaValue': 0x89},
        'Fix_heat_damage_speed_echoes_bug': {'address': 0x08b629, 'value': 0x01, 'vanillaValue': 0x00},
        'Disable_GT_Code': {'address': 0x15491c, 'value': 0x80, 'vanillaValue': 0xd0},
        'Disable_Space_Time_select_in_menu': {'address': 0x013175, 'value': 0x01, 'vanillaValue': 0x08},
        'Fix_Morph_Ball_Hidden_Chozo_PLMs': {'address': 0x0268ce, 'value': 0x04, 'vanillaValue': 0x02},
        'Fix_Screw_Attack_selection_in_menu': {'address': 0x0134c5, 'value': 0x0c, 'vanillaValue': 0x0a},
        'No_Music': {'address': 0x278413, 'value': 0x6f, 'vanillaValue': 0xcd},
        'random_music': {'address': 0x10F320, 'value': 0x01, 'vanillaValue': 0xff},
        'fix_suits_selection_in_menu': {'address': 0x13000, 'value': 0x90, 'vanillaValue': 0x80},
        'traverseWreckedShip': {'address': 0x219dbf, 'value': 0xFB, 'vanillaValue': 0xeb},
        'Infinite_Space_Jump': {'address': 0x82493, 'value': 0xEA, 'vanillaValue': 0xf0},
        'refill_before_save': {'address': 0x270C2, 'value': 0x98, 'vanillaValue': 0xff},
        'nerfed_rainbow_beam': {'address': 0x14BA2E, 'value': 0x13, 'vanillaValue': 0x2b},
        'croc_area': {'address': 0x78ba3, 'value': 0x8c, 'vanillaValue': 0x4},
        'area_rando_warp_door': {'address': 0x26425E, 'value': 0x80, 'vanillaValue': 0x70},
        'minimizer_bosses': {'address': 0x10F500, 'value': 0xAD, 'vanillaValue': 0xff},
        'minimizer_tourian': {'address': 0x7F730, 'value': 0xA9, 'vanillaValue': 0xff},
        'open_zebetites': {'address': 0x26DF22, 'value': 0xc3, 'vanillaValue': 0x43},
        'beam_doors': {'address': 0x226e5, 'value': 0x0D, 'vanillaValue': 0xaf},
        'rotation': {'address': 0x44DF, 'value': 0xD0, 'vanillaValue': 0xe0},
        'no_demo': {'address': 0x59F2C, 'value': 0x80, 'vanillaValue': 0xf0},
        'varia_hud': {'address': 0x15EF7, 'value': 0x5C, 'vanillaValue': 0xAE},
        'nothing_item_plm': {'address': 0x23AD1, 'value': 0x24, 'vanillaValue': 0xb9},
        'vanilla_bugfixes': {'address': 0x33704, 'value': 0xF0, 'vanillaValue': 0xD0},
        'widescreen': {'address': 0xD8, 'value': 0x40, 'vanillaValue': 0x10},
        'objectives': {'address': 0x12822, 'value': 0x08, 'vanillaValue': 0x14},
        'percent': {'address': 0x17ffe, 'value': 0x60, 'vanillaValue': 0xff}
    }

    @staticmethod
    def getDefaultPatches():
        # called by the isolver in seedless mode
        # activate only layout patch (the most common one) and blue bt/red tower blue doors
        ret = {}
        for patch in RomReader.patches['common']:
            if patch in ['layout', 'startLS']:  # FIXME layout patch varies depending on flavor
                ret[RomReader.patches[patch]['address']] = RomReader.patches[patch]['value']
            else:
                ret[RomReader.patches[patch]['address']] = 0xFF

        # add phantoon door ptr used by boss rando detection
        doorPtr = getAccessPoint('PhantoonRoomOut').ExitInfo['DoorPtr']
        doorPtr = (0x10000 | doorPtr) + 10
        ret[doorPtr] = 0
        ret[doorPtr+1] = 0

        return ret

    @staticmethod
    def getLogicFromIPS(ips):
        # call by customizer to extract logic from seed ips when logic param is random
        patch = IPS_Patch.load(ips)
        for logic, data in RomReader.flavorPatches.items():
            address = data['address']
            value = patch.getValue(address)
            if value is not None and value == data['value']:
                return logic
        return "vanilla"

    def __init__(self, romFile, magic=None):
        self.romFile = romFile
        self.race = None
        # default to morph ball location
        self.nothingId = 0x1a
        self.nothingAddr = snes_to_pc(0x8f86de)
        if magic is not None:
            from rom.race_mode import RaceModeReader
            self.race = RaceModeReader(self, magic)

    def loadSymbols(self):
        self.symbols = RomFlavor.symbols
        self.romOptions = RomOptions(self.romFile, self.symbols)

    def isEscapeTrigger(self):
        val = self.romOptions.read('escapeTrigger')
        # compatibility with previous releases
        if val == 0xff:
            val = 0
        return bool(val)

    def readPlmWord(self, address):
        if self.race is None:
            return self.romFile.readWord(address)
        else:
            return self.race.readPlmWord(address)

    def getItemBytes(self):
        value1 = int.from_bytes(self.romFile.read(1), byteorder='little')
        value2 = int.from_bytes(self.romFile.read(1), byteorder='little')
        return (value1, value2)

    def getItem(self, address, visibility):
        # return the hex code of the object at the given address
        self.romFile.seek(address)
        # value is in two bytes
        if self.race is None:
            (value1, value2) = self.getItemBytes()
        else:
            (value1, value2) = self.race.getItemBytes(address)

        # match itemVisibility with
        # | Visible -> 0
        # | Chozo -> 0x54 (84)
        # | Hidden -> 0xA8 (168)
        if visibility == 'Visible':
            itemCode = hex(value2*256+(value1-0))
        elif visibility == 'Chozo':
            itemCode = hex(value2*256+(value1-84))
        elif visibility == 'Hidden':
            itemCode = hex(value2*256+(value1-168))
        else:
            raise Exception("RomReader: unknown visibility: {}".format(visibility))

        # for the new nothing item plm the visibility is:
        # Visible/Chozo -> 0
        # Hidden -> 4
        if itemCode not in self.items:
            if visibility in ['Visible', 'Chozo']:
                nothingCode = hex(value2*256+(value1-0))
            elif visibility == 'Hidden':
                nothingCode = hex(value2*256+(value1-4))
            if nothingCode in self.nothings:
                itemCode = nothingCode

        # dessyreqt randomizer make some missiles non existant, detect it
        self.romFile.seek(address+4)
        value3 = int.from_bytes(self.romFile.read(1), byteorder='little')
        if (value3 == self.nothingId
            and int(itemCode, 16) == 0xeedb
            and address != self.nothingAddr):
            return hex(0)
        else:
            return itemCode

    def getMajorsSplit(self):
        address = Addresses.getOne('majorsSplit')
        split = chr(self.romFile.readByte(address))
        splits = {
            'F': 'Full',
            'Z': 'Chozo',
            'M': 'Major',
            'H': 'FullWithHUD',
            'S': 'Scavenger'
        }
        # default to Full
        return splits.get(split, 'Full')

    def loadItems(self, locations):
        majorsSplit = self.getMajorsSplit()

        for loc in locations:
            if loc.isBoss():
                # the boss item has the same name as its location, except for mother brain which has a space
                loc.itemName = loc.Name.replace(' ', '')
                continue
            item = self.getItem(loc.Address, loc.Visibility)
            try:
                loc.itemName = self.items[item]["name"]
            except:
                # race seeds
                loc.itemName = "NoEnergy"
                item = '0x0'

        return (majorsSplit if majorsSplit != 'FullWithHUD' else 'Full', majorsSplit)

    # used to read scavenger locs
    def genLocIdsDict(self, locations):
        locIdsDict = {}
        for loc in locations:
            if loc.isScavenger():
                locIdsDict[loc.Id] = loc
        return locIdsDict

    def loadScavengerOrder(self, locations):
        order = []
        locIdsDict = self.genLocIdsDict(locations)
        self.romFile.seek(Addresses.getOne('scavengerOrder'))
        while True:
            data = self.romFile.readWord()
            locId = (data & 0xFF00) >> 8
            if locId == 0xFF:
                break
            loc = locIdsDict[locId]
            order.append(loc)

            # check that there's no nothing in the loc
            assert loc.itemName != "Nothing", "Nothing detected in scav loc {}".format(loc.Name)
        return order

    def loadTransitions(self, tourian):
        # return the transitions
        rooms = GraphUtils.getRooms()
        bossTransitions = {}
        areaTransitions = {}
        for accessPoint in Logic.accessPoints():
            if accessPoint.isInternal() == True:
                continue
            key = self.getTransition(accessPoint.ExitInfo['DoorPtr'])
            if key not in rooms:
                # can happen with race mode seeds
                continue
            destAP = rooms[key]
            if accessPoint.Boss == True or destAP.Boss == True:
                bossTransitions[accessPoint.Name] = destAP.Name
            else:
                areaTransitions[accessPoint.Name] = destAP.Name

        def removeBiTrans(transitions):
            # remove bidirectionnal transitions
            # can't del keys in a dict while iterating it
            transitionsCopy = copy.copy(transitions)
            for src in transitionsCopy:
                if src in transitions:
                    dest = transitions[src]
                    if dest in transitions:
                        if transitions[dest] == src:
                            del transitions[dest]

            return [(t, transitions[t]) for t in transitions]

        # get escape transition
        if tourian == 'Disabled':
            escapeSrcAP = getAccessPoint('Climb Bottom Left')
        else:
            escapeSrcAP = getAccessPoint('Tourian Escape Room 4 Top Right')
        key = self.getTransition(escapeSrcAP.ExitInfo['DoorPtr'])
        # may not be set in plandomizer
        if key in rooms:
            escapeDstAP = rooms[key]
            escapeTransition = [(escapeSrcAP.Name, escapeDstAP.Name)]
        else:
            escapeTransition = []

        areaTransitions = removeBiTrans(areaTransitions)
        bossTransitions = removeBiTrans(bossTransitions)

        return (areaTransitions, bossTransitions, escapeTransition, GraphUtils.hasMixedTransitions(areaTransitions, bossTransitions))

    def readRoomPtr(self, address=None):
        if self.race is None:
            return self.romFile.readWord(address)
        else:
            return self.race.readDoorTransition(address)

    def getTransition(self, doorPtr):
        # room ptr is in two bytes
        roomPtr = self.readRoomPtr(0x10000 | doorPtr)

        direction = self.romFile.readByte((0x10000 | doorPtr) + 3)

        sx = self.romFile.readByte((0x10000 | doorPtr) + 6)
        sy = self.romFile.readByte()

        distanceToSpawn = self.romFile.readWord()

        if distanceToSpawn == 0:
            # incompatible transition use samus X/Y instead of direction
            # as incompatible transition change the value of direction
            asmAddress = 0x70000 | self.romFile.readWord()

            offset = 0
            b = self.romFile.readByte(asmAddress+3)
            if b == 0x20:
                # ignore original door asm ptr call
                offset += 3
            b = self.romFile.readByte(asmAddress+6)
            if b == 0x20:
                # ignore exit asm ptr call
                offset += 3

            x = self.romFile.readWord(asmAddress+4+offset)
            y = self.romFile.readWord(asmAddress+10+offset)

            return (roomPtr, (sx, sy), (x, y))
        else:
            return (roomPtr, (sx, sy), direction)

    def _patchPresent(self, patchName, patchDict):
        if patchName not in patchDict:
            return False
        value = self.romFile.readByte(patchDict[patchName]['address'])
        return value == patchDict[patchName]['value']

    def patchPresent(self, patchName):
        return self._patchPresent(patchName, self.patches['common']) or self._patchPresent(patchName, self.patches[RomFlavor.flavor])

    def getPatches(self):
        # for display in the solver
        result = []
        def getPatchesFromDict(patchDict):
            nonlocal result
            for patch, patchEntry in patchDict.items():
                if self._patchPresent(patch, patchDict) == True:
                    result.append(patchEntry['desc'])
        getPatchesFromDict(self.flavorPatches)
        getPatchesFromDict(self.patches['common'])
        getPatchesFromDict(self.patches[RomFlavor.flavor])
        return result

    def getRawPatches(self):
        # for interactive solver
        result = {}
        for patchName in self.patches:
            value = self.romFile.readByte(self.patches[patchName]['address'])
            result[self.patches[patchName]['address']] = value

        # add boss detection bytes
        doorPtr = getAccessPoint('PhantoonRoomOut').ExitInfo['DoorPtr']
        doorPtr = (0x10000 | doorPtr) + 10

        result[doorPtr] = self.romFile.readByte(doorPtr)
        result[doorPtr+1] = self.romFile.readByte()

        return result

    def getAllPatches(self):
        # to display in cli solver (for debug use)
        ret = []
        for patch in self.allPatches:
            value = self.romFile.readByte(self.allPatches[patch]['address'])
            if value == self.allPatches[patch]["value"]:
                ret.append(patch)
        return sorted(ret)

    def getPlandoAddresses(self):
        self.romFile.seek(Addresses.getOne('plandoAddresses'))
        addresses = []
        for i in range(128):
            address = self.romFile.readWord()
            if address == 0xFFFF:
                break
            else:
                addresses.append(address)
        return addresses

    def getPlandoTransitions(self, maxTransitions):
        self.romFile.seek(Addresses.getOne('plandoTransitions'))
        addresses = []
        for i in range(maxTransitions):
            srcDoorPtr = self.romFile.readWord()
            destDoorPtr = self.romFile.readWord()
            if srcDoorPtr == 0xFFFF and destDoorPtr == 0xFFFF:
                break
            else:
                addresses.append((srcDoorPtr, destDoorPtr))
        return addresses

    def decompress(self, address):
        # return (size of compressed data, decompressed data)
        return Compressor().decompress(self.romFile, address)

    def getEscapeTimer(self):
        second = self.romFile.readByte(Addresses.getOne('escapeTimer'))
        minute = self.romFile.readByte()

        second = int(second / 16)*10 + second%16
        minute = int(minute / 16)*10 + minute%16

        return "{:02d}:{:02d}".format(minute, second)

    def readLogic(self):
        for flavor in self.flavorPatches:
            if self._patchPresent(flavor, self.flavorPatches):
                return flavor
        return 'vanilla'

    def readObjectives(self, objectives):
        objectives.readGoals(self)

    def readItemMasks(self):
        itemsMask = self.romFile.readWord(Addresses.getOne('itemsMask'))
        beamsMask = self.romFile.readWord(Addresses.getOne('beamsMask'))
        return itemsMask, beamsMask

    def getStartAP(self):
        address = Addresses.getOne('startAP')
        value = self.romFile.readWord(address)

        startLocation = 'Landing Site'
        startArea = 'Crateria Landing Site'
        startPatches = []
        for ap in Logic.accessPoints():
            if ap.Start is not None and 'spawn' in ap.Start and ap.Start['spawn'] == value:
                startLocation = ap.Name
                startArea = ap.Start['solveArea']
                if 'patches' in ap.Start:
                    startPatches = ap.Start['patches']
                break

        return (startLocation, startArea, startPatches)

    # go read all location IDs by area for item split
    def getLocationsIds(self):
        ret = defaultdict(list)
        for area in graphAreas:
            addr = Addresses.getOne('objectives_locs_'+area)
            self.romFile.seek(addr)
            while True:
               idByte = self.romFile.readByte()
               if idByte == 0xff:
                   break
               ret[area].append(idByte)
        return ret

    def loadEventBitMasks(self):
        address = Addresses.getOne('objectiveEventsArray')
        ret = {}
        for i in range(Objectives.maxActiveGoals):
            self.romFile.seek(address + i*2)
            event = self.romFile.readWord()
            byteIndex = event >> 3
            bitMask = 1 << (event & 7)
            ret[i] = {"byteIndex": byteIndex, "bitMask": bitMask}
        return ret

    def getAdditionalEtanks(self):
        address = Addresses.getOne('additionalETanks')
        return self.romFile.readByte(address)
