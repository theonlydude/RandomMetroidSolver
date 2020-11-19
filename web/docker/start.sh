#!/bin/bash
# start varia containers

docker container ls -a | grep 'varia' | awk '{print $1}' | while read CONTAINER_ID; do docker container start ${CONTAINER_ID}; done

docker container ls | grep -E 'STATUS|varia'

echo "done"
