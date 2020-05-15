


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

    def isLocMajor(self, loc):
        return 'Boss' not in loc['Class'] and (self.restrictions['MajorMinor'] == "Full" or self.restrictions['MajorMinor'] in loc['Class'])

    def isLocMinor(self, loc):
        return 'Boss' not in loc['Class'] and (self.restrictions['MajorMinor'] == "Full" or self.restrictions['MajorMinor'] not in loc['Class'])

    def isItemMajor(self, item):
        if self.restrictions['MajorMinor'] == "Full":
            return True
        else:
            return item['Class'] == self.restrictions['MajorMinor']

    def isItemMinor(self, item):
        if self.restrictions['MajorMinor'] == "Full":
            return True
        else:
            return item['Class'] == "Minor"

    def getItemManager(self, smbm):
        return ItemManager(self.restrictions['MajorMinor'], self.qty, self.smbm)
