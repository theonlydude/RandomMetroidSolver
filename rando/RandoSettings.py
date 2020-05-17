
from rando.Items import ItemManager

class RandoSettings(object):
    def __init__(self, startAP, maxDiff, progSpeed, progDiff, qty, restrictions,
                 superFun, runtimeLimit_s, escapeRando, vcr, plandoRando):
        self.startAP = startAP
        self.progSpeed = progSpeed
        self.progDiff = progDiff
        self.maxDiff = maxDiff
        self.qty = qty
        self.restrictions = restrictions
        self.superFun = superFun
        self.runtimeLimit_s = runtimeLimit_s
        if self.runtimeLimit_s <= 0:
            self.runtimeLimit_s = sys.maxsize
        self.escapeRando = escapeRando
        self.vcr = vcr
        self.plandoRando = plandoRando

    def getItemManager(self, smbm):
        return ItemManager(self.restrictions['MajorMinor'], self.qty, self.smbm)
