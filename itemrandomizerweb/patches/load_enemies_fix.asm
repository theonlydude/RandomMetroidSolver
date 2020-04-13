;;; fixes enemies loading so that when there are no enemies, some values are still reset
;;; (used to make 0 enemy permanently blinking grey doors)

arch snes.cpu
lorom


org $a08ae5
	;; hijack enemy list empty check
	jsr check_empty

org $a0f820
check_empty:
	cmp #$ffff		; original empty enemy list check
	bne .end		; it not empty: return
	stz $0e4e		; nb of enemies in the room = 0
	stz $0e52		; nb of enemies needed to clear the room = 0
.end:
	rts

warnpc $a0f830
