#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes, RealROM
from rom.ips import IPS_Patch

def writeAsm(binary, outAsm, start, end, chunk):
    print("Writing " + outAsm + "...")
    b=RealROM(binary)
    with open(outAsm, 'w') as f:
        f.write("lorom\narch 65816\n\n")
        addr = start
        eof = lambda: addr >= end
        while not eof():
            f.write("org $%06x\n" % addr)
            f.write("\tdw ")
            for i in range(chunk):
                w = b.readWord()
                if i > 0:
                    f.write(", ")
                f.write("$%04x" % w)
                addr += 2
                if eof():
                    break
            f.write('\n')

b = sys.argv[1]
start = int(sys.argv[2], 16)
end = int(sys.argv[3], 16)
chunk = int(sys.argv[4]) if len(sys.argv) > 4 else 32
outAsm = os.path.splitext(b)[0] + ".asm"
writeAsm(b, outAsm, start, end, chunk)
