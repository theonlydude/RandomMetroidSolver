;;; 
;;; Nerfed charge beam patch
;;; 
;;; Author: Smiley
;;; 
;;; Disassembled from DASH IPS patch
;;; 
;;; Effects : charge beam is available from the start, with nerfed damage

;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; goes to charge branch whatever items
org $90b81e
	bit #$0000
	bra $0a

;;; disables a "no charge" check
org $90b8f2
	bra $00

;;; hijack for beam damage modification 
org $90b9e6
	jsr charge

;;; nerfed charge : damage modification
org $90f700
charge:
	lda $09A6		; equipped beams
	bit #$1000		; check for charge
	bne .end
	;; if no charge, nerfs charge dmg
	;; say original damage = D
	;; this sets it to (D + D/4)/4 = 0.3125 * D
	lda $0C2C,X
	lsr $0C2C,X
	lsr $0C2C,X
	adc $0C2C,X
	lsr
	lsr
	sta $0C2C,X
.end:
	lda $0C18,X
	rts
