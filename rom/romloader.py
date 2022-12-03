import os, json

from rom.rom_patches import RomPatches
from rom.rom import RealROM, FakeROM
from rom.romreader import RomReader
from utils.doorsmanager import DoorsManager
from graph.graph_utils import getAccessPoint
from collections import defaultdict

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
        isArea = False
        isBoss = False
        isEscape = False

        # check total base (blue bt and red tower blue door)
        if self.hasPatch("startCeres") or self.hasPatch("startLS"):
            RomPatches.ActivePatches += [RomPatches.BlueBrinstarBlueDoor,
                                         RomPatches.RedTowerBlueDoors]

        if self.hasPatch("newGame"):
            RomPatches.ActivePatches.append(RomPatches.RedTowerBlueDoors)

        # check total soft lock protection
        if self.hasPatch("layout"):
            RomPatches.ActivePatches += RomPatches.TotalLayout

        # check total casual (blue brinstar missile swap)
        if self.hasPatch("casual"):
            RomPatches.ActivePatches.append(RomPatches.BlueBrinstarMissile)

        # check gravity heat protection
        if self.hasPatch("gravityNoHeatProtection"):
            RomPatches.ActivePatches.append(RomPatches.NoGravityEnvProtection)

        if self.hasPatch("progressiveSuits"):
            RomPatches.ActivePatches.append(RomPatches.ProgressiveSuits)
        if self.hasPatch("nerfedCharge"):
            RomPatches.ActivePatches.append(RomPatches.NerfedCharge)
        if self.hasPatch('nerfedRainbowBeam'):
            RomPatches.ActivePatches.append(RomPatches.NerfedRainbowBeam)

        # check varia tweaks
        if self.hasPatch("variaTweaks"):
            RomPatches.ActivePatches += RomPatches.VariaTweaks

        # check area
        if self.hasPatch("area"):
            RomPatches.ActivePatches += [RomPatches.SingleChamberNoCrumble,
                                         RomPatches.AreaRandoGatesBase,
                                         RomPatches.AreaRandoBlueDoors,
                                         RomPatches.CrocBlueDoors,
                                         RomPatches.CrabShaftBlueDoor,
                                         RomPatches.MaridiaSandWarp,
                                         RomPatches.AreaRandoMoreBlueDoors]
            isArea = True

        # check area layout
        if self.hasPatch("areaLayout"):
            RomPatches.ActivePatches.append(RomPatches.AreaRandoGatesOther)
        if self.hasPatch("traverseWreckedShip"):
            RomPatches.ActivePatches += [RomPatches.EastOceanPlatforms, RomPatches.SpongeBathBlueDoor]
        if self.hasPatch("aqueductBombBlocks"):
            RomPatches.ActivePatches.append(RomPatches.AqueductBombBlocks)

        # check boss rando
        isBoss = self.isBoss()

        # check escape rando
        isEscape = self.hasPatch("areaEscape")

        # minimizer
        if self.hasPatch("minimizer_bosses"):
            RomPatches.ActivePatches.append(RomPatches.NoGadoras)
        if self.hasPatch("open_zebetites"):
            RomPatches.ActivePatches.append(RomPatches.OpenZebetites)

        # red doors
        if self.hasPatch('red_doors'):
            RomPatches.ActivePatches.append(RomPatches.RedDoorsMissileOnly)

        # Tourian
        tourian = 'Vanilla'
        if self.hasPatch("minimizer_tourian"):
            RomPatches.ActivePatches.append(RomPatches.TourianSpeedup)
            tourian = 'Fast'
        if bool(self.readOption("escapeTrigger")):
            RomPatches.ActivePatches.append(RomPatches.NoTourian)
            tourian = 'Disabled'

        # objectives
        hasObjectives = self.hasPatch('objectives')

        # Round robin CF
        if self.hasPatch('round_robin_cf'):
            RomPatches.ActivePatches.append(RomPatches.RoundRobinCF)

        return (isArea, isBoss, isEscape, hasObjectives, tourian)

    def getPatches(self):
        return self.romReader.getPatches()

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

    def getAdditionalEtanks(self):
        return self.romReader.getAdditionalEtanks()

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
            dictROM = {}
            # in json keys are strings
            for address in tmpDictROM:
                dictROM[int(address)] = tmpDictROM[address]
            super(RomLoaderJson, self).__init__(dictROM, magic)
