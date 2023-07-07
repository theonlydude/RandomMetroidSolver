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

for patch in area_rando_warp_door crab_shaft area_layout_ln_exit area_layout_caterpillar area_layout_east_tunnel area_layout_greenhillzone area_layout_crabe_tunnel east_ocean aqueduct_bomb_blocks; do
    VARIA_PATCH=${patch}_${VANILLA}
    MIRROR_PATCH=${patch}_${MIRROR}
    cp ${VANILLA} ${VARIA_PATCH}
    cp ${MIRROR} ${MIRROR_PATCH}
    ${PYTHON} tools/apply_ips.py patches/vanilla/ips/${patch}.ips ${VARIA_PATCH} || die "patch ${patch}"
    ${PYTHON} tools/gen_mirror_layout.py ${VANILLA} ${MIRROR_PATCH} ${VARIA_PATCH} patches/mirror/ips ${patch} || die "mirror patch ${patch}"
    rm -f ${VARIA_PATCH} ${MIRROR_PATCH}
done

# special case for area_layout_single_chamber which is applied on top of area_layout_ln_exit.ips
patch=area_layout_single_chamber
VARIA_PATCH=${patch}_${VANILLA}
MIRROR_PATCH=${patch}_${MIRROR}
cp ${VANILLA} ${VARIA_PATCH}
cp ${MIRROR} ${MIRROR_PATCH}
${PYTHON} tools/apply_ips.py patches/vanilla/ips/area_layout_ln_exit.ips ${VARIA_PATCH} || die "patch special"
${PYTHON} tools/apply_ips.py patches/vanilla/ips/${patch}.ips ${VARIA_PATCH} || die "patch special2"
${PYTHON} tools/apply_ips.py patches/mirror/ips/area_layout_ln_exit.ips ${MIRROR_PATCH} || die "patch special3"

${PYTHON} tools/gen_mirror_layout.py ${VANILLA} ${MIRROR_PATCH} ${VARIA_PATCH} patches/mirror/ips ${patch} || die "mirror patch special"
rm -f ${VARIA_PATCH} ${MIRROR_PATCH}
