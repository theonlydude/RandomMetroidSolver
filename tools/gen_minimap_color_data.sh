#!/bin/bash

set -e

tools/gen_minimap_color_data.py "patches/vanilla/src/minimap_data_area_rando.asm"
tools/gen_minimap_color_data.py "patches/vanilla/src/minimap_data_vanilla_layout.asm" alt
tools/gen_minimap_color_data.py "patches/mirror/src/minimap_data_area_rando.asm"
tools/gen_minimap_color_data.py "patches/mirror/src/minimap_data_vanilla_layout.asm" alt

make -C patches
