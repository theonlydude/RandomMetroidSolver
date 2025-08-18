import os, json

from rom.rom_patches import RomPatches, definitions as patches_definitions
from rom.rom import RealROM, FakeROM
from rom.romreader import RomReader
from utils.doorsmanager import DoorsManager
from graph.graph_utils import getAccessPoint
from collections import defaultdict
from rom.flavor import RomFlavor

class RomLoader(object):
    @staticmethod
    def factory(rom, magic=None):
        # can be a real rom. can be a json or a dict with the ROM address/values
        if type(rom) == str:
            ext = os.path.splitext(rom)
            if ext[1].lower() == '.sfc' or ext[1].lower() == '.smc':
                return RomLoaderSfc(rom, magic)
            elif ext[1].lower() == '.json':
                return RomLoaderJson(rom, magic)
            else:
                raise Exception("wrong rom file type: {}".format(ext[1]))
        elif type(rom) is dict:
            return RomLoaderDict(rom, magic)

    def loadSymbols(self):
        self.romReader.loadSymbols()

    def assignItems(self, locations):
        return self.romReader.loadItems(locations)

    def getTransitions(self, tourian):
        return self.romReader.loadTransitions(tourian)

    def hasPatch(self, patchName):
        return self.romReader.patchPresent(patchName)

    def readOption(self, name):
        return self.romReader.romOptions.read(name)

    def loadPatches(self):
        RomPatches.ActivePatches = []
        isBoss = False
        isEscape = False
        # check patches with logic impact
        patchList = list(patches_definitions['common'].keys()) + list(patches_definitions[RomFlavor.flavor].keys())
        for patchName in patchList:
            patchDef = patches_definitions['common'].get(patchName, patches_definitions[RomFlavor.flavor].get(patchName))
            if 'logic' in patchDef and self.hasPatch(patchName):
                RomPatches.ActivePatches += patchDef['logic']
        # check area rando
        isArea = self.hasPatch("area")
        # check boss rando
        isBoss = self.isBoss()
        # check escape rando
        isEscape = self.hasPatch("areaEscape")
        # Tourian
        tourian = 'Vanilla'
        if self.hasPatch("fast_tourian"):
            tourian = 'Fast'
        if self.isEscapeTrigger():
            RomPatches.ActivePatches.append(RomPatches.NoTourian)
            tourian = 'Disabled'
        # objectives
        hasObjectives = self.hasPatch('objectives')

        return (isArea, isBoss, isEscape, hasObjectives, tourian)

    def getPatchIds(self):
        return self.romReader.getPatchIds()

    def getRawPatches(self):
        # used in interactive solver
        return self.romReader.getRawPatches()

    def getAllPatches(self):
        # used in cli
        return self.romReader.getAllPatches()

    def getPlandoAddresses(self):
        return self.romReader.getPlandoAddresses()

    def getPlandoTransitions(self, maxTransitions):
        return self.romReader.getPlandoTransitions(maxTransitions)

    def decompress(self, address):
        return self.romReader.decompress(address)

    def getROM(self):
        return self.romReader.romFile

    def isEscapeTrigger(self):
        return self.romReader.isEscapeTrigger()

    def isBoss(self):
        romFile = self.getROM()
        phOut = getAccessPoint('PhantoonRoomOut')
        doorPtr = phOut.ExitInfo['DoorPtr']
        romFile.seek((0x10000 | doorPtr) + 10)
        asmPtr = romFile.readWord()
        return asmPtr != 0 # this is at 0 in vanilla

    def getEscapeTimer(self):
        return self.romReader.getEscapeTimer()

    def getStartAP(self):
        return self.romReader.getStartAP()

    def loadDoorsColor(self):
        rom = self.getROM()
        if self.romReader.race is None:
            return DoorsManager().loadDoorsColor(rom, rom.readWord)
        else:
            return DoorsManager().loadDoorsColor(rom, self.romReader.readPlmWord)

    def readLogic(self):
        return self.romReader.readLogic()

    def loadObjectives(self, objectives):
        self.romReader.readObjectives(objectives)

    def updateSplitLocs(self, split, locations):
        locIdsByArea = self.romReader.getLocationsIds()
        locIds = []
        for area, ids in locIdsByArea.items():
            locIds += ids
        for loc in locations:
            if loc.isBoss():
                continue
            elif loc.Id in locIds:
                loc.setClass([split])
            else:
                loc.setClass(["Minor"])

    def getSplitLocsByArea(self, locations):
        locIdsByArea = self.romReader.getLocationsIds()
        locsByArea = defaultdict(list)
        for area, locIds in locIdsByArea.items():
            for loc in locations:
                if loc.Id in locIds:
                    locsByArea[area].append(loc.Name)
        return locsByArea

    def loadScavengerOrder(self, locations):
        return self.romReader.loadScavengerOrder(locations)

    def loadMajorUpgrades(self):
        itemsMask, beamsMask = self.romReader.readItemMasks()
        itemBits = {
            'Bomb':0x1000,
            'HiJump':0x100,
            'SpeedBooster':0x2000,
            'SpringBall':0x2,
            'Varia':0x1,
            'Grapple':0x4000,
            'Morph':0x4,
            'Gravity':0x20,
            'XRayScope':0x8000,
            'SpaceJump':0x200,
            'ScrewAttack':0x8
        }
        beamBits = {
            'Charge':0x1000,
            'Ice':0x2,
            'Wave':0x1,
            'Spazer':0x4,
            'Plasma':0x8
        }
        upgrades = [item for item,mask in itemBits.items() if itemsMask & mask != 0]
        upgrades += [item for item,mask in beamBits.items() if beamsMask & mask != 0]
        return upgrades

    def loadEventBitMasks(self):
        return self.romReader.loadEventBitMasks()

    def getStartingEnergy(self):
        return self.romReader.getStartingEnergy()

class RomLoaderSfc(RomLoader):
    # standard usage (when calling from the command line)
    def __init__(self, romFileName, magic=None):
        super(RomLoaderSfc, self).__init__()
        realROM = RealROM(romFileName)
        self.romReader = RomReader(realROM, magic)

class RomLoaderDict(RomLoader):
    # when called from the website (the js in the browser uploads a dict of address: value)
    def __init__(self, dictROM, magic=None):
        super(RomLoaderDict, self).__init__()
        fakeROM = FakeROM(dictROM)
        self.romReader = RomReader(fakeROM, magic)

class RomLoaderJson(RomLoaderDict):
    # when called from the test suite and the website (when loading already uploaded roms converted to json)
    def __init__(self, jsonFileName, magic=None):
        with open(jsonFileName) as jsonFile:
            tmpDictROM = json.load(jsonFile)
            # in json keys are strings
            dictROM = {int(address): data for address, data in tmpDictROM.items()}
            super(RomLoaderJson, self).__init__(dictROM, magic)
