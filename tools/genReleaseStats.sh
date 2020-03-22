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

    sed -e "s+.*${PARAM}='\([^']*\)'.*+\1+" ${CWD}/db_params.py
}
host=$(getDBParam "host")
user=$(getDBParam "user")
database=$(getDBParam "database")
password=$(getDBParam "password")

#################
# truncate tables
rm -rf ${CWD}/sql ${CWD}/logs

SQL="truncate table difficulties;
truncate table extended_stats;
truncate table item_locs;
truncate table solver_stats;
truncate table techniques;"
echo "${SQL}" | mysql -h ${host} -u ${user} -p${password} ${database}

#################
# compute stats

# 100 seeds pour tous les skill/setting presets
${CWD}/tools/genExtStats.sh ${ROM} 100

# 900 seeds pour les skill/settings presets de tournoi
${CWD}/tools/genExtStats.sh ${ROM} 900 Season_Races
${CWD}/tools/genExtStats.sh ${ROM} 900 Playoff_Races
${CWD}/tools/genExtStats.sh ${ROM} 900 SMRAT2020

# 1000 seed pour les stats de prog speed
${CWD}/tools/genProgSpeedStats.sh ${ROM} 1000
${CWD}/tools/genProgSpeedStats.sh ${ROM} 1000 FULL

# Stats sur l'échantillon de seeds total
${CWD}/tools/genTotalStats.sh ~/download/total_seeds_majors
${CWD}/tools/genTotalStats.sh ~/download/total_seeds_full FULL

#################
# load stats
${CWD}/tools/loadExtStats.sh

# dump stats
mysqldump -h ${host} -u ${user} -p${password} ${database} difficulties extended_stats item_locs techniques solver_stats > ${CWD}/new_stats.sql
gzip ${CWD}/new_stats.sql
