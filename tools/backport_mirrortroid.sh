#!/bin/bash

function die {
    echo "ERROR: ${*}"
    exit 1
}

[ -n "${VANILLA}" ] || die "no vanilla rom"
[ -n "${PYTHON}" ] || PYTHON=python3

mirrortroid_patch_nostrip=${1}
tmp_sfc=tmp.sfc
tmp_ips=tmp.ips
cp ${VANILLA} ${tmp_sfc}

grep strip_ips.py tools/strip_mirrortroid.sh | grep -v '#' | while IFS=' ' read _ _ start end _ ; do
    echo "start: ${start} end: ${end}"
    strip_start=0x808000
    strip_end=0xffffff

    start=$(pyston -c "import sys; print(hex(int(sys.argv[1], 16)-1))" ${start})
    if [ ${end} != 0xffffff ]; then
        end=$(pyston -c "import sys; print(hex(int(sys.argv[1], 16)+1))" ${end})
    fi

    # strip everything except the part we stripped for varia mirrortroid
    cp ${mirrortroid_patch_nostrip} ${tmp_ips}
    echo "----------- strip from ${strip_start} to ${start} ------------"
    tools/strip_ips.py ${tmp_ips} ${strip_start} ${start} replace
    if [ ${end} != 0xffffff ]; then
        echo "----------- strip from ${end} to ${strip_end} --------------"
        tools/strip_ips.py ${tmp_ips} ${end} ${strip_end} replace
    fi

    # apply to tmp sfc
    tools/apply_ips.py ${tmp_ips} ${tmp_sfc}
done

# gen patch with everything we removed from vanilla mirrortroid
tools/make_ips.py ${VANILLA} ${tmp_sfc} backport_mirrortroid.ips

# apply varia fixes to mirrortroid
for patch in 'mirrortroid.ips' 'bank_8f.ips' 'bank_83.ips' 'baby_room.ips' 'baby_remove_blocks.ips' 'escape_animals.ips' 'snails.ips' 'boulders.ips' 'rinkas.ips' 'etecoons.ips' 'crab_main_street.ips' 'crab_mt_everest.ips' 'mother_brain.ips' 'kraid.ips' 'torizos.ips' 'botwoon.ips' 'crocomire.ips'; do
    tools/apply_ips.py patches/mirror/ips/${patch} ${tmp_sfc}
done

tools/make_ips.py ${VANILLA} ${tmp_sfc} mirrortroid_1.3.ips
