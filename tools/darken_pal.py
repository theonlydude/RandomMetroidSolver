#!/usr/bin/python3

import sys, os, colorsys

dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

# create a "darkened" version of a yy-chr RGB palette
pal_in_path = sys.argv[1]
pal_out_path = sys.argv[2]

luminance_coeff = 0.25

pal_in = open(pal_in_path, "rb")
pal_out = open(pal_out_path, "wb")

while True:
    colorRaw = pal_in.read(3)
    if len(colorRaw) < 3:
        break
    r, g, b = int(colorRaw[0]), int(colorRaw[1]), int(colorRaw[2])
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l *= luminance_coeff
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    pal_out.write(bytearray([int(r), int(g), int(b)]))

pal_in.close()
pal_out.close()
