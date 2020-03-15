#!/usr/bin/python3

import sys, struct

rom = sys.argv[1]
plm_set_addr = int(sys.argv[2], 16) # inside bank 8F
plm_idx = int(sys.argv[3], 16)
name = sys.argv[4]
room = int(sys.argv[5], 16)

#     "WS_Map_Grey_Door": {
#         'room': 0Xcc6f,
#         'plm_bytes_list': [
#             [0x48, 0xc8, 0x1, 0x6, 0x61, 0x90]
#         ]
#     },


with open(rom, 'rb') as romFile:
    def readPLM():
        romFile.seek(0x70000 + plm_set_addr + plm_idx * 6)
        return romFile.read(6)
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
