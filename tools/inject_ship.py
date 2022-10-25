#!/usr/bin/python3
# inject a custom ship in a Super Metroid ROM from a png file.
# an example custom file GIMP is available in tools/ship/example_ship.xcf
# inject the ship in game and in the mode 7 outro.
# generate a layout matching the ship's shape and inject it in Landing Site layout data.
# you can force some slopes if the generated ones are not perfect.
#
# there's six boxes in the file, from left to right and top to bottom:
#  -available slopes to create the ship layout (don't modify them).
#  -force some slopes for the ship, slopes can be mirrored horizontaly of verticaly, putting the tile to red means no slopes.
#  -hatch: vanilla colors, you can set custom colors under them, if no custom colors the hatch is removed.
#  -ship glow color: to use a custom glow color (must be present in the ship colors). leave empty to disable glow color, allow the use of 16 colors.
#   you can add a second glow color under the first to glow between the two colors instead of from black to first color.
#  -mode7 ship: 16 colors (including the empty one), on the 8x6=48 8x8 tiles only 34 can be used.
#  -in game ship: 16 colors (including the empty one), on the 7x5=35 16x16 tiles only 24 can be used.
#
# hints:
#  -you should set the GIMP grid to 16x16 when you're working on the in-game ship and to 8x8 when you're working on the mode-7 ship.
#  -a slopes.png file is generated, you can import it in the GIMP in the upper right box as a base if you need to override some slopes.
#   you can use the red override to force an empty slope and the purple one to force a solid block.
#   in the example_ship.xcf it's imported in the 'am2r gen slopes' layer.
#   don't forget to hide this layer before exporting the GIMP file to png.
#   you can load the updated ROM in SMILE to see if there're errors in the generated slopes (displayed in red in SMILE).
#   look for the Super Metroid Mode Manual for more infos on slopes.

import sys, os, argparse, random, itertools
from shutil import copyfile
from collections import defaultdict

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

try:
    from PIL import Image, ImageChops, ImageOps
except:
    print("Missing prerequisite pillow")
    sys.exit(1)
try:
    import numpy as np
except:
    print("Missing prerequisite numpy")
    sys.exit(1)

from rom.rom import RealROM, snes_to_pc, pc_to_snes
from rom.compression import Compressor
from rom.leveldata import LevelData, Room, BoundingRect

def isEmpty(img, box):
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            r, g, b, a = img.getpixel((x, y))
            if r != 0 or g != 0 or b != 0:
                return False
    return True

def RGB_15_to_24(SNESColor):
    R = ((SNESColor      ) % 32) * 8
    G = ((SNESColor//32  ) % 32) * 8
    B = ((SNESColor//1024) % 32) * 8

    return (R,G,B)

def RGB_24_to_15(color_tuple):
    R_adj = int(color_tuple[0])//8
    G_adj = int(color_tuple[1])//8
    B_adj = int(color_tuple[2])//8

    return B_adj * 1024 + G_adj * 32 + R_adj

def genDummyColor(usedColors):
    while True:
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        if color in usedColors:
            continue
        else:
            return color

# from sprite something
def get_single_raw_tile(image):
    # Here transpose() is used because otherwise we get column-major
    #  format in getdata(), which is not helpful
    return convert_indexed_tile_to_bitplanes(
        image.transpose(Image.TRANSPOSE).getdata()
    )

# from sprite something
def convert_indexed_tile_to_bitplanes(indexed_tile):
    # this should literally just be the inverse of
    #  convert_tile_from_bitplanes(), and so it was written in this way
    indexed_tile = np.array(indexed_tile, dtype=np.uint8).reshape(8, 8)
    indexed_tile = np.fliplr(indexed_tile)
    indexed_tile = indexed_tile.swapaxes(0, 1)
    # in the opposite direction, this had axis=1 collapsed
    fixed_bits = indexed_tile.reshape(8, 1, 8)
    tile_bits = np.unpackbits(fixed_bits, axis=1)
    shaped_tile = np.packbits(tile_bits, axis=2)
    tile = shaped_tile.reshape(8, 8)
    low_bitplanes = np.ravel(tile[:, 6:8])[::-1]
    high_bitplanes = np.ravel(tile[:, 4:6])[::-1]
    return np.append(low_bitplanes, high_bitplanes)

# from sprite something
def convert_to_4bpp(image, offset, dimensions, extra_area):
    # have to process these differently so that 16x16 tiles canbe correctly
    #  reconstructed
    top_row = []
    bottom_row = []
    small_tiles = []
    for bounding_box in itertools.chain(
        [dimensions], extra_area if extra_area else []
    ):
        xmin, ymin, xmax, ymax = bounding_box
        xmin += offset[0]
        ymin += offset[1]
        xmax += offset[0]
        ymax += offset[1]
        x_chad_length = (xmax - xmin) % 16
        y_chad_length = (ymax - ymin) % 16
        for y in range(ymin, ymax - 15, 16):
            for x in range(xmin, xmax - 15, 16):
                # make a 16x16 tile from (x,y)
                # tuples in left-up-right-bottom format
                #  (it's ok if this crops an area not completely in the image)
                top_row.extend(get_single_raw_tile(
                    image.crop((x, y, x + 8, y + 8))))
                top_row.extend(get_single_raw_tile(
                    image.crop((x + 8, y, x + 16, y + 8))))
                bottom_row.extend(get_single_raw_tile(
                    image.crop((x, y + 8, x + 8, y + 16))))
                bottom_row.extend(get_single_raw_tile(
                    image.crop((x + 8, y + 8, x + 16, y + 16))))
            # check to see if xmax-xmin has a hanging chad
            if x_chad_length == 0:
                pass  # no chad
            elif x_chad_length == 8:
                # make two 8x8 tiles from (chad,y), (chad,y+8)
                small_tiles.extend(get_single_raw_tile(
                    image.crop((xmax - 8, y, xmax, y + 8))))
                small_tiles.extend(get_single_raw_tile(
                    image.crop((xmax - 8, y + 8, xmax, y + 16))))
            else:
                # FIXME: English
                raise AssertionError(
                    f"received call to get_raw_pose() for image" + " " +
                    f"'{image.name}' but the dimensions for x" + " " +
                    f"({xmin},{xmax}) are not divisible by 8")
        # check to see if ymax-ymin has hanging chads
        if y_chad_length == 0:
            pass  # cool
        elif y_chad_length == 8:
            for x in range(xmin, xmax - 15, 16):
                # construct the big chads first from (x,chad), (x+8,chad)
                small_tiles.extend(get_single_raw_tile(
                    image.crop((x, ymax - 8, x + 8, ymax))))
                small_tiles.extend(get_single_raw_tile(
                    image.crop((x + 8, ymax - 8, x + 16, ymax))))
            # now check for the bottom right chad
            y_chad_length = ymax - ymin % 16
            if x_chad_length == 0:
                pass  # cool
            elif x_chad_length == 8:
                # make the final chad
                small_tiles.extend(get_single_raw_tile(
                    image.crop((xmax - 8, ymax - 8, xmax, ymax))))
            else:
                # FIXME: English
                raise AssertionError(
                    f"received call to get_raw_pose() for image" + ' ' +
                    f"'{image.name}' but the dimensions for x" + ' ' +
                    f"({xmin},{xmax}) are not divisible by 8")
        else:
            raise AssertionError(
                f"received call to get_raw_pose() for image" + ' ' +
                f"'{image.name}' but the dimensions for y" + ' ' +
                f"({xmin},{xmax}) are not divisible by 8")

    # even out the small tiles into the rest of the space
    for offset in range(0, len(small_tiles), 0x40):
        top_row.extend(small_tiles[offset:offset + 0x20])
        bottom_row.extend(small_tiles[offset + 0x20:offset + 0x40])

    return top_row + bottom_row

# from sprite something
def palettize(this_image, palette):
    palette = palette + palette[:3] * (256 - (len(palette) // 3))
    palette_seed = Image.new("P", (1, 1))
    palette_seed.putpalette(palette)

    # this is a workaround to quantize without dithering
    paletted_image = this_image._new(
        this_image.im.convert("P", 0, palette_seed.im))

    # have to shift the palette over now to include the
    #  transparent pixels correctly
    # did it this way so that color pixels would not accidentally
    #  be matched to transparency
    original_image_L = [
        0 if alpha < 255 else 1
        for _, _, _, alpha in this_image.getdata()
    ]
    new_image_indices = [
        L * (index + 1)
        for (L, index) in zip(
            original_image_L, paletted_image.getdata()
        )
    ]
    paletted_image.putdata(new_image_indices)
    shifted_palette = [0, 0, 0] + palette[:-3]
    paletted_image.putpalette(shifted_palette)

    return paletted_image

def extractColors(color):
    R = ((color      ) % 32)
    G = ((color//32  ) % 32)
    B = ((color//1024) % 32)
    return (R,G,B)
def createColor(r, g, b):
    return b * 1024 + g * 32 + r

def applyMergePercent(percent, startColor, endColor):
    startColor = extractColors(startColor)
    endColor = extractColors(endColor)
    r = min(startColor[0] + (endColor[0] * percent)//100, endColor[0])
    g = min(startColor[1] + (endColor[1] * percent)//100, endColor[1])
    b = min(startColor[2] + (endColor[2] * percent)//100, endColor[2])
    return createColor(r, g, b)

def applyPercent(percent, basePalette):
    computedPalette = []
    for color in basePalette:
        color = extractColors(color)
        r, g, b = color
        r = min((r * (100 + percent)) // 100, 31)
        g = min((g * (100 + percent)) // 100, 31)
        b = min((b * (100 + percent)) // 100, 31)
        computedPalette.append(createColor(r, g, b))
    return computedPalette

def findMatchingSlope(overide, slopes):
    overideData = overide.getdata()
    for slope, data in slopes.items():
        slopeData = data["reg"].getdata()
        if list(overideData) == list(slopeData):
            return slope
    raise Exception("Can't find a matching slope")

def isOutline(x, y, height):
    if emptyMatrix[y][x]:
        return False
    # tiles on the Y borders are outlines
    if y == 0 or y == height-1:
        return True

    # a tile is an outline if it has one empty tile around it
    for subX in [x-1, x, x+1]:
        for subY in [y-1, y, y+1]:
            try:
                empty = emptyMatrix[subY][subX] or slopesOverideMatrix[subY][subX] == forceEmpty
            except:
                continue
            if empty:
                return True
    return False

def getBestSlope(x, y, slopes, shipAlphaImg):
    # extract ship tile
    shipTile = shipAlphaImg.crop((x*16, y*16, (x+1)*16, (y+1)*16))
    shipTilei = ImageOps.invert(shipTile).convert('1')
    shipTile = shipTile.convert('1')

    bestScore = -1
    bestSlope = -1
    for slope, imgs in slopes.items():
        # match both empty to maximize empty ship pixels outside of the slop
        empty = ImageChops.logical_and(shipTilei, imgs["inv"])
        colors = empty.getcolors()
        # get the 255 color
        emptyScore = 0
        for color in colors:
            if color[1] == 255:
                emptyScore = color[0]
                break

        # match both filled to maximize ship pixels under the slop
        filled = ImageChops.logical_and(shipTile, imgs["reg"])
        colors = filled.getcolors()
        # get the 255 color
        filledScore = 0
        for color in colors:
            if color[1] == 255:
                filledScore = color[0]
                break

        finalScore = emptyScore + filledScore
        if finalScore > bestScore:
            bestScore = finalScore
            bestSlope = slope

    return bestSlope

parser = argparse.ArgumentParser(description="ship injector")
parser.add_argument('--rom', '-r', help="the input rom", dest="vanilla")
parser.add_argument('--png', '-p', help="ship png template", dest="ship_template")
parser.add_argument('--no-layout', '-l', help="no layout update", dest="no_layout",
                    action='store_true', default=False)
parser.add_argument('--no-mode7', '-m', help="no mode7 update", dest="no_mode7",
                    action='store_true', default=False)
parser.add_argument('--no-ship', '-s', help="no ship update", dest="no_ship",
                    action='store_true', default=False)
args = parser.parse_args()

vanillaRom = RealROM(args.vanilla)
baseImg = Image.open(args.ship_template)

# extract ship
shipBox = (128, 144, 240, 224)
shipImg = baseImg.crop(shipBox)
shipAlphaImg = shipImg.getchannel('A')
shipGlowCustomImg = baseImg.crop((176, 120, 184, 128))
(r, g, b, a) = shipGlowCustomImg.getpixel((0, 0))
shipGlowCustomColor = [r, g, b]
enableShipGlowCustom = sum(shipGlowCustomColor) > 0
shipGlowCustomMinImg = baseImg.crop((176, 128, 184, 136))
(r, g, b, a) = shipGlowCustomMinImg.getpixel((0, 0))
shipGlowCustomMinColor = [r, g, b]
enableShipGlowMinCustom = sum(shipGlowCustomMinColor) > 0
#shipImg.show()
print("custom final glow color enabled: {}".format(enableShipGlowCustom))
print("custom start glow color enabled: {}".format(enableShipGlowMinCustom))

# extract hatch tiles, original palette, new palette
hatchOrigPaletteBox = (56, 96, 96, 104)
hatchOrigPaletteImg = baseImg.crop(hatchOrigPaletteBox)
hatchNewPaletteBox = (56, 104, 96, 112)
hatchNewPaletteImg = baseImg.crop(hatchNewPaletteBox)
hatchCloseBox = (64, 120, 80, 128)
hatchCloseImg = baseImg.crop(hatchCloseBox)
hatchOpenBox = (64, 128, 80, 136)
hatchOpenImg = baseImg.crop(hatchOpenBox)

# get hatch old & new colors
hatchColors = (hatchOrigPaletteBox[2] - hatchOrigPaletteBox[0]) // 8 # 8x8 square for each color
hatchOrigPalette = []
for x in range(hatchColors):
    hatchOrigPalette.append(hatchOrigPaletteImg.getpixel((x*8, 0)))
hatchNewPalette = []
for x in range(hatchColors):
    hatchNewPalette.append(hatchNewPaletteImg.getpixel((x*8, 0)))

#print("hatch colors:")
#print(hatchOrigPalette)
#print(hatchNewPalette)

# check if new hatch palette has no colors, which means that we disable the hatch sprite. (0,0,0,0) is empty color.
enableHatch = sum([r+g+b+a for r,g,b,a in hatchNewPalette]) > 0

# mode 7
mode7shipBox = (40, 160, 104, 208)
mode7shipImg = baseImg.crop(mode7shipBox)

# slopes
slopesOverideBox = (240, 16, 352, 96)
slopesOverideImg = baseImg.crop(slopesOverideBox)

if not args.no_ship:
    # check how many tiles in the ship image are not empty.
    # ship image in the template is 7 x 5 tiles.
    width = 7
    height = 5
    emptyMatrix = [ [ True for x in range(width) ] for y in range(height) ]

    for tileX in range(width):
        for tileY in range(height):
            emptyMatrix[tileY][tileX] = isEmpty(shipImg, (tileX*16, tileY*16, (tileX+1)*16, (tileY+1)*16))

    #print("matrix:")
    #for row in emptyMatrix:
    #    print(row)

    # max 26 tiles can be non empty, as vanilla has 52 oam for the ship
    maxTiles = 26
    nonEmptyCount = sum([row.count(False) for row in emptyMatrix])
    assert nonEmptyCount <= maxTiles, "Too many tiles in the ship: {}, max authorized is {}".format(nonEmptyCount, maxTiles)

    # convert hatch tiles with new colors
    if enableHatch:
        for origColor, newColor in zip(hatchOrigPalette, hatchNewPalette):
            data = np.array(hatchCloseImg)
            data[(data == origColor).all(axis = -1)] = newColor
            hatchCloseImg = Image.fromarray(data, mode='RGBA')

            data = np.array(hatchOpenImg)
            data[(data == origColor).all(axis = -1)] = newColor
            hatchOpenImg = Image.fromarray(data, mode='RGBA')

    # check how many different colors are in the ship, max 16 (including the glowing and transparent one)
    # TODO::use provided function
    shipColors = set()
    for r, g, b, a in shipImg.getdata():
        shipColors.add((r, g, b))

    if enableHatch:
        for r, g, b, a in hatchCloseImg.getdata():
            shipColors.add((r, g, b))
        for r, g, b, a in hatchOpenImg.getdata():
            shipColors.add((r, g, b))

    # remove transparent color
    try:
        shipColors.remove((0, 0, 0))
    except:
        pass

    print("ship colors: {}".format(shipColors))
    maxColors = 16
    if len(shipColors) >= maxColors:
        print("Too many colors in the image: {}, convert it to 16 colors using ImageMagick for example:".format(len(shipColors)))
        print("convert {} +dither -colors 16 - | convert - PNG32:{}".format(args.ship_template, args.ship_template))
        sys.exit(1)

    # put back transparency as first element
    shipColors = [(0, 0, 0)] + list(shipColors)

    paletteFinal = []
    paletteFinalRGB = []
    for color in shipColors:
        paletteFinalRGB += color
        paletteFinal.append(RGB_24_to_15(color))

    print("final palette, {} colors: {}".format(len(paletteFinal), [hex(c) for c in paletteFinal]))
    print("final palette RGB: {}".format(paletteFinalRGB))

    # if all 16 colors are used disable the glowing color
    if len(shipColors) == maxColors and not enableShipGlowCustom:
        glowListAddr = snes_to_pc(0x8DCA52)
        vanillaRom.seek(glowListAddr)
        vanillaRom.writeWord(0x0005) # set color
        vanillaRom.writeWord(paletteFinal[-1]) # glow color
        vanillaRom.writeWord(0xC595) # done
        vanillaRom.writeWord(0xC61E) # goto CA52
        vanillaRom.writeWord(0xCA52)

    if enableShipGlowCustom:
        # we need to have the glowing color as last color in the palette
        finalGlowColor = RGB_24_to_15(shipGlowCustomColor)
        # if not all 16 colors are filled, add dummy colors
        if len(shipColors) < 16:
            colorsToAdd = 16 - len(shipColors)
            #dummyColorRGB = genDummyColor(shipColors)
            dummyColorRGB = [paletteFinalRGB[3], paletteFinalRGB[4], paletteFinalRGB[5]]
            dummyColorFinal = RGB_24_to_15(dummyColorRGB)
            paletteFinalRGB += dummyColorRGB * colorsToAdd
            paletteFinal += [dummyColorFinal] * colorsToAdd
        index = paletteFinal.index(finalGlowColor)
        paletteFinal.remove(finalGlowColor)
        paletteFinal.append(finalGlowColor)
        paletteFinalRGB = paletteFinalRGB[:index*3] + paletteFinalRGB[index*3+3:] + shipGlowCustomColor

        print("final palette, {} colors: {}".format(len(paletteFinal), [hex(c) for c in paletteFinal]))
        print("final palette RGB: {}".format(paletteFinalRGB))

        if enableShipGlowMinCustom:
            glowListAddr = snes_to_pc(0x8DCA52) + 2
            paletteGap = 6
            finalGlowMinColor = RGB_24_to_15(shipGlowCustomMinColor)
            percents = [0,   15,  30,  45,  60,  75, 100, 100, 75, 60,  45,  30,  15,  0]
            for j in range(14):
                percentGlowColor = applyMergePercent(percents[j], finalGlowMinColor, finalGlowColor)
                vanillaRom.writeWord(percentGlowColor, glowListAddr+paletteGap*j)
        else:
            glowListAddr = snes_to_pc(0x8DCA52) + 8
            paletteGap = 6
            percents = [-85, -70, -55, -40, -25, -10, 0, -10, -25, -40, -55, -70, -85]
            for j in range(12):
                percentGlowColor = applyPercent(percents[j], [finalGlowColor])[0]
                vanillaRom.writeWord(percentGlowColor, glowListAddr+paletteGap*j)

    if enableHatch:
        # add hatch tiles to ship tiles to palettize all images with the same palette
        tmpImg = Image.new("RGBA", (112, 96))
        tmpImg.paste(shipImg, (0, 0))
        tmpImg.paste(hatchCloseImg, (0, 80, 16, 88))
        tmpImg.paste(hatchOpenImg, (0, 88, 16, 96))
        # tmpImg.show()

        tmpImg = palettize(tmpImg, paletteFinalRGB[3:])
        shipImg = tmpImg.crop((0, 0, 112, 80))
        hatchCloseImg = tmpImg.crop((0, 80, 16, 88))
        hatchOpenImg = tmpImg.crop((0, 88, 16, 96))
    else:
        # convert image to 4bpp, indexed in final palette.
        # treat each 16x16 tile separately.
        shipImg = palettize(shipImg, paletteFinalRGB[3:])

    #print("ship palette: {}".format(shipImg.getpalette()))
    #shipImg.show()

    # convert to 4bpp
    tiles = {}
    for y in range(height):
        for x in range(width):
            if not emptyMatrix[y][x]:
                # extract 16x16 tile
                tile = shipImg.crop((x*16, y*16, (x+1)*16, (y+1)*16))
                tiles[(y, x)] = convert_to_4bpp(tile, (0,0), (0,0,16,16), None)

    if enableHatch: 
        hatchCloseTile = convert_to_4bpp(hatchCloseImg, (0,0), (0,0,16,8), None)
        hatchOpenTile = convert_to_4bpp(hatchOpenImg, (0,0), (0,0,16,8), None)

    #for pos, data in tiles.items():
    #    print("{} {}".format(pos, len(data)))

    # write palette data
    paletteAddr = snes_to_pc(0xA2A59E)
    vanillaRom.seek(paletteAddr)
    for word in paletteFinal:
        vanillaRom.writeWord(word)

    # write tile data
    tileAddr = snes_to_pc(0xADB600)
    vanillaRom.seek(tileAddr)

    # there's 16 8x8 tiles per row, a 16x16 tile is on two rows.
    # cut tiles in batchs of 8
    tilesKeys = list(tiles.keys())
    tilesBatchs = defaultdict(list)
    for i, k in enumerate(tilesKeys):
        tilesBatchs[i//8].append(k)
    #print("tilesBatchs: {}".format(tilesBatchs))

    # a 16 8x8 4bpp tiles row size
    rowSize = 32 * 16

    length = len(tiles[tilesKeys[0]])
    for i, poses in tilesBatchs.items():
        for pos in poses:
            # first row
            for byte in tiles[pos][:length//2]:
                vanillaRom.writeByte(int(byte))
        if len(poses) < 8:
            # last row is incomplete
            lastRow8Addr = tileAddr + i * 2 * rowSize + rowSize
            vanillaRom.seek(lastRow8Addr)
        for pos in poses:
            # second row
            for byte in tiles[pos][length//2:]:
                vanillaRom.writeByte(int(byte))

    # if last two tiles are used we also have to copy them to escape tiles
    escapeTilesAddr = snes_to_pc(0x94C800)
    if len(tilesKeys) > 24:
        vanillaRom.seek(escapeTilesAddr)
        poses = tilesBatchs[3]
        for pos in poses:
            # top row
            for byte in tiles[pos][:length//2]:
                vanillaRom.writeByte(int(byte))
        # last row is incomplete
        lastRow8Addr = escapeTilesAddr + rowSize
        vanillaRom.seek(lastRow8Addr)
        for pos in poses:
            # second row
            for byte in tiles[pos][length//2:]:
                vanillaRom.writeByte(int(byte))

    # if hatch colors have changed, also copy its tiles to escape tiles
    tile8size = 32
    row8size = tile8size * 16
    hatchAddr = tileAddr + row8size * 6 + tile8size * 4
    hatchEscapeAddr = escapeTilesAddr + tile8size * 4
    if enableHatch:
        for addr in [hatchAddr, hatchEscapeAddr]:
            vanillaRom.seek(addr)
            for byte in hatchCloseTile:
                vanillaRom.writeByte(int(byte))
            for byte in hatchOpenTile:
                vanillaRom.writeByte(int(byte))
    else:
        # put transparent tiles
        for addr in [hatchAddr, hatchEscapeAddr]:
            vanillaRom.seek(addr)
            for i in range(128):
                vanillaRom.writeByte(0)

    # compute tile index
    tilesIndexes = {}
    for index, pos in enumerate(tilesKeys):
        # each tile is 16x16, so twice as large as a 8x8 for x, same for y.
        # 8 16x16 tiles on each row
        tilesIndexes[pos] = index * 2 + (index//8) * 16

    print("tilesIndexes: {}".format(tilesIndexes))

    defaultOAM = {
        (0, 0): [0xC391,0xEE,0x3F00], (0, 1): [0xC3A1,0xEE,0x3F00], (0, 2): [0xC3B1,0xEE,0x3F00], (0, 3): [0xC3C1,0xEE,0x3F00], (0, 4): [0xC3D1,0xEE,0x3F00], (0, 5): [0xC3E1,0xEE,0x3F00], (0, 6): [0xC3F1,0xEE,0x3F00],
        (1, 0): [0xC391,0xFE,0x3F00], (1, 1): [0xC3A1,0xFE,0x3F00], (1, 2): [0xC3B1,0xFE,0x3F00], (1, 3): [0xC3C1,0xFE,0x3F00], (1, 4): [0xC3D1,0xFE,0x3F00], (1, 5): [0xC3E1,0xFE,0x3F00], (1, 6): [0xC3F1,0xFE,0x3F00],
        (2, 0): [0xC391,0xE6,0x3F00], (2, 1): [0xC3A1,0xE6,0x3F00], (2, 2): [0xC3B1,0xE6,0x3F00], (2, 3): [0xC3C1,0xE6,0x3F00], (2, 4): [0xC3D1,0xE6,0x3F00], (2, 5): [0xC3E1,0xE6,0x3F00], (2, 6): [0xC3F1,0xE6,0x3F00],
        (3, 0): [0xC391,0xF6,0x3F00], (3, 1): [0xC3A1,0xF6,0x3F00], (3, 2): [0xC3B1,0xF6,0x3F00], (3, 3): [0xC3C1,0xF6,0x3F00], (3, 4): [0xC3D1,0xF6,0x3F00], (3, 5): [0xC3E1,0xF6,0x3F00], (3, 6): [0xC3F1,0xF6,0x3F00],
        (4, 0): [0xC391,0x06,0x3F00], (4, 1): [0xC3A1,0x06,0x3F00], (4, 2): [0xC3B1,0x06,0x3F00], (4, 3): [0xC3C1,0x06,0x3F00], (4, 4): [0xC3D1,0x06,0x3F00], (4, 5): [0xC3E1,0x06,0x3F00], (4, 6): [0xC3F1,0x06,0x3F00],
    }

    defaultOAMMirror = {
        (0, 6): [0xC201,0xEE,0x7F00], (0, 5): [0xC211,0xEE,0x7F00], (0, 4): [0xC221,0xEE,0x7F00], (0, 3): [0xC231,0xEE,0x7F00], (0, 2): [0xC241,0xEE,0x7F00], (0, 1): [0xC251,0xEE,0x7F00], (0, 0): [0xC261,0xEE,0x7F00],
        (1, 6): [0xC201,0xFE,0x7F00], (1, 5): [0xC211,0xFE,0x7F00], (1, 4): [0xC221,0xFE,0x7F00], (1, 3): [0xC231,0xFE,0x7F00], (1, 2): [0xC241,0xFE,0x7F00], (1, 1): [0xC251,0xFE,0x7F00], (1, 0): [0xC261,0xFE,0x7F00],
        (2, 6): [0xC201,0xE6,0x7F00], (2, 5): [0xC211,0xE6,0x7F00], (2, 4): [0xC221,0xE6,0x7F00], (2, 3): [0xC231,0xE6,0x7F00], (2, 2): [0xC241,0xE6,0x7F00], (2, 1): [0xC251,0xE6,0x7F00], (2, 0): [0xC261,0xE6,0x7F00],
        (3, 6): [0xC201,0xF6,0x7F00], (3, 5): [0xC211,0xF6,0x7F00], (3, 4): [0xC221,0xF6,0x7F00], (3, 3): [0xC231,0xF6,0x7F00], (3, 2): [0xC241,0xF6,0x7F00], (3, 1): [0xC251,0xF6,0x7F00], (3, 0): [0xC261,0xF6,0x7F00],
        (4, 6): [0xC201,0x06,0x7F00], (4, 5): [0xC211,0x06,0x7F00], (4, 4): [0xC221,0x06,0x7F00], (4, 3): [0xC231,0x06,0x7F00], (4, 2): [0xC241,0x06,0x7F00], (4, 1): [0xC251,0x06,0x7F00], (4, 0): [0xC261,0x06,0x7F00],
    }


    # write OAM
    # top is first two rows
    oamAddrTop = snes_to_pc(0xA2AD81)
    # we compute left part of the image, mult by 2 to add mirrored tiles
    topSpriteHeight = 2
    bottomSpriteHeight = 3
    tilesInTopCount = sum([row.count(False) for row in emptyMatrix[0:topSpriteHeight]]) * 2
    tilesInTop = []
    for y in range(topSpriteHeight):
        for x in range(width):
            if not emptyMatrix[y][x]:
                tilesInTop.append((y, x))
    tilesInBottom = []
    for y in range(topSpriteHeight, topSpriteHeight + bottomSpriteHeight):
        for x in range(width):
            if not emptyMatrix[y][x]:
                tilesInBottom.append((y, x))

    # bottom is last three rows
    tilesInBottomCount = sum([row.count(False) for row in emptyMatrix[topSpriteHeight:]]) * 2
    # 5 bytes per oam, sprite map size is 2
    oamSize = 5
    spritemapSize = 2
    oamAddrBottom = oamAddrTop + tilesInTopCount * oamSize + spritemapSize

    # convert from (y, x) in the image to OAM (x, y) and tile index
    oamTop = []
    for pos in tilesInTop:
        baseOam = defaultOAM[pos]
        baseOam[2] = (baseOam[2] & 0xFF00) + (tilesIndexes[pos] & 0xFF)
        oamTop.append(baseOam)
    for pos in tilesInTop:
        baseOam = defaultOAMMirror[pos]
        baseOam[2] = (baseOam[2] & 0xFF00) + (tilesIndexes[pos] & 0xFF)
        oamTop.append(baseOam)

    oamBottom = []
    for pos in tilesInBottom:
        baseOam = defaultOAM[pos]
        baseOam[2] = (baseOam[2] & 0xFF00) + (tilesIndexes[pos] & 0xFF)
        oamBottom.append(baseOam)
    for pos in tilesInBottom:
        baseOam = defaultOAMMirror[pos]
        baseOam[2] = (baseOam[2] & 0xFF00) + (tilesIndexes[pos] & 0xFF)
        oamBottom.append(baseOam)

    # write oam data
    vanillaRom.seek(oamAddrTop)
    vanillaRom.writeWord(tilesInTopCount)
    for oam in oamTop:
        vanillaRom.writeWord(oam[0])
        vanillaRom.writeByte(oam[1])
        vanillaRom.writeWord(oam[2])
    vanillaRom.writeWord(tilesInBottomCount)
    for oam in oamBottom:
        vanillaRom.writeWord(oam[0])
        vanillaRom.writeByte(oam[1])
        vanillaRom.writeWord(oam[2])

    # write ship bottom start oam list in ship bottom instruction list
    vanillaRom.seek(snes_to_pc(0xA2A61E))
    vanillaRom.writeWord(pc_to_snes(oamAddrBottom) & 0xFFFF)

# mode 7, convert whole ship sprite (with left & right part) to 112x48 pixels
# first check is image is not empty
width, height = mode7shipImg.size
enableMode7 = not isEmpty(mode7shipImg, (0, 0, width, height))
if enableMode7 and not args.no_mode7:
    wholeMode7ShipImg = Image.new("RGBA", (width*2, height))
    wholeMode7ShipImg.paste(mode7shipImg, (0, 0))
    wholeMode7ShipImg.paste(mode7shipImg.transpose(Image.FLIP_LEFT_RIGHT), (width, 0))

    # get non empty 8x8 tiles in the image
    width, height = (16, 6)
    emptyMatrixMode7 = [ [ True for x in range(width) ] for y in range(height) ]
    for tileX in range(width):
        for tileY in range(height):
            emptyMatrixMode7[tileY][tileX] = isEmpty(wholeMode7ShipImg, (tileX*8, tileY*8, (tileX+1)*8, (tileY+1)*8))

    maxTilesMode7 = 68
    nonEmptyCount = sum([row.count(False) for row in emptyMatrixMode7])
    assert nonEmptyCount <= maxTilesMode7, "Too many tiles in the mode7 ship: {}, max authorized is {}".format(nonEmptyCount, maxTilesMode7)

    mode7shipColors = set()
    for r, g, b, a in wholeMode7ShipImg.getdata():
        mode7shipColors.add((r, g, b))

    print("mode7 ship has {} different colors".format(len(mode7shipColors)))
    # remove transparent color
    try:
        mode7shipColors.remove((0, 0, 0))
    except:
        pass

    print("mode7 ship colors: {}".format(mode7shipColors))
    maxColors = 16
    if len(mode7shipColors) >= maxColors:
        print("Too many colors in the mode7 image, convert it to 16 colors using ImageMagick for example:")
        print("convert {} +dither -colors 16 - | convert - PNG32:{}".format(args.ship_template, args.ship_template))
        sys.exit(1)

    # put back transparency as first element
    mode7shipColors = [(0, 0, 0)] + list(mode7shipColors)

    mode7paletteFinal = []
    mode7paletteFinalRGB = []
    for color in mode7shipColors:
        mode7paletteFinalRGB += color
        mode7paletteFinal.append(RGB_24_to_15(color))

    print("final mode 7 palette, {} colors: {}".format(len(mode7paletteFinal), [hex(c) for c in mode7paletteFinal]))
    print("final mode 7 palette RGB, {} colors: {}".format(len(mode7paletteFinalRGB), mode7paletteFinalRGB))

    # convert image to 4bpp, indexed in final palette.
    # ship palette is in the 6th row, we'll have to add 0x50 to each pixel as mode 7 is not interleaved
    wholeMode7ShipImg = palettize(wholeMode7ShipImg, mode7paletteFinalRGB[3:])

    # extract 8x8 tiles
    width, height = (16, 6)
    tilesMode7 = {}
    for y in range(height):
        for x in range(width):
            if not emptyMatrixMode7[y][x]:
                # extract 8x8 tile
                tilesMode7[(y, x)] = wholeMode7ShipImg.crop((x*8, y*8, (x+1)*8, (y+1)*8))

    # to not have to relocate the back ship use only the 68 vanilla tiles locations of the front ship
    availableTiles = [
              0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,       0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
        0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
        0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f,
        0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,       0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f,
        0x40, 0x41, 0x42, 0x43,
        0x50, 0x51, 0x52
    ]

    # compute tile index
    tilesMode7Keys = list(tilesMode7.keys())
    tilesMode7Indexes = {}
    for pos, tileIndex in zip(tilesMode7Keys, availableTiles):
        tilesMode7Indexes[pos] = tileIndex

    # decompress tiles & tilemap
    tileAddr = snes_to_pc(0x95A82F)
    tilemapAddr = snes_to_pc(0x96FE69)
    compressedTilemapSize, tilemapData = Compressor().decompress(vanillaRom, tilemapAddr)        
    compressedTileSize, tileData = Compressor().decompress(vanillaRom, tileAddr)        

    # put transparent tile everywhere under the possible ship tiles
    transparentTile = 0x8c
    tilemapRowLength = 128
    for y in range(6):
        for x in range(16):
            pos = y*tilemapRowLength + x
            tilemapData[pos] = transparentTile
        
    # write tile data & tilemap
    # each pixel is a byte, tile is 8x8
    tileSize = 8 * 8
    # palette has 256 colors, our is on the 6th line
    paletteOffset = 0x50
    for pos, index in tilesMode7Indexes.items():
        posInData = index * tileSize
        for i, byte in enumerate(tilesMode7[pos].getdata()):
            tileData[posInData + i] = int(byte) + (paletteOffset if int(byte) > 0 else 0)
        posInTilemap = pos[0]*tilemapRowLength+pos[1]
        tilemapData[posInTilemap] = index

    # write palette
    # skip three first word instructions
    paletteAddr = snes_to_pc(0x8DD6BA) + 6
    # there 0x24 bytes between two palettes start (16 colors and 2 instructions)
    paletteGap = 0x24
    vanillaRom.seek(paletteAddr)

    # 16 palettes during the animation
    # 1st is all white
    whitePalette = [0x0000] + [0x7fff]*15
    for i, word in enumerate(whitePalette):
        vanillaRom.writeWord(word, paletteAddr+i*2)

    # 14 transitions
    percents = [90, 70, 50, 30, 10, -10, -30, -30, -25, -20, -15, -10, -5, -1]
    for j in range(14):
        palette = applyPercent(percents[j], mode7paletteFinal)
        for i, word in enumerate(palette):
            vanillaRom.writeWord(word, paletteAddr+paletteGap*(j+1)+i*2)
        for i in range(16-len(palette)):
            vanillaRom.writeWord(0x7fff)

    # last is regular palette
    j += 1
    for i, word in enumerate(mode7paletteFinal):
        vanillaRom.writeWord(word, paletteAddr+paletteGap*(j+1)+i*2)
    for i in range(16-len(mode7paletteFinal)):
        vanillaRom.writeWord(0x7fff)

    # compress
    print("compressing tilemap")
    compressedData = Compressor().compress(tilemapData)
    recompressedDataSize = len(compressedData)
    vanillaSize = 171
    if recompressedDataSize > vanillaSize:
        freespaceSize = 4574
        assert recompressedDataSize < freespaceSize
        # relocate in freespace
        freespaceAddr = snes_to_pc(0x99EE21)
        tilemapAddr = freespaceAddr
        print("rellocating tilemap data in freespace")
        # change pointers
        vanillaRom.writeWord(0x9900, snes_to_pc(0x8BBCCE))
        vanillaRom.writeWord(0xEE21, snes_to_pc(0x8BBCD3))
        vanillaRom.writeWord(0x9900, snes_to_pc(0x8BC166))
        vanillaRom.writeWord(0xEE21, snes_to_pc(0x8BC16B))
        vanillaRom.writeWord(0x9900, snes_to_pc(0x8BD58E))
        vanillaRom.writeWord(0xEE21, snes_to_pc(0x8BD593))

    # write compress data
    vanillaRom.seek(tilemapAddr)
    for byte in compressedData:
        vanillaRom.writeByte(byte)

    print("compressing tiles, {}".format(len(tileData)))
    compressedData = Compressor().compress(tileData)
    vanillaSize = 10330
    recompressedDataSize = len(compressedData)
    print("recompressedDataSize: {} vanillaSize: {}".format(recompressedDataSize, vanillaSize))
    assert recompressedDataSize <= vanillaSize
    # write compress data
    vanillaRom.seek(tileAddr)
    for byte in compressedData:
        vanillaRom.writeByte(byte)

if not args.no_layout:
    # generate layout behind the ship
    slopesImg = Image.open('tools/ship/slopes.png')
    # keep only alpha channel
    slopesImg = slopesImg.getchannel('A')
    #slopesImg.show()

    tmpslopes = {
        # fully filled blocks on the outside of the ship
        19: {"flipX": False, "flipY": True},
        # regular slopes
        0: {"flipX": False, "flipY": True},
        1: {"flipX": True,  "flipY": False},
        2: {"flipX": True,  "flipY": True},
        3: {"flipX": True,  "flipY": True},
        5: {"flipX": True,  "flipY": True},
        6: {"flipX": True,  "flipY": True},
        7: {"flipX": True,  "flipY": True},
        18: {"flipX": True,  "flipY": True},
        20: {"flipX": True,  "flipY": True},
        21: {"flipX": True,  "flipY": True},
        22: {"flipX": True,  "flipY": True},
        23: {"flipX": True,  "flipY": True},
        24: {"flipX": True,  "flipY": True},
        25: {"flipX": True,  "flipY": True},
        26: {"flipX": True,  "flipY": True},
        27: {"flipX": True,  "flipY": True},
        28: {"flipX": True,  "flipY": True},
        29: {"flipX": True,  "flipY": True},
        30: {"flipX": True,  "flipY": True},
        31: {"flipX": True,  "flipY": True}
    }

    slopes = defaultdict(dict)
    for slope, data in tmpslopes.items():
        # extract slope image
        x = (slope % 8) * 16
        y = (slope//8) * 16
        slopeImg = slopesImg.crop((x, y, x+16, y+16))
        slopeImgi = ImageOps.invert(slopeImg)

        slopes[slope]["reg"] = slopeImg.convert('1')
        slopes[slope]["inv"] = slopeImgi.convert('1')

        # generated flipped images
        if data["flipX"]:
            slopes[0x100+slope]["reg"] = slopeImg.transpose(Image.FLIP_LEFT_RIGHT).convert('1')
            slopes[0x100+slope]["inv"] = slopeImgi.transpose(Image.FLIP_LEFT_RIGHT).convert('1')
        if data["flipY"]:
            slopes[0x200+slope]["reg"] = slopeImg.transpose(Image.FLIP_TOP_BOTTOM).convert('1')
            slopes[0x200+slope]["inv"] = slopeImgi.transpose(Image.FLIP_TOP_BOTTOM).convert('1')
        if data["flipX"] and data["flipY"]:
            slopes[0x300+slope]["reg"] = slopeImg.transpose(Image.ROTATE_180).convert('1')
            slopes[0x300+slope]["inv"] = slopeImgi.transpose(Image.ROTATE_180).convert('1')

    # extract slopes overide
    width = 7
    height = 5
    forceEmpty = -1
    forceSolid = -2
    slopesOverideMatrix = [ [ None for x in range(width) ] for y in range(height) ]
    for tileY in range(height):
        for tileX in range(width):
            if not emptyMatrix[tileY][tileX]:
                # first check for empty slope force (color 0xcc3535) and solid (color 0x700030)
                r, g, b, a = slopesOverideImg.getpixel((tileX*16, tileY*16))
                if r == 0xcc and g == 0x35 and b == 0x35:
                    slopesOverideMatrix[tileY][tileX] = forceEmpty
                elif r == 0x70 and g == 0x00 and b == 0x30:
                    slopesOverideMatrix[tileY][tileX] = forceSolid

    # convert slopes overide to 1bit per pixel image
    for tileY in range(height):
        for tileX in range(width):
            if slopesOverideMatrix[tileY][tileX] is None:
                slope = slopesOverideImg.crop((tileX*16, tileY*16, (tileX+1)*16, (tileY+1)*16))
                if not isEmpty(slope, (0, 0, 16, 16)):
                    slope = slope.getchannel('A').convert('1')
                    slopesOverideMatrix[tileY][tileX] = findMatchingSlope(slope, slopes)

    #print("slopes overide matrix:")
    #for row in slopesOverideMatrix:
    #    print(row)

    # generate ship outline from empty matrix
    width = 7
    height = 5
    outlineMatrix = [ [ False for x in range(width) ] for y in range(height) ]

    for tileX in range(width):
        for tileY in range(height):
            outlineMatrix[tileY][tileX] = isOutline(tileX, tileY, height)

    #print("empty matrix")
    #for row in emptyMatrix:
    #    print(row)
    #print("")
    #
    #print("outline matrix")
    #for row in outlineMatrix:
    #    print(row)
    #print("")

    # generate inside matrix from empty & outline matrixes
    insideMatrix = [ [ False for x in range(width) ] for y in range(height) ]
    for tileX in range(width):
        for tileY in range(height):
            insideMatrix[tileY][tileX] = (not emptyMatrix[tileY][tileX]) and (not outlineMatrix[tileY][tileX])

    #print("inside matrix")
    #for row in insideMatrix:
    #    print(row)


    print("compute slopes")
    slopesMatrix = [ [ {} for x in range(width) ] for y in range(height) ]
    for tileX in range(width):
        for tileY in range(height):
            if slopesOverideMatrix[tileY][tileX] is not None:
                overide = slopesOverideMatrix[tileY][tileX]
                if overide == forceEmpty:
                    slopesMatrix[tileY][tileX] = {"isSolid": False, "bts": None}
                elif overide == forceSolid:
                    slopesMatrix[tileY][tileX] = {"isSolid": True, "bts": None}
                else:
                    slopesMatrix[tileY][tileX] = {"isSolid": False, "bts": overide}
            elif emptyMatrix[tileY][tileX]:
                slopesMatrix[tileY][tileX] = {"isSolid": False, "bts": None}
            elif insideMatrix[tileY][tileX]:
                slopesMatrix[tileY][tileX] = {"isSolid": True, "bts": None}
            else:
                slopesMatrix[tileY][tileX] = {"isSolid": False, "bts": getBestSlope(tileX, tileY, slopes, shipAlphaImg)}

    # mirror slopes matrix
    fullSlopesMatrix = [ [ {} for x in range(width*2) ] for y in range(height) ]
    for tileX in range(width):
        for tileY in range(height):
            fullSlopesMatrix[tileY][tileX] = slopesMatrix[tileY][tileX]
    for tileX in range(width, 2*width):
        for tileY in range(height):
            fullSlopesMatrix[tileY][tileX] = slopesMatrix[tileY][2*width - tileX -1]
            bts = fullSlopesMatrix[tileY][tileX]["bts"]
            if bts is not None:
                # inverse X flip
                bts ^= 0x100
                fullSlopesMatrix[tileY][tileX] = {"isSolid": False, "bts": bts}

#    print("full slopes matrix")
#    for row in fullSlopesMatrix:
#        print(row)
#
    # generate img with slopes
    result = Image.new('1', (7*16, 5*16))
    for tileX in range(width):
        for tileY in range(height):
            slope = slopesMatrix[tileY][tileX]
            if not slope["isSolid"] and slope["bts"] is None:
                continue
            elif slope["isSolid"]:
                # copy filled slope
                result.paste(ImageOps.invert(slopes[19]["inv"].convert("L")), (tileX*16, tileY*16))
            else:
                result.paste(ImageOps.invert(slopes[slope["bts"]]["inv"].convert("L")), (tileX*16, tileY*16))
    result.save('slopes.png')

    # now insert the slopes/tiles into landing site layout
    print("insert ship slopes into landing site layout")


    landingSiteAddr = snes_to_pc(0x8F91F8)
    vLandingSite = Room(vanillaRom, landingSiteAddr)
    vLevelDataAddr = vLandingSite.defaultRoomState.levelDataPtr
    vRoomScreenSize = (vLandingSite.width, vLandingSite.height)
    vlevelData = LevelData(vanillaRom, snes_to_pc(vLevelDataAddr), vRoomScreenSize)

    boundingRect = BoundingRect()
    boundingRect.x1 = 17
    boundingRect.y1 = 78
    boundingRect.x2 = 241
    boundingRect.y2 = 158
    vShipScreen = (4,4)

    #vlevelData.displaySubScreen(vShipScreen, boundingRect)

    # empty layout data
    vlevelData.emptyLayout(vShipScreen, boundingRect)

    # generate layout data
    layer1 = []
    bts = []
    width = boundingRect.width()
    height = boundingRect.height()
    for y in range(height):
        for x in range(width):
            slopeData = fullSlopesMatrix[y][x]
            if slopeData["isSolid"]:
                btsType = 8
                layoutWord = (btsType << 12) + 0xFF
                layer1.append(layoutWord)
                bts.append(0)
            elif slopeData["bts"] is None:
                layer1.append(0xFF)
                bts.append(0)
            else:
                # layout: bbbbhvtttttttttt b: bts type h: hflip, v: vflip t: tile
                # bts:    vhbbbbbb v: vflip h: hflip b: value
                rawBts = slopeData["bts"]
                if rawBts & 0xFF == 19 and not (y == 0 or emptyMatrix[y-1][x if x < width//2 else width//2-((x-width//2)+1)]) and slopesOverideMatrix[y][x if x < width//2 else width//2-((x-width//2)+1)] is None:
                    # put a solid block instead, but not if the block is a top one
                    btsType = 8
                    layoutWord = (btsType << 12) + 0xFF
                    layer1.append(layoutWord)
                    bts.append(0)
                else:
                    flip = (rawBts & 0xFF00) >> 8
                    btsHFlip = flip & 0x1
                    btsVFlip = (flip & 0x2) >> 1
                    btsType = 1
                    btsValue = rawBts & 0xFF
                    layoutWord = (btsType << 12) + 0xFF
                    btsByte = (btsVFlip << 7) + (btsHFlip << 6) + (btsValue & 0x3F)
                    layer1.append(layoutWord)
                    bts.append(btsByte)

    layoutData = [layer1, bts]

    # paste layout data in landing site
    vlevelData.pasteLayout(layoutData, vShipScreen, boundingRect)
    #vlevelData.displaySubScreen(vShipScreen, boundingRect)

    print("compress landing site layout")
    vlevelData.write()

vanillaRom.close()
