#!/bin/bash

src=$1

incdirs="$(dirname $src) ${INCLUDE_DIRS}"
includes=$(grep '^incsrc' $src | cut -f 2 -d ' ' | sed -e "s/'//g" -e 's/"//g')

printf "${src}:\t"

for inc in ${includes}; do
    for incdir in ${incdirs}; do
        incfile=${incdir}/${inc}
        [ -f "${incfile}" ] && {
            printf " ${incfile}"
            break
        }
    done
done
printf "\n"
