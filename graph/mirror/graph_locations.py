from graph.vanilla.graph_locations import locationsDict
from graph.vanilla.graph_locations import LocationsHelper
from rom.rom import snes_to_pc

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

# croc room plm's have been relocated in 8f freespace
locationsDict["Energy Tank, Crocomire"].Address = snes_to_pc(0x8ffdf1)

locations = [loc for loc in locationsDict.values()]
