
import re, struct, sys, os, json, copy, base64, random

from smbool import SMBool
from itemrandomizerweb.Items import ItemManager
from itemrandomizerweb.patches import patches, additional_PLMs
from itemrandomizerweb.stdlib import List
from compression import Compressor
from ips import IPS_Patch
from parameters import appDir
from utils import normalizeRounding

def readWord(romFile):
    r0 = struct.unpack("B", romFile.read(1))[0]
    r1 = struct.unpack("B", romFile.read(1))[0]
    word = (r1 << 8) + r0
    return word

def getWord(w):
    return (w & 0x00FF, (w & 0xFF00) >> 8)

def writeWord(romFile, w):
    (w0, w1) = getWord(w)
    romFile.write(struct.pack('B', w0))
    romFile.write(struct.pack('B', w1))

# layout patches added by randomizers
class RomPatches:
    #### Patches definitions

    ### Layout
    # blue door to access the room with etank+missile
    BlueBrinstarBlueDoor      = 10
    # missile in the first room is a major item and accessible and ceiling is a minor
    BlueBrinstarMissile       = 11
    # shot block instead of bomb blocks for spazer access
    SpazerShotBlock           = 20
    # climb back up red tower from bottom no matter what
    RedTowerLeftPassage       = 21
    # exit red tower top to crateria or back to red tower without power bombs
    RedTowerBlueDoors         = 22
    # shot block in crumble blocks at early supers
    EarlySupersShotBlock      = 23
    # shot block to exit hi jump area
    HiJumpShotBlock           = 30
    # access main upper norfair without anything
    CathedralEntranceWallJump = 31
    # moat bottom block
    MoatShotBlock             = 41
    ## Area rando patches
    # remove crumble block for reverse lower norfair door access
    SingleChamberNoCrumble    = 101
    # remove green gates for reverse maridia access
    AreaRandoGatesBase        = 102
    # remove crab green gate in maridia and blue gate in green brinstar
    AreaRandoGatesOther       = 103
    # disable Green Hill Yellow, Noob Bridge Green, Coude Yellow, and Kronic Boost yellow doors
    AreaRandoBlueDoors        = 104
    

    ### Other
    # Gravity no longer protects from environmental damage (heat, spikes...)
    NoGravityEnvProtection  = 1000
    # Wrecked Ship etank accessible when Phantoo is alive
    WsEtankPhantoonAlive    = 1001
    # Lower Norfair chozo (vanilla access to GT/Screw Area) : disable space jump check
    LNChozoSJCheckDisabled  = 1002
    # Progressive suits patch, mutually exclusive with NoGravityEnvProtection
    ProgressiveSuits        = 1003
    # Nerfed charge beam available from the start
    NerfedCharge            = 1004

    #### Patch sets
    # total randomizer
    TotalBase = [ BlueBrinstarBlueDoor, RedTowerBlueDoors, NoGravityEnvProtection ]
    # tournament and full
    TotalLayout = [ MoatShotBlock, EarlySupersShotBlock,
                    SpazerShotBlock, RedTowerLeftPassage,
                    HiJumpShotBlock, CathedralEntranceWallJump ]

    Total = TotalBase + TotalLayout

    # casual
    TotalCasual = [ BlueBrinstarMissile ] + Total

    # area rando patch set
    AreaSet = [ SingleChamberNoCrumble, AreaRandoGatesBase, AreaRandoGatesOther, AreaRandoBlueDoors ]

    # VARIA specific patch set
    VariaTweaks = [ WsEtankPhantoonAlive, LNChozoSJCheckDisabled ]

    # dessyreqt randomizer
    Dessy = []

    ### Active patches
    ActivePatches = []

    @staticmethod
    def has(patch):
        return SMBool(patch in RomPatches.ActivePatches)

class RomReader:
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
        '0x0': {'name': 'Nothing'}
    }

    patches = {
        'startCeres': {'address': 0x7F1F, 'value': 0xB6, 'desc': "Blue Brinstar and Red Tower blue doors"},
        'startLS': {'address': 0x7F17, 'value': 0xB6, 'desc': "Blue Brinstar and Red Tower blue doors"},
        'layout': {'address': 0x21BD80, 'value': 0xD5, 'desc': "Anti soft lock layout modifications"},
        'casual': {'address': 0x22E879, 'value': 0xF8, 'desc': "Switch Blue Brinstar Etank and missile"},
        'gravityNoHeatProtection': {'address': 0x0869dd, 'value': 0x01, 'desc': "Gravity suit heat protection removed"},
        'progressiveSuits': {'address':0x869df, 'value': 0xF0, 'desc': "Progressive suits"},
        'nerfedCharge': {'address':0x83821, 'value': 0x80, 'desc': "Nerfed charge beam from the start of the game"}, # this value works for both DASH and VARIA variants
        'variaTweaks': {'address': 0x7CC4D, 'value': 0x37, 'desc': "VARIA tweaks"},
        'area': {'address': 0x22D564, 'value': 0xF2, 'desc': "Area layout modifications"},
        'areaLayout': {'address': 0x252FA7, 'value': 0xF8, 'desc': "Area layout additional modifications"}
    }

    allPatches = {
        'AimAnyButton': {'address': 0x175ca, 'value': 0x60, 'vanillaValue': 0xad},
        'animal_enemies': {'address': 0x78418, 'value': 0x3B, 'vanillaValue': 0x48},
        # all the modifications from animals are included in animal_enemies...
        #'animals': {'address': 0x7841D, 'value': 0x8C, 'vanillaValue': 0x18},
        'area_rando_blue_doors': {'address': 0x7823E, 'value': 0x3B, 'vanillaValue': 0x66},
        'area_rando_door_transition': {'address': 0x852BA, 'value': 0x20, 'vanillaValue': 0xad},
        'area_rando_escape': {'address': 0x15f38, 'value': 0x5c, 'vanillaValue': 0xbd},
        'area_rando_layout_base': {'address': 0x788A0, 'value': 0x2B, 'vanillaValue': 0x26},
        'area_rando_layout': {'address': 0x78666, 'value': 0x62, 'vanillaValue': 0x64},
        'bomb_torizo': {'address': 0x7FDC, 'value': 0xF2, 'vanillaValue': 0x20},
        'brinstar_map_room': {'address': 0x784EC, 'value': 0x3B, 'vanillaValue': 0x42},
        'credits_varia': {'address': 0x44B, 'value': 0x5C, 'vanillaValue': 0xa2},
        'dachora': {'address': 0x22A173, 'value': 0xC9, 'vanillaValue': 0xc8},
        'draygonimals': {'address': 0x1ADAC, 'value': 0x60, 'vanillaValue': 0xff},
        'early_super_bridge': {'address': 0x22976B, 'value': 0xC7, 'vanillaValue': 0x43},
        'elevators_doors_speed': {'address': 0x2E9D, 'value': 0x08, 'vanillaValue': 0x04},
        'endingtotals': {'address': 0x7FDC, 'value': 0x7B, 'vanillaValue': 0x20},
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
        'Mother_Brain_Cutscene_Edits': {'address': 0x148824, 'value': 0x01, 'vanillaValue': 0x40},
        'Suit_acquisition_animation_skip': {'address': 0x020717, 'value': 0xea, 'vanillaValue': 0x22},
        'Fix_Morph_and_Missiles_Room_State': {'address': 0x07e655, 'value': 0xea, 'vanillaValue': 0x89},
        'Fix_heat_damage_speed_echoes_bug': {'address': 0x08b629, 'value': 0x01, 'vanillaValue': 0x00},
        'Disable_GT_Code': {'address': 0x15491c, 'value': 0x80, 'vanillaValue': 0xd0},
        'Disable_Space_Time_select_in_menu': {'address': 0x013175, 'value': 0x01, 'vanillaValue': 0x08},
        'Fix_Morph_Ball_Hidden_Chozo_PLMs': {'address': 0x0268ce, 'value': 0x04, 'vanillaValue': 0x02},
        'Fix_Screw_Attack_selection_in_menu': {'address': 0x0134c5, 'value': 0x0c, 'vanillaValue': 0x0a},
        'No_Music': {'address': 0x278413, 'value': 0x6f, 'vanillaValue': 0xcd}
    }

    @staticmethod
    def getDefaultPatches():
        # called by the isolver in seedless mode
        # activate only layout patch (the most common one) and blue bt/red tower blue doors
        ret = {}
        for patch in RomReader.patches:
            if patch in ['layout', 'startLS']:
                ret[RomReader.patches[patch]['address']] = RomReader.patches[patch]['value']
            else:
                ret[RomReader.patches[patch]['address']] = 0xFF

        # add phantoon door ptr used by boss rando detection
        from graph_access import getAccessPoint
        doorPtr = getAccessPoint('PhantoonRoomOut').ExitInfo['DoorPtr']
        doorPtr = (0x10000 | doorPtr) + 10
        ret[doorPtr] = 0
        ret[doorPtr+1] = 0

        return ret

    def __init__(self, romFile, magic=None):
        self.romFile = romFile
        self.race = None
        if magic is not None:
            from race_mode import RaceModeReader
            self.race = RaceModeReader(self, magic)

    def readWord(self):
        return readWord(self.romFile)

    def getItemBytes(self):
        value1 = struct.unpack("B", self.romFile.read(1))[0]
        value2 = struct.unpack("B", self.romFile.read(1))[0]
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

        # dessyreqt randomizer make some missiles non existant, detect it
        # 0xeedb is missile item
        # 0x786de is Morphing Ball location
        self.romFile.seek(address+4)
        value3 = struct.unpack("B", self.romFile.read(1))[0]
        if (value3 == int('0x1a', 16)
            and int(itemCode, 16) == int('0xeedb', 16)
            and address != int('0x786DE', 16)):
            return hex(0)
        else:
            return itemCode

    def getMajorsSplit(self):
        address = 0x17B6C
        self.romFile.seek(address)
        split = chr(struct.unpack("B", self.romFile.read(1))[0])
        if split in ['F', 'M', 'Z']:
            splits = {
                'F': 'Full',
                'Z': 'Chozo',
                'M': 'Major'
            }
            return splits[split]
        else:
            return None

    def loadItems(self, locations):
        majorsSplit = self.getMajorsSplit()

        if majorsSplit == None:
            isFull = False
            chozoItems = {}
        for loc in locations:
            if 'Boss' in loc['Class']:
                loc["itemName"] = "Nothing"
                continue
            item = self.getItem(loc["Address"], loc["Visibility"])
            try:
                loc["itemName"] = self.items[item]["name"]
            except:
                # race seeds
                loc["itemName"] = "Nothing"
                item = '0x0'
            if majorsSplit == None:
                if 'Major' in loc['Class'] and self.items[item]['name'] in ['Missile', 'Super', 'PowerBomb']:
                    isFull = True
                if 'Minor' in loc['Class'] and self.items[item]['name'] not in ['Missile', 'Super', 'PowerBomb']:
                    isFull = True
                if 'Chozo' in loc['Class']:
                    if loc['itemName'] in chozoItems:
                        chozoItems[loc['itemName']] = chozoItems[loc['itemName']] + 1
                    else:
                        chozoItems[loc['itemName']] = 1

        # if majors split is not written in the seed, use an heuristic
        if majorsSplit == None:
            isChozo = self.isChozoSeed(chozoItems)
            if isChozo == True:
                return 'Chozo'
            elif isFull == True:
                return 'Full'
            else:
                return 'Major'
        else:
            return majorsSplit

    def isChozoSeed(self, chozoItems):
        # we have 2 Missiles, 2 Supers and 1 PB in the chozo locations
        if 'Missile' not in chozoItems:
            return False
        if chozoItems['Missile'] != 2:
            return False
        if 'Super' not in chozoItems:
            return False
        if chozoItems['Super'] != 2:
            return False
        if 'PowerBomb' not in chozoItems:
            return False
        if chozoItems['PowerBomb'] != 1:
            return False

        # we have at least 3 E and 1 R
        if 'ETank' not in chozoItems:
            return False
        if chozoItems['ETank'] < 3:
            return False
        if 'Reserve' not in chozoItems:
            return False

        # all the majors items which can't be superfuned
        if 'Charge' not in chozoItems:
            return False
        if 'Morph' not in chozoItems:
            return False
        if 'Ice' not in chozoItems:
            return False

        return True

    def loadTransitions(self):
        # return the transitions
        from graph_access import accessPoints, getRooms
        rooms = getRooms()
        bossTransitions = {}
        areaTransitions = {}
        for accessPoint in accessPoints:
            if accessPoint.isInternal() == True:
                continue
            (destRoomPtr, destEntryScreen) = self.getTransition(accessPoint.ExitInfo['DoorPtr'])
            destAP = rooms[(destRoomPtr, destEntryScreen)]
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

        return (removeBiTrans(areaTransitions), removeBiTrans(bossTransitions))

    def getTransition(self, doorPtr):
        self.romFile.seek(0x10000 | doorPtr)

        # room ptr is in two bytes
        v1 = struct.unpack("B", self.romFile.read(1))[0]
        v2 = struct.unpack("B", self.romFile.read(1))[0]

        self.romFile.seek((0x10000 | doorPtr) + 6)
        sx = struct.unpack("B", self.romFile.read(1))[0]
        sy = struct.unpack("B", self.romFile.read(1))[0]

        return (v1 | (v2 << 8), (sx, sy))

    def patchPresent(self, patchName):
        self.romFile.seek(self.patches[patchName]['address'])
        value = struct.unpack("B", self.romFile.read(1))[0]
        return value == self.patches[patchName]['value']

    def getPatches(self):
        # for display in the solver
        result = []
        for patch in self.patches:
            if self.patchPresent(patch) == True:
                result.append(self.patches[patch]['desc'])
        return result

    def getRawPatches(self):
        # for interactive solver
        result = {}
        for patchName in self.patches:
            self.romFile.seek(self.patches[patchName]['address'])
            value = struct.unpack("B", self.romFile.read(1))[0]
            result[self.patches[patchName]['address']] = value

        # add boss detection bytes
        from graph_access import getAccessPoint
        doorPtr = getAccessPoint('PhantoonRoomOut').ExitInfo['DoorPtr']
        doorPtr = (0x10000 | doorPtr) + 10

        self.romFile.seek(doorPtr)
        result[doorPtr] = struct.unpack("B", self.romFile.read(1))[0]
        self.romFile.seek(doorPtr+1)
        result[doorPtr+1] = struct.unpack("B", self.romFile.read(1))[0]

        return result

    def getAllPatches(self):
        # to display in cli solver (for debug use)
        ret = []
        for patch in self.allPatches:
            self.romFile.seek(self.allPatches[patch]['address'])
            value = struct.unpack("B", self.romFile.read(1))[0]
            if value == self.allPatches[patch]["value"]:
                ret.append(patch)
        return sorted(ret)

    def getPlandoAddresses(self):
        self.romFile.seek(0x2F6000)
        addresses = []
        for i in range(128):
            address = self.readWord()
            if address == 0xFFFF:
                break
            else:
                addresses.append(address)
        return addresses

    def getPlandoTransitions(self, maxTransitions):
        self.romFile.seek(0x2F6100)
        addresses = []
        for i in range(maxTransitions):
            srcDoorPtr = self.readWord()
            destDoorPtr = self.readWord()
            if srcDoorPtr == 0xFFFF and destDoorPtr == 0xFFFF:
                break
            else:
                addresses.append((srcDoorPtr, destDoorPtr))
        return addresses

    def decompress(self, address):
        # return (size of compressed data, decompressed data)
        return Compressor().decompress(self.romFile, address)

class RomPatcher:
    # standard:
    # Instantly open G4 passage when all bosses are killed
    #   g4_skip.ips
    # Wake up zebes when going right from morph
    #   wake_zebes.ips
    # Seed display
    #   seed_display.ips
    # Custom credits with stats
    #   credits.ips
    # Custom credits with stats (tracking code)
    #   tracking.ips
    # Removes Gravity Suit heat protection
    # Mother Brain Cutscene Edits
    # Suit acquisition animation skip
    # Fix Morph & Missiles Room State
    # Fix heat damage speed echoes bug
    # Disable GT Code
    # Disable Space/Time select in menu
    # Fix Morph Ball Hidden/Chozo PLM's
    # Fix Screw Attack selection in menu
    #
    # optional (Kejardon):
    # Allows the aim buttons to be assigned to any button
    #   AimAnyButton.ips
    #
    # optional (Scyzer):
    # Remove fanfare when picking up an item
    #   itemsounds.ips
    # Allows Samus to start spinning in mid air after jumping or falling
    #   spinjumprestart.ips
    #
    # optional standard (imcompatible with MSU1 music):
    # Max Ammo Display
    #   max_ammo_display.ips
    #
    # optional (DarkShock):
    # Play music with MSU1 chip on SD2SNES
    #   supermetroid_msu1.ips
    #
    # layout:
    # Disable respawning blocks at dachora pit
    #   dachora.ips
    # Make it possible to escape from below early super bridge without bombs
    #   early_super_bridge.ips
    # Replace bomb blocks with shot blocks before Hi-Jump
    #   high_jump.ips
    # Replace bomb blocks with shot blocks at Moat
    #   moat.ips
    # Raise platform in first heated norfair room to not require hi-jump
    #   nova_boost_platform.ip
    # Raise platforms in red tower bottom to always be able to get back up
    #   red_tower.ips
    # Replace bomb blocks with shot blocks before Spazer
    #   spazer.ips
    IPSPatches = {
        'Standard': ['new_game.ips', 'plm_spawn.ips',
                     'credits_varia.ips', 'seed_display.ips', 'tracking.ips',
                     'wake_zebes.ips', 'g4_skip.ips', # XXX those are door ASMs
                     'Mother_Brain_Cutscene_Edits',
                     'Suit_acquisition_animation_skip', 'Fix_Morph_and_Missiles_Room_State',
                     'Fix_heat_damage_speed_echoes_bug', 'Disable_GT_Code',
                     'Disable_Space_Time_select_in_menu', 'Fix_Morph_Ball_Hidden_Chozo_PLMs',
                     'Fix_Screw_Attack_selection_in_menu',
                     'Removes_Gravity_Suit_heat_protection',
                     'AimAnyButton.ips', 'endingtotals.ips',
                     'supermetroid_msu1.ips', 'max_ammo_display.ips'],
        'VariaTweaks' : ['ws_etank.ips', 'ln_chozo_sj_check_disable.ips', 'ln_chozo_platform.ips', 'bomb_torizo.ips'],
        'Layout': ['dachora.ips', 'early_super_bridge.ips', 'high_jump.ips', 'moat.ips', 'spospo_save.ips',
                   'nova_boost_platform.ips', 'red_tower.ips', 'spazer.ips', 'brinstar_map_room.ips'],
        'Optional': ['itemsounds.ips', 'rando_speed.ips',
                     'spinjumprestart.ips', 'elevators_doors_speed.ips', 'No_Music',
                     'skip_intro.ips', 'skip_ceres.ips', 'animal_enemies.ips', 'animals.ips',
                     'draygonimals.ips', 'escapimals.ips', 'gameend.ips', 'grey_door_animals.ips',
                     'low_timer.ips', 'metalimals.ips', 'phantoonimals.ips', 'ridleyimals.ips'],
        'Area': ['area_rando_blue_doors.ips', 'area_rando_layout.ips', 'area_rando_door_transition.ips','area_rando_escape.ips','area_rando_escape_ws_fix.ips' ]
    }

    def __init__(self, romFileName=None, magic=None, plando=False):
        self.romFileName = romFileName
        self.race = None
        if romFileName == None:
            self.romFile = FakeROM()
        else:
            self.romFile = open(romFileName, 'rb+')
        if magic is not None:
            from race_mode import RaceModePatcher
            self.race = RaceModePatcher(self, magic, plando)
        self.ipsPatches = [] # IPS_Patch objects list

    def end(self):
        self.romFile.close()

    def writeWord(self, w):
        writeWord(self.romFile, w)

    def writeItemCode(self, item, visibility, address):
        itemCode = ItemManager.getItemTypeCode(item, visibility)
        if self.race is None:
            self.romFile.seek(address)
            self.writeWord(itemCode)
        else:
            self.race.writeItemCode(address, itemCode)

    def writeNothing(self, itemLoc):
        loc = itemLoc['Location']
        if 'Boss' in loc['Class']:
            return
        # missile
        self.writeItemCode({'Code': 0xeedb}, loc['Visibility'], loc['Address'])
        self.romFile.seek(loc['Address'] + 4)
        # morph ball slot. all Nothing at non-Morph loc will disappear
        # when morph loc item is collected
        self.romFile.write(struct.pack('B', 0x1a))

    def writeItem(self, itemLoc):
        loc = itemLoc['Location']
        if 'Boss' in loc['Class']:
            raise ValueError('Cannot write Boss location')
        #print('write ' + itemLoc['Item']['Type'] + ' at ' + loc['Name'])
        self.writeItemCode(itemLoc['Item'], loc['Visibility'], loc['Address'])

        self.romFile.seek(loc['Address'] + 4)
        # if nothing was written at this loc before (in plando), then restore the vanilla value
        self.romFile.write(struct.pack('B', loc['Id']))

    def writeItemsLocs(self, itemLocs):
        self.nItems = 0
        self.nothingAtMorph = False
        for itemLoc in itemLocs:
            if 'Boss' in itemLoc['Location']['Class']:
                continue
            isMorph = itemLoc['Location']['Name'] == 'Morphing Ball'
            if itemLoc['Item']['Category'] == 'Nothing':
                self.writeNothing(itemLoc)
                if isMorph:
                    # nothing at morph gives a missile pack
                    self.nothingAtMorph = True
                    self.nItems += 1
            else:
                self.nItems += 1
                self.writeItem(itemLoc)
            if isMorph:
                self.patchMorphBallEye(itemLoc['Item'])

    # trigger morph eye enemy on whatever item we put there,
    # not just morph ball
    def patchMorphBallEye(self, item):
#        print('Eye item = ' + item['Type'])
        # consider Nothing as missile, because if it is at morph ball it will actually be a missile
        isAmmo = item['Category'] == 'Ammo' or item['Category'] == 'Nothing'
        isMissile = item['Type'] == 'Missile' or item['Category'] == 'Nothing'
        # category to check
        if ItemManager.isBeam(item):
            cat = 0xA8 # collected beams
        elif item['Type'] == 'ETank':
            cat = 0xC4 # max health
        elif item['Type'] == 'Reserve':
            cat = 0xD4 # max reserves
        elif isMissile:
            cat = 0xC8 # max missiles
        elif item['Type'] == 'Super':
            cat = 0xCC # max supers
        elif item['Type'] == 'PowerBomb':
            cat = 0xD0 # max PBs
        else:
            cat = 0xA4 # collected items
        # comparison/branch instruction
        # the branch is taken if we did NOT collect item yet
        if item['Category'] == 'Energy' or isAmmo:
            comp = 0xC9 # CMP (immediate)
            branch = 0x30 # BMI
        else:
            comp = 0x89 # BIT (immediate)
            branch = 0xF0 # BEQ
        # what to compare to
        if item['Type'] == 'ETank':
            operand = 0x65 # < 100
        elif item['Type'] == 'Reserve' or isAmmo:
            operand = 0x1 # < 1
        elif ItemManager.isBeam(item):
            operand = ItemManager.BeamBits[item['Type']]
        else:
            operand = ItemManager.ItemBits[item['Type']]
        self.patchMorphBallCheck(0x1410E6, cat, comp, operand, branch) # eye main AI
        self.patchMorphBallCheck(0x1468B2, cat, comp, operand, branch) # head main AI

    def patchMorphBallCheck(self, offset, cat, comp, operand, branch):
        # actually patch enemy AI
        self.romFile.seek(offset)
        self.romFile.write(struct.pack('B', cat))
        self.romFile.seek(offset+2)
        self.romFile.write(struct.pack('B', comp))
        self.writeWord(operand)
        self.romFile.write(struct.pack('B', branch))

    def writeItemsNumber(self):
        # write total number of actual items for item percentage patch (patch the patch)
        for addr in [0x5E64E, 0x5E6AB]:
            self.romFile.seek(addr)
            self.romFile.write(struct.pack('B', self.nItems))

    def addIPSPatches(self, patches):
        for patchName in patches:
            self.applyIPSPatch(patchName)

    def customSprite(self, sprite):
        self.applyIPSPatch(sprite, ipsDir='itemrandomizerweb/patches/sprites')

    def applyIPSPatches(self, startAP="Landing Site",
                        optionalPatches=[], noLayout=False, suitsMode="Classic",
                        area=False, bosses=False, areaLayoutBase=False,
                        noVariaTweaks=False, nerfedCharge=False,
                        noEscapeRando=False, noRemoveEscapeEnemies=False):
        try:
            # apply standard patches
            stdPatches = []
            plms = []
            # apply race mode first because it fills the rom with a bunch of crap
            if self.race is not None:
                stdPatches.append('race_mode.ips')
            stdPatches += RomPatcher.IPSPatches['Standard'][:]
            if self.race is not None:
                stdPatches.append('race_mode_credits.ips')
            if suitsMode != "Classic":
                stdPatches.remove('Removes_Gravity_Suit_heat_protection')
            if suitsMode == "Progressive":
                stdPatches.append('progressive_suits.ips')
            if nerfedCharge == True:
                stdPatches.append('nerfed_charge.ips')
            if bosses == True or area == True:
                stdPatches.append('ws_save.ips')
                plms.append('WS_Save_Blinking_Door')
            if bosses == True:
                stdPatches.append("Phantoon_Eye_Door")

            for patchName in stdPatches:
                self.applyIPSPatch(patchName)

            if noLayout == False:
                # apply layout patches
                for patchName in RomPatcher.IPSPatches['Layout']:
                    self.applyIPSPatch(patchName)
            if noVariaTweaks == False:
                # VARIA tweaks
                for patchName in RomPatcher.IPSPatches['VariaTweaks']:
                    self.applyIPSPatch(patchName)

            # apply optional patches
            for patchName in optionalPatches:
                if patchName in RomPatcher.IPSPatches['Optional']:
                    self.applyIPSPatch(patchName)

            # apply area patches
            if area == True:
                if areaLayoutBase == True:
                    RomPatcher.IPSPatches['Area'].remove('area_rando_layout.ips')
                    RomPatcher.IPSPatches['Area'].append('area_rando_layout_base.ips')
                if noEscapeRando == True:
                    RomPatcher.IPSPatches['Area'].remove('area_rando_escape.ips')
                    RomPatcher.IPSPatches['Area'].remove('area_rando_escape_ws_fix.ips')
                else:
                    if noRemoveEscapeEnemies == True:
                        RomPatcher.IPSPatches['Area'].append('Escape_Rando_Enable_Enemies')
                    plms.append("WS_Map_Grey_Door")
                for patchName in RomPatcher.IPSPatches['Area']:
                    self.applyIPSPatch(patchName)
            elif bosses == True:
                self.applyIPSPatch('area_rando_door_transition.ips')
            self.applyPLMs(plms)
            self.applyStartAP(startAP)
        except Exception as e:
            raise Exception("Error patching {}. ({})".format(self.romFileName, e))

    def applyIPSPatch(self, patchName, patchDict=None, ipsDir="itemrandomizerweb/patches"):
        if patchDict is None:
            patchDict = patches
        print("Apply patch {}".format(patchName))
        if patchName in patchDict:
            patch = IPS_Patch(patchDict[patchName])
        else:
            # look for ips file
            patch = IPS_Patch.load(appDir + '/' + ipsDir + '/' + patchName)
        self.ipsPatches.append(patch)

    def applyStartAP(self, apName):
        from graph_access import getAccessPoint
        ap = getAccessPoint(apName)
        (w0, w1) = getWord(ap.Start)
        patchDict = {
            'StartAP': {
                0x10F200: [w0, w1]
            }
        }
        self.applyIPSPatch('StartAP', patchDict)
        # TODO handle custom saves

    # adds ad-hoc "IPS patches" for additional PLM tables
    def applyPLMs(self, plms):
        # compose a dict (room, state, door) => PLM array
        # 'PLMs' being a 6 byte arrays
        plmDict = {}
        for p in plms:
            plm = additional_PLMs[p]
            room = plm['room']
            state = 0
            if 'state' in plm:
                state = plm['state']
            door = 0
            if 'door' in plm:
                door = plm['door']
            k = (room, state, door)
            if k not in plmDict:
                plmDict[k] = []
            plmDict[k] += plm['plm_bytes_list']
        # make two patches out of this dict
        # use instances vars because of terrible python scoping
        self.plmTblAddr = 0x7E9A0 # moves downwards
        self.plmPatchData = []
        self.roomTblAddr = 0x7EC00 # moves upwards
        self.roomPatchData = []
        self.plmTblOffset = self.plmTblAddr
        def appendPlmBytes(bytez):
            self.plmPatchData += bytez
            self.plmTblOffset += len(bytez)
        def addRoomPatchData(bytez):
            self.roomPatchData = bytez + self.roomPatchData
            self.roomTblAddr -= len(bytez)
        for roomKey, plmList in plmDict.items():
            entryAddr = self.plmTblOffset
            roomData = []
            for plmBytes in plmList:
                assert len(plmBytes) == 6, "Invalid PLM entry for roomKey " + str(roomKey) + ": PLM list len is " + str(len(plmBytes))
                appendPlmBytes(plmBytes)
            appendPlmBytes([0x0, 0x0]) # list terminator
            def appendRoomWord(w, data):
                (w0, w1) = getWord(w)
                data += [w0, w1]
            for i in range(3):
                appendRoomWord(roomKey[i], roomData)
            appendRoomWord(entryAddr, roomData)
            addRoomPatchData(roomData)
        # write room table terminator
        addRoomPatchData([0x0] * 8)
        assert self.plmTblOffset < self.roomTblAddr, "Spawn PLM table overlap"
        patchDict = {
            "PLM_Spawn_Tables" : {
                self.plmTblAddr: self.plmPatchData,
                self.roomTblAddr: self.roomPatchData
            }
        }
        self.applyIPSPatch("PLM_Spawn_Tables", patchDict)

    def commitIPS(self):
        if self.romFileName is not None:
            # CLI
            for ips in self.ipsPatches:
                ips.applyFile(self.romFile)
        else:
            # Web
            mergedIPS = IPS_Patch()
            for ips in self.ipsPatches:
                mergedIPS.append(ips)
            patchData = mergedIPS.encode()
            self.romFile.data["ips"] = base64.b64encode(patchData).decode()
            if mergedIPS.truncate_length is not None:
                self.romFile.data["truncate_length"] = mergedIPS.truncate_length
            self.romFile.data["max_size"] = mergedIPS.max_size

    def writeSeed(self, seed):
        random.seed(seed)
        seedInfo = random.randint(0, 0xFFFF)
        seedInfo2 = random.randint(0, 0xFFFF)
        self.romFile.seek(0x2FFF00)
        self.writeWord(seedInfo)
        self.writeWord(seedInfo2)

    def writeMagic(self):
        if self.race is not None:
            self.race.writeMagic()

    def writeMajorsSplit(self, majorsSplit):
        address = 0x17B6C
        if majorsSplit == 'Chozo':
            char = 'Z'
        elif majorsSplit == 'Full':
            char = 'F'
        else:
            char = 'M'
        self.romFile.seek(address)
        self.romFile.write(struct.pack('B', ord(char)))

    def getItemQty(self, itemLocs, itemType):
        q = len([il for il in itemLocs if il['Item']['Type'] == itemType])
        if itemType == 'Missile' and self.nothingAtMorph == True:
            q += 1
        # in vcr mode if the seed has stuck we may not have these items, return at least 1
        return max(q, 1)

    def getMinorsDistribution(self, itemLocs):
        dist = {}
        minQty = 100
        minors = ['Missile', 'Super', 'PowerBomb']
        for m in minors:
            q = float(self.getItemQty(itemLocs, m))
            dist[m] = {'Quantity' : q }
            if q < minQty:
                minQty = q
        for m in minors:
            dist[m]['Proportion'] = dist[m]['Quantity']/minQty
        
        return dist

    def getAmmoPct(self, minorsDist):
        q = 0
        for m,v in minorsDist.items():
            q += v['Quantity']
        return 100*q/66

    def writeRandoSettings(self, settings, itemLocs):
        dist = self.getMinorsDistribution(itemLocs)
        tanks = self.getItemQty(itemLocs, 'ETank') + self.getItemQty(itemLocs, 'Reserve')

        address = 0x2736C0
        value = "{:>2}".format(int(dist['Missile']['Quantity']))
        line = " MISSILE PACKS               %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " missile packs ............. %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        value = "{:>2}".format(int(dist['Super']['Quantity']))
        line = " SUPER PACKS                 %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " super packs ............... %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        value = "{:>2}".format(int(dist['PowerBomb']['Quantity']))
        line = " POWER BOMB PACKS            %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " power bomb packs .......... %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        value = "{:>2}".format(int(tanks))
        line = " HEALTH TANKS                %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " health tanks .............. %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        # value = " "+settings.qty['energy'].upper()
        # line = " ENERGY QUANTITY ......%s " % value.rjust(8, '.')
        # self.writeCreditsString(address, 0x04, line)
        address += 0x40

        value = " "+settings.progSpeed.upper()
        line = " PROGRESSION SPEED ....%s " % value.rjust(8, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        line = " PROGRESSION DIFFICULTY  %s " % settings.progDiff.upper()
        self.writeCreditsString(address, 0x04, line)
        address += 0x80 # skip item distrib title

        param = (' SUITS RESTRICTION ........%s', 'Suits')
        line = param[0] % ('. ON' if settings.restrictions[param[1]] == True else ' OFF')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        value = " "+settings.restrictions['Morph'].upper()
        line  = " MORPH PLACEMENT .....%s" % value.rjust(9, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        for superFun in [(' SUPER FUN COMBAT .........%s', 'Combat'),
                         (' SUPER FUN MOVEMENT .......%s', 'Movement'),
                         (' SUPER FUN SUITS ..........%s', 'Suits')]:
            line = superFun[0] % ('. ON' if superFun[1] in settings.superFun else ' OFF')
            self.writeCreditsString(address, 0x04, line)
            address += 0x40

        value = "%.1f %.1f %.1f" % (dist['Missile']['Proportion'], dist['Super']['Proportion'], dist['PowerBomb']['Proportion'])
        line = " AMMO DISTRIBUTION  %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " ammo distribution  %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        # write ammo/energy pct
        address = 0x273C40
        (ammoPct, energyPct) = (int(self.getAmmoPct(dist)), int(100*tanks/18))
        line = " AVAILABLE AMMO {:>3}% ENERGY {:>3}%".format(ammoPct, energyPct)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40
        line = " available ammo {:>3}% energy {:>3}%".format(ammoPct, energyPct)
        self.writeCreditsStringBig(address, line, top=False)

    def writeSpoiler(self, itemLocs, progItemLocs=None):
        # keep only majors, filter out Etanks and Reserve
        fItemLocs = List.filter(lambda il: il['Item']['Category'] not in ['Ammo', 'Nothing', 'Energy'],
                                itemLocs)
        # add location of the first instance of each minor
        for t in ['Missile', 'Super', 'PowerBomb']:
            itLoc = None
            if progItemLocs is not None:
                itLoc = next((il for il in progItemLocs if il['Item']['Type'] == t), None)
            if itLoc is None:
                itLoc = next((il for il in itemLocs if il['Item']['Type'] == t), None)
            if itLoc is not None: # in vcr mode if the seed has stucked we may not have these minors
                fItemLocs.append(itLoc)
        regex = re.compile(r"[^A-Z0-9\.,'!: ]+")

        itemLocs = {}
        for iL in fItemLocs:
            itemLocs[iL['Item']['Name']] = iL['Location']['Name']

        def prepareString(s, isItem=True):
            s = s.upper()
            # remove chars not displayable
            s = regex.sub('', s)
            # remove space before and after
            s = s.strip()
            # limit to 30 chars, add one space before
            # pad to 32 chars
            if isItem is True:
                s = " " + s[0:30]
                s = s.ljust(32)
            else:
                s = " " + s[0:30] + " "
                s = " " + s.rjust(31, '.')

            return s

        isRace = self.race is not None
        address = 0x2f5240
        if isRace:
            addr = address - 0x40
            data = [0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x1008, 0x1013, 0x1004, 0x100c, 0x007f, 0x100b, 0x100e, 0x1002, 0x1000, 0x1013, 0x1008, 0x100e, 0x100d, 0x1012, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f]
            for i in range(0x20):
                w = data[i]
                self.romFile.seek(addr)
                self.race.writeWordMagic(w)
                addr += 0x2
        # standard item order
        items = ["Missile", "Super Missile", "Power Bomb",
                 "Charge Beam", "Ice Beam", "Wave Beam", "Spazer", "Plasma Beam",
                 "Varia Suit", "Gravity Suit",
                 "Morph Ball", "Bomb", "Spring Ball", "Screw Attack",
                 "Hi-Jump Boots", "Space Jump", "Speed Booster",
                 "Grappling Beam", "X-Ray Scope"]
        displayNames = {}
        if progItemLocs is not None:
            # reorder it with progression indices
            prog = ord('A')
            idx = 0
            progNames = [il['Item']['Name'] for il in progItemLocs]
            for i in range(len(progNames)):
                item = progNames[i]
                if item in items and item not in displayNames:
                    items.remove(item)
                    items.insert(idx, item)
                    displayNames[item] = chr(prog + i) + ": " + item
                    idx += 1
        for item in items:
            # super fun removes items
            if item not in itemLocs:
                continue
            display = item
            if item in displayNames:
                display = displayNames[item]
            itemName = prepareString(display)
            locationName = prepareString(itemLocs[item], isItem=False)

            self.writeCreditsString(address, 0x04, itemName, isRace)
            self.writeCreditsString((address + 0x40), 0x18, locationName, isRace)

            address += 0x80

        # we need 19 items displayed, if we've removed majors, add some blank text
        for i in range(19 - len(fItemLocs)):
            self.writeCreditsString(address, 0x04, prepareString(""), isRace)
            self.writeCreditsString((address + 0x40), 0x18, prepareString(""), isRace)

            address += 0x80

        self.patchBytes(address, [0, 0, 0, 0], isRace)

    def writeCreditsString(self, address, color, string, isRace=False):
        array = [self.convertCreditsChar(color, char) for char in string]
        self.patchBytes(address, array, isRace)

    def writeCreditsStringBig(self, address, string, top=True):
        array = [self.convertCreditsCharBig(char, top) for char in string]
        self.patchBytes(address, array)

    def convertCreditsChar(self, color, byte):
        if byte == ' ':
            ib = 0x7f
        elif byte == '!':
            ib = 0x1F
        elif byte == ':':
            ib = 0x1E
        elif byte == '\\':
            ib = 0x1D
        elif byte == '_':
            ib = 0x1C
        elif byte == ',':
            ib = 0x1B
        elif byte == '.':
            ib = 0x1A
        else:
            ib = ord(byte) - 0x41

        if ib == 0x7F:
            return 0x007F
        else:
            return (color << 8) + ib

    def convertCreditsCharBig(self, byte, top=True):
        # from: https://jathys.zophar.net/supermetroid/kejardon/TextFormat.txt
        # 2-tile high characters:
        # A-P = $XX20-$XX2F(TOP) and $XX30-$XX3F(BOTTOM)
        # Q-Z = $XX40-$XX49(TOP) and $XX50-$XX59(BOTTOM)
        # ' = $XX4A, $XX7F
        # " = $XX4B, $XX7F
        # . = $XX7F, $XX5A
        # 0-9 = $XX60-$XX69(TOP) and $XX70-$XX79(BOTTOM)
        # % = $XX6A, $XX7A

        if byte == ' ':
            ib = 0x7F
        elif byte == "'":
            if top == True:
                ib = 0x4A
            else:
                ib = 0x7F
        elif byte == '"':
            if top == True:
                ib = 0x4B
            else:
                ib = 0x7F
        elif byte == '.':
            if top == True:
                ib = 0x7F
            else:
                ib = 0x5A
        elif byte == '%':
            if top == True:
                ib = 0x6A
            else:
                ib = 0x7A

        byte = ord(byte)
        if byte >= ord('A') and byte <= ord('P'):
            ib = byte - 0x21
        elif byte >= ord('Q') and byte <= ord('Z'):
            ib = byte - 0x11
        elif byte >= ord('a') and byte <= ord('p'):
            ib = byte - 0x31
        elif byte >= ord('q') and byte <= ord('z'):
            ib = byte - 0x21
        elif byte >= ord('0') and byte <= ord('9'):
            if top == True:
                ib = byte + 0x30
            else:
                ib = byte + 0x40

        return ib

    def patchBytes(self, address, array, isRace=False):
        self.romFile.seek(address)
        for w in array:
            if not isRace:
                self.writeWord(w)
            else:
                self.race.writeWordMagic(w)

    # write area randomizer transitions to ROM
    # doorConnections : a list of connections. each connection is a dictionary describing
    # - where to write in the ROM :
    # DoorPtr : door pointer to write to
    # - what to write in the ROM :
    # RoomPtr, direction, bitflag, cap, screen, distanceToSpawn : door properties
    # * if SamusX and SamusY are defined in the dict, custom ASM has to be written
    #   to reposition samus, and call doorAsmPtr if non-zero. The written Door ASM
    #   property shall point to this custom ASM.
    # * if not, just write doorAsmPtr as the door property directly.
    def writeDoorConnections(self, doorConnections):
        asmAddress = 0x7F800
        for conn in doorConnections:
            # write door ASM for transition doors (code and pointers)
#            print('Writing door connection ' + conn['ID'])
            doorPtr = conn['DoorPtr']
            roomPtr = conn['RoomPtr']
            if roomPtr == 0x93fe: # west ocean
                self.patchWestOcean(doorPtr)
            if doorPtr == 0x91ce: # kraid room exit door
                self.patchKraidExit(roomPtr)
            self.romFile.seek(0x10000 + doorPtr)

            # write room ptr
            self.romFile.write(struct.pack('B', roomPtr & 0x000FF))
            self.romFile.write(struct.pack('B', (roomPtr & 0x0FF00) >> 8))

            # write bitflag (if area switch we have to set bit 0x40, and remove it if same area)
            self.romFile.write(struct.pack('B', conn['bitFlag']))

            # write direction
            self.romFile.write(struct.pack('B', conn['direction']))

            # write door cap x
            self.romFile.write(struct.pack('B', conn['cap'][0]))

            # write door cap y
            self.romFile.write(struct.pack('B', conn['cap'][1]))

            # write screen x
            self.romFile.write(struct.pack('B', conn['screen'][0]))

            # write screen y
            self.romFile.write(struct.pack('B', conn['screen'][1]))

            # write distance to spawn
            self.romFile.write(struct.pack('B', conn['distanceToSpawn'] & 0x00FF))
            self.romFile.write(struct.pack('B', (conn['distanceToSpawn'] & 0xFF00) >> 8))

            # write door asm
            asmPatch = []
            # call original door asm ptr if needed
            if conn['doorAsmPtr'] != 0x0000:
                # endian convert
                (D0, D1) = (conn['doorAsmPtr'] & 0x00FF, (conn['doorAsmPtr'] & 0xFF00) >> 8)
                asmPatch += [ 0x20, D0, D1 ]        # JSR $doorAsmPtr
            # incompatible transition
            if 'SamusX' in conn:
                # endian convert
                (X0, X1) = (conn['SamusX'] & 0x00FF, (conn['SamusX'] & 0xFF00) >> 8)
                (Y0, Y1) = (conn['SamusY'] & 0x00FF, (conn['SamusY'] & 0xFF00) >> 8)
                # force samus position
                # see area_rando_door_transition.asm. assemble it to print routines SNES addresses.
                asmPatch += [ 0x20, 0x00, 0xF6 ]    # JSR incompatible_doors
                asmPatch += [ 0xA9, X0,   X1   ]    # LDA #$SamusX        ; fixed Samus X position
                asmPatch += [ 0x8D, 0xF6, 0x0A ]    # STA $0AF6           ; update Samus X position in memory
                asmPatch += [ 0xA9, Y0,   Y1   ]    # LDA #$SamusY        ; fixed Samus Y position
                asmPatch += [ 0x8D, 0xFA, 0x0A ]    # STA $0AFA           ; update Samus Y position in memory
            else:
                # still give I-frames
                asmPatch += [ 0x20, 0x40, 0xF6 ]    # JSR giveiframes
            # return
            asmPatch += [ 0x60 ]   # RTS
            self.romFile.write(struct.pack('B', asmAddress & 0x00FF))
            self.romFile.write(struct.pack('B', (asmAddress & 0xFF00) >> 8))

            self.romFile.seek(asmAddress)
            for byte in asmPatch:
                self.romFile.write(struct.pack('B', byte))

            asmAddress += len(asmPatch)
            # update room state header with song changes
            if 'song' in conn:
                for addr in conn["songs"]:
                    self.romFile.seek(0x70000 + addr)
                    self.romFile.write(struct.pack('B', conn['song']))
                    self.romFile.write(struct.pack('B', 0x5))

    # change BG table to avoid scrolling sky bug when transitioning to west ocean
    def patchWestOcean(self, doorPtr):
        # endian convert
        self.romFile.seek(0x7B7BB)
        self.writeWord(doorPtr)

    # forces CRE graphics refresh when exiting kraid's room in boss rando
    def patchKraidExit(self, roomPtr):
        # Room ptr in bank 8F + CRE flag offset
        offset = 0x70000 + roomPtr + 0x8
        self.romFile.seek(offset)
        self.romFile.write(struct.pack('B', 0x2))

    def writeEscapeTimer(self, escapeTimer):
        minute = int(escapeTimer / 60)
        second = escapeTimer % 60
        minute = int(minute / 10) * 16 + minute % 10
        second = int(second / 10) * 16 + second % 10
        self.romFile.seek(0x1E21)
        self.romFile.write(struct.pack('B', second))
        self.romFile.write(struct.pack('B', minute))

    buttons = {
        "Select" : [0x00, 0x20],
        "A"      : [0x80, 0x00],
        "B"      : [0x00, 0x80],
        "X"      : [0x40, 0x00],
        "Y"      : [0x00, 0x40],
        "L"      : [0x20, 0x00],
        "R"      : [0x10, 0x00],
        "None"   : [0x00, 0x00]
    }

    controls = {
        "Shot"       : [0xb331, 0x1722d],
        "Jump"       : [0xb325, 0x17233],
        "Dash"       : [0xb32b, 0x17239],
        "ItemSelect" : [0xb33d, 0x17245],
        "ItemCancel" : [0xb337, 0x1723f],
        "AngleUp"    : [0xb343, 0x1724b],
        "AngleDown"  : [0xb349, 0x17251]
    }

    # write custom contols to ROM.
    # controlsDict : possible keys are "Shot", "Jump", "Dash", "ItemSelect", "ItemCancel", "AngleUp", "AngleDown"
    #                possible values are "A", "B", "X", "Y", "L", "R", "Select", "None"
    def writeControls(self, controlsDict):
        for ctrl, button in controlsDict.items():
            if ctrl not in RomPatcher.controls:
                raise ValueError("Invalid control name : " + str(ctrl))
            if button not in RomPatcher.buttons:
                raise ValueError("Invalid button name : " + str(button))
            for addr in RomPatcher.controls[ctrl]:
                self.romFile.seek(addr)
                self.romFile.write(struct.pack('B', RomPatcher.buttons[button][0]))
                self.romFile.write(struct.pack('B', RomPatcher.buttons[button][1]))

    def writePlandoAddresses(self, locations):
        self.romFile.seek(0x2F6000)
        for loc in locations:
            self.writeWord(loc['Address'] & 0xFFFF)

        # fill remaining addresses with 0xFFFF
        maxLocsNumber = 128
        for i in range(0, maxLocsNumber-len(locations)):
            self.writeWord(0xFFFF)

    def writePlandoTransitions(self, transitions, doorsPtrs, maxTransitions):
        self.romFile.seek(0x2F6100)

        for (src, dest) in transitions:
            self.writeWord(doorsPtrs[src])
            self.writeWord(doorsPtrs[dest])

        # fill remaining addresses with 0xFFFF
        for i in range(0, maxTransitions-len(transitions)):
            self.writeWord(0xFFFF)
            self.writeWord(0xFFFF)

    def enableMoonWalk(self):
        self.romFile.seek(0xB35D)
        # replace STZ with STA since A is non-zero at this point
        self.romFile.write(struct.pack('B', 0x8D))

    def compress(self, address, data):
        # data: [] of 256 int
        # address: the address where the compressed bytes will be written
        # return the size of the compressed data
        compressedData = Compressor().compress(data)

        self.romFile.seek(address)
        for byte in compressedData:
            self.romFile.write(struct.pack('B', byte))

        return len(compressedData)

class FakeROM:
    # to have the same code for real ROM and the webservice
    def __init__(self, data={}):
        self.curAddress = 0
        self.data = data

    def seek(self, address):
        self.curAddress = address

    def write(self, byte):
        self.data[self.curAddress] = struct.unpack("B", byte)[0]
        self.curAddress += 1

    def read(self, byteCount):
        # in our case byteCount is always equals to 1
        ret = struct.pack("B", self.data[self.curAddress])
        self.curAddress += 1
        return ret

    def close(self):
        pass

def isString(string):
    # unicode only exists in python2
    if sys.version[0] == '2':
        return type(string) == str or type(string) == unicode
    else:
        return type(string) == str

class RomLoader(object):
    @staticmethod
    def factory(rom, magic=None):
        # can be a real rom. can be a json or a dict with the ROM address/values
        if isString(rom):
            ext = os.path.splitext(rom)
            if ext[1].lower() == '.sfc' or ext[1].lower() == '.smc':
                return RomLoaderSfc(rom, magic)
            elif ext[1].lower() == '.json':
                return RomLoaderJson(rom, magic)
            else:
                raise Exception("wrong rom file type: {}".format(ext[1]))
        elif type(rom) is dict:
            return RomLoaderDict(rom, magic)

    def assignItems(self, locations):
        return self.romReader.loadItems(locations)

    def getTransitions(self):
        return self.romReader.loadTransitions()

    def hasPatch(self, patchName):
        return self.romReader.patchPresent(patchName)

    def loadPatches(self):
        RomPatches.ActivePatches = []
        isArea = False
        isBoss = False

        # check total base (blue bt and red tower blue door)
        if self.hasPatch("startCeres") or self.hasPatch("startLS"):
            RomPatches.ActivePatches += [RomPatches.BlueBrinstarBlueDoor,
                                         RomPatches.RedTowerBlueDoors]

        # check total soft lock protection
        if self.hasPatch("layout"):
            RomPatches.ActivePatches += RomPatches.TotalLayout

        # check total casual (blue brinstar missile swap)
        if self.hasPatch("casual"):
            RomPatches.ActivePatches.append(RomPatches.BlueBrinstarMissile)

        # check gravity heat protection
        if self.hasPatch("gravityNoHeatProtection"):
            RomPatches.ActivePatches.append(RomPatches.NoGravityEnvProtection)

        if self.hasPatch("progressiveSuits"):
            RomPatches.ActivePatches.append(RomPatches.ProgressiveSuits)
        if self.hasPatch("nerfedCharge"):
            RomPatches.ActivePatches.append(RomPatches.NerfedCharge)

        # check varia tweaks
        if self.hasPatch("variaTweaks"):
            RomPatches.ActivePatches += RomPatches.VariaTweaks

        # check area
        if self.hasPatch("area"):
            RomPatches.ActivePatches += [RomPatches.SingleChamberNoCrumble,
                                         RomPatches.AreaRandoGatesBase,
                                         RomPatches.AreaRandoBlueDoors]
            isArea = True

        # check area layout
        if self.hasPatch("areaLayout"):
            RomPatches.ActivePatches.append(RomPatches.AreaRandoGatesOther)


        # check boss rando
        isBoss = self.isBoss()

        return (isArea, isBoss)

    def getPatches(self):
        return self.romReader.getPatches()

    def getRawPatches(self):
        # used in interactive solver
        return self.romReader.getRawPatches()

    def getAllPatches(self):
        # used in cli
        return self.romReader.getAllPatches()

    def getPlandoAddresses(self):
        return self.romReader.getPlandoAddresses()

    def getPlandoTransitions(self, maxTransitions):
        return self.romReader.getPlandoTransitions(maxTransitions)

    def decompress(self, address):
        return self.romReader.decompress(address)

    def getROM(self):
        return self.romReader.romFile

    def isBoss(self):
        from graph_access import getAccessPoint
        romFile = self.getROM()
        phOut = getAccessPoint('PhantoonRoomOut')
        doorPtr = phOut.ExitInfo['DoorPtr']
        romFile.seek((0x10000 | doorPtr) + 10)
        asmPtr = readWord(romFile)
        return asmPtr != 0 # this is at 0 in vanilla

class RomLoaderSfc(RomLoader):
    # standard usage (when calling from the command line)
    def __init__(self, romFileName, magic=None):
        super(RomLoaderSfc, self).__init__()
        romFile = open(romFileName, "rb")
        self.romReader = RomReader(romFile, magic)

class RomLoaderDict(RomLoader):
    # when called from the website (the js in the browser uploads a dict of address: value)
    def __init__(self, dictROM, magic=None):
        super(RomLoaderDict, self).__init__()
        self.dictROM = dictROM
        fakeROM = FakeROM(self.dictROM)
        self.romReader = RomReader(fakeROM, magic)

class RomLoaderJson(RomLoaderDict):
    # when called from the test suite and the website (when loading already uploaded roms converted to json)
    def __init__(self, jsonFileName, magic=None):
        with open(jsonFileName) as jsonFile:
            tmpDictROM = json.load(jsonFile)
            dictROM = {}
            # in json keys are strings
            for address in tmpDictROM:
                dictROM[int(address)] = tmpDictROM[address]
            super(RomLoaderJson, self).__init__(dictROM, magic)
