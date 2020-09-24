import random
from smbool import SMBool
from rom_patches import RomPatches
import log, logging

LOG = log.get('DoorsManager')

colorsList = ['red', 'green', 'yellow']

class Facing:
    Left = 0
    Right = 1
    Top = 2
    Bottom = 3

# door facing left - right - top   - bottom
plmRed    = [0x8a,   0x90,   0x96,   0x9c]
plmGreen  = [0x72,   0x78,   0x7e,   0x84]
plmYellow = [0x5a,   0x60,   0x66,   0x6c]
plmBlink  = [0x42,   0x48,   0x4e,   0x54]

colors2plm = {
    'red': plmRed,
    'green': plmGreen,
    'yellow': plmYellow
}

class Door(object):
    __slots__ = ('name', 'address', 'vanillaColor', 'color', 'forced', 'facing', 'hidden')
    def __init__(self, name, address, vanillaColor, facing):
        self.name = name
        self.address = address
        self.vanillaColor = vanillaColor
        self.setColor(vanillaColor)
        self.forced = False
        self.facing = facing
        self.hidden = False

    def forceBlue(self):
        # custom start location, area, patches can force doors to blue
        self.setColor('blue')
        self.forced = True

    def setColor(self, color):
        if color == 'grey':
            self.hidden = True
        else:
            self.color = color

    def getColor(self):
        if self.hidden:
            return 'grey'
        else:
            return self.color

    def isRandom(self):
        return self.color != self.vanillaColor and self.color != 'blue'

    def randomize(self):
        if not self.forced:
            self.setColor(random.choice(colorsList))

    def traverse(self, smbm):
        if self.hidden:
            return SMBool(False)
        elif self.color == 'red':
            return smbm.canOpenRedDoors()
        elif self.color == 'green':
            return smbm.canOpenGreenDoors()
        elif self.color == 'yellow':
            return smbm.canOpenYellowDoors()
        else:
            return SMBool(True)

    def __repr__(self):
        print("Door({}, {})".format(self.name, self.color))

    def writeColor(self, rom):
        if not self.isRandom():
            return

        rom.writeByte(colors2plm[self.color][self.facing], self.address)

    def readColor(self, rom):
        if self.forced:
            return

        plm = rom.readByte(self.address)
        if plm in plmRed:
            self.setColor('red')
        elif plm in plmGreen:
            self.setColor('green')
        elif plm in plmYellow:
            self.setColor('yellow')
        elif plm in plmBlink:
            self.setColor('blue')
        else:
            raise Exception("Unknown color {} for {}".format(hex(plm), self.name))

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

class DoorsManager():
    doors = {
        # crateria
        'LandingSiteRight': Door('LandingSiteRight', 0x78018, 'green', Facing.Left),
        'LandingSiteTopRight': Door('LandingSiteTopRight', 0x07801e, 'yellow', Facing.Left),
        'KihunterBottom': Door('KihunterBottom', 0x78228, 'yellow', Facing.Top),
        'KihunterRight': Door('KihunterRight', 0x78222, 'yellow', Facing.Left),
        'FlywayRight': Door('FlywayRight', 0x78420, 'red', Facing.Left),
        'GreenPiratesShaftBottomRight': Door('GreenPiratesShaftBottomRight', 0x78470, 'red', Facing.Left),
        'RedBrinstarElevatorTop': Door('RedBrinstarElevatorTop', 0x78256, 'yellow', Facing.Bottom),
        'ClimbRight': Door('ClimbRight', 0x78304, 'yellow', Facing.Left),
        # blue brinstar
        'ConstructionZoneRight': Door('ConstructionZoneRight', 0x78784, 'red', Facing.Left),
        # green brinstar
        'GreenHillZoneTopRight': Door('GreenHillZoneTopRight', 0x78670, 'yellow', Facing.Left),
        'NoobBridgeRight': Door('NoobBridgeRight', 0x787a6, 'green', Facing.Left),
        'MainShaftRight': Door('MainShaftRight', 0x784be, 'red', Facing.Left),
        'MainShaftBottomRight': Door('MainShaftBottomRight', 0x784c4, 'red', Facing.Left),
        'EarlySupersRight': Door('EarlySupersRight', 0x78512, 'red', Facing.Left),
        'EtecoonEnergyTankLeft': Door('EtecoonEnergyTankLeft', 0x787c8, 'green', Facing.Right),
        # pink brinstar
        'BigPinkTopRight': Door('BigPinkTopRight', 0x78626, 'red', Facing.Left),
        'BigPinkRight': Door('BigPinkRight', 0x7861a, 'yellow', Facing.Left),
        'BigPinkBottomRight': Door('BigPinkBottomRight', 0x78620, 'green', Facing.Left),
        'BigPinkBottomLeft': Door('BigPinkBottomLeft', 0x7862c, 'red', Facing.Right),
        # red brinstar
        'RedTowerLeft': Door('RedTowerLeft', 0x78866, 'yellow', Facing.Right),
        'RedBrinstarFirefleaLeft': Door('RedBrinstarFirefleaLeft', 0x7886e, 'red', Facing.Right),
        'RedTowerElevatorTopLeft': Door('RedTowerElevatorTopLeft', 0x788aa, 'green', Facing.Right),
        'RedTowerElevatorLeft': Door('RedTowerElevatorLeft', 0x788b0, 'yellow', Facing.Right),
        'RedTowerElevatorBottomLeft': Door('RedTowerElevatorBottomLeft', 0x788b6, 'green', Facing.Right),
        'BelowSpazerTopRight': Door('BelowSpazerTopRight', 0x78966, 'green', Facing.Left),
        # Wrecked ship
        'WestOceanRight': Door('WestOceanRight', 0x781e2, 'green', Facing.Left),
        'LeCoudeBottom': Door('LeCoudeBottom', 0x7823e, 'yellow', Facing.Top),
        'WreckedShipMainShaftBottom': Door('WreckedShipMainShaftBottom', 0x7c277, 'green', Facing.Top),
        'ElectricDeathRoomTopLeft': Door('ElectricDeathRoomTopLeft', 0x7c32f, 'red', Facing.Right),
        # Upper Norfair
        'BusinessCenterTopLeft': Door('BusinessCenterTopLeft', 0x78b00, 'green', Facing.Right),
        'BusinessCenterBottomLeft': Door('BusinessCenterBottomLeft', 0x78b0c, 'red', Facing.Right),
        'CathedralEntranceRight': Door('CathedralEntranceRight', 0x78af2, 'red', Facing.Left),
        'CathedralRight': Door('CathedralRight', 0x78aea, 'green', Facing.Left),
        'BubbleMountainTopRight': Door('BubbleMountainTopRight', 0x78c60, 'green', Facing.Left),
        'BubbleMountainTopLeft': Door('BubbleMountainTopLeft', 0x78c5a, 'green', Facing.Right),
        'SpeedBoosterHallRight': Door('SpeedBoosterHallRight', 0x78c7a, 'red', Facing.Left),
        'SingleChamberRight': Door('SingleChamberRight', 0x78ca8, 'red', Facing.Left),
        'DoubleChamberRight': Door('DoubleChamberRight', 0x78cc2, 'red', Facing.Left),
        'KronicBoostBottomLeft': Door('KronicBoostBottomLeft', 0x78d4e, 'yellow', Facing.Right),
        'CrocomireSpeedwayBottom': Door('CrocomireSpeedwayBottom', 0x78b96, 'green', Facing.Top),
        # Crocomire
        'PostCrocomireUpperLeft': Door('PostCrocomireUpperLeft', 0x78bf4, 'red', Facing.Right),
        'PostCrocomireShaftRight': Door('PostCrocomireShaftRight', 0x78c0c, 'red', Facing.Left),
        # Lower Norfair
        'RedKihunterShaftBottom': Door('RedKihunterShaftBottom', 0x7902e, 'yellow', Facing.Top),
        'WastelandLeft': Door('WastelandLeft', 0x790ba, 'green', Facing.Right),
        # Maridia
        'MainStreetBottomRight': Door('MainStreetBottomRight', 0x7c431, 'red', Facing.Left),
        'FishTankRight': Door('FishTankRight', 0x7c475, 'red', Facing.Left),
        'CrabShaftRight': Door('CrabShaftRight', 0x7c4fb, 'green', Facing.Left),
        'ColosseumBottomRight': Door('ColosseumBottomRight', 0x7c6fb, 'green', Facing.Left),
        'PlasmaSparkBottom': Door('PlasmaSparkBottom', 0x7c577, 'green', Facing.Top),
        'OasisTop': Door('OasisTop', 0x7c5d3, 'green', Facing.Bottom),
    }

    def setSMBM(self, smbm):
        self.smbm = smbm

    # call from logic
    def traverse(self, doorName):
        return DoorsManager.doors[doorName].traverse(self.smbm)

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
        if RomPatches.has(RomPatches.AreaRandoMoreBlueDoors):
            DoorsManager.doors['KihunterBottom'].forceBlue()
            DoorsManager.doors['GreenPiratesShaftBottomRight'].forceBlue()
        if RomPatches.has(RomPatches.CrocBlueDoors):
            DoorsManager.doors['CrocomireSpeedwayBottom'].forceBlue()
        if RomPatches.has(RomPatches.CrabShaftBlueDoor):
            DoorsManager.doors['CrabShaftRight'].forceBlue()

    @staticmethod
    def randomize():
        for door in DoorsManager.doors.values():
            door.randomize()
        # set both ends of toilet to the same color to avoid soft locking in area rando
        toiletTop = DoorsManager.doors['PlasmaSparkBottom']
        toiletBottom = DoorsManager.doors['OasisTop']
        if toiletTop.color != toiletBottom.color:
            toiletBottom.setColor(toiletTop.color)
        DoorsManager.debugDoorsColor()

    # call from rom loader
    @staticmethod
    def loadDoorsColor(rom):
        # force to blue some doors depending on patches
        DoorsManager.setDoorsColor()
        # for each door store it's color
        for door in DoorsManager.doors.values():
            door.readColor(rom)
        DoorsManager.debugDoorsColor()

        # tell that we have randomized doors
        return any(door.isRandom() for door in DoorsManager.doors.values())

    @staticmethod
    def debugDoorsColor():
        if LOG.getEffectiveLevel() == logging.DEBUG:
            for door in DoorsManager.doors.values():
                LOG.debug("{:>32}: {:>6}".format(door.name, door.color))

    # call from rom patcher
    @staticmethod
    def writeDoorsColor(rom):
        for door in DoorsManager.doors.values():
            door.writeColor(rom)

    # call from web
    @staticmethod
    def getAddressesToRead():
        return [door.address for door in DoorsManager.doors.values()]

    # for isolver state
    @staticmethod
    def serialize():
        return {door.name: (door.getColor(), door.facing) for door in DoorsManager.doors.values()}

    @staticmethod
    def unserialize(state):
        for name, (color, facing) in state.items():
            DoorsManager.doors[name].setColor(color)

    # when using the tracker, first set all colored doors to grey until the user clicks on it
    @staticmethod
    def initTracker():
        for door in DoorsManager.doors.values():
            door.hide()

    # when the user clicks on a door in the tracker
    @staticmethod
    def switchVisibility(name):
        DoorsManager.doors[name].switch()
