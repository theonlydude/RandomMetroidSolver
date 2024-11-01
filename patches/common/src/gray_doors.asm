;;; Add bomb torizo-type doors for all directions, and improve them to change trigger conditions.
;;; 
;;; In BT room: Fix bomb torizo awakening, wakes up on item acquisition instead of bombs collected
;;; (original patch by PJBoy, adapted for VARIA)
;;; In other rooms: check a temporary RAM flag (lifetime being the current room) to trigger, and use
;;; that to close when the boss in the room is hurt
;;; (original patch by Maddo for Map Rando, adapted for VARIA)

lorom
arch 65816

incsrc "constants.asm"
incsrc "macros.asm"

incsrc "sym/objectives_options.asm"

!current_room = $079b
!BT_room = $9804

;; reuse decompression params RAM to ensure we're overwritten when leaving the room
!trig_addr = $48
;; this would mean bank FF and addr starting with 00 in decomp routine so this is impossible enough that we can use this value as marker
!trig_marker = $ff00

; Grey door
org $84BA6F
        jsr btcheck : BNE +
	INY : INY
        RTS
+
	LDA $0000,y : TAY
        RTS

warnpc $84ba7f

; Statue
org $84D33B
	jsr btcheck : BNE +
        ;; vanilla code to wake plm
	LDA #$0001 : STA $7EDE1C,x
	INC $1D27,x : INC $1D27,x
	LDA #$D356 : STA $1CD7,x
+
	RTS

warnpc $84D357

%freespaceStart($84f830)
%export(bt_wake_on_item)        ; VARIA tweaks flag
        db $00

btcheck:
        lda !current_room : cmp #!BT_room : beq .bt
.other:
        lda !trig_addr : cmp #!trig_marker : bra .end
.bt:
        ;; check if VARIA tweaks enabled
        lda bt_wake_on_item : and #$00ff : bne .varia_tweaks
        ;; vanilla check, wake if Samus has bombs
        lda !collected_items_mask : and #$1000 : cmp #$1000 : bra .end
.varia_tweaks:
        ;; check if BT should never wake up
        lda.l objectives_options_settings_flags : bit.w #!option_BT_sleep_mask : bne .end
        ;; return 0 flag if PLM 1 is deleted
        LDA $1C83
.end:
        rts

print "b84 end: ", pc
%freespaceEnd($84f8ff)
