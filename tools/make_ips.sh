#!/bin/bash

# should be a Makefile

my_dir=$(dirname $(readlink -f $0))

[ -z "$ASAR" ] && ASAR=asar.exe
[ -z "$XKAS_PLUS" ] && XKAS_PLUS=xkas.exe
[ -z "$ASAR_OPTS" ] && ASAR_OPTS=--fix-checksum=off
[ -z "$VANILLA" ] && VANILLA=${my_dir}/../vanilla.sfc

[ $# -lt 1 ] && {
    echo "make_ips.sh <patch.asm> [assembler_stdout]" >&2
    exit 1
}

patch=$1
assembler_stdout=$2
tdir=$(dirname $patch)
[ -d "${tdir}/../ips" ] && tdir=${tdir}/../ips
target=${tdir}/$(basename $patch asm)ips
tmprom=$(mktemp)

cp $VANILLA $tmprom

tmprom=$(readlink -f $tmprom)

[ "$OSTYPE" == "cygwin" ] && {
    tmprom=$(cygpath -w $tmprom)
}

assembler=asar

grep 'xkas-plus' $patch > /dev/null

[ $? -eq 0 ] && {
    assembler="xkas-plus"
}

echo "Assembling $patch with $assembler ..."

function call_assembler() {
    if [ -z "$assembler_stdout" ]; then
	eval $cmd
    else
	eval $cmd >> $assembler_stdout
    fi
}

case $assembler in
    asar)
	cmd="$ASAR $ASAR_OPTS $patch '$tmprom'"
	call_assembler
	;;

    xkas-plus)
	(
	    cd $(dirname $patch)
	    cmd="$XKAS_PLUS -o '$tmprom' $(basename $patch)"
	    call_assembler
	)
	;;

    *)
	echo "Unknown assembler $assembler" >&2
	exit 1
	;;
esac

[ $? -ne 0 ] && {
    echo "$assembler failed" >&2
    exit 1
}

echo
echo "Generating $target ..."

${my_dir}/make_ips.py $VANILLA $tmprom $target

rm -f $tmprom

echo
echo "Done"
