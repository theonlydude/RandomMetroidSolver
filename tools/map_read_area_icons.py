#!/usr/bin/python3

import sys, os, json

sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc

rom = RealROM(sys.argv[1])

area_icon_data = {
    "Crateria": (0x82c759, ["Brinstar Left", "Brinstar Middle", "Brinstar Right", "Wrecked Ship", "Maridia"]),
    "Brinstar": (0x82c779, ["Crateria Left", "Crateria Middle", "Crateria Right", "Maridia", "Norfair"]),
    "Norfair": (0x82c799, ["Brinstar"]),
    "Maridia": (0x82c7af, ["Crateria", "Brinstar Left", "Brinstar Right"])
}

for area, areaData in area_icon_data.items():
    addr, icons = areaData
    rom.seek(snes_to_pc(addr))
    print(f'''"{area}": {{
    "addr": 0x{addr:0>6x},
    "icons": {{''')
    for icon in icons:
        x, y, t = rom.readWord(), rom.readWord(), rom.readWord()
        print(f'        "{icon}": {{"x": {x}, "y": {y}, "type": 0x{t:x}}},')
    print("    },")
    print("},")
