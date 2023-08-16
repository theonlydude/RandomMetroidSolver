
from collections import defaultdict
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
        return (self.idx & 0x3FF)|((self.pal & 0x7) << 10)|(int(self.prio) << 13)|(int(self.hFlip) << 14)|(int(self.vFlip) << 15)

    @staticmethod
    def fromWord(tile):
        return BGtile(tile & 0x3FF, (tile >> 10) & 0x7, bool(tile & 0x2000), bool(tile & 0x4000), bool(tile & 0x8000))

    def __str__(self):
        return "BGtile[i=$%02x p=$%x %s%s%s%s]" % (self.idx, self.pal, "P" if self.prio else "", "H" if self.hFlip else "", "V" if self.vFlip else "", "X" if self.present else "")

# area map => {graph area=>palette}
palettesByArea = {
    "Ceres": {"Ceres": 3},
    "Tourian": {"Tourian": 7},
    # there are single tiles for RedBrinstar and GreenPinkBrinstar but not enough palettes...
    # "fixed" by having map icons on top of tiles when the portal is taken once, and using the "undefined" color
    "Crateria": {"Crateria": 7, "WreckedShip": 6, "Tourian": 5, "EastMaridia": 4, "GreenPinkBrinstar": 3, "RedBrinstar": 3},
    "Brinstar": {"GreenPinkBrinstar": 7, "RedBrinstar": 6, "Crateria": 5, "Kraid": 4, "Norfair": 3},
    "Norfair": {"Norfair": 7, "LowerNorfair": 6, "Crocomire": 5},
    "Maridia": {"RedBrinstar": 7, "WestMaridia": 6, "EastMaridia": 5},
    "WreckedShip": {"WreckedShip": 7}
}

# "hidden" unused in VARIA (or even replaced), but referencing them is useful for the helper tool
kindToIndex = {
    LocationMapTileKind.FourWallsOneDoor: {"double":0x3, "minor":0x4, "nothing":0x5, "hidden": 0x6, "major":0x7},
    LocationMapTileKind.ThreeWallsOpenBottom: {"double":0x8, "minor":0x9, "nothing":0xa, "major":0xb},
    LocationMapTileKind.ThreeWallsOpenRight: {"double":0x13, "minor":0x14, "nothing":0x15, "hidden": 0x16, "major":0x17},
    LocationMapTileKind.ThreeWallsOneDoorOpenRight: {"minor": 0x1c, "nothing":0x1d, "major": 0x1e},
#    LocationMapTileKind.TwoWallsCornerWithPixel: {"minor": 0x20, "nothing": 0x21},
    # relocated to add extra tile for major
    LocationMapTileKind.TwoWallsCornerWithPixel: {"minor": 0x56, "nothing": 0x57, "major": 0x58},
    LocationMapTileKind.TwoWallsCorner: {"double":0x23, "minor":0x24, "nothing":0x25, "hidden": 0x26, "major":0x27},
    LocationMapTileKind.TwoWallsCornerWithHorizontalDoor: {"minor":0x28, "nothing": 0x29, "major":0x2a},
    LocationMapTileKind.TwoWallsCornerWithVerticalDoor: {"minor": 0x2b, "nothing": 0x2c},
    LocationMapTileKind.FourWallsCorridor: {"minor":0x4c, "nothing":0x4d, "major":0x4e},
    LocationMapTileKind.TwoWallsCorridor: {"minor":0x51, "nothing":0x52, "major":0x53},
    LocationMapTileKind.SingleWallHorizontal: {"minor":0x61, "nothing":0x62, "major":0x63},
    LocationMapTileKind.FourWallsTwoDoors: {"minor": 0x66, "nothing": 0x67, "major": 0x68},
    LocationMapTileKind.SingleWallVertical: {"minor":0x71, "nothing":0x72, "major":0x73},
    LocationMapTileKind.ThreeWallsOneDoorOpenBottom: {"nothing":0x90, "minor":0x91, "major":0x92}
}

def getTileKind(tileIndex):
    for kind, indices in kindToIndex.items():
        for category, index in indices.items():
            if index == tileIndex:
                return (kind, category)
    return (LocationMapTileKind.Unknown, "nothing")

def getTileIndex(kind, tileClass):
    idxEntry = kindToIndex[kind]
    if tileClass in idxEntry:
        return idxEntry[tileClass]
    else:
        raise ValueError(f"No '{tileClass}' entry for tile kind {kind}")

nPages = 2
pageSize = 32

class AreaMap(object):
    def __init__(self, vertical=False):
        self.width = nPages * pageSize if not vertical else pageSize
        self.height = pageSize if not vertical else nPages * pageSize
        self.pages = [[None]*pageSize*pageSize for i in range(nPages)]
        self.vertical = vertical
        # (x,y) => [(loc, tileClass), ...]
        # in practice the list will be one or two entries
        self.items = defaultdict(list)

    def getPage(self, x, y):
        return x // pageSize if not self.vertical else y // pageSize

    def getIndexInPage(self, x, y):
        return pageSize*(y % pageSize) + (x % pageSize)

    def getCoords(self, index):
        page = index // (pageSize*pageSize)
        pageIdx = index % (pageSize*pageSize)
        if not self.vertical:
            return page * pageSize + (pageIdx % pageSize), pageIdx // pageSize
        else:
            return pageIdx % pageSize, page * pageSize + pageIdx // pageSize

    def getCoordsByte(self, byteIndex, bitMask):
        index = byteIndex*8 + 8 - bitMask.bit_length()
        return self.getCoords(index)

    def getByteIndexMask(self, x, y):
        page, idx = self.getPage(x, y), self.getIndexInPage(x, y)
        idx += page*pageSize*pageSize
        return idx // 8, 1 << (7 - (idx % 8))

    def getTile(self, x, y):
        page = self.pages[self.getPage(x, y)]
        return page[self.getIndexInPage(x, y)]

    def setTile(self, x, y, tile):
        page = self.pages[self.getPage(x, y)]
        page[self.getIndexInPage(x, y)] = tile

    @staticmethod
    def load(mapRom, presenceRom=None, mapOffset=0, presenceOffset=0, vertical=False):
        ret = AreaMap(vertical)
        mapRom.seek(mapOffset)
        for page in ret.pages:
            for i in range(pageSize*pageSize):
                page[i] = BGtile.fromWord(mapRom.readWord())
        if presenceRom is not None:
            presenceRom.seek(presenceOffset)
            for page in ret.pages:
                for i in range((pageSize*pageSize) // 8):
                    b = presenceRom.readByte()
                    for s in range(8):
                        tile = page[i*8 + s]
                        tile.present = bool(b & (1 << (7 - s)))
        return ret

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

    def getOffset(self, x, y, mapOffset=0):
        page, idx = self.getPage(x, y), self.getIndexInPage(x, y)
        addr = pageSize*pageSize*2*page + idx*2
        return mapOffset + addr

    def writeBGtile(self, rom, x, y, mapOffset=0):
        tile = self.getTile(x, y)
        addr = self.getOffset(x, y, mapOffset)
        rom.writeWord(tile.toWord(), addr)

    def readBGtile(self, rom, x, y, mapOffset=None):
        addr = self.getOffset(x, y, mapOffset)
        self.setTile(BGtile.fromWord(rom.readWord(addr)))

    def setItemLoc(self, itemLoc, split, revealNothing=False):
        item, loc = itemLoc.Item, itemLoc.Location
        attrs = loc.MapAttrs
        # determine tile class
        tileClass = "minor"
        if not split.startswith("Full") and loc.isClass(split):
            tileClass = "major"
        if revealNothing == True and item.Category == "Nothing":
            tileClass = "nothing"
        self.items[(attrs.X, attrs.Y)].append((loc, tileClass))

    def writeItemTiles(self, rom, mapOffset, itemMaskOffset):
        # write map tiles, taking care of double items:
        # - if one of the two is a nothing, only draw the relevant tile
        # - if both are minors, draw the double map tile, and set the same mask for the two locs
        # - write a single major tile in the case of major+minor or major+major on the same spot
        #   (we can only do double -> minor -> nothing tile cover transition):
        #      -> "elect" one of the two tiles, and ignore the other (act as 'nothing') to avoid double
        #          item pickup issue when not using the double tile
        selectClass = lambda itemEntry, tileClass: [item for item in itemEntry if item[1] == tileClass]
        def drawTile(itemEntry, tileClassOverride=None):
            loc, tileClass = itemEntry
            attrs = loc.MapAttrs
            if tileClassOverride is not None:
                tileClass = tileClassOverride
            pal = palettesByArea[loc.Area][loc.GraphArea]
            tile = BGtile(getTileIndex(attrs.TileKind, tileClass), pal, hFlip=attrs.hFlip, vFlip=attrs.vFlip)
            self.setTile(attrs.X, attrs.Y, tile)
            self.writeBGtile(rom, attrs.X, attrs.Y, mapOffset)
        # see map/ItembitTileChangeList.asm for explanations
        tileMasks = {-1: 0b00, -2: 0b01, 1: 0b10, 2: 0b11}
        areaMasks = {"Crateria": 0b000, "Brinstar": 0b001, "Norfair": 0b010, "WreckedShip": 0b011, "Maridia":0b100}
        def setItemMask(itemEntry, tileClassOverride=None):
            loc, tileClass = itemEntry
            attrs = loc.MapAttrs
            if tileClassOverride is not None:
                tileClass = tileClassOverride
            # write item tile change collection info
            if tileClass != "nothing":
                tile = self.getTile(attrs.X, attrs.Y)
                tileCollectionOffset = getTileIndex(attrs.TileKind, "nothing") - tile.idx if tileClass != "double" else 1
                page = self.getPage(attrs.X, attrs.Y)
                x, y = attrs.X % pageSize, attrs.Y % pageSize
                w = (x & 0x1f) | ((y & 0x1f) << 5) | (page << 10) | (areaMasks[loc.Area] << 11) | (tileMasks[tileCollectionOffset] << 14)
            else:
                w = 0
            rom.writeWord(w, itemMaskOffset + loc.Id * 2)
        for coords, itemEntry in self.items.items():
            if len(itemEntry) == 1:
                drawTile(itemEntry[0])
                setItemMask(itemEntry[0])
            elif len(itemEntry) == 2:
                nothings = selectClass(itemEntry, "nothing")
                minors = selectClass(itemEntry, "minor")
                majors = selectClass(itemEntry, "major")
                if len(majors) > 0:
                    major = majors[0]
                    other = itemEntry[(itemEntry.index(major)+1) % 2]
                    drawTile(major)
                    setItemMask(major)
                    setItemMask(other, "nothing")
                elif len(nothings) == 1:
                    nothing = nothings[0]
                    other = itemEntry[(itemEntry.index(nothing)+1) % 2]
                    drawTile(other)
                    setItemMask(other)
                    setItemMask(nothing)
                elif len(nothings) == 2:
                    drawTile(itemEntry[0])
                    setItemMask(itemEntry[0])
                    setItemMask(itemEntry[1])
                elif len(minors) == 2:
                    drawTile(itemEntry[0], "double")
                    setItemMask(itemEntry[0], "double")
                    setItemMask(itemEntry[1], "double")
                else:
                    raise RuntimeError("Invalid item entry list at "+str(coords))
            else:
                raise RuntimeError("Invalid item entry list at "+str(coords))

# actually map icons 1 tile-sized
class MapIcon(BGtile):
    def __init__(self, index, palette=0, prio=True, hFlip=False, vFlip=False, x=0, y=0):
        super().__init__(index, palette, prio=prio, hFlip=hFlip, vFlip=vFlip)
        self.X = int(x) & 0x1ff # 9 bits
        self.Y = int(y) & 0xff # 8 bits
        self.table_index = None

    #     s000000xxxxxxxxx yyyyyyyy YXppPPPttttttttt
    # Where:
    #     s = size bit
    #     x = X offset of sprite from centre
    #     y = Y offset of sprite from centre
    #     Y = Y flip
    #     X = X flip
    #     P = palette
    #     p = priority (relative to background)
    #     t = tile number
    def toWord(self):
        return (self.idx & 0x3FF)|((self.pal & 0x7) << 9)|(int(self.prio) << 13)|(int(self.hFlip) << 14)|(int(self.vFlip) << 15)

    def toSpriteAsm(self):
        return f"    dw ${self.X:0>4x} : db ${self.Y:0>2x} : dw ${self.toWord():0>4x}"

class DoorMapIcon(MapIcon):
    def __init__(self, index, hFlip=False, vFlip=False, x=0, y=0):
        super().__init__(index, palette=5, hFlip=hFlip, vFlip=vFlip, x=x, y=y)

class PortalMapIcon(MapIcon):
    def __init__(self, index):
        super().__init__(index, palette=4, y=-1)

class ObjectiveMapIcon(MapIcon):
    def __init__(self, objIdx):
        super().__init__(0xE6 + objIdx, palette=7, x=1, y=-1)
        self.table_index = objIdx

portal_mapicons = {
    "Crateria": PortalMapIcon(0xDB),
    "GreenPinkBrinstar": PortalMapIcon(0xDC),
    "RedBrinstar": PortalMapIcon(0xDD),
    "WreckedShip": PortalMapIcon(0xDE),
    "Kraid": PortalMapIcon(0xDF),
    "Norfair": PortalMapIcon(0xE0),
    "Crocomire": PortalMapIcon(0xE1),
    "LowerNorfair": PortalMapIcon(0xE2),
    "WestMaridia": PortalMapIcon(0xE3),
    "EastMaridia": PortalMapIcon(0xE4),
    "Tourian": PortalMapIcon(0xE5),
    "KraidBoss": PortalMapIcon(0xF8),
    "PhantoonBoss": PortalMapIcon(0xF9),
    "DraygonBoss": PortalMapIcon(0xFA),
    "RidleyBoss": PortalMapIcon(0xFB)
}

def assignMapIconSpriteTableIndices():
    i = 0
    for icon in portal_mapicons.values():
        icon.table_index = i
        i += 1

assignMapIconSpriteTableIndices()
