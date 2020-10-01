import base64

from rom.ips import IPS_Patch

class ROM(object):
    def readWord(self, address=None):
        return self.readBytes(2, address)

    def readByte(self, address=None):
        return self.readBytes(1, address)

    def readBytes(self, size, address=None):
        if address != None:
            self.seek(address)
        return int.from_bytes(self.read(size), byteorder='little')

    def writeWord(self, word, address=None):
        self.writeBytes(word, 2, address)

    def writeByte(self, byte, address=None):
        self.writeBytes(byte, 1, address)

    def writeBytes(self, value, size, address=None):
        if address != None:
            self.seek(address)
        self.write(value.to_bytes(size, byteorder='little'))

class FakeROM(ROM):
    # to have the same code for real ROM and the webservice
    def __init__(self, data={}):
        self.curAddress = 0
        self.data = data

    def seek(self, address):
        self.curAddress = address

    def write(self, bytes):
        for byte in bytes:
            self.data[self.curAddress] = byte
            self.curAddress += 1

    def read(self, byteCount):
        bytes = []
        for i in range(byteCount):
            bytes.append(self.data[self.curAddress])
            self.curAddress += 1

        return bytes

    def close(self):
        pass

    def ipsPatch(self, ipsPatches):
        mergedIPS = IPS_Patch()
        for ips in ipsPatches:
            mergedIPS.append(ips)

        # generate records for ips from self data
        groupedData = {}
        startAddress = -1
        prevAddress = -1
        curData = []
        for address in sorted(self.data):
            if address == prevAddress + 1:
                curData.append(self.data[address])
                prevAddress = address
            else:
                if len(curData) > 0:
                    groupedData[startAddress] = curData
                startAddress = address
                prevAddress = address
                curData = [self.data[startAddress]]
        if startAddress != -1:
            groupedData[startAddress] = curData

        patch = IPS_Patch(groupedData)
        mergedIPS.append(patch)
        patchData = mergedIPS.encode()
        self.data = {}
        self.data["ips"] = base64.b64encode(patchData).decode()
        if mergedIPS.truncate_length is not None:
            self.data["truncate_length"] = mergedIPS.truncate_length
        self.data["max_size"] = mergedIPS.max_size

class RealROM(ROM):
    def __init__(self, name):
        self.romFile = open(name, "rb+")
        self.address = 0

    def seek(self, address):
        self.address = address
        self.romFile.seek(address)

    def write(self, bytes):
        self.romFile.write(bytes)

    def read(self, byteCount):
        return self.romFile.read(byteCount)

    def close(self):
        self.romFile.close()

    def ipsPatch(self, ipsPatches):
        for ips in ipsPatches:
            ips.applyFile(self)
