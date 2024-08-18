#!/bin/bash

set -e

tools/gen_area_in_rooms.py vanilla.sfc "patches/vanilla/src/area_ids_area_rando.asm"
tools/gen_area_in_rooms.py vanilla.sfc "patches/vanilla/src/area_ids_vanilla_layout.asm" alt
tools/gen_area_in_rooms.py vanilla.sfc "patches/mirror/src/include/area_ids_area_rando_base.asm"
tools/gen_area_in_rooms.py vanilla.sfc "patches/mirror/src/include/area_ids_vanilla_layout_base.asm" alt

make -C patches
