#!/bin/bash
# check patch bytes in both rom a display difference if any is found

patch=$1
rom1=$2
rom2=$3

patch_map=$(~/RandomMetroidSolver/tools/gen_ips_map.py $patch 'out')

rom1_bytes=$(mktemp)
rom2_bytes=$(mktemp)

function extract_patch_bytes {
    rom="$1"
    echo "${patch_map}" | while read line; do
        address=$(echo $line|cut -d '|' -f 1)
        count=$(echo $line|cut -d '|' -f 2)
        ~/RandomMetroidSolver/tools/extract_data.py "$rom" $address $count
    done
}

extract_patch_bytes "${rom1}" > $rom1_bytes
extract_patch_bytes "${rom2}" > $rom2_bytes

echo "Display diff:"
diff $rom1_bytes $rom2_bytes
[ $? -eq 0 ] && echo "no diff found"

rm -f $rom1_bytes $rom2_bytes
