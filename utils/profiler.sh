#!/bin/bash

if [ ! $# -ge 1 ]; then
    echo "missing params"
    exit -1
fi

python3 -m cProfile -o solver.cprof solver.py $*
pyprof2calltree -k -i solver.cprof
rm -f solver.cprof
