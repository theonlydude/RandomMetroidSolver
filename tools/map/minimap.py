import json, os

from rom.map import AreaMap, palettesByArea
from rom.rom import RealROM
from rooms import rooms as rooms_area
from rooms import rooms_alt

areas = {
    "Brinstar": "brinstar",
    "Norfair": "norfair",
    "Maridia": "maridia",
    "Crateria": "crateria",
    "WreckedShip": "wrecked_ship",
    "Tourian": "tourian",
    "Ceres": "ceres"
}

MINIMAP_WIDTH = 5
MINIMAP_HEIGHT = 3

class RoomTile(object):
    def __init__(self, room, graphArea):
        self.room = room
        self.graphArea = graphArea

class RoomPalettes(object):
    def __init__(self, name, area):
        self.name = name
        self.area = area
        self._palettes = set()

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name}: {self.palettes}"

    @property
    def palettes(self):
        return sorted(list(self._palettes))

    def __eq__(self, other):
        return other.palettes == self.palettes

    def addGraphArea(self, graphArea):
        self._palettes.add(palettesByArea[self.area][graphArea])

class PalettesConfigGenerator(object):
    def __init__(self, dataDir="tools/map/graph_area", binMapDir="patches/vanilla/src/map", alt=False):
        self.rooms = rooms_area if not alt else rooms_alt
        self.dataDir = dataDir
        self.binMapDir = binMapDir
        self.alt = alt
        self.paletteConfigs = {}
        self.maps = {}
        self.roomPalettes = {}
        self.loadMaps()
        self.loadRoomTiles()
        self.findRoomPalettes()

    def loadMaps(self):
        for area, baseName in areas.items():
            mapRom = RealROM(os.path.join(self.binMapDir, f"{baseName}.bin"))
            presenceRom = RealROM(os.path.join(self.binMapDir, f"{baseName}_data_reveal.bin"))
            self.maps[area] = AreaMap.load(mapRom, presenceRom)
            mapRom.close()
            presenceRom.close()

    def loadRoomTiles(self):
        for area, baseName in areas.items():
            areaMap = self.maps[area]
            with open(os.path.join(self.dataDir, f"normal_{baseName}.json"), "r") as fp:
                mapData = json.load(fp)
            if self.alt == True:
                altPath = os.path.join(self.dataDir, f"alt_{baseName}.json")
                if os.path.exists(altPath):
                    with open(altPath, "r") as fp:
                        altMapData = json.load(fp)
                    for graphArea, rooms in altMapData.items():
                        if graphArea in mapData:
                            mapData[graphArea].update(altMapData[graphArea])
                        else:
                            mapData[graphArea] = altMapData[graphArea]
            for graphArea, rooms in mapData.items():
                for room, coords in rooms.items():
                    for c in coords:
                        x, y = c[0], c[1]
                        areaMap.setTile(x, y, RoomTile(room, graphArea))

    def findRoomPalettes(self):
        # very dumb algorithm but we can afford it
        for area, areaMap in self.maps.items():
            for x in range(areaMap.width):
                for y in range(areaMap.height):
                    baseTile = areaMap.getTile(x, y)
                    if not isinstance(baseTile, RoomTile):
                        continue
                    if baseTile.room in self.roomPalettes:
                        roomPal = self.roomPalettes[baseTile.room]
                    else:
                        roomPal = RoomPalettes(baseTile.room, area)
                        self.roomPalettes[baseTile.room] = roomPal
                    xmin = int(max(0, x - (MINIMAP_WIDTH - 1)/2))
                    xmax = int(min(areaMap.width, x + (MINIMAP_WIDTH - 1)/2 + 1))
                    ymin = int(max(0, y - (MINIMAP_HEIGHT - 1)/2))
                    ymax = int(min(areaMap.height, y + (MINIMAP_HEIGHT - 1)/2 + 1))
                    for tx in range(xmin, xmax):
                        for ty in range(ymin, ymax):
                            t = areaMap.getTile(tx, ty)
                            if not isinstance(t, RoomTile):
                                continue
                            roomPal.addGraphArea(t.graphArea)
