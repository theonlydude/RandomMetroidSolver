#!/bin/bash

function die {
    echo "ERROR: $*"
    exit 1
}

CWD=$(dirname $0)/..
cd ${CWD}
CWD=$(pwd)

if [ $# -ne 1 ]; then
    echo "missing param: directory with the png to resize"
    exit 1
fi

PNG_DIR="${1}"
cd "${PNG_DIR}" || die "Can't cd to ${PNG_DIR}"

# get bounding box
MAXX=0
MAXY=0
for i in *.png; do
    A=$(identify $i | awk '{print $3}')
    X=$(echo $A | cut -d 'x' -f 1)
    Y=$(echo $A | cut -d 'x' -f 2)
    if [ $X -gt $MAXX ]; then
        MAXX=$X
    fi
    if [ $Y -gt $MAXY ]; then
        MAXY=$Y
    fi
done

echo "(x: $MAXX y: $MAXY)"

for i in *.png; do
    A=$(identify $i | awk '{print $3}')
    X=$(echo $A | cut -d 'x' -f 1)
    Y=$(echo $A | cut -d 'x' -f 2)
    if [ $X -eq $MAXX -a $Y -eq $MAXY ]; then
        continue
    fi
    convert $i -gravity center -background "rgba(0,0,0,0)" -extent ${MAXX}x${MAXY} $i
done

echo "Done"
