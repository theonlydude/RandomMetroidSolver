;;; Skip G4 drowning
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; ; Room $99BD: Green Pirates Shaft, 3rd door, leading to Tourian
;;; $83:8C52             dx A5ED,00,04,01,06,00,00,8000,0000
org $838c5c
        dw open_g4              ; add door asm ptr

;;; objectives_completed function from objectives_pause patch which is applied by default
org $82fb6d
objectives_completed:

org $8ffe00
open_g4:
	;; check objectives
	jsl objectives_completed
	bcc .end

	;; open g4
        lda $7ed820
        ora #$0400              ; set event Ah - entrance to Tourian is unlocked
        sta $7ed820

.end
        rts
