#!/bin/bash

> test_jm.log
#> test_jm.err
#> test_jm.csv

if [ $# -ne 2 ]; then
    echo "params: ROM LOOPS"
    exit -1
fi

#ROM=~/supermetroid_random/Super_Metroid_JU.smc
#ROM=~/downloads/samus/roms/Super_Metroid_orig.smc
ROM=$1
LOOPS=$2

## get git head
#TEMP_DIR=$(mktemp)
#rm -f ${TEMP_DIR}
#mkdir -p ${TEMP_DIR}
#(
#    cd ${TEMP_DIR}
#    git clone git@github.com:theonlydude/RandomMetroidSolver.git
#)
#ORIG=${TEMP_DIR}/RandomMetroidSolver/
ORIG=.

PRESETS=("regular" "noob" "master")
DIFFS=("--maxDifficulty easy" "--maxDifficulty medium" "--maxDifficulty hard" "--maxDifficulty harder" "--maxDifficulty hardcore" "--maxDifficulty mania")
AREAS=("" "--area")

function generate_params {
    SEED="$1"
    PRESET="$2"
    DIFF_CAP="$3"

    let S=$RANDOM%${#AREAS[@]}
    AREA=${AREAS[$S]}

    echo -n "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --progressionSpeed random --morphPlacement random --progressionDifficulty random --missileQty 0 --superQty 0 --powerBombQty 0 --minorQty 0 --energyQty random --fullRandomization random --spreadItems random --suitsRestriction random --hideItems random --strictMinors random --superFun CombatRandom --superFun MovementRandom --superFun SuitsRandom ${AREA}"
    if [ "${DIFF_CAP}" = "diffcap" ]; then
	echo -n " --maxDifficulty random"
    fi
    echo ""
}

function computeSeed {
    # generate seed
    DIFF_CAP="${1}"

    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}" "${DIFF_CAP}")
    CSV=test_jm_${DIFF_CAP}.csv
    if [ ! -f "${CSV}" ]; then
	echo "seed;diff_cap;time cache;time nocache;params;" | tee -a ${CSV}
    fi

    OUT=$(/usr/bin/time -f "\t%E real" python2 ./randomizer.py ${PARAMS} 2>&1)
    if [ $? -ne 0 ]; then
	TIME_NOCACHE="n/a"
    else
	TIME_NOCACHE=$(echo "${OUT}" | grep real | awk '{print $1}')
	rm -f VARIA_Randomizer_*X${SEED}_${PRESET}.sfc
    fi

    PARAMS="${PARAMS} --cache"

    OUT=$(/usr/bin/time -f "\t%E real" python2 ./randomizer.py ${PARAMS} 2>&1)
    if [ $? -ne 0 ]; then
	TIME_CACHE="n/a"
    else
	TIME_CACHE=$(echo "${OUT}" | grep real | awk '{print $1}')
	rm -f VARIA_Randomizer_*X${SEED}_${PRESET}.sfc
    fi

    echo "${SEED};${DIFF_CAP};${TIME_CACHE};${TIME_NOCACHE};${PARAMS};" | tee -a ${CSV}

#    # solve seed twice
#    ROM=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)
#
#    python2 ./solver.py ${ROM} --preset standard_presets/${PRESET}.json -g | grep -v 'SMBM::factory' > ${ROM}.nocache
#    python2 ./solver.py ${ROM} --preset standard_presets/${PRESET}.json -g -c | grep -v 'SMBM::factory' > ${ROM}.cache
#
#    DIFF=$(diff ${ROM}.cache ${ROM}.nocache)
#
#    if [ -z "${DIFF}" ]; then
#	rm -f ${ROM} ${ROM}.nocache ${ROM}.cache
#	echo "${SEED};${ROM};SOLVER;${PRESET};n/a;OK;" | tee -a test_jm.csv
#    else
#	echo "${SEED};${ROM};SOLVER;${PRESET};n/a;NOK;" | tee -a test_jm.csv
#    fi
}

#if [ -z test_jm.csv ]; then
#    echo "seed;params;rando/solver;time/preset;stuck;md5sum/result;" > test_jm.csv
#fi

#let LOOPS=${LOOPS}/2
for DIFF_CAP in "diffcap" "nodiffcap"; do
    for i in $(seq 1 ${LOOPS}); do
	computeSeed "${DIFF_CAP}" #&
	#computeSeed "${DIFF_CAP}" &
	#computeSeed "${DIFF_CAP}" &
	#computeSeed "${DIFF_CAP}" &
	#wait
    done | tee test_jm.log
done

#rm -rf ${TEMP_DIR}
