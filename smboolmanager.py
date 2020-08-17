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
        self.smboolFalse = SMBool(False)
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
            setattr(self, item, SMBool(False))

        for item in SMBoolManager.countItems:
            setattr(self, item+'Count', 0)

        Cache.reset()

    def addItem(self, item):
        # a new item is available
        setattr(self, item, SMBool(True, items=[item]))
        if self.isCountItem(item):
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def addItems(self, items):
        if len(items) == 0:
            return
        for item in items:
            setattr(self, item, SMBool(True, items=[item]))
            if self.isCountItem(item):
                setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if self.isCountItem(item):
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, SMBool(False))
        else:
            setattr(self, item, SMBool(False))

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
                setattr(self, 'knows'+knows, lambda knows=knows: SMBool(Knows.__dict__[knows].bool,
                                                                        Knows.__dict__[knows].difficulty,
                                                                        knows=[knows]))

    def isCountItem(self, item):
        return item in self.countItems

    def itemCount(self, item):
        # return integer
        return getattr(self, item+'Count')

    def haveItem(self, item):
        return getattr(self, item)

    def wand(self, *args):
        if False in args:
            return self.smboolFalse
        else:
            return SMBool(True,
                          sum([smb.difficulty for smb in args]),
                          [know for smb in args for know in smb.knows],
                          [item for smb in args for item in smb.items])

    def wor(self, *args):
        if True in args:
            # return the smbool with the smallest difficulty among True smbools.
            return min(args)
        else:
            return self.smboolFalse

    # negates boolean part of the SMBool
    def wnot(self, a):
        return SMBool(not a.bool, a.difficulty)

    def itemCountOk(self, item, count, difficulty=0):
        if self.itemCount(item) >= count:
            if item in ['ETank', 'Reserve']:
                item = '{}-{}'.format(count, item)
            return SMBool(True, difficulty, items = [item])
        else:
            return self.smboolFalse

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
            return SMBool(True, difficulty, items = [items])
        else:
            return self.smboolFalse

class SMBoolManagerPlando(SMBoolManager):
    def __init__(self):
        super(SMBoolManagerPlando, self).__init__()

    def addItem(self, item):
        # a new item is available
        already = self.haveItem(item)
        isCount = self.isCountItem(item)
        if isCount or not already:
            setattr(self, item, SMBool(True, items=[item]))
        else:
            # handle duplicate major items (plandos)
            setattr(self, 'dup_'+item, True)
        if isCount:
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        Cache.reset()

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if self.isCountItem(item):
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, SMBool(False))
        else:
            dup = 'dup_'+item
            if getattr(self, dup, None) is None:
                setattr(self, item, SMBool(False))
            else:
                delattr(self, dup)

        Cache.reset()
