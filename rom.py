
import re, struct, sys, random, os, json, copy
from smbool import SMBool
from itemrandomizerweb import Items
from itemrandomizerweb.patches import patches
from itemrandomizerweb import Items
from itemrandomizerweb.stdlib import List

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
    SingleChamberNoCrumble    = 101,
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

    #### Patch sets
    # total randomizer
    Total_Base = [ BlueBrinstarBlueDoor, RedTowerBlueDoors, NoGravityEnvProtection ]
    # tournament and full
    Total = Total_Base + [ MoatShotBlock, EarlySupersShotBlock,
                           SpazerShotBlock, RedTowerLeftPassage,
                           HiJumpShotBlock, CathedralEntranceWallJump ]
    # casual
    Total_CX = [ BlueBrinstarMissile ] + Total

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


class RomType:
    # guesses ROM type string based on filename and return it
    # if no ROM type could be guessed, returns None
    @staticmethod
    def guess(fileName):
        fileName = os.path.basename(fileName)

        # VARIA ?
        m = re.match(r'^.*VARIA_Randomizer_([A]?[F]?X)\d+.*$', fileName)
        if m is not None:
            return 'VARIA_' + m.group(1)

        # total ?
        m = re.match(r'^.*?([CTFH]?X)\d+.*$', fileName)
        if m is not None:
            return 'Total_' + m.group(1)

        # dessy ?
        m = re.match(r'^.*[CMS]\d+.*$', fileName)
        if m is not None:
            return 'Dessy'

        # vanilla ?
        m = re.match(r'^.*Super[ _]*Metroid.*$', fileName)
        if m is not None:
            return 'Vanilla'

        return None

    # "applies" ROM patches, return if full randomization and area randomization
    @staticmethod
    def apply(romType, patches):
        if romType.startswith('Total_'):
            RomPatches.ActivePatches = RomPatches.Total_Base
        if romType == 'Total_CX':
            RomPatches.ActivePatches = RomPatches.Total_CX
        elif romType in ['Total_TX', 'Total_FX']:
            RomPatches.ActivePatches = RomPatches.Total
        elif romType.startswith('VARIA_'):
            if patches['layoutPresent'] == True:
                RomPatches.ActivePatches = RomPatches.Total
            else:
                print("RomType::apply: no layout patches")
                RomPatches.ActivePatches = RomPatches.Total_Base
            if patches['gravityNoHeatProtectionPresent'] == False:
                print("RomType::apply: Gravity heat protection")
                if RomPatches.NoGravityEnvProtection in RomPatches.ActivePatches:
                    RomPatches.ActivePatches.remove(RomPatches.NoGravityEnvProtection)
            if patches['variaTweaks'] == True:
                RomPatches.ActivePatches += RomPatches.VariaTweaks
            if romType.startswith('VARIA_A'):
                RomPatches.ActivePatches += RomPatches.AreaSet
                if patches['areaLayout'] == False:
                    RomPatches.ActivePatches -= RomPatches.AreaRandoGatesOther
        elif romType == 'Dessy':
            RomPatches.ActivePatches = RomPatches.Dessy

        return ((romType == 'Total_FX' or romType == 'Dessy' or romType == 'VARIA_FX' or romType == 'VARIA_AFX'),
                (romType == 'VARIA_AX' or romType == 'VARIA_AFX'))

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
        'layoutPresent': {'address': 0x21BD80, 'value': 0xD5},
        'gravityNoHeatProtectionPresent': {'address': 0x06e37d, 'value': 0x01},        
        'variaTweaks': {'address': 0x7CC4D, 'value': 0x37},
        'areaLayout': {'address':0x252FA7, 'value':0xF8}
    }

    def getItem(self, romFile, address, visibility):
        # return the hex code of the object at the given address

        romFile.seek(address)
        # value is in two bytes
        value1 = struct.unpack("B", romFile.read(1))
        value2 = struct.unpack("B", romFile.read(1))

        # match itemVisibility with
        # | Visible -> 0
        # | Chozo -> 0x54 (84)
        # | Hidden -> 0xA8 (168)
        if visibility == 'Visible':
            itemCode = hex(value2[0]*256+(value1[0]-0))
        elif visibility == 'Chozo':
            itemCode = hex(value2[0]*256+(value1[0]-84))
        elif visibility == 'Hidden':
            itemCode = hex(value2[0]*256+(value1[0]-168))
        else:
            raise Exception("RomReader: unknown visibility: {}".format(visibility))

        # dessyreqt randomizer make some missiles non existant, detect it
        # 0x1a is to say that the item is a morphball
        # 0xeedb is missile item
        # 0x786de is Morphing Ball location
        romFile.seek(address+4)
        value3 = struct.unpack("B", romFile.read(1))
        if (value3[0] == int('0x1a', 16)
            and int(itemCode, 16) == int('0xeedb', 16)
            and address != int('0x786DE', 16)):
            return hex(0)
        else:
            return itemCode

    def loadItems(self, romFile, locations):
        for loc in locations:
            item = self.getItem(romFile, loc["Address"], loc["Visibility"])
            loc["itemName"] = self.items[item]["name"]
            #print("name: {} class: {} address: {} visibility: {} item: {}".format(loc["Name"], loc["Class"], loc['Address'], loc['Visibility'], item))

    def loadTransitions(self, romFile):
        # return the transitions or None if vanilla transitions
        from graph_access import accessPoints

        rooms = {
            # (roomPtr, screen): name
            (0x9969, (0x0, 0x0)): 'Lower Mushrooms Left',
            (0x95ff, (0x1, 0x0)): 'Moat Right',
            (0x948c, (0x1, 0x2)): 'Keyhunter Room Bottom',
            (0x9e9f, (0x0, 0x2)): 'Morph Ball Room Left',
            (0x9938, (0x0, 0x0)): 'Green Brinstar Elevator Right',
            (0x9e52, (0x1, 0x0)): 'Green Hill Zone Top Right',
            (0x9fba, (0x5, 0x0)): 'Noob Bridge Right',
            (0x93fe, (0x0, 0x4)): 'West Ocean Left',
            (0x957d, (0x0, 0x1)): 'Crab Maze Left',
            (0xaf14, (0x3, 0x0)): 'Lava Dive Right',
            (0xb656, (0x1, 0x0)): 'Three Muskateers Room Left',
            (0xa6a1, (0x0, 0x0)): 'Warehouse Entrance Left',
            (0xad5e, (0x5, 0x0)): 'Single Chamber Top Right',
            (0xae74, (0x1, 0x2)): 'Kronic Boost Room Bottom Left',
            (0xcfc9, (0x1, 0x7)): 'Main Street Bottom',
            (0xd21c, (0x0, 0x1)): 'Crab Hole Bottom Left',
            (0x95a8, (0x0, 0x0)): 'Le Coude Right',
            (0xd104, (0x0, 0x0)): 'Red Fish Room Left',
            (0xa253, (0x0, 0x4)): 'Red Tower Top Left',
            (0xa322, (0x2, 0x3)): 'Caterpillar Room Top Right',
            (0x962a, (0x0, 0x0)): 'Red Brinstar Elevator',
            (0xcf80, (0x0, 0x1)): 'East Tunnel Right',
            (0xcf80, (0x3, 0x0)): 'East Tunnel Top Right',
            (0xcefb, (0x0, 0x0)): 'Glass Tunnel Top',
            (0x99bd, (0x0, 0x6)): 'Green Pirates Shaft Bottom Right',
            (0xa5ed, (0x0, 0x0)): 'Statues Hallway Left'
        }

        transitions = {}
        for accessPoint in accessPoints:
            if accessPoint.Name == 'Landing Site' or accessPoint.Internal == True:
                continue
            (destRoomPtr, destEntryScreen) = self.getTransition(romFile, accessPoint.ExitInfo['DoorPtr'])
            destAPName = rooms[(destRoomPtr, destEntryScreen)]
            transitions[accessPoint.Name] = destAPName


        # remove bidirectionnal transitions
        # can't del keys in a dict while iterating it
        transitionsCopy = copy.copy(transitions)
        for src in transitionsCopy:
            if src in transitions:
                dest = transitions[src]
                if dest in transitions:
                    if transitions[dest] == src:
                        del transitions[dest]

        transitions = [(t, transitions[t]) for t in transitions]

        # check if transitions are vanilla transitions
        from graph_access import isVanillaTransitions
        if isVanillaTransitions(transitions):
            return None
        else:
            return transitions

    def getTransition(self, romFile, doorPtr):
        romFile.seek(0x10000 | doorPtr)

        # room ptr is in two bytes
        v1 = struct.unpack("B", romFile.read(1))
        v2 = struct.unpack("B", romFile.read(1))

        romFile.seek((0x10000 | doorPtr) + 6)
        sx = struct.unpack("B", romFile.read(1))
        sy = struct.unpack("B", romFile.read(1))

        return (v1[0] | (v2[0] << 8), (sx[0], sy[0]))

    def patchPresent(self, romFile, patchName):
        romFile.seek(self.patches[patchName]['address'])
        value = struct.unpack("B", romFile.read(1))
        return value[0] == self.patches[patchName]['value']
    
class RomPatcher:
    # standard:
    # Intro/Ceres Skip and initial door flag setup
    #   introskip_doorflags.ips
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
        'Standard': ['credits_varia.ips', 'g4_skip.ips',
                     'seed_display.ips', 'tracking.ips', 'wake_zebes.ips',
                     'Mother_Brain_Cutscene_Edits',
                     'Suit_acquisition_animation_skip', 'Fix_Morph_and_Missiles_Room_State',
                     'Fix_heat_damage_speed_echoes_bug', 'Disable_GT_Code',
                     'Disable_Space_Time_select_in_menu', 'Fix_Morph_Ball_Hidden_Chozo_PLMs',
                     'Fix_Screw_Attack_selection_in_menu',
                     'Removes_Gravity_Suit_heat_protection',
                     'AimAnyButton.ips', 'ws_etank.ips', 'ln_chozo_sj_check_disable.ips', 'endingtotals.ips'],
        'Layout': ['dachora.ips', 'early_super_bridge.ips', 'high_jump.ips', 'moat.ips',
                   'nova_boost_platform.ips', 'red_tower.ips', 'spazer.ips'],
        'Optional': ['itemsounds.ips', 'max_ammo_display.ips',
                     'spinjumprestart.ips', 'supermetroid_msu1.ips', 'elevators_doors_speed.ips',
                     'skip_intro.ips', 'skip_ceres.ips', 'animal_enemies.ips', 'animals.ips',
                     'draygonimals.ips', 'escapimals.ips', 'gameend.ips', 'grey_door_animals.ips',
                     'low_timer.ips', 'metalimals.ips', 'phantoonimals.ips', 'ridleyimals.ips'],
        'Area': ['area_rando_blue_doors.ips', 'area_rando_layout.ips', 'area_rando_door_transition.ips' ]
    }

    def __init__(self, romFileName=None):
        self.romFileName = romFileName
        if romFileName == None:
            self.romFile = FakeROM()
        else:
            self.romFile = open(romFileName, 'r+')

    def end(self):
        self.romFile.close()

    def writeItemsLocs(self, itemLocs):
        nItems = 0
        for itemLoc in itemLocs:
            if itemLoc['Item']['Type'] in ['Nothing', 'NoEnergy']:
                # put missile morphball like dessy
                itemCode = Items.getItemTypeCode({'Code': 0xeedb}, itemLoc['Location']['Visibility'])
                self.romFile.seek(itemLoc['Location']['Address'])
                self.romFile.write(itemCode[0])
                self.romFile.write(itemCode[1])
                self.romFile.seek(itemLoc['Location']['Address'] + 4)
                self.romFile.write(struct.pack('B', 0x1a))
            else:
                nItems += 1
                itemCode = Items.getItemTypeCode(itemLoc['Item'],
                                                 itemLoc['Location']['Visibility'])
                self.romFile.seek(itemLoc['Location']['Address'])
                self.romFile.write(itemCode[0])
                self.romFile.write(itemCode[1])
            if itemLoc['Location']['Name'] == 'Morphing Ball':
                self.patchMorphBallEye(itemLoc['Item'])
        # write total number of actual items for item percentage patch
        self.romFile.seek(0x5E63B)
        self.romFile.write(struct.pack('B', nItems))

    # trigger morph eye enemy on whatever item we put there,
    # not just morph ball
    def patchMorphBallEye(self, item):
#        print('Eye item = ' + item['Type'])
        # category to check
        if Items.isBeam(item):
            cat = 0xA8 # collected beams
        elif item['Type'] == 'ETank':
            cat = 0xC4 # max health
        elif item['Type'] == 'Reserve':
            cat = 0xD4 # max reserves
        elif item['Type'] == 'Missile':
            cat = 0xC8 # max missiles
        elif item['Type'] == 'Super':
            cat = 0xCC # max supers
        elif item['Type'] == 'PowerBomb':
            cat = 0xD0 # max PBs
        else:
            cat = 0xA4 # collected items
        # comparison/branch instruction
        # the branch is taken if we did NOT collect item yet
        if item['Category'] == 'Energy' or item['Category'] == 'Ammo':
            comp = 0xC9 # CMP (immediate)
            branch = 0x30 # BMI
        else:
            comp = 0x89 # BIT (immediate)
            branch = 0xF0 # BEQ
        # what to compare to
        if item['Type'] == 'ETank':
            operand = 0x65 # < 100
        elif item['Type'] == 'Reserve' or item['Category'] == 'Ammo':
            operand = 0x1 # < 1
        elif Items.isBeam(item):
            operand = Items.BeamBits[item['Type']]
        else:
            operand = Items.ItemBits[item['Type']]
        # endianness
        op0 = operand & 0x00FF
        op1 = (operand & 0xFF00) >> 8
        # actually patch enemy AI
        self.romFile.seek(0x1410E6)
        self.romFile.write(struct.pack('B', cat))
        self.romFile.seek(0x1410E8)
        self.romFile.write(struct.pack('B', comp))
        self.romFile.write(struct.pack('B', op0))
        self.romFile.write(struct.pack('B', op1))
        self.romFile.write(struct.pack('B', branch))

    def writeWord(self, w):
        (w0, w1) = (w & 0x00FF, (w & 0xFF00) >> 8)
        self.romFile.write(struct.pack('B', w0))
        self.romFile.write(struct.pack('B', w1))

    def patchBT(self):
        # write door ASM ptrs from bomb_torizo.asm for BT room entry and exit doors
        self.romFile.seek(0x18bc2 + 10) # entry door
        self.writeWord(0xe9a0)
        self.romFile.seek(0x18baa + 10) # exit door
        self.writeWord(0xe9a7)

    def applyIPSPatches(self, optionalPatches=[], noLayout=False, noGravHeat=False, area=False, areaLayoutBase=False):
        try:
            # apply standard patches
            stdPatches = RomPatcher.IPSPatches['Standard']
            if noGravHeat == True:
                stdPatches = [patch for patch in stdPatches if patch != 'Removes_Gravity_Suit_heat_protection']
            for patchName in stdPatches:
                self.applyIPSPatch(patchName)

            if noLayout == False:
                # apply layout patches
                for patchName in RomPatcher.IPSPatches['Layout']:
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
                for patchName in RomPatcher.IPSPatches['Area']:
                    self.applyIPSPatch(patchName)
        except Exception as e:
            print("Error patching {}. ({})".format(self.romFileName, e))
            sys.exit(-1)

    def applyIPSPatch(self, patchName):
        print("Apply patch {}".format(patchName))
        patchData = patches[patchName]
        for address in patchData:
            self.romFile.seek(address)
            for byte in patchData[address]:
                self.romFile.write(struct.pack('B', byte))

    def writeSeed(self, seed):
        random.seed(seed)

        seedInfo = random.randint(0, 0xFFFF)
        seedInfo2 = random.randint(0, 0xFFFF)
        seedInfoArr = Items.toByteArray(seedInfo)
        seedInfoArr2 = Items.toByteArray(seedInfo2)

        self.romFile.seek(0x2FFF00)
        self.romFile.write(seedInfoArr[0])
        self.romFile.write(seedInfoArr[1])
        self.romFile.write(seedInfoArr2[0])
        self.romFile.write(seedInfoArr2[1])

    def writeRandoSettings(self, settings):
        address = 0x2736C0
        value = "%.1f" % settings.qty['missile']
        line = " MISSILE PROBABILITY        %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " missile probability ...... %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        value = "%.1f" % settings.qty['super']
        line = " SUPER PROBABILITY          %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " super probability ........ %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        value = "%.1f" % settings.qty['powerBomb']
        line = " POWER BOMB PROBABILITY     %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " power bomb probability ... %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        value = "%03d%s" % (settings.qty['minors'], '%')
        line = " MINORS QUANTITY           %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " minors quantity ......... %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        value = " "+settings.qty['energy'].upper()
        line = " ENERGY QUANTITY ......%s " % value.rjust(8, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        value = " "+settings.progSpeed.upper()
        line = " PROGRESSION SPEED ....%s " % value.rjust(8, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        line = " PROGRESSION DIFFICULTY  %s " % settings.progDiff.upper()
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        for param in [(' SPREAD PROG ITEMS ........%s', 'SpreadItems'),
                      (' SUITS RESTRICTION ........%s', 'Suits'),
                      (' EARLY MORPH ..............%s', 'SpeedScrew')]:
            line = param[0] % ('. ON' if settings.restrictions[param[1]] == True else ' OFF')
            self.writeCreditsString(address, 0x04, line)
            address += 0x40

        for superFun in [(' SUPER FUN COMBAT .........%s', 'Combat'),
                         (' SUPER FUN MOVEMENT .......%s', 'Movement'),
                         (' SUPER FUN SUITS ..........%s', 'Suits')]:
            line = superFun[0] % ('. ON' if superFun[1] in settings.superFun else ' OFF')
            self.writeCreditsString(address, 0x04, line)
            address += 0x40

    def writeSpoiler(self, itemLocs):
        # keep only majors, filter out Etanks and Reserve
        fItemLocs = List.sortBy(lambda il: il['Item']['Type'],
                                List.filter(lambda il: (il['Item']['Class'] == 'Major'
                                                        and il['Item']['Type'] not in ['ETank', 'Reserve',
                                                                                       'NoEnergy', 'Nothing']),
                                            itemLocs))

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

        address = 0x2f5240
        for item in ["Charge Beam", "Ice Beam", "Wave Beam", "Spazer", "Plasma Beam", "Varia Suit",
                     "Gravity Suit", "Morph Ball", "Bomb", "Spring Ball", "Screw Attack",
                     "Hi-Jump Boots", "Space Jump", "Speed Booster", "Grappling Beam", "X-Ray Scope"]:
            # super fun removes items
            if item not in itemLocs:
                continue
            itemName = prepareString(item)
            locationName = prepareString(itemLocs[item], isItem=False)

            self.writeCreditsString(address, 0x04, itemName)
            self.writeCreditsString((address + 0x40), 0x18, locationName)

            address += 0x80

        # we need 16 majors displayed, if we've removed majors, add some blank text
        for i in range(16 - len(fItemLocs)):
            self.writeCreditsString(address, 0x04, prepareString(""))
            self.writeCreditsString((address + 0x40), 0x18, prepareString(""))

            address += 0x80

        self.patchBytes(address, [0, 0, 0, 0])

    def writeCreditsString(self, address, color, string):
        array = [self.convertCreditsChar(color, char) for char in string]
        self.patchBytes(address, array)

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

    def patchBytes(self, address, array):
        self.romFile.seek(address)
        for dByte in array:
            dByteArr = Items.toByteArray(dByte)
            self.romFile.write(dByteArr[0])
            self.romFile.write(dByteArr[1])

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
        self.asmAddress = 0x7EB00

        for conn in doorConnections:
#            print('Writing door connection ' + conn['ID'])
            roomPtr = conn['RoomPtr']
            if roomPtr == 0x93fe: # west ocean
                self.patchWestOcean(conn['DoorPtr'])
            self.romFile.seek(0x10000+conn['DoorPtr'])

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
                asmPatch += [ 0x20, 0x00, 0xEA ]    # JSR cancel_movement ; see area_rando_door_transition.asm
                asmPatch += [ 0xA9, X0,   X1   ]    # LDA #$SamusX        ; fixed Samus X position
                asmPatch += [ 0x8D, 0xF6, 0x0A ]    # STA $0AF6           ; update Samus X position in memory
                asmPatch += [ 0xA9, Y0,   Y1   ]    # LDA #$SamusY        ; fixed Samus Y position
                asmPatch += [ 0x8D, 0xFA, 0x0A ]    # STA $0AFA           ; update Samus Y position in memory
            else:
                # still give I-frames
                asmPatch += [ 0x20, 0x36, 0xEA ]    # JSR .end_cancel     ; see area_rando_door_transition.asm
            # change song if needed
            if 'song' in conn:
                asmPatch += [ 0xA9, conn['song'], 0xFF ]       # LDA #$song       ; A is argument for change_song
                asmPatch += [ 0x20, 0x3D,         0XEA ]       # JSR change_song  ; see area_rando_door_transition.asm
            # return
            asmPatch += [ 0x60 ]   # RTS
            self.romFile.write(struct.pack('B', self.asmAddress & 0x00FF))
            self.romFile.write(struct.pack('B', (self.asmAddress & 0xFF00) >> 8))

            self.romFile.seek(self.asmAddress)
            for byte in asmPatch:
                self.romFile.write(struct.pack('B', byte))

            self.asmAddress += 0x20
        self.writeTourianRefill()

    # change BG table to avoid scrolling sky bug when transitioning to west ocean
    def patchWestOcean(self, doorPtr):
        # endian convert
        self.romFile.seek(0x7B7BB)
        self.writeWord(doorPtr)

    # add ASM to Tourian "door" down elevator to trigger full refill (ammo + energy)
    def writeTourianRefill(self):
        tourianDoor = 0x19222
        self.romFile.seek(tourianDoor + 10) # go to door ASM ptr field
        # $0F:EA52 is full_refill routine address. see area_rando_door_transition.asm
        self.romFile.write(struct.pack('B', 0x52))
        self.romFile.write(struct.pack('B', 0xEA))

    def writeTransitionsCredits(self, transitions):
        address = 0x273B40
        lineLength = 32

        for (src, dest) in transitions:
            # line is 32 chars long, need a space between the two access points
            length = len(src) + len(dest) + len(" ")
            if length > lineLength:
                self.writeCreditsString(address, 0x04, src)
                address += 0x40

                dest = " "+dest
                self.writeCreditsString(address, 0x04, dest.rjust(lineLength))
                address += 0x40
            else:
                self.writeCreditsString(address, 0x04, src+" "*(lineLength-(len(src)+len(dest)))+dest)
                address += 0x40

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
        for ctrl, button in controlsDict.iteritems():
            if ctrl not in RomPatcher.controls:
                raise ValueError("Invalid control name : " + str(ctrl))
            if button not in RomPatcher.buttons:
                raise ValueError("Invalid button name : " + str(button))
            for addr in RomPatcher.controls[ctrl]:
                self.romFile.seek(addr)
                self.romFile.write(struct.pack('B', RomPatcher.buttons[button][0]))
                self.romFile.write(struct.pack('B', RomPatcher.buttons[button][1]))

class FakeROM:
    # to have the same code for real rom and the webservice
    def __init__(self, data={}):
        self.curAddress = 0
        self.data = data

    def seek(self, address):
        self.curAddress = address

    def write(self, byte):
        self.data[self.curAddress] = struct.unpack("B", byte)
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
    def factory(rom):
        # can be a real rom. can be a json or a dict with the locations - items association
        if isString(rom):
            ext = os.path.splitext(rom)
            if ext[1].lower() == '.sfc' or ext[1].lower() == '.smc':
                return RomLoaderSfc(rom)
            elif ext[1].lower() == '.json':
                return RomLoaderJson(rom)
            else:
                print("wrong rom file type: {}".format(ext[1]))
                sys.exit(-1)
        elif type(rom) is dict:
            return RomLoaderDict(rom)

    def __init__(self):
        self.patches = {
            # total rando anti-softlock
            'layoutPresent': True,
            'gravityNoHeatProtectionPresent': True,
            # WS etank without killing phantoon + LN torizo no space jump check
            'variaTweaks': False,
            # complementary layout patches for area rando: see RomPatches.AreaRandoGatesOther
            'areaLayout' : False
        }

    def assignItems(self, locations):
        # update the itemName and Class of the locations
        for loc in locations:
            loc['itemName'] = self.locsItems[loc['Name']]

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.locsItems, jsonFile)

    def getTransitions(self):
        if 'transitions' in self.locsItems:
            return self.locsItems['transitions']
        else:
            return None

class RomLoaderSfc(RomLoader):
    # standard usage (when calling from the command line)
    def __init__(self, romFileName):
        print("RomLoaderSfc::init")
        super(RomLoaderSfc, self).__init__()
        self.romFileName = romFileName
        self.romReader = RomReader()

    def assignItems(self, locations):
        # update the itemName of the locations
        with open(self.romFileName, "rb") as romFile:
            self.romReader.loadItems(romFile, locations)
            for patch in self.patches:
                self.patches[patch] = self.romReader.patchPresent(romFile, patch)

            transitions = self.romReader.loadTransitions(romFile)

        self.locsItems = {}
        for loc in locations:
            self.locsItems[loc['Name']] = loc['itemName']
        for patch in self.patches:
            self.locsItems[patch] = self.patches[patch]

        self.locsItems['transitions'] = transitions

class RomLoaderJson(RomLoader):
    # when called from the test suite and the website (when loading already uploaded roms converted to json)
    def __init__(self, jsonFileName):
        print("RomLoaderJson::init")
        super(RomLoaderJson, self).__init__()
        with open(jsonFileName) as jsonFile:
            self.locsItems = json.load(jsonFile)

        for patch in self.patches:
            if patch in self.locsItems:
                self.patches[patch] = self.locsItems[patch]
            self.locsItems[patch] = self.patches[patch]

class RomLoaderDict(RomLoader):
    # when called from the website (the js in the browser uploads a dict of address: value)
    def __init__(self, dictROM):
        print("RomLoaderDict::init")
        super(RomLoaderDict, self).__init__()
        self.dictROM = dictROM
        self.romReader = RomReader()

    def assignItems(self, locations):
        # update the itemName of the locations
        fakeROM = FakeROM(self.dictROM)
        self.romReader.loadItems(fakeROM, locations)
        for patch in self.patches:
            self.patches[patch] = self.romReader.patchPresent(fakeROM, patch)

        transitions = self.romReader.loadTransitions(fakeROM)

        self.locsItems = {}
        for loc in locations:
            self.locsItems[loc['Name']] = loc['itemName']
        for patch in self.patches:
            self.locsItems[patch] = self.patches[patch]

        self.locsItems['transitions'] = transitions
