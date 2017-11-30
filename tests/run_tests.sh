#!/bin/bash
python -m unittest discover

for ROM in roms/*; do
    echo "${ROM}"
    python2 ../solver.py "${ROM}"
    python3 ../solver.py "${ROM}"
done
