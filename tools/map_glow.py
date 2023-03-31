#!/usr/bin/python3

import sys, os, colorsys

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from utils.colors import RGB_15_to_24, RGB_24_to_15

areaColors = {
    "Crateria":0x35e9,
    "GreenPinkBrinstar":0x06e1,
    "RedBrinstar":0x0515,
    "WreckedShip":0x3ad6,
    "Kraid":0x1dc0,
    "Norfair":0x023f,
    "Crocomire":0x2497,
    "LowerNorfair":0x00df,
    "WestMaridia":0x7e20,
    "EastMaridia": 0x6e3c,
    "Tourian":0x5297
}

rgb2hsv = colorsys.rgb_to_hsv
hsv2rgb = colorsys.hsv_to_rgb

s_offsets = [ 0, 8, 16, 24, 32, 24, 16, 8 ]
v_offsets = [-off for off in s_offsets ]

bound = lambda b: max(0, min(255, b))
def applyOffset(i, h, s, v):
    return h, bound(s+s_offsets[i]), bound(v+v_offsets[i])
color2bytes = lambda c: tuple(int(i*256) for i in c)
bytes2color = lambda c: tuple(float(i)/256 for i in c)

def shiftColor(c, i):
    return RGB_24_to_15(color2bytes(hsv2rgb(*bytes2color(applyOffset(i, *color2bytes(rgb2hsv(*RGB_15_to_24(c))))))))

for area, snesColor in areaColors.items():
    shiftedColors = [shiftColor(snesColor, i) for i in range(len(s_offsets))]
    print("!Glow_%s = %s" % (area, ','.join(["$%04x" % c for c in shiftedColors])))
