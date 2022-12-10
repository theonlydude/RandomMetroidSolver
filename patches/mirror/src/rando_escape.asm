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
