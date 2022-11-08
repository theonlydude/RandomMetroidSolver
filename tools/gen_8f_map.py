#!/bin/python3

# prereq:
# start with bank_8F.asm from total's banklog parser.
# replace comments with labels. 
# compile it with asar with wla symbols export in sm.sym_wla
# echo "bank_8f = {" > bank8f_addresses.py
# grep -E '^8F:' sm.sym_wla | sed -e 's+^8F:\([0-9A-Z]*\) \(.*\)$+0x8F\1: "\2",+' | sort >> bank8f_addresses.py
# echo "}" >> bank8f_addresses.py
# mv bank8f_addresses.py ~/RandomMetroidSolver/rom/

import sys, os
from collections import defaultdict

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.bank8f_addresses import bank_8f
from rom.ips import IPS_Patch
from rom.rom import pc_to_snes, snes_to_pc, RealROM
from tools.rooms import rooms

def gen_bank8f_map(bank8f, patched):
    # generate a big dict telling for each byte in which vanilla section it is
    bank8f_map = {}
    # also tell the length of each label data
    bank8f_len = {}

    prev_address = -1
    for address in bank8f.keys():
        # fill remaining of previous address
        #print("set {} to [{} - {}]".format(hex(prev_address), hex(prev_address), hex(address - 1)))
        for i in range(prev_address, address):
            bank8f_map[i] = prev_address
        prev_address = address

    prev_address = None
    for address in bank8f.keys():
        if prev_address is not None:
            length = address - prev_address
            bank8f_len[prev_address] = length
        prev_address = address

    # search for non 0xff in free space
    freespace_start = prev_address
    patched.seek(snes_to_pc(freespace_start))
    freespace = [patched.readByte() for _ in range(0x8fffff - freespace_start + 1)]
    count = 0
    in_data = False
    cur_label = None
    for i, byte in enumerate(freespace):
        if byte == 0xff:
            if in_data:
                # add lenght of previous non free segment
                length = freespace_start + i - prev_address
                bank8f_len[prev_address] = length
            in_data = False
            bank8f_map[freespace_start + i] = -1
        elif not in_data:
            # add new label
            in_data = True
            cur_label = "FreeSpace_{}".format(bhex2(count))
            count += 1
            bank8f[freespace_start + i] = cur_label
            prev_address = freespace_start + i
            bank8f_map[freespace_start + i] = prev_address
        else:
            bank8f_map[freespace_start + i] = prev_address
    if in_data:
        # if data goes up to the end of the bank
        bank8f_len[prev_address] = 0x8fffff - prev_address

    return (bank8f_map, bank8f_len)

def bhex(v):
    hex_part = hex(v)[2:]
    if len(hex_part) == 1:
        return "$0{}".format(hex_part)
    else:
        return "${}".format(hex_part)

def bhex2(v):
    hex_part = hex(v)[2:]
    if len(hex_part) == 1:
        ret = "0{}".format(hex_part)
    else:
        ret = "{}".format(hex_part)
    return ret.upper()

def whex(v):
    hex_part = hex(v)[2:]
    if len(hex_part) == 1:
        return "$000{}".format(hex_part)
    elif len(hex_part) == 2:
        return "$00{}".format(hex_part)
    elif len(hex_part) == 3:
        return "$0{}".format(hex_part)
    else:
        return "${}".format(hex_part)

def whex2(v):
    hex_part = hex(v)[2:]
    if len(hex_part) == 1:
        ret = "000{}".format(hex_part)
    elif len(hex_part) == 2:
        ret = "00{}".format(hex_part)
    elif len(hex_part) == 3:
        ret = "0{}".format(hex_part)
    else:
        ret = "{}".format(hex_part)
    return ret.upper()

patch = sys.argv[1]
ips = IPS_Patch.load(patch)

vanilla = RealROM(sys.argv[2])
patched = RealROM(sys.argv[3])

(bank8f_map, bank8f_len) = gen_bank8f_map(bank_8f, patched)

rooms_name = { hex(d["Address"] & 0xFFFF)[2:].upper(): d["Name"] for d in rooms}

# get all addresses modified by the patch
modified = defaultdict(int)
ranges = defaultdict(set)
for r in ips.getRanges():
    # keep only bank 8f
    if r.start < snes_to_pc(0x8f8000) or r.stop > snes_to_pc(0x8fffff):
        continue
    for i in r:
        address = bank8f_map[pc_to_snes(i)]
        if address != -1:
            modified[address] += 1
            ranges[address].add(r)

print("patch {} has modifications in bank 8f:".format(patch))
print("")
print("Address  | Bytes | Label")
print("-"*128)
modifiedKeys = sorted(list(modified.keys()))
for address in modifiedKeys:
    print("{} | {:>5} | {} | {}".format(hex(address), modified[address], bank_8f[address], ["[{}-{}]".format(hex(pc_to_snes(r.start)), hex(pc_to_snes(r.stop))) for r in sorted(ranges[address], key=lambda x: x.start)]))

plm_name = {
    0xB62F: "Don't make PLM",
    0xB633: "Collision reaction, special, BTS Brinstar 80h/81h. Nothing",
    0xB637: "Unused. Nothing",
    0xB63B: "Rightwards extension",
    0xB63F: "Leftwards extension",
    0xB643: "Downwards extension",
    0xB647: "Upwards extension",
    0xB64B: "Wrecked Ship entrance treadmill from west",
    0xB64F: "Wrecked Ship entrance treadmill from east",
    0xB653: "Inside reaction, special air, BTS Norfair 80h. Nothing",
    0xB657: "Inside reaction, special air, BTS Norfair 81h. Nothing",
    0xB65B: "Inside reaction, special air, BTS Norfair 82h. Nothing",
    0xB65F: "Unused",
    0xB663: "Unused",
    0xB667: "Unused",
    0xB66B: "Unused",
    0xB66F: "Unused",
    0xB673: "Fill Mother Brain's wall",
    0xB677: "Mother Brain's room escape door",
    0xB67B: "Mother Brain's background row 2",
    0xB67F: "Mother Brain's background row 3",
    0xB683: "Mother Brain's background row 4",
    0xB687: "Mother Brain's background row 5",
    0xB68B: "Mother Brain's background row 6",
    0xB68F: "Mother Brain's background row 7",
    0xB693: "Mother Brain's background row 8",
    0xB697: "Mother Brain's background row 9",
    0xB69B: "Mother Brain's background row Ah",
    0xB69F: "Mother Brain's background row Bh",
    0xB6A3: "Mother Brain's background row Ch",
    0xB6A7: "Mother Brain's background row Dh",
    0xB6AB: "Unused",
    0xB6AF: "Unused",
    0xB6B3: "Clear ceiling block in Mother Brain's room",
    0xB6B7: "Clear ceiling tube in Mother Brain's room",
    0xB6BB: "Clear Mother Brain's bottom-middle-side tube",
    0xB6BF: "Clear Mother Brain's bottom-middle tubes",
    0xB6C3: "Clear Mother Brain's bottom-left tube",
    0xB6C7: "Clear Mother Brain's bottom-right tube",
    0xB6CB: "Inside reaction, special air, BTS Brinstar 80h. Floor plant",
    0xB6CF: "Inside reaction, special air, BTS Brinstar 81h. Ceiling plant",
    0xB6D3: "Map station",
    0xB6D7: "Collision reaction, special, BTS 47h. Map station right access",
    0xB6DB: "Collision reaction, special, BTS 48h. Map station left access",
    0xB6DF: "Energy station",
    0xB6E3: "Collision reaction, special, BTS 49h. Energy station right access",
    0xB6E7: "Collision reaction, special, BTS 4Ah. Energy station left access",
    0xB6EB: "Missile station",
    0xB6EF: "Collision reaction, special, BTS 4Bh. Missile station right access",
    0xB6F3: "Collision reaction, special, BTS 4Ch. Missile station left access",
    0xB6F7: "Nothing",
    0xB6FB: "Nothing",
    0xB6FF: "Collision reaction, special, BTS 46h / inside reaction, special air, BTS 46h. Scroll PLM trigger",
    0xB703: "Scroll PLM",
    0xB707: "Unused. Solid scroll PLM",
    0xB70B: "Elevator platform",
    0xB70F: "Inside reaction, special air, BTS Crateria/Debug 80h",
    0xB713: "Inside reaction, special air, BTS Maridia 80h/81h/82h. Quicksand surface",
    0xB717: "Unused. Clone of PLM B713",
    0xB71B: "Unused. Clone of PLM B713",
    0xB71F: "Inside reaction, special air, BTS Maridia 83h. Submerging quicksand",
    0xB723: "Inside reaction, special air, BTS Maridia 84h. Sand falls - slow",
    0xB727: "Inside reaction, special air, BTS Maridia 85h. Sand falls - fast",
    0xB72B: "Collision reaction, special, BTS Maridia 80h/81h/82h. Quicksand surface",
    0xB72F: "Unused",
    0xB733: "Unused",
    0xB737: "Collision reaction, special, BTS Maridia 83h. Submerging quicksand",
    0xB73B: "Collision reaction, special, BTS Maridia 84h. Sand falls - slow",
    0xB73F: "Collision reaction, special, BTS Maridia 85h. Sand falls - fast",
    0xB743: "Unused. Torizo drool?",
    0xB747: "Clear Crocomire's bridge",
    0xB74B: "Crumble a block of Crocomire's bridge",
    0xB74F: "Clear a block of Crocomire's bridge",
    0xB753: "Clear Crocomire invisible wall",
    0xB757: "Create Crocomire invisible wall",
    0xB75B: "Unused. Draw 13 blank air tiles",
    0xB75F: "Unused. Draw 13 blank solid tiles",
    0xB763: "Clear Shitroid invisible wall",
    0xB767: "Create Shitroid invisible wall",
    0xB76B: "Collision reaction, special, BTS 4Dh. Save station trigger",
    0xB76F: "Save station",
    0xB773: "Crumble access to Tourian elevator",
    0xB777: "Clear access to Tourian elevator",
    0xB8AC: "Speed Booster escape",
    0xBAF4: "Bomb Torizo grey door",
    0xBB05: "Wrecked Ship attic",
    0xC806: "Shot/bombed/grappled reaction, shootable, BTS 4Ah. Left green gate trigger",
    0xC80A: "Shot/bombed/grappled reaction, shootable, BTS 4Bh. Right green gate trigger",
    0xC80E: "Shot/bombed/grappled reaction, shootable, BTS 48h. Left red gate trigger",
    0xC812: "Shot/bombed/grappled reaction, shootable, BTS 49h. Right red gate trigger",
    0xC816: "Shot/bombed/grappled reaction, shootable, BTS 46h. Left blue gate trigger",
    0xC81A: "Shot/bombed/grappled reaction, shootable, BTS 47h. Right blue gate trigger",
    0xC81E: "Shot/bombed/grappled reaction, shootable, BTS 4Ch. Left yellow gate trigger",
    0xC822: "Shot/bombed/grappled reaction, shootable, BTS 4Dh. Right yellow gate trigger",
    0xC826: "Downwards open gate",
    0xC82A: "Downwards closed gate",
    0xC82E: "Upwards open gate",
    0xC832: "Upwards closed gate",
    0xC836: "Downwards gate shotblock",
    0xC83A: "Upwards gate shotblock",
    0xC83E: "Shot/bombed/grappled reaction, shootable, BTS 44h / collision reaction, special, BTS 44h. Generic shot trigger for a PLM",
    0xC842: "Door. Grey door facing left",
    0xC848: "Door. Grey door facing right",
    0xC84E: "Door. Grey door facing up",
    0xC854: "Door. Grey door facing down",
    0xC85A: "Door. Yellow door facing left",
    0xC860: "Door. Yellow door facing right",
    0xC866: "Door. Yellow door facing up",
    0xC86C: "Door. Yellow door facing down",
    0xC872: "Door. Green door facing left",
    0xC878: "Door. Green door facing right",
    0xC87E: "Door. Green door facing up",
    0xC884: "Door. Green door facing down",
    0xC88A: "Door. Red door facing left",
    0xC890: "Door. Red door facing right",
    0xC896: "Door. Red door facing up",
    0xC89C: "Door. Red door facing down",
    0xC8A2: "Door. shot/bombed/grappled reaction, shootable, BTS 40h. Blue facing left",
    0xC8A8: "Door. shot/bombed/grappled reaction, shootable, BTS 41h. Blue facing right",
    0xC8AE: "Door. shot/bombed/grappled reaction, shootable, BTS 42h. Blue facing up",
    0xC8B4: "Door. shot/bombed/grappled reaction, shootable, BTS 43h. Blue facing down",
    0xC8BA: "Blue door closing facing left",
    0xC8BE: "Blue door closing facing right",
    0xC8C2: "Blue door closing facing up",
    0xC8C6: "Blue door closing facing down",
    0xC8CA: "Door. Gate that closes during escape in room after Mother Brain",
    0xC8D0: "PLM version of the above",
    0xCFEC: "Unused. Draws 1x1 shot block",
    0xCFF0: "Unused. Draws 1x2 shot block",
    0xCFF4: "Unused. Draws 2x1 shot block",
    0xCFF8: "Unused. Draws 2x2 shot block",
    0xCFFC: "Bomb reaction, special block, BTS 0/4. 1x1 (respawning) crumble block",
    0xD000: "Bomb reaction, special block, BTS 1/5. 2x1 (respawning) crumble block",
    0xD004: "Bomb reaction, special block, BTS 2/6. 1x2 (respawning) crumble block",
    0xD008: "Bomb reaction, special block, BTS 3/7. 2x2 (respawning) crumble block",
    0xD00C: "Unused",
    0xD010: "Unused",
    0xD014: "Unused",
    0xD018: "Unused",
    0xD01C: "Unused",
    0xD020: "Unused",
    0xD024: "Bomb reaction, special block, BTS Eh/Fh / Brinstar 82h/83h/84h/85h. Speed boost block",
    0xD028: "Unused",
    0xD02C: "Unused",
    0xD030: "Collision reaction, special, BTS Brinstar 82h",
    0xD034: "Collision reaction, special, BTS Brinstar 83h",
    0xD038: "Collision reaction, special, BTS Eh. Respawning speed boost block",
    0xD03C: "Collision reaction, special, BTS Brinstar 84h. Respawning speed boost block (used by dachora pit)",
    0xD040: "Collision reaction, special, BTS Fh / Brinstar 85h. Speed boost block",
    0xD044: "Collision reaction, special, BTS 0. 1x1 respawning crumble block",
    0xD048: "Collision reaction, special, BTS 1. 2x1 respawning crumble block",
    0xD04C: "Collision reaction, special, BTS 2. 1x2 respawning crumble block",
    0xD050: "Collision reaction, special, BTS 3. 2x2 respawning crumble block",
    0xD054: "Collision reaction, special, BTS 4. 1x1 crumble block",
    0xD058: "Collision reaction, special, BTS 5. 2x1 crumble block",
    0xD05C: "Collision reaction, special, BTS 6. 1x2 crumble block",
    0xD060: "Collision reaction, special, BTS 7. 2x2 crumble block",
    0xD064: "Shot/bombed/grappled reaction, shootable, BTS 0. 1x1 respawning shot block",
    0xD068: "Shot/bombed/grappled reaction, shootable, BTS 1. 2x1 respawning shot block",
    0xD06C: "Shot/bombed/grappled reaction, shootable, BTS 2. 1x2 respawning shot block",
    0xD070: "Shot/bombed/grappled reaction, shootable, BTS 3. 2x2 respawning shot block",
    0xD074: "Shot/bombed/grappled reaction, shootable, BTS 4. 1x1 shot block",
    0xD078: "Shot/bombed/grappled reaction, shootable, BTS 5. 2x1 shot block",
    0xD07C: "Shot/bombed/grappled reaction, shootable, BTS 6. 1x2 shot block",
    0xD080: "Shot/bombed/grappled reaction, shootable, BTS 7. 2x2 shot block",
    0xD084: "Shot/bombed/grappled reaction, shootable, BTS 8. Respawning power bomb block",
    0xD088: "Shot/bombed/grappled reaction, shootable, BTS 9. Power bomb block",
    0xD08C: "Shot/bombed/grappled reaction, shootable, BTS A. Respawning super missile block",
    0xD090: "Shot/bombed/grappled reaction, shootable, BTS B. Super missile block",
    0xD094: "Enemy collision reaction, spike block, BTS Fh. Enemy breakable block",
    0xD098: "Collision reaction, bombable, BTS 0. 1x1 respawning bomb block",
    0xD09C: "Collision reaction, bombable, BTS 1. 2x1 respawning bomb block",
    0xD0A0: "Collision reaction, bombable, BTS 2. 1x2 respawning bomb block",
    0xD0A4: "Collision reaction, bombable, BTS 3. 2x2 respawning bomb block",
    0xD0A8: "Collision reaction, bombable, BTS 4. 1x1 bomb block",
    0xD0AC: "Collision reaction, bombable, BTS 5. 2x1 bomb block",
    0xD0B0: "Collision reaction, bombable, BTS 6. 1x2 bomb block",
    0xD0B4: "Collision reaction, bombable, BTS 7. 2x2 bomb block",
    0xD0B8: "Shot/bombed/grappled reaction, bombable, BTS 0. 1x1 respawning bomb block",
    0xD0BC: "Shot/bombed/grappled reaction, bombable, BTS 1. 2x1 respawning bomb block",
    0xD0C0: "Shot/bombed/grappled reaction, bombable, BTS 2. 1x2 respawning bomb block",
    0xD0C4: "Shot/bombed/grappled reaction, bombable, BTS 3. 2x2 respawning bomb block",
    0xD0C8: "Shot/bombed/grappled reaction, bombable, BTS 4. 1x1 bomb block",
    0xD0CC: "Shot/bombed/grappled reaction, bombable, BTS 5. 2x1 bomb block",
    0xD0D0: "Shot/bombed/grappled reaction, bombable, BTS 6. 1x2 bomb block",
    0xD0D4: "Shot/bombed/grappled reaction, bombable, BTS 7. 2x2 bomb block",
    0xD0D8: "Grappled reaction, grapple block, BTS 0/3. Grapple block",
    0xD0DC: "Grappled reaction, grapple block, BTS 1. Respawning breakable grapple block",
    0xD0E0: "Grappled reaction, grapple block, BTS 2. Breakable grapple block",
    0xD0E4: "Grappled reaction, generic spike block",
    0xD0E8: "Grappled reaction, spike block, BTS 3. Draygon's broken turret",
    0xD6D6: "Lower Norfair chozo hand",
    0xD6DA: "Collision reaction, special, BTS Norfair 83h. Lower Norfair chozo hand check",
    0xD6DE: "Mother Brain's glass",
    0xD6E2: "Unused. Mother Brain's glass, area boss dead",
    0xD6E6: "Unused. Mother Brain's glass, no glass state",
    0xD6EA: "Bomb Torizo's crumbling chozo",
    0xD6EE: "Wrecked Ship chozo hand",
    0xD6F2: "Collision reaction, special, BTS Wrecked Ship 80h. Wrecked Ship chozo hand check",
    0xD6F8: "Clear slope access for Wrecked Ship chozo",
    0xD6FC: "Block slope access for Wrecked Ship chozo",
    0xD700: "Unused. Wrecked Ship 3x4 chozo bomb block",
    0xD704: "Unused. Alternate Lower Norfair chozo hand",
    0xD708: "Unused. Lower Norfair 2x2 chozo shot block",
    0xD70C: "n00b tube",
    0xDB44: "Sets Metroids cleared states when required",
    0xDB48: "Eye door eye, facing right",
    0xDB4C: "Door. Eye door, facing right",
    0xDB52: "Eye door bottom, facing right",
    0xDB56: "Eye door eye, facing left",
    0xDB5A: "Door. Eye door, facing left",
    0xDB60: "Eye door bottom, facing left",
    0xDF59: "Draygon cannon, with shield, facing right",
    0xDF5D: "Unused. Draygon cannon, with shield, facing down-right",
    0xDF61: "Unused. Draygon cannon, with shield, facing up-right",
    0xDF65: "Draygon cannon, facing right",
    0xDF69: "Unused. Draygon cannon, facing down-right",
    0xDF6D: "Unused. Draygon cannon, facing up-right",
    0xDF71: "Draygon cannon, with shield, facing left",
    0xDF75: "Unused. Draygon cannon, with shield, facing down-left",
    0xDF79: "Unused. Draygon cannon, with shield, facing up-left",
    0xDF7D: "Dragon cannon, facing left",
    0xDF81: "Unused. Draygon cannon, facing down-left",
    0xDF85: "Unused. Draygon cannon, facing up-left",
    0xEED3: "Shot/bombed/grappled reaction, shootable, BTS 45h / collision reaction, special, BTS 45h. Item collision detection",
    0xEED7: "Energy tank",
    0xEEDB: "Missile tank",
    0xEEDF: "Super missile tank",
    0xEEE3: "Power bomb tank",
    0xEEE7: "Bombs",
    0xEEEB: "Charge beam",
    0xEEEF: "Ice beam",
    0xEEF3: "Hi-jump",
    0xEEF7: "Speed booster",
    0xEEFB: "Wave beam",
    0xEEFF: "Spazer beam",
    0xEF03: "Spring ball",
    0xEF07: "Varia suit",
    0xEF0B: "Gravity suit",
    0xEF0F: "X-ray scope",
    0xEF13: "Plasma beam",
    0xEF17: "Grapple beam",
    0xEF1B: "Space jump",
    0xEF1F: "Screw attack",
    0xEF23: "Morph ball",
    0xEF27: "Reserve tank",
    0xEF2B: "Energy tank, chozo orb",
    0xEF2F: "Missile tank, chozo orb",
    0xEF33: "Super missile tank, chozo orb",
    0xEF37: "Power bomb tank, chozo orb",
    0xEF3B: "Bombs, chozo orb",
    0xEF3F: "Charge beam, chozo orb",
    0xEF43: "Ice beam, chozo orb",
    0xEF47: "Hi-jump, chozo orb",
    0xEF4B: "Speed booster, chozo orb",
    0xEF4F: "Wave beam, chozo orb",
    0xEF53: "Spazer beam, chozo orb",
    0xEF57: "Spring ball, chozo orb",
    0xEF5B: "Varia suit, chozo orb",
    0xEF5F: "Gravity suit, chozo orb",
    0xEF63: "X-ray scope, chozo orb",
    0xEF67: "Plasma beam, chozo orb",
    0xEF6B: "Grapple beam, chozo orb",
    0xEF6F: "Space jump, chozo orb",
    0xEF73: "Screw attack, chozo orb",
    0xEF77: "Morph ball, chozo orb",
    0xEF7B: "Reserve tank, chozo orb",
    0xEF7F: "Energy tank, shot block",
    0xEF83: "Missile tank, shot block",
    0xEF87: "Super missile tank, shot block",
    0xEF8B: "Power bomb tank, shot block",
    0xEF8F: "Bombs, shot block",
    0xEF93: "Charge beam, shot block",
    0xEF97: "Ice beam, shot block",
    0xEF9B: "Hi-jump, shot block",
    0xEF9F: "Speed booster, shot block",
    0xEFA3: "Wave beam, shot block",
    0xEFA7: "Spazer beam, shot block",
    0xEFAB: "Spring ball, shot block",
    0xEFAF: "Varia suit, shot block",
    0xEFB3: "Gravity suit, shot block",
    0xEFB7: "X-ray scope, shot block",
    0xEFBB: "Plasma beam, shot block",
    0xEFBF: "Grapple beam, shot block",
    0xEFC3: "Space jump, shot block",
    0xEFC7: "Screw attack, shot block",
    0xEFCB: "Morph ball, shot block",
    0xEFCF: "Reserve tank, shot block",

    # mirrortroid custom
    0xFC1F: "Chain block (relocated)",
    0xF060: "Chain block (original)",

    # varia custom
    0xBAE9: "Nothing item, visible block",
    0xBAED: "Nothing item, shot block",

    0xFBB0: "plm_indicator_missile_left",
    0xFBB6: "plm_indicator_missile_right",
    0xFBBC: "plm_indicator_missile_top",
    0xFBC2: "plm_indicator_missile_bottom",
    0xFBC8: "plm_indicator_super_left",
    0xFBCE: "plm_indicator_super_right",
    0xFBD4: "plm_indicator_super_top",
    0xFBDA: "plm_indicator_super_bottom",
    0xFBE0: "plm_indicator_PB_left",
    0xFBE6: "plm_indicator_PB_right",
    0xFBEC: "plm_indicator_PB_top",
    0xFBF2: "plm_indicator_PB_bottom",
    0xFBF8: "plm_indicator_none_left",
    0xFBFE: "plm_indicator_none_right",
    0xFC04: "plm_indicator_none_top",
    0xFC0A: "plm_indicator_none_bottom"
}

def print_plm(out, rom, address, length, room_address, modifiedKeys):
    plm_length = 6
    nb_plm = (length-2)//plm_length
    rom.seek(snes_to_pc(address))
    early = False
    for _ in range(nb_plm):
        plm = rom.readWord()

        if plm == 0x0000:
            out.write("    ; plms terminates before vanilla\n")
            early = True
        x = rom.readByte()
        y = rom.readByte()
        params = rom.readWord()

        params_label = False
        # if door add label with door id
        if not early and plm in (0xC842, 0xC848, 0xC84E, 0xC854, # grey
                                 0xC85A, 0xC860, 0xC866, 0xC86C, # yellow
                                 0xC872, 0xC878, 0xC87E, 0xC884, # green
                                 0xC88A, 0xC890, 0xC896, 0xC89C, # red
                                 0xC8BA, 0xC8BE, 0xC8C2, 0xC8C6, # blue
                                 0xC8A2, 0xC8A8, 0xC8AE, 0xC8B4, # special blue
                                 0xC8CA, 0xB677, 0xBAF4, # special grey
                                 0xDB4C, 0xDB5A, # gadora
                                 # VARIA special
                                 0xFBB0, 0xFBB6, 0xFBBC, 0xFBC2, # red indicator
                                 0xFBC8, 0xFBCE, 0xFBD4, 0xFBDA, # green indicator
                                 0xFBE0, 0xFBE6, 0xFBEC, 0xFBF2, # yellow indicator
                                 0xFBF8, 0xFBFE, 0xFC04, 0xFC0A):# grey indicator
            door_id = params & 0xff
            out.write("Door_{}_Room_{}_PLM_{}:\n".format(bhex2(door_id), room_address, whex2(plm)))
        elif plm == 0xB703:
            # replace scroll parameter with a label
            params_long = 0x8f0000 + params
            if params_long in modifiedKeys:
                params_label = True
                label = bank_8f[params_long]

        out.write("    ; {}\n".format(plm_name.get(plm, "Unknown PLM")))
        out.write("    {}dw {} : db {} : db {} : dw {} \n".format('; ' if early else '', whex(plm), bhex(x), bhex(y), label if params_label else whex(params)))
    # list ends with 0000
    out.write("    dw $0000\n")

def print_room_header(out, rom, address, length):
    rom.seek(snes_to_pc(address))
    roomIndex = rom.readByte()
    area = rom.readByte()
    mapX = rom.readByte()
    mapY = rom.readByte()
    width = rom.readByte()
    height = rom.readByte()
    upScroller = rom.readByte()
    downScroller = rom.readByte()
    specialGfxBitflag = rom.readByte()
    # in 8f
    doorsPtr = rom.readWord()

    out.write("    db {} ; room index\n".format(bhex(roomIndex)))
    out.write("    db {} ; area\n".format(bhex(area)))
    out.write("    db {} ; map X\n".format(bhex(mapX)))
    out.write("    db {} ; map Y\n".format(bhex(mapY)))
    out.write("    db {} ; width\n".format(bhex(width)))
    out.write("    db {} ; height\n".format(bhex(height)))
    out.write("    db {} ; up scroller\n".format(bhex(upScroller)))
    out.write("    db {} ; down scroller\n".format(bhex(downScroller)))
    out.write("    db {} ; special graphics bitflag\n".format(bhex(specialGfxBitflag)))
    out.write("    dw {} ; doors pointer\n".format(whex(doorsPtr)))

    roomstateTypes = {
        0xE5E6: "Standard",
        0xE612: "Events",
        0xE629: "Bosses",
        0xE5FF: "TourianBoss",
        0xE640: "Morph",
        0xE652: "MorphMissiles",
        0xE669: "PowerBombs",
        0xE676: "SpeedBooster"
    }

    stateType = rom.readWord()
    while roomstateTypes[stateType] != "Standard":
        # handle current room state type
        out.write("    dw {} ; room state {}\n".format(whex(stateType), roomstateTypes[stateType]))

        if roomstateTypes[stateType] in ("Events", "Bosses"):
            event = rom.readByte()
            out.write("    db {} ; event\n".format(bhex(event)))
        ptr = rom.readWord()
        out.write("    dw {} ; room state pointer\n".format(whex(ptr)))

        # get next
        stateType = rom.readWord()
    out.write("    dw {} ; room state standard\n".format(whex(stateType)))

def print_room_state_header(out, rom, address, length, modifiedKeys):
    rom.seek(snes_to_pc(address))
    levelDataPointer = rom.readLong()
    tileset = rom.readByte()
    songSet = rom.readByte()
    playIndex = rom.readByte()
    FXpointer = rom.readWord()
    enemySetpointer = rom.readWord()
    enemyGFXpointer = rom.readWord()
    backgroundXYscrolling = rom.readWord()
    roomScrollspointer = rom.readWord()
    unusedPointer = rom.readWord()
    mainASMpointer = rom.readWord()
    PLMSetPointer = rom.readWord()
    backgroundPointer = rom.readWord()
    setupASMpointer = rom.readWord()

    # replace plm set pointer with a label
    plm_label = False
    PLMSetPointer_long = 0x8f0000 + PLMSetPointer
    if PLMSetPointer_long in modifiedKeys:
        plm_label = True
        label = bank_8f[PLMSetPointer_long]

    out.write("    dl {} ; Level data pointer\n".format(bhex(levelDataPointer)))
    out.write("    db {} ; Tileset\n".format(bhex(tileset)))
    out.write("    db {} ; Song Set\n".format(bhex(songSet)))
    out.write("    db {} ; Play Index\n".format(bhex(playIndex)))
    out.write("    dw {} ; FX pointer\n".format(whex(FXpointer)))
    out.write("    dw {} ; Enemy Set pointer\n".format(whex(enemySetpointer)))
    out.write("    dw {} ; Enemy GFX pointer\n".format(whex(enemyGFXpointer)))
    out.write("    dw {} ; Background X/Y scrolling\n".format(whex(backgroundXYscrolling)))
    out.write("    dw {} ; Room Scrolls pointer\n".format(whex(roomScrollspointer)))
    out.write("    dw {} ; Unused pointer\n".format(whex(unusedPointer)))
    out.write("    dw {} ; Main ASM pointer\n".format(whex(mainASMpointer)))
    out.write("    dw {} ; PLM Set pointer\n".format(label if plm_label else whex(PLMSetPointer)))
    out.write("    dw {} ; Background pointer\n".format(whex(backgroundPointer)))
    out.write("    dw {} ; Setup ASM pointer\n".format(whex(setupASMpointer)))

with open('vanilla.asm', 'w') as v:
    with open('patched.asm', 'w') as p:
        for address in modifiedKeys:
            length = bank8f_len[address]
            label = bank_8f[address]

            v.write("org {}\n".format(bhex(address)))
            p.write("org {}\n".format(bhex(address)))

            room_address = None
            if label.startswith('Room_'):
                room_address = label[5:9]
                room_name = rooms_name.get(room_address, "Unknown Room")
                v.write("; room {}: {}\n".format(room_address, room_name))
                p.write("; room {}: {}\n".format(room_address, room_name))

            if label.startswith('RoomPtr_'):
                room_address = label[8:12]
                room_name = rooms_name.get(room_address, "Unknown Room")
                v.write("; room {}: {}\n".format(room_address, room_name))
                p.write("; room {}: {}\n".format(room_address, room_name))

            v.write("{}:\n".format(label))
            p.write("{}:\n".format(label))

            if label.endswith("PLM"):
                print_plm(v, vanilla, address, length, room_address, modifiedKeys)
                print_plm(p, patched, address, length, room_address, modifiedKeys)
            elif (label.endswith("Header") and "_state_" not in label) or (label.startswith('RoomPtr_')):
                print_room_header(v, vanilla, address, length)
                print_room_header(p, patched, address, length)
            elif label.endswith("Header") and "_state_" in label:
                print_room_state_header(v, vanilla, address, length, modifiedKeys)
                print_room_state_header(p, patched, address, length, modifiedKeys)
            else:
                vanilla.seek(snes_to_pc(address))
                patched.seek(snes_to_pc(address))
                v_data = [bhex(vanilla.readByte()) for _ in range(length)]
                p_data = [bhex(patched.readByte()) for _ in range(length)]
                v.write("    db {}\n".format(','.join(v_data)))

                if label.startswith("FreeSpace_"):
                    if p_data[-1] == '$80':
                        p.write("    ; Scroll data\n")
                    elif p_data[-1] == '$00' and p_data[-2] == '$00':
                        p.write("    ; PLM Set\n")
                        print_plm(p, patched, address, length, room_address, modifiedKeys)
                        continue

                p.write("    db {}\n".format(','.join(p_data)))

print("vanilla.asm and patched.asm generated")
