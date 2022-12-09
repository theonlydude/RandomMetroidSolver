arch snes.cpu
lorom

org $83ADA0
	db $FD, $92, $00, $05, $3E, $26, $03, $02, $00, $80, $A2, $B9	; door to parlor
	db $2E, $B3, $40, $04, $01, $16, $00, $01, $00, $80, $00, $00	; door to bt, changed to ridley
	db $79, $98, $40, $05, $2E, $06, $02, $00, $00, $80, $00, $00	; ridley exit, changed to pre-bt
	
org $8F98DC
	db $06, $F0 													; setup asm pointer for pre-bt room
	
org $8FF000
	db $A0, $AD, $AC, $AD											; door out pointer for pre-bt
	
org $8FF006
	LDA #$0000
	STA $7ED82A														; reset boss flag
	LDA #$F000														; load door pointer
	STA $7E07B5														; change door out pointer
	JML $8F91BB														; run original code
	
org $8FB358
	db $18, $F0														; setup asm pointer for ridley
	
org $8FF018
	LDA $7ED820 													; loads event flags
	BIT #$4000  													; checks for escape flag set
	BEQ quit
	LDA #$0000
	STA $7ED8BB
	LDA #door_ptr														; load door pointer
	STA $7E07B5														; change door out pointer
	LDA #$AAAA
	STA $7E1CD5														; move top right grey door PLM far away
	LDA #$80AE : STA $7F00DE
	LDA #$80CE : STA $7F00FE
	LDA #$88CE : STA $7F011E
	LDA #$88AE : STA $7F013E										; change top right door tiles to grey
	JML $8F91F7														; run original code for ridley
	
quit:
	JML $8F91F7														; run original code for ridley

door_ptr:
	db $B8, $AD														; door out pointer
