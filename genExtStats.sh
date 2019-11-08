#!/bin/bash

if [ $# -ne 2 -a $# -ne 3 ]; then
    echo "params: ROM LOOPS"
    exit -1
fi

ROM=$1
LOOPS=$2

function computeSeed {
    RANDO_PRESET="$1"
    SKILL_PRESET="$2"
    JOB_ID=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)

    LOG=log_$(basename ${RANDO_PRESET} | cut -d '.' -f 1)_$(basename ${SKILL_PRESET} | cut -d '.' -f 1)_${JOB_ID}.log
    SQL=extStats_${JOB_ID}.sql

    ./randomizer.py -r "${ROM}" --randoPreset "${RANDO_PRESET}" --param "${SKILL_PRESET}" --ext_stats "${SQL}" --runtime 10 > ${LOG}
     if [ $? -eq 0 ]; then
	 SEED=$(grep 'Rom generated:' ${LOG} | awk '{print $NF}')".sfc"
	 if [ -f "${SEED}" ]; then
	     printf "."
	     rm -f ${LOG}

	     ./solver.py -r "${SEED}" --preset "${SKILL_PRESET}" --pickupStrategy any --difficultyTarget 1 --ext_stats "${SQL}" >/dev/null

	     # delete generated ROM
	     rm -f "${SEED}"
	 else
	     printf "x"
	 fi
     else
	 printf "x"
     fi
}

function wait_for_a_child {
    PIDS="$1"

    while true; do
	for PID in $PIDS; do
	    kill -0 $PID 2>/dev/null
	    if [ $? -ne 0 ]; then
		PIDS=$(echo "$PIDS" | sed -e "s+ $PID ++")
		return
	    fi
	done
	sleep 1
    done
}

function info {
    MSG="$*"
    echo "$(date '+%Y/%m/%d_%H:%M:%S'): ${MSG}"
}

STOP=""
NB_CPU=$(cat /proc/cpuinfo  | grep 'processor' | wc -l)

for RANDO_PRESET in $(ls -1 rando_presets/*.json); do 
    # ignore random presets
    if(echo "${RANDO_PRESET}" | grep -q "random"); then
	continue
    fi

    info "Begin rando preset ${RANDO_PRESET}"

    for SKILL_PRESET in $(ls -1 standard_presets/*.json | grep -v -E 'solution|samus'); do
	info "  Begin skill preset ${SKILL_PRESET}"

	CUR_JOBS=0
	CUR_LOOP=0
	PIDS=""
	while true; do
	    while [ ${CUR_JOBS} -lt ${NB_CPU} -a ${CUR_LOOP} -lt ${LOOPS} ]; do
		computeSeed "${RANDO_PRESET}" "${SKILL_PRESET}" &
		PIDS="$PIDS $! "
		let CUR_JOBS=$CUR_JOBS+1
		let CUR_LOOP=$CUR_LOOP+1
	    done

	    wait_for_a_child "${PIDS}"
	    let CUR_JOBS=$CUR_JOBS-1

	    if [ $CUR_JOBS -eq 0 -a $CUR_LOOP -ge $LOOPS ]; then
		break
	    fi
	done
	echo ""
    done
    echo ""
done

# will fail if more than 'getconf ARG_MAX' sql files (2097152 on linux)
for F in extStats_*.sql; do
    RESULT=${RANDOM}
    let "RESULT %= ${NB_CPU}"

    cat ${F} >> extStats_${RESULT}.sql && rm -f ${F}
done

echo "DONE"
