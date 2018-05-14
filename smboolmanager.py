# object to handle the smbools and optimize them

from functools import reduce

from smbool import SMBool
from rom import RomPatches
from helpers import Helpers
from graph_helpers import HelpersGraph

class SMBoolManager(object):
    @staticmethod
    def factory(store='all', cache=True, graph=False):
        # possible values: all, diff, bool
        # all: store the difficulty, knows and items used, bool result (solver)
        # diff: store the difficulty and the bool result (randomizer with difficulty target)
        # bool: store only the bool result (randomizer w/o difficulty target)
        if store not in ['all', 'diff', 'bool']:
            raise Exception("SMBM::factory::invalid store param")

        print("SMBM::factory store {} cache {}".format(store, cache))

        if store == 'all':
            return SMBMAll(cache, graph)
        elif store == 'diff':
            return SMBMDiff(cache, graph)
        elif store == 'bool':
            return SMBMBool(cache, graph)

    items = ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']
    countItems = ['ETank', 'Reserve', 'Missile', 'Super', 'PowerBomb']

    def __init__(self, cache, graph=False):
        if graph == True:
            self.helpers = HelpersGraph(self)
        else:
            self.helpers = Helpers(self)
        self.curSMBool = SMBool(False)
        self.useCache = cache
        self.createCacheAndFacadeFunctions()
        self.createKnowsFunctions()
        self.resetItems()

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
        if item is None:
            ret = self.getSMBool()
        else:
            ret = self.getSMBoolCopy()
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

        if self.useCache == True:
            self.updateCache('reset', None)

    def updateCache(self, action, item):
        # reset: set last item added to None, recompute current
        if action == 'reset':
            self.lastItemAdded = None
            for fun in self.helpers.cachedMethods:
                self.resetSMBool()
                getattr(self.helpers, fun)()
                setattr(self, fun+'SMBool', self.getSMBoolCopy())

        # add: copy current in bak, set lastItemAdded, recompute current
        elif action == 'add':
            self.lastItemAdded = item
            for fun in self.helpers.cachedMethods:
                setattr(self, fun+'SMBoolbak', getattr(self, fun+'SMBool'))
                self.resetSMBool()
                getattr(self.helpers, fun)()
                setattr(self, fun+'SMBool', self.getSMBoolCopy())

        # remove: if item removed is last added, copy bak in current, set lastItemAdded to None
        elif action == 'remove':
            if self.lastItemAdded == item:
                self.lastItemAdded = None
                for fun in self.helpers.cachedMethods:
                    setattr(self, fun+'SMBool', getattr(self, fun+'SMBoolbak'))
            else:
                self.lastItemAdded = None
                for fun in self.helpers.cachedMethods:
                    self.resetSMBool()
                    getattr(self.helpers, fun)()
                    setattr(self, fun+'SMBool', self.getSMBoolCopy())

    def addItem(self, item):
        # a new item is available
        setattr(self, item, True)
        if item in self.countItems:
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        if self.useCache == True:
            self.updateCache('add', item)

    def addItems(self, items):
        # called by the randomizer with super fun times
        for item in items:
            setattr(self, item, True)
            if item in self.countItems:
                setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        if self.useCache == True:
            self.updateCache('add', item)

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if item in self.countItems:
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, False)
        else:
            setattr(self, item, False)

        if self.useCache == True:
            self.updateCache('remove', item)

    def createCacheAndFacadeFunctions(self):
        for fun in dir(self.helpers):
            if fun != 'smbm' and fun[0:2] != '__':
                if fun in self.helpers.cachedMethods and self.useCache == True:
                    setattr(self, fun, lambda fun=fun: self.getCacheSMBool(fun+'SMBool'))
                else:
                    setattr(self, fun, getattr(self.helpers, fun))

    def getCacheSMBool(self, fun):
        smb = getattr(self, fun)
        self.setSMBoolCache(smb)
        return smb

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
    def __init__(self, cache, graph=False):
        super(SMBMBool, self).__init__(cache, graph)

    def setSMBoolCache(self, smbool):
        self.curSMBool.bool = smbool.bool

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = getattr(self, item)
        return self.curSMBool.bool

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows[0]
        return self.curSMBool.bool

    def wand(self, a, b, c=True, d=True, difficulty=0):
        self.curSMBool.bool = a and b and c and d
        return self.curSMBool.bool

    def wor(self, a, b, c=False, d=False, difficulty=0):
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
    def __init__(self, cache, graph=False):
        super(SMBMDiff, self).__init__(cache, graph)

    def setSMBoolCache(self, smbool):
        self.curSMBool.bool = smbool.bool
        self.curSMBool.difficulty = smbool.difficulty

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = getattr(self, item)
        self.curSMBool.difficulty = difficulty
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows[0]
        self.curSMBool.difficulty = smKnows[1]
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wand2(self, a, b, difficulty=0):
        if a[0] == True and b[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a[1] + b[1] + difficulty
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wand(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            self.wand2(a, b)
        elif c is None:
            self.wand2(self.wand2(a, b), d)
        elif d is None:
            self.wand2(self.wand2(a, b), c)
        else:
            self.wand2(self.wand2(self.wand2(a, b), c), d)

        if self.curSMBool.bool == True and difficulty != 0:
            self.curSMBool.difficulty += difficulty

        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wor2(self, a, b, difficulty=0):
        if a[0] == True and b[0] == True:
            if a[1] <= b[1]:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = a[1] + difficulty
            else:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = b[1] + difficulty
        elif a[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a[1] + difficulty
        elif b[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = b[1] + difficulty
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0

        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wor(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            self.wor2(a, b)
        elif c is None:
            self.wor2(self.wor2(a, b), d)
        elif d is None:
            self.wor2(self.wor2(a, b), c)
        else:
            self.wor2(self.wor2(self.wor2(a, b), c), d)

        if self.curSMBool.bool == True and difficulty != 0:
            self.curSMBool.difficulty += difficulty

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
    def __init__(self, cache, graph=False):
        super(SMBMAll, self).__init__(cache, graph)

    def setSMBoolCache(self, smbool):
        self.curSMBool.bool = smbool.bool
        self.curSMBool.difficulty = smbool.difficulty
        self.curSMBool.items = smbool.items[:]
        self.curSMBool.knows = smbool.knows[:]

    def haveItem(self, item, difficulty=0):
        return SMBool(getattr(self, item), difficulty, items=[item])

    def knowsKnows(self, knows, smKnows):
        return SMBool(smKnows[0], smKnows[1], knows=[knows])

    def wand2(self, a, b, difficulty=0):
        if a.bool is True and b.bool is True:
            return SMBool(True, a.difficulty + b.difficulty + difficulty,
                          a.knows + b.knows, a.items + b.items)
        else:
            return SMBool(False)

    def wand(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            ret = self.wand2(a, b)
        elif c is None:
            ret = self.wand2(self.wand2(a, b), d)
        elif d is None:
            ret = self.wand2(self.wand2(a, b), c)
        else:
            ret = self.wand2(self.wand2(self.wand2(a, b), c), d)

        if ret.bool is True:
            ret.difficulty += difficulty

        return ret

    def wor2(self, a, b, difficulty=0):
        if a.bool is True and b.bool is True:
            if a.difficulty < b.difficulty:
                return SMBool(True, a.difficulty + difficulty, a.knows, a.items)
            elif a.difficulty > b.difficulty:
                return SMBool(True, b.difficulty + difficulty, b.knows, b.items)
            else:
                # in case of egality we return both knows
                return SMBool(True, a.difficulty + difficulty,
                              a.knows + b.knows, a.items + b.items)
        elif a.bool is True:
            return SMBool(True, a.difficulty + difficulty, a.knows, a.items)
        elif b.bool is True:
            return SMBool(True, b.difficulty + difficulty, b.knows, b.items)
        else:
            return SMBool(False)

    def wor(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            ret = self.wor2(a, b)
        elif c is None:
            ret = self.wor2(self.wor2(a, b), d)
        elif d is None:
            ret = self.wor2(self.wor2(a, b), c)
        else:
            ret = self.wor2(self.wor2(self.wor2(a, b), c), d)

        if ret.bool is True:
            ret.difficulty += difficulty

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
        # internal is a smbool
        return internal

    def eval(self, func, item=None):
        if item is not None:
            self.addItem(item)

        ret = func(self)

        if item is not None:
            self.removeItem(item)

        return ret
