import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc
from rom.leveldata import LevelData, Room
from rom.ips import IPS_Patch

from utils.log import init

vanillaRom = RealROM(sys.argv[1])
mirrorRomName = sys.argv[2]
# varia rom with layout patches, varia tweaks, area layout
variaRom = RealROM(sys.argv[3])
ipsPath = sys.argv[4]

def transformTile(t):
    tile = t & 0x3FF
    hflip = (t >> 10) & 1
    vflip = (t >> 11) & 1
    btsType = (t >> 12) & 0xF

    # invert hflip
    hflip = 1 - hflip

    return (tile) | (hflip << 10) | (vflip << 11) | (btsType << 12)

def transformPos(sx, sy, tx, ty, screenSize):
    # in vanilla tile is in screen (0, 0) at pos (6, 6)
    # in mirror  tile is in screen (1, 0) at pos (9, 6)
    # => screen x: width in screens - 1 - vanilla screen x
    # => screen y: the same
    # => tile x: screen width in tiles - 1 - vanilla tile x
    # => tile y: the same
    return (screenSize[0] - 1 - sx, sy,
            16 - 1 - tx,            ty)

patches = [
    # patch name, room addr
    # layout
    ('dachora',   0x8f9cb3, None),
    ('early_super_bridge', 0x8f9BC8, None),
    ('high_jump', 0x8fAA41, None),
    ('moat',      0x8f95FF, None),
    ('spospo_save', 0x8f9D19, None),
    ('nova_boost_platform', 0x8fa7b3, None),
    ('red_tower', 0x8fa253, None),
    ('spazer',    0x8fa408, None),
    ('kraid_save', 0x8fA4DA, None),
    ('mission_impossible', 0x8f9e11, None),
    # VARIA tweaks
    ('ln_chozo_platform', 0x8fb1e5, None),
    # area layout
    ('area_rando_warp_door', 0x8fd6fd, None),
    ('crab_shaft', 0x8fd1a3, None),
    ('area_layout_caterpillar', 0x8fa322, None),
    ('area_layout_ln_exit', 0x8fad5e, None),
    ('area_layout_east_tunnel', 0x8fcf80, None),
    # area additional layout
    ('area_layout_greenhillzone', 0x8f9e52, None),
    ('area_layout_crabe_tunnel', 0x8fd08a, None),
    ('east_ocean', 0x8f94fd, None),
    ('aqueduct_bomb_blocks', 0x8fd5a7, None),
    # custom start locations
    ('mama_save', 0x8fD055, None),
    ('firefleas_shot_block', 0x8fB55A, None),
    # fast tourian
    ('open_zebetites', 0x8fdd58, None),
    # escape
    ('rando_escape_ws_fix', 0x8fCAF6, 0x8FCB22),
]

for (patch, roomAddr, stateAddr) in patches:
    print("create patch {} at room {}".format(patch, hex(roomAddr)))
    print("-"*64)
    patchRomName = "{}.sfc".format(patch)
    copyfile(mirrorRomName, patchRomName)
    patchRom = RealROM(patchRomName)

    print("load vanilla room")
    vRoom = Room(vanillaRom, roomAddr)
    print("load VARIA room")
    vaRoom = Room(variaRom, roomAddr)
    print("load mirror room")
    mRoom = Room(patchRom, roomAddr)

    print("")
    if stateAddr is not None:
        vLevelData = vRoom.levelData[vRoom.roomStates[stateAddr].levelDataPtr]
    else:
        vLevelData = vRoom.levelData[vRoom.defaultRoomState.levelDataPtr]
    if stateAddr is not None:
        vaLevelData = vaRoom.levelData[vaRoom.roomStates[stateAddr].levelDataPtr]
    else:
        vaLevelData = vaRoom.levelData[vaRoom.defaultRoomState.levelDataPtr]
    if stateAddr is not None:
        mLevelData = mRoom.levelData[mRoom.roomStates[stateAddr].levelDataPtr]
    else:
        mLevelData = mRoom.levelData[mRoom.defaultRoomState.levelDataPtr]

    print("update tiles")
    screenSize = (vRoom.width, vRoom.height)
    tiles = vLevelData.getModifiedTiles(vaLevelData)
    for (sx, sy, tx, ty) in tiles:
        print("update tile at screen ({}, {}) pos ({}, {})".format(sx, sy, tx, ty))
        (vTile, vBTS) = vLevelData.getTile((sx, sy), tx, ty)
        (vaTile, vaBTS) = vaLevelData.getTile((sx, sy), tx, ty)
        print("vanilla tile    : {}/{}".format(vLevelData.displayLayoutTile(vTile), hex(vBTS)))
        print("varia tile      : {}/{}".format(vaLevelData.displayLayoutTile(vaTile), hex(vaBTS)))

        # look for h/v-copy around
        (vaTileR, vaBTSR) = vaLevelData.getTile((sx, sy), tx+1, ty)
        (vaTileL, vaBTSL) = vaLevelData.getTile((sx, sy), tx-1, ty)
        (vaTileD, vaBTSD) = vaLevelData.getTile((sx, sy), tx, ty+1)
        (vaTileU, vaBTSU) = vaLevelData.getTile((sx, sy), tx, ty-1)
        
        if vaBTSL == 0x01:
            print("varia tile L    : {}/{}".format(vaLevelData.displayLayoutTile(vaTileL), hex(vaBTSL)))
            print("WARNING: h-copy left not handled")
        if vaBTSD == 0xff:
            print("varia tile D    : {}/{}".format(vaLevelData.displayLayoutTile(vaTileD), hex(vaBTSD)))
            print("WARNING: v-copy down not handled")
        if vaBTSU == 0x01:
            print("varia tile U    : {}/{}".format(vaLevelData.displayLayoutTile(vaTileU), hex(vaBTSU)))
            print("WARNING: v-copy up not handled")

        if vaBTSR == 0xff:
            print("h-copy right detected")
            print("varia tile R    : {}/{}".format(vaLevelData.displayLayoutTile(vaTileR), hex(vaBTSR)))
            # invert tile and h-copy bts
            (msx, msy, mtx, mty) = transformPos(sx, sy, tx+1, ty, screenSize)
            (msxR, msyR, mtxR, mtyR) = transformPos(sx, sy, tx, ty, screenSize)
            mTile = transformTile(vaTile)
            mTileR = transformTile(vaTileR)
            print("transformed  tile: {}/{}".format(mLevelData.displayLayoutTile(mTile), hex(vaBTS)))
            print("transformed tileR: {}/{}".format(mLevelData.displayLayoutTile(mTileR), hex(vaBTSR)))
            print("new tile positions screen ({}, {}) pos ({}, {})".format(msx, msy, mtx, mty))
            print("new tileR  positions screen ({}, {}) pos ({}, {})".format(msxR, msyR, mtxR, mtyR))
            mLevelData.updateTile((msxR, msyR), mtxR, mtyR, mTileR, vaBTSR)
            mLevelData.updateTile((msx, msy), mtx, mty, mTile, vaBTS)
        else:
            mTile = transformTile(vaTile)
            print("transformed tile: {}/{}".format(mLevelData.displayLayoutTile(mTile), hex(vaBTS)))
            (msx, msy, mtx, mty) = transformPos(sx, sy, tx, ty, screenSize)
            print("new tile positions screen ({}, {}) pos ({}, {})".format(msx, msy, mtx, mty))
            mLevelData.updateTile((msx, msy), mtx, mty, mTile, vaBTS)

    print("")
    print("save room")
    vanillaSize = vLevelData.compressedSize
    mLevelData.write(vanillaSize)

    print("")
    print("gen ips")
    patchRom.close()
    patchIps = IPS_Patch.create(open(mirrorRomName, 'rb').read(), open(patchRomName, 'rb').read())
    target = os.path.join(ipsPath, "{}.ips".format(patch))
    patchIps.save(target)

    # delete patch rom
    os.remove(patchRomName)
