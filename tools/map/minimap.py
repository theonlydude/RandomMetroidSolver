import json, sys, os

from rom.map import AreaMap, palettesByArea, getGraphArea
from rom.rom import RealROM

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

    @property
    def graphAreas(self):
        return [getGraphArea(self.area, palette) for palette in self.palettes]

    def __eq__(self, other):
        return other.palettes == self.palettes

    def addGraphArea(self, graphArea):
        self._palettes.add(palettesByArea[self.area][graphArea])

class RoomType(object):
    _id = 0

    def __init__(self, paletteTriplet, graphAreas):
        self.id = None
        self.paletteTriplet = paletteTriplet
        self.graphAreas = graphAreas

    def enable(self):
        self.id = RoomType._id
        RoomType._id += 1

    def __eq__(self, other):
        return self.graphAreas == other.graphAreas and self.paletteTriplet == other.paletteTriplet

    def __repr__(self):
        return f"{self.id} | {self.graphAreas} | {self.paletteTriplet}"

class PalettesConfigGenerator(object):
    def __init__(self, dataDir="tools/map/graph_area", binMapDir="patches/vanilla/src/map", alt=False):
        self.dataDir = dataDir
        self.binMapDir = binMapDir
        self.alt = alt
        self.paletteConfigs = {}
        self.maps = {}
        self.roomPalettes = {}
        self.paletteTriplets = {}
        self.roomTypes = {}
        self.loadMaps()
        self.loadRoomTiles()
        self.findRoomPalettes()
        self.createPaletteTriplets()
        self.createRoomTypes()

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

    def createPaletteTriplets(self):
        for room, roomPalettes in self.roomPalettes.items():
            pals = set(roomPalettes.palettes)
            n = sys.maxsize
            selected, selectedColors = None, None
            for triplet in self.paletteTriplets.values():
                newColors = [c for c in pals if c not in triplet]
                if len(newColors) < n and len(newColors) + len(triplet) <= 3:
                    n = len(newColors)
                    selected = triplet
                    selectedColors = newColors
            if selected is not None:
                for c in selectedColors:
                    selected.add(c)
            else:
                selected = pals
            self.paletteTriplets[room] = selected

    def createRoomTypes(self):
        for room, roomPalette in self.roomPalettes.items():
            triplet = self.paletteTriplets[room]
            roomType = RoomType(triplet, roomPalette.graphAreas)
            existent = next((rt for rt in self.roomTypes.values() if rt == roomType), None)
            if existent is not None:
                roomType = existent
            else:
                roomType.enable()
            self.roomTypes[room] = roomType
