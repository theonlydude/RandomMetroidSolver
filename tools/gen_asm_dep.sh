#!/bin/bash

src=$1

incdirs="$(dirname $src) ${INCLUDE_DIRS}"

printf "${src}:\t"

function add_deps() {
    includes=$(grep '^incsrc' $1 | cut -f 2 -d ' ' | sed -e "s/'//g" -e 's/"//g')
    for inc in ${includes}; do
        for incdir in ${incdirs}; do
            incfile=${incdir}/${inc}
            [ -f "${incfile}" ] && {
                printf " ${incfile}"
                add_deps ${incfile}
                break
            }
        done
    done
}

add_deps $src

printf "\n\t@touch ${src}\n"
