#!/usr/bin/python3

import sys, os, json

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))


bmp_dir = sys.argv[1]
map_path = sys.argv[2]
map_data_path = sys.argv[3]
mode = sys.argv[4] if len(sys.argv) > 4 else "attrs"
map_offset = int(sys.argv[5], 16) if len(sys.argv) > 5 else 0
map_data_offset = int(sys.argv[6], 16) if len(sys.argv) > 6 else 0

from rom.map import AreaMap, getTileKind
from rom.rom import RealROM
from graph.location import LocationMapTileKind
from rooms import rooms, rooms_alt
from collections import defaultdict

mapRom = RealROM(map_path)
mapDataRom = RealROM(map_data_path)

areaMap = AreaMap.load(mapRom, mapDataRom)

mapRom.close()
mapDataRom.close()

TILE_SIZE = 8
TILE_ROW = 16
ZOOM = 2
DISP_TILE_SIZE = TILE_SIZE * ZOOM
SCREEN_WIDTH = areaMap.width * DISP_TILE_SIZE
SCREEN_HEIGHT = areaMap.height * DISP_TILE_SIZE

# Initialize Pygame
import pygame

pygame.init()

# map images by palette index
zoom = lambda image: pygame.transform.scale_by(image, ZOOM)

map_images = [pygame.image.load("%s/pause_gfx_%d.bmp" % (bmp_dir, i))  for i in range(8)]

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Draw the map tiles on the screen
for x in range(areaMap.width):
    for y in range(areaMap.height):
        mapTile = areaMap.getTile(x, y)
        sheet = map_images[mapTile.pal]
        rect = pygame.Rect((mapTile.idx % TILE_ROW) * TILE_SIZE, (mapTile.idx // TILE_ROW) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tile = zoom(sheet.subsurface(rect))
        if mapTile.hFlip or mapTile.vFlip:
            tile = pygame.transform.flip(tile, mapTile.hFlip, mapTile.vFlip)
        dest = pygame.Rect(x * DISP_TILE_SIZE, y * DISP_TILE_SIZE, DISP_TILE_SIZE, DISP_TILE_SIZE)
        screen.blit(tile, dest)

if mode == "graph_area":
    # output the (x,y) of the map tiles in a JSON organized by graph area
    def getRoomsByGraphArea(roomList):
        ret = defaultdict(list)
        for r in roomList:
            ret[r['GraphArea']].append(r)
        return ret
    roomsByGraphArea = getRoomsByGraphArea(rooms)
    roomsAltByGraphArea = getRoomsByGraphArea(rooms_alt)
    roomDicts = [(roomsByGraphArea, "normal"), (roomsAltByGraphArea, "alt")]
    curRoomDict = None
    curRoomList = None
    curMap = None
    roomDictsIter = iter(roomDicts)
    mapName, _ = os.path.splitext(os.path.basename(map_path))
# Main loop
while True:
    # process special modes
    if mode == "graph_area":
        if curRoomDict is None:
            try:
                curRoomDict, curRoomDictName = next(roomDictsIter)
                roomListsByAreaIter = iter(curRoomDict.items())
                curMap = {}
            except StopIteration:
                curRoomDict = None
        if curRoomDict is not None:
            if curRoomList is None:
                try:
                    confirmed = False
                    while not confirmed:
                        curArea, curRoomList = next(roomListsByAreaIter)
                        ans = input(curArea + " (Y/[N])? ")
                        confirmed = ans.lower() == "y"
                    curMap[curArea] = defaultdict(list)
                    curRoom = None
                    roomListIter = iter(curRoomList)
                except StopIteration:
                    if curMap is not None:
                        fName = "%s_%s.json" % (curRoomDictName, mapName)
                        print("Writing "+fName)
                        with open(fName, "w") as fp:
                            json.dump(curMap, fp, indent=4)
                    curRoomList = None
                    curRoomDict = None
                    curMap = None
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                # Get the mouse click position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Calculate the tile coordinates
                x = mouse_x // DISP_TILE_SIZE
                y = mouse_y // DISP_TILE_SIZE
                # Output the tile description
                mapTile = areaMap.getTile(x, y)            
                print("Tile clicked at (%d, %d): %s" % (x, y, str(mapTile)))
                if mode == "attrs":
                    kind, category = getTileKind(mapTile.idx)
                    if kind != LocationMapTileKind.Unknown:
                        print("loc.MapAttrs = LocationMapAttrs(%d, %d, LocationMapTileKind.%s, hFlip=%s, vFlip=%s)" % (x, y, kind.name, str(mapTile.hFlip), str(mapTile.vFlip)))
                elif mode == "graph_area":
                    if curMap is not None and curRoom is not None:
                        r = curMap[curArea][curRoom["Name"]]
                        if (x, y) not in r:
                            r.append((x, y))
            elif event.button == pygame.BUTTON_RIGHT and mode == "graph_area":
                if curRoomList is not None:
                    if curRoom is None:
                        try:
                            curRoom = next(roomListIter)
                        except StopIteration:
                            curRoomList = None
                    if curRoom is not None:
                        ans = input(curRoom["Name"] + " finished (Y/[N]/R/A)?")
                        if ans.lower() == "y":
                            curRoom = None
                        elif ans.lower() == "r":
                            if curRoom["Name"] in curMap[curArea]:
                                del curMap[curArea][curRoom["Name"]]
                        elif ans.lower() == "a":
                            curRoomList = None
                                
    # Update the display
    pygame.display.flip()
