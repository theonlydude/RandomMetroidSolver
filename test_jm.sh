#!/bin/bash

LOG=test_jm.log
> ${LOG}
#> test_jm.err
#> test_jm.csv

if [ $# -ne 2 -a $# -ne 3 ]; then
    echo "params: ROM LOOPS [COMPARE]"
    exit -1
fi

#ROM=~/supermetroid_random/Super_Metroid_JU.smc
ROM=$1
LOOPS=$2
if [ -n "$3" ]; then
    COMPARE=0
else
    COMPARE=1
fi

# get git head
if [ ${COMPARE} -eq 0 ]; then
    TEMP_DIR=$(mktemp)
    rm -f ${TEMP_DIR}
    mkdir -p ${TEMP_DIR}
    (
	cd ${TEMP_DIR}
	git clone git@github.com:theonlydude/RandomMetroidSolver.git
	cd RandomMetroidSolver
	#git reset --hard 14e9088f07f64e093c53b773b016f5042765044b
    )
    ORIG=${TEMP_DIR}/RandomMetroidSolver/
else
    ORIG=.
fi

PRESETS=("regular" "noob" "master")
AREAS=("" "--area")
BOSSES=("" "--bosses")

function generate_params {
    SEED="$1"
    PRESET="$2"

    let S=$RANDOM%${#AREAS[@]}
    AREA=${AREAS[$S]}
    let S=$RANDOM%${#BOSSES[@]}
    BOSS=${BOSSES[$S]}

    echo "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --progressionSpeed random --morphPlacement random --progressionDifficulty random --missileQty 0 --superQty 0 --powerBombQty 0 --minorQty 0 --energyQty random --majorsSplit random --suitsRestriction random --hideItems random --strictMinors random --superFun CombatRandom --superFun MovementRandom --superFun SuitsRandom --maxDifficulty random --runtime 20 ${AREA} ${BOSS}"
}

function computeSeed {
    # generate seed
    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}")
    CSV=test_jm.csv
    if [ ! -s "${CSV}" ]; then
	echo "seed;diff_cap;rtime old;rtime new;stime old;stime new;;md5sum ok;params;" | tee -a ${CSV}
    fi

    if [ ${COMPARE} -eq 0 ]; then
	OLD_MD5="old n/a"
	OUT=$(/usr/bin/time -f "\t%E real" python2 ${ORIG}/randomizer.py ${PARAMS} 2>&1)
	if [ $? -ne 0 ]; then
	    OLD="error"
	    echo "${OUT}" >> ${LOG}
	else
	    RTIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
	    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
	    if [ $? -eq 0 ]; then
		OLD_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	    fi
	fi
    fi

    NEW_MD5="new n/a"
    OUT=$(/usr/bin/time -f "\t%E real" python2 ./randomizer.py ${PARAMS} 2>&1)

    RTIME_NEW=$(echo "${OUT}" | grep real | awk '{print $1}')
    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
    if [ $? -eq 0 ]; then
	NEW_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
    fi

    if [ "${OLD_MD5}" != "${NEW_MD5}" -a ${COMPARE} -eq 0 ]; then
	if [ "${OLD_MD5}" = "old n/a" ] && [ "${NEW_MD5}" = "new n/a" ]; then
	    MD5="n/a"
	else
	    MD5="mismatch"
	    echo "OLD: ${OLD_MD5} NEW: ${NEW_MD5}"
	    STOP="now"
	fi
    else
	MD5=${NEW_MD5}
    fi

    # solve seed
    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)
    if [ $? -ne 0 ]; then
	echo "error;${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};" | tee -a ${CSV}
	exit 0
    fi

    if [ ${COMPARE} -eq 0 ]; then
	OUT=$(/usr/bin/time -f "\t%E real" python2 ${ORIG}/solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor 2>&1)
	if [ $? -ne 0 ]; then
            echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};" | tee -a ${CSV}
            echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
            exit 0
	    STIME_OLD="n/a"
	else
	    STIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
	    echo "${OUT}" | grep -q "has already been picked up"
	    DUP_OLD=$?
	    echo "${OUT}" > ${ROM_GEN}.old
	fi
    else
	DUP_OLD=1
    fi

    OUT=$(/usr/bin/time -f "\t%E real" python2 ./solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor 2>&1)
    if [ $? -ne 0 ]; then
        echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};" | tee -a ${CSV}
        echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
        exit 0
	STIME_NEW="n/a"
    else
	STIME_NEW=$(echo "${OUT}" | grep real | awk '{print $1}')
	echo "${OUT}" | grep -q "has already been picked up"
	DUP_NEW=$?

	if [ ${COMPARE} -eq 0 ]; then
	    echo "${OUT}" > ${ROM_GEN}.new
	fi
    fi

    if [ ${DUP_NEW} -eq 0 -o ${DUP_OLD} -eq 0 ]; then
	DUP="dup major detected"
    fi
    echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};${DUP}" | tee -a ${CSV}

    if [ ${COMPARE} -eq 0 ]; then
	DIFF=$(diff ${ROM_GEN}.old ${ROM_GEN}.new)

	if [ -z "${DIFF}" ]; then
	    rm -f ${ROM_GEN} ${ROM_GEN}.new ${ROM_GEN}.old
	    echo "${SEED};${ROM_GEN};SOLVER;${PRESET};OK;" | tee -a test_jm.csv
	else
	    echo "${SEED};${ROM_GEN};SOLVER;${PRESET};NOK;" | tee -a test_jm.csv
	    STOP="now"
	fi
    else
	rm -f ${ROM_GEN}
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
done

echo "DONE"
rm -rf ${TEMP_DIR}
