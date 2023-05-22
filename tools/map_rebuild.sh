#!/bin/bash

# automate every step to rebuild all maps. run from VARIA source root dir

tools/map_tilecount.py tools/map/graph_area graph/vanilla/map_tilecount.py
tools/map_tilecount.py tools/map/graph_area_mirror graph/mirror/map_tilecount.py

tools/map_icon_sprites.py patches/common/src/map/mapicon_sprites.asm
tools/map_glow.py > patches/common/src/map/config/area_colors.asm

tools/map_area_palettes.sh

tools/map_mirror.sh

make -C patches
