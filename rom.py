
import re, struct, sys, random, os, json
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
    # shot block to exit hu jump area
    HiJumpShotBlock           = 30
    # access main upper norfair without anything
    CathedralEntranceWallJump = 31
    # moat bottom block
    MoatShotBlock             = 41
    # remove crumble block for reverse lower norfair door access
    SingleChamberNoCrumble    = 101,
    # remove green gates for reverse maridia access
    NoMaridiaGreenGates       = 102


    ### Other
    # Gravity no longer protects from environmental damage (heat, spikes...)
    NoGravityEnvProtection  = 1000

    #### Patch sets
    # total randomizer
    Total_Base = [ BlueBrinstarBlueDoor, RedTowerBlueDoors, NoGravityEnvProtection ]
    # tournament and full
    Total = Total_Base + [ MoatShotBlock, EarlySupersShotBlock,
                           SpazerShotBlock, RedTowerLeftPassage,
                           HiJumpShotBlock, CathedralEntranceWallJump ]
    # casual
    Total_CX = [ BlueBrinstarMissile ] + Total

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
        m = re.match(r'^VARIA_Randomizer_([F]?X)\d+.*$', fileName)
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

    # "applies" ROM patches, return true if full randomization, false if not
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
                RomPatches.ActivePatches.remove(RomPatches.NoGravityEnvProtection)
        elif romType == 'Dessy':
            RomPatches.ActivePatches = RomPatches.Dessy

        return romType == 'Total_FX' or romType == 'Dessy' or romType == 'VARIA_FX'

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
        'gravityNoHeatProtectionPresent': {'address': 0x06e37d, 'value': 0x01}
    }

    def __init__(self, romFileName=None, dictROM=None):
        self.romFileName = romFileName
        self.dictROM = dictROM

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
            #print("{}: {} => {}".format(loc["Name"], loc["Class"], loc["itemName"]))

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
                     'Removes_Gravity_Suit_heat_protection'],
        'Layout': ['dachora.ips', 'early_super_bridge.ips', 'high_jump.ips', 'moat.ips',
                   'nova_boost_platform.ips', 'red_tower.ips', 'spazer.ips'],
        'Optional': ['AimAnyButton.ips', 'itemsounds.ips', 'max_ammo_display.ips',
                     'spinjumprestart.ips', 'supermetroid_msu1.ips', 'elevators_doors_speed.ips',
                     'skip_intro.ips', 'skip_ceres.ips', 'animal_enemies.ips', 'animals.ips',
                     'draygonimals.ips', 'escapimals.ips', 'gameend.ips', 'grey_door_animals.ips',
                     'low_timer.ips', 'metalimals.ips', 'phantoonimals.ips', 'ridleyimals.ips']
    }

    @staticmethod
    def writeItemsLocs(outFileName, itemLocs):
        if outFileName is not None:
            outFile = open(outFileName, 'r+')
        else:
            outFile = FakeROM()

        for itemLoc in itemLocs:
            if itemLoc['Item']['Type'] in ['Nothing', 'NoEnergy']:
                # put missile morphball like dessy
                itemCode = Items.getItemTypeCode({'Code': 0xeedb}, itemLoc['Location']['Visibility'])
                outFile.seek(itemLoc['Location']['Address'])
                outFile.write(itemCode[0])
                outFile.write(itemCode[1])
                outFile.seek(itemLoc['Location']['Address'] + 4)
                outFile.write(struct.pack('B', 0x1a))
            else:
                itemCode = Items.getItemTypeCode(itemLoc['Item'],
                                                 itemLoc['Location']['Visibility'])
                outFile.seek(itemLoc['Location']['Address'])
                outFile.write(itemCode[0])
                outFile.write(itemCode[1])

        outFile.close()

        if outFileName is None:
            return outFile.data

    @staticmethod
    def applyIPSPatches(romFileName, optionalPatches=[], noLayout=False, noGravHeat=False):
        try:
            if romFileName is not None:
                romFile = open(romFileName, 'r+')
            else:
                romFile = FakeROM()

            # apply standard patches
            stdPatches = RomPatcher.IPSPatches['Standard']
            if noGravHeat == True:
                stdPatches = [patch for patch in stdPatches if patch != 'Removes_Gravity_Suit_heat_protection']
            for patchName in stdPatches:
                RomPatcher.applyIPSPatch(romFile, patchName)

            if noLayout == False:
                # apply layout patches
                for patchName in RomPatcher.IPSPatches['Layout']:
                    RomPatcher.applyIPSPatch(romFile, patchName)

            # apply optional patches
            for patchName in optionalPatches:
                if patchName in RomPatcher.IPSPatches['Optional']:
                    RomPatcher.applyIPSPatch(romFile, patchName)

            romFile.close()

            if romFileName is None:
                return romFile.data

        except Exception as e:
            print("Error patching {}. ({})".format(romFileName, e))
            sys.exit(-1)

    @staticmethod
    def applyIPSPatch(romFile, patchName):
        print("Apply patch {}".format(patchName))
        patchData = patches[patchName]
        for address in patchData:
            romFile.seek(address)
            for byte in patchData[address]:
                romFile.write(struct.pack('B', byte))

    @staticmethod
    def writeSeed(romFileName, seed):
        if romFileName is not None:
            romFile = open(romFileName, 'r+')
        else:
            romFile = FakeROM()

        random.seed(seed)

        seedInfo = random.randint(0, 0xFFFF)
        seedInfo2 = random.randint(0, 0xFFFF)
        seedInfoArr = Items.toByteArray(seedInfo)
        seedInfoArr2 = Items.toByteArray(seedInfo2)

        romFile.seek(0x2FFF00)
        romFile.write(seedInfoArr[0])
        romFile.write(seedInfoArr[1])
        romFile.write(seedInfoArr2[0])
        romFile.write(seedInfoArr2[1])

        romFile.close()

        if romFileName is None:
            return romFile.data

    @staticmethod
    def writeRandoSettings(romFileName, settings):
        if romFileName is not None:
            romFile = open(romFileName, 'r+')
        else:
            romFile = FakeROM()

        address = 0x2738C0
        value = "%.1f" % settings.qty['missile']
        line = " MISSILE PROBABILITY        %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=True)
        address += 0x40

        line = " missile probability ...... %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=False)
        address += 0x40

        value = "%.1f" % settings.qty['super']
        line = " SUPER PROBABILITY          %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=True)
        address += 0x40

        line = " super probability ........ %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=False)
        address += 0x40

        value = "%.1f" % settings.qty['powerBomb']
        line = " POWER BOMB PROBABILITY     %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=True)
        address += 0x40

        line = " power bomb probability ... %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=False)
        address += 0x40

        value = "%03d%s" % (settings.qty['minors'], '%')
        line = " MINORS QUANTITY           %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=True)
        address += 0x40

        line = " minors quantity ......... %s " % value
        RomPatcher.writeCreditsStringBig(romFile, address, line, top=False)
        address += 0x80

        address = 0x273b00
        line = " ...................... %s " % settings.qty['energy'].upper()
        RomPatcher.writeCreditsString(romFile, address, 0x04, line)
        address += 0x80

        line = " ...................... %s " % settings.progSpeed.upper()
        RomPatcher.writeCreditsString(romFile, address, 0x04, line)
        address += 0x80

        for param in ['SpreadItems', 'Suits', 'SpeedScrew']:
            line = " ..........................%s " % ('. ON' if settings.restrictions[param] == True else ' OFF')
            RomPatcher.writeCreditsString(romFile, address, 0x04, line)
            address += 0x80

        for superFun in ['Combat', 'Movement', 'Suits']:
            line = " ..........................%s " % ('. ON' if superFun in settings.superFun else ' OFF')
            RomPatcher.writeCreditsString(romFile, address, 0x04, line)
            address += 0x80

        romFile.close()

        if romFileName is None:
            return romFile.data

    @staticmethod
    def writeSpoiler(romFileName, itemLocs):
        # keep only majors, filter out Etanks and Reserve
        fItemLocs = List.sortBy(lambda il: il['Item']['Type'],
                                List.filter(lambda il: (il['Item']['Class'] == 'Major'
                                                        and il['Item']['Type'] not in ['ETank', 'Reserve',
                                                                                       'NoEnergy', 'Nothing']),
                                            itemLocs))

        regex = re.compile(r"[^A-Z0-9\.,'!: ]+")

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

        if romFileName is not None:
            romFile = open(romFileName, 'r+')
        else:
            romFile = FakeROM()

        address = 0x2f5240
        for iL in fItemLocs:
            itemName = prepareString(iL['Item']['Name'])
            locationName = prepareString(iL['Location']['Name'], isItem=False)

            RomPatcher.writeCreditsString(romFile, address, 0x04, itemName)
            RomPatcher.writeCreditsString(romFile, (address + 0x40), 0x18, locationName)

            address += 0x80

        # we need 16 majors displayed, if we've removed majors, add some blank text
        for i in range(16 - len(fItemLocs)):
            RomPatcher.writeCreditsString(romFile, address, 0x04, prepareString(""))
            RomPatcher.writeCreditsString(romFile, (address + 0x40), 0x18, prepareString(""))

            address += 0x80

        RomPatcher.patchBytes(romFile, address, [0, 0, 0, 0])

        romFile.close()

        if romFileName is None:
            return romFile.data

    @staticmethod
    def writeCreditsString(romFile, address, color, string):
        array = [RomPatcher.convertCreditsChar(color, char) for char in string]
        RomPatcher.patchBytes(romFile, address, array)

    @staticmethod
    def writeCreditsStringBig(romFile, address, string, top=True):
        array = [RomPatcher.convertCreditsCharBig(char, top) for char in string]
        RomPatcher.patchBytes(romFile, address, array)

    @staticmethod
    def convertCreditsChar(color, byte):
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

    @staticmethod
    def convertCreditsCharBig(byte, top=True):
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

    @staticmethod
    def patchBytes(romFile, address, array):
        romFile.seek(address)
        for dByte in array:
            dByteArr = Items.toByteArray(dByte)
            romFile.write(dByteArr[0])
            romFile.write(dByteArr[1])

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
            'layoutPresent': True,
            'gravityNoHeatProtectionPresent': True
        }

    def assignItems(self, locations):
        # update the itemName and Class of the locations
        for loc in locations:
            loc['itemName'] = self.locsItems[loc['Name']]

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.locsItems, jsonFile)


class RomLoaderSfc(RomLoader):
    # standard usage (when calling from the command line)
    def __init__(self, romFileName):
        print("RomLoaderSfc::init")
        super(RomLoaderSfc, self).__init__()
        self.romFileName = romFileName
        self.romReader = RomReader(romFileName)

    def assignItems(self, locations):
        # update the itemName of the locations
        with open(self.romFileName, "rb") as romFile:
            self.romReader.loadItems(romFile, locations)
            for patch in self.patches:
                self.patches[patch] = self.romReader.patchPresent(romFile, patch)

        self.locsItems = {}
        for loc in locations:
            self.locsItems[loc['Name']] = loc['itemName']
        for patch in self.patches:
            self.locsItems[patch] = self.patches[patch]

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

        self.locsItems = {}
        for loc in locations:
            self.locsItems[loc['Name']] = loc['itemName']
        for patch in self.patches:
            self.locsItems[patch] = self.patches[patch]
