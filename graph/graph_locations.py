from logic.helpers import Bosses
from utils.parameters import Settings, infinity
from rom.rom_patches import RomPatches
from logic.smbool import SMBool
import copy

class Location:
    graph_slots = (
        'distance', 'accessPoint', 'difficulty', 'path',
        'pathDifficulty', 'locDifficulty' )
    
    rando_slots = (
        'restricted', )

    solver_slots = (
        'itemName', 'comeBack', 'areaWeight' )

    __slots__ = graph_slots + rando_slots + solver_slots

    def __init__(
            self, distance=None, accessPoint=None,
            difficulty=None, path=None, pathDifficulty=None,
            locDifficulty=None, restricted=None, itemName=None,
            itemType=None, comeBack=None, areaWeight=None):
        self.distance = distance
        self.accessPoint = accessPoint
        self.difficulty = difficulty
        self.path = path
        self.pathDifficulty = pathDifficulty
        self.locDifficulty = locDifficulty
        self.restricted = restricted
        self.itemName = itemName
        self.itemType = itemType
        self.comeBack = comeBack
        self.areaWeight = areaWeight

    def isMajor(self):
        return self._isMajor

    def isChozo(self):
        return self._isChozo

    def isMinor(self):
        return self._isMinor

    def isBoss(self):
        return self._isBoss

    def isClass(self, _class):
        return _class in self.Class

    def evalPostAvailable(self, smbm):
        if self.difficulty.bool == True and self.PostAvailable is not None:
            smbm.addItem(self.itemName)
            postAvailable = self.PostAvailable(smbm)
            smbm.removeItem(self.itemName)

            self.difficulty = self.difficulty & postAvailable

    def evalComeBack(self, smbm, areaGraph, ap):
        if self.difficulty.bool == True:
            # check if we can come back to given ap from the location
            self.comeBack = areaGraph.canAccess(smbm, self.accessPoint, ap, infinity, self.itemName)

    def json(self):
        # to return after plando rando
        ret = {'Name': self.Name, 'accessPoint': self.accessPoint}
        if self.difficulty is not None:
            ret['difficulty'] = self.difficulty.json()
        return ret

    def __repr__(self):
        return "Location({}: {})".format(self.Name,
            '. '.join(
                (repr(getattr(self, slot)) for slot in Location.__slots__)))

    def __copy__(self):
        d = self.difficulty
        difficulty = copy.copy(d) if d is not None else None
        ret = type(self)(
            self.distance, self.accessPoint, difficulty, self.path,
            self.pathDifficulty, self.locDifficulty, self.restricted,
            self.itemName, self.itemType, self.comeBack,
            self.areaWeight)

        return ret

def define_location(
        Area, GraphArea, SolveArea, Name, Class, CanHidden, Address, Id,
        Visibility, Room, AccessFrom, Available, PostAvailable=None):
    name = Name.replace(' ', '').replace(',', '') + 'Location'
    subclass = type(name, (Location,), {
        'Area': Area,
        'GraphArea': GraphArea,
        'SolveArea': SolveArea,
        'Name': Name,
        'Class': Class,
        'CanHidden': CanHidden,
        'Address': Address,
        'Id': Id,
        'Visibility': Visibility,
        'Room': Room,
        'AccessFrom': AccessFrom,
        'Available': Available,
        'PostAvailable': PostAvailable,
        '_isMajor': 'Major' in Class,
        '_isChozo': 'Chozo' in Class,
        '_isMinor': 'Minor' in Class,
        '_isBoss': 'Boss' in Class
    })
    return subclass()

# all the items locations with the prerequisites to access them
locations = [
###### MAJORS
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Gauntlet",
    Name="Energy Tank, Gauntlet",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78264,
    Id=0x5,
    Visibility="Visible",
    Room='Gauntlet Energy Tank Room',
    AccessFrom={
        'Landing Site': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wor(sm.canEnterAndLeaveGauntlet(),
                                   sm.wand(sm.canShortCharge(),
                                           sm.canEnterAndLeaveGauntletQty(1, 0)), # thanks ponk! https://youtu.be/jil5zTBCF1s
                                   sm.canDoLowGauntlet())
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Bombs",
    Name="Bomb",
    Address=0x78404,
    Id=0x7,
    Class=["Major", "Chozo"],
    CanHidden=False,
    Visibility="Chozo",
    Room='Bomb Torizo Room',
    AccessFrom={
        'Landing Site': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.haveItem('Morph'),
                                      sm.traverse('FlywayRight')),
    PostAvailable=lambda loc, sm: sm.wor(sm.knowsAlcatrazEscape(),
                                         sm.canPassBombPassages())
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Terminator",
    Name="Energy Tank, Terminator",
    Class=["Major"],
    CanHidden=False,
    Address=0x78432,
    Id=0x8,
    Visibility="Visible",
    Room='Terminator Room',
    AccessFrom={
        'Landing Site': lambda sm: sm.canPassTerminatorBombWall(),
        'Lower Mushrooms Left': lambda sm: sm.canPassCrateriaGreenPirates(),
        'Gauntlet Top': lambda sm: sm.haveItem('Morph')
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Reserve Tank, Brinstar",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x7852C,
    Id=0x11,
    Visibility="Chozo",
    Room='Brinstar Reserve Tank Room',
    AccessFrom={
        'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
    },
    Available=lambda loc, sm: sm.wand(sm.wor(sm.canMockball(),
                                             sm.haveItem('SpeedBooster')),
                                      sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('EarlySupersRight')))
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Charge Beam",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78614,
    Id=0x17,
    Visibility="Chozo",
    Room='Big Pink',
    AccessFrom={
        'Big Pink': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canPassBombPassages()
),
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Morphing Ball",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x786DE,
    Id=0x1a,
    Visibility="Visible",
    Room='Morph Ball Room',
    AccessFrom={
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Energy Tank, Brinstar Ceiling",
    Class=["Major"],
    CanHidden=False,
    Address=0x7879E,
    Id=0x1d,
    Visibility="Hidden",
    Room='Blue Brinstar Energy Tank Room',
    AccessFrom={
        'Blue Brinstar Elevator Bottom': lambda sm: sm.wor(RomPatches.has(RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight'))
    },
    # EXPLAINED: to get this major item the different technics are:
    #  -can fly (continuous bomb jump or space jump)
    #  -have the high jump boots
    #  -freeze the Reo to jump on it
    #  -do a damage boost with one of the two Geemers
    Available=lambda loc, sm: sm.wor(sm.knowsCeilingDBoost(),
                                   sm.canFly(),
                                   sm.wor(sm.haveItem('HiJump'),
                                          sm.haveItem('Ice'),
                                          sm.wand(sm.canUsePowerBombs(),
                                                  sm.haveItem('SpeedBooster')),
                                          sm.canSimpleShortCharge()))
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Energy Tank, Etecoons",
    Class=["Major"],
    CanHidden=True,
    Address=0x787C2,
    Id=0x1e,
    Visibility="Visible",
    Room='Etecoon Energy Tank Room',
    AccessFrom={
        'Etecoons Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Energy Tank, Waterway",
    Class=["Major"],
    CanHidden=True,
    Address=0x787FA,
    Id=0x21,
    Visibility="Visible",
    Room='Waterway Energy Tank Room',
    AccessFrom={
        'Big Pink': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canUsePowerBombs(),
                                      sm.traverse('BigPinkBottomLeft'),
                                      sm.haveItem('SpeedBooster'),
                                      sm.wor(sm.haveItem('Gravity'),
                                             sm.canSimpleShortCharge())) # from the blocks above the water
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Energy Tank, Brinstar Gate",
    Class=["Major"],
    CanHidden=True,
    Address=0x78824,
    Id=0x23,
    Visibility="Visible",
    Room='Hopper Energy Tank Room',
    AccessFrom={
        'Big Pink': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('BigPinkRight'),
                                      sm.wor(sm.haveItem('Wave'),
                                             sm.wand(sm.haveItem('Super'),
                                                     sm.haveItem('HiJump'),
                                                     sm.knowsReverseGateGlitch()),
                                             sm.wand(sm.haveItem('Super'),
                                                     sm.knowsReverseGateGlitchHiJumpLess())))
),
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar",
    Name="X-Ray Scope",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78876,
    Id=0x26,
    Visibility="Chozo",
    Room='X-Ray Scope Room',
    AccessFrom={
        'Red Tower Top Left': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canUsePowerBombs(),
                                      sm.traverse('RedTowerLeft'),
                                      sm.traverse('RedBrinstarFirefleaLeft'),
                                      sm.wor(sm.haveItem('Grapple'),
                                             sm.haveItem('SpaceJump'),
                                             sm.wand(sm.energyReserveCountOkHardRoom('X-Ray'),
                                                     sm.wor(sm.knowsXrayDboost(),
                                                            sm.wand(sm.haveItem('Ice'),
                                                                    sm.wor(sm.haveItem('HiJump'), sm.knowsXrayIce())),
                                                            sm.canInfiniteBombJump(),
                                                            sm.wand(sm.haveItem('HiJump'),
                                                                    sm.wor(sm.haveItem('SpeedBooster'),
                                                                           sm.canSpringBallJump()))))))
),
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar",
    Name="Spazer",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x7896E,
    Id=0x2a,
    Visibility="Chozo",
    Room='Spazer Room',
    AccessFrom={
        'East Tunnel Right': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('BelowSpazerTopRight'),
                                      sm.wor(sm.canPassBombPassages(),
                                             sm.wand(sm.haveItem('Morph'),
                                                     RomPatches.has(RomPatches.SpazerShotBlock))))
),
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid",
    Name="Energy Tank, Kraid",
    Class=["Major"],
    CanHidden=False,
    Address=0x7899C,
    Id=0x2b,
    Visibility="Hidden",
    Room='Warehouse Energy Tank Room',
    AccessFrom={
        'Warehouse Zeela Room Left': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: Bosses.bossDead(sm, 'Kraid')
),
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid Boss",
    Name="Kraid",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B055,
    Id=None,
    Visibility="Hidden",
    Room='Kraid Room',
    AccessFrom={
        'KraidRoomIn': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.enoughStuffsKraid()
),
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid Boss",
    Name="Varia Suit",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78ACA,
    Id=0x30,
    Visibility="Chozo",
    Room='Varia Suit Room',
    AccessFrom={
        'KraidRoomIn': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: Bosses.bossDead(sm, 'Kraid')
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Ice",
    Name="Ice Beam",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78B24,
    Id=0x32,
    Visibility="Chozo",
    Room='Ice Beam Room',
    AccessFrom={
        'Business Center': lambda sm: sm.traverse('BusinessCenterTopLeft')
    },
    Available=lambda loc, sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Ice Beam']),
                                      sm.wor(sm.canPassBombPassages(), # to exit, or if you fail entrance
                                             sm.wand(sm.haveItem('Ice'), # harder strat
                                                     sm.haveItem('Morph'),
                                                     sm.knowsIceEscape())),
                                      sm.wor(sm.wand(sm.haveItem('Morph'),
                                                     sm.knowsMockball()),
                                             sm.haveItem('SpeedBooster')))
),
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Energy Tank, Crocomire",
    Class=["Major"],
    CanHidden=True,
    Address=0x78BA4,
    Id=0x34,
    Visibility="Visible",
    Room="Crocomire's Room",
    AccessFrom={
        'Crocomire Room Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.enoughStuffCroc(),
                                    sm.wor(sm.haveItem('Grapple'),
                                           sm.haveItem('SpaceJump'),
                                           sm.energyReserveCountOk(3/sm.getDmgReduction()[0])))
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Hi-Jump Boots",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78BAC,
    Id=0x35,
    Visibility="Chozo",
    Room='Hi Jump Boots Room',
    AccessFrom={
        'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
    },
    Available=lambda loc, sm: sm.haveItem('Morph'),
    PostAvailable=lambda loc, sm: sm.wor(sm.canPassBombPassages(),
                                       sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.HiJumpShotBlock)))
),
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Grapple Beam",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78C36,
    Id=0x3c,
    Visibility="Chozo",
    Room='Grapple Beam Room',
    AccessFrom={
        'Crocomire Room Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.enoughStuffCroc(),
                                      sm.wor(sm.wand(sm.haveItem('Morph'),
                                                     sm.canFly()),
                                             sm.wand(sm.haveItem('SpeedBooster'),
                                                     sm.wor(sm.knowsShortCharge(),
                                                            sm.canUsePowerBombs())),
                                             sm.wand(sm.haveItem('Morph'),
                                                     sm.wor(sm.haveItem('SpeedBooster'),
                                                            sm.canSpringBallJump()),
                                                     sm.haveItem('HiJump')), # jump from the yellow plateform ennemy
                                             sm.canGreenGateGlitch()))
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Reserve",
    Name="Reserve Tank, Norfair",
    Class=["Major"],
    CanHidden=False,
    Address=0x78C3E,
    Id=0x3d,
    Visibility="Chozo",
    Room='Norfair Reserve Tank Room',
    AccessFrom={
        'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
        'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop(),
    },
    Available=lambda loc, sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Speed",
    Name="Speed Booster",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78C82,
    Id=0x42,
    Visibility="Chozo",
    Room='Speed Booster Room',
    AccessFrom={
        'Bubble Mountain Top': lambda sm: sm.wor(RomPatches.has(RomPatches.SpeedAreaBlueDoors),
                                                 sm.wand(sm.traverse('BubbleMountainTopRight'),
                                                         sm.traverse('SpeedBoosterHallRight')))
    },
    Available=lambda loc, sm: sm.canHellRunToSpeedBooster()
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Wave",
    Name="Wave Beam",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78CCA,
    Id=0x44,
    Visibility="Chozo",
    Room='Wave Beam Room',
    AccessFrom={
        'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
    },
    Available=lambda loc, sm: sm.traverse('DoubleChamberRight'),
    PostAvailable=lambda loc, sm: sm.wor(sm.haveItem('Morph'), # exit through lower passage under the spikes
                                         sm.wand(sm.wor(sm.haveItem('SpaceJump'), # exit through blue gate
                                                        sm.haveItem('Grapple')),
                                                 sm.wor(sm.wand(sm.canBlueGateGlitch(), sm.heatProof()), # hell run + green gate glitch is too much
                                                        sm.haveItem('Wave'))))
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Ridley Boss",
    Name="Ridley",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B056,
    Id=None,
    Visibility="Hidden",
    Room="Ridley's Room",
    AccessFrom={
        'RidleyRoomIn': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']), sm.enoughStuffsRidley())
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Ridley Boss",
    Name="Energy Tank, Ridley",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x79108,
    Id=0x4e,
    Visibility="Hidden",
    Room='Ridley Tank Room',
    AccessFrom={
        'RidleyRoomIn': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.haveItem('Ridley')
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Screw Attack",
    Name="Screw Attack",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x79110,
    Id=0x4f,
    Visibility="Chozo",
    Room='Screw Attack Room',
    # everything is handled by the graph
    AccessFrom={
        'Screw Attack Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True),
    # we still put post available for easier super fun checks
    PostAvailable=lambda loc, sm: sm.canExitScrewAttackArea()
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Energy Tank, Firefleas",
    Class=["Major"],
    CanHidden=True,
    Address=0x79184,
    Id=0x50,
    Visibility="Visible",
    Room='Lower Norfair Fireflea Room',
    AccessFrom={
        'Firefleas': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wor(RomPatches.has(RomPatches.FirefleasRemoveFune),
                                     # get past the fune
                                     sm.haveItem('Super'),
                                     sm.canPassBombPassages(),
                                     sm.canUseSpringBall()),
    PostAvailable=lambda loc, sm: sm.wor(sm.knowsFirefleasWalljump(),
                                       sm.wor(sm.haveItem('Ice'),
                                              sm.haveItem('HiJump'),
                                              sm.canFly(),
                                              sm.canSpringBallJump()))
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Gravity",
    Name="Reserve Tank, Wrecked Ship",
    Class=["Major"],
    CanHidden=False,
    Address=0x7C2E9,
    Id=0x81,
    Visibility="Chozo",
    Room='Bowling Alley',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.haveItem('SpeedBooster'),
                                    sm.canPassBowling())
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Back",
    Name="Energy Tank, Wrecked Ship",
    Class=["Major", "Chozo"],
    CanHidden=True,
    Address=0x7C337,
    Id=0x84,
    Visibility="Visible",
    Room='Wrecked Ship Energy Tank Room',
    AccessFrom={
        'Wrecked Ship Back': lambda sm: sm.wor(RomPatches.has(RomPatches.WsEtankBlueDoor),
                                               sm.traverse('ElectricDeathRoomTopLeft'))
    },
    Available=lambda loc, sm: sm.wor(Bosses.bossDead(sm, 'Phantoon'),
                                     RomPatches.has(RomPatches.WsEtankPhantoonAlive))
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="Phantoon Boss",
    Name="Phantoon",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B057,
    Id=None,
    Visibility="Hidden",
    Room="Phantoon's Room",
    AccessFrom={
        'PhantoonRoomIn': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.enoughStuffsPhantoon()
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Main",
    Name="Right Super, Wrecked Ship",
    Class=["Major", "Chozo"],
    CanHidden=True,
    Address=0x7C365,
    Id=0x86,
    Visibility="Visible",
    Room='Wrecked Ship East Super Room',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: Bosses.bossDead(sm, 'Phantoon')
    },
    Available=lambda loc, sm: sm.canPassBombPassages()
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Gravity",
    Name="Gravity Suit",
    Class=["Major"],
    CanHidden=False,
    Address=0x7C36D,
    Id=0x87,
    Visibility="Chozo",
    Room='Gravity Suit Room',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canPassBombPassages(),
                                    sm.canPassBowling())
),
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Energy Tank, Mama turtle",
    Class=["Major"],
    CanHidden=True,
    Address=0x7C47D,
    Id=0x8a,
    Visibility="Visible",
    Room='Mama Turtle Room',
    AccessFrom={
        'Main Street Bottom': lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'), sm.canDoSuitlessOuterMaridia()),
                                                 sm.wor(sm.traverse('FishTankRight'),
                                                        RomPatches.has(RomPatches.MamaTurtleBlueDoor)),
                                                 sm.wor(sm.wor(sm.canFly(),
                                                               sm.wand(sm.haveItem('Gravity'),
                                                                       sm.haveItem('SpeedBooster')),
                                                               sm.wand(sm.haveItem('HiJump'),
                                                                       sm.haveItem('SpeedBooster'),
                                                                       sm.knowsHiJumpMamaTurtle())),
                                                        sm.wor(sm.wand(sm.canUseSpringBall(),
                                                                       sm.wor(sm.wand(sm.haveItem('HiJump'),
                                                                                      sm.knowsSpringBallJump()),
                                                                              sm.knowsSpringBallJumpFromWall())),
                                                               sm.haveItem('Grapple')))),
        'Mama Turtle': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Forgotten Highway",
    Name="Plasma Beam",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x7C559,
    Id=0x8f,
    Visibility="Chozo",
    Room='Plasma Room',
    AccessFrom={
        'Toilet Top': lambda sm: SMBool(True)
    },
    # DONE: to leave the Plasma Beam room you have to kill the space pirates and return to the door
    # to unlock the door:
    #  -kill draygon
    # to kill the space pirates:
    #  -do short charges with speedbooster
    #  -use pseudo screw
    #  -have screw attack
    #  -have plasma beam
    # to go back to the door:
    #  -have high jump boots
    #  -can fly (space jump or infinite bomb jump)
    #  -use short charge with speedbooster
    Available=lambda loc, sm: Bosses.bossDead(sm, 'Draygon'),
    PostAvailable=lambda loc, sm: sm.wand(sm.wor(sm.wand(sm.canShortCharge(),
                                                       sm.knowsKillPlasmaPiratesWithSpark()),
                                               sm.wand(sm.canFireChargedShots(),
                                                       sm.knowsKillPlasmaPiratesWithCharge(),
                                                       # 160/80/40 dmg * 4 ground plasma pirates
                                                       # => 640/320/160 damage take required
                                                       # check below is 1099/599/299 (give margin for taking dmg a bit)
                                                       # (* 4 for nerfed charge, since you need to take hits 4 times instead of one)
                                                       sm.energyReserveCountOk(int(10.0 * sm.getPiratesPseudoScrewCoeff()/sm.getDmgReduction(False)[0]))),
                                               sm.haveItem('ScrewAttack'),
                                               sm.haveItem('Plasma')),
                                        sm.wor(sm.canFly(),
                                               sm.wand(sm.haveItem('HiJump'),
                                                       sm.knowsGetAroundWallJump()),
                                               sm.canShortCharge(),
                                               sm.wand(sm.canSpringBallJump(),
                                                       sm.knowsSpringBallJumpFromWall())))
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Left Sandpit",
    Name="Reserve Tank, Maridia",
    Class=["Major"],
    CanHidden=False,
    Address=0x7C5E3,
    Id=0x91,
    Visibility="Chozo",
    Room='West Sand Hole',
    AccessFrom={
        'Left Sandpit': lambda sm: sm.canClimbWestSandHole()
    },
    Available=lambda loc, sm: sm.canAccessItemsInWestSandHole()
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Sandpits",
    Name="Spring Ball",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x7C6E5,
    Id=0x96,
    Visibility="Chozo",
    Room='Spring Ball Room',
    AccessFrom={
        'Oasis Bottom': lambda sm: sm.canTraverseSandPits()
    },
    Available=lambda loc, sm: sm.wand(sm.canUsePowerBombs(), # in Shaktool room to let Shaktool access the sand blocks
                                    sm.wor(sm.wand(sm.haveItem('Ice'), # puyo clip
                                                   sm.wor(sm.wand(sm.haveItem('Gravity'),
                                                                  sm.knowsPuyoClip()),
                                                          sm.wand(sm.haveItem('Gravity'),
                                                                  sm.haveItem('XRayScope'),
                                                                  sm.knowsPuyoClipXRay()),
                                                          sm.knowsSuitlessPuyoClip())),
                                           sm.wand(sm.haveItem('Grapple'), # go through grapple block
                                                   sm.wor(sm.wand(sm.haveItem('Gravity'),
                                                                  sm.wor(sm.wor(sm.wand(sm.haveItem('HiJump'), sm.knowsAccessSpringBallWithHiJump()),
                                                                                sm.haveItem('SpaceJump')),
                                                                         sm.knowsAccessSpringBallWithGravJump(),
                                                                         sm.wand(sm.haveItem('Bomb'),
                                                                                 sm.wor(sm.knowsAccessSpringBallWithBombJumps(),
                                                                                        sm.wand(sm.haveItem('SpringBall'),
                                                                                                sm.knowsAccessSpringBallWithSpringBallBombJumps()))),
                                                                         sm.wand(sm.haveItem('SpringBall'), sm.knowsAccessSpringBallWithSpringBallJump()))),
                                                          sm.wand(sm.haveItem('SpaceJump'), sm.knowsAccessSpringBallWithFlatley()))),
                                           sm.wand(sm.haveItem('XRayScope'), sm.knowsAccessSpringBallWithXRayClimb()), # XRay climb
                                           sm.canCrystalFlashClip()),
                                    sm.wor(sm.haveItem('Gravity'), sm.canUseSpringBall())), # acess the item in spring ball room
    PostAvailable=lambda loc, sm: sm.wor(sm.wand(sm.haveItem('Gravity'),
                                               sm.wor(sm.haveItem('HiJump'),
                                                      sm.canFly(),
                                                      sm.knowsMaridiaWallJumps())),
                                       sm.canSpringBallJump())
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Top",
    Name="Energy Tank, Botwoon",
    Class=["Major"],
    CanHidden=True,
    Address=0x7C755,
    Id=0x98,
    Visibility="Visible",
    Room='Botwoon Energy Tank Room',
    AccessFrom={
        'Post Botwoon': lambda sm: sm.canJumpUnderwater()
    },
    Available=lambda loc, sm: sm.haveItem('Morph')
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Draygon Boss",
    Name="Draygon",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B058,
    Id=None,
    Visibility="Hidden",
    Room="Draygon's Room",
    AccessFrom={
        'Draygon Room Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Draygon Boss",
    Name="Space Jump",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x7C7A7,
    Id=0x9a,
    Visibility="Chozo",
    Room='Space Jump Room',
    AccessFrom={        
        'Draygon Room Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True),
    # put dray dead condition in post available to make it a comeback check and allow
    # rando to put stuff there to get out
    PostAvailable=lambda loc, sm: Bosses.bossDead(sm, 'Draygon')
),
define_location(
    Area="Tourian",
    GraphArea="Tourian",
    SolveArea="Tourian",
    Name="Mother Brain",
    Class=["Boss"],
    Address=0xB055B059,
    Id=None,
    Visibility="Hidden",
    CanHidden=False,
    Room='Mother Brain Room',
    AccessFrom={
        'Golden Four': lambda sm: Bosses.allBossesDead(sm)
    },
    Available=lambda loc, sm: sm.enoughStuffTourian(),
),
###### MINORS
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Power Bomb (Crateria surface)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x781CC,
    Id=0x0,
    Visibility="Visible",
    Room='Crateria Power Bomb Room',
    AccessFrom={
        'Landing Site': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('LandingSiteTopRight'),
                                      sm.wor(sm.haveItem('SpeedBooster'),
                                             sm.canFly()))
),
define_location(
    Area="Crateria",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Bottom",
    Name="Missile (outside Wrecked Ship bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x781E8,
    Id=0x1,
    Visibility="Visible",
    Room='West Ocean',
    AccessFrom={
        'West Ocean Left': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.haveItem('Morph'),
    PostAvailable=lambda loc, sm: sm.canPassBombPassages()
),
define_location(
    Area="Crateria",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Top",
    Name="Missile (outside Wrecked Ship top)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x781EE,
    Id=0x2,
    Visibility="Hidden",
    Room='West Ocean',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: Bosses.bossDead(sm, 'Phantoon')
),
define_location(
    Area="Crateria",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Top",
    Name="Missile (outside Wrecked Ship middle)",
    CanHidden=True,
    Class=["Minor"],
    Address=0x781F4,
    Id=0x3,
    Visibility="Visible",
    Room='West Ocean',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.haveItem('Super'), sm.haveItem('Morph'), Bosses.bossDead(sm, 'Phantoon'))
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Missile (Crateria moat)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78248,
    Id=0x4,
    Visibility="Visible",
    Room='The Moat',
    AccessFrom={
        'Keyhunter Room Bottom': lambda sm: sm.traverse('KihunterRight'),
        'Moat Right': lambda sm: sm.canPassMoatReverse()
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Missile (Crateria bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x783EE,
    Id=0x6,
    Visibility="Visible",
    Room='Pit Room',
    AccessFrom={
        'Landing Site': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wor(sm.canDestroyBombWalls(),
                                   sm.wand(sm.haveItem('SpeedBooster'),
                                           sm.knowsOldMBWithSpeed()))
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Gauntlet",
    Name="Missile (Crateria gauntlet right)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78464,
    Id=0x9,
    Visibility="Visible",
    Room='Green Pirates Shaft',
    AccessFrom={
        'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                                  sm.canPassBombPassages()),
                                          sm.canDoLowGauntlet()),
        'Gauntlet Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Gauntlet",
    Name="Missile (Crateria gauntlet left)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7846A,
    Id=0xa,
    Visibility="Visible",
    Room='Green Pirates Shaft',
    AccessFrom={
        'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                                  sm.canPassBombPassages()),
                                          sm.canDoLowGauntlet()),
        'Gauntlet Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Super Missile (Crateria)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78478,
    Id=0xb,
    Visibility="Visible",
    Room='Crateria Super Room',
    AccessFrom={
        'Landing Site': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canPassBombPassages(),
                                      sm.traverse("ClimbRight"),
                                      sm.haveItem('SpeedBooster'),
                                      # reserves are hard to trigger midspark when not having ETanks
                                      sm.wor(sm.wand(sm.energyReserveCountOk(2), sm.itemCountOk('ETank', 1)), # need energy to get out
                                             sm.wand(sm.itemCountOk('ETank', 1),
                                                     sm.wor(sm.haveItem('Grapple'), # use grapple/space or dmg protection to get out
                                                            sm.haveItem('SpaceJump'),
                                                            sm.heatProof()))),
                                      sm.wor(sm.haveItem('Ice'),
                                             sm.wand(sm.canSimpleShortCharge(), sm.canUsePowerBombs()))) # there's also a dboost involved in simple short charge or you have to kill the yellow enemies with some power bombs
),
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Missile (Crateria middle)",
    Class=["Minor", "Chozo"],
    CanHidden=True,
    Address=0x78486,
    Id=0xc,
    Visibility="Visible",
    Room='The Final Missile',
    AccessFrom={
        'Landing Site': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canPassBombPassages()
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Power Bomb (green Brinstar bottom)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x784AC,
    Id=0xd,
    Visibility="Chozo",
    Room='Green Brinstar Main Shaft',
    AccessFrom={
        'Etecoons Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.haveItem('Morph'),
                                      sm.wor(sm.haveMissileOrSuper(), sm.canUsePowerBombs(), sm.haveItem('ScrewAttack'))) # beetoms
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Super Missile (pink Brinstar)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x784E4,
    Id=0xe,
    Visibility="Chozo",
    Room='Spore Spawn Super Room',
    AccessFrom={
        'Big Pink': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wor(sm.wand(sm.traverse('BigPinkTopRight'),
                                             sm.enoughStuffSporeSpawn()),
                                     # back way into spore spawn
                                     sm.wand(sm.canOpenGreenDoors(),
                                             sm.canPassBombPassages())),
    PostAvailable=lambda loc, sm: sm.wand(sm.canOpenGreenDoors(),
                                          sm.canPassBombPassages())
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Missile (green Brinstar below super missile)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78518,
    Id=0xf,
    Visibility="Visible",
    Room='Early Supers Room',
    AccessFrom={
        'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
    },
    Available=lambda loc, sm: SMBool(True),
    PostAvailable=lambda loc, sm: sm.wor(RomPatches.has(RomPatches.EarlySupersShotBlock), sm.canPassBombPassages())
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Super Missile (green Brinstar top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7851E,
    Id=0x10,
    Visibility="Visible",
    Room='Early Supers Room',
    AccessFrom={
        'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
    },
    Available=lambda loc, sm: sm.wor(sm.canMockball(),
                                     sm.haveItem('SpeedBooster'))
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Missile (green Brinstar behind missile)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78532,
    Id=0x12,
    Visibility="Hidden",
    Room='Brinstar Reserve Tank Room',
    AccessFrom={
        'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
    },
    Available=lambda loc, sm: sm.wand(sm.haveItem('Morph'),
                                      sm.wor(sm.canMockball(),
                                             sm.haveItem('SpeedBooster')),
                                      sm.traverse('EarlySupersRight'),
                                      sm.wor(sm.canPassBombPassages(),
                                             sm.wand(sm.knowsRonPopeilScrew(),
                                                     sm.haveItem('ScrewAttack'))))
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Missile (green Brinstar behind reserve tank)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78538,
    Id=0x13,
    Visibility="Visible",
    Room='Brinstar Reserve Tank Room',
    AccessFrom={
        'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('EarlySupersRight'),
                                      sm.haveItem('Morph'),
                                      sm.wor(sm.canMockball(),
                                             sm.haveItem('SpeedBooster')))
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Missile (pink Brinstar top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78608,
    Id=0x15,
    Visibility="Visible",
    Room='Big Pink',
    AccessFrom={
        'Big Pink': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Missile (pink Brinstar bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7860E,
    Id=0x16,
    Visibility="Visible",
    Room='Big Pink',
    AccessFrom={
        'Big Pink': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Power Bomb (pink Brinstar)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7865C,
    Id=0x18,
    Visibility="Visible",
    Room='Pink Brinstar Power Bomb Room',
    AccessFrom={
        'Big Pink': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canUsePowerBombs(),
                                    sm.haveItem('Super'))
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Brinstar Hills",
    Name="Missile (green Brinstar pipe)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78676,
    Id=0x19,
    Visibility="Visible",
    Room='Green Hill Zone',
    AccessFrom={
        'Green Hill Zone Top Right': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.haveItem('Morph')
),
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Power Bomb (blue Brinstar)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7874C,
    Id=0x1b,
    Visibility="Visible",
    Room='Morph Ball Room',
    AccessFrom={
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canUsePowerBombs()
),
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar middle)",
    Address=0x78798,
    Id=0x1c,
    Class=["Minor"],
    CanHidden=True,
    Visibility="Visible",
    Room='Blue Brinstar Energy Tank Room',
    AccessFrom={
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.wor(RomPatches.has(RomPatches.BlueBrinstarMissile), sm.haveItem('Morph')),
                                      sm.wor(RomPatches.has(RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight')))
),
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Super Missile (green Brinstar bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x787D0,
    Id=0x1f,
    Visibility="Visible",
    Room='Etecoon Super Room',
    AccessFrom={
        'Etecoons Supers': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar bottom)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x78802,
    Id=0x22,
    Visibility="Chozo",
    Room='First Missile Room',
    AccessFrom={
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.haveItem('Morph')
),
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78836,
    Id=0x24,
    Visibility="Visible",
    Room='Billy Mays Room',
    AccessFrom={
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canAccessBillyMays()
),
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar behind missile)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7883C,
    Id=0x25,
    Visibility="Hidden",
    Room='Billy Mays Room',
    AccessFrom={
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canAccessBillyMays()
),
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar Top",
    Name="Power Bomb (red Brinstar sidehopper room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x788CA,
    Id=0x27,
    Visibility="Visible",
    Room='Beta Power Bomb Room',
    AccessFrom={
        'Red Brinstar Elevator': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('RedTowerElevatorTopLeft'),
                                      sm.canUsePowerBombs())
),
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar Top",
    Name="Power Bomb (red Brinstar spike room)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x7890E,
    Id=0x28,
    Visibility="Chozo",
    Room='Alpha Power Bomb Room',
    AccessFrom={
        'Red Brinstar Elevator': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.traverse('RedTowerElevatorBottomLeft')
),
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar Top",
    Name="Missile (red Brinstar spike room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78914,
    Id=0x29,
    Visibility="Visible",
    Room='Alpha Power Bomb Room',
    AccessFrom={
        'Red Brinstar Elevator': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('RedTowerElevatorBottomLeft'),
                                      sm.canUsePowerBombs())
),
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid",
    Name="Missile (Kraid)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x789EC,
    Id=0x2c,
    Visibility="Hidden",
    Room='Warehouse Keyhunter Room',
    AccessFrom={
        'Warehouse Zeela Room Left': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canUsePowerBombs()
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Missile (lava room)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78AE4,
    Id=0x31,
    Visibility="Hidden",
    Room='Cathedral',
    AccessFrom={
        'Cathedral': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.haveItem('Morph')
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Ice",
    Name="Missile (below Ice Beam)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78B46,
    Id=0x33,
    Visibility="Hidden",
    Room='Crumble Shaft',
    AccessFrom={
        'Business Center': lambda sm: sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                              sm.canUsePowerBombs(),
                                              sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Ice Beam']),
                                              sm.wor(sm.wand(sm.haveItem('Morph'),
                                                             sm.knowsMockball()),
                                                     sm.haveItem('SpeedBooster'))),
        'Crocomire Speedway Bottom': lambda sm: sm.wand(sm.isVanillaCroc(),
                                                        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Ice Missiles']),
                                                        sm.haveItem('SpeedBooster'),
                                                        sm.knowsIceMissileFromCroc())
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Grapple Escape",
    Name="Missile (above Crocomire)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78BC0,
    Id=0x36,
    Visibility="Visible",
    Room='Crocomire Escape',
    AccessFrom={
        'Crocomire Speedway Bottom': lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Grapple Escape Missiles'])
    },
    Available=lambda loc, sm: sm.canGrappleEscape()
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Missile (Hi-Jump Boots)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78BE6,
    Id=0x37,
    Visibility="Visible",
    Room='Hi Jump Energy Tank Room',
    AccessFrom={
        'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
    },
    Available=lambda loc, sm: sm.haveItem('Morph'),
    PostAvailable=lambda loc, sm: sm.wor(sm.canPassBombPassages(),
                                       sm.wand(RomPatches.has(RomPatches.HiJumpShotBlock), sm.haveItem('Morph')))
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Energy Tank (Hi-Jump Boots)",
    CanHidden=True,
    Class=["Minor"],
    Address=0x78BEC,
    Id=0x38,
    Visibility="Visible",
    Room='Hi Jump Energy Tank Room',
    AccessFrom={
        'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Power Bomb (Crocomire)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C04,
    Id=0x39,
    Visibility="Visible",
    Room='Post Crocomire Power Bomb Room',
    AccessFrom={
        'Crocomire Room Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('PostCrocomireUpperLeft'),
                                      sm.enoughStuffCroc(),
                                      sm.wor(sm.wor(sm.canFly(),
                                                    sm.haveItem('Grapple'),
                                                    sm.wand(sm.haveItem('SpeedBooster'),
                                                            sm.wor(sm.heatProof(),
                                                                   sm.energyReserveCountOk(1)))), # spark from the room before
                                             sm.wor(sm.haveItem('HiJump'), # run and jump from yellow platform
                                                    sm.wand(sm.haveItem('Ice'),
                                                            sm.knowsCrocPBsIce()),
                                                    sm.knowsCrocPBsDBoost())))
),
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Missile (below Crocomire)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C14,
    Id=0x3a,
    Visibility="Visible",
    Room='Post Crocomire Missile Room',
    AccessFrom={
        'Crocomire Room Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.traverse('PostCrocomireShaftRight'), sm.enoughStuffCroc(), sm.haveItem('Morph'))
),
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Missile (Grapple Beam)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C2A,
    Id=0x3b,
    Visibility="Visible",
    Room='Post Crocomire Jump Room',
    AccessFrom={
        'Crocomire Room Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.enoughStuffCroc(),
                                      sm.wor(sm.wor(sm.wand(sm.haveItem('Morph'), # from below
                                                            sm.canFly()),
                                                    sm.wand(sm.haveItem('SpeedBooster'),
                                                            sm.wor(sm.knowsShortCharge(),
                                                                   sm.canUsePowerBombs()))),
                                             sm.wand(sm.canGreenGateGlitch(), # from grapple room
                                                     sm.canFly()))), # TODO::test if accessible with a spark (short charge), and how many etanks required
    PostAvailable=lambda loc, sm: sm.wor(sm.haveItem('Morph'), # normal exit
                                         sm.wand(sm.haveItem('Super'), # go back to grapple room
                                                 sm.wor(sm.haveItem('SpaceJump'),
                                                        sm.wand(sm.haveItem('SpeedBooster'), sm.haveItem('HiJump'))))) # jump from the yellow plateform ennemy
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Reserve",
    Name="Missile (Norfair Reserve Tank)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78C44,
    Id=0x3e,
    Visibility="Hidden",
    Room='Norfair Reserve Tank Room',
    AccessFrom={
        'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
        'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop()
    },
    Available=lambda loc, sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Reserve",
    Name="Missile (bubble Norfair green door)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C52,
    Id=0x3f,
    Visibility="Visible",
    Room='Green Bubbles Missile Room',
    AccessFrom={
        'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
        'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop()
    },
    Available=lambda loc, sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve Missiles'])
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Bottom",
    Name="Missile (bubble Norfair)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C66,
    Id=0x40,
    Visibility="Visible",
    Room='Bubble Mountain',
    AccessFrom={
        'Bubble Mountain': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Speed",
    Name="Missile (Speed Booster)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78C74,
    Id=0x41,
    Visibility="Hidden",
    Room='Speed Booster Hall',
    AccessFrom={
        'Bubble Mountain Top': lambda sm: sm.wor(RomPatches.has(RomPatches.SpeedAreaBlueDoors),
                                                 sm.traverse('BubbleMountainTopRight'))
    },
    Available=lambda loc, sm: sm.canHellRunToSpeedBooster()
),
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Wave",
    Name="Missile (Wave Beam)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78CBC,
    Id=0x43,
    Visibility="Visible",
    Room='Double Chamber',
    AccessFrom={
        'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Screw Attack",
    Name="Missile (Gold Torizo)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78E6E,
    Id=0x46,
    Visibility="Visible",
    Room="Golden Torizo's Room",
    AccessFrom={
        'LN Above GT': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
    PostAvailable=lambda loc, sm: sm.enoughStuffGT()
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Screw Attack",
    Name="Super Missile (Gold Torizo)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78E74,
    Id=0x47,
    Visibility="Hidden",
    Room="Golden Torizo's Room",
    AccessFrom={
        'Screw Attack Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True),
    PostAvailable=lambda loc, sm: sm.enoughStuffGT()
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Before Amphitheater",
    Name="Missile (Mickey Mouse room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78F30,
    Id=0x49,
    Visibility="Visible",
    Room='Mickey Mouse Room',
    AccessFrom={
        'LN Entrance': lambda sm: sm.wand(sm.canUsePowerBombs(), sm.canPassWorstRoom()),
    },
    Available=lambda loc, sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Missile (lower Norfair above fire flea room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78FCA,
    Id=0x4a,
    Visibility="Visible",
    Room='Lower Norfair Spring Ball Maze Room',
    AccessFrom={
        'Firefleas': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Power Bomb (lower Norfair above fire flea room)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78FD2,
    Id=0x4b,
    Visibility="Visible",
    Room='Lower Norfair Escape Power Bomb Room',
    AccessFrom={
        'Firefleas Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Power Bomb (Power Bombs of shame)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x790C0,
    Id=0x4c,
    Visibility="Visible",
    Room='Wasteland',
    AccessFrom={
        'Ridley Zone': lambda sm: sm.canUsePowerBombs()
    },
    Available=lambda loc, sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
),
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Missile (lower Norfair near Wave Beam)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x79100,
    Id=0x4d,
    Visibility="Visible",
    Room="Three Muskateers' Room",
    AccessFrom={
        'Firefleas': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                    sm.canDestroyBombWalls(),
                                    sm.haveItem('Morph'))
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Main",
    Name="Missile (Wrecked Ship middle)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C265,
    Id=0x80,
    Visibility="Visible",
    Room='Wrecked Ship Main Shaft',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.canPassBombPassages()
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Gravity",
    Name="Missile (Gravity Suit)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x7C2EF,
    Id=0x82,
    Visibility="Visible",
    Room='Bowling Alley',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.canPassBowling(),
                                    sm.canPassBombPassages())
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Top",
    Name="Missile (Wrecked Ship top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C319,
    Id=0x83,
    Visibility="Visible",
    Room='Wrecked Ship East Missile Room',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: Bosses.bossDead(sm, 'Phantoon')
),
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Main",
    Name="Super Missile (Wrecked Ship left)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C357,
    Id=0x85,
    Visibility="Visible",
    Room='Wrecked Ship West Super Room',
    AccessFrom={
        'Wrecked Ship Main': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: Bosses.bossDead(sm, 'Phantoon')
),
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Missile (green Maridia shinespark)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7C437,
    Id=0x88,
    Visibility="Visible",
    Room='Main Street',
    AccessFrom={
        'Main Street Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wand(sm.haveItem('Gravity'),
                                      sm.haveItem('SpeedBooster'),
                                      sm.wor(sm.wand(sm.wor(sm.haveItem('Super'), # run from room on the right
                                                            RomPatches.has(RomPatches.AreaRandoGatesOther)),
                                                     sm.itemCountOk('ETank', 1)), # etank for the spark since sparking from low ground
                                             sm.canSimpleShortCharge())), # run from above
),
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Super Missile (green Maridia)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C43D,
    Id=0x89,
    Visibility="Visible",
    Room='Main Street',
    AccessFrom={
        'Main Street Bottom': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                                sm.canDoSuitlessOuterMaridia())
        # we could add eas access from red fish room here, but if you miss it you can't retry
    },
    Available=lambda loc, sm: sm.haveItem('Morph')
),
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Missile (green Maridia tatori)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7C483,
    Id=0x8b,
    Visibility="Hidden",
    Room='Mama Turtle Room',
    AccessFrom={
        'Main Street Bottom': lambda sm: sm.wand(sm.wor(sm.traverse('FishTankRight'),
                                                        RomPatches.has(RomPatches.MamaTurtleBlueDoor)),
                                                 sm.wor(sm.haveItem('Gravity'),
                                                        sm.canDoSuitlessOuterMaridia())),
        'Mama Turtle': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Super Missile (yellow Maridia)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C4AF,
    Id=0x8c,
    Visibility="Visible",
    Room='Watering Hole',
    AccessFrom={
        'Watering Hole Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Missile (yellow Maridia super missile)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C4B5,
    Id=0x8d,
    Visibility="Visible",
    Room='Watering Hole',
    AccessFrom={
        'Watering Hole Bottom': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Missile (yellow Maridia false wall)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C533,
    Id=0x8e,
    Visibility="Visible",
    Room='Pseudo Plasma Spark Room',
    AccessFrom={
        'Beach': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Left Sandpit",
    Name="Missile (left Maridia sand pit room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C5DD,
    Id=0x90,
    Visibility="Visible",
    Room='West Sand Hole',
    AccessFrom={
        'Left Sandpit': lambda sm: sm.canClimbWestSandHole()
    },
    Available=lambda loc, sm: sm.canAccessItemsInWestSandHole()
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Right Sandpit",
    Name="Missile (right Maridia sand pit room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C5EB,
    Id=0x92,
    Visibility="Visible",
    Room='East Sand Hole',
    AccessFrom={
        'Right Sandpit': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: sm.wor(sm.haveItem('Gravity'),
                                   sm.wand(sm.haveItem('HiJump'),
                                           sm.knowsGravLessLevel3()))
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Right Sandpit",
    Name="Power Bomb (right Maridia sand pit room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C5F1,
    Id=0x93,
    Visibility="Visible",
    Room='East Sand Hole',
    AccessFrom={
        'Right Sandpit': lambda sm: sm.haveItem('Morph')
    },
    Available=lambda loc, sm: sm.wor(sm.haveItem('Gravity'),
                                   sm.wand(sm.knowsGravLessLevel3(),
                                           sm.haveItem('HiJump'),
                                           sm.canSpringBallJump())) # https://www.youtube.com/watch?v=7LYYxphRRT0
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Missile (pink Maridia)",
    Address=0x7C603,
    Id=0x94,
    Class=["Minor"],
    CanHidden=True,
    Visibility="Visible",
    Room='Aqueduct',
    AccessFrom={
        'Aqueduct': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Super Missile (pink Maridia)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C609,
    Id=0x95,
    Visibility="Visible",
    Room='Aqueduct',
    AccessFrom={
        'Aqueduct': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
),
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Top",
    Name="Missile (Draygon)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7C74D,
    Id=0x97,
    Visibility="Hidden",
    Room='The Precious Room',
    AccessFrom={
        'Precious Room Top': lambda sm: SMBool(True)
    },
    Available=lambda loc, sm: SMBool(True)
)
]
