#!/bin/sh

vanilla_dir=patches/vanilla/src/map
mirror_dir=patches/mirror/src/map

areas="brinstar ceres crateria maridia norfair tourian wrecked_ship"

set -e

for a in $areas; do
    # mirror actual map and generate presence bin
    tools/map_mirror.py ${vanilla_dir}/${a}.bin ${vanilla_dir}/${a}_data.bin ${mirror_dir}/${a}.bin ${mirror_dir}/${a}_data.bin
    # generate map reveal presence bin
    tools/gen_map_reveal.py ${mirror_dir}/${a}.bin ${mirror_dir}/${a}_data.bin ${mirror_dir}/${a}_data_reveal.bin
done

# generate area palette JSONs
vanilla_area_json_dir=tools/map/graph_area
mirror_area_json_dir=tools/map/graph_area_mirror

for json in ${vanilla_area_json_dir}/*.json; do
    mirror_json=${mirror_area_json_dir}/$(basename $json)
    tools/map_mirror_area.py $json $mirror_json
done

# generate area palette map asm data for mirror
json_dir=${mirror_area_json_dir} map_dir=${mirror_dir} tools/map_area_palettes.sh

# generate map icons mirror coords
tools/map_mirror_icons.py
