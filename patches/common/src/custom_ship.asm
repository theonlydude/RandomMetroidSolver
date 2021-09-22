;;; Compile with "asar" (https://github.com/RPGHacker/asar/releases)

lorom

!invisible_flag = $7fff42
;;; relative to the ship. midway between top and bottom samus position
!invisible_offset = #$0018

org $9085ec
	jml handle_invisible_flag

org $9085f1
visibility_checks:

org $908606
visible:

org $908647
invisible:

org $A2AA69
	jsl lower_samus

org $A2AB7A
	jsl raise_samus_save

org $A2A95C
	jsl raise_samus_land

org $a1f800
handle_invisible_flag:
	lda !invisible_flag : bne .invisible
	lda $18aa : beq .checks	; hijacked vanilla check
	jml visible
.invisible:
	jml invisible
.checks:
	jml visibility_checks

lower_samus:
	clc : adc #$0002	; hijacked code
	pha			; save result
	lda $12
	sec : sbc.l !invisible_offset
	bra check_invisible_offset

raise_samus_save:
	sec : sbc #$0002	; hijacked code
	bra raise_samus
raise_samus_land:
	sec : sbc #$0001	; hijacked code
raise_samus:
	pha			; save result
	lda $12
	clc : adc.l !invisible_offset
check_invisible_offset:
	sta !invisible_flag	; use flag RAM as tmp value
	pla : pha
	cmp !invisible_flag : bpl .end
	lda #$0000 : sta !invisible_flag
.end:
	pla
	rtl
