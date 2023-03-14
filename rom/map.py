
from rom.rom import RealROM

class BGtile(object):
    def __init__(self, idx, pal, prio=False, hFlip=False, vFlip=False):
        self.idx = idx
        self.pal = pal
        self.prio = prio
        self.hFlip = hFlip
        self.vFlip = vFlip
        self.present = False

    def toWord(self):
        return (idx & 0x3FF)|((pal & 0x7) << 10)|(int(prio) << 13)|(int(hFlip) << 14)|(int(vFlip) << 15)

    @staticmethod
    def fromWord(tile):
        return BGtile(tile & 0x3FF, (tile >> 10) & 0x7, bool(tile & 0x2000), bool(tile & 0x4000), bool(tile & 0x8000))

    def __str__(self):
        return "BGtile[i=$%02x p=$%x %s%s%s%s]" % (self.idx, self.pal, "P" if self.prio else "", "H" if self.hFlip else "", "V" if self.vFlip else "", "X" if self.present else "")

nPages = 2
pageSize = 32

class AreaMap(object):
    def __init__(self, vertical=False):
        self.width = nPages * pageSize if not vertical else pageSize
        self.height = pageSize if not vertical else nPages * pageSize
        self.pages = [[None]*pageSize*pageSize for i in range(nPages)]
        self.vertical = vertical

    def getPage(self, x, y):
        return x // pageSize if not self.vertical else y // pageSize

    def getIndex(self, x, y):
        return pageSize*(y % pageSize) + (x % pageSize)

    def getTile(self, x, y):
        page = self.pages[self.getPage(x, y)]
        return page[self.getIndex(x, y)]

    def setTile(self, x, y, tile):
        page = self.pages[self.getPage(x, y)]
        page[self.getIndex(x, y)] = tile

    def getOffset(self, rom, x, y, mapStart=None):
        if mapStart is not None:
            rom.seek(mapStart)
        addr = rom.tell()
        page, idx = self.getPage(x, y), self.getIndex(x, y)
        addr += pageSize*pageSize*2*page + idx*2
        return addr

    def readBGtile(self, rom, x, y, mapStart=None):
        addr = self.getOffset(rom, x, y, mapStart)
        self.setTile(BGtile.fromWord(rom.readWord(addr)))

    @staticmethod
    def load(mapRom, presenceRom=None, mapOffset=0, presenceOffset=0, vertical=False):
        if presenceRom is None:
            presenceRom = mapRom
        ret = AreaMap(vertical)
        mapRom.seek(mapOffset)
        for page in ret.pages:
            for i in range(pageSize*pageSize):
                page[i] = BGtile.fromWord(mapRom.readWord())
        presenceRom.seek(presenceOffset)
        for page in ret.pages:
            for i in range((pageSize*pageSize) // 8):
                b = presenceRom.readByte()
                for s in range(8):
                    tile = page[i*8 + s]
                    tile.present = bool(b & (1 << (7 - s)))
        return ret

    def writeBGtile(self, rom, x, y, mapStart=0):
        tile = self.getTile(x, y)
        addr = self.getOffset(mapRom, x, y, mapStart)        
        mapRom.writeWord(tile.toWord(), addr)
