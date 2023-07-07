;;; stats hijacks and tracking
;;;
;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

incsrc "sym/base.asm"

;;; -------------------------------
;;; CONSTANTS ;;;
;;; -------------------------------

incsrc "constants.asm"

;; Temp variables
!door_timer_tmp = $7fff00
!door_adjust_tmp = $7fff02
!add_time_tmp = $7fff04
!region_timer_tmp = $7fff06
!region_tmp = $7fff08
!add_time_32_tmp_lo = $7fff0e
!add_time_32_tmp_hi = $7fff1a

;; pause menu time stat RAM
!pause_timer_idx = #$ff0a
!pause_timer_lo = $7fff0a
!pause_timer_hi = $7fff0c

;;; -------------------------------
;; HIJACKS
;;; -------------------------------

;; Samus hit a door block (Gamestate change to $09 just before hitting $0a)
org $82e176
    jml door_entered

;; Samus gains control back after door (Gamestate change back to $08 after door transition)
org $82e764
    jml door_exited

org $89AD0A
    jsl touched_ceres_elevator

;; Door starts adjusting
org $82e309
    jml door_adjust_start

;; Door stops adjusting
org $82e34c
    jml door_adjust_stop

;; samus is dead
org $82DCD8
    jsl death
    nop
    nop

;; timer is up (equivalent to death)
org $828423
    jsl time_up
    nop
    nop

;; update current region stat
org $82DEFD
	jml load_state

;; Firing uncharged beam
org $90b911
    jml uncharged_beam
org $90b92a
    jml uncharged_beam
org $90bd5f
    jml hyper_shot

;; Firing charged beam
org $90b9a1
    jml charged_beam

;; Firing SBAs
org $90ccde
    jmp fire_sba_local

;;Missiles/supers fired
org $90beb7
    jml missiles_fired

;;Bombs/PBs laid
org $90c107
    jml bombs_laid

org $90f800
fire_sba_local:
    jml fire_sba

;; screen finished fading out
org $828cea
    jmp pausing_local

;; screen starts fading in
org $82939c
    jmp resuming_local

;; remapped at begining of $82 free space
org $82f70E
pausing_local:
    jml pausing
resuming_local:
    jml resuming

;; Hijack when samus is in the ship and ready to leave the planet
org $a2ab0d
	jsl game_end
	nop
	nop

;; skip lag count during message box display
org $858086
        JSR SetMessageBoxFlag
org $8580B7
        JSR UnsetMessageBoxFlag

;; -------------------------------
;; CODE (using bank A1 free space)
;; -------------------------------
org $a1ec00
update_and_store_region_time:
	phx
	jsr update_region_time
	jsr store_region_time
	plx
	rtl

;; Helper function to add a time delta, X = stat to add to, A = value to check against
;; This uses 4-bytes for each time delta
add_time:
    sta !add_time_tmp
    lda !timer1
    sec
    sbc !add_time_tmp
    sta !add_time_tmp
    txa
    jsl base_load_stat
    clc
    adc !add_time_tmp
    bcc +
    jsl base_store_stat    ;; If carry set, increase the high bits
    inx
    txa
    jsl base_inc_stat
+
    jsl base_store_stat
    rts

;; same as above, using 32bits date for couting long times (> 65535 frames, ~18min)
;; X = offset in bank 7F for 32-bit tmp var, Y = stat to add to
add_time_32:
    ;; first, do the 32-bit subtraction
    lda $7f0000,x
    sta !add_time_32_tmp_lo
    inx
    inx
    lda $7f0000,x
    sta !add_time_32_tmp_hi
    sec				;; set carry for borrow purpose
    lda !timer1
    sbc !add_time_32_tmp_lo	;; perform subtraction on the LSBs
    sta !add_time_32_tmp_lo
    lda !timer2			;; do the same for the MSBs, with carry
    sbc !add_time_32_tmp_hi
    sta !add_time_32_tmp_hi
    ;; add to current 32 bit stat value (don't use load_stat/store_stat for shorter code)
    tya
    asl
    tax
    lda !stats_ram,x
    clc				;; clear carry
    adc !add_time_32_tmp_lo	;; add LSBs
    sta !stats_ram,x
    inx
    inx
    lda !stats_ram,x
    adc !add_time_32_tmp_hi	;; add the MSBs using carry
    sta !stats_ram,x
    rts

;; ran when loading state header, to have up to date region stat
load_state:
    pha
    phx
    ;; init region timer tmp if needed
    lda !region_tmp
    bne +
    jsr store_region_time
+
    ;; Store (region*2) + stats_regions to region_tmp.(region == graph area, found in state header)
    lda $7e07bb
    tax
    lda $8f0010,x : and #$00ff
    asl
    clc
    adc !stat_rta_regions
    sta !region_tmp
    plx
    pla
    ;; run hijacked code and return
    and #$00ff
    asl
    jml $82DF01

;; Samus hit a door block (Gamestate change to $09 just before hitting $0a)
door_entered:
    ;; save last stats to resist power cycle
    jsl base_save_last_stats
    ;; Number of door transitions
    lda !stat_nb_door_transitions
    jsl base_inc_stat
    ;; update time spent in current region
    ;; (time spent in door transition will count as part
    ;; of destination area)
    jsl update_and_store_region_time
    ;; Save RTA time to temp variable
    lda !timer1
    sta !door_timer_tmp
    ;; Run hijacked code and return
    plp
    inc !game_state
    jml $82e1b7

update_region_time:
    ;; Store time spent in last room/area unless region_tmp is 0
    lda !region_tmp
    beq +
    tax
    lda !region_timer_tmp
    jsr add_time
+
    rts
store_region_time:
    ;; Store the current frame and the current region to temp variables
    lda !timer1
    sta !region_timer_tmp
    rts

;; Samus gains control back after door (Gamestate change back to $08 after door transition)
door_exited:
    ;; Increment saved value with time spent in door transition
    lda !door_timer_tmp
    ldx !stat_rta_door_transitions
    jsr add_time

    ;; Run hijacked code and return
    lda #$0008
    sta !game_state
    jml $82e76a

;; Door adjust start
door_adjust_start:
    lda !timer1
    sta !door_adjust_tmp ;; Save RTA time to temp variable

    ;; Run hijacked code and return
    lda #$e310
    sta $099c
    jml $82e30f

;; Door adjust stop
door_adjust_stop:
    lda !door_adjust_tmp
    inc ;; Add extra frame to time delta so that perfect doors counts as 0
    ldx !stat_rta_door_align
    jsr add_time

    ;; Run hijacked code and return
    lda #$e353
    sta $099c
    jml $82e352

;; samus is dead
death:
    jsr count_death
    ;; hijacked code
    stz $18aa
    inc !game_state
    rtl

;; timer is up (equivalent to death)
time_up:
    jsr count_death
    ;; hijacked code
    lda #$0024
    sta !game_state
    rtl

count_death:
    jsr update_region_time
    lda #$0000
    sta !region_tmp
    lda !stat_deaths
    jsl base_inc_stat
    jsl base_save_last_stats
    rts

;; uncharged Beam Fire
uncharged_beam:
    sta $0ccc ;; execute first part of hijacked code, to freely use A

    lda !stat_uncharged_shots
    jsl base_inc_stat
    ;; do the vanilla check, done in both auto and normal fire
    pla
    bit #$0001
    bne +
    ;; jump back to common branches for auto and normal fire
    jml $90b933
+
    jml $90b94c

hyper_shot:
    sta $0cd0 ;; execute first part of hijacked code, to freely use A

    lda !stat_uncharged_shots
    jsl base_inc_stat

    plp ;; execute last instr of hijacked code
    jml $90bd63 ;; return

;; Charged Beam Fire
charged_beam:
    lda !stat_charged_shots
    jsl base_inc_stat
    ;; Run hijacked code and return
    LDX #$0000
    LDA $0c2c, x
    JML $90b9a7

;; Firing SBAs : hijack the point where new qty of PBs is stored
fire_sba:
    ;; check if SBA routine actually changed PB count: means valid beam combo selected
    cmp $09ce
    beq .end
    pha
    lda !stat_SBAs
    jsl base_inc_stat
    pla
    ;; Run hijacked code and return
.end:
    sta $09ce
    jml $90cce1

;;MissilesSupers used
missiles_fired:
    lda $09d2
    cmp #$0002
    beq .super
    dec $09c6
    lda !stat_missiles
    jsl base_inc_stat
    bra .end
.super:
    dec $09ca
    lda !stat_supers
    jsl base_inc_stat
.end:
    jml $90bec7

;;bombs/PBs laid
bombs_laid:
    lda $09d2			;; HUD sleection index
    cmp #$0003
    beq .power_bomb
    lda !stat_bombs
    bra .end
.power_bomb:
    lda !stat_PBs
.end:
    jsl base_inc_stat
    ;;run hijacked code and return
    lda $0cd2
    inc
    jml $90c10b

;; stopped fading out, game state about to change to 0Dh
pausing:
    ;; save last stats to resist power cycle
    jsl base_save_last_stats
    ;; Save RTA time to temp variable
    lda !timer1
    sta !pause_timer_lo
    lda !timer2
    sta !pause_timer_hi
    ;; don't count time spent in pause in region counters
    jsr update_region_time
    ;; run hijacked code and return
    inc !game_state
    jml $828ced

;; start fading in, game state about to change to 12h
resuming:
    ;; add time spent in pause to stat at 27-28 spot
    phy ;; XXX don't know whether Y is actually used in vanilla code, save it for safety
    ldy !stat_rta_menu
    ldx !pause_timer_idx
    jsr add_time_32
    ply
    ;; don't count  time spent in pause in region counters
    jsr store_region_time
    ;; save last stats to resist power cycle
    jsl base_save_last_stats
    ;; run hijacked code and return
    inc !game_state
    jml $82939f

;; correctly count Ceres and Crateria timers
touched_ceres_elevator:
	JSL $90F084 ;; hijacked code
	jsr update_region_time
	lda #$0000
	sta !region_tmp
	rtl

;; Game has ended, save RTA timer to RAM and copy all stats to SRAM a final time
game_end:
    ;; update region time (will be slightly off, but avoids dealing with negative substraction result, see below)
    jsl update_and_store_region_time
    ;; Subtract frames from pressing down at ship to this code running
    lda !timer1
    sec
    sbc #$013d
    sta !timer1
    lda #$0000  ;; if carry clear this will subtract one from the high byte of timer
    sbc !timer2

    ;; save timer in stats
    lda !timer1
    sta !stats_timer
    lda !timer2
    sta !stats_timer+2

    ;; save stats to SRAM
    lda #$0001
    jsl base_save_stats

    ;; don't count lag during takeoff
    inc !skip_lag_count_flag

    ;; hijacked code
    stz $0df2
    lda #$000a
    rtl

warnpc $a1efff

org $85cf00
SetMessageBoxFlag:
        STA.w $1C1F ; What we wrote over
        INC.w !skip_lag_count_flag
        RTS

UnsetMessageBoxFlag:
        JSR.w $80FA ; What we wrote over
        STZ.w !skip_lag_count_flag
        RTS

print "b85 end: ", pc
warnpc $85cf0f
