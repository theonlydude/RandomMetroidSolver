#!/bin/bash

[ -z "$SPRITE_SOMETHING" ] && SPRITE_SOMETHING=${HOME}/SpriteSomething
[ -z "$SPRITE_PATCHES" ] && SPRITE_PATCHES=varia_custom_sprites/patches/samus
[ -z "$VANILLA" ] && VANILLA=vanilla.sfc

sheets=$*

[ -z "$sheets" ] && sheets=varia_custom_sprites/sprite_sheets/*.png

set -e

# args: sheet, inject rom
function runSpriteSomething() {
    sheet_abs=$(readlink -f $1)
    rom_abs=$(readlink -f $2)
    (
	cd $SPRITE_SOMETHING
	./SpriteSomething --cli=1 --sprite=$sheet_abs --mode=inject --dest-filename=$rom_abs --src-filename=$rom_abs
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

head -c 32768 $VANILLA > ${zero_rom}
cp ${zero_rom} ${ff_rom}

cat /dev/zero | head -c 4161536 >> ${zero_rom}
cat /dev/zero | tr '\0' '\377' | head -c 4161536 >> ${ff_rom} # ff octal

for sheet in $sheets; do
    sprite=$(basename $sheet .png)
    echo "****** $sprite ******"
    cp $zero_rom $tmp_zero_rom
    cp $ff_rom $tmp_ff_rom
    runSpriteSomething $sheet $tmp_zero_rom
    runSpriteSomething $sheet $tmp_ff_rom
    ips=${SPRITE_PATCHES}/${sprite}.ips    
    tools/complete_ips.py $tmp_zero_rom $tmp_ff_rom $ips
    tools/clean_sprite_ips.py $ips
    rm -f ${tmp_zero_rom} ${tmp_ff_rom}
done
