#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes
from rom.ips import IPS_Patch

def writeAsm(patch, outAsm):
    print("Writing " + outAsm + "...")
    p=IPS_Patch.load(patch).toDict()
    with open(outAsm, 'w') as f:
        f.write("lorom\narch 65816\n\n")
        for addr,bytez in p.items():
            f.write("org $%06x\nprint pc\n" % pc_to_snes(addr))
            for i in range(0, len(bytez), 8):
                blist = ["$%02x" % b for b in bytez[i:min(len(bytez), i+8)]]
                f.write("\tdb %s\n" % ','.join(blist))
            f.write('print pc\n')

for patch in sys.argv[1:]:
    outAsm = os.path.splitext(patch)[0] + ".asm"
    writeAsm(patch, outAsm)
