# object to handle the smbools and optimize them

from functools import reduce

from smbool import SMBool
from rom import RomPatches
from graph_helpers import HelpersGraph

class SMBoolManager(object):
    @staticmethod
    def factory(store='all'):
        # possible values: all, diff, bool
        # all: store the difficulty, knows and items used, bool result (solver)
        # diff: store the difficulty and the bool result (randomizer with difficulty target)
        # bool: store only the bool result (randomizer w/o difficulty target)
        if store not in ['all', 'diff', 'bool']:
            raise Exception("SMBM::factory::invalid store param")

        print("SMBM::factory store {}".format(store))

        if store == 'all':
            return SMBMAll()
        elif store == 'diff':
            return SMBMDiff()
        elif store == 'bool':
            return SMBMBool()

    items = ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']
    countItems = ['ETank', 'Reserve', 'Missile', 'Super', 'PowerBomb']

    def __init__(self):
        self.helpers = HelpersGraph(self)
        self.curSMBool = SMBool(False)
        self.createFacadeFunctions()
        self.createKnowsFunctions()
        self.resetItems()

    def getItems(self):
        # get a dict of collected items and how many (to be displayed on the solver spoiler)
        itemsDict = {}
        for item in self.items:
            itemsDict[item] = getattr(self, item)
        for item in self.countItems:
            itemsDict[item] = getattr(self, item+"Count")
        return itemsDict

    def resetSMBool(self):
        self.curSMBool.bool = False
        self.curSMBool.difficulty = 0
        self.curSMBool.items = []
        self.curSMBool.knows = []

    def getSMBool(self):
        return self.curSMBool

    def getSMBoolCopy(self):
        return SMBool(self.curSMBool.bool,
                      self.curSMBool.difficulty,
                      self.curSMBool.knows[:],
                      self.curSMBool.items[:])

    def eval(self, func, item=None):
        if item is not None:
            self.addItem(item)
        self.resetSMBool()
        func(self)
        ret = self.getSMBoolCopy()
        if item is not None:
            self.removeItem(item)
        return ret

    def setSMBool(self, bool, diff=0, items=[]):
        self.curSMBool.bool = bool
        self.curSMBool.difficulty = diff
        self.curSMBool.items = items
        return self.getSMBoolCopy()

    def getBool(self, dummy):
        # get access to current smbool boolean (as internaly it can be bool or (bool, diff) or smbool)
        return self.curSMBool.bool

    def resetItems(self):
        # start without items
        for item in SMBoolManager.items:
            setattr(self, item, False)

        for item in SMBoolManager.countItems:
            setattr(self, item+'Count', 0)

    def addItem(self, item):
        # a new item is available
        setattr(self, item, True)
        if item in self.countItems:
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

    def addItems(self, items):
        if len(items) == 0:
            return
        for item in items:
            setattr(self, item, True)
            if item in self.countItems:
                setattr(self, item+'Count', getattr(self, item+'Count') + 1)

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if item in self.countItems:
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, False)
        else:
            setattr(self, item, False)

    def createFacadeFunctions(self):
        for fun in dir(self.helpers):
            if fun != 'smbm' and fun[0:2] != '__':
                setattr(self, fun, getattr(self.helpers, fun))

    def createKnowsFunctions(self):
        # for each knows we have a function knowsKnows (ex: knowsAlcatrazEscape()) which
        # take no parameter
        from parameters import Knows, isKnows
        for knows in Knows.__dict__:
            if isKnows(knows):
                setattr(self, 'knows'+knows, lambda knows=knows: self.knowsKnows(knows,
                                                                                 (Knows.__dict__[knows].bool,
                                                                                  Knows.__dict__[knows].difficulty)))

    def itemCount(self, item):
        # return integer
        return getattr(self, item+'Count')


class SMBMBool(SMBoolManager):
    # only care about the bool, internaly: bool
    def __init__(self):
        super(SMBMBool, self).__init__()

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = getattr(self, item)
        return self.curSMBool.bool

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows[0]
        return self.curSMBool.bool

    def wand(self, a, b, c=True, d=True):
        self.curSMBool.bool = a and b and c and d
        return self.curSMBool.bool

    def wor(self, a, b, c=False, d=False):
        self.curSMBool.bool = a or b or c or d
        return self.curSMBool.bool

    def wnot(self, a):
        self.curSMBool.bool = not a
        return self.curSMBool.bool

    def itemCountOk(self, item, count, difficulty=0):
        self.curSMBool.bool = self.itemCount(item) >= count
        return self.curSMBool.bool

    def energyReserveCountOk(self, count, difficulty=0):
        self.curSMBool.bool = self.energyReserveCount() >= count
        return self.curSMBool.bool

    def internal2SMBool(self, internal):
        # internal is a bool
        return SMBool(internal)

class SMBMDiff(SMBoolManager):
    # bool and diff here, internaly: only a tuple (bool, diff)
    def __init__(self):
        super(SMBMDiff, self).__init__()

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = getattr(self, item)
        self.curSMBool.difficulty = difficulty
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows[0]
        self.curSMBool.difficulty = smKnows[1]
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wand2(self, a, b):
        if a[0] == True and b[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a[1] + b[1]
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wand(self, a, b, c=None, d=None):
        if c is None and d is None:
            self.wand2(a, b)
        elif c is None:
            self.wand2(self.wand2(a, b), d)
        elif d is None:
            self.wand2(self.wand2(a, b), c)
        else:
            self.wand2(self.wand2(self.wand2(a, b), c), d)

        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wor2(self, a, b):
        if a[0] == True and b[0] == True:
            if a[1] <= b[1]:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = a[1]
            else:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = b[1]
        elif a[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a[1]
        elif b[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = b[1]
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0

        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wor(self, a, b, c=None, d=None):
        if c is None and d is None:
            self.wor2(a, b)
        elif c is None:
            self.wor2(self.wor2(a, b), d)
        elif d is None:
            self.wor2(self.wor2(a, b), c)
        else:
            self.wor2(self.wor2(self.wor2(a, b), c), d)

        return (self.curSMBool.bool, self.curSMBool.difficulty)

    # negates boolean part of the SMBool
    def wnot(self, a):
        self.curSMBool.bool = not a[0]
        self.curSMBool.difficulty = a[1]
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def itemCountOk(self, item, count, difficulty=0):
        if self.itemCount(item) >= count:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = difficulty
        else:
            self.curSMBool.bool = False
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def energyReserveCountOk(self, count, difficulty=0):
        if self.energyReserveCount() >= count:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = difficulty
        else:
            self.curSMBool.bool = False
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def internal2SMBool(self, internal):
        # internal is a (bool, diff)
        return SMBool(internal[0], internal[1])

class SMBMAll(SMBoolManager):
    # full package, internaly: smbool
    def __init__(self):
        super(SMBMAll, self).__init__()

    def haveItem(self, item, difficulty=0):
        return SMBool(getattr(self, item), difficulty, items=[item])

    def knowsKnows(self, knows, smKnows):
        return SMBool(smKnows[0], smKnows[1], knows=[knows])

    def wand2(self, a, b):
        if a.bool is True and b.bool is True:
            return SMBool(True, a.difficulty + b.difficulty,
                          a.knows + b.knows, a.items + b.items)
        else:
            return SMBool(False)

    def wand(self, a, b, c=None, d=None):
        if c is None and d is None:
            ret = self.wand2(a, b)
        elif c is None:
            ret = self.wand2(self.wand2(a, b), d)
        elif d is None:
            ret = self.wand2(self.wand2(a, b), c)
        else:
            ret = self.wand2(self.wand2(self.wand2(a, b), c), d)

        return ret

    def wor2(self, a, b):
        if a.bool is True and b.bool is True:
            if a.difficulty <= b.difficulty:
                return SMBool(True, a.difficulty, a.knows, a.items)
            else:
                return SMBool(True, b.difficulty, b.knows, b.items)
        elif a.bool is True:
            return SMBool(True, a.difficulty, a.knows, a.items)
        elif b.bool is True:
            return SMBool(True, b.difficulty, b.knows, b.items)
        else:
            return SMBool(False)

    def wor(self, a, b, c=None, d=None):
        if c is None and d is None:
            ret = self.wor2(a, b)
        elif c is None:
            ret = self.wor2(self.wor2(a, b), d)
        elif d is None:
            ret = self.wor2(self.wor2(a, b), c)
        else:
            ret = self.wor2(self.wor2(self.wor2(a, b), c), d)

        return ret

    # negates boolean part of the SMBool
    def wnot(self, a):
        return SMBool(not a.bool, a.difficulty, a.knows, a.items)

    def itemCountOk(self, item, count, difficulty=0):
        if self.itemCount(item) >= count:
            return SMBool(True, difficulty, items = [item])
        else:
            return SMBool(False)

    def energyReserveCountOk(self, count, difficulty=0):
        if self.energyReserveCount() >= count:
            return SMBool(True, difficulty, items = ['ETank', 'Reserve'])
        else:
            return SMBool(False)

    def setSMBool(self, bool, diff=0, items=[]):
        return SMBool(bool, diff, items=items)

    def getBool(self, dummy):
        return dummy.bool

    def internal2SMBool(self, internal):
        # internal is a smbool, return a copy to avoid having internal updated later (if internal is store in cache)
        return SMBool(internal.bool, internal.difficulty, internal.items[:], internal.knows[:])

    def eval(self, func, item=None):
        if item is not None:
            self.addItem(item)

        ret = func(self)

        if item is not None:
            self.removeItem(item)

        return ret
