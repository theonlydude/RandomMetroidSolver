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

# get git head
#TEMP_DIR=$(mktemp)
#rm -f ${TEMP_DIR}
#mkdir -p ${TEMP_DIR}
#(
#    cd ${TEMP_DIR}
#    git clone git@github.com:theonlydude/RandomMetroidSolver.git
#)
#ORIG=${TEMP_DIR}/RandomMetroidSolver/
ORIG=/tmp/tmp.KtU7aob2Ba/RandomMetroidSolver/
#ORIG=.

PRESETS=("regular" "noob" "master")
AREAS=("" "--area")

function generate_params {
    SEED="$1"
    PRESET="$2"

    let S=$RANDOM%${#AREAS[@]}
    AREA=${AREAS[$S]}

    echo "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --progressionSpeed random --morphPlacement random --progressionDifficulty random --missileQty 0 --superQty 0 --powerBombQty 0 --minorQty 0 --energyQty random --fullRandomization random --spreadItems random --suitsRestriction random --hideItems random --strictMinors random --superFun CombatRandom --superFun MovementRandom --superFun SuitsRandom --maxDifficulty random ${AREA}"
}

function computeSeed {
    # generate seed
    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}")
    CSV=test_jm.csv
    if [ ! -f "${CSV}" ]; then
	echo "seed;diff_cap;rtime old;rtime cache;rtime nocache;stime old;stime cache; stime nocache;md5sum ok;params;" | tee -a ${CSV}
    fi

    OLD_MD5="old n/a"
    OUT=$(/usr/bin/time -f "\t%E real" python2 ${ORIG}/randomizer.py ${PARAMS} 2>&1)
    if [ $? -ne 0 ]; then
	RTIME_OLD="n/a"
    else
	RTIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
	ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)
	if [ $? -eq 0 ]; then
	    OLD_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	fi
    fi

    PARAMS="${PARAMS} --cache"

    CACHE_MD5="cache n/a"
    OUT=$(/usr/bin/time -f "\t%E real" python2 ./randomizer.py ${PARAMS} 2>&1)
    if [ $? -ne 0 ]; then
	RTIME_CACHE="n/a"
    else
	RTIME_CACHE=$(echo "${OUT}" | grep real | awk '{print $1}')
	ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)
	if [ $? -eq 0 ]; then
	    CACHE_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	fi
    fi

    if [ "${OLD_MD5}" != "${CACHE_MD5}" ]; then
	if [ "${OLD_MD5}" = "old n/a" ] && [ "${CACHE_MD5}" = "cache n/a" ]; then
	    MD5="n/a"
	else
	    MD5="mismatch"
	    echo "OLD: ${OLD_MD5} CACHE: ${CACHE_MD5}"
	    STOP="now"
	fi
    else
	MD5=${OLD_MD5}
    fi

    # solve seed
    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)
    if [ $? -ne 0 ]; then
	return
    fi

    OUT=$(/usr/bin/time -f "\t%E real" python2 ${ORIG}/solver.py ${ROM_GEN} --preset standard_presets/${PRESET}.json -g 2>&1) > ${ROM_GEN}.old
    if [ $? -ne 0 ]; then
	STIME_OLD="n/a"
    else
	STIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
    fi
    OUT=$(/usr/bin/time -f "\t%E real" python2 ./solver.py ${ROM_GEN} --preset standard_presets/${PRESET}.json -g 2>&1) > ${ROM_GEN}.nocache
    if [ $? -ne 0 ]; then
	STIME_NOCACHE="n/a"
    else
	STIME_NOCACHE=$(echo "${OUT}" | grep real | awk '{print $1}')
    fi
    OUT=$(/usr/bin/time -f "\t%E real" python2 ./solver.py ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --cache 2>&1) > ${ROM_GEN}.cache
    if [ $? -ne 0 ]; then
	STIME_CACHE="n/a"
    else
	STIME_CACHE=$(echo "${OUT}" | grep real | awk '{print $1}')
    fi

    echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_CACHE};${RTIME_NOCACHE};${STIME_OLD};${STIME_CACHE};${STIME_NOCACHE};${MD5};${PARAMS};" | tee -a ${CSV}

    DIFF1=$(diff ${ROM_GEN}.old ${ROM_GEN}.nocache)
    DIFF2=$(diff ${ROM_GEN}.cache ${ROM_GEN}.nocache)

    if [ -z "${DIFF1}" -a -z "${DIFF2}" ]; then
	rm -f ${ROM_GEN} ${ROM_GEN}.nocache ${ROM_GEN}.cache ${ROM_GEN}.old
	echo "${SEED};${ROM_GEN};SOLVER;${PRESET};OK;" | tee -a test_jm.csv
    else
	echo "${SEED};${ROM_GEN};SOLVER;${PRESET};NOK;" | tee -a test_jm.csv
	STOP="now"
    fi
}

STOP=""
let LOOPS=${LOOPS}/4
for i in $(seq 1 ${LOOPS}); do
    computeSeed &
    computeSeed &
    computeSeed &
    computeSeed &
    wait

    if [ "${STOP}" = "now" ]; then
	exit 1
    fi
done | tee test_jm.log

#rm -rf ${TEMP_DIR}
