#!/bin/bash

# take mirrortroid ips in input
ips="${1}"

# scyzer saveload patch
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8000 0xf0aa replace
# Area label tilemaps
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x11670 0x11717 replace
# crateria
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1172d 0x117f8 replace
# brinstar
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1182c 0x11936 replace
# norfair
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x118ef 0x119f3 replace
# WS
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x11a54 0x11af9 replace
# maridia
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x11b2e 0x11bfa replace
# tourian
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x11c4d 0x11cf5 replace
# ceres
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x11d54 0x11d6f replace
# brinstar
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1489d 0x148cc replace
# norfair
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1490b 0x1493a replace
# WS
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x14981 0x14994 replace
# maridia
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x149db 0x14a02 replace
# tourian
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x14a49 0x14a58 replace
# chained blocks plm patch in freespace
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x27060 0x27169 replace
# Large message box top/bottom border tilemap
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x28024 0x28025 replace
# Small message box top/bottom border tilemap
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x28051 0x28054 replace
# Message tilemaps
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x28793 0x295aa replace
# Item PLM graphics - bombs
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48004 0x480c0 replace
# spring ball
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48200 0x48349 replace
# varia
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x482e0 0x485fe replace
# hi-jump
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x483f0 0x485fe replace
# screw
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x483f0 0x485fe replace
# space jump
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x4860a 0x486c0 replace
# morph
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48700 0x487fe replace
# speed booster
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48a04 0x48afc replace
# charge
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48b26 0x48bb8 replace
# wave
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48d22 0x48db6 replace
# plasma
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48e24 0x48f00 replace
# spazer
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x48f23 0x48fbc replace
# Cinematic BG object definitions
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x5cf5b 0x5cf62 replace
# Intro text - page 1
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6438f 0x64793 replace
# page 2
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x647a3 0x64b41 replace
# page 3
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x64b51 0x64e2f replace
# page 4
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x64e3f 0x655d3 replace
# page 5
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x64f83 0x655d3 replace
# Palettes - intro
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6656b 0x66589 replace
# Palettes - space/gunship/Ceres
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6668c 0x666a9 replace
# Instruction list - palette FX object $E1C0 (gunship glow)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6ca5b 0x6caa4 replace
# Instruction list - palette FX object $E1E4
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6d6e6 0x6d8fa replace
# Instruction list - palette FX object $E1F4 (Samus loading - power suit)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6db91 0x6dc95 replace
# Instruction list - palette FX object $E1F8 (Samus loading - varia suit)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6dcf7 0x6ddfb replace
# Instruction list - palette FX object $E1FC (Samus loading - gravity suit)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6de5d 0x6df61 replace
# Instruction list - Samus in heat - power suit
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6e48c 0x6e670 replace
#  Instruction list - Samus in heat - varia suit
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6e6be 0x6e8af replace
# Instruction list - Samus in heat - gravity suit
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x6e8ea 0x6eadb replace
# Menu BG1/2 tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x7020c 0x73eda replace
# Transfer Samus tiles to VRAM
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1383 0x1401 replace
# Handle Samus animation delay
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8032e 0x80330 replace
# Animation delay instruction Bh - select animation delay sequence for wall-jump
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x80483 0x8048b replace
# Function pointer table - check if Samus bottom half drawn
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8064e 0x80686 replace
# Flag that Samus bottom half is not drawn
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x80688 0x806ff replace
# Determine if Samus bottom half is drawn - standing
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x80688 0x806ff replace
# Determine if Samus bottom half is drawn - spin jumping
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x80688 0x806ff replace
# Determine if Samus bottom half is drawn - knockback / crystal flash ending
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x80688 0x806ff replace
# Handle horizontal scrolling
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x81645 0x8164e replace
# Wall jump check
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x81d64 0x81dd6 replace
# Draw arm cannon
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x84787 0x847b9 replace
# many things including samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8480f 0xa3308 replace
# other tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xa80db 0xdfe10 replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xe0000 0xe802d replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xe7ff2 0xf0080 replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xeffda 0xf8020 replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xf7ff4 0x100000 replace
# Palette - enemy $D07F/$D0BF (gunship)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1125a2 0x1125b3 replace
# Tiles - debugger font
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x15ea20 0x15f33c replace
# Tiles - pause screen BG1/2
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1b0042 0x1b3939 replace
# Tiles - menu / pause screen sprites
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1b4000 0x1b5f15 replace
# Tilemap - equipment screen
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1b6aaa 0x1b6c26 replace
# Tiles - escape timer text
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x1bdb80 0x1bdb8e replace
# Extra bank (samus new tiles from sprite something)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x300000 0x400000 replace
# bank 8f
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x78000 0x7ffff replace
