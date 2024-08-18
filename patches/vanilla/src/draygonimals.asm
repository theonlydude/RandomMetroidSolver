arch snes.cpu
lorom

org $83ADA0
	db $FD, $92, $00, $05, $3E, $26, $03, $02, $00, $80, $A2, $B9	; door to parlor
	db $60, $DA, $40, $04, $01, $16, $00, $01, $00, $80, $00, $00	; door to bt, changed to draygon
	db $79, $98, $40, $05, $2E, $06, $02, $00, $00, $80, $00, $00	; draygon 00 bts door left
	
org $8F98DC
	dw setup_bt 													; setup asm pointer for pre-bt room

org $8FDA8A
	dw setupdray														; setup asm pointer for draygon

org $8FF000
	db $A0, $AD, $AC, $AD											; door out pointer for pre-bt
	
org $8FF006
setup_bt:
        ; reset boss flags
	LDA #$0000
        STA $7ED829
	STA $7ED82B
	LDA #$F000														; load door pointer
	STA $7E07B5														; change door out pointer
	JML $8F91BB														; run original code
	
setupdray:
	LDA $7ED820 													; loads event flags
	BIT #$4000  													; checks for escape flag set
	BEQ quit
	LDA #door_ptr														; load door pointer
	STA $7E07B5														; change door out pointer
	LDA #$FFFF
	STA $7E1CD5														; move top right grey door PLM far away
	LDA #$80AE : STA $7F01BE
	LDA #$80CE : STA $7F01FE
	LDA #$88CE : STA $7F023E
	LDA #$88AE : STA $7F027E										; change top right door tiles to grey
	PHP
	SEP #$20
	LDA #$00
	STA $7F66C2 : STA $7F66E2 
	STA $7F6702 : STA $7F6722										; change door bts of bottom right door in dray
	REP #$20
	PLP
	JML $8FC8DD														; run original code for draygon
	
quit:
	JML $8FC8DD

door_ptr:
	db $B8, $AD														; door out pointer
	

