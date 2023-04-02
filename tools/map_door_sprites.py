#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from utils.doorsmanager import doors_mapicons

asmPath = sys.argv[1]

def getLabel(color, facing):
    return "%s_%s" % (color, str(facing).split('.')[1])

with open(asmPath, "w") as asm:
    asm.write("include\n\n")
    for attrs, icon in doors_mapicons.items():
        asm.write("%s:\n\t%s\n" % (getLabel(*attrs), icon.toSpriteAsm()))
    asm.write("\ndoors_mapicons_sprite_table:\n\tdw %s\n" % ','.join([getLabel(*attrs) for attrs in doors_mapicons.keys()]))
