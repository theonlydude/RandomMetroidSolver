#!/bin/bash

RANDO=./randomizer.py
SOLVER=./solver.py
GET_STATS=./get_stats.py


presets="flo noob speedrunner"
#presets="flo speedrunner"
progs="slowest slow medium fast fastest"
n=20

test_set=$1

nb_cpu=$(grep processor /proc/cpuinfo | wc -l)
#nb_cpu=1

[ -z "$test_set" ] && test_set="seeds"

[ -d "$test_set" ] && {
    echo "$test_set already exists" >&2
    exit 1
}

mkdir -p $test_set/old_seeds
mv VARIA_Randomizer_*.sfc $test_set/old_seeds 2> /dev/null
rmdir $test_set/old_seeds 2> /dev/null

which pypy && PYPY="pypy"

abort_msg=

function worker {
    p=$1
    speed=$2
    i=$3
    dest=$4
    extra=$5    
    
    echo
    echo "**** $p $speed $i ****"
    echo $extra
    seed=$(head -c 500 /dev/urandom | tr -dc '0-9' | fold -w 7 | head -n 1 | sed 's/^0*//')
    ${PYPY} $RANDO --seed ${seed} -i $speed $extra --param diff_presets/$p.json -c AimAnyButton.ips -c itemsounds.ips -c max_ammo_display.ips -c skip_ceres.ips -c elevators_doors_speed.ips --rom ~/roms/Super\ Metroid\ \(Japan\,\ USA\)\ \(En\,Ja\).sfc
    solver_log="$dest/${seed}.txt"
    rom="VARIA_Randomizer_*${seed}_${p}*.sfc"
    ls $rom > /dev/null 2>&1 && {
	$SOLVER $rom --param diff_presets/$p.json  --difficultyTarget 5 --displayGeneratedPath > $solver_log
	[ $? -ne 0 ] && {
	    abort_msg="Could not solve $rom !! $abort_msg"
	    return
	}
	mv $rom $dest
    }
}

for p in $presets; do
    mkdir $test_set/$p
    for speed in $progs; do
	dest=$test_set/$p/$speed
	extra="--speedScrewRestriction"
#	extra="--speedScrewRestriction --superFun Combat --superFun Movement"
	if [[ $speed == slow* ]] || [[ $speed == "medium" ]]; then
	    extra="$extra --spreadItems"
	fi
	if [[ $speed != "fastest" ]]; then
	    extra="$extra --suitsRestriction"
	fi
	mkdir $dest
	workers=0
	for i in $(seq 1 $n); do
	    if [ ${workers} -ge ${nb_cpu} ]; then
		wait
		[ ! -z "$abort_msg" ] && {
		    echo $abort_msg
		    exit 1
		}
		workers=0
	    fi
	    worker ${p} ${speed} ${i} ${dest} "$extra" &
            renice -n 10 -p $!
	    let workers=${workers}+1
	done
        wait
	[ ! -z "$abort_msg" ] && {
	    echo $abort_msg
	    exit 1
	}
	$GET_STATS $dest/*.sfc
	mv *stats.csv $dest
    done
done
