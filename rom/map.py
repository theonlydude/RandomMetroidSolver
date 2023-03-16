
from rom.rom import RealROM
from graph.location import LocationMapTileKind, LocationMapAttrs

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


# "hidden" unused in VARIA (or even replaced), but referencing them is useful for the helper tool
kindToIndex = {
    LocationMapTileKind.FourWallsOneDoor: {"double":0x3, "minor":0x4, "nothing":0x5, "hidden": 0x6, "major":0x7},
    LocationMapTileKind.ThreeWallsOpenBottom: {"double":0x8, "minor":0x9, "nothing":0xa, "major":0xb},
    LocationMapTileKind.ThreeWallsOpenRight: {"double":0x13, "minor":0x14, "nothing":0x15, "hidden": 0x16, "major":0x17},
    LocationMapTileKind.ThreeWallsOneDoorOpenRight: {"minor": 0x1c, "nothing":0x1d, "major": 0x1e},
    LocationMapTileKind.TwoWallsCornerWithPixel: {"minor": 0x20, "nothing": 0x21},
    LocationMapTileKind.TwoWallsCorner: {"double":0x23, "minor":0x24, "nothing":0x25, "hidden": 0x26, "major":0x27},
    LocationMapTileKind.TwoWallsCornerWithHorizontalDoor: {"minor":0x28, "nothing": 0x29, "major":0x2a},
    LocationMapTileKind.TwoWallsCornerWithVerticalDoor: {"minor": 0x2b, "nothing": 0x2c},
    LocationMapTileKind.FourWallsCorridor: {"minor":0x4c, "nothing":0x4d, "major":0x4e},
    LocationMapTileKind.TwoWallsCorridor: {"minor":0x51, "nothing":0x52, "major":0x53},
    LocationMapTileKind.SingleWallHorizontal: {"minor":0x61, "nothing":0x62, "major":0x63},
    LocationMapTileKind.FourWallsTwoDoors: {"minor": 0x6b, "nothing": 0x6c},
    LocationMapTileKind.SingleWallVertical: {"minor":0x71, "nothing":0x72, "major":0x73},
    LocationMapTileKind.ThreeWallsOneDoorOpenBottom: {"nothing":0x90, "minor":0x91, "major":0x92}
}

def getTileKind(tileIndex):
    for kind, indices in kindToIndex.items():
        for category, index in indices.items():
            if index == tileIndex:
                return (kind, category)
    return (LocationMapTileKind.Unknown, "nothing")

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

    def save(self, rom, offset=0):
        rom.seek(offset)
        for page in self.pages:
            for i in range(pageSize*pageSize):
                rom.writeWord(page[i].toWord())

    def savePresence(self, rom, offset=0):
        rom.seek(offset)
        for page in self.pages:
            for i in range((pageSize*pageSize) // 8):
                b = 0
                for s in range(8):
                    tile = page[i*8 + s]
                    if tile.present:
                        b |= 1 << (7 - s)
                rom.writeByte(b)
