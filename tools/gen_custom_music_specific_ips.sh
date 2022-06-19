#!/bin/bash

# exec from VARIA root dir

[ -z "$ASAR" ] && ASAR=asar.exe
[ -z "$ASAR_OPTS" ] && ASAR_OPTS=--fix-checksum=off
[ -z "$VANILLA" ] && VANILLA=vanilla.sfc
[ -z "$MAKE_IPS" ] && MAKE_IPS=tools/make_ips.sh

songs="Green_Brinstar Upper_Norfair Red_Brinstar Lower_Norfair East_Maridia Tourian_Bubbles Mother_Brain_2 Mother_Brain_3 Wrecked_Ship___Power_off Wrecked_Ship___Power_on Boss_fight___Ridley Boss_fight___Kraid Boss_fight___Phantoon Boss_fight___Crocomire Boss_fight___Spore_Spawn Boss_fight___Botwoon Boss_fight___Draygon"

set -e

asm_dir=patches/common/src
ips_dir=patches/common/ips
dest_dir=${ips_dir}/custom_music_specific

mkdir -p ${dest_dir}

for song in $songs; do
    ASAR=$ASAR VANILLA=$VANILLA ASAR_OPTS="$ASAR_OPTS -D${song}" $MAKE_IPS ${asm_dir}/custom_music_specific.asm
    mv ${ips_dir}/custom_music_specific.ips ${dest_dir}/${song}.ips
done
