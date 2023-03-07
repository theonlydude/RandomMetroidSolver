#!/bin/bash

src=$1
ips=$2

printf "${ips}:\t${src}"

function add_deps() {
    local incdirs="$(dirname $1) ${INCLUDE_DIRS}"
    local includes=$(grep -i '^incsrc' $1 | cut -f 2 -d ' ' | sed -e "s/'//g" -e 's/"//g')
    local incbins=$(grep -i '^incbin' $1 | cut -f 2 -d ' ' | sed -e "s/'//g" -e 's/"//g')
    echo "BINARIES" >&2
    echo "incbins = ${incbins}" >&2
    for inc in ${incbins}; do
        echo "bin inc ${inc}" >&2
        for incdir in ${incdirs}; do
            local incfile=${incdir}/${inc}
            echo "incfile ${incfile}" >&2
            [ -f "${incfile}" ] && {
                echo "OK!" >&2
                printf " ${incfile}"
                break
            }
        done
    done
    echo "SRCS" >&2
    echo "includes = ${includes}" >&2
    for inc in ${includes}; do
        echo "src inc ${inc}" >&2
        for incdir in ${incdirs}; do
            local incfile=${incdir}/${inc}
            echo "incfile ${incfile}" >&2
            [ -f "${incfile}" ] && {
                echo "OK!" >&2
                printf " ${incfile}"
                add_deps ${incfile}
                break
            }
            [[ "$SYM_ASM_FILES" == *"$incfile"* ]] && {
                echo "SYM OK!" >&2
                # we reference a symbol export file that does not exist yet
                printf " ${incfile}"
            }
        done
    done
}

add_deps $src
