#!/bin/sh

# should be a Makefile

my_dir=$(dirname $(readlink -f $0))

[ -z "$ASAR" ] && ASAR=asar.exe
[ -z "$ASAR_OPTS" ] && ASAR_OPTS=--fix-checksum=off
[ -z "$VANILLA" ] && VANILLA=${my_dir}/../vanilla.sfc

[ $# -lt 1 ] && {
    echo "make_ips.sh <patch.asm>" >&2
    exit 1
}

set -e

patch=$1
tdir=$(dirname $patch)
[ -d "${tdir}/../ips" ] && tdir=${tdir}/../ips
target=${tdir}/$(basename $patch asm)ips
tmprom=sm.sfc

cp $VANILLA $tmprom

echo "Assembling $patch ..."

$ASAR $ASAR_OPTS $patch $tmprom

echo
echo "Generating $target ..."

${my_dir}/make_ips.py $VANILLA $tmprom $target
rm -f $tmprom

echo
echo "Done"
