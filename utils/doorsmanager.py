import random
from enum import IntEnum,IntFlag
from logic.smbool import SMBool
from rom.rom_patches import RomPatches
from rom.rom import snes_to_pc
from rom.map import DoorMapIcon
from logic.logic import Logic
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

# door color indicators PLMs (flashing on the other side of colored doors)
indicatorsDirection = {
    Facing.Left: Facing.Right,
    Facing.Right: Facing.Left,
    Facing.Top: Facing.Bottom,
    Facing.Bottom: Facing.Top
}

colors2plmIndicator = None

class IndicatorFlag(IntFlag):
    Standard = 1
    AreaRando = 2
    DoorRando = 4

# indicator always there
IndicatorAll = IndicatorFlag.Standard | IndicatorFlag.AreaRando | IndicatorFlag.DoorRando
# indicator there when not in area rando
IndicatorDoor = IndicatorFlag.Standard | IndicatorFlag.DoorRando

colorSymbols = {
    "red": "missile",
    "green": "super",
    "yellow": "PB",
    "grey": "none"
}

directions = ["left", "right", "top", "bottom"]
beams = ["wave", "spazer", "plasma", "ice"]

class DoorsAddresses(object):
    _instance = None

    def Instance(symbols):
        if DoorsAddresses._instance is None:
            DoorsAddresses._instance = DoorsAddresses(symbols)
        return DoorsAddresses._instance

    def __init__(self, symbols):
        getReq = lambda color: colorSymbols[color] if color in colorSymbols else color
        beamDoorPLM = lambda color, dir: symbols.getAddress("beam_doors_plms", f"plm_{getReq(color)}_{dir}") & 0xffff
        indicatorPatch = "door_indicators_plms"
        indicatorPLM = lambda color, dir: symbols.getAddress(indicatorPatch, f"plm_indicator_{getReq(color)}_{dir}") & 0xffff
        self.doorPLMs = {
            # door facing left - right - top   - bottom
            "red": [0xc88a, 0xc890, 0xc896, 0xc89c],
            "green": [0xc872, 0xc878, 0xc87e, 0xc884],
            "yellow": [0xc85a, 0xc860, 0xc866, 0xc86c],
            "grey": [0xc842, 0xc848, 0xc84e, 0xc854]
        }
        self.indicatorPLMs = {color:[indicatorPLM(color, direction) for direction in directions] for color in self.doorPLMs.keys()}
        indicatorPatch = "beam_doors_plms"
        for beam in beams:
            self.doorPLMs[beam] = [beamDoorPLM(beam, direction) for direction in directions]
            self.indicatorPLMs[beam] = [indicatorPLM(beam, direction) for direction in directions]
        self.plmInfoById = {plms[f]: (f, color) for color, plms in self.doorPLMs.items() for f in Facing}

class Door(object):
    __slots__ = ('name', 'canRandom', 'address', 'vanillaColor', 'color', 'forced', 'facing', 'hidden', 'id', 'canGrey', 'forbiddenColors','indicator', 'doorsAddresses')
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
        self.doorsAddresses = None

    def vanilla(self):
        self.setColor(self.vanillaColor)

    def setAddress(self, symbols):
        self.doorsAddresses = DoorsAddresses.Instance(symbols)
        # using door id get symbol label containing PLM id and its associated address
        # labels are: Door_95_Room_D48E_PLM_C884, need namespace as prefix: bank_8f
        labelRegex = 'Door_{0:0{1}X}_Room_[0-9A-Z]*_PLM_[0-9A-Z]*'.format(self.id, 2)
        addresses = symbols.getAddresses('bank_8f', labelRegex)
        assert len(addresses) == 1, "Multiple or no labels found: {} for door id: {}".format(len(addresses), hex(self.id))
        label = list(addresses.keys())[0]
        addr = list(addresses.values())[0]

        self.address = addr

        # get facing from plm id
        plmId = int(label[-4:], 16)
        self.facing = self.doorsAddresses.plmInfoById[plmId][0]

    def forceBlue(self):
        # custom start location, area, patches can force doors to blue
        self.setColor('blue')
        self.forced = True
        self.hidden = False

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

    def filterColorList(self, colorsList, forbiddenColors):
        forb = []
        if self.forbiddenColors is not None:
            forb += self.forbiddenColors
        if forbiddenColors is not None:
            forb += forbiddenColors
        return colorsList if len(forb) == 0 else [color for color in colorsList if color not in forb]

    def randomize(self, allowGreyDoors, forbiddenColors=None):
        if self.canRandomize():
            colList = colorsListGrey if self.canGrey and allowGreyDoors else colorsList
            self.setColor(random.choice(self.filterColorList(colList, forbiddenColors)))

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

        writeWordFunc(self.doorsAddresses.doorPLMs[self.color][self.facing], snes_to_pc(self.address))

        # also set plm args high byte to never opened, even during escape
        if self.color == 'grey':
            rom.writeByte(0x90, snes_to_pc(self.address+5))

    # assumes rom is positioned correctly in table
    def writeMapIcon(self, x, y, writeWordFunc):
        if self.isBlue() or self.isRefillSave():
            return
        writeWordFunc(x)
        writeWordFunc(y)
        icon = doors_mapicons[(self.color, self.facing)]
        writeWordFunc(icon.table_index)
        writeWordFunc(self.id)

    def readColor(self, rom, readWordFunc):
        if self.forced or self.isRefillSave():
            return
        plm = readWordFunc(snes_to_pc(self.address))
        plmInfo = self.doorsAddresses.plmInfoById.get(plm)
        if plmInfo is not None:
            self.setColor(plmInfo[1])
        else:
            # we can't read the color, handle as grey door (can happen in race protected seeds)
            self.setColor('grey')

    # gives the PLM ID for matching indicator door
    def getIndicatorPLM(self, indicatorFlags):
        ret = None
        if (indicatorFlags & self.indicator) != 0 and self.color in self.doorsAddresses.indicatorPLMs:
            ret = self.doorsAddresses.indicatorPLMs[self.color][indicatorsDirection[self.facing]]
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

    # to send/receive state to tracker/plando.
    # having Facing object in the state makes web2py create a new session with it restarts,
    # so serialize to integer.
    def serialize(self):
        return (self.color, int(self.facing), self.hidden)

    def unserialize(self, data):
        self.setColor(data[0])
        self.facing = Facing(data[1])
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
    def setDoorsColor(seedless=False):
        if seedless:
            # reset to vanilla colors
            for door in DoorsManager.doors.values():
                door.vanilla()

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
        if RomPatches.has(RomPatches.AlphaPowerBombBlueDoor):
            DoorsManager.doors['RedTowerElevatorBottomLeft'].forceBlue()
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
        if RomPatches.has(RomPatches.WsEtankBlueDoor):
            DoorsManager.doors['ElectricDeathRoomTopLeft'].forceBlue()

    @staticmethod
    def randomize(allowGreyDoors, forbiddenColors=None):
        for door in DoorsManager.doors.values():
            door.randomize(allowGreyDoors, forbiddenColors)
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
    # assumes rom is positioned correctly to start of door table
    def writeDoorsMapIcons(area, areaMap, writeWordFunc):
        mapIconData = Logic.map_tiles.doors
        for doorName, tileEntry in mapIconData.items():
            if tileEntry['area'] != area:
                continue
            x, y = areaMap.getCoordsByte(tileEntry['byteIndex'], tileEntry['bitMask'])
            door = DoorsManager.doors[doorName]
            # *8 to convert tile coords to pixel coords
            door.writeMapIcon(x*8, y*8, writeWordFunc)
        writeWordFunc(0xffff) # terminator

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
    def initTracker(hide):
        if hide:
            for door in DoorsManager.doors.values():
                door.hide()
        else:
            for door in DoorsManager.doors.values():
                door.reveal()

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

doors_mapicons = {
    ('red', Facing.Left): DoorMapIcon(0xCB, x=-1, y=-1),
    ('green', Facing.Left): DoorMapIcon(0xCC, x=-1, y=-1),
    ('yellow', Facing.Left): DoorMapIcon(0xCD, x=-1, y=-1),
    ('grey', Facing.Left): DoorMapIcon(0xCE, x=-1, y=-1),
    ('wave', Facing.Left): DoorMapIcon(0xCF, x=-1, y=-1),
    ('plasma', Facing.Left): DoorMapIcon(0xD0, x=-1, y=-1),
    ('spazer', Facing.Left): DoorMapIcon(0xD1, x=-1, y=-1),
    ('ice', Facing.Left): DoorMapIcon(0xD2, x=-1, y=-1),

    ('red', Facing.Bottom): DoorMapIcon(0xD3, y=1),
    ('green', Facing.Bottom): DoorMapIcon(0xD4, y=1),
    ('yellow', Facing.Bottom): DoorMapIcon(0xD5, y=1),
    ('grey', Facing.Bottom): DoorMapIcon(0xD6, y=1),
    ('wave', Facing.Bottom): DoorMapIcon(0xD7, y=1),
    ('plasma', Facing.Bottom): DoorMapIcon(0xD8, y=1),
    ('spazer', Facing.Bottom): DoorMapIcon(0xD9, y=1),
    ('ice', Facing.Bottom): DoorMapIcon(0xDA, y=1),

    ('red', Facing.Right): DoorMapIcon(0xCB, hFlip=True, x=1, y=-1),
    ('green', Facing.Right): DoorMapIcon(0xCC, hFlip=True, x=1, y=-1),
    ('yellow', Facing.Right): DoorMapIcon(0xCD, hFlip=True, x=1, y=-1),
    ('grey', Facing.Right): DoorMapIcon(0xCE, hFlip=True, x=1, y=-1),
    ('wave', Facing.Right): DoorMapIcon(0xCF, hFlip=True, x=1, y=-1),
    ('plasma', Facing.Right): DoorMapIcon(0xD0, hFlip=True, x=1, y=-1),
    ('spazer', Facing.Right): DoorMapIcon(0xD1, hFlip=True, x=1, y=-1),
    ('ice', Facing.Right): DoorMapIcon(0xD2, hFlip=True, x=1, y=-1),

    ('red', Facing.Top): DoorMapIcon(0xD3, vFlip=True, y=-1),
    ('green', Facing.Top): DoorMapIcon(0xD4, vFlip=True, y=-1),
    ('yellow', Facing.Top): DoorMapIcon(0xD5, vFlip=True, y=-1),
    ('grey', Facing.Top): DoorMapIcon(0xD6, vFlip=True, y=-1),
    ('wave', Facing.Top): DoorMapIcon(0xD7, vFlip=True, y=-1),
    ('plasma', Facing.Top): DoorMapIcon(0xD8, vFlip=True, y=-1),
    ('spazer', Facing.Top): DoorMapIcon(0xD9, vFlip=True, y=-1),
    ('ice', Facing.Top): DoorMapIcon(0xDA, vFlip=True, y=-1),
}

def assignMapIconSpriteTableIndices():
    i = 0
    for icon in doors_mapicons.values():
        icon.table_index = i
        i += 1

assignMapIconSpriteTableIndices()
