
from rando.Items import ItemManager

class RandoSettings(object):
    def __init__(self, maxDiff, progSpeed, progDiff, qty, restrictions,
                 superFun, runtimeLimit_s, vcr, plandoRando):
        self.progSpeed = progSpeed
        self.progDiff = progDiff
        self.maxDiff = maxDiff
        self.qty = qty
        self.restrictions = restrictions
        self.superFun = superFun
        self.runtimeLimit_s = runtimeLimit_s
        if self.runtimeLimit_s <= 0:
            self.runtimeLimit_s = sys.maxsize
        self.vcr = vcr

    def getItemManager(self, smbm):
        return ItemManager(self.restrictions['MajorMinor'], self.qty, smbm)

class GraphSettings(object):
    def __init__(self, startAP, areaRando, bossRando, escapeRando, dotFile):
        self.bidir = True
        self.startAP = startAP
        self.areaRando = areaRando
        self.bossRando = bossRando
        self.escapeRando = escapeRando
        self.dotFile = dotFile
