#!/bin/bash

# !! must be launched from RandomMetroidSolver directory, not tests directory !!

python -m unittest discover

for ROM in tests/roms/*; do
    echo "${ROM}"
    python2 solver.py "${ROM}"
    python3 solver.py "${ROM}"
done
