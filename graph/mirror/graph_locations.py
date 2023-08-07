from graph.vanilla.graph_locations import locationsDict as vanillaLocDict
# reuse the one from vanilla which is loaded by logic
from graph.vanilla.graph_locations import LocationsHelper
from rom.addresses import Addresses
from graph.location import LocationMapAttrs, LocationMapTileKind
import copy

locationsDict = copy.deepcopy(vanillaLocDict)

# regular gate glitchs no longer available,
# but now avaible for the previously unavailable ones.
locationsDict["Energy Tank, Brinstar Gate"].Available = (
    lambda sm: sm.wand(sm.traverse('BigPinkRight'),
                       sm.wor(sm.haveItem('Wave'),
                              sm.wand(sm.haveMissileOrSuper(),
                                      sm.knowsWaveGateGlitchMirror())))
)
locationsDict["Grapple Beam"].Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.wand(sm.haveItem('Morph'),
                                      sm.canFly()),
                              sm.wand(sm.haveItem('SpeedBooster'),
                                      sm.wor(sm.knowsShortCharge(),
                                             sm.canUsePowerBombs())),
                              sm.wand(sm.haveItem('Morph'),
                                      sm.wor(sm.haveItem('SpeedBooster'),
                                             sm.canSpringBallJump()),
                                      sm.haveItem('HiJump')))) # jump from the yellow plateform ennemy
)
locationsDict["Missile (Grapple Beam)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.wor(sm.wand(sm.haveItem('Morph'), # from below
                                             sm.canFly()),
                                     sm.wand(sm.haveItem('SpeedBooster'),
                                             sm.wor(sm.knowsShortCharge(),
                                                    sm.canUsePowerBombs())))))
)

def fixLocAddresses():
    # some PLMs have been relocated in 8f freespace.
    # change Address in class and not instance so that copy use the updated address
    type(locationsDict["Energy Tank, Crocomire"]).Address = Addresses.getOne("bank_8f_Energy_Tank_Crocomire")
    type(locationsDict["Reserve Tank, Wrecked Ship"]).Address = Addresses.getOne("bank_8f_Room_C98E_Reserve")
    type(locationsDict["Missile (Gravity Suit)"]).Address = Addresses.getOne("bank_8f_Room_C98E_Missile")

locations = [loc for loc in locationsDict.values()]

type(locationsDict['Energy Tank, Gauntlet']).MapAttrs = LocationMapAttrs(45, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Bomb']).MapAttrs = LocationMapAttrs(37, 7, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Energy Tank, Terminator']).MapAttrs = LocationMapAttrs(50, 7, LocationMapTileKind.ThreeWallsOneDoorOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Reserve Tank, Brinstar']).MapAttrs = LocationMapAttrs(50, 5, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Charge Beam']).MapAttrs = LocationMapAttrs(46, 12, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Morphing Ball']).MapAttrs = LocationMapAttrs(38, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Energy Tank, Brinstar Ceiling']).MapAttrs = LocationMapAttrs(32, 11, LocationMapTileKind.TwoWallsCorridor, hFlip=True, vFlip=False)

type(locationsDict['Energy Tank, Etecoons']).MapAttrs = LocationMapAttrs(57, 11, LocationMapTileKind.ThreeWallsOneDoorOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Energy Tank, Waterway']).MapAttrs = LocationMapAttrs(55, 14, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Energy Tank, Brinstar Gate']).MapAttrs = LocationMapAttrs(42, 9, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['X-Ray Scope']).MapAttrs = LocationMapAttrs(40, 16, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Spazer']).MapAttrs = LocationMapAttrs(25, 18, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Energy Tank, Kraid']).MapAttrs = LocationMapAttrs(20, 20, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Varia Suit']).MapAttrs = LocationMapAttrs(6, 20, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Ice Beam']).MapAttrs = LocationMapAttrs(57, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Energy Tank, Crocomire']).MapAttrs = LocationMapAttrs(43, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Hi-Jump Boots']).MapAttrs = LocationMapAttrs(55, 7, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Grapple Beam']).MapAttrs = LocationMapAttrs(59, 17, LocationMapTileKind.ThreeWallsOneDoorOpenBottom, hFlip=False, vFlip=True)

type(locationsDict['Reserve Tank, Norfair']).MapAttrs = LocationMapAttrs(44, 3, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Speed Booster']).MapAttrs = LocationMapAttrs(25, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Wave Beam']).MapAttrs = LocationMapAttrs(33, 5, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Energy Tank, Ridley']).MapAttrs = LocationMapAttrs(40, 18, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Screw Attack']).MapAttrs = LocationMapAttrs(42, 17, LocationMapTileKind.ThreeWallsOneDoorOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Energy Tank, Firefleas']).MapAttrs = LocationMapAttrs(25, 12, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=True)

type(locationsDict['Reserve Tank, Wrecked Ship']).MapAttrs = LocationMapAttrs(39, 12, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Energy Tank, Wrecked Ship']).MapAttrs = LocationMapAttrs(36, 14, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)

type(locationsDict['Right Super, Wrecked Ship']).MapAttrs = LocationMapAttrs(33, 18, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Gravity Suit']).MapAttrs = LocationMapAttrs(44, 14, LocationMapTileKind.FourWallsCorridor, hFlip=True, vFlip=False)

type(locationsDict['Energy Tank, Mama turtle']).MapAttrs = LocationMapAttrs(48, 13, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)

type(locationsDict['Plasma Beam']).MapAttrs = LocationMapAttrs(38, 3, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=True)

type(locationsDict['Reserve Tank, Maridia']).MapAttrs = LocationMapAttrs(46, 15, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)

type(locationsDict['Spring Ball']).MapAttrs = LocationMapAttrs(33, 17, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Energy Tank, Botwoon']).MapAttrs = LocationMapAttrs(37, 9, LocationMapTileKind.TwoWallsCorridor, hFlip=True, vFlip=False)

type(locationsDict['Space Jump']).MapAttrs = LocationMapAttrs(28, 11, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Power Bomb (Crateria surface)']).MapAttrs = LocationMapAttrs(29, 2, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (outside Wrecked Ship bottom)']).MapAttrs = LocationMapAttrs(24, 6, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (outside Wrecked Ship top)']).MapAttrs = LocationMapAttrs(23, 1, LocationMapTileKind.SingleWallHorizontal, hFlip=True, vFlip=False)

type(locationsDict['Missile (outside Wrecked Ship middle)']).MapAttrs = LocationMapAttrs(24, 3, LocationMapTileKind.SingleWallVertical, hFlip=True, vFlip=False)

type(locationsDict['Missile (Crateria moat)']).MapAttrs = LocationMapAttrs(26, 5, LocationMapTileKind.TwoWallsCornerWithHorizontalDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (Crateria bottom)']).MapAttrs = LocationMapAttrs(42, 19, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Missile (Crateria gauntlet right)']).MapAttrs = LocationMapAttrs(51, 4, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Missile (Crateria gauntlet left)']).MapAttrs = LocationMapAttrs(51, 4, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Super Missile (Crateria)']).MapAttrs = LocationMapAttrs(38, 10, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (Crateria middle)']).MapAttrs = LocationMapAttrs(46, 8, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Power Bomb (green Brinstar bottom)']).MapAttrs = LocationMapAttrs(51, 8, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Super Missile (pink Brinstar)']).MapAttrs = LocationMapAttrs(39, 10, LocationMapTileKind.TwoWallsCornerWithPixel, hFlip=False, vFlip=True)

type(locationsDict['Missile (green Brinstar below super missile)']).MapAttrs = LocationMapAttrs(52, 5, LocationMapTileKind.TwoWallsCorridor, hFlip=True, vFlip=False)

type(locationsDict['Super Missile (green Brinstar top)']).MapAttrs = LocationMapAttrs(53, 4, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (green Brinstar behind missile)']).MapAttrs = LocationMapAttrs(49, 5, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (green Brinstar behind reserve tank)']).MapAttrs = LocationMapAttrs(49, 5, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (pink Brinstar top)']).MapAttrs = LocationMapAttrs(46, 8, LocationMapTileKind.SingleWallVertical, hFlip=True, vFlip=False)

type(locationsDict['Missile (pink Brinstar bottom)']).MapAttrs = LocationMapAttrs(46, 11, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=True)

type(locationsDict['Power Bomb (pink Brinstar)']).MapAttrs = LocationMapAttrs(48, 9, LocationMapTileKind.TwoWallsCornerWithPixel, hFlip=True, vFlip=True)

type(locationsDict['Missile (green Brinstar pipe)']).MapAttrs = LocationMapAttrs(41, 12, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)

type(locationsDict['Power Bomb (blue Brinstar)']).MapAttrs = LocationMapAttrs(40, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (blue Brinstar middle)']).MapAttrs = LocationMapAttrs(31, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Super Missile (green Brinstar bottom)']).MapAttrs = LocationMapAttrs(58, 11, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (blue Brinstar bottom)']).MapAttrs = LocationMapAttrs(35, 12, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (blue Brinstar top)']).MapAttrs = LocationMapAttrs(34, 9, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (blue Brinstar behind missile)']).MapAttrs = LocationMapAttrs(34, 9, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Power Bomb (red Brinstar sidehopper room)']).MapAttrs = LocationMapAttrs(28, 9, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Power Bomb (red Brinstar spike room)']).MapAttrs = LocationMapAttrs(28, 12, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (red Brinstar spike room)']).MapAttrs = LocationMapAttrs(29, 12, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (Kraid)']).MapAttrs = LocationMapAttrs(16, 19, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (lava room)']).MapAttrs = LocationMapAttrs(46, 5, LocationMapTileKind.TwoWallsCornerWithHorizontalDoor, hFlip=False, vFlip=True)

type(locationsDict['Missile (below Ice Beam)']).MapAttrs = LocationMapAttrs(60, 5, LocationMapTileKind.ThreeWallsOneDoorOpenBottom, hFlip=False, vFlip=False)

type(locationsDict['Missile (above Crocomire)']).MapAttrs = LocationMapAttrs(51, 7, LocationMapTileKind.TwoWallsCornerWithHorizontalDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (Hi-Jump Boots)']).MapAttrs = LocationMapAttrs(54, 6, LocationMapTileKind.TwoWallsCornerWithPixel, hFlip=True, vFlip=False)

type(locationsDict['Energy Tank (Hi-Jump Boots)']).MapAttrs = LocationMapAttrs(53, 6, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Power Bomb (Crocomire)']).MapAttrs = LocationMapAttrs(53, 11, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (below Crocomire)']).MapAttrs = LocationMapAttrs(48, 16, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (Grapple Beam)']).MapAttrs = LocationMapAttrs(54, 16, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)

type(locationsDict['Missile (Norfair Reserve Tank)']).MapAttrs = LocationMapAttrs(44, 3, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (bubble Norfair green door)']).MapAttrs = LocationMapAttrs(41, 3, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (bubble Norfair)']).MapAttrs = LocationMapAttrs(39, 6, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=True)

type(locationsDict['Missile (Speed Booster)']).MapAttrs = LocationMapAttrs(26, 3, LocationMapTileKind.ThreeWallsOneDoorOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (Wave Beam)']).MapAttrs = LocationMapAttrs(36, 5, LocationMapTileKind.SingleWallHorizontal, hFlip=True, vFlip=False)

type(locationsDict['Missile (Gold Torizo)']).MapAttrs = LocationMapAttrs(44, 16, LocationMapTileKind.FourWallsOneDoor, hFlip=False, vFlip=False)

type(locationsDict['Super Missile (Gold Torizo)']).MapAttrs = LocationMapAttrs(43, 16, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)

type(locationsDict['Missile (Mickey Mouse room)']).MapAttrs = LocationMapAttrs(34, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (lower Norfair above fire flea room)']).MapAttrs = LocationMapAttrs(27, 6, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Power Bomb (lower Norfair above fire flea room)']).MapAttrs = LocationMapAttrs(25, 7, LocationMapTileKind.FourWallsTwoDoors, hFlip=False, vFlip=True)

type(locationsDict['Power Bomb (Power Bombs of shame)']).MapAttrs = LocationMapAttrs(30, 15, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (lower Norfair near Wave Beam)']).MapAttrs = LocationMapAttrs(33, 6, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (Wrecked Ship middle)']).MapAttrs = LocationMapAttrs(42, 17, LocationMapTileKind.ThreeWallsOpenRight, hFlip=True, vFlip=False)

type(locationsDict['Missile (Gravity Suit)']).MapAttrs = LocationMapAttrs(41, 14, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Missile (Wrecked Ship top)']).MapAttrs = LocationMapAttrs(33, 11, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

type(locationsDict['Super Missile (Wrecked Ship left)']).MapAttrs = LocationMapAttrs(39, 18, LocationMapTileKind.FourWallsOneDoor, hFlip=True, vFlip=False)

type(locationsDict['Missile (green Maridia shinespark)']).MapAttrs = LocationMapAttrs(56, 13, LocationMapTileKind.SingleWallVertical, hFlip=True, vFlip=False)

type(locationsDict['Super Missile (green Maridia)']).MapAttrs = LocationMapAttrs(55, 12, LocationMapTileKind.SingleWallVertical, hFlip=False, vFlip=False)

type(locationsDict['Missile (green Maridia tatori)']).MapAttrs = LocationMapAttrs(47, 14, LocationMapTileKind.SingleWallVertical, hFlip=False, vFlip=False)

type(locationsDict['Super Missile (yellow Maridia)']).MapAttrs = LocationMapAttrs(54, 7, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Missile (yellow Maridia super missile)']).MapAttrs = LocationMapAttrs(54, 7, LocationMapTileKind.ThreeWallsOpenBottom, hFlip=True, vFlip=True)

type(locationsDict['Missile (yellow Maridia false wall)']).MapAttrs = LocationMapAttrs(46, 7, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=True)

type(locationsDict['Missile (left Maridia sand pit room)']).MapAttrs = LocationMapAttrs(46, 15, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)

type(locationsDict['Missile (right Maridia sand pit room)']).MapAttrs = LocationMapAttrs(43, 15, LocationMapTileKind.TwoWallsCorner, hFlip=True, vFlip=False)

type(locationsDict['Power Bomb (right Maridia sand pit room)']).MapAttrs = LocationMapAttrs(42, 16, LocationMapTileKind.TwoWallsCornerWithVerticalDoor, hFlip=False, vFlip=True)

type(locationsDict['Missile (pink Maridia)']).MapAttrs = LocationMapAttrs(42, 10, LocationMapTileKind.SingleWallHorizontal, hFlip=True, vFlip=False)

type(locationsDict['Super Missile (pink Maridia)']).MapAttrs = LocationMapAttrs(41, 10, LocationMapTileKind.TwoWallsCorner, hFlip=False, vFlip=False)

type(locationsDict['Missile (Draygon)']).MapAttrs = LocationMapAttrs(24, 8, LocationMapTileKind.ThreeWallsOpenRight, hFlip=False, vFlip=False)

