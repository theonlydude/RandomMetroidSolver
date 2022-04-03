#!/bin/bash
# update git in varia container
# ./update.sh -b master
# -b branch: optional branch checkouted during build (default to master)
# -c branch: customizer data branch


BRANCH="master"
CUSTOMIZER_BRANCH="main"
while getopts "b:c:" ARG; do
    case ${ARG} in
        b) export BRANCH="${OPTARG}";;
	c) export CUSTOMIZER_BRANCH="${OPTARG}";;
	*) echo "Unknown option ${ARG}"; exit 0;;
    esac
done

docker exec -w /root/RandomMetroidSolver varia-${BRANCH} git pull
docker exec -w /root/web2py varia-${BRANCH} rm -rf applications/solver/sessions/*
docker exec -w /root/RandomMetroidSolver varia-${BRANCH} web/install.sh
docker exec -w /root/RandomMetroidSolver/varia_custom_sprites varia-${BRANCH} git pull origin ${CUSTOMIZER_BRANCH}
docker exec -w /root/RandomMetroidSolver/varia_custom_sprites varia-${BRANCH} ./install.sh --clean
docker exec -w /root/varia-race-mode varia-${BRANCH} git pull

if [ $? -eq 0 ]; then 
    docker exec -w /root/varia-race-mode varia-${BRANCH} ./install.sh
else
    echo "Race Mode update failed. It's normal if you don't have access to race mode repository"
fi
