#!/bin/bash

[ -z "$SPRITE_SOMETHING" ] && SPRITE_SOMETHING=../SpriteSomething
[ -z "$SPRITE_PATCHES" ] && SPRITE_PATCHES=varia_custom_sprites/patches/samus
[ -z "$VANILLA" ] && VANILLA=vanilla.sfc
[ -z "$PYTHON" ] && PYTHON=python3

sheets=$*

[ -z "$sheets" ] && sheets=varia_custom_sprites/sprite_sheets/*.png

set -e

# args: sheet, inject rom
function runSpriteSomething() {
    sheet_abs=$(readlink -f $1)
    rom_abs=$(readlink -f $2)
    (
	cd $SPRITE_SOMETHING
	python3 SpriteSomething.py --cli=1 --sprite=$sheet_abs --mode=inject --dest-filename=$rom_abs --src-filename=$rom_abs
    )
}

zero_rom=zero.sfc
ff_rom=ff.sfc

tmp_zero_rom=$(mktemp)
tmp_ff_rom=$(mktemp)

# base ROMs vanilla appended with 0s/FFs up until 4MB
# (we keep a vanilla base for ROM detection by SpriteSomething)
cp $VANILLA ${zero_rom}
cp $VANILLA ${ff_rom}

cat /dev/zero | head -c 1048576 >> ${zero_rom}
cat /dev/zero | tr '\0' '\377' | head -c 1048576 >> ${ff_rom} # ff octal

for sheet in $sheets; do
    sprite=$(basename $sheet .png)
    echo "****** $sprite ******"
    cp $zero_rom $tmp_zero_rom
    cp $ff_rom $tmp_ff_rom
    echo "*** Injecting into zero ROM ..."
    runSpriteSomething $sheet $tmp_zero_rom
    echo "*** Injecting into FF ROM ..."
    runSpriteSomething $sheet $tmp_ff_rom
    ips=${SPRITE_PATCHES}/${sprite}.ips
    echo "*** Generating IPS ..."
    tools/complete_ips.py $VANILLA $tmp_zero_rom $tmp_ff_rom $ips
    tools/clean_sprite_ips.py $ips
    ln -s ${tmp_zero_rom} ${sprite}.sfc
    echo "*** Generating palettes ..."
    tools/gen_sprite_palettes.sh ${sprite}.sfc
    unlink ${sprite}.sfc
    rm -f ${tmp_zero_rom} ${tmp_ff_rom}
done
