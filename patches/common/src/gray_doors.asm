;;; Add bomb torizo-type doors for all directions, and improve them to change trigger conditions.
;;; 
;;; In BT room: Fix bomb torizo awakening, wakes up on item acquisition instead of bombs collected
;;; (original patch by PJBoy, adapted for VARIA)
;;; In other rooms: check a temporary RAM flag (lifetime being the current room) to trigger, and use
;;; that to close when the boss in the room is hurt
;;; (original patch by Maddo for Map Rando, simplified/adapted for VARIA)

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

;; vanilla gray doors
org $84bed9
instr_list_gray_door_facing_right:
org $84be70
instr_list_gray_door_facing_left:
org $84bf42
instr_list_gray_door_facing_up:
org $84bfab
instr_list_gray_door_facing_down:

org $84baf4                     ; rewrite vanilla BT PLM to use generic gray door inst list and gain a little space
%export(bt_door_facing_right)
        dw $c794, instr_list_gray_door_facing_right, setup_bt_door_facing_right

org $84ba4c
setup_bt_door_facing_right:
org $84BA6D
        dw instr_list_gray_door_facing_right ; overwrite last jump in BT door facing right setup func

;; overwrite now unused vanilla BT door instr list, and some unused setup code for it
instr_btcheck:
        jsr btcheck : BNE +
	INY : INY
        RTS
+
	LDA $0000,y : TAY
        RTS

setup_bt_door_facing_left:
        dw $0002,$A683          ; wait 2 frames
        dw instr_btcheck, setup_bt_door_facing_left
        dw $0028,$A683          ; wait 40 frames
        dw $8C19 : db $08    ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002, $A6CB
        dw $0002, $A6BF
        dw $0002, $A6B3
	dw $0001, $A6A7
        dw $8724,instr_list_gray_door_facing_left

setup_bt_door_facing_up:
        dw $0002,$A683          ; wait 2 frames
        dw instr_btcheck, setup_bt_door_facing_up
        dw $0028,$A683          ; wait 40 frames
        dw $8C19 : db $08    ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002,$A72B
        dw $0002,$A71F
        dw $0002,$A713
        dw $0001,$A707
        dw $8724,instr_list_gray_door_facing_up

setup_bt_door_facing_down:
        dw $0002,$A683          ; wait 2 frames
        dw instr_btcheck, setup_bt_door_facing_down
        dw $0028,$A683          ; wait 40 frames
        dw $8C19 : db $08    ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002,$A75B
        dw $0002,$A74F
        dw $0002,$A743
        dw $0001,$A737
        dw $8724,instr_list_gray_door_facing_down

%export(bt_door_facing_left)
        dw $c794, instr_list_gray_door_facing_left, setup_bt_door_facing_left

%export(bt_door_facing_up)
        dw $c794, instr_list_gray_door_facing_up, setup_bt_door_facing_up

warnpc $84baf4

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

%freespaceStart($84f0b0)
%export(bt_wake_on_item)        ; VARIA tweaks flag
        db $00

%export(bt_door_facing_down)
        dw $c794, instr_list_gray_door_facing_down, setup_bt_door_facing_down
%freespaceEnd($84f0bf)

%freespaceStart($84f830)
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
%freespaceEnd($84f86f)
