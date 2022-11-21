;;; VARIA boot, save/load/backup saves management (including stats), RTA timer, base stats functions
;;; 
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

math pri on

incsrc "sym/seed_display.asm"
incsrc "sym/utils.asm"

;;; -------------------------------
;;; CONSTANTS ;;;
;;; -------------------------------

incsrc "constants.asm"

;;; normal game SRAM
!regular_save_size = $0900      ; expanded by saveload patch (modified, A00 in original patch)
!regular_save_sram = $0010      ; after checksum
!regular_save_sram_slot0 = !regular_save_sram
!regular_save_sram_slot1 #= !regular_save_sram+!regular_save_size
!regular_save_sram_slot2 #= !regular_save_sram+!regular_save_size*2
!sram_station_info_offset = $0156 ; offset in a save file where current save station and area are stored
;;; stats SRAM
!stats_sram_sz_b = $0080
!stats_sram_sz_w = !stats_sram_sz_b/2
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
!backup_counter = $7fff38
!backup_candidate = $7fff3a

;;; boot and RTA timer
;; store last save slot and used saves in unused SRAM
!last_saveslot #= $700000+!stats_sram_slot0+3*!full_stats_area_sz_b
!used_slots_mask #= !last_saveslot+2
;; SRAM magic set to seed ID to check if we ever booted the seed
!was_started_flag32 #= !last_saveslot+4
;; special value here to check on boot if console was just reset
!softreset = $7fffe6
!reset_flag = #$babe
;; magic value used as marker in some places
!magic_flag = #$caca
;; backup RAM for timer to avoid it to get cleared at boot
!timer_backup1 = $7fffe2
!timer_backup2 = !timer_backup1+2
;; timer integrity protection
!timer_xor = $7eff00

;;; temp ram used
!tmp_area_sz = #$00df

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

;; patch copy routine to copy SRAM stats, and fix save slot size
org $819A66
    jsr copy_stats
org $819A62
        dw !regular_save_size

;; patch clear routine to update used save slots bitmask in SRAM, and fix save slot size
org $819cc3
	jsr patch_clear
org $819CBF
        dw !regular_save_size

;; hijack menu display for backup saves
org $819f13
	jsr load_menu_1st_file
org $819f46
	jsr load_menu_2nd_file
org $819f7c
	jsr load_menu_3rd_file

;; hijack menu display to show save area instead of energy if backup saves are enabled
org $81A09B
	jsr menu_show_save_data

;; Hijack loading new game to reset stats
org $82805f
    jsl clear_values

;; end gamestate hijack to resync IGT from RTA that stopped ~6 seconds earlier
org $8284D3
        jsl igt_end

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
    jmp .inc
org $809602 ;; overwrite lag handling to count lag in global counter
    jmp .inc
    ;; handle 32 bit counter :
org $808FA3 ;; overwrite unused routine
.inc:
    rep #$30
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
    rti

warnpc $808FC2 ;; next used routine start

;;; -------------------------------
;;; Boot
;; Patch boot to init stuff
org $80fe00
boot1:
    ;; check timer integrity: if not ok disable soft reset flag
    lda !timer1
    eor !timer2
    cmp !timer_xor
    beq +
    lda !magic_flag
    sta !softreset
+
    lda #$0000
    sta !timer_backup1
    sta !timer_backup2
    ;; check if first boot ever by checking magic 32-bit value in SRAM
    lda !was_started_flag32
    cmp seed_display_seed_value
    bne .first
    lda !was_started_flag32+2
    cmp seed_display_seed_value+2
    beq .check_reset
.first:
    ;; no game was ever saved:
    ;; init used save slots bitmask
    lda #$0000
    sta !used_slots_mask
    ;; clear all save files by corrupting checksums
    ldx	#$0005
    lda !magic_flag
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
    ;; check if soft reset, if so, restore RAM timer
    lda !softreset
    cmp !reset_flag
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
    ldx !tmp_area_sz
    lda #$0000
-
    sta $7fff00, x
    dex
    dex
    bpl -
    ;; resume vanilla code
    jml $8084af

warnpc $80ffbf

;;; -------------------------------
;;; Save files management : adds timer, stats and backup features to save files
org $81ef20
;; Rolling backup save mechanism:
;;
;; Additional data in saves :
;;	- initial save slot ID
;;	- a player usage flag, set when a game is loaded by the user
;;	- a backup counter, incremented everytime a backup is made
;; - when loading a game (i.e. the player actually uses a file),
;;   mark the file as used with the player usage flag.
;;	- if loading an existing file without the player flag (a backup),
;;	  copy over stats from current player save (non-backup with the
;;	  closest save counter? or highest?), or directly from RAM
;;	  if possible
;; - when saving a game, and it's not the first file creating save, and save
;;   station used is different from the last one :
;;	- scan through save files to determine the best candidate to use as
;;	  backup
;;	- priority: empty save, old backup, recent backup
;;	- ignore save files with player flag set (was loaded once)
;;	- ignore backup files from different slots

;; make optional to auto backup save, set this flag to non-zero in ROM to enable the feature
opt_backup:
	dw $0000

;;; zero flag set if we're starting a new game
check_new_game:
    ;; Make sure game mode is 1f
    lda $7e0998
    cmp #$001f : bne .end
    ;; check that Game time and frames is equal zero for new game
    lda $09DA
    and #$fffe                  ; consider 1 IGT frame as 0 (workaround for start game with intro text)
    ora $09DC
    ora $09DE
    ora $09E0
.end:
    rtl

;; a save will always be performed when starting a new game (see start.asm)
new_save:
	;; call save routine
	lda !current_save_slot
	jsl $818000
	;; if backup saves are disabled, return
	lda.l opt_backup
	beq .end
	;; set current save slot as used in SRAM bitmask
	lda !current_save_slot
	asl
	tax
	lda !used_slots_mask
	ora.l slots_bitmasks,x	;; bitmask index table in ROM
	sta !used_slots_mask

	;; init backup save data :

	;; first, get offset in SRAM, using save_index routine,
	;; which is based on last_saveslot value, which is correct,
	;; since we juste saved stats (through patch_save)
	jsl save_index		;; A is non-0, so get standard stats addr
	;; x += backup_save_data_off
	txa
	clc
	adc.w #!backup_save_data_off
	tax
	;; store current save slot in the save itself (useful if we reload
	;; a backup save, to copy over stats from original save)
	lda !current_save_slot
	sta $700000,x
	;; store 0 + high bit set (player flag) as backup counter
	lda #$8000
	sta $700002,x
.end:
	rtl

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
	;; first, check if current save station is different from last save
	lda !current_save_slot
	asl
	asl
	asl
	tay
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
	lda $700002,x
	and #$7fff
	sta !backup_counter
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
	ldy #slot0_data
	jsr check_slot
	ldy #slot1_data
	jsr check_slot
	ldy #slot2_data
	jsr check_slot
	;; clear all our work flags from backup_candidate
	lda !backup_candidate
	and #$0003
	;; check that we can actually backup somewhere
	cmp #$0003
	beq .no_backup
	sta !backup_candidate
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
	;; if not our save slot, skip
	ldx $0004,y
	lda $700000,x
	cmp !current_save_slot
	bne .end
	;; if not a backup save, skip
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
	asl
	asl
	asl
	tax
	lda.l slots_data+4,x
	tax
	lda $700002,x
	inc
	sta $700002,x

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
	lda !current_save_slot
	asl
	tax
	lda.l slots_sram_offsets,x ;; get SRAM offset in bank 70 for slot
	sta $47
	;; destination slot is in backup_candidate
	lda !backup_candidate
	asl
	tax
	lda.l slots_sram_offsets,x ;; get SRAM offset in bank 70 for slot
	sta $4a
	;; copy save file
	ldy #$0000
-
	lda [$47],y
	sta [$4a],y
	iny
	iny
	cpy #$065c
	bmi -
	;; copy checksum
	lda !current_save_slot
	asl
	tax
	lda $701ff0,x
	pha
	lda $701ff8,x
	pha
	lda $700000,x
	pha
	lda $700008,x
	pha
	lda !backup_candidate
	asl
	tax
	pla
	sta $700008,x
	pla
	sta $700000,x
	pla
	sta $701ff8,x
	pla
	sta $701ff0,x
	;; copy stats (includes backup data)
	lda !current_save_slot
	asl
	tax
	lda.l save_slots,x
	sta $47
	lda !backup_candidate
	asl
	tax
	lda.l save_slots,x
	sta $4a
	ldy #$0000
-
	lda [$47],y
	sta [$4a],y
	iny
	iny
	cpy.w #!full_stats_area_sz_b
	bcc -
	;; clear player flag in backup data area
	lda $4a		;; still has destination slot SRAM offset
	clc
	adc.w #!backup_save_data_off
	tax
	lda $700002,x
	and #$7fff
	sta $700002,x
	;; mark backup slot as used in bitmask
	lda !backup_candidate
	asl
	tax
	lda !used_slots_mask
	ora.l slots_bitmasks,x	;; bitmask index table in ROM
	sta !used_slots_mask
	rts

incsrc "saveload.asm"

;; Patch load and save routines
patch_save:                     ; called from saveload patch
	;; backup saves management:
	jsl check_new_game
	beq .save_stats
	lda.l opt_backup
	beq .stats
	;; we have backup saves enabled, and it is not the 1st save:
	;; check if we shall backup the save
	jsr is_backup_needed
	bcc .stats
	jsr backup_save
	;; handle timer/stats after backup
.stats:
	;; copy RTA timer to RAM stats and IGT RAM
	lda !timer1
	sta !stats_timer
	lda !timer2
	sta !stats_timer+2
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
    bcc .backup_check
    ;; skip to end if new file or SRAM corrupt
    jmp .end
.backup_check:
	lda.l opt_backup
	beq .check
	;; if backup saves are enabled:
	;; check if we load a backup save, and if so, get stats
	;; from original save slot, and mark this slot as non-backup
	lda !current_save_slot
	asl
	asl
	asl
	tax
	lda.l slots_data+4,x
	tax
	lda $700002,x
	bmi .check
.load_backup:
	phx
	;; n flag not set, we're loading a backup
	;; check if we're soft resetting: if so, will take stats from RAM
	lda !softreset
	cmp !reset_flag
	beq .load_backup_end
	;; load stats from original save SRAM
	lda $700000,x	;; save slot in SRAM
	clc
	adc #$0010
	sta !last_saveslot
	lda #$0000
	jsl save_index
	jsl load_stats_at
	;; update live timer
	lda !stats_timer
	sta !timer1
	lda !stats_timer+2
	sta !timer2
.load_backup_end:
	;; update current save slot in SRAM, and set player flag
	plx
	lda !current_save_slot
	sta $700000,x
	clc
	adc #$0010
	sta !last_saveslot
	lda $700002,x
	ora #$8000
	sta $700002,x
	bra .end_ok
.check:
    ;; check save slot
    lda !current_save_slot
    clc
    adc #$0010
    cmp !last_saveslot
    bne .load
    ;; we're loading the same save that's played last
    lda !softreset
    cmp !reset_flag
    beq .end_ok     ;; soft reset, use stats and timer from RAM
    ;; TODO add menu time to pause stat and make it a general menus stat?
.load:
    ;; load stats from SRAM
    jsl load_stats
    ;; update live timer
    lda !stats_timer
    sta !timer1
    lda !stats_timer+2
    sta !timer2
.end_ok:
    ;; place marker for resets
    lda !reset_flag
    sta !softreset
    ;; increment reset count
    lda !stat_resets
    jsl inc_stat
    jsl save_last_stats
    ;; return carry clear
    clc
.end:
    ply
    plx
    plb
    rtl


;;; Patch copy and clear routines

save_slots:
    dw !stats_sram_slot0
    dw !stats_sram_slot1
    dw !stats_sram_slot2

copy_stats:
    ;; src slot idx = 19b7, dst slot idx = 19b9
    lda $19b7
    asl
    tax
    lda.l save_slots,x
    sta $00
    lda $19b9
    asl
    tax
    lda.l save_slots,x
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
    ;; disable save slot check. if data is copied we cannot rely on RAM contents
    lda #$0000
    sta !last_saveslot
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


;;; Patch load file menu to show backup saves info

files_tilemaps:
	dw $b436,$b456,$b476

;; arg A=file
load_menu_file:
	phx
	pha
	lda.l opt_backup
	beq .nochange
.check_slot:
	pla
	pha
	asl
	tax
	lda.l slots_bitmasks,x	;; bitmask index table in ROM
	and !used_slots_mask
	beq .nochange
.load_slot:
	;; load save slot value in SRAM
	pla
	pha
	asl
	asl
	asl
	tax
	lda.l slots_data+4,x
	tax
	lda $700000,x
	bra .load_tilemap
.nochange:
	pla
	pha
.load_tilemap:
	asl
	tax
	lda.l files_tilemaps,x
	tay
.end:
	pla
	plx
	rts

load_menu_1st_file:
	lda #$0000
	jmp load_menu_file

load_menu_2nd_file:
	lda #$0001
	jmp load_menu_file

load_menu_3rd_file:
	lda #$0002
	jmp load_menu_file

;;; show save area and station instead of energy when backup saves are enabled
menu_show_save_data:
	lda.l opt_backup
	beq .energy
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


;;; -------------------------------
;;; Stats base functions

;; clear stats on new game
clear_values:
    php
    rep #$30
    jsl check_new_game
    bne .ret

    ldx #$0000
    lda #$0000
-
    jsl store_stat
    inx
    cpx #!stats_sram_sz_w
    bne -

    ;; Clear RTA Timer
    lda #$0000
    sta !timer1
    sta !timer2
    ;; place marker for resets
    lda !reset_flag
    sta !softreset
.ret:
    plp
    jsl $80a07b	;; hijacked code
    rtl

;; assuming a valid save slot is in last_saveslot,
;; stores in X the bank $70 index to stats area
;; arg A: if 0 we want last stats, otherwise standard stats
save_index:
    pha
    lda !last_saveslot
    cmp #$0010
    beq .slot0
    cmp #$0011
    beq .slot1
.slot2:
    ldx.w #!stats_sram_slot2
    bra .last
.slot0:
    ldx.w #!stats_sram_slot0
    bra .last
.slot1:
    ldx.w #!stats_sram_slot1
.last:
    pla
    bne .end
    txa
    clc
    adc #!stats_sram_sz_b
    tax
.end:
    rtl

load_stats:
    phx
    phy
    lda !current_save_slot
    clc
    adc #$0010
    sta !last_saveslot
    ;; tries to load from last stats
    jsr is_last_save_flag_ok
    bcc .notok
    lda #$0000
    jsl save_index
.notok:
    jsl load_stats_at
    ply
    plx
    rtl

;; arg X = index of where to load stats from in bank $70
load_stats_at:
    phx
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
    cpy #!stats_sram_sz_b
    bcc .loop
    plb
    plx
    rtl

;; return carry flag set if flag ok
is_last_save_flag_ok:
    phx
    pha
    lda #$0001
    jsl save_index
    txa
    clc
    adc.w #!last_stats_save_ok_off
    tax
    lda !magic_flag
    cmp $700000,x
    beq .flag_ok
    clc
    bra .end
.flag_ok:
    sec
.end:
    pla
    plx
    rts

;; args: A = value to store
;; X and A untouched
set_last_save_ok_flag:
    phx
    pha
    lda #$0001
    jsl save_index
    txa
    clc
    adc.w #!last_stats_save_ok_off
    tax
    pla
    sta $700000,x
    plx
    rts

;; arg X = index of where to save stats in bank $70
save_stats_at:
    phx
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
    cpy #!stats_sram_sz_b
    bcc .loop
    plb
    plx
    rts

;; save stats both in standard and last areas
;; arg: A = 0 if we just want to save last stats
;;      A != 0 save all stats (save stations)
;; used by gameend.asm, update address it in if moved
save_stats:
    phx
    phy
    pha
    ;; actually save stats now
    lda !current_save_slot
    clc
    adc #$0010
    sta !last_saveslot
    pla
    beq .last   ;; skip standard save if A=0
    jsl save_index ;; A is not 0, so we ask for standard stats index
    jsr save_stats_at
    lda #$0000
.last:
    jsl save_index ;; A is 0, so we ask for last stats index
    lda #$0000
    jsr set_last_save_ok_flag
    jsr save_stats_at
    lda !magic_flag
    jsr set_last_save_ok_flag
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
    lda !timer1
    sta !stats_timer
    lda !timer2
    sta !stats_timer+2
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

print "b81 end: ", pc

warnpc $81ffff
