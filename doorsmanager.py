from smbool import SMBool
from rom_patches import RomPatches

colorsList = ['red', 'green', 'yellow']
# TODO::get values
plmRed = 0x0
plmGreen = 0x0
plmYellow = 0x0

colors2plm = {
    'red': plmRed,
    'green': plmGreen,
    'yellow': plmYellow
}

plm2colors = {
    plmRed: 'red',
    plmGreen: 'green',
    plmYellow: 'yellow',
    # TODO::how to detect blue doors ?
    0x0: 'blue'
}

class Door(object):
    __slots__ = ('name', 'address', 'vanillaColor', 'color', 'canRandom')
    def __init__(self, name, address, vanillaColor):
        self.name = name
        self.address = address
        self.vanillaColor = vanillaColor
        self.setColor(vanillaColor)
        self.canRandom = True

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
        rom.writeWord(self.address, colors2plm[self.color])

    def readColor(self, rom):
        self.setColor(plm2colors[rom.readWord(self.address)])

class DoorsManager():
    doors = {
        # crateria
        'LandingSiteRight': Door('LandingSiteRight', 0x0, 'green'),
        'LandingSiteTopRight': Door('LandingSiteTopRight', 0x0, 'yellow'),
        'KihunterBottom': Door('KihunterBottom', 0x0, 'yellow'),
        'KihunterRight': Door('KihunterRight', 0x0, 'yellow'),
        'FlywayRight': Door('FlywayRight', 0x0, 'red'),
        'GreenPiratesShaftBottomRight': Door('GreenPiratesShaftBottomRight', 0x0, 'red'),
        'RedBrinstarElevatorTop': Door('RedBrinstarElevatorTop', 0x0, 'yellow'),
        # blue brinstar
        'ConstructionZoneRight': Door('ConstructionZoneRight', 0x0, 'red'),
        # green brinstar
        'GreenHillZoneTopRight': Door('GreenHillZoneTopRight', 0x0, 'yellow'),
        'NoobBridgeRight': Door('NoobBridgeRight', 0x0, 'green'),
        'MainShaftRight': Door('MainShaftRight', 0x0, 'red'),
        'MainShaftBottomRight': Door('MainShaftBottomRight', 0x0, 'red'),
        'EarlySupersRight': Door('EarlySupersRight', 0x0, 'red'),
        'EtecoonEnergyTankLeft': Door('EtecoonEnergyTankLeft', 0x0, 'green'),
        # pink brinstar
        'BigPinkTopRight': Door('BigPinkTopRight', 0x0, 'red'),
        'BigPinkRight': Door('BigPinkRight', 0x0, 'yellow'),
        'BigPinkBottomRight': Door('BigPinkBottomRight', 0x0, 'green'),
        'BigPinkBottomLeft': Door('BigPinkBottomLeft', 0x0, 'red'),
        # red brinstar
        'RedTowerLeft': Door('RedTowerLeft', 0x0, 'yellow'),
        'RedBrinstarFirefleaLeft': Door('RedBrinstarFirefleaLeft', 0x0, 'red'),
        'RedTowerElevatorTopLeft': Door('RedTowerElevatorTopLeft', 0x0, 'green'),
        'RedTowerElevatorLeft': Door('RedTowerElevatorLeft', 0x0, 'yellow'),
        'RedTowerElevatorBottomLeft': Door('RedTowerElevatorBottomLeft', 0x0, 'green'),
        'BelowSpazerTopRight': Door('BelowSpazerTopRight', 0x0, 'green'),
        # Wrecked ship
        'WestOceanRight': Door('WestOceanRight', 0x0, 'green'),
        'LeCoudeBottom': Door('LeCoudeBottom', 0x0, 'yellow'),
        'WreckedShipMainShaftBottom': Door('WreckedShipMainShaftBottom', 0x0, 'green'),
        'ElectricDeathRoomTopLeft': Door('ElectricDeathRoomTopLeft', 0x0, 'red'),
        # Upper Norfair
        'BusinessCenterTopLeft': Door('BusinessCenterTopLeft', 0x0, 'green'),
        'BusinessCenterBottomLeft': Door('BusinessCenterBottomLeft', 0x0, 'red'),
        'CathedralEntranceRight': Door('CathedralEntranceRight', 0x0, 'red'),
        'CathedralRight': Door('CathedralRight', 0x0, 'green'),
        'BubbleMountainTopRight': Door('BubbleMountainTopRight', 0x0, 'green'),
        'BubbleMountainTopLeft': Door('BubbleMountainTopLeft', 0x0, 'green'),
        'SpeedBoosterHallRight': Door('SpeedBoosterHallRight', 0x0, 'red'),
        'SingleChamberRight': Door('SingleChamberRight', 0x0, 'red'),
        'DoubleChamberRight': Door('DoubleChamberRight', 0x0, 'red'),
        'KronicBoostBottomLeft': Door('KronicBoostBottomLeft', 0x0, 'yellow'),
        'CrocomireSpeedwayBottom': Door('CrocomireSpeedwayBottom', 0x0, 'green'),
        # Crocomire
        'PostCrocomireUpperLeft': Door('PostCrocomireUpperLeft', 0x0, 'red'),
        'PostCrocomireShaftRight': Door('PostCrocomireShaftRight', 0x0, 'red'),
        # Lower Norfair
        'RedKihunterShaftBottom': Door('RedKihunterShaftBottom', 0x0, 'yellow'),
        'WastelandLeft': Door('WastelandLeft', 0x0, 'green'),
        # Maridia
        'MainStreetBottomRight': Door('MainStreetBottomRight', 0x0, 'red'),
        'FishTankRight': Door('FishTankRight', 0x0, 'red'),
        'CrabShaftRight': Door('CrabShaftRight', 0x0, 'green'),
        'ColosseumBottomRight': Door('ColosseumBottomRight', 0x0, 'green'),
        'PlasmaSparkBottom': Door('PlasmaSparkBottom', 0x0, 'green'),
        'OasisTop': Door('OasisTop', 0x0, 'green'),
    }

    def setSMBM(self, smbm):
        self.smbm = smbm

    # call from logic
    def traverse(self, doorName):
        return DoorsManager.doors[doorName].traverse(self.smbm)

    def setDoorsColor(self):
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

    def randomize(self):
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
