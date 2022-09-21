#!/usr/bin/python3

import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.palette import shrink_palette

from rando.palettes import palettes
p = shrink_palette(palettes)
with open('spalettes.py', 'w') as f:
    f.write("palettes = {\n")
    for addr, values in p.items():
        f.write("{}: {},\n".format(addr, values))
    f.write("}\n")

from varia_custom_sprites.sprite_palettes import sprite_palettes
o = {}
for sprite, palette in sprite_palettes.items():
    o[sprite] = shrink_palette(palette)
with open('ssprite_palettes.py', 'w') as f:
    f.write("sprite_palettes = {}\n")
    for sprite, palette in o.items():
        f.write("sprite_palettes['{}'] = {{".format(sprite))
        for addr, values in palette.items():
            f.write("{}: {},\n".format(addr, values))
        f.write("}\n")

from rando.color_palettes import color_palettes
p = shrink_palette(color_palettes)
with open('scolor_palettes.py', 'w') as f:
    f.write("color_palettes = {\n")
    for addr, values in p.items():
        f.write("{}: {},\n".format(addr, values))
    f.write("}\n")
