# object to handle the smbools and optimize them

import copy
from smbool import SMBool

class SMOptim(object):
    @staticmethod
    def factory(store='all'):
        # possible values: all, diff, bool
        # all: store the difficulty, knows and items used, bool result (solver)
        # diff: store the difficulty and the bool result (randomizer with difficulty target)
        # bool: store only the bool result (randomizer w/o difficulty target)
        if store not in ['all', 'diff', 'bool']:
            raise Exception("SMOptim::factory::invalid store param")

        if store == 'all':
            return SMOptimAll()
        elif store == 'diff':
            return SMOptimDiff()
        elif store == 'bool':
            return SMOptimBool()

    items = ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']
    countItems = ['ETank', 'Reserve', 'Missile', 'Super', 'PowerBomb']

    def __init__(self):
        self.resetItems()
        self.createItemsFunctions()
        self.createKnowsFunctions()
        self.resetSMBool()

    def resetSMBool(self):
        self.curSMBool = SMBool(False)

    def getSMBool(self):
        return self.curSMBool

    def getSMBoolCopy(self):
        # may not be useful, if we do a getSMBool(), then a resetSMBool(), then it should be ok
        return copy.copy(self.curSMBool)

    def resetItems(self):
        # start without items
        for item in SMOptim.items:
            self.__dict__[item] = False

        for item in SMOptim.countItems:
            self.__dict__[item+'Count'] = 0

    def addItem(self, item):
        # a new item is available
        self.__dict__[item] = True
        if item+'Count' in self.__dict__:
            self.__dict__[item+'Count'] = self.__dict__[item+'Count'] + 1

    def removeItem(self, item):
        # randomizer removed an item
        if item+'Count' in self.__dict__:
            self.__dict__[item+'Count'] = self.__dict__[item+'Count'] - 1
            if self.__dict__[item+'Count'] == 0:
                self.__dict__[item] = False
        else:
            self.__dict__[item] = False

    def createItemsFunctions(self):
        # for each item we have a function haveItem (ex: haveBomb()) which take an
        # optional parameter: the difficulty
        for item in SMOptim.items:
            self.__dict__['have'+item] = lambda difficulty=0: self.haveItem(item, difficulty)

        for item in SMOptim.countItems:
            self.__dict__['count'+item] = lambda: self.countItem(item)

    def createKnowsFunctions(self):
        # for each knows we have a function knowsKnows (ex: knowsAlcatrazEscape()) which
        # take no parameter
        from parameters import Knows, isKnows
        for knows in Knows.__dict__:
            if isKnows(knows):
                self.__dict__['knows'+knows] = lambda: self.knowsKnows(knows, Knows.__dict__[knows])

    # all the functions from helpers
    def countItem(self, item):
        return self.__dict__[item+'Count']


class SMOptimBool(SMOptim):
    # only care about the bool, internaly: bool
    def __init__(self):
        super(SMOptimBool, self).__init__()

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = self.__dict__[item]
        return self.__dict__[item]

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows.bool
        return smKnows.bool

    def wand2(self, a, b, difficulty=0):
        ret = a is True and b is True
        self.curSMBool.bool = ret
        return ret

    def wand(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            return wand2(a, b)
        elif c is None:
            return wand2(wand2(a, b), d)
        elif d is None:
            return wand2(wand2(a, b), c)
        else:
            return wand2(wand2(wand2(a, b), c), d)

    def wor2(self, a, b, difficulty=0):
        ret = a is True or b is True
        self.curSMBool.bool = ret
        return ret

    def wor(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            return wor2(a, b)
        elif c is None:
            return wor2(wor2(a, b), d)
        elif d is None:
            return wor2(wor2(a, b), c)
        else:
            return wor2(wor2(wor2(a, b), c), d)

    def wnot(self, a):
        ret = not a
        self.curSMBool.bool = ret
        return ret
    
class SMOptimDiff(SMOptim):
    # bool and diff here, internaly: only a tuple (bool, diff)
    def __init__(self):
        super(SMOptimDiff, self).__init__()

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = self.__dict__[item]
        self.curSMBool.difficulty = difficulty
        return (self.__dict__[item], difficulty)

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows.bool
        self.curSMBool.difficulty = smKnows.difficulty
        return (smKnows.bool, smKnows.difficulty)

    def wand2(self, a, b, difficulty=0):
        if a[0] is True and b[0] is True:
            return (True, a[1] + b[1] + difficulty)
        else:
            return (False, 0)

    def wand(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            ret = wand2(a, b)
        elif c is None:
            ret = wand2(wand2(a, b), d)
        elif d is None:
            ret = wand2(wand2(a, b), c)
        else:
            ret = wand2(wand2(wand2(a, b), c), d)

        if ret[0] is True:
            ret = (ret[0], ret[1] + difficulty)

        return ret

    def wor2(self, a, b, difficulty=0):
        if a[0] is True and b[0] is True:
            if a[1] <= b[1]:
                return (True, a[1] + difficulty)
            else:
                return (True, b[1] + difficulty)
        elif a[0] is True:
            return (True, a[1] + difficulty)
        elif b[0] is True:
            return (True, b[1] + difficulty)
        else:
            return (False, 0)

    def wor(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            ret = wor2(a, b)
        elif c is None:
            ret = wor2(wor2(a, b), d)
        elif d is None:
            ret = wor2(wor2(a, b), c)
        else:
            ret = wor2(wor2(wor2(a, b), c), d)

        if ret[0] is True:
            ret = (ret[0], ret[1] + difficulty)

        return ret

    # negates boolean part of the SMBool
    def wnot(self, a):
        return (not a[0], a[1])

class SMOptimAll(SMOptimDiff):
    # full package, internaly: only a tuple (bool, diff)
    def __init__(self):
        super(SMOptimAll, self).__init__()

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = self.__dict__[item]
        self.curSMBool.difficulty = difficulty
        if self.__dict__[item] is True:
            self.curSMBool.items.append(item)
        return (self.__dict__[item], difficulty)

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows.bool
        self.curSMBool.difficulty = smKnows.difficulty
        if smKnows.bool is True:
            self.curSMBool.knows.append(knows)
        return (smKnows.bool, smKnows.difficulty)
