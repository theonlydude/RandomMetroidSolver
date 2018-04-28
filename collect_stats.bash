#!/bin/bash

RANDO=./randomizer.py
SOLVER=./solver.py
GET_STATS=./get_stats.py


presets="flo manu noob speedrunner"
#presets="flo speedrunner"
progs="slowest slow medium fast fastest random"
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
mv VARIA_Randomizer_*.json $test_set/old_seeds 2> /dev/null
rmdir $test_set/old_seeds 2> /dev/null
abort_msg=

function worker {
    p=$1
    speed=$2
    i=$3
    dest=$4
    extra=$5    
    
    echo
    echo "**** $dest $i ****"
    echo $extra
    seed=$(head -c 500 /dev/urandom | tr -dc '0-9' | fold -w 7 | head -n 1 | sed 's/^0*//')
    $RANDO --seed ${seed} -i $speed $extra --param diff_presets/$p.json
    rom=$(ls VARIA_Randomizer_*${seed}_${p}*.json)
    rom1st=${dest}/${rom/json/1st}
    solver_log=${dest}/${rom/json/log}
    ls $rom > /dev/null 2>&1 && {
	$SOLVER $rom --param diff_presets/$p.json  --difficultyTarget 5 --displayGeneratedPath -1 $rom1st > $solver_log
	[ $? -ne 0 ] && {
	    abort_msg="Could not solve $rom !! $abort_msg"
	    return
	}
	mv $rom $dest
    }
}

function get_difficulties() {
    echo "Seed;Difficulty"
    for slog in $*; do
	seed=$(basename $slog .log)
	diff=$(tail -2 $slog | head -1  | awk '{print $1}' | sed -e 's+[(,]*++g')
	echo "${seed};${diff}"
    done
}

function gen_seeds() {
    base_dir=$test_set/$1/$2
    base_extra=$3
    progDiff=$2
    for p in $presets; do
	mkdir -p $base_dir/$p
	for speed in $progs; do
	    extra="$base_extra --progressionDifficulty $progDiff --graph"
#	    extra="$base_extra --superQty 1 --powerBombQty 1 --missileQty 4.6"
	    if [[ $speed != "random" ]]; then
		extra="$extra --speedScrewRestriction"
	    fi
	    #	extra="--speedScrewRestriction --superFun Combat --superFun Movement"
	    if [[ $speed == slow* ]] || [[ $speed == "medium" ]]; then
		extra="$extra --spreadItems"
	    fi
	    if [[ $speed != "fastest" ]]; then
		extra="$extra --suitsRestriction"
	    fi
	    dest=$base_dir/$p/$speed
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
	    $GET_STATS $dest/*.1st
	    get_difficulties $dest/*.log > $dest/difficulties.csv
	    mv *stats.csv $dest
	done
    done
}

gen_seeds "classic" "random"
gen_seeds "classic" "easier"
gen_seeds "classic" "harder"
gen_seeds "full" "random" "--fullRandomization"
gen_seeds "full" "easier" "--fullRandomization"
gen_seeds "full" "harder" "--fullRandomization"
