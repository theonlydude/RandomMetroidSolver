#!/bin/bash

base_ips=~/RandomMetroidSolver/patches/vanilla/ips/area_rando_layout.ips

# strip base layout
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x788A0 0x788A1 replace
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x7C41F 0x7C420 replace
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x231F62 0x232688 replace
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x23EC11 0x23F4AE replace
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x24E816 0x24EC95 replace
# strip gates plm
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x78666 0x78667 replace
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x7C48E 0x7C48f replace
# strip le coude/kronic boost as no layout change in it
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x21BBA7 0x21BCA3 replace
~/RandomMetroidSolver/tools/strip_ips.py ${base_ips} 0x241443 0x241A16 replace


# area_layout_greenhillzone.ips
new_ips=~/RandomMetroidSolver/patches/vanilla/ips/area_layout_greenhillzone.ips
cp ${base_ips} ${new_ips}
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x252FA7 0x2531DC replace

# area_layout_crabe_tunnel.ips
new_ips=~/RandomMetroidSolver/patches/vanilla/ips/area_layout_crabe_tunnel.ips
cp ${base_ips} ${new_ips}
~/RandomMetroidSolver/tools/strip_ips.py ${new_ips} 0x22D564 0x22DBB4 replace

echo "done"
