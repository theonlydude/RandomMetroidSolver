;;; VARIA HUD to display current area (in the area randomizer sense),
;;; the split type (letter F, M, or Z), and the remaining number of items
;;; of the chozen split in the current area

;;; Adapted from death counter and etank bar combine by lioran

;;; Compile with "asar" (https://github.com/RPGHacker/asar/releases)


;free space make sure it doesnt override anything you have
!freespace80 = $80CD8E ;$80 hijack the etank drawing action and draw the skull+death count number as well
!hudposition = #$0006 ;position of the death counter on the hud, lowest possible spot is #$0006 increase to desired position, is taking the spot of the second row of etank by default

lorom

; comment all of this out if escapes are not part of your hack
	
org $809B96
	JSR draw_info
	;the following code will overwrite the normal etank drawing code, no extra space require, just turn the 2 lines of 14 etank into 1 lines of combined 14 etanks
	;if you do not wish you have etank row combined , comment this whole block
	STA $4204
	SEP #$20
	LDA #$64
	STA $4206 
	REP #$30
	LDA #$0000
	STA $14
	LDY #$0007
	TAX
	LDA $4216
	STA $12
	-
	LDA $14 : CLC : ADC #$0064 : STA $14
	ADC #$02BC : STA $16
	INX : INX 
	LDA $09C4
	CMP $14 : BCS +;check if empty
	LDA #$2C0F
	BRA ++
	+
	LDA $09C2
	CMP $16 : BCC +
	LDA #$2C31
	BRA ++
	+
	CMP $14 : BCC +
	LDA #$2831
	BRA ++
	+
	LDA #$3430
	++
	STA $7EC648,x
	DEY
	BNE -
	NOP 
;end of etank row combine

org !freespace80 ;free space in bank $80
	;draw the death counter
draw_info:
	phx
	phy

	;; determine current graph area text address
	ldx $07bb
	lda $8f0010,x
	asl : asl : asl : asl
	tay
	;; draw text
	ldx !hudposition	
.draw_loop:
	lda area_names,y
	beq .end
	sta $7ec602,x
	iny : iny
	inx : inx
	bra .draw_loop
.end:
	ply
	plx
	lda $09C2 ;original code that was hijacked
	rts


; A=value to display (2 digits)
draw_two:	
	sta $4204
	sep #$20
	lda #$0a
	sta $4206
	pha : pla : pha : pla : rep #$20
	lda $4214 : asl : tay
	lda NumberGFXTable, y			
	sta $7ec604, x		; FIXME
	lda $4216 : asl : tay
	lda NumberGFXTable, y		
	sta $7ec606, x		; FIXME
	rts

;; Normal numbers (like energy/ammo)
NumberGFXTable:
	DW #$0C09,#$0C00,#$0C01,#$0C02,#$0C03,#$0C04,#$0C05,#$0C06,#$0C07,#$0C08

;; Inverse video numbers
;; NumberGFXTable:
;; 	DW #$0C45,#$0C3C,#$0C3D,#$0C3E,#$0C3F,#$0C40,#$0C41,#$0C42,#$0C43,#$0C44

table "tables/hud_chars.txt"

area_names:
	dw "CERES  "
	dw $0000
	dw " CRAT  "
	dw $0000
	dw "GRE B  "
	dw $0000
	dw "RED B  "
	dw $0000
	dw " SHIP  "
	dw $0000
	dw "KRAID  "
	dw $0000
	dw "UNORF  "
	dw $0000
	dw " CROC  "
	dw $0000
	dw "LNORF  "
	dw $0000
	dw "WMARI  "
	dw $0000
	dw "EMARI  "
	dw $0000
	dw " TOUR  "
	dw $0000

cleartable
