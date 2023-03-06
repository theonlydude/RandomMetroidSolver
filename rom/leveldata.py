# from SM3E

import sys
from enum import Enum, IntFlag, auto
import logging
from collections import defaultdict
import utils.log
from rom.rom import snes_to_pc, pc_to_snes
from rom.compression import Compressor
from utils.doorsmanager import plmRed, plmGreen, plmYellow, plmGrey, Facing, plmFacing, indicatorsDirection
from rom.romreader import RomReader

doorPlms = plmRed + plmGreen + plmYellow + plmGrey

class Ship(object):
    # plm sleep instruction
    sleepInstr = 0x812F

    def __init__(self, name, rom, enemy, center):
        self.name = name
        self.rom = rom
        self.enemy = enemy
        self.center = center
        self.bank = self.enemy.bank << 16

        self.load()

    def getShipAddr(self, addr):
        return self.bank + addr

    def findInstrListAddrs(self):
        # opcodes
        sta = 0x9D
        lda = 0xA9
        rtl = 0x6B
        rts = 0x60

        self.rom.seek(snes_to_pc(self.getShipAddr(self.enemy.initAi)))
        code = []
        for i in range(256):
            byte = self.rom.readByte()
            code.append(byte)
            if byte in (rtl, rts):
                break

        # we're looking for that:
        # $A2:A659 A9 16 A6    LDA #$A616             ;\
        # $A2:A65C 9D 92 0F    STA $0F92,x[$7E:0F92]  ;} Enemy instruction list pointer = $A616
        # $A2:A6F4 A9 1C A6    LDA #$A61C             ;\ Else ([enemy parameter 2] = 0):
        # $A2:A6F7 9D 92 0F    STA $0F92,x[$7E:0FD2]  ;} Enemy instruction list pointer = $A61C
        instrListAddrs = []
        for i, opcode in enumerate(code):
            if opcode != lda:
                continue
            if i+4 > len(code):
                break
            if code[i+3] != sta:
                continue
            if code[i+4] != 0x92 or code[i+5] != 0x0F:
                continue
            # we found it
            instrListAddrs.append(code[i+1] + (code[i+2] << 8))
            print("instr list addr found: {} ({} {})".format(hex(instrListAddrs[-1]), hex(code[i+1]), hex(code[i+2])))

        if not instrListAddrs:
            raise Exception("at {} ship has custom ASM for its init".format(hex(self.enemy.initAi)))

        return instrListAddrs

    def load(self):
        instrListAddrs = self.findInstrListAddrs()

        self.spritemapAddr = None
        for addr in instrListAddrs:
            # load instruction list
            self.rom.seek(snes_to_pc(self.getShipAddr(addr)))

            # first word is frame delay
            frameDelay = self.rom.readWord()
            if frameDelay >= 0x8000:
                print("at {} not a frame delay: {}".format(hex(addr), hex(frameDelay)))
                continue

            # second word is spritemap pointer
            spritemapAddr = self.rom.readWord()
            if spritemapAddr < 0x8000:
                print("at {} not a spritemap pointer: {}".format(hex(addr+2), hex(spritemapAddr)))
                continue

            # third word is sleep
            sleep = self.rom.readWord()
            if sleep != Ship.sleepInstr:
                print("at {} not a sleep instruction: {}".format(hex(addr+4), hex(sleep)))
                continue

            # found
            self.spritemapAddr = spritemapAddr
            break

        if not self.spritemapAddr:
            raise Exception("Can't find spritemap addr")

        # load spritemaps
        self.spritemap = Spritemap(self.rom, self.getShipAddr(self.spritemapAddr), self.center)

class Spritemap(object):
    def __init__(self, rom, dataAddr, center):
        self.rom = rom
        print("load spritemap at {}".format(hex(dataAddr)))
        self.dataAddr = dataAddr
        self.center = center
        self.load()

    def load(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        self.oamCount = self.rom.readWord()
        if self.oamCount > 0x100:
            raise Exception("at {} spritemap oam count is too high: {}".format(hex(self.dataAddr), hex(self.oamCount)))
        print("load spritemap at {} with {} OAMs".format(hex(self.dataAddr), self.oamCount))
        self.oams = []
        for i in range(self.oamCount):
            curAddr = 2+ self.dataAddr + i * OAM.size
            oam = OAM(self.rom, curAddr, self.center)
            #oam.debug()
            self.oams.append(oam)

        self.boundingRect = self.getBoundingRect()

    def getBoundingRect(self):
        r = BoundingRect()
        for oam in self.oams:
            r.add(oam.realX, oam.realY)
        #r.debug()
        return r

class BoundingRect(object):
    def __init__(self):
        # top left corner, y=0 is top, x=0 is left
        self.x1 = sys.maxsize
        self.y1 = sys.maxsize

        # bottom right corner
        self.x2 = 0
        self.y2 = 0

        # 16x16 pixels
        self.size = 16

    def add(self, x, y):
        if x < self.x1:
            self.x1 = x
        if y < self.y1:
            self.y1 = y
        if x+self.size > self.x2:
            self.x2 = x+self.size
        if y+self.size > self.y2:
            self.y2 = y+self.size

    def isInside(self, x, y):
        # x,y are in 16x16 tile size
        x += 1
        x *= 16
        y *= 16
        return x > self.x1 and x < self.x2 and y > self.y1 and y < self.y2

    def debug(self):
        print("bounding rect:")
        print("{:3} {:3}           ".format(self.x1, self.y1))
        print("           {:3} {:3}".format(self.x2, self.y2))

    def width(self):
        return int((self.x2 - self.x1)/16)

    def height(self):
        return int((self.y2 - self.y1)/16)

    def start(self):
        return (int(self.x1/16), int(self.y1/16)+1)

class OAM(object):
    # an oam entry is made of five bytes: (s000000 xxxxxxxxx) (yyyyyyyy) (YXppPPPt tttttttt)
    size = 5

    def __init__(self, rom, dataAddr, center):
        self.rom = rom
        self.dataAddr = dataAddr
        # (x, y) position in the displayed screen
        # $12: Y pos, $14 X pos as parameter to 818AB8
        self.center = center
        self.load()

    def fixX(self, lowerX, highX):
        if highX == 0:
            # after center
            return lowerX + self.center[0]
        else:
            # before center
            return (lowerX + self.center[0]) & 0xFF

    def fixY(self, y):
        return (y + self.center[1]) & 0xFF

    def load(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        w1 = self.rom.readWord()
        b = self.rom.readByte()
        w2 = self.rom.readWord()

        self.size = w1 >> 15
        self.unknown = (w1 >> 9) & 0x3F
        self.lowerX = w1 & 0x1FF
        self.highX = (w1 & 0x100) >> 8
        self.realX = self.fixX(self.lowerX, self.highX)
        self.y = b
        self.realY = self.fixY(self.y)
        self.xFlip = (w2 >> 14) & 1
        self.yFlip = w2 >> 15
        self.priority = (w2 >> 12) & 0b11
        self.palette = (w2 >> 9) & 0b111
        self.tile = w2 & 0xFF

        self.raw = "{} {} {}".format(hex(w1), hex(b), hex(w2))

    def debug(self):
        print("OAM at {} size: {} x: {:3} y: {:3} Xflip: {} Yflip: {} priority: {} palette: {} tile: {:3} raw: {}".format(self.dataAddr, self.size, self.realX, self.realY, self.xFlip, self.yFlip, self.priority, self.palette, self.tile, self.raw))

class EnemyHeader(object):
    def __init__(self, rom, dataAddr):
        self.rom = rom
        self.dataAddr = dataAddr
        self.load()

    def load(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        self.tileDataSize = self.rom.readWord()
        self.palette = self.rom.readWord()
        self.health = self.rom.readWord()
        self.damage = self.rom.readWord()
        self.xRadius = self.rom.readWord()
        self.yRadius = self.rom.readWord()
        self.bank = self.rom.readByte()
        self.hurtAiTime = self.rom.readByte()
        self.cry = self.rom.readWord()
        self.bossValue = self.rom.readWord()
        self.initAi = self.rom.readWord()
        self.numberParts = self.rom.readWord()
        self.rom.readWord()
        self.mainAi = self.rom.readWord()
        self.grappleAi = self.rom.readWord()
        self.hurtAi = self.rom.readWord()
        self.frozenAi = self.rom.readWord()
        self.XrayAi = self.rom.readWord()
        self.deathAnim = self.rom.readWord()
        self.rom.readWord()
        self.rom.readWord()
        self.pbReaction = self.rom.readWord()
        self.rom.readWord()
        self.rom.readWord()
        self.rom.readWord()
        self.enemyTouch = self.rom.readWord()
        self.enemyShot = self.rom.readWord()
        self.rom.readWord()
        self.tileData = self.rom.readBytes(3)
        self.layer = self.rom.readByte()
        self.dropChance = self.rom.readWord()
        self.vulnerabilities = self.rom.readWord()
        self.enemyName = self.rom.readWord()

    def debug(self):
        print("")
        print("enemy: {}".format(hex(self.enemyId)))
        for key, value in self.__dict__.items():
            if key == 'rom':
                continue
            print("{}: {}".format(key, hex(value)))

class Transform(Enum):
    Mirror = 0

class Room(object):
    def __init__(self, rom, dataAddr):
        self.rom = rom
        self.dataAddr = dataAddr
        self.load()

    def load(self):
        print("* load room header")
        self.loadHeader()
        print("* load state headers")
        self.loadStateHeaders()
        print("* load states")
        self.loadStates()
        print("* load enemies")
        self.loadEnemies()
        print("* load PLMs")
        self.loadPLMs()
        print("* load VARIA area")
        self.loadVariaArea()
        print("* load layouts")
        self.loadLayout()
        print("* load scrolls")
        self.loadScrolls()
        print("* load doors")
        self.loadDoors()
        print("")

    def loadHeader(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        self.roomIndex = self.rom.readByte()
        self.area = self.rom.readByte()
        self.mapX = self.rom.readByte()
        self.mapY = self.rom.readByte()
        self.width = self.rom.readByte()
        self.height = self.rom.readByte()
        self.upScroller = self.rom.readByte()
        self.downScroller = self.rom.readByte()
        self.specialGfxBitflag = self.rom.readByte()
        # LoROM address
        self.doorsPtr = 0x8F0000 + self.rom.readWord()
        print("room: {}".format(hex(self.dataAddr)))

    def loadStateHeaders(self):
        self.roomStateHeaders = []
        roomStateHeader = RoomStateHeader(self.rom, pc_to_snes(self.rom.tell()))
        print("state header: {} type: {}".format(hex(roomStateHeader.dataAddr), hex(roomStateHeader.headerType)))
        assert roomStateHeader.headerType != 0, "state type is 0"
        self.roomStateHeaders.append(roomStateHeader)
        while roomStateHeader.headerType != StateType.Standard:
            roomStateHeader = RoomStateHeader(self.rom, pc_to_snes(self.rom.tell()))
            assert roomStateHeader.headerType != 0, "state type is 0"
            print("state header: {} type: {}".format(hex(roomStateHeader.dataAddr), hex(roomStateHeader.headerType)))
            self.roomStateHeaders.append(roomStateHeader)

    def loadStates(self):
        self.roomStates = {}
        for roomStateHeader in self.roomStateHeaders:
            print("state: {}".format(hex(roomStateHeader.roomStatePtr)))
            roomState = RoomState(self.rom, roomStateHeader.roomStatePtr)
            self.roomStates[roomStateHeader.roomStatePtr] = roomState
            # choose one of the standard state as the state we're going to use
            if roomStateHeader.headerType == StateType.Standard:
                self.defaultRoomState = roomState

    def loadEnemies(self):
        # loop on room state then on enemy set
        self.enemies = {}
        self.enemyHeaders = {}

        for state in self.roomStates.values():
            if state.enemySetPtr in self.enemies:
                continue

            self.enemies[state.enemySetPtr] = []

            self.rom.seek(snes_to_pc(state.enemySetPtr))
            enemyId = 0
            for _ in range(32):
                enemyId = self.rom.readWord()
                if enemyId == 0xFFFF:
                    break
                self.enemies[state.enemySetPtr].append(EnemyInstance(self.rom, enemyId, pc_to_snes(self.rom.tell()-2)))

            for enemy in self.enemies[state.enemySetPtr]:
                if enemy.enemyId not in self.enemyHeaders:
                    self.enemyHeaders[enemy.enemyId] = EnemyHeader(self.rom, 0xA00000+enemyId)

        for setPtr, enemies in self.enemies.items():
            print("enemies in set {}: {}".format(hex(setPtr), [hex(enemy.enemyId) for enemy in enemies]))

    def loadPLMs(self):
        # loop on room state then on plm set
        self.plms = {}

        for state in self.roomStates.values():
            if state.plmSetPtr in self.plms:
                continue

            self.plms[state.plmSetPtr] = []

            plmSize = 6
            self.rom.seek(snes_to_pc(state.plmSetPtr))
            plmId = 0
            for i in range(40):
                plmId = self.rom.readWord()
                if plmId == 0x0000:
                    break
                self.plms[state.plmSetPtr].append(PLM(self.rom, plmId))

        for setPtr, plms in self.plms.items():
            print("plms in set {}: {}".format(hex(setPtr), [hex(plm.plmId) for plm in plms]))

    def loadVariaArea(self):
        for roomStateHeader in self.roomStateHeaders:
            # only standard state
            if roomStateHeader.headerType == StateType.Standard:
                self.variaArea = self.roomStates[roomStateHeader.roomStatePtr].unusedPtr & 0xffff

    def loadLayout(self):
        self.levelData = {}
        for state in self.roomStates.values():
            if state.levelDataPtr in self.levelData:
                continue
            print("level data set: {}".format(hex(state.levelDataPtr)))
            self.levelData[state.levelDataPtr] = LevelData(self.rom, state.levelDataPtr, (self.width, self.height))

    def loadScrolls(self):
        self.scrolls = {}
        for state in self.roomStates.values():
            if state.scrollSetPtr in self.scrolls:
                continue
            self.scrolls[state.scrollSetPtr] = Scroll(self.rom, state.scrollSetPtr, (self.width, self.height))

        for setPtr, scroll in self.scrolls.items():
            print("scrolls in set {}: {}".format(hex(setPtr), scroll.screens))

    def loadDoors(self):
        # load all ROM doors to get these pointing to the room
        doorsSetsAddr = [(0x8388FE, 0x839AC2), (0x83A18C, 0x83ABF0)]
        doorSize = 12
        doors = defaultdict(list)
        for (start, end) in doorsSetsAddr:
            self.rom.seek(snes_to_pc(start))
            for i in range((end-start)//doorSize):
                self.rom.seek(start + i*doorSize)
                doorId = pc_to_snes(self.rom.tell()) & 0xffff
                door = Door(self.rom, doorId)
                doors[door.destRoom & 0xffff].append(door)

        self.doors = doors[self.dataAddr & 0xffff]

        print("doors: {}".format([hex(door.doorId) for door in self.doors]))

    def write(self):
        print("* write room header")
        self.writeHeader()
        print("* write state headers")
        self.writeStateHeaders()
        print("* write states")
        self.writeStates()
        print("* write enemies")
        self.writeEnemies()
        print("* write PLMs")
        self.writePLMs()
        print("* write layouts")
        self.writeLayout()
        print("* write scrolls")
        self.writeScrolls()
        print("* write doors")
        self.writeDoors()

    def writeHeader(self):
        self.rom.seek(snes_to_pc(self.dataAddr))

        self.rom.writeByte(self.roomIndex)
        self.rom.writeByte(self.area)
        self.rom.writeByte(self.mapX)
        self.rom.writeByte(self.mapY)
        self.rom.writeByte(self.width)
        self.rom.writeByte(self.height)
        self.rom.writeByte(self.upScroller)
        self.rom.writeByte(self.downScroller)
        self.rom.writeByte(self.specialGfxBitflag)
        self.rom.writeWord(self.doorsPtr & 0xffff)

    def writeStateHeaders(self):
        for roomStateHeader in self.roomStateHeaders:
            roomStateHeader.write()

    def writeStates(self):
        for state in self.roomStates.values():
            state.write()

    def writeEnemies(self):
        for enemySetPtr, enemies in self.enemies.items():
            for enemy in enemies:
                enemy.write()

    def writePLMs(self):
        for plmSetPtr, plms in self.plms.items():
            self.rom.seek(snes_to_pc(plmSetPtr))
            for plm in plms:
                plm.write()

    def writeLayout(self):
        for layout in self.levelData.values():
            layout.unload()
            layout.write()

    def writeScrolls(self):
        for scroll in self.scrolls.values():
            scroll.write()

    def writeDoors(self):
        for door in self.doors:
            door.write()

    def transform(self, transformation):
        if transformation == Transform.Mirror:
            print("* transform room: {}".format(transformation))

            # enemies
            for enemySetPtr, enemies in self.enemies.items():
                for enemy in enemies:
                    enemy.transform(transformation, (self.width, self.height))

            # plms
            for plmSetPtr, plms in self.plms.items():
                self.rom.seek(snes_to_pc(plmSetPtr))
                for plm in plms:
                    plm.transform(transformation, (self.width, self.height))

            # scrolls
            for scroll in self.scrolls.values():
                scroll.transform(transformation, (self.width, self.height))

            # doors
            for door in self.doors:
                door.transform(transformation, (self.width, self.height))

            # layout
            for layout in self.levelData.values():
                layout.transform(transformation, (self.width, self.height))

        else:
            raise Exception("{} not implemented".format(transformation))

        print("")

class StateType:
    Standard = 0xE5E6
    Events = 0xE612
    Bosses = 0xE629
    TourianBoss = 0xE5FF
    Morph = 0xE640
    MorphMissiles = 0xE652
    PowerBombs = 0xE669
    SpeedBooster = 0xE676

class RoomStateHeader(object):
    sizeStandard = 2
    sizeEvents = 5
    sizeItems = 4

    def __init__(self, rom, dataAddr):
        self.rom = rom
        self.dataAddr = dataAddr
        self.load()

    def load(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        self.headerType = self.rom.readWord()
        self.value = 0

        if self.headerType == StateType.Standard:
            self.roomStatePtr = self.dataAddr+2
        elif self.headerType in [StateType.Events, StateType.Bosses]:
            self.value = self.rom.readByte()
            self.roomStatePtr = 0x8F0000 + self.rom.readWord()
        else:
            self.roomStatePtr = 0x8F0000 + self.rom.readWord()

    def size(self):
        if self.headerType == StateType.Standard:
            return RoomStateHeader.sizeStandard
        elif self.headerType in [StateType.Events, StateType.Bosses]:
            return RoomStateHeader.sizeEvents
        else:
            return RoomStateHeader.sizeItems

    def write(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        self.rom.writeWord(self.headerType)

        if self.headerType == StateType.Standard:
            pass
        elif self.headerType in [StateType.Events, StateType.Bosses]:
            self.rom.writeByte(self.value)
            self.rom.writeWord(self.roomStatePtr & 0xffff)
        else:
            self.rom.writeWord(self.roomStatePtr & 0xffff)

class RoomState(object):
    def __init__(self, rom, dataAddr):
        self.rom = rom
        self.dataAddr = dataAddr
        self.load()

    def load(self):
        self.rom.seek(snes_to_pc(self.dataAddr))

        self.levelDataPtr        = self.rom.readBytes(3)
        self.tileSet             = self.rom.readByte()
        self.songSet             = self.rom.readByte()
        self.playIndex           = self.rom.readByte()
        self.fxPtr               = 0x830000 + self.rom.readWord()
        self.enemySetPtr         = 0xA10000 + self.rom.readWord()
        self.enemyGfxPtr         = 0xB40000 + self.rom.readWord()
        self.backgroundScrolling = self.rom.readWord()
        self.scrollSetPtr        = 0x8F0000 + self.rom.readWord()
        self.unusedPtr           = 0x8F0000 + self.rom.readWord() # in VARIA store area id
        self.mainAsmPtr          = 0x8F0000 + self.rom.readWord()
        self.plmSetPtr           = 0x8F0000 + self.rom.readWord()
        self.backgroundPtr       = 0x8F0000 + self.rom.readWord()
        self.setupAsmPtr         = 0x8F0000 + self.rom.readWord()

    def write(self):
        self.rom.seek(snes_to_pc(self.dataAddr))

        self.rom.writeBytes(self.levelDataPtr, 3)
        self.rom.writeByte(self.tileSet)
        self.rom.writeByte(self.songSet)
        self.rom.writeByte(self.playIndex)
        self.rom.writeWord(self.fxPtr & 0xffff)
        self.rom.writeWord(self.enemySetPtr  & 0xffff)
        self.rom.writeWord(self.enemyGfxPtr  & 0xffff)
        self.rom.writeWord(self.backgroundScrolling)
        self.rom.writeWord(self.scrollSetPtr & 0xffff)
        self.rom.writeWord(self.unusedPtr   & 0xffff)
        self.rom.writeWord(self.mainAsmPtr  & 0xffff)
        self.rom.writeWord(self.plmSetPtr   & 0xffff)
        self.rom.writeWord(self.backgroundPtr  & 0xffff)
        self.rom.writeWord(self.setupAsmPtr  & 0xffff)

class EnemyInstance(object):
    def __init__(self, rom, enemyId, dataAddr):
        self.rom = rom
        self.enemyId = enemyId
        self.dataAddr = dataAddr
        self.load()

    def load(self):
        # offset in rom is already set to after id
        self.Xpos = self.rom.readWord()
        self.Ypos = self.rom.readWord()
        self.initParam = self.rom.readWord()
        self.properties = self.rom.readWord()
        self.extraProperties = self.rom.readWord()
        self.param1 = self.rom.readWord()
        self.param2 = self.rom.readWord()

    def write(self):
        self.rom.seek(snes_to_pc(self.dataAddr))

        self.rom.writeWord(self.enemyId)
        self.rom.writeWord(self.Xpos)
        self.rom.writeWord(self.Ypos)
        self.rom.writeWord(self.initParam)
        self.rom.writeWord(self.properties)
        self.rom.writeWord(self.extraProperties)
        self.rom.writeWord(self.param1)
        self.rom.writeWord(self.param2)

    def transform(self, transformation, size):
        # enemies positions are in pixel unit
        width = size[0] * 256
        height = size[1] * 256
        if transformation == Transform.Mirror:
            print("enemy {}: old x: {} new x: {}".format(hex(self.enemyId), hex(self.Xpos), hex(width - self.Xpos)))
            self.Xpos = width - self.Xpos

class PLM(object):
    @staticmethod
    def factory(rom, plmId):
        if hex(plmId).lower() in RomReader.items:
            return PLMItem(rom, plmId)
        elif plmId in doorPlms:
            return PLMDoor(rom, plmId)
        else:
            return PLM(rom, plmId)

    def __init__(self, rom, plmId):
        self.rom = rom
        self.plmId = plmId
        self.load()

    def load(self):
        # offset in rom is already set to after id
        self.Xpos = self.rom.readByte()
        self.Ypos = self.rom.readByte()
        self.plmParam = self.rom.readWord()

    def write(self):
        # offset in rom is already set to plm start
        self.rom.writeWord(self.plmId)
        self.rom.writeByte(self.Xpos)
        self.rom.writeByte(self.Ypos)
        self.rom.writeWord(self.plmParam)

    def transform(self, transformation, size):
        # plm unit is tiles
        width = size[0] * 16
        height = size[1] * 16
        if transformation == Transform.Mirror:
            self.Xpos = width - self.Xpos - 1

class PLMDoor(PLM):
    def transform(self, transformation, size):
        super().transform(transformation, size)

        if transformation == Transform.Mirror:
            # also change facing
            facing = plmFacing(self.plmId)
            if facing in (Facing.Left, Facing.Right):
                facing = indicatorsDirection[facing]

                for plmColor in plmRed, plmGreen, plmYellow, plmGrey:
                    if self.plmId in plmColor:
                        self.plmId = plmColor[facing]

class PLMItem(PLM):
    pass

class Mode(IntFlag):
    _16 = auto()
    _8 = auto()

# REP #$10 Sets X and Y to 16-bit mode
# REP #$20 Sets A to 16-bit mode
# REP #$30 Sets A, X and Y to 16-bit mode
# SEP #$10 Sets X and Y to 8-bit mode
# SEP #$20 Sets A to 8-bit mode
# SEP #$30 Sets A, X and Y to 8-bit mode
class CPUState(object):
    def __init__(self):
        self.mi_flag = Mode._16
        self.ma_flag = Mode._16

    def sep(self, newState):
        if newState & 0x10:
            self.mi_flag = Mode._8
        if newState & 0x20:
            self.ma_flag = Mode._8

    def rep(self, newState):
        if newState & 0x10:
            self.mi_flag = Mode._16
        if newState & 0x20:
            self.ma_flag = Mode._16

class Opcode(object):
    @staticmethod
    def factory(rom, cpuState):
        opcode = rom.readByte()
        if opcode == 0x08:
            return PHP()
        elif opcode == 0xE2:
            newState = rom.readByte()
            cpuState.sep(newState)
            return SEP(newState)
        elif opcode == 0xA9:
            if cpuState.ma_flag == Mode._16:
                return LDA_IMM(rom.readWord(), cpuState.ma_flag)
            else:
                return LDA_IMM(rom.readByte(), cpuState.ma_flag)
        elif opcode == 0x8F:
            return STA_LONG(rom.readLong())
        elif opcode == 0x28:
            return PLP()
        elif opcode == 0x60:
            return RTS()
        else:
            return UNKNOWN(opcode)

class PHP(Opcode):
    opcode = 0x08
    def write(self, rom):
        rom.writeByte(PHP.opcode)
    def display(self):
        return "PHP"

class SEP(Opcode):
    opcode = 0xE2
    def __init__(self, value):
        self.value = value
    def write(self, rom):
        rom.writeByte(SEP.opcode)
        rom.writeByte(self.value)
    def display(self):
        return "SEP #${:02x}".format(self.value)

class LDA_IMM(Opcode):
    opcode = 0xA9
    def __init__(self, value, flag):
        self.value = value
        self.flag = flag
    def write(self, rom):
        rom.writeByte(LDA_IMM.opcode)
        if self.flag == Mode._16:
            rom.writeWord(self.value)
        else:
            rom.writeByte(self.value)
    def display(self):
        if self.flag == Mode._16:
            return "LDA #${:04x}".format(self.value)
        else:
            return "LDA #${:02x}".format(self.value)

class STA_LONG(Opcode):
    opcode = 0x8F
    def __init__(self, value):
        self.value = value
    def write(self, rom):
        rom.writeByte(STA_LONG.opcode)
        rom.writeLong(self.value)
    def display(self):
        return "STA ${:06x}".format(self.value)

class PLP(Opcode):
    opcode = 0x28
    def write(self, rom):
        rom.writeByte(PLP.opcode)
    def display(self):
        return "PLP"

class RTS(Opcode):
    opcode = 0x60
    def write(self, rom):
        rom.writeByte(RTS.opcode)
    def display(self):
        return "RTS"

class UNKNOWN(Opcode):
    def __init__(self, opcode):
        self.opcode = opcode
    def display(self):
        return "Unknown opcode: {:02x}".format(self.opcode)

class Door(object):
    def __init__(self, rom, doorId):
        self.rom = rom
        self.doorId = doorId
        self.dataAddr = 0x830000 + self.doorId
        self.load()

    def load(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        self.destRoom = 0x8f0000 + self.rom.readWord()
        self.elevatorProperties = self.rom.readByte()
        self.orientation = self.rom.readByte()
        self.capX = self.rom.readByte()
        self.capY = self.rom.readByte()
        self.screenX = self.rom.readByte()
        self.screenY = self.rom.readByte()
        self.distanceToSpawn = self.rom.readWord()
        self.customASM = 0x8f0000 + self.rom.readWord()

        if self.customASM != 0x8f0000:
            self.loadASM()

    def loadASM(self):
        self.asm = []
        self.rom.seek(snes_to_pc(self.customASM))

        self.validASM = False
        cpuState = CPUState()

        while True:
            self.asm.append(Opcode.factory(self.rom, cpuState))

            # read until RTS
            if type(self.asm[-1]) is RTS:
                self.validASM = True
                break
            elif type(self.asm[-1]) is UNKNOWN:
                self.validASM = False
                break

    def write(self):
        self.rom.seek(snes_to_pc(self.dataAddr))

        self.rom.writeWord(self.destRoom & 0xffff)
        self.rom.writeByte(self.elevatorProperties)
        self.rom.writeByte(self.orientation)
        self.rom.writeByte(self.capX)
        self.rom.writeByte(self.capY)
        self.rom.writeByte(self.screenX)
        self.rom.writeByte(self.screenY)
        self.rom.writeWord(self.distanceToSpawn)
        self.rom.writeWord(self.customASM & 0xffff)

        if self.customASM != 0x8f0000 and self.validASM:
            self.writeASM()

    def writeASM(self):
        self.rom.seek(snes_to_pc(self.customASM))
        for opcode in self.asm:
            opcode.write(self.rom)

    def displayASM(self):
        if self.customASM != 0x8f0000:
            out = ""
            out += "org ${:06x}\n".format(self.customASM)
            for opcode in self.asm:
                out += "    {}\n".format(opcode.display())
            return (self.customASM, out)
        else:
            return (None, None)

    def transform(self, transformation, size):
        # cap unit is tiles
        width = size[0] * 16
        height = size[1] * 16
        if transformation == Transform.Mirror:
            self.screenX = size[0] - self.screenX - 1
            self.capX = width - self.capX - 1

        # $7E:CD20..51: Scrolls
        #     0: Red. Cannot scroll into this area
        #     1: Blue. Hides the bottom 2 rows of the area
        #     2: Green. Unrestricted
        if self.customASM != 0x8f0000 and self.validASM:
            scrolls_start = 0x7ECD20
            for opcode in self.asm:
                if type(opcode) == STA_LONG:
                    screen = opcode.value - scrolls_start
                    x = screen % size[0]
                    y = screen // size[0]
                    if transformation == Transform.Mirror:
                        x = size[0] - x - 1
                        screen = x + y * size[0]
                    opcode.value = scrolls_start + screen

class Scroll(object):
    def __init__(self, rom, dataAddr, size):
        self.rom = rom
        self.dataAddr = dataAddr
        # (screens X, screens Y)
        self.size = size
        self.load()

    def load(self):
        self.rom.seek(snes_to_pc(self.dataAddr))
        self.screens = []
        for _ in range(self.size[0] * self.size[1]):
            self.screens.append(self.rom.readByte())

    def write(self):
        self.rom.seek(snes_to_pc(self.dataAddr))

        for scroll in self.screens:
            self.rom.writeByte(scroll)

    def transform(self, transformation, size):
        # scroll unit is screens
        width = size[0]
        height = size[1]
        if transformation == Transform.Mirror:
            transScreens = [0]*(width * height)
            for x in range(width):
                for y in range(height):
                    transScreens[x + y*width] = self.screens[(width - x - 1) + y*width]
            self.screens = transScreens

class LevelData(object):
    def __init__(self, rom, dataAddr, size):
        self.log = utils.log.get('LevelData')
        self.rom = rom
        self.dataAddr = dataAddr
        # [width, height] in screens
        self.size = size
        self.screenCount = 0

        self.layer1 = []
        self.layer2 = []
        self.bts = []

        self.loaded = False
        self.compressedSize = 0
        self.rawData = []

        self.load()

    def _concatBytes(self, b0, b1):
        return b0 + (b1 << 8)

    def _unconcatWord(self, w):
        return [w & 0x00FF, (w & 0xFF00) >> 8]

    def debug(self):
        print("compressedSize: {}".format(self.compressedSize))
        print("decompressedSize: {}".format(self.decompressedSize))
        print("screenCount: {}".format(self.screenCount))
        print("layer1Size: {}".format(self.layer1Size))
        print("btsSize: {}".format(self.btsSize))
        print("layer2Size: {}".format(self.layer2Size))
        print("len layer1: {}".format(len(self.layer1)))
        print("len bts: {}".format(len(self.bts)))
        print("len layer2: {}".format(len(self.layer2)))

    def displayLayoutTile(self, t, displayBts=True):
        tile = t & 0x3FF
        hflip = (t >> 10) & 1
        vflip = (t >> 11) & 1
        btsType = (t >> 12) & 0xF
        if displayBts:
            return "{:3}|{}|{}|{}".format(hex(tile)[2:], hflip, vflip, hex(btsType)[2:])
        else:
            return "{:2}|{}|{}  ".format(hex(tile)[2:], hflip, vflip)

    def displayScreen(self, screen):
        x, y = screen
        # a screen is 16x16 tiles
        base = x * 16 + y * self.size[0] * 256
        nextRow = self.size[0] * 16
        print("layer1:")
        for i in range(16):
            rowBase = base + i * nextRow
            print(["{}/{:3}".format(self.displayLayoutTile(t), b) for (t, b) in zip(self.layer1[rowBase:rowBase+16], self.bts[rowBase:rowBase+16])])

    def displayBts(self, b):
        if b >= 0x80:
            vFlip = 1
            b ^= 0x80
        else:
            vFlip = 0
        if b >= 0x40:
            hFlip = 1
            b ^= 0x40
        else:
            hFlip = 0
        return "{:2}|{}|{}".format(hex(b)[2:], hFlip, vFlip)

    def displaySubScreen(self, screen, boundingRect):
        x, y = screen
        # display only boundingRect of screen (x,y), display only bts
        base = x * 16 + y * self.size[0] * 256
        nextRow = self.size[0] * 16
        print("subscreen: (bts value|hFlip|vFlip|type)")
        print("subscreen: (layout tile|hFlip|vFlip)")
        for i in range(16):
            rowBase = base + i * nextRow
            print(" ".join(["{}|{:1}".format(self.displayBts(b), hex((t >> 12) & 0xF)[2:]) if boundingRect.isInside(j, i) else "    .   " for j, (t, b) in enumerate(zip(self.layer1[rowBase:rowBase+16], self.bts[rowBase:rowBase+16]))]))
            print(" ".join([self.displayLayoutTile(t, displayBts=False) if boundingRect.isInside(j, i) else "    .   " for j, t in enumerate(self.layer1[rowBase:rowBase+16])]))

    def load(self):
        data = Compressor().decompress(self.rom, snes_to_pc(self.dataAddr))
        self.compressedSize = data[0]
        print("compressed data size: {}".format(self.compressedSize))
        self.rawData = data[1]
        self.decompressedSize = len(self.rawData)
        print("uncompressed data size: {}".format(self.decompressedSize))

        self.layer1Size = self._concatBytes(self.rawData[0], self.rawData[1])
        self.btsSize = int(self.layer1Size / 2)
        if self.layer1Size + self.btsSize + 2 < self.decompressedSize:
            self.layer2Size = self.layer1Size
        else:
            self.layer2Size = 0
        self.screenCount = int(self.btsSize / 256)

        print("size layer1: {} bts: {} layer2: {}".format(self.layer1Size, self.btsSize, self.layer2Size))

        if self.layer1Size + self.btsSize + self.layer2Size + 2 != self.decompressedSize:
            print("WARNING: wrong decompressed data size")
            if self.decompressedSize == self.layer1Size + self.btsSize + self.layer2Size + 2 - 1:
                print("add missing byte in layer2 data")
                self.rawData.append(0x3)

        # validate that raw data is ok
        if self.log.getEffectiveLevel() == logging.DEBUG:
            for i, r in enumerate(self.rawData):
                if r >= 0x100:
                    assert False, "byte in rawData at {} is too big: {}".format(i, hex(r))

        layer1Counter = 2
        btsCounter = 2 + self.layer1Size
        layer2Counter = 2 + self.layer1Size + self.btsSize

        for i in range(self.btsSize):
            self.layer1.append(self._concatBytes(self.rawData[layer1Counter], self.rawData[layer1Counter+1]))
            self.bts.append(self.rawData[btsCounter])
            if self.layer2Size > 0:
                self.layer2.append(self._concatBytes(self.rawData[layer2Counter], self.rawData[layer2Counter+1]))

            layer1Counter += 2
            btsCounter += 1
            layer2Counter += 2

        print("len layer1: {} bts: {} layer2: {}".format(len(self.layer1), len(self.bts), len(self.layer2)))

    def unload(self):
        # rebuild raw data
        rawData = []
        rawData += self._unconcatWord(self.layer1Size)
        # transform back from word to byte
        print("layer1 size: {}".format(self.layer1Size))
        print("len(layer1): {}".format(len(self.layer1)))

        for word in self.layer1:
            rawData += self._unconcatWord(word)

        print("len rawData with layer1: {}".format(len(rawData)))

        rawData += self.bts

        for word in self.layer2:
            rawData += self._unconcatWord(word)

        print("len rawData: {}".format(len(rawData)))
        return rawData

    def write(self, vanillaSize=None):
        if vanillaSize is None:
            vanillaSize = self.compressedSize

        # rebuild raw data
        rawData = self.unload()
        print("rawData len: {}".format(len(rawData)))

        # recompress data
        compressedData = Compressor(profile='Slow').compress(rawData)
        recompressedDataSize = len(compressedData)
        print("compressedData len: {} (old: {}, vanilla: {})".format(recompressedDataSize, self.compressedSize, vanillaSize))
        assert recompressedDataSize <= vanillaSize
        # write compress data
        self.rom.seek(snes_to_pc(self.dataAddr))
        for byte in compressedData:
            self.rom.writeByte(byte)

    def copyLayout(self, screen, boundingRect):
        # copy layer1 and bts
        x, y = screen
        layer1 = []
        bts = []
        start = boundingRect.start()
        width = boundingRect.width()
        height = boundingRect.height()
        base = x * 16 + start[0] + y * self.size[0] * 256 + start[1] * self.size[0] * 16
        nextRow = self.size[0] * 16

        boundingRect.debug()
        print("copy: start: {} width: {} height: {}".format(start, width, height))

        for i in range(height):
            rowBase = base + i * nextRow
            layer1 += self.layer1[rowBase:rowBase+width]
            bts += self.bts[rowBase:rowBase+width]

        self.displayCopy(layer1, bts, boundingRect)

        return (layer1, bts)

    def displayCopy(self, layer1, bts, boundingRect):
        width = boundingRect.width()
        height = boundingRect.height()
        for i in range(height):
            print(" ".join(["{}|{:1}".format(self.displayBts(b), hex((t >> 12) & 0xF)[2:]) for (t, b) in zip(layer1[i*width:(i+1)*width], bts[i*width:(i+1)*width])]))
            print(" ".join([self.displayLayoutTile(t, displayBts=False) for t in layer1[i*width:(i+1)*width]]))


    def pasteLayout(self, data, screen, boundingRect):
        x, y = screen
        layer1 = data[0]
        bts = data[1]
        start = boundingRect.start()
        width = boundingRect.width()
        height = boundingRect.height()

        base = x * 16 + start[0] + y * self.size[0] * 256 + start[1] * self.size[0] * 16
        nextRow = self.size[0] * 16

        boundingRect.debug()
        print("paste: start: {} width: {} height: {}".format(start, width, height))

        for i in range(height):
            rowBase = base + i * nextRow
            for j in range(width):
                self.layer1[rowBase+j] = layer1[i*width+j]
                self.bts[rowBase+j] = bts[i*width+j]

    def emptyLayout(self, screen, boundingRect):
        x, y = screen
        start = boundingRect.start()
        width = boundingRect.width()
        height = boundingRect.height()

        defaultLayer = 0xFF
        defaultBts = 0x00

        base = x * 16 + start[0] + y * self.size[0] * 256 + start[1] * self.size[0] * 16
        nextRow = self.size[0] * 16

        boundingRect.debug()
        print("empty: start: {} width: {} height: {}".format(start, width, height))

        for i in range(height):
            rowBase = base + i * nextRow
            for j in range(width):
                self.layer1[rowBase+j] = defaultLayer
                self.bts[rowBase+j] = defaultBts

    def getTileAddr(self, screen, tx, ty):
        (sx, sy) = screen
        base = sx * 16 + sy * self.size[0] * 256
        nextRow = self.size[0] * 16

        rowBase = base + ty * nextRow
        return rowBase + tx

    def getTileAddrInv(self, i):
        rowLength = self.size[0] * 16
        y = i // rowLength
        sy = y // 16
        ty = y % 16

        x = i % rowLength
        sx = x // 16
        tx = x % 16

        return (sx, sy, tx, ty)

    def getTile(self, screen, tx, ty):
        addr = self.getTileAddr(screen, tx, ty)
        return (self.layer1[addr], self.bts[addr])

    def updateTile(self, screen, tx, ty, newTile, newBTS):
        tileAddr = self.getTileAddr(screen, tx, ty)
        self.layer1[tileAddr] = newTile
        self.bts[tileAddr] = newBTS

    def getModifiedTiles(self, patch):
        modified = set()
        for i, (oTile, pTile) in enumerate(zip(self.layer1, patch.layer1)):
            if oTile != pTile:
                modified.add(i)
        for i, (oBTS, pBTS) in enumerate(zip(self.bts, patch.bts)):
            if oBTS != pBTS:
                modified.add(i)

        ret = []
        for i in modified:
            # transform i into (sx, sy, tx, ty)
            (sx, sy, tx, ty) = self.getTileAddrInv(i)
            ret.append((sx, sy, tx, ty))

        return ret

    def transformPos(self, transformation, sx, sy, tx, ty, screenSize):
        if transformation == Transform.Mirror:
            # in vanilla tile is in screen (0, 0) at pos (6, 6)
            # in mirror  tile is in screen (1, 0) at pos (9, 6)
            # => screen x: width in screens - 1 - vanilla screen x
            # => screen y: the same
            # => tile x: screen width in tiles - 1 - vanilla tile x
            # => tile y: the same
            return (screenSize[0] - 1 - sx, sy,
                    16 - 1 - tx,            ty)

    def transformTile(self, transformation, t):
        tile = t & 0x3FF
        hflip = (t >> 10) & 1
        vflip = (t >> 11) & 1
        btsType = (t >> 12) & 0xF

        if transformation == Transform.Mirror:
            # invert hflip
            hflip = 1 - hflip

        return (tile) | (hflip << 10) | (vflip << 11) | (btsType << 12)

    def transform(self, transformation, size):
        # layout unit is tiles
        width = size[0] * 16
        height = size[1] * 16
        if transformation == Transform.Mirror:
            transLayer1 = [0]*len(self.layer1)
            transBts = [0]*len(self.bts)

            for sx in range(size[0]):
                for sy in range(size[1]):
                    for y in range(16):
                        for x in range(16):
                            addr = self.getTileAddr((sx, sy), x, y)
                            tile = self.layer1[addr]
                            bts = self.bts[addr]
                            msx, msy, mx, my = self.transformPos(transformation, sx, sy, x, y, size)
                            newAddr = self.getTileAddr((msx, msy), mx, my)
                            newTile = self.transformTile(transformation, tile)

                            #print("{}: sx: {} sy: {} x: {} y: {} - {}: msx: {} msy: {} mx: {} my: {}".format(addr, sx, sy, x, y, newAddr, msx, msy, mx, my))

                            transLayer1[newAddr] = newTile
                            transBts[newAddr] = bts

            self.layer1 = transLayer1
            self.bts = transBts
