#!/usr/bin/env python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))
sys.path.insert(0, os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes, snes_to_pc, RealROM
from utils.doorsmanager import DoorsManager, Facing
from logic.logic import Logic
from rom.addresses import Addresses
from rom.symbols import Symbols
from patches.patchaccess import PatchAccess

def toWord(b1, b2):
    return (b2 << 8) | b1
def toBytes(w):
    return ((w & 0xff), ((w & 0xff00) >> 8))

mirror = RealROM(sys.argv[1])

# load vanilla door addresses
with open('patches/vanilla/sym/bank_8f.json', 'r') as f:
    vanilla_door_labels = json.load(f)
vanilla_door_addresses = {a: l[:-4] for l,a in vanilla_door_labels.items() if l.startswith('Door_')}

# load mirror door addresses
with open('patches/mirror/sym/bank_8f.json', 'r') as f:
    mirror_door_labels = json.load(f)
mirror_door_labels = {l[:-4]: a for l,a in mirror_door_labels.items() if l.startswith('Door_')}

# load vanilla doors patches
from patches.vanilla.patches import patches, additional_PLMs

print("from rom.rom import snes_to_pc")
print("")
print("patches = {")
for name, data in patches.items():
    print("    '{}': {{".format(name))
    if name.startswith('Blinking') or name.startswith('Indicator'):
        for pc_addr, bytes in data.items():
            snes_addr = pc_to_snes(pc_addr)
            bank = snes_addr >> 16
            if bank == 0x8f:
                # it's a door PLM, find its label
                if snes_addr in vanilla_door_addresses:
                    label = vanilla_door_addresses[snes_addr]
                    mirror_snes_addr = mirror_door_labels[label]
                    # read plm x,y from mirror
                    mirror.seek(snes_to_pc(mirror_snes_addr) + 2)
                    x = mirror.readByte()
                    y = mirror.readByte()
                    bytes[2] = x
                    bytes[3] = y

                    # change plm facing for bliking grey door
                    if bytes[1] == 0xc8:
                        if bytes[0] == 0x42:
                            bytes[0] = 0x48
                        elif bytes[0] == 0x48:
                            bytes[0] = 0x42

                    print("        # door {} x/y updated".format(label))
                    print("        snes_to_pc({}): [{}],".format(hex(mirror_snes_addr), ', '.join([hex(b) for b in bytes])))
                else:
                    print("        snes_to_pc({}): [{}], # can't find door address".format(hex(snes_addr), ', '.join([hex(b) for b in bytes])))
            else:
                print("        snes_to_pc({}): [{}],".format(hex(snes_addr), ', '.join([hex(b) for b in bytes])))
    elif name.startswith('Save_'):
        for pc_addr, bytes in data.items():
            snes_addr = pc_to_snes(pc_addr)
            bank = snes_addr >> 16
            # load point in 0x80
            if bank == 0x80:
                print("        # {} load point entry - x/y updated".format(hex(snes_addr)))
                room_ptr = toWord(bytes[0], bytes[1])
                door_ptr = toWord(bytes[2], bytes[3])
                door_bts = toWord(bytes[4], bytes[5])
                screenX = toWord(bytes[6], bytes[7])
                screenY = toWord(bytes[8], bytes[9])
                samusYoffset = toWord(bytes[10], bytes[11]) # relative to screen top
                samusXoffset = toWord(bytes[12], bytes[13]) # relative to screen center

                room_addr = snes_to_pc((0x8f << 16) | room_ptr)
                # read room size in screens
                mirror.seek(room_addr + 4)
                swidth = mirror.readByte()
                sheight = mirror.readByte()
                # a screen is 256 pixels long
                pwidth = swidth * 256

                # in pixel from top left of the room
                vanilla_save_x = screenX
                mirror_save_x = pwidth - 256 - vanilla_save_x
                # in pixel from top center of the screen
                vanilla_samus_x = samusXoffset
                # 2 complement
                mirror_samus_x = ((~vanilla_samus_x)+1) & 0xffff
                bytes[6], bytes[7] = toBytes(mirror_save_x)
                bytes[12], bytes[13] = toBytes(mirror_samus_x)
                print("        snes_to_pc({}): [{}],".format(hex(snes_addr), ', '.join([hex(b) for b in bytes])))
            # music in 0x8f
            elif bank == 0x8f:
                print("        # music in room state header")
                print("        snes_to_pc({}): [{}],".format(hex(snes_addr), ', '.join([hex(b) for b in bytes])))
            # map icon x/y in 0x82
            elif bank == 0x82:
                print("        # TODO map icon X/Y")
                print("        snes_to_pc({}): [{}],".format(hex(snes_addr), ', '.join([hex(b) for b in bytes])))

    print("    },")
print("}")

print("")

Logic.factory('mirror')
symbols = Symbols(PatchAccess())
symbols.loadAllSymbols()
Addresses.updateFromSymbols(symbols)
doorsManager = DoorsManager()
doorsManager.setDoorsAddress(symbols)

print("additional_PLMs = {")
for name, data in additional_PLMs.items():
    print("    '{}': {{".format(name))

    room_addr = snes_to_pc(0x8f0000 | data['room'])
    plm_bytes_list = data['plm_bytes_list'][0]

    # get room width to compute new door x
    mirror.seek(room_addr + 4)
    swidth = mirror.readByte()
    sheight = mirror.readByte()

    # change plm facing for bliking grey door
    door_length = 1
    if plm_bytes_list[1] == 0xc8:
        if plm_bytes_list[0] == 0x42:
            plm_bytes_list[0] = 0x48
        elif plm_bytes_list[0] == 0x48:
            plm_bytes_list[0] = 0x42
        else:
            door_length = 4
    elif plm_bytes_list[0] == 0x6f and plm_bytes_list[1] == 0xb7:
        # save station is two tiles long
        door_length = 2
    elif plm_bytes_list[0] == 0xff and plm_bytes_list[1] == 0xff and name.startswith('Indicator'):
        door_name = name[len('Indicator['):-1]
        door = doorsManager.doors[door_name]
        if door.facing in (Facing.Left, Facing.Right):
            door_length = 1
        else:
            door_length = 4

    vanilla_door_x = plm_bytes_list[2]
    mirror_door_x = (swidth * 16) - door_length - vanilla_door_x
    plm_bytes_list[2] = mirror_door_x


    print("        'room': {},".format(hex(data['room'])))
    if 'state' in data:
        print("        'state': {},".format(hex(data['state'])))
    print("        'plm_bytes_list': [")
    print("            [{}],".format(', '.join([hex(b) for b in plm_bytes_list])))
    print("        ],")
    if 'locations' in data:
        print("        'locations': {},".format(data['locations']))
    print("    },")
print("}")
