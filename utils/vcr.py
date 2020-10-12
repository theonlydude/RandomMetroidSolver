import json, os.path

# record solver/rando to play in the VCR tracker
class VCR(object):
    def __init__(self, name, type):
        self.outFileName = "{}.{}.vcr".format(os.path.basename(os.path.splitext(name)[0]), type)
        self.tape = []

    def addLocation(self, locName, itemName):
        self.tape.append({'type': 'location', 'loc': locName, 'item': itemName})

    def addRollback(self, count):
        self.tape.append({'type': 'rollback', 'count': count})

    def dump(self, reverse=False):
        if reverse:
            self.tape.reverse()
        with open(self.outFileName, 'w') as jsonFile:
            json.dump(self.tape, jsonFile)
