#!/bin/bash

if [ $# -ne 1 ]; then
    echo "params: ROM"
    exit -1
fi

# cd to root dir
CWD=$(dirname $0)/..
cd ${CWD}
CWD=$(pwd)

ROM=$1

function getDBParam {
    PARAM="$1"

    sed -e "s+.*${PARAM}=\([^,)]*\).*+\1+" ${CWD}/db_params.py | sed -e "s+'++g"
}
host=$(getDBParam "host")
user=$(getDBParam "user")
database=$(getDBParam "database")
password=$(getDBParam "password")
port=$(getDBParam "port")

#################
# truncate tables
rm -rf ${CWD}/sql ${CWD}/logs

SQL="drop table difficulties;
drop table extended_stats;
drop table item_locs;
drop table solver_stats;
drop table techniques;
source ${CWD}/web/database/create_extended_stats.sql"
echo "${SQL}" | mysql -h ${host} -u ${user} -p${password} -P${port} ${database}

#################
# compute stats

# 100 seeds pour tous les skill/setting presets
${CWD}/tools/genExtStats.sh ${ROM} 100

# 900 seeds pour les skill/settings presets de tournoi
${CWD}/tools/genExtStats.sh ${ROM} 900 Season_Races Season_Races
${CWD}/tools/genExtStats.sh ${ROM} 900 SMRAT2021 SMRAT2021
${CWD}/tools/genExtStats.sh ${ROM} 900 Torneio_SGPT3_stage1 Torneio_SGPT3
${CWD}/tools/genExtStats.sh ${ROM} 900 Torneio_SGPT3_stage2 Torneio_SGPT3
${CWD}/tools/genExtStats.sh ${ROM} 900 VARIA_Weekly casual
${CWD}/tools/genExtStats.sh ${ROM} 900 SGL23Online Season_Races

# 900 seeds pour les skill preset inclus dans les rando presets
${CWD}/tools/genExtStats.sh ${ROM} 900 Chozo_Speedrun regular
${CWD}/tools/genExtStats.sh ${ROM} 900 default regular
${CWD}/tools/genExtStats.sh ${ROM} 900 free newbie
${CWD}/tools/genExtStats.sh ${ROM} 900 hardway2hell master
${CWD}/tools/genExtStats.sh ${ROM} 900 haste Season_Races
${CWD}/tools/genExtStats.sh ${ROM} 900 highway2hell expert
${CWD}/tools/genExtStats.sh ${ROM} 900 minimizer_hardcore expert
${CWD}/tools/genExtStats.sh ${ROM} 900 objectives_hard_heat expert
${CWD}/tools/genExtStats.sh ${ROM} 900 objectives_hard_water expert
${CWD}/tools/genExtStats.sh ${ROM} 900 scavenger_hard expert
${CWD}/tools/genExtStats.sh ${ROM} 900 stupid_hard master
${CWD}/tools/genExtStats.sh ${ROM} 900 way_of_chozo regular

# 100 seeds pour une selection de settings presets random
${CWD}/tools/genExtStats.sh ${ROM} 100 where_am_i regular
${CWD}/tools/genExtStats.sh ${ROM} 100 surprise regular

# 1000 seed pour les stats de prog speed
${CWD}/tools/genProgSpeedStats.sh ${ROM} 1000
${CWD}/tools/genProgSpeedStats.sh ${ROM} 1000 FULL

# Stats sur l'échantillon de seeds total
(cd ${CWD}/tools ; tar zxf sql_total.tar.gz)
for FP in $(ls -1 ${CWD}/tools/sql_total/*.sql); do
    F=$(basename ${FP})
    cat ${FP} >> ${CWD}/sql/${F}
done
rm -rf ${CWD}/tools/sql_total/

#################
# load stats
${CWD}/tools/loadExtStats.sh

# dump stats
mysqldump -h ${host} -u ${user} -p${password} -P${port} ${database} difficulties extended_stats item_locs techniques solver_stats > ${CWD}/new_stats.sql
gzip ${CWD}/new_stats.sql
