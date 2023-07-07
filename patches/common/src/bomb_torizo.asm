;;; Fix bomb torizo awakening, wakes up on item acquisition instead of bombs collected
;;; original patch by PJBoy, adapted for VARIA

lorom
arch 65816

incsrc "constants.asm"

incsrc "sym/objectives_options.asm"

; Grey door
org $84BA6F ; Instruction - go to [[Y]] if Samus doesn't have bombs
	; Check if PLM 1 (vanilla bombs PLM) has been deleted instead
        jsr btcheck : BNE +
	INY : INY
        RTS
+
	LDA $0000,y : TAY
        RTS

warnpc $84ba7f

; Statue
org $84D33B ; Pre-instruction - wake PLM if Samus has bombs
	; Check if PLM 1 (vanilla bombs PLM) has been deleted instead
	jsr btcheck : BNE +
        ;; vanilla code to wake plm
	LDA #$0001 : STA $7EDE1C,x
	INC $1D27,x : INC $1D27,x
	LDA #$D356 : STA $1CD7,x
+
	RTS

warnpc $84D357

org $84f840
btcheck:
        ;; check if BT should never wake up
        lda.l objectives_options_settings_flags
        bit.w #!option_BT_sleep_mask : bne .end
        ;; PLM 1
        LDA $1C83
.end:
        rts

print "b84 end: ", pc
warnpc $84f860
