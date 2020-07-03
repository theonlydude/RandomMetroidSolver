#!/bin/sh

# should be a Makefile

my_dir=$(dirname $(readlink -f $0))

[ -z "$ASAR" ] && ASAR=asar.exe
[ -z "$VANILLA" ] && VANILLA=${my_dir}/../vanilla.sfc

[ $# -lt 1 ] && {
    echo "make_ips.sh <patch.asm>" >&2
    exit 1
}

set -e

patch=$1
target=$(dirname $patch)/$(basename $patch asm)ips
tmprom=sm.sfc

cp $VANILLA $tmprom

echo "Assembling $patch ..."

$ASAR $patch $tmprom 

echo
echo "Generating $target ..."

${my_dir}/make_ips.py $VANILLA $tmprom $target
rm -f $tmprom

echo
echo "Done"
