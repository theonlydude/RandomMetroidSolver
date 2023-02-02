#!/bin/bash

if [ $# -ne 1 ]; then
    echo "usage: $0 ship.png"
    exit 1
fi

[ -z "${VANILLA}" ] && exit 1
[ -z "${PYTHON}" ] && exit 1

# cd to root dir
CWD=$(dirname $0)/..
cd ${CWD}
CWD=$(pwd)

# take ship png as input
png="${1}"
ship=${png%.png}

gfx_rom=${ship}_gfx.sfc
layout_vanilla_rom=${ship}_vanilla.sfc
layout_mirror_rom=${ship}_mirror.sfc

patch=${ship}.ips

cp ${VANILLA} ${gfx_rom}
cp ${VANILLA} ${layout_vanilla_rom}
cp ${VANILLA} ${layout_mirror_rom}

# apply mirror patch to mirror rom
${PYTHON} ./tools/apply_ips.py ./patches/mirror/ips/mirrortroid.ips ${layout_mirror_rom} || exit 1
VANILLA_MIRROR=$(mktemp)
cp ${layout_mirror_rom} ${VANILLA_MIRROR}

echo "==== inject gfx ====" 
${PYTHON} ./tools/inject_ship.py -r ${gfx_rom} -p ${png} --no-layout || exit 1

echo ""
echo "==== inject vanilla layout ===="
${PYTHON} ./tools/inject_ship.py -r ${layout_vanilla_rom} -p ${png} --no-mode7 --no-ship || exit 1

echo ""
echo "==== inject mirror layout ===="
${PYTHON} ./tools/inject_ship.py -r ${layout_mirror_rom} -p ${png} --no-mode7 --no-ship || exit 1

echo ""
echo "==== create patches ===="
${PYTHON} ./tools/make_ips.py ${VANILLA} ${gfx_rom} varia_custom_sprites/patches/ship/${patch} || exit 1
${PYTHON} ./tools/make_ips.py ${VANILLA} ${layout_vanilla_rom} varia_custom_sprites/patches/ship/vanilla/${patch} || exit 1
${PYTHON} ./tools/make_ips.py ${VANILLA_MIRROR} ${layout_mirror_rom} varia_custom_sprites/patches/ship/mirror/${patch} || exit 1

rm -f ${VANILLA_MIRROR}

echo "the end"
