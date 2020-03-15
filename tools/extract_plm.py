#!/usr/bin/python3

import sys, struct

rom = sys.argv[1]
plm_set_addr = int(sys.argv[2], 16) # inside bank 8F
plm_idx = int(sys.argv[3], 16)
name = sys.argv[4]
room = int(sys.argv[5], 16)
nmy_set_addr = int(sys.argv[6], 16) # inside bank A1

#     "WS_Map_Grey_Door": {
#         'room': 0Xcc6f,
#         'plm_bytes_list': [
#             [0x48, 0xc8, 0x1, 0x6, 0x61, 0x90]
#         ]
#     },

#    "Escape_Rando_Tourian_Doors":{
#        0x7C836: [0x0C]
#    },
with open(rom, 'rb') as romFile:
    def readPLM():
        romFile.seek(0x70000 + plm_set_addr + plm_idx * 6)
        return romFile.read(6)
    def readMaxEnemiesAddr():
        romFile.seek(0x100000 + nmy_set_addr)
        w = 0
        while w != 0xffff:
            w = int.from_bytes(romFile.read(2), byteorder='little')
        return romFile.tell()
    print("    '%s': {" % name)
    print("        'room': 0x%04x," % room)
    print("        'plm_bytes_list': [")
    line = "            ["
    first=True
    for b in readPLM():
        if not first:
            line += ', '
        line += ('0x%02x' % b)
        first = False
    line += ']'
    print(line)
    print("        ]")
    print("    },")
    print("\n")
    print("    '%s': {" % name)
    print("        0x%X: [0x0]" % readMaxEnemiesAddr())
    print("    },")
