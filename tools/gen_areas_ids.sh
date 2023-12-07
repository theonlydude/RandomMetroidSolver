#!/bin/bash

set -e

tools/gen_area_in_rooms.py vanilla.sfc "patches/vanilla/src/area_ids.asm"
tools/gen_area_in_rooms.py vanilla.sfc "patches/vanilla/src/area_ids_alt.asm" alt
tools/gen_area_in_rooms.py vanilla.sfc "patches/mirror/src/include/area_ids_base.asm"
tools/gen_area_in_rooms.py vanilla.sfc "patches/mirror/src/area_ids_alt.asm" alt

make -C patches
