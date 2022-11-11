#!/bin/bash

src=$1

printf "${src}:\t"

function add_deps() {
    incdirs="$(dirname $1) ${INCLUDE_DIRS}"
    includes=$(grep '^incsrc' $1 | cut -f 2 -d ' ' | sed -e "s/'//g" -e 's/"//g')
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

printf "\n\t@touch ${src}\n"
