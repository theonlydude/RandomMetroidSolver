#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes, getBank
from rom.ips import IPS_Patch

def splitPatchByBank(patchDict):
    newPatchDict = {}
    for addr,bytez in patchDict.items():
        curAddr = addr
        curBank = getBank(pc_to_snes(addr))
        curBytes = []
        newPatchDict[addr] = curBytes
        for b in bytez:
            bank = getBank(pc_to_snes(curAddr))
            if bank != curBank:
                curBank = bank
                curBytes = []
                newPatchDict[curAddr] = curBytes
            curBytes.append(b)
            curAddr += 1
    return newPatchDict

def writeAsm(patch, outAsm):
    print("Writing " + outAsm + "...")
    p=splitPatchByBank(IPS_Patch.load(patch).toDict())
    with open(outAsm, 'w') as f:
        f.write("lorom\narch snes.cpu\n\n")
        for addr,bytez in p.items():
            f.write("org $%06x\n" % pc_to_snes(addr))
            for i in range(0, len(bytez), 8):
                blist = ["$%02x" % b for b in bytez[i:min(len(bytez), i+8)]]
                f.write("\tdb %s\n" % ','.join(blist))
            f.write('\n')

for patch in sys.argv[1:]:
    outAsm = os.path.splitext(patch)[0] + ".asm"
    writeAsm(patch, outAsm)
