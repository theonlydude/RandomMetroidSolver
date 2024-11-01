;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

lorom

incsrc "sym/gray_doors.asm"

org $8f83fe
; room 9804: Bomb Torizo Room
Door_1B_Room_9804_PLM_BAF4:
    ; Bomb Torizo grey door
    dw gray_doors_bt_door_facing_left : db $0e : db $06 : dw $081b 
