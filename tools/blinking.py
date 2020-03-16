#!/usr/bin/python3

import sys, struct

mode = sys.argv[1]
rom = sys.argv[2]
plm_set_addr = int(sys.argv[3], 16) # inside bank 8F
plm_idx = int(sys.argv[4], 16)
name = sys.argv[5]
room = int(sys.argv[6], 16)
nmy_set_addr = int(sys.argv[7], 16) # inside bank A1

#     "WS_Map_Grey_Door": {
#         'room': 0Xcc6f,
#         'plm_bytes_list': [
#             [0x48, 0xc8, 0x1, 0x6, 0x61, 0x90]
#         ]
#     },

#    "Escape_Rando_Tourian_Doors":{
#        0x7C836: [0x0C]
#    },

plmAddr = 0x70000 + plm_set_addr + plm_idx * 6

def makePlmBytes(plm):
    line = "["
    first=True
    for b in plm:
        if not first:
            line += ', '
        line += ('0x%02x' % b)
        first = False
    line += ']'
    return line

with open(rom, 'rb') as romFile:
    def readPLM():
        romFile.seek(plmAddr)
        return romFile.read(6)
    def readMaxEnemiesAddr():
        romFile.seek(0x100000 + nmy_set_addr)
        w = 0
        while w != 0xffff:
            w = int.from_bytes(romFile.read(2), byteorder='little')
        return romFile.tell()
    plm = readPLM()
    if mode[0] == 'a':
        print("    '%s': {" % name)
        print("        'room': 0x%04x," % room)
        print("        'plm_bytes_list': [")
        print("            " + makePlmBytes(plm))
        print("        ]")
        print("    },")
        print("\n")
    print("    '%s': {" % name)
    if mode[0] == 'p':
        print("        0x%X: %s," % (plmAddr, makePlmBytes(plm)))
    print("        0x%X: [0x0]" % readMaxEnemiesAddr())
    print("    },")
