#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from utils.doorsmanager import doors_mapicons
from rom.map import portal_mapicons

asmPath = sys.argv[1]

def getDoorLabel(color, facing):
    return "door_%s_%s" % (color, str(facing).split('.')[1])

def getPortalLabel(area):
    return "portal_%s" % area

with open(asmPath, "w") as asm:
    asm.write("include\n\n")
    for attrs, icon in doors_mapicons.items():
        asm.write("%s:\n\t%s\n" % (getDoorLabel(*attrs), icon.toSpriteAsm()))
    asm.write("\ndoors_mapicons_sprite_table:\n\tdw %s\n\n" % ','.join([getDoorLabel(*attrs) for attrs in doors_mapicons.keys()]))
    for area, icon in portal_mapicons.items():
        asm.write("%s:\n\t%s\n" % (getPortalLabel(area), icon.toSpriteAsm()))
    asm.write("\nportals_mapicons_sprite_table:\n\tdw %s\n\n" % ','.join([getPortalLabel(area) for area in portal_mapicons.keys()]))
