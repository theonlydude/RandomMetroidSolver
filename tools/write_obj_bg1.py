#!/usr/bin/python3

import sys, os, random

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc

rom = sys.argv[1]

char2tile = {
    '.': 0x4A,
    '?': 0x4B,
    '!': 0x4C,
    ' ': 0x00,
    '%': 0x02,
    '*': 0x03,
    '0': 0x04,
    'a': 0x30,
}
for i in range(1, ord('z')-ord('a')+1):
    char2tile[chr(ord('a')+i)] = char2tile['a']+i
for i in range(1, ord('9')-ord('0')+1):
    char2tile[chr(ord('0')+i)] = char2tile['0']+i

lineLength = 64
firstChar = 2 * 2
baseAddr = 0xB6F200 + lineLength * 8 + firstChar

texts = [
    "1. {} kraid",
    "2. {} phantoon",
    "3. {} draygon",
    "4. {} ridley"
]

kill_synonyms = [
    "massacre",
    "slaughter",
    "slay",
    "wipe out",
    "annihilate",
    "eradicate",
    "erase",
    "exterminate",
    "finish",
    "neutralize",
    "obliterate",
    "destroy",
    "wreck",
    "smash",
    "crush",
    "end",
    "eliminate",
    "terminate"
]


romFile = RealROM(sys.argv[1])

alreadyUsed = []
for i, text in enumerate(texts):
    verb = random.choice(kill_synonyms)
    while verb in alreadyUsed:
        verb = random.choice(kill_synonyms)
    alreadyUsed.append(verb)
    text = text.format(verb)
    print(text)
    addr = baseAddr + i * lineLength * 4
    romFile.seek(snes_to_pc(addr))
    for c in text:
        romFile.writeWord(0x3800 + char2tile[c])

romFile.close()


print("text written")
