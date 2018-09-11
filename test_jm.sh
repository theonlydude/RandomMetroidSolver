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
DIFFS=("" "" "" "" "" "" "--maxDifficulty easy" "--maxDifficulty medium" "--maxDifficulty hard" "--maxDifficulty harder" "--maxDifficulty hardcore" "--maxDifficulty mania")
AREAS=("" "--area")

function generate_params {
    SEED="$1"
    PRESET="$2"

    let S=$RANDOM%${#DIFFS[@]}
    DIFF=${DIFFS[$S]}
    let S=$RANDOM%${#AREAS[@]}
    AREA=${AREAS[$S]}

    echo "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --progressionSpeed random --morphPlacement random --progressionDifficulty random --missileQty 0 --superQty 0 --powerBombQty 0 --minorQty 0 --energyQty random --fullRandomization random --spreadItems random --suitsRestriction random --hideItems random --strictMinors random --superFun CombatRandom --superFun MovementRandom --superFun SuitsRandom ${DIFF} ${AREA}"
}

function computeSeed {
    # generate seed
    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}")
    python2 ./randomizer.py ${PARAMS}
    if [ $? -ne 0 ]; then
	echo "${SEED};${PARAMS};OLD;0;yes;n/a;" | tee -a test_jm.csv
	return
    fi

    TIME=$(echo "${OUT}" | grep real | awk '{print $1}')
    SUM_OLD=$(md5sum VARIA_Randomizer_*X${SEED}_${PRESET}.sfc | cut -d ' ' -f 1)

    echo "${SEED};${PARAMS};RANDO;${TIME};${STUCK};${SUM_OLD};" | tee -a test_jm.csv

    # solve seed twice
    ROM=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)

    python2 ./solver.py ${ROM} --preset standard_presets/${PRESET}.json -g | grep -v 'SMBM::factory' > ${ROM}.nocache
    python2 ./solver.py ${ROM} --preset standard_presets/${PRESET}.json -g -c | grep -v 'SMBM::factory' > ${ROM}.cache

    DIFF=$(diff ${ROM}.cache ${ROM}.nocache)

    if [ -z "${DIFF}" ]; then
	rm -f ${ROM} ${ROM}.nocache ${ROM}.cache
	echo "${SEED};${ROM};SOLVER;${PRESET};n/a;OK;" | tee -a test_jm.csv
    else
	echo "${SEED};${ROM};SOLVER;${PRESET};n/a;NOK;" | tee -a test_jm.csv
    fi
}

if [ -z test_jm.csv ]; then
    echo "seed;params;rando/solver;time/preset;stuck;md5sum/result;" > test_jm.csv
fi

MISMATCH_FOUND=1
let LOOPS=${LOOPS}/4
for i in $(seq 1 ${LOOPS}); do
    computeSeed &
    computeSeed &
    computeSeed &
    computeSeed &
    wait
done | tee test_jm.log

if [ ${MISMATCH_FOUND} -eq 0 ]; then
    echo "WARNING_Mismatch found !"
else
    echo "No mismatch found"
fi

rm -rf ${TEMP_DIR}
