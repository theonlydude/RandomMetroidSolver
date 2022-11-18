;;; compile with asar

arch snes.cpu
lorom

;;; remove gate at crabe tunnel by ending PLM list
org $8fc48b
; room D08A: Crab Tunnel
Room_D08A_state_D097_PLM:
    dw $0000
