import random
from enum import IntEnum,IntFlag
from logic.smbool import SMBool
from rom.rom_patches import RomPatches
from patches.patchaccess import PatchAccess
from rom.symbols import Symbols
from rom.rom import snes_to_pc
import utils.log, logging

LOG = utils.log.get('DoorsManager')

colorsList = ['red', 'green', 'yellow', 'wave', 'spazer', 'plasma', 'ice']
# 1/15 chance to have the door set to grey
colorsListGrey = colorsList * 2 + ['grey']

class Facing(IntEnum):
    Left = 0
    Right = 1
    Top = 2
    Bottom = 3

# door facing left - right - top   - bottom
plmRed    = [0xc88a, 0xc890, 0xc896, 0xc89c]
plmGreen  = [0xc872, 0xc878, 0xc87e, 0xc884]
plmYellow = [0xc85a, 0xc860, 0xc866, 0xc86c]
plmGrey   = [0xc842, 0xc848, 0xc84e, 0xc854]
plmWave   = [0xf763, 0xf769, 0xf70f, 0xf715]
plmSpazer = [0xf733, 0xf739, 0xf73f, 0xf745]
plmPlasma = [0xf74b, 0xf751, 0xf757, 0xf75d]
plmIce    = [0xf71b, 0xf721, 0xf727, 0xf72d]

plmFacing = {plms[f]: f for plms in [plmRed, plmGreen, plmYellow, plmGrey, plmWave, plmSpazer, plmPlasma, plmIce] for f in Facing}

colors2plm = {
    'red': plmRed,
    'green': plmGreen,
    'yellow': plmYellow,
    'grey': plmGrey,
    'wave': plmWave,
    'spazer': plmSpazer,
    'plasma': plmPlasma,
    'ice': plmIce
}

# door color indicators PLMs (flashing on the other side of colored doors)
indicatorsDirection = {
    Facing.Left: Facing.Right,
    Facing.Right: Facing.Left,
    Facing.Top: Facing.Bottom,
    Facing.Bottom: Facing.Top
}

# door facing        left -   right - top   - bottom
plmRedIndicator    = [0xFBB0, 0xFBB6, 0xFBBC, 0xFBC2]
plmGreenIndicator  = [0xFBC8, 0xFBCE, 0xFBD4, 0xFBDA]
plmYellowIndicator = [0xFBE0, 0xFBE6, 0xFBEC, 0xFBF2]
plmGreyIndicator   = [0xFBF8, 0xFBFE, 0xFC04, 0xFC0A]
plmWaveIndicator   = [0xF60B, 0xF611, 0xF617, 0xF61D]
plmSpazerIndicator = [0xF63B, 0xF641, 0xF647, 0xF64D]
plmPlasmaIndicator = [0xF623, 0xF629, 0xF62F, 0xF635]
plmIceIndicator    = [0xF653, 0xF659, 0xF65F, 0xF665]

colors2plmIndicator = {
    'red': plmRedIndicator,
    'green': plmGreenIndicator,
    'yellow': plmYellowIndicator,
    'grey': plmGreyIndicator,
    'wave': plmWaveIndicator,
    'spazer': plmSpazerIndicator,
    'plasma': plmPlasmaIndicator,
    'ice': plmIceIndicator
}

class IndicatorFlag(IntFlag):
    Standard = 1
    AreaRando = 2
    DoorRando = 4

# indicator always there
IndicatorAll = IndicatorFlag.Standard | IndicatorFlag.AreaRando | IndicatorFlag.DoorRando
# indicator there when not in area rando
IndicatorDoor = IndicatorFlag.Standard | IndicatorFlag.DoorRando

class Door(object):
    __slots__ = ('name', 'canRandom', 'address', 'vanillaColor', 'color', 'forced', 'facing', 'hidden', 'id', 'canGrey', 'forbiddenColors','indicator')
    def __init__(self, name, canRandom, vanillaColor, id, canGrey=False, forbiddenColors=None, indicator=0):
        self.name = name
        self.canRandom = canRandom
        self.vanillaColor = vanillaColor
        self.setColor(vanillaColor)
        self.forced = False
        self.hidden = False
        self.canGrey = canGrey
        self.id = id
        # list of forbidden colors
        self.forbiddenColors = forbiddenColors
        self.indicator = indicator

    def setAddress(self, symbols):
        # using door id get symbol label containing PLM id and its associated address
        # labels are: Door_95_Room_D48E_PLM_C884, need namespace as prefix: bank_8f
        labelRegex = 'bank_8f_Door_{0:0{1}X}_Room_[0-9A-Z]*_PLM_[0-9A-Z]*'.format(self.id, 2)
        addresses = symbols.getAddresses(labelRegex)
        assert len(addresses) == 1, "Multiple or no labels found: {} for door id: {}".format(len(addresses), hex(self.id))
        label = list(addresses.keys())[0]
        addr = list(addresses.values())[0]

        self.address = addr

        # get facing from plm id
        plmId = int(label[-4:], 16)
        self.facing = plmFacing[plmId]

    def forceBlue(self):
        # custom start location, area, patches can force doors to blue
        self.setColor('blue')
        self.forced = True

    def setColor(self, color):
        self.color = color

    def getColor(self):
        if self.hidden:
            return 'grey'
        else:
            return self.color

    def isRandom(self):
        return self.color != self.vanillaColor and not self.isBlue()

    def isBlue(self):
        return self.color == 'blue'

    def canRandomize(self):
        return not self.forced and self.canRandom

    def filterColorList(self, colorsList):
        if self.forbiddenColors is None:
            return colorsList
        else:
            return [color for color in colorsList if color not in self.forbiddenColors]

    def randomize(self, allowGreyDoors):
        if self.canRandomize():
            if self.canGrey and allowGreyDoors:
                self.setColor(random.choice(self.filterColorList(colorsListGrey)))
            else:
                self.setColor(random.choice(self.filterColorList(colorsList)))

    def traverse(self, smbm):
        if self.hidden or self.color == 'grey':
            return SMBool(False)
        elif self.color == 'red':
            return smbm.canOpenRedDoors()
        elif self.color == 'green':
            return smbm.canOpenGreenDoors()
        elif self.color == 'yellow':
            return smbm.canOpenYellowDoors()
        elif self.color == 'wave':
            return smbm.haveItem('Wave')
        elif self.color == 'spazer':
            return smbm.haveItem('Spazer')
        elif self.color == 'plasma':
            return smbm.haveItem('Plasma')
        elif self.color == 'ice':
            return smbm.haveItem('Ice')
        else:
            return SMBool(True)

    def __repr__(self):
        return "Door({}, {})".format(self.name, self.color)

    def isRefillSave(self):
        return not self.canRandom

    def writeColor(self, rom, writeWordFunc):
        if self.isBlue() or self.isRefillSave():
            return

        writeWordFunc(colors2plm[self.color][self.facing], snes_to_pc(self.address))

        # also set plm args high byte to never opened, even during escape
        if self.color == 'grey':
            rom.writeByte(0x90, snes_to_pc(self.address+5))

    def readColor(self, rom, readWordFunc):
        if self.forced or self.isRefillSave():
            return

        plm = readWordFunc(snes_to_pc(self.address))
        if plm in plmRed:
            self.setColor('red')
        elif plm in plmGreen:
            self.setColor('green')
        elif plm in plmYellow:
            self.setColor('yellow')
        elif plm in plmGrey:
            self.setColor('grey')
        elif plm in plmWave:
            self.setColor('wave')
        elif plm in plmSpazer:
            self.setColor('spazer')
        elif plm in plmPlasma:
            self.setColor('plasma')
        elif plm in plmIce:
            self.setColor('ice')
        else:
            # we can't read the color, handle as grey door (can happen in race protected seeds)
            self.setColor('grey')

    # gives the PLM ID for matching indicator door
    def getIndicatorPLM(self, indicatorFlags):
        ret = None
        if (indicatorFlags & self.indicator) != 0 and self.color in colors2plmIndicator:
            ret = colors2plmIndicator[self.color][indicatorsDirection[self.facing]]
        return ret

    # for tracker
    def canHide(self):
        return self.color != 'blue'

    def hide(self):
        if self.canHide():
            self.hidden = True

    def reveal(self):
        self.hidden = False

    def switch(self):
        if self.hidden:
            self.reveal()
        else:
            self.hide()

    # to send/receive state to tracker/plando
    def serialize(self):
        return (self.color, self.facing, self.hidden)

    def unserialize(self, data):
        self.setColor(data[0])
        self.facing = data[1]
        self.hidden = data[2]

class DoorsManager():
    doors = {
        # crateria
        'LandingSiteRight': Door('LandingSiteRight', True, 'green', canGrey=True, indicator=IndicatorAll, id=0x00),
        'LandingSiteTopRight': Door('LandingSiteTopRight', True, 'yellow', id=0x01),
        'KihunterBottom': Door('KihunterBottom', True, 'yellow', canGrey=True, indicator=IndicatorDoor, id=0x0e),
        'KihunterRight': Door('KihunterRight', True, 'yellow', canGrey=True, indicator=IndicatorAll, id=0x0d),
        'FlywayRight': Door('FlywayRight', True, 'red', id=0x1d),
        'GreenPiratesShaftBottomRight': Door('GreenPiratesShaftBottomRight', True, 'red', canGrey=True, id=0x1e),
        'RedBrinstarElevatorTop': Door('RedBrinstarElevatorTop', True, 'yellow', id=0x10),
        'ClimbRight': Door('ClimbRight', True, 'yellow', id=0x13),
        # blue brinstar
        'ConstructionZoneRight': Door('ConstructionZoneRight', True, 'red', id=0x32),
        # green brinstar
        'GreenHillZoneTopRight': Door('GreenHillZoneTopRight', True, 'yellow', canGrey=True, indicator=IndicatorFlag.DoorRando, id=0x30),
        'NoobBridgeRight': Door('NoobBridgeRight', True, 'green', canGrey=True, indicator=IndicatorDoor, id=0x33),
        'MainShaftRight': Door('MainShaftRight', True, 'red', id=0x21),
        'MainShaftBottomRight': Door('MainShaftBottomRight', True, 'red', canGrey=True, indicator=IndicatorAll, id=0x22),
        'EarlySupersRight': Door('EarlySupersRight', True, 'red', id=0x26),
        'EtecoonEnergyTankLeft': Door('EtecoonEnergyTankLeft', True, 'green', id=0x34),
        # pink brinstar
        'BigPinkTopRight': Door('BigPinkTopRight', True, 'red', id=0x2a),
        'BigPinkRight': Door('BigPinkRight', True, 'yellow', id=0x28),
        'BigPinkBottomRight': Door('BigPinkBottomRight', True, 'green', canGrey=True, indicator=IndicatorAll, id=0x29),
        'BigPinkBottomLeft': Door('BigPinkBottomLeft', True, 'red', id=0x2b),
        # red brinstar
        'RedTowerLeft': Door('RedTowerLeft', True, 'yellow', id=0x39),
        'RedBrinstarFirefleaLeft': Door('RedBrinstarFirefleaLeft', True, 'red', id=0x3a),
        'RedTowerElevatorTopLeft': Door('RedTowerElevatorTopLeft', True, 'green', id=0x3b),
        'RedTowerElevatorLeft': Door('RedTowerElevatorLeft', True, 'yellow', indicator=IndicatorAll, id=0x3c),
        'RedTowerElevatorBottomLeft': Door('RedTowerElevatorBottomLeft', True, 'green', id=0x3d),
        'BelowSpazerTopRight': Door('BelowSpazerTopRight', True, 'green', id=0x3f),
        # Wrecked ship
        'WestOceanRight': Door('WestOceanRight', True, 'green', canGrey=True, indicator=IndicatorAll, id=0x0c),
        'LeCoudeBottom': Door('LeCoudeBottom', True, 'yellow', canGrey=True, indicator=IndicatorDoor, id=0x0f),
        'WreckedShipMainShaftBottom': Door('WreckedShipMainShaftBottom', True, 'green', indicator=IndicatorFlag.AreaRando, id=0x84),
        'ElectricDeathRoomTopLeft': Door('ElectricDeathRoomTopLeft', True, 'red', id=0x8b),
        # Upper Norfair
        'BusinessCenterTopLeft': Door('BusinessCenterTopLeft', True, 'green', id=0x4b),
        'BusinessCenterBottomLeft': Door('BusinessCenterBottomLeft', True, 'red', id=0x4d),
        'CathedralEntranceRight': Door('CathedralEntranceRight', True, 'red', canGrey=True, indicator=IndicatorAll, id=0x4a),
        'CathedralRight': Door('CathedralRight', True, 'green',indicator=IndicatorAll, id=0x49),
        'BubbleMountainTopRight': Door('BubbleMountainTopRight', True, 'green', id=0x54),
        'BubbleMountainTopLeft': Door('BubbleMountainTopLeft', True, 'green', id=0x53),
        'SpeedBoosterHallRight': Door('SpeedBoosterHallRight', True, 'red', id=0x55),
        'SingleChamberRight': Door('SingleChamberRight', True, 'red', id=0x56),
        'DoubleChamberRight': Door('DoubleChamberRight', True, 'red', id=0x57),
        'KronicBoostBottomLeft': Door('KronicBoostBottomLeft', True, 'yellow', canGrey=True, id=0x58),
        'CrocomireSpeedwayBottom': Door('CrocomireSpeedwayBottom', True, 'green', canGrey=True, id=0x4e),
        # Crocomire
        'PostCrocomireUpperLeft': Door('PostCrocomireUpperLeft', True, 'red', id=0x51),
        'PostCrocomireShaftRight': Door('PostCrocomireShaftRight', True, 'red', id=0x52),
        # Lower Norfair
        'RedKihunterShaftBottom': Door('RedKihunterShaftBottom', True, 'yellow', indicator=IndicatorFlag.AreaRando, id=0x5e),
        'WastelandLeft': Door('WastelandLeft', True, 'green', forbiddenColors=['yellow'], indicator=IndicatorFlag.AreaRando, id=0x5f),
        # Maridia
        'MainStreetBottomRight': Door('MainStreetBottomRight', True, 'red', indicator=IndicatorAll, id=0x8d),
        'FishTankRight': Door('FishTankRight', True, 'red', id=0x8e),
        'CrabShaftRight': Door('CrabShaftRight', True, 'green', indicator=IndicatorDoor, id=0x8f),
        'ColosseumBottomRight': Door('ColosseumBottomRight', True, 'green', indicator=IndicatorFlag.AreaRando, id=0x9a),
        'PlasmaSparkBottom': Door('PlasmaSparkBottom', True, 'green', id=0x94),
        'OasisTop': Door('OasisTop', True, 'green', id=0x95),
        # refill/save
        'GreenBrinstarSaveStation': Door('GreenBrinstarSaveStation', False, 'red', id=0x1f),
        'MaridiaBottomSaveStation': Door('MaridiaBottomSaveStation', False, 'red', id=0x8c),
        'MaridiaAqueductSaveStation': Door('MaridiaAqueductSaveStation', False, 'red', id=0x96),
        'ForgottenHighwaySaveStation': Door('ForgottenHighwaySaveStation', False, 'red', id=0x92),
        'DraygonSaveRefillStation': Door('DraygonSaveRefillStation', False, 'red', id=0x98),
        'KraidRefillStation': Door('KraidRefillStation', False, 'green', id=0x44),
        'RedBrinstarEnergyRefill': Door('RedBrinstarEnergyRefill', False, 'green', id=0x38),
        'GreenBrinstarMissileRefill': Door('GreenBrinstarMissileRefill', False, 'red', id=0x23)
    }

    def __init__(self):
        pass

    @staticmethod
    def setDoorsAddress(symbols):
        for door in DoorsManager.doors.values():
            door.setAddress(symbols)

    # call from logic
    def traverse(self, smbm, doorName):
        return DoorsManager.doors[doorName].traverse(smbm)

    @staticmethod
    def setDoorsColor():
        # depending on loaded patches, force some doors to blue, excluding them from randomization
        if RomPatches.has(RomPatches.BlueBrinstarBlueDoor):
            DoorsManager.doors['ConstructionZoneRight'].forceBlue()
        if RomPatches.has(RomPatches.BrinReserveBlueDoors):
            DoorsManager.doors['MainShaftRight'].forceBlue()
            DoorsManager.doors['EarlySupersRight'].forceBlue()
        if RomPatches.has(RomPatches.EtecoonSupersBlueDoor):
            DoorsManager.doors['EtecoonEnergyTankLeft'].forceBlue()
        #if RomPatches.has(RomPatches.SpongeBathBlueDoor):
        #    DoorsManager.doors[''].forceBlue()
        if RomPatches.has(RomPatches.HiJumpAreaBlueDoor):
            DoorsManager.doors['BusinessCenterBottomLeft'].forceBlue()
        if RomPatches.has(RomPatches.SpeedAreaBlueDoors):
            DoorsManager.doors['BubbleMountainTopRight'].forceBlue()
            DoorsManager.doors['SpeedBoosterHallRight'].forceBlue()
        if RomPatches.has(RomPatches.MamaTurtleBlueDoor):
            DoorsManager.doors['FishTankRight'].forceBlue()
        if RomPatches.has(RomPatches.HellwayBlueDoor):
            DoorsManager.doors['RedTowerElevatorLeft'].forceBlue()
        if RomPatches.has(RomPatches.RedTowerBlueDoors):
            DoorsManager.doors['RedBrinstarElevatorTop'].forceBlue()
        if RomPatches.has(RomPatches.AreaRandoBlueDoors):
            DoorsManager.doors['GreenHillZoneTopRight'].forceBlue()
            DoorsManager.doors['NoobBridgeRight'].forceBlue()
            DoorsManager.doors['LeCoudeBottom'].forceBlue()
            DoorsManager.doors['KronicBoostBottomLeft'].forceBlue()
        else:
            # no area rando, prevent some doors to be in the grey doors pool
            DoorsManager.doors['GreenPiratesShaftBottomRight'].canGrey = False
            DoorsManager.doors['CrocomireSpeedwayBottom'].canGrey = False
            DoorsManager.doors['KronicBoostBottomLeft'].canGrey = False
        if RomPatches.has(RomPatches.AreaRandoMoreBlueDoors):
            DoorsManager.doors['KihunterBottom'].forceBlue()
            DoorsManager.doors['GreenPiratesShaftBottomRight'].forceBlue()
        if RomPatches.has(RomPatches.CrocBlueDoors):
            DoorsManager.doors['CrocomireSpeedwayBottom'].forceBlue()
        if RomPatches.has(RomPatches.CrabShaftBlueDoor):
            DoorsManager.doors['CrabShaftRight'].forceBlue()

    @staticmethod
    def randomize(allowGreyDoors):
        for door in DoorsManager.doors.values():
            door.randomize(allowGreyDoors)
        # set both ends of toilet to the same color to avoid soft locking in area rando
        toiletTop = DoorsManager.doors['PlasmaSparkBottom']
        toiletBottom = DoorsManager.doors['OasisTop']
        if toiletTop.color != toiletBottom.color:
            toiletBottom.setColor(toiletTop.color)
        DoorsManager.debugDoorsColor()

    # call from rom loader
    @staticmethod
    def loadDoorsColor(rom, readWordFunc):
        # force to blue some doors depending on patches
        DoorsManager.setDoorsColor()
        # for each door store it's color
        for door in DoorsManager.doors.values():
            door.readColor(rom, readWordFunc)
        DoorsManager.debugDoorsColor()

        # tell that we have randomized doors
        isRandom = DoorsManager.isRandom()
        if isRandom:
            DoorsManager.setRefillSaveToBlue()
        return isRandom

    @staticmethod
    def isRandom():
        return any(door.isRandom() for door in DoorsManager.doors.values())

    @staticmethod
    def setRefillSaveToBlue():
        for door in DoorsManager.doors.values():
            if not door.canRandom:
                door.forceBlue()

    @staticmethod
    def debugDoorsColor():
        if LOG.getEffectiveLevel() == logging.DEBUG:
            for door in DoorsManager.doors.values():
                LOG.debug("{:>32}: {:>6}".format(door.name, door.color))

    # call from rom patcher
    @staticmethod
    def writeDoorsColor(rom, writeWordFunc):
        for door in DoorsManager.doors.values():
            door.writeColor(rom, writeWordFunc)

    @staticmethod
    def getBlueDoors(doors):
        for door in DoorsManager.doors.values():
            # set save/refill doors to blue
            if not door.canRandom:
                doors.append(door.id)

    # returns a dict {'DoorName': indicatorPlmType }
    @staticmethod
    def getIndicatorPLMs(indicatorFlags):
        ret = {}
        for doorName,door in DoorsManager.doors.items():
            plm = door.getIndicatorPLM(indicatorFlags)
            if plm is not None:
                ret[doorName] = plm
        return ret

    # call from web
    @staticmethod
    def getAddressesToRead():
        return [snes_to_pc(door.address) for door in DoorsManager.doors.values() if door.address is not None] + [snes_to_pc(door.address+1) for door in DoorsManager.doors.values() if door.address is not None]

    # for isolver state
    @staticmethod
    def serialize():
        return {door.name: door.serialize() for door in DoorsManager.doors.values()}

    @staticmethod
    def unserialize(state):
        for name, data in state.items():
            DoorsManager.doors[name].unserialize(data)

    @staticmethod
    def allDoorsRevealed():
        for door in DoorsManager.doors.values():
            if door.hidden:
                return False
        return True

    # when using the tracker, first set all colored doors to grey until the user clicks on it
    @staticmethod
    def initTracker():
        for door in DoorsManager.doors.values():
            door.hide()

    # when the user clicks on a door in the tracker
    @staticmethod
    def switchVisibility(name):
        DoorsManager.doors[name].switch()

    # when the user clicks on a door in the race tracker or the plando
    @staticmethod
    def setColor(name, color):
        # in race mode the doors are hidden
        DoorsManager.doors[name].reveal()
        DoorsManager.doors[name].setColor(color)

    # in autotracker we need the current doors state
    @staticmethod
    def getDoorsState():
        hiddenDoors = set([door.name for door in DoorsManager.doors.values() if door.hidden])
        revealedDoor = set([door.name for door in DoorsManager.doors.values() if (not door.hidden) and door.canHide()])
        return (hiddenDoors, revealedDoor)
