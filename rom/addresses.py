from rom.rom import snes_to_pc, pc_to_snes

# TODO::add patches

class Byte(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value]

class Word(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value, self.value+1]

class Long(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value, self.value+1, self.value+2]

class ValueSingle(object):
    def __init__(self, value, storage=Word):
        self.value = snes_to_pc(value)
        self.storage = storage

    def getOne(self):
        return self.value

    def getAll(self):
        return [self.value]

    def getWeb(self):
        return self.storage(self.value).expand()

class ValueList(object):
    def __init__(self, values, storage=Word):
        self.values = [snes_to_pc(value) for value in values]
        self.storage = storage

    def getOne(self):
        return self.values[0]

    def getAll(self):
        return self.values

    def getWeb(self):
        out = []
        for value in self.values:
            out += self.storage(value).expand()
        return out

class ValueRange(object):
    def __init__(self, start, length=-1, end=-1):
        self.start = snes_to_pc(start)
        if length != -1:
            self.end = self.start + length
            self.length = length
        else:
            self.end = snes_to_pc(end)
            self.length = self.end - self.start

    def getOne(self):
        return self.start

    def getAll(self):
        return [self.start+i for i in range(self.length)]

    def getWeb(self):
        return [self.start, self.end]

class Addresses(object):
    @staticmethod
    def getOne(key):
        value = Addresses.addresses[key]
        return value.getOne()

    @staticmethod
    def getAll(key):
        value = Addresses.addresses[key]
        return value.getAll()

    @staticmethod
    def getWeb(key):
        value = Addresses.addresses[key]
        return value.getWeb()

    @staticmethod
    def getRange(key):
        value = Addresses.addresses[key]
        return value.getWeb()

    addresses = {
        'totalItems': ValueList([0x8BE656, 0x8BE6B3], storage=Byte),
        'totalItemsPercent': ValueList([0x82FA7E, 0x82FA86, 0x82FA8E, 0x82FA96]),
        'objectivesList': ValueSingle(0x82f983),
        'objectivesSpritesOAM': ValueSingle(0x82FEB0),
        'objectivesText': ValueSingle(0xB6F200),
        'majorsSplit': ValueSingle(0x82fb6c, storage=Byte),
        # scavenger hunt items list (17 prog items (including ridley) + hunt over + terminator, each is a word)
        'scavengerOrder': ValueRange(0xA1F5D8, length=(17+1+1)*2),
        'plandoAddresses': ValueRange(0xdee000, length=128),
        'plandoTransitions': ValueSingle(0xdee100),
        'escapeTimer': ValueSingle(0x809e21),
        'escapeTimerTable': ValueSingle(0xA1F0AA),
        'startAP': ValueSingle(0xa1f200),
        'customDoorsAsm': ValueSingle(0x8ff800),
        'locIdsByArea': ValueRange(0xA1F568, end=0xA1F5D7),
        'plmSpawnTable': ValueSingle(0x8fe9a0),
        'plmSpawnRoomTable': ValueSingle(0x8ff000),
        'moonwalk': ValueSingle(0x81b35d),
        'additionalETanks': ValueSingle(0xA1F470),
        'hellrunRate': ValueSingle(0x8DE387)
    }
