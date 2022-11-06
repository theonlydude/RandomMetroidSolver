#!/usr/bin/env python3

# prereq:
#  git clone git@github.com:tewtal/sm_banklog_parser.git
#  cd sm_banklog_parser/logs
#  python3 download_banks.py
#  cd ..
#  cargo run --release
#  cd asm
#  echo "vanilla = {" > vanilla_addresses.py; for asm in bank_??.asm; do bank=$(echo "${asm}" | cut -d '_' -f 2 | cut -d '.' -f 1); grep -E '^;;; \$[0-9A-F]*:' ${asm} | sed -e "s+;;; \$\([0-9A-F]*\): \(.*\) ;;;+0x${bank}\1: \"\2\",+" -e 's+;;; \$\([0-9A-F][0-9A-F]\):\([0-9A-F]*\): \(.*\) ;;;+0x\1\2: "\3",+'; done >> vanilla_addresses.py; echo "}" >> vanilla_addresses.py
#  mv vanilla_addresses.py ~/RandomMetroidSolver/rom/

import sys, os
from collections import defaultdict

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.vanilla_addresses import vanilla
from rom.ips import IPS_Patch
from rom.rom import pc_to_snes

def gen_vanilla_map(vanilla):
    # generate a big dict telling for each byte in which vanilla section it is
    vanilla_map = {}

    # some entries in pjboy disam spawn on multiple banks, manually add entries for these
    vanilla[0xBA0000] = "Backgrounds (compressed)"
    vanilla[0xBB0000] = "Tiles (compressed)"
    vanilla[0xBC0000] = "Tiles (compressed)"
    vanilla[0xBD0000] = "Tiles (compressed)"
    vanilla[0xBE0000] = "Tiles (compressed)"
    vanilla[0xBF0000] = "Tiles (compressed)"
    vanilla[0xC00000] = "Tiles (compressed)"
    vanilla[0xC10000] = "Tiles (compressed)"
    vanilla[0xC20000] = "Tile tables (compressed)"
    vanilla[0xC30000] = "Level data (compressed)"
    vanilla[0xC40000] = "Level data (compressed)"
    vanilla[0xC50000] = "Level data (compressed)"
    vanilla[0xC60000] = "Level data (compressed)"
    vanilla[0xC70000] = "Level data (compressed)"
    vanilla[0xC80000] = "Level data (compressed)"
    vanilla[0xC90000] = "Level data (compressed)"
    vanilla[0xCA0000] = "Level data (compressed)"
    vanilla[0xCB0000] = "Level data (compressed)"
    vanilla[0xCC0000] = "Level data (compressed)"
    vanilla[0xCD0000] = "Level data (compressed)"
    vanilla[0xCE0000] = "Level data (compressed)"
    # if extra banks are used by the patch
    for b in range(0xe0, 0xff+1):
        vanilla[b<<16] = "Extra bank"

    cur_bank = 0x80
    prev_address = -1
    for address in vanilla.keys():
        bank = (address & 0xff0000) >> 16
        #print("bank: {} address: {}".format(hex(bank), hex(address)))
        if bank != cur_bank:
            # fill remaining of previous bank
            #print("fill {} to [{} - {}]".format(hex(prev_address), hex(prev_address), hex(bank << 16)))
            for i in range(prev_address, (bank << 16)):
                vanilla_map[i] = prev_address
            cur_bank = bank
            prev_address = address
        else:
            # fill remaining of previous address
            #print("set {} to [{} - {}]".format(hex(prev_address), hex(prev_address), hex(address - 1)))
            for i in range(prev_address, address):
                vanilla_map[i] = prev_address
            prev_address = address

    # fill remaining of last address
    #print("last fill {} to [{} - {}]".format(hex(prev_address), hex(prev_address), hex((bank << 16) + 0xffff)))
    for i in range(prev_address, (bank << 16) + 0xffff + 1):
        vanilla_map[i] = prev_address

    return vanilla_map

patch = sys.argv[1]
ips = IPS_Patch.load(patch)

vanilla_map = gen_vanilla_map(vanilla)

# get all addresses modified by the patch
modified = defaultdict(int)
for r in ips.getRanges():
    for i in r:
        modified[vanilla_map[pc_to_snes(i)]] += 1

print("patch {} has modifications in:".format(patch))
print("")
print("Address  | Bytes | Label")
print("-"*128)
modifiedKeys = sorted(list(modified.keys()))
for address in modifiedKeys:
    print("{} | {:>5} | {}".format(hex(address), modified[address], vanilla[address]))
