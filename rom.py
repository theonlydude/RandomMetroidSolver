
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
    # shot block to exit hu jump area 
    HiJumpShotBlock           = 30
    # access main upper norfair without anything
    CathedralEntranceWallJump = 31

    ### Other
    # lava gives less damage than in vanilla
    ReducedLavaDamage       = 1000
    # Gravity no longer protects from environmental damage (heat, spikes...)
    NoGravityEnvProtection  = 1010
    
    #### Patch sets
    # total randomizer: tournament and full
    Total = [ BlueBrinstarBlueDoor,
              SpazerShotBlock, RedTowerLeftPassage, RedTowerBlueDoors,
              HiJumpShotBlock, CathedralEntranceWallJump,
              ReducedLavaDamage, NoGravityEnvProtection ]

    # total randomizer, casual seeds
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
    def apply(romType):
        if romType == 'Total_CX':
            RomPatches.ActivePatches = RomPatches.Total_CX
        elif romType in ['Total_TX', 'Total_FX']:
            RomPatches.ActivePatches = RomPatches.Total
        elif romType.startswith('VARIA_'):
            RomPatches.ActivePatches = RomPatches.Total
        elif romType == 'Dessy':
            RomPatches.ActivePatches = RomPatches.Dessy
        
        return romType == 'Total_FX' or romType == 'Dessy'
    
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

    def __init__(self, romFileName=None):
        if romFileName is not None:
            self.romFileName = romFileName

    def getItemFromFakeRom(self, fakeRom, address, visibility):
        value1 = fakeRom[address]
        value2 = fakeRom[address+1]
        value3 = fakeRom[address+4]

        if (value3 == int('0x1a', 16)
            and value2*256+value1 == int('0xeedb', 16)
            and address != int('0x786DE', 16)):
            return hex(0)

        if visibility == 'Visible':
            return hex(value2*256+(value1-0))
        elif visibility == 'Chozo':
            return hex(value2*256+(value1-84))
        elif visibility == 'Hidden':
            return hex(value2*256+(value1-168))
        else:
            # crash !
            manger.du(cul)

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
            # crash !
            manger.du(cul)

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

    def loadItemsFromFakeRom(self, fakeRom, locations):
        for loc in locations:
            item = self.getItemFromFakeRom(fakeRom, loc["Address"], loc["Visibility"])
            loc["itemName"] = self.items[item]["name"]

    def loadItems(self, locations):
        with open(self.romFileName, "rb") as romFile:
            for loc in locations:
                item = self.getItem(romFile, loc["Address"], loc["Visibility"])
                loc["itemName"] = self.items[item]["name"]
                #print("{}: {} => {}".format(loc["Name"], loc["Class"], loc["itemName"]))

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
        'Standard': ['credits_varia.ips', 'g4_skip.ips', 'introskip_doorflags.ips',
                     'seed_display.ips', 'tracking.ips', 'wake_zebes.ips',
                     'Removes_Gravity_Suit_heat_protection', 'Mother_Brain_Cutscene_Edits',
                     'Suit_acquisition_animation_skip', 'Fix_Morph_and_Missiles_Room_State',
                     'Fix_heat_damage_speed_echoes_bug', 'Disable_GT_Code',
                     'Disable_Space_Time_select_in_menu', 'Fix_Morph_Ball_Hidden_Chozo_PLMs',
                     'Fix_Screw_Attack_selection_in_menu'],
        'Layout': ['dachora.ips', 'early_super_bridge.ips', 'high_jump.ips', 'moat.ips',
                   'nova_boost_platform.ips', 'red_tower.ips', 'spazer.ips'],
        'Optional': ['AimAnyButton.ips', 'itemsounds.ips', 'max_ammo_display.ips',
                     'spinjumprestart.ips', 'supermetroid_msu1.ips', 'elevators_doors_speed.ips']
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
    def applyIPSPatches(romFileName, optionalPatches=[]):
        try:
            if romFileName is not None:
                romFile = open(romFileName, 'r+')
            else:
                romFile = FakeROM()

            # apply standard patches
            for patchName in RomPatcher.IPSPatches['Standard']:
                RomPatcher.applyIPSPatch(romFile, patchName)

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

        RomPatcher.patchBytes(romFile, address, [0, 0, 0, 0])

        romFile.close()

        if romFileName is None:
            return romFile.data

    @staticmethod
    def writeCreditsString(romFile, address, color, string):
        array = [RomPatcher.convertCreditsChar(color, char) for char in string]
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
    def patchBytes(romFile, address, array):
        romFile.seek(address)
        for dByte in array:
            dByteArr = Items.toByteArray(dByte)
            romFile.write(dByteArr[0])
            romFile.write(dByteArr[1])

class FakeROM:
    # to have the same code for real rom and the webservice
    def __init__(self):
        self.curAddress = 0
        self.data = {}

    def seek(self, address):
        self.curAddress = address

    def write(self, byte):
        self.data[self.curAddress] = struct.unpack("B", byte)
        self.curAddress += 1

    def close(self):
        pass

def isString(string):
    # unicode only exists in python2
    if sys.version[0] == '2':
        return type(string) == str or type(string) == unicode
    else:
        return type(string) == str

class RomLoader:
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

    def assignItems(self, locations):
        # update the itemName and Class of the locations
        for loc in locations:
            loc['itemName'] = self.locsItems[loc['Name']]

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.locsItems, jsonFile)


class RomLoaderSfc(RomLoader):
    # standard usage
    def __init__(self, romFileName):
        self.romFileName = romFileName
        self.romReader = RomReader(romFileName)

    def assignItems(self, locations):
        # update the itemName of the locations
        self.romReader.loadItems(locations)

        self.locsItems = {}
        for loc in locations:
            self.locsItems[loc['Name']] = loc['itemName']

class RomLoaderJson(RomLoader):
    # when called from the test suite
    def __init__(self, jsonFileName):
        with open(jsonFileName) as jsonFile:
            self.locsItems = json.load(jsonFile)

class RomLoaderDict(RomLoader):
    # when called from the website
    def __init__(self, fakeRom):
        self.fakeRom = fakeRom

    def assignItems(self, locations):
        # update the itemName of the locations
        RomReader().loadItemsFromFakeRom(self.fakeRom, locations)

        self.locsItems = {}
        for loc in locations:
            self.locsItems[loc['Name']] = loc['itemName']

