from rom.rom import snes_to_pc

# TODO::use it to get web addresses to read
# TODO::handle addresses ranges
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

    addresses = {
        'totalItems': ValueList([0x8BE656, 0x8BE6B3], storage=Byte),
        'totalItemsPercent': ValueList([0x82FA91, 0x82FA99, 0x82FAA1, 0x82FAA9]),
        'objectivesList': ValueSingle(0x82f983),
        'objectivesSpritesOAM': ValueSingle(0x82FD40),
        'objectivesText': ValueSingle(0xB6F200),
    }
