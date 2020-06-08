# object to handle the smbools and optimize them

from cache import Cache
from graph_helpers import HelpersGraph
from parameters import Knows, isKnows
from smbool import SMBool
from helpers import Bosses

class SMBoolManager(object):
    items = ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack', 'Nothing', 'NoEnergy', 'MotherBrain'] + Bosses.Golden4()
    countItems = ['Missile', 'Super', 'PowerBomb', 'ETank', 'Reserve']

    def __init__(self):
        Cache.reset()
        self.helpers = HelpersGraph(self)
        self.createFacadeFunctions()
        self.createKnowsFunctions()
        self.resetItems()

    def isEmpty(self):
        for item in self.items:
            if self.haveItem(item):
                return False
        for item in self.countItems:
            if self.itemCount(item) > 0:
                return False
        return True

    def getItems(self):
        # get a dict of collected items and how many (to be displayed on the solver spoiler)
        itemsDict = {}
        for item in self.items[:-2]: # ignore last two items: nothing and noenergy
            itemsDict[item] = getattr(self, item)
        for item in self.countItems:
            itemsDict[item] = getattr(self, item+"Count")
        return itemsDict

    def eval(self, func, item=None):
        if item is not None:
            self.addItem(item)

        ret = func(self)

        if item is not None:
            self.removeItem(item)

        return ret

    def resetItems(self):
        # start without items
        for item in SMBoolManager.items:
            setattr(self, item, False)

        for item in SMBoolManager.countItems:
            setattr(self, item+'Count', 0)

        Cache.reset()

    def addItem(self, item):
        # a new item is available
        setattr(self, item, True)
        if self.isCountItem(item):
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def addItems(self, items):
        if len(items) == 0:
            return
        for item in items:
            setattr(self, item, True)
            if self.isCountItem(item):
                setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if self.isCountItem(item):
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, False)
        else:
            setattr(self, item, False)

        Cache.reset()

    def createFacadeFunctions(self):
        for fun in dir(self.helpers):
            if fun != 'smbm' and fun[0:2] != '__':
                setattr(self, fun, getattr(self.helpers, fun))

    def createKnowsFunctions(self):
        # for each knows we have a function knowsKnows (ex: knowsAlcatrazEscape()) which
        # take no parameter
        for knows in Knows.__dict__:
            if isKnows(knows):
                setattr(self, 'knows'+knows, lambda knows=knows: self.knowsKnows(knows,
                                                                                 (Knows.__dict__[knows].bool,
                                                                                  Knows.__dict__[knows].difficulty)))

    def isCountItem(self, item):
        return item in self.countItems

    def itemCount(self, item):
        # return integer
        return getattr(self, item+'Count')

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
            if item in ['ETank', 'Reserve']:
                item = '{}-{}'.format(count, item)
            return SMBool(True, difficulty, items = [item])
        else:
            return SMBool(False)

    def energyReserveCountOk(self, count, difficulty=0):
        if self.energyReserveCount() >= count:
            nEtank = self.itemCount('ETank')
            if nEtank > count:
                nEtank = int(count)
            items = '{}-ETank'.format(nEtank)
            nReserve = self.itemCount('Reserve')
            if nEtank < count:
                nReserve = int(count) - nEtank
                items += ' - {}-Reserve'.format(nReserve)
            else:
                nReserve = 0
            return SMBool(True, difficulty, items = [items])
        else:
            return SMBool(False)

class SMBoolManagerPlando(SMBoolManager):
    def __init__(self):
        super(SMBoolManagerPlando, self).__init__()

    def addItem(self, item):
        # a new item is available
        already = self.haveItem(item)
        isCount = self.isCountItem(item)
        if isCount or not already:
            setattr(self, item, True)
        else:
            # handle duplicate major items (plandos)
            setattr(self, 'dup_'+item, False)
        if isCount:
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if self.isCountItem(item):
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, False)
        else:
            dup = 'dup_'+item
            if getattr(self, dup, None) is None:
                setattr(self, item, False)
            else:
                setattr(self, dup, False)

        Cache.reset()
