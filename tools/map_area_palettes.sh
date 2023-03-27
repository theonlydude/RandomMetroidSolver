#!/bin/sh

pal_tool=tools/map_area_palettes.py
json_dir=tools/map/graph_area
map_dir=patches/vanilla/src/map

${pal_tool} ${json_dir}/normal_crateria.json ${map_dir}/crateria.bin ${map_dir}/crateria_data_reveal.bin ${map_dir}/crateria.asm Crateria
${pal_tool} ${json_dir}/alt_crateria.json ${map_dir}/crateria.bin ${map_dir}/crateria_data_reveal.bin ${map_dir}/crateria_alt.asm Crateria

${pal_tool} ${json_dir}/normal_brinstar.json ${map_dir}/brinstar.bin ${map_dir}/brinstar_data_reveal.bin ${map_dir}/brinstar.asm Brinstar
${pal_tool} ${json_dir}/alt_brinstar.json ${map_dir}/brinstar.bin ${map_dir}/brinstar_data_reveal.bin ${map_dir}/brinstar_alt.asm Brinstar

${pal_tool} ${json_dir}/normal_norfair.json ${map_dir}/norfair.bin ${map_dir}/norfair_data_reveal.bin ${map_dir}/norfair.asm Norfair
${pal_tool} ${json_dir}/alt_norfair.json ${map_dir}/norfair.bin ${map_dir}/norfair_data_reveal.bin ${map_dir}/norfair_alt.asm Norfair

${pal_tool} ${json_dir}/normal_maridia.json ${map_dir}/maridia.bin ${map_dir}/maridia_data_reveal.bin ${map_dir}/maridia.asm Maridia

${pal_tool} ${json_dir}/normal_wrecked_ship.json ${map_dir}/wrecked_ship.bin ${map_dir}/wrecked_ship_data_reveal.bin ${map_dir}/wrecked_ship.asm WreckedShip

${pal_tool} ${json_dir}/normal_tourian.json ${map_dir}/tourian.bin ${map_dir}/tourian_data_reveal.bin ${map_dir}/tourian.asm Tourian

${pal_tool} ${json_dir}/normal_ceres.json ${map_dir}/ceres.bin ${map_dir}/ceres_data_reveal.bin ${map_dir}/ceres.asm Ceres
