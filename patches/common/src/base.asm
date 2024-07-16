;;; VARIA boot, save/load/backup saves management (including stats), RTA timer, base stats functions
;;; 
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

math pri on

incsrc "sym/seed_display.asm"
incsrc "sym/utils.asm"

incsrc "macros.asm"

;;; -------------------------------
;;; CONSTANTS ;;;
;;; -------------------------------

incsrc "constants.asm"

;;; temp ram used
!tmp_area_sz = $00df
!temp = $0743                   ; general temp var in menus

;;; normal game SRAM
!regular_save_size = $0900      ; expanded by saveload patch (modified, A00 in original patch)
!regular_save_sram = $0010      ; after checksum
!regular_save_sram_slot0 = !regular_save_sram
!regular_save_sram_slot1 #= !regular_save_sram+!regular_save_size
!regular_save_sram_slot2 #= !regular_save_sram+!regular_save_size*2
!sram_station_info_offset = $0156 ; offset in a save file where current save station and area are stored
;;; stats SRAM
!stats_sram_sz_b #= $0080
!stats_sram_sz_w #= !stats_sram_sz_b/2
!full_stats_area_sz_b #= 2*!stats_sram_sz_b+$20   ; twice the size of stats to account for last stats + $20 extra SRAM
!stats_sram_slot0 #= !regular_save_sram+!regular_save_size*3
!stats_sram_slot1 #= !stats_sram_slot0+!full_stats_area_sz_b
!stats_sram_slot2 #= !stats_sram_slot1+!full_stats_area_sz_b
!last_stats_save_ok_off #= !full_stats_area_sz_b-4

;;; backup saves
!backup_save_data_off #= !full_stats_area_sz_b-8
!backup_sram_slot0 #= !stats_sram_slot0+!backup_save_data_off
!backup_sram_slot1 #= !stats_sram_slot1+!backup_save_data_off
!backup_sram_slot2 #= !stats_sram_slot2+!backup_save_data_off
!backup_counter = !temp
!backup_candidate = $7fff3a

;;; boot and RTA timer
;; store last save slot and used saves in unused SRAM
!last_saveslot #= $700000+!stats_sram_slot0+3*!full_stats_area_sz_b
!used_slots_mask #= !last_saveslot+2
;; SRAM magic set to seed ID to check if we ever booted the seed
!was_started_flag32 #= !last_saveslot+4
;; bitmask of which saves are locked (to know when to play the lock/unlock sound)
!locked_slots_mask #= !last_saveslot+8
;; magic value used as marker in some places
!magic_flag = $caca
;; backup RAM for timer to avoid it to get cleared at boot
!timer_backup1 = $7fffe2
!timer_backup2 = !timer_backup1+2
;; timer integrity protection
!timer_xor = $033e

;;; save-related vanilla RAM
!area_index = $079f
!load_station_index = $078b
!current_save_slot = $7e0952

;;; -------------------------------
;;; HIJACKS ;;;
;;; -------------------------------

;; vanilla array of save slots offsets in bank 70
org $81812b
slots_sram_offsets:
        dw !regular_save_sram_slot0,!regular_save_sram_slot1,!regular_save_sram_slot2

;; vanilla array of bitmasks to check used save slots
org $819af4
slots_bitmasks:

;; Patch boot to init our stuff
org $80844B
    jml boot1
org $808490
    jml boot2

;; bypass SRAM check to avoid loading 1st save at boot
org $808268
    jmp $8294

;; Patch load/save/copy
org $818000
        jmp SaveGame            ; in saveload included patch

org $818085
        jmp LoadGame            ; in saveload included patch

org $81A24A
    jsl patch_load ;; patch load from menu only

;; hijack copy routine to copy stats
org $819A66
    jsr copy_stats
;; fix save slot size in copy routine
org $819A62
        dw !regular_save_size

;; patch clear routine to update used save slots bitmask in SRAM, and fix save slot size
org $819cc3
	jsr patch_clear
org $819CBF
        dw !regular_save_size

;; hijack menu display to show save area instead of energy if backup saves are enabled
org $81A09B
	jsr menu_show_save_data

;; Hijack loading new game to reset stats
org $82805f
    jsl clear_values

;; end gamestate hijack to resync IGT from RTA that stopped ~6 seconds earlier
org $8284D3
        jsl igt_end

;;; draw locked file status on top of samus helmet in load menu
org $819e25
        jsl draw_lock

;;; control selected save locked status
org $81A1DB
        jsr control_lock

;;; draw help for lock control
org $819FEA
        jsr draw_lock_help

;;; hijack load state header to put area ID/minimap room type ID in RAM
org $82DEF7
        jsl load_state : nop : nop

;;; -------------------------------
;;; CODE ;;;
;;; -------------------------------

;;; -------------------------------
;;; RTA timer
;; Patch NMI to skip resetting 05ba and instead use that as an extra time counter
org $8095e5
nmi:
    ;; copy from vanilla routine without lag counter reset
    ldx #$00
    stx $05b4
    ldx $05b5
    inx
    stx $05b5
    inc $05b6
.nolag:
    rep #$30
    jmp .inc
warnpc $809602
org $809602 ; lag handling: increment lag stat in main gameplay
    lda !game_state : cmp.w #8 : bne .nolag
    lda !skip_lag_count_flag : bne .nolag
    rep #$30
    jmp .lag
warnpc $809616
    ;; handle 32 bit counter :
org $808FA3 ;; overwrite unused routine
.lag:
    ;; don't count lag on 32 bits, as 18+ minutes of it seems unlikely
    inc !timer_lag
.inc:
    ;; actually increment 32-bit timer
    inc !timer1
    bne .end
    inc !timer2
.end:
    ;; timer integrity protection
    lda !timer1
    eor !timer2
    sta !timer_xor
    ply
    plx
    pla
    pld
    plb
.rti:
    rti

warnpc $808FC1 ;; next used routine start

;;; -------------------------------
;;; Boot
;; Patch boot to init stuff
%freespaceStart($80fe00)
boot1:
    ;; check timer integrity: if not ok disable soft reset flag
    lda !timer1
    eor !timer2
    cmp !timer_xor
    beq +
    lda #!magic_flag
    sta !softreset
+
    lda #$0000
    sta !timer_backup1
    sta !timer_backup2
    ;; check if first boot ever by checking magic 32-bit value in SRAM
print "first boot check: ", pc
    lda !was_started_flag32
    cmp seed_display_seed_value
    bne .first
    lda !was_started_flag32+2
    cmp seed_display_seed_value+2
    beq .check_reset
.first:
    ;; no game was ever saved:
    ;; init used save slots bitmasks
    lda #$0000
    sta !used_slots_mask
    sta !locked_slots_mask
    ;; clear all save files by corrupting checksums
    ldx	#$0005
    lda #!magic_flag
.clear_loop:
    sta $701ff0,x
    sta $701ff8,x
    sta $700000,x
    sta $700008,x
    dex
    dex
    bpl .clear_loop
    ;; write magic number
    lda seed_display_seed_value
    sta !was_started_flag32
    lda seed_display_seed_value+2
    sta !was_started_flag32+2
    ;; skip soft reset check, since it's the 1st boot
    bra .cont
.check_reset:
    ;; check if special soft reset: dec reset count if set
    lda !softreset
    cmp #!dec_reset_flag : bne +
    lda !stat_resets : jsl dec_stat
    ;; set it back to normal soft reset
    lda #!reset_flag : sta !softreset
+
    cmp #!reset_flag
    bne .cont
    lda !timer1
    sta !timer_backup1
    lda !timer2
    sta !timer_backup2
.cont:
    ;; vanilla init stuff (will overwrite our timer, hence the backup)
    ldx #$1ffe
    lda #$0000
-
    stz $0000, x
    dex
    dex
    bpl -
    ;; restore timer
    lda !timer_backup1
    sta !timer1
    lda !timer_backup2
    sta !timer2
    ;; resume
    jml $808455

boot2:
    ;; backup the timer again, game likes to clear this area on boot
    lda !timer1
    sta !timer_backup1
    lda !timer2
    sta !timer_backup2
    ;; vanilla init stuff
    ldx #$1ffe
-
    stz $0000,x
    stz $2000,x
    stz $4000,x
    stz $6000,x
    stz $8000,x
    stz $a000,x
    stz $c000,x
    stz $e000,x
    dex
    dex
    bpl -
    ;; restore timer
    lda !timer_backup1
    sta !timer1
    lda !timer_backup2
    sta !timer2
    ;; clear temp variables
    ldx #!tmp_area_sz
    lda #$0000
-
    sta $7fff00, x
    dex
    dex
    bpl -
    ;; resume vanilla code
    jml $8084af

print "bank 80 end: ", pc
%freespaceEnd($80feff)

;;; -------------------------------
;;; Save files management : adds timer, stats and backup features to save files
%freespaceStart($81ef20)

;; stats SRAM offsets lookup tables
stats_sram_offsets:
    dw !stats_sram_slot0
    dw !stats_sram_slot1
    dw !stats_sram_slot2

last_stats_sram_offsets:
    dw !stats_sram_slot0+!stats_sram_sz_b
    dw !stats_sram_slot1+!stats_sram_sz_b
    dw !stats_sram_slot2+!stats_sram_sz_b

;;; In: A = save file
;;; Out: X = stats data offset in bank 70
macro statsIndex()
        asl : tax
        lda.l stats_sram_offsets, x : tax
endmacro

;;; In: A = save file
;;; Out: X = last stats data offset in bank 70
macro lastStatsIndex()
        asl : tax
        lda.l last_stats_sram_offsets, x : tax
endmacro

;; save slot data:
;; slot ID, slot bitmask, SRAM addr for backup data, SRAM addr for load station info
;; (SRAM addresses are offsets in bank $70)
slots_data:
slot0_data:
	dw $0000,$0001,!backup_sram_slot0,!regular_save_sram_slot0+!sram_station_info_offset

slot1_data:
	dw $0001,$0002,!backup_sram_slot1,!regular_save_sram_slot1+!sram_station_info_offset

slot2_data:
	dw $0002,$0004,!backup_sram_slot2,!regular_save_sram_slot2+!sram_station_info_offset

;;; In: A = save file
;;; Out: X = backup data offset in bank 70
macro backupIndex()
    asl #3 : tax : lda.l slots_data+4,x : tax
endmacro

;; a save will always be performed when starting a new game (see start.asm)
new_save:
	;; set current save slot as used in SRAM bitmask
	lda !current_save_slot : asl : tax
	lda !used_slots_mask : ora.l slots_bitmasks,x : sta !used_slots_mask
	lda !locked_slots_mask : ora.l slots_bitmasks,x : sta !locked_slots_mask
	;; init backup save data :
        lda !current_save_slot
        pha
        %backupIndex()
        pla
        sta $700000,x
	;; store 0 + high bit set (player flag) as backup counter
	lda #$8000
	sta $700002,x        

	;; call save routine
	lda !current_save_slot
	jsl $818000

        ;; clear new game flag
        lda.w #0 : sta !new_game_flag
.end:
	rtl


;; backup is needed if no existing backup of current save slot
;; or last backup is at a different save station than this one
;;
;; return carry set if we need to backup the save, and we can use a
;; slot to do so.
;; sets the most suitable save slot in backup_candidate,
;; or 3 if no suitable slot found (in that case, carry is clear anyway)
is_backup_needed:
	;; save DB and set it to current bank in order to
	;; read slots data tables
	phb
	phk
	plb
	;; save X and Y as they will be used
	phx
	phy
        ;; init backup candidate with special value meaning we did no check yet
        lda #$8000 : sta !backup_candidate
	;; first, check if current save station is different from last save
	lda !current_save_slot : asl #3 : tay
	ldx slots_data+6,y
	lda $700000,x
	cmp !load_station_index
	bne .check_needed
	lda $700002,x
	cmp !area_index
	beq .no_backup
.check_needed:
	;; find out our backup counter, and save it in backup_counter
	ldx slots_data+4,y
	lda $700002,x : and #$7fff : sta !backup_counter
	;; backup_candidate will be used to store the backup slot candidate
	;; and various info as follows:
	;;
	;; eo------------ss
	;;
	;; ss: save slot usable for backup
	;; e: ss is empty
	;; o: ss contains an old backup
	;; (e and o are only use internally by check_slot to determine ss)
	lda #$0003	;; 3 is used as invalid value marker, as slots are 0 to 2
	sta !backup_candidate
	;; check all slots
	ldy #slot2_data : jsr check_slot
	ldy #slot1_data : jsr check_slot
	ldy #slot0_data : jsr check_slot
	;; clear all our work flags from backup_candidate
	lda !backup_candidate : and #$0003 : sta !backup_candidate
	;; check that we can actually backup somewhere
	cmp #$0003 : beq .no_backup
.backup:
	sec
	bra .end
.no_backup:
	clc
.end:
	ply
	plx
	plb
	rts

;; arg. Y: offset to slot data in bank 81 (DB is assumed 81)
;; sets flags and candidate in backup_candidate
check_slot:
        ;; check empty save bitmask
	lda $0002,y
	and !used_slots_mask
	;; if save empty, mark as backup candidate, with high bit (e)
	;; set to indicate it's an empty file
	bne .not_empty
	lda !backup_candidate
	and #$fffc
	ora $0000,y
	ora #$8000
	sta !backup_candidate
	bra .end
.not_empty:
	;; if not our timeline, skip
	ldx $0004,y
	lda $700000,x
	cmp.l !last_saveslot
	bne .end
	;; if locked save, skip
	lda $700002,x
	bmi .end
	;; if backup counter is different:
	cmp !backup_counter
	beq .last_backup
	;; mark as backup candidate, with 'old backup' (o) bit marked
	;; only if no (e) flag bit marked yet
	lda !backup_candidate
	bmi .end
	and #$fffc
	ora $0000,y
	ora #$4000
	sta !backup_candidate
	bra .end
.last_backup:
	;; we're here only if this save slot is the most recent backup
	lda !backup_candidate
	bit #$c000 ;; checks both e and o flags
	bne .end
	;; no better candidate yet
	and #$fffc
	ora $0000,y
	sta !backup_candidate
.end:
	rts

backup_save:
	;; increment backup counter in our save file
	lda !current_save_slot
        %backupIndex()
	lda $700002,x : inc : sta $700002,x

	;; direct page indirect addressing copy :
	;; reuse $47/$4A used in decompression routine (according to RAM map)
	;; we have to use direct page for addresses, and I'm not sure we can use
	;; the start of direct page in game as it is done in original menu
	;; routine ($00/$03)

	;; set bank $70 as source and dest banks for copy
	lda #$0070
	sta $49
	sta $4c	
	;; source slot is current one
	lda !current_save_slot : asl : tax
	lda.l slots_sram_offsets,x ;; get SRAM offset in bank 70 for slot
	sta $47
	;; destination slot is in backup_candidate
	lda !backup_candidate : asl : tax
	lda.l slots_sram_offsets,x ;; get SRAM offset in bank 70 for slot
	sta $4a
	;; copy save file
	ldy #$0000
-
	lda [$47],y
	sta [$4a],y
	iny : iny
	cpy #!regular_save_size
	bmi -
	;; copy checksum
	lda !current_save_slot : asl : tax
	lda $701ff0,x : pha
	lda $701ff8,x : pha
	lda $700000,x : pha
	lda $700008,x : pha
	lda !backup_candidate : asl : tax
	pla : sta $700008,x
	pla : sta $700000,x
	pla : sta $701ff8,x
	pla : sta $701ff0,x
	;; copy timeline ID and backup counter (stats will be automatically up to date since we save them to all necessary slots)
	lda !current_save_slot
        %backupIndex()
        lda.l $700002, x : pha
        lda.l $700000, x : pha
        lda !backup_candidate
        %backupIndex()
        pla : sta.l $700000, x
        pla : and #$7fff : sta.l $700002, x  ; clear player flag in the backup
	;; mark backup slot as used in bitmask
	lda !backup_candidate : asl : tax
	lda !used_slots_mask
	ora.l slots_bitmasks,x	;; bitmask index table in ROM
	sta !used_slots_mask
	rts

incsrc "base/saveload.asm"

;; Patch load and save routines
patch_save:                     ; called from saveload patch
	;; backup saves management:
	lda !new_game_flag : bne .save_stats
	;; check if we shall backup the save
	jsr is_backup_needed
	bcc .stats
	jsr backup_save
	;; handle timer/stats after backup
.stats:
	;; copy RTA timer to RAM stats and IGT RAM
	lda !timer1 : sta !stats_timer
	lda !timer2 : sta !stats_timer+2
        lda !timer_lag : sta !stat_rta_lag_ram
	jsl update_igt
.save_stats:
	;; save all stats
	lda #$0001
	jsl save_stats
	rts

patch_load:
    phb
    phx
    phy
    pea $7e7e
    plb
    plb
    ;; call load routine
    jsl LoadGame
    bcc .lock
    ;; new save or SRAM corrupt, place flag for new game
    lda.w #1 : sta !new_game_flag
    ;; save current timeline
    lda !current_save_slot : sta !last_saveslot
    bra .end
.lock:
    ;; mark this slot as non-backup
    lda !current_save_slot
    %backupIndex()
    lda $700002,x : ora #$8000 : sta $700002,x
.check:
    ;; check initial save slot and save it
    lda $700000,x : cmp !last_saveslot
    sta !last_saveslot
    bne .load
    ;; we're loading the same timeline that's played last
    lda !softreset
    cmp #!reset_flag
    bne .load
    ;; soft reset, use stats and timer from RAM
    lda !stat_rta_lag_ram : sta !timer_lag ; restore lag timer, as it gets cleared on boot
    bra .end_ok
    ;; TODO add menu time to pause stat and make it a general menus stat?
.load:
    ;; load stats from SRAM
    jsl load_stats
    ;; update live timer
    lda !stats_timer : sta !timer1
    lda !stats_timer+2 : sta !timer2
    lda !stat_rta_lag_ram : sta !timer_lag
.end_ok:
    ;; place marker for resets
    lda #!reset_flag
    sta !softreset
    ;; clear new game flag
    lda.w #0 : sta !new_game_flag
    ;; return carry clear
    clc
.end:
    ply
    plx
    plb
    rtl


;;; Patch copy and clear routines
copy_stats:
    ;; src slot idx = 19b7, dst slot idx = 19b9
    lda $19b7
    asl
    tax
    lda.l stats_sram_offsets,x
    sta $00
    lda $19b9
    asl
    tax
    lda.l stats_sram_offsets,x
    sta $03
    ldy #$0000
    ;; bank part for indirect long in already setup by original
    ;; routine at $02 and $05
.loop:
    lda [$00],y
    sta [$03],y
    iny
    iny
    cpy.w #!full_stats_area_sz_b
    bcc .loop
.lock:
    lda $19b9
    %backupIndex()
    lda $700002,x : ora #$8000 : sta $700002,x
    ;; set locked status
    lda $19b9 : asl : tax
    lda !locked_slots_mask : ora.l slots_bitmasks, x : sta !locked_slots_mask
.end:
    lda $19B7   ;; hijacked code
    rts

;; clear slot in used_slots_mask in SRAM
patch_clear:
	;; $19b7 hold slot being cleared
	lda $19b7
	asl
	tax
	lda.l slots_bitmasks,x	;; bitmask index table in ROM
	eor #$ffff
	and !used_slots_mask
	sta !used_slots_mask
.end:
	lda $19b7	;; hijacked code
	rts

;;; -------------------------------
;;; Stats base functions

;; clear stats on new game
clear_values:
    php
    rep #$30
    lda !new_game_flag : beq .ret

    ldx #$0000
    lda #$0000
-
    jsl store_stat
    inx
    cpx.w #!stats_sram_sz_w
    bne -

    ;; Clear RTA Timer
    lda #$0000
    sta !timer1
    sta !timer2
    ;; place marker for resets
    lda #!reset_flag
    sta !softreset
.ret:
    plp
    jsl $80a07b	;; hijacked code
    rtl

load_stats:
    phx
    phy
    ;; tries to load from last stats
    lda !current_save_slot : asl : tax
    jsr is_last_save_flag_ok
    bcc .notok
    lda.l last_stats_sram_offsets, x : tax
    bra .load
.notok:
    lda.l stats_sram_offsets, x : tax
.load:
    jsr load_stats_at
    ply
    plx
    rtl

;; arg X = index of where to load stats from in bank $70
load_stats_at:
    phb
    pea $7f7f
    plb
    plb
    ldy #$0000
.loop:
    lda $700000,x
    sta $!_stats_ram,y
    iny
    iny
    inx
    inx
    cpy.w #!stats_sram_sz_b
    bcc .loop
    plb
    rts

;; return carry flag set if flag ok
is_last_save_flag_ok:
        phx
        lda !current_save_slot
        %statsIndex()
        lda #!magic_flag : cmp.l $700000+!last_stats_save_ok_off, x
        beq .ok
        clc
        bra .end
.ok:
        sec
.end:
        plx
        rts

;; args: A = value to store
;; X and A untouched
set_last_save_ok_flag:
        phx
        pha
        lda !current_save_slot
        %statsIndex()
        pla
        sta $700000+!last_stats_save_ok_off,x
        plx
        rts

;; arg X = index of where to save stats in bank $70
save_stats_at:
    phx
    phy
    phb
    pea $7f7f
    plb
    plb
    ldy #$0000
.loop:
    lda $!_stats_ram,y
    sta $700000,x
    iny
    iny
    inx
    inx
    cpy.w #!stats_sram_sz_b
    bcc .loop
    plb
    ply
    plx
    rts

;; save stats both in standard and last areas
;; arg: A = 0 if we just want to save last stats
;;      A != 0 save all stats (save stations)
save_stats:
        phx
        phy
        pha
        ;; find all slots concerning our "timeline" (last_saveslot), and save stats everywhere
        ldy.w #3
.loop:
        dey : bmi .end
        tya : asl : tax
        lda !used_slots_mask : and.l slots_bitmasks, x
        beq .loop
        tya
        %backupIndex()
        lda $700000, x : cmp !last_saveslot : bne .loop
        pla : pha
        beq .last
        tya
        %statsIndex()
        jsr save_stats_at
.last:
        lda.w #0 : jsr set_last_save_ok_flag
        tya
        %lastStatsIndex()
        jsr save_stats_at
        lda.w #!magic_flag : jsr set_last_save_ok_flag
        bra .loop
.end:
        pla
        ply
        plx
        rtl

;; Increment Statistic (in A)
inc_stat:
    phx
    asl
    tax
    lda.l !stats_ram, x
    inc
    sta.l !stats_ram, x
    plx
    rtl

;; save last stats. to be used from door transitions/menus
;; keeps all registers intact
save_last_stats:
    pha
    lda !timer1 : sta !stats_timer
    lda !timer2 : sta !stats_timer+2
    lda !timer_lag : sta !stat_rta_lag_ram
    lda #$0000
    jsl save_stats
    pla
    rtl

;; Decrement Statistic (in A)
dec_stat:
    phx
    asl
    tax
    lda.l !stats_ram, x
    dec
    sta.l !stats_ram, x
    plx
    rtl

;; Store Statistic (value in A, stat in X)
store_stat:
    phx
    pha
    txa
    asl
    tax
    pla
    sta.l !stats_ram, x
    plx
    rtl

;; Load Statistic (stat in A, returns value in A)
load_stat:
    phx
    asl
    tax
    lda.l !stats_ram, x
    plx
    rtl

;;; -------------------------------
;;; RTA <> IGT sync
;; resync IGT when game transitions away from gameplay state
igt_end:
        jsl update_igt
        jsl $80834B ;; hijacked code
        rtl

;; load RTA in IGT
update_igt:
        php
        rep #$30
	;; divide total frames in 32 bits by 3600 to have 16bits minutes and remaining frames,
        ;; to correctly handle times up to 99:59:59.59 like vanilla
	lda !stats_timer
	sta $16
	lda !stats_timer+2
	sta $14
	lda #3600
	sta $12
	jsl utils_div32
	lda $14
	sta !igt_frames ;; store remainder to igt frames
	lda $16  ;; RTA in minutes
	sta $004204 ;; divide by 60 to get hours
	sep #$20
	lda #$3c
	sta $004206
	pha : pla :  pha : pla : rep #$20
	lda $004216 ;; rta minutes
	sta !igt_minutes ;; replace igt minutes
	lda $004214 ;; hours
        sta !igt_hours ;; replace igt hours
        cmp #$0064 ;; if < 100 hours, continue
        bpl .overflow
        lda !igt_frames ;; frames remainder after initial division to get minutes
	sta $004204 ;; divide by 60 to get seconds and frames
	sep #$20
	lda #$3c
	sta $004206
	pha : pla :  pha : pla : rep #$20
	lda $004216 ;; rta frames
	sta !igt_frames ;; replace igt frames
	lda $004214 ;; rta seconds
        sta !igt_seconds ;; replace igt seconds
        bra .end
.overflow: ;; IGT = 99:59:59.59
        lda #$0063
        sta !igt_hours
        lda #$003b
        sta !igt_minutes
        sta !igt_seconds
        sta !igt_frames
.end:
        plp
        rtl

load_state:
        ldx $07bb               ; hijacked code
        lda $0010, x : sta !VARIA_room_data
        LDA $0003,x             ; hijacked code
        rtl

;;; show save area and station instead of energy
menu_show_save_data:
	;; draw save area: find station in table
	ldx #$0000
.loop:
	lda.l save_area_text_table, x
	cmp #$ffff
	beq .energy
	cmp !area_index
	bne .next
	lda.l save_area_text_table+2, x
	cmp !load_station_index
	beq .draw
.next:
	txa
	clc
	adc #$0008
	tax
	bra .loop
.draw:
	phx
	;; 1st line
	lda.l save_area_text_table+4, x
	tay
	ldx $1A
	jsr $B3E2
	;; 2nd line
	plx
	lda.l save_area_text_table+6, x
	tay
	lda $1A
	clc
	adc #$0040
	tax
	jsr $B3E2
	pla ;; discard return address : return to previous caller, we have nothing left to do in hijacked routine
	rts
.energy:
	LDY #$B496 ;; hijacked energy tilemap address load
	rts

;; area index, save station index, 1st line addr, 2nd line addr
save_area_text_table:
	dw $0000, $0000, .crateria, .ship
	dw $0000, $0001, .crateria, .parlor
	dw $0000, $0006, .crateria, .gauntlet
	dw $0000, $0007, .tourian, .g4_hall
	dw $0001, $0000, .green_brin, .spore_spawn
	dw $0001, $0001, .green_brin, .main_shaft
	dw $0001, $0002, .green_brin, .etecoons
	dw $0001, $0003, .kraid, .notext
	dw $0001, $0004, .red_brin, .tower_top
	dw $0001, $0007, .green_brin, .etecoons
	dw $0001, $0008, .green_brin, .elevator
	dw $0001, $000A, .red_brin, .elevator
	dw $0002, $0000, .crocomire, .notext
	dw $0002, $0001, .upper_norfair, .bubble_mountain
	dw $0002, $0002, .upper_norfair, .business_center
	dw $0002, $0003, .upper_norfair, .pre_croc
	dw $0002, $0004, .lower_norfair, .elevator
	dw $0002, $0005, .lower_norfair, .ridley
	dw $0002, $0007, .lower_norfair, .firefleas
	dw $0002, $0008, .upper_norfair, .elevator
	dw $0003, $0000, .wrecked, .ship
	dw $0004, $0000, .red_brin, .tube
	dw $0004, $0001, .east_maridia, .forgotten_highway
	dw $0004, $0002, .east_maridia, .aqueduct
	dw $0004, $0003, .east_maridia, .draygon
	dw $0004, $0005, .east_maridia, .aqueduct
	dw $0004, $0006, .west_maridia, .mama_turtle
	dw $0004, $0007, .west_maridia, .watering_hole
	dw $0004, $0009, .west_maridia, .crab_shaft
	dw $0004, $000A, .west_maridia, .main_street
	dw $0005, $0000, .tourian, .mother_brain
	dw $0005, $0001, .tourian, .entrance
	dw $0006, $0000, .ceres, .elevator
	;; table terminator
	dw $ffff

table "tables/menu.tbl",rtl
;; strings ending with ffff terminator
;; 13 chars max on top line, 11 on bottom
.crateria:
	dw " CRATERIA"
.notext:
	dw $ffff
.green_brin:
	dw "GREEN BRIN."
	dw $ffff
.red_brin:
	dw "RED BRINSTAR"
	dw $ffff
.upper_norfair:
	dw "UPPER NORFAIR"
	dw $ffff
.lower_norfair:
	dw "LOWER NORFAIR"
	dw $ffff
.east_maridia:
	dw "EAST MARIDIA"
	dw $ffff
.west_maridia:
	dw "WEST MARIDIA"
	dw $ffff
.tourian:
	dw "  TOURIAN"
	dw $ffff
.ceres:
	dw "   CERES"
	dw $ffff
.wrecked:
	dw "  WRECKED"
	dw $ffff
.ship:
	dw "   SHIP"
	dw $ffff
.parlor:
	dw "  PARLOR"
	dw $ffff
.gauntlet:
	dw " GAUNTLET"
	dw $ffff
.g4_hall:
	dw " GOLDEN 4"
	dw $ffff
.spore_spawn:
	dw "SPORE SPAWN"
	dw $ffff
.main_shaft:
	dw "MAIN SHAFT"
	dw $ffff
.etecoons:
	dw " ETECOONS"
	dw $ffff
.kraid:
	dw "   KRAID"
	dw $ffff
.tower_top:
	dw "TOWER TOP"
	dw $ffff
.elevator:
	dw " ELEVATOR"
	dw $ffff
.crocomire:
	dw "CROCOMIRE"
	dw $ffff
.bubble_mountain:
	dw "BUBBLE MTN."
	dw $ffff
.business_center:
	dw "BIZ CENTER"
	dw $ffff
.pre_croc:
	dw "BEFORE CROC"
	dw $ffff
.ridley:
	dw "  RIDLEY"
	dw $ffff
.firefleas:
	dw " FIREFLEAS"
	dw $ffff
.tube:
	dw "   TUBE"
	dw $ffff
.forgotten_highway:
	dw "  HIGHWAY"
	dw $ffff
.aqueduct:
	dw " AQUEDUCT"
	dw $ffff
.draygon:
	dw "  DRAYGON"
	dw $ffff
.mama_turtle:
	dw "MAMA TURTLE"
	dw $ffff
.watering_hole:
	dw "WATER HOLE"
	dw $ffff
.crab_shaft:
	dw "CRAB SHAFT"
	dw $ffff
.main_street:
	dw "MAIN STREET"
	dw $ffff
.mother_brain:
	dw "  M BRAIN"
	dw $ffff
.entrance:
	dw " ENTRANCE"
	dw $ffff

;;; if "player flag" is set in the slot, draw a lock on top of samus helmet
;;; (drawing the sprite before puts it on top)
draw_lock:
        pha : phx : phy
        ;; infer the drawn save slot from context
        ;; retrieve X register pushed at the start of calling routine
        lda 11,s
        ;; possible values are 4, 6, 8, apply x -> ((x - 1) >> 1) - 1 to get 0, 1, 2
        dec : lsr : dec
        ;; save value
        sta !temp
        ;; check if the save is actually used
        asl : tax
        lda !used_slots_mask : and.l slots_bitmasks, x
        beq .end
        ;; check for locked status in SRAM
        lda !temp
        %backupIndex()
        lda $700002, x
        bpl .unlocked
.locked:
        ;; check if previous status was unlocked
        lda !temp : asl : tax
        lda !locked_slots_mask : and.l slots_bitmasks, x
        bne .draw_lock               ; already locked, just draw lock sprite
        ;; set locked status
        lda !locked_slots_mask : ora.l slots_bitmasks, x : sta !locked_slots_mask
        ;; play "moved cursor" sound
        lda #$0037 : JSL $809049
        bra .draw_lock
.unlocked:
        ;; check if previous status was unlocked
        lda !temp : asl : tax
        lda !locked_slots_mask : and.l slots_bitmasks, x
        beq .end               ; already unlocked
        ;; clear locked status
        lda.l slots_bitmasks, x : eor #$ffff : and.l !locked_slots_mask : sta !locked_slots_mask
        ;; play "moved cursor" sound
        lda #$0037 : JSL $809049
        bra .end
.draw_lock:
        ply : plx : phx : phy
        lda #$0a00 : sta $03    ; set palette to 5
        lda #$0068 : jsl $81891F
.end:
        ;; draw lock for help if needed
        ;; (doing this here is not really efficient, but good enough)
        lda.l !used_slots_mask : beq .helmet
        ldx.w #(32*8-1) : ldy.w #(27*8+2)
        lda #$0a00 : sta $03    ; set palette to 5
        lda #$0068 : jsl $81891F
.helmet:
        ply : plx
        lda #$0e00 : sta $03    ; set palette to 7
        pla : jsl $81891F
        rtl

;;; when in load menu, check if left, right, X or Y are pressed, if so, change
;;; selected file lock status
control_lock:
        jsr $9DE4               ; hijacked code
        lda $8f                 ; read newly pressed buttons
        bit #$1c80 : bne .end ; if A, B, start, up or down pressed, do nothing
        bit #$4340 : beq .end ; check for left, right, X or Y
        ;; check that we're actually selecting a slot
        lda !current_save_slot : cmp.w #3 : bpl .end
        ;; actually toggle lock
        %backupIndex()
        lda $700002, x : eor #$8000 : sta $700002, x
.end:
        rts

print "b81 end 1: ", pc

%freespaceEnd($81fa7f)

!arrow_tile_idx #= $c0
!menu_bg1_tilemap #= $7e3600
!lock_help_tilemap_size #= 8*2

%freespaceStart($81fc00)
draw_lock_help:
        lda.l !used_slots_mask : beq .end
        ldx.w #!lock_help_tilemap_size
.loop:
        dex : dex
        bmi .end
        lda.l lock_help_tilemap, x : sta.l !menu_bg1_tilemap+tileOffset(21, 26), x
        bra .loop
.end:
        JSR $969F               ; hijacked code
        rts

lock_help_tilemap:
        dw BGtile(!arrow_tile_idx, 0, 1, 0, 0), BGtile(!arrow_tile_idx, 0, 1, 1, 0) ; <>
        dw "TOGGLE"

print "b81 end 2: ", pc
%freespaceEnd($81fcff)

org $8e8000+(32*!arrow_tile_idx)
incbin "base/arrow_tile.gfx"

;;; Spritemap pointers table end. It can be expanded, since we spill over unused data
org $82c639
        dw spritemap_lock       ; entry $68

spritemap_lock:
        dw $0001
        %sprite($8A, 0, 492, 244, 0, %11, 0, 0)

warnpc $82c749 ; useful data resumes here

;;; when saving, inform the player in the "SAVE COMPLETED" message box of the backup status
!n_vanilla_entries #= $1C
!new_save_completed_msg_box #= $1d
!line_strlen #= 26
!msgbox_ram_tilemap = $7E3200
!full_line_size #= $40
!third_line_addr #= 3*!full_line_size+!msgbox_ram_tilemap+6

org $8580CE
        dw !new_save_completed_msg_box ; ship point to new save completed box

org $84B027
        dw !new_save_completed_msg_box ; save station point to new save completed box

org $85848D
        db !new_save_completed_msg_box ; special case in handle msg box interaction routine

;;; some fixes to message box handling to add our own without touching the vanilla tables and tilemaps
;;; code based on MessageBoxesV5 by Kejardon, JAM, Nodever2 (https://metroidconstruction.com/resource.php?id=334)
org $85869B
msgbox_vanilla_entries:
        skip !n_vanilla_entries*6
.end:

org $85824B
        JSR FixMessageDefOffset
org $8582ED
        JSR FixMessageDefOffset

org $8580D6
        jsr ship_actually_save


%freespaceStart($859643)
FixMessageDefOffset:
    CLC : ADC $34               ; hijacked code
    CMP.w #!n_vanilla_entries*6 : BMI + ; if we are reading from before the end of message box 1C data, return
    ;; adjust table offset for entries >= 1D
    STA $34 : LDA #(msgbox_new_entries-msgbox_vanilla_entries_end) : CLC : ADC $34
+   RTS

;;; vanilla code is a bit of a troll by actually saving once Samus
;;; gets out of ship, we need to actually save before displaying the
;;; save completed msg box
ship_actually_save:
        php
        %ai16()
        ;; pasted from gunship code, will be ran again afterwards but who cares
        LDA $7ED8F8
        ORA #$0001             ;} Set Crateria save station 0
        STA $7ED8F8            ;/
        STZ $078B              ; Load station index = 0
        LDA $0952              ;\
        JSL $818000            ;} Save current save slot to SRAM
        plp
        ;; Play saving sound effect (hijacked code)
        JSR $8119
        rts

;;; start at index 1D
msgbox_new_entries:
        dw save_completed_custom, $825A, tilemap_save_completed
        dw $8436, $8289, tilemap_terminator

;;; write info about last backup in save completed msg box
save_completed_custom:
        php
        %ai16()
        lda.l !backup_candidate
        bmi .backup_not_necessary
        and #$0003
        cmp.w #3 : beq .backup_failed
.backup_done:
        pha
        ldy #tilemap_backup_done : jsr replace_3rd_line
        pla : clc : adc #$28e0  ; get pink letter for slot
        sta.l 2*23+!third_line_addr
        bra .end
.backup_not_necessary:
        ldy #tilemap_backup_not_needed : jsr replace_3rd_line
        bra .end
.backup_failed:
        ldy #tilemap_backup_failed : jsr replace_3rd_line
.end:
        plp
        jsr $8441
        rts

;;; rewrite 3rd line of large message box in RAM tilemap
;;; Y: offset of line string in bank 85
replace_3rd_line:
        ldx.w #0
.loop:
        lda $0000, y
        sta.l !third_line_addr, x
        iny : iny : inx : inx
        cpx.w #(2*!line_strlen) : bmi .loop
        rts

;;; tilemap definitions
table "tables/msgbox.tbl"

!msg_box_border = $000e, $000e, $000e

tilemap_save_completed:
        dw !msg_box_border : dw "     SAVE COMPLETED.      " : dw !msg_box_border
        dw !msg_box_border : dw "                          " : dw !msg_box_border
        dw !msg_box_border : dw "                          " : dw !msg_box_border

tilemap_terminator:

tilemap_backup_failed:
        dw " NO SLOT LEFT FOR BACKUP! "

tilemap_backup_done:
        dw " PREVIOUS SAVE TO SLOT X. "

tilemap_backup_not_needed:
        dw "   BACKUP NOT NECESSARY.  "

print "85 end: ", pc
%freespaceEnd($8598ff)

;;; Disable special X-Ray handler for animals room during escape, as
;;; this otherwise unused state header field is used to hold VARIA
;;; area for the room
org $84836A
handle_special_xray:
        bra .skip
org $848398
.skip:
