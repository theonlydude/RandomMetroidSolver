#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch
from rom.rom import pc_to_snes, snes_to_pc

# only keep IPS patch data in banks F5-FF, as it's the only place SpriteSomething writes to
# depending on the IPS patcher used, it zero-fills any data >= bank E0, which can conflict 
# with other stuff

patches = sys.argv[1:]

sprite_smthg_bank = 0xF5
sprite_smthg_bank_start = snes_to_pc((sprite_smthg_bank << 16) | 0x8000)

for p in patches:
    if os.path.getsize(p) == 0:
        continue
    print(p)
    patch = IPS_Patch.load(p)
    toRemove = []
    toAdd = []
    for r in patch.records:        
        firstByteAddr = pc_to_snes(r['address'])
        lastByteAddr = pc_to_snes(r['address'] + r['size'] - 1)
        startBank = firstByteAddr >> 16
        endBank = lastByteAddr >> 16
        if startBank > 0xDF and startBank < sprite_smthg_bank:
            toRemove.append(r)
            if endBank >= sprite_smthg_bank:
                assert 'rle_count' in r, "Unhandled simple record"
                before = sprite_smthg_bank_start - r['address']
                newSz = r['size'] - before
                assert newSz > 0
                toAdd.append({'address': sprite_smthg_bank_start, 'data': r['data'], 'rle_count': newSz, 'size': newSz})
    for r in toRemove:
        patch.records.remove(r)
    for r in toAdd:
        patch.records.append(r)
    patch.save(p)
