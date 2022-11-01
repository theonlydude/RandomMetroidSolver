#!/bin/bash

[ -z "$SPRITE_SOMETHING" ] && SPRITE_SOMETHING=../SpriteSomething
[ -z "$VANILLA" ] && VANILLA=vanilla.sfc
[ -z "$SPRITE_PATCHES" ] && SPRITE_PATCHES=varia_custom_sprites/patches
[ -z "$MAKE_IPS" ] && MAKE_IPS=tools/make_ips.py

sheets=$*

[ -z "$sheets" ] && sheets=varia_custom_sprites/sprite_sheets/*.png

set -e

for sheet in $sheets; do    
    sprite=$(basename $sheet .png)
    echo "****** $sprite ******"
    cp $VANILLA ${sprite}.sfc
    sheet_abs=$(readlink -f $sheet)
    rom_abs=$(readlink -f ${sprite}.sfc)
    (
	cd $SPRITE_SOMETHING
	python3 ./SpriteSomething.py --cli=1 --sprite=$sheet_abs --mode=inject --dest-filename=$rom_abs --src-filename=$rom_abs
    )
    ips=${SPRITE_PATCHES}/${sprite}.ips
    $MAKE_IPS $VANILLA $rom_abs $ips
    rm -f $rom_abs
done
