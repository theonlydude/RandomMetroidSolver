import os, random, re, json

from math import ceil
from enum import IntFlag
from collections import defaultdict
from rando.Items import ItemManager
from rom.compression import Compressor
from rom.ips import IPS_Patch
from utils.doorsmanager import DoorsManager, IndicatorFlag
from utils.objectives import Objectives
from graph.graph_utils import GraphUtils, getAccessPoint, graphAreas, gameAreas
from graph.flags import BossAccessPointFlags
from logic.logic import Logic
from rom.rom import RealROM, FakeROM, snes_to_pc, pc_to_snes
from rom.addresses import Addresses
from rom.rom_patches import RomPatches, getPatchSet, getPatchSetsFromPatcherSettings
from rom.rom_options import RomOptions
from rom.flavor import RomFlavor
from rom.map import AreaMap, getTileIndex, portal_mapicons, areaSpriteMaps
from rom.enemies_objectives_data import enemies_objectives_data
from patches.patchaccess import PatchAccess
from utils.parameters import appDir, Settings
from logic.helpers import Bosses
import utils.log

def getWord(w):
    return (w & 0x00FF, (w & 0xFF00) >> 8)

def getWordBytes(addr):
    w = getWord(addr & 0xffff)
    return [w[0], w[1]]

class RomPatcher:
    def __init__(self, settings=None, romFileName=None, magic=None):
        self.log = utils.log.get('RomPatcher')
        self.settings = settings
        self.romFileName = romFileName
        self.patchAccess = RomFlavor.patchAccess
        self.symbols = RomFlavor.symbols
        self.race = None
        if romFileName == None:
            self.romFile = FakeROM()
        else:
            self.romFile = RealROM(romFileName)
        self.romOptions = RomOptions(self.romFile, self.symbols)
        if magic is not None:
            from rom.race_mode import RaceModePatcher
            self.race = RaceModePatcher(self, magic)
        # IPS_Patch objects list
        self.ipsPatches = []
        # loc name to alternate address. we still write to original
        # address to help the RomReader.
        self.altLocsAddresses = {}
        # specific fixes for area rando connections
        self.roomConnectionSpecific = {
            # fix scrolling sky when transitioning to west ocean
            0x93fe: self.patchWestOcean
        }
        self.doorConnectionSpecific = {
            # get out of kraid room: reload CRE
            0x91ce: self.forceRoomCRE,
            # get out of croc room: reload CRE
            0x93ea: self.forceRoomCRE
        }
        # TODO create vertical maps for rotation
        self.areaMaps = defaultdict(AreaMap)

    def patchRom(self):
        self._mapIconTableAddr = Addresses.getOne("map_mapicons_tables")
        self._accessibleAreasNoBoss = self._getAccessibleAreasNoBoss(self.settings["itemLocs"])
        self._updateMapIconsGraphAreas(self.settings["itemLocs"])
        # apply patches first
        self.applyIPSPatches()
        self.commitIPS()
        # apply ROM options on top of patches
        self.romOptions.write('escapeTrigger', int(self.settings["tourian"] == "Disabled"))
        self.romOptions.write('escapeTriggerCrateria', int(not self.settings['isPlando']))
        if self.settings['escapeRandoRemoveEnemies'] is not None:
            self.romOptions.write('escapeRandoRemoveEnemies', int(self.settings['escapeRandoRemoveEnemies']))
        self.romOptions.write('objectivesSFX', 0 if self.settings['vanillaObjectives'] else 0x80)
        self.romOptions.write("objectivesHidden", 0 if not Objectives.hidden else 0x2)
        if self.settings["tourian"] == "Fast" and self.settings["area"] == False:
            # skip Tourian entrance full refill if not area rando
            # (we actually overwrite code, so we actually decide the condition before writing this time)
            self.romOptions.write("fastTourianSkipRefill", 0x60) # RTS
        # write seed data
        if not self.settings["isPlando"]:
            self.writeSeed(self.settings["seed"]) # lol if race mode
        # items/locs
        self.writeItemsLocs(self.settings["itemLocs"])
        self.writeSplitLocs(self.settings["majorsSplit"], self.settings["itemLocs"], self.settings["progItemLocs"])
        self.writeItemMapTiles(self.settings["majorsSplit"], self.settings["itemLocs"])
        self.writeItemsNumber()
        # objectives
        self.writeObjectives(self.settings["itemLocs"], self.settings["tourian"])
        self.writeObjectivesMapIcons(self.settings["tourian"])
        # area/boss connections
        self.writeDoorConnections(self.settings["doors"])
        self.writeDoorConnectionsMapIcons(self.settings["doors"], self.settings["tourian"])
        # door caps
        self.writeDoorsColor()
        self.writeDoorsMapIcons()
        # map tile count
        self.writeMapTileCount(self.settings["area"], self.settings["escapeAttr"] is not None, self.settings["tourian"])
        # credits stuff
        self.writeSpoiler(self.settings["itemLocs"], self.settings["progItemLocs"])
        self.writeRandoSettings(self.settings["randoSettings"], self.settings["itemLocs"])
        self.writeEndscreenTables(self.settings["itemLocs"])
        assert self._mapIconTableAddr <= Addresses.getOne("map_mapicons_tables_limit"), "Map icons table overflow"

        self.writeVersion(self.settings["displayedVersion"])
        if self.settings["ctrlDict"] is not None:
            self.writeControls(self.settings["ctrlDict"])
        if self.settings["moonWalk"] == True:
            self.enableMoonWalk()

        self.writeMagic()
        self.writeMajorsSplit(self.settings["majorsSplit"])
        self.writeStartingEnergy(self.settings["starting_energy"])

        if self.settings["isPlando"] and self.race is None:
            doorsPtrs = GraphUtils.getAps2DoorsPtrs()
            self.writePlandoTransitions(self.settings["plando"]["graphTrans"], doorsPtrs,
                                        self.settings["plando"]["maxTransitions"])
            self.writePlandoAddresses(self.settings["plando"]["visitedLocations"])
        if self.settings["isPlando"] and self.settings["escapeAttr"] is not None:
            self.removeAnimalsHunt()

        self.end()

    def end(self):
        self.romFile.fillToNextBank()
        self.romFile.close()

    def writeItemCode(self, item, visibility, address):
        itemCode = ItemManager.getItemTypeCode(item, visibility)
        self.writePlmWord(itemCode, address)

    def writePlmWord(self, word, address=None):
        if self.race is None:
            self.romFile.writeWord(word, address)
        else:
            self.race.writePlmWord(word, address)

    def writeWordMagic(self, word, address=None):
        if self.race is None:
            self.romFile.writeWord(word, address)
        else:
            self.race.writeWordMagic(word, address)

    def getLocAddresses(self, loc):
        ret = [loc.Address]
        if loc.Name in self.altLocsAddresses:
            ret.append(self.altLocsAddresses[loc.Name])
        return ret

    def writeItem(self, itemLoc):
        loc = itemLoc.Location
        if loc.isBoss():
            raise ValueError('Cannot write Boss location')
        self.log.debug('write {} at {}@{}'.format(itemLoc.Item.Type, loc.Name, hex(pc_to_snes(loc.Address))))
        for addr in self.getLocAddresses(loc):
            self.writeItemCode(itemLoc.Item, loc.Visibility, addr)

    def writeItemsLocs(self, itemLocs):
        self.nItems = 0
        for itemLoc in itemLocs:
            loc = itemLoc.Location
            item = itemLoc.Item
            if loc.isBoss():
                continue
            self.writeItem(itemLoc)
            if item.Category != 'Nothing':
                if not loc.restricted:
                    self.nItems += 1
                if loc.Name == 'Morphing Ball':
                    self.patchMorphBallEye(item)

    def writeSplitLocs(self, split, itemLocs, progItemLocs):
        majChozoCheck = lambda itemLoc: itemLoc.Item.Class == split and itemLoc.Location.isClass(split)
        fullCheck = lambda itemLoc: itemLoc.Location.Id is not None and itemLoc.Location.BossItemType is None
        splitChecks = {
            'Full': fullCheck,
            'Scavenger': fullCheck,
            'Major': majChozoCheck,
            'Chozo': majChozoCheck,
            'FullWithHUD': lambda itemLoc: itemLoc.Item.Category not in ['Energy', 'Ammo', 'Boss', 'MiniBoss']
        }
        itemLocCheck = lambda itemLoc: itemLoc.Item.Category != "Nothing" and splitChecks[split](itemLoc)
        for area in graphAreas:
            locs = [il.Location for il in itemLocs if itemLocCheck(il) and il.Location.GraphArea == area and not il.Location.restricted]
            self.log.debug("writeSplitLocs. area="+area)
            self.log.debug(str([loc.Name for loc in locs]))
            addr = Addresses.getOne('objectives_locs_'+area)
            self.romFile.seek(addr)
            for loc in locs:
                self.romFile.writeByte(loc.Id)
            self.romFile.writeByte(0xff)
        if split == "Scavenger":
            # write required major item order
            self.romFile.seek(Addresses.getOne('scavengerOrder'))
            for itemLoc in progItemLocs:
                self.romFile.writeWord((itemLoc.Location.Id << 8) | itemLoc.Location.HUD)
            # bogus loc ID | "HUNT OVER" index
            self.romFile.writeWord(0xff11)
            # fill remaining list with 0xFFFF to avoid issue with plandomizer having less items than in the base seed
            for i in range(18-len(progItemLocs)):
                self.romFile.writeWord(0xffff)

    def writeItemMapTiles(self, split, itemLocs):
        for il in itemLocs:
            if il.Location.isBoss():
                continue
            if not il.Location.SolveArea.endswith("Boss") and il.Location.GraphArea not in self._accessibleAreasNoBoss:
                continue
#            print("loc %s, area %s" % (il.Location.Name, il.Location.Area))
            self.areaMaps[il.Location.Area].setItemLoc(il, split)
        itemMaskOffset = Addresses.getOne("map_ItemTileCheckList")
        for area, areaMap in self.areaMaps.items():
            mapOffset = Addresses.getOne("map_data_" + area)
            areaMap.writeItemTiles(self.romFile, mapOffset, itemMaskOffset)

    # trigger morph eye enemy on whatever item we put there,
    # not just morph ball
    def patchMorphBallEye(self, item):
#        print('Eye item = ' + item.Type)
        isAmmo = item.Category == 'Ammo'
        # category to check
        if ItemManager.isBeam(item):
            cat = 0xA8 # collected beams
        elif item.Type == 'ETank':
            cat = 0xC4 # max health
        elif item.Type == 'Reserve':
            cat = 0xD4 # max reserves
        elif item.Type == 'Missile':
            cat = 0xC8 # max missiles
        elif item.Type == 'Super':
            cat = 0xCC # max supers
        elif item.Type == 'PowerBomb':
            cat = 0xD0 # max PBs
        else:
            cat = 0xA4 # collected items
        # comparison/branch instruction
        # the branch is taken if we did NOT collect item yet
        if item.Category == 'Energy' or isAmmo:
            comp = 0xC9 # CMP (immediate)
            branch = 0x30 # BMI
        else:
            comp = 0x89 # BIT (immediate)
            branch = 0xF0 # BEQ
        # what to compare to
        if item.Type == 'ETank':
            operand = 0x65 # < 100
        elif item.Type == 'Reserve' or isAmmo:
            operand = 0x1 # < 1
        elif ItemManager.isBeam(item):
            operand = item.BeamBits
        else:
            operand = item.ItemBits
        self.patchMorphBallCheck(Addresses.getOne('morphEyeAI'), cat, comp, operand, branch)
        self.patchMorphBallCheck(Addresses.getOne('morphHeadAI'), cat, comp, operand, branch)

    def patchMorphBallCheck(self, offset, cat, comp, operand, branch):
        # actually patch enemy AI
        self.romFile.writeByte(cat, offset)
        self.romFile.writeByte(comp, offset+2)
        self.romFile.writeWord(operand)
        self.romFile.writeByte(branch)

    def writeItemsNumber(self):
        # write total number of actual items for item percentage patch (patch the patch)
        for addr in Addresses.getAll('totalItems'):
            self.romFile.writeByte(self.nItems, addr)

        # for X% collected items objectives, precompute values and write them in objectives functions
        for percent, addr in zip([25, 50, 75, 100], Addresses.getAll('totalItemsPercent')):
            self.romFile.writeWord(ceil((self.nItems * percent)/100), addr)

    def addIPSPatches(self, patches):
        for patchName in patches:
            self.applyIPSPatch(patchName)

    def customShip(self, ship):
        # gfx
        self.applyIPSPatch(ship, ipsDir='varia_custom_sprites/patches/ship')
        # layout
        self.applyIPSPatch(ship, ipsDir='varia_custom_sprites/patches/ship/{}'.format(Logic.implementation))

    def purgeSprite(self):
        # custom sprites are also modifying ship palettes, so remove these records from the custom sprite
        paletteShip = [Addresses.getOne('paletteShip_1'), Addresses.getOne('paletteShip_2')]
        paletteShip7 = [Addresses.getOne('paletteShip7_1'), Addresses.getOne('paletteShip7_2')]
        paletteShipGlow = [Addresses.getOne('paletteShipGlow_1'), Addresses.getOne('paletteShipGlow_2')]
        spriteIps = self.ipsPatches[-1]
        spriteIps = spriteIps.toDict()
        filteredDict ={}
        for keyLow, data in spriteIps.items():
            dataLength = len(data)
            keyHigh = keyLow + dataLength
            if ((keyHigh < paletteShip[0] or keyLow >= paletteShip[1]) and
                (keyHigh < paletteShip7[0] or keyLow >= paletteShip7[1]) and
                (keyHigh < paletteShipGlow[0] or keyLow >= paletteShipGlow[1])):
                filteredDict[keyLow] = data
        self.ipsPatches[-1] = IPS_Patch(filteredDict)

    def customSprite(self, sprite, customNames, noSpinAttack, purge):
        sprite = "{}.ips".format(sprite)
        self.applyIPSPatch(sprite, ipsDir='varia_custom_sprites/patches/samus')

        if purge:
            self.purgeSprite()

        if noSpinAttack == True:
            self.applyIPSPatch('SpriteSomething_Disable_Spin_Attack')

        if not customNames:
            return

        from varia_custom_sprites.custom_sprites import messageBoxes

        messageBoxes['samus_upside_down_and_backwards.ips'] = messageBoxes['samus_backwards.ips']
        vFlip = ['samus_upside_down.ips', 'samus_upside_down_and_backwards.ips']
        hFlip = ['samus_backwards.ips']
        doVFlip = sprite in vFlip
        doHFlip = sprite in hFlip
        if (doVFlip or doHFlip) and sprite not in messageBoxes:
            sprite = 'vanilla'
        if sprite in messageBoxes:
            messageBox = MessageBox(self.romFile)
            for (messageKey, newMessage) in messageBoxes[sprite].items():
                messageBox.updateMessage(messageKey, newMessage, doVFlip, doHFlip)

    def getPatchSetsFromSettings(self):
        return getPatchSetsFromPatcherSettings(self.settings)

    def applyPatchSet(self, patchSetName, plms):
        patchSet = getPatchSet(patchSetName, RomFlavor.flavor)
        ipsPatches = patchSet.get('ips', [])
        for ips in ipsPatches:
            self.applyIPSPatch(ips)
        plmList = patchSet.get('plms', [])
        plms += [plm for plm in plmList if plm not in plms]

    def removeMinimizerUnusedAreas(self):
        # remove map tiles
        allAreas = list(self._accessibleAreasNoBoss) + ['Ceres', 'Tourian']
        missingAreas = [area for area in graphAreas if area not in allAreas]
        removeAreaPatches = [f"remove_{area}.ips" for area in missingAreas]
        for patch in removeAreaPatches:
            self.applyIPSPatch(patch)
        # remove spritemaps above elevators
        spritemapsRemoved = {
            "Crateria": {
                "Brinstar Left": "GreenPinkBrinstar",
                "Brinstar Middle": "Crateria",
                "Brinstar Right": "RedBrinstar",
                "Wrecked Ship": "WreckedShip",
                "Maridia": "EastMaridia"
            },
            "Brinstar": {
                "Crateria Left": "GreenPinkBrinstar",
                "Crateria Middle": "Crateria",
                "Crateria Right": "RedBrinstar",
                "Maridia": "RedBrinstar",
                "Norfair": "Norfair"
            },
            "Norfair": {
                "Brinstar": "Norfair"
            },
            "Maridia": {
                "Crateria": "EastMaridia",
                "Brinstar Left": "RedBrinstar",
                "Brinstar Right": "RedBrinstar"
            }
        }
        spritemaps = areaSpriteMaps[RomFlavor.flavor]
        for area, areaData in spritemaps.items():
            self.romFile.seek(snes_to_pc(areaData["addr"]))
            for iconName, icon in areaData["icons"].items():
                graphArea = spritemapsRemoved[area][iconName]
                if graphArea in missingAreas:
                    continue
                self.romFile.writeWord(icon["x"])
                self.romFile.writeWord(icon["y"])
                self.romFile.writeWord(icon["type"])
            self.romFile.writeWord(0xffff)

    def applyIPSPatches(self):
        try:
            ## apply base patches, then special patches, PLMs and other modifications, then optional patches
            plms = []
            patchSets = self.getPatchSetsFromSettings()
            for patchSet in patchSets:
                self.applyPatchSet(patchSet, plms)
            deadEnds, corridors = GraphUtils.getDeadEndsAndCorridors(Objectives.graph, self.settings["boss"])
            for deadEnd in deadEnds:
                self.applyPatchSet(f"dead_end_{deadEnd}", plms)
            for corridor in corridors:
                self.applyPatchSet(f"corridor_{corridor}", plms)
            if self.settings["boss"]:
                self.writeBossDoors(self.settings["boss"], Objectives.graph, plms)
            # special patches
            if self.race is not None:
                self.applyIPSPatch('race_mode_post.ips')
            # show objectives and Tourian status in a shortened intro sequence
            # if not full vanilla objectives+tourian
            if not self.settings["vanillaObjectives"] or self.settings["tourian"] != "Vanilla":
                self.applyIPSPatch("Restore_Intro") # important to apply this after start.ips
                self.applyIPSPatch("intro_text.ips")
            if (self.settings["majorsSplit"] == 'Scavenger'
                and any(il for il in self.settings["progItemLocs"] if il.Location.Name == "Ridley")):
                # ridley as scav loc
                self.applyIPSPatch("Blinking[RidleyRoomIn]")
            # random escape
            if self.settings["escapeAttr"] is not None:
                # animals and timer
                self.applyEscapeAttributes(self.settings["escapeAttr"], plms)
            # VARIA area IDs/minimap room types/area map palettes
            if self.settings["area"] == False:
                self.applyIPSPatch('area_ids_vanilla_layout.ips')
                self.applyIPSPatch('minimap_data_vanilla_layout.ips')
                self.applyIPSPatch('map_data_area_alt.ips')
            else:
                self.applyIPSPatch('area_ids_area_rando.ips')
                self.applyIPSPatch('minimap_data_area_rando.ips')
            if self.settings["minimizerN"] is not None:
                self.removeMinimizerUnusedAreas()
            # blue doors
            doors = self.getStartDoors(plms, self.settings["area"], self.settings["minimizerN"])
            DoorsManager.getBlueDoors(doors)
            # door indicators
            if "door_indicators_plms" in patchSets:
                self.writeDoorIndicators(plms, self.settings["area"], self.settings["doorsColorsRando"])
            # starting locations
            self.applyStartAP(self.settings["startLocation"], plms, doors)
            # patch PLMs
            self.applyPLMs(plms)

            # apply optional patches
            for patchName in self.settings["optionalPatches"]:
                self.applyIPSPatch(patchName)
        except Exception as e:
            raise Exception("Error patching {}. ({})".format(self.romFileName, e))

    def applyIPSPatch(self, patchName, patchDict=None, ipsDir=None):
        if patchDict is None:
            patchDict = self.patchAccess.getDictPatches()
        print("Apply patch {}".format(patchName))
        if patchName in patchDict:
            patch = IPS_Patch(patchDict[patchName])
        else:
            # look for ips file
            if ipsDir is None:
                patch = IPS_Patch.load(self.patchAccess.getPatchPath(patchName))
            else:
                patch = IPS_Patch.load(os.path.join(appDir, ipsDir, patchName))
        self.ipsPatches.append(patch)

    def getStartDoors(self, plms, area, minimizerN):
        doors = [0x10] # red brin elevator
        def addBlinking(name):
            key = 'Blinking[{}]'.format(name)
            if key in self.patchAccess.getDictPatches():
                self.applyIPSPatch(key)
            if key in self.patchAccess.getAdditionalPLMs():
                plms.append(key)
        if area == True:
            plms += ['Maridia Sand Hall Seal', "Save_Main_Street", "Save_Crab_Shaft"]
            for accessPoint in Logic.accessPoints():
                if accessPoint.Internal == True or accessPoint.Boss == True:
                    continue
                addBlinking(accessPoint.Name)
            addBlinking("West Sand Hall Left")
            addBlinking("Below Botwoon Energy Tank Right")
        if minimizerN is not None:
            # add blinking doors inside and outside boss rooms
            for accessPoint in Logic.accessPoints():
                if accessPoint.Boss:
                    addBlinking(accessPoint.Name)
        return doors

    def applyStartAP(self, apName, plms, doors):
        ap = getAccessPoint(apName)
        # if start loc is not Ceres or Landing Site, or the ceiling loc picked up before morph loc,
        # Zebes will be awake and morph loc item will disappear.
        # this PLM ensures the item will be here whenever zebes awakes
        plms.append('Morph_Zebes_Awake')
        (w0, w1) = getWord(ap.Start['spawn'])
        patchDict = {
            'StartAP': {
                Addresses.getOne('startAP'): [w0, w1]
            }
        }
        if 'doors' in ap.Start:
            doors += ap.Start['doors']
        doors.append(0x0)
        doorsAddr = Addresses.getOne('start_opt_doors')
        assert (doorsAddr + len(doors)) < Addresses.getOne('start_startup'), "Stopped before start code overwrite"
        patchDict["StartAP"][doorsAddr] = doors
        self.applyIPSPatch('StartAP', patchDict)
        # handle custom saves
        if 'save' in ap.Start:
            self.applyIPSPatch(ap.Start['save'])
            plms.append(ap.Start['save'])
        # handle optional rom patches
        if 'rom_patches' in ap.Start:
            for patch in ap.Start['rom_patches']:
                self.applyIPSPatch(patch)

    def applyEscapeAttributes(self, escapeAttr, plms):
        # timer
        escapeTimer = escapeAttr['Timer']
        if escapeTimer is not None:
            patchDict = { 'Escape_Timer': {} }
            timerPatch = patchDict["Escape_Timer"]
            def getTimerBytes(t):
                minute = int(t / 60)
                second = int(t % 60)
                minute = int(minute / 10) * 16 + minute % 10
                second = int(second / 10) * 16 + second % 10
                return [second, minute]
            def calcTimer(t):
                a, b = Settings.algoSettings['escapeRandoTimeComputeParams']
                div = a * Settings.skillScore + b
                t = t / div
                return 5 * ceil(t / 5)
            if 'TimerTable' not in escapeAttr:
                t = calcTimer(escapeTimer)
#                print(f"escapeTimer = {escapeTimer}, t = {t}")
                timerPatch[Addresses.getOne('escapeTimer')] = getTimerBytes(t)
                timerPatch[Addresses.getOne("rando_escape_common_timer_half_value")] = getTimerBytes(t/2)
            else:
                # timer table for Disabled Tourian escape: write 0 time as marker to use the table
                timerPatch[Addresses.getOne('escapeTimer')] = [0,0]
                tableBytes = []
                halfTableBytes = []
                timerPatch[Addresses.getOne('escapeTimerTable')] = tableBytes
                timerPatch[Addresses.getOne('rando_escape_common_timer_half_values_by_area_id')] = halfTableBytes
                for area in graphAreas[1:-1]: # no Ceres or Tourian
                    t = calcTimer(escapeAttr['TimerTable'][area])
                    tableBytes += getTimerBytes(t)
                    halfTableBytes += getTimerBytes(t/2)
            self.applyIPSPatch('Escape_Timer', patchDict)
        # animals door to open
        if escapeAttr['Animals'] is not None:
            escapeOpenPatches = {
                'Green Brinstar Main Shaft Top Left':'Escape_Animals_Open_Brinstar',
                'Business Center Mid Left':"Escape_Animals_Open_Norfair",
                'Crab Hole Bottom Right':"Escape_Animals_Open_Maridia",
            }
            if escapeAttr['Animals'] in escapeOpenPatches:
                plms.append("WS_Map_Grey_Door")
                self.applyIPSPatch(escapeOpenPatches[escapeAttr['Animals']])
            else:
                plms.append("WS_Map_Grey_Door_Openable")
        else:
            plms.append("WS_Map_Grey_Door")
        # optional patches (enemies, scavenger)
        if 'patches' in escapeAttr:
            for patch in escapeAttr['patches']:
                self.applyIPSPatch(patch)

    # adds ad-hoc "IPS patches" for additional PLM tables
    def applyPLMs(self, plms):
        # compose a dict (room, state, door) => PLM array
        # 'PLMs' being a 6 byte arrays
        plmDict = {}
        # we might need to update locations addresses on the fly
        plmLocs = {} # room key above => loc name
        additionalPLMs = self.patchAccess.getAdditionalPLMs()
        for p in plms:
            print("Apply plm {}".format(p))
            plm = additionalPLMs[p]
            room = plm['room']
            state = 0
            if 'state' in plm:
                state = plm['state']
            door = 0
            if 'door' in plm:
                door = plm['door']
            k = (room, state, door)
            if k not in plmDict:
                plmDict[k] = []
            plmDict[k] += plm['plm_bytes_list']
            if 'locations' in plm:
                locList = plm['locations']
                for locName, locIndex in locList:
                    plmLocs[(k, locIndex)] = locName
        # make two patches out of this dict
        plmTblAddr = Addresses.getOne('plmSpawnTable') # moves downwards
        plmPatchData = []
        roomTblAddr = Addresses.getOne('plmSpawnRoomTable') # moves upwards
        roomPatchData = []
        plmTblOffset = plmTblAddr
        def appendPlmBytes(bytez):
            nonlocal plmPatchData, plmTblOffset
            plmPatchData += bytez
            plmTblOffset += len(bytez)
        def addRoomPatchData(bytez):
            nonlocal roomPatchData, roomTblAddr
            roomPatchData = bytez + roomPatchData
            roomTblAddr -= len(bytez)
        for roomKey, plmList in plmDict.items():
            entryAddr = plmTblOffset
            roomData = []
            for i in range(len(plmList)):
                plmBytes = plmList[i]
                assert len(plmBytes) == 6, "Invalid PLM entry for roomKey " + str(roomKey) + ": PLM list len is " + str(len(plmBytes))
                if (roomKey, i) in plmLocs:
                    self.altLocsAddresses[plmLocs[(roomKey, i)]] = plmTblOffset
                appendPlmBytes(plmBytes)
            appendPlmBytes([0x0, 0x0]) # list terminator
            def appendRoomWord(w, data):
                (w0, w1) = getWord(w)
                data += [w0, w1]
            for i in range(3):
                appendRoomWord(roomKey[i], roomData)
            appendRoomWord(entryAddr, roomData)
            addRoomPatchData(roomData)
        # write room table terminator
        addRoomPatchData([0x0] * 8)
        assert plmTblOffset < roomTblAddr, "Spawn PLM table overlap. PLM table offset is 0x%x, Room table address is 0x%x" % (plmTblOffset,roomTblAddr)
        self.log.debug(f"finished PLM table: {plmTblOffset - plmTblAddr} bytes, {roomTblAddr - plmTblOffset} bytes left")
        patchDict = {
            "PLM_Spawn_Tables" : {
                plmTblAddr: plmPatchData,
                roomTblAddr: roomPatchData
            }
        }
        self.applyIPSPatch("PLM_Spawn_Tables", patchDict)

    def commitIPS(self):
        self.romFile.ipsPatch(self.ipsPatches)

    def writeSeed(self, seed):
        random.seed(seed)
        seedInfo = random.randint(0, 0xFFFF)
        seedInfo2 = random.randint(0, 0xFFFF)
        self.romFile.writeWord(seedInfo, Addresses.getOne('seed_display_seed_value'))
        self.romFile.writeWord(seedInfo2)

    def writeMagic(self):
        if self.race is not None:
            self.race.writeMagic()

    def writeMajorsSplit(self, majorsSplit):
        address = Addresses.getOne('majorsSplit')
        splits = {
            'Chozo': 'Z',
            'Major': 'M',
            'FullWithHUD': 'H',
            'Scavenger': 'S'
        }
        char = splits.get(majorsSplit, 'F')
        self.romFile.writeByte(ord(char), address)

    def getItemQty(self, itemLocs, itemType):
        return len([il for il in itemLocs if il.Accessible and il.Item.Type == itemType])

    def getMinorsDistribution(self, itemLocs):
        dist = {}
        minQty = 100
        minors = ['Missile', 'Super', 'PowerBomb']
        for m in minors:
            # in vcr mode if the seed has stuck we may not have these items, return at least 1
            q = float(max(self.getItemQty(itemLocs, m), 1))
            dist[m] = {'Quantity' : q }
            if q < minQty:
                minQty = q
        for m in minors:
            dist[m]['Proportion'] = dist[m]['Quantity']/minQty

        return dist

    def getAmmoPct(self, minorsDist):
        q = 0
        for m,v in minorsDist.items():
            q += v['Quantity']
        return 100*q/66

    def writeRandoSettings(self, settings, itemLocs):
        dist = self.getMinorsDistribution(itemLocs)
        totalAmmo = sum(d['Quantity'] for ammo,d in dist.items())
        totalItemLocs = sum(1 for il in itemLocs if il.Accessible and not il.Location.isBoss())
        totalNothing = sum(1 for il in itemLocs if il.Accessible and il.Item.Category == 'Nothing')
        totalEnergy = self.getItemQty(itemLocs, 'ETank')+self.getItemQty(itemLocs, 'Reserve')
        totalMajors = max(totalItemLocs - totalEnergy - totalAmmo - totalNothing, 0)
        address = Addresses.getOne("credits_credits_items_distrib")
        value = "{:>2}".format(totalItemLocs)
        line = " ITEM LOCATIONS              %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " item locations ............ %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        maj = "{:>2}".format(int(totalMajors))
        htanks = "{:>2}".format(int(totalEnergy))
        ammo = "{:>2}".format(int(totalAmmo))
        blank = "{:>2}".format(int(totalNothing))
        line = "  MAJ %s EN %s AMMO %s BLANK %s " % (maj, htanks, ammo, blank)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40
        line = "  maj %s en %s ammo %s blank %s " % (maj, htanks, ammo, blank)
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        pbs = "{:>2}".format(int(dist['PowerBomb']['Quantity']))
        miss = "{:>2}".format(int(dist['Missile']['Quantity']))
        supers = "{:>2}".format(int(dist['Super']['Quantity']))
        line = " AMMO PACKS  MI %s SUP %s PB %s " % (miss, supers, pbs)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " ammo packs  mi %s sup %s pb %s " % (miss, supers, pbs)
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        etanks = "{:>2}".format(int(self.getItemQty(itemLocs, 'ETank')))
        reserves = "{:>2}".format(int(self.getItemQty(itemLocs, 'Reserve')))
        line = " HEALTH TANKS         E %s R %s " % (etanks, reserves)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " health tanks ......  e %s r %s " % (etanks, reserves)
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x80

        value = " "+settings.progSpeed.upper()
        line = " PROGRESSION SPEED ....%s " % value.rjust(8, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        line = " PROGRESSION DIFFICULTY  %s " % settings.progDiff.upper()
        self.writeCreditsString(address, 0x04, line)
        address += 0x80 # skip item distrib title

        param = (' SUITS RESTRICTION ........%s', 'Suits')
        line = param[0] % ('. ON' if settings.restrictions[param[1]] == True else ' OFF')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        value = " "+settings.restrictions['Morph'].upper()
        line  = " MORPH PLACEMENT .....%s" % value.rjust(9, '.')
        self.writeCreditsString(address, 0x04, line)
        address += 0x40

        for superFun in [(' SUPER FUN COMBAT .........%s', 'Combat'),
                         (' SUPER FUN MOVEMENT .......%s', 'Movement'),
                         (' SUPER FUN SUITS ..........%s', 'Suits')]:
            line = superFun[0] % ('. ON' if superFun[1] in settings.superFun else ' OFF')
            self.writeCreditsString(address, 0x04, line)
            address += 0x40

        value = "%.1f %.1f %.1f" % (dist['Missile']['Proportion'], dist['Super']['Proportion'], dist['PowerBomb']['Proportion'])
        line = " AMMO DISTRIBUTION  %s " % value
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40

        line = " ammo distribution  %s " % value
        self.writeCreditsStringBig(address, line, top=False)
        address += 0x40

        # write ammo/energy pct
        address = Addresses.getOne("credits_credits_items_distrib_continued")
        (ammoPct, energyPct) = (int(self.getAmmoPct(dist)), int(100*totalEnergy/18))
        line = " AVAILABLE AMMO {:>3}% ENERGY {:>3}%".format(ammoPct, energyPct)
        self.writeCreditsStringBig(address, line, top=True)
        address += 0x40
        line = " available ammo {:>3}% energy {:>3}%".format(ammoPct, energyPct)
        self.writeCreditsStringBig(address, line, top=False)

    def writeEndscreenTables(self, itemLocs):
        # energy/ammo: write number of packs
        minorTypes = ItemManager.getCategoryTypes('Ammo') + ItemManager.getCategoryTypes('Energy')
        qtyOffset = 6
        for itemType in minorTypes:
            addr = Addresses.getOne("credits_minors_table_entry_" + itemType) + qtyOffset
            self.romFile.writeWord(self.getItemQty(itemLocs, itemType), addr)
        # upgrades: if missing, write 0 as collected RAM ptr
        missingMajors = [itemType for itemType in ItemManager.getUpgradeTypes() if not any(il.Item.Type == itemType for il in itemLocs)]
        collectedOffset = 4
        for itemType in missingMajors:
            addr = Addresses.getOne("credits_majors_table_entry_" + itemType) + collectedOffset
            self.romFile.writeWord(0, addr)

    def writeSpoiler(self, itemLocs, progItemLocs=None):
        # keep only majors
        fItemLocs = [il for il in itemLocs if il.Item.Category not in ['Ammo', 'Nothing', 'Energy', 'Boss']]
        # add location of the first instance of each minor
        for t in ['Missile', 'Super', 'PowerBomb']:
            itLoc = None
            if progItemLocs is not None:
                itLoc = next((il for il in progItemLocs if il.Item.Type == t), None)
            if itLoc is None:
                itLoc = next((il for il in itemLocs if il.Item.Type == t), None)
            if itLoc is not None: # in vcr mode if the seed has stucked we may not have these minors
                fItemLocs.append(itLoc)
        regex = re.compile(r"[^A-Z0-9\.,'!: ]+")

        itemLocs = {}
        for iL in fItemLocs:
            itemLocs[iL.Item.Name] = iL.Location.Name

        def prepareString(s, isItem=True):
            s = s.upper()
            # remove chars not displayable
            s = regex.sub('', s)
            # remove space before and after
            s = s.strip()
            # limit to 30 chars, add one space before
            # pad to 32 chars
            if isItem is True:
                s = " " + s[0:30]
                s = s.ljust(32)
            else:
                s = " " + s[0:30] + " "
                s = " " + s.rjust(31, '.')

            return s

        isRace = self.race is not None
        startCreditAddress = Addresses.getOne('credits_itemlocations_start')
        address = startCreditAddress
        if isRace:
            addr = address - 0x40
            data = [0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x1008, 0x1013, 0x1004, 0x100c, 0x007f, 0x100b, 0x100e, 0x1002, 0x1000, 0x1013, 0x1008, 0x100e, 0x100d, 0x1012, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f, 0x007f]
            for i in range(0x20):
                w = data[i]
                self.romFile.seek(addr)
                self.race.writeWordMagic(w)
                addr += 0x2
        # standard item order
        items = ["Missile", "Super Missile", "Power Bomb",
                 "Charge Beam", "Ice Beam", "Wave Beam", "Spazer", "Plasma Beam",
                 "Varia Suit", "Gravity Suit",
                 "Morph Ball", "Bomb", "Spring Ball", "Screw Attack",
                 "Hi-Jump Boots", "Space Jump", "Speed Booster",
                 "Grappling Beam", "X-Ray Scope"]
        displayNames = {}
        if progItemLocs is not None:
            # reorder it with progression indices
            prog = ord('A')
            idx = 0
            progNames = [il.Item.Name for il in progItemLocs if il.Item.Category != 'Boss']
            for i in range(len(progNames)):
                item = progNames[i]
                if item in items and item not in displayNames:
                    items.remove(item)
                    items.insert(idx, item)
                    displayNames[item] = chr(prog + i) + ": " + item
                    idx += 1
        for item in items:
            # super fun removes items
            if item not in itemLocs:
                continue
            display = item
            if item in displayNames:
                display = displayNames[item]
            itemName = prepareString(display)
            locationName = prepareString(itemLocs[item], isItem=False)

            self.writeCreditsString(address, 0x04, itemName, isRace)
            self.writeCreditsString((address + 0x40), 0x18, locationName, isRace)

            address += 0x80

        # we need 19 items displayed, if we've removed majors, add some blank text
        while address < startCreditAddress + len(items)*0x80:
            self.writeCreditsString(address, 0x04, prepareString(""), isRace)
            self.writeCreditsString((address + 0x40), 0x18, prepareString(""), isRace)

            address += 0x80

        self.patchBytes(address, [0, 0, 0, 0], isRace)

    def writeCreditsString(self, address, color, string, isRace=False):
        array = [self.convertCreditsChar(color, char) for char in string]
        self.patchBytes(address, array, isRace)

    def writeCreditsStringBig(self, address, string, top=True):
        array = [self.convertCreditsCharBig(char, top) for char in string]
        self.patchBytes(address, array)

    def convertCreditsChar(self, color, byte):
        if byte == ' ':
            ib = 0x7f
        elif byte == '!':
            ib = 0x1F
        elif byte == ':':
            ib = 0x1E
        elif byte == '\\':
            ib = 0x1D
        elif byte == '_':
            ib = 0x1C
        elif byte == ',':
            ib = 0x1B
        elif byte == '.':
            ib = 0x1A
        else:
            ib = ord(byte) - 0x41

        if ib == 0x7F:
            return 0x007F
        else:
            return (color << 8) + ib

    def convertCreditsCharBig(self, byte, top=True):
        # from: https://jathys.zophar.net/supermetroid/kejardon/TextFormat.txt
        # 2-tile high characters:
        # A-P = $XX20-$XX2F(TOP) and $XX30-$XX3F(BOTTOM)
        # Q-Z = $XX40-$XX49(TOP) and $XX50-$XX59(BOTTOM)
        # ' = $XX4A, $XX7F
        # " = $XX4B, $XX7F
        # . = $XX7F, $XX5A
        # 0-9 = $XX60-$XX69(TOP) and $XX70-$XX79(BOTTOM)
        # % = $XX6A, $XX7A

        if byte == ' ':
            ib = 0x7F
        elif byte == "'":
            if top == True:
                ib = 0x4A
            else:
                ib = 0x7F
        elif byte == '"':
            if top == True:
                ib = 0x4B
            else:
                ib = 0x7F
        elif byte == '.':
            if top == True:
                ib = 0x7F
            else:
                ib = 0x5A
        elif byte == '%':
            if top == True:
                ib = 0x6A
            else:
                ib = 0x7A

        byte = ord(byte)
        if byte >= ord('A') and byte <= ord('P'):
            ib = byte - 0x21
        elif byte >= ord('Q') and byte <= ord('Z'):
            ib = byte - 0x11
        elif byte >= ord('a') and byte <= ord('p'):
            ib = byte - 0x31
        elif byte >= ord('q') and byte <= ord('z'):
            ib = byte - 0x21
        elif byte >= ord('0') and byte <= ord('9'):
            if top == True:
                ib = byte + 0x30
            else:
                ib = byte + 0x40

        return ib

    # isRace can be False even if self.race is not None
    def patchBytes(self, address, array, isRace=False):
        self.romFile.seek(address)
        for w in array:
            if isRace:
                self.writeWordMagic(w)
            else:
                self.romFile.writeWord(w)

    def writeDoorTransition(self, roomPtr):
        if self.race is None:
            self.romFile.writeWord(roomPtr)
        else:
            self.race.writeDoorTransition(roomPtr)

    def symbolWordBytes(self, symbol):
        ptr = self.symbols.getAddress(symbol)
        return getWordBytes(ptr)

    # write area randomizer transitions to ROM
    # doorConnections : a list of connections. each connection is a dictionary describing
    # - where to write in the ROM :
    # DoorPtr or DoorPtrSym : door pointer to write to, in direct address or symbol form
    # - what to write in the ROM :
    # RoomPtr, direction, bitflag, cap, screen, distanceToSpawn : door properties
    # * if SamusX and SamusY are defined in the dict, custom ASM has to be written
    #   to reposition samus, and call doorAsmPtr if non-zero. The written Door ASM
    #   property shall point to this custom ASM.
    # * if not, just write doorAsmPtr as the door property directly.
    def writeDoorConnections(self, doorConnections):
        assert len(self.areaMaps) > 0, "Build area maps before calling writeDoorConnections"
        r = Addresses.getRange('customDoorsAsm')
        asmAddress, asmRegionEnd = r[0], r[1]
        def loadDoorTransitionShortPtrBytes(label, patch='door_transition'):
            ptr = self.symbols.getAddress(patch, label)
            return getWordBytes(ptr)
        incompatible_doors = loadDoorTransitionShortPtrBytes("incompatible_doors")
        giveiframes = loadDoorTransitionShortPtrBytes("giveiframes")
        reveal_objectives = loadDoorTransitionShortPtrBytes("reveal_objectives", patch="objectives")
        explore_tile = loadDoorTransitionShortPtrBytes("explore_tile")
        for conn in doorConnections:
            # write door ASM for transition doors (code and pointers)
            if 'DoorPtrSym' not in conn:
                doorPtr = conn['DoorPtr']
            else:
                doorPtr = self.symbols.getAddress(conn['DoorPtrSym']) & 0xffff
            roomPtr = conn['RoomPtr']
#            print('Writing door connection ' + conn['ID'] + ". doorPtr="+hex(doorPtr))
            if doorPtr in self.doorConnectionSpecific:
                self.doorConnectionSpecific[doorPtr](roomPtr)
            if roomPtr in self.roomConnectionSpecific:
                self.roomConnectionSpecific[roomPtr](doorPtr)
            self.romFile.seek(0x10000 + doorPtr)
            # write room ptr
            self.writeDoorTransition(roomPtr & 0xFFFF)

            # write bitflag (if area switch we have to set bit 0x40, and remove it if same area)
            self.romFile.writeByte(conn['bitFlag'])

            # write direction
            self.romFile.writeByte(conn['direction'])

            # write door cap x
            self.romFile.writeByte(conn['cap'][0])

            # write door cap y
            self.romFile.writeByte(conn['cap'][1])

            # write screen x
            self.romFile.writeByte(conn['screen'][0])

            # write screen y
            self.romFile.writeByte(conn['screen'][1])

            # write distance to spawn
            self.romFile.writeWord(conn['distanceToSpawn'] & 0xFFFF)

            # write door asm
            asmPatch = []
            # incompatible transition
            if 'SamusX' in conn:
                SamusX = getWordBytes(conn['SamusX'])
                SamusY = getWordBytes(conn['SamusY'])
                # force samus position
                asmPatch += [ 0xA9 ] + SamusX             # LDA #$SamusX        ; fixed Samus X position
                asmPatch += [ 0x8D, 0xF6, 0x0A ]          # STA $0AF6           ; update Samus X position in memory
                asmPatch += [ 0xA9 ] + SamusY             # LDA #$SamusY        ; fixed Samus Y position
                asmPatch += [ 0x8D, 0xFA, 0x0A ]          # STA $0AFA           ; update Samus Y position in memory
                asmPatch += [ 0x20 ] + incompatible_doors # JSR incompatible_doors
            else:
                # still give I-frames
                asmPatch += [ 0x20 ] + giveiframes        # JSR giveiframes
            # call original door asm ptr if needed
            if conn['doorAsmPtr'] != 0x0000:
                # may be a symbol
                if type(conn['doorAsmPtr']) is str:
                    doorAsmPtr = self.symbolWordBytes(conn['doorAsmPtr'])
                else:
                    # endian convert
                    doorAsmPtr = getWordBytes(conn['doorAsmPtr'])
                asmPatch += [ 0x20 ] + doorAsmPtr         # JSR $doorAsmPtr
            # special ASM hook point for VARIA needs when taking the door (used for animals)
            if 'exitAsm' in conn:
                # endian convert
                exitAsm = self.symbolWordBytes(conn['exitAsm'])
                asmPatch += [ 0x20 ] + exitAsm            # JSR exitAsm
            # for special access points display on map, artificially explore the tile where
            # the portal is drawn, since it's not the same as the actual map tile checked to
            # see if the portal is taken
            src, dst = conn['transition']
            def writeExploreMapAsm(ap, matching):
                nonlocal asmPatch
                apInfo = Logic.map_tiles.areaAccessPointsInGameDisplay.get(ap.Name)
                if apInfo is not None:
                    areaMap = self.areaMaps[apInfo['area']]
                    byteIndex, bitMask = areaMap.getByteIndexMask(*apInfo['coords'])
                    ramAddr = self._getExploredMapRam(apInfo['area'], byteIndex)
                    if apInfo.get("coversTile", False):
                        # in that case, the tile we want to explore could be explored by the player,
                        # call a dedicated function
                        # LDX #[map tile byte index]
                        asmPatch += [ 0xA2 ] + getWordBytes(ramAddr)
                        # LDA #[graph area]
                        asmPatch += [ 0xA9 ] + getWordBytes(graphAreas.index(ap.GraphArea))
                        # STA $12
                        asmPatch += [ 0x85, 0x12 ]
                        # LDA #[map tile mask]
                        asmPatch += [ 0xA9 ] + getWordBytes(bitMask)
                        # JSR explore_tile
                        asmPatch += [ 0x20 ] + explore_tile
                    else:
                        ramAddrBytes = getWordBytes(ramAddr) + [ 0x7E ]
                        # LDA.l $7E[map tile byte index]
                        asmPatch += [ 0xAF ] + ramAddrBytes
                        # ORA.w #[map tile mask]
                        asmPatch += [ 0x09 ] + getWordBytes(bitMask)
                        # STA.l $7E[map tile byte index]
                        asmPatch += [ 0x8F ] + ramAddrBytes
                    # for index
                    if apInfo['area'] == gameAreas[matching.RoomInfo['area']]:
                        # JSL $80858C ; Load mirror of current area's map explored
                        # (needed for current area explored tiles to be synced)
                        asmPatch += [ 0x22, 0x8C, 0x85, 0x80 ]
            writeExploreMapAsm(src, dst)
            if src != dst:
                writeExploreMapAsm(dst, src)
            # if crateria-less minimizer, append reveal_objectives function to door asm leading to climb
            if dst.Name == "Climb Bottom Left":
                asmPatch += [ 0x20 ] + reveal_objectives
            # return
            asmPatch += [ 0x60 ]   # RTS
            assert asmAddress + len(asmPatch) <= asmRegionEnd, "door asm region overflow"
            self.log.debug(f"door connections asm patch: {len(asmPatch)} bytes, {asmRegionEnd - asmAddress - len(asmPatch)} bytes left")
            self.romFile.writeWord(asmAddress & 0xFFFF)
            self.romFile.seek(asmAddress)
            for byte in asmPatch:
                self.romFile.writeByte(byte)
            # print("asmAddress=%x" % asmAddress)
            # print("asmPatch=" + str(["%02x" % b for b in asmPatch]))

            asmAddress += len(asmPatch)
            # update room state header with song changes
            # TODO just do an IPS patch for this as it is completely static
            #      this would get rid of both 'song' and 'songs' fields
            #      as well as this code
            if 'song' in conn:
                for addr in conn["songs"]:
                    self.romFile.seek(0x70000 + addr)
                    self.romFile.writeByte(conn['song'])
                    self.romFile.writeByte(0x5)

    def writeBossDoors(self, bossFlags, graph, plms):
        newPlms = {}
        def getPLMbytes(door, closed=False):
            symbol = "gray_doors_%s_door_facing_%s" % ("gray" if closed else "bt", door['facing'])
            return self.symbolWordBytes(symbol) + [door['x'], door['y']] + getWordBytes(door['var'])
        def writeDoors(boss):
            doors = Logic.boss_doors[boss]
            if len(doors) == 1 and 'address' in doors[0]:
                # overwrite existing PLM
                self.romFile.seek(doors[0]['address'])
                bytez = getPLMbytes(doors[0])
                for b in bytez:
                    self.romFile.writeByte(b)
            else: 
                for i, door in enumerate(doors):
                    self.log.debug(f"processing boss {boss} door {i}")
                    # add new PLMs: when coming in at this door, put a bt door there and gray doors elsewhere.
                    # that way when the player enters the door behind them stays open until hurting the boss,
                    # and other doors are locked by the boss (or already sealed off if dead end)
                    incoming = door.get('from')
                    if not incoming:
                        ap = graph.accessPoints[door['connection']]
                        if ap.ConnectedTo is None:
                            self.log.debug("skipped")
                            continue
                        incoming = graph.accessPoints[ap.ConnectedTo].ExitInfo['DoorPtr']
                        self.log.debug("connection: %s" % ap.Name)
                    self.log.debug("incoming: %04x" % incoming)
                    otherDoors = [d for d in doors if d != door]
                    plm = {
                        'room': door['room'],
                        'door': incoming,
                        'plm_bytes_list': []
                    }
                    newPlms[f"{boss}_entering_from_door_facing_{door['facing']}_{incoming:04x}"] = plm
                    def addDoor(d, closed):
                        nonlocal plm
                        assert d['room'] == plm['room']
                        self.log.debug("adding %s door: %s" % ("gray" if closed else "bt", str(d)))
                        plm['plm_bytes_list'].append(getPLMbytes(d, closed))
                    for d in otherDoors:
                        if "connection" in d and graph.accessPoints[d['connection']].ConnectedTo is None:
                            # don't add doors where dead end permanent gray doors are already added
                            continue
                        addDoor(d, True)
                    addDoor(door, False)
                    # disable original PLM, if any
                    if 'address' in door:
                        self.romFile.writeWord(0xb63b, door['address']) # PLM type = copy arrow
        # determine bosses in the seed and write boss doors
        bosses = set()
        for apName, ap in graph.accessPoints.items():
            if ap.Boss & bossFlags:
                boss, _ = GraphUtils.getBossProperties(apName)
                if boss:
                    bosses.add(boss)
        for boss in bosses:
            writeDoors(boss)
        self.patchAccess.updateAdditionalPLMs(newPlms)
        plms += list(newPlms.keys())

    def _getExploredMapRam(self, area, index=0):
        if isinstance(area, str):
            area = gameAreas.index(area)
        exploredBaseRam = 0xCD52
        exploredAreaSize = 0x100
        return exploredBaseRam + area*exploredAreaSize + index

    def _updateMapIconsGraphAreas(self, itemLocs):
        mapIcons = Logic.map_tiles
        def updateAccessPoints(apIcons):
            for apName, icon in apIcons.items():
                ap = getAccessPoint(apName)
                icon['graphArea'] = ap.GraphArea
        updateAccessPoints(mapIcons.areaAccessPoints)
        updateAccessPoints(mapIcons.areaAccessPointsInGameDisplay)
        updateAccessPoints(mapIcons.bossAccessPoints)
        updateAccessPoints(mapIcons.escapeAccessPoints)
        for il in itemLocs:
            if il.Location.isBoss():
                continue
            icon = mapIcons.itemLocations[il.Location.Name]
            icon["graphArea"] = il.Location.GraphArea

    def _writePortalIcons(self, doorConnections, area, areaMap, tourian):
        def getMapInfo(apName, isSrc):
            if isSrc and apName in Logic.map_tiles.areaAccessPointsInGameDisplay:
                return Logic.map_tiles.areaAccessPointsInGameDisplay[apName]
            elif apName in Logic.map_tiles.areaAccessPoints:
                return Logic.map_tiles.areaAccessPoints[apName]
            elif apName in Logic.map_tiles.bossAccessPoints:
                return Logic.map_tiles.bossAccessPoints[apName]
            return None
        graphAreaOverride = {
            "KraidRoomIn": "KraidBoss",
            "PhantoonRoomIn": "PhantoonBoss",
            "DraygonRoomIn": "DraygonBoss",
            "RidleyRoomIn": "RidleyBoss"
        }
        allAreas = list(self._accessibleAreasNoBoss)
        if tourian != "Disabled":
            allAreas.append("Tourian")
        for conn in doorConnections:
            src, dst = conn['transition']
            srcMapInfo, dstMapInfo = getMapInfo(src.Name, True), getMapInfo(dst.Name, False)
            if srcMapInfo is None or dstMapInfo is None or srcMapInfo['area'] != area:
                continue
            if src.Name not in graphAreaOverride and src.GraphArea not in allAreas:
                continue
            if "coords" in srcMapInfo:
                x, y = srcMapInfo['coords']
            else:
                x, y = areaMap.getCoordsByte(srcMapInfo['byteIndex'], srcMapInfo['bitMask'])
            self.writeWordMagic(x*8)
            self.writeWordMagic(y*8)
            graphArea = graphAreaOverride.get(dst.Name, dst.GraphArea)
            self.writeWordMagic(portal_mapicons[graphArea].table_index)
            self.writeWordMagic(self._getExploredMapRam(dst.RoomInfo['area'], dstMapInfo['byteIndex']))
            self.romFile.writeWord(dstMapInfo['bitMask'])
        self.writeWordMagic(0xffff) # terminator

    def writeDoorConnectionsMapIcons(self, doorConnections, tourian):
        assert len(self.areaMaps) > 0, "call writeDoorConnectionsMapIcons when areaMaps are built"
        # write area portal tables
        self.romFile.seek(self._mapIconTableAddr)
        mapicon_ptrs = {}
        for area, areaMap in self.areaMaps.items():
            mapicon_ptrs[area] = self.romFile.tell()
            self._writePortalIcons(doorConnections, area, areaMap, tourian)
        self._mapIconTableAddr = self.romFile.tell()
        self._writeMapIconTable(mapicon_ptrs, Addresses.getOne("map_portals_mapicons_by_area"))

    # change BG table to avoid scrolling sky bug when transitioning to west ocean
    def patchWestOcean(self, doorPtr):
        self.romFile.writeWord(doorPtr, Addresses.getOne('westOceanScrollingSky'))

    # forces CRE graphics refresh when exiting kraid's or croc room
    def forceRoomCRE(self, roomPtr, creFlag=0x2):
        # Room ptr in bank 8F + CRE flag offset
        offset = 0x70000 + roomPtr + 0x8
        self.romFile.writeByte(creFlag, offset)

    buttons = {
        "Select" : [0x00, 0x20],
        "A"      : [0x80, 0x00],
        "B"      : [0x00, 0x80],
        "X"      : [0x40, 0x00],
        "Y"      : [0x00, 0x40],
        "L"      : [0x20, 0x00],
        "R"      : [0x10, 0x00],
        "None"   : [0x00, 0x00]
    }

    controls = {
        "Shot"       : [0xb331, 0x1722d],
        "Jump"       : [0xb325, 0x17233],
        "Dash"       : [0xb32b, 0x17239],
        "ItemSelect" : [0xb33d, 0x17245],
        "ItemCancel" : [0xb337, 0x1723f],
        "AngleUp"    : [0xb343, 0x1724b],
        "AngleDown"  : [0xb349, 0x17251]
    }

    # write custom contols to ROM.
    # controlsDict : possible keys are "Shot", "Jump", "Dash", "ItemSelect", "ItemCancel", "AngleUp", "AngleDown"
    #                possible values are "A", "B", "X", "Y", "L", "R", "Select", "None"
    def writeControls(self, controlsDict):
        for ctrl, button in controlsDict.items():
            if ctrl not in RomPatcher.controls:
                raise ValueError("Invalid control name : " + str(ctrl))
            if button not in RomPatcher.buttons:
                raise ValueError("Invalid button name : " + str(button))
            for addr in RomPatcher.controls[ctrl]:
                self.romFile.writeByte(RomPatcher.buttons[button][0], addr)
                self.romFile.writeByte(RomPatcher.buttons[button][1])

    def writePlandoAddresses(self, locations):
        self.romFile.seek(Addresses.getOne('plandoAddresses'))
        for loc in locations:
            self.romFile.writeWord(loc.Address & 0xFFFF)

        # fill remaining addresses with 0xFFFF
        maxLocsNumber = 128
        for i in range(0, maxLocsNumber-len(locations)):
            self.romFile.writeWord(0xFFFF)

    def writePlandoTransitions(self, transitions, doorsPtrs, maxTransitions):
        self.romFile.seek(Addresses.getOne('plandoTransitions'))

        for (src, dest) in transitions:
            self.romFile.writeWord(doorsPtrs[src])
            self.romFile.writeWord(doorsPtrs[dest])

        # fill remaining addresses with 0xFFFF
        for i in range(0, maxTransitions-len(transitions)):
            self.romFile.writeWord(0xFFFF)
            self.romFile.writeWord(0xFFFF)

    def enableMoonWalk(self):
        # replace STZ with STA since A is non-zero at this point
        self.romFile.writeByte(0x8D, Addresses.getOne('moonwalk'))

    def writeStartingEnergy(self, energy):
        self.romFile.writeWord(energy, Addresses.getOne("start_starting_energy"))

    def writeAdditionalETanks(self, additionalETanks):
        energy = additionalETanks*100 + 99
        self.writeStartingEnergy(energy)

    def writeHellrunRate(self, hellrunRatePct):
        hellrunRateVal = min(int(0x40*float(hellrunRatePct)/100.0), 0xff)
        self.romFile.writeByte(hellrunRateVal, Addresses.getOne("hellrunRate"))

    def compress(self, address, data):
        # data: [] of 256 int
        # address: the address where the compressed bytes will be written
        # return the size of the compressed data
        compressedData = Compressor().compress(data)

        self.romFile.seek(address)
        for byte in compressedData:
            self.romFile.writeByte(byte)

        return len(compressedData)

    def setOamTile(self, nth, middle, newTile, y=0xFC):
        # an oam entry is made of five bytes: (s000000 xxxxxxxxx) (yyyyyyyy) (YXpp000t tttttttt)

        # after and before the middle of the screen is not handle the same
        if nth >= middle:
            x = (nth - middle) * 0x08
        else:
            x = 0x200 - (0x08 * (middle - nth))

        self.romFile.writeWord(x)
        self.romFile.writeByte(y)
        self.romFile.writeWord(0x3100+newTile)

    def writeVersion(self, version, addRotation=False):
        # max 32 chars

        # new oamlist address in free space at the end of bank 8C
        ptr = pc_to_snes(Addresses.getOne('versionOamList')) & 0xffff
        self.romFile.writeWord(ptr, Addresses.getOne('versionOamListPtr1'))
        self.romFile.writeWord(ptr, Addresses.getOne('versionOamListPtr2'))

        # string length
        versionLength = len(version)
        if addRotation:
            rotationLength = len('rotation')
            length = versionLength + rotationLength
        else:
            length = versionLength
        self.romFile.writeWord(length, Addresses.getOne('versionOamList'))
        versionMiddle = int(versionLength / 2) + versionLength % 2

        # oams
        for (i, char) in enumerate(version):
            self.setOamTile(i, versionMiddle, char2tile[char])

        if addRotation:
            rotationMiddle = int(rotationLength / 2) + rotationLength % 2
            for (i, char) in enumerate('rotation'):
                self.setOamTile(i, rotationMiddle, char2tile[char], y=0x8e)

    def _writeMapIconTable(self, mapicon_ptrs, baseAddr):
        # write pointer table to index above tables by area
        for idx, area in enumerate(['Crateria', 'Brinstar', 'Norfair', 'WreckedShip', 'Maridia', 'Tourian']): # ignore Ceres and Debug
            if area not in mapicon_ptrs:
                continue
            addr = baseAddr + idx*2
            self.romFile.writeWord(pc_to_snes(mapicon_ptrs[area]) & 0xffff, addr)

    def writeDoorsColor(self):
        DoorsManager.writeDoorsColor(self.romFile, self.writePlmWord)

    def writeDoorsMapIcons(self):
        assert len(self.areaMaps) > 0, "call writeDoorsMapIcons when areaMaps are built"
        # write area door tables
        self.romFile.seek(self._mapIconTableAddr)
        mapicon_ptrs = {}
        for area, areaMap in self.areaMaps.items():
            mapicon_ptrs[area] = self.romFile.tell()
            DoorsManager.writeDoorsMapIcons(area, areaMap, self.writeWordMagic)
        self._mapIconTableAddr = self.romFile.tell()
        self._writeMapIconTable(mapicon_ptrs, Addresses.getOne("map_doors_mapicons_by_area"))

    def writeDoorIndicators(self, plms, area, door):
        indicatorFlags = IndicatorFlag.Standard | (IndicatorFlag.AreaRando if area else 0) | (IndicatorFlag.DoorRando if door else 0)
        patchDict = self.patchAccess.getDictPatches()
        additionalPLMs = self.patchAccess.getAdditionalPLMs()
        def updateIndicatorPLM(door, doorType):
            nonlocal additionalPLMs, patchDict
            plmName = 'Indicator[%s]' % door
            addPlm = False
            if plmName in patchDict:
                for addr,bytez in patchDict[plmName].items():
                    plmBytes = bytez
                    break
            else:
                plmBytes = additionalPLMs[plmName]['plm_bytes_list'][0]
                addPlm = True
            w = getWord(doorType)
            plmBytes[0] = w[0]
            plmBytes[1] = w[1]
            return plmName, addPlm
        indicatorPLMs = DoorsManager.getIndicatorPLMs(indicatorFlags)
        for doorName,plmType in indicatorPLMs.items():
            plmName,addPlm = updateIndicatorPLM(doorName, plmType)
            if addPlm:
                plms.append(plmName)
            else:
                self.applyIPSPatch(plmName)

    def _getAccessibleAreasNoBoss(self, itemLocs):
        # filter areas : exclude Tourian and Ceres, and filter excluded areas in minimizer
        #
        # special boss check to avoid varia/space jump/ridley E locs in minimizer and get only graph
        # areas entirely in layout :
        bossSolveAreeas = [b + " Boss" for b in Bosses.Golden4()]
        bossChk = lambda loc: loc.isBoss() or loc.SolveArea in bossSolveAreeas
        return {il.Location.GraphArea for il in itemLocs if not bossChk(il.Location) and not il.Location.restricted}

    def writeMapTileCount(self, isArea, isEscape, tourian):
        accessibleAreasNoBoss = self._accessibleAreasNoBoss
        self.log.debug(f"writeMapTileCount. accessibleareas: {accessibleAreasNoBoss}")
        # G4 are always there, even when their area is not in minimizer layout
        bossTiles = {
            "Kraid": 5,
            "WreckedShip": 1,
            "EastMaridia": 5,
            "LowerNorfair": 3
        }
        # tile count offsets for when escape rando is on (maps stations sealed off)
        escapeRandoOffsets = {
            "GreenPinkBrinstar": -4,
            "Norfair": -1,
            "WreckedShip": -1,
            "WestMaridia": -1
        }
        # write individual areas tile count
        tilecount = Logic.map_tilecount["area_rando" if isArea else "vanilla_layout"]
        total = 0
        self.romFile.seek(Addresses.getOne("map_area_tiles"))
        for area in graphAreas:
            if area in accessibleAreasNoBoss:
                # count all tiles
                offset = 0 if not isEscape else escapeRandoOffsets.get(area, 0)
                count = tilecount[area] + offset
            elif area in bossTiles:
                # only boss tiles
                count = bossTiles[area]
            else:
                # disable tile counting for this area
                count = 0
            total += count
            self.romFile.writeByte(count)
        # write total tile count in map patch
        self.romFile.writeWord(total, Addresses.getOne("map_total_tiles"))
        # for X% map explored objectives, precompute values and write them in objectives functions
        for percent in [25, 50, 75, 100]:
            addr = Addresses.getOne("objectives_explored_map_%d_pct" % percent)
            self.romFile.writeWord(ceil((total * percent)/100), addr)

    def writeEnemiesTotals(self, itemLocs):
        accessibleAreasNoBoss = self._accessibleAreasNoBoss
        for nmyType, nmyEntry in enemies_objectives_data.items():
            areaCounts = nmyEntry["area_count"]
            total = sum(areaCounts[area] for area in areaCounts if area in accessibleAreasNoBoss)
            self.romFile.writeByte(total, Addresses.getOne(nmyEntry["total_sym"]))

    def writeObjectives(self, itemLocs, tourian):
        objectives = Objectives()
        objectives.writeGoals(self.romFile, tourian)
        self.writeItemsMasks(itemLocs)
        self.writeEnemiesTotals(itemLocs)
        # change etecoons/dachora map tiles depending on ROM flavor
        if objectives.isGoalActive("visit the animals"):
            animals = {
                'vanilla': {
                    'dachora': (0x082C, 0x20),
                    'etecoons': (0x0828, 0x10)
                },
                'mirror': {
                    'dachora': (0x08AD, 0x4),
                    'etecoons': (0x08A9, 0x8)
                }
            }
            for animal,entry in animals[RomFlavor.flavor].items():
                offset, mask = entry
                addr = Addresses.getOne("objectives_map_tile_%s_addr" % animal)
                self.romFile.writeWord(offset, addr)
                addr = Addresses.getOne("objectives_map_tile_%s_mask" % animal)
                self.romFile.writeWord(mask, addr)
        # handle VARIA tweaks BT behavior ROM option here. wake BT if there is an item there or activate chozo robots obj is on
        if RomPatches.has(RomPatches.BombTorizoWake):
            bomb = next((il for il in itemLocs if il.Location.Name == "Bomb"), None)
            if (bomb is not None and bomb.Item.Category == "Nothing") and not objectives.isGoalActive("activate chozo robots"):
                self.romOptions.write('BTsleep', 0x4)

    def writeItemsMasks(self, itemLocs):
        # write items/beams masks for "collect all major" objective
        itemsMask = 0
        beamsMask = 0
        for il in itemLocs:
            if not il.Location.restricted:
                item = il.Item
                itemsMask |= item.ItemBits
                beamsMask |= item.BeamBits
        self.romFile.writeWord(itemsMask, Addresses.getOne('itemsMask'))
        self.romFile.writeWord(beamsMask, Addresses.getOne('beamsMask'))

    def writeObjectivesMapIcons(self, tourian):
        assert len(self.areaMaps) > 0, "call writeObjectivesMapIcons when areaMaps are built"
        # create a dict area => {(x, y) => (obj, mapIcon)}
        objByArea = defaultdict(dict)
        objTiles = Logic.map_tiles.objectives
        for goal in Objectives.activeGoals:
            for mapIcon in goal.mapIcons:
                coords = objTiles[mapIcon]["map_coords_px"]
                area = objTiles[mapIcon]["area"]
                graphArea = objTiles[mapIcon].get("graphArea")
                if graphArea is not None and graphArea not in self._accessibleAreasNoBoss:
                    continue
                addIcon = coords not in objByArea[area]
                if not addIcon:
                    # icon coords conflict, choose one
                    otherGoal, _ = objByArea[area][coords]
                    # prioritize icons of objectives of same categories with short icons list:
                    # we prefer to show a unique boss obj than the list obj when both are present
                    # prioritize Memes over other categories, as it is more obscure
                    addIcon = (otherGoal.category == goal.category and len(otherGoal.mapIcons) > len(goal.mapIcons))\
                           or (otherGoal.category != goal.category and goal.category == "Memes")
                if addIcon:
                    objByArea[area][coords] = (goal, mapIcon)
        # write icon tables
        self.romFile.seek(self._mapIconTableAddr)
        mapicon_ptrs = {}
        for area, objs in objByArea.items():
            mapicon_ptrs[area] = self.romFile.tell()
            for coords, objData in objs.items():
                goalIdx, mapIcon = objData[0].rank - 1, objTiles[objData[1]]
                assert coords == mapIcon["map_coords_px"]
                x, y = coords
                self.romFile.writeWord(x)
                self.romFile.writeWord(y)
                self.romFile.writeWord(goalIdx)
                self.romFile.writeWord(mapIcon["event"])
            self.romFile.writeWord(0xffff) # terminator
        self._mapIconTableAddr = self.romFile.tell()
        self._writeMapIconTable(mapicon_ptrs, Addresses.getOne("map_objectives_mapicons_by_area"))

    def removeAnimalsHunt(self):
        # remove custom door asm ptr used by animals hunt as their target is overwritten by door_transition patch
        flyway = getAccessPoint("Flyway Right")
        self.romFile.writeWord(0x0000, snes_to_pc(0x830000 + flyway.ExitInfo['DoorPtr'] + 0x0a))
        bombTorizo = getAccessPoint("Bomb Torizo Room Left")
        self.romFile.writeWord(0x0000, snes_to_pc(0x830000 + bombTorizo.ExitInfo['DoorPtr'] + 0x0a))

# tile number in tileset
char2tile = {
    '-': 207,
    'a': 208,
    '.': 243,
    '0': 244
}
for i in range(1, ord('z')-ord('a')+1):
    char2tile[chr(ord('a')+i)] = char2tile['a']+i
for i in range(1, ord('9')-ord('0')+1):
    char2tile[chr(ord('0')+i)] = char2tile['0']+i

class MessageBox(object):
    def __init__(self, rom):
        self.rom = rom

        # in message boxes the char a is at offset 0xe0 in the tileset
        self.char2tile = {'1': 0x00, '2': 0x01, '3': 0x02, '4': 0x03, '5': 0x04, '6': 0x05, '7': 0x06, '8': 0x07, '9': 0x08, '0': 0x09,
                          ' ': 0x4e, '-': 0xcf, 'a': 0xe0, '.': 0xfa, ',': 0xfb, '`': 0xfc, "'": 0xfd, '?': 0xfe, '!': 0xff}
        for i in range(1, ord('z')-ord('a')+1):
            self.char2tile[chr(ord('a')+i)] = self.char2tile['a']+i

        # add 0x0c/0x06 to offsets as there's 12/6 bytes before the strings, string length is either 0x13/0x1a
        self.offsets = {
            'ETank': (snes_to_pc(0x85877f)+0x0c, 0x13),
            'Missile': (0x287bf+0x06, 0x1a),
            'Super': (0x288bf+0x06, 0x1a),
            'PowerBomb': (0x289bf+0x06, 0x1a),
            'Grapple': (0x28abf+0x06, 0x1a),
            'XRayScope': (0x28bbf+0x06, 0x1a),
            'Varia': (0x28cbf+0x0c, 0x13),
            'SpringBall': (0x28cff+0x0c, 0x13),
            'Morph': (0x28d3f+0x0c, 0x13),
            'ScrewAttack': (0x28d7f+0x0c, 0x13),
            'HiJump': (0x28dbf+0x0c, 0x13),
            'SpaceJump': (0x28dff+0x0c, 0x13),
            'SpeedBooster': (0x28e3f+0x06, 0x1a),
            'Charge': (0x28f3f+0x0c, 0x13),
            'Ice': (0x28f7f+0x0c, 0x13),
            'Wave': (0x28fbf+0x0c, 0x13),
            'Spazer': (0x28fff+0x0c, 0x13),
            'Plasma': (0x2903f+0x0c, 0x13),
            'Bomb': (0x2907f+0x06, 0x1a),
            'Reserve': (0x294ff+0x0c, 0x13),
            'Gravity': (0x2953f+0x0c, 0x13)
        }

    def updateMessage(self, box, message, vFlip=False, hFlip=False):
        (address, oldLength) = self.offsets[box]
        newLength = len(message)
        assert newLength <= oldLength, "string '{}' is too long, max {}".format(message, oldLength)
        padding = oldLength - newLength
        paddingLeft = int(padding / 2)
        paddingRight = int(padding / 2)
        paddingRight += padding % 2

        attr = self.getAttr(vFlip, hFlip)

        # write spaces for padding left
        for i in range(paddingLeft):
            self.writeChar(address, ' ')
            address += 0x02
        # write message
        for char in message:
            self.writeChar(address, char)
            address += 0x01
            self.updateAttr(attr, address)
            address += 0x01
        # write spaces for padding right
        for i in range(paddingRight):
            self.writeChar(address, ' ')
            address += 0x02

    def writeChar(self, address, char):
        self.rom.writeByte(self.char2tile[char], address)

    def getAttr(self, vFlip, hFlip):
        # vanilla is 0x28:
        byte = 0x28
        if vFlip:
            byte |= 0b10000000
        if hFlip:
            byte |= 0b01000000
        return byte

    def updateAttr(self, byte, address):
        self.rom.writeByte(byte, address)

class RomTypeForMusic(IntFlag):
    VariaSeed = 1
    AreaSeed = 2
    BossSeed = 4

class MusicPatcher(object):
    # rom: ROM object to patch
    # romType: 0 if not varia seed, or bitwise or of RomTypeForMusic enum
    # baseDir: directory containing all music data/descriptors/constraints
    # constraintsFile: file to constraints JSON descriptor, relative to baseDir/constraints.
    #                  if None, will be determined automatically from romType
    def __init__(self, rom, romType,
                 baseDir=os.path.join(appDir, 'varia_custom_sprites', 'music'),
                 constraintsFile=None):
        self.rom = rom
        self.baseDir = baseDir
        variaSeed = bool(romType & RomTypeForMusic.VariaSeed)
        self.area = variaSeed and bool(romType & RomTypeForMusic.AreaSeed)
        self.boss = variaSeed and bool(romType & RomTypeForMusic.BossSeed)
        metaDir = os.path.join(baseDir, "_metadata")
        constraintsDir = os.path.join(baseDir, "_constraints")
        if constraintsFile is None:
            constraintsFile = 'varia.json' if variaSeed else 'vanilla.json'
        with open(os.path.join(constraintsDir, constraintsFile), 'r') as f:
            self.constraints = json.load(f)
        nspcInfoPath = os.path.join(baseDir, "nspc_metadata.json")
        with open(nspcInfoPath, "r") as f:
            nspcInfo = json.load(f)
        self.nspcInfo = {}
        for nspc,info in nspcInfo.items():
            self.nspcInfo[self._nspc_path(nspc)] = info
        self.allTracks = {}
        self.vanillaTracks = None
        for metaFile in os.listdir(metaDir):
            metaPath = os.path.join(metaDir, metaFile)
            if not metaPath.endswith(".json"):
                continue
            with open(metaPath, 'r') as f:
                meta = json.load(f)
            # will silently overwrite entries with same name, so avoid
            # conflicting descriptor files ...
            self.allTracks.update(meta)
            if metaFile == "vanilla.json":
                self.vanillaTracks = meta
        assert self.vanillaTracks is not None, "MusicPatcher: missing vanilla JSON descriptor"
        self.replaceableTracks = [track for track in self.vanillaTracks if track not in self.constraints['preserve'] and track not in self.constraints['discard']]
        self.musicDataTableMaxSize = 45 # to avoid overwriting useful data in bank 8F

    # tracks: dict with track name to replace as key, and replacing track name as value
    # updateReferences: change room state headers and special tracks. may be False if you're patching a rom hack or something
    # output: if not None, dump a JSON file with what was done
    # replaced tracks must be in
    # replaceableTracks, and new tracks must be in allTracks
    # tracks not in the dict will be kept vanilla
    # raise RuntimeError if not possible
    def replace(self, tracks, updateReferences=True, output=None):
        for track in tracks:
            if track not in self.replaceableTracks:
                raise RuntimeError("Cannot replace track %s" % track)
        trackList = self._getTrackList(tracks)
        replacedVanilla = [t for t in self.replaceableTracks if t in trackList and t not in tracks]
        for van in replacedVanilla:
            tracks[van] = van
#        print("trackList="+str(trackList))
        musicData = self._getMusicData(trackList)
#        print("musicData="+str(musicData))
        if len(musicData) > self.musicDataTableMaxSize:
            raise RuntimeError("Music data table too long. %d entries, max is %d" % (len(musicData, self.musicDataTableMaxSize)))
        musicDataAddresses = self._getMusicDataAddresses(musicData)
        self._writeMusicData(musicDataAddresses)
        self._writeMusicDataTable(musicData, musicDataAddresses)
        if updateReferences == True:
            self._updateReferences(trackList, musicData, tracks)
        if output is not None:
            self._dump(output, trackList, musicData, musicDataAddresses)

    # compose a track list from vanilla tracks, replaced tracks, and constraints
    def _getTrackList(self, replacedTracks):
        trackList = set()
        for track in self.vanillaTracks:
            if track in replacedTracks:
                trackList.add(replacedTracks[track])
            elif track not in self.constraints['discard']:
                trackList.add(track)
        return list(trackList)

    def _nspc_path(self, nspc_path):
        return os.path.join(self.baseDir, nspc_path)

    # get list of music data files to include in the ROM
    # can contain empty entries, marked with a None, to account
    # for fixed place data ('preserve' constraint)
    def _getMusicData(self, trackList):
        # first, make musicData the minimum size wrt preserved tracks
        preservedTracks = {trackName:self.vanillaTracks[trackName] for trackName in self.constraints['preserve']}
        preservedDataIndexes = [track['data_index'] for trackName,track in preservedTracks.items()]
        musicData = [None]*(max(preservedDataIndexes)+1)
        # fill preserved spots
        for track in self.constraints['preserve']:
            idx = self.vanillaTracks[track]['data_index']
            nspc = self._nspc_path(self.vanillaTracks[track]['nspc_path'])
            if nspc not in musicData:
                musicData[idx] = nspc
#                print("stored " + nspc + " at "+ str(idx))
        # then fill data in remaining spots
        idx = 0
        for track in trackList:
            previdx = idx
            if track not in self.constraints['preserve']:
                nspc = self._nspc_path(self.allTracks[track]['nspc_path'])
                if nspc not in musicData:
                    for i in range(idx, len(musicData)):
#                        print("at " + str(i) + ": "+str(musicData[i]))
                        if musicData[i] is None:
                            musicData[i] = nspc
                            idx = i+1
                            break
                    if idx == previdx:
                        idx += 1
                        musicData.append(nspc)
#                    print("stored " + nspc + " at "+ str(idx))
        return musicData

    # get addresses to store each data file to. raise RuntimeError if not possible
    # pretty dumb algorithm for now, just store data wherever possible,
    # prioritizing first areas in usableSpace
    # store data from end of usable space to make room for other data (for hacks for instance)
    def _getMusicDataAddresses(self, musicData):
        usableSpace = self.constraints['usable_space_ranges_pc']
        musicDataAddresses = {}
        for dataFile in musicData:
            if dataFile is None:
                continue
            sz = os.path.getsize(dataFile)
            blocks = self.nspcInfo[dataFile]['block_headers_offsets']
            for r in usableSpace:
                # find a suitable address so header words are not split across banks (header is 2 words)
                addr = r['end'] - sz
                def isCrossBank(off):
                    nonlocal addr
                    endBankOffset = pc_to_snes(addr+off+4) & 0x7fff
                    return endBankOffset == 1 or endBankOffset == 3
                while addr >= r['start'] and any(isCrossBank(off) for off in blocks):
                    addr -= 1
                if addr >= r['start']:
                    musicDataAddresses[dataFile] = addr
                    r['end'] = addr
                    break
            if dataFile not in musicDataAddresses:
                raise RuntimeError("Cannot find enough space to store music data file "+dataFile)
        return musicDataAddresses

    def _writeMusicData(self, musicDataAddresses):
        for dataFile, addr in musicDataAddresses.items():
            self.rom.seek(addr)
            with open(dataFile, 'rb') as f:
                self.rom.write(f.read())

    def _writeMusicDataTable(self, musicData, musicDataAddresses):
        self.rom.seek(Addresses.getOne('musicDataTable'))
        for dataFile in musicData:
            addr = pc_to_snes(musicDataAddresses[dataFile]) if dataFile in musicDataAddresses else 0
            self.rom.writeLong(addr)

    def _getDataId(self, musicData, track):
        return (musicData.index(self._nspc_path(self.allTracks[track]['nspc_path']))+1)*3

    def _getTrackId(self, track):
        return self.allTracks[track]['track_index'] + 5

    def _updateReferences(self, trackList, musicData, replacedTracks):
        trackAddresses = {}
        def addAddresses(track, vanillaTrackData, prio=False):
            nonlocal trackAddresses
            addrs = []
            prioAddrs = []
            if 'pc_addresses' in vanillaTrackData:
                addrs += vanillaTrackData['pc_addresses']
            if self.area and 'pc_addresses_area' in vanillaTrackData:
                prioAddrs += vanillaTrackData['pc_addresses_area']
            if self.boss and 'pc_addresses_boss' in vanillaTrackData:
                prioAddrs += vanillaTrackData['pc_addresses_boss']
            if track not in trackAddresses:
                trackAddresses[track] = []
            # if prioAddrs are somewhere else, remove if necessary
            prioSet = set(prioAddrs)
            for t,tAddrs in trackAddresses.items():
                trackAddresses[t] = list(set(tAddrs) - prioSet)
            # if some of addrs are somewhere else, remove them from here
            for t,tAddrs in trackAddresses.items():
                addrs = list(set(addrs) - set(tAddrs))
            trackAddresses[track] += prioAddrs + addrs
        for track in trackList:
            if track in replacedTracks.values():
                for van,rep in replacedTracks.items():
                    if rep == track:
                        addAddresses(track, self.vanillaTracks[van])
            else:
                addAddresses(track, self.vanillaTracks[track])
        for track in trackList:
            dataId = self._getDataId(musicData, track)
            trackId = self._getTrackId(track)
            for addr in trackAddresses[track]:
                self.rom.seek(addr)
                self.rom.writeByte(dataId)
                self.rom.writeByte(trackId)
        self._writeSpecialReferences(replacedTracks, musicData)

    # write special (boss) data
    def _writeSpecialReferences(self, replacedTracks, musicData, static=True, dynamic=True):
        for track,replacement in replacedTracks.items():
            # static patches are needed only when replacing tracks
            if track != replacement:
                staticPatches = self.vanillaTracks[track].get("static_patches", None)
            else:
                staticPatches = None
            # dynamic patches are similar to pc_addresses*, and must be written also
            # when track is vanilla, as music data table is changed
            dynamicPatches = self.vanillaTracks[track].get("dynamic_patches", None)
            if static and staticPatches:
                for addr,bytez in staticPatches.items():
                    self.rom.seek(int(addr))
                    for b in bytez:
                        self.rom.writeByte(b)
            if dynamic and dynamicPatches:
                dataId = self._getDataId(musicData, replacement)
                trackId = self._getTrackId(replacement)
                dataIdAddrs = dynamicPatches.get("data_id", [])
                trackIdAddrs = dynamicPatches.get("track_id", [])
                for addr in dataIdAddrs:
                    self.rom.writeByte(dataId, addr)
                for addr in trackIdAddrs:
                    self.rom.writeByte(trackId, addr)

    def _dump(self, output, trackList, musicData, musicDataAddresses):
        music={}
        no=0
        for md in musicData:
            if md is None:
                music["NoData_%d" % no] = None
                no += 1
            else:
                tracks = []
                h,t=os.path.split(md)
                md=os.path.join(os.path.split(h)[1], t)
                for track,trackData in self.allTracks.items():
                    if trackData['nspc_path'] == md:
                        tracks.append(track)
                music[md] = tracks
        musicSnesAddresses = {}
        for nspc, addr in musicDataAddresses.items():
            h,t=os.path.split(nspc)
            nspc=os.path.join(os.path.split(h)[1], t)
            musicSnesAddresses[nspc] = "$%06x" % pc_to_snes(addr)
        dump = {
            "track_list": sorted(trackList),
            "music_data": music,
            "music_data_addresses": musicSnesAddresses
        }
        with open(output, 'w') as f:
            json.dump(dump, f, indent=4)
