#!/bin/bash

base_ips=~/RandomMetroidSolver/patches/vanilla/ips/area_rando_layout_base.ips

# strip gates
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x788A0 0x788A1 replace
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x7C41F 0x7C41F replace

# area_layout_caterpillar.ips
new_ips=~/RandomMetroidSolver/patches/vanilla/ips/area_layout_caterpillar.ips
cp ${base_ips} ${new_ips}
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x23EC11 0x23EC12 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x23F4BC 0x23F4BD replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x24E816 0x24E817 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x24EC9A 0x24EC9B replace

# area_layout_ln_exit.ips
new_ips=~/RandomMetroidSolver/patches/vanilla/ips/area_layout_ln_exit.ips
cp ${base_ips} ${new_ips}
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x231F62 0x231F63 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x232691 0x232692 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x24E816 0x24E817 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x24EC9A 0x24EC9B replace

# area_layout_east_tunnel.ips
new_ips=~/RandomMetroidSolver/patches/vanilla/ips/area_layout_east_tunnel.ips
cp ${base_ips} ${new_ips}
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x231F62 0x231F63 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x232691 0x232692 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x23EC11 0x23EC12 replace
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x23F4BC 0x23F4BD replace

echo "done"
