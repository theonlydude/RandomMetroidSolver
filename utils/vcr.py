import json, os.path

# record solver/rando to play in the VCR tracker
class VCR(object):
    def __init__(self, name, type):
        self.outFileName = "{}.{}.vcr".format(os.path.basename(os.path.splitext(name)[0]), type)
        self.tape = []
        self.filler = 'front'

    def setFiller(self, filler):
        self.filler = filler

    def addInitialItems(self, items):
        # used by assumed filler, add all the initial items.
        # replace NoEnergy by Nothing, as NoEnergy is only used in the randomizer
        self.tape.append({'type': 'init',
                          'items': [it if it != 'NoEnergy' else 'Nothing' for it in items]})

    def addLocation(self, locName, itemName):
        # collect item at location, front filler: collect item, assumed filler: remove item
        self.tape.append({'type': 'location',
                          'loc': locName,
                          'item': itemName if itemName != 'NoEnergy' else 'Nothing',
                          'filler': self.filler})

    def addRollback(self, count):
        # used by filler progspeed rollbacks
        self.tape.append({'type': 'rollback', 'count': count})

    def removeLocation(self, locName, itemName):
        # used by assumed filler item swap, put item at loc back in the pool
        self.tape.append({'type': 'remove',
                          'loc': locName,
                          'item': itemName if itemName != 'NoEnergy' else 'Nothing'})

    def dump(self):
        with open(self.outFileName, 'w') as jsonFile:
            json.dump(self.tape, jsonFile)
