#!/usr/bin/python3

import sys, os, colorsys

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from utils.colors import RGB_15_to_24, RGB_24_to_15, areaColors

rgb2hsv = colorsys.rgb_to_hsv
hsv2rgb = colorsys.hsv_to_rgb

s_offsets = [ 0, 8, 16, 24, 32, 24, 16, 8 ]
v_offsets = [-off for off in s_offsets ]

bound = lambda b: max(0, min(255, b))
def applyOffset(i, h, s, v):
    return h, bound(s+s_offsets[i]), bound(v+v_offsets[i])
color2bytes = lambda c: tuple(int(i*255) for i in c)
bytes2color = lambda c: tuple(float(i)/255 for i in c)

def shiftColor(c, i):
    return RGB_24_to_15(color2bytes(hsv2rgb(*bytes2color(applyOffset(i, *color2bytes(rgb2hsv(*bytes2color(c))))))))

print("include")
print("!unexplored_gray = $318c")
print("!vanilla_etank_color = $48fb")
print("!AreaColor_Ceres = !vanilla_etank_color")
for area, color in areaColors.items():
    print("\n;; %s : RGB %s / Hex RGB $%06x" % (area, str(color), color[0] << 16 | color[1] << 8 | color[2]))
    print("!AreaColor_%s = $%04x" % (area,  RGB_24_to_15(color)))
    shiftedColors = [shiftColor(color, i) for i in range(len(s_offsets))]
    print("!Glow_%s = %s" % (area, ','.join(["$%04x" % c for c in shiftedColors])))
