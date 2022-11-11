;;; To apply on top of some custom ships where samus is visible inside the ship
;;; 
;;; Compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

lorom
arch 65816

!temp = $0743		; from pause screen RAM

;;; relative to the ship. midway between top and bottom samus position
!invisible_offset = #$0018

org $A2A814
	jsl landing_descent

org $A2AA69
	jsl lower_samus

org $A2AB7A
	jsl raise_samus_save

org $A2A95C
	jsl raise_samus_land

org $a1f900
landing_descent:
	jsr hide_samus
	;; hijacked code
	lda $0AFC
	clc
	rtl

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
	sta !temp
	pla : pha
	cmp !temp : bmi .visible
	jsr hide_samus
	bra .end
.visible:
	jsr show_samus
.end:
	pla
	rtl

hide_samus:
	;; set en empty samus draw handler
	LDA #$E90E : STA $0A5C
	rts

show_samus:
	;; restore default samus draw handler
	LDA #$EB52 : STA $0A5C
	rts

warnpc $a1f97f
