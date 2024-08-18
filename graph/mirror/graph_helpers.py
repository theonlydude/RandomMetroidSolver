from graph.vanilla.graph_helpers import HelpersGraph
from logic.cache import Cache
from rom.rom_patches import RomPatches
from logic.smbool import SMBool

# gates are reversed
class HelpersGraphMirror(HelpersGraph):
    def __init__(self, smbm):
        self.smbm = smbm

    @Cache.decorator
    def canPassRedTowerToMaridiaNode(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       sm.wor(RomPatches.has(RomPatches.CaterpillarGreenGateRemoved),
                              sm.canGreenGateGlitch()))

    @Cache.decorator
    def canExitWaveBeam(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Morph'), # exit through lower passage under the spikes
                      sm.wand(sm.wor(sm.haveItem('SpaceJump'), # exit through blue gate
                                     sm.haveItem('Grapple')),
                              sm.haveItem('Wave')))

    # (this is actually Left to Right in mirror)
    def canPassFrogSpeedwayRightToLeft(self):
        return super().canPassFrogSpeedwayLeftToRight()

    # (this is actually Right to Left in mirror)
    def canPassFrogSpeedwayLeftToRight(self):
        return super().canPassFrogSpeedwayRightToLeft()

    @Cache.decorator
    def canAccessMaridiaReserveFromTopWestSandHole(self):
        v = super().canAccessItemsInWestSandHole()
        if 'WestSandHoleMorphOnlyItemAccess' in v.knows:
            # wiggling is not possible from right to left
            return SMBool(False, 0)
        return v
