#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import snes_to_pc, RealROM
from rom.compression import Compressor

romFile = sys.argv[1]

rom = RealROM(romFile)

palettes = {
    "Tileset 0: Upper Crateria": 0xC2AD7C,
    "Tileset 1: Red Crateria": 0xC2AE5D,
    "Tileset 2: Lower Crateria": 0xC2AF43,
    "Tileset 3: Old Tourian": 0xC2B015,
    "Tileset 4: Wrecked Ship - power on": 0xC2B0E7,
    "Tileset 5: Wrecked Ship - power off": 0xC2B1A6,
    "Tileset 6: Green/blue Brinstar": 0xC2B264,
    "Tileset 7: Red Brinstar / Kraid's lair": 0xC2B35F,
    "Tileset 8: Pre Tourian entrance corridor": 0xC2B447,
    "Tileset 1Ah: Kraid's room": 0xC2B510,
    "Tileset 9: Heated Norfair": 0xC2B5E4,
    "Tileset Ah: Unheated Norfair": 0xC2B6BB,
    "Tileset 1Bh: Crocomire's room": 0xC2B798,
    "Tileset Bh: Sandless Maridia": 0xC2B83C,
    "Tileset Ch: Sandy Maridia": 0xC2B92E,
    "Tileset 1Ch: Draygon's room": 0xC2BA2C,
    "Tileset Dh: Tourian": 0xC2BAED,
    "Tileset Eh: Mother Brain's room": 0xC2BBC1,
    "Tileset 15h: Map room / Tourian entrance": 0xC2BC9C,
    "Tileset 16h: Wrecked Ship map room - power off": 0xC2BD7B,
    "Tileset 17h: Blue refill room": 0xC2BE58,
    "Tileset 18h: Yellow refill room": 0xC2BF3D,
    "Tileset 19h: Save room": 0xC2C021,
    "Tileset Fh/11h/13h: Blue Ceres": 0xC2C104,
    "Tileset 10h/12h/14h: White Ceres": 0xC2C1E3
}

def print_digit(digit):
    print(hex(digit)[2:].zfill(2), end='')

def RGB_15_to_24(SNESColor):
    R = ((SNESColor      ) % 32) * 8
    G = ((SNESColor//32  ) % 32) * 8
    B = ((SNESColor//1024) % 32) * 8

    return (R,G,B)

def RGB_24_to_15(color_tuple):
    R_adj = int(color_tuple[0])//8
    G_adj = int(color_tuple[1])//8
    B_adj = int(color_tuple[2])//8

    c = B_adj * 1024 + G_adj * 32 + R_adj
    return (c)

def print_color(color):
    R,G,B = color
    print('#', end='')
    print_digit(R)
    print_digit(G)
    print_digit(B)
    print(' ', end='')

def print_palette_bytes(data):
    print("palette {}".format(",".join(["${}".format(hex(b)[2:].zfill(2)) for b in data])))
    print("")

def print_palette_raw(data):
    i = 0
    for i, b in enumerate(data):
        if i % 32 == 0:
            print("")
        print_digit(b)
        i += 1
    print("")

def print_palette_color(data):
    # display it as RGB colors
    i = 0
    while i < len(data)-1:
        if i % 32 == 0:
            print("")
        word = data[i] + (data[i+1] << 8)
        color = RGB_15_to_24(word)
        print_color(color)
        i += 2
    print("")

orange_door = (1, 2, 3)
green_door = (17, 18, 19)
red_door = (33, 34, 35)

# new color blind colors for orange/green/red doors
new_colors = {
    1: (0xFF, 0x4A, 0x00),
    2: (0xCE, 0x3A, 0x00),
    3: (0x99, 0x2B, 0x00),
    17: (0x96, 0xFF, 0x96),
    18: (0x78, 0xCC, 0x78),
    19: (0x5A, 0x99, 0x5A),
    33: (0xFF, 0x00, 0xFF),
    34: (0xD3, 0x00, 0xD3),
    35: (0xA0, 0x00, 0xA0)
}

f = open('color_palettes.py', 'w')
f.write('color_palettes = {')

for palette, address in palettes.items():
    print("--------------------- {}@{} --------------------".format(palette, hex(address)))

    output = Compressor().decompress(rom, snes_to_pc(address))
    orig_length, data = output

    print("compressed palette length: {}".format(orig_length))
    print("uncompressed palette length: {}".format(len(data)))

#    print_palette_bytes(data)
#    print_palette_raw(data)
#    print_palette_color(data)

    # update doors colors
    for pos, rgbcolor in new_colors.items():
        rgb15 = RGB_24_to_15(rgbcolor)
        low = rgb15 & 0xff
        high = (rgb15 & 0xff00) >> 8
        data[pos*2] = low
        data[pos*2+1] = high

#    print_palette_color(data)

    # recompress and check if it fits in original place
    compressed = Compressor().compress(data)
    new_length = len(compressed)
    print("recompressed palette length: {}".format(new_length))

    assert new_length <= orig_length, "new compressed palette is bigger than original"

    # write new palette
    rom.seek(snes_to_pc(address))
    for i, b in enumerate(compressed):
        rom.writeByte(b)
        f.write("{}: {},\n".format(snes_to_pc(address)+i, b))

f.write("}")

rom.close()
f.close()
