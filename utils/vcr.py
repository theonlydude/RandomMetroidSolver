import json, os.path

# record solver/rando to play in the VCR tracker
class VCR(object):
    def __init__(self, name, type):
        self.outFileName = "{}.{}.vcr".format(os.path.basename(os.path.splitext(name)[0]), type)
        self.tape = []
        self.reverse = False

    def addLocation(self, locName, itemName):
        self.tape.append({'type': 'location', 'loc': locName, 'item': itemName})

    def addRollback(self, count):
        self.tape.append({'type': 'rollback', 'count': count})

    def dump(self):
        with open(self.outFileName, 'w') as jsonFile:
            json.dump(self.tape, jsonFile)

    def beginAssumed(self):
        self.tapeBackup = self.tape
        self.tape = []

    def endAssumed(self):
        self.tape.reverse()
        self.tape = self.tapeBackup + self.tape
