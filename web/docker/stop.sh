#!/bin/bash
# stop varia containers

docker container ls -a | grep 'varia' | awk '{print $1}' | while read CONTAINER_ID; do docker container stop ${CONTAINER_ID}; done

docker container ls -a | grep -E 'STATUS|varia'

echo "done"
