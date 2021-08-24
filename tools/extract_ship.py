#!/usr/bin/python3

import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# extract ship tiles & palette from hack, generate an ips in the end.
# works only if ship has not been relocated.
# don't update collisions, so ship must have the same shape as vanilla.

from rom.rom import RealROM, snes_to_pc
from rom.ips import IPS_Patch

vanilla = sys.argv[1]
hack = sys.argv[2]

# copy vanilla in tmpfile
tmpfile = '/tmp/vanilla.sfc'
copyfile(vanilla, tmpfile)

# extract data from hack
tilesAddr = [snes_to_pc(0xADB600), snes_to_pc(0xADC600)]
palettesAddr = [snes_to_pc(0xA2A59E), snes_to_pc(0xA2A5BE)]

hackRom = RealROM(hack)
tilesBytes = []
for addr in range(tilesAddr[0], tilesAddr[1]):
    tilesBytes.append(hackRom.readByte(addr))
palettesBytes = []
for addr in range(palettesAddr[0], palettesAddr[1]):
    palettesBytes.append(hackRom.readByte(addr))

# write data in tmpfile
tmpRom = RealROM(tmpfile)
tmpRom.seek(tilesAddr[0])
for byte in tilesBytes:
    tmpRom.writeByte(byte)
tmpRom.seek(palettesAddr[0])
for byte in palettesBytes:
    tmpRom.writeByte(byte)
tmpRom.close()

# generate ips between vanilla & tempfile

patch = IPS_Patch.create(open(vanilla, 'rb').read(), open(tmpfile, 'rb').read())
out = hack+'.ips'
patch.save(out)
print("ips generated: {}".format(out))
