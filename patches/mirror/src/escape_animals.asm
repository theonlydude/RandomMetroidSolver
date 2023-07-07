;;; compile with thedopefish asar
;;; fix escape animals X position and movement

arch 65816
lorom

;  Enemy population format is:
;   ____________________________________ Enemy ID
;  |      _______________________________ X position
;  |     |      __________________________ Y position
;  |     |     |      _____________________ Initialisation parameter (orientation in SMILE)
;  |     |     |     |      ________________ Properties (special in SMILE)
;  |     |     |     |     |      ___________ Extra properties (special graphics bitset in SMILE)
;  |     |     |     |     |     |      ______ Parameter 1 (speed in SMILE)
;  |     |     |     |     |     |     |      _ Parameter 2 (speed2 in SMILE)
;  |     |     |     |     |     |     |     |
;  iiii  xxxx  yyyy  oooo  pppp  gggg  aaaa  bbbb

;;; Room Bomb Torizo, state escape
; Room $9804, state $984F: Enemy population
org $a18ed3
;;;     dw $F313,$00E0,$00B8,$0000,$2400,$0000,$0000,$0000
        dw $F313,$0020,$00B8,$0000,$2400,$0000,$0000,$0000 ; dachora


;;; inverse dachora movement

;;; $EAC9: Instruction - enemy X position -= 6 ;;;
; $B3:EAC9 AE 54 0E    LDX $0E54  [$7E:0E54]
; $B3:EACC BD 7A 0F    LDA $0F7A,x[$7E:0F7A]
; $B3:EACF 38          SEC
; $B3:EAD0 E9 06 00    SBC #$0006
; $B3:EAD3 9D 7A 0F    STA $0F7A,x[$7E:0F7A]
; $B3:EAD6 6B          RTL
org $B3EACF
        CLC
        ADC #$0006

;;; $EAD7: Instruction - enemy X position += 6 ;;;
; $B3:EAD7 AE 54 0E    LDX $0E54  [$7E:0E54]
; $B3:EADA BD 7A 0F    LDA $0F7A,x[$7E:0F7A]
; $B3:EADD 18          CLC
; $B3:EADE 69 06 00    ADC #$0006
; $B3:EAE1 9D 7A 0F    STA $0F7A,x[$7E:0F7A]
; $B3:EAE4 6B          RTL
org $B3EADD
        SEC
        SBC #$0006


;;; inverse dachora spritemaps

;;; $EB1B: Escape dachora spritemaps ;;;
org $B3eb1b
    dw $0009,$0008 : db $F2 : dw $7310,$C3F8 : db $EA : dw $7301,$01F6 : db $F7 : dw $731E,$01FE : db $F7 : dw $730E,$0006 : db $03 : dw $731F,$0006 : db $FB : dw $730F,$0006 : db $0F : dw $7322,$C3F6 : db $07 : dw $7313,$C3F6 : db $FF : dw $7303
    dw $0009,$0009 : db $F3 : dw $7310,$C3F9 : db $EB : dw $7301,$01F6 : db $F8 : dw $735F,$01FE : db $F8 : dw $735E,$0006 : db $04 : dw $731F,$0006 : db $FC : dw $730F,$C3F6 : db $08 : dw $7316,$0006 : db $08 : dw $7315,$C3F6 : db $00 : dw $7306
    dw $000B,$000A : db $F1 : dw $7310,$C3FA : db $E9 : dw $7301,$000E : db $0E : dw $732D,$01F6 : db $F6 : dw $731E,$01FE : db $F6 : dw $730E,$0006 : db $FA : dw $730F,$C3F6 : db $FE : dw $7309,$C3FE : db $FE : dw $7308,$01EE : db $0E : dw $732B,$01EE : db $06 : dw $731B,$C3FE : db $06 : dw $7318
    dw $0009,$0008 : db $F2 : dw $7310,$C3F8 : db $EA : dw $7301,$01F6 : db $F7 : dw $735F,$01FE : db $F7 : dw $735E,$0006 : db $0F : dw $7352,$0006 : db $03 : dw $731F,$0006 : db $FB : dw $730F,$C3F6 : db $07 : dw $7343,$C3F6 : db $FF : dw $7333
    dw $0009,$0009 : db $F3 : dw $7310,$C3F9 : db $EB : dw $7301,$0004 : db $10 : dw $7352,$0006 : db $04 : dw $731F,$0006 : db $FC : dw $730F,$01F6 : db $F8 : dw $731E,$01FE : db $F8 : dw $730E,$C3F6 : db $08 : dw $7346,$C3F6 : db $00 : dw $7336
    dw $000B,$000A : db $F1 : dw $7310,$C3FA : db $E9 : dw $7301,$01F6 : db $F6 : dw $735F,$01FE : db $F6 : dw $735E,$000E : db $0E : dw $735A,$0006 : db $FA : dw $730F,$C3F6 : db $FE : dw $7339,$C3FE : db $06 : dw $7348,$01EE : db $06 : dw $734B,$01EE : db $0E : dw $735B,$C3FE : db $FE : dw $7338

    dw $0009,$01F0 : db $F2 : dw $3310,$C3F8 : db $EA : dw $3301,$0002 : db $F7 : dw $331E,$01FA : db $F7 : dw $330E,$01F2 : db $03 : dw $331F,$01F2 : db $FB : dw $330F,$01F2 : db $0F : dw $3322,$C3FA : db $07 : dw $3313,$C3FA : db $FF : dw $3303
    dw $0009,$01EF : db $F3 : dw $3310,$C3F7 : db $EB : dw $3301,$0002 : db $F8 : dw $335F,$01FA : db $F8 : dw $335E,$01F2 : db $04 : dw $331F,$01F2 : db $FC : dw $330F,$C3FA : db $08 : dw $3316,$01F2 : db $08 : dw $3315,$C3FA : db $00 : dw $3306
    dw $000B,$01EE : db $F1 : dw $3310,$C3F6 : db $E9 : dw $3301,$01EA : db $0E : dw $332D,$0002 : db $F6 : dw $331E,$01FA : db $F6 : dw $330E,$01F2 : db $FA : dw $330F,$C3FA : db $FE : dw $3309,$C3F2 : db $FE : dw $3308,$000A : db $0E : dw $332B,$000A : db $06 : dw $331B,$C3F2 : db $06 : dw $3318
    dw $0009,$01F0 : db $F2 : dw $3310,$C3F8 : db $EA : dw $3301,$0002 : db $F7 : dw $335F,$01FA : db $F7 : dw $335E,$01F2 : db $0F : dw $3352,$01F2 : db $03 : dw $331F,$01F2 : db $FB : dw $330F,$C3FA : db $07 : dw $3343,$C3FA : db $FF : dw $3333
    dw $0009,$01EF : db $F3 : dw $3310,$C3F7 : db $EB : dw $3301,$01F4 : db $10 : dw $3352,$01F2 : db $04 : dw $331F,$01F2 : db $FC : dw $330F,$0002 : db $F8 : dw $331E,$01FA : db $F8 : dw $330E,$C3FA : db $08 : dw $3346,$C3FA : db $00 : dw $3336
    dw $000B,$01EE : db $F1 : dw $3310,$C3F6 : db $E9 : dw $3301,$0002 : db $F6 : dw $335F,$01FA : db $F6 : dw $335E,$01EA : db $0E : dw $335A,$01F2 : db $FA : dw $330F,$C3FA : db $FE : dw $3339,$C3F2 : db $06 : dw $3348,$000A : db $06 : dw $334B,$000A : db $0E : dw $335B,$C3F2 : db $FE : dw $3338



;;; inverse etecoons starting X position
org $B3E718
;       dw $0080,$00A0,$00E8
        dw $0080,$0060,$0018

;;; inverse etecoons starting spritemap
org $B3E72A
;       dw $E556,$E582,$E5C6
        dw $E582,$E556,$E5C6

;;; inverse etecoons X velocity
org $B3E730 
;       dw $FE00,$0280,$0000
        dw $0280,$FE00,$0000

;;; make stationnary etecoon move right after wall is opened
org $B3E5DA
;;; $E5DA: Instruction list -  ;;;
    dw $8074 ; | B3E5DA | Enemy $0FB2 = RTS
    dw $8123,$0008 ; | B3E5DC | Timer = 0008h
    dw $0008,$E75F
    dw $E610,$0003 ; | B3E5E4 | Enemy X position += 3h
    dw $0008,$E770
    dw $E610,$0003 ; | B3E5EC | Enemy X position += 3h
    dw $0008,$E77C
    dw $E610,$0003 ; | B3E5F4 | Enemy X position += 3h
    dw $0008,$E770
    dw $E610,$0003 ; | B3E5FC | Enemy X position += 3h
    dw $8110,$E5E0 ; | B3E600 | Decrement timer and go to $E5E0 if non-zero
    dw $0040,$E8B0
    dw $0008,$E8D5
    dw $80ED,$E5AE ; | B3E60C | Go to $E5AE
	
;;; etecoon run to exit room, change facing
org $B3E5AE
;;; $E5AE: Instruction list -  ;;;
    dw $806B,$E65C ; | B3E5AE | Enemy $0FB2 = $E65C
    dw $0003,$E736
    dw $0003,$E747
    dw $0003,$E753
    dw $0003,$E747
    dw $80ED,$E5B2 ; | B3E5C2 | Go to $E5B2

;;; moving etecoons IA
VelocityX = $7E0FA8
InstructionTimer = $7E0F94
SpriteMapList = $7E0F92

org $A0C6AB
MoveEnemyHorizontal:

org $A0C786
MoveEnemyVertical:

org $808233
ChecksEventAHasHappened:

org $B3E680
;;; $E680:  ;;;
    STZ.b $12                   ; \
    STZ.b $14                   ; |
    LDA.w VelocityX,X           ; |
    BPL FacingRight             ; } $14.$12 = [enemy X velocity] / 100h
    DEC.b $14                   ; |

FacingRight:
    STA.b $13                   ; /
    JSL.l MoveEnemyHorizontal   ; Move enemy right by [$14].[$12]
    BCC NoWallCollision         ; If not collided with wall
    LDA.w #$0001
    STA.w InstructionTimer,X
    LDA.w VelocityX,X           ; Invert X velocity
    EOR.w #$FFFF
    INC
    STA.w VelocityX,X
    BPL FacingRightSpritemap    ; set spritemap list to match facing and velocity
    LDA.w #$E556                ; spritemap list facing left
    BRA BRA_B3E6AD

FacingRightSpritemap:
    LDA.w #$E582                ; spritemap list facing right

BRA_B3E6AD:
    STA.w SpriteMapList,X

    LDA.w #$000F                ; check if wall has been opened (event 0F)
    JSL.l ChecksEventAHasHappened
    BCC WallNotOpened
    LDA.w #$E5AE                ; update spritemap list to etecoon leaving the room, which change the AI to E65C
    STA.w SpriteMapList,X

WallNotOpened:
NoWallCollision:
    STZ.b $12                   ; \
    LDA.w #$0001                ; |
    STA.b $14                   ; } Move enemy down by 1.0
    JSL.l MoveEnemyVertical     ; /
    RTS


SubPositionX = $7E0F7C
PositionX = $7E0F7A

;;; etecoon AI when leaving the room
org $B3E65C
;;; $E65C:  ;;;
    LDA.w SubPositionX,X
    SEC                         ; go left instead of right
    SBC.w #$8000
    STA.w SubPositionX,X
    LDA.w PositionX,X
    SBC.w #$0003                ; go left instead of right
    STA.w PositionX,X
    RTS
