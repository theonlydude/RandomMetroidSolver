# from https://github.com/DJuttmann/SM3E/blob/master/SM3E/Tools/Compression.cs
import struct

class Compressor:
    def __init__(self, romFile):
        self.romFile = romFile

    def concatBytes(self, b0, b1):
        return b0 + (b1 << 8)

    def nextByte(self):
        return struct.unpack("B", self.romFile.read(1))[0]

    def decompress(self, address):
        self.romFile.seek(address)

        startAddress = address
        curAddress = address
        output = []

        while curAddress < startAddress + 0x8000:
            currentByte = self.nextByte()
            curAddress += 1

            # End of compressed data
            if currentByte == 0xFF:
                return (curAddress - startAddress, output)

            command = currentByte >> 5
            length = (currentByte & 0b11111) + 1

            while True:
                isLongLength = False

                if command == 0b000:
                    # Copy source bytes
                    for i in range(length):
                        output.append(self.nextByte())
                    curAddress += length

                elif command == 0b001:
                    # Repeat one byte <length> times
                    copyByte = self.nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(copyByte)

                elif command == 0b010:
                    # Alternate between two bytes <length> times
                    copyByte1 = self.nextByte()
                    copyByte2 = self.nextByte()
                    curAddress += 2
                    for i in range(length):
                      output.append(copyByte1 if i % 2 == 0 else copyByte2)

                elif command == 0b011:
                    # Sequence of increasing bytes
                    copyByte = self.nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(copyByte)
                        copyByte += 1

                elif command == 0b100:
                    # Copy from output stream
                    outAddress = self.concatBytes(self.nextByte(), self.nextByte())
                    curAddress += 2

                    for i in range(length):
                        output.append(output[outAddress + i])

                elif command == 0b101:
                    # Copy from output stream, flip bits
                    outAddress = self.concatBytes(self.nextByte(), self.nextByte())
                    curAddress += 2
                    for i in range(length):
                        output.append(output[outAddress + i] ^ 0xFF)

                elif command == 0b110:
                    # Copy from output stream, relative to current index
                    outAddress = len(output) - self.nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(output[outAddress + i])

                elif command == 0b111:
                    # Long length (10 bits) command
                    command = (currentByte >> 2) & 0b111;
                    length = ((currentByte & 0b11) << 8) + self.nextByte() + 1;
                    curAddress += 1

                    if command == 0b111:
                        # Copy output relative to current index, flip bits
                        outAddress = len(output) - self.nextByte()
                        curAddress += 1
                        for i in range(length):
                            output.append(output[outAddress + i] ^ 0xFF)
                    else:
                        isLongLength = True;

                if isLongLength == False:
                    break
