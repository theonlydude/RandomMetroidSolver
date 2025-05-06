#!/usr/bin/python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc
from rom.rompatcher import MusicPatcher,RomTypeForMusic
from utils.parameters import appDir

nspc = open(sys.argv[1], 'rb')
data = nspc.read()
size = len(data)


print(sys.argv[1])

# ; Data format:
# ;     ssss dddd [xx xx...] (data block 0)
# ;     ssss dddd [xx xx...] (data block 1)
# ;     ...
# ;     0000 aaaa
# ; Where:
# ;     s = data block size in bytes
# ;     d = destination address
# ;     x = data
# ;     a = entry address. Ignored by SPC engine after first APU transfer

class Range:
    def __init__(self, low, high, name, canUse):
        self.low = low
        self.high = high
        self.name = name
        self.canUse = canUse

    def inside(self, dataStart, dataLen):
        dataEnd = dataStart + dataLen
        return (dataStart >= self.low and dataStart <= self.high
                or dataEnd >= self.low and dataEnd <= self.high)

class DataBlock:
    def __init__(self, addr, rom):
        self.header = 4
        self.addr = addr
        self.size = rom.readWord(addr)
        self.dest = rom.readWord()
        self.data = rom.readBytes(self.size)

    def getNextBlockAddr(self):
        return self.addr + self.header + self.size

allowUnused = True
ranges = [
    Range(0x0000, 0x14ff, "RAM before SPC Engine", False),
    Range(0x1500, 0x530D, "SPC Engine Code", True),
      Range(0x1500, 0x1cc4, "SPC Engine Code 1", False),
      Range(0x1cc5, 0x1cc7, "SPC Engine Code Total patch 1", True),
      Range(0x1cc8, 0x1e8a, "SPC Engine Code 2", False),
      Range(0x1e8b, 0x1e90, "SPC Engine Code Total patch 2", True),
      Range(0x1e91, 0x530D, "SPC Engine Code 3", False),
    Range(0x530E, 0x56E1, "Shared trackers", False),
      Range(0x530E, 0x546D, "  Music track 1 - Samus fanfare", False),
      Range(0x546E, 0x5568, "  Music track 2 - item fanfare", False),
      Range(0x5569, 0x5696, "  Music track 3 - elevator", False),
      Range(0x5697, 0x56E1, "  Music track 4 - pre-statue hall", False),
    Range(0x56E2, 0x56EF, "Unused", allowUnused),
    Range(0x56F0, 0x5701, "Total Patch Extra RAM", allowUnused),
    Range(0x5702, 0x57FF, "Unused", allowUnused),
    Range(0x5800, 0x5817, "Note length table", True),
      Range(0x5800, 0x5807, "  Note ring length multiplier * 100h", True),
      Range(0x5808, 0x5817, "  Note volume multiplier * 100h", True),
    Range(0x5818, 0x581F, "Unused", allowUnused),
    Range(0x5820, 0x6818, "Tracker data", True),
      Range(0x5820, 0x5827, "  Shared tracker pointers", False),
        Range(0x5820, 0x5821, "    Music track 1 - Samus fanfare", False),
        Range(0x5822, 0x5823, "    Music track 2 - item fanfare", False),
        Range(0x5824, 0x5825, "    Music track 3 - elevator", False),
        Range(0x5826, 0x5827, "    Music track 4 - pre-statue hall", False),
      Range(0x5828, 0x6818, "  Song-specific tracker data", True),
    Range(0x6819, 0x6BFF, "Unused", allowUnused),
    Range(0x6C00, 0x6CE9, "Instrument table", True),
      Range(0x6C00, 0x6C83, "  Shared instruments (0..15h)", False),
      Range(0x6C84, 0x6CE9, "  Song-specific instruments (16h..26h)", True),
    Range(0x6CEA, 0x6CFF, "Unused", allowUnused),
    Range(0x6D00, 0x6D9F, "Sample table", True),
      Range(0x6D00, 0x6D57, "  Shared sample table", False),
      Range(0x6D58, 0x6D9F, "  Song-specific sample table", True),
    Range(0x6DA0, 0x6DFF, "Unused", allowUnused),
    Range(0x6E00, 0xFFFF, "Sample data", True),
      Range(0x6E00, 0xB20F, "  Shared sample data", False),
      Range(0xB210, 0xFFFF, "  Song-specific sample data", True)
]

rom = RealROM(sys.argv[1])

dataBlocks = []
addr = 0
while size - addr > 4:
    dataBlock = DataBlock(addr, rom)
    if dataBlock.size == 0:
        break
    print("datablock addr: {} size: {} dest: {}".format(dataBlock.addr, dataBlock.size, hex(dataBlock.dest)))
    dataBlocks.append(dataBlock)
    addr = dataBlock.getNextBlockAddr()
    #print("next addr: {}".format(addr))

print("found {} data blocks".format(len(dataBlocks)))
print("last addr: {} last bytes: {}".format(addr, data[addr:]))

endBytes = 4
dataBlocksSize = sum([d.size + d.header for d in dataBlocks]) + endBytes
if dataBlocksSize == size:
    print("  OK size is a match: {}".format(size))
else:
    print("  WARNING size mismatch !! dbSize: {} fileSize: {}".format(dataBlocksSize, size))

# check where music data is sent in the spc
violation = False
for i, dataBlock in enumerate(dataBlocks):
    for _range in ranges:
        if _range.inside(dataBlock.dest, dataBlock.size):
            print("data block {} is inside {}".format(i, _range.name))
            if not _range.canUse:
                print("  CRITICAL write in forbidden SPC memory. data [$%04x - $%04x] memory: [$%04x - $%04x]" % (dataBlock.dest, dataBlock.dest+dataBlock.size, _range.low, _range.high))
                violation = True


if violation:
    print("  CRITICAL memory violation for {}".format(sys.argv[1]))
    sys.exit(1)
else:
    print("  OK no memory violation")
    sys.exit(0)
