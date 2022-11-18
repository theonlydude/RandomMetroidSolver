;;; compile with asar

arch snes.cpu
lorom

;;; remove gate at green hill zone by moving it out of the screen
org $8f8664
; room 9E52: Green Hill Zone
Room_9E52_state_9E5F_PLM:
    ; Downwards closed gate
    dw $c82a : db $1d : db $12 : dw $8000 
    ; Downwards gate shotblock
    dw $c836 : db $1d : db $12 : dw $0000 
