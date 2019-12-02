;;; 
;;; Nerfed charge beam patch
;;; 
;;; Authors: Smiley for permanent charge and beam damage hijack.
;;;          Flo for hardware division usage and SBA/pseudo screw damage.
;;; 
;;; Originally disassembled from DASH IPS patch
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

;;; divides projectile damage by 3
macro divprojdmg3()
	lda $0C2C,X
	sta $4204
	sep #$20
	lda #$03
	sta $4206
	rep #$20
	pha : pla : xba : xba 	; wait for division
	lda $4214
	sta $0C2C,X
endmacro

;;; nerfed charge : damage modification
org $90f6a0
charge:
	lda $09A6		; equipped beams
	bit #$1000		; check for charge
	bne .end
	;; if no charge, nerfs charge dmg : divide by 3
	%divprojdmg3()
.end:
	lda $0C18,X
	rts

;;; nerf SBA damage
org $9381b9
	jsr sba

org $93f620
sba:
	sta $0C2C,X
	lda $09A6		; equipped beams
	bit #$1000		; check for charge
	bne .end
	;; if no charge, nerfs SBA dmg : divide by 3
	%divprojdmg3()
.end:
	rts

;;; nerf pseudo screw damage
org $a0a4cc
	jsr pseudo

org $a0f800
pseudo:
	;; we can't freely use A here. Y shall contain pseudo screw dmg at the end
	pha
	lda $09A6		; equipped beams
	bit #$1000		; check for charge
	beq .nocharge
.charge:
	ldy #$00C8		; vanilla value
	bra .end
.nocharge:
	ldy #$0042		; 66 (approx 200/3)
.end:
	pla
	rts
