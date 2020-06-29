#!/bin/bash

if [ $# -ne 2 -a $# -ne 3 ]; then
    echo "params: ROM LOOPS"
    exit -1
fi

# cd to root dir
CWD=$(dirname $0)/..
cd ${CWD}
CWD=$(pwd)

# directory to store the logs and sqls
LOG_DIR=${CWD}/logs
PLOT_DIR=${CWD}/plot
mkdir -p ${LOG_DIR} ${PLOT_DIR}

ROM=$1
LOOPS=$2

function computeSeed {
    RANDO_PRESET="$1"
    SKILL_PRESET="$2"
    PROG_SPEED="$3"
    JOB_ID=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)
    RUNTIME_LIMIT=15

    LOG=${LOG_DIR}/log_$(basename ${RANDO_PRESET} | cut -d '.' -f 1)_$(basename ${SKILL_PRESET} | cut -d '.' -f 1)_${JOB_ID}.log
    DATAFILE=${PLOT_DIR}/${PROG_SPEED}_${JOB_ID}.data

    python3.7 ${CWD}/randomizer.py -r "${ROM}" --randoPreset "${RANDO_PRESET}" --param "${SKILL_PRESET}" --runtime ${RUNTIME_LIMIT} > ${LOG}
     if [ $? -eq 0 ]; then
	 SEED=$(grep 'Rom generated:' ${LOG} | awk '{print $NF}')".sfc"
	 if [ -f "${SEED}" ]; then
	     printf "."
	     rm -f ${LOG}

	     python3.7 ${CWD}/solver.py -r "${SEED}" --preset "${SKILL_PRESET}" --pickupStrategy all --difficultyTarget 10  --plot "${DATAFILE}" >/dev/null

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

SKILL_PRESET=${CWD}/standard_presets/Season_Races.json
BASE_RANDO_PRESET=${CWD}/rando_presets/Season_Races.json
for PROG_SPEED in slowest slow medium fast fastest basic; do
    # generate rando preset
    RANDO_PRESET=${CWD}/rando_presets/Season_Races_${PROG_SPEED}.json
    sed -e "s+VARIAble+${PROG_SPEED}+" ${BASE_RANDO_PRESET} > ${RANDO_PRESET}

    info "Begin rando preset ${RANDO_PRESET} - skill preset ${SKILL_PRESET}"

    CUR_JOBS=0
    CUR_LOOP=0
    PIDS=""
    while true; do
	while [ ${CUR_JOBS} -lt ${NB_CPU} -a ${CUR_LOOP} -lt ${LOOPS} ]; do
	    computeSeed "${RANDO_PRESET}" "${SKILL_PRESET}" "${PROG_SPEED}" &
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

    rm -f ${RANDO_PRESET}

    for F in ${PLOT_DIR}/${PROG_SPEED}_*.data; do
	cat ${F} >> ${PLOT_DIR}/${PROG_SPEED}.data && rm -f ${F}
    done

    PLOT_FILE=${PLOT_DIR}/${PROG_SPEED}.plot
echo "#!/usr/bin/env gnuplot

set term pngcairo
set output '${PLOT_DIR}/${PROG_SPEED}.png'

set yr [0:100]

set style fill transparent solid 0.04 noborder
set style circle radius 1
plot '${PLOT_DIR}/${PROG_SPEED}.data' u 1:2 with circles lc rgb 'red'" > ${PLOT_FILE}
    chmod 755 ${PLOT_FILE}
    ${PLOT_FILE}
done

info "DONE"
