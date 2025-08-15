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
!trig = $48
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

org $84C842
%export(gray_door_facing_left)
org $84C848
%export(gray_door_facing_right)
org $84C84E
%export(gray_door_facing_up)
org $84C854
%export(gray_door_facing_down)

org $84baf4                     ; rewrite vanilla BT PLM to use generic gray door inst list and gain a little space
%export(bt_door_facing_right)
        dw $c794, instr_list_gray_door_facing_right, setup_bt_door_facing_right

org $84ba4c
setup_bt_door_facing_right:
        dw $0002,$A683          ; wait 2 frames
        dw instr_btcheck, setup_bt_door_facing_right
        dw $0026,$A683          ; wait 38 frames
.wait_clear:
        dw $0002, $A683    ; Wait for Samus not to be in the doorway (to avoid getting stuck)
        dw left_doorway_clear, .wait_clear
        dw $8C19 : db $08    ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002, $A6FB
        dw $0002, $A6EF
        dw $0002, $A6E3
        dw $0001, $A6D7
        dw $8724,instr_list_gray_door_facing_right

setup_bt_door_facing_left:
        dw $0002,$A677          ; wait 2 frames
        dw instr_btcheck, setup_bt_door_facing_left
        dw $0026,$A677          ; wait 38 frames
.wait_clear:
        dw $0002, $A677    ; Wait for Samus not to be in the doorway (to avoid getting stuck)
        dw right_doorway_clear, .wait_clear
        dw $8C19 : db $08    ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002, $A6CB
        dw $0002, $A6BF
        dw $0002, $A6B3
        dw $0001, $A6A7
        dw $8724,instr_list_gray_door_facing_left

setup_bt_door_facing_up:
        dw $0002,$A68F          ; wait 2 frames
        dw instr_btcheck, setup_bt_door_facing_up
        dw $0028,$A68F          ; wait 40 frames
        dw $8C19 : db $08    ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002,$A72B
        dw $0002,$A71F
        dw $0002,$A713
        dw $0001,$A707
        dw $8724,instr_list_gray_door_facing_up

warnpc $84bad1

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

%export(bt_door_facing_left)
        dw $c794, instr_list_gray_door_facing_left, setup_bt_door_facing_left

%export(bt_door_facing_up)
        dw $c794, instr_list_gray_door_facing_up, setup_bt_door_facing_up
%freespaceEnd($84f0bf)

%freespaceStart($84f830)
%export(bt_door_facing_down)
        dw $c794, instr_list_gray_door_facing_down, setup_bt_door_facing_down

setup_bt_door_facing_down:
        dw $0002,$A69B          ; wait 2 frames
        dw instr_btcheck, setup_bt_door_facing_down
        dw $0028,$A69B          ; wait 40 frames
        dw $8C19 : db $08    ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002,$A75B
        dw $0002,$A74F
        dw $0002,$A743
        dw $0001,$A737
        dw $8724,instr_list_gray_door_facing_down

instr_btcheck:
    jsr btcheck : BNE +
    INY : INY
    RTS
+
    LDA $0000,y : TAY
    RTS

btcheck:
    lda !current_room : cmp #!BT_room : beq .bt
.other:
    lda !trig : cmp #!trig_marker : bra .end
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

;;; Check if Samus is away from the left door (X position >= $25)
left_doorway_clear:
    lda $0AF6
    cmp #$0025
    bcc .not_clear
    iny
    iny
    rts
.not_clear:
    lda $0000,y
    tay
    rts

;;; Check if Samus is away from the right door (X position < room_width - $24)
right_doorway_clear:
    lda $07A9  ; room width in screens
    xba        ; room width in pixels
    clc
    sbc #$0024
    cmp $0AF6
    bcc .not_clear
    iny
    iny
    rts
.not_clear:
    lda $0000,y
    tay
    rts


print "84 end: ", pc
%freespaceEnd($84f8bf)

;;;;;;;;
;;; Add hijacks to trigger BT-type doors to close when boss takes a hit:
;;;;;;;;

org $A7DD42
    jsl phantoon_hurt
    nop : nop

org $A7B374
    jsl kraid_hurt

org $A5954D
    jsl draygon_hurt
    nop : nop

; The Ridley "time frozen AI" (during reserve trigger) falls through to the hurt AI.
; But we don't want it to trigger the gray door to close, so we make it skip over that part:
org $A6B291
    jsl ridley_time_frozen
    bra ridley_odd_frame_counter

warnpc $A6B297

org $A6B2BA
ridley_odd_frame_counter:

org $A6B297
    jsl ridley_hurt
    nop : nop

org $AAD3BA
    jsl golden_torizo_hurt
    nop : nop

org $A4868A
    jsl crocomire_hurt

; Botwoon doesn't have its own hurt AI (it just uses the common enemy hurt AI),
; so we use its shot AI and check if its full health.
org $B3A024
    jsl botwoon_shot

; Spore Spawn doesn't have its own hurt AI (it just uses the common enemy hurt AI),
; so we use its shot AI and check if its full health.
org $A5EDF3
    jsl spore_spawn_shot
    nop : nop

; free space in any bank
%freespaceStart($85cf30)
phantoon_hurt:
    lda #!trig_marker : sta !trig
    ; run hi-jacked instructions
    lda $0F9C
    cmp #$0008
    rtl

kraid_hurt:
    lda #!trig_marker : sta !trig
    ; run hi-jacked instruction
    lda $7E782A
    rtl

draygon_hurt:
    lda #!trig_marker : sta !trig
    ; run hi-jacked instruction
    ldy #$A277
    ldx $0E54
    rtl

ridley_time_frozen:
    ; run hi-jacked instructions
    lda #$0001
    sta $0FA4
    ; there's nothing more we need to do.
    ; We just needed to make space for the "BRA" instruction that comes after returning.
    rtl

ridley_hurt:
    lda #!trig_marker : sta !trig
    ; run hi-jacked instruction
    lda $0FA4
    and #$0001
    rtl

botwoon_shot:
    lda $0F8C  ; Enemy 0 health
    cmp #3000  ; Check if Botwoon is full health
    bcs .miss
    lda #!trig_marker : sta !trig
.miss
    ; run hi-jacked instruction
    lda $7E8818,x
    rtl

spore_spawn_shot:
    lda $0F8C  ; Enemy 0 health
    cmp #960   ; Check if Spore Spawn is full health
    bcs .miss
    lda #!trig_marker : sta !trig
.miss
    ; run hi-jacked instructions
    ldx $0E54
    lda $0F8C,x
    rtl

crocomire_hurt:
    lda #!trig_marker : sta !trig
    ; run hi-jacked instruction
    jsl $A48B5B
    rtl

print "85 end: ", pc
%freespaceEnd($85cf9f)

; Free space in bank $AA
%freespaceStart($AAF7D3)
golden_torizo_hurt:
    lda #!trig_marker : sta !trig
    ; run hi-jacked instruction
    ldx $0E54
    jsr $C620
    rtl

print "aa end: ", pc
%freespaceEnd($AAF7FF)
