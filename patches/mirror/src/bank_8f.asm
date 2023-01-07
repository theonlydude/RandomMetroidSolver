;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

;;; add include for changing scroll set by doors
incsrc "bank_8f_area_door_scroll.asm"

org $8f8000
; room 91F8: Landing Site
Room_91F8_state_9247_PLM:
    ; Scroll PLM
    dw $b703 : db $71 : db $28 : dw Room_91F8_state_9261_PLM_index_0_PLM_scroll_data
    ; Upwards extension
    dw $b647 : db $78 : db $1c : dw $8000 
Door_00_Room_91F8_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $46 : dw $0000 
Door_01_Room_91F8_PLM_C860:
    ; Door. Yellow door facing right
    dw $c860 : db $01 : db $16 : dw $0001 
    ; plms terminates before vanilla
    ; Unknown PLM
    ; dw $0000 : db $01 : db $46 : dw $0000 
    ; Door. Yellow door facing right
    ; dw $c860 : db $01 : db $16 : dw $0001 
    dw $0000
org $8f8026
; room 91F8: Landing Site
Room_91F8_state_9261_PLM:
    ; Scroll PLM
    dw $b703 : db $71 : db $28 : dw Room_91F8_state_9261_PLM_index_0_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $1e : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1e : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1e : db $25 : dw $8000 
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0008 
Door_02_Room_91F8_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $16 : dw $9002 
Door_03_Room_91F8_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $46 : dw $9003 
Door_04_Room_91F8_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $8e : db $26 : dw $9004 
    dw $0000
org $8f8058
; room 92B3: Gauntlet Entrance
Room_92B3_state_92DF_PLM:
    dw $0000
org $8f805a
; room 92FD: Parlor and Alcatraz
Room_92FD_state_932E_PLM:
    ; Scroll PLM
    dw $b703 : db $10 : db $0b : dw Room_92FD_state_9348_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0c : db $0b : dw Room_92FD_state_9348_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $35 : db $0d : dw Room_92FD_state_9348_PLM_index_2_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $2c : db $13 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $2c : db $13 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $2c : db $13 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $36 : db $0b : dw Room_92FD_state_9348_PLM_index_6_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $37 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $38 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $39 : db $0b : dw $8000 
    ; Scroll PLM
    dw $b703 : db $41 : db $07 : dw Room_92FD_state_9348_PLM_index_A_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $42 : db $00 : dw $8000 
    ; Upwards extension
    dw $b647 : db $40 : db $01 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $33 : db $0a : dw Room_92FD_state_9348_PLM_index_D_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $33 : db $09 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $05 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1d : db $0b : dw Room_92FD_state_9348_PLM_index_14_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $13 : db $0b : dw Room_92FD_state_9348_PLM_index_14_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $12 : db $11 : dw Room_92FD_state_9348_PLM_index_15_PLM_scroll_data 
    ; Downwards extension
    dw $b643 : db $0c : db $16 : dw $8000 
    ; Downwards extension
    dw $b643 : db $0c : db $17 : dw $8000 
    ; Downwards extension
    dw $b643 : db $0c : db $18 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0c : db $15 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1b : db $0d : dw Room_92FD_state_9348_PLM_index_1A_PLM_scroll_data 
Door_05_Room_92FD_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $31 : db $36 : dw $0005 
    dw $0000
org $8f8104
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM:
    ; Scroll PLM
    dw $b703 : db $10 : db $0b : dw Room_92FD_state_9348_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0c : db $0b : dw Room_92FD_state_9348_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $35 : db $0d : dw Room_92FD_state_9348_PLM_index_2_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $17 : db $0d : dw $8000 
    ; Rightwards extension
    dw $b63b : db $18 : db $0d : dw $8000 
    ; Rightwards extension
    dw $b63b : db $19 : db $0d : dw $8000 
    ; Scroll PLM
    dw $b703 : db $36 : db $0b : dw Room_92FD_state_9348_PLM_index_6_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $37 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $39 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $38 : db $0b : dw $8000 
    ; Scroll PLM
    dw $b703 : db $41 : db $07 : dw Room_92FD_state_9348_PLM_index_A_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $0b : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $01 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $33 : db $0a : dw Room_92FD_state_9348_PLM_index_D_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $33 : db $09 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $33 : db $05 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1d : db $0b : dw Room_92FD_state_9348_PLM_index_14_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $13 : db $0b : dw Room_92FD_state_9348_PLM_index_14_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $12 : db $11 : dw Room_92FD_state_9348_PLM_index_15_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $3b : db $11 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $3c : db $11 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $3d : db $11 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $3e : db $11 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1b : db $0d : dw Room_92FD_state_9348_PLM_index_1A_PLM_scroll_data 
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $000a 
Door_06_Room_92FD_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $4e : db $06 : dw $9006 
Door_07_Room_92FD_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $3e : db $26 : dw $9007 
Door_08_Room_92FD_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $31 : db $36 : dw $9008 
Door_09_Room_92FD_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $3e : db $36 : dw $9009 
Door_0A_Room_92FD_PLM_C84E:
    ; Door. Grey door facing up
    dw $c84e : db $36 : db $4d : dw $900a 
    dw $0000
org $8f81cc
; room 93AA: Crateria Power Bomb Room
Room_93AA_state_93B7_PLM:
    ; Power bomb tank
    dw $eee3 : db $02 : db $07 : dw $0000 
    dw $0000
org $8f81d4
; room 93D5: [Parlor Save Room]
Room_93D5_state_93E2_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0001 
    dw $0000
org $8f81dc
; room 93FE: West Ocean
Room_93FE_state_940B_PLM:
Door_0B_Room_93FE_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $21 : db $36 : dw $900b 
Door_0C_Room_93FE_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $46 : dw $000c 
    ; Missile tank
    dw $eedb : db $7d : db $5b : dw $0001 
    ; Missile tank, shot block
    dw $ef83 : db $63 : db $03 : dw $0002 
    ; Missile tank
    dw $eedb : db $7e : db $2f : dw $0003 
    dw $0000
org $8f81fc
; room 9461: Bowling Alley Path
Room_9461_state_946E_PLM:
    dw $0000
org $8f81fe
; room 948C: Crateria Keyhunter Room
Room_948C_state_9499_PLM:
    ; Scroll PLM
    dw $b703 : db $17 : db $0f : dw $94c2 
    ; Rightwards extension
    dw $b63b : db $18 : db $0f : dw $8000 
    ; Scroll PLM
    dw $b703 : db $16 : db $0c : dw $94c7 
    ; Rightwards extension
    dw $b63b : db $17 : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $18 : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $19 : db $0c : dw $8000 
Door_0D_Room_948C_PLM_C860:
    ; Door. Yellow door facing right
    dw $c860 : db $01 : db $06 : dw $000d 
Door_0E_Room_948C_PLM_C866:
    ; Door. Yellow door facing up
    dw $c866 : db $16 : db $2d : dw $000e 
    dw $0000
org $8f8230
; room 94CC: [Elevator to Maridia]
Room_94CC_state_94D9_PLM:
    ; Scroll PLM
    dw $b703 : db $08 : db $0d : dw $94fa 
    dw $0000
org $8f8238
; room 94FD: East Ocean
Room_94FD_state_950A_PLM:
    dw $0000
org $8f823a
; room 9552: Forgotten Highway Kago Room
Room_9552_state_955F_PLM:
    dw $0000
org $8f823c
; room 957D: Crab Maze
Room_957D_state_958A_PLM:
    dw $0000
org $8f823e
; room 95A8: [Crab Maze to Elevator]
Room_95A8_state_95B5_PLM:
Door_0F_Room_95A8_PLM_C866:
    ; Door. Yellow door facing up
    dw $c866 : db $06 : db $0d : dw $000f 
    dw $0000
org $8f8246
; room 95D4: Crateria Tube
Room_95D4_state_95E1_PLM:
    dw $0000
org $8f8248
; room 95FF: The Moat
Room_95FF_state_960C_PLM:
    ; Missile tank
    dw $eedb : db $11 : db $09 : dw $0004 
    dw $0000
org $8f8250
; room 962A: [Elevator to Red Brinstar]
Room_962A_state_9637_PLM:
    ; Scroll PLM
    dw $b703 : db $08 : db $0d : dw $9658 
Door_10_Room_962A_PLM_C86C:
    ; Door. Yellow door facing down
    dw $c86c : db $06 : db $02 : dw $0010 
    dw $0000
org $8f825e
; room 965B: Gauntlet Energy Tank Room
Room_965B_state_9668_PLM:
    ; Scroll PLM
    dw $b703 : db $0b : db $00 : dw Room_965B_state_9668_PLM_index_0_PLM_scroll_data
    ; Energy tank
    dw $eed7 : db $0c : db $08 : dw $0005 
    dw $0000
org $8f826c
; room 968F: [West Ocean Geemer Corridor]
Room_968F_state_969C_PLM:
    dw $0000
org $8f826e
; room 96BA: Climb
Room_96BA_state_96EB_PLM:
    ; Scroll PLM
    dw $b703 : db $12 : db $05 : dw Room_96BA_state_9705_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $02 : db $05 : dw Room_96BA_state_9705_PLM_scroll_data_FS
    ; Scroll PLM
    dw $b703 : db $12 : db $76 : dw Room_96BA_state_9705_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $02 : db $76 : dw Room_96BA_state_9705_PLM_scroll_data_FS
    ; Rightwards extension
    dw $b63b : db $1d : db $85 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1c : db $85 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $85 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $86 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $87 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $88 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1b : db $89 : dw Room_96BA_state_9705_PLM_index_A_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $26 : db $7a : dw $8000 
    ; Upwards extension
    dw $b647 : db $25 : db $7c : dw $8000 
    ; Upwards extension
    dw $b647 : db $27 : db $7d : dw $8000 
    ; Scroll PLM
    dw $b703 : db $20 : db $86 : dw Room_96BA_state_9705_PLM_index_E_PLM_scroll_data
    ; Upwards extension
    dw $b647 : db $0d : db $86 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $87 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $88 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $23 : db $89 : dw Room_96BA_state_9705_PLM_index_12_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $08 : db $86 : dw $8000 
    ; Upwards extension
    dw $b647 : db $08 : db $87 : dw $8000 
    ; Upwards extension
    dw $b647 : db $08 : db $88 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $81 : dw Room_96BA_PLM_scroll_data_FS
Door_11_Room_96BA_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $9011 
Door_12_Room_96BA_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $2e : db $86 : dw $9012 
Door_13_Room_96BA_PLM_C860:
    ; Door. Yellow door facing right
    dw $c860 : db $01 : db $76 : dw $0013 
    dw $0000
org $8f830c
; room 96BA: Climb
Room_96BA_state_9705_PLM:
    ; Scroll PLM
    dw $b703 : db $12 : db $05 : dw Room_96BA_state_9705_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $02 : db $05 : dw Room_96BA_state_9705_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $12 : db $76 : dw Room_96BA_state_9705_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $02 : db $76 : dw Room_96BA_state_9705_PLM_index_3_PLM_scroll_data 
    ; Leftwards extension
    dw $b63f : db $08 : db $83 : dw $8000 
    ; Leftwards extension
    dw $b63f : db $23 : db $83 : dw $8000 
    ; Upwards extension
    dw $b647 : db $11 : db $86 : dw $8000 
    ; Upwards extension
    dw $b647 : db $11 : db $89 : dw $8000 
    ; Upwards extension
    dw $b647 : db $11 : db $87 : dw $8000 
    ; Upwards extension
    dw $b647 : db $11 : db $88 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1b : db $89 : dw Room_96BA_state_9705_PLM_index_A_PLM_scroll_data 
    ; Downwards extension
    dw $b643 : db $23 : db $83 : dw $8000 
    ; Downwards extension
    dw $b643 : db $23 : db $83 : dw $8000 
    ; Downwards extension
    dw $b643 : db $23 : db $83 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $20 : db $86 : dw Room_96BA_state_9705_PLM_index_E_PLM_scroll_data 
    ; Downwards extension
    dw $b643 : db $23 : db $83 : dw $8000 
    ; Downwards extension
    dw $b643 : db $23 : db $83 : dw $8000 
    ; Downwards extension
    dw $b643 : db $23 : db $83 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $23 : db $89 : dw Room_96BA_state_9705_PLM_index_12_PLM_scroll_data 
    ; Downwards extension
    dw $b643 : db $23 : db $83 : dw $8000 
    ; Upwards extension
    dw $b647 : db $10 : db $88 : dw $8000 
    ; Upwards extension
    dw $b647 : db $10 : db $89 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $86 : dw Room_96BA_PLM_scroll_data_FS
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $000c 
Door_14_Room_96BA_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $9014 
Door_15_Room_96BA_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $76 : dw $9015 
Door_16_Room_96BA_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $2e : db $86 : dw $9016 
Door_17_Room_96BA_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $11 : db $86 : dw $9017 
    dw $0000
org $8f83b6
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_state_976D_PLM:
    ; Scroll PLM
    dw $b703 : db $2b : db $0f : dw Room_975C_state_9787_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $29 : db $0f : dw Room_975C_state_9787_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $2a : db $09 : dw Room_975C_state_9787_PLM_index_2_PLM_scroll_data 
Door_18_Room_975C_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $2e : db $06 : dw $9018 
    dw $0000
org $8f83d0
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_state_9787_PLM:
    ; Scroll PLM
    dw $b703 : db $2b : db $0f : dw Room_975C_state_9787_PLM_scroll_data_FS_1
    ; Scroll PLM
    dw $b703 : db $29 : db $0f : dw Room_975C_state_9787_PLM_scroll_data_FS_1
    ; Scroll PLM
    dw $b703 : db $2a : db $09 : dw Room_975C_state_9787_PLM_scroll_data_FS_2
Door_19_Room_975C_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $2e : db $06 : dw $0c19 
Door_1A_Room_975C_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c1a 
    ; Missile tank
    dw $eedb : db $2a : db $1a : dw $0006 
    dw $0000
org $8f83f6
; room 97B5: [Elevator to Blue Brinstar]
Room_97B5_state_97E0_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $0d : dw $9801 
    dw $0000
org $8f83fe
; room 9804: Bomb Torizo Room
Room_9804_state_9835_PLM:
Door_1B_Room_9804_PLM_BAF4:
    ; Bomb Torizo grey door
    dw $BAF4 : db $0e : db $06 : dw $081b
    ; Bombs, chozo orb
    dw $ef3b : db $06 : db $0a : dw $0007 
    ; Bomb Torizo's crumbling chozo
    dw $d6ea : db $07 : db $0b : dw $0000 
    dw $0000
org $8f8412
; room 9804: Bomb Torizo Room
Room_9804_state_984F_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $000e 
Door_1C_Room_9804_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $0e : db $06 : dw $181c 
    dw $0000
org $8f8420
; room 9879: Flyway
Room_9879_state_98AA_PLM:
Door_1D_Room_9879_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $06 : dw $001d 
    dw $0000
org $8f8428
; room 9879: Flyway
Room_9879_state_98C4_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0010 
    dw $0000
org $8f8430
; room 98E2: Pre-Map Flyway
Room_98E2_state_98EF_PLM:
    dw $0000
org $8f8432
; room 990D: Terminator Room
Room_990D_state_991A_PLM:
    ; Energy tank
    dw $eed7 : db $58 : db $2a : dw $0008 
    dw $0000
org $8f843a
; room 9938: [Elevator to Green Brinstar]
Room_9938_state_9945_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $0d : dw $9966 
    dw $0000
org $8f8442
; room 9969: Lower Mushrooms
Room_9969_state_9976_PLM:
    dw $0000
org $8f8444
; room 9994: Crateria Map Room
Room_9994_state_99A1_PLM:
    ; Map station
    dw $b6d3 : db $05 : db $0a : dw $8000 
    dw $0000
org $8f844c
; room 99BD: Green Pirates Shaft
Room_99BD_state_99CA_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $43 : dw $99f3 
    ; Rightwards extension
    dw $b63b : db $08 : db $43 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $05 : db $46 : dw $99f6 
    ; Rightwards extension
    dw $b63b : db $06 : db $46 : dw $8000 
    ; Missile tank
    dw $eedb : db $0d : db $1b : dw $0009 
    ; Missile tank
    dw $eedb : db $02 : db $1b : dw $000a 
Door_1E_Room_99BD_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $66 : dw $001e 
    dw $0000
org $8f8478
; room 99F9: Crateria Super Room
Room_99F9_state_9A06_PLM:
    ; Super missile tank
    dw $eedf : db $04 : db $09 : dw $000b 
    dw $0000
org $8f8480
; room 9A44: Final Missile Bombway
Room_9A44_state_9A56_PLM:
    dw $0000
org $8f8482
; room 9A44: Final Missile Bombway
Room_9A44_state_9A70_PLM:
    dw $0000
org $8f8484
; room 9A90: The Final Missile
Room_9A90_state_9AA2_PLM:
    dw $0000
org $8f8486
; room 9A90: The Final Missile
Room_9A90_state_9ABC_PLM:
    ; Missile tank
    dw $eedb : db $0b : db $07 : dw $000c 
    dw $0000
org $8f848e
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_state_9AE6_PLM:
    ; Scroll PLM
    dw $b703 : db $35 : db $70 : dw Room_9AD9_state_9AE6_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $2f : db $a8 : dw Room_9AD9_state_9AE6_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $1e : db $a8 : dw Room_9AD9_state_9AE6_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $32 : db $ac : dw Room_9AD9_state_9AE6_PLM_index_3_PLM_scroll_data 
    ; Elevator platform
    dw $b70b : db $36 : db $2c : dw $8000 
    ; Power bomb tank, chozo orb
    dw $ef37 : db $03 : db $7a : dw $000d 
Door_1F_Room_9AD9_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $3e : db $56 : dw $001f 
Door_21_Room_9AD9_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $31 : db $46 : dw $0021
Door_20_Room_9AD9_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $3e : db $46 : dw $0020
Door_23_Room_9AD9_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $3e : db $66 : dw $0023
Door_22_Room_9AD9_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $31 : db $66 : dw $0022
Door_24_Room_9AD9_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $31 : db $76 : dw $9024 
    dw $0000
org $8f84d8
; room 9B5B: Spore Spawn Super Room
Room_9B5B_state_9B68_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $0b : dw Room_9B5B_state_9B68_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $08 : db $0b : dw $8000 
    ; Super missile tank, chozo orb
    dw $ef33 : db $05 : db $87 : dw $000e 
    dw $0000
org $8f84ec
; room 9B9D: Brinstar Pre-Map Room
Room_9B9D_state_9BAA_PLM:
Door_25_Room_9B9D_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c25 
    dw $0000
org $8f84f4
; room 9BC8: Early Supers Room
Room_9BC8_state_9BD5_PLM:
    ; Scroll PLM
    dw $b703 : db $04 : db $0e : dw $9bf9 
    ; Rightwards extension
    dw $b63b : db $06 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $05 : db $0e : dw $8000 
    ; Scroll PLM
    dw $b703 : db $2b : db $13 : dw $9c00 
    ; Scroll PLM
    dw $b703 : db $04 : db $10 : dw $9bf9 
Door_26_Room_9BC8_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $16 : dw $0026 
    ; Missile tank
    dw $eedb : db $1c : db $1b : dw $000f 
    ; Super missile tank
    dw $eedf : db $2b : db $06 : dw $0010 
    dw $0000
org $8f8526
; room 9C07: Brinstar Reserve Tank Room
Room_9C07_state_9C14_PLM:
    ; Scroll PLM
    dw $b703 : db $11 : db $0b : dw Room_9C07_state_9C14_PLM_index_0_PLM_scroll_data 
    ; Reserve tank, chozo orb
    dw $ef7b : db $14 : db $07 : dw $0011 
    ; Missile tank, shot block
    dw $ef83 : db $01 : db $07 : dw $0012 
    ; Missile tank
    dw $eedb : db $06 : db $07 : dw $0013 
    dw $0000
org $8f8540
; room 9C35: Brinstar Map Room
Room_9C35_state_9C42_PLM:
    ; Map station
    dw $b6d3 : db $0b : db $0a : dw $8000 
    dw $0000
org $8f8548
; room 9C5E: Green Brinstar Fireflea Room
Room_9C5E_state_9C6B_PLM:
Door_27_Room_9C5E_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $26 : dw $0027 
    dw $0000
org $8f8550
; room 9C89: [Green Brinstar Missile Station]
Room_9C89_state_9C96_PLM:
    ; Missile station
    dw $b6eb : db $0b : db $0a : dw $0014 
    dw $0000
org $8f8558
; room 9CB3: Dachora Room
Room_9CB3_state_9CC0_PLM:
    ; Downwards extension
    dw $b643 : db $38 : db $01 : dw $8000 
    ; Leftwards extension
    dw $b63f : db $35 : db $01 : dw $8000 
    ; Leftwards extension
    dw $b63f : db $34 : db $01 : dw $8000 
    ; Leftwards extension
    dw $b63f : db $33 : db $01 : dw $8000 
    ; Leftwards extension
    dw $b63f : db $32 : db $01 : dw $8000 
    ; Leftwards extension
    dw $b63f : db $31 : db $01 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $25 : db $0d : dw Room_9CB3_state_9CC0_PLM_index_6_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $39 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $3a : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $3b : db $01 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $2f : db $0b : dw Room_9CB3_state_9CC0_PLM_index_A_PLM_scroll_data 
    ; Downwards extension
    dw $b643 : db $36 : db $01 : dw $8000 
    ; Downwards extension
    dw $b643 : db $37 : db $01 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $48 : db $38 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $47 : db $38 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $6d : db $06 : dw Room_9CB3_PLM_scroll_data_FS
    ; Rightwards extension
    dw $b63b : db $41 : db $01 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $40 : db $01 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $3f : db $01 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $3e : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $3c : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $3d : db $01 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $24 : db $0b : dw Room_9CB3_state_9CC0_PLM_index_A_PLM_scroll_data 
    dw $0000
org $8f85e4
; room 9D19: Big Pink
Room_9D19_state_9D26_PLM:
    ; Scroll PLM
    dw $b703 : db $21 : db $6b : dw Room_9D19_state_9D26_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $2f : db $7a : dw Room_9D19_state_9D26_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $12 : db $57 : dw Room_9D19_state_9D26_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0f : db $57 : dw Room_9D19_state_9D26_PLM_index_3_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $30 : db $08 : dw Room_9D19_state_9D26_PLM_index_4_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $2e : db $08 : dw Room_9D19_state_9D26_PLM_index_5_PLM_scroll_data 
    ; Missile tank
    dw $eedb : db $2b : db $32 : dw $0015 
    ; Missile tank
    dw $eedb : db $2d : db $67 : dw $0016 
    ; Charge beam, chozo orb
    dw $ef3f : db $2a : db $76 : dw $0017 
Door_28_Room_9D19_PLM_C860:
    ; Door. Yellow door facing right
    dw $c860 : db $11 : db $46 : dw $0028 
Door_29_Room_9D19_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $11 : db $66 : dw $0029 
Door_2A_Room_9D19_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $11 : db $06 : dw $002a 
Door_2B_Room_9D19_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $4e : db $96 : dw $002b 
    dw $0000
org $8f8634
; room 9D9C: Spore Spawn Keyhunter Room
Room_9D9C_state_9DA9_PLM:
Door_2C_Room_9D9C_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $3e : db $06 : dw $0c2c 
Door_2D_Room_9D9C_PLM_C854:
    ; Door. Grey door facing down
    dw $c854 : db $06 : db $03 : dw $0c2d 
    dw $0000
org $8f8642
; room 9DC7: Spore Spawn Room
Room_9DC7_state_9DF3_PLM:
Door_2E_Room_9DC7_PLM_C87E:
    ; Door. Green door facing up
    dw $c87e : db $06 : db $2e : dw $002e 
    dw $0000
org $8f864a
; room 9E11: Pink Brinstar Power Bomb Room
Room_9E11_state_9E1E_PLM:
    ; Scroll PLM
    dw $b703 : db $17 : db $0e : dw Room_9E11_state_9E1E_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $17 : db $0b : dw $9e49 
Door_2F_Room_9E11_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c2f 
    ; Power bomb tank
    dw $eee3 : db $19 : db $17 : dw $0018 
    dw $0000
org $8f8664
; room 9E52: Green Hill Zone
Room_9E52_state_9E5F_PLM:
    ; Downwards closed gate
    dw $c82a : db $1b : db $37 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $1b : db $37 : dw $0002 
Door_30_Room_9E52_PLM_C860:
    ; Door. Yellow door facing right
    dw $c860 : db $61 : db $06 : dw $0030 
    ; Missile tank
    dw $eedb : db $42 : db $18 : dw $0019 
    dw $0000
org $8f867e
; room 9E9F: Morph Ball Room
Room_9E9F_state_9EB1_PLM:
    ; Scroll PLM
    dw $b703 : db $60 : db $2b : dw Room_9E9F_state_9ECB_PLM_index_0_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $77 : db $23 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $24 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $25 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $28 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $29 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $2a : dw $8000 
    ; Scroll PLM
    dw $b703 : db $77 : db $2b : dw Room_9E9F_state_9ECB_PLM_index_9_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $28 : db $21 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $25 : dw Room_9E9F_state_9ECB_PLM_index_F_PLM_scroll_data
    ; Rightwards extension
    dw $b63b : db $28 : db $0a : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $0a : dw Room_9E9F_state_9ECB_PLM_index_D_PLM_scroll_data
    ; Rightwards extension
    dw $b63b : db $28 : db $25 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $21 : dw Room_9E9F_state_9ECB_PLM_index_D_PLM_scroll_data
    ; Morph ball
    dw $ef23 : db $3a : db $29 : dw $001a 
    dw $0000
org $8f86e6
; room 9E9F: Morph Ball Room
Room_9E9F_state_9ECB_PLM:
    ; Scroll PLM
    dw $b703 : db $60 : db $2b : dw Room_9E9F_state_9ECB_PLM_index_0_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $77 : db $23 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $24 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $25 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $28 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $29 : dw $8000 
    ; Upwards extension
    dw $b647 : db $77 : db $2a : dw $8000 
    ; Scroll PLM
    dw $b703 : db $77 : db $2b : dw Room_9E9F_state_9ECB_PLM_index_9_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $28 : db $21 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $21 : dw Room_9E9F_state_9ECB_PLM_index_D_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $28 : db $0a : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $0a : dw Room_9E9F_state_9ECB_PLM_index_D_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $28 : db $26 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $27 : db $26 : dw Room_9E9F_state_9ECB_PLM_index_F_PLM_scroll_data 
Door_31_Room_9E9F_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $7e : db $26 : dw $0c31 
    ; Power bomb tank
    dw $eee3 : db $57 : db $2a : dw $001b 
    dw $0000
org $8f8754
; room 9F11: Construction Zone
Room_9F11_state_9F3D_PLM:
    ; Scroll PLM
    dw $b703 : db $04 : db $0b : dw $9f5f 
    ; Rightwards extension
    dw $b63b : db $05 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $06 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $07 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $08 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $09 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0b : db $0b : dw $8000 
Door_32_Room_9F11_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $06 : dw $0032 
    dw $0000
org $8f878c
; room 9F64: Blue Brinstar Energy Tank Room
Room_9F64_state_9F90_PLM:
    ; Scroll PLM
    dw $b703 : db $08 : db $0b : dw Room_9F64_state_9F90_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $08 : db $25 : dw Room_9F64_state_9F90_PLM_index_1_PLM_scroll_data 
    ; Missile tank
    dw $eedb : db $01 : db $29 : dw $001c 
    ; Energy tank, shot block
    dw $ef7f : db $13 : db $22 : dw $001d 
    dw $0000
org $8f87a6
; room 9FBA: Noob Bridge
Room_9FBA_state_9FC7_PLM:
Door_33_Room_9FBA_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $06 : dw $0033 
    dw $0000
org $8f87ae
; room 9FE5: Green Brinstar Beetom Room
Room_9FE5_state_9FF2_PLM:
    dw $0000
org $8f87b0
; room A011: Etecoon Energy Tank Room
Room_A011_state_A01E_PLM:
    ; Scroll PLM
    dw $b703 : db $47 : db $0b : dw Room_A011_state_A01E_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $26 : db $06 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $21 : db $04 : dw $8000 
    ; Energy tank
    dw $eed7 : db $49 : db $09 : dw $001e 
Door_34_Room_A011_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $4e : db $06 : dw $0034 
    dw $0000
org $8f87d0
; room A051: Etecoon Super Room
Room_A051_state_A05E_PLM:
    ; Super missile tank
    dw $eedf : db $08 : db $09 : dw $001f 
    dw $0000
org $8f87d8
; room A07B: [Dachora Room Energy Charge Station]
Room_A07B_state_A088_PLM:
    ; Energy station
    dw $b6df : db $0b : db $0a : dw $0020 
    dw $0000
org $8f87e0
; room A0A4: Spore Spawn Farming Room
Room_A0A4_state_A0B1_PLM:
Door_35_Room_A0A4_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $2e : db $06 : dw $0035 
    dw $0000
org $8f87e8
; room A0D2: Waterway Energy Tank Room
Room_A0D2_state_A0DF_PLM:
    ; Upwards extension
    dw $b647 : db $60 : db $09 : dw $8000 
    ; Upwards extension
    dw $b647 : db $60 : db $0a : dw $8000 
    ; Scroll PLM
    dw $b703 : db $60 : db $0b : dw Room_A0D2_state_A0DF_PLM_index_2_PLM_scroll_data 
    ; Energy tank
    dw $eed7 : db $6b : db $09 : dw $0021 
    dw $0000
org $8f8802
; room A107: First Missile Room
Room_A107_state_A114_PLM:
    ; Missile tank, chozo orb
    dw $ef2f : db $0b : db $07 : dw $0022 
    dw $0000
org $8f880a
; room A130: Pink Brinstar Hopper Room
Room_A130_state_A13D_PLM:
    ; Downwards closed gate
    dw $c82a : db $0e : db $04 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $0e : db $04 : dw $0000 
Door_36_Room_A130_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $16 : dw $0c36 
Door_37_Room_A130_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $1e : db $16 : dw $0c37 
    dw $0000
org $8f8824
; room A15B: Hopper Energy Tank Room
Room_A15B_state_A168_PLM:
    ; Energy tank
    dw $eed7 : db $04 : db $09 : dw $0023 
    dw $0000
org $8f882c
; room A184: [Spore Spawn Save Room]
Room_A184_state_A191_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0000 
    dw $0000
org $8f8834
; room A1AD: Blue Brinstar Boulder Room
Room_A1AD_state_A1BA_PLM:
    dw $0000
org $8f8836
; room A1D8: Blue Brinstar Double Missile Room
Room_A1D8_state_A1E5_PLM:
    ; Missile tank
    dw $eedb : db $08 : db $09 : dw $0024 
    ; Missile tank, shot block
    dw $ef83 : db $0a : db $0c : dw $0025 
    dw $0000
org $8f8844
; room A201: [Green Brinstar Main Shaft Save Room]
Room_A201_state_A20E_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0001 
    dw $0000
org $8f884c
; room A22A: [Etecoon Save Room]
Room_A22A_state_A237_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0002 
    dw $0000
org $8f8854
; room A253: Red Tower
Room_A253_state_A260_PLM:
    ; Scroll PLM
    dw $b703 : db $05 : db $6a : dw Room_A253_state_A260_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $06 : db $6a : dw $8000 
Door_38_Room_A253_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $0e : db $96 : dw $0038 
Door_39_Room_A253_PLM_C85A:
    ; Door. Yellow door facing left
    dw $c85a : db $0e : db $66 : dw $0039 
    dw $0000
org $8f886e
; room A293: Red Brinstar Fireflea Room
Room_A293_state_A2A0_PLM:
Door_3A_Room_A293_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $7e : db $06 : dw $003a 
    dw $0000
org $8f8876
; room A2CE: X-Ray Scope Room
Room_A2CE_state_A2DB_PLM:
    ; X-ray scope, chozo orb
    dw $ef63 : db $1a : db $07 : dw $0026 
    dw $0000
org $8f887e
; room A2F7: Hellway
Room_A2F7_state_A304_PLM:
    dw $0000
org $8f8880
; room A322: Caterpillar Room
Room_A322_state_A32F_PLM:
    ; Scroll PLM
    dw $b703 : db $29 : db $5e : dw Room_A322_state_A32F_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $2a : db $5e : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1f : db $3b : dw Room_A322_state_A32F_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $22 : db $37 : dw $a379 
    ; Elevator platform
    dw $b70b : db $26 : db $2c : dw $8000 
    ; Downwards closed gate
    dw $c82a : db $09 : db $35 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $09 : db $35 : dw $0008 
Door_3B_Room_A322_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $2e : db $36 : dw $003b 
Door_3C_Room_A322_PLM_C85A:
    ; Door. Yellow door facing left
    dw $c85a : db $2e : db $56 : dw $003c 
Door_3D_Room_A322_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $2e : db $76 : dw $003d 
    dw $0000
org $8f88be
; room A37C: Beta Power Bomb Room
Room_A37C_state_A389_PLM:
    ; Scroll PLM
    dw $b703 : db $17 : db $0e : dw Room_A37C_state_A389_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $18 : db $0e : dw $8000 
    ; Power bomb tank
    dw $eee3 : db $1b : db $13 : dw $0027 
Door_3E_Room_A37C_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c3e 
    dw $0000
org $8f88d8
; room A3AE: Alpha Power Bomb Room
Room_A3AE_state_A3BB_PLM:
    ; Upwards extension
    dw $b647 : db $12 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $13 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $14 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $15 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $16 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $11 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $10 : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0f : db $01 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $20 : db $0c : dw Room_A3AE_state_A3BB_PLM_index_8_PLM_scroll_data 
    ; Power bomb tank, chozo orb
    dw $ef37 : db $1b : db $09 : dw $0028 
    ; Missile tank
    dw $eedb : db $2d : db $08 : dw $0029 
    dw $0000
org $8f891c
; room A3DD: Bat Room
Room_A3DD_state_A3EA_PLM:
    dw $0000
org $8f891e
; room A408: Below Spazer
Room_A408_state_A415_PLM:
    ; Scroll PLM
    dw $b703 : db $17 : db $11 : dw $a439 
    ; Rightwards extension
    dw $b63b : db $0d : db $11 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0e : db $11 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0f : db $11 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $17 : db $14 : dw $a43e 
    ; Rightwards extension
    dw $b63b : db $0d : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0e : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0f : db $14 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $0c : db $11 : dw $a439 
    ; Scroll PLM
    dw $b703 : db $0c : db $14 : dw $a43e 
    ; Scroll PLM
    dw $b703 : db $1d : db $11 : dw $a439 
    ; Scroll PLM
    dw $b703 : db $1d : db $14 : dw $a43e 
Door_3F_Room_A408_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $06 : dw $003f 
    dw $0000
org $8f896e
; room A447: Spazer Room
Room_A447_state_A454_PLM:
    ; Spazer beam, chozo orb
    dw $ef53 : db $04 : db $09 : dw $002a 
    dw $0000
org $8f8976
; room A471: Warehouse Zeela Room
Room_A471_state_A47E_PLM:
    ; Scroll PLM
    dw $b703 : db $1d : db $0b : dw Room_A471_state_A47E_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $1d : db $19 : dw Room_A471_state_A47E_PLM_index_3_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0a : db $19 : dw Room_A471_state_A47E_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $18 : db $19 : dw Room_A471_state_A47E_PLM_index_3_PLM_scroll_data 
Door_40_Room_A471_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $1e : db $16 : dw $0040 
    dw $0000
org $8f8996
; room A4B1: Warehouse Energy Tank Room
Room_A4B1_state_A4BE_PLM:
Door_41_Room_A4B1_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c41 
    ; Energy tank, shot block
    dw $ef7f : db $0a : db $04 : dw $002b 
    dw $0000
org $8f89a4
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_state_A4E7_PLM:
    ; Scroll PLM
    dw $b703 : db $28 : db $0b : dw Room_A4DA_state_A4E7_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $28 : db $0e : dw Room_A4DA_state_A4E7_PLM_index_1_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $34 : db $04 : dw $8000 
    ; Upwards extension
    dw $b647 : db $34 : db $05 : dw $8000 
    ; Upwards extension
    dw $b647 : db $34 : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $34 : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $34 : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $34 : db $09 : dw $8000 
    ; Upwards extension
    dw $b647 : db $34 : db $0a : dw $8000 
    ; Scroll PLM
    dw $b703 : db $34 : db $0b : dw Room_A4DA_state_A4E7_PLM_index_9_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $18 : db $0c : dw Room_A4DA_state_A4E7_PLM_index_B_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $11 : db $0c : dw Room_A4DA_state_A4E7_PLM_index_B_PLM_scroll_data 
    ; Missile tank, shot block
    dw $ef83 : db $11 : db $08 : dw $002c 
    dw $0000
org $8f89f4
; room A521: Baby Kraid Room
Room_A521_state_A54D_PLM:
Door_42_Room_A521_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $5e : db $06 : dw $0c42 
Door_43_Room_A521_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c43 
    dw $0000
org $8f8a02
; room A56B: Kraid Eye Door Room
Room_A56B_state_A578_PLM:
    ; Scroll PLM
    dw $b703 : db $1a : db $12 : dw Room_A56B_state_A578_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $1b : db $12 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1c : db $12 : dw $8000 
Door_44_Room_A56B_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $11 : db $06 : dw $0044 
Door_45_Room_A56B_PLM_DB4C:
    ; Door. Eye door, facing right
    dw $db4c : db $01 : db $16 : dw $0045 
    ; Eye door bottom, facing right
    dw $db52 : db $01 : db $19 : dw $0045 
    ; Eye door eye, facing right
    dw $db48 : db $01 : db $17 : dw $0045 
    dw $0000
org $8f8a2e
; room A59F: Kraid Room
Room_A59F_state_A5CB_PLM:
Door_46_Room_A59F_PLM_C848:     ; door to varia
    ; Door. Grey door facing left
    dw $c848 : db $01 : db $16 : dw $0046 
Door_47_Room_A59F_PLM_C842:     ; door to warehouse
    ; Door. Grey door facing right
    dw $c842 : db $1e : db $16 : dw $0047 
    dw $0000
org $8f8a3c
; room A5ED: Statues Hallway
Room_A5ED_state_A5FA_PLM:
    dw $0000
org $8f8a3e
; room A618: [Red Tower Energy Charge Station]
Room_A618_state_A625_PLM:
    ; Energy station
    dw $b6df : db $0b : db $0a : dw $002d 
    dw $0000
org $8f8a46
; room A641: [Kraid Recharge Station]
Room_A641_state_A64E_PLM:
    ; Missile station
    dw $b6eb : db $06 : db $0a : dw $002e 
    ; Energy station
    dw $b6df : db $08 : db $0a : dw $002f 
    dw $0000
org $8f8a54
; room A66A: Statues Room
Room_A66A_state_A677_PLM:
Door_48_Room_A66A_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $0e : db $06 : dw $9448 
    dw $0000
org $8f8a5c
; room A6A1: Warehouse Entrance
Room_A6A1_state_A6AE_PLM:
    ; Scroll PLM
    dw $b703 : db $27 : db $0c : dw Room_A6A1_state_A6AE_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $28 : db $0c : dw $8000 
    ; Scroll PLM
    dw $b703 : db $02 : db $06 : dw Room_A6A1_state_A6AE_PLM_index_2_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $1f : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1f : db $07 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1c : db $0b : dw Room_A6A1_state_A6AE_PLM_index_5_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $1d : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1d : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1d : db $06 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1d : db $09 : dw Room_A6A1_state_A6AE_PLM_index_9_PLM_scroll_data 
    ; Leftwards extension
    dw $b63f : db $1b : db $0b : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $0a : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $09 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $05 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1b : db $04 : dw $8000 
    dw $0000
org $8f8aca
; room A6E2: Varia Suit Room
Room_A6E2_state_A6EF_PLM:
    ; Varia suit, chozo orb
    dw $ef5b : db $07 : db $09 : dw $0030 
    dw $0000
org $8f8ad2
; room A70B: [Kraid Save Room]
Room_A70B_state_A718_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0003 
    dw $0000
org $8f8ada
; room A734: [Caterpillar Save Room]
Room_A734_state_A741_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0004 
    dw $0000
org $8f8ae2
; room A75D: Ice Beam Acid Room
Room_A75D_state_A76A_PLM:
    dw $0000
org $8f8ae4
; room A788: Cathedral
Room_A788_state_A795_PLM:
    ; Missile tank, shot block
    dw $ef83 : db $0d : db $1c : dw $0031 
Door_49_Room_A788_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $16 : dw $0049 
    dw $0000
org $8f8af2
; room A7B3: Cathedral Entrance
Room_A7B3_state_A7C0_PLM:
Door_4A_Room_A7B3_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $06 : dw $004a 
    dw $0000
org $8f8afa
; room A7DE: Business Center
Room_A7DE_state_A7EB_PLM:
    ; Elevator platform
    dw $b70b : db $06 : db $2c : dw $8000 
Door_4B_Room_A7DE_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $0e : db $36 : dw $004b 
Door_4C_Room_A7DE_PLM_C85A:
    ; Door. Yellow door facing left
    dw $c85a : db $0e : db $46 : dw $004c 
Door_4D_Room_A7DE_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $0e : db $56 : dw $004d 
    dw $0000
org $8f8b14
; room A815: Ice Beam Gate Room
Room_A815_state_A822_PLM:
    ; Scroll PLM
    dw $b703 : db $37 : db $2d : dw $a860 
    ; Rightwards extension
    dw $b63b : db $38 : db $2d : dw $8000 
    dw $0000
org $8f8b22
; room A865: Ice Beam Tutorial Room
Room_A865_state_A872_PLM:
    dw $0000
org $8f8b24
; room A890: Ice Beam Room
Room_A890_state_A89D_PLM:
    ; Ice beam, chozo orb
    dw $ef43 : db $03 : db $07 : dw $0032 
    dw $0000
org $8f8b2c
; room A8B9: Ice Beam Snake Room
Room_A8B9_state_A8C6_PLM:
    ; Scroll PLM
    dw $b703 : db $02 : db $19 : dw Room_A8B9_state_A8C6_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $12 : db $17 : dw Room_A8B9_state_A8C6_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0e : db $17 : dw Room_A8B9_state_A8C6_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0c : db $17 : dw Room_A8B9_state_A8C6_PLM_index_3_PLM_scroll_data 
    dw $0000
org $8f8b46
; room A8F8: Crumble Shaft
Room_A8F8_state_A905_PLM:
    ; Missile tank, shot block
    dw $ef83 : db $0e : db $08 : dw $0033 
    dw $0000
org $8f8b4e
; room A923: Crocomire Speedway
Room_A923_state_A930_PLM:
    ; Scroll PLM
    dw $b703 : db $31 : db $28 : dw Room_A923_state_A930_PLM_index_0_PLM_scroll_data
    ; Upwards extension
    dw $b647 : db $31 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $31 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $31 : db $25 : dw $8000 
    ; Upwards extension
    dw $b647 : db $31 : db $24 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $11 : db $29 : dw Room_A923_state_A930_PLM_index_5_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $be : db $28 : dw $8000 
    ; Upwards extension
    dw $b647 : db $be : db $27 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $0d : db $29 : dw Room_A923_state_A930_PLM_index_8_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $c2 : db $28 : dw $8000 
    ; Upwards extension
    dw $b647 : db $c2 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $c2 : db $26 : dw $8000 
Door_4E_Room_A923_PLM_C87E:
    ; Door. Green door facing up
    dw $c87e : db $06 : db $2d : dw $004e 
    dw $0000
org $8f8b9e
; room A98D: Crocomire's Room
Room_A98D_state_A9B9_PLM:
    ; Door. Grey door facing down
    dw $c854 : db $36 : db $02 : dw $044f 
    ; Energy tank
    dw $eed7 : db $02 : db $06 : dw $0034 
    dw $0000
org $8f8bac
; room A9E5: Hi Jump Boots Room
Room_A9E5_state_A9F2_PLM:
    ; Hi-jump, chozo orb
    dw $ef47 : db $0c : db $0a : dw $0035 
    dw $0000
org $8f8bb4
; room AA0E: Crocomire Escape
Room_AA0E_state_AA1B_PLM:
    ; Downwards closed gate
    dw $c82a : db $39 : db $05 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $39 : db $05 : dw $0008 
    ; Missile tank
    dw $eedb : db $32 : db $09 : dw $0036 
    dw $0000
org $8f8bc8
; room AA41: Hi Jump Energy Tank Room
Room_AA41_state_AA4E_PLM:
    ; Scroll PLM
    dw $b703 : db $0f : db $09 : dw Room_AA41_state_AA4E_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $10 : db $05 : dw Room_AA41_state_AA4E_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $17 : db $1c : dw Room_AA41_state_AA4E_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $14 : db $12 : dw Room_AA41_state_AA4E_PLM_index_3_PLM_scroll_data 
Door_50_Room_AA41_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c50 
    ; Missile tank
    dw $eedb : db $16 : db $06 : dw $0037 
    ; Energy tank
    dw $eed7 : db $08 : db $08 : dw $0038 
    dw $0000
org $8f8bf4
; room AA82: Post Crocomire Farming Room
Room_AA82_state_AA8F_PLM:
Door_51_Room_AA82_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $1e : db $06 : dw $0051 
    dw $0000
org $8f8bfc
; room AAB5: [Post Crocomire Save Room]
Room_AAB5_state_AAC2_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0000 
    dw $0000
org $8f8c04
; room AADE: Post Crocomire Power Bomb Room
Room_AADE_state_AAEB_PLM:
    ; Power bomb tank
    dw $eee3 : db $08 : db $08 : dw $0039 
    dw $0000
org $8f8c0c
; room AB07: Post Crocomire Shaft
Room_AB07_state_AB14_PLM:
Door_52_Room_AB07_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $36 : dw $0052 
    dw $0000
org $8f8c14
; room AB3B: Post Crocomire Missile Room
Room_AB3B_state_AB48_PLM:
    ; Missile tank
    dw $eedb : db $03 : db $09 : dw $003a 
    dw $0000
org $8f8c1c
; room AB64: Grapple Tutorial Room 3
Room_AB64_state_AB71_PLM:
    ; Downwards closed gate
    dw $c82a : db $05 : db $05 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $05 : db $05 : dw $000a 
    dw $0000
org $8f8c2a
; room AB8F: Post Crocomire Jump Room
Room_AB8F_state_AB9C_PLM:
    ; Missile tank
    dw $eedb : db $3c : db $09 : dw $003b 
    dw $0000
org $8f8c32
; room ABD2: Grapple Tutorial Room 2
Room_ABD2_state_ABDF_PLM:
    dw $0000
org $8f8c34
; room AC00: Grapple Tutorial Room 1
Room_AC00_state_AC0D_PLM:
    dw $0000
org $8f8c36
; room AC2B: Grapple Beam Room
Room_AC2B_state_AC38_PLM:
    ; Grapple beam, chozo orb
    dw $ef6b : db $0b : db $27 : dw $003c 
    dw $0000
org $8f8c3e
; room AC5A: Norfair Reserve Tank Room
Room_AC5A_state_AC67_PLM:
    ; Reserve tank, chozo orb
    dw $ef7b : db $1d : db $07 : dw $003d 
    ; Missile tank, shot block
    dw $ef83 : db $18 : db $0b : dw $003e 
    dw $0000
org $8f8c4c
; room AC83: Green Bubbles Missile Room
Room_AC83_state_AC90_PLM:
    ; Scroll PLM
    dw $b703 : db $0f : db $05 : dw Room_AC83_state_AC90_PLM_index_0_PLM_scroll_data 
    ; Missile tank
    dw $eedb : db $0b : db $0a : dw $003f 
    dw $0000
org $8f8c5a
; room ACB3: Bubble Mountain
Room_ACB3_state_ACC0_PLM:
Door_53_Room_ACB3_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $06 : dw $0053 
Door_54_Room_ACB3_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $1e : db $06 : dw $0054 
    ; Missile tank
    dw $eedb : db $0b : db $3c : dw $0040 
    dw $0000
org $8f8c6e
; room ACF0: Speed Booster Hall
Room_ACF0_state_ACFD_PLM:
    ; Speed Booster escape
    dw $b8ac : db $b1 : db $19 : dw $8000 
    ; Missile tank, shot block
    dw $ef83 : db $03 : db $13 : dw $0041 
Door_55_Room_ACF0_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $16 : dw $0055 
    dw $0000
org $8f8c82
; room AD1B: Speed Booster Room
Room_AD1B_state_AD28_PLM:
    ; Speed booster, chozo orb
    dw $ef4b : db $04 : db $06 : dw $0042 
    dw $0000
org $8f8c8a
; room AD5E: Single Chamber
Room_AD5E_state_AD6B_PLM:
    ; Scroll PLM
    dw $b703 : db $51 : db $08 : dw Room_AD5E_state_AD6B_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $4f : db $08 : dw Room_AD5E_state_AD6B_PLM_index_4_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $12 : db $0a : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $0b : dw $8000 
    ; Scroll PLM
    dw $b703 : db $12 : db $0c : dw Room_AD5E_state_AD6B_PLM_index_4_PLM_scroll_data 
Door_56_Room_AD5E_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $51 : db $16 : dw $0056 
    dw $0000
org $8f8cb0
; room ADAD: Double Chamber
Room_ADAD_state_ADBA_PLM:
    ; Downwards closed gate
    dw $c82a : db $25 : db $05 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $25 : db $05 : dw $0002 
    ; Missile tank
    dw $eedb : db $20 : db $09 : dw $0043 
Door_57_Room_ADAD_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $06 : dw $0057 
    dw $0000
org $8f8cca
; room ADDE: Wave Beam Room
Room_ADDE_state_ADEB_PLM:
    ; Wave beam, chozo orb
    dw $ef4f : db $04 : db $06 : dw $0044 
    dw $0000
org $8f8cd2
; room AE07: Spiky Platforms Tunnel
Room_AE07_state_AE14_PLM:
    dw $0000
org $8f8cd4
; room AE32: Volcano Room
Room_AE32_state_AE3F_PLM:
    ; Scroll PLM
    dw $b703 : db $0f : db $26 : dw Room_AE32_state_AE3F_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $10 : db $29 : dw Room_AE32_state_AE3F_PLM_index_1_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $16 : db $24 : dw $8000 
    ; Upwards extension
    dw $b647 : db $16 : db $25 : dw $8000 
    ; Upwards extension
    dw $b647 : db $16 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $16 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $16 : db $28 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $19 : db $2c : dw Room_AE32_state_AE3F_PLM_index_7_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $09 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $09 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $09 : db $28 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $09 : db $29 : dw $ae71 
    dw $0000
org $8f8d1e
; room AE74: Kronic Boost Room
Room_AE74_state_AE81_PLM:
    ; Scroll PLM
    dw $b703 : db $1d : db $19 : dw Room_AE74_state_AE81_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0e : db $17 : dw Room_AE74_state_AE81_PLM_index_1_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $17 : db $15 : dw $8000 
    ; Upwards extension
    dw $b647 : db $17 : db $16 : dw $8000 
    ; Upwards extension
    dw $b647 : db $17 : db $17 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $17 : db $18 : dw Room_AE74_state_AE81_PLM_index_5_PLM_scroll_data 
    ; Downwards closed gate
    dw $c82a : db $18 : db $14 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $18 : db $14 : dw $0002 
Door_58_Room_AE74_PLM_C85A:
    ; Door. Yellow door facing left
    dw $c85a : db $0e : db $26 : dw $0058 
    dw $0000
org $8f8d56
; room AEB4: Magdollite Tunnel
Room_AEB4_state_AEC1_PLM:
    dw $0000
org $8f8d58
; room AEDF: Purple Shaft
Room_AEDF_state_AEEC_PLM:
    ; Scroll PLM
    dw $b703 : db $02 : db $0b : dw $af0f 
    ; Rightwards extension
    dw $b63b : db $03 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $04 : db $0b : dw $8000 
    ; Scroll PLM
    dw $b703 : db $0b : db $0b : dw $af0f 
    ; Rightwards extension
    dw $b63b : db $0c : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0d : db $0b : dw $8000 
    dw $0000
org $8f8d7e
; room AF14: Lava Dive Room
Room_AF14_state_AF21_PLM:
    dw $0000
org $8f8d80
; room AF3F: [Elevator to Lower Norfair]
Room_AF3F_state_AF4C_PLM:
    ; Scroll PLM
    dw $b703 : db $08 : db $0b : dw $af6f 
    dw $0000
org $8f8d88
; room AF72: Upper Norfair Farming Room
Room_AF72_state_AF7F_PLM:
    ; Downwards closed gate
    dw $c82a : db $19 : db $15 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $19 : db $15 : dw $0002 
    dw $0000
org $8f8d96
; room AFA3: Rising Tide
Room_AFA3_state_AFB0_PLM:
    dw $0000
org $8f8d98
; room AFCE: Acid Snakes Tunnel
Room_AFCE_state_AFDB_PLM:
    dw $0000
org $8f8d9a
; room AFFB: Spiky Acid Snakes Tunnel
Room_AFFB_state_B008_PLM:
    dw $0000
org $8f8d9c
; room B026: [Crocomire Recharge Room]
Room_B026_state_B033_PLM:
    ; Energy station
    dw $b6df : db $08 : db $0a : dw $0045 
    dw $0000
org $8f8da4
; room B051: Purple Farming Room
Room_B051_state_B05E_PLM:
    dw $0000
org $8f8da6
; room B07A: Bat Cave
Room_B07A_state_B087_PLM:
    ; Scroll PLM
    dw $b703 : db $05 : db $0c : dw $b0a7 
    ; Rightwards extension
    dw $b63b : db $06 : db $0c : dw $8000 
    ; Scroll PLM
    dw $b703 : db $05 : db $10 : dw $b0ac 
    ; Rightwards extension
    dw $b63b : db $06 : db $10 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $06 : db $13 : dw $b0b1 
    ; Rightwards extension
    dw $b63b : db $07 : db $13 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $08 : db $13 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $09 : db $13 : dw $8000 
    dw $0000
org $8f8dd8
; room B0B4: Norfair Map Room
Room_B0B4_state_B0C1_PLM:
    ; Map station
    dw $b6d3 : db $0b : db $0a : dw $8000 
    dw $0000
org $8f8de0
; room B0DD: [Bubble Mountain Save Room]
Room_B0DD_state_B0EA_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0001 
    dw $0000
org $8f8de8
; room B106: Frog Speedway
Room_B106_state_B113_PLM:
    dw $0000
org $8f8dea
; room B139: Red Pirate Shaft
Room_B139_state_B146_PLM:
    dw $0000
org $8f8dec
; room B167: [Business Center Save Room]
Room_B167_state_B174_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0002 
    dw $0000
org $8f8df4
; room B192: [Crocomire Save Room]
Room_B192_state_B19F_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0003 
    dw $0000
org $8f8dfc
; room B1BB: [Elevator Save Room]
Room_B1BB_state_B1C8_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0004 
    dw $0000
org $8f8e04
; room B1E5: Acid Statue Room
Room_B1E5_state_B1F2_PLM:
    ; Scroll PLM
    dw $b703 : db $23 : db $1e : dw Room_B1E5_state_B1F2_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $23 : db $23 : dw $b22d 
    dw $0000
org $8f8e12
; room B236: Main Hall
Room_B236_state_B243_PLM:
    ; Scroll PLM
    dw $b703 : db $37 : db $08 : dw Room_B236_state_B243_PLM_index_2_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $38 : db $08 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $37 : db $23 : dw Room_B236_state_B243_PLM_index_2_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $38 : db $23 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $37 : db $29 : dw Room_B236_state_B243_PLM_index_4_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $38 : db $29 : dw $8000 
    ; Elevator platform
    dw $b70b : db $36 : db $2a : dw $8000 
    dw $0000
org $8f8e3e
; room B283: Golden Torizo's Room
Room_B283_state_B2AF_PLM:
    ; Scroll PLM
    dw $b703 : db $14 : db $0c : dw $b2d1 
    ; Rightwards extension
    dw $b63b : db $16 : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $17 : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $18 : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $19 : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1a : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1b : db $0c : dw $8000 
    ; Rightwards extension
    dw $b63b : db $15 : db $0c : dw $8000 
    ; Missile tank
    dw $eedb : db $12 : db $08 : dw $0046 
    ; Super missile tank, shot block
    dw $ef87 : db $0a : db $08 : dw $0047 
Door_59_Room_B283_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $16 : dw $0859 
    dw $0000
org $8f8e82
; room B2DA: Fast Ripper Room
Room_B2DA_state_B2E7_PLM:
    ; Downwards closed gate
    dw $c82a : db $0b : db $05 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $0b : db $05 : dw $000a 
    dw $0000
org $8f8e90
; room B305: [Screw Attack Energy Charge Room]
Room_B305_state_B312_PLM:
    ; Energy station
    dw $b6df : db $07 : db $0a : dw $0048 
    dw $0000
org $8f8e98
; room B32E: Ridley's Room
Room_B32E_state_B35A_PLM:
Door_5A_Room_B32E_PLM_C848:
    ; Door. Grey door facing left
    dw $c848 : db $01 : db $06 : dw $005a 
Door_5B_Room_B32E_PLM_C842:
    ; Door. Grey door facing right
    dw $c842 : db $0e : db $16 : dw $005b 
    dw $0000
org $8f8ea6
; room B37A: Lower Norfair Farming Room
Room_B37A_state_B387_PLM:
Door_5C_Room_B37A_PLM_DB5A:
    ; Door. Eye door, facing left
    dw $db5a : db $2e : db $06 : dw $005c 
    ; Eye door bottom, facing left
    dw $db60 : db $2e : db $09 : dw $005c 
    ; Eye door eye, facing left
    dw $db56 : db $2e : db $07 : dw $005c 
    dw $0000
org $8f8eba
; room B3A5: Fast Pillars Setup Room
Room_B3A5_state_B3B2_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $21 : dw $b3d9 
    ; Rightwards extension
    dw $b63b : db $08 : db $21 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $07 : db $1b : dw $b3dc 
    ; Rightwards extension
    dw $b63b : db $08 : db $1b : dw $8000 
    dw $0000
org $8f8ed4
; room B3E1: Unknown Room
Room_B3E1_state_B3EE_PLM:
    dw $0000
org $8f8ed6
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_PLM:
    ; Scroll PLM
    dw $b703 : db $0f : db $16 : dw Room_B40A_state_B417_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0d : db $16 : dw Room_B40A_state_B417_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $12 : db $16 : dw Room_B40A_state_B417_PLM_index_2_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $14 : db $14 : dw $8000 
    ; Upwards extension
    dw $b647 : db $14 : db $15 : dw $8000 
    ; Upwards extension
    dw $b647 : db $14 : db $16 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $14 : db $17 : dw Room_B40A_state_B417_PLM_index_6_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $07 : db $36 : dw $8000 
    ; Upwards extension
    dw $b647 : db $07 : db $37 : dw $8000 
    ; Upwards extension
    dw $b647 : db $07 : db $38 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $07 : db $39 : dw Room_B40A_state_B417_PLM_index_A_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $04 : db $34 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $03 : db $34 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $02 : db $34 : dw Room_B40A_state_B417_PLM_index_D_PLM_scroll_data 
Door_5D_Room_B40A_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $3e : db $36 : dw $0c5d 
    ; Missile tank
    dw $eedb : db $18 : db $1b : dw $0049 
    dw $0000
org $8f8f38
; room B457: Pillar Room
Room_B457_state_B464_PLM:
    dw $0000
org $8f8f3a
; room B482: Plowerhouse Room
Room_B482_state_B48F_PLM:
    dw $0000
org $8f8f3c
; room B4AD: The Worst Room In The Game
Room_B4AD_state_B4BA_PLM:
    ; Scroll PLM
    dw $b703 : db $03 : db $10 : dw $b4e0 
    ; Rightwards extension
    dw $b63b : db $04 : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $05 : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $06 : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $07 : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $08 : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $09 : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0b : db $10 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0c : db $10 : dw $8000 
    dw $0000
org $8f8f7a
; room B4E5: Amphitheatre
Room_B4E5_state_B4F2_PLM:
    dw $0000
org $8f8f7c
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_state_B51D_PLM:
    ; Scroll PLM
    dw $b703 : db $41 : db $09 : dw Room_B510_state_B51D_PLM_index_0_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $41 : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $41 : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $41 : db $06 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $45 : db $12 : dw Room_B510_state_B51D_PLM_index_4_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $04 : db $12 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $05 : db $12 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $06 : db $12 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $07 : db $12 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $08 : db $12 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $09 : db $12 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $12 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $20 : db $03 : dw Room_B510_state_B51D_PLM_index_C_PLM_scroll_data 
    ; Missile tank
    dw $eedb : db $24 : db $07 : dw $004a 
    dw $0000
org $8f8fd2
; room B55A: Lower Norfair Escape Power Bomb Room
Room_B55A_state_B567_PLM:
    ; Power bomb tank
    dw $eee3 : db $03 : db $08 : dw $004b 
    dw $0000
org $8f8fda
; room B585: Red Keyhunter Shaft
Room_B585_state_B592_PLM:
    ; Scroll PLM
    dw $b703 : db $1e : db $48 : dw $b5c3 
    ; Rightwards extension
    dw $b63b : db $1a : db $42 : dw $8000 
    ; Upwards extension
    dw $b647 : db $16 : db $43 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $26 : db $46 : dw $b5c8 
    ; Scroll PLM
    dw $b703 : db $10 : db $48 : dw $b5c3 
    ; Scroll PLM
    dw $b703 : db $0b : db $48 : dw $b5c8 
    ; Scroll PLM
    dw $b703 : db $26 : db $0e : dw Room_B585_state_B592_PLM_index_6_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $27 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $28 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $29 : db $0e : dw $8000 
    ; Scroll PLM
    dw $b703 : db $26 : db $0b : dw Room_B585_state_B592_PLM_index_A_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $27 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $28 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $29 : db $0b : dw $8000 
Door_5E_Room_B585_PLM_C866:
    ; Door. Yellow door facing up
    dw $c866 : db $06 : db $4d : dw $005e 
    dw $0000
org $8f9036
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM:
    ; Scroll PLM
    dw $b703 : db $47 : db $0d : dw Room_B5D5_state_B5E2_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $48 : db $0d : dw $8000 
    ; Scroll PLM
    dw $b703 : db $45 : db $08 : dw Room_B5D5_state_B5E2_PLM_index_2_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $16 : db $08 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $17 : db $08 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $18 : db $08 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $19 : db $08 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1a : db $08 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $10 : db $09 : dw Room_B5D5_state_B5E2_PLM_index_C_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0e : db $09 : dw Room_B5D5_state_B5E2_PLM_index_B_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $50 : db $0b : dw Room_B5D5_state_B5E2_PLM_index_A_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $23 : db $09 : dw Room_B5D5_state_B5E2_PLM_index_B_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $20 : db $09 : dw Room_B5D5_state_B5E2_PLM_index_C_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $4c : db $07 : dw Room_B5D5_state_B5E2_PLM_index_D_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $4c : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $4c : db $05 : dw $8000 
    ; Upwards extension
    dw $b647 : db $4c : db $04 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $55 : db $09 : dw Room_B5D5_state_B5E2_PLM_index_11_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $55 : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $55 : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $55 : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $55 : db $05 : dw $8000 
Door_5F_Room_B5D5_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $4e : db $26 : dw $005f 
    ; Power bomb tank
    dw $eee3 : db $58 : db $08 : dw $004c 
    dw $0000
org $8f90c8
; room B62B: Metal Pirates Room
Room_B62B_state_B638_PLM:
Door_60_Room_B62B_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $2e : db $06 : dw $0c60 
    dw $0000
org $8f90d0
; room B656: Three Muskateers' Room
Room_B656_state_B663_PLM:
    ; Scroll PLM
    dw $b703 : db $34 : db $28 : dw Room_B656_state_B663_PLM_index_0_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $0b : db $29 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0b : db $28 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0b : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0b : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0b : db $25 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $30 : db $2a : dw Room_B656_state_B663_PLM_index_6_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $2b : db $2a : dw Room_B656_state_B663_PLM_index_7_PLM_scroll_data 
    ; Missile tank
    dw $eedb : db $37 : db $29 : dw $004d 
    dw $0000
org $8f9108
; room B698: Ridley Tank Room
Room_B698_state_B6A5_PLM:
    ; Energy tank, shot block
    dw $ef7f : db $01 : db $0b : dw $004e 
    dw $0000
org $8f9110
; room B6C1: Screw Attack Room
Room_B6C1_state_B6CE_PLM:
    ; Screw attack, chozo orb
    dw $ef73 : db $04 : db $28 : dw $004f 
    dw $0000
org $8f9118
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_state_B6FB_PLM:
    ; Upwards extension
    dw $b647 : db $10 : db $36 : dw $8000 
    ; Upwards extension
    dw $b647 : db $10 : db $37 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $10 : db $38 : dw Room_B6EE_state_B6FB_PLM_index_2_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $04 : db $39 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $03 : db $39 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $02 : db $39 : dw Room_B6EE_state_B6FB_PLM_index_5_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $20 : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $20 : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $20 : db $08 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $20 : db $09 : dw Room_B6EE_state_B6FB_PLM_index_9_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $1b : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1a : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $19 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $18 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $17 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $16 : db $0b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $15 : db $0b : dw $8000 
    ; Scroll PLM
    dw $b703 : db $14 : db $0b : dw $b73c 
    ; Energy tank
    dw $eed7 : db $05 : db $51 : dw $0050 
    dw $0000
org $8f918c
; room B741: [Red Keyhunter Shaft Save Room]
Room_B741_state_B74E_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0005 
    dw $0000

org $8483D7
SpawnHardCodedPlm:
EarthquakeType = $7E183E
EarthquakeTimer = $7E1840

org $8f9194
;;; $9194: Setup ASM: clear a few blocks after saving animals and shake screen ;;;
; Room $92FD, state $9348. Crateria mainstreet, Zebes timebomb set
SetupAsm:
    JSL.l SpawnHardCodedPlm
    db $0D,$0B : dw $BB30
    LDA.w #$0018
    STA.w EarthquakeType           ; Earthquake type = BG1, BG2 and enemies; 3 pixel displacement, horizontal
    LDA.w #$FFFF
    STA.w EarthquakeTimer
    RTS

org $8f91a9
;;; $91A9: Setup ASM: auto-destroy the wall during escape ;;;
; Room $96BA, state $9705. Old Tourian escape shaft, Zebes timebomb set
SetupAsmAutoDestroyTheWallDuringEscape:
    JSL.l SpawnHardCodedPlm
    db $1e,$87 : dw $B964
    RTS

org $8f91b2
;;; $91B2: Setup ASM: turn wall into shotblocks during escape ;;;
; Room $9804, state $984F. Bomb Torizo's room, Zebes timebomb set
SetupAsmTurnWallIntoShotblocksDuringEscape:
    JSL.l SpawnHardCodedPlm
    db $00,$0A : dw $B9ED
    RTS

org $8f91f8
RoomHeadersScrollDataDooroutData:
    db $00,$00,$1f,$00,$09,$05,$70,$a0,$00,$7b,$92,$12,$e6,$0e,$61,$92,$69,$e6,$47,$92,$12,$e6,$00,$2d,$92,$e6,$e5
org $8f9283
; room 91F8: Landing Site
Room_91F8_state_9261_Scroll:
    db $02,$02,$02,$02,$02,$02,$02,$00,$00,$02,$02,$02,$02,$02,$02,$02,$00,$00,$02,$02,$02,$02,$02,$02,$02,$00,$01,$02,$02,$02,$02,$02,$02,$02,$00,$00,$01,$01,$01,$01,$01,$01,$01,$01,$01
org $8f92b0
; room 91F8: Landing Site
Room_91F8_state_9261_PLM_index_0_PLM_scroll_data:
    db $19,$01,$80
org $8f92b3
; room 92B3: Gauntlet Entrance
Room_92B3_Header:
    db $01 ; room index
    db $00 ; area
    db $28 ; map X
    db $02 ; map Y
    db $05 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $92f9 ; doors pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $92df ; room state pointer
    dw $e5e6 ; room state standard
org $8f92fd
; room 92FD: Parlor and Alcatraz
Room_92FD_Header:
    db $02 ; room index
    db $00 ; area
    db $28 ; map X
    db $04 ; map Y
    db $05 ; width
    db $05 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9362 ; doors pointer
    dw $e612 ; room state Events
    db $0e ; event
    dw $9348 ; room state pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $932e ; room state pointer
    dw $e5e6 ; room state standard
org $8f9370
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_Scroll:
    db $01,$01,$01,$01,$00,$00,$00,$00,$00,$00,$00,$01,$00,$02,$00,$00,$00,$00,$02,$00,$01,$00,$00,$02,$00
org $8f9389
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_0_PLM_scroll_data:
    db $06,$02,$80
org $8f938c
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_1_PLM_scroll_data:
    db $06,$00,$80
org $8f938f
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_2_PLM_scroll_data:
    db $02,$00,$04,$00,$08,$02,$80
org $8f9396
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_6_PLM_scroll_data:
    db $08,$00,$80
org $8f9399
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_A_PLM_scroll_data:
    db $04,$01,$80
org $8f939c
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_D_PLM_scroll_data:
    db $02,$01,$80
org $8f939f
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_14_PLM_scroll_data:
    db $00,$01,$80
org $8f93a2
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_15_PLM_scroll_data:
    db $00,$00,$80
org $8f93a5
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9348_PLM_index_1A_PLM_scroll_data:
    db $00,$00,$06,$02,$80
org $8f93aa
; room 93AA: Crateria Power Bomb Room
Room_93AA_Header:
    db $03 ; room index
    db $00 ; area
    db $1d ; map X
    db $01 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $93d1 ; doors pointer
    dw $e5e6 ; room state standard
org $8f93d5
; room 93D5: [Parlor Save Room]
RoomPtr_93D5:
    db $04 ; room index
    db $00 ; area
    db $2c ; map X
    db $06 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $93fc ; doors pointer
    dw $e5e6 ; room state standard
org $8f93fe
; room 93FE: West Ocean
Room_93FE_Header:
    db $05 ; room index
    db $00 ; area
    db $11 ; map X
    db $00 ; map Y
    db $08 ; width
    db $06 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9425 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9431
; room 93FE: West Ocean
Room_93FE_state_940B_Scroll:
    db $02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$00,$00,$02,$00,$00,$02,$02,$02,$00,$00,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$01,$01,$01,$01,$01,$01,$01,$01
org $8f9461
; room 9461: Bowling Alley Path
Room_9461_Header:
    db $06 ; room index
    db $00 ; area
    db $14 ; map X
    db $02 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9488 ; doors pointer
    dw $e5e6 ; room state standard
org $8f948c
; room 948C: Crateria Keyhunter Room
Room_948C_Header:
    db $07 ; room index
    db $00 ; area
    db $1b ; map X
    db $04 ; map Y
    db $03 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $94b3 ; doors pointer
    dw $e5e6 ; room state standard
org $8f94cc
; room 94CC: [Elevator to Maridia]
RoomPtr_94CC:
    db $08 ; room index
    db $00 ; area
    db $0a ; map X
    db $0a ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $94f3 ; doors pointer
    dw $e5e6 ; room state standard
org $8f94fd
; room 94FD: East Ocean
RoomPtr_94FD:
    db $09 ; room index
    db $00 ; area
    db $07 ; map X
    db $00 ; map Y
    db $07 ; width
    db $06 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9524 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9552
; room 9552: Forgotten Highway Kago Room
Room_9552_Header:
    db $0a ; room index
    db $00 ; area
    db $06 ; map X
    db $04 ; map Y
    db $01 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9579 ; doors pointer
    dw $e5e6 ; room state standard
org $8f957d
; room 957D: Crab Maze
Room_957D_Header:
    db $0b ; room index
    db $00 ; area
    db $06 ; map X
    db $08 ; map Y
    db $04 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $95a4 ; doors pointer
    dw $e5e6 ; room state standard
org $8f95a8
; room 95A8: [Crab Maze to Elevator]
Room_95A8_Header:
    db $0c ; room index
    db $00 ; area
    db $0a ; map X
    db $09 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $95cf ; doors pointer
    dw $e5e6 ; room state standard
org $8f95d4
; room 95D4: Crateria Tube
Room_95D4_Header:
    db $0d ; room index
    db $00 ; area
    db $1e ; map X
    db $04 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $95fb ; doors pointer
    dw $e5e6 ; room state standard
org $8f95ff
; room 95FF: The Moat
Room_95FF_Header:
    db $0e ; room index
    db $00 ; area
    db $19 ; map X
    db $04 ; map Y
    db $02 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9626 ; doors pointer
    dw $e5e6 ; room state standard
org $8f962a
; room 962A: [Elevator to Red Brinstar]
RoomPtr_962A:
    db $0f ; room index
    db $00 ; area
    db $1c ; map X
    db $07 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9651 ; doors pointer
    dw $e5e6 ; room state standard
org $8f965b
; room 965B: Gauntlet Energy Tank Room
Room_965B_Header:
    db $10 ; room index
    db $00 ; area
    db $2d ; map X
    db $02 ; map Y
    db $06 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9682 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9686
; room 965B: Gauntlet Energy Tank Room
Room_965B_state_9668_Scroll:
    db $01,$00,$01,$01,$01,$01
org $8f968c
; room 965B: Gauntlet Energy Tank Room
Room_965B_state_9668_PLM_index_0_PLM_scroll_data:
    db $01,$01,$80
org $8f968f
; room 968F: [West Ocean Geemer Corridor]
Room_968F_Header:
    db $11 ; room index
    db $00 ; area
    db $13 ; map X
    db $02 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $96b6 ; doors pointer
    dw $e5e6 ; room state standard
org $8f96ba
; room 96BA: Climb
Room_96BA_Header:
    db $12 ; room index
    db $00 ; area
    db $2a ; map X
    db $09 ; map Y
    db $03 ; width
    db $09 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $971f ; doors pointer
    dw $e612 ; room state Events
    db $0e ; event
    dw $9705 ; room state pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $96eb ; room state pointer
    dw $e5e6 ; room state standard
org $8f9744
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_1_PLM_scroll_data:
    db $00,$01,$80
org $8f9747
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_0_PLM_scroll_data:
    db $00,$00,$80
org $8f974a
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_3_PLM_scroll_data:
    db $15,$01,$80
org $8f974d
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_2_PLM_scroll_data:
    db $15,$00,$80
org $8f9750
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_E_PLM_scroll_data:
    db $1a,$01,$80
org $8f9753
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_A_PLM_scroll_data:
    db $1a,$00,$80
org $8f9756
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_12_PLM_scroll_data:
    db $19,$01,$80
org $8f9759
; room 96BA: Climb
Room_96BA_state_9705_PLM_index_16_PLM_scroll_data:
    db $18,$00,$19
org $8f975c
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_Header:
    db $00 ; room index
    db $00 ; area
    db $28 ; map X
    db $11 ; map Y
    db $03 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $97a1 ; doors pointer
    dw $e652 ; room state MorphMissiles
    dw $9787 ; room state pointer
    dw $e5e6 ; room state standard
org $8f97ab
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_state_9787_PLM_index_1_PLM_scroll_data:
    db $02,$02,$05,$02,$80
org $8f97b0
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_state_9787_PLM_index_2_PLM_scroll_data:
    db $02,$01,$05,$00,$80
org $8f97b5
; room 97B5: [Elevator to Blue Brinstar]
RoomPtr_97B5:
    db $14 ; room index
    db $00 ; area
    db $27 ; map X
    db $11 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $97fa ; doors pointer
    dw $e652 ; room state MorphMissiles
    dw $97e0 ; room state pointer
    dw $e5e6 ; room state standard
org $8f9804
; room 9804: Bomb Torizo Room
Room_9804_Header:
    db $15 ; room index
    db $00 ; area
    db $25 ; map X
    db $06 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9869 ; doors pointer
    dw $e612 ; room state Events
    db $0e ; event
    dw $984f ; room state pointer
    dw $e629 ; room state Bosses
    db $04 ; event
    dw $9835 ; room state pointer
    dw $e5e6 ; room state standard
org $8f9879
; room 9879: Flyway
Room_9879_Header:
    db $16 ; room index
    db $00 ; area
    db $26 ; map X
    db $06 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $98de ; doors pointer
    dw $e612 ; room state Events
    db $0e ; event
    dw $98c4 ; room state pointer
    dw $e629 ; room state Bosses
    db $04 ; event
    dw $98aa ; room state pointer
    dw $e5e6 ; room state standard
org $8f98e2
; room 98E2: Pre-Map Flyway
Room_98E2_Header:
    db $17 ; room index
    db $00 ; area
    db $28 ; map X
    db $07 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9909 ; doors pointer
    dw $e5e6 ; room state standard
org $8f990d
; room 990D: Terminator Room
Room_990D_Header:
    db $18 ; room index
    db $00 ; area
    db $2d ; map X
    db $04 ; map Y
    db $06 ; width
    db $03 ; height
    db $a0 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9934 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9938
; room 9938: [Elevator to Green Brinstar]
RoomPtr_9938:
    db $19 ; room index
    db $00 ; area
    db $38 ; map X
    db $08 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $995f ; doors pointer
    dw $e5e6 ; room state standard
org $8f9969
; room 9969: Lower Mushrooms
Room_9969_Header:
    db $1a ; room index
    db $00 ; area
    db $34 ; map X
    db $08 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9990 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9994
; room 9994: Crateria Map Room
Room_9994_Header:
    db $1b ; room index
    db $00 ; area
    db $27 ; map X
    db $07 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $99bb ; doors pointer
    dw $e5e6 ; room state standard
org $8f99bd
; room 99BD: Green Pirates Shaft
Room_99BD_Header:
    db $1c ; room index
    db $00 ; area
    db $33 ; map X
    db $02 ; map Y
    db $01 ; width
    db $07 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $99e4 ; doors pointer
    dw $e5e6 ; room state standard
org $8f99ec
; room 99BD: Green Pirates Shaft
Room_99BD_state_99CA_Scroll:
    db $02,$02,$02,$02,$02,$02,$01
org $8f99f9
; room 99F9: Crateria Super Room
Room_99F9_Header:
    db $1d ; room index
    db $00 ; area
    db $26 ; map X
    db $09 ; map Y
    db $04 ; width
    db $08 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9a20 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9a24
; room 99F9: Crateria Super Room
Room_99F9_state_9A06_Scroll:
    db $02,$01,$01,$01,$02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$01,$01,$01,$01
org $8f9a44
; room 9A44: Final Missile Bombway
Room_9A44_Header:
    db $1e ; room index
    db $00 ; area
    db $2c ; map X
    db $07 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9a8a ; doors pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $9a70 ; room state pointer
    dw $e5e6 ; room state standard
org $8f9a90
; room 9A90: The Final Missile
Room_9A90_Header:
    db $1f ; room index
    db $00 ; area
    db $2e ; map X
    db $07 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9ad6 ; doors pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $9abc ; room state pointer
    dw $e5e6 ; room state standard
org $8f9ad9
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
RoomPtr_9AD9:
    db $00 ; room index
    db $01 ; area
    db $33 ; map X
    db $00 ; map Y
    db $04 ; width
    db $0c ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9b00 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9b16
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_state_9AE6_Scroll:
    db $02,$00,$00,$02,$02,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$02,$02,$02,$02,$00,$00,$02,$00,$02,$00,$02,$00,$02,$00,$02,$00,$02,$00,$02,$00,$00
org $8f9b46
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_state_9AE6_PLM_index_0_PLM_scroll_data:
    db $1e,$00,$1f,$02,$80
org $8f9b4b
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_state_9AE6_PLM_index_2_PLM_scroll_data:
    db $1e,$01,$1f,$00,$2a,$01,$80
org $8f9b52
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_state_9AE6_PLM_index_3_PLM_scroll_data:
    db $1b,$02,$1e,$00,$1f,$02,$2a,$00,$80
org $8f9b5b
; room 9B5B: Spore Spawn Super Room
Room_9B5B_Header:
    db $01 ; room index
    db $01 ; area
    db $27 ; map X
    db $01 ; map Y
    db $02 ; width
    db $09 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9b82 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9b86
; room 9B5B: Spore Spawn Super Room
Room_9B5B_state_9B68_Scroll:
    db $01,$01,$00,$00,$02,$00,$02,$00,$02,$00,$02,$00,$02,$00,$02,$00,$01,$01
org $8f9b98
; room 9B5B: Spore Spawn Super Room
Room_9B5B_state_9B68_PLM_index_0_PLM_scroll_data:
    db $00,$02,$02,$02,$80
org $8f9b9d
; room 9B9D: Brinstar Pre-Map Room
Room_9B9D_Header:
    db $02 ; room index
    db $01 ; area
    db $37 ; map X
    db $04 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9bc4 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9bc8
; room 9BC8: Early Supers Room
Room_9BC8_Header:
    db $03 ; room index
    db $01 ; area
    db $33 ; map X
    db $03 ; map Y
    db $03 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9bef ; doors pointer
    dw $e5e6 ; room state standard
org $8f9c07
; room 9C07: Brinstar Reserve Tank Room
Room_9C07_Header:
    db $04 ; room index
    db $01 ; area
    db $31 ; map X
    db $04 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9c2e ; doors pointer
    dw $e5e6 ; room state standard
org $8f9c30
; room 9C07: Brinstar Reserve Tank Room
Room_9C07_state_9C14_Scroll:
    db $00,$01
org $8f9c32
; room 9C07: Brinstar Reserve Tank Room
Room_9C07_state_9C14_PLM_index_0_PLM_scroll_data:
    db $00,$01,$80
org $8f9c35
; room 9C35: Brinstar Map Room
Room_9C35_Header:
    db $05 ; room index
    db $01 ; area
    db $3a ; map X
    db $04 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9c5c ; doors pointer
    dw $e5e6 ; room state standard
org $8f9c5e
; room 9C5E: Green Brinstar Fireflea Room
Room_9C5E_Header:
    db $06 ; room index
    db $01 ; area
    db $37 ; map X
    db $06 ; map Y
    db $03 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9c85 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9c89
; room 9C89: [Green Brinstar Missile Station]
Room_9C89_Header:
    db $07 ; room index
    db $01 ; area
    db $3a ; map X
    db $07 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9cb0 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9cb3
; room 9CB3: Dachora Room
Room_9CB3_Header:
    db $08 ; room index
    db $01 ; area
    db $2f ; map X
    db $06 ; map Y
    db $07 ; width
    db $07 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9cda ; doors pointer
    dw $e5e6 ; room state standard
org $8f9ce0
; room 9CB3: Dachora Room
Room_9CB3_state_9CC0_Scroll:
    db $01,$01,$01,$01,$01,$01,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$02,$02,$02,$02,$02,$02,$02
org $8f9d11
; room 9CB3: Dachora Room
Room_9CB3_state_9CC0_PLM_index_6_PLM_scroll_data:
    db $09,$02,$80
org $8f9d14
; room 9CB3: Dachora Room
Room_9CB3_state_9CC0_PLM_index_A_PLM_scroll_data:
    db $02,$01,$09,$00,$80
org $8f9d19
; room 9D19: Big Pink
RoomPtr_9D19:
    db $09 ; room index
    db $01 ; area
    db $2c ; map X
    db $04 ; map Y
    db $05 ; width
    db $0a ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9d40 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9d52
; room 9D19: Big Pink
Room_9D19_state_9D26_Scroll:
    db $00,$02,$02,$00,$00,$00,$02,$02,$00,$00,$00,$02,$02,$00,$00,$00,$02,$02,$00,$00,$00,$02,$02,$00,$00,$00,$02,$02,$00,$00,$00,$01,$01,$00,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$02,$00,$00,$00,$00,$02
org $8f9d84
; room 9D19: Big Pink
Room_9D19_state_9D26_PLM_index_0_PLM_scroll_data:
    db $20,$02,$24,$02,$25,$02,$80
org $8f9d8b
; room 9D19: Big Pink
Room_9D19_state_9D26_PLM_index_1_PLM_scroll_data:
    db $26,$02,$80
org $8f9d8e
; room 9D19: Big Pink
Room_9D19_state_9D26_PLM_index_2_PLM_scroll_data:
    db $19,$00,$80
org $8f9d91
; room 9D19: Big Pink
Room_9D19_state_9D26_PLM_index_3_PLM_scroll_data:
    db $19,$01,$1a,$01,$80
org $8f9d96
; room 9D19: Big Pink
Room_9D19_state_9D26_PLM_index_4_PLM_scroll_data:
    db $03,$02,$80
org $8f9d99
; room 9D19: Big Pink
Room_9D19_state_9D26_PLM_index_5_PLM_scroll_data:
    db $03,$00,$80
org $8f9d9c
; room 9D9C: Spore Spawn Keyhunter Room
Room_9D9C_Header:
    db $0a ; room index
    db $01 ; area
    db $29 ; map X
    db $04 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9dc3 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9dc7
; room 9DC7: Spore Spawn Room
Room_9DC7_Header:
    db $0b ; room index
    db $01 ; area
    db $29 ; map X
    db $01 ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9e0d ; doors pointer
    dw $e629 ; room state Bosses
    db $02 ; event
    dw $9df3 ; room state pointer
    dw $e5e6 ; room state standard
org $8f9e11
; room 9E11: Pink Brinstar Power Bomb Room
Room_9E11_Header:
    db $0c ; room index
    db $01 ; area
    db $2f ; map X
    db $07 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9e38 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9e40
; room 9E11: Pink Brinstar Power Bomb Room
Room_9E11_state_9E1E_PLM_index_0_PLM_scroll_data:
    db $00,$00,$01,$02,$02,$01,$03,$01,$80
org $8f9e52
; room 9E52: Green Hill Zone
Room_9E52_Header:
    db $0d ; room index
    db $01 ; area
    db $25 ; map X
    db $0a ; map Y
    db $08 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9e79 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9e7f
; room 9E52: Green Hill Zone
Room_9E52_state_9E5F_Scroll:
    db $ff,$ff,$ff,$ff,$00,$00,$02,$02,$00,$00,$00,$00,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$01,$01,$01,$01,$01,$01,$00,$01
org $8f9e9f
; room 9E9F: Morph Ball Room
RoomPtr_9E9F:
    db $0e ; room index
    db $01 ; area
    db $23 ; map X
    db $08 ; map Y
    db $08 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9ee5 ; doors pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $9ecb ; room state pointer
    dw $e5e6 ; room state standard
org $8f9eed
; room 9E9F: Morph Ball Room
Room_9E9F_state_9ECB_Scroll:
    db $00,$00,$02,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01,$01,$01,$01,$01,$01
org $8f9f05
; room 9E9F: Morph Ball Room
Room_9E9F_state_9ECB_PLM_index_0_PLM_scroll_data:
    db $15,$01,$80
org $8f9f08
; room 9E9F: Morph Ball Room
Room_9E9F_state_9ECB_PLM_index_9_PLM_scroll_data:
    db $15,$00,$80
org $8f9f0b
; room 9E9F: Morph Ball Room
Room_9E9F_state_9ECB_PLM_index_D_PLM_scroll_data:
    db $0a,$02,$80
org $8f9f0e
; room 9E9F: Morph Ball Room
Room_9E9F_state_9ECB_PLM_index_F_PLM_scroll_data:
    db $0a,$00,$80
org $8f9f11
; room 9F11: Construction Zone
Room_9F11_Header:
    db $0f ; room index
    db $01 ; area
    db $22 ; map X
    db $0a ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9f57 ; doors pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $9f3d ; room state pointer
    dw $e5e6 ; room state standard
org $8f9f64
; room 9F64: Blue Brinstar Energy Tank Room
Room_9F64_Header:
    db $10 ; room index
    db $01 ; area
    db $1f ; map X
    db $08 ; map Y
    db $03 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9faa ; doors pointer
    dw $e612 ; room state Events
    db $00 ; event
    dw $9f90 ; room state pointer
    dw $e5e6 ; room state standard
org $8f9fae
; room 9F64: Blue Brinstar Energy Tank Room
Room_9F64_state_9F90_Scroll:
    db $01,$00,$00,$00,$00,$00,$01,$01,$01
org $8f9fb7
; room 9F64: Blue Brinstar Energy Tank Room
Room_9F64_state_9F90_PLM_index_1_PLM_scroll_data:
    db $03,$02,$80
org $8f9fba
; room 9FBA: Noob Bridge
Room_9FBA_Header:
    db $11 ; room index
    db $01 ; area
    db $1f ; map X
    db $0d ; map Y
    db $06 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $9fe1 ; doors pointer
    dw $e5e6 ; room state standard
org $8f9fe5
; room 9FE5: Green Brinstar Beetom Room
Room_9FE5_Header:
    db $12 ; room index
    db $01 ; area
    db $37 ; map X
    db $0a ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a00c ; doors pointer
    dw $e5e6 ; room state standard
org $8fa011
; room A011: Etecoon Energy Tank Room
Room_A011_Header:
    db $13 ; room index
    db $01 ; area
    db $35 ; map X
    db $0a ; map Y
    db $05 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a038 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa040
; room A011: Etecoon Energy Tank Room
Room_A011_state_A01E_Scroll:
    db $00,$00,$00,$01,$01,$01,$01,$01,$00,$00
org $8fa04a
; room A011: Etecoon Energy Tank Room
Room_A011_state_A01E_PLM_index_0_PLM_scroll_data:
    db $03,$02,$08,$01,$09,$01,$80
org $8fa051
; room A051: Etecoon Super Room
Room_A051_Header:
    db $14 ; room index
    db $01 ; area
    db $3a ; map X
    db $0a ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a078 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa07b
; room A07B: [Dachora Room Energy Charge Station]
Room_A07B_Header:
    db $15 ; room index
    db $01 ; area
    db $36 ; map X
    db $0c ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a0a2 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa0a4
; room A0A4: Spore Spawn Farming Room
Room_A0A4_Header:
    db $16 ; room index
    db $01 ; area
    db $29 ; map X
    db $09 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a0cb ; doors pointer
    dw $e5e6 ; room state standard
org $8fa0d2
; room A0D2: Waterway Energy Tank Room
Room_A0D2_Header:
    db $17 ; room index
    db $01 ; area
    db $31 ; map X
    db $0d ; map Y
    db $07 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a0f9 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa0fd
; room A0D2: Waterway Energy Tank Room
Room_A0D2_state_A0DF_Scroll:
    db $01,$01,$01,$01,$01,$01,$00
org $8fa104
; room A0D2: Waterway Energy Tank Room
Room_A0D2_state_A0DF_PLM_index_2_PLM_scroll_data:
    db $06,$01,$80
org $8fa107
; room A107: First Missile Room
Room_A107_Header:
    db $18 ; room index
    db $01 ; area
    db $23 ; map X
    db $0b ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a12e ; doors pointer
    dw $e5e6 ; room state standard
org $8fa130
; room A130: Pink Brinstar Hopper Room
Room_A130_Header:
    db $19 ; room index
    db $01 ; area
    db $2b ; map X
    db $07 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a157 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa15b
; room A15B: Hopper Energy Tank Room
Room_A15B_Header:
    db $1a ; room index
    db $01 ; area
    db $2a ; map X
    db $08 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a182 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa184
; room A184: [Spore Spawn Save Room]
RoomPtr_A184:
    db $1b ; room index
    db $01 ; area
    db $30 ; map X
    db $04 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a1ab ; doors pointer
    dw $e5e6 ; room state standard
org $8fa1ad
; room A1AD: Blue Brinstar Boulder Room
Room_A1AD_Header:
    db $1c ; room index
    db $01 ; area
    db $20 ; map X
    db $08 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a1d4 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa1d8
; room A1D8: Blue Brinstar Double Missile Room
Room_A1D8_Header:
    db $1d ; room index
    db $01 ; area
    db $22 ; map X
    db $08 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a1ff ; doors pointer
    dw $e5e6 ; room state standard
org $8fa201
; room A201: [Green Brinstar Main Shaft Save Room]
RoomPtr_A201:
    db $1e ; room index
    db $01 ; area
    db $37 ; map X
    db $05 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a228 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa22a
; room A22A: [Etecoon Save Room]
RoomPtr_A22A:
    db $1f ; room index
    db $01 ; area
    db $3a ; map X
    db $0b ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a251 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa253
; room A253: Red Tower
Room_A253_Header:
    db $20 ; room index
    db $01 ; area
    db $1e ; map X
    db $09 ; map Y
    db $01 ; width
    db $0a ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a27a ; doors pointer
    dw $e5e6 ; room state standard
org $8fa284
; room A253: Red Tower
Room_A253_state_A260_Scroll:
    db $02,$02,$02,$02,$02,$02,$02,$02,$02,$01
org $8fa28e
; room A253: Red Tower
Room_A253_state_A260_PLM_index_0_PLM_scroll_data:
    db $0a,$00,$80,$ff,$ff
org $8fa293
; room A293: Red Brinstar Fireflea Room
Room_A293_Header:
    db $21 ; room index
    db $01 ; area
    db $1f ; map X
    db $0f ; map Y
    db $08 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a2ba ; doors pointer
    dw $e5e6 ; room state standard
org $8fa2be
; room A293: Red Brinstar Fireflea Room
Room_A293_state_A2A0_Scroll:
    db $01,$01,$02,$02,$01,$01,$02,$02,$00,$00,$01,$01,$00,$00,$01,$01
org $8fa2ce
; room A2CE: X-Ray Scope Room
Room_A2CE_Header:
    db $22 ; room index
    db $01 ; area
    db $27 ; map X
    db $0f ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a2f5 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa2f7
; room A2F7: Hellway
Room_A2F7_Header:
    db $23 ; room index
    db $01 ; area
    db $1b ; map X
    db $09 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a31e ; doors pointer
    dw $e5e6 ; room state standard
org $8fa322
; room A322: Caterpillar Room
RoomPtr_A322:
    db $24 ; room index
    db $01 ; area
    db $18 ; map X
    db $04 ; map Y
    db $03 ; width
    db $08 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a349 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa357
; room A322: Caterpillar Room
Room_A322_state_A32F_Scroll:
    db $00,$00,$02,$00,$00,$02,$00,$00,$02,$01,$00,$02,$00,$00,$02,$00,$00,$01,$00,$00,$02,$00,$00,$02
org $8fa36f
; room A322: Caterpillar Room
Room_A322_state_A32F_PLM_index_0_PLM_scroll_data:
    db $11,$02,$14,$02,$80
org $8fa374
; room A322: Caterpillar Room
Room_A322_state_A32F_PLM_index_2_PLM_scroll_data:
    db $0a,$01,$0b,$02,$80
org $8fa37c
; room A37C: Beta Power Bomb Room
Room_A37C_Header:
    db $25 ; room index
    db $01 ; area
    db $1b ; map X
    db $07 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a3a3 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa3a9
; room A37C: Beta Power Bomb Room
Room_A37C_state_A389_PLM_index_0_PLM_scroll_data:
    db $01,$02,$03,$01,$80
org $8fa3ae
; room A3AE: Alpha Power Bomb Room
Room_A3AE_Header:
    db $26 ; room index
    db $01 ; area
    db $1b ; map X
    db $0b ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a3d5 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa3d7
; room A3AE: Alpha Power Bomb Room
Room_A3AE_state_A3BB_Scroll:
    db $01,$01,$00
org $8fa3da
; room A3AE: Alpha Power Bomb Room
Room_A3AE_state_A3BB_PLM_index_8_PLM_scroll_data:
    db $02,$01,$80
org $8fa3dd
; room A3DD: Bat Room
Room_A3DD_Header:
    db $27 ; room index
    db $01 ; area
    db $1c ; map X
    db $12 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a404 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa408
; room A408: Below Spazer
Room_A408_Header:
    db $28 ; room index
    db $01 ; area
    db $1a ; map X
    db $11 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a42f ; doors pointer
    dw $e5e6 ; room state standard
org $8fa447
; room A447: Spazer Room
Room_A447_Header:
    db $29 ; room index
    db $01 ; area
    db $19 ; map X
    db $11 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a46e ; doors pointer
    dw $e5e6 ; room state standard
org $8fa471
; room A471: Warehouse Zeela Room
Room_A471_Header:
    db $2a ; room index
    db $01 ; area
    db $12 ; map X
    db $12 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a498 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa49e
; room A471: Warehouse Zeela Room
Room_A471_state_A47E_Scroll:
    db $00,$01,$01,$00
org $8fa4a2
; room A471: Warehouse Zeela Room
Room_A471_state_A47E_PLM_index_0_PLM_scroll_data:
    db $01,$02,$02,$00,$03,$01,$80
org $8fa4a9
; room A471: Warehouse Zeela Room
Room_A471_state_A47E_PLM_index_3_PLM_scroll_data:
    db $01,$02,$02,$01,$03
org $8fa4ae
; room A471: Warehouse Zeela Room
Room_A471_state_A47E_PLM_index_2_PLM_scroll_data:
    db $01,$80,$03
org $8fa4b1
; room A4B1: Warehouse Energy Tank Room
Room_A4B1_Header:
    db $01 ; room index
    db $01 ; area
    db $14 ; map X
    db $13 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a4d8 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa4da
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_Header:
    db $2c ; room index
    db $01 ; area
    db $0f ; map X
    db $12 ; map Y
    db $04 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a501 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa507
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_state_A4E7_Scroll:
    db $00,$01,$01,$02,$00,$00,$01,$00
org $8fa50f
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_state_A4E7_PLM_index_0_PLM_scroll_data:
    db $02,$01,$06,$00,$80
org $8fa514
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_state_A4E7_PLM_index_1_PLM_scroll_data:
    db $02,$02,$06,$01,$80
org $8fa519
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_state_A4E7_PLM_index_9_PLM_scroll_data:
    db $06,$00,$80
org $8fa51c
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_state_A4E7_PLM_index_B_PLM_scroll_data:
    db $00,$01,$06,$00,$80
org $8fa521
; room A521: Baby Kraid Room
Room_A521_Header:
    db $2d ; room index
    db $01 ; area
    db $0b ; map X
    db $13 ; map Y
    db $06 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a567 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $a54d ; room state pointer
    dw $e5e6 ; room state standard
org $8fa56b
; room A56B: Kraid Eye Door Room
RoomPtr_A56B:
    db $2e ; room index
    db $01 ; area
    db $09 ; map X
    db $12 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $02 ; special graphics bitflag
    dw $a592 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa59c
; room A56B: Kraid Eye Door Room
Room_A56B_state_A578_PLM_index_0_PLM_scroll_data:
    db $01,$02,$80
org $8fa59f
; room A59F: Kraid Room
Room_A59F_Header:
    db $2f ; room index
    db $01 ; area
    db $07 ; map X
    db $12 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $05 ; special graphics bitflag
    dw $a5e5 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $a5cb ; room state pointer
    dw $e5e6 ; room state standard
org $8fa5ed
; room A5ED: Statues Hallway
Room_A5ED_Header:
    db $30 ; room index
    db $00 ; area
    db $2e ; map X
    db $08 ; map Y
    db $05 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a614 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa618
; room A618: [Red Tower Energy Charge Station]
Room_A618_Header:
    db $31 ; room index
    db $01 ; area
    db $1f ; map X
    db $12 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a63f ; doors pointer
    dw $e5e6 ; room state standard
org $8fa641
; room A641: [Kraid Recharge Station]
Room_A641_Header:
    db $32 ; room index
    db $01 ; area
    db $09 ; map X
    db $12 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a668 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa66a
; room A66A: Statues Room
RoomPtr_A66A:
    db $33 ; room index
    db $00 ; area
    db $2d ; map X
    db $08 ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a691 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa6a1
; room A6A1: Warehouse Entrance
RoomPtr_A6A1:
    db $34 ; room index
    db $01 ; area
    db $14 ; map X
    db $12 ; map Y
    db $03 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a6c8 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa6d0
; room A6A1: Warehouse Entrance
Room_A6A1_state_A6AE_Scroll:
    db $02,$00,$01,$01,$01,$00
org $8fa6d6
; room A6A1: Warehouse Entrance
Room_A6A1_state_A6AE_PLM_index_0_PLM_scroll_data:
    db $02,$02,$80
org $8fa6d9
; room A6A1: Warehouse Entrance
Room_A6A1_state_A6AE_PLM_index_2_PLM_scroll_data:
    db $01,$02,$80
org $8fa6dc
; room A6A1: Warehouse Entrance
Room_A6A1_state_A6AE_PLM_index_5_PLM_scroll_data:
    db $02,$00,$80
org $8fa6df
; room A6A1: Warehouse Entrance
Room_A6A1_state_A6AE_PLM_index_9_PLM_scroll_data:
    db $02,$01,$80
org $8fa6e2
; room A6E2: Varia Suit Room
Room_A6E2_Header:
    db $35 ; room index
    db $01 ; area
    db $06 ; map X
    db $13 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $02 ; special graphics bitflag
    dw $a709 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa70b
; room A70B: [Kraid Save Room]
RoomPtr_A70B:
    db $36 ; room index
    db $01 ; area
    db $0e ; map X
    db $12 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a732 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa734
; room A734: [Caterpillar Save Room]
RoomPtr_A734:
    db $37 ; room index
    db $01 ; area
    db $19 ; map X
    db $08 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a75b ; doors pointer
    dw $e5e6 ; room state standard
org $8fa75d
; room A75D: Ice Beam Acid Room
Room_A75D_Header:
    db $00 ; room index
    db $02 ; area
    db $39 ; map X
    db $03 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a784 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa788
; room A788: Cathedral
Room_A788_Header:
    db $01 ; room index
    db $02 ; area
    db $2e ; map X
    db $03 ; map Y
    db $03 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a7af ; doors pointer
    dw $e5e6 ; room state standard
org $8fa7b3
; room A7B3: Cathedral Entrance
Room_A7B3_Header:
    db $02 ; room index
    db $02 ; area
    db $31 ; map X
    db $03 ; map Y
    db $03 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a7da ; doors pointer
    dw $e5e6 ; room state standard
org $8fa7de
; room A7DE: Business Center
RoomPtr_A7DE:
    db $03 ; room index
    db $02 ; area
    db $34 ; map X
    db $00 ; map Y
    db $01 ; width
    db $07 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a805 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa815
; room A815: Ice Beam Gate Room
Room_A815_Header:
    db $04 ; room index
    db $02 ; area
    db $35 ; map X
    db $01 ; map Y
    db $07 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a83c ; doors pointer
    dw $e5e6 ; room state standard
org $8fa844
; room A815: Ice Beam Gate Room
Room_A815_state_A822_Scroll:
    db $00,$00,$00,$02,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01,$01,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01
org $8fa865
; room A865: Ice Beam Tutorial Room
Room_A865_Header:
    db $05 ; room index
    db $02 ; area
    db $39 ; map X
    db $01 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a88c ; doors pointer
    dw $e5e6 ; room state standard
org $8fa890
; room A890: Ice Beam Room
Room_A890_Header:
    db $06 ; room index
    db $02 ; area
    db $39 ; map X
    db $02 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a8b7 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa8b9
; room A8B9: Ice Beam Snake Room
Room_A8B9_Header:
    db $07 ; room index
    db $02 ; area
    db $3a ; map X
    db $01 ; map Y
    db $02 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a8e0 ; doors pointer
    dw $e5e6 ; room state standard
org $8fa8e6
; room A8B9: Ice Beam Snake Room
Room_A8B9_state_A8C6_Scroll:
    db $00,$02,$00,$02,$00,$01
org $8fa8ec
; room A8B9: Ice Beam Snake Room
Room_A8B9_state_A8C6_PLM_index_0_PLM_scroll_data:
    db $02,$01,$80
org $8fa8ef
; room A8B9: Ice Beam Snake Room
Room_A8B9_state_A8C6_PLM_index_1_PLM_scroll_data:
    db $02,$00,$80
org $8fa8f2
; room A8B9: Ice Beam Snake Room
Room_A8B9_state_A8C6_PLM_index_2_PLM_scroll_data:
    db $03,$02,$80
org $8fa8f5
; room A8B9: Ice Beam Snake Room
Room_A8B9_state_A8C6_PLM_index_3_PLM_scroll_data:
    db $03,$00,$80
org $8fa8f8
; room A8F8: Crumble Shaft
Room_A8F8_Header:
    db $08 ; room index
    db $02 ; area
    db $3c ; map X
    db $04 ; map Y
    db $01 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $a91f ; doors pointer
    dw $e5e6 ; room state standard
org $8fa923
; room A923: Crocomire Speedway
RoomPtr_A923:
    db $09 ; room index
    db $02 ; area
    db $2f ; map X
    db $07 ; map Y
    db $0d ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $02 ; special graphics bitflag
    dw $a94a ; doors pointer
    dw $e5e6 ; room state standard
org $8fa954
; room A923: Crocomire Speedway
Room_A923_state_A930_Scroll:
    db $02,$00,$00,$00,$00,$00,$00,$02,$02,$02,$02,$02,$02,$02,$00,$00,$00,$00,$00,$02,$02,$02,$02,$00,$00,$00,$02,$00,$02,$02,$02,$02,$02,$02,$00,$00,$00,$00,$00,$19,$02,$26,$02,$80
org $8fa980
; Room A923: Crocomire Speedway
Room_A923_state_A930_PLM_index_0_PLM_scroll_data:
    db $1b,$02,$80
org $8fa987
; room A923: Crocomire Speedway
Room_A923_state_A930_PLM_index_5_PLM_scroll_data:
    db $1b,$02,$80
org $8fa98a
; room A923: Crocomire Speedway
Room_A923_state_A930_PLM_index_8_PLM_scroll_data:
    db $1b,$00,$80
org $8fa98d
; room A98D: Crocomire's Room
Room_A98D_Header:
    db $0a ; room index
    db $02 ; area
    db $2c ; map X
    db $0a ; map Y
    db $08 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $01 ; special graphics bitflag
    dw $a9d3 ; doors pointer
    dw $e629 ; room state Bosses
    db $02 ; event
    dw $a9b9 ; room state pointer
    dw $e5e6 ; room state standard
org $8fa99f
; room A98D: Crocomire's Room
Room_A98D_state_A99F_Header:
    dl $c79d71 ; Level data pointer
    db $1b ; Tileset
    db $27 ; Song Set
    db $05 ; Play Index
    dw $84d0 ; FX pointer
    dw $bb0e ; Enemy Set pointer
    dw $8b11 ; Enemy GFX pointer
    dw $0101 ; Background X/Y scrolling
    dw $a9d7 ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $e8cd ; Main ASM pointer
    dw Room_A98D_PLM ; PLM Set pointer (in freespace)
    dw $b84d ; Background pointer
    dw $91f6 ; Setup ASM pointer
org $8fa9e5
; room A9E5: Hi Jump Boots Room
Room_A9E5_Header:
    db $0b ; room index
    db $02 ; area
    db $37 ; map X
    db $06 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $aa0c ; doors pointer
    dw $e5e6 ; room state standard
org $8faa0e
; room AA0E: Crocomire Escape
Room_AA0E_Header:
    db $0c ; room index
    db $02 ; area
    db $30 ; map X
    db $06 ; map Y
    db $04 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $aa35 ; doors pointer
    dw $e5e6 ; room state standard
org $8faa41
; room AA41: Hi Jump Energy Tank Room
Room_AA41_Header:
    db $0d ; room index
    db $02 ; area
    db $35 ; map X
    db $05 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $aa68 ; doors pointer
    dw $e5e6 ; room state standard
org $8faa6c
; room AA41: Hi Jump Energy Tank Room
Room_AA41_state_AA4E_Scroll:
    db $01,$00,$00,$00
org $8faa70
; room AA41: Hi Jump Energy Tank Room
Room_AA41_state_AA4E_PLM_index_1_PLM_scroll_data:
    db $01,$02,$03,$02,$80
org $8faa75
; room AA41: Hi Jump Energy Tank Room
Room_AA41_state_AA4E_PLM_index_0_PLM_scroll_data:
    db $01,$02,$03,$02,$80,$ff,$ff
org $8faa7c
; room AA41: Hi Jump Energy Tank Room
Room_AA41_state_AA4E_PLM_index_2_PLM_scroll_data:
    db $02,$00,$80
org $8faa7f
; room AA41: Hi Jump Energy Tank Room
Room_AA41_state_AA4E_PLM_index_3_PLM_scroll_data:
    db $02,$02,$80
org $8faa82
; room AA82: Post Crocomire Farming Room
RoomPtr_AA82:
    db $0e ; room index
    db $02 ; area
    db $34 ; map X
    db $0a ; map Y
    db $02 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $02 ; special graphics bitflag
    dw $aaa9 ; doors pointer
    dw $e5e6 ; room state standard
org $8faab5
; room AAB5: [Post Crocomire Save Room]
RoomPtr_AAB5:
    db $0f ; room index
    db $02 ; area
    db $33 ; map X
    db $0b ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $aadc ; doors pointer
    dw $e5e6 ; room state standard
org $8faade
; room AADE: Post Crocomire Power Bomb Room
Room_AADE_Header:
    db $10 ; room index
    db $02 ; area
    db $36 ; map X
    db $0a ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ab05 ; doors pointer
    dw $e5e6 ; room state standard
org $8fab07
; room AB07: Post Crocomire Shaft
Room_AB07_Header:
    db $11 ; room index
    db $02 ; area
    db $35 ; map X
    db $0c ; map Y
    db $01 ; width
    db $05 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ab2e ; doors pointer
    dw $e5e6 ; room state standard
org $8fab3b
; room AB3B: Post Crocomire Missile Room
Room_AB3B_Header:
    db $12 ; room index
    db $02 ; area
    db $31 ; map X
    db $0f ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ab62 ; doors pointer
    dw $e5e6 ; room state standard
org $8fab64
; room AB64: Grapple Tutorial Room 3
Room_AB64_Header:
    db $13 ; room index
    db $02 ; area
    db $36 ; map X
    db $0c ; map Y
    db $03 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ab8b ; doors pointer
    dw $e5e6 ; room state standard
org $8fab8f
; room AB8F: Post Crocomire Jump Room
Room_AB8F_Header:
    db $14 ; room index
    db $02 ; area
    db $34 ; map X
    db $0f ; map Y
    db $08 ; width
    db $03 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $abb6 ; doors pointer
    dw $e5e6 ; room state standard
org $8fabba
; room AB8F: Post Crocomire Jump Room
Room_AB8F_state_AB9C_Scroll:
    db $00,$00,$00,$02,$02,$02,$02,$02,$00,$00,$00,$02,$02,$02,$02,$02,$01,$01,$01,$01,$01,$01,$01,$01
org $8fabd2
; room ABD2: Grapple Tutorial Room 2
Room_ABD2_Header:
    db $15 ; room index
    db $02 ; area
    db $39 ; map X
    db $0c ; map Y
    db $01 ; width
    db $03 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $abf9 ; doors pointer
    dw $e5e6 ; room state standard
org $8fac00
; room AC00: Grapple Tutorial Room 1
Room_AC00_Header:
    db $16 ; room index
    db $02 ; area
    db $3a ; map X
    db $0e ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ac27 ; doors pointer
    dw $e5e6 ; room state standard
org $8fac2b
; room AC2B: Grapple Beam Room
Room_AC2B_Header:
    db $17 ; room index
    db $02 ; area
    db $3c ; map X
    db $0e ; map Y
    db $01 ; width
    db $04 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ac52 ; doors pointer
    dw $e5e6 ; room state standard
org $8fac5a
; room AC5A: Norfair Reserve Tank Room
Room_AC5A_Header:
    db $18 ; room index
    db $02 ; area
    db $2b ; map X
    db $02 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ac81 ; doors pointer
    dw $e5e6 ; room state standard
org $8fac83
; room AC83: Green Bubbles Missile Room
Room_AC83_Header:
    db $19 ; room index
    db $02 ; area
    db $29 ; map X
    db $02 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $acaa ; doors pointer
    dw $e5e6 ; room state standard
org $8facae
; room AC83: Green Bubbles Missile Room
Room_AC83_state_AC90_Scroll:
    db $01,$00
org $8facb0
; room AC83: Green Bubbles Missile Room
Room_AC83_state_AC90_PLM_index_0_PLM_scroll_data:
    db $01,$01,$80
org $8facb3
; room ACB3: Bubble Mountain
Room_ACB3_Header:
    db $1a ; room index
    db $02 ; area
    db $27 ; map X
    db $02 ; map Y
    db $02 ; width
    db $04 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $acda ; doors pointer
    dw $e5e6 ; room state standard
org $8facf0
; room ACF0: Speed Booster Hall
Room_ACF0_Header:
    db $1b ; room index
    db $02 ; area
    db $1a ; map X
    db $01 ; map Y
    db $0c ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ad17 ; doors pointer
    dw $e5e6 ; room state standard
org $8fad1b
; room AD1B: Speed Booster Room
Room_AD1B_Header:
    db $1c ; room index
    db $02 ; area
    db $19 ; map X
    db $02 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ad5c ; doors pointer
    dw $e5e6 ; room state standard
org $8fad5e
; room AD5E: Single Chamber
Room_AD5E_Header:
    db $1d ; room index
    db $02 ; area
    db $21 ; map X
    db $03 ; map Y
    db $06 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ad85 ; doors pointer
    dw $e5e6 ; room state standard
org $8fad8f
; room AD5E: Single Chamber
Room_AD5E_state_AD6B_Scroll:
    db $01,$01,$01,$01,$00,$02,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$01
org $8fada7
; room AD5E: Single Chamber
Room_AD5E_state_AD6B_PLM_index_0_PLM_scroll_data:
    db $04,$00,$80
org $8fadaa
; room AD5E: Single Chamber
Room_AD5E_state_AD6B_PLM_index_4_PLM_scroll_data:
    db $04,$01,$80
org $8fadad
; room ADAD: Double Chamber
Room_ADAD_Header:
    db $1e ; room index
    db $02 ; area
    db $22 ; map X
    db $04 ; map Y
    db $04 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $add4 ; doors pointer
    dw $e5e6 ; room state standard
org $8fadde
; room ADDE: Wave Beam Room
Room_ADDE_Header:
    db $1f ; room index
    db $02 ; area
    db $21 ; map X
    db $04 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ae05 ; doors pointer
    dw $e5e6 ; room state standard
org $8fae07
; room AE07: Spiky Platforms Tunnel
Room_AE07_Header:
    db $20 ; room index
    db $02 ; area
    db $22 ; map X
    db $06 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ae2e ; doors pointer
    dw $e5e6 ; room state standard
org $8fae32
; room AE32: Volcano Room
Room_AE32_Header:
    db $21 ; room index
    db $02 ; area
    db $21 ; map X
    db $06 ; map Y
    db $03 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ae59 ; doors pointer
    dw $e5e6 ; room state standard
org $8fae5d
; room AE32: Volcano Room
Room_AE32_state_AE3F_Scroll:
    db $02,$00,$00,$02,$00,$00,$01,$00,$00
org $8fae66
; room AE32: Volcano Room
Room_AE32_state_AE3F_PLM_index_0_PLM_scroll_data:
    db $07,$01,$08,$01,$80
org $8fae6b
; room AE32: Volcano Room
Room_AE32_state_AE3F_PLM_index_1_PLM_scroll_data:
    db $06,$01,$80
org $8fae6e
; room AE32: Volcano Room
Room_AE32_state_AE3F_PLM_index_7_PLM_scroll_data:
    db $06,$00,$80
org $8fae74
; room AE74: Kronic Boost Room
Room_AE74_Header:
    db $22 ; room index
    db $02 ; area
    db $24 ; map X
    db $08 ; map Y
    db $02 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ae9b ; doors pointer
    dw $e5e6 ; room state standard
org $8faea3
; room AE74: Kronic Boost Room
Room_AE74_state_AE81_Scroll:
    db $02,$00,$02,$00,$01,$00
org $8faea9
; room AE74: Kronic Boost Room
Room_AE74_state_AE81_PLM_index_0_PLM_scroll_data:
    db $03,$01,$80
org $8faeac
; room AE74: Kronic Boost Room
Room_AE74_state_AE81_PLM_index_1_PLM_scroll_data:
    db $02,$02,$03,$00,$80
org $8faeb1
; room AE74: Kronic Boost Room
Room_AE74_state_AE81_PLM_index_5_PLM_scroll_data:
    db $02,$00,$80
org $8faeb4
; room AEB4: Magdollite Tunnel
Room_AEB4_Header:
    db $23 ; room index
    db $02 ; area
    db $25 ; map X
    db $08 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $aedb ; doors pointer
    dw $e5e6 ; room state standard
org $8faedf
; room AEDF: Purple Shaft
Room_AEDF_Header:
    db $24 ; room index
    db $02 ; area
    db $28 ; map X
    db $06 ; map Y
    db $01 ; width
    db $03 ; height
    db $a0 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $af06 ; doors pointer
    dw $e5e6 ; room state standard
org $8faf14
; room AF14: Lava Dive Room
Room_AF14_Header:
    db $25 ; room index
    db $02 ; area
    db $25 ; map X
    db $0a ; map Y
    db $04 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $af3b ; doors pointer
    dw $e5e6 ; room state standard
org $8faf3f
; room AF3F: [Elevator to Lower Norfair]
RoomPtr_AF3F:
    db $26 ; room index
    db $02 ; area
    db $29 ; map X
    db $0a ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $af66 ; doors pointer
    dw $e5e6 ; room state standard
org $8faf72
; room AF72: Upper Norfair Farming Room
Room_AF72_Header:
    db $27 ; room index
    db $02 ; area
    db $29 ; map X
    db $05 ; map Y
    db $02 ; width
    db $02 ; height
    db $a0 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $af99 ; doors pointer
    dw $e5e6 ; room state standard
org $8fafa3
; room AFA3: Rising Tide
Room_AFA3_Header:
    db $28 ; room index
    db $02 ; area
    db $29 ; map X
    db $04 ; map Y
    db $05 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $afca ; doors pointer
    dw $e5e6 ; room state standard
org $8fafce
; room AFCE: Acid Snakes Tunnel
Room_AFCE_Header:
    db $29 ; room index
    db $02 ; area
    db $2b ; map X
    db $09 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $aff5 ; doors pointer
    dw $e5e6 ; room state standard
org $8faffb
; room AFFB: Spiky Acid Snakes Tunnel
Room_AFFB_Header:
    db $2a ; room index
    db $02 ; area
    db $26 ; map X
    db $09 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b022 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb026
; room B026: [Crocomire Recharge Room]
Room_B026_Header:
    db $2b ; room index
    db $02 ; area
    db $2a ; map X
    db $09 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b04d ; doors pointer
    dw $e5e6 ; room state standard
org $8fb051
; room B051: Purple Farming Room
Room_B051_Header:
    db $2c ; room index
    db $02 ; area
    db $27 ; map X
    db $07 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b078 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb07a
; room B07A: Bat Cave
Room_B07A_Header:
    db $2d ; room index
    db $02 ; area
    db $26 ; map X
    db $01 ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b0a1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb0b4
; room B0B4: Norfair Map Room
Room_B0B4_Header:
    db $2e ; room index
    db $02 ; area
    db $35 ; map X
    db $04 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b0db ; doors pointer
    dw $e5e6 ; room state standard
org $8fb0dd
; room B0DD: [Bubble Mountain Save Room]
RoomPtr_B0DD:
    db $2f ; room index
    db $02 ; area
    db $29 ; map X
    db $03 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b104 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb106
; room B106: Frog Speedway
Room_B106_Header:
    db $30 ; room index
    db $02 ; area
    db $2b ; map X
    db $05 ; map Y
    db $08 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b12d ; doors pointer
    dw $e5e6 ; room state standard
org $8fb139
; room B139: Red Pirate Shaft
Room_B139_Header:
    db $31 ; room index
    db $02 ; area
    db $2b ; map X
    db $06 ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b160 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb167
; room B167: [Business Center Save Room]
RoomPtr_B167:
    db $32 ; room index
    db $02 ; area
    db $33 ; map X
    db $05 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b18e ; doors pointer
    dw $e5e6 ; room state standard
org $8fb192
; room B192: [Crocomire Save Room]
RoomPtr_B192:
    db $33 ; room index
    db $02 ; area
    db $2e ; map X
    db $08 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b1b9 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb1bb
; room B1BB: [Elevator Save Room]
RoomPtr_B1BB:
    db $34 ; room index
    db $02 ; area
    db $2a ; map X
    db $0a ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b1e2 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb1e5
; room B1E5: Acid Statue Room
Room_B1E5_Header:
    db $35 ; room index
    db $02 ; area
    db $2d ; map X
    db $0d ; map Y
    db $03 ; width
    db $03 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b20c ; doors pointer
    dw $e5e6 ; room state standard
org $8fb210
; room B1E5: Acid Statue Room
Room_B1E5_state_B1F2_Scroll:
    db $00,$02,$02,$00,$01,$01,$00,$00,$00,$03,$01,$04,$01,$06,$00,$07,$00,$08,$00,$80
org $8fb224
; room B1E5: Acid Statue Room
Room_B1E5_state_B1F2_PLM_index_0_PLM_scroll_data:
    db $04,$02,$05,$02,$07,$02,$08,$02,$80
org $8fb236
; room B236: Main Hall
RoomPtr_B236:
    db $36 ; room index
    db $02 ; area
    db $26 ; map X
    db $0b ; map Y
    db $08 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b25d ; doors pointer
    dw $e5e6 ; room state standard
org $8fb265
; room B236: Main Hall
Room_B236_state_B243_Scroll:
    db $00,$00,$00,$02,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01,$01,$01,$01,$01,$01
org $8fb27d
; room B236: Main Hall
Room_B236_state_B243_PLM_index_2_PLM_scroll_data:
    db $0b,$02,$80
org $8fb280
; room B236: Main Hall
Room_B236_state_B243_PLM_index_4_PLM_scroll_data:
    db $0b,$00,$80
org $8fb283
; room B283: Golden Torizo's Room
RoomPtr_B283:
    db $37 ; room index
    db $02 ; area
    db $2b ; map X
    db $0f ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b2c9 ; doors pointer
    dw $e629 ; room state Bosses
    db $04 ; event
    dw $b2af ; room state pointer
    dw $e5e6 ; room state standard
org $8fb2cd
; room B283: Golden Torizo's Room
Room_B283_state_B2AF_Scroll:
    db $00,$02,$01,$00
org $8fb2da
; room B2DA: Fast Ripper Room
Room_B2DA_Header:
    db $38 ; room index
    db $02 ; area
    db $26 ; map X
    db $0e ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b301 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb305
; room B305: [Screw Attack Energy Charge Room]
Room_B305_Header:
    db $39 ; room index
    db $02 ; area
    db $29 ; map X
    db $0f ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b32c ; doors pointer
    dw $e5e6 ; room state standard
org $8fb32e
; room B32E: Ridley's Room
Room_B32E_Header:
    db $3a ; room index
    db $02 ; area
    db $27 ; map X
    db $10 ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b374 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $b35a ; room state pointer
    dw $e5e6 ; room state standard
org $8fb37a
; room B37A: Lower Norfair Farming Room
RoomPtr_B37A:
    db $3b ; room index
    db $02 ; area
    db $24 ; map X
    db $10 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b3a1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb3a5
; room B3A5: Fast Pillars Setup Room
Room_B3A5_Header:
    db $3c ; room index
    db $02 ; area
    db $25 ; map X
    db $0c ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b3cc ; doors pointer
    dw $e5e6 ; room state standard
org $8fb40a
; room B40A: Mickey Mouse Room
Room_B40A_Header:
    db $3e ; room index
    db $02 ; area
    db $21 ; map X
    db $09 ; map Y
    db $04 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b431 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb435
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_Scroll:
    db $02,$00,$00,$00,$02,$00,$00,$00,$02,$00,$00,$00,$01,$01,$01,$01
org $8fb445
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_PLM_index_0_PLM_scroll_data:
    db $05,$01,$80
org $8fb448
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_PLM_index_1_PLM_scroll_data:
    db $05,$00,$80
org $8fb44b
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_PLM_index_2_PLM_scroll_data:
    db $04,$01,$80
org $8fb44e
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_PLM_index_6_PLM_scroll_data:
    db $04,$00,$80
org $8fb451
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_PLM_index_A_PLM_scroll_data:
    db $0d,$01,$80
org $8fb454
; room B40A: Mickey Mouse Room
Room_B40A_state_B417_PLM_index_D_PLM_scroll_data:
    db $0d,$00,$80
org $8fb457
; room B457: Pillar Room
Room_B457_Header:
    db $3f ; room index
    db $02 ; area
    db $21 ; map X
    db $0e ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b47e ; doors pointer
    dw $e5e6 ; room state standard
org $8fb482
; room B482: Plowerhouse Room
Room_B482_Header:
    db $40 ; room index
    db $02 ; area
    db $21 ; map X
    db $10 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b4a9 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb4ad
; room B4AD: The Worst Room In The Game
Room_B4AD_Header:
    db $41 ; room index
    db $02 ; area
    db $20 ; map X
    db $09 ; map Y
    db $01 ; width
    db $06 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b4d4 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb4e5
; room B4E5: Amphitheatre
Room_B4E5_Header:
    db $42 ; room index
    db $02 ; area
    db $1c ; map X
    db $09 ; map Y
    db $04 ; width
    db $05 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b50c ; doors pointer
    dw $e5e6 ; room state standard
org $8fb510
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_Header:
    db $43 ; room index
    db $02 ; area
    db $19 ; map X
    db $05 ; map Y
    db $05 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b537 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb53d
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_state_B51D_Scroll:
    db $02,$00,$00,$00,$02,$00,$00,$00,$01,$01
org $8fb547
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_state_B51D_PLM_index_0_PLM_scroll_data:
    db $02,$01,$03,$01,$08,$00,$80
org $8fb54e
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_state_B51D_PLM_index_4_PLM_scroll_data:
    db $01,$00,$02,$00,$03,$00,$08
org $8fb555
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_state_B51D_PLM_index_C_PLM_scroll_data:
    db $01,$80,$01,$01,$80
org $8fb55a
; room B55A: Lower Norfair Escape Power Bomb Room
Room_B55A_Header:
    db $44 ; room index
    db $02 ; area
    db $19 ; map X
    db $06 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b581 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb585
; room B585: Red Keyhunter Shaft
Room_B585_Header:
    db $45 ; room index
    db $02 ; area
    db $19 ; map X
    db $09 ; map Y
    db $03 ; width
    db $05 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b5ac ; doors pointer
    dw $e5e6 ; room state standard
org $8fb5b4
; room B585: Red Keyhunter Shaft
Room_B585_state_B592_Scroll:
    db $00,$00,$01,$00,$00,$02,$00,$00,$02,$00,$00,$02,$02,$00,$02
org $8fb5cd
; room B585: Red Keyhunter Shaft
Room_B585_state_B592_PLM_index_6_PLM_scroll_data:
    db $02,$02,$05,$02,$80
org $8fb5d2
; room B585: Red Keyhunter Shaft
Room_B585_state_B592_PLM_index_A_PLM_scroll_data:
    db $02,$02,$80
org $8fb5d5
; room B5D5: Wasteland
Room_B5D5_Header:
    db $46 ; room index
    db $02 ; area
    db $19 ; map X
    db $0e ; map Y
    db $06 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b5fc ; doors pointer
    dw $e5e6 ; room state standard
org $8fb600
; room B5D5: Wasteland
Room_B5D5_state_B5E2_Scroll:
    db $01,$00,$01,$01,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$02,$00
org $8fb612
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM_index_0_PLM_scroll_data:
    db $0a,$02,$80
org $8fb615
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM_index_2_PLM_scroll_data:
    db $04,$01,$0a,$00,$80
org $8fb61a
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM_index_C_PLM_scroll_data:
    db $01,$01,$80
org $8fb61d
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM_index_A_PLM_scroll_data:
    db $04,$01,$05,$01,$80
org $8fb622
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM_index_B_PLM_scroll_data:
    db $01,$00,$80
org $8fb625
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM_index_D_PLM_scroll_data:
    db $05,$00,$80
org $8fb628
; room B5D5: Wasteland
Room_B5D5_state_B5E2_PLM_index_11_PLM_scroll_data:
    db $04,$00,$80
org $8fb656
; room B656: Three Muskateers' Room
Room_B656_Header:
    db $48 ; room index
    db $02 ; area
    db $1e ; map X
    db $03 ; map Y
    db $04 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b67d ; doors pointer
    dw $e5e6 ; room state standard
org $8fb681
; room B656: Three Muskateers' Room
Room_B656_state_B663_Scroll:
    db $00,$00,$02,$00,$00,$00,$02,$00,$01,$01,$01,$00
org $8fb68d
; room B656: Three Muskateers' Room
Room_B656_state_B663_PLM_index_0_PLM_scroll_data:
    db $0a,$00,$80
org $8fb690
; room B656: Three Muskateers' Room
Room_B656_state_B663_PLM_index_6_PLM_scroll_data:
    db $0a,$01,$0b,$01,$80
org $8fb695
; room B656: Three Muskateers' Room
Room_B656_state_B663_PLM_index_7_PLM_scroll_data:
    db $0b,$00,$80
org $8fb698
; room B698: Ridley Tank Room
Room_B698_Header:
    db $49 ; room index
    db $02 ; area
    db $28 ; map X
    db $11 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b6bf ; doors pointer
    dw $e5e6 ; room state standard
org $8fb6c1
; room B6C1: Screw Attack Room
Room_B6C1_Header:
    db $4a ; room index
    db $02 ; area
    db $2a ; map X
    db $0e ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b6e8 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb6ee
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_Header:
    db $4b ; room index
    db $02 ; area
    db $19 ; map X
    db $06 ; map Y
    db $03 ; width
    db $06 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b715 ; doors pointer
    dw $e5e6 ; room state standard
org $8fb71b
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_state_B6FB_Scroll:
    db $00,$02,$00,$00,$02,$00,$00,$02,$00,$00,$01,$00,$00,$00,$00,$01,$01,$00
org $8fb72d
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_state_B6FB_PLM_index_2_PLM_scroll_data:
    db $09,$01,$80
org $8fb730
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_state_B6FB_PLM_index_5_PLM_scroll_data:
    db $09,$02,$0c,$02,$0d,$02,$80
org $8fb737
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_state_B6FB_PLM_index_9_PLM_scroll_data:
    db $02,$01,$04,$00,$80
org $8fb741
; room B741: [Red Keyhunter Shaft Save Room]
RoomPtr_B741:
    db $4c ; room index
    db $02 ; area
    db $1a ; map X
    db $0c ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $b768 ; doors pointer
    dw $e5e6 ; room state standard
org $8fc215
; room C98E: Bowling Alley
Room_C98E_state_C9A0_PLM:
    ; Scroll PLM
    dw $b703 : db $1f : db $2d : dw Room_C98E_state_C9BA_PLM_index_0_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $40 : db $2a : dw $8000 
    ; Upwards extension
    dw $b647 : db $41 : db $27 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $16 : db $1d : dw $a286 
    dw $0000
org $8fc22f
; room CA08: Wrecked Ship Entrance
Room_CA08_state_CA1A_PLM:
    dw $0000
org $8fc231
; room CA52: Attic
Room_CA52_state_CA64_PLM:
Door_80_Room_CA52_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0080 
Door_81_Room_CA52_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $6e : db $06 : dw $0081 
    ; Wrecked Ship attic
    dw $bb05 : db $08 : db $08 : dw $8000 
    dw $0000
org $8fc245
; room CAAE: Wrecked Ship East Missile Room
Room_CAAE_state_CAC0_PLM:
    dw $0000
org $8fc247
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_state_CB22_PLM:
    ; Scroll PLM
    dw $b703 : db $21 : db $57 : dw Room_CAF6_state_CB22_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $0e : db $66 : dw Room_CAF6_state_CB22_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $1e : db $57 : dw Room_CAF6_state_CB22_PLM_index_2_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $11 : db $69 : dw Room_CAF6_state_CB22_PLM_index_3_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $18 : db $6d : dw Room_CAF6_state_CB22_PLM_index_4_PLM_scroll_data
    ; Missile tank
    dw $eedb : db $5d : db $59 : dw $0080 
Door_82_Room_CAF6_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $1e : db $66 : dw $0082 
Door_83_Room_CAF6_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $11 : db $46 : dw $0083 
Door_84_Room_CAF6_PLM_C87E:
    ; Door. Green door facing up
    dw $c87e : db $16 : db $7d : dw $0084 
    dw $0000
org $8fc27f
; room CB8B: Spiky Death Room
Room_CB8B_state_CB9D_PLM:
    dw $0000
org $8fc281
; room CBD5: Electric Death Room
Room_CBD5_state_CBE7_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $10 : dw $cc24 
    ; Rightwards extension
    dw $b63b : db $08 : db $10 : dw $8000 
    dw $0000
org $8fc28f
; room CC27: Wrecked Ship Energy Tank Room
Room_CC27_state_CC39_PLM:
    dw $0000
org $8fc291
; room CC6F: Basement
Room_CC6F_state_CC81_PLM:
    ; Scroll PLM
    dw $b703 : db $0f : db $0f : dw Room_CC6F_state_CC9B_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $08 : db $0c : dw Room_CC6F_state_CC9B_PLM_index_1_PLM_scroll_data 
Door_85_Room_CC6F_PLM_DB4C:
    ; Door. Eye door, facing right
    dw $db4c : db $01 : db $06 : dw $0085 
    ; Eye door bottom, facing right
    dw $db52 : db $01 : db $09 : dw $0085 
    ; Eye door eye, facing right
    dw $db48 : db $01 : db $07 : dw $0085 
    dw $0000
org $8fc2b1
; room CCCB: Wrecked Ship Map Room
Room_CCCB_state_CCDD_PLM:
    dw $0000
org $8fc2b3
; room CD13: Phantoon's Room
Room_CD13_state_CD3F_PLM:
Door_86_Room_CD13_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $0e : db $06 : dw $0086 
    dw $0000
org $8fc2bb
; room CD5C: Sponge Bath
Room_CD5C_state_CD6E_PLM:
    dw $0000
org $8fc2bd
; room CDA8: Wrecked Ship West Super Room
Room_CDA8_state_CDBA_PLM:
    dw $0000
org $8fc2bf
; room CDF1: Wrecked Ship East Super Room
Room_CDF1_state_CE03_PLM:
    ; Scroll PLM
    dw $b703 : db $10 : db $07 : dw Room_CDF1_state_CE1D_PLM_index_0_PLM_scroll_data 
    dw $0000
org $8fc2c7
; room CE8A: [Wrecked Ship Save Room]
Room_CE8A_state_CE9C_PLM:
    dw $0000
org $8fc2c9
; room CE8A: [Wrecked Ship Save Room]
Room_CE8A_state_CEB6_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0000 
    dw $0000
org $8fc2fd
; room CA08: Wrecked Ship Entrance
Room_CA08_state_CA34_PLM:
    dw $0000
org $8fc2ff
; room CA52: Attic
Room_CA52_state_CA7E_PLM:
Door_88_Room_CA52_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0c88 
Door_89_Room_CA52_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $6e : db $06 : dw $0c89 
Door_8A_Room_CA52_PLM_C84E:
    ; Door. Grey door facing up
    dw $c84e : db $26 : db $0e : dw $0c8a 
    ; Wrecked Ship attic
    dw $bb05 : db $08 : db $08 : dw $8000 
    dw $0000
org $8fc319
; room CAAE: Wrecked Ship East Missile Room
Room_CAAE_state_CADA_PLM:
    ; Missile tank
    dw $eedb : db $02 : db $08 : dw $0083 
    dw $0000
org $8fc321
; room CB8B: Spiky Death Room
Room_CB8B_state_CBB7_PLM:
    dw $0000
org $8fc323
; room CBD5: Electric Death Room
Room_CBD5_state_CC01_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $10 : dw $cc24 
    ; Rightwards extension
    dw $b63b : db $08 : db $10 : dw $8000 
Door_8B_Room_CBD5_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $0e : db $06 : dw $008b 
    dw $0000
org $8fc337
; room CC27: Wrecked Ship Energy Tank Room
Room_CC27_state_CC53_PLM:
    ; Energy tank
    dw $eed7 : db $2c : db $06 : dw $0084 
    dw $0000
org $8fc33f
; room CC6F: Basement
Room_CC6F_state_CC9B_PLM:
    ; Scroll PLM
    dw $b703 : db $0f : db $0f : dw Room_CC6F_state_CC9B_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $08 : db $0c : dw Room_CC6F_state_CC9B_PLM_index_1_PLM_scroll_data 
    dw $0000
org $8fc34d
; room CCCB: Wrecked Ship Map Room
Room_CCCB_state_CCF7_PLM:
    ; Map station
    dw $b6d3 : db $0b : db $0a : dw $8000 
    dw $0000
org $8fc355
; room CD5C: Sponge Bath
Room_CD5C_state_CD88_PLM:
    dw $0000
org $8fc357
; room CDA8: Wrecked Ship West Super Room
Room_CDA8_state_CDD4_PLM:
    ; Super missile tank
    dw $eedf : db $0d : db $07 : dw $0085 
    dw $0000
org $8fc35f
; room CDF1: Wrecked Ship East Super Room
Room_CDF1_state_CE1D_PLM:
    ; Scroll PLM
    dw $b703 : db $10 : db $07 : dw Room_CDF1_state_CE1D_PLM_index_0_PLM_scroll_data 
    ; Super missile tank
    dw $eedf : db $07 : db $09 : dw $0086 
    dw $0000
org $8fc36d
; room CE40: Gravity Suit Room
Room_CE40_state_CE6C_PLM:
    ; Gravity suit, chozo orb
    dw $ef5f : db $07 : db $09 : dw $0087 
    dw $0000
org $8fc375
; room CED2: [Glass Tunnel Save Room]
Room_CED2_state_CEDF_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0000 
    dw $0000
org $8fc37d
; room CEFB: Glass Tunnel
Room_CEFB_state_CF27_PLM:
    ; Scroll PLM
    dw $b703 : db $03 : db $14 : dw $cf4c 
    ; Rightwards extension
    dw $b63b : db $04 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $05 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $06 : db $14 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $09 : db $14 : dw $cf4c 
    ; Rightwards extension
    dw $b63b : db $0a : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0b : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0c : db $14 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $05 : db $1d : dw $cf4f 
    ; Rightwards extension
    dw $b63b : db $06 : db $1d : dw $8000 
    ; Rightwards extension
    dw $b63b : db $07 : db $1d : dw $8000 
    ; Rightwards extension
    dw $b63b : db $08 : db $1d : dw $8000 
    ; Rightwards extension
    dw $b63b : db $09 : db $1d : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $1d : dw $8000 
    ; n00b tube
    dw $d70c : db $02 : db $15 : dw $0080 
Door_8C_Room_CEFB_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $26 : dw $008c 
    dw $0000
org $8fc3df
; room CF54: West Tunnel
Room_CF54_state_CF61_PLM:
    dw $0000
org $8fc3e1
; room CF80: East Tunnel
Room_CF80_state_CF8D_PLM:
    ; Scroll PLM
    dw $b703 : db $3a : db $09 : dw Room_CF80_state_CF8D_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $3a : db $10 : dw Room_CF80_state_CF8D_PLM_index_1_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $3a : db $16 : dw Room_CF80_state_CF8D_PLM_index_2_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $0a : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0a : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0a : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0a : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0a : db $01 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0a : db $01 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $35 : db $09 : dw Room_CF80_state_CF8D_PLM_index_9_PLM_scroll_data 
    ; Downwards closed gate
    dw $c82a : db $29 : db $05 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $29 : db $05 : dw $0008 
    dw $0000
org $8fc42b
; room CFC9: Main Street
Room_CFC9_state_CFD6_PLM:
    ; Scroll PLM
    dw $b703 : db $0a : db $29 : dw $d012 
Door_8D_Room_CFC9_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $11 : db $76 : dw $008d 
    ; Missile tank
    dw $eedb : db $21 : db $35 : dw $0088 
    ; Super missile tank
    dw $eedf : db $19 : db $28 : dw $0089 
    dw $0000
org $8fc445
; room D017: Fish Tank
Room_D017_state_D024_PLM:
    ; Upwards extension
    dw $b647 : db $1f : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1f : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1f : db $28 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $20 : db $29 : dw Room_D017_state_D024_PLM_index_7_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $30 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $30 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $30 : db $28 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $0f : db $29 : dw Room_D017_state_D024_PLM_index_7_PLM_scroll_data 
Door_8E_Room_D017_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $26 : dw $008e 
    dw $0000
org $8fc47d
; room D055: Mama Turtle Room
Room_D055_state_D062_PLM:
    ; Energy tank
    dw $eed7 : db $10 : db $0a : dw $008a 
    ; Missile tank, shot block
    dw $ef83 : db $03 : db $1d : dw $008b 
    dw $0000
org $8fc48b
; room D08A: Crab Tunnel
Room_D08A_state_D097_PLM:
    ; Downwards closed gate
    dw $c82a : db $31 : db $07 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $31 : db $07 : dw $000a 
    dw $0000
org $8fc499
; room D0B9: Mt. Everest
Room_D0B9_state_D0C6_PLM:
    dw $0000
org $8fc49b
; room D104: Red Fish Room
Room_D104_state_D111_PLM:
    ; Scroll PLM
    dw $b703 : db $0f : db $06 : dw Room_D104_state_D111_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $11 : db $06 : dw Room_D104_state_D111_PLM_index_1_PLM_scroll_data 
    dw $0000
org $8fc4a9
; room D13B: Watering Hole
Room_D13B_state_D148_PLM:
    ; Scroll PLM
    dw $b703 : db $18 : db $1f : dw Room_D13B_state_D148_PLM_index_0_PLM_scroll_data 
    ; Super missile tank
    dw $eedf : db $1b : db $26 : dw $008c 
    ; Missile tank
    dw $eedb : db $14 : db $27 : dw $008d 
    dw $0000
org $8fc4bd
; room D16D: Northwest Maridia Bug Room
Room_D16D_state_D17A_PLM:
    ; Upwards extension
    dw $b647 : db $1f : db $16 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1f : db $17 : dw $8000 
    ; Upwards extension
    dw $b647 : db $1f : db $18 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $1f : db $19 : dw Room_D16D_state_D17A_PLM_index_7_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $30 : db $16 : dw $8000 
    ; Upwards extension
    dw $b647 : db $30 : db $17 : dw $8000 
    ; Upwards extension
    dw $b647 : db $30 : db $18 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $30 : db $19 : dw Room_D16D_state_D17A_PLM_index_7_PLM_scroll_data 
    dw $0000
org $8fc4ef
; room D1A3: Crab Shaft
Room_D1A3_state_D1B0_PLM:
    ; Scroll PLM
    dw $b703 : db $18 : db $2d : dw Room_D1A3_state_D1B0_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $1e : db $2d : dw $8000 
Door_8F_Room_D1A3_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $36 : dw $008f 
    dw $0000
org $8fc503
; room D1DD: Pseudo Plasma Spark Room
Room_D1DD_state_D1EA_PLM:
    ; Upwards extension
    dw $b647 : db $20 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $20 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $20 : db $28 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $20 : db $29 : dw Room_D1DD_state_D1EA_PLM_index_3_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $22 : db $26 : dw $8000 
    ; Upwards extension
    dw $b647 : db $22 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $22 : db $28 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $22 : db $29 : dw Room_D1DD_state_D1EA_PLM_index_7_PLM_scroll_data 
    ; Missile tank
    dw $eedb : db $13 : db $28 : dw $008e 
    dw $0000
org $8fc53b
; room D21C: Crab Hole
Room_D21C_state_D229_PLM:
    ; Scroll PLM
    dw $b703 : db $07 : db $0e : dw $d24d 
    ; Scroll PLM
    dw $b703 : db $07 : db $11 : dw $d24d 
Door_90_Room_D21C_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $16 : dw $0090 
    dw $0000
org $8fc54f
; room D252: [Tunnel to West Sand Hall]
Room_D252_state_D25F_PLM:
    dw $0000
org $8fc551
; room D27E: Plasma Tutorial Room
Room_D27E_state_D28B_PLM:
    dw $0000
org $8fc553
; room D2AA: Plasma Room
Room_D2AA_state_D2B7_PLM:
Door_91_Room_D2AA_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $1e : db $06 : dw $0c91 
    ; Plasma beam, chozo orb
    dw $ef67 : db $06 : db $26 : dw $008f 
    dw $0000
org $8fc561
; room D2D9: Thread The Needle Room
Room_D2D9_state_D2E6_PLM:
    dw $0000
org $8fc563
; room D30B: Maridia Elevator Room
Room_D30B_state_D318_PLM:
    ; Elevator platform
    dw $b70b : db $06 : db $2c : dw $8000 
Door_92_Room_D30B_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $46 : dw $0092 
    dw $0000
org $8fc571
; room D340: Plasma Spark Room
Room_D340_state_D34D_PLM:
Door_93_Room_D340_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $11 : db $16 : dw $0093 
Door_94_Room_D340_PLM_C87E:
    ; Door. Green door facing up
    dw $c87e : db $36 : db $2d : dw $0094 
    dw $0000
org $8fc57f
; room D387: Plasma Climb
Room_D387_state_D394_PLM:
    dw $0000
org $8fc581
; room D3B6: Maridia Map Room
Room_D3B6_state_D3C3_PLM:
    ; Map station
    dw $b6d3 : db $05 : db $0a : dw $8000 
    dw $0000
org $8fc589
; room D3DF: [Maridia Elevator Save Room]
Room_D3DF_state_D3EC_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0001 
    dw $0000
org $8fc591
; room D408: [Vertical Tube]
Room_D408_state_D415_PLM:
    dw $0000
org $8fc593
; room D433: Bug Sand Hole
Room_D433_state_D440_PLM:
    dw $0000
org $8fc595
; room D461: West Sand Hall
Room_D461_state_D46E_PLM:
    dw $0000
org $8fc597
; room D48E: Oasis
Room_D48E_state_D49B_PLM:
    ; Scroll PLM
    dw $b703 : db $03 : db $14 : dw $d4bd 
    ; Rightwards extension
    dw $b63b : db $04 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $05 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $06 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $07 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $08 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $09 : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0b : db $14 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0c : db $14 : dw $8000 
Door_95_Room_D48E_PLM_C884:
    ; Door. Green door facing down
    dw $c884 : db $06 : db $02 : dw $0095 
    dw $0000
org $8fc5db
; room D4C2: East Sand Hall
Room_D4C2_state_D4CF_PLM:
    dw $0000
org $8fc5dd
; room D4EF: West Sand Hole
Room_D4EF_state_D4FC_PLM:
    ; Missile tank
    dw $eedb : db $19 : db $04 : dw $0090 
    ; Reserve tank, chozo orb
    dw $ef7b : db $10 : db $04 : dw $0091 
    dw $0000
org $8fc5eb
; room D51E: East Sand Hole
Room_D51E_state_D52B_PLM:
    ; Missile tank
    dw $eedb : db $1c : db $07 : dw $0092 
    ; Power bomb tank
    dw $eee3 : db $06 : db $10 : dw $0093 
    dw $0000
org $8fc5f9
; room D54D: [West Sand Fall]
Room_D54D_state_D55A_PLM:
    dw $0000
org $8fc5fb
; room D57A: [East Sand Fall]
Room_D57A_state_D587_PLM:
    dw $0000
org $8fc5fd
; room D5A7: Aqueduct
Room_D5A7_state_D5B4_PLM:
Door_96_Room_D5A7_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $5e : db $26 : dw $0096 
    ; Missile tank
    dw $eedb : db $13 : db $09 : dw $0094 
    ; Super missile tank
    dw $eedf : db $03 : db $08 : dw $0095 
    dw $0000
org $8fc611
; room D5EC: Butterfly Room
Room_D5EC_state_D5F9_PLM:
Door_97_Room_D5EC_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0097 
    dw $0000
org $8fc619
; room D617: Botwoon Hallway
Room_D617_state_D624_PLM:
    dw $0000
org $8fc61b
; room D646: Pants Room
Room_D646_state_D653_PLM:
    ; Scroll PLM
    dw $b703 : db $16 : db $32 : dw Room_D646_state_D653_PLM_index_4_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $17 : db $32 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $18 : db $32 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $19 : db $32 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $12 : db $0c : dw Room_D646_state_D653_PLM_index_4_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $0d : db $0b : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $0a : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $09 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $07 : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $06 : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $05 : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $04 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $0d : db $0e : dw Room_D646_state_D653_PLM_index_D_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $0d : db $0d : dw $8000 
    ; Upwards extension
    dw $b647 : db $0d : db $0c : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $0b : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $0a : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $09 : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $08 : dw $8000 
    ; Upwards extension
    dw $b647 : db $12 : db $07 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $08 : db $2b : dw Room_D646_state_D653_PLM_index_15_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $09 : db $2b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $2b : dw $8000 
    dw $0000
org $8fc6ad
; room D69A: [Pants Room West half]
Room_D69A_state_D6A7_PLM:
    ; Scroll PLM
    dw $b703 : db $05 : db $22 : dw $d6c8 
    ; Rightwards extension
    dw $b63b : db $06 : db $22 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $07 : db $22 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $08 : db $22 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $09 : db $22 : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $12 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $08 : db $1b : dw $d6cb 
    ; Rightwards extension
    dw $b63b : db $09 : db $1b : dw $8000 
    ; Rightwards extension
    dw $b63b : db $0a : db $1b : dw $8000 
    dw $0000
org $8fc6e5
; room D6D0: Spring Ball Room
Room_D6D0_state_D6DD_PLM:
    ; Spring ball, chozo orb
    dw $ef57 : db $07 : db $16 : dw $0096 
    dw $0000
org $8fc6ed
; room D6FD: Below Botwoon Energy Tank
Room_D6FD_state_D70A_PLM:
    dw $0000
org $8fc6ef
; room D72A: Colosseum
Room_D72A_state_D737_PLM:
Door_98_Room_D72A_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $06 : dw $0098 
Door_99_Room_D72A_PLM_C872:
    ; Door. Green door facing left
    dw $c872 : db $4e : db $26 : dw $0099 
Door_9A_Room_D72A_PLM_C878:
    ; Door. Green door facing right
    dw $c878 : db $01 : db $16 : dw $009a 
    dw $0000
org $8fc703
; room D765: [Aqueduct Save Room]
Room_D765_state_D772_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0002 
    dw $0000
org $8fc70b
; room D78F: The Precious Room
Room_D78F_state_D7BB_PLM:
    ; Scroll PLM
    dw $b703 : db $14 : db $0e : dw Room_D78F_state_D7BB_PLM_index_0_PLM_scroll_data 
    ; Rightwards extension
    dw $b63b : db $15 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $16 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $17 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $18 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $19 : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1a : db $0e : dw $8000 
    ; Rightwards extension
    dw $b63b : db $1b : db $0e : dw $8000 
Door_9B_Room_D78F_PLM_DB5A:
    ; Door. Eye door, facing left
    dw $db5a : db $1e : db $26 : dw $009b 
    ; Eye door bottom, facing left
    dw $db60 : db $1e : db $29 : dw $009b 
    ; Eye door eye, facing left
    dw $db56 : db $1e : db $27 : dw $009b 
    ; Missile tank, shot block
    dw $ef83 : db $03 : db $06 : dw $0097 
    dw $0000
org $8fc755
; room D7E4: Botwoon Energy Tank Room
Room_D7E4_state_D7F1_PLM:
    ; Energy tank
    dw $eed7 : db $3d : db $05 : dw $0098 
    dw $0000
org $8fc75d
; room D81A: [Colosseum Save Room]
Room_D81A_state_D827_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0003 
    dw $0000
org $8fc765
; room D845: [Halfie Climb Missile Station]
Room_D845_state_D852_PLM:
    ; Missile station
    dw $b6eb : db $07 : db $0a : dw $0099 
    dw $0000
org $8fc76d
; room D86E: [Bug Sand Fall]
Room_D86E_state_D87B_PLM:
    dw $0000
org $8fc76f
; room D898: [Botwoon Sand Fall]
Room_D898_state_D8A5_PLM:
    dw $0000
org $8fc771
; room D8C5: Shaktool Room
Room_D8C5_state_D8F1_PLM:
    dw $0000
org $8fc773
; room D913: Halfie Climb Room
Room_D913_state_D920_PLM:
    ; Scroll PLM
    dw $b703 : db $3f : db $26 : dw Room_D913_state_D920_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $43 : db $29 : dw Room_D913_state_D920_PLM_index_1_PLM_scroll_data 
    ; Upwards extension
    dw $b647 : db $43 : db $28 : dw $8000 
    ; Upwards extension
    dw $b647 : db $43 : db $27 : dw $8000 
    ; Upwards extension
    dw $b647 : db $43 : db $26 : dw $8000 
    ; Scroll PLM
    dw $b703 : db $41 : db $29 : dw Room_D913_state_D920_PLM_index_5_PLM_scroll_data 
Door_9C_Room_D913_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $4e : db $16 : dw $009c 
    dw $0000
org $8fc79f
; room D95E: Botwoon's Room
Room_D95E_state_D98A_PLM:
Door_9D_Room_D95E_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $049d 
    dw $0000
org $8fc7a7
; room D9AA: Space Jump Room
Room_D9AA_state_D9B7_PLM:
    ; Space jump, chozo orb
    dw $ef6f : db $0b : db $08 : dw $009a 
    dw $0000
org $8fc7af
; room D9D4: [Colosseum Energy Charge Room]
Room_D9D4_state_D9E1_PLM:
    ; Energy station
    dw $b6df : db $07 : db $0a : dw $009b 
    dw $0000
org $8fc7b7
; room D9FE: Cactus Alley [West]
Room_D9FE_state_DA0B_PLM:
    dw $0000
org $8fc7b9
; room DA2B: Cactus Alley [East]
Room_DA2B_state_DA38_PLM:
    dw $0000
org $8fc7bb
; room DA60: Draygon's Room
Room_DA60_state_DA8C_PLM:
Door_9E_Room_DA60_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $009e 
Door_9F_Room_DA60_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $1e : db $16 : dw $009f 
    ; Dragon cannon, facing left
    dw $df7d : db $1d : db $0b : dw $8802 
    ; Draygon cannon, with shield, facing left
    dw $df71 : db $1d : db $12 : dw $8804 
    ; Draygon cannon, with shield, facing right
    dw $df59 : db $02 : db $0f : dw $8806 
    ; Draygon cannon, with shield, facing right
    dw $df59 : db $02 : db $15 : dw $8808 
    dw $0000
org $8fc7e1
; room DAAE: Tourian First Room
Room_DAAE_state_DABB_PLM:
    ; Elevator platform
    dw $b70b : db $06 : db $2c : dw $8000 
    dw $0000
org $8fc7e9
; room DAE1: Metroid Room 1
Room_DAE1_state_DB0D_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0012 
Door_A0_Room_DAE1_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $5e : db $06 : dw $0ca0 
    dw $0000
org $8fc7f7
; room DB31: Metroid Room 2
Room_DB31_state_DB5D_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0014 
Door_A1_Room_DB31_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $16 : dw $0ca1 
    dw $0000
org $8fc805
; room DB7D: Metroid Room 3
Room_DB7D_state_DBA9_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0016 
Door_A2_Room_DB7D_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $0ca2 
    dw $0000
org $8fc813
; room DBCD: Metroid Room 4
Room_DBCD_state_DBF9_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0018 
Door_A3_Room_DBCD_PLM_C84E:
    ; Door. Grey door facing up
    dw $c84e : db $06 : db $1e : dw $0ca3 
    dw $0000
org $8fc821
; room DC19: Blue Hopper Room
Room_DC19_state_DC45_PLM:
    dw $0000
org $8fc823
; room DC65: Dust Torizo Room
Room_DC65_state_DC91_PLM:
Door_A4_Room_DC65_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $01 : db $06 : dw $90a4 
Door_A5_Room_DC65_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $1e : db $06 : dw $0ca5 
    dw $0000
org $8fc831
; room DCB1: Big Boy Room
Room_DCB1_state_DCDD_PLM:
Door_A6_Room_DCB1_PLM_C848:
    ; Door. Grey door facing right
    dw $c848 : db $21 : db $06 : dw $90a6 
    dw $0000
org $8fc839
; room DCFF: Seaweed Room
Room_DCFF_state_DD0C_PLM:
Door_A7_Room_DCFF_PLM_C890:
    ; Door. Red door facing right
    dw $c890 : db $01 : db $16 : dw $00a7 
    dw $0000
org $8fc841
; room DD2E: Tourian Recharge Room
Room_DD2E_state_DD3B_PLM:
    ; Missile station
    dw $b6eb : db $07 : db $0a : dw $009c 
    ; Energy station
    dw $b6df : db $09 : db $0a : dw $009d 
    dw $0000
org $8fc84f
; room DD58: Mother Brain Room
Room_DD58_state_DDA2_PLM:
    ; Mother Brain's glass
    dw $d6de : db $06 : db $05 : dw $8000 
    dw $0000
org $8fc857
; room DDC4: Tourian Eye Door Room
Room_DDC4_state_DDD1_PLM:
Door_A8_Room_DDC4_PLM_DB4C:
    ; Door. Eye door, facing right
    dw $db4c : db $01 : db $06 : dw $00a8 
    ; Eye door bottom, facing right
    dw $db52 : db $01 : db $09 : dw $00a8 
    ; Eye door eye, facing right
    dw $db48 : db $01 : db $07 : dw $00a8 
    dw $0000
org $8fc86b
; room DDF3: Rinka Shaft
Room_DDF3_state_DE00_PLM:
Door_A9_Room_DDF3_PLM_C88A:
    ; Door. Red door facing left
    dw $c88a : db $0e : db $26 : dw $00a9 
    dw $0000
org $8fc873
; room DE23: [Mother Brain Save Room]
Room_DE23_state_DE30_PLM:
    ; Save station
    dw $b76f : db $09 : db $0b : dw $0000 
    dw $0000
org $8fc87b
; room DE4D: Tourian Escape Room 1
Room_DE4D_state_DE5A_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0000 
    ; Door. Gate that closes during escape in room after Mother Brain
    dw $c8ca : db $00 : db $06 : dw $8000 
    dw $0000
org $8fc889
; room DE7A: Tourian Escape Room 2
Room_DE7A_state_DE87_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0002 
Door_AA_Room_DE7A_PLM_C854:
    ; Door. Grey door facing down
    dw $c854 : db $06 : db $03 : dw $90aa 
    dw $0000
org $8fc897
; room DEA7: Tourian Escape Room 3
Room_DEA7_state_DEB4_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0004 
Door_AB_Room_DEA7_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $5e : db $16 : dw $90ab 
    dw $0000
org $8fc8a5
; room DEDE: Tourian Escape Room 4
Room_DEDE_state_DEEB_PLM:
    ; Sets Metroids cleared states when required
    dw $db44 : db $08 : db $08 : dw $0006 
Door_AC_Room_DEDE_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $2e : db $36 : dw $90ac 
    dw $0000
org $8fc8b3
; room DF1B: [Tourian First Save Room]
Room_DF1B_state_DF28_PLM:
    ; Save station
    dw $b76f : db $07 : db $0b : dw $0001 
    dw $0000
org $8fc8bb
; room DF45: [Ceres Elevator Room]
Room_DF45_state_DF71_PLM:
    dw $0000
org $8fc8bd
; room DF8D: [Ceres Jump Tutorial Room]
Room_DF8D_state_DFB9_PLM:
    dw $0000
org $8fc8bf
; room DFD7: [Ceres Staircase Room]
Room_DFD7_state_E003_PLM:
    dw $0000
org $8fc8c1
; room E021: [Ceres Dead Scientists Room]
Room_E021_state_E04D_PLM:
    dw $0000
org $8fc8c3
; room E06B: [Ceres Last Corridor]
Room_E06B_state_E097_PLM:
    dw $0000
org $8fc8c5
; room E0B5: [Ceres Ridley Room]
Room_E0B5_state_E0E1_PLM:
    dw $0000
org $8fc98e
RoomHeadersScrollDataDoorout:
    db $00,$03,$27,$0b,$06,$03,$70,$a0,$00,$d4,$c9,$29,$e6,$01,$ba,$c9,$e6,$e5
org $8fc9a0
; room C98E: Bowling Alley
Room_C98E_state_C9A0_Header:
    dl $c48322 ; Level data pointer
    db $05 ; Tileset
    db $30 ; Song Set
    db $03 ; Play Index
    dw $9ba4 ; FX pointer
    dw $be93 ; Enemy Set pointer
    dw $8b87 ; Enemy GFX pointer
    dw $0000 ; Background X/Y scrolling
    dw $c9da ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_C98E_PLM ; PLM Set pointer
    dw $0000 ; Background pointer
    dw $c8c7 ; Setup ASM pointer
org $8fc9ba
; room C98E: Bowling Alley
Room_C98E_state_C9BA_Header:
    dl $c48322 ; Level data pointer
    db $04 ; Tileset
    db $30 ; Song Set
    db $03 ; Play Index
    dw $9ac2 ; FX pointer
    dw $c1ae ; Enemy Set pointer
    dw $8c01 ; Enemy GFX pointer
    dw $0000 ; Background X/Y scrolling
    dw $c9da ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_C98E_PLM ; PLM Set pointer
    dw $0000 ; Background pointer
    dw $c8c7 ; Setup ASM pointer
org $8fc9da
; room C98E: Bowling Alley
Room_C98E_state_C9BA_Scroll:
    db $02,$01,$01,$01,$00,$00,$02,$01,$01,$01,$01,$01,$02,$00,$00,$00,$01,$00
org $8fc9ec
; room C98E: Bowling Alley
Room_C98E_state_C9BA_PLM_index_0_PLM_scroll_data:
    db $0e,$01,$0f,$01,$80
org $8fc9f1
; room C98E: Bowling Alley
Room_C98E_state_C9BA_PLM_index_3_PLM_scroll_data:
    db $00,$02,$01,$00,$06,$02,$0c,$01,$0d,$01,$80,$05,$01,$80,$04,$01,$80,$05,$00,$80,$04,$00,$80
org $8fca08
; room CA08: Wrecked Ship Entrance
RoomPtr_CA08:
    db $01 ; room index
    db $03 ; area
    db $27 ; map X
    db $0e ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ca4e ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $ca34 ; room state pointer
    dw $e5e6 ; room state standard
org $8fca52
; room CA52: Attic
Room_CA52_Header:
    db $02 ; room index
    db $03 ; area
    db $24 ; map X
    db $0a ; map Y
    db $07 ; width
    db $01 ; height
    db $00 ; up scroller
    db $00 ; down scroller
    db $00 ; special graphics bitflag
    dw $ca98 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $ca7e ; room state pointer
    dw $e5e6 ; room state standard
org $8fca64
; room CA52: Attic
Room_CA52_state_CA64_Header:
    dl $c49eae ; Level data pointer
    db $05 ; Tileset
    db $30 ; Song Set
    db $05 ; Play Index
    dw $9bc4 ; FX pointer
    dw $c6f2 ; Enemy Set pointer
    dw $8ca9 ; Enemy GFX pointer
    dw $f1c1 ; Background X/Y scrolling
    dw $ca9e ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_CA52_state_CA64_PLM ; PLM Set pointer
    dw $e168 ; Background pointer
    dw $c8c7 ; Setup ASM pointer
org $8fca7e
; room CA52: Attic
Room_CA52_state_CA7E_Header:
    dl $c4a2e7 ; Level data pointer
    db $04 ; Tileset
    db $30 ; Song Set
    db $06 ; Play Index
    dw $9ae2 ; FX pointer
    dw $bfe6 ; Enemy Set pointer
    dw $8b99 ; Enemy GFX pointer
    dw $f1c1 ; Background X/Y scrolling
    dw $ca9e ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_CA52_state_CA7E_PLM ; PLM Set pointer
    dw $e168 ; Background pointer
    dw $c8c7 ; Setup ASM pointer
org $8fcaae
; room CAAE: Wrecked Ship East Missile Room
Room_CAAE_Header:
    db $03 ; room index
    db $03 ; area
    db $21 ; map X
    db $0a ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $caf4 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cada ; room state pointer
    dw $e5e6 ; room state standard
org $8fcaf6
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_Header:
    db $04 ; room index
    db $03 ; area
    db $25 ; map X
    db $0b ; map Y
    db $06 ; width
    db $08 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cb3c ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cb22 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcb4a
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_state_CB22_Scroll:
    db $00,$02,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$02,$00,$00,$00,$00,$00,$02,$00,$01,$01,$01,$00,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
org $8fcb7a
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_state_CB22_PLM_index_0_PLM_scroll_data:
    db $20,$01,$80
org $8fcb7d
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_state_CB22_PLM_index_1_PLM_scroll_data:
    db $24,$01,$80
org $8fcb80
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_state_CB22_PLM_index_2_PLM_scroll_data:
    db $20,$00,$80
org $8fcb83
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_state_CB22_PLM_index_3_PLM_scroll_data:
    db $24,$00,$80
org $8fcb86
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_state_CB22_PLM_index_4_PLM_scroll_data:
    db $25,$02,$2b,$02,$80
org $8fcb8b
; room CB8B: Spiky Death Room
Room_CB8B_Header:
    db $05 ; room index
    db $03 ; area
    db $22 ; map X
    db $0f ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cbd1 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cbb7 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcbd5
; room CBD5: Electric Death Room
Room_CBD5_Header:
    db $06 ; room index
    db $03 ; area
    db $21 ; map X
    db $0d ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cc1b ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cc01 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcc27
; room CC27: Wrecked Ship Energy Tank Room
Room_CC27_Header:
    db $07 ; room index
    db $03 ; area
    db $22 ; map X
    db $0d ; map Y
    db $03 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cc6d ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cc53 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcc6f
; room CC6F: Basement
RoomPtr_CC6F:
    db $08 ; room index
    db $03 ; area
    db $24 ; map X
    db $13 ; map Y
    db $05 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ccb5 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cc9b ; room state pointer
    dw $e5e6 ; room state standard
org $8fccbb
; room CC6F: Basement
Room_CC6F_state_CC9B_Scroll:
    db $00,$01,$01,$01,$01
org $8fccc0
; room CC6F: Basement
Room_CC6F_state_CC9B_PLM_index_0_PLM_scroll_data:
    db $00,$01,$01,$01,$80
org $8fccc5
; room CC6F: Basement
Room_CC6F_state_CC9B_PLM_index_1_PLM_scroll_data:
    db $01,$00,$80
org $8fcccb
; room CCCB: Wrecked Ship Map Room
Room_CCCB_Header:
    db $09 ; room index
    db $03 ; area
    db $29 ; map X
    db $13 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cd11 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $ccf7 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcd13
; room CD13: Phantoon's Room
Room_CD13_Header:
    db $0a ; room index
    db $03 ; area
    db $23 ; map X
    db $13 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cd59 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cd3f ; room state pointer
    dw $e5e6 ; room state standard
org $8fcd5c
; room CD5C: Sponge Bath
Room_CD5C_Header:
    db $0b ; room index
    db $03 ; area
    db $24 ; map X
    db $0f ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cda2 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cd88 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcda8
; room CDA8: Wrecked Ship West Super Room
Room_CDA8_Header:
    db $0c ; room index
    db $03 ; area
    db $27 ; map X
    db $11 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cdee ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $cdd4 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcdf1
; room CDF1: Wrecked Ship East Super Room
Room_CDF1_Header:
    db $0d ; room index
    db $03 ; area
    db $21 ; map X
    db $11 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ce37 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $ce1d ; room state pointer
    dw $e5e6 ; room state standard
org $8fce39
; room CDF1: Wrecked Ship East Super Room
Room_CDF1_state_CE1D_Scroll:
    db $00,$01,$01,$01
org $8fce3d
; room CDF1: Wrecked Ship East Super Room
Room_CDF1_state_CE1D_PLM_index_0_PLM_scroll_data:
    db $00,$01,$80
org $8fce40
; room CE40: Gravity Suit Room
Room_CE40_Header:
    db $0e ; room index
    db $03 ; area
    db $2c ; map X
    db $0d ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ce86 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $ce6c ; room state pointer
    dw $e5e6 ; room state standard
org $8fce8a
; room CE8A: [Wrecked Ship Save Room]
RoomPtr_CE8A:
    db $0f ; room index
    db $03 ; area
    db $25 ; map X
    db $0e ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ced0 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $ceb6 ; room state pointer
    dw $e5e6 ; room state standard
org $8fced2
; room CED2: [Glass Tunnel Save Room]
RoomPtr_CED2:
    db $00 ; room index
    db $04 ; area
    db $36 ; map X
    db $13 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cef9 ; doors pointer
    dw $e5e6 ; room state standard
org $8fcefb
; room CEFB: Glass Tunnel
Room_CEFB_Header:
    db $01 ; room index
    db $04 ; area
    db $37 ; map X
    db $11 ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cf41 ; doors pointer
    dw $e612 ; room state Events
    db $0b ; event
    dw $cf27 ; room state pointer
    dw $e5e6 ; room state standard
org $8fcf54
; room CF54: West Tunnel
Room_CF54_Header:
    db $02 ; room index
    db $04 ; area
    db $38 ; map X
    db $12 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cf7b ; doors pointer
    dw $e5e6 ; room state standard
org $8fcf80
; room CF80: East Tunnel
Room_CF80_Header:
    db $03 ; room index
    db $04 ; area
    db $33 ; map X
    db $11 ; map Y
    db $04 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cfa7 ; doors pointer
    dw $e5e6 ; room state standard
org $8fcfad
; room CF80: East Tunnel
Room_CF80_state_CF8D_Scroll:
    db $01,$01,$01,$01,$00,$00,$00,$01
org $8fcfb5
; room CF80: East Tunnel
Room_CF80_state_CF8D_PLM_index_0_PLM_scroll_data:
    db $02,$00,$03,$01,$07,$00,$80
org $8fcfbc
; room CF80: East Tunnel
Room_CF80_state_CF8D_PLM_index_1_PLM_scroll_data:
    db $03,$02,$07,$01,$80
org $8fcfc1
; room CF80: East Tunnel
Room_CF80_state_CF8D_PLM_index_2_PLM_scroll_data:
    db $03,$00,$07,$01,$80
org $8fcfc6
; room CF80: East Tunnel
Room_CF80_state_CF8D_PLM_index_9_PLM_scroll_data:
    db $02,$01,$80
org $8fcfc9
; room CFC9: Main Street
Room_CFC9_Header:
    db $04 ; room index
    db $04 ; area
    db $36 ; map X
    db $09 ; map Y
    db $03 ; width
    db $08 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $cff0 ; doors pointer
    dw $e5e6 ; room state standard
org $8fcffa
; room CFC9: Main Street
Room_CFC9_state_CFD6_Scroll:
    db $00,$02,$02,$00,$02,$02,$01,$02,$02,$00,$02,$02,$00,$02,$02,$00,$02,$02,$02,$02,$02,$00,$02,$02
org $8fd017
; room D017: Fish Tank
Room_D017_Header:
    db $05 ; room index
    db $04 ; area
    db $32 ; map X
    db $0d ; map Y
    db $04 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d03e ; doors pointer
    dw $e5e6 ; room state standard
org $8fd046
; room D017: Fish Tank
Room_D017_state_D024_Scroll:
    db $02,$02,$02,$02,$02,$02,$02,$02,$02,$00,$02,$02
org $8fd052
; room D017: Fish Tank
Room_D017_state_D024_PLM_index_7_PLM_scroll_data:
    db $09,$02,$80
org $8fd055
; room D055: Mama Turtle Room
Room_D055_Header:
    db $06 ; room index
    db $04 ; area
    db $2f ; map X
    db $0c ; map Y
    db $03 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d07c ; doors pointer
    dw $e5e6 ; room state standard
org $8fd07e
; room D055: Mama Turtle Room
Room_D055_state_D062_Scroll:
    db $02,$02,$00,$02,$02,$00,$02,$02,$00,$02,$02,$02
org $8fd08a
; room D08A: Crab Tunnel
Room_D08A_Header:
    db $07 ; room index
    db $04 ; area
    db $33 ; map X
    db $10 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d0b1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd0b9
; room D0B9: Mt. Everest
Room_D0B9_Header:
    db $08 ; room index
    db $04 ; area
    db $31 ; map X
    db $09 ; map Y
    db $06 ; width
    db $04 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d0e0 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd104
; room D104: Red Fish Room
Room_D104_Header:
    db $09 ; room index
    db $04 ; area
    db $34 ; map X
    db $07 ; map Y
    db $03 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d12b ; doors pointer
    dw $e5e6 ; room state standard
org $8fd12f
; room D104: Red Fish Room
Room_D104_state_D111_Scroll:
    db $02,$00,$01,$02,$00,$00
org $8fd135
; room D104: Red Fish Room
Room_D104_state_D111_PLM_index_0_PLM_scroll_data:
    db $00,$02,$80
org $8fd138
; room D104: Red Fish Room
Room_D104_state_D111_PLM_index_1_PLM_scroll_data:
    db $01,$01,$80
org $8fd13b
; room D13B: Watering Hole
Room_D13B_Header:
    db $0a ; room index
    db $04 ; area
    db $35 ; map X
    db $04 ; map Y
    db $02 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d162 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd164
; room D13B: Watering Hole
Room_D13B_state_D148_Scroll:
    db $01,$02,$00,$02,$00,$00
org $8fd16a
; room D13B: Watering Hole
Room_D13B_state_D148_PLM_index_0_PLM_scroll_data:
    db $05,$01,$80
org $8fd16d
; room D16D: Northwest Maridia Bug Room
Room_D16D_Header:
    db $0b ; room index
    db $04 ; area
    db $31 ; map X
    db $04 ; map Y
    db $04 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d194 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd198
; room D16D: Northwest Maridia Bug Room
Room_D16D_state_D17A_Scroll:
    db $00,$00,$00,$02,$01,$01,$00,$01
org $8fd1a0
; room D16D: Northwest Maridia Bug Room
Room_D16D_state_D17A_PLM_index_7_PLM_scroll_data:
    db $06,$01,$80
org $8fd1a3
; room D1A3: Crab Shaft
Room_D1A3_Header:
    db $0c ; room index
    db $04 ; area
    db $2f ; map X
    db $07 ; map Y
    db $02 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d1ca ; doors pointer
    dw $e5e6 ; room state standard
org $8fd1d0
; room D1A3: Crab Shaft
Room_D1A3_state_D1B0_Scroll:
    db $00,$02,$00,$02,$00,$01,$01,$00
org $8fd1d8
; room D1A3: Crab Shaft
Room_D1A3_state_D1B0_PLM_index_0_PLM_scroll_data:
    db $05,$02,$07,$01,$80
org $8fd1dd
; room D1DD: Pseudo Plasma Spark Room
RoomPtr_D1DD:
    db $0d ; room index
    db $04 ; area
    db $2d ; map X
    db $04 ; map Y
    db $04 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d204 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd20a
; room D1DD: Pseudo Plasma Spark Room
Room_D1DD_state_D1EA_Scroll:
    db $02,$02,$02,$02,$02,$02,$02,$02,$00,$00,$02,$02
org $8fd216
; room D1DD: Pseudo Plasma Spark Room
Room_D1DD_state_D1EA_PLM_index_3_PLM_scroll_data:
    db $09,$02,$80
org $8fd219
; room D1DD: Pseudo Plasma Spark Room
Room_D1DD_state_D1EA_PLM_index_7_PLM_scroll_data:
    db $09,$00,$80
org $8fd21c
; room D21C: Crab Hole
Room_D21C_Header:
    db $0e ; room index
    db $04 ; area
    db $32 ; map X
    db $10 ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d243 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd252
; room D252: [Tunnel to West Sand Hall]
Room_D252_Header:
    db $0f ; room index
    db $04 ; area
    db $31 ; map X
    db $10 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d279 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd27e
; room D27E: Plasma Tutorial Room
Room_D27E_Header:
    db $10 ; room index
    db $04 ; area
    db $28 ; map X
    db $00 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d2a5 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd2aa
; room D2AA: Plasma Room
Room_D2AA_Header:
    db $11 ; room index
    db $04 ; area
    db $26 ; map X
    db $00 ; map Y
    db $02 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d2d1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd2d9
; room D2D9: Thread The Needle Room
Room_D2D9_Header:
    db $12 ; room index
    db $04 ; area
    db $21 ; map X
    db $05 ; map Y
    db $07 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d300 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd30b
; room D30B: Maridia Elevator Room
RoomPtr_D30B:
    db $13 ; room index
    db $04 ; area
    db $20 ; map X
    db $00 ; map Y
    db $01 ; width
    db $06 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d332 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd340
; room D340: Plasma Spark Room
Room_D340_Header:
    db $14 ; room index
    db $04 ; area
    db $29 ; map X
    db $02 ; map Y
    db $04 ; width
    db $06 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d367 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd36f
; room D340: Plasma Spark Room
Room_D340_state_D34D_Scroll:
    db $00,$02,$02,$00,$00,$02,$02,$00,$02,$02,$02,$02,$02,$02,$02,$00,$02,$02,$02,$00,$01,$01,$01,$00
org $8fd387
; room D387: Plasma Climb
Room_D387_Header:
    db $15 ; room index
    db $04 ; area
    db $29 ; map X
    db $00 ; map Y
    db $01 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d3ae ; doors pointer
    dw $e5e6 ; room state standard
org $8fd3b6
; room D3B6: Maridia Map Room
Room_D3B6_Header:
    db $16 ; room index
    db $04 ; area
    db $31 ; map X
    db $11 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d3dd ; doors pointer
    dw $e5e6 ; room state standard
org $8fd3df
; room D3DF: [Maridia Elevator Save Room]
RoomPtr_D3DF:
    db $17 ; room index
    db $04 ; area
    db $1f ; map X
    db $04 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d406 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd408
; room D408: [Vertical Tube]
Room_D408_Header:
    db $18 ; room index
    db $04 ; area
    db $2c ; map X
    db $05 ; map Y
    db $01 ; width
    db $0a ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d42f ; doors pointer
    dw $e5e6 ; room state standard
org $8fd433
; room D433: Bug Sand Hole
Room_D433_Header:
    db $19 ; room index
    db $04 ; area
    db $28 ; map X
    db $05 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d45a ; doors pointer
    dw $e5e6 ; room state standard
org $8fd461
; room D461: West Sand Hall
Room_D461_Header:
    db $1a ; room index
    db $04 ; area
    db $2d ; map X
    db $10 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d488 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd48e
; room D48E: Oasis
RoomPtr_D48E:
    db $1b ; room index
    db $04 ; area
    db $2c ; map X
    db $0f ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d4b5 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd4c2
; room D4C2: East Sand Hall
Room_D4C2_Header:
    db $1c ; room index
    db $04 ; area
    db $29 ; map X
    db $10 ; map Y
    db $03 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d4e9 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd4ef
; room D4EF: West Sand Hole
Room_D4EF_Header:
    db $1d ; room index
    db $04 ; area
    db $2d ; map X
    db $0e ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d516 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd51e
; room D51E: East Sand Hole
Room_D51E_Header:
    db $1e ; room index
    db $04 ; area
    db $2a ; map X
    db $0e ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d545 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd54d
; room D54D: [West Sand Fall]
Room_D54D_Header:
    db $1f ; room index
    db $04 ; area
    db $2d ; map X
    db $0c ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d574 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd57a
; room D57A: [East Sand Fall]
Room_D57A_Header:
    db $20 ; room index
    db $04 ; area
    db $2b ; map X
    db $0c ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d5a1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd5a7
; room D5A7: Aqueduct
Room_D5A7_Header:
    db $21 ; room index
    db $04 ; area
    db $29 ; map X
    db $09 ; map Y
    db $06 ; width
    db $03 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d5ce ; doors pointer
    dw $e5e6 ; room state standard
org $8fd5ec
; room D5EC: Butterfly Room
Room_D5EC_Header:
    db $22 ; room index
    db $04 ; area
    db $28 ; map X
    db $07 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d613 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd617
; room D617: Botwoon Hallway
RoomPtr_D617:
    db $23 ; room index
    db $04 ; area
    db $2b ; map X
    db $08 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d63e ; doors pointer
    dw $e5e6 ; room state standard
org $8fd646
; room D646: Pants Room
Room_D646_Header:
    db $24 ; room index
    db $04 ; area
    db $27 ; map X
    db $0d ; map Y
    db $02 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d66d ; doors pointer
    dw $e5e6 ; room state standard
org $8fd675
; room D646: Pants Room
Room_D646_state_D653_Scroll:
    db $02,$02,$02,$02,$01,$00,$00,$01
org $8fd67d
; room D646: Pants Room
Room_D646_state_D653_PLM_index_4_PLM_scroll_data:
    db $02,$00,$03,$02,$04,$00,$05,$02,$06,$00,$07,$01,$80
org $8fd68a
; room D646: Pants Room
Room_D646_state_D653_PLM_index_D_PLM_scroll_data:
    db $02,$02,$03,$00,$04,$02,$05,$00,$06,$01,$07
org $8fd695
; room D646: Pants Room
Room_D646_state_D653_PLM_index_15_PLM_scroll_data:
    db $00,$80,$06,$01,$80
org $8fd69a
; room D69A: [Pants Room West half]
Room_D69A_Header:
    db $25 ; room index
    db $04 ; area
    db $27 ; map X
    db $0e ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d6c1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd6d0
; room D6D0: Spring Ball Room
Room_D6D0_Header:
    db $26 ; room index
    db $04 ; area
    db $21 ; map X
    db $0f ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d6f7 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd6f9
; room D6D0: Spring Ball Room
Room_D6D0_state_D6DD_Scroll:
    db $00,$02,$01,$01
org $8fd6fd
; room D6FD: Below Botwoon Energy Tank
Room_D6FD_Header:
    db $27 ; room index
    db $04 ; area
    db $25 ; map X
    db $0a ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d724 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd72a
; room D72A: Colosseum
Room_D72A_Header:
    db $28 ; room index
    db $04 ; area
    db $1a ; map X
    db $06 ; map Y
    db $07 ; width
    db $02 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d751 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd765
; room D765: [Aqueduct Save Room]
RoomPtr_D765:
    db $29 ; room index
    db $04 ; area
    db $2f ; map X
    db $0b ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d78c ; doors pointer
    dw $e5e6 ; room state standard
org $8fd78f
; room D78F: The Precious Room
RoomPtr_D78F:
    db $2a ; room index
    db $04 ; area
    db $18 ; map X
    db $07 ; map Y
    db $02 ; width
    db $03 ; height
    db $90 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d7d5 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $d7bb ; room state pointer
    dw $e5e6 ; room state standard
org $8fd7d9
; room D78F: The Precious Room
Room_D78F_state_D7BB_Scroll:
    db $01,$01,$00,$00,$00,$01
org $8fd7df
; room D78F: The Precious Room
Room_D78F_state_D7BB_PLM_index_0_PLM_scroll_data:
    db $01,$02,$03,$02,$80
org $8fd7e4
; room D7E4: Botwoon Energy Tank Room
Room_D7E4_Header:
    db $2b ; room index
    db $04 ; area
    db $22 ; map X
    db $08 ; map Y
    db $07 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d80b ; doors pointer
    dw $e5e6 ; room state standard
org $8fd81a
; room D81A: [Colosseum Save Room]
RoomPtr_D81A:
    db $2c ; room index
    db $04 ; area
    db $19 ; map X
    db $06 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d841 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd845
; room D845: [Halfie Climb Missile Station]
Room_D845_Header:
    db $2d ; room index
    db $04 ; area
    db $1c ; map X
    db $08 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d86c ; doors pointer
    dw $e5e6 ; room state standard
org $8fd86e
; room D86E: [Bug Sand Fall]
Room_D86E_Header:
    db $2e ; room index
    db $04 ; area
    db $28 ; map X
    db $06 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d895 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd898
; room D898: [Botwoon Sand Fall]
Room_D898_Header:
    db $2f ; room index
    db $04 ; area
    db $25 ; map X
    db $09 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d8bf ; doors pointer
    dw $e5e6 ; room state standard
org $8fd8c5
; room D8C5: Shaktool Room
Room_D8C5_Header:
    db $30 ; room index
    db $04 ; area
    db $23 ; map X
    db $0f ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d90b ; doors pointer
    dw $e612 ; room state Events
    db $0d ; event
    dw $d8f1 ; room state pointer
    dw $e5e6 ; room state standard
org $8fd8d7
; room D8C5: Shaktool Room
Room_D8C5_state_D8D7_Header:
    dl $ccfd75 ; Level data pointer
    db $0c ; Tileset
    db $00 ; Song Set
    db $00 ; Play Index
    dw $9f84 ; FX pointer
    dw $d281 ; Enemy Set pointer
    dw $8dff ; Enemy GFX pointer
    dw $00c0 ; Background X/Y scrolling
    dw $d90f ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_D8C5_PLM ; PLM Set pointer (in freespace)
    dw $0000 ; Background pointer
    dw $c8d3 ; Setup ASM pointer
org $8fd8f1
; room D8C5: Shaktool Room
Room_D8C5_state_D8F1_Header:
    dl $cd8404 ; Level data pointer
    db $0c ; Tileset
    db $00 ; Song Set
    db $00 ; Play Index
    dw $9f84 ; FX pointer
    dw $d281 ; Enemy Set pointer
    dw $8dff ; Enemy GFX pointer
    dw $00c0 ; Background X/Y scrolling
    dw $d90f ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_D8C5_PLM ; PLM Set pointer (in freespace)
    dw $0000 ; Background pointer
    dw $c8dc ; Setup ASM pointer
org $8fd913
; room D913: Halfie Climb Room
Room_D913_Header:
    db $31 ; room index
    db $04 ; area
    db $1d ; map X
    db $06 ; map Y
    db $05 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d93a ; doors pointer
    dw $e5e6 ; room state standard
org $8fd942
; room D913: Halfie Climb Room
Room_D913_state_D920_Scroll:
    db $00,$00,$00,$00,$02,$00,$00,$00,$00,$02,$01,$01,$01,$00,$01
org $8fd951
; room D913: Halfie Climb Room
Room_D913_state_D920_PLM_index_0_PLM_scroll_data:
    db $09,$00,$0d,$01,$80
org $8fd956
; room D913: Halfie Climb Room
Room_D913_state_D920_PLM_index_1_PLM_scroll_data:
    db $09,$01,$0d,$00,$80
org $8fd95b
; room D913: Halfie Climb Room
Room_D913_state_D920_PLM_index_5_PLM_scroll_data:
    db $0e,$01,$80
org $8fd95e
; room D95E: Botwoon's Room
Room_D95E_Header:
    db $32 ; room index
    db $04 ; area
    db $29 ; map X
    db $08 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d9a4 ; doors pointer
    dw $e629 ; room state Bosses
    db $02 ; event
    dw $d98a ; room state pointer
    dw $e5e6 ; room state standard
org $8fd9aa
; room D9AA: Space Jump Room
Room_D9AA_Header:
    db $33 ; room index
    db $04 ; area
    db $1c ; map X
    db $0a ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d9d1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fd9d4
; room D9D4: [Colosseum Energy Charge Room]
Room_D9D4_Header:
    db $34 ; room index
    db $04 ; area
    db $18 ; map X
    db $06 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $d9fb ; doors pointer
    dw $e5e6 ; room state standard
org $8fd9fe
; room D9FE: Cactus Alley [West]
Room_D9FE_Header:
    db $35 ; room index
    db $04 ; area
    db $27 ; map X
    db $06 ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $da25 ; doors pointer
    dw $e5e6 ; room state standard
org $8fda2b
; room DA2B: Cactus Alley [East]
Room_DA2B_Header:
    db $36 ; room index
    db $04 ; area
    db $22 ; map X
    db $06 ; map Y
    db $05 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $da52 ; doors pointer
    dw $e5e6 ; room state standard
org $8fda60
; room DA60: Draygon's Room
Room_DA60_Header:
    db $37 ; room index
    db $04 ; area
    db $1a ; map X
    db $09 ; map Y
    db $02 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $01 ; special graphics bitflag
    dw $daa6 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $da8c ; room state pointer
    dw $e5e6 ; room state standard
org $8fdaae
; room DAAE: Tourian First Room
RoomPtr_DAAE:
    db $00 ; room index
    db $05 ; area
    db $2b ; map X
    db $09 ; map Y
    db $01 ; width
    db $04 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dad5 ; doors pointer
    dw $e5e6 ; room state standard
org $8fdae1
; room DAE1: Metroid Room 1
Room_DAE1_Header:
    db $01 ; room index
    db $05 ; area
    db $2c ; map X
    db $0c ; map Y
    db $06 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $db27 ; doors pointer
    dw $e612 ; room state Events
    db $10 ; event
    dw $db0d ; room state pointer
    dw $e5e6 ; room state standard
org $8fdb31
; room DB31: Metroid Room 2
Room_DB31_Header:
    db $02 ; room index
    db $05 ; area
    db $32 ; map X
    db $0c ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $db77 ; doors pointer
    dw $e612 ; room state Events
    db $11 ; event
    dw $db5d ; room state pointer
    dw $e5e6 ; room state standard
org $8fdb7d
; room DB7D: Metroid Room 3
Room_DB7D_Header:
    db $03 ; room index
    db $05 ; area
    db $2c ; map X
    db $0d ; map Y
    db $06 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dbc3 ; doors pointer
    dw $e612 ; room state Events
    db $12 ; event
    dw $dba9 ; room state pointer
    dw $e5e6 ; room state standard
org $8fdbcd
; room DBCD: Metroid Room 4
Room_DBCD_Header:
    db $04 ; room index
    db $05 ; area
    db $2b ; map X
    db $0d ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dc13 ; doors pointer
    dw $e612 ; room state Events
    db $13 ; event
    dw $dbf9 ; room state pointer
    dw $e5e6 ; room state standard
org $8fdc19
; room DC19: Blue Hopper Room
Room_DC19_Header:
    db $05 ; room index
    db $05 ; area
    db $2b ; map X
    db $0f ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dc5f ; doors pointer
    dw $e612 ; room state Events
    db $14 ; event
    dw $dc45 ; room state pointer
    dw $e5e6 ; room state standard
org $8fdc65
; room DC65: Dust Torizo Room
Room_DC65_Header:
    db $06 ; room index
    db $05 ; area
    db $2d ; map X
    db $0f ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dcab ; doors pointer
    dw $e612 ; room state Events
    db $14 ; event
    dw $dc91 ; room state pointer
    dw $e5e6 ; room state standard
org $8fdcb1
; room DCB1: Big Boy Room
Room_DCB1_Header:
    db $07 ; room index
    db $05 ; area
    db $2d ; map X
    db $0f ; map Y
    db $06 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dcf7 ; doors pointer
    dw $e612 ; room state Events
    db $14 ; event
    dw $dcdd ; room state pointer
    dw $e5e6 ; room state standard
org $8fdcc3
; room DCB1: Big Boy Room
Room_DCB1_state_DCC3_Header:
    dl $cdd930 ; Level data pointer
    db $0d ; Tileset
    db $00 ; Song Set
    db $00 ; Play Index
    dw $a074 ; FX pointer
    dw $e26e ; Enemy Set pointer
    dw $90ec ; Enemy GFX pointer
    dw $c1c1 ; Background X/Y scrolling
    dw Room_DCB1_Room_Scrolls_Pointer ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_DCB1_state_DCDD_PLM ; PLM Set pointer
    dw $e41e ; Background pointer
    dw $c91e ; Setup ASM pointer
org $8fdcff
; room DCFF: Seaweed Room
Room_DCFF_Header:
    db $08 ; room index
    db $05 ; area
    db $33 ; map X
    db $0f ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dd26 ; doors pointer
    dw $e5e6 ; room state standard
org $8fdd2e
; room DD2E: Tourian Recharge Room
Room_DD2E_Header:
    db $09 ; room index
    db $05 ; area
    db $34 ; map X
    db $10 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dd55 ; doors pointer
    dw $e5e6 ; room state standard
org $8fdd58
; room DD58: Mother Brain Room
Room_DD58_Header:
    db $0a ; room index
    db $05 ; area
    db $2e ; map X
    db $12 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw Room_DD58_Doors_List ; doors pointer (in freespace)
    dw $e5ff ; room state TourianBoss
    dw $dda2 ; room state pointer
    dw $e612 ; room state Events
    db $02 ; event
    dw $dd88 ; room state pointer
    dw $e5e6 ; room state standard
org $8fdd6e
; room DD58: Mother Brain Room
Room_DD58_state_DD6E_Header:       ; regular state
    dl $cddede ; Level data pointer
    db $0e ; Tileset
    db $00 ; Song Set
    db $00 ; Play Index
    dw $a0a4 ; FX pointer
    dw $e321 ; Enemy Set pointer
    dw $9102 ; Enemy GFX pointer
    dw $c1c1 ; Background X/Y scrolling
    dw Room_DD58_state_DDA2_Scroll ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_DD58_state_DDA2_PLM ; PLM Set pointer
    dw $e48a ; Background pointer
    dw $c91e ; Setup ASM pointer
org $8fdd88
Room_DD58_state_DD88_Header:       ; when MB glass is broken (event 2)
    dl $cddede ; Level data pointer
    db $0e ; Tileset
    db $00 ; Song Set
    db $00 ; Play Index
    dw $a0a4 ; FX pointer
    dw $e321 ; Enemy Set pointer
    dw $9102 ; Enemy GFX pointer
    dw $c1c1 ; Background X/Y scrolling
    dw Room_DD58_state_DDA2_Scroll ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_DD58_state_DDA2_PLM ; PLM Set pointer
    dw $e48a ; Background pointer
    dw $c91e ; Setup ASM pointer
org $8fdda2
Room_DD58_state_DDA2_Header:       ; returning to the room after MB is dead
    dl $cddede ; Level data pointer
    db $0e ; Tileset
    db $00 ; Song Set
    db $03 ; Play Index
    dw $a188 ; FX pointer
    dw $8000 ; Enemy Set pointer
    dw $8000 ; Enemy GFX pointer
    dw $c1c1 ; Background X/Y scrolling
    dw Room_DD58_state_DDA2_Scroll ; Room Scrolls pointer
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer
    dw Room_DD58_state_DDA2_PLM ; PLM Set pointer
    dw $e48a ; Background pointer
    dw $c91e ; Setup ASM pointer
org $8fddc0
; room DD58: Mother Brain Room
Room_DD58_state_DDA2_Scroll:
    db $00,$01,$01,$01
org $8fddc4
; room DDC4: Tourian Eye Door Room
Room_DDC4_Header:
    db $0b ; room index
    db $05 ; area
    db $2f ; map X
    db $10 ; map Y
    db $04 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $ddeb ; doors pointer
    dw $e5e6 ; room state standard
org $8fddf3
; room DDF3: Rinka Shaft
RoomPtr_DDF3:
    db $0c ; room index
    db $05 ; area
    db $2e ; map X
    db $10 ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $de1a ; doors pointer
    dw $e5e6 ; room state standard
org $8fde23
; room DE23: [Mother Brain Save Room]
RoomPtr_DE23:
    db $0d ; room index
    db $05 ; area
    db $2f ; map X
    db $11 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $de4a ; doors pointer
    dw $e5e6 ; room state standard
org $8fde4d
; room DE4D: Tourian Escape Room 1
Room_DE4D_Header:
    db $0e ; room index
    db $05 ; area
    db $33 ; map X
    db $12 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $de74 ; doors pointer
    dw $e5e6 ; room state standard
org $8fde7a
; room DE7A: Tourian Escape Room 2
Room_DE7A_Header:
    db $0f ; room index
    db $05 ; area
    db $34 ; map X
    db $13 ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dea1 ; doors pointer
    dw $e5e6 ; room state standard
org $8fdea7
; room DEA7: Tourian Escape Room 3
Room_DEA7_Header:
    db $10 ; room index
    db $05 ; area
    db $2e ; map X
    db $13 ; map Y
    db $06 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dece ; doors pointer
    dw $e5e6 ; room state standard
org $8fdede
; room DEDE: Tourian Escape Room 4
Room_DEDE_Header:
    db $11 ; room index
    db $05 ; area
    db $2b ; map X
    db $10 ; map Y
    db $03 ; width
    db $06 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $df05 ; doors pointer
    dw $e5e6 ; room state standard
org $8fdf1b
; room DF1B: [Tourian First Save Room]
RoomPtr_DF1B:
    db $12 ; room index
    db $05 ; area
    db $2a ; map X
    db $0c ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $df42 ; doors pointer
    dw $e5e6 ; room state standard
org $8fdf45
; room DF45: [Ceres Elevator Room]
RoomPtr_DF45:
    db $00 ; room index
    db $06 ; area
    db $1c ; map X
    db $0d ; map Y
    db $01 ; width
    db $03 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $05 ; special graphics bitflag
    dw $df8b ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $df71 ; room state pointer
    dw $e5e6 ; room state standard
org $8fdf8d
; room DF8D: [Ceres Jump Tutorial Room]
Room_DF8D_Header:
    db $01 ; room index
    db $06 ; area
    db $1a ; map X
    db $0f ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $dfd3 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $dfb9 ; room state pointer
    dw $e5e6 ; room state standard
org $8fdfd7
; room DFD7: [Ceres Staircase Room]
Room_DFD7_Header:
    db $02 ; room index
    db $06 ; area
    db $19 ; map X
    db $0f ; map Y
    db $01 ; width
    db $02 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $e01d ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $e003 ; room state pointer
    dw $e5e6 ; room state standard
org $8fe021
; room E021: [Ceres Dead Scientists Room]
Room_E021_Header:
    db $03 ; room index
    db $06 ; area
    db $17 ; map X
    db $10 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $e067 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $e04d ; room state pointer
    dw $e5e6 ; room state standard
org $8fe06b
; room E06B: [Ceres Last Corridor]
Room_E06B_Header:
    db $04 ; room index
    db $06 ; area
    db $15 ; map X
    db $10 ; map Y
    db $02 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw $e0b1 ; doors pointer
    dw $e629 ; room state Bosses
    db $01 ; event
    dw $e097 ; room state pointer
    dw $e5e6 ; room state standard
org $8ffd40  ; freespace


;;; moved at begining of freespace to no longer change its address
;;; new MB room (referenced in bank 83 at Room_DD58_door_list_index_2_Door)
Room_FD40_Header:
    db $13 ; room index
    db $05 ; area
    db $32 ; map X
    db $12 ; map Y
    db $01 ; width
    db $01 ; height
    db $70 ; up scroller
    db $a0 ; down scroller
    db $00 ; special graphics bitflag
    dw Room_DD58_Doors_List ; doors pointer (in freespace)
    dw $e5ff ; room state TourianBoss
    dw Room_FD40_state_FD8A_Header ; room state pointer
    dw $e612 ; room state Events
    db $02 ; event
    dw Room_FD40_state_FD70_Header ; room state pointer (the one called in fast tourian)
    dw $e5e6 ; room state standard
Room_FD40_state_FD56_Header:    ; regular state
    dl $ce8000 ; Level data pointer
    db $0e ; Tileset
    db $00 ; Song Set
    db $05 ; Play Index
    dw $0000 ; FX pointer (in 83)
    dw $e321 ; Enemy Set pointer (in a1)
    dw $9102 ; Enemy GFX pointer (in b4)
    dw $c1c1 ; Background X/Y scrolling
    dw Room_FD40_Scroll ; Room Scrolls pointer (in 8f)
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer (in 8f)
    dw $c84f ; PLM Set pointer (in 8f)
    dw $e48a ; Background pointer (in 8f)
    dw $c91e ; Setup ASM pointer (in 8f)
Room_FD40_state_FD70_Header:    ; when MB glass is broken (in fast tourian)
    dl $ce8000 ; Level data pointer
    db $0e ; Tileset
    db $00 ; Song Set
    db $05 ; Play Index
    dw $0000 ; FX pointer (in 83)
    dw $e321 ; Enemy Set pointer (in a1)
    dw $9102 ; Enemy GFX pointer (in b4)
    dw $c1c1 ; Background X/Y scrolling
    dw Room_FD40_Scroll ; Room Scrolls pointer (in 8f)
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer (in 8f)
    dw $c84f ; PLM Set pointer (in 8f)
    dw $e48a ; Background pointer (in 8f)
    dw $c91e ; Setup ASM pointer (in 8f)
Room_FD40_state_FD8A_Header:    ; returning to the room after MB is dead
    dl $cddede ; Level data pointer
    db $0e ; Tileset
    db $00 ; Song Set
    db $03 ; Play Index
    dw $a188 ; FX pointer
    dw $8000 ; Enemy Set pointer
    dw $8000 ; Enemy GFX pointer
    dw $c1c1 ; Background X/Y scrolling
    dw Room_FD40_Scroll ; Room Scrolls pointer (in 8f)
    dw $0000 ; Unused pointer
    dw $0000 ; Main ASM pointer (in 8f)
    dw $c84f ; PLM Set pointer (in 8f)
    dw $e48a ; Background pointer (in 8f)
    dw $c91e ; Setup ASM pointer (in 8f)
Room_FD40_Door_List:
    dw $aa80
    dw $aa8c
Room_FD40_Scroll:
     db $01,$ff,$ff,$ff

; room 96BA: Climb
Room_96BA_state_9705_PLM_scroll_data_FS:
    ; Scroll data
    db $00,$02,$15,$02,$80
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_state_9787_PLM_scroll_data_FS_1:
    ; Scroll data
    db $02,$02,$05,$01,$80
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_state_9787_PLM_scroll_data_FS_2:
    ; Scroll data
    db $02,$01,$05,$00,$80,$03,$02,$80
; room C98E: Bowling Alley
Room_C98E_PLM_scroll_data_FS_1:
    ; Scroll data
    db $01,$00,$02,$00,$03,$00,$06,$00,$10,$00,$80
; room DCB1: Big Boy Room
Room_DCB1_Room_Scrolls_Pointer:
    db $00,$00,$01,$01,$01,$01
; room C98E: Bowling Alley
Room_C98E_PLM_scroll_data_FS_2:
    ; Scroll data
    db $07,$00,$08,$00,$09,$00,$0a,$00,$0b,$00,$0d,$00,$0f,$00,$10,$01,$80
; room DD58: Mother Brain Room
Room_DD58_Doors_List:
    dw $aa80                    ; bank 83: Room_DD58_door_list_index_0_Door: Rinka Shaft
    dw $aa8c                    ; bank 83: Room_DD58_door_list_index_1_Door: Tourian Escape Room 1
    dw $ad66                    ; bank 83: Room_DD58_door_list_index_2_Door: [new MB room] (new door in freespace)
    dw $0000
; room C98E: Bowling Alley
Room_C98E_PLM:
    ; PLM Set
    ; Scroll PLM
    dw $b703 : db $40 : db $2d : dw Room_C98E_state_C9BA_PLM_index_0_PLM_scroll_data 
    ; Scroll PLM
    dw $b703 : db $3d : db $06 : dw $a286 
    ; Scroll PLM
    dw $b703 : db $5d : db $19 : dw Room_C98E_PLM_scroll_data_FS_1
    ; Scroll PLM
    dw $b703 : db $1e : db $28 : dw Room_C98E_state_C9BA_PLM_index_3_PLM_scroll_data 
Room_C98E_Reserve:
    ; Reserve tank, chozo orb
    dw $ef7b : db $0c : db $0b : dw $0081 
Room_C98E_Missile:
    ; Missile tank
    dw $eedb : db $23 : db $26 : dw $0082 
Door_87_Room_C98E_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $5e : db $16 : dw $9087 
    ; Rightwards extension
    dw $b63b : db $54 : db $02 : dw $020b 
    ; Rightwards extension
    dw $b63b : db $54 : db $04 : dw $0436 
    ; Rightwards extension
    dw $b63b : db $54 : db $08 : dw $0105 
    ; Rightwards extension
    dw $b63b : db $54 : db $0a : dw $0132 
    ; Rightwards extension
    dw $b63b : db $54 : db $06 : dw $0105 
    ; Scroll PLM
    dw $b703 : db $4d : db $26 : dw Room_C98E_PLM_scroll_data_FS_2
    dw $0000
; room D8C5: Shaktool Room
Room_D8C5_PLM:
    ; PLM Set
    ; Scroll PLM
    dw $b703 : db $02 : db $0a : dw Room_D8C5_PLM_scroll_data_FS
    ; Scroll PLM
    dw $b703 : db $3d : db $0a : dw Room_D8C5_PLM_scroll_data_FS
    dw $0000
; room 9CB3: Dachora Room
Room_9CB3_PLM_scroll_data_FS:
    ; Scroll data
    db $02,$00,$80
; room D8C5: Shaktool Room
Room_D8C5_PLM_scroll_data_FS:
    ; Scroll data
    db $00,$01,$01,$01,$02,$01,$03,$01,$80
; room 96BA: Climb
Room_96BA_PLM_scroll_data_FS:
    ; Scroll data
    db $00,$00,$02,$00,$19,$00,$80

; room A98D: Crocomire's Room
Room_A98D_PLM:
    ; PLM Set
Door_4F_Room_A98D_PLM_C854:
    ; Door. Grey door facing down
    dw $c854 : db $36 : db $02 : dw $044f 
Energy_Tank_Crocomire:
    ; Energy tank
    dw $eed7 : db $02 : db $06 : dw $0034 
Door_EE_Room_A98D_PLM_C842:
    ; Door. Grey door facing left
    dw $c842 : db $7e : db $06 : dw $04ee 
    dw $0000

End_FreeSpace_8F:
warnpc $8FFE71
