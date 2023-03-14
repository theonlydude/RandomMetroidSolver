#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))


bmp_dir = sys.argv[1]
map_path = sys.argv[2]
map_data_path = sys.argv[3]
map_offset = int(sys.argv[4], 16) if len(sys.argv) > 4 else 0
map_data_offset = int(sys.argv[5], 16) if len(sys.argv) > 5 else 0

from rom.map import AreaMap
from rom.rom import RealROM

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

# Main loop
while True:
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            # Get the mouse click position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Calculate the tile coordinates
            x = mouse_x // DISP_TILE_SIZE
            y = mouse_y // DISP_TILE_SIZE
            # Output the tile description
            mapTile = areaMap.getTile(x, y)
            print("Tile clicked at (%d, %d): %s" % (x, y, str(mapTile)))
    # Update the display
    pygame.display.flip()
