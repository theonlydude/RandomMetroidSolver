;;; Compiles with thedopefish asar

arch 65816
lorom

incsrc "sym/rando_escape_common.asm"

;;; elevator for business center
org rando_escape_common_elevator_business_center
    dw $D73F,$0080,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for red tower top
org rando_escape_common_elevator_red_tower_top
    dw $D73F,$0080,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for green brin shaft
org rando_escape_common_elevator_green_bt_shaft
    dw $D73F,$0080,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for forgotten highway
org rando_escape_common_elevator_forgotten_highway
    dw $D73F,$0080,$02C0,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for morph room
org rando_escape_common_elevator_morph_room
    dw $D73F,$0580,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; elevator for LN main hall
org rando_escape_common_elevator_ln_main_hall
    dw $D73F,$0480,$02A2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

;;; DATA, bank 8F. makes map stations doors in norfair/brin/maridia/ws
;;; permanently grey
org $8f8b06                     ; norfair map
    dw $C848
    db $01,$46
    dw $904C

org $8fc547                     ; maridia map
    dw $C842
    db $0E,$16
    dw $9090

org $8f84b8                     ; brinstar map
    dw $C848
    db $01,$46
    dw $9020


;;; alternate flyway (= pre BT) door lists for escape animals surprise
macro FlywayDoorList(n)
    ;; door to parlor
    db $FD, $92, $00, $05, $3E, $26, $03, $02, $00, $80, $A2, $B9
.door<n>:
    ;; placeholder for BT door to be filled in by randomizer
    db $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca
endmacro

org rando_escape_common_flyway_door_lists
flyway_door_lists:
%FlywayDoorList(0)
%FlywayDoorList(1)
%FlywayDoorList(2)
%FlywayDoorList(3)
