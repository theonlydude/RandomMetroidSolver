#!/bin/bash

[ -z "$SOLVER_DIR" ] && SOLVER_DIR=~/RandomMetroidSolver

(
cd $SOLVER_DIR/itemrandomizerweb/patches/sprites

echo "sprite_patches = {"

for i in *.ips; do ../ips.pl $i; done
echo "}"
) > $SOLVER_DIR/itemrandomizerweb/sprite_patches.py
