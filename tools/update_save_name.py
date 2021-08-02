#!/usr/bin/python3

import sys, os
# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))
from rom.rom import RealROM, snes_to_pc

romFileName = sys.argv[1]
romFile = RealROM(romFileName)

# compute tiles for upper and lower letters
# lower chars are made of only one tile
char2tileLower = {'0': 96,
                  'a': 106,
                  '!': 132,
                  '?': 133,
                  '+': 134,
                  '-': 135,
                  '.': 136,
                  ',': 137,
                  '(': 138,
                  ')': 139,
                  ':': 140,
                  ' ': 15}

# add remaining letters/numbers
for i in range(1, ord('z')-ord('a')+1):
    char2tileLower[chr(ord('a')+i)] = char2tileLower['a']+i
for i in range(1, ord('9')-ord('0')+1):
    char2tileLower[chr(ord('0')+i)] = char2tileLower['0']+i

# upper chars are made of two tiles
char2tileUpperUp = {'0': 0, 'a': 10, 'g': 32, 'p': 40, 'x': 64,' ': 15}
char2tileUpperDown = {'0': 16, 'a': 26, 'g': 48, 'p': 56, 'x': 80, ' ': 15}
for i in range(1, ord('9')-ord('0')+1):
    char2tileUpperUp[chr(ord('0')+i)] = char2tileUpperUp['0']+i
    char2tileUpperDown[chr(ord('0')+i)] = char2tileUpperUp['0']+i+16
for i in range(1, ord('f')-ord('a')+1):
    char2tileUpperUp[chr(ord('a')+i)] = char2tileUpperUp['a']+i
    char2tileUpperDown[chr(ord('a')+i)] = char2tileUpperUp['a']+i+16
# there's no letter o
for i in range(1, ord('n')-ord('g')+1):
    char2tileUpperUp[chr(ord('g')+i)] = char2tileUpperUp['g']+i
    char2tileUpperDown[chr(ord('g')+i)] = char2tileUpperUp['g']+i+16
for i in range(1, ord('w')-ord('p')+1):
    char2tileUpperUp[chr(ord('p')+i)] = char2tileUpperUp['p']+i
    char2tileUpperDown[chr(ord('p')+i)] = char2tileUpperUp['p']+i+16
for i in range(1, ord('z')-ord('x')+1):
    char2tileUpperUp[chr(ord('x')+i)] = char2tileUpperUp['x']+i
    char2tileUpperDown[chr(ord('x')+i)] = char2tileUpperUp['x']+i+16
# match with chars in the tile
char2tileUpperUp['9'] = char2tileUpperUp['0']
char2tileUpperUp['f'] = char2tileUpperUp['e']
char2tileUpperUp['g'] = char2tileUpperUp['c']
char2tileUpperUp['o'] = char2tileUpperUp['0']
char2tileUpperUp['p'] = char2tileUpperUp['b']
char2tileUpperUp['q'] = char2tileUpperUp['0']
char2tileUpperUp['r'] = char2tileUpperUp['b']
char2tileUpperUp['v'] = char2tileUpperUp['u']

char2tileUpperDown['i'] = char2tileUpperDown['1']
char2tileUpperDown['o'] = char2tileUpperDown['0']
char2tileUpperDown['t'] = char2tileUpperDown['1']
char2tileUpperDown['u'] = char2tileUpperDown['0']
char2tileUpperDown['y'] = char2tileUpperDown['1']

def updateLowerText(romFile, address, text):
    tileStart = 0x2000
    for char in text:
        romFile.writeWord(tileStart + char2tileLower[char], address)
        address += 2

def updateUpperText(romFile, address, text, vanillaTextLenght):
    tileStart = 0x2000
    # there's a FFFF at the end, each tile is a word
    nextLine = (vanillaTextLenght+1)*2
    for char in text:
        romFile.writeWord(tileStart + char2tileUpperUp[char], address)
        romFile.writeWord(tileStart + char2tileUpperDown[char], address+nextLine)
        address += 2
    # fill remain with space
    for i in range(vanillaTextLenght - len(text)):
        romFile.writeWord(tileStart + char2tileUpperUp[' '], address)
        romFile.writeWord(tileStart + char2tileUpperDown[' '], address+nextLine)
        address += 2

# update 'no data' message
#; NO DATA
#$81:B4AC                000F, 2077, 2078, 200F, 206D, 206A, 207D, 206A, 200F, 200F, 200F, FFFF

# first word is 000F, not an actual char
startAddress = snes_to_pc(0x81B4AC+2)
updateLowerText(romFile, startAddress, 'no dude')

# update 'samus a' message
# ; SAMUS A
# $81:B436                202B, 200A, 2026, 202D, 202B, 200F, 200A, FFFE,
#                         203B, 201A, 2036, 2010, 203B, 200F, 201A, FFFF
startAddress = snes_to_pc(0x81B436)
updateUpperText(romFile, startAddress, 'dude  a', len('samus a'))

# update 'samus data' message
# ; SAMUS DATA
# $81:B40A             dw 202B, 200A, 2026, 202D, 202B, 200F, 200D, 200A, 202C, 200A, FFFE,
#                         203B, 201A, 2036, 2010, 203B, 200F, 201D, 201A, 2011, 201A, FFFF

startAddress = snes_to_pc(0x81B40A)
updateUpperText(romFile, startAddress, 'dude  data', len('samus data'))
