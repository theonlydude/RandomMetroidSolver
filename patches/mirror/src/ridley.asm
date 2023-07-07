;;; compile with thedopefish asar
;;; mirror ridley in norfair
;;; only update ridley starting position and facing, the rest of the fight is like vanilla

arch 65816
lorom

;;; ceres ridley
;$A0:E13F             dx 2000, E14F, 7FFF, 0005, 0008, 0008, A6, 08, 0000, 0001, A0F5, 0001, 0000, A288, 800F, A2D3, 8041, 0000, 0000, 00000000, DFB2, 0000, 00000000, 8023, DF8A, 0000, B09400, 05, F44C, F1B2, 0000
;;; norfair ridley
;$A0:E17F             dx 2000, E14F, 4650, 00A0, 0008, 0008, A6, 08, 0000, 0005, A0F5, 0001, 0000, B227, 800F, B297, 8041, B28A, 0000, 00000000, DFB2, 0000, 00000000, 8023, DF8A, 0000, B09400, 02, F44C, F1B2, 0000


;;; $A0F5: Initialisation AI - enemy $E13F/$E17F (Ridley) ;;;
; $A6:A170 A9 60 00    LDA #$0060
; $A6:A173 8D 7A 0F    STA $0F7A  [$7E:0F7A]
;;; norfair ridley x start position
org $A6A170
        lda #$00a0

; $A6:A1B9 A9 02 00    LDA #$0002
; $A6:A1BC 8F 20 78 7E STA $7E7820[$7E:7820]
;;; norfair ridley direction in $7E7820 (2 for right, 0 for left)
org $A6A1B9
        lda #$0000

;;; $E91D: Instruction list -  ;;;
; ; Fly up and start main AI, I guess
; $A6:E91D             dx E517,E945,      ; ???
org $A6E91D
	dw check_ridley_area, $E945

org $A6E514
goto_next_command:
org $A6E4E9
goto_argument:

;;; $E828: Unused ;;;
org $A6E828
;;; create a new instruction which checks area instead of facing
;;; Move on to next command if Ridley is in ceres, else go to argument.
check_ridley_area:
        LDA $079F               ; load current area
        CMP #$0002              ; ceres area is 6, norfair is 2
        beq .argument
        jmp goto_next_command
.argument
	jmp goto_argument

warnpc $A6E83F

;;; $E945: Instruction list -  ;;;
; $A6:E945             dx 0003,E9A5,      ; extended spritemaps, ridley facing right
;                         E51F,FFFF,FFF4, ; position for wings
;                         0004,EA93,      ; extended spritemaps, ridley facing right, legs half extended
;                         E51F,0004,FFF8, ; ???
;                         0005,EAB5,      ; extended spritemaps, ridley facing right, legs extended
;                         E976,           ; ???
;                         0011,EA93,      ; Ridley facing right, legs half extended
;                         0011,E9A5,      ; Ridley facing right
;                         812F            ; Sleep
;;; update instruction list when ridley first take off in norfair
org $A6E945
        dw $0003, $E983         ; extended spritemaps, ridley facing left
        dw $E51F, $0001, $FFF4  ; add to ridley x/y
        dw $0004, $EA4F         ; extended spritemaps, ridley facing left, legs half extended
	dw $E51F, $0004, $FFF8  ; add to ridley x/y again
        dw $0005, $EA71         ; Ridley facing left, legs extended
	dw $E976                ; Set Ridley's main AI to B2F3, and vertical speed to FEA0. (Norfair)
        dw $0011, $EA4F         ; Ridley facing left, legs half extended
        dw $0011, $E983         ; Ridley facing left
