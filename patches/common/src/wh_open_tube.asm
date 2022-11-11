;;; Opens Maridia Tube for Watering Hole start to have more varied seed starts
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)


arch 65816
lorom

;;; door ASM ptr for door associated to save starting point
org $83a4a2
    dw open_tube

org $8ff400
open_tube:
    lda #$000b : jsl $8081fa
    rts

warnpc $8ff40f
