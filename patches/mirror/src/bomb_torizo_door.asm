;;; compile with asar

arch snes.cpu
lorom

;;; make bomb torizo door facing left

;;; right: A683 left: A677
;;; right: A6FB left: A6CB
;;; right: A6EF left: A6BF
;;; right: A6E3 left: A6B3
;;; right: A6D7 left: A6A7
;;; right: A9EF left: A9B3

;;; $BA4C: Instruction list - PLM $BAF4 (bomb torizo grey door) ;;;
org $84ba4c
{
InstructionListPlmBaf4BombTorizoGreyDoor:
    dw $0002,$A677
    dw $BA6F,$BA4C ; | 84BA50 | Go to $BA4C if Samus doesn't have bombs
    dw $0028,$A677
    dw $8C19 : db $08 ; | 84BA58 | Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
    dw $0002,$A6CB
    dw $0002,$A6BF
    dw $0002,$A6B3
    dw $0001,$A6A7
    dw $8724,$BA7F ; | 84BA6B | Go to $BA7F
}

;;; $BA7F: Instruction list - PLM $BAF4 (bomb torizo grey door) ;;;
{
org $84ba7f
InstructionListPlmBaf4BombTorizoGreyDoor_BA7F:
    dw $8A72,$C4E2 ; | 84BA7F | Go to $C4E2 if the room argument door is set
    dw $8A24,$BA93 ; | 84BA83 | Link instruction = $BA93
    dw $BE3F ; | 84BA87 | Set grey door pre-instruction
    dw $0001,$A6A7
    dw $86B4 ; | 84BA8D | Sleep
    dw $8724,$BA8D ; | 84BA8F | Go to $BA8D
    dw $8A24,$BAB7 ; | 84BA93 | Link instruction = $BAB7
    dw $86C1,$BD0F ; | 84BA97 | Pre-instruction = go to link instruction if shot
    dw $0003,$A9B3
    dw $0004,$A6A7
    dw $0003,$A9B3
    dw $0004,$A6A7
    dw $0003,$A9B3
    dw $0004,$A6A7
    dw $8724,$BA9B ; | 84BAB3 | Go to $BA9B
    dw $8A91 : db $01 : dw $BABC ; | 84BAB7 | Increment door hit counter; Set room argument door and go to $BABC if [door hit counter] >= 01h
    dw $8C19 : db $07 ; | 84BABC | Queue sound 7, sound library 3, max queued sounds allowed = 6 (door opened)
    dw $0004,$A6B3
    dw $0004,$A6BF
    dw $0004,$A6CB
    dw $0001,$A677
    dw $86BC ; | 84BACF | Delete
}

org $8f83fe
; room 9804: Bomb Torizo Room
Door_1B_Room_9804_PLM_BAF4:
    ; Bomb Torizo grey door
    dw $baf4 : db $0e : db $06 : dw $081b 
