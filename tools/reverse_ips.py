#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch
from rom.rom import RealROM

vanilla=sys.argv[1]
ipsToReverse = sys.argv[2:]

rom = RealROM(vanilla)

for ips in ipsToReverse:
    ipsPath = os.path.abspath(ips)
    destDir, destFile = os.path.split(ipsPath)
    destFile = "remove_" + destFile
    destPath = os.path.join(destDir, destFile)
    patch = IPS_Patch.load(ips)
    patchDict = patch.toDict()
    reversePatchDict = {}
    for addr, bytez in patchDict.items():
        sz = len(bytez)
        origBytes = []
        rom.seek(addr)
        for i in range(sz):
            origBytes.append(rom.readByte())
        assert len(origBytes) == sz
        reversePatchDict[addr] = origBytes
    reversePatch = IPS_Patch(reversePatchDict)
    reversePatch.save(destPath)

rom.close()
