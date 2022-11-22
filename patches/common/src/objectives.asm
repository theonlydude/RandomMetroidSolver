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

incsrc "sym/utils.asm"
incsrc "sym/rando_escape.asm"
incsrc "sym/custom_music.asm"
incsrc "sym/disable_screen_shake.asm"

!timer = !timer1
!current_room = $079b
!samus_x = $0AF6
!samus_y = $0AFA
!temp = $0743

;;; external routines
!song_routine = $808fc1

;;; custom music patch detection for escape music trigger
!custom_music_id = #$caca

;;; no screen shake patch detection for escape music trigger
!disable_earthquake_id = #$0060

;;; for items % objectives
!CollectedItems  = $7ED86E

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ROM OPTIONS
org !disabled_tourian_escape_flag
;;; if non-zero trigger escape as soon as objectives are completed
escape_option:
	db $00
;;; low bit: with nothing objective, trigger escape only in crateria
;;; high bit: play sfx on objective completion (don't use for vanilla objectives)
objectives_options_mask:
	db $01

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
	jsl periodic_obj_check

;;; replace pause mode code pointers list
org $82910A
        jsr (new_pause_actions_func_list,x)

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
org $a1fa80
print "A1 start: ", pc
;;; checks for objectives periodically
;;; seed objectives checker functions pointers, max 5, list ends with $0000
print " --- objectives checker functions: ", pc, " ---"
objective_funcs:
        dw kraid_is_dead
        dw phantoon_is_dead
        dw draygon_is_dead
        dw ridley_is_dead
        dw $0000
        dw $0000

periodic_obj_check:
	lda !timer : and !obj_check_period-1
	cmp !obj_check_period-1 : bne .end
	jsr objectives_completed
.end:
	JSL $8FE8BD		; hijacked code
	rtl

;;; checks for all individual objectives and sets their events if completed
;;; if all are completed, sets objectives_completed_event
objectives_completed:
        phx
	;; don't check anything if objectives are already completed
	lda !objectives_completed_event : jsl !check_event : bcs .end
	stz !temp
        ldx #$0000
.loop:
        lda.l objective_funcs, x
        beq .end_loop      ; checkers function list end
	;; check objective if not already completed
	lda.l objective_events, x : jsl !check_event
	bcs .next
        jsr (objective_funcs, x)
	bcc .next
	;; objective completed
	lda.l objective_events, x : jsl !mark_event
	;; store a non-zero value in temp if an obj is completed
	lda #$0001 : sta !temp
.next:
        inx : inx
        cpx.w !max_objectives*2
        bne .loop
.end_loop:
	jsr check_objectives_events
	;; check if we should play an sfx upon objective completion
	lda !temp : beq .end 	; do nothing anyway if no obj completed
	lda.l objectives_options_mask : bit #$0080 : beq .end
.sfx:
	;; play G4 particle sfx
	lda #$0019 : jsl $8090A3
.end:
        plx
        rts

;;; check if all objectives events are set, sets objectives_completed_event if so
;;; (subroutine of objectives_completed)
;;; input X : last loop index in objective check event, gives objective list size
check_objectives_events:
.loop:
	dex : dex
	bmi .completed
	lda.l objective_events,x
	jsl !check_event : bcc .end
	bra .loop
.completed:
        lda !objectives_completed_event : jsl !mark_event
	lda.l escape_option : and #$00ff : beq .end
	jsr trigger_escape
	stz !temp		; disable notification sfx
.end:
	rts

objective_events:
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
        cmp !disable_earthquake_id : beq .end
	LDA #$0018             ;\
	STA $183E              ;} Earthquake type = BG1, BG2 and enemies; 3 pixel displacement, horizontal
	LDA #$FFFF
	STA $1840
.end:
	rts

trigger_escape:
	phx : phy
	jsl rando_escape_escape_setup_l
	jsr room_earthquake	; could not be called by setup asm since not in escape yet
	; load timer graphics
	lda #$000f : jsl $90f084
	jsl utils_fix_timer_gfx
	lda #$0002 : sta $0943	 ; set timer state to 2 (MB timer start)
	jsr clear_music_queue
	jsr trigger_escape_music
	lda !escape_event : jsl !mark_event ; timebomb set event
	ply : plx
	rts

trigger_escape_music:
	lda #$0000 : jsl !song_routine ; stop current music
	lda.l custom_music_marker
	cmp !custom_music_id : beq .custom_music
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
	lda !escape_event : jsl !check_event ;if escape flag is off:
	bcs .end
	lda #$0003 : jsl $808FC1 	     ;  Queue elevator music track
.end:				 	     ;else do nothing
	rtl

;;; objectives checker functions, set carry if objective is completed
;;; helper macro to autodef simple event checker functions
macro eventChecker(func_name, event)
<func_name>:
	lda <event> : jsl !check_event
	rts
endmacro

%eventChecker(kraid_is_dead, !kraid_event)
%eventChecker(phantoon_is_dead, !phantoon_event)
%eventChecker(draygon_is_dead, !draygon_event)
%eventChecker(ridley_is_dead, !ridley_event)

all_g4_dead:
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

all_mini_bosses_dead:
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
.end
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
.end
        rts

macro nbBossChecker(n, bossType)
<bossType>_<n>_killed:
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
collect_<percent>_items:
	lda !CollectedItems
        cmp.l .pct              ; set carry when A is >= value
        rts
.pct:
        dw <percent>
endmacro

%itemPercentChecker(25)
%itemPercentChecker(50)
%itemPercentChecker(75)
%itemPercentChecker(100)

nothing_objective:
	;; if option enabled, complete objective only when in
	;; crateria/blue brin, in case we trigger escape immediately
	;; and we have custom start location.
	lda.l escape_option : and #$00ff : beq .ok
	lda.l objectives_options_mask : and #$0001 : beq .ok
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

all_items_mask:
	dw $f32f
all_beams_mask:
	dw $100f
all_major_items:
	lda $09A4 : cmp.l all_items_mask : bne .not
	lda $09A8 : cmp.l all_beams_mask : bne .not
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

all_chozo_robots:
	jsr golden_torizo_is_dead : bcc .end
	lda !BT_event : jsl !check_event : bcc .end
	lda !bowling_chozo_event : jsl !check_event : bcc .end
	lda !LN_chozo_lowered_acid_event : jsl !check_event
.end:
	rts

macro defineMapTile(tile, addr, mask)
map_tile_<tile>:
.addr:
        dw <addr>
.mask:
        dw <mask>
endmacro

macro checkMapTile(tile)
        lda.l map_tile_<tile>_addr : tax
        lda.l map_tile_<tile>_mask
        bit $0000,x
endmacro

%defineMapTile(etecoons, $0828, $0010)
%defineMapTile(dachora, $082c, $0020)

visited_animals:
        phx
	lda !area_index : cmp #!brinstar : bne .not
        %checkMapTile(etecoons) : beq .not
        %checkMapTile(dachora) : beq .not
.ok:
        sec
        bra .end
.not:
	clc
.end:
        plx
	rts

%eventChecker(king_cac_dead, !king_cac_event)

print "A1 end: ", pc
;; warnpc $a1faff

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
	lda !objectives_completed_event : jsl !check_event
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
	lda !king_cac_event : jsl !mark_event
.end:
	rtl

org $a3f350
check_red_fish_tickle:
	lda !current_room : cmp #$d104 : bne .end
	;; we're using grapple on a fish, in red fish room:
	lda !fish_tickled_event : jsl !mark_event
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
	lda !orange_geemer_event : jsl !mark_event
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
	lda !shak_dead_event : jsl !mark_event
.end:
	rtl

set_bowling_event:
	lda !bowling_chozo_event : jsl !mark_event
	LDA #$0001		; hijacked code
	rts

warnpc $aaf82f

;;; continue in 82 after InfoStr in seed_display.asm
org $82FB6D

print "Pause stuff: ", pc

;;;
;;; pause menu objectives display
;;;

;;; pause state
!pause_index = $0727

;;; pause index values
!pause_index_map_screen = #$0000
!pause_index_equipment_screen = #$0001
!pause_index_map2equip_fading_out = #$0002
!pause_index_map2equip_load_equip = #$0003
!pause_index_map2equip_fading_in = #$0004
!pause_index_equip2map_fading_out = #$0005
!pause_index_equip2map_load_map = #$0006
!pause_index_equip2map_fading_in = #$0007
;;; new screen:
!pause_index_objective_screen = #$0008
!pause_index_map2obj_fading_out = #$0009
!pause_index_map2obj_load_obj = #$000A
!pause_index_map2obj_fading_in = #$000B
!pause_index_obj2map_fading_out = #$000C
!pause_index_obj2map_load_map = #$000D
!pause_index_obj2map_fading_in = #$000E


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
!l_button = #$0020
!r_button = #$0010
!light_up_no_button = #$0000
!light_up_l_button  = #$0001
!light_up_r_button  = #$0002

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

;;; load from ROM $B6F200 to VRAM $3000 (bg1)
transfert_objective_bg1:
        php
        sep #$30

        LDA #$00     ;\
        STA $2116    ;| VRAM Address Registers (Low) - This sets the address for $2118/9
        LDA #$30     ;|
        STA $2117    ;| VRAM Address Registers (High) - This sets the address for $2118/9 => $3000
        LDA #$80     ;|
        STA $2115    ;} Video Port Control Register - Set VRAM transfer mode to word-access, increment by 1.
                     ;    0x80 == 0b10000000 => i---ffrr => i=1 (increment when $2119 is accessed),
                     ;    ff=0 (full graphic ??), rr=0 (increment by 2 bytes)
        JSL $8091A9 ; Set up a DMA transfer
        db $01,$01,$18
        dl $B6F200
        dw $0800
        LDA #$02
        STA $420B   ; start transfert

        plp
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
        JMP $B9C8    ; Map screen - draw Samus position indicator
.equip:
        JSR $B267    ; Draw item selector
        JSR $B2A2    ; Display reserve tank amount
        JMP $A56D    ; Updates the flashing buttons when you change pause screens
.objective:
        jsr draw_completed_objectives_sprites
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
        dw $2899, $2888, $289E, $289F, $289D

obj_bottom:
        dw $28A9, $2898, $28AE, $28AF, $28AD

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

draw_completed_objectives_sprites:
	phx : phy
	ldx.w #!max_objectives*2
.loop:
	dex : dex
	bmi .end
	lda.l objective_events,x : jsl !check_event
	bcc .loop
	;; draw objective completed sprite
	ldy completed_spritemaps,x
	jsr draw_spritemap
	bra .loop
.end:
	ply : plx
        rts

draw_spritemap:
        ;; Y: spritemap addr
        PHP
        REP #$30
        PHB

        PEA $8200
        PLB
        PLB
        LDA #$1E00
        STA $16                 ; palette * 200h
        lda #$0008
        STA $14                 ; X
	lda #$0080
        STA $12                 ; Y at screen center
        JSL $81879F ; Add spritemap to OAM

        PLB
        PLP
        RTS

;;; new pointers list
new_pause_actions_func_list:
        dw $9120                ; map
        dw $9142                ; equipment
        dw $9156, $91AB, $9231  ; map2equip
        dw $9186, $91D7, $9200  ; equip2map
        dw func_objective_screen
        dw func_map2obj_fading_out, func_map2obj_load_obj, func_map2obj_fading_in
        dw func_obj2map_fading_out, $91D7, $9200

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
        STZ $B1      ; BG1 X scroll = 0
        STZ $B3      ; BG1 Y scroll = 0
        JSR draw_completed_objectives_sprites
        JSR $A505    ; Checks for L or R input during pause screens
        JSR $A5B7    ; Checks for start input during pause screen
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
        JSR transfert_objective_bg1  ; objective screen - transfer BG1 tilemap
        JSR draw_completed_objectives_sprites
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
        JSR draw_completed_objectives_sprites
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
        JSR draw_completed_objectives_sprites
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


;;; sprites for completed objectives.
;;; an oam entry is made of five bytes: (s000000 xxxxxxxxx) (yyyyyyyy) (YXppPPPt tttttttt)
print " *** completed spritemaps: ", pc
first_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
second_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
third_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
fourth_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
fifth_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C

completed_spritemaps:
	dw first_spritemap, second_spritemap, third_spritemap, fourth_spritemap, fifth_spritemap

print "82 end: ", pc

;;; start of percent patch
warnpc $82ffbf

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

;;; new tiles for 'OBJ' button in unused tiles
org $B69100
        db $00,$ff,$00,$00,$ff,$ff,$ff,$ff,$f8,$f8,$f0,$f0,$f2,$f2,$f2,$f2,$ff,$ff,$ff,$ff,$00,$ff,$00,$ff,$07,$f8,$0f,$f0,$0d,$f2,$0d,$f2
org $B69300
        db $f2,$f2,$f2,$f2,$f0,$f0,$f8,$f8,$ff,$ff,$00,$ff,$00,$00,$00,$ff,$0d,$f2,$0d,$f2,$0f,$f0,$07,$f8,$00,$ff,$ff,$00,$ff,$ff,$ff,$ff
org $B693C0
        db $00,$ff,$00,$00,$ff,$ff,$ff,$ff,$c1,$c1,$4c,$4c,$4c,$4c,$41,$41,$ff,$ff,$ff,$ff,$00,$ff,$00,$ff,$3e,$c1,$b3,$4c,$b3,$4c,$be,$41
org $B693E0
        db $00,$ff,$00,$00,$ff,$ff,$ff,$ff,$f3,$f3,$f3,$f3,$f3,$f3,$f3,$f3,$ff,$ff,$ff,$ff,$00,$ff,$00,$ff,$0c,$f3,$0c,$f3,$0c,$f3,$0c,$f3
org $B695C0
        db $41,$41,$4c,$4c,$4c,$4c,$c1,$c1,$ff,$ff,$00,$ff,$00,$00,$00,$ff,$be,$41,$b3,$4c,$b3,$4c,$3e,$c1,$00,$ff,$ff,$00,$ff,$ff,$ff,$ff
org $B695E0
        db $93,$93,$93,$93,$83,$83,$c7,$c7,$ff,$ff,$00,$ff,$00,$00,$00,$ff,$6c,$93,$6c,$93,$7c,$83,$38,$c7,$00,$ff,$ff,$00,$ff,$ff,$ff,$ff

;;; blank objective screen from B6F200 to B6FA00
org $B6F200
objectivesText:
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        ;;                                                 ===== ::          O     B     J     E     C     T     I     V     E     S           ::    =====
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$68BD,$2801,$383E,$3831,$3839,$3834,$3832,$3843,$3838,$3845,$3834,$3842,$2801,$68BD,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
