#!/usr/bin/python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# extract vanilla soundtrack as nspc files. args:
# - vanilla ROM
# - path to nspc directory 
# - path to JSON metadata file to write

from rom.rom import RealROM, snes_to_pc

vanilla=sys.argv[1]
nspc_dir=sys.argv[2]
json_path=sys.argv[3]

rom=RealROM(vanilla)
musicDataTable = snes_to_pc(0x8FE7E4)
musicDataEnd = snes_to_pc(0xDED1C0)
# tracks pointed  music table, in that order
# array is songs in music data 
vanillaMusicData = [
    # Song 0: intro,
    # Song 1: menu theme
    ["Title sequence intro", "Menu theme"],
    # Song 0: thunder - zebes asleep,
    # Song 1: thunder - zebes awake,
    # Song 2: no thunder (morph room...)
    ["Crateria Landing - Thunder, Zebes asleep", "Crateria Landing - Thunder, Zebes awake", "Crateria Landing - No Thunder"],
    # Song 0: Main theme,
    # Song 1: Tourian Entrance
    ["Crateria Pirates", "Tourian Entrance"],
    # Song 0: Upper Crateria with PBs/outside Wrecked Ship
    ["Samus Theme"],
    ["Green Brinstar"],
    ["Red Brinstar"],
    ["Upper Norfair"],
    ["Lower Norfair"],
    # Song 0: East Maridia, Song 1: West Maridia
    ["East Maridia", "West Maridia"],
    # Song 0: Tourian, Song 1: no music
    ["Tourian"],
    ["Mother Brain"],
    # Song 0: BT/Ridley/Draygon,
    # Song 1: BT tension,
    # Song 2: Escape
    ["Boss fight - BT/Ridley/Draygon", "Boss fight - BT tension"],
    # Song 0: Kraid/Phantoon/Croc,
    # Song 1: Tension
    ["Boss fight - Kraid/Phantoon/Croc", "Boss fight - Kraid/Phantoon/Croc tension"],
    # Song 0: Spore Spawn/Botwoon
    ["Boss fight - Spore Spawn/Botwoon"],
    # Song 0: Flying to Ceres,
    # Song 1: Ceres,
    # Song 2: Flying to Zebes,
    # Song 3: Ceres time up
    ["Flying to Ceres", "Ceres", "Flying to Zebes", "Ceres time up"],
    # Song 0: Power off,
    # Song 1: Power on
    ["Wrecked Ship - Power off", "Wrecked Ship - Power on"],
    ["Zebes boom"],
    ["Intro"],
    ["Death"],
    ["Credits"],
    ["The last Metroid is in captivity"],
    ["The galaxy is at peace"],
    # Song 0: Boss music,
    # Song 1: Pre-boss music,
    # Song 2: No music
    ["Baby Metroid", "Baby Metroid - Tension", "Baby Metroid - No music"],
    ["Mother Brain 3 (Samus Theme 2)"]
]

metadata = {}

for i in range(len(vanillaMusicData)):
    addr = musicDataTable+i*3
    ptr = snes_to_pc(rom.readLong(addr))
    if i < len(vanillaMusicData)-1:
        # vanilla data ptrs are conveniently sorted
        endptr = snes_to_pc(rom.readLong(addr+3))
    else:
        endptr = musicDataEnd
    rom.seek(addr)
    nspc_path = "%s/vanilla_%06x_%06x.nspc" % (nspc_dir, ptr, endptr-1)
    print("Writing %s ..." % nspc_path)
    with open(nspc_path, "wb") as nspc:
        nspc.write(rom.read(endptr-ptr))
    musicdata = vanillaMusicData[i]
    for j in range(len(musicdata)):
        track = musicdata[j]
        metadata[track] = {
            'nspc_path':nspc_path,
            'track_index':j,
            'original_author':'Kenji Yamamoto',
            'port_author': '',
            'description': "Original track from vanilla Super Metroid"
        }

print("Writing %s ..." % json_path)
with open(json_path, 'w') as fp:
    json.dump(metadata, fp, indent=4)
