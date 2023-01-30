arch snes.cpu
lorom

org $83ADA0
	db $FD, $92, $00, $05, $3E, $26, $03, $02, $00, $80, $A2, $B9	; door to parlor
	db $2B, $B6, $40, $04, $01, $06, $00, $00, $00, $80, $00, $00	; door to metal pirates
	db $79, $98, $40, $05, $2E, $06, $02, $00, $00, $80, $00, $00	; to pre-bt

org $8F98DC
	db $06, $F0 													; setup asm pointer for pre-bt room
	
org $8FF000
	db $A0, $AD, $AC, $AD											; door out pointer for pre-bt
	
org $8FF006
	LDA #$F000														; load door pointer
	STA $7E07B5														; change door out pointer
	JML $8F91BB														; run original code
	
org $8FB650
	db $18, $F0														; setup asm pointer for metal pirates
	
org $8FF018
	LDA $7ED820 													; loads event flags
	BIT #$4000  													; checks for escape flag set
	BEQ quit
	LDA #$0000
	STA $7ED8BC														; resets grey door for metal pirates
	LDA #door_ptr														; load door pointer
	STA $7E07B5														; change door out pointer
	JML $8F91F7														; run original code for ridley
	
quit:
RTS
	
door_ptr:
	db $B8, $AD, $AC, $AD											; door out pointer for metal pirates room
	
