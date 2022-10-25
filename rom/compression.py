# from https://github.com/DJuttmann/SM3E/blob/master/SM3E/Tools/Compression.cs
import logging
import utils.log
from enum import IntEnum
from collections import defaultdict

class Command(IntEnum):
    DirectCopy = 0b000
    ByteFill = 0b001
    WordFill = 0b010
    SigmaFill = 0b011
    LibraryCopy = 0b100
    EORedCopy = 0b101
    MinusCopy = 0b110
    EORedMinusCopy = 0b111
    Long = 0b111
    End = 0xff

# profile:
#  Fast: fastest but sometimes bigger than vanilla
#  Slow: most compression, guaranteed smaller than vanilla
class Compressor:
    def __init__(self, profile='Fast'):
        self.log = utils.log.get('Compressor')
        self.profile = profile
        # for debug purpose
        self.stats = defaultdict(int)

    def _concatBytes(self, b0, b1):
        return b0 + (b1 << 8)

    def _nextByte(self):
        return self.romFile.readByte()

    def decompress(self, romFile, address):
        self.romFile = romFile
        self.romFile.seek(address)

        startAddress = address
        curAddress = address
        output = []

        while curAddress < startAddress + 0x8000:
            curByte = self._nextByte()
            curAddress += 1

            # End of compressed data
            if curByte == Command.End:
                return (curAddress - startAddress, output)

            command = curByte >> 5
            length = (curByte & 0b11111) + 1

            if self.log.getEffectiveLevel() == logging.DEBUG:
                self.log.debug("@: {} curByte: {} cmd: {} len: {}".format(curAddress-startAddress-1, curByte, bin(command), length))
                self.stats[command] += length

            while True:
                isLongLength = False

                if command == Command.DirectCopy:
                    # Copy source bytes
                    for i in range(length):
                        output.append(self._nextByte())
                    curAddress += length
                    if self.log.getEffectiveLevel() == logging.DEBUG:
                        self.log.debug("Uncompressed: {}".format(output[-length:]))

                elif command == Command.ByteFill:
                    # Repeat one byte <length> times
                    copyByte = self._nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(copyByte)
                    if self.log.getEffectiveLevel() == logging.DEBUG:
                        self.log.debug("Repeat: {}".format(output[-length:]))

                elif command == Command.WordFill:
                    # Alternate between two bytes <length> times
                    copyByte1 = self._nextByte()
                    copyByte2 = self._nextByte()
                    curAddress += 2
                    for i in range(length):
                      output.append(copyByte1 if i % 2 == 0 else copyByte2)
                    if self.log.getEffectiveLevel() == logging.DEBUG:
                        self.log.debug("Word: {}".format(output[-length:]))

                elif command == Command.SigmaFill:
                    # Sequence of increasing bytes
                    copyByte = self._nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(copyByte)
                        copyByte += 1
                    if self.log.getEffectiveLevel() == logging.DEBUG:
                        self.log.debug("Increment: {}".format(output[-length:]))

                elif command == Command.LibraryCopy:
                    # Copy from output stream
                    outAddress = self._concatBytes(self._nextByte(), self._nextByte())
                    curAddress += 2
                    for i in range(length):
                        output.append(output[outAddress + i])
                    if self.log.getEffectiveLevel() == logging.DEBUG:
                        self.log.debug("Copy: {}".format(output[-length:]))

                elif command == Command.EORedCopy:
                    # Copy from output stream, flip bits
                    outAddress = self._concatBytes(self._nextByte(), self._nextByte())
                    curAddress += 2
                    for i in range(length):
                        output.append(output[outAddress + i] ^ 0xFF)
                    if self.log.getEffectiveLevel() == logging.DEBUG:
                        self.log.debug("CopyXOR: {}".format(output[-length:]))

                elif command == Command.MinusCopy:
                    # Copy from output stream, relative to current index
                    outAddress = len(output) - self._nextByte()
                    curAddress += 1
                    for i in range(length):
                        output.append(output[outAddress + i])
                    if self.log.getEffectiveLevel() == logging.DEBUG:
                        self.log.debug("RelativeCopy: {}".format(output[-length:]))

                elif command == Command.Long:
                    # Long length (10 bits) command
                    command = (curByte >> 2) & 0b111;
                    length = ((curByte & 0b11) << 8) + self._nextByte() + 1;
                    curAddress += 1
                    self.log.debug("Long command")

                    if command == Command.EORedMinusCopy:
                        # Copy output relative to current index, flip bits
                        outAddress = len(output) - self._nextByte()
                        curAddress += 1
                        for i in range(length):
                            output.append(output[outAddress + i] ^ 0xFF)
                        if self.log.getEffectiveLevel() == logging.DEBUG:
                            self.log.debug("LongRelativeCopyXOR: {}".format(output[-length:]))
                    else:
                        isLongLength = True;

                if isLongLength == False:
                    break


    def compress(self, inputData):
        # compress the data in input array, return array of compressed bytes
        self.inputData = inputData
        self.length = len(self.inputData)
        self.output = []

        self._computeStart()

        # to use a command it must replace 4 bytes of input data, else just copy uncompressed
        min_length = 4

        i = 0
        while i < self.length:
            value = self.inputData[i]
            lengths = self._computeNext(i)
            length, command = lengths['best']

            if length < min_length:
                j = i+1
                while j < self.length and length < min_length:
                    lengths = self._computeNext(j)
                    length = lengths['best'][0]
                    j += 1
                length = j - i if j == self.length else j - i - 1
                self._writeUncompressed(i, length)

            elif command == Command.ByteFill:
                length = min(length, 1024)
                self._writeByteFill(value, length)

            elif command == Command.WordFill:
                length = min(length, 1024)
                self._writeWordFill(value, self.inputData[i+1], length)

            elif command == Command.SigmaFill:
                length = min(length, 1024)
                self._writeByteIncrement(value, length)

            elif command == Command.LibraryCopy:
                length = min(length, 1024)
                address = lengths[Command.LibraryCopy][1]
                if i - address < 0xFF:
                    self._writeNegativeCopy(i, i - address, length)
                else:
                    self._writeCopy(address, length)

            elif command == Command.EORedCopy:
                length = min(length, 1024)
                address = lengths[Command.EORedCopy][1]
                if i - address < 0xFF:
                    self._writeNegativeCopyXor(i, i - address, length)
                else:
                    self._writeCopyXor(address, length)

            i += length

        # end of compressed data marker
        self.output.append(Command.End)

        if len(self.output) > len(inputData):
            print("WARNING !!! len compressed {} > original data {}".format(len(self.output), len(inputData)))
            print("original: {}".format(inputData))
            print("compressed: {}".format(self.output))

        return self.output[:]

    def _writeChunkHeader(self, type, length):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.stats[type] += length

        length -= 1
        if length < 32 and type != Command.EORedMinusCopy:
            # regular command
            self.output.append(type << 5 | length)
            if self.log.getEffectiveLevel() == logging.DEBUG:
                self.log.debug("_writeChunkHeader: cmd: {} len: {} value: {}".format(bin(type), length, type << 5 | length))
        else:
            # long command or relative xor copy
            self.output.append(0b11100000 | type << 2 | length >> 8)
            self.output.append(length & 0xFF)
            if self.log.getEffectiveLevel() == logging.DEBUG:
                self.log.debug("_writeChunkHeader: long cmd: {} len: {} value: {} {}".format(bin(type), length, 0b11100000 | type << 2 | length >> 8, length & 0xFF))

    def _writeUncompressed(self, index, length):
        self._writeChunkHeader(Command.DirectCopy, length)
        self.output += self.inputData[index:index+length]
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeUncompressed: len: {} index: {} data: {}".format(length, index, self.inputData[index:index+length]))

    def _writeByteFill(self, byte, length):
        self._writeChunkHeader(Command.ByteFill, length)
        self.output.append(byte)
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeByteFill: len: {} byte: {}: {}".format(length, byte, [byte for i in range(length)]))

    def _writeWordFill(self, b0, b1, length):
        self._writeChunkHeader(Command.WordFill, length)
        self.output.append(b0)
        self.output.append(b1)
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeWordFill: len: {} b0: {} b1: {}: {}".format(length, b0, b1, [b0 if i%2==0 else b1 for i in range(length)]))

    def _writeByteIncrement(self, byte, length):
        self._writeChunkHeader(Command.SigmaFill, length)
        self.output.append(byte)
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeByteIncrement: len: {} byte: {}: {}".format(length, byte, [byte+i for i in range(length)]))

    def _writeCopy(self, address, length):
        self._writeChunkHeader(Command.LibraryCopy, length)
        self.output.append(address & 0xFF)
        self.output.append(address >> 8)
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeCopy: {}".format(self.output[-3:]))
            self.log.debug("_writeCopy: len: {} address: {}: {}".format(length, address, self.inputData[address:address+length]))

    def _writeCopyXor(self, address, length):
        self._writeChunkHeader(Command.EORedCopy, length)
        self.output.append(address & 0xFF)
        self.output.append(address >> 8)
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeCopyXor: {}".format(self.output[-3:]))
            self.log.debug("_writeCopyXor: len: {} address: {}: {}".format(length, address, self.inputData[address:address+length]))

    def _writeNegativeCopy(self, i, address, length):
        self._writeChunkHeader(Command.MinusCopy, length)
        self.output.append(address)
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeNegativeCopy: len: {} address: {}: {}".format(length, address, self.inputData[i-address:i-address+length]))

    def _writeNegativeCopyXor(self, i, address, length):
        self._writeChunkHeader(Command.EORedMinusCopy, length)
        self.output.append(address)
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("_writeNegativeCopy: len: {} address: {}: {}".format(length, address, self.inputData[i-address:i-address+length]))

    def _computeStart(self):
        # for each possible value store the positions of the value in the input data
        self.start = defaultdict(list)
        for i in range(self.length-1):
            self.start[self.inputData[i]].append(i)

        if self.profile == 'Slow':
            return

        settings = {
            'Fast': {
                'length': 256,
                'step': 64
            }
        }

        # remove too close values
        min_length = self.length / settings[self.profile]['length']
        min_step = self.length / settings[self.profile]['step']
        for k, l in self.start.items():
            line_lenght = len(l)
            if line_lenght <= min_length:
                continue
            filtered = []
            i = 0
            j = 1
            filtered.append(l[i])
            while j < line_lenght:
                while j<line_lenght-1 and l[j] - l[i] < min_step:
                    j += 1
                filtered.append(l[j])
                i = j
                j=i+1
            self.start[k] = filtered

    def _computeNext(self, pos):
        ret = {}
        bestLength = 0
        bestCommand = 0

        length = self._computeByteFill(pos)
        ret[Command.ByteFill] = length
        if length > bestLength:
            bestLength = length
            bestCommand = Command.ByteFill

        length = self._computeWordFill(pos)
        ret[Command.WordFill] = length
        if length > bestLength:
            bestLength = length
            bestCommand = Command.WordFill

        length = self._computeByteIncrement(pos)
        ret[Command.SigmaFill] = length
        if length > bestLength:
            bestLength = length
            bestCommand = Command.SigmaFill

        (length, address) = self._computeCopy(pos)
        ret[Command.LibraryCopy] = (length, address)
        if length > bestLength:
            bestLength = length
            bestCommand = Command.LibraryCopy

        (length, address) = self._computeCopy(pos, 0xff)
        ret[Command.EORedCopy] = (length, address)
        if length > bestLength:
            bestLength = length
            bestCommand = Command.EORedCopy

        ret["best"] = (bestLength, bestCommand)

        return ret

    def _computeByteFill(self, pos):
        carry = 0
        i = pos
        value = self.inputData[i]
        # count how many repeating value we have
        while i + carry < self.length and self.inputData[i + carry] == value:
            carry += 1
        return carry

    def _computeWordFill(self, pos):
        if pos+1 >= self.length:
            return 0

        i = pos
        carry = 1
        value = (self.inputData[i], self.inputData[i+1])
        while i + carry < self.length and self.inputData[i + carry] == value[carry & 1]:
            carry += 1
        return carry

    def _computeByteIncrement(self, pos):
        carry = 0
        i = pos
        value = self.inputData[i]
        while i + carry < self.length and self.inputData[i + carry] == value:
            carry += 1
            value += 1
        return carry

    def _computeCopy(self, pos, xor=0x00):
        value = self.inputData[pos] ^ xor
        maxLength = 0
        maxAddress = -1
        for j, address in enumerate(self.start[value], start=0):
            # only in previous addresses
            if address >= pos:
                break
            length = self._matchSubSequences(address, pos, xor)
            if length > maxLength:
                maxLength = length
                maxAddress = address
        #self.log.debug("i: {} cc addr: {} len: {} data: {}".format(i, maxAddress, maxLength, inputData[i:i+maxLength]))
        return (maxLength, maxAddress)

    # Find the max length of two matching sequences starting at a and b in Input array.
    def _matchSubSequences(self, a, b, xor):
        i = 0
        last_equal = True
        # max data in chunk is 1024 bytes in long commands
        max_search = self.length-b if self.length-b < 1024 else 1024
        for i in range(max_search):
            if (self.inputData[a+i] ^ xor) != self.inputData[b+i]:
                last_equal = False
                break
        if last_equal:
            i += 1

        return i
