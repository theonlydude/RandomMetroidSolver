;;; Compiles with thedopefish asar

arch 65816
lorom

incsrc "sym/rando_escape_common.asm"
incsrc "sym/bank_8f.asm"

incsrc "macros.asm"

;;; elevator for business center
org rando_escape_common_elevator_business_center
    dw $D73F,$0080,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for red tower top
org rando_escape_common_elevator_red_tower_top
    dw $D73F,$0280,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for green brin shaft
org rando_escape_common_elevator_green_bt_shaft
    dw $D73F,$0380,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for forgotten highway
org rando_escape_common_elevator_forgotten_highway
    dw $D73F,$0080,$02C0,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for morph room
org rando_escape_common_elevator_morph_room
    dw $D73F,$0280,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for LN main hall
org rando_escape_common_elevator_ln_main_hall
    dw $D73F,$0380,$02A2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; DATA, bank 8F. makes map stations doors in norfair/brin/maridia/ws permanently grey
org bank_8f_Door_4C_Room_A7DE_PLM_C85A    ; norfair map
    dw $C842
    db $0e,$46
    dw $904C

org bank_8f_Door_90_Room_D21C_PLM_C890    ; maridia map
    dw $C848
    db $01,$16
    dw $9090

org bank_8f_Door_20_Room_9AD9_PLM_C88A    ; brinstar map
    dw $C842
    db $3e,$46
    dw $9020


;;; alternate flyway (= pre BT) door lists for escape animals surprise
macro FlywayDoorList(n)
    ;; door to parlor
    dw $92FD ; Destination room header pointer (bank $8F): Parlor and Alcatraz
    db $00   ; Bit Flag (Elevator properties)
    db $04   ; Direction
    db $11   ; X cap
    db $26   ; Y cap
    db $01   ; X screen
    db $02   ; Y screen
    dw $8000 ; Distance from door to spawn Samus
    dw $B9A2 ; Custom door ASM to execute (bank $8F)
%export(flyway_door_lists_door<n>)
    ;; placeholder for BT door to be filled in by randomizer
    db $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca
endmacro

org rando_escape_common_flyway_door_lists
flyway_door_lists:
%FlywayDoorList(0)
%FlywayDoorList(1)
%FlywayDoorList(2)
%FlywayDoorList(3)
