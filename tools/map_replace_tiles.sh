#!/bin/bash

map_dirs="patches/vanilla/src/map patches/mirror/src/map"
areas="brinstar ceres crateria maridia norfair tourian wrecked_ship"

to_replace=$1
replacement=$2

maps=

for d in $map_dirs; do
    for a in $areas; do
        maps="$maps ${d}/${a}.bin"
    done
done

tools/map_replace_tiles.py ${to_replace} ${replacement} ${maps}
