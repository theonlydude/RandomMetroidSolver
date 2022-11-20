#!/usr/bin/env python3

# prereq:
# start with bank_83.asm from total's banklog parser.
# replace comments with labels. 
# compile it with asar with wla symbols export in sm.sym_wla
# echo "bank_83 = {" > bank83_addresses.py
# grep -E '^83:' sm.sym_wla | sed -e 's+^83:\([0-9A-Z]*\) \(.*\)$+0x83\1: "\2",+' | sort >> bank83_addresses.py
# echo "}" >> bank83_addresses.py
# mv bank83_addresses.py ~/RandomMetroidSolver/rom/

import sys, os
from collections import defaultdict

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from patches.vanilla.sym.reverse.bank83_addresses import bank_83
from rom.ips import IPS_Patch
from rom.rom import pc_to_snes, snes_to_pc, RealROM
from tools.rooms import rooms

def gen_bank83_map(bank83, patched):
    # generate a big dict telling for each byte in which vanilla section it is
    bank83_map = {}
    # also tell the length of each label data
    bank83_len = {}

    prev_address = -1
    for address in bank83.keys():
        # fill remaining of previous address
        #print("set {} to [{} - {}]".format(hex(prev_address), hex(prev_address), hex(address - 1)))
        for i in range(prev_address, address):
            bank83_map[i] = prev_address
        prev_address = address

    prev_address = None
    for address in bank83.keys():
        if prev_address is not None:
            length = address - prev_address
            bank83_len[prev_address] = length
        prev_address = address

    # search for non 0xff in free space
    freespace_start = prev_address
    patched.seek(snes_to_pc(freespace_start))
    freespace = [patched.readByte() for _ in range(0x83ffff - freespace_start + 1)]
    count = 0
    in_data = False
    cur_label = None
    for i, byte in enumerate(freespace):
        if byte == 0xff:
            if in_data:
                # add lenght of previous non free segment
                length = freespace_start + i - prev_address
                bank83_len[prev_address] = length
            in_data = False
            bank83_map[freespace_start + i] = -1
        elif not in_data:
            # add new label
            in_data = True
            cur_label = "FreeSpace_{}".format(bhex2(count))
            count += 1
            bank83[freespace_start + i] = cur_label
            prev_address = freespace_start + i
            bank83_map[freespace_start + i] = prev_address
        else:
            bank83_map[freespace_start + i] = prev_address
    if in_data:
        # if data goes up to the end of the bank
        bank83_len[prev_address] = 0x83ffff - prev_address

    return (bank83_map, bank83_len)

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

(bank83_map, bank83_len) = gen_bank83_map(bank_83, patched)

rooms_name = { hex(d["Address"] & 0xFFFF)[2:].upper(): d["Name"] for d in rooms}

# get all addresses modified by the patch
modified = defaultdict(int)
ranges = defaultdict(set)
for r in ips.getRanges():
    # keep only bank 83
    if r.start < snes_to_pc(0x838000) or r.stop > snes_to_pc(0x83ffff):
        continue
    for i in r:
        address = bank83_map[pc_to_snes(i)]
        if address != -1:
            modified[address] += 1
            ranges[address].add(r)

print("patch {} has modifications in bank 83:".format(patch))
print("")
print("Address  | Bytes | Label")
print("-"*128)
modifiedKeys = sorted(list(modified.keys()))
for address in modifiedKeys:
    print("{} | {:>5} | {} | {}".format(hex(address), modified[address], bank_83[address], ["[{}-{}]".format(hex(pc_to_snes(r.start)), hex(pc_to_snes(r.stop))) for r in sorted(ranges[address], key=lambda x: x.start)]))

def print_fx(out, rom, address):
    rom.seek(snes_to_pc(address))

    Doorpointer = rom.readWord()
    if Doorpointer == 0xffff:
        out.write("    dw {} ; no FX\n".format(whex(Doorpointer)))
        return

    BaseYposition = rom.readWord()
    TargetYposition = rom.readWord()
    Yvelocity = rom.readWord()
    Timer = rom.readByte()
    Type = rom.readByte()
    DefaultLayerBlendingConf = rom.readByte()
    FXlayer3layerBlendingConf = rom.readByte()
    FXliquidOptions = rom.readByte()
    PaletteFXbitset = rom.readByte()
    AnimatedTilesBitset = rom.readByte()
    PaletteBlend = rom.readByte()

    out.write("    dw {} ; Door pointer\n".format(whex(Doorpointer)))
    out.write("    dw {} ; Base Y position\n".format(whex(BaseYposition)))
    out.write("    dw {} ; Target Y position\n".format(whex(TargetYposition)))
    out.write("    dw {} ; Y velocity\n".format(whex(Yvelocity)))
    out.write("    db {} ; Timer\n".format(bhex(Timer)))
    out.write("    db {} ; Type (foreground layer 3)\n".format(bhex(Type)))
    out.write("    db {} ; Default layer blending configuration (FX A)\n".format(bhex(DefaultLayerBlendingConf)))
    out.write("    db {} ; FX layer 3 layer blending configuration (FX B)\n".format(bhex(FXlayer3layerBlendingConf)))
    out.write("    db {} ; FX liquid options (FX C)\n".format(bhex(FXliquidOptions)))
    out.write("    db {} ; Palette FX bitset\n".format(bhex(PaletteFXbitset)))
    out.write("    db {} ; Animated tiles bitset\n".format(bhex(AnimatedTilesBitset)))
    out.write("    db {} ; Palette blend\n".format(bhex(PaletteBlend)))

def print_door(out, rom, address, rooms_name):
    rom.seek(snes_to_pc(address))

    DestinationRoomHeaderPointer = rom.readWord()
    BitFlag = rom.readByte()
    Direction = rom.readByte()
    XposLow = rom.readByte()
    YPosLow = rom.readByte()
    XPosHigh = rom.readByte()
    YPosHigh = rom.readByte()
    DistanceFromDoor = rom.readWord()
    CustomDoorASM = rom.readWord()

    out.write("    dw {} ; Destination room header pointer (bank $8F): {}\n".format(whex(DestinationRoomHeaderPointer), rooms_name.get(hex(DestinationRoomHeaderPointer)[2:].upper(), "Unknown Room")))
    out.write("    db {} ; Bit Flag (Elevator properties)\n".format(bhex(BitFlag)))
    out.write("    db {} ; Direction\n".format(bhex(Direction)))
    out.write("    db {} ; X cap\n".format(bhex(XposLow)))
    out.write("    db {} ; Y cap\n".format(bhex(YPosLow)))
    out.write("    db {} ; X screen\n".format(bhex(XPosHigh)))
    out.write("    db {} ; Y screen\n".format(bhex(YPosHigh)))
    out.write("    dw {} ; Distance from door to spawn Samus\n".format(whex(DistanceFromDoor)))
    out.write("    dw {} ; Custom door ASM to execute (bank $8F)\n".format(whex(CustomDoorASM)))

with open('vanilla.asm', 'w') as v:
    with open('patched.asm', 'w') as p:
        for address in modifiedKeys:
            length = bank83_len[address]
            label = bank_83[address]

            v.write("org {}\n".format(bhex(address)))
            p.write("org {}\n".format(bhex(address)))

            room_address = None
            if label.startswith('Room_'):
                room_address = label[5:9]
                room_name = rooms_name.get(room_address, "Unknown Room")
                v.write("; room {}: {}\n".format(room_address, room_name))
                p.write("; room {}: {}\n".format(room_address, room_name))

            v.write("{}:\n".format(label))
            p.write("{}:\n".format(label))

            if label.endswith("FX"):
                print_fx(v, vanilla, address)
                print_fx(p, patched, address)
            elif label.endswith("Door") and "_door_list_index_" in label:
                print_door(v, vanilla, address, rooms_name)
                print_door(p, patched, address, rooms_name)
            else:
                vanilla.seek(snes_to_pc(address))
                patched.seek(snes_to_pc(address))
                v_data = [bhex(vanilla.readByte()) for _ in range(length)]
                p_data = [bhex(patched.readByte()) for _ in range(length)]
                v.write("    db {}\n".format(','.join(v_data)))
                p.write("    db {}\n".format(','.join(p_data)))

print("vanilla.asm and patched.asm generated")
