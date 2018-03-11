#!/bin/bash

RANDO=./randomizer.py
SOLVER=./solver.py
GET_STATS=./get_stats.py


presets="flo manu noob speedrunner"
progs="slowest slow medium fast fastest"
n=20

test_set=$1

[ -z "$test_set" ] && test_set="seeds"

[ -d "$test_set" ] && {
    echo "$test_set already exists" >&2
    exit 1
}

mkdir -p $test_set/old_seeds
mv Ouiche_Randomizer_*.sfc $test_set/old_seeds 2> /dev/null
rmdir $test_set/old_seeds 2> /dev/null

for p in $presets; do
    mkdir $test_set/$p
    for speed in $progs; do
	dest=$test_set/$p/$speed
	mkdir $dest
	for i in $(seq 1 $n); do
	    echo
	    echo "**** $p $speed $i ****"
	    echo
	    $RANDO -i $speed --param diff_presets/$p.json -c AimAnyButton.ips -c itemsounds.ips -c max_ammo_display.ips -c spinjumprestart.ips  --rom ~/roms/Super\ Metroid\ \(Japan\,\ USA\)\ \(En\,Ja\).sfc
	    seed=Ouiche_Randomizer_*.sfc
	    solver_log="$dest/$(basename -s .sfc $seed).txt"
	    $SOLVER $seed --param diff_presets/$p.json  --difficultyTarget 5 --displayGeneratedPath > $solver_log
	    mv $seed $dest
	done
	$GET_STATS $dest/*.sfc
	mv *stats.csv $dest
    done
done
