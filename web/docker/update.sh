#!/bin/bash
# update git in varia container
# ./update.sh -b master
# -b branch: optional branch checkouted during build (default to master)


BRANCH="master"
while getopts "b:d:t:" ARG; do
    case ${ARG} in
        b) export BRANCH="${OPTARG}";;
	*) echo "Unknown option ${ARG}"; exit 0;;
    esac
done

docker exec -w /root/RandomMetroidSolver varia-${BRANCH} git pull
