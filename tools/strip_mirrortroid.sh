#!/bin/bash

# take mirrortroid ips in input
ips="${1}"

# hud stuffs
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x80988d 0x809d77 replace


# scyzer saveload patch && hud updates
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x818000 0x81f0aa replace
# Area label tilemaps
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x829670 0x829717 replace
# bank 83
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x838000 0x83ffff replace
# items plm (palette update)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x84e189 0x84eccf replace
# chained blocks plm patch in freespace
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x84f060 0x84f169 replace
# Large message box top/bottom border tilemap
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x858024 0x858025 replace
# Small message box top/bottom border tilemap
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x858051 0x858054 replace
# special buttons tilemaps
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8583d1 0x858754 replace
# Message tilemaps
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x858793 0x8595aa replace
# Item PLM graphics - bombs
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898004 0x8980c0 replace
# spring ball
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898200 0x898349 replace
# varia
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8982e0 0x8985fe replace
# hi-jump
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8983f0 0x8985fe replace
# screw
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8983f0 0x8985fe replace
# space jump
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x89860a 0x8986c0 replace
# morph
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898700 0x8987fe replace
# speed booster
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898a04 0x898afc replace
# charge
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898b26 0x898bb8 replace
# wave
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898d22 0x898df2 replace
# plasma
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898e24 0x898f00 replace
# spazer
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x898f23 0x898fbc replace
# Cinematic BG object definitions
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8bcf5b 0x8bcf62 replace
# intro/ceres text
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8c8103 0x8c968d replace
# Intro text - page 1
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8cc38f 0x8cc793 replace
# page 2
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8cc7a3 0x8ccb41 replace
# page 3
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8ccb51 0x8cce2f replace
# page 4
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8cce3f 0x8cd5d3 replace
# page 5
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8ccf83 0x8cd5d3 replace
# Palettes - intro
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8ce56b 0x8ce589 replace
# Palettes - space/gunship/Ceres
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8ce68c 0x8ce6a9 replace
# Instruction list - palette FX object $E1C0 (gunship glow)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8dca5b 0x8dcaa4 replace
# Instruction list - palette FX object $E1E4
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8dd6e6 0x8dd8fa replace
# Instruction list - palette FX object $E1F4 (Samus loading - power suit)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8ddb91 0x8ddc95 replace
# Instruction list - palette FX object $E1F8 (Samus loading - varia suit)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8ddcf7 0x8dddfb replace
# Instruction list - palette FX object $E1FC (Samus loading - gravity suit)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8dde5d 0x8ddf61 replace
# Instruction list - Samus in heat - power suit
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8de48c 0x8de670 replace
#  Instruction list - Samus in heat - varia suit
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8de6be 0x8de8af replace
# Instruction list - Samus in heat - gravity suit
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8de8ea 0x8deadb replace
# Menu BG1/2 tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8e820c 0x8ebeda replace
# Transfer Samus tiles to VRAM
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x809383 0x809401 replace
# zebes and stars tilemap
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8edc00 0x8edd24 replace
# bank 8f
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8f8000 0x8f9187 replace
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x8f91fa 0x8fffff replace
# Handle Samus animation delay
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x90832e 0x908330 replace
# Animation delay instruction Bh - select animation delay sequence for wall-jump
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x908483 0x90848b replace
# Function pointer table - check if Samus bottom half drawn
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x90864e 0x908686 replace
# Flag that Samus bottom half is not drawn
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x908688 0x9086ff replace
# Determine if Samus bottom half is drawn - standing
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x908688 0x9086ff replace
# Determine if Samus bottom half is drawn - spin jumping
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x908688 0x9086ff replace
# Determine if Samus bottom half is drawn - knockback / crystal flash ending
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x908688 0x9086ff replace
# Handle horizontal scrolling
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x909645 0x90964e replace
# Wall jump check
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x909d64 0x909dd6 replace
# Update HUD mini-map tilemap
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x90aa43 0x90ab5b replace
# Disable mini-map and mark boss room map tiles as explored
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x90a7f8 0x90a801 replace
# Draw arm cannon
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x90c787 0x90c7b9 replace
# many things including samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x90c80f 0x94b308 replace

# title sprites (collide with varia logo)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x95817a 0x959f9f replace

# Tiles - gunship/Ceres (mode 7)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x95a853 0x95c827 replace
# Tiles - font 1
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x95d093 0x95d614 replace
# Tiles - space/Ceres
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x96d142 0x96eb9d replace
# Tilemap - gunship/Ceres (mode 7)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x96fec0 0x96ff14 replace
# Tilemap - Zebes
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x978ae2 0x978df1 replace
# Tilemap - intro BG3 (the last Metroid is in captivity)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x978ae2 0x978df1 replace
# other tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x97d7fc 0x9bfe10 replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x9c8000 0x9d802d replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x9cfff2 0x9e8080 replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x9dffda 0x9f8020 replace
# Samus tiles
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0x9efff4 0xa08000 replace
# Palette - enemy $D07F/$D0BF (gunship)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xa2a5a2 0xa2a5b3 replace
# Typewriter text - Ceres escape timer
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xa6c458 0xa6c49a replace
# Typewriter text - Zebes escape timer
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xa6c4a2 0xa6c4c9 replace
# Tiles - debugger font
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xabea20 0xabf33c replace
# Tiles - escape timer numbers
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xb0c2c7 0xb0c31e replace
# Tiles - pause screen BG1/2
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xb68042 0xb6b939 replace
# Tiles - menu / pause screen sprites
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xb6c000 0xb6df15 replace
# Tilemap - equipment screen
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xb6eaaa 0xb6ec26 replace
# Tiles - escape timer text
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xb7da00 0xb7e2ff replace
# CRE
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xb98000 0xb9a633 replace
# Tileset Dh/Eh: Tourian (to remove mirrored text chars)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xBFD414 0xC0860A replace
# Extra bank in pc addresses (samus new tiles from sprite something)
~/RandomMetroidSolver/tools/strip_ips.py ${ips} 0xe08000 0xffffff replace
