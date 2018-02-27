
import re, struct, sys, shutil, random
from helpers import SMBool
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
    # total randomizer, all seeds
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
        elif romType.startswith('Total_'):
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

        romFile.seek(address, 0)
        # value is in two bytes
        value1 = struct.unpack("B", romFile.read(1))
        value2 = struct.unpack("B", romFile.read(1))

        # dessyreqt randomizer make some missiles non existant, detect it
        # 0x1a is to say that the item is a morphball
        # 0xeedb is missile item
        # 0x786de is Morphing Ball location
        romFile.seek(address+4, 0)
        value3 = struct.unpack("B", romFile.read(1))
        if (value3[0] == int('0x1a', 16)
            and value2[0]*256+(value1[0]) == int('0xeedb', 16)
            and address != int('0x786DE', 16)):
            return hex(0)

        # match itemVisibility with
        # | Visible -> 0
        # | Chozo -> 0x54 (84)
        # | Hidden -> 0xA8 (168)
        if visibility == 'Visible':
            return hex(value2[0]*256+(value1[0]-0))
        elif visibility == 'Chozo':
            return hex(value2[0]*256+(value1[0]-84))
        elif visibility == 'Hidden':
            return hex(value2[0]*256+(value1[0]-168))
        else:
            # crash !
            manger.du(cul)

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
    IPSPatches = {
        'Standard': ['Fix_Morph_Ball_Hidden_Chozo_PLMs', 'Disable_GT_Code', 'Fix_heat_damage_speed_echoes_bug',
                     'Removes_Gravity_Suit_heat_protection', 'Fix_Screw_Attack_selection_in_menu',
                     'Instantly_open_G4_passage_when_all_bosses_are_killed', 'Seed_display',
                     'Suit_acquisition_animation_skip', 'Custom_credits_with_stats',
                     'Fix_Morph_and_Missiles_Room_State', 'Intro_Ceres_Skip_and_initial_door_flag_setup',
                     'Custom_credits_with_stats__tracking_code', 'Disable_Space_Time_select_in_menu',
                     'Wake_up_zebes_when_going_right_from_morph', 'Mother_Brain_Cutscene_Edits'],
        'Layout': ['Raise_platforms_in_red_tower_bottom_to_always_be_able_to_get_back_up',
                   'Disable respawning blocks at dachora pit',
                   'Raise_platform_in_first_heated_norfair_room_to_not_require_hi_jump',
                   'Make_it_possible_to_escape_from_below_early_super_bridge_without_bombs',
                   'Replace_bomb_blocks_with_shot_blocks_before_Hi_Jump',
                   'Replace_bomb_blocks_with_shot_blocks_at_Moat',
                   'Replace_bomb_blocks_with_shot_blocks_before_Spazer'],
        # TODO::missing optional patches:
        #  -remove fanfare
        #  -map angle down on select
        #  -respin
        #  -naked dying samus
        'Optional': ['Max_Ammo_Display', 'MSU1_audio'],
        'Casual': ['Swap_construction_zone_etank_with_missiles_and_open_up_path_to_missiles'],
        'Tournament': [],
        'Full': []
    }

    @staticmethod
    def patch(romFileName, outFileName, itemLocs):
        try:
            shutil.copyfile(romFileName, outFileName)

            with open(outFileName, 'r+') as outFile:
                for itemLoc in itemLocs:
                    itemCode = Items.getItemTypeCode(itemLoc['Item'],
                                                     itemLoc['Location']['Visibility'])
                    outFile.seek(itemLoc['Location']['Address'], 0)
                    outFile.write(itemCode[0])
                    outFile.seek(itemLoc['Location']['Address'] + 1, 0)
                    outFile.write(itemCode[1])
        except Exception as e:
            print("Error patching {}. Is {} a valid ROM ? ({})".format(outFileName, romFileName, e))
            sys.exit(-1)

    @staticmethod
    def applyIPSPatches(romFileName, difficulty='Tournament', optionalPatches=[]):
        try:
            with open(romFileName, 'r+') as romFile:
                # apply standard patches
                for patchName in RomPatcher.IPSPatches['Standard']:
                    RomPatcher.applyIPSPatch(romFile, patchName)

                # apply layout patches
                for patchName in RomPatcher.IPSPatches['Layout']:
                    RomPatcher.applyIPSPatch(romFile, patchName)

                # apply difficulty patches
                for patchName in RomPatcher.IPSPatches[difficulty]:
                    RomPatcher.applyIPSPatch(romFile, patchName)

                # apply optional patches
                for patchName in optionalPatches:
                    if patchName in RomPatcher.IPSPatches['Optional']:
                        RomPatcher.applyIPSPatch(romFile, patchName)
        except Exception as e:
            print("Error patching {}. ({})".format(romFileName, e))
            sys.exit(-1)

    @staticmethod
    def applyIPSPatch(romFile, patchName):
        patchData = patches[patchName]
        for address in patchData:
            romFile.seek(address)
            romFile.write(struct.pack('B', patchData[address]))

    @staticmethod
    def writeSeed(romFileName, seed):
        with open(romFileName, 'r+') as romFile:
            random.seed(seed)

            seedInfo = random.randint(0, 0xFFFF)
            seedInfo2 = random.randint(0, 0xFFFF)
            seedInfoArr = Items.toByteArray(seedInfo)
            seedInfoArr2 = Items.toByteArray(seedInfo2)

            romFile.seek(0x2FFF00)
            romFile.write(seedInfoArr[0])
            romFile.seek(0x2FFF01)
            romFile.write(seedInfoArr[1])
            romFile.seek(0x2FFF02)
            romFile.write(seedInfoArr2[0])
            romFile.seek(0x2FFF03)
            romFile.write(seedInfoArr2[1])

    @staticmethod
    def writeSpoiler(romFileName, itemLocs):
        # keep only majors, filter out Etanks and Reserve
        fItemLocs = List.sortBy(lambda il: il['Item']['Type'],
                                List.filter(lambda il: (il['Item']['Class'] == 'Major'
                                                        and il['Item']['Type'] not in ['ETank',
                                                                                       'Reserve']),
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

        with open(romFileName, 'r+') as romFile:
            address = 0x2f5240
            for iL in fItemLocs:
                itemName = prepareString(iL['Item']['Name'])
                locationName = prepareString(iL['Location']['Name'], isItem=False)

                RomPatcher.writeCreditsString(romFile, address, 0x04, itemName)
                RomPatcher.writeCreditsString(romFile, (address + 0x40), 0x18, locationName)

                address += 0x80

            RomPatcher.patchBytes(romFile, address, [0, 0, 0, 0])

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
        for dByte in array:
            dByteArr = Items.toByteArray(dByte)

            romFile.seek(address)
            romFile.write(dByteArr[0])
            address += 1

            romFile.seek(address)
            romFile.write(dByteArr[1])
            address += 1
