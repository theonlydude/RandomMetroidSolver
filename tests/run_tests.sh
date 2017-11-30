#!/bin/bash

# !! must be launched from RandomMetroidSolver directory, not tests directory !!

echo "Tests in python2:"
python2 -m unittest discover
echo ""

echo "Tests in python3:"
python3 -m unittest discover
echo ""

echo "Test each rom in python2 and python3:"
time for ROM in tests/roms/*; do
    echo "${ROM}"
    python2 solver.py "${ROM}"
    python3 solver.py "${ROM}"
done
