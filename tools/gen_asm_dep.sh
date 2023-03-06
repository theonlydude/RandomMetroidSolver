#!/bin/bash

src=$1
ips=$2

printf "${ips}:\t${src}"

function add_deps() {
    incdirs="$(dirname $1) ${INCLUDE_DIRS}"
    includes=$(grep -i '^incsrc' $1 | cut -f 2 -d ' ' | sed -e "s/'//g" -e 's/"//g')
    incbins=$(grep -i '^incbin' $1 | cut -f 2 -d ' ' | sed -e "s/'//g" -e 's/"//g')
    for inc in ${incbins}; do
        for incdir in ${incdirs}; do
            incfile=${incdir}/${inc}
            [ -f "${incfile}" ] && {
                printf " ${incfile}"
                break
            }
        done
    done
    for inc in ${includes}; do
        for incdir in ${incdirs}; do
            incfile=${incdir}/${inc}
            [ -f "${incfile}" ] && {
                printf " ${incfile}"
                add_deps ${incfile}
                break
            }
            [[ "$SYM_ASM_FILES" == *"$incfile"* ]] && {
                # we reference a symbol export file that does not exist yet
                printf " ${incfile}"
            }
        done
    done
}

add_deps $src
