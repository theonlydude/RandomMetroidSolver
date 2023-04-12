
# mirrortroid maps are handcrafted, so their mirroring is not consistent

mirrorMapOffsets = {
    "brinstar": 1,
    "crateria": 2,
    "ceres": 24,
    "maridia": -2,
    "norfair": 2,
    "tourian": 1,
    "wrecked_ship": 10
}

mirrorMapOffsets["Brinstar"] = mirrorMapOffsets["brinstar"]
mirrorMapOffsets["Crateria"] = mirrorMapOffsets["crateria"]
mirrorMapOffsets["Maridia"] = mirrorMapOffsets["maridia"]
mirrorMapOffsets["Norfair"] = mirrorMapOffsets["norfair"]
mirrorMapOffsets["WreckedShip"] = mirrorMapOffsets["wrecked_ship"]

def getOffsetFromFilePath(filePath):
    for area, offset in mirrorMapOffsets.items():
        if area in filePath:
            return offset
