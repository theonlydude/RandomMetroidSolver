;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

;;; remove gate at caterpillar by moving it out of the screen
org $8f889e
    ; Downwards closed gate
    dw $c82a : db $04 : db $4a : dw $8000
    ; Downwards gate shotblock
    dw $c836 : db $04 : db $4a : dw $000a
