from graph.vanilla.graph_locations import locationsDict
from graph.vanilla.graph_locations import LocationsHelper
from rom.addresses import Addresses

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
