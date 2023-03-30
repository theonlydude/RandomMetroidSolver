#!/usr/bin/python3

import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes
from rom.leveldata import Room, Transform, Door
from rom.ips import IPS_Patch

vanillaRomName = sys.argv[1]
mirrorRomName = "mirror_{}".format(os.path.basename(vanillaRomName))
copyfile(vanillaRomName, mirrorRomName)
mirrorRom = RealROM(mirrorRomName)

roomAddr = int(sys.argv[2], 16)
if roomAddr < 0x800000:
    roomAddr = pc_to_snes(roomAddr)

room = Room(mirrorRom, roomAddr)
room.transform(Transform.Mirror)
room.write()
mirrorRom.close()

# pyston ./tools/mirror_room.py ~/metroid/SuperMetroid.sfc 0x8fA98D
# ./tools/make_ips.py ~/metroid/SuperMetroid.sfc mirror_SuperMetroid.sfc croc.ips
# cp ~/metroid/SuperMetroid.sfc croc.sfc
# ./tools/strip_ips.py croc.ips 0x808000 0xa28000 replace
# ./tools/strip_ips.py patches/mirror/ips/mirrortroid.ips 0xC79D71  0xC7A035 replace
# cp ~/metroid/SuperMetroid.sfc .
# ./tools/apply_ips.py patches/mirror/ips/mirrortroid.ips SuperMetroid.sfc 
# ./tools/apply_ips.py croc.ips SuperMetroid.sfc 
# ./tools/make_ips.py ~/metroid/SuperMetroid.sfc SuperMetroid.sfc patches/mirror/ips/mirrortroid.ips 

#  (cd patches/mirror; make); pyston ./randomizer.py -r ~/metroid/SuperMetroid.sfc --randoPreset mirrortroid.json -d |tail -1
#  ./tools/apply_ips.py croc.ips VARIA_Mirrortroid_FX1312835629424366472_regular_medium.sfc
