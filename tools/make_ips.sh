#!/bin/sh

# should be a Makefile

my_dir=$(dirname $(readlink -f $0))

[ -z "$ASAR" ] && ASAR=asar.exe
[ -z "$XKAS_PLUS" ] && XKAS_PLUS=xkas.exe
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

tmprom=$(readlink -f $tmprom)

assembler=asar

grep '//' $patch > /dev/null

[ $? -eq 0 ] && {
    assembler="xkas-plus"
}

echo "Assembling $patch with $assembler ..."

case $assembler in
    asar)
	$ASAR $ASAR_OPTS $patch $tmprom	
	;;

    xkas-plus)
	(
	    cd $(dirname $patch)
	    $XKAS_PLUS -o $tmprom $(basename $patch)
	)
	;;

    *)
	echo "Unknown assembler $assembler" >&2
	exit 1
	;;

esac

echo
echo "Generating $target ..."

${my_dir}/make_ips.py $VANILLA $tmprom $target
rm -f $tmprom

echo
echo "Done"
