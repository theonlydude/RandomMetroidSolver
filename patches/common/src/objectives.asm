;;; Objectives management and display
;;;
;;; Checks objectives regularly, and set an event when done. The event
;;; is used to unlock G4 (auto sink all statues). Statues will never
;;; individually sink, even if you kill G4 bosses.
;;; Alternatively (ROM option), escape will be automatically triggered
;;; when all objectives are completed.
;;;
;;; Add a new menu in pause to display objectives to finish the seed.
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

lorom
arch 65816

incsrc "event_list.asm"
incsrc "constants.asm"
incsrc "macros.asm"

incsrc "sym/utils.asm"
incsrc "sym/rando_escape_common.asm"
incsrc "sym/custom_music.asm"
incsrc "sym/disable_screen_shake.asm"
incsrc "sym/map.asm"
incsrc "sym/endingtotals.asm"
incsrc "sym/objectives_options.asm"

!timer = !timer1
!current_room = $079b
!samus_x = $0AF6
!samus_y = $0AFA

;; RAM to store amount of objectives completed
!obj_completed_count = $7fff48
!obj_sfx_flag = $7fff4a

!tmp_in_progress_done = $16
!tmp_in_progress_total = $18
!tmp_in_progress_pct_marker = $ffff

;;; counted by main obj routine, read by pause menu routine
!n_objs_left = $7fff4c

;;; external routines
!song_routine = $808fc1

;;; custom music patch detection for escape music trigger
!custom_music_id = $caca

;;; no screen shake patch detection for escape music trigger
!disable_earthquake_id = $0060

;;; Change G4 SFX priority to 1, because we play it on obj completion (when non-vanilla objectives)
!SPC_Engine_Base = $CF6C08

macro orgSPC(addr)
org !SPC_Engine_Base+<addr>
endmacro

%orgSPC($38D0)
        dw $39A8

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; HIJACKS
;;; hijack main ASM call to check objectives regularly
org $828BA8
	jsl obj_check

;;; new function to check for L/R button pressed
org $82A505
        jsr check_l_r_pressed

;;; replace pause screen button label palettes functions
org $82A61D
        jsr (new_pause_palettes_func_list,x)

;;; For minimizer or scavenger with ridley as last loc, disable
;;; elevator music change when boss drops appear if escape is
;;; triggered.
;;; (only handle G4, minibosses death flag is never set early)
;; Kraid
org $A7C81E
	jsl boss_drops
;; Phantoon
org $A7DB94
	jsl boss_drops
;; Draygon handled directly in minimizer_bosses, as elevator music is triggered early enough
;; Ridley
org $A6C5ED
	jsl boss_drops

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; CODE
org $85d000
print "85 start: ", pc

;;; total possible objectives
%export(n_objectives)
        dw $0004

;;; total required objectives
%export(n_objectives_required)
        dw $0004

;;; seed objectives checker functions pointers, list ends with $0000
;;; objective checker returns carry set if obj completed, clear if not
%export(objective_funcs)
        dw kraid_is_dead
        dw phantoon_is_dead
        dw draygon_is_dead
        dw ridley_is_dead
!_obj_idx #= 4
while !_obj_idx < !max_objectives
        dw $0000
        !_obj_idx #= !_obj_idx+1
endif

;;; "in progress" objective checkers. optional, set to 0 if not applicable for given objective
;;; called only when objective is not completed yet, returns carry set if obj in progress, clear if not
;;; can optionally set ($16, $18) as progress indicator, ie $16 "sub-objectives" completed out of $18.
%export(in_progress_funcs)
!_obj_idx #= 0
while !_obj_idx < !max_objectives
        dw $0000
        !_obj_idx #= !_obj_idx+1
endif

obj_check:
	jsr objectives_completed
.end:
	JSL $8FE8BD		; hijacked code
	rtl

;;; Checks for individual objectives and sets their events if completed.
;;; If all required are completed, sets objectives_completed_event.
;;; If all are completed, sets all_objectives_completed_event.
;;; Progressively checks objectives, one at a time.
;;; That way, exec time is constant, and does not depend on number of objectives.
objectives_completed:
	;; don't check anything if all objectives are already completed
        %checkEvent(!all_objectives_completed_event)
        bcc .check_objective
        rts
.check_objective:
        phx
        lda !obj_check_index : asl : tax
	;; check objective if not already completed
	lda.l objective_events, x : jsl !check_event
	bcs .completed
        jsr (objective_funcs, x)
        bcc .next
	;; objective completed
	lda.l objective_events, x
        sta !obj_sfx_flag       ; non-zero value
        jsl !mark_event
.completed:
        lda !obj_completed_count : inc : sta !obj_completed_count
.next:
        lda !obj_check_index : inc : cmp.l n_objectives : beq .end_list
        sta !obj_check_index
        bra .end
.end_list:
        ;; check if all objectives are completed to avoid further useless checks
        lda !obj_completed_count : cmp.l n_objectives : bmi .check_required
        %markEvent(!all_objectives_completed_event)
.check_required:
        %checkEvent(!objectives_completed_event)
        bcs .reset
        ;; n_objs_left = required_objs - completed_objs
        lda.l n_objectives_required : sec : sbc !obj_completed_count : sta !n_objs_left
        ;; required objectives are completed if n_objs_left is <= 0
        bmi .all_required_completed : beq .all_required_completed : bra .check_sfx
.all_required_completed:
        lda.w #0 : sta !n_objs_left ; reset to 0 in case it's negative, as it's displayed in pause menu
        %markEvent(!objectives_completed_event)
	lda.l objectives_options_escape_flag : and #$00ff : beq .check_sfx
	jsr trigger_escape
        bra .reset
.check_sfx:
	;; check if we should play an sfx upon objective completion
	lda !obj_sfx_flag : beq .reset
	lda.l objectives_options_settings_flags : bit.w #!option_play_sfx_on_completion_mask : beq .reset
.sfx:
	;; play G4 particle sfx and reset flag
	lda #$0019 : jsl $8090A3
.reset:
        lda.w #0
        sta !obj_sfx_flag
        sta !obj_check_index
        sta !obj_completed_count
.end:
        plx
        rts

%export(objective_events)
%objectivesCompletedEventArray()

;;; copy-pasted from a PLM instruction
clear_music_queue:
	PHX
	LDX #$000E
	STZ $0619,x
	STZ $0629,x
	DEX
	DEX
	BPL $F6
	PLX
	LDA $0639
	STA $063B
	LDA #$0000
	STA $063F
	STA $063D
	rts

;;; copied from escape rooms setup asm
room_earthquake:
        ;; don't trigger if no screen shake patch if detected
        lda.l disable_screen_shake_marker : and #$00ff
        cmp #!disable_earthquake_id : beq .end
	LDA #$0018             ;\
	STA $183E              ;} Earthquake type = BG1, BG2 and enemies; 3 pixel displacement, horizontal
	LDA #$FFFF
	STA $1840
.end:
	rts

trigger_escape:
	phx : phy
	jsl rando_escape_common_escape_setup_l
	jsr room_earthquake	; could not be called by setup asm since not in escape yet
	; load timer graphics
	lda #$000f : jsl $90f084
	jsl utils_fix_timer_gfx
	lda #$0002 : sta $0943	 ; set timer state to 2 (MB timer start)
	jsr clear_music_queue
	jsr trigger_escape_music
        %markEvent(!escape_event) ; timebomb set event
	ply : plx
	rts

trigger_escape_music:
	lda #$0000 : jsl !song_routine ; stop current music
	lda.l custom_music_marker
	cmp #!custom_music_id : beq .custom_music
	lda #$ff24 : jsl !song_routine ; load boss 1 music data
	lda #$0007 : jsl !song_routine ; load music track 2
	bra .end
.custom_music:
	lda custom_music_escape : ora #$ff00 : jsl !song_routine
	lda custom_music_escape+1 : and #$00ff : jsl !song_routine
.end:
	rts

;;; when escape is trigerred, avoid changing music when boss drops appear
boss_drops:
        %checkEvent(!escape_event)  ;if escape flag is off:
	bcs .end
	lda #$0003 : jsl $808FC1 	     ;  Queue elevator music track
.end:				 	     ;else do nothing
	rtl

;;; objectives checker functions, set carry if objective is completed
;;; helper macro to autodef simple event checker functions
macro eventChecker(func_name, event)
%export(<func_name>)
        %checkEvent(<event>)
	rts
endmacro

%eventChecker(kraid_is_dead, !kraid_event)
%eventChecker(phantoon_is_dead, !phantoon_event)
%eventChecker(draygon_is_dead, !draygon_event)
%eventChecker(ridley_is_dead, !ridley_event)

%export(all_g4_dead)
        jsr kraid_is_dead
        bcc .no
        jsr phantoon_is_dead
        bcc .no
        jsr draygon_is_dead
        bcc .no
        jsr ridley_is_dead
        bcc .no
        sec
.no:
        rts

%eventChecker(spore_spawn_is_dead, !spospo_event)
%eventChecker(botwoon_is_dead, !botwoon_event)
%eventChecker(crocomire_is_dead, !croc_event)
%eventChecker(golden_torizo_is_dead, !GT_event)

%export(all_mini_bosses_dead)
        jsr spore_spawn_is_dead
        bcc .no
        jsr botwoon_is_dead
        bcc .no
        jsr crocomire_is_dead
        bcc .no
        jsr golden_torizo_is_dead
        bcc .no
        sec
.no:
        rts

%eventChecker(scavenger_hunt_completed, !hunt_over_event)

nb_killed_bosses:
        ;; return number of killed bosses in X
        ldx #$0000
.kraid:
        jsr kraid_is_dead
        bcc .phantoon
	inx
.phantoon:
        jsr phantoon_is_dead
        bcc .draygon
	inx
.draygon:
        jsr draygon_is_dead
        bcc .ridley
	inx
.ridley:
        jsr ridley_is_dead
        bcc .end
        inx
.end:
        rts

nb_killed_minibosses:
        ;; return number of killed minibosses in X
        ldx #$0000
.spore_spawn:
        jsr spore_spawn_is_dead
        bcc .botwoon
	inx
.botwoon:
        jsr botwoon_is_dead
        bcc .crocomire
	inx
.crocomire:
        jsr crocomire_is_dead
        bcc .golden_torizo
	inx
.golden_torizo:
        jsr golden_torizo_is_dead
        bcc .end
        inx
.end:
        rts

macro nbBossChecker(n, bossType)
%export(<bossType>_<n>_killed)
	phx
        jsr nb_killed_<bossType>es
	;; cpx set carry if greater or equal
        cpx.w #<n>
        plx
        rts
endmacro

%nbBossChecker(1,boss)
%nbBossChecker(2,boss)
%nbBossChecker(3,boss)

%nbBossChecker(1,miniboss)
%nbBossChecker(2,miniboss)
%nbBossChecker(3,miniboss)

macro itemPercentChecker(percent)
%export(collect_<percent>_items)
	lda !CollectedItems
        cmp.l .pct              ; set carry when A is >= value
        rts
%export(collect_<percent>_items_pct)
        dw <percent>
endmacro

%itemPercentChecker(25)
%itemPercentChecker(50)
%itemPercentChecker(75)
%itemPercentChecker(100)

%export(nothing_objective)
	;; if option enabled, complete objective only when in
	;; crateria/blue brin, in case we trigger escape immediately
	;; and we have custom start location.
	lda.l objectives_options_escape_flag : and #$00ff : beq .ok
	lda.l objectives_options_settings_flags : and.w #!option_nothing_trigger_escape_crateria_mask : beq .ok
	;; determine current graph area in special byte in room state header
	phx
	ldx $07bb
	lda $8f0010,x : and #$00ff
	plx
	;; crateria ID is 1
	cmp #$0001 : beq .ok
	clc
	bra .end
.ok:
        sec
.end:
        rts

%eventChecker(fish_tickled, !fish_tickled_event)
%eventChecker(orange_geemer, !orange_geemer_event)
%eventChecker(shak_dead, !shak_dead_event)

%export(all_items_mask)
	dw $f32f
%export(all_beams_mask)
	dw $100f
%export(all_major_items)
	lda !collected_items_mask : cmp.l all_items_mask : bne .not
	lda !collected_beams_mask : cmp.l all_beams_mask : bne .not
	sec
	bra .end
.not:
	clc
.end:
	rts

%eventChecker(crateria_cleared, !crateria_cleared_event)
%eventChecker(green_brin_cleared, !green_brin_cleared_event)
%eventChecker(red_brin_cleared, !red_brin_cleared_event)
%eventChecker(ws_cleared, !ws_cleared_event)
%eventChecker(kraid_cleared, !kraid_cleared_event)
%eventChecker(upper_norfair_cleared, !upper_norfair_cleared_event)
%eventChecker(croc_cleared, !croc_cleared_event)
%eventChecker(lower_norfair_cleared, !lower_norfair_cleared_event)
%eventChecker(west_maridia_cleared, !west_maridia_cleared_event)
%eventChecker(east_maridia_cleared, !east_maridia_cleared_event)

%export(all_chozo_robots)
	jsr golden_torizo_is_dead : bcc .end
        %checkEvent(!BT_event)
        bcc .end
        %checkEvent(!bowling_chozo_event)
        bcc .end
        %checkEvent(!LN_chozo_lowered_acid_event)
.end:
	rts

macro defineMapTile(tile, addr, mask)
%export(map_tile_<tile>)
%export(map_tile_<tile>_addr)
        dw <addr>
%export(map_tile_<tile>_mask)
        dw <mask>
endmacro

macro checkMapTile(tile)
        lda.l map_tile_<tile>_addr : tax
        lda.l map_tile_<tile>_mask
        bit $0000,x
endmacro

%defineMapTile(etecoons, $0828, $0010)
%defineMapTile(dachora, $082c, $0020)

%export(visited_animals)
        phx
	lda !area_index : cmp #!brinstar : bne .not
        %checkMapTile(etecoons) : beq .dachora
        %markEvent(!etecoons_event)
.dachora:
        %checkMapTile(dachora) : beq .not
        %markEvent(!dachora_event)
        %checkEvent(!etecoons_event)
        bcc .not
.ok:
        sec
        bra .end
.not:
	clc
.end:
        plx
	rts

%eventChecker(king_cac_dead, !king_cac_event)

macro mapPercentChecker(percent)
%export(explored_map_<percent>)
        lda.l !map_total_tilecount : cmp.l .pct ; carry set if >=
        rts
%export(explored_map_<percent>_pct)
        skip 2
endmacro

%mapPercentChecker(25)
%mapPercentChecker(50)
%mapPercentChecker(75)
%mapPercentChecker(100)

macro exploredAreaChecker(area, index)
%export(<area>_explored)
        %a8()
        lda.l !map_tilecounts_table+<index> : cmp.l map_area_tiles+<index> ; carry set if >=
        %a16()
        rts
endmacro

%exploredAreaChecker(crateria, 1)
%exploredAreaChecker(green_brin, 2)
%exploredAreaChecker(red_brin, 3)
%exploredAreaChecker(ws, 4)
%exploredAreaChecker(kraid, 5)
%exploredAreaChecker(upper_norfair, 6)
%exploredAreaChecker(croc, 7)
%exploredAreaChecker(lower_norfair, 8)
%exploredAreaChecker(west_maridia, 9)
%exploredAreaChecker(east_maridia, 10)

;;; "in progress" objective checkers

macro inProgressBossChecker(n, bossType)
%export(in_progress_<bossType>_<n>_killed)
        lda.w #<n> : sta.b !tmp_in_progress_total
	phx
        jsr nb_killed_<bossType>es : stx.b !tmp_in_progress_done
        lda.b !tmp_in_progress_done : beq .no_progress
        sec
        bra .end
.no_progress:
        clc
.end:
        plx
        rts
endmacro

%inProgressBossChecker(2,boss)
%inProgressBossChecker(3,boss)
%inProgressBossChecker(4,boss)

%inProgressBossChecker(2,miniboss)
%inProgressBossChecker(3,miniboss)
%inProgressBossChecker(4,miniboss)

%export(items_percent)
        ;; item% = (CollectedItems*100)/total_items
        %a8()
        lda.l !CollectedItems : sta !mul_u8
        lda.b #100 : sta !mul_u8_do
        pha : pla : xba : xba
        %a16()
        lda !mul_u16_result : sta !div_u16
        %a8()
        lda.l endingtotals_total_items : sta !div_u8_do
        pha : pla : xba : xba
        %a16()
        lda #!tmp_in_progress_pct_marker : sta !tmp_in_progress_total   ; mark result as percent
        lda !div_u16_result_quotient : sta !tmp_in_progress_done
        beq .no_progress
        sec
        bra .end
.no_progress:
        clc
.end:
        rts

count_upgrades:
        ldx.w #16
.loop:
        dex : bmi .end
        lsr $14 : bcs .item
        lsr
        bra .loop
.item:
        inc !tmp_in_progress_total
        lsr : bcc .next
        inc !tmp_in_progress_done
.next:
        bra .loop
.end:
        rts

%export(upgrades_collected)
        phx
        stz !tmp_in_progress_done : stz !tmp_in_progress_total
        lda.l all_items_mask : sta $14
        lda !collected_items_mask
        jsr count_upgrades
        lda.l all_beams_mask : sta $14
        lda !collected_beams_mask
        jsr count_upgrades
        lda !tmp_in_progress_done : beq .no_progress
        sec
        bra .end
.no_progress:
        clc
.end:
        plx
	rts

%eventChecker(scav_started, !hunt_started_event)

incsrc "locs_by_areas.asm"

;;; A: VARIA area index
;;; returns: total number of items in area in Y, collected in $16
;;; (X and A also modified)
count_items_in_area:
        stz !tmp_in_progress_done
        ldy.w #0		; Y will be used to store number of items in current area
        ;; get loc id list index in X
        asl : tax : lda.l locs_by_areas,x : tax
.count_loop:
        lda $850000,x : and #$00ff
        cmp #$00ff : beq .end
        phx
        jsl !bit_index
        lda !item_bit_array,x : and $05e7
        beq .next
        inc !tmp_in_progress_done
.next:
        plx
        iny
        inx
        bra .count_loop
.end:
        rtl

macro clearAreaProgress(area, index)
%export(<area>_clear_progress)
        phx : phy
        %checkEvent(!<area>_clear_start_event)
        bcc .no_progress
        lda.w #<index> : jsl count_items_in_area
        sty !tmp_in_progress_total
        sec
        bra .end
.no_progress:
        clc
.end:
        ply : plx
        rts
endmacro

%clearAreaProgress(crateria, 1)
%clearAreaProgress(green_brin, 2)
%clearAreaProgress(red_brin, 3)
%clearAreaProgress(ws, 4)
%clearAreaProgress(kraid, 5)
%clearAreaProgress(upper_norfair, 6)
%clearAreaProgress(croc, 7)
%clearAreaProgress(lower_norfair, 8)
%clearAreaProgress(west_maridia, 9)
%clearAreaProgress(east_maridia, 10)

%export(in_progress_chozo_robots)
        lda.w #4 : sta.b !tmp_in_progress_total
	jsr golden_torizo_is_dead : bcc .bt
        inc !tmp_in_progress_done
.bt:
        %checkEvent(!BT_event)
        bcc .bowl
        inc !tmp_in_progress_done
.bowl:
        %checkEvent(!bowling_chozo_event)
        bcc .ln
        inc !tmp_in_progress_done
.ln:
        %checkEvent(!LN_chozo_lowered_acid_event)
        bcc .done
        inc !tmp_in_progress_done
.done:
        lda !tmp_in_progress_done
        bne .progress
        clc
        bra .end
.progress:
        sec
.end:
	rts

%export(in_progress_animals)
        lda.w #2 : sta.b !tmp_in_progress_total
.etecoons:
        %checkEvent(!etecoons_event)
        bcc .dachora
        inc !tmp_in_progress_done
.dachora:
        %checkEvent(!dachora_event)
        bcc .done
        inc !tmp_in_progress_done
.done:
        lda !tmp_in_progress_done
        bne .progress
        clc
        bra .end
.progress:
        sec
.end:
	rts

%export(explored_all_map_percent)
        ;; map% = (explored_tiles/8)*100/(total_tiles/8)
        ;; (accomodate for divisor being 8 bits, and total map tiles in 1024-2048 range
        lda !map_total_tilecount
        beq .no_progress
        lsr #3
        %a8()
        sta !mul_u8
        lda.b #100 : sta !mul_u8_do
        pha : pla : xba : xba
        %a16()
        lda !mul_u16_result : sta !div_u16
        lda.l map_total_tiles : lsr #3
        %a8()
        sta !div_u8_do
        pha : pla : xba : xba
        %a16()
        lda !div_u16_result_quotient
        cmp.w #100 : bmi +
        lda.w #99               ; with the loss of precision above we can have a wrong 100%
+
        sta !tmp_in_progress_done
        sec
        bra .end
.no_progress:
        clc
.end:
        lda.w #!tmp_in_progress_pct_marker : sta !tmp_in_progress_total   ; mark result as percent
        rts

macro exploredAreaPercent(area, index)
%export(<area>_explored_percent)
        %a8()
        lda.l !map_tilecounts_table+<index> : bne .compute
        %a16()
        clc                     ; no progress
        bra .end
.compute:
        ;; map% = explored_tiles*100/total_tiles
        sta !mul_u8
        lda.b #100 : sta !mul_u8_do
        pha : pla : xba : xba
        %a16()
        lda !mul_u16_result : sta !div_u16
        %a8()
        lda.l map_area_tiles+<index> : sta !div_u8_do
        pha : pla : xba : xba
        %a16()
        lda !div_u16_result_quotient : sta !tmp_in_progress_done
        sec
        bra .end
.end:
        lda.w #!tmp_in_progress_pct_marker : sta !tmp_in_progress_total   ; mark result as percent
        rts
endmacro

%exploredAreaPercent(crateria, 1)
%exploredAreaPercent(green_brin, 2)
%exploredAreaPercent(red_brin, 3)
%exploredAreaPercent(ws, 4)
%exploredAreaPercent(kraid, 5)
%exploredAreaPercent(upper_norfair, 6)
%exploredAreaPercent(croc, 7)
%exploredAreaPercent(lower_norfair, 8)
%exploredAreaPercent(west_maridia, 9)
%exploredAreaPercent(east_maridia, 10)

warnpc $85f7ff
obj_85_end:
print "obj 85 end: ", pc

;;; only sink the ground in G4 room if objectives are completed.
;;; otherwise you'd just have to beat G4 and go to statues room
;;; to have vanilla behaviour and Tourian access open
org $878400			; Phantoon
	dw alt_set_event

org $878468			; Ridley
	dw alt_set_event

org $8784d0			; Kraid
	dw alt_set_event

org $878538			; Draygon
	dw alt_set_event

org $87d000
;;; alternate instruction for statues objects:
;;; set event in argument only if objectives are completed
alt_set_event:
        %checkEvent(!objectives_completed_event)
	bcc .end
.set_event:
	lda $0000,y : jsl !mark_event
.end:
	iny : iny
	rts

;;; overwrite fish grapple AI to check if we're in red fish room
org $a0d719
	dw check_red_fish_tickle

;;; overwrite orange geemer various AIs to check for death
org $a0dc59
	dw check_orange_geemer_grapple
org $a0dc67
	dw check_orange_geemer_PB
org $a0dc6f
	dw check_orange_geemer_touch
org $a0dc71
	dw check_orange_geemer_shot

;;; overwrite Shaktool various AIs to check for death
org $a0f0af
	dw check_shak_touch
org $a0f0b1
	dw check_shak_shot

;;; overwrite Cacatac various AIs to check for King Cac death
org $a0d019
	dw check_cac_grapple
org $a0d027
	dw check_cac_PB
org $a0d02f
	dw check_cac_touch
org $a0d031
	dw check_cac_shot

org $a2f4a0
check_cac_grapple:
	jsl $a2800A
	bra check_cac

check_cac_PB:
	jsl $a28037
	bra check_cac

check_cac_touch:
	jsl $a28023
	bra check_cac

check_cac_shot:
	jsl $a2802d
	bra check_cac

check_cac:
	lda !current_room : cmp #$acb3 : bne .end
	;; we're in bubble mountain, check for cac death
	lda $0F8C,x : bne .end	; if current enemy health is positive, do nothing
	;; king cac is dead
        %markEvent(!king_cac_event)
.end:
	rtl

org $a3f350
check_red_fish_tickle:
	lda !current_room : cmp #$d104 : bne .end
	;; we're using grapple on a fish, in red fish room:
        %markEvent(!fish_tickled_event)
.end:
	jmp $8000 		; original AI

check_orange_geemer_PB:
	jsl $a38037
	bra check_orange_geemer

check_orange_geemer_shot:
	jsl $a3802d
	bra check_orange_geemer

check_orange_geemer_touch:
	jsl $a38023
	bra check_orange_geemer

check_orange_geemer_grapple:
	jsl $a3800a
	bra check_orange_geemer

check_orange_geemer:
	lda $0F8C : bne .end	; if enemy 0 health is positive, do nothing
	;; we killed orange geemer
        %markEvent(!orange_geemer_event)
.end:
	rtl

warnpc $a3f38f

;; hijack when bowling chozo gives control back to samus
org $AAE706
	jsr set_bowling_event

org $aaf800

check_shak_shot:
	jsl $aadf34
	bra check_shak

check_shak_touch:
	jsl $aadf2f
	bra check_shak

check_shak:
	lda $0F8C,x : bne .end	; if current enemy health is positive, do nothing
	;; we killed shak
        %markEvent(!shak_dead_event)
.end:
	rtl

set_bowling_event:
        %markEvent(!bowling_chozo_event)
	LDA #$0001		; hijacked code
	rts

warnpc $aaf82f

;;; Pause stuff

;;; new map state functions pointers list
org map_PauseRoutineIndex_objectives ; map patch already add some functions, and makes some room for our pointers in the patch
        dw func_objective_screen
        dw func_map2obj_fading_out, func_map2obj_load_obj, func_map2obj_fading_in
        dw func_obj2map_fading_out, $91D7, $9200

;;;
;;; pause menu objectives display
;;;

table "tables/pause.tbl",rtl

;;; new screen:
;;; (skip 3 indices used by map patch)
!pause_index_objective_screen = #$000B
!pause_index_map2obj_fading_out = #$000C
!pause_index_map2obj_load_obj = #$000D
!pause_index_map2obj_fading_in = #$000E
!pause_index_obj2map_fading_out = #$000F
!pause_index_obj2map_load_map = #$0010
!pause_index_obj2map_fading_in = #$0011


;;; pause screen button label mode
!pause_screen_button_mode = $0753
!pause_screen_button_map = #$0000     ; Map screen (SAMUS on the right, OBJ on the left)
!pause_screen_button_nothing = #$0001 ; Unpausing (nothing)
!pause_screen_button_equip = #$0002   ; Equipment screen (MAP on the left)
;;; new button mode:
!pause_screen_button_obj = #$0003     ; Objective screen (MAP on the right)

;;; Pause screen mode
!pause_screen_mode = $0763

;;; pause screen mode values
!pause_screen_mode_map = #$0000
!pause_screen_mode_equip = #$0001
;;; new mode:
!pause_screen_mode_obj = #$0002


!held_buttons = $05E1
!newly_pressed_buttons = $8F
!l_button = #$0020
!r_button = #$0010
!up_button = #$0800
!down_button = #$0400
!light_up_no_button = #$0000
!light_up_l_button  = #$0001
!light_up_r_button  = #$0002

;; dynamic objective text: BG1 tilemap in RAM
!BG1_tilemap = $7E3800
;; rows [5, 23] of screen
!BG1_tilemap_size = $4c0

!line_size #= 32*2
;; relative to tilemap
!obj_1st_line #= 5
!obj_last_line #= 18
!draw_obj_tile_limit #= tileOffset(2, !obj_last_line)

;; box tiles
!box_top_left = $3941
!box_top = $3942
!box_top_right = $7941
!box_left = $3940
!box_right = $7940
!box_bottom_left = $B941
!box_bottom = $B942
!box_bottom_right = $F941

;; obj completion tiles
!completed_tick #= BGtile($176, 1, 1, 0, 0)
!in_progress_dots #= BGtile($177, 1, 1, 0, 0)

;; scroll arrows tiles
!scroll_up_left #= BGtile($1B8, 6, 1, 0, 0)
!scroll_up_right #= BGtile($1B8, 6, 1, 1, 0)
!scroll_down_left #= BGtile($1B8, 6, 1, 0, 1)
!scroll_down_right #= BGtile($1B8, 6, 1, 1, 1)

!click_sfx = $37
!scroll_blocked_sfx = $36
!play_sfx_lib1 = $809049

;; RAM
;; current first objective displayed
!obj_index = $073d
;; last objective displayed
!last_obj_index = $0731

;;; digit to draw in A
;;; x, y are relative to viewable area
macro drawDigit(x, y)
        clc : adc.w #'0'
        sta.l !BG1_tilemap+tileOffset(<x>, <y>)
endmacro

;;; digit to draw in A
;;; tile offset in X (updated)
macro drawDigitOffset()
        clc : adc.w #'0' : sta.l !BG1_tilemap, x
        inx : inx
endmacro

;;; x, y are relative to viewable area
macro drawTile(tile, x, y)
        lda.w #<tile> : sta.l !BG1_tilemap+tileOffset(<x>, <y>)
endmacro

;;; tile offset in X (updated)
macro drawTileOffset(tile)
        lda.w #<tile> : sta.l !BG1_tilemap, x
        inx : inx
endmacro

;;; continue in bank 85 for obj screen management code
org obj_85_end
;;; load base screen tilemap from ROM to RAM
load_obj_tilemap:
        %loadRamDMA(obj_bg1_tilemap, !BG1_tilemap, obj_txt_ptrs-obj_bg1_tilemap)
        ;; update number of objectives left to complete in RAM tilemap
        lda !n_objs_left
        %drawDigit(2, 2)
        rtl

;;; update RAM tilemap with objectives text, line by line
!tmp_tile_offset = $12

update_objs:
        ;; don't do anything if objectives are hidden
        lda.l objectives_options_settings_flags : bit.w #!option_hidden_objectives_mask : beq +
        %checkEvent(!objectives_revealed_event)
        bcs +
        rtl
+
        ;; draw scroll up arrow if !obj_index > 0
        lda !obj_index : beq .clear_up_arrow
        %drawTile(!scroll_up_left, 15, !obj_1st_line)
        %drawTile(!scroll_up_right, 16, !obj_1st_line)
        bra .start
.clear_up_arrow:
        ;; clear any previously drawn up arrow
        %drawTile(0, 15, !obj_1st_line)
        %drawTile(0, 16, !obj_1st_line)
.start:
        ;; init: place tile index at beggining of 1st obj line
        lda.w #((!obj_1st_line+1)*!line_size)+4 : sta.b !tmp_tile_offset
        lda !obj_index : sta !last_obj_index
.draw_obj_loop:
        ;; draw objective line
        ;; reset "in progress" tmp vars
        stz !tmp_in_progress_done : stz !tmp_in_progress_total
        ;; check if completed
        lda !last_obj_index : asl : tax : lda.l objective_events, x
        jsl !check_event
        bcc .not_completed
        lda #!completed_tick
        bra .compl_end
.not_completed:
        ;; handle "in progress" status
        lda !last_obj_index : asl : tax
        lda.l in_progress_funcs, x : beq .not_in_progress
        jsr (in_progress_funcs, x) : bcc .not_in_progress
        lda.w #!in_progress_dots : bra .compl_end
.not_in_progress:
        lda.w #0
.compl_end:
        ldx !tmp_tile_offset
        sta !BG1_tilemap, x
        inx : inx : stx !tmp_tile_offset
.draw_obj_text:
        ;; objective string
        lda !last_obj_index : asl : tax
        lda.l obj_txt_ptrs, x
        tax
.obj_txt_loop:
        lda.l $B60000, x
        cmp #$ffff : beq .obj_txt_loop_end
        phx
        ldx !tmp_tile_offset : sta.l !BG1_tilemap, x
        inx : inx : stx !tmp_tile_offset
        plx
        inx : inx
        bra .obj_txt_loop
.obj_txt_loop_end:
        ;; handle in-progress display
        lda !tmp_in_progress_total : beq .pad
        ldx !tmp_tile_offset
        %drawTileOffset(0)
        %drawTileOffset('(')
        lda !tmp_in_progress_done : jsr draw_number
        lda !tmp_in_progress_total : cmp.w #!tmp_in_progress_pct_marker : beq .progress_percent
        ;; "i/n"
        %drawTileOffset('/')
        lda !tmp_in_progress_total : jsr draw_number
        bra .end_in_progress
.progress_percent:
        ;; "i%"
        %drawTileOffset('%')
.end_in_progress:
        %drawTileOffset(')')
        stx !tmp_tile_offset
.pad:
        ;; pad with 0 to the end of line
        ldx !tmp_tile_offset
        jsr pad_0
.obj_pad_loop_end:
        ;; draw empty line
        jsr pad_0
        ;; check if no more space to draw to or no more obj to draw
        cpx.w #!draw_obj_tile_limit : bpl .draw_obj_loop_end
        lda !last_obj_index : inc : sta !last_obj_index
        cmp.l n_objectives : beq .last_pad
        jmp .draw_obj_loop
.last_pad:
        jsr pad_0
        cpx.w #!draw_obj_tile_limit : bmi .last_pad
.draw_obj_loop_end:
        ;; check if objs left to draw and draw down arrow if necessary
        !_obj_last_line #= !obj_last_line-1
        lda !last_obj_index : inc : cmp.l n_objectives : bpl .clear_down_arrow
        %drawTile(!scroll_down_left, 15, !_obj_last_line)
        %drawTile(!scroll_down_right, 16, !_obj_last_line)
        bra .end
.clear_down_arrow:
        ;; clear any previously drawn down arrow
        %drawTile(0, 15, !_obj_last_line)
        %drawTile(0, 16, !_obj_last_line)
.end:
        rtl

;; pad with 0s until end of line, and skip to start of next line
pad_0:
.loop:
        txa : inc #4 : and #$003f : beq .end
        lda #$0000 : sta.l !BG1_tilemap,x
        inx : inx
        bra .loop
.end:
        inx #8
        stx !tmp_tile_offset
        rts

;;; draw number < 100
draw_number:
        cmp.w #10 : bmi .digit
        ;; draw tenth
        sta $4204
        %a8()
        lda.b #10 : sta $4206
        pha : pla : xba : xba
        %a16()
        lda $4214
        %drawDigitOffset()
        lda $4216
.digit:
        %drawDigitOffset()
        rts

;;; direct DMA of BG1 tilemap to VRAM
blit_objs:
        %gfxDMA(!BG1_tilemap, $48A0, !BG1_tilemap_size)
        rtl

;;; DMA tilemap each frame
queue_obj_tilemap:
        %queueGfxDMA(!BG1_tilemap, $48A0, !BG1_tilemap_size)
        rtl

;;; check if up/down press, and if applicable, scroll (play sfx for scroll ok/ko)
obj_scroll:
        lda !newly_pressed_buttons
        bit !up_button : bne .up
        bit !down_button : bne .down
        bra .end
.up:
        lda !obj_index : beq .blocked
        dec !obj_index
        bra .click
.down:
        lda !last_obj_index : inc : cmp.l n_objectives : bpl .blocked
        inc !obj_index
.click:
        lda.w #!click_sfx : jsl !play_sfx_lib1
        bra .end
.blocked:
        lda.w #!scroll_blocked_sfx : jsl !play_sfx_lib1
.end:
        rtl

warnpc $85f7ff
print "pause 85 end: ", pc

;;; main pause menu interaction in 82 after InfoStr in seed_display.asm
org $82FB6D

;;; check for L or R input and update pause_index && pause_screen_button_mode
check_l_r_pressed:
        PHP
        REP #$30
        LDA !held_buttons
        BIT !l_button
        BNE .press_L
        BIT !r_button
        BNE .press_R
        BRA .end

.press_R:
        LDA !pause_screen_button_mode
        CMP !pause_screen_button_equip  ; if already equipment screen => end
        BEQ .end
        ;; common actions
        LDA $C10A   ; $82:C10A             db 05,00
        STA $0729   ; Frames to flash L/R/Start button on pause screen
        LDA !light_up_r_button
        STA $0751   ; $0751: Which button lights up for $0729 frames when changing screens from pause screen 

        LDA !pause_screen_button_mode
        CMP !pause_screen_button_obj
        BEQ .move_to_map_from_obj

.move_to_equip_from_map:
        LDA !pause_index_map2equip_fading_out
        STA !pause_index
        LDA !pause_screen_button_equip
        STA !pause_screen_button_mode
        BRA .play_sound

.move_to_map_from_obj:
        LDA !pause_index_obj2map_fading_out
        STA !pause_index
        LDA !pause_screen_button_map
        STA !pause_screen_button_mode   ; pause_screen_button_mode set to pause_screen_button_equip
        BRA .play_sound

.press_L:
        LDA !pause_screen_button_mode  ; pause_screen_button_mode, 00 == map screen
        CMP !pause_screen_button_obj
        BEQ .end                ; if already on objective screen => end
        ;; common actions
        LDA $C10A  ; $82:C10A             db 05,00
        STA $0729  ; frames to flash L/R/Start button on pause screen
        LDA !light_up_l_button
        STA $0751

        LDA !pause_screen_button_mode
        CMP !pause_screen_button_map
        BEQ .move_to_obj_from_map   ; if on map screen and L pressed => objective screen

.move_to_map_from_equip:
        LDA !pause_index_equip2map_fading_out
        STA !pause_index
        STZ !pause_screen_button_mode  ; pause_screen_button_mode set to pause_screen_button_map
        BRA .play_sound

.move_to_obj_from_map:
        LDA !pause_index_map2obj_fading_out
        STA !pause_index
        LDA !pause_screen_button_obj
        STA !pause_screen_button_mode
        
.play_sound:
        JSR $A615   ; $A615: Set pause screen buttons label palettes to show/hide them
        LDA #$0038  ;\
        JSL $809049 ;} Queue sound 38h, sound library 1, max queued sounds allowed = 6 (menu option selected)

.end:
        PLP
        RTS

;;; unpause
display_unpause:
        LDA !pause_screen_mode
        CMP !pause_screen_mode_equip
        BEQ .equip
        CMP !pause_screen_mode_obj
        BEQ .objective
.map:
        JSL $82BB30  ; Display map elevator destinations
        JSL $82B672  ; Draw map icons
        JMP map_DrawIndicatorIfInCurrentArea    ; Map screen - draw Samus position indicator
.equip:
        JSR $B267    ; Draw item selector
        JSR $B2A2    ; Display reserve tank amount
.objective:
        JMP $A56D    ; Updates the flashing buttons when you change pause screens

;;; buttons addresses in BG2
!left_button_top     = $7E364A
!left_button_bottom  = $7E368A
!right_button_top    = $7E366C
!right_button_bottom = $7E36AC

;;; replace 'MAP' with 'OBJ' in left BG2, put back 'SAMUS' in right BG2
set_bg2_map_screen:
        LDY #$000A
        LDX #$0000
.left_loop_top:
        LDA obj_top,x
        STA !left_button_top,x
        INX : INX
        DEY : DEY
        BNE .left_loop_top

        LDY #$000A
        LDX #$0000
.left_loop_bottom:
        LDA obj_bottom,x
        STA !left_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .left_loop_bottom

        LDY #$000A
        LDX #$0000
.right_loop_top:
        LDA samus_top,x
        STA !right_button_top,x
        INX : INX
        DEY : DEY
        BNE .right_loop_top

        LDY #$000A
        LDX #$0000
.right_loop_bottom:
        LDA samus_bottom,x
        STA !right_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .right_loop_bottom
        LDY #$000A              ; vanilla code
        RTS


;;; put back 'MAP' in BG2 left
set_bg2_equipment_screen:
        LDY #$000A
        LDX #$0000
.loop_top:
        LDA map_top,x
        STA !left_button_top,x
        INX : INX
        DEY : DEY
        BNE .loop_top

        LDY #$000A
        LDX #$0000
.loop_bottom:
        LDA map_bottom,x
        STA !left_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .loop_bottom
        LDY #$000A              ; vanilla code
        RTS

;;; replace 'SAMUS' with 'MAP' in BG2 right
set_bg2_objective_screen:
        LDY #$000A
        LDX #$0000
.loop_top:
        LDA map_top,x
        STA !right_button_top,x
        INX : INX
        DEY : DEY
        BNE .loop_top

        LDY #$000A
        LDX #$0000
.loop_bottom:
        LDA map_bottom,x
        STA !right_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .loop_bottom
        RTS

;;; obj:   left: grey (obj), right: MAP
;;; map:   left: OBJ,        right: samus
;;; equip: left: map,        right: grey (samus)

;;; obj/map/samus buttons tiles
obj_top:
        dw $2899, $2896, $2897, $2898, $289D

obj_bottom:
        dw $28A9, $28a6, $28a7, $28a8, $28AD

map_top:
        dw $2899, $289A, $289B, $289C, $289D

map_bottom:
        dw $28A9, $28AA, $28AB, $28AC, $28AD

samus_top:
        dw $2879, $287A, $287B, $287C, $287D

samus_bottom:
        dw $2889, $288A, $288B, $288C, $288D

;;; glowing sprites around L/R
glowing_LR_animation:
        dw $002A, $002A, $002A, $002A

new_pause_palettes_func_list:
        dw $A796, $A6DF, $A628, update_palette_objective_screen

update_palette_objective_screen:
        PHP
        REP #$30
        jsr set_bg2_objective_screen
        LDY #$000A
        LDX #$0000
.loop_top:
        LDA $7E364A,x
        AND #$E3FF
        ORA #$1400
        STA $7E364A,x ;} Set tilemap palette indices at $7E:364A..53 to 5 (top of MAP)
        INX : INX
        DEY : DEY
        BNE .loop_top

        LDY #$000A
        LDX #$0000
.loop_bottom:
        LDA $7E368A,x
        AND #$E3FF
        ORA #$1400
        STA $7E368A,x ;} Set tilemap palette indices at $7E:368A..93 to 5 (bottom of MAP)
        INX : INX
        DEY : DEY
        BNE .loop_bottom
        PLP
        RTS

func_objective_screen:
        JSR $A505    ; Checks for L or R input during pause screens
        JSR $A5B7    ; Checks for start input during pause screen
        jsl obj_scroll
        jsl update_objs
        jsl queue_obj_tilemap
        LDA !pause_screen_mode_obj ;\
        STA !pause_screen_mode     ;} Pause screen mode = objective screen
        RTS

func_map2obj_fading_out:
        JSL $82BB30  ; Display map elevator destinations
        JSR $B9C8    ; Map screen - draw Samus position indicator
        JSL $82B672  ; Draw map icons
        JSR $A56D    ; Updates the flashing buttons when you change pause screens
        JSL $808924  ; Handle fading out
        SEP #$20
        LDA $51      ;\
        CMP #$80     ;} If not finished fading out: return
        BNE .end     ;/
        JSL $80834B  ; Enable NMI
        REP #$20
        STZ $0723    ; Screen fade delay = 0
        STZ $0725    ; Screen fade counter = 0
        INC !pause_index    ; Pause index = 6 (equipment screen to map screen - load map screen)
.end:
        RTS


func_map2obj_load_obj:
        REP #$30
        ;; backup map's scroll
        LDA $B1
        STA $BD  ;} BG4 X scroll = [BG1 X scroll]
        LDA $B3
        STA $BF  ;} BG4 Y scroll = [BG1 Y scroll]
        ;; no scroll
        STZ $B1      ; BG1 X scroll = 0
        STZ $B3      ; BG1 Y scroll = 0
        
        stz !obj_index
        jsl load_obj_tilemap
        jsl update_objs
        jsl blit_objs
        LDA !pause_screen_mode_obj   ;\
        STA !pause_screen_mode       ;} Pause screen mode = objective screen
        JSR $A615    ; Set pause screen button label palettes
        STZ $073F    ; $073F = 0
        LDA $C10C    ;\
        STA $072B    ;} $072B = Fh
        LDA #$0001   ;\
        STA $0723    ;} Screen fade delay = 1
        STA $0725    ; Screen fade counter = 1
        INC !pause_index    ; Pause index = B (map screen to objective screen - fading in)
        RTS

func_map2obj_fading_in:
        LDA !pause_screen_mode_obj   ;\
        STA !pause_screen_mode       ;} Pause screen mode = objective screen
        JSL $80894D  ; Handle fading in
        SEP #$20
        LDA $51      ;\
        CMP #$0F     ;} If not finished fading in: return
        BNE .end     ;/
        REP #$20
        STZ $0723    ; Screen fade delay = 0
        STZ $0725    ; Screen fade counter = 0
        LDA !pause_screen_button_obj
        STA !pause_screen_button_mode
        LDA !pause_index_objective_screen ; index = objective
        STA !pause_index    ;/
.end:
        RTS

func_obj2map_fading_out:
        ;; fade out to map
        JSR $A56D    ; Updates the flashing buttons when you change pause screens
        JSL $808924  ; Handle fading out
        SEP #$20
        LDA $51      ;\
        CMP #$80     ;} If not finished fading out: return
        BNE .end     ;/
        JSL $80834B  ; Enable NMI
        REP #$20
        STZ $0723    ; Screen fade delay = 0
        STZ $0725    ; Screen fade counter = 0
        INC !pause_index    ; Pause index = D (obj screen to map screen - load map screen)
.end:
        RTS

print "82 end: ", pc

;;; start of equipment screen patch
warnpc $82febf

;;; keep 'MAP' left button visible on map screen by keeping palette 2 instead of palette 5 (grey one)
org $82A820
        ORA #$0800
org $82A83E
        ORA #$0800

;;; update BG2 buttons
org $82A79B
        JSR set_bg2_map_screen
org $82A62D
        JSR set_bg2_equipment_screen

;;; display correct sprites when unpausing
org $82932B
        JSR display_unpause

;;; update glowing sprite around L/R pointer
org $82C1E6
        dw glowing_LR_animation

;;; new tiles for 'OBJ' button in unused tiles : included in map patch gfx

;;; obj screen tilemap, obj text
org $B6F200
%export(obj_bg1_tilemap)
        ;; line 0 : pause "window title"
        fillbyte $00 : fill 20
        dw " OBJECTIVES "
        fillbyte $00 : fill 20
        ;; line 1 : top line of obj left/tourian boxes
        dw $0000, !box_top_left, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top_right
        dw !box_top_left, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top_right, $0000
        ;; line 2 : obj left/tourian text
        dw $0000, !box_left
        dw "  Obj left"
        dw !box_right, !box_left
        dw "Tourian:"
%export(obj_bg1_tilemap_tourian)
        fillbyte $00 : fill 16
        dw !box_right, $0000
        ;; line 3 : bottom line of obj left/tourian boxes
        dw $0000, !box_bottom_left, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom_right
        dw !box_bottom_left, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom_right, $0000
        ;; line 4 : top line of objectives text box
        dw $0000, !box_top_left, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top, !box_top_right, $0000
        ;; lines 5-9 : objectives text borders
!_line_idx = 5
while !_line_idx < 10
        dw $0000, !box_left, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, !box_right, $0000
	!_line_idx #= !_line_idx+1
endif
        ;; line 10 : text for hidden objectives
        dw $0000, !box_left
        dw "To reveal objectives list,"
        dw $0000, $0000, !box_right, $0000
        ;; line 11 : objectives text borders
        dw $0000, !box_left, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, !box_right, $0000
        ;; line 12 : text for hidden objectives
        dw $0000, !box_left
        dw "visit"
%export(obj_bg1_tilemap_reveal_room)
        dw $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, !box_right, $0000
        ;; lines 13-17 : objectives text borders
!_line_idx = 13
while !_line_idx < 18
        dw $0000, !box_left, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, !box_right, $0000
	!_line_idx #= !_line_idx+1
endif
        ;; line 18 : bottom line of objectives text box
        dw $0000, !box_bottom_left, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom, !box_bottom_right, $0000


%export(obj_txt_ptrs)
        skip !max_objectives*2

%export(objs_txt)
;; strings written by randomizer
print "B6 end: ", pc

warnpc $B6FA00
org $B6FA00
%export(objs_txt_limit)

;;; function to use as door asm when entering the room that reveals objectives
org $8ffe80
%export(reveal_objectives)
        %markEvent(!objectives_revealed_event)
        rts

;;; hardcode here the rooms for vanilla tourian (and disabled tourian with Tourian still in the graph)
;;; in case Tourian is not in the graph, the door asm will be added to the transition leading to climb
;;; if Tourian is fast, reveal_objectives will be called from minimizer_tourian_common patch
org $8391FC                     ; Statues Hallway door to Statues Room
        dw reveal_objectives
