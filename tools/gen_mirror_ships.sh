#!/bin/bash

function die {
    echo "ERROR: ${*}"
    exit 1
}

[ -n "${VANILLA}" ] || die "no vanilla rom"
[ -n "${PYTHON}" ] || PYTHON=python3

MIRROR=mirror_base.sfc
cp ${VANILLA} vanilla_base.sfc
VANILLA=vanilla_base.sfc
cp ${VANILLA} ${MIRROR}
tools/apply_ips.py patches/mirror/ips/mirrortroid.ips ${MIRROR} || die "patch mirrortroid"
tools/apply_ips.py patches/mirror/ips/bank_8f.ips ${MIRROR} || die "patch 8f"
tools/apply_ips.py patches/mirror/ips/bank_83.ips ${MIRROR} || die "patch 83"

for ship in Frieza_ship GameCube_ship MFFusionship Red-M0nk3ySMShip1 Red-M0nk3ySMShip2 Red-M0nk3ySMShip3 Red-M0nk3ySMShip4 Red-M0nk3ySMShip5 SNES_ship am2r_ship ascent_ship bowser_ship egg_prison enterprise hyperion_ship ice_metal_ship kirbyship lastresort_ship lost_world_ship mario_ship metalslug_ship minitroid_ship n64_ship opposition_ship phazon_ship pocket_rocket stairs_ship the_baby top_hunter_ship xwing; do
    echo "cur ship: ${ship}"
    vanilla_rom_ship=${ship}_vanilla.sfc
    cp ${VANILLA} ${vanilla_rom_ship}
    mirror_rom_ship=${ship}_mirror.sfc
    cp ${MIRROR} ${mirror_rom_ship}
    vanilla_patch=varia_custom_sprites/patches/ship/vanilla/${ship}.ips
    mirror_patch=varia_custom_sprites/patches/ship/mirror/${ship}.ips

    ${PYTHON} tools/apply_ips.py ${vanilla_patch} ${vanilla_rom_ship} &&
    ${PYTHON} tools/gen_mirror_ship.py ${vanilla_rom_ship} ${mirror_rom_ship} &&
    ${PYTHON} tools/make_ips.py ${MIRROR} ${mirror_rom_ship} ${mirror_patch}

    rm -f ${vanilla_rom_ship} ${mirror_rom_ship}
done

rm -f ${MIRROR} ${VANILLA}
