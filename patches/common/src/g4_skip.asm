;;; Skip G4 drowning
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; ; Room $99BD: Green Pirates Shaft, 3rd door, leading to Tourian
;;; $83:8C52             dx A5ED,00,04,01,06,00,00,8000,0000
org $838c5c
        dw check_g4_dead        ; add door asm ptr

; $7E:D828..2F: Boss bits. Indexed by area
;     1: Area boss (Kraid, Phantoon, Draygon, both Ridleys)
;     2: Area mini-boss (Spore Spawn, Botwoon, Crocomire, Mother Brain)
;     4: Area torizo (Bomb Torizo, Golden Torizo)
; 
; $079F: Area index
;     0: Crateria
;     1: Brinstar
;     2: Norfair
;     3: Wrecked Ship
;     4: Maridia
;     5: Tourian
;     6: Ceres
;     7: Debug
org $8ffe00
check_g4_dead:
	lda $7ed828
	bit.w #$0100            ; Brinstar - Kraid
	beq .end
	lda $7ed82c             ; Maridia
	bit.w #$0001            ; Draygon
	beq .end
	lda $7ed82a             ; Norfair & Wrecked Ship
	and.w #$0101            ; Ridley  & Phantoon
	cmp.w #$0101
	bne .end
        lda $7ed820
        ora #$0400              ; set event Ah - entrance to Tourian is unlocked
        sta $7ed820
.end
        rts
