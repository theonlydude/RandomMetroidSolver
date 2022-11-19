#!/usr/bin/env python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes, snes_to_pc, RealROM

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
                room_addr = snes_to_pc((0x8f << 16) | toWord(bytes[0], bytes[1]))
                # read room size in screens
                mirror.seek(room_addr + 4)
                swidth = mirror.readByte()
                sheight = mirror.readByte()
                # a screen is 256 pixels long
                pwidth = swidth * 256

                # in pixel from top left of the room
                vanilla_save_x = toWord(bytes[6], bytes[7])
                mirror_save_x = pwidth - 256 - vanilla_save_x
                # in pixel from top left of the screen
                vanilla_samus_x = toWord(bytes[10], bytes[11])
                mirror_samus_x = 256 - vanilla_samus_x
                bytes[6], bytes[7] = toBytes(mirror_save_x)
                bytes[10], bytes[11] = toBytes(mirror_samus_x)
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

print("additional_PLMs = {")
for name, data in additional_PLMs.items():
    print("    '{}': {{".format(name))

    room_addr = snes_to_pc(0x8f0000 | data['room'])
    plm_bytes_list = data['plm_bytes_list'][0]

    # get room width to compute new door x
    mirror.seek(room_addr + 4)
    swidth = mirror.readByte()
    sheight = mirror.readByte()

    vanilla_door_x = plm_bytes_list[2]
    mirror_door_x = (swidth * 16) - 1 - vanilla_door_x
    plm_bytes_list[2] = mirror_door_x

    # plms are one tile lower than expected...
    vanilla_door_y = plm_bytes_list[3]
    plm_bytes_list[3] = vanilla_door_y - 1


    # change plm facing for bliking grey door
    if plm_bytes_list[1] == 0xc8:
        if plm_bytes_list[0] == 0x42:
            plm_bytes_list[0] = 0x48
        elif plm_bytes_list[0] == 0x48:
            plm_bytes_list[0] = 0x42
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
