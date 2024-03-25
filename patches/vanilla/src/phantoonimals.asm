arch snes.cpu
lorom

incsrc "macros.asm"


org $83ADA0
door_to_parlor:
	db $FD, $92, $00, $05, $3E, $26, $03, $02, $00, $80, $A2, $B9	; door to parlor
door_to_phantoon:
	db $13, $CD, $40, $04, $01, $06, $00, $00, $00, $80, $00, $00	; door to bt, changed to ghost
door_from_phantoon:
	db $79, $98, $40, $05, $2E, $06, $02, $00, $00, $80, $00, $00	; ghost exit, changed to pre-bt
	
org $8F98DC
	dw setup_asm_bt			; setup asm pointer for pre-bt room

org $8FCD3D
	dw setup_asm_phantoon		; setup asm pointer for ghost
	
org $8FF000
door_ptr_bt:
	dw door_to_parlor               ; door out pointers
        dw door_to_phantoon
	
org $8FF006
setup_asm_bt:
        ; reset boss flags
	LDA #$0000
        STA $7ED829
	STA $7ED82B
	LDA #door_ptr_bt		; load door pointer
	STA $7E07B5			; change door out pointer
	JML $8F91BB			; run original code

setup_asm_phantoon:
	LDA $7ED820 			; loads event flags
	BIT #$4000  			; checks for escape flag set
	BEQ quit
	lda #$0000
	sta $7ED8C0
	LDA #door_ptr_phantoon		; load door pointer
	STA $7E07B5			; change door out pointer
	JML $8FC8D0			; run original code
	
quit:
	JML $8FC8D0			; run original code

;;; need to relocate this as it collides with plm spawn table
door_ptr_phantoon:
	dw door_from_phantoon		; door out pointer
