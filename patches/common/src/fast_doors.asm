
arch snes.cpu

;;; add Kejardon faster decompression patch (has lorom directive)
incsrc "decompression.asm"

;;; Door Transition Speed by kazuto + extra code to fix samus initial position
;;; just double the speed, discard configurability due to the extra code

;Door stuff	
!S = $0008	;Door scroll speed
!F = $0006	;Screen fade speed

;Don't touch these values
!X = $0100/!S	;Horizontal loop counter, X times S should equal $100
!Y = $00E0/!S+1	;Vertical loop counter, Y times S should equal $E0 ($100-$20 due to the HUD)
!C = $0010/!S+1	;Vertical counter for drawing tile rows "behind" HUD (prior to scrolling)

org $80AE9D
	dw !S
org $80AEA7
	dw !S
org $80AEB6
	dw !X
org $80AEE1
	dw !S
org $80AEEB
	dw !S
org $80AEFA
	dw !X
org $80AF45
	dw !Y
org $80AF64
	dw !S
org $80AF6E
	dw !S
org $80AF7D
	dw !Y
org $80AFE6
	dw !S
org $80AFF0
	dw !S
org $80AFF6
	dw !C
org $80B02A
	dw !Y
org $82D962
	dw !F

org $82DE50
	BPL $0F
	LDA $0791
	ROR A
	ROR A
	BCS $05
	LDA #$00C8
	BRA $03
	LDA #$0180

;Uncomment one of the three following lines
;	LSR A		;Uncomment only if S equals $0002
;	NOP		;Uncomment only if S equals $0004
	ASL A		;Uncomment only if S equals $0008

org $82e3c5
	jsr fix_samus_pos

;;; Door centering speed by Kazuto:
!Speed = 2	;Pixels per-frame to slide the screen, default $01
!FreeSpace = $82F70F	;Safe to move anywhere in ROM

org $82E325	;Horizontal doors
	NOP
	PHP
	LDX #$0004
	PLP
	JSL SlideCode
org $82E339	;Vertical doors
	NOP
	PHP
	LDX #$0000
	PLP
	JSL SlideCode

org !FreeSpace
SlideCode:
	SEP #$20
	BMI $09
	LDA $0911,X
	CMP.b #$00+!Speed
	BPL $12
	BRA $0A
	LDA $0911,X
	CMP.b #$00-!Speed
	BMI $10
	INC $0912,X	;These two lines handle odd
	STZ $0911,X	;screen scrolling distances
	REP #$20
	RTL

	REP #$20
	LDA.w #$0000-!Speed	;Screen is scrolling up or left
	BRA $05
	REP #$20
	LDA.w #$0000+!Speed	;Screen is scrolling down or right
	CLC
	ADC $0911,X
	STA $0911,X
	RTL

;;; for double door speed: act as if we moved only 4px
fix_samus_pos:
	lda $0791
	bit #$0002
	beq .horizontal
.vertical:
	bit #$0001
	beq .down
.up:
	lda $0915
	clc
	adc #!S/2
	bra .vertical_end
.down:
	lda $0915
	sec
	sbc #!S/2
.vertical_end:
	sta $0915
	bra .end
.horizontal:
	bit #$0001
	beq .right
.left:
	lda $0911
	clc
	adc #!S/2
	bra .horizontal_end
.right:
	lda $0911
	sec
	sbc #!S/2
.horizontal_end:
	sta $0911
.end:
	lda $0af6		; hijacked code
	rts
