from enum import Enum, unique
from smbool import SMBool
from rom_patches import RomPatches

colorsList = ['red', 'green', 'yellow']

@unique
class Facing(Enum):
    Left = 0
    Right = 1
    Top = 2
    Bottom = 3

# door facing left - right - top   - bottom
plmRed    = [0xc88a, 0xc890, 0xc896, 0xc89c]
plmGreen  = [0xc872, 0xc878, 0xc87e, 0xc884]
plmYellow = [0xc85a, 0xc860, 0xc866, 0xc86c]

colors2plm = {
    'red': plmRed,
    'green': plmGreen,
    'yellow': plmYellow
}

class Door(object):
    __slots__ = ('name', 'address', 'vanillaColor', 'color', 'canRandom', 'facing')
    def __init__(self, name, address, vanillaColor, facing):
        self.name = name
        self.address = address
        self.vanillaColor = vanillaColor
        self.setColor(vanillaColor)
        self.canRandom = True
        self.facing = facing

    def forceBlue(self):
        # custom start location, area, patches can force doors to blue
        self.setColor('blue')
        self.canRandom = False

    def setColor(self, color):
        self.color = color

    def isRandom(self):
        return self.color != self.vanillaColor

    def randomize(self):
        if self.canRandom:
            self.setColor(random.choice(colorsList))

    def traverse(self, smbm):
        if self.color == 'red':
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
        if not self.isRandom() or self.color == 'blue':
            return

        rom.writeWord(self.address, colors2plm[self.color][self.facing])

    def readColor(self, rom):
        plm = rom.readWord(self.address)
        if plm in plmRed:
            self.setColor('red')
        elif plm in plmGreen:
            self.setColor('green')
        elif plm in plmYellow:
            self.setColor('yellow')
        else:
            raise "Unknown color {} for {}".format(hex(plm), self.name)

class DoorsManager():
    doors = {
        # crateria
        'LandingSiteRight': Door('LandingSiteRight', 0x78018, 'green', Facing.Left),
        'LandingSiteTopRight': Door('LandingSiteTopRight', 0x0, 'yellow', Facing.Left),
        'KihunterBottom': Door('KihunterBottom', 0x0, 'yellow', Facing.Top),
        'KihunterRight': Door('KihunterRight', 0x0, 'yellow', Facing.Left),
        'FlywayRight': Door('FlywayRight', 0x0, 'red', Facing.Left),
        'GreenPiratesShaftBottomRight': Door('GreenPiratesShaftBottomRight', 0x0, 'red', Facing.Left),
        'RedBrinstarElevatorTop': Door('RedBrinstarElevatorTop', 0x0, 'yellow', Facing.Bottom),
        # blue brinstar
        'ConstructionZoneRight': Door('ConstructionZoneRight', 0x0, 'red', Facing.Left),
        # green brinstar
        'GreenHillZoneTopRight': Door('GreenHillZoneTopRight', 0x0, 'yellow', Facing.Left),
        'NoobBridgeRight': Door('NoobBridgeRight', 0x0, 'green', Facing.Left),
        'MainShaftRight': Door('MainShaftRight', 0x0, 'red', Facing.Left),
        'MainShaftBottomRight': Door('MainShaftBottomRight', 0x0, 'red', Facing.Left),
        'EarlySupersRight': Door('EarlySupersRight', 0x0, 'red', Facing.Left),
        'EtecoonEnergyTankLeft': Door('EtecoonEnergyTankLeft', 0x0, 'green', Facing.Right),
        # pink brinstar
        'BigPinkTopRight': Door('BigPinkTopRight', 0x0, 'red', Facing.Left),
        'BigPinkRight': Door('BigPinkRight', 0x0, 'yellow', Facing.Left),
        'BigPinkBottomRight': Door('BigPinkBottomRight', 0x0, 'green', Facing.Left),
        'BigPinkBottomLeft': Door('BigPinkBottomLeft', 0x0, 'red', Facing.Right),
        # red brinstar
        'RedTowerLeft': Door('RedTowerLeft', 0x0, 'yellow', Facing.Right),
        'RedBrinstarFirefleaLeft': Door('RedBrinstarFirefleaLeft', 0x0, 'red', Facing.Right),
        'RedTowerElevatorTopLeft': Door('RedTowerElevatorTopLeft', 0x0, 'green', Facing.Right),
        'RedTowerElevatorLeft': Door('RedTowerElevatorLeft', 0x0, 'yellow', Facing.Right),
        'RedTowerElevatorBottomLeft': Door('RedTowerElevatorBottomLeft', 0x0, 'green', Facing.Right),
        'BelowSpazerTopRight': Door('BelowSpazerTopRight', 0x0, 'green', Facing.Left),
        # Wrecked ship
        'WestOceanRight': Door('WestOceanRight', 0x0, 'green', Facing.Left),
        'LeCoudeBottom': Door('LeCoudeBottom', 0x0, 'yellow', Facing.Top),
        'WreckedShipMainShaftBottom': Door('WreckedShipMainShaftBottom', 0x0, 'green', Facing.Top),
        'ElectricDeathRoomTopLeft': Door('ElectricDeathRoomTopLeft', 0x0, 'red', Facing.Right),
        # Upper Norfair
        'BusinessCenterTopLeft': Door('BusinessCenterTopLeft', 0x0, 'green', Facing.Right),
        'BusinessCenterBottomLeft': Door('BusinessCenterBottomLeft', 0x0, 'red', Facing.Right),
        'CathedralEntranceRight': Door('CathedralEntranceRight', 0x0, 'red', Facing.Left),
        'CathedralRight': Door('CathedralRight', 0x0, 'green', Facing.Left),
        'BubbleMountainTopRight': Door('BubbleMountainTopRight', 0x0, 'green', Facing.Left),
        'BubbleMountainTopLeft': Door('BubbleMountainTopLeft', 0x0, 'green', Facing.Right),
        'SpeedBoosterHallRight': Door('SpeedBoosterHallRight', 0x0, 'red', Facing.Left),
        'SingleChamberRight': Door('SingleChamberRight', 0x0, 'red', Facing.Left),
        'DoubleChamberRight': Door('DoubleChamberRight', 0x0, 'red', Facing.Left),
        'KronicBoostBottomLeft': Door('KronicBoostBottomLeft', 0x0, 'yellow', Facing.Right),
        'CrocomireSpeedwayBottom': Door('CrocomireSpeedwayBottom', 0x0, 'green', Facing.Top),
        # Crocomire
        'PostCrocomireUpperLeft': Door('PostCrocomireUpperLeft', 0x0, 'red', Facing.Right),
        'PostCrocomireShaftRight': Door('PostCrocomireShaftRight', 0x0, 'red', Facing.Left),
        # Lower Norfair
        'RedKihunterShaftBottom': Door('RedKihunterShaftBottom', 0x0, 'yellow', Facing.Top),
        'WastelandLeft': Door('WastelandLeft', 0x0, 'green', Facing.Right),
        # Maridia
        'MainStreetBottomRight': Door('MainStreetBottomRight', 0x0, 'red', Facing.Left),
        'FishTankRight': Door('FishTankRight', 0x0, 'red', Facing.Left),
        'CrabShaftRight': Door('CrabShaftRight', 0x0, 'green', Facing.Left),
        'ColosseumBottomRight': Door('ColosseumBottomRight', 0x0, 'green', Facing.Left),
        'PlasmaSparkBottom': Door('PlasmaSparkBottom', 0x0, 'green', Facing.Top),
        'OasisTop': Door('OasisTop', 0x0, 'green', Facing.Bottom),
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

    # call from rom loader
    def loadDoorsColor(self, rom):
        # for each door store it's color
        for door in DoorsManager.doors.values():
            door.readColor(rom)

    # call from rom patcher
    def writeDoorsColor(self, rom):
        for door in DoorsManager.doors.values():
            door.writeColor(rom)
