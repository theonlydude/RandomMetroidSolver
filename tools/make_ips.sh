#!/bin/bash

# should be a Makefile

my_dir=$(dirname $(readlink -f $0))

# use thedopefish's asar which can generated an ips: https://github.com/thedopefish/asar/releases
[ -z "$ASAR" ] && ASAR=asar
[ -z "$ASAR_OPTS" ] && ASAR_OPTS=--fix-checksum=off

[ $# -lt 1 ] && {
    echo "make_ips.sh <patch.asm> [assembler_stdout]" >&2
    exit 1
}

patch=$1
assembler_stdout=$2
tdir=$(dirname $patch)
[ -d "${tdir}/../ips" ] && tdir=${tdir}/../ips
target=${tdir}/$(basename $patch asm)ips
tmp_rom=$(mktemp)
assembler=asar

echo "Assembling ${patch} with ${assembler} ..."

function call_assembler() {
    if [ -z "$assembler_stdout" ]; then
	eval $cmd
    else
	eval $cmd >> $assembler_stdout
    fi
}

cmd="$ASAR $ASAR_OPTS --ips ${target} ${patch} ${tmp_rom}"
call_assembler

[ $? -ne 0 ] && {
    echo "$assembler failed" >&2
    exit 1
}

rm -f ${tmp_rom}

echo
echo "Done"
