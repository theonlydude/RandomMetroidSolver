import sys
import struct
import colorsys
import os
import shutil
import random
import re
import math
import subprocess
import time
import logging

#Palette Hue Shift

#Most palette info taken from http://www.metroidconstruction.com/SMMM/ and http://patrickjohnston.org/bank/9B#f9400
#Every palette consists of sixteen 2-byte-sets, suit palettes are uncompressed

#To-Do | Adjustments:

#Suits:
#find crystal flash, maybe D96C0-5F  | visor oddities that might be missing: DA3C6-02 Samus' visor flashing yellow in dark rooms. ,1652C-00 Samus' green visor when first entering a room. 

#Enemies:
#Kzan is not changed, would look odd

#glowing elevator platform palette pointer seems to be messed up, need to find the real palette location at some point. might be using the general palette.

#excluded lava-like enemies from hue shifting because lava color is not being shifted yet. e.g.: hibashi, puromi, lavaman



#Information about compressed palettes for main areas:
#
#$00 normal Crateria: 				C2AD7C	0x212D7C  
#$01 red Cratera:					C2AE5D 	0x212E5D
#$02 old Crateria: 					C2AF43	0x212F43
#$03 old Crateria:					C2B015  0x213015
#$04 Wrecked Ship: 					C2B0E7	0x2130E7
#$05 Wrecked Ship:					C2B1A6  0x2131A6
#$06 Green Brinstar: 				C2B264	0x213264
#$07 Red Brinstar: 					C2B35F	0x21335F
#$08 Red Brinstar:					C2B447	0x213447
#$09 Norfair: 						C2B5E4	0x2135E4
#$0A Norfair:						C2B6BB	0x2136BB
#$0B Maridia: 						C2B83C	0x21383C
#$0C Maridia:						C2B92E	0x21392E
#$0D Tourian: 						C2BAED	0x213AED
#$0E Tourian:						C2BBC1	0x213BC1
#$0F Ceres: 						C2C104	0x214104
#$10 Ceres:							C2C1E3	0x2141E3
#$11 Mode 7 Ceres:					C2C104	0x214104
#$12 Mode 7 Ceres:					C2C1E3	0x2141E3
#$13 Mode 7 Ridley:					C2C104	0x214104
#$14 Mode 7 Ridley:					C2C1E3	0x2141E3
#$15 Save/G4 [0]: 					C2BC9C	0x213C9C
#$16 Save/G4 [1]: 					C2BD7B	0x213D7B
#$17 Save/G4 [2]: 					C2BE58	0x213E58
#$18 Save/G4 [3]: 					C2BF3D	0x213F3D
#$19 Save/G4 [4]: 					C2C021	0x214021
#$1A Kraid room:					C2B510	0x213510
#$1B Crocomire room:				C2B798	0x213798
#$1C Draygon room:					C2BA2C	0x213A2C


#Pointer Locations:

#$00	0x7E6A8 = 7C AD C2   
#$01	0x7E6B1 = 5D AE C2
#$02	0x7E6BA = 43 AF C2
#$03	0x7E6C3 = 15 B0 C2
#$04	0x7E6CC = E7 B0 C2
#$05	0x7E6D5 = A6 B1 C2
#$06	0x7E6DE = 64 B2 C2
#$07	0x7E6E7 = 5F B3 C2
#$08	0x7E6F0 = 47 B4 C2
#$09	0x7E6F9 = E4 B5 C2
#$0A	0x7E702 = BB B6 C2
#$0B	0x7E70B = 3C B8 C2
#$0C	0x7E714 = 2E B9 C2
#$0D	0x7E71D = ED BA C2
#$0E	0x7E726 = C1 BB C2
#$0F	0x7E72F = 04 C1 C2
#$10	0x7E738 = E3 C1 C2

#Mode 7 stuff, probably best to leave this alone for now
#$11	0x7E741 = 04 C1 C2
#$12	0x7E74A = E3 C1 C2
#$13	0x7E753 = 04 C1 C2
#$14	0x7E75C = E3 C1 C2

#Back to normal room palettes
#$15	0x7E765 = 9C BC C2
#$16	0x7E76E = 7B BD C2
#$17	0x7E777 = 58 BE C2
#$18	0x7E780 = 3D BF C2
#$19	0x7E789 = 21 C0 C2
#$1A	0x7E792 = 10 B5 C2
#$1B	0x7E79B = 98 B7 C2
#$1C	0x7E7A4 = 2C BA C2


#Inserting palettes around 0x2FE050
#
#Decompressed palette info:
#		2					+	26							+ 	2			+	2			=	32 bytes used per palette (hex-size = 0x20)   ||||| 32 * 8 = 256 bytes per palette set
# Transparency Color | 13 colors used in tileset palette | default white | default black

#boss_tileset_palettes = [0x213510,0x213798,0x213A2C,0x213BC1]
#boss_pointer_addresses = [0x7E792,0x7E79B,0x7E7A4,0x7E726]
#gray doors + hud elements [0x28,0x2A,0x2C,0x2E]
tileset_palette_offsets = [0x212D7C,0x212E5D,0x212F43,0x213015,0x2130E7,0x2131A6,0x213264,0x21335F,0x213447,0x2135E4,0x2136BB,0x21383C,0x21392E,0x213AED,0x213BC1,0x214104,0x2141E3,0x213C9C,0x213D7B,0x213E58,0x213F3D,0x214021,0x213510,0x213798,0x213A2C]
bluedoor_bytes = [0x62,0x64,0x66]
palette_single_bytes = [0x08,0x0A,0x0C,0x0E,0x48,0x4A,0x4C,0x4E,0x50,0x52,0x54,0x56,0x58,0x5A,0x68,0x6A,0x6C,0x6E,0x70,0x72,0x74,0x76,0x78,0x7A]  

#replaced crateria $00 with $01 pointer for nicer colors on surface crateria (was [0x7E6A8,0x7E6B1,[...] before the change)
pointer_addresses = [0x7E6A8,0x7E6A8,0x7E6BA,0x7E6C3,0x7E6CC,0x7E6D5,0x7E6DE,0x7E6E7,0x7E6F0,0x7E6F9,0x7E702,0x7E70B,0x7E714,0x7E71D,0x7E726,0x7E72F,0x7E738,0x7E765,0x7E76E,0x7E777,0x7E780,0x7E789,0x7E792,0x7E79B,0x7E7A4]
pointers_to_insert = []


#Fx1 palettes and the length of each individual color palette
#Ridley room fade-in
fx1_palettes_ri = [0x132509]
fx1_length_ri = [0xD1]
#Brinstar blue glow
fx1_palettes_gb = [0x6ED9F,0x6EDA9,0x6EDB3,0x6EDBD,0x6EDC7,0x6EDD1,0x6EDDB,0x6EDE5,0x6EDEF,0x6EDF9,0x6EE03,0x6EE0D,0x6EE17,0x6EE21]
fx1_length_gb = [0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02]
#Red brinstar glow purple
fx1_palettes_rb = [0x6EEDD,0x6EEF1,0x6EF05,0x6EF19,0x6EF2D,0x6EF41,0x6EF55,0x6EF69,0x6EF7D,0x6EF91,0x6EFA5,0x6EFB9,0x6EFCD,0x6EFE1]
fx1_length_rb = [0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07]
#Wrecked Ship green glow
fx1_palettes_ws = [0x6EAE8,0x6EAF0,0x6EAF8,0x6EB00,0x6EB08,0x6EB10,0x6EB18,0x6EB20,0x13CA61]
fx1_length_ws = [0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x6F]
#Crateria pulse red, 
fx1_palettes_cr = [0x6FD03,0x6FD15,0x6FD27,0x6FD39,0x6FD4B,0x6FD5D,0x6FD6F,0x6FD81,0x6FD93,0x6FDA5,0x6FDB7,0x6FDC9,0x6FDDB,0x6FDED]
fx1_length_cr = [0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06]
#Tourian slow pulse red/blue,
fx1_palettes_tr = [0x6F640,0x6F656,0x6F66C,0x6F682,0x6F698,0x6F6AE,0x6F6C4,0x6F6DA,0x6F6F0,0x6F706,0x6F71C,0x6F7AF,0x6F7BF,0x6F7CF,0x6F7DF,0x6F7EF,0x6F7FF,0x6F80F,0x6F81F,0x6F82F,0x6F83F,0x6F84F,0x6F85F,0x6F86F,0x6F87F,0x6F94F,0x6F963,0x6F977,0x6F98B,0x6F99F,0x6F9B3,0x6F9C7,0x6F9DB,0x6F9EF,0x6FA03,0x6FA17,0x6FA2B,0x6FA3F,0x6FA53,0x6F897,0x6F8A3,0x6F8AF,0x6F8BB,0x6F8C7,0x6F8D3,0x6F8DF,0x6F8EB,0x6F8F7,0x6F903,0x6F90F,0x6F91B,0x6F927,0x6F933]
fx1_length_tr = [0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03]
#Maridia quicksand etc.
fx1_palettes_ma = [0x6F4EF,0x6F503,0x6F517,0x6F52B,0x6F547,0x6F553,0x6F55F,0x6F56B,0x6F57F,0x6F593,0x6F5A7,0x6F5BB,0x6F5CF,0x6F5E3,0x6F5F7,0x6F60B]
fx1_length_ma = [0x07,0x07,0x07,0x07,0x03,0x03,0x03,0x03,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07]
#Lantern glow
fx1_palettes_lanterns = [0x6EFFD,0x6F00B,0x6F019,0x6F027,0x6F035,0x6F043,0x6F054,0x6F062,0x6F070,0x6F07E]
fx1_length_lanterns = [0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02]

#this isn't implemented, the other elevator colors are probably managed via the global palette D01A0-0F
ceres_elevator_palettes = [0x137871,0x137881,0x137891,0x1378A1,0x1378B1,0x1378C1,0x1378D1,0x1378E1]
ceres_elevator_palettes_length = [0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05]

beam_palettes = [0x843E1]
beam_palettes_length = [0x4F]

#This is in the general palette so as a side-effect it also changes things like energy drops, missile tip colors and other things excluding super missile tips
wave_beam_trail_palettes = [0xD01AA]
wave_beam_trail_length = [0x02]

#Single address for grapple extension color, shifted with same hue as beam palette
grapple_beam_palettes = [0xDC687]
grapple_beam_length = [0x00]


#Boss palettes
#[sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]

#Draygon, Kraid, Crocomire and Mother Brain have seperate colors hidden in tileset palettes which are addressed in the boss shift function
spore_spawn_palettes = [0x12E359]
spore_spawn_length = [0x3F]
kraid_palettes = [0x138687,0x13B3F3,0x13B533,0x13AAB0,0x1386C7]
kraid_length = [0x1F,0x8F,0x7F,0x03,0x0F]
phantoon_palettes = [0x13CA01,0x13CB41]
phantoon_length = [0x0F,0x7F]
botwoon_palettes = [0x199319,0x19971B]
botwoon_length = [0x0F,0x7F]
#draygon projectiles: 12A237-0F , they are gray so wouldn't shift well to begin with, leaving this out
draygon_palettes = [0x12A1F7,0x1296AF]
draygon_length = [0x4F, 0x1F]
crocomire_palettes = [0x12387D,0x1238CB,0x1238FD]
crocomire_length = [0x1F, 0x08,0x0F]
bomb_torizo_palettes = [0x1506C7,0x150707]
bomb_torizo_length = [0x1F, 0x1F]
gold_torizo_palettes = [0x150747,0x150787,0x020032]
gold_torizo_length = [0x1F,0x1F,0xFF]
ridley_palettes = [0x1362AA,0x13631A,0x13646A]
ridley_length = [0x2F,0xA7,0x29]
mbrain_palettes = [0x149472,0x1494B2,0x14D264,0x16E448,0x16E648,0x16E6AC,0x16E74C,0x16EA08,0x16EC08,0x16EDAC,0x16EF97,0x16F117,0x1494F2,0x14D082,0x16F281]
mbrain_length = [0x1F,0x0F,0x3F,0xFF,0x2C,0x4A,0x4A,0xFF,0xC0,0x98,0xA8,0x78,0x1F,0x5F,0xC4]

#All enemy palettes have a length of 0x0F
#enemy_names = [boyon,tatori+young tatori,puyo,cacatac,owtch,mellow,mella,memu,multiviola,polyp,rio,squeept,geruta,holtz,oum,chute,gripper,ripperII,ripper,dragon,shutter1-4,kamer,waver,metaree,fireflea,skultera,sciser,zero,tripper,kamer,sbug+sbug(glitched),sidehopper,desgeega,big sidehopper,big sidehopper(tourian),big desgeega,zoa,viola,skree,yard,"samus" geemer,zeela,norfair geemer,geemer,grey geemer,boulder,ebi+projectile,fune,namihe,coven,yapping maw,kago,beetom,powamp,work robot+work robot(disabled),bull,alcoon,atomic,green kihunter,greenish kihunter,red kihunter,shaktool,zeb,zebbo,gamet,geega,grey zebesian,green zebesian,red zebesian,gold zebesian,pink zebesian,black zebesian]
enemy_palettes = [0x110687,0x110B60,0x11198D,0x111E6A,0x11238B,0x112FF3,0x11320C,0x113264,0x1132BC,0x113A7B,0x113E1C,0x1140D1,0x1145FA,0x114A2B,0x11580C,0x11617B,0x1162C0,0x116457,0x11657B,0x116978,0x116DC7,0x118687,0x1188F0,0x118C0F,0x11900A,0x11965B,0x11980B,0x119B7B,0x119B9B,0x11A051,0x11B0A5,0x11B3A1,0x11B5B3,0x11C63E,0x11C8A6,0x11DFA2,0x11E23C,0x11E57C,0x11E5B0,0x11E5D0,0x130687,0x140687,0x141379,0x14159D,0x1419AC,0x141F4F,0x142AFE,0x14365E,0x144143,0x1446B3,0x145821,0x145BC7,0x146230,0x14699A,0x1469BA,0x1469DA,0x155911,0x19878B,0x1989FD,0x198AC1,0x198EDC,0x190687,0x1906A7,0x1906E7,0x190727,0x1906C7,0x190707 ]

####Enemy Palette Groups####
#Animal "enemies"
animal_palettes = [0x13E7FE,0x13F225,0x19E525,0x19E944]

#Sidehopper enemies
sidehopper_palettes = [0x11AA48, 0x11B085]

#Desgeega enemies
desgeega_palettes = [0x11AF85,0x11B217]

#Lava enemies | not implementing these unless lava color gets randomized eventually | not sure if multiviola should be in here
#hibashi,puromi,magdollite
lava_enemy_palettes = [0x130CFB,0x131470,0x142C1C]

#All Metroid-colored enemies:
metroid_palettes = [0x11A725,0x11E9AF,0x14F8E6,0x1494D2]

various_metroid_palettes = [0x14F6D1,0x16E892,0x16E7F2,0x16E8F0]
various_metroid_length = [0x3F,0x27,0x47,0x61]

#Crateria security eye + face tile
crateria_special_enemies = [0x140F8C,0x1467AC]

#Wrecked ship sparks
wrecked_ship_special_enemies = [0x146587]

#Tourian rinka and undocumented zebetite animation palette
tourian_special_enemies = [0x113A5B,0x137D87]

#Ship is treated as an enemy in the game
ship_palette = 0x11259E

#G4 statue 2nd half, 1st half is handled via one of the saveroom shifts
statue_palette_ridley = 0x155745
statue_palette_phantoon = 0x155765
statue_base = 0x155785
statue_fadeout_palettes = [0x6E242,0x6E256,0x6E26A,0x6E27E,0x6E292,0x6E2A6,0x6E2BA,0x6E2CE,0x3839C]
statue_fadeout_size = [0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x07]

#Degree shuffle array for individual tileset shuffles
#Insert two entries for [0,1,2,4,5,6,7,8]
#[0 0 1 1 2 2 3 4 4 5 5 6 6 7 7 8 8 9 10 11 12 13 14 15 16]
degree_list=[]

#Boss degree list follows this order: [sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]
boss_degree_list=[]

###########################
#Suit Palette Information:#
###########################
#Loading and heat-damage glow palettes:
#Every heat palette is seperated by 2 (unused?) bytes
#Loader Power Suit: 0x6DB6B, 0x6DBBA, 0x6DC09, 0x6DC58, 0x6DCA4 
#Heat Power Suit: 0x6E466, 0x6E488, 0x6E4AA, 0x6E4CC, 0x6E4EE, 0x6E510, 0x6E532, 0x6E554, 0x6E576, 0x6E598, 0x6E5BA, 0x6E5DC, 0x6E5FE, 0x6E620, 0x6E642, 0x6E664  |||| final one: 0x6E664 ?
#Loader Varia Suit: 0x6DCD1, 0x6DD20, 0x6DD6F, 0x6DDBE, 0x6DE0A
#Heat Varia Suit : 0x6E692, 0x6E6B4, 0x6E6D6, 0x6E6F8, 0x6E71A, 0x6E73C, 0x6E75E, 0x6E780, 0x6E7A2, 0x6E7C4, 0x6E7E6, 0x6E808, 0x6E82A, 0x6E84C, 0x6E86E, 0x6E890  |||| final one: 0x6E890 ?
#Loader Gravity Suit: 0x6DE37, 0x6DE86, 0x6DED5, 0x6DF24, 0x6DF70
#Heat Gravity Suit: 0x6E8BE, 0x6E8E0, 0x6E902, 0x6E924, 0x6E946, 0x6E968, 0x6E98A, 0x6E9AC, 0x6E9CE, 0x6E9F0, 0x6EA12, 0x6EA34, 0x6EA56, 0x6EA78, 0x6EA9A, 0x6EABC |||| final one: 0x6EABC ?
#[$9B:9540-$9B:97E0] not suit palettes?
#other_palette_offsets = [0x0D9400,0x0D9520,0x0D9540,0x0D9560,0x0D9580,0x0D95A0,0x0D95C0,0x0D95E0,0x0D9600,0x0D9620,0x0D9640,0x0D9660,0x0D9680,0x0D96A0,0x0D9780,0x0D97A0,0x0D97C0,0x0D97E0,0x0D9800,0x0D9820,0x0D9840,0x0D9860,0x0D9880,0x0D98A0,0x0D98C0,0x0D98E0,0x0D9900,0x0D9920,0x0D9940,0x0D9960,0x0D9980,0x0D99A0,0x0D99C0,0x0D99E0,0x0D9A00,0x0D9A20,0x0D9A40,0x0D9A60,0x0D9A80,0x0D9AA0,0x0D9AC0,0x0D9AE0,0x0D9B00,0x0D9B20,0x0D9B40,0x0D9B60,0x0D9B80,0x0D9BA0,0x0D9BC0,0x0D9BE0,0x0D9C00,0x0D9C20,0x0D9C40,0x0D9C60,0x0D9C80,0x0D9CA0,0x0D9CC0,0x0D9CE0,0x0D9D00,0x0D9D20,0x0D9D40,0x0D9D60,0x0D9D80,0x0D9DA0,0x0D9DC0,0x0D9DE0,0x0D9E00,0x0D9E20,0x0D9E40,0x0D9E60,0x0D9E80,0x0D9EA0,0x0D9EC0,0x0D9EE0,0x0D9F00,0x0D9F20,0x0D9F40,0x0D9F60,0x0D9F80,0x0D9FA0,0x0D9FC0,0x0D9FE0,0x0DA000,0x0DA020,0x0DA040,0x0DA060,0x0DA080,0x0DA0A0,0x0DA0C0,0x0DA0E0,0x0DA100]


filename = sys.argv[1]

#########################
#		SETTINGS		#
#########################

#set to True if all suits should get a separate hue-shift degree
individual_suit_shift = True

#set to True if all tileset palettes should get a separate hue-shift degree
individual_tileset_shift = True

#Match ship palette with power suit palette
match_ship_and_power = True

#Group up similar looking enemy palettes to give them similar looks after hue-shifting (e.g. metroids, big+small sidehoppers)
seperate_enemy_palette_groups = True

#Match boss palettes with boss room degree
match_room_shift_with_boss = False


### These variables define what gets shifted
shift_tileset_palette = True

shift_boss_palettes = True

shift_suit_palettes = True

shift_enemy_palettes = True

shift_beam_palettes = True

shift_ship_palette = True
###



#Change offsets to work with SM practice rom, this was just used for easier feature debugging, changes where new palettes are inserted.
practice_rom = False
debug = False

power_palette_offsets = [0x0D9400,0x0D9820,0x0D9840,0x0D9860,0x0D9880,0x0D98A0,0x0D98C0,0x0D98E0,0x0D9900,0x0D9B20,0x0D9B40,0x0D9B60,0x0D9B80,0x0D9BA0,0x0D9BC0,0x0D9BE0,0x0D9C00,0x0D9C20,0x0D9C40,0x0D9C60,0x0D9C80,0x0D9CA0,0x0D9CC0,0x0D9CE0,0x0D9D00,0x6DB6B, 0x6DBBA, 0x6DC09, 0x6DC58, 0x6DCA4,0x6E466, 0x6E488, 0x6E4AA, 0x6E4CC, 0x6E4EE, 0x6E510, 0x6E532, 0x6E554, 0x6E576, 0x6E598, 0x6E5BA, 0x6E5DC, 0x6E5FE, 0x6E620, 0x6E642, 0x6E664,0x6DB8F,0x6DC2D,0x6DC7C,0x6DBDE]
varia_palette_offsets = [0x0D9520,0x0D9920,0x0D9940,0x0D9960,0x0D9980,0x0D99A0,0x0D99C0,0x0D99E0,0x0D9A00,0x0D9D20,0x0D9D40,0x0D9D60,0x0D9D80,0x0D9DA0,0x0D9DC0,0x0D9DE0,0x0D9E00,0x0D9E20,0x0D9E40,0x0D9E60,0x0D9E80,0x0D9EA0,0x0D9EC0,0x0D9EE0,0x0D9F00,0x6DCD1, 0x6DD20, 0x6DD6F, 0x6DDBE, 0x6DE0A,0x6E692, 0x6E6B4, 0x6E6D6, 0x6E6F8, 0x6E71A, 0x6E73C, 0x6E75E, 0x6E780, 0x6E7A2, 0x6E7C4, 0x6E7E6, 0x6E808, 0x6E82A, 0x6E84C, 0x6E86E, 0x6E890,0x6DCF5,0x6DD44,0x6DD93,0x6DDE2]
gravity_palette_offsets = [0x0D9540,0x0D9560,0x0D9580,0x0D95A0,0x0D95C0,0x0D95E0,0x0D9600,0x0D9620,0x0D9640,0x0D9660,0x0D9680,0x0D96A0,0x0D9780,0x0D97A0,0x0D97C0,0x0D97E0,0x0D9800,0x0D9A20,0x0D9A40,0x0D9A60,0x0D9A80,0x0D9AA0,0x0D9AC0,0x0D9AE0,0x0D9B00,0x0D9F20,0x0D9F40,0x0D9F60,0x0D9F80,0x0D9FA0,0x0D9FC0,0x0D9FE0,0x0DA000,0x0DA020,0x0DA040,0x0DA060,0x0DA080,0x0DA0A0,0x0DA0C0,0x0DA0E0,0x0DA100,0x6DE37, 0x6DE86, 0x6DED5, 0x6DF24, 0x6DF70,0x6E8BE, 0x6E8E0, 0x6E902, 0x6E924, 0x6E946, 0x6E968, 0x6E98A, 0x6E9AC, 0x6E9CE, 0x6E9F0, 0x6EA12, 0x6EA34, 0x6EA56, 0x6EA78, 0x6EA9A, 0x6EABC,0x6DE5B,0x6DEAA,0x6DEF9,0x6DF48]

max_degree = 360

max_palette_length = 0x100



def wait_timeout(proc, seconds):
    #Wait for a process to finish, or raise exception after timeout
    start = time.time()
    end = start + seconds
    interval = min(seconds / 1000.0, .25)

    while True:
        result = proc.poll()
        if result is not None:
            return result
        if time.time() >= end:
            proc.kill()
        time.sleep(interval)
    return
		
def snes_to_pc(snesaddress):
	pcaddress=((snesaddress&0x7F0000)>>1|(snesaddress&0x7FFF))
	return pcaddress
	
def pc_to_snes(pcaddress):
	snesaddress=(((pcaddress<<1)&0x7F0000)|(pcaddress&0x7FFF)|0x8000)|0x800000
	return snesaddress

def adjust_hue_degree(hsl_color, degree):

	hue = hsl_color[0] *360
	hue_adj = (hue +degree) % 360
	if debug: print("Original hue: ",hue)
	if debug: print("Adjusted hue:", hue_adj)
	if debug: print("Degree:", degree)
	
	return hue_adj
	
def adjust_sat(hsl_color, adjustment):
	
	sat = hsl_color[1]*100
	sat_adj = (sat+ adjustment) % 100
	if debug: print("Original sat: ",sat)
	if debug: print("Adjusted sat:", sat_adj)
	if debug: print("Adjustment", adjustment)
	
	return sat_adj

def adjust_light(hsl_color, adjustment):
	
	lit = hsl_color[2]*100
	lit_adj = (lit + adjustment) % 100
	if debug: print("Original lit: ",lit)
	if debug: print("Adjusted lit:", lit_adj)
	if debug: print("Adjustment", adjustment)
	
	return lit_adj

def RGB_24_to_15 (color_tuple):

	R_adj = int(color_tuple[0])//8
	G_adj = int(color_tuple[1])//8
	B_adj = int(color_tuple[2])//8
	
	c = B_adj * 1024 + G_adj * 32 + R_adj
	return (c)
	
def RGB_15_to_24 (SNESColor):

	R = ((SNESColor		) % 32) * 8
	G = ((SNESColor//32	) % 32) * 8
	B = ((SNESColor//1024) % 32) * 8

	return (R,G,B)
	
def read_pointer(file,address,length):

	file.seek(address)
	read_bytes = file.read(length)
	int_value_LE = int.from_bytes(read_bytes,'little')
	
	return int_value_LE

def write_pointer(file,address,value,length):
	if os.path.exists(filename):
		src = os.path.realpath(filename)
	file = open(src, "r+b")
	file.seek(address)
	file.write(value.to_bytes(length, byteorder='little'))
	return

#Only used for individual tileset degrees (required to adjust fx1 effects accordingly)
#Insert two entries for [0,1,2,4,5,6,7,8]
#[0 0 1 1 2 2 3 4 4 5 5 6 6 7 7 8 8 9 10 11 12 13] 14 15 16
def generate_tileset_degrees():
	count=-1
	while (count < 16):
		count = count+1
		if count in (3,9,10,11,12,13,14,15,16):
			degree = random.randint(0,max_degree)
			degree_list.append(degree)
		else:
			degree = random.randint(0,max_degree)
			degree_list.append(degree)
			degree_list.append(degree)
	return

def generate_boss_degrees():
	#[sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]
	count=-1
	while (count<10):
		count = count+1
		degree = random.randint(0,max_degree)
		boss_degree_list.append(degree)
	return
	
def hue_shift_palette_lists(file,degree,address_list, size_list):
	count=-1
	for address in address_list:
		count = count+1
		for i in range(0,(size_list[count])+1):
			read_address=address+(i*2)
			file.seek(read_address)
			
			print("Fx1 address:",hex(address)," at offset: ", hex(i*2))
			#Read 2 bytes at index i*2
			read_bytes = file.read(2)

			#Convert from LE to BE
			int_value_LE = struct.unpack_from("<h", read_bytes)[0]
		
			#Convert 15bit RGB to 24bit RGB
			rgb_value_24 = RGB_15_to_24(int_value_LE)
		
			#24bit RGB to HLS
			hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255,rgb_value_24[1]/255,rgb_value_24[2]/255)
		
			#Generate new hue based on degree
			new_hue = adjust_hue_degree(hls_col, degree)/360
			
			rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])
		
			#Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
			rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))

			BE_hex_color = RGB_24_to_15(rgb_final)

			file.seek(read_address)
			file.write(BE_hex_color.to_bytes(2, byteorder='little'))
	return
		

def hue_shift_palette_single_offsets(file, offset_list, degree, address):
	
	#if green brinstar or crateria palette, shuffle blue door caps to also shuffle lower crateria color
	if (address == 0x213264) or (address == 0x21335F): 
		copy_offset_list = (offset_list+bluedoor_bytes)
	else:
		copy_offset_list = offset_list
		
	for offset in copy_offset_list:
		#print("Offset: ",hex(offset))
		file.seek(offset)
		#Read 2byte color at offset
		read_bytes = file.read(2)
		if debug: print("read decomp palette offset:", hex(offset), " value:" , read_bytes )
				
		#Convert from LE to BE
		int_value_LE = struct.unpack_from("<h", read_bytes)[0]
				
		#Convert 15bit RGB to 24bit RGB
		rgb_value_24 = RGB_15_to_24(int_value_LE)
					
		if debug: print("24RGB: ",rgb_value_24)
				
		#24bit RGB to HLS
		hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255,rgb_value_24[1]/255,rgb_value_24[2]/255)
		
		#Generate new hue based on degree
		new_hue = adjust_hue_degree(hls_col, degree)/360
		
		rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])
					
		#Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
		rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))
					
		if debug: print("New 24RGB", rgb_final)
						
		BE_hex_color = RGB_24_to_15(rgb_final)
					
		if debug: print("15bit BE_hex_color", hex(BE_hex_color))
					
		file.seek(offset)
		file.write(BE_hex_color.to_bytes(2, byteorder='little'))
		if debug: print("write decomp palette offset:", hex(offset), " value:" , BE_hex_color.to_bytes(2, byteorder='little') )
	return
	
	

#Function to shift palette hues by set degree for a palette with fixed size 0x0F
def hue_shift_fixed_size_palette(file, base_address, degree,size):
	if debug: print("Shifting suit palette at ", hex(base_address)," by degree ", degree)
	
	for i in range(0,size+1):
		read_address=base_address+(i*2)
		file.seek(read_address)
		
		#Read 2 bytes at index i*2
		read_bytes = file.read(2)

		#Convert from LE to BE
		int_value_LE = struct.unpack_from("<h", read_bytes)[0]
		
		#Convert 15bit RGB to 24bit RGB
		rgb_value_24 = RGB_15_to_24(int_value_LE)
		
		#24bit RGB to HLS
		hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255,rgb_value_24[1]/255,rgb_value_24[2]/255)
		
		#Generate new hue based on degree
		new_hue = adjust_hue_degree(hls_col, degree)/360
			
		rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])
		
		#Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
		rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))

		BE_hex_color = RGB_24_to_15(rgb_final)

		file.seek(read_address)
		file.write(BE_hex_color.to_bytes(2, byteorder='little'))
	return

def hue_shift_tileset_palette(degree):
	count=-1
	for address in tileset_palette_offsets:
	
		count = count+1
		if individual_tileset_shift:
			degree = degree_list[count]

		if debug:print("Count: ", hex(count))
		print("Decompressing palette at ", hex(address), " by degree: ", degree)
		p = subprocess.Popen([decomppath+"/decomp.exe", decomppath+"/"+filename, "decomppalette.bin", hex(address), "4", "0"])	
		wait_timeout(p,0.5)
			
		#Check if decompression happened
		if os.path.exists("./decomppalette.bin"):
			src = os.path.realpath("./decomppalette.bin")
		else:
			print("No decompressed binary file found. Exiting.")
			sys.exit(1)
			
		if debug: print("opening ", src)
		file = open(src, "r+b")
			
		hue_shift_palette_single_offsets(file, palette_single_bytes, degree, address)
		
		#special case for mother brain room
		if address == 0x213BC1:
			temp_TLS_palette_subsets = [0xA0,0xC0,0xE0]
		#and kraids room
		elif address == 0x213510: 
			temp_TLS_palette_subsets = [0x80,0xA0,0xC0]
		#and draygons room
		elif address == 0x213A2C:
			temp_TLS_palette_subsets = [0x80,0xC0,0xE0]
		else:
			temp_TLS_palette_subsets = [0x80,0xA0,0xC0,0xE0]
		
		#skip 2-byte-pair at index 0 (this is the transparency color)
		for subset in temp_TLS_palette_subsets:
			for j in range(1,15):
				#print("Reading at ", hex(subset+(j*2)))
				file.seek(subset+(j*2))
				#Read 2 bytes at index j*2
				read_bytes = file.read(2)
				if debug: print("read decomp palette index:", hex(subset+(j*2)), " value:" , read_bytes )
				
				#Convert from LE to BE
				int_value_LE = struct.unpack_from("<h", read_bytes)[0]
			
				#Convert 15bit RGB to 24bit RGB
				rgb_value_24 = RGB_15_to_24(int_value_LE)
					
				if debug: print("24RGB: ",rgb_value_24)
				
				#24bit RGB to HLS
				hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255,rgb_value_24[1]/255,rgb_value_24[2]/255)
	
				#Generate new hue based on degree
				new_hue = adjust_hue_degree(hls_col, degree)/360
					
				rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])
					
				#Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
				rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))
					
				if debug: print("New 24RGB", rgb_final)
				
				BE_hex_color = RGB_24_to_15(rgb_final)
					
				if debug: print("15bit BE_hex_color", hex(BE_hex_color))
					
				file.seek(subset+(j*2))
				file.write(BE_hex_color.to_bytes(2, byteorder='little'))
				if debug: print("write decomp palette index:", hex(subset+(j*2)), " value:" , BE_hex_color.to_bytes(2, byteorder='little') )
				
			
		#Close file access to allow for new decompression-process
		file.close()
		#practice rom free space 0x2F51C0 -> 0x2F7FFF
		if practice_rom:
			insert_address= 0x2F51C0 + (count*0x100)
		else:
			insert_address= 0x2FE050 + (count*0x100)
			
		pointers_to_insert.append(insert_address)
		if debug: print("pointers_to_insert: ",pointers_to_insert)
			
		#Recompress palette and re-insert at offset
		p = subprocess.Popen([recomppath+"/recomp.exe", recomppath+"/decomppalette.bin", recomppath+"/"+filename, hex(insert_address), "4", "0"])
		wait_timeout(p,0.5)
	return
	
def boss_palette_shift(file):
	if match_room_shift_with_boss:
		hue_shift_palette_lists(file,degree_list[6],spore_spawn_palettes,spore_spawn_length)
		hue_shift_palette_lists(file,degree_list[22],kraid_palettes,kraid_length)
		hue_shift_palette_lists(file,degree_list[4],phantoon_palettes,phantoon_length)
		hue_shift_palette_lists(file,degree_list[11],botwoon_palettes,botwoon_length)
		hue_shift_palette_lists(file,degree_list[24],draygon_palettes,draygon_length)
		hue_shift_palette_lists(file,degree_list[23],crocomire_palettes,crocomire_length)
		hue_shift_palette_lists(file,degree_list[0],bomb_torizo_palettes,bomb_torizo_length)
		hue_shift_palette_lists(file,degree_list[9],gold_torizo_palettes,gold_torizo_length)
		hue_shift_palette_lists(file,degree_list[9],ridley_palettes,ridley_length)
		hue_shift_palette_lists(file,degree_list[14],mbrain_palettes,mbrain_length)
	else:
		#[sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]
		hue_shift_palette_lists(file,boss_degree_list[0],spore_spawn_palettes,spore_spawn_length)
		hue_shift_palette_lists(file,boss_degree_list[1],kraid_palettes,kraid_length)
		hue_shift_palette_lists(file,boss_degree_list[2],phantoon_palettes,phantoon_length)
		hue_shift_palette_lists(file,boss_degree_list[3],botwoon_palettes,botwoon_length)
		hue_shift_palette_lists(file,boss_degree_list[4],draygon_palettes,draygon_length)
		hue_shift_palette_lists(file,boss_degree_list[5],crocomire_palettes,crocomire_length)
		hue_shift_palette_lists(file,boss_degree_list[6],bomb_torizo_palettes,bomb_torizo_length)
		hue_shift_palette_lists(file,boss_degree_list[7],gold_torizo_palettes,gold_torizo_length)
		hue_shift_palette_lists(file,boss_degree_list[8],ridley_palettes,ridley_length)
		hue_shift_palette_lists(file,boss_degree_list[9],mbrain_palettes,mbrain_length)	
	
	if shift_tileset_palette and len(pointers_to_insert)==0:
		print("tileset shifting needs to be called before boss palette shifting if both are active!")
		sys.exit(1)
	
	if shift_tileset_palette:
		boss_address_list = [pointers_to_insert[14],pointers_to_insert[22],pointers_to_insert[24]]
	else:
		boss_address_list = [0x213BC1,0x213510,0x213A2C]
		
	for address in boss_address_list:
		#kraid's room tileset sub-palettes containing boss colors
		if address == 0x213510 or (shift_tileset_palette and address == pointers_to_insert[22]):
			temp_TLS_palette_subsets = [0xE0]
			if match_room_shift_with_boss:
				degree = degree_list[22]
			else:
				degree = boss_degree_list[1]				
		#mother brain's room tileset sub-palettes containing boss colors
		if address == 0x213BC1 or (shift_tileset_palette and address == pointers_to_insert[14]):
			temp_TLS_palette_subsets = [0x80]
			if match_room_shift_with_boss:
				degree = degree_list[14]
			else:
				degree = boss_degree_list[9]			
		#draygon's room tileset sub-palettes containing boss colors
		if address == 0x213A2C or (shift_tileset_palette and address == pointers_to_insert[24]):
			temp_TLS_palette_subsets = [0xA0]
			if match_room_shift_with_boss:
				degree = degree_list[24]
			else:
				degree = boss_degree_list[4]
				
		p = subprocess.Popen([decomppath+"/decomp.exe", decomppath+"/"+filename, "decomppalette.bin", hex(address), "4", "0"])	
		wait_timeout(p,0.5)
			
		#Check if decompression happened
		if os.path.exists("./decomppalette.bin"):
			src = os.path.realpath("./decomppalette.bin")
		else:
			print("No decompressed binary file found. Exiting.")
			sys.exit(1)
			
		if debug: print("opening ", src)
		file = open(src, "r+b")

		for subset in temp_TLS_palette_subsets:
			for j in range(1,15):
				#print("Reading at ", hex(subset+(j*2)))
				file.seek(subset+(j*2))
				#Read 2 bytes at index j*2
				read_bytes = file.read(2)
				if debug: print("read decomp palette index:", hex(subset+(j*2)), " value:" , read_bytes )
				
				#Convert from LE to BE
				int_value_LE = struct.unpack_from("<h", read_bytes)[0]
			
				#Convert 15bit RGB to 24bit RGB
				rgb_value_24 = RGB_15_to_24(int_value_LE)
					
				if debug: print("24RGB: ",rgb_value_24)
				
				#24bit RGB to HLS
				hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255,rgb_value_24[1]/255,rgb_value_24[2]/255)

				#Generate new hue based on degree
				new_hue = adjust_hue_degree(hls_col, degree)/360
					
				rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])
					
				#Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
				rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))
					
				if debug: print("New 24RGB", rgb_final)
				
				BE_hex_color = RGB_24_to_15(rgb_final)
					
				if debug: print("15bit BE_hex_color", hex(BE_hex_color))
					
				file.seek(subset+(j*2))
				file.write(BE_hex_color.to_bytes(2, byteorder='little'))
				if debug: print("write decomp palette index:", hex(subset+(j*2)), " value:" , BE_hex_color.to_bytes(2, byteorder='little') )
				
			
		#Close file access to allow for new decompression-process
		file.close()	
			
		#quick hack to re-insert, should work without issues
		insert_address = address
			
		#Recompress palette and re-insert at offset
		p = subprocess.Popen([recomppath+"/recomp.exe", recomppath+"/decomppalette.bin", recomppath+"/"+filename, hex(insert_address), "4", "0"])
		wait_timeout(p,0.5)
		

	return

######################### 

#Create Backup or restore for new hue shift
if os.path.exists(filename+".bak"):
    src = os.path.realpath(filename+".bak")
    dst = src[:-4]
    MainFile = dst
    shutil.copy(src,dst)
    print("Copied *.bak over *.sfc\n")
elif os.path.exists(filename):
    src = os.path.realpath(filename)
    MainFile = src
    dst = src + ".bak"
    shutil.copy(src,dst)
    print("Couldn't find *.bak, created new backup\n")
else:
    print("No sfc file found. Exiting.")
    sys.exit(1)
	
#Check if tools are present
if os.path.exists("./decomp.exe"):
    decomppath = os.path.realpath("./")
    print("Decomp Path: ", decomppath)
else:
    print("Decomp not found. Exiting.")
    sys.exit(1)
    
if os.path.exists("./recomp.exe"):
    recomppath = os.path.realpath("./")
    print("Recomp Path: ", recomppath)
else:
    print("Recomp not found. Exiting.")
    sys.exit(1)


#Open file for uncompressed binary op
with open(filename, "r+b") as file:

	tileset_degree = random.randint(0,max_degree)
	generate_tileset_degrees()
	generate_boss_degrees()
	
	if shift_tileset_palette:
		hue_shift_tileset_palette(tileset_degree)
		
		if individual_tileset_shift:
			hue_shift_palette_lists(file,degree_list[0],fx1_palettes_cr, fx1_length_cr)
			hue_shift_palette_lists(file,degree_list[6],fx1_palettes_gb, fx1_length_gb)
			hue_shift_palette_lists(file,degree_list[7],fx1_palettes_rb,fx1_length_rb)
			hue_shift_palette_lists(file,degree_list[4],fx1_palettes_ws, fx1_length_ws)
			hue_shift_palette_lists(file,degree_list[13],fx1_palettes_tr, fx1_length_tr)
			hue_shift_palette_lists(file,degree_list[11],fx1_palettes_ma,fx1_length_ma)
			hue_shift_palette_lists(file,degree_list[7],fx1_palettes_lanterns, fx1_length_lanterns)
			hue_shift_palette_lists(file,degree_list[6],crateria_special_enemies,[0x0F,0x0F]) 
			print("Wrecked Ship sparks shifted by ",degree_list[4])
			hue_shift_palette_lists(file,degree_list[4],wrecked_ship_special_enemies,[0x0F])
			hue_shift_palette_lists(file,degree_list[13],tourian_special_enemies,[0x0F,0x0F])
			hue_shift_fixed_size_palette(file,statue_palette_ridley,degree_list[17],0x0F)
			hue_shift_fixed_size_palette(file,statue_palette_phantoon,degree_list[17],0x0F)
			hue_shift_fixed_size_palette(file,statue_base,degree_list[17],0x0F)
			hue_shift_palette_lists(file,degree_list[17],statue_fadeout_palettes,statue_fadeout_size)
		else:
			degree = tileset_degree
			hue_shift_palette_lists(file,degree,fx1_palettes_cr, fx1_length_cr)
			hue_shift_palette_lists(file,degree,fx1_palettes_gb, fx1_length_gb)
			hue_shift_palette_lists(file,degree,fx1_palettes_rb, fx1_length_rb)
			hue_shift_palette_lists(file,degree,fx1_palettes_ws, fx1_length_ws)
			hue_shift_palette_lists(file,degree,fx1_palettes_tr, fx1_length_tr)
			hue_shift_palette_lists(file,degree,fx1_palettes_ma,fx1_length_ma)
			hue_shift_palette_lists(file,degree,fx1_palettes_lanterns, fx1_length_lanterns)
			hue_shift_palette_lists(file,degree,crateria_special_enemies,[0x0F,0x0F])
			hue_shift_palette_lists(file,degree,wrecked_ship_special_enemies,[0x0F])
			hue_shift_palette_lists(file,degree,tourian_special_enemies,[0x0F])
			hue_shift_fixed_size_palette(file,statue_palette_ridley,degree,0x0F)
			hue_shift_fixed_size_palette(file,statue_palette_phantoon,degree,0x0F)
			hue_shift_fixed_size_palette(file,statue_base,degree,0x0F)
			hue_shift_palette_lists(file,degree,statue_fadeout_palettes,statue_fadeout_size)

		
		i=-1
		for p_update in pointers_to_insert:
			i=i+1
			if debug: print("New Pointer Address: ",p_update)
			if debug: print("Write this to file: ", hex(pc_to_snes(p_update)))
			write_pointer(file,pointer_addresses[i], pc_to_snes(p_update), 3)
	
	#this NEEDS to be called after the tileset palette shift function (if tileset shift actually gets called) because it references newly created pointers
	if shift_boss_palettes:
		boss_palette_shift(file)

	if shift_enemy_palettes:
		if seperate_enemy_palette_groups:
			enemy_degree=random.randint(0,max_degree)
			hue_shift_palette_lists(file,enemy_degree,metroid_palettes,[0x0F,0x0F,0x0F,0x0F])
			hue_shift_palette_lists(file,enemy_degree,various_metroid_palettes,various_metroid_length)
			enemy_degree=random.randint(0,max_degree)
			hue_shift_palette_lists(file,enemy_degree,desgeega_palettes,[0x0F,0x0F])
			enemy_degree=random.randint(0,max_degree)
			hue_shift_palette_lists(file,enemy_degree,sidehopper_palettes,[0x0F,0x0F])
			enemy_degree=random.randint(0,max_degree)
			hue_shift_palette_lists(file,enemy_degree,animal_palettes,[0x0F,0x0F,0x0F,0x0F])
			for address in enemy_palettes:
				enemy_degree=random.randint(0,max_degree)
				hue_shift_fixed_size_palette(file,address,enemy_degree,0x0F)
		else:
			enemy_palettes.extend(metroid_palettes)
			enemy_palettes.extend(desgeega_palettes)
			enemy_palettes.extend(sidehopper_palettes)
			enemy_palettes.extend(animal_palettes)
			enemy_degree = random.randint(0,max_degree)
			hue_shift_palette_lists(file,enemy_degree,various_metroid_palettes,various_metroid_length)
			for address in enemy_palettes:
				enemy_degree=random.randint(0,max_degree)
				hue_shift_fixed_size_palette(file,address,enemy_degree,0x0F)
		
	if debug: print(degree_list)
	
	if shift_beam_palettes:
		beam_degree=random.randint(0,max_degree)
		hue_shift_palette_lists(file,beam_degree,beam_palettes,beam_palettes_length)
		hue_shift_palette_lists(file,beam_degree,wave_beam_trail_palettes,wave_beam_trail_length)
		hue_shift_palette_lists(file,beam_degree,grapple_beam_palettes,grapple_beam_length)

	if shift_ship_palette and not shift_suit_palettes:
			if match_ship_and_power:
				ship_degree = 0
			else:
				ship_degree=random.randint(0,max_degree)
			hue_shift_fixed_size_palette(file,ship_palette,ship_degree,0x0F)

	if shift_suit_palettes:	
		base_degree = random.randint(0,max_degree)
	
		for address in power_palette_offsets:
			hue_shift_fixed_size_palette(file, address, base_degree,0x0F)
	
		if match_ship_and_power:
			ship_degree = base_degree
		else:
			ship_degree=random.randint(0,max_degree)
			
		if shift_ship_palette:
			hue_shift_fixed_size_palette(file,ship_palette,ship_degree,0x0F)
	
		if individual_suit_shift:
			degree = random.randint(0,max_degree)
	
		for address in varia_palette_offsets:
			hue_shift_fixed_size_palette(file, address, degree,0x0F)
	
		if individual_suit_shift:
			degree = random.randint(0,max_degree)
		
		for address in gravity_palette_offsets:
			hue_shift_fixed_size_palette(file, address, degree,0x0F)	