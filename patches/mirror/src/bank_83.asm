;;; compile with thedopefish asar

arch 65816
lorom

incsrc "sym/bank_8f.asm"

org $838000
; room 91F8: Landing Site
Room_91F8_state_9261_FX:
    dw $95be ; Door pointer
    dw $01da ; Base Y position
    dw $00b0 ; Target Y position
    dw $0000 ; Y velocity
    db $f0 ; Timer
    db $02 ; Type (foreground layer 3)
    db $02 ; Default layer blending configuration (FX A)
    db $1e ; FX layer 3 layer blending configuration (FX B)
    db $0b ; FX liquid options (FX C)
    db $1f ; Palette FX bitset
    db $02 ; Animated tiles bitset
    db $02 ; Palette blend
org $8380f0
; room 92FD: Parlor and Alcatraz
Room_92FD_state_9314_FX:
    dw $0000 ; Door pointer
    dw $0466 ; Base Y position
    dw $ffff ; Target Y position
    dw $0000 ; Y velocity
    db $00 ; Timer
    db $00 ; Type (foreground layer 3)
    db $28 ; Default layer blending configuration (FX A)
    db $02 ; FX layer 3 layer blending configuration (FX B)
    db $00 ; FX liquid options (FX C)
    db $00 ; Palette FX bitset
    db $00 ; Animated tiles bitset
    db $62 ; Palette blend
org $83876a
; room B1E5: Acid Statue Room
Room_B1E5_state_B1F2_FX:
    dw $9876 ; Door pointer
    dw $02d2 ; Base Y position
    dw $ffff ; Target Y position
    dw $0000 ; Y velocity
    db $00 ; Timer
    db $04 ; Type (foreground layer 3)
    db $02 ; Default layer blending configuration (FX A)
    db $1e ; FX layer 3 layer blending configuration (FX B)
    db $82 ; FX liquid options (FX C)
    db $1f ; Palette FX bitset
    db $00 ; Animated tiles bitset
    db $00 ; Palette blend
org $83882c
; room B4AD: The Worst Room In The Game
Room_B4AD_state_B4BA_FX:
    dw $0000 ; Door pointer
    dw $ffff ; Base Y position
    dw $ffff ; Target Y position
    dw $0000 ; Y velocity
    db $00 ; Timer
    db $04 ; Type (foreground layer 3)
    db $02 ; Default layer blending configuration (FX A)
    db $1e ; FX layer 3 layer blending configuration (FX B)
    db $02 ; FX liquid options (FX C)
    db $1f ; Palette FX bitset
    db $02 ; Animated tiles bitset
    db $00 ; Palette blend
org $838916
; room 91F8: Landing Site
Room_91F8_door_list_index_0_Door:
    dw $92fd ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838922
; room 91F8: Landing Site
Room_91F8_door_list_index_1_Door:
    dw $95d4 ; Destination room header pointer (bank $8F): Crateria Tube
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83892e
; room 91F8: Landing Site
Room_91F8_door_list_index_2_Door:
    dw $92b3 ; Destination room header pointer (bank $8F): Gauntlet Entrance
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83893a
; room 91F8: Landing Site
Room_91F8_door_list_index_3_Door:
    dw $93aa ; Destination room header pointer (bank $8F): Crateria Power Bomb Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838946
; room 92B3: Gauntlet Entrance
Room_92B3_door_list_index_0_Door:
    dw $91f8 ; Destination room header pointer (bank $8F): Landing Site
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $8e ; X cap
    db $26 ; Y cap
    db $08 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $b997 ; Custom door ASM to execute (bank $8F)
org $838952
; room 92B3: Gauntlet Entrance
Room_92B3_door_list_index_1_Door:
    dw $965b ; Destination room header pointer (bank $8F): Gauntlet Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83895e
; room 92FD: Parlor and Alcatraz
Room_92FD_door_list_index_0_Door:
    dw $990d ; Destination room header pointer (bank $8F): Terminator Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83896a
; room 92FD: Parlor and Alcatraz
Room_92FD_door_list_index_1_Door:
    dw $91f8 ; Destination room header pointer (bank $8F): Landing Site
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $8e ; X cap
    db $46 ; Y cap
    db $08 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838976
; room 92FD: Parlor and Alcatraz
Room_92FD_door_list_index_2_Door:
    dw $98e2 ; Destination room header pointer (bank $8F): Pre-Map Flyway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838982
; room 92FD: Parlor and Alcatraz
Room_92FD_door_list_index_3_Door:
    dw $9879 ; Destination room header pointer (bank $8F): Flyway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83899a
; room 92FD: Parlor and Alcatraz
Room_92FD_door_list_index_5_Door:
    dw $93d5 ; Destination room header pointer (bank $8F): [Parlor Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8389a6
; room 92FD: Parlor and Alcatraz
Room_92FD_door_list_index_6_Door:
    dw $9a44 ; Destination room header pointer (bank $8F): Final Missile Bombway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8389b2
; room 93AA: Crateria Power Bomb Room
Room_93AA_door_list_index_0_Door:
    dw $91f8 ; Destination room header pointer (bank $8F): Landing Site
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8389be
; room 93D5: [Parlor Save Room]
Room_93D5_door_list_index_0_Door:
    dw $92fd ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $26 ; Y cap
    db $03 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $B981 ; Custom door ASM to execute (bank $8F)
org $8389ca
; room 93FE: West Ocean
Room_93FE_door_list_index_0_Door:
    dw $95ff ; Destination room header pointer (bank $8F): The Moat
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8389d6
; room 93FE: West Ocean
Room_93FE_door_list_index_1_Door:
    dw $ca08 ; Destination room header pointer (bank $8F): Wrecked Ship Entrance
    db $50 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $b971 ; Custom door ASM to execute (bank $8F)
org $8389e2
; room 93FE: West Ocean
Room_93FE_door_list_index_2_Door:
    dw $9461 ; Destination room header pointer (bank $8F): Bowling Alley Path
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8389ee
; room 93FE: West Ocean
Room_93FE_door_list_index_3_Door:
    dw $ca52 ; Destination room header pointer (bank $8F): Attic
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $06 ; Y cap
    db $06 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8389fa
; room 93FE: West Ocean
Room_93FE_door_list_index_4_Door:
    dw $c98e ; Destination room header pointer (bank $8F): Bowling Alley
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $b9b3 ; Custom door ASM to execute (bank $8F)
org $838a12
; room 9461: Bowling Alley Path
Room_9461_door_list_index_0_Door:
    dw $93fe ; Destination room header pointer (bank $8F): West Ocean
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $51 ; X cap
    db $26 ; Y cap
    db $05 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838a1e
; room 9461: Bowling Alley Path
Room_9461_door_list_index_1_Door:
    dw $968f ; Destination room header pointer (bank $8F): [West Ocean Geemer Corridor]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838a2a
; room 948C: Crateria Keyhunter Room
Room_948C_door_list_index_0_Door:
    dw $95d4 ; Destination room header pointer (bank $8F): Crateria Tube
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838a36
; room 948C: Crateria Keyhunter Room
Room_948C_door_list_index_1_Door:
    dw $95ff ; Destination room header pointer (bank $8F): The Moat
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838a66
; room 94FD: East Ocean
Room_94FD_door_list_index_0_Door:
    dw $cbd5 ; Destination room header pointer (bank $8F): Electric Death Room
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838a72
; room 94FD: East Ocean
Room_94FD_door_list_index_1_Door:
    dw $9552 ; Destination room header pointer (bank $8F): Forgotten Highway Kago Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838a7e
; room 9552: Forgotten Highway Kago Room
Room_9552_door_list_index_0_Door:
    dw $94fd ; Destination room header pointer (bank $8F): East Ocean
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $46 ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838a8a
; room 9552: Forgotten Highway Kago Room
Room_9552_door_list_index_1_Door:
    dw $957d ; Destination room header pointer (bank $8F): Crab Maze
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $06 ; X cap
    db $02 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838aa2
; room 95A8: [Crab Maze to Elevator]
Room_95A8_door_list_index_0_Door:
    dw $957d ; Destination room header pointer (bank $8F): Crab Maze
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $16 ; Y cap
    db $03 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838aae
; room 957D: Crab Maze
Room_957D_door_list_index_1_Door:
    dw $95a8 ; Destination room header pointer (bank $8F): [Crab Maze to Elevator]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ac6
; room 95D4: Crateria Tube
Room_95D4_door_list_index_0_Door:
    dw $91f8 ; Destination room header pointer (bank $8F): Landing Site
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $46 ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ad2
; room 95D4: Crateria Tube
Room_95D4_door_list_index_1_Door:
    dw $948c ; Destination room header pointer (bank $8F): Crateria Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ade
; room 95FF: The Moat
Room_95FF_door_list_index_0_Door:
    dw $948c ; Destination room header pointer (bank $8F): Crateria Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838aea
; room 95FF: The Moat
Room_95FF_door_list_index_1_Door:
    dw $93fe ; Destination room header pointer (bank $8F): West Ocean
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $46 ; Y cap
    db $07 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838af6
; room 962A: [Elevator to Red Brinstar]
Room_962A_door_list_index_0_Door:
    dw $948C ; Destination room header pointer (bank $8F): Crateria Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $16 ; X cap
    db $2D ; Y cap
    db $01 ; X screen
    db $02 ; Y screen
    dw $01C0 ; Distance from door to spawn Samus
    dw $B9F1 ; Custom door ASM to execute (bank $8F)
org $838b02
; room 962A: [Elevator to Red Brinstar]
Room_962A_door_list_index_1_Door:
    dw $a322 ; Destination room header pointer (bank $8F): Caterpillar Room
    db $e0 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $20 ; X cap
    db $00 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $0000 ; Distance from door to spawn Samus
    dw $BA21 ; Custom door ASM to execute (bank $8F)
org $838b0e
; room 965B: Gauntlet Energy Tank Room
Room_965B_door_list_index_0_Door:
    dw $92b3 ; Destination room header pointer (bank $8F): Gauntlet Entrance
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b1a
; room 965B: Gauntlet Energy Tank Room
Room_965B_door_list_index_1_Door:
    dw $99bd ; Destination room header pointer (bank $8F): Green Pirates Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $ba2c ; Custom door ASM to execute (bank $8F)
org $838b26
; room 968F: [West Ocean Geemer Corridor]
Room_968F_door_list_index_0_Door:
    dw $9461 ; Destination room header pointer (bank $8F): Bowling Alley Path
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b32
; room 968F: [West Ocean Geemer Corridor]
Room_968F_door_list_index_1_Door:
    dw $c98e ; Destination room header pointer (bank $8F): Bowling Alley
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $16 ; Y cap
    db $05 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $B9CA ; Custom door ASM to execute (bank $8F)
org $838b3e
; room 96BA: Climb
Room_96BA_door_list_index_0_Door:
    dw $92fd ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $36 ; X cap
    db $4d ; Y cap
    db $03 ; X screen
    db $04 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b4a
; room 96BA: Climb
Room_96BA_door_list_index_1_Door:
    dw $99f9 ; Destination room header pointer (bank $8F): Crateria Super Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b56
; room 96BA: Climb
Room_96BA_door_list_index_2_Door:
    dw $99f9 ; Destination room header pointer (bank $8F): Crateria Super Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $76 ; Y cap
    db $03 ; X screen
    db $07 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b62
; room 96BA: Climb
Room_96BA_door_list_index_3_Door:
    dw $975c ; Destination room header pointer (bank $8F): Pit Room [Old Mother Brain Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b6e
; room 96BA: Climb
Room_96BA_door_list_index_4_Door:
    dw $dede ; Destination room header pointer (bank $8F): Tourian Escape Room 4
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b7a
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_door_list_index_0_Door:
    dw $96ba ; Destination room header pointer (bank $8F): Climb
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $86 ; Y cap
    db $01 ; X screen
    db $08 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b86
; room 975C: Pit Room [Old Mother Brain Room]
Room_975C_door_list_index_1_Door:
    dw $97b5 ; Destination room header pointer (bank $8F): [Elevator to Blue Brinstar]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b92
; room 97B5: [Elevator to Blue Brinstar]
Room_97B5_door_list_index_0_Door:
    dw $975c ; Destination room header pointer (bank $8F): Pit Room [Old Mother Brain Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838b9e
; room 97B5: [Elevator to Blue Brinstar]
Room_97B5_door_list_index_1_Door:
    dw $9e9f ; Destination room header pointer (bank $8F): Morph Ball Room
    db $f0 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $20 ; X cap
    db $00 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $0000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838baa
; room 9804: Bomb Torizo Room
Room_9804_door_list_index_0_Door:
    dw $9879 ; Destination room header pointer (bank $8F): Flyway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838bb6
; room 9879: Flyway
Room_9879_door_list_index_0_Door:
    dw $92fd ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $26 ; Y cap
    db $01 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $B9A2 ; Custom door ASM to execute (bank $8F)
org $838bc2
; room 9879: Flyway
Room_9879_door_list_index_1_Door:
    dw $9804 ; Destination room header pointer (bank $8F): Bomb Torizo Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838bce
; room 98E2: Pre-Map Flyway
Room_98E2_door_list_index_0_Door:
    dw $92fd ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $31 ; X cap
    db $36 ; Y cap
    db $03 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838bda
; room 98E2: Pre-Map Flyway
Room_98E2_door_list_index_1_Door:
    dw $9994 ; Destination room header pointer (bank $8F): Crateria Map Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838be6
; room 990D: Terminator Room
Room_990D_door_list_index_0_Door:
    dw $99bd ; Destination room header pointer (bank $8F): Green Pirates Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $46 ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838bf2
; room 990D: Terminator Room
Room_990D_door_list_index_1_Door:
    dw $92fd ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $b98c ; Custom door ASM to execute (bank $8F)
org $838bfe
; room 9938: [Elevator to Green Brinstar]
Room_9938_door_list_index_0_Door:
    dw $9969 ; Destination room header pointer (bank $8F): Lower Mushrooms
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c0a
; room 9938: [Elevator to Green Brinstar]
Room_9938_door_list_index_1_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $c0 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $30 ; X cap
    db $00 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $0000 ; Distance from door to spawn Samus
    dw $bd25 ; Custom door ASM to execute (bank $8F)
org $838c16
; room 9969: Lower Mushrooms
Room_9969_door_list_index_0_Door:
    dw $99bd ; Destination room header pointer (bank $8F): Green Pirates Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $66 ; Y cap
    db $00 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c22
; room 9969: Lower Mushrooms
Room_9969_door_list_index_1_Door:
    dw $9938 ; Destination room header pointer (bank $8F): [Elevator to Green Brinstar]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c2e
; room 9994: Crateria Map Room
Room_9994_door_list_index_0_Door:
    dw $98e2 ; Destination room header pointer (bank $8F): Pre-Map Flyway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c3a
; room 99BD: Green Pirates Shaft
Room_99BD_door_list_index_0_Door:
    dw $990d ; Destination room header pointer (bank $8F): Terminator Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $26 ; Y cap
    db $05 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c46
; room 99BD: Green Pirates Shaft
Room_99BD_door_list_index_1_Door:
    dw $9969 ; Destination room header pointer (bank $8F): Lower Mushrooms
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c52
; room 99BD: Green Pirates Shaft
Room_99BD_door_list_index_2_Door:
    dw $a5ed ; Destination room header pointer (bank $8F): Statues Hallway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c5e
; room 99BD: Green Pirates Shaft
Room_99BD_door_list_index_3_Door:
    dw $965b ; Destination room header pointer (bank $8F): Gauntlet Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $ba16 ; Custom door ASM to execute (bank $8F)
org $838c6a
; room 99F9: Crateria Super Room
Room_99F9_door_list_index_0_Door:
    dw $96ba ; Destination room header pointer (bank $8F): Climb
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BA00 ; Custom door ASM to execute (bank $8F)
org $838c76
; room 99F9: Crateria Super Room
Room_99F9_door_list_index_1_Door:
    dw $96ba ; Destination room header pointer (bank $8F): Climb
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $76 ; Y cap
    db $00 ; X screen
    db $07 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BA0B ; Custom door ASM to execute (bank $8F)
org $838c82
; room 9A44: Final Missile Bombway
Room_9A44_door_list_index_0_Door:
    dw $9a90 ; Destination room header pointer (bank $8F): The Final Missile
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c8e
; room 9A44: Final Missile Bombway
Room_9A44_door_list_index_1_Door:
    dw $92fd ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $36 ; Y cap
    db $03 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838c9a
; room 9A90: The Final Missile
Room_9A90_door_list_index_0_Door:
    dw $9a44 ; Destination room header pointer (bank $8F): Final Missile Bombway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838cb2
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_1_Door:
    dw $9b9d ; Destination room header pointer (bank $8F): Brinstar Pre-Map Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838cbe
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_2_Door:
    dw $9fe5 ; Destination room header pointer (bank $8F): Green Brinstar Beetom Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838cca
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_3_Door:
    dw $9c5e ; Destination room header pointer (bank $8F): Green Brinstar Fireflea Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838cd6
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_4_Door:
    dw $9bc8 ; Destination room header pointer (bank $8F): Early Supers Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $16 ; Y cap
    db $02 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ce2
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_5_Door:
    dw $9cb3 ; Destination room header pointer (bank $8F): Dachora Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $06 ; Y cap
    db $06 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BD6C ; Custom door ASM to execute (bank $8F)
org $838cee
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_6_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $76 ; Y cap
    db $02 ; X screen
    db $07 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd25 ; Custom door ASM to execute (bank $8F)
org $838cfa
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_7_Door:
    dw $a011 ; Destination room header pointer (bank $8F): Etecoon Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd16 ; Custom door ASM to execute (bank $8F)
org $838d06
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_8_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $31 ; X cap
    db $76 ; Y cap
    db $03 ; X screen
    db $07 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd07 ; Custom door ASM to execute (bank $8F)
org $838d12
; room 9AD9: Green Brinstar Main Shaft [etecoon room]
Room_9AD9_door_list_index_A_Door:
    dw $a201 ; Destination room header pointer (bank $8F): [Green Brinstar Main Shaft Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d1e
; room 9B5B: Spore Spawn Super Room
Room_9B5B_door_list_index_0_Door:
    dw $a0a4 ; Destination room header pointer (bank $8F): Spore Spawn Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d2a
; room 9B5B: Spore Spawn Super Room
Room_9B5B_door_list_index_1_Door:
    dw $9dc7 ; Destination room header pointer (bank $8F): Spore Spawn Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d36
; room 9B9D: Brinstar Pre-Map Room
Room_9B9D_door_list_index_0_Door:
    dw $9c35 ; Destination room header pointer (bank $8F): Brinstar Map Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d42
; room 9B9D: Brinstar Pre-Map Room
Room_9B9D_door_list_index_1_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $46 ; Y cap
    db $03 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d4e
; room 9BC8: Early Supers Room
Room_9BC8_door_list_index_0_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $31 ; X cap
    db $46 ; Y cap
    db $03 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d5a
; room 9BC8: Early Supers Room
Room_9BC8_door_list_index_1_Door:
    dw $9c07 ; Destination room header pointer (bank $8F): Brinstar Reserve Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d66
; room 9C07: Brinstar Reserve Tank Room
Room_9C07_door_list_index_0_Door:
    dw $9bc8 ; Destination room header pointer (bank $8F): Early Supers Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d72
; room 9C35: Brinstar Map Room
Room_9C35_door_list_index_0_Door:
    dw $9b9d ; Destination room header pointer (bank $8F): Brinstar Pre-Map Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d7e
; room 9C5E: Green Brinstar Fireflea Room
Room_9C5E_door_list_index_0_Door:
    dw $9c89 ; Destination room header pointer (bank $8F): [Green Brinstar Missile Station]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d8a
; room 9C5E: Green Brinstar Fireflea Room
Room_9C5E_door_list_index_1_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $66 ; Y cap
    db $03 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838d96
; room 9C89: [Green Brinstar Missile Station]
Room_9C89_door_list_index_0_Door:
    dw $9c5e ; Destination room header pointer (bank $8F): Green Brinstar Fireflea Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $16 ; Y cap
    db $02 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838da2
; room 9CB3: Dachora Room
Room_9CB3_door_list_index_0_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $31 ; X cap
    db $66 ; Y cap
    db $03 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838dae
; room 9CB3: Dachora Room
Room_9CB3_door_list_index_1_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $26 ; Y cap
    db $02 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838dba
; room 9CB3: Dachora Room
Room_9CB3_door_list_index_2_Door:
    dw $a07b ; Destination room header pointer (bank $8F): [Dachora Room Energy Charge Station]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838dc6
; room 9D19: Big Pink
Room_9D19_door_list_index_0_Door:
    dw $9d9c ; Destination room header pointer (bank $8F): Spore Spawn Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838dd2
; room 9D19: Big Pink
Room_9D19_door_list_index_1_Door:
    dw $9cb3 ; Destination room header pointer (bank $8F): Dachora Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838dde
; room 9D19: Big Pink
Room_9D19_door_list_index_2_Door:
    dw $9e11 ; Destination room header pointer (bank $8F): Pink Brinstar Power Bomb Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd30 ; Custom door ASM to execute (bank $8F)
org $838dea
; room 9D19: Big Pink
Room_9D19_door_list_index_3_Door:
    dw $9e52 ; Destination room header pointer (bank $8F): Green Hill Zone
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $06 ; Y cap
    db $07 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838df6
; room 9D19: Big Pink
Room_9D19_door_list_index_4_Door:
    dw $a184 ; Destination room header pointer (bank $8F): [Spore Spawn Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e02
; room 9D19: Big Pink
Room_9D19_door_list_index_5_Door:
    dw $9e11 ; Destination room header pointer (bank $8F): Pink Brinstar Power Bomb Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e0e
; room 9D19: Big Pink
Room_9D19_door_list_index_6_Door:
    dw $a0d2 ; Destination room header pointer (bank $8F): Waterway Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e1a
; room 9D19: Big Pink
Room_9D19_door_list_index_7_Door:
    dw $a130 ; Destination room header pointer (bank $8F): Pink Brinstar Hopper Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e26
; room 9D19: Big Pink
Room_9D19_door_list_index_8_Door:
    dw $a0a4 ; Destination room header pointer (bank $8F): Spore Spawn Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e32
; room 9D9C: Spore Spawn Keyhunter Room
Room_9D9C_door_list_index_0_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e4a
; room 9DC7: Spore Spawn Room
Room_9DC7_door_list_index_0_Door:
    dw $9b5b ; Destination room header pointer (bank $8F): Spore Spawn Super Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bdc0 ; Custom door ASM to execute (bank $8F)
org $838e56
; room 9DC7: Spore Spawn Room
Room_9DC7_door_list_index_1_Door:
    dw $9d9c ; Destination room header pointer (bank $8F): Spore Spawn Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $06 ; X cap
    db $03 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e62
; room 9E11: Pink Brinstar Power Bomb Room
Room_9E11_door_list_index_0_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $2e ; X cap
    db $36 ; Y cap
    db $02 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e6e
; room 9E11: Pink Brinstar Power Bomb Room
Room_9E11_door_list_index_1_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $46 ; Y cap
    db $02 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e7a
; room 9E52: Green Hill Zone
Room_9E52_door_list_index_0_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $66 ; Y cap
    db $01 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e86
; room 9E52: Green Hill Zone
Room_9E52_door_list_index_1_Door:
    dw $9e9f ; Destination room header pointer (bank $8F): Morph Ball Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $26 ; Y cap
    db $07 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e92
; room 9E52: Green Hill Zone
Room_9E52_door_list_index_2_Door:
    dw $9fba ; Destination room header pointer (bank $8F): Noob Bridge
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838e9e
; room 9E9F: Morph Ball Room
Room_9E9F_door_list_index_0_Door:
    dw $9e52 ; Destination room header pointer (bank $8F): Green Hill Zone
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $61 ; X cap
    db $06 ; Y cap
    db $06 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838eaa
; room 9E9F: Morph Ball Room
Room_9E9F_door_list_index_1_Door:
    dw $9f11 ; Destination room header pointer (bank $8F): Construction Zone
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ec2
; room 9F11: Construction Zone
Room_9F11_door_list_index_0_Door:
    dw $9e9f ; Destination room header pointer (bank $8F): Morph Ball Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ece
; room 9F11: Construction Zone
Room_9F11_door_list_index_1_Door:
    dw $9f64 ; Destination room header pointer (bank $8F): Blue Brinstar Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $26 ; Y cap
    db $02 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838eda
; room 9F11: Construction Zone
Room_9F11_door_list_index_2_Door:
    dw $a107 ; Destination room header pointer (bank $8F): First Missile Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ee6
; room 9F64: Blue Brinstar Energy Tank Room
Room_9F64_door_list_index_0_Door:
    dw $9f11 ; Destination room header pointer (bank $8F): Construction Zone
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ef2
; room 9F64: Blue Brinstar Energy Tank Room
Room_9F64_door_list_index_1_Door:
    dw $a1ad ; Destination room header pointer (bank $8F): Blue Brinstar Boulder Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838efe
; room 9FBA: Noob Bridge
Room_9FBA_door_list_index_0_Door:
    dw $9e52 ; Destination room header pointer (bank $8F): Green Hill Zone
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f0a
; room 9FBA: Noob Bridge
Room_9FBA_door_list_index_1_Door:
    dw $a253 ; Destination room header pointer (bank $8F): Red Tower
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $46 ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f16
; room 9FE5: Green Brinstar Beetom Room
Room_9FE5_door_list_index_0_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $a6 ; Y cap
    db $03 ; X screen
    db $0a ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd07 ; Custom door ASM to execute (bank $8F)
org $838f22
; room 9FE5: Green Brinstar Beetom Room
Room_9FE5_door_list_index_1_Door:
    dw $a011 ; Destination room header pointer (bank $8F): Etecoon Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $31 ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f2e
; room A011: Etecoon Energy Tank Room
Room_A011_door_list_index_0_Door:
    dw $9fe5 ; Destination room header pointer (bank $8F): Green Brinstar Beetom Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f3a
; room A011: Etecoon Energy Tank Room
Room_A011_door_list_index_1_Door:
    dw $a051 ; Destination room header pointer (bank $8F): Etecoon Super Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f46
; room A011: Etecoon Energy Tank Room
Room_A011_door_list_index_2_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $b6 ; Y cap
    db $01 ; X screen
    db $0b ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f52
; room A011: Etecoon Energy Tank Room
Room_A011_door_list_index_3_Door:
    dw $a22a ; Destination room header pointer (bank $8F): [Etecoon Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f5e
; room A051: Etecoon Super Room
Room_A051_door_list_index_0_Door:
    dw $a011 ; Destination room header pointer (bank $8F): Etecoon Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f6a
; room A07B: [Dachora Room Energy Charge Station]
Room_A07B_door_list_index_0_Door:
    dw $9cb3 ; Destination room header pointer (bank $8F): Dachora Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $66 ; Y cap
    db $06 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BD50 ; Custom door ASM to execute (bank $8F)
org $838f76
; room A0A4: Spore Spawn Farming Room
Room_A0A4_door_list_index_0_Door:
    dw $9b5b ; Destination room header pointer (bank $8F): Spore Spawn Super Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $86 ; Y cap
    db $01 ; X screen
    db $08 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838f82
; room A0A4: Spore Spawn Farming Room
Room_A0A4_door_list_index_1_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $56 ; Y cap
    db $00 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd5b ; Custom door ASM to execute (bank $8F)
org $838f8e
; room A0D2: Waterway Energy Tank Room
Room_A0D2_door_list_index_0_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $96 ; Y cap
    db $04 ; X screen
    db $09 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd77 ; Custom door ASM to execute (bank $8F)
org $838fa6
; room A107: First Missile Room
Room_A107_door_list_index_0_Door:
    dw $9f11 ; Destination room header pointer (bank $8F): Construction Zone
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $be25 ; Custom door ASM to execute (bank $8F)
org $838fb2
; room A130: Pink Brinstar Hopper Room
Room_A130_door_list_index_0_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $46 ; Y cap
    db $01 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838fbe
; room A130: Pink Brinstar Hopper Room
Room_A130_door_list_index_1_Door:
    dw $a15b ; Destination room header pointer (bank $8F): Hopper Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838fca
; room A15B: Hopper Energy Tank Room
Room_A15B_door_list_index_0_Door:
    dw $a130 ; Destination room header pointer (bank $8F): Pink Brinstar Hopper Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838fd6
; room A184: [Spore Spawn Save Room]
Room_A184_door_list_index_0_Door:
    dw $9d19 ; Destination room header pointer (bank $8F): Big Pink
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $be00 ; Custom door ASM to execute (bank $8F)
org $838fe2
; room A1AD: Blue Brinstar Boulder Room
Room_A1AD_door_list_index_0_Door:
    dw $9f64 ; Destination room header pointer (bank $8F): Blue Brinstar Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd8a ; Custom door ASM to execute (bank $8F)
org $838fee
; room A1AD: Blue Brinstar Boulder Room
Room_A1AD_door_list_index_1_Door:
    dw $a1d8 ; Destination room header pointer (bank $8F): Blue Brinstar Double Missile Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $838ffa
; room A1D8: Blue Brinstar Double Missile Room
Room_A1D8_door_list_index_0_Door:
    dw $a1ad ; Destination room header pointer (bank $8F): Blue Brinstar Boulder Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839006
; room A201: [Green Brinstar Main Shaft Save Room]
Room_A201_door_list_index_0_Door:
    dw $9ad9 ; Destination room header pointer (bank $8F): Green Brinstar Main Shaft [etecoon room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $56 ; Y cap
    db $03 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839012
; room A22A: [Etecoon Save Room]
Room_A22A_door_list_index_0_Door:
    dw $a011 ; Destination room header pointer (bank $8F): Etecoon Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $16 ; Y cap
    db $04 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bd16 ; Custom door ASM to execute (bank $8F)
org $83901e
; room A253: Red Tower
Room_A253_door_list_index_0_Door:
    dw $a2f7 ; Destination room header pointer (bank $8F): Hellway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83902a
; room A253: Red Tower
Room_A253_door_list_index_1_Door:
    dw $9fba ; Destination room header pointer (bank $8F): Noob Bridge
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839036
; room A253: Red Tower
Room_A253_door_list_index_2_Door:
    dw $a293 ; Destination room header pointer (bank $8F): Red Brinstar Fireflea Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839042
; room A253: Red Tower
Room_A253_door_list_index_3_Door:
    dw $a3dd ; Destination room header pointer (bank $8F): Bat Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83904e
; room A253: Red Tower
Room_A253_door_list_index_4_Door:
    dw $a618 ; Destination room header pointer (bank $8F): [Red Tower Energy Charge Station]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83905a
; room A293: Red Brinstar Fireflea Room
Room_A293_door_list_index_0_Door:
    dw $a2ce ; Destination room header pointer (bank $8F): X-Ray Scope Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839066
; room A293: Red Brinstar Fireflea Room
Room_A293_door_list_index_1_Door:
    dw $a253 ; Destination room header pointer (bank $8F): Red Tower
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $66 ; Y cap
    db $00 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839072
; room A2CE: X-Ray Scope Room
Room_A2CE_door_list_index_0_Door:
    dw $a293 ; Destination room header pointer (bank $8F): Red Brinstar Fireflea Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $06 ; Y cap
    db $07 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83907e
; room A2F7: Hellway
Room_A2F7_door_list_index_0_Door:
    dw $a253 ; Destination room header pointer (bank $8F): Red Tower
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83908a
; room A2F7: Hellway
Room_A2F7_door_list_index_1_Door:
    dw $a322 ; Destination room header pointer (bank $8F): Caterpillar Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $56 ; Y cap
    db $02 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $be1a ; Custom door ASM to execute (bank $8F)
org $839096
; room A322: Caterpillar Room
Room_A322_door_list_index_0_Door:
    dw $a3ae ; Destination room header pointer (bank $8F): Alpha Power Bomb Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8390a2
; room A322: Caterpillar Room
Room_A322_door_list_index_1_Door:
    dw $a37c ; Destination room header pointer (bank $8F): Beta Power Bomb Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8390ae
; room A322: Caterpillar Room
Room_A322_door_list_index_2_Door:
    dw $a2f7 ; Destination room header pointer (bank $8F): Hellway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8390c6
; room A322: Caterpillar Room
Room_A322_door_list_index_4_Door:
    dw $d104 ; Destination room header pointer (bank $8F): Red Fish Room
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BDAF ; Custom door ASM to execute (bank $8F)
org $8390d2
; room A322: Caterpillar Room
Room_A322_door_list_index_6_Door:
    dw $a734 ; Destination room header pointer (bank $8F): [Caterpillar Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8390de
; room A37C: Beta Power Bomb Room
Room_A37C_door_list_index_0_Door:
    dw $a322 ; Destination room header pointer (bank $8F): Caterpillar Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $36 ; Y cap
    db $02 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8390ea
; room A3AE: Alpha Power Bomb Room
Room_A3AE_door_list_index_0_Door:
    dw $a322 ; Destination room header pointer (bank $8F): Caterpillar Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $76 ; Y cap
    db $02 ; X screen
    db $07 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $be0b ; Custom door ASM to execute (bank $8F)
org $8390f6
; room A3DD: Bat Room
Room_A3DD_door_list_index_0_Door:
    dw $a253 ; Destination room header pointer (bank $8F): Red Tower
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $96 ; Y cap
    db $00 ; X screen
    db $09 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bda0 ; Custom door ASM to execute (bank $8F)
org $839102
; room A3DD: Bat Room
Room_A3DD_door_list_index_1_Door:
    dw $a408 ; Destination room header pointer (bank $8F): Below Spazer
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83910e
; room A408: Below Spazer
Room_A408_door_list_index_0_Door:
    dw $a3dd ; Destination room header pointer (bank $8F): Bat Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83911a
; room A408: Below Spazer
Room_A408_door_list_index_1_Door:
    dw $cf54 ; Destination room header pointer (bank $8F): West Tunnel
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839126
; room A408: Below Spazer
Room_A408_door_list_index_2_Door:
    dw $a447 ; Destination room header pointer (bank $8F): Spazer Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839132
; room A447: Spazer Room
Room_A447_door_list_index_0_Door:
    dw $a408 ; Destination room header pointer (bank $8F): Below Spazer
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bdf1 ; Custom door ASM to execute (bank $8F)
org $83913e
; room A471: Warehouse Zeela Room
Room_A471_door_list_index_0_Door:
    dw $a6a1 ; Destination room header pointer (bank $8F): Warehouse Entrance
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BD3F ; Custom door ASM to execute (bank $8F)
org $83914a
; room A471: Warehouse Zeela Room
Room_A471_door_list_index_1_Door:
    dw $a4b1 ; Destination room header pointer (bank $8F): Warehouse Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839156
; room A471: Warehouse Zeela Room
Room_A471_door_list_index_2_Door:
    dw $a4da ; Destination room header pointer (bank $8F): Warehouse Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $36 ; X cap
    db $0c ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $0240 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839162
; room A4B1: Warehouse Energy Tank Room
Room_A4B1_door_list_index_0_Door:
    dw $a471 ; Destination room header pointer (bank $8F): Warehouse Zeela Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83916e
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_door_list_index_0_Door:
    dw $a471 ; Destination room header pointer (bank $8F): Warehouse Zeela Room
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $06 ; X cap
    db $13 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83917a
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_door_list_index_1_Door:
    dw $a521 ; Destination room header pointer (bank $8F): Baby Kraid Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839186
; room A4DA: Warehouse Keyhunter Room
Room_A4DA_door_list_index_2_Door:
    dw $a70b ; Destination room header pointer (bank $8F): [Kraid Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839192
; room A521: Baby Kraid Room
Room_A521_door_list_index_0_Door:
    dw $a4da ; Destination room header pointer (bank $8F): Warehouse Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $21 ; X cap
    db $16 ; Y cap
    db $02 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83919e
; room A521: Baby Kraid Room
Room_A521_door_list_index_1_Door:
    dw $a56b ; Destination room header pointer (bank $8F): Kraid Eye Door Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391aa
; room A56B: Kraid Eye Door Room
Room_A56B_door_list_index_0_Door:
    dw $a521 ; Destination room header pointer (bank $8F): Baby Kraid Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391b6
; room A56B: Kraid Eye Door Room
Room_A56B_door_list_index_1_Door:
    dw $a59f ; Destination room header pointer (bank $8F): Kraid Room
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391c2
; room A56B: Kraid Eye Door Room
Room_A56B_door_list_index_2_Door:
    dw $a641 ; Destination room header pointer (bank $8F): [Kraid Recharge Station]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391ce
; room A59F: Kraid Room
Room_A59F_door_list_index_0_Door:
    dw $a56b ; Destination room header pointer (bank $8F): Kraid Eye Door Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391da
; room A59F: Kraid Room
Room_A59F_door_list_index_1_Door:
    dw $a6e2 ; Destination room header pointer (bank $8F): Varia Suit Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391e6
; room A5ED: Statues Hallway
Room_A5ED_door_list_index_0_Door:
    dw $99bd ; Destination room header pointer (bank $8F): Green Pirates Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $66 ; Y cap
    db $00 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391f2
; room A5ED: Statues Hallway
Room_A5ED_door_list_index_1_Door:
    dw $a66a ; Destination room header pointer (bank $8F): Statues Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8391fe
; room A618: [Red Tower Energy Charge Station]
Room_A618_door_list_index_0_Door:
    dw $a253 ; Destination room header pointer (bank $8F): Red Tower
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $96 ; Y cap
    db $00 ; X screen
    db $09 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bda0 ; Custom door ASM to execute (bank $8F)
org $83920a
; room A641: [Kraid Recharge Station]
Room_A641_door_list_index_0_Door:
    dw $a56b ; Destination room header pointer (bank $8F): Kraid Eye Door Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BD95 ; Custom door ASM to execute (bank $8F)
org $839216
; room A66A: Statues Room
Room_A66A_door_list_index_0_Door:
    dw $a5ed ; Destination room header pointer (bank $8F): Statues Hallway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83922e
; room A6A1: Warehouse Entrance
Room_A6A1_door_list_index_0_Door:
    dw $cf80 ; Destination room header pointer (bank $8F): East Tunnel
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $31 ; X cap
    db $16 ; Y cap
    db $03 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bdd1 ; Custom door ASM to execute (bank $8F)
org $83923a
; room A6A1: Warehouse Entrance
Room_A6A1_door_list_index_1_Door:
    dw $a471 ; Destination room header pointer (bank $8F): Warehouse Zeela Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839252
; room A6E2: Varia Suit Room
Room_A6E2_door_list_index_0_Door:
    dw $a59f ; Destination room header pointer (bank $8F): Kraid Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83925e
; room A70B: [Kraid Save Room]
Room_A70B_door_list_index_0_Door:
    dw $a4da ; Destination room header pointer (bank $8F): Warehouse Keyhunter Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $BDE2 ; Custom door ASM to execute (bank $8F)
org $83926a
; room A734: [Caterpillar Save Room]
Room_A734_door_list_index_0_Door:
    dw $a322 ; Destination room header pointer (bank $8F): Caterpillar Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $21 ; X cap
    db $46 ; Y cap
    db $02 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839276
; room A75D: Ice Beam Acid Room
Room_A75D_door_list_index_0_Door:
    dw $a815 ; Destination room header pointer (bank $8F): Ice Beam Gate Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $26 ; Y cap
    db $03 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839282
; room A75D: Ice Beam Acid Room
Room_A75D_door_list_index_1_Door:
    dw $a8b9 ; Destination room header pointer (bank $8F): Ice Beam Snake Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $26 ; Y cap
    db $01 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83928e
; room A788: Cathedral
Room_A788_door_list_index_0_Door:
    dw $a7b3 ; Destination room header pointer (bank $8F): Cathedral Entrance
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83929a
; room A788: Cathedral
Room_A788_door_list_index_1_Door:
    dw $afa3 ; Destination room header pointer (bank $8F): Rising Tide
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392a6
; room A7B3: Cathedral Entrance
Room_A7B3_door_list_index_0_Door:
    dw $a7de ; Destination room header pointer (bank $8F): Business Center
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392b2
; room A7B3: Cathedral Entrance
Room_A7B3_door_list_index_1_Door:
    dw $a788 ; Destination room header pointer (bank $8F): Cathedral
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392be
; room A7DE: Business Center
Room_A7DE_door_list_index_0_Door:
    dw $a815 ; Destination room header pointer (bank $8F): Ice Beam Gate Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392ca
; room A7DE: Business Center
Room_A7DE_door_list_index_1_Door:
    dw $a7b3 ; Destination room header pointer (bank $8F): Cathedral Entrance
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392d6
; room A7DE: Business Center
Room_A7DE_door_list_index_2_Door:
    dw $aa41 ; Destination room header pointer (bank $8F): Hi Jump Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392e2
; room A7DE: Business Center
Room_A7DE_door_list_index_3_Door:
    dw $aa0e ; Destination room header pointer (bank $8F): Crocomire Escape
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392ee
; room A7DE: Business Center
Room_A7DE_door_list_index_4_Door:
    dw $a6a1 ; Destination room header pointer (bank $8F): Warehouse Entrance
    db $d0 ; Bit Flag (Elevator properties)
    db $03 ; Direction
    db $20 ; X cap
    db $00 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $0000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8392fa
; room A7DE: Business Center
Room_A7DE_door_list_index_6_Door:
    dw $b167 ; Destination room header pointer (bank $8F): [Business Center Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839306
; room A7DE: Business Center
Room_A7DE_door_list_index_7_Door:
    dw $b0b4 ; Destination room header pointer (bank $8F): Norfair Map Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839312
; room A815: Ice Beam Gate Room
Room_A815_door_list_index_0_Door:
    dw $a865 ; Destination room header pointer (bank $8F): Ice Beam Tutorial Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83931e
; room A815: Ice Beam Gate Room
Room_A815_door_list_index_1_Door:
    dw $a75d ; Destination room header pointer (bank $8F): Ice Beam Acid Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83932a
; room A815: Ice Beam Gate Room
Room_A815_door_list_index_2_Door:
    dw $a7de ; Destination room header pointer (bank $8F): Business Center
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839336
; room A815: Ice Beam Gate Room
Room_A815_door_list_index_3_Door:
    dw $a8f8 ; Destination room header pointer (bank $8F): Crumble Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839342
; room A865: Ice Beam Tutorial Room
Room_A865_door_list_index_0_Door:
    dw $a8b9 ; Destination room header pointer (bank $8F): Ice Beam Snake Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83934e
; room A865: Ice Beam Tutorial Room
Room_A865_door_list_index_1_Door:
    dw $a815 ; Destination room header pointer (bank $8F): Ice Beam Gate Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bffa ; Custom door ASM to execute (bank $8F)
org $83935a
; room A890: Ice Beam Room
Room_A890_door_list_index_0_Door:
    dw $a8b9 ; Destination room header pointer (bank $8F): Ice Beam Snake Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $C03A ; Custom door ASM to execute (bank $8F)
org $839366
; room A8B9: Ice Beam Snake Room
Room_A8B9_door_list_index_0_Door:
    dw $a75d ; Destination room header pointer (bank $8F): Ice Beam Acid Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839372
; room A8B9: Ice Beam Snake Room
Room_A8B9_door_list_index_1_Door:
    dw $a865 ; Destination room header pointer (bank $8F): Ice Beam Tutorial Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83937e
; room A8B9: Ice Beam Snake Room
Room_A8B9_door_list_index_2_Door:
    dw $a890 ; Destination room header pointer (bank $8F): Ice Beam Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83938a
; room A8F8: Crumble Shaft
Room_A8F8_door_list_index_0_Door:
    dw $a815 ; Destination room header pointer (bank $8F): Ice Beam Gate Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $36 ; Y cap
    db $06 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c0ef ; Custom door ASM to execute (bank $8F)
org $839396
; room A8F8: Crumble Shaft
Room_A8F8_door_list_index_1_Door:
    dw $a923 ; Destination room header pointer (bank $8F): Crocomire Speedway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $ce ; X cap
    db $06 ; Y cap
    db $0c ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8393a2
; room A923: Crocomire Speedway
Room_A923_door_list_index_0_Door:
    dw $a8f8 ; Destination room header pointer (bank $8F): Crumble Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8393ae
; room A923: Crocomire Speedway
Room_A923_door_list_index_1_Door:
    dw $aa0e ; Destination room header pointer (bank $8F): Crocomire Escape
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8393ba
; room A923: Crocomire Speedway
Room_A923_door_list_index_2_Door:
    dw $b192 ; Destination room header pointer (bank $8F): [Crocomire Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8393c6
; room A923: Crocomire Speedway
Room_A923_door_list_index_3_Door:
    dw $afce ; Destination room header pointer (bank $8F): Acid Snakes Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8393de
; room A98D: Crocomire's Room
Room_A98D_door_list_index_0_Door:
    dw $aa82 ; Destination room header pointer (bank $8F): Post Crocomire Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8393ea
; room A98D: Crocomire's Room
Room_A98D_door_list_index_1_Door:
    dw $a923 ; Destination room header pointer (bank $8F): Crocomire Speedway
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $06 ; X cap
    db $2d ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8393f6
; room A9E5: Hi Jump Boots Room
Room_A9E5_door_list_index_0_Door:
    dw $aa41 ; Destination room header pointer (bank $8F): Hi Jump Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c016 ; Custom door ASM to execute (bank $8F)
org $839402
; room AA0E: Crocomire Escape
Room_AA0E_door_list_index_0_Door:
    dw $a7de ; Destination room header pointer (bank $8F): Business Center
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $66 ; Y cap
    db $00 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83940e
; room AA0E: Crocomire Escape
Room_AA0E_door_list_index_1_Door:
    dw $a923 ; Destination room header pointer (bank $8F): Crocomire Speedway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83941a
; room AA41: Hi Jump Energy Tank Room
Room_AA41_door_list_index_0_Door:
    dw $a7de ; Destination room header pointer (bank $8F): Business Center
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $56 ; Y cap
    db $00 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839426
; room AA41: Hi Jump Energy Tank Room
Room_AA41_door_list_index_1_Door:
    dw $a9e5 ; Destination room header pointer (bank $8F): Hi Jump Boots Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839432
; room AA82: Post Crocomire Farming Room
Room_AA82_door_list_index_0_Door:
    dw $a98d ; Destination room header pointer (bank $8F): Crocomire's Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $06 ; Y cap
    db $07 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bfda ; Custom door ASM to execute (bank $8F)
org $83943e
; room AA82: Post Crocomire Farming Room
Room_AA82_door_list_index_1_Door:
    dw $aade ; Destination room header pointer (bank $8F): Post Crocomire Power Bomb Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839456
; room AA82: Post Crocomire Farming Room
Room_AA82_door_list_index_3_Door:
    dw $aab5 ; Destination room header pointer (bank $8F): [Post Crocomire Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839462
; room AAB5: [Post Crocomire Save Room]
Room_AAB5_door_list_index_0_Door:
    dw $aa82 ; Destination room header pointer (bank $8F): Post Crocomire Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83946e
; room AADE: Post Crocomire Power Bomb Room
Room_AADE_door_list_index_0_Door:
    dw $aa82 ; Destination room header pointer (bank $8F): Post Crocomire Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83947a
; room AB07: Post Crocomire Shaft
Room_AB07_door_list_index_0_Door:
    dw $aa82 ; Destination room header pointer (bank $8F): Post Crocomire Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $16 ; X cap
    db $1d ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839486
; room AB07: Post Crocomire Shaft
Room_AB07_door_list_index_1_Door:
    dw $ab64 ; Destination room header pointer (bank $8F): Grapple Tutorial Room 3
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839492
; room AB07: Post Crocomire Shaft
Room_AB07_door_list_index_2_Door:
    dw $ab3b ; Destination room header pointer (bank $8F): Post Crocomire Missile Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83949e
; room AB07: Post Crocomire Shaft
Room_AB07_door_list_index_3_Door:
    dw $ab8f ; Destination room header pointer (bank $8F): Post Crocomire Jump Room
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $16 ; X cap
    db $22 ; Y cap
    db $01 ; X screen
    db $02 ; Y screen
    dw $0140 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8394aa
; room AB3B: Post Crocomire Missile Room
Room_AB3B_door_list_index_0_Door:
    dw $ab07 ; Destination room header pointer (bank $8F): Post Crocomire Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8394b6
; room AB64: Grapple Tutorial Room 3
Room_AB64_door_list_index_0_Door:
    dw $abd2 ; Destination room header pointer (bank $8F): Grapple Tutorial Room 2
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8394c2
; room AB64: Grapple Tutorial Room 3
Room_AB64_door_list_index_1_Door:
    dw $ab07 ; Destination room header pointer (bank $8F): Post Crocomire Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8394da
; room AB8F: Post Crocomire Jump Room
Room_AB8F_door_list_index_1_Door:
    dw $ac2b ; Destination room header pointer (bank $8F): Grapple Beam Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8394e6
; room ABD2: Grapple Tutorial Room 2
Room_ABD2_door_list_index_0_Door:
    dw $ac00 ; Destination room header pointer (bank $8F): Grapple Tutorial Room 1
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8394f2
; room ABD2: Grapple Tutorial Room 2
Room_ABD2_door_list_index_1_Door:
    dw $ab64 ; Destination room header pointer (bank $8F): Grapple Tutorial Room 3
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8394fe
; room AC00: Grapple Tutorial Room 1
Room_AC00_door_list_index_0_Door:
    dw $ac2b ; Destination room header pointer (bank $8F): Grapple Beam Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83950a
; room AC00: Grapple Tutorial Room 1
Room_AC00_door_list_index_1_Door:
    dw $abd2 ; Destination room header pointer (bank $8F): Grapple Tutorial Room 2
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839516
; room AC2B: Grapple Beam Room
Room_AC2B_door_list_index_0_Door:
    dw $ab8f ; Destination room header pointer (bank $8F): Post Crocomire Jump Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $16 ; Y cap
    db $07 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839522
; room AC2B: Grapple Beam Room
Room_AC2B_door_list_index_1_Door:
    dw $ac00 ; Destination room header pointer (bank $8F): Grapple Tutorial Room 1
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83952e
; room AC5A: Norfair Reserve Tank Room
Room_AC5A_door_list_index_0_Door:
    dw $ac83 ; Destination room header pointer (bank $8F): Green Bubbles Missile Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c0d3 ; Custom door ASM to execute (bank $8F)
org $83953a
; room AC83: Green Bubbles Missile Room
Room_AC83_door_list_index_0_Door:
    dw $acb3 ; Destination room header pointer (bank $8F): Bubble Mountain
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839546
; room AC83: Green Bubbles Missile Room
Room_AC83_door_list_index_1_Door:
    dw $ac5a ; Destination room header pointer (bank $8F): Norfair Reserve Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839552
; room ACB3: Bubble Mountain
Room_ACB3_door_list_index_0_Door:
    dw $ac83 ; Destination room header pointer (bank $8F): Green Bubbles Missile Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83955e
; room ACB3: Bubble Mountain
Room_ACB3_door_list_index_1_Door:
    dw $afa3 ; Destination room header pointer (bank $8F): Rising Tide
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83956a
; room ACB3: Bubble Mountain
Room_ACB3_door_list_index_2_Door:
    dw $af72 ; Destination room header pointer (bank $8F): Upper Norfair Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839582
; room ACB3: Bubble Mountain
Room_ACB3_door_list_index_4_Door:
    dw $ad5e ; Destination room header pointer (bank $8F): Single Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83958e
; room ACB3: Bubble Mountain
Room_ACB3_door_list_index_5_Door:
    dw $b07a ; Destination room header pointer (bank $8F): Bat Cave
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83959a
; room ACB3: Bubble Mountain
Room_ACB3_door_list_index_6_Door:
    dw $b0dd ; Destination room header pointer (bank $8F): [Bubble Mountain Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8395a6
; room ACF0: Speed Booster Hall
Room_ACF0_door_list_index_0_Door:
    dw $b07a ; Destination room header pointer (bank $8F): Bat Cave
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bfe9 ; Custom door ASM to execute (bank $8F)
org $8395b2
; room ACF0: Speed Booster Hall
Room_ACF0_door_list_index_1_Door:
    dw $ad1b ; Destination room header pointer (bank $8F): Speed Booster Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8395be
; room AD1B: Speed Booster Room
Room_AD1B_door_list_index_0_Door:
    dw $acf0 ; Destination room header pointer (bank $8F): Speed Booster Hall
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8395ca
; room AD5E: Single Chamber
Room_AD5E_door_list_index_0_Door:
    dw $acb3 ; Destination room header pointer (bank $8F): Bubble Mountain
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8395d6
; room AD5E: Single Chamber
Room_AD5E_door_list_index_1_Door:
    dw $adad ; Destination room header pointer (bank $8F): Double Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8395e2
; room AD5E: Single Chamber
Room_AD5E_door_list_index_2_Door:
    dw $adad ; Destination room header pointer (bank $8F): Double Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $16 ; Y cap
    db $03 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8395ee
; room AD5E: Single Chamber
Room_AD5E_door_list_index_3_Door:
    dw $ae07 ; Destination room header pointer (bank $8F): Spiky Platforms Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8395fa
; room AD5E: Single Chamber
Room_AD5E_door_list_index_4_Door:
    dw $b656 ; Destination room header pointer (bank $8F): Three Muskateers' Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839606
; room ADAD: Double Chamber
Room_ADAD_door_list_index_0_Door:
    dw $ad5e ; Destination room header pointer (bank $8F): Single Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $51 ; X cap
    db $16 ; Y cap
    db $05 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839612
; room ADAD: Double Chamber
Room_ADAD_door_list_index_1_Door:
    dw $ad5e ; Destination room header pointer (bank $8F): Single Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $51 ; X cap
    db $26 ; Y cap
    db $05 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83961e
; room ADAD: Double Chamber
Room_ADAD_door_list_index_2_Door:
    dw $adde ; Destination room header pointer (bank $8F): Wave Beam Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83962a
; room ADDE: Wave Beam Room
Room_ADDE_door_list_index_0_Door:
    dw $adad ; Destination room header pointer (bank $8F): Double Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839636
; room AE07: Spiky Platforms Tunnel
Room_AE07_door_list_index_0_Door:
    dw $ad5e ; Destination room header pointer (bank $8F): Single Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $51 ; X cap
    db $36 ; Y cap
    db $05 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839642
; room AE07: Spiky Platforms Tunnel
Room_AE07_door_list_index_1_Door:
    dw $ae32 ; Destination room header pointer (bank $8F): Volcano Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83964e
; room AE32: Volcano Room
Room_AE32_door_list_index_0_Door:
    dw $ae07 ; Destination room header pointer (bank $8F): Spiky Platforms Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83965a
; room AE32: Volcano Room
Room_AE32_door_list_index_1_Door:
    dw $ae74 ; Destination room header pointer (bank $8F): Kronic Boost Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839666
; room AE74: Kronic Boost Room
Room_AE74_door_list_index_0_Door:
    dw $aeb4 ; Destination room header pointer (bank $8F): Magdollite Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839672
; room AE74: Kronic Boost Room
Room_AE74_door_list_index_1_Door:
    dw $ae32 ; Destination room header pointer (bank $8F): Volcano Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $26 ; Y cap
    db $02 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c025 ; Custom door ASM to execute (bank $8F)
org $83967e
; room AE74: Kronic Boost Room
Room_AE74_door_list_index_2_Door:
    dw $af14 ; Destination room header pointer (bank $8F): Lava Dive Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83968a
; room AE74: Kronic Boost Room
Room_AE74_door_list_index_3_Door:
    dw $affb ; Destination room header pointer (bank $8F): Spiky Acid Snakes Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839696
; room AEB4: Magdollite Tunnel
Room_AEB4_door_list_index_0_Door:
    dw $aedf ; Destination room header pointer (bank $8F): Purple Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396a2
; room AEB4: Magdollite Tunnel
Room_AEB4_door_list_index_1_Door:
    dw $ae74 ; Destination room header pointer (bank $8F): Kronic Boost Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396ae
; room AEDF: Purple Shaft
Room_AEDF_door_list_index_0_Door:
    dw $acb3 ; Destination room header pointer (bank $8F): Bubble Mountain
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $16 ; X cap
    db $3d ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396ba
; room AEDF: Purple Shaft
Room_AEDF_door_list_index_1_Door:
    dw $aeb4 ; Destination room header pointer (bank $8F): Magdollite Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396c6
; room AEDF: Purple Shaft
Room_AEDF_door_list_index_2_Door:
    dw $b051 ; Destination room header pointer (bank $8F): Purple Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396d2
; room AF14: Lava Dive Room
Room_AF14_door_list_index_0_Door:
    dw $ae74 ; Destination room header pointer (bank $8F): Kronic Boost Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396de
; room AF14: Lava Dive Room
Room_AF14_door_list_index_1_Door:
    dw $af3f ; Destination room header pointer (bank $8F): [Elevator to Lower Norfair]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396ea
; room AF3F: [Elevator to Lower Norfair]
Room_AF3F_door_list_index_0_Door:
    dw $af14 ; Destination room header pointer (bank $8F): Lava Dive Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8396f6
; room AF3F: [Elevator to Lower Norfair]
Room_AF3F_door_list_index_1_Door:
    dw $b236 ; Destination room header pointer (bank $8F): Main Hall
    db $a0 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $30 ; X cap
    db $00 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $0000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839702
; room AF3F: [Elevator to Lower Norfair]
Room_AF3F_door_list_index_3_Door:
    dw $b1bb ; Destination room header pointer (bank $8F): [Elevator Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83970e
; room AF72: Upper Norfair Farming Room
Room_AF72_door_list_index_0_Door:
    dw $b106 ; Destination room header pointer (bank $8F): Frog Speedway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83971a
; room AF72: Upper Norfair Farming Room
Room_AF72_door_list_index_1_Door:
    dw $acb3 ; Destination room header pointer (bank $8F): Bubble Mountain
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $36 ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839726
; room AF72: Upper Norfair Farming Room
Room_AF72_door_list_index_2_Door:
    dw $b139 ; Destination room header pointer (bank $8F): Red Pirate Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839732
; room AFA3: Rising Tide
Room_AFA3_door_list_index_0_Door:
    dw $a788 ; Destination room header pointer (bank $8F): Cathedral
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83973e
; room AFA3: Rising Tide
Room_AFA3_door_list_index_1_Door:
    dw $acb3 ; Destination room header pointer (bank $8F): Bubble Mountain
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $26 ; Y cap
    db $01 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83974a
; room AFCE: Acid Snakes Tunnel
Room_AFCE_door_list_index_0_Door:
    dw $a923 ; Destination room header pointer (bank $8F): Crocomire Speedway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839756
; room AFCE: Acid Snakes Tunnel
Room_AFCE_door_list_index_1_Door:
    dw $b026 ; Destination room header pointer (bank $8F): [Crocomire Recharge Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83976e
; room AFFB: Spiky Acid Snakes Tunnel
Room_AFFB_door_list_index_0_Door:
    dw $b026 ; Destination room header pointer (bank $8F): [Crocomire Recharge Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83977a
; room AFFB: Spiky Acid Snakes Tunnel
Room_AFFB_door_list_index_1_Door:
    dw $ae74 ; Destination room header pointer (bank $8F): Kronic Boost Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c0fa ; Custom door ASM to execute (bank $8F)
org $839786
; room B026: [Crocomire Recharge Room]
Room_B026_door_list_index_0_Door:
    dw $afce ; Destination room header pointer (bank $8F): Acid Snakes Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839792
; room B026: [Crocomire Recharge Room]
Room_B026_door_list_index_1_Door:
    dw $affb ; Destination room header pointer (bank $8F): Spiky Acid Snakes Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83979e
; room B051: Purple Farming Room
Room_B051_door_list_index_0_Door:
    dw $aedf ; Destination room header pointer (bank $8F): Purple Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397aa
; room B07A: Bat Cave
Room_B07A_door_list_index_0_Door:
    dw $acb3 ; Destination room header pointer (bank $8F): Bubble Mountain
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397b6
; room B07A: Bat Cave
Room_B07A_door_list_index_1_Door:
    dw $acf0 ; Destination room header pointer (bank $8F): Speed Booster Hall
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $be ; X cap
    db $06 ; Y cap
    db $0b ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397c2
; room B0B4: Norfair Map Room
Room_B0B4_door_list_index_0_Door:
    dw $a7de ; Destination room header pointer (bank $8F): Business Center
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $46 ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397ce
; room B0DD: [Bubble Mountain Save Room]
Room_B0DD_door_list_index_0_Door:
    dw $acb3 ; Destination room header pointer (bank $8F): Bubble Mountain
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397da
; room B106: Frog Speedway
Room_B106_door_list_index_0_Door:
    dw $b167 ; Destination room header pointer (bank $8F): [Business Center Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397e6
; room B106: Frog Speedway
Room_B106_door_list_index_1_Door:
    dw $af72 ; Destination room header pointer (bank $8F): Upper Norfair Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397f2
; room B139: Red Pirate Shaft
Room_B139_door_list_index_0_Door:
    dw $af72 ; Destination room header pointer (bank $8F): Upper Norfair Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8397fe
; room B139: Red Pirate Shaft
Room_B139_door_list_index_1_Door:
    dw $afce ; Destination room header pointer (bank $8F): Acid Snakes Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $06 ; X cap
    db $02 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $0140 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83980a
; room B167: [Business Center Save Room]
Room_B167_door_list_index_0_Door:
    dw $b106 ; Destination room header pointer (bank $8F): Frog Speedway
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $06 ; Y cap
    db $07 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839816
; room B167: [Business Center Save Room]
Room_B167_door_list_index_1_Door:
    dw $a7de ; Destination room header pointer (bank $8F): Business Center
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $56 ; Y cap
    db $00 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839822
; room B192: [Crocomire Save Room]
Room_B192_door_list_index_0_Door:
    dw $a923 ; Destination room header pointer (bank $8F): Crocomire Speedway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83982e
; room B1BB: [Elevator Save Room]
Room_B1BB_door_list_index_0_Door:
    dw $af3f ; Destination room header pointer (bank $8F): [Elevator to Lower Norfair]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83983a
; room B1E5: Acid Statue Room
Room_B1E5_door_list_index_0_Door:
    dw $b283 ; Destination room header pointer (bank $8F): Golden Torizo's Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $C089 ; Custom door ASM to execute (bank $8F)
org $839846
; room B1E5: Acid Statue Room
Room_B1E5_door_list_index_1_Door:
    dw $b236 ; Destination room header pointer (bank $8F): Main Hall
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $7e ; X cap
    db $26 ; Y cap
    db $07 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839852
; room B236: Main Hall
Room_B236_door_list_index_0_Door:
    dw $b1e5 ; Destination room header pointer (bank $8F): Acid Statue Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83985e
; room B236: Main Hall
Room_B236_door_list_index_1_Door:
    dw $b3a5 ; Destination room header pointer (bank $8F): Fast Pillars Setup Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839876
; room B283: Golden Torizo's Room
Room_B283_door_list_index_0_Door:
    dw $b1e5 ; Destination room header pointer (bank $8F): Acid Statue Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $bf9e ; Custom door ASM to execute (bank $8F)
org $839882
; room B283: Golden Torizo's Room
Room_B283_door_list_index_1_Door:
    dw $b6c1 ; Destination room header pointer (bank $8F): Screw Attack Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83988e
; room B2DA: Fast Ripper Room
Room_B2DA_door_list_index_0_Door:
    dw $b6c1 ; Destination room header pointer (bank $8F): Screw Attack Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83989a
; room B2DA: Fast Ripper Room
Room_B2DA_door_list_index_1_Door:
    dw $b3a5 ; Destination room header pointer (bank $8F): Fast Pillars Setup Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c056 ; Custom door ASM to execute (bank $8F)
org $8398a6
; room B305: [Screw Attack Energy Charge Room]
Room_B305_door_list_index_0_Door:
    dw $b6c1 ; Destination room header pointer (bank $8F): Screw Attack Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8398b2
; room B32E: Ridley's Room
Room_B32E_door_list_index_0_Door:
    dw $b698 ; Destination room header pointer (bank $8F): Ridley Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8398be
; room B32E: Ridley's Room
Room_B32E_door_list_index_1_Door:
    dw $b37a ; Destination room header pointer (bank $8F): Lower Norfair Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8398ca
; room B37A: Lower Norfair Farming Room
Room_B37A_door_list_index_0_Door:
    dw $b32e ; Destination room header pointer (bank $8F): Ridley's Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8398d6
; room B37A: Lower Norfair Farming Room
Room_B37A_door_list_index_1_Door:
    dw $b482 ; Destination room header pointer (bank $8F): Plowerhouse Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8398e2
; room B3A5: Fast Pillars Setup Room
Room_B3A5_door_list_index_0_Door:
    dw $b236 ; Destination room header pointer (bank $8F): Main Hall
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8398ee
; room B3A5: Fast Pillars Setup Room
Room_B3A5_door_list_index_1_Door:
    dw $b40a ; Destination room header pointer (bank $8F): Mickey Mouse Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $36 ; Y cap
    db $03 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839906
; room B3A5: Fast Pillars Setup Room
Room_B3A5_door_list_index_3_Door:
    dw $b2da ; Destination room header pointer (bank $8F): Fast Ripper Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839912
; room B3A5: Fast Pillars Setup Room
Room_B3A5_door_list_index_4_Door:
    dw $b457 ; Destination room header pointer (bank $8F): Pillar Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83992a
; room B40A: Mickey Mouse Room
Room_B40A_door_list_index_0_Door:
    dw $b3a5 ; Destination room header pointer (bank $8F): Fast Pillars Setup Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839936
; room B40A: Mickey Mouse Room
Room_B40A_door_list_index_1_Door:
    dw $b4ad ; Destination room header pointer (bank $8F): The Worst Room In The Game
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c0a2 ; Custom door ASM to execute (bank $8F)
org $839942
; room B457: Pillar Room
Room_B457_door_list_index_0_Door:
    dw $b3a5 ; Destination room header pointer (bank $8F): Fast Pillars Setup Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c056 ; Custom door ASM to execute (bank $8F)
org $83994e
; room B457: Pillar Room
Room_B457_door_list_index_1_Door:
    dw $b4ad ; Destination room header pointer (bank $8F): The Worst Room In The Game
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $56 ; Y cap
    db $00 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83995a
; room B482: Plowerhouse Room
Room_B482_door_list_index_0_Door:
    dw $b37a ; Destination room header pointer (bank $8F): Lower Norfair Farming Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839966
; room B482: Plowerhouse Room
Room_B482_door_list_index_1_Door:
    dw $b62b ; Destination room header pointer (bank $8F): Metal Pirates Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839972
; room B4AD: The Worst Room In The Game
Room_B4AD_door_list_index_0_Door:
    dw $b40a ; Destination room header pointer (bank $8F): Mickey Mouse Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $C10B ; Custom door ASM to execute (bank $8F)
org $83997e
; room B4AD: The Worst Room In The Game
Room_B4AD_door_list_index_1_Door:
    dw $b4e5 ; Destination room header pointer (bank $8F): Amphitheatre
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $16 ; Y cap
    db $03 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83998a
; room B4AD: The Worst Room In The Game
Room_B4AD_door_list_index_2_Door:
    dw $b457 ; Destination room header pointer (bank $8F): Pillar Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839996
; room B4E5: Amphitheatre
Room_B4E5_door_list_index_0_Door:
    dw $b4ad ; Destination room header pointer (bank $8F): The Worst Room In The Game
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8399a2
; room B4E5: Amphitheatre
Room_B4E5_door_list_index_1_Door:
    dw $b585 ; Destination room header pointer (bank $8F): Red Keyhunter Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $C067 ; Custom door ASM to execute (bank $8F)
org $8399ae
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_door_list_index_0_Door:
    dw $b656 ; Destination room header pointer (bank $8F): Three Muskateers' Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8399ba
; room B510: Lower Norfair Spring Ball Maze Room
Room_B510_door_list_index_1_Door:
    dw $b6ee ; Destination room header pointer (bank $8F): Lower Norfair Fireflea Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $C0AD ; Custom door ASM to execute (bank $8F)
org $8399d2
; room B55A: Lower Norfair Escape Power Bomb Room
Room_B55A_door_list_index_0_Door:
    dw $b6ee ; Destination room header pointer (bank $8F): Lower Norfair Fireflea Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c078 ; Custom door ASM to execute (bank $8F)
org $8399de
; room B55A: Lower Norfair Escape Power Bomb Room
Room_B55A_door_list_index_1_Door:
    dw $b510 ; Destination room header pointer (bank $8F): Lower Norfair Spring Ball Maze Room
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $06 ; X cap
    db $0d ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $bfbb ; Custom door ASM to execute (bank $8F)
org $8399ea
; room B585: Red Keyhunter Shaft
Room_B585_door_list_index_0_Door:
    dw $b5d5 ; Destination room header pointer (bank $8F): Wasteland
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $06 ; X cap
    db $02 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $8399f6
; room B585: Red Keyhunter Shaft
Room_B585_door_list_index_1_Door:
    dw $b4e5 ; Destination room header pointer (bank $8F): Amphitheatre
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a02
; room B585: Red Keyhunter Shaft
Room_B585_door_list_index_2_Door:
    dw $b6ee ; Destination room header pointer (bank $8F): Lower Norfair Fireflea Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $36 ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a0e
; room B585: Red Keyhunter Shaft
Room_B585_door_list_index_3_Door:
    dw $b741 ; Destination room header pointer (bank $8F): [Red Keyhunter Shaft Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a1a
; room B5D5: Wasteland
Room_B5D5_door_list_index_0_Door:
    dw $b62b ; Destination room header pointer (bank $8F): Metal Pirates Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a26
; room B5D5: Wasteland
Room_B5D5_door_list_index_1_Door:
    dw $b585 ; Destination room header pointer (bank $8F): Red Keyhunter Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $06 ; X cap
    db $4d ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $0200 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a32
; room B62B: Metal Pirates Room
Room_B62B_door_list_index_0_Door:
    dw $b482 ; Destination room header pointer (bank $8F): Plowerhouse Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a3e
; room B62B: Metal Pirates Room
Room_B62B_door_list_index_1_Door:
    dw $b5d5 ; Destination room header pointer (bank $8F): Wasteland
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $26 ; Y cap
    db $04 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $c04b ; Custom door ASM to execute (bank $8F)
org $839a4a
; room B656: Three Muskateers' Room
Room_B656_door_list_index_0_Door:
    dw $ad5e ; Destination room header pointer (bank $8F): Single Chamber
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a56
; room B656: Three Muskateers' Room
Room_B656_door_list_index_1_Door:
    dw $b510 ; Destination room header pointer (bank $8F): Lower Norfair Spring Ball Maze Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a62
; room B698: Ridley Tank Room
Room_B698_door_list_index_0_Door:
    dw $b32e ; Destination room header pointer (bank $8F): Ridley's Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a6e
; room B6C1: Screw Attack Room
Room_B6C1_door_list_index_0_Door:
    dw $b2da ; Destination room header pointer (bank $8F): Fast Ripper Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a7a
; room B6C1: Screw Attack Room
Room_B6C1_door_list_index_1_Door:
    dw $b305 ; Destination room header pointer (bank $8F): [Screw Attack Energy Charge Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a86
; room B6C1: Screw Attack Room
Room_B6C1_door_list_index_2_Door:
    dw $b283 ; Destination room header pointer (bank $8F): Golden Torizo's Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a92
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_door_list_index_0_Door:
    dw $b510 ; Destination room header pointer (bank $8F): Lower Norfair Spring Ball Maze Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $31 ; X cap
    db $16 ; Y cap
    db $03 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839a9e
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_door_list_index_1_Door:
    dw $b55a ; Destination room header pointer (bank $8F): Lower Norfair Escape Power Bomb Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $839aaa
; room B6EE: Lower Norfair Fireflea Room
Room_B6EE_door_list_index_2_Door:
    dw $b585 ; Destination room header pointer (bank $8F): Red Keyhunter Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $21 ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $C0C2 ; Custom door ASM to execute (bank $8F)
org $839ab6
; room B741: [Red Keyhunter Shaft Save Room]
Room_B741_door_list_index_0_Door:
    dw $b585 ; Destination room header pointer (bank $8F): Red Keyhunter Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $21 ; X cap
    db $36 ; Y cap
    db $02 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a014
; room DAE1: Metroid Room 1
Room_DAE1_state_DB0D_FX:
    dw $0000 ; Door pointer
    dw $00d0 ; Base Y position
    dw $ffff ; Target Y position
    dw $0000 ; Y velocity
    db $00 ; Timer
    db $04 ; Type (foreground layer 3)
    db $02 ; Default layer blending configuration (FX A)
    db $1e ; FX layer 3 layer blending configuration (FX B)
    db $01 ; FX liquid options (FX C)
    db $02 ; Palette FX bitset
    db $00 ; Animated tiles bitset
    db $02 ; Palette blend
org $83a034
; room DB7D: Metroid Room 3
Room_DB7D_state_DBA9_FX:
    dw $0000 ; Door pointer
    dw $00d0 ; Base Y position
    dw $ffff ; Target Y position
    dw $0000 ; Y velocity
    db $00 ; Timer
    db $04 ; Type (foreground layer 3)
    db $02 ; Default layer blending configuration (FX A)
    db $1e ; FX layer 3 layer blending configuration (FX B)
    db $01 ; FX liquid options (FX C)
    db $02 ; Palette FX bitset
    db $00 ; Animated tiles bitset
    db $02 ; Palette blend
org $83a0a4
; room DD58: Mother Brain Room
Room_DD58_state_DD88_FX:
    dw $0000 ; Door pointer
    dw $00e8 ; Base Y position
    dw $ffff ; Target Y position
    dw $0000 ; Y velocity
    db $00 ; Timer
    db $04 ; Type (foreground layer 3)
    db $02 ; Default layer blending configuration (FX A)
    db $1e ; FX layer 3 layer blending configuration (FX B)
    db $01 ; FX liquid options (FX C)
    db $02 ; Palette FX bitset
    db $00 ; Animated tiles bitset
    db $02 ; Palette blend
org $83a18c
; room C98E: Bowling Alley
Room_C98E_door_list_index_0_Door:
    dw $93fe ; Destination room header pointer (bank $8F): West Ocean
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a198
; room C98E: Bowling Alley
Room_C98E_door_list_index_1_Door:
    dw $968f ; Destination room header pointer (bank $8F): [West Ocean Geemer Corridor]
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1a4
; room C98E: Bowling Alley
Room_C98E_door_list_index_2_Door:
    dw $ce40 ; Destination room header pointer (bank $8F): Gravity Suit Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1b0
; room CA08: Wrecked Ship Entrance
Room_CA08_door_list_index_0_Door:
    dw $93fe ; Destination room header pointer (bank $8F): West Ocean
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $46 ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1bc
; room CA08: Wrecked Ship Entrance
Room_CA08_door_list_index_1_Door:
    dw $caf6 ; Destination room header pointer (bank $8F): Wrecked Ship Main Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $36 ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1c8
; room CA52: Attic
Room_CA52_door_list_index_0_Door:
    dw $caf6 ; Destination room header pointer (bank $8F): Wrecked Ship Main Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $16 ; X cap
    db $02 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1d4
; room CA52: Attic
Room_CA52_door_list_index_1_Door:
    dw $caae ; Destination room header pointer (bank $8F): Wrecked Ship East Missile Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1e0
; room CA52: Attic
Room_CA52_door_list_index_2_Door:
    dw $93fe ; Destination room header pointer (bank $8F): West Ocean
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1ec
; room CAAE: Wrecked Ship East Missile Room
Room_CAAE_door_list_index_0_Door:
    dw $ca52 ; Destination room header pointer (bank $8F): Attic
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a1f8
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_door_list_index_0_Door:
    dw $ca08 ; Destination room header pointer (bank $8F): Wrecked Ship Entrance
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e1d8 ; Custom door ASM to execute (bank $8F)
org $83a204
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_door_list_index_1_Door:
    dw $cd5c ; Destination room header pointer (bank $8F): Sponge Bath
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a210
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_door_list_index_2_Door:
    dw $cda8 ; Destination room header pointer (bank $8F): Wrecked Ship West Super Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a228
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_door_list_index_4_Door:
    dw $ca52 ; Destination room header pointer (bank $8F): Attic
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $26 ; X cap
    db $0e ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a234
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_door_list_index_5_Door:
    dw $cdf1 ; Destination room header pointer (bank $8F): Wrecked Ship East Super Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a240
; room CAF6: Wrecked Ship Main Shaft
Room_CAF6_door_list_index_6_Door:
    dw $ce8a ; Destination room header pointer (bank $8F): [Wrecked Ship Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a24c
; room CB8B: Spiky Death Room
Room_CB8B_door_list_index_0_Door:
    dw $cd5c ; Destination room header pointer (bank $8F): Sponge Bath
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e1e8 ; Custom door ASM to execute (bank $8F)
org $83a258
; room CB8B: Spiky Death Room
Room_CB8B_door_list_index_1_Door:
    dw $cbd5 ; Destination room header pointer (bank $8F): Electric Death Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a264
; room CBD5: Electric Death Room
Room_CBD5_door_list_index_0_Door:
    dw $94fd ; Destination room header pointer (bank $8F): East Ocean
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $46 ; Y cap
    db $06 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a270
; room CBD5: Electric Death Room
Room_CBD5_door_list_index_1_Door:
    dw $cb8b ; Destination room header pointer (bank $8F): Spiky Death Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a27c
; room CBD5: Electric Death Room
Room_CBD5_door_list_index_2_Door:
    dw $cc27 ; Destination room header pointer (bank $8F): Wrecked Ship Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a288
; room CC27: Wrecked Ship Energy Tank Room
Room_CC27_door_list_index_0_Door:
    dw $cbd5 ; Destination room header pointer (bank $8F): Electric Death Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e1f3 ; Custom door ASM to execute (bank $8F)
org $83a294
; room CC6F: Basement
Room_CC6F_door_list_index_0_Door:
    dw $caf6 ; Destination room header pointer (bank $8F): Wrecked Ship Main Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $16 ; X cap
    db $7d ; Y cap
    db $01 ; X screen
    db $07 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $e21a ; Custom door ASM to execute (bank $8F)
org $83a2a0
; room CC6F: Basement
Room_CC6F_door_list_index_1_Door:
    dw $cccb ; Destination room header pointer (bank $8F): Wrecked Ship Map Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a2ac
; room CC6F: Basement
Room_CC6F_door_list_index_2_Door:
    dw $cd13 ; Destination room header pointer (bank $8F): Phantoon's Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a2b8
; room CCCB: Wrecked Ship Map Room
Room_CCCB_door_list_index_0_Door:
    dw $cc6f ; Destination room header pointer (bank $8F): Basement
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a2c4
; room CD13: Phantoon's Room
Room_CD13_door_list_index_0_Door:
    dw $cc6f ; Destination room header pointer (bank $8F): Basement
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $E1FE ; Custom door ASM to execute (bank $8F)
org $83a2d0
; room CD5C: Sponge Bath
Room_CD5C_door_list_index_0_Door:
    dw $caf6 ; Destination room header pointer (bank $8F): Wrecked Ship Main Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $46 ; Y cap
    db $01 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a2dc
; room CD5C: Sponge Bath
Room_CD5C_door_list_index_1_Door:
    dw $cb8b ; Destination room header pointer (bank $8F): Spiky Death Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a2e8
; room CDA8: Wrecked Ship West Super Room
Room_CDA8_door_list_index_0_Door:
    dw $caf6 ; Destination room header pointer (bank $8F): Wrecked Ship Main Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $66 ; Y cap
    db $01 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a2f4
; room CDF1: Wrecked Ship East Super Room
Room_CDF1_door_list_index_0_Door:
    dw $caf6 ; Destination room header pointer (bank $8F): Wrecked Ship Main Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $66 ; Y cap
    db $00 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e20f ; Custom door ASM to execute (bank $8F)
org $83a300
; room CE40: Gravity Suit Room
Room_CE40_door_list_index_0_Door:
    dw $93fe ; Destination room header pointer (bank $8F): West Ocean
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $21 ; X cap
    db $36 ; Y cap
    db $02 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a30c
; room CE40: Gravity Suit Room
Room_CE40_door_list_index_1_Door:
    dw $c98e ; Destination room header pointer (bank $8F): Bowling Alley
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $26 ; Y cap
    db $04 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e229 ; Custom door ASM to execute (bank $8F)
org $83a318
; room CE8A: [Wrecked Ship Save Room]
Room_CE8A_door_list_index_0_Door:
    dw $caf6 ; Destination room header pointer (bank $8F): Wrecked Ship Main Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $36 ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a324
; room CED2: [Glass Tunnel Save Room]
Room_CED2_door_list_index_0_Door:
    dw $cefb ; Destination room header pointer (bank $8F): Glass Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a33c
; room CEFB: Glass Tunnel
Room_CEFB_door_list_index_1_Door:
    dw $cf54 ; Destination room header pointer (bank $8F): West Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a348
; room CEFB: Glass Tunnel
Room_CEFB_door_list_index_2_Door:
    dw $cf80 ; Destination room header pointer (bank $8F): East Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $16 ; Y cap
    db $03 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e345 ; Custom door ASM to execute (bank $8F)
org $83a354
; room CEFB: Glass Tunnel
Room_CEFB_door_list_index_3_Door:
    dw $ced2 ; Destination room header pointer (bank $8F): [Glass Tunnel Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a360
; room CF54: West Tunnel
Room_CF54_door_list_index_0_Door:
    dw $cefb ; Destination room header pointer (bank $8F): Glass Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e378 ; Custom door ASM to execute (bank $8F)
org $83a36c
; room CF54: West Tunnel
Room_CF54_door_list_index_1_Door:
    dw $a408 ; Destination room header pointer (bank $8F): Below Spazer
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a378
; room CF80: East Tunnel
Room_CF80_door_list_index_0_Door:
    dw $cefb ; Destination room header pointer (bank $8F): Glass Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e378 ; Custom door ASM to execute (bank $8F)
org $83a384
; room CF80: East Tunnel
Room_CF80_door_list_index_1_Door:
    dw $a6a1 ; Destination room header pointer (bank $8F): Warehouse Entrance
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a390
; room CF80: East Tunnel
Room_CF80_door_list_index_2_Door:
    dw $d21c ; Destination room header pointer (bank $8F): Crab Hole
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e356 ; Custom door ASM to execute (bank $8F)
org $83a3a8
; room CFC9: Main Street
Room_CFC9_door_list_index_1_Door:
    dw $d08a ; Destination room header pointer (bank $8F): Crab Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a3b4
; room CFC9: Main Street
Room_CFC9_door_list_index_2_Door:
    dw $d017 ; Destination room header pointer (bank $8F): Fish Tank
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $26 ; Y cap
    db $03 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a3c0
; room CFC9: Main Street
Room_CFC9_door_list_index_3_Door:
    dw $d0b9 ; Destination room header pointer (bank $8F): Mt. Everest
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a3cc
; room CFC9: Main Street
Room_CFC9_door_list_index_4_Door:
    dw $d0b9 ; Destination room header pointer (bank $8F): Mt. Everest
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $4e ; X cap
    db $26 ; Y cap
    db $04 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a3d8
; room D017: Fish Tank
Room_D017_door_list_index_0_Door:
    dw $cfc9 ; Destination room header pointer (bank $8F): Main Street
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $66 ; Y cap
    db $00 ; X screen
    db $06 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a3e4
; room D017: Fish Tank
Room_D017_door_list_index_1_Door:
    dw $d055 ; Destination room header pointer (bank $8F): Mama Turtle Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $36 ; Y cap
    db $02 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a3f0
; room D017: Fish Tank
Room_D017_door_list_index_2_Door:
    dw $d0b9 ; Destination room header pointer (bank $8F): Mt. Everest
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $46 ; X cap
    db $3d ; Y cap
    db $04 ; X screen
    db $03 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a3fc
; room D017: Fish Tank
Room_D017_door_list_index_3_Door:
    dw $d0b9 ; Destination room header pointer (bank $8F): Mt. Everest
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $16 ; X cap
    db $3d ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a408
; room D055: Mama Turtle Room
Room_D055_door_list_index_0_Door:
    dw $d017 ; Destination room header pointer (bank $8F): Fish Tank
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a414
; room D08A: Crab Tunnel
Room_D08A_door_list_index_0_Door:
    dw $cfc9 ; Destination room header pointer (bank $8F): Main Street
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $76 ; Y cap
    db $01 ; X screen
    db $07 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a420
; room D08A: Crab Tunnel
Room_D08A_door_list_index_1_Door:
    dw $d21c ; Destination room header pointer (bank $8F): Crab Hole
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a42c
; room D0B9: Mt. Everest
Room_D0B9_door_list_index_0_Door:
    dw $d104 ; Destination room header pointer (bank $8F): Red Fish Room
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $06 ; X cap
    db $1d ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a438
; room D0B9: Mt. Everest
Room_D0B9_door_list_index_1_Door:
    dw $cfc9 ; Destination room header pointer (bank $8F): Main Street
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a444
; room D0B9: Mt. Everest
Room_D0B9_door_list_index_2_Door:
    dw $d017 ; Destination room header pointer (bank $8F): Fish Tank
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $36 ; X cap
    db $02 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a450
; room D0B9: Mt. Everest
Room_D0B9_door_list_index_3_Door:
    dw $d017 ; Destination room header pointer (bank $8F): Fish Tank
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $06 ; X cap
    db $02 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a45c
; room D0B9: Mt. Everest
Room_D0B9_door_list_index_4_Door:
    dw $cfc9 ; Destination room header pointer (bank $8F): Main Street
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a468
; room D0B9: Mt. Everest
Room_D0B9_door_list_index_5_Door:
    dw $d1a3 ; Destination room header pointer (bank $8F): Crab Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $26 ; Y cap
    db $01 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a474
; room D104: Red Fish Room
Room_D104_door_list_index_0_Door:
    dw $d0b9 ; Destination room header pointer (bank $8F): Mt. Everest
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $36 ; X cap
    db $02 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a480
; room D104: Red Fish Room
Room_D104_door_list_index_1_Door:
    dw $a322 ; Destination room header pointer (bank $8F): Caterpillar Room
    db $40 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $E367 ; Custom door ASM to execute (bank $8F)
org $83a48c
; room D13B: Watering Hole
Room_D13B_door_list_index_0_Door:
    dw $d16d ; Destination room header pointer (bank $8F): Northwest Maridia Bug Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a498
; room D16D: Northwest Maridia Bug Room
Room_D16D_door_list_index_0_Door:
    dw $d13b ; Destination room header pointer (bank $8F): Watering Hole
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a4a4
; room D16D: Northwest Maridia Bug Room
Room_D16D_door_list_index_1_Door:
    dw $d1dd ; Destination room header pointer (bank $8F): Pseudo Plasma Spark Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $16 ; Y cap
    db $03 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a4b0
; room D1A3: Crab Shaft
Room_D1A3_door_list_index_0_Door:
    dw $d0b9 ; Destination room header pointer (bank $8F): Mt. Everest
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a4bc
; room D1A3: Crab Shaft
Room_D1A3_door_list_index_1_Door:
    dw $d1dd ; Destination room header pointer (bank $8F): Pseudo Plasma Spark Room
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $36 ; X cap
    db $2d ; Y cap
    db $03 ; X screen
    db $02 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a4c8
; room D1A3: Crab Shaft
Room_D1A3_door_list_index_2_Door:
    dw $d5a7 ; Destination room header pointer (bank $8F): Aqueduct
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $16 ; Y cap
    db $05 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a4d4
; room D1DD: Pseudo Plasma Spark Room
Room_D1DD_door_list_index_0_Door:
    dw $d16d ; Destination room header pointer (bank $8F): Northwest Maridia Bug Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a4e0
; room D1DD: Pseudo Plasma Spark Room
Room_D1DD_door_list_index_1_Door:
    dw $d1a3 ; Destination room header pointer (bank $8F): Crab Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $16 ; X cap
    db $02 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a4f8
; room D21C: Crab Hole
Room_D21C_door_list_index_0_Door:
    dw $d08a ; Destination room header pointer (bank $8F): Crab Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a504
; room D21C: Crab Hole
Room_D21C_door_list_index_1_Door:
    dw $d252 ; Destination room header pointer (bank $8F): [Tunnel to West Sand Hall]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a510
; room D21C: Crab Hole
Room_D21C_door_list_index_2_Door:
    dw $cf80 ; Destination room header pointer (bank $8F): East Tunnel
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a51c
; room D21C: Crab Hole
Room_D21C_door_list_index_3_Door:
    dw $d3b6 ; Destination room header pointer (bank $8F): Maridia Map Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a528
; room D252: [Tunnel to West Sand Hall]
Room_D252_door_list_index_0_Door:
    dw $d21c ; Destination room header pointer (bank $8F): Crab Hole
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a534
; room D252: [Tunnel to West Sand Hall]
Room_D252_door_list_index_1_Door:
    dw $d461 ; Destination room header pointer (bank $8F): West Sand Hall
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a540
; room D27E: Plasma Tutorial Room
Room_D27E_door_list_index_0_Door:
    dw $d387 ; Destination room header pointer (bank $8F): Plasma Climb
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a54c
; room D27E: Plasma Tutorial Room
Room_D27E_door_list_index_1_Door:
    dw $d2aa ; Destination room header pointer (bank $8F): Plasma Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a558
; room D2AA: Plasma Room
Room_D2AA_door_list_index_0_Door:
    dw $d27e ; Destination room header pointer (bank $8F): Plasma Tutorial Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a564
; room D2D9: Thread The Needle Room
Room_D2D9_door_list_index_0_Door:
    dw $d433 ; Destination room header pointer (bank $8F): Bug Sand Hole
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a570
; room D2D9: Thread The Needle Room
Room_D2D9_door_list_index_1_Door:
    dw $d30b ; Destination room header pointer (bank $8F): Maridia Elevator Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $56 ; Y cap
    db $00 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a57c
; room D30B: Maridia Elevator Room
Room_D30B_door_list_index_0_Door:
    dw $d2d9 ; Destination room header pointer (bank $8F): Thread The Needle Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a588
; room D30B: Maridia Elevator Room
Room_D30B_door_list_index_1_Door:
    dw $d3df ; Destination room header pointer (bank $8F): [Maridia Elevator Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a5a0
; room D340: Plasma Spark Room
Room_D340_door_list_index_0_Door:
    dw $d5ec ; Destination room header pointer (bank $8F): Butterfly Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a5b8
; room D340: Plasma Spark Room
Room_D340_door_list_index_2_Door:
    dw $d387 ; Destination room header pointer (bank $8F): Plasma Climb
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a5c4
; room D340: Plasma Spark Room
Room_D340_door_list_index_3_Door:
    dw $d433 ; Destination room header pointer (bank $8F): Bug Sand Hole
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a5d0
; room D387: Plasma Climb
Room_D387_door_list_index_0_Door:
    dw $d340 ; Destination room header pointer (bank $8F): Plasma Spark Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a5dc
; room D387: Plasma Climb
Room_D387_door_list_index_1_Door:
    dw $d27e ; Destination room header pointer (bank $8F): Plasma Tutorial Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a5e8
; room D3B6: Maridia Map Room
Room_D3B6_door_list_index_0_Door:
    dw $d21c ; Destination room header pointer (bank $8F): Crab Hole
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e356 ; Custom door ASM to execute (bank $8F)
org $83a5f4
; room D3DF: [Maridia Elevator Save Room]
Room_D3DF_door_list_index_0_Door:
    dw $d30b ; Destination room header pointer (bank $8F): Maridia Elevator Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $46 ; Y cap
    db $00 ; X screen
    db $04 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a60c
; room D408: [Vertical Tube]
Room_D408_door_list_index_1_Door:
    dw $d340 ; Destination room header pointer (bank $8F): Plasma Spark Room
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $36 ; X cap
    db $2d ; Y cap
    db $03 ; X screen
    db $02 ; Y screen
    dw $0200 ; Distance from door to spawn Samus
    dw $e301 ; Custom door ASM to execute (bank $8F)
org $83a618
; room D433: Bug Sand Hole
Room_D433_door_list_index_0_Door:
    dw $d2d9 ; Destination room header pointer (bank $8F): Thread The Needle Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $06 ; Y cap
    db $06 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a630
; room D433: Bug Sand Hole
Room_D433_door_list_index_2_Door:
    dw $d340 ; Destination room header pointer (bank $8F): Plasma Spark Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a63c
; room D461: West Sand Hall
Room_D461_door_list_index_0_Door:
    dw $d252 ; Destination room header pointer (bank $8F): [Tunnel to West Sand Hall]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a648
; room D461: West Sand Hall
Room_D461_door_list_index_1_Door:
    dw $d48e ; Destination room header pointer (bank $8F): Oasis
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a660
; room D48E: Oasis
Room_D48E_door_list_index_0_Door:
    dw $d461 ; Destination room header pointer (bank $8F): West Sand Hall
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a66c
; room D48E: Oasis
Room_D48E_door_list_index_1_Door:
    dw $d4c2 ; Destination room header pointer (bank $8F): East Sand Hall
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a684
; room D4C2: East Sand Hall
Room_D4C2_door_list_index_0_Door:
    dw $d48e ; Destination room header pointer (bank $8F): Oasis
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a690
; room D4C2: East Sand Hall
Room_D4C2_door_list_index_1_Door:
    dw $d646 ; Destination room header pointer (bank $8F): Pants Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $36 ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e3a3 ; Custom door ASM to execute (bank $8F)
org $83a6b4
; room D4EF: West Sand Hole
Room_D4EF_door_list_index_1_Door:
    dw $d461 ; Destination room header pointer (bank $8F): West Sand Hall
    db $00 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $10 ; X cap
    db $00 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a6e4
; room D54D: [West Sand Fall]
Room_D54D_door_list_index_1_Door:
    dw $d4ef ; Destination room header pointer (bank $8F): West Sand Hole
    db $00 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $00 ; X cap
    db $00 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a6fc
; room D57A: [East Sand Fall]
Room_D57A_door_list_index_1_Door:
    dw $d51e ; Destination room header pointer (bank $8F): East Sand Hole
    db $00 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $10 ; X cap
    db $00 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a708
; room D5A7: Aqueduct
Room_D5A7_door_list_index_0_Door:
    dw $d1a3 ; Destination room header pointer (bank $8F): Crab Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e398 ; Custom door ASM to execute (bank $8F)
org $83a72c
; room D5A7: Aqueduct
Room_D5A7_door_list_index_3_Door:
    dw $d617 ; Destination room header pointer (bank $8F): Botwoon Hallway
    db $00 ; Bit Flag (Elevator properties)
    db $07 ; Direction
    db $36 ; X cap
    db $0d ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $01c0 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a738
; room D5A7: Aqueduct
Room_D5A7_door_list_index_4_Door:
    dw $d6fd ; Destination room header pointer (bank $8F): Below Botwoon Energy Tank
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a744
; room D5A7: Aqueduct
Room_D5A7_door_list_index_5_Door:
    dw $d765 ; Destination room header pointer (bank $8F): [Aqueduct Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a750
; room D5EC: Butterfly Room
Room_D5EC_door_list_index_0_Door:
    dw $d340 ; Destination room header pointer (bank $8F): Plasma Spark Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $56 ; Y cap
    db $00 ; X screen
    db $05 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a75c
; room D5EC: Butterfly Room
Room_D5EC_door_list_index_1_Door:
    dw $d9fe ; Destination room header pointer (bank $8F): Cactus Alley [West]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a768
; room D617: Botwoon Hallway
Room_D617_door_list_index_0_Door:
    dw $d5a7 ; Destination room header pointer (bank $8F): Aqueduct
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $56 ; X cap
    db $02 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a774
; room D617: Botwoon Hallway
Room_D617_door_list_index_1_Door:
    dw $d95e ; Destination room header pointer (bank $8F): Botwoon's Room
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a780
; room D646: Pants Room
Room_D646_door_list_index_0_Door:
    dw $d4c2 ; Destination room header pointer (bank $8F): East Sand Hall
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a78c
; room D646: Pants Room
Room_D646_door_list_index_1_Door:
    dw $d69a ; Destination room header pointer (bank $8F): [Pants Room West half]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a798
; room D646: Pants Room
Room_D646_door_list_index_2_Door:
    dw $d8c5 ; Destination room header pointer (bank $8F): Shaktool Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a7a4
; room D646: Pants Room
Room_D646_door_list_index_3_Door:
    dw $d646 ; Destination room header pointer (bank $8F): Pants Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $36 ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $E3B9 ; Custom door ASM to execute (bank $8F)
org $83a7b0
; room D69A: [Pants Room West half]
Room_D69A_door_list_index_0_Door:
    dw $d646 ; Destination room header pointer (bank $8F): Pants Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $11 ; X cap
    db $36 ; Y cap
    db $01 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e3a3 ; Custom door ASM to execute (bank $8F)
org $83a7bc
; room D69A: [Pants Room West half]
Room_D69A_door_list_index_1_Door:
    dw $d8c5 ; Destination room header pointer (bank $8F): Shaktool Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a7c8
; room D6D0: Spring Ball Room
Room_D6D0_door_list_index_0_Door:
    dw $d8c5 ; Destination room header pointer (bank $8F): Shaktool Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a7d4
; room D6FD: Below Botwoon Energy Tank
Room_D6FD_door_list_index_0_Door:
    dw $d5a7 ; Destination room header pointer (bank $8F): Aqueduct
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a7e0
; room D72A: Colosseum
Room_D72A_door_list_index_0_Door:
    dw $d913 ; Destination room header pointer (bank $8F): Halfie Climb Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $41 ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a7ec
; room D72A: Colosseum
Room_D72A_door_list_index_1_Door:
    dw $d81a ; Destination room header pointer (bank $8F): [Colosseum Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a7f8
; room D72A: Colosseum
Room_D72A_door_list_index_2_Door:
    dw $d78f ; Destination room header pointer (bank $8F): The Precious Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a828
; room D765: [Aqueduct Save Room]
Room_D765_door_list_index_0_Door:
    dw $d5a7 ; Destination room header pointer (bank $8F): Aqueduct
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $26 ; Y cap
    db $05 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a834
; room D78F: The Precious Room
Room_D78F_door_list_index_0_Door:
    dw $d72a ; Destination room header pointer (bank $8F): Colosseum
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a840
; room D78F: The Precious Room
Room_D78F_door_list_index_1_Door:
    dw $da60 ; Destination room header pointer (bank $8F): Draygon's Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a84c
; room D7E4: Botwoon Energy Tank Room
Room_D7E4_door_list_index_0_Door:
    dw $d95e ; Destination room header pointer (bank $8F): Botwoon's Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e38d ; Custom door ASM to execute (bank $8F)
org $83a858
; room D7E4: Botwoon Energy Tank Room
Room_D7E4_door_list_index_1_Door:
    dw $d898 ; Destination room header pointer (bank $8F): [Botwoon Sand Fall]
    db $00 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $00 ; X cap
    db $00 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a864
; room D7E4: Botwoon Energy Tank Room
Room_D7E4_door_list_index_2_Door:
    dw $d898 ; Destination room header pointer (bank $8F): [Botwoon Sand Fall]
    db $00 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $10 ; X cap
    db $00 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a870
; room D7E4: Botwoon Energy Tank Room
Room_D7E4_door_list_index_3_Door:
    dw $d913 ; Destination room header pointer (bank $8F): Halfie Climb Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $26 ; Y cap
    db $04 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a87c
; room D81A: [Colosseum Save Room]
Room_D81A_door_list_index_0_Door:
    dw $d9d4 ; Destination room header pointer (bank $8F): [Colosseum Energy Charge Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a888
; room D81A: [Colosseum Save Room]
Room_D81A_door_list_index_1_Door:
    dw $d72a ; Destination room header pointer (bank $8F): Colosseum
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a894
; room D845: [Halfie Climb Missile Station]
Room_D845_door_list_index_0_Door:
    dw $d913 ; Destination room header pointer (bank $8F): Halfie Climb Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $E318 ; Custom door ASM to execute (bank $8F)
org $83a8ac
; room D898: [Botwoon Sand Fall]
Room_D898_door_list_index_0_Door:
    dw $d6fd ; Destination room header pointer (bank $8F): Below Botwoon Energy Tank
    db $00 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $10 ; X cap
    db $00 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a8b8
; room D898: [Botwoon Sand Fall]
Room_D898_door_list_index_1_Door:
    dw $d6fd ; Destination room header pointer (bank $8F): Below Botwoon Energy Tank
    db $00 ; Bit Flag (Elevator properties)
    db $02 ; Direction
    db $00 ; X cap
    db $00 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a8c4
; room D8C5: Shaktool Room
Room_D8C5_door_list_index_0_Door:
    dw $d69a ; Destination room header pointer (bank $8F): [Pants Room West half]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e3c8 ; Custom door ASM to execute (bank $8F)
org $83a8d0
; room D8C5: Shaktool Room
Room_D8C5_door_list_index_1_Door:
    dw $d6d0 ; Destination room header pointer (bank $8F): Spring Ball Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a8dc
; room D913: Halfie Climb Room
Room_D913_door_list_index_0_Door:
    dw $d7e4 ; Destination room header pointer (bank $8F): Botwoon Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a8e8
; room D913: Halfie Climb Room
Room_D913_door_list_index_1_Door:
    dw $d72a ; Destination room header pointer (bank $8F): Colosseum
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $06 ; Y cap
    db $06 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a8f4
; room D913: Halfie Climb Room
Room_D913_door_list_index_2_Door:
    dw $d845 ; Destination room header pointer (bank $8F): [Halfie Climb Missile Station]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a900
; room D913: Halfie Climb Room
Room_D913_door_list_index_3_Door:
    dw $da2b ; Destination room header pointer (bank $8F): Cactus Alley [East]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a90c
; room D95E: Botwoon's Room
Room_D95E_door_list_index_0_Door:
    dw $d617 ; Destination room header pointer (bank $8F): Botwoon Hallway
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a918
; room D95E: Botwoon's Room
Room_D95E_door_list_index_1_Door:
    dw $d7e4 ; Destination room header pointer (bank $8F): Botwoon Energy Tank Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $6e ; X cap
    db $06 ; Y cap
    db $06 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a924
; room D9AA: Space Jump Room
Room_D9AA_door_list_index_0_Door:
    dw $da60 ; Destination room header pointer (bank $8F): Draygon's Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $16 ; Y cap
    db $01 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a930
; room D9D4: [Colosseum Energy Charge Room]
Room_D9D4_door_list_index_0_Door:
    dw $d81a ; Destination room header pointer (bank $8F): [Colosseum Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a93c
; room D9FE: Cactus Alley [West]
Room_D9FE_door_list_index_0_Door:
    dw $d5ec ; Destination room header pointer (bank $8F): Butterfly Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a948
; room D9FE: Cactus Alley [West]
Room_D9FE_door_list_index_1_Door:
    dw $da2b ; Destination room header pointer (bank $8F): Cactus Alley [East]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $06 ; Y cap
    db $04 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a954
; room DA2B: Cactus Alley [East]
Room_DA2B_door_list_index_0_Door:
    dw $d9fe ; Destination room header pointer (bank $8F): Cactus Alley [West]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a960
; room DA2B: Cactus Alley [East]
Room_DA2B_door_list_index_1_Door:
    dw $d913 ; Destination room header pointer (bank $8F): Halfie Climb Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $4e ; X cap
    db $16 ; Y cap
    db $04 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a96c
; room DA60: Draygon's Room
Room_DA60_door_list_index_0_Door:
    dw $d78f ; Destination room header pointer (bank $8F): The Precious Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $26 ; Y cap
    db $01 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $E3D9 ; Custom door ASM to execute (bank $8F)
org $83a978
; room DA60: Draygon's Room
Room_DA60_door_list_index_1_Door:
    dw $d9aa ; Destination room header pointer (bank $8F): Space Jump Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a984
; room DAAE: Tourian First Room
Room_DAAE_door_list_index_0_Door:
    dw $dae1 ; Destination room header pointer (bank $8F): Metroid Room 1
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a99c
; room DAAE: Tourian First Room
Room_DAAE_door_list_index_3_Door:
    dw $df1b ; Destination room header pointer (bank $8F): [Tourian First Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9a8
; room DAE1: Metroid Room 1
Room_DAE1_door_list_index_0_Door:
    dw $daae ; Destination room header pointer (bank $8F): Tourian First Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9b4
; room DAE1: Metroid Room 1
Room_DAE1_door_list_index_1_Door:
    dw $db31 ; Destination room header pointer (bank $8F): Metroid Room 2
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9c0
; room DB31: Metroid Room 2
Room_DB31_door_list_index_0_Door:
    dw $dae1 ; Destination room header pointer (bank $8F): Metroid Room 1
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9cc
; room DB31: Metroid Room 2
Room_DB31_door_list_index_1_Door:
    dw $db7d ; Destination room header pointer (bank $8F): Metroid Room 3
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9d8
; room DB7D: Metroid Room 3
Room_DB7D_door_list_index_0_Door:
    dw $db31 ; Destination room header pointer (bank $8F): Metroid Room 2
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9e4
; room DB7D: Metroid Room 3
Room_DB7D_door_list_index_1_Door:
    dw $dbcd ; Destination room header pointer (bank $8F): Metroid Room 4
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9f0
; room DBCD: Metroid Room 4
Room_DBCD_door_list_index_0_Door:
    dw $db7d ; Destination room header pointer (bank $8F): Metroid Room 3
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83a9fc
; room DBCD: Metroid Room 4
Room_DBCD_door_list_index_1_Door:
    dw $dc19 ; Destination room header pointer (bank $8F): Blue Hopper Room
    db $00 ; Bit Flag (Elevator properties)
    db $06 ; Direction
    db $06 ; X cap
    db $03 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa14
; room DC19: Blue Hopper Room
Room_DC19_door_list_index_1_Door:
    dw $dc65 ; Destination room header pointer (bank $8F): Dust Torizo Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa20
; room DC65: Dust Torizo Room
Room_DC65_door_list_index_0_Door:
    dw $dc19 ; Destination room header pointer (bank $8F): Blue Hopper Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa2c
; room DC65: Dust Torizo Room
Room_DC65_door_list_index_1_Door:
    dw $dcb1 ; Destination room header pointer (bank $8F): Big Boy Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $21 ; X cap
    db $06 ; Y cap
    db $02 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa38
; room DCB1: Big Boy Room
Room_DCB1_door_list_index_0_Door:
    dw $dc65 ; Destination room header pointer (bank $8F): Dust Torizo Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa44
; room DCB1: Big Boy Room
Room_DCB1_door_list_index_1_Door:
    dw $dcff ; Destination room header pointer (bank $8F): Seaweed Room
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $02 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa50
; room DCFF: Seaweed Room
Room_DCFF_door_list_index_0_Door:
    dw $dcb1 ; Destination room header pointer (bank $8F): Big Boy Room
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $5e ; X cap
    db $06 ; Y cap
    db $05 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa5c
; room DCFF: Seaweed Room
Room_DCFF_door_list_index_1_Door:
    dw $ddc4 ; Destination room header pointer (bank $8F): Tourian Eye Door Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $3e ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa68
; room DCFF: Seaweed Room
Room_DCFF_door_list_index_2_Door:
    dw $dd2e ; Destination room header pointer (bank $8F): Tourian Recharge Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa74
; room DD2E: Tourian Recharge Room
Room_DD2E_door_list_index_0_Door:
    dw $dcff ; Destination room header pointer (bank $8F): Seaweed Room
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa80
; room DD58: Mother Brain Room
Room_DD58_door_list_index_0_Door:
    dw $ddf3 ; Destination room header pointer (bank $8F): Rinka Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa8c
; room DD58: Mother Brain Room
Room_DD58_door_list_index_1_Door:
    dw $de4d ; Destination room header pointer (bank $8F): Tourian Escape Room 1
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $02 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aa98
; room DDC4: Tourian Eye Door Room
Room_DDC4_door_list_index_0_Door:
    dw $dcff ; Destination room header pointer (bank $8F): Seaweed Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aaa4
; room DDC4: Tourian Eye Door Room
Room_DDC4_door_list_index_1_Door:
    dw $ddf3 ; Destination room header pointer (bank $8F): Rinka Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aab0
; room DDF3: Rinka Shaft
Room_DDF3_door_list_index_0_Door:
    dw $ddc4 ; Destination room header pointer (bank $8F): Tourian Eye Door Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aabc
; room DDF3: Rinka Shaft
Room_DDF3_door_list_index_1_Door:
    dw $de23 ; Destination room header pointer (bank $8F): [Mother Brain Save Room]
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aac8
; room DDF3: Rinka Shaft
Room_DDF3_door_list_index_2_Door:
    dw $dd58 ; Destination room header pointer (bank $8F): Mother Brain Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aad4
; room DE23: [Mother Brain Save Room]
Room_DE23_door_list_index_0_Door:
    dw $ddf3 ; Destination room header pointer (bank $8F): Rinka Shaft
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $0e ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83AAE0
; Room $DE4D, door list index 0: Door
    dw $DD58 ; Destination room header pointer (bank $8F):  Mother Brain Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $3E ; X cap
    db $06 ; Y cap
    db $03 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab04
; room DE7A: Tourian Escape Room 2
Room_DE7A_door_list_index_1_Door:
    dw $dea7 ; Destination room header pointer (bank $8F): Tourian Escape Room 3
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $5e ; X cap
    db $16 ; Y cap
    db $05 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab10
; room DEA7: Tourian Escape Room 3
Room_DEA7_door_list_index_0_Door:
    dw $de7a ; Destination room header pointer (bank $8F): Tourian Escape Room 2
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab1c
; room DEA7: Tourian Escape Room 3
Room_DEA7_door_list_index_1_Door:
    dw $dede ; Destination room header pointer (bank $8F): Tourian Escape Room 4
    db $00 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $36 ; Y cap
    db $02 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab28
; room DEDE: Tourian Escape Room 4
Room_DEDE_door_list_index_0_Door:
    dw $dea7 ; Destination room header pointer (bank $8F): Tourian Escape Room 3
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab34
; room DEDE: Tourian Escape Room 4
Room_DEDE_door_list_index_1_Door:
    dw $96ba ; Destination room header pointer (bank $8F): Climb
    db $40 ; Bit Flag (Elevator properties)
    db $05 ; Direction
    db $2e ; X cap
    db $86 ; Y cap
    db $02 ; X screen
    db $08 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $E4CF ; Custom door ASM to execute (bank $8F)
org $83ab40
; room DF1B: [Tourian First Save Room]
Room_DF1B_door_list_index_0_Door:
    dw $daae ; Destination room header pointer (bank $8F): Tourian First Room
    db $00 ; Bit Flag (Elevator properties)
    db $04 ; Direction
    db $01 ; X cap
    db $36 ; Y cap
    db $00 ; X screen
    db $03 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab4c
; room DF45: [Ceres Elevator Room]
Room_DF45_door_list_index_0_Door:
    dw $df8d ; Destination room header pointer (bank $8F): [Ceres Jump Tutorial Room]
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e513 ; Custom door ASM to execute (bank $8F)
org $83ab58
; room DF8D: [Ceres Jump Tutorial Room]
Room_DF8D_door_list_index_0_Door:
    dw $df45 ; Destination room header pointer (bank $8F): [Ceres Elevator Room]
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $02 ; X cap
    db $26 ; Y cap
    db $00 ; X screen
    db $02 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $e4e0 ; Custom door ASM to execute (bank $8F)
org $83ab64
; room DF8D: [Ceres Jump Tutorial Room]
Room_DF8D_door_list_index_1_Door:
    dw $dfd7 ; Destination room header pointer (bank $8F): [Ceres Staircase Room]
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab70
; room DFD7: [Ceres Staircase Room]
Room_DFD7_door_list_index_0_Door:
    dw $df8d ; Destination room header pointer (bank $8F): [Ceres Jump Tutorial Room]
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $02 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab7c
; room DFD7: [Ceres Staircase Room]
Room_DFD7_door_list_index_1_Door:
    dw $e021 ; Destination room header pointer (bank $8F): [Ceres Dead Scientists Room]
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab88
; room E021: [Ceres Dead Scientists Room]
Room_E021_door_list_index_0_Door:
    dw $dfd7 ; Destination room header pointer (bank $8F): [Ceres Staircase Room]
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $02 ; X cap
    db $16 ; Y cap
    db $00 ; X screen
    db $01 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83ab94
; room E021: [Ceres Dead Scientists Room]
Room_E021_door_list_index_1_Door:
    dw $e06b ; Destination room header pointer (bank $8F): [Ceres Last Corridor]
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $1e ; X cap
    db $06 ; Y cap
    db $01 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83aba0
; room E06B: [Ceres Last Corridor]
Room_E06B_door_list_index_0_Door:
    dw $e021 ; Destination room header pointer (bank $8F): [Ceres Dead Scientists Room]
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83abac
; room E06B: [Ceres Last Corridor]
Room_E06B_door_list_index_1_Door:
    dw $e0b5 ; Destination room header pointer (bank $8F): [Ceres Ridley Room]
    db $00 ; Bit Flag (Elevator properties)
    db $01 ; Direction
    db $0e ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
org $83abb8
; room E0B5: [Ceres Ridley Room]
Room_E0B5_door_list_index_0_Door:
    dw $e06b ; Destination room header pointer (bank $8F): [Ceres Last Corridor]
    db $00 ; Bit Flag (Elevator properties)
    db $00 ; Direction
    db $01 ; X cap
    db $06 ; Y cap
    db $00 ; X screen
    db $00 ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $0000 ; Custom door ASM to execute (bank $8F)
