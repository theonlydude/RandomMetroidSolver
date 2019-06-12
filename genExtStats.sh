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
    JOB_ID="$3"

    ./randomizer.py -r "${ROM}" --randoPreset "${RANDO_PRESET}" --param "${SKILL_PRESET}" --ext_stats "extStats_${JOB_ID}.sql" --runtime 5 > /dev/null && printf "." || printf "x"
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
    info "Begin rando preset ${RANDO_PRESET}"

    for SKILL_PRESET in $(ls -1 standard_presets/*.json | grep -v -E 'solution|samus'); do
	info "  Begin skill preset ${SKILL_PRESET}"

	CUR_JOBS=0
	CUR_LOOP=0
	PIDS=""
	while true; do
	    while [ ${CUR_JOBS} -lt ${NB_CPU} -a ${CUR_LOOP} -lt ${LOOPS} ]; do
		computeSeed "${RANDO_PRESET}" "${SKILL_PRESET}" "${CUR_JOBS}" &
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

cat extStats_*.sql > extStats.sql
rm -f extStats_*.sql

echo "DONE"
