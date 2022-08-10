;;; VARIA HUD to display current area (in the area randomizer sense),
;;; the split type (M for major, or Z for chozo), and the remaining
;;; number of items of the chosen split in the current area (1 digit
;;; for M/Z, 2 digits in full - no split indicator, and more items)
;;;
;;; It also handles Scavenger mode HUD. If the rando writes a list
;;; of required locations (see address format specified at scav_order),
;;; it will :
;;; - display the next scav loc to get to in the HUD, and its index in the
;;;   scav list
;;; - cycle through remaining required scav locs (the route) during pause
;;; - prevent the player to go to out of order scav locs
;;; - prevent the player to go through G4 if all required scav locs have
;;;   not been collected.
;;; When all required scav locs have been collected, the HUD displays 'HUNT OVER',
;;; and the !hunt_over_event is set

;;; Includes etank bar combine by lioran

;;; Compile with "asar" (https://github.com/RPGHacker/asar/releases)

!game_state = $0998		; used to check pause/unpause

!hudposition = #$0006
;;; RAM used to store previous values to see whether we must draw
;;; area/item counter or next scav display
!previous = $7fff3c		; hi: area/00, lo: remaining items/next scav loc
;;; RAM for remaining items in current area
!n_items = $7fff3e
;;; RAM for current index in scav list order in scavenger
!scav_idx = $7ed86a		; saved to SRAM automatically
!scav_tmp  = $7fff40		; temp RAM used for a lot of stuff in scavenger
!hud_special = $7fff42		; temp RAM used to draw temporary stuff in the HUD (prompt, notification)
!hud_special_timer = $7fff44	; and associated timer
;;; item split written by randomizer
!seed_type = $82fb6c
;;; vanilla bit array to keep track of collected items
!item_bit_array = $7ed870
;;; bit index to byte index/bitmask routine
!bit_index = $80818e
;;; RAM area to write to for split/locs in HUD
!split_locs_hud = $7ec618

;;; special HUD display state mask, by priority
!press_xy_hud_mask = $8000	; hud_special bit telling we shall write 'PRESS X-Y' in scavenger hunt pause
!all_objectives_hud_mask = $4000 ; hud_special bit telling we shall write 'OBJS OK!'
!objective_hud_mask = $2000     ; hud_special bit telling we shall write an individual objective

;;; objectives notifications display
!objective_global_mask = (!all_objectives_hud_mask|!objective_hud_mask)
!notification_display_frames = #300 ; 5 seconds
!timer = $05b8
!obj_check_period = #$0020	; unit:frames, works only in powers of 2

;;; scavenger stuff
!hunt_over_hud = #$11		; HUD ID of the fake loc 'HUNT OVER'
!ridley_id = #$00aa
!area_index = $079f
!norfair = #$0002
!ridley_timer = $0FB2
!scav_next_found = #$aaaa

incsrc "event_list.asm"

lorom

;;; hijack the start of health handling in the HUD to draw area or
;;; remaining items if necessary
org $809B8B
	JSR draw_info

;;; hijack load room state, to init remaining items counter
org $82def7
	jml load_state

;;; yet another item pickup hijack, different from the ones in endingtotals and bomb_torizo
;;; this one is used to count remaining items in current area, and handle scavenger hunt
org $848899
	jml item_pickup
org $84889D
item_resume_pickup:
org $8488AF
item_abort_pickup:

;;; a bunch of hijacks post item collection to count items
org $8488de			; Beams
	nop : nop : nop
	jsl item_post_collect

org $848905			; Equipment
	nop : nop : nop
	jsl item_post_collect

org $848930			; Grapple
	nop : nop : nop
	jsl item_post_collect

org $848957			; X-Ray
	nop : nop : nop
	jsl item_post_collect

org $848975			; ETank
	nop : nop : nop
	jsl item_post_collect

org $848998			; RTank
	nop : nop : nop
	jsl item_post_collect

org $8489c1			; Missile
	nop : nop : nop
	jsl item_post_collect

org $8489ea			; Super
	nop : nop : nop
	jsl item_post_collect

org $848a13			; Power Bomb
	nop : nop : nop
	jsl item_post_collect

org $A6A377
	jml scav_ridley_check
org $A6A37C
ridley_initial_wait_show:
org $A6A388
ridley_initial_wait_continue:

org $A6C58B
	jml scav_ridley_dead
org $A6C550
ridley_still_dying:
org $A6C590			; would have been simpler to just hijack here, but already done by minimizer bosses patch
ridley_dead:

;;; skip top row of auto reserve to have more room (HUD draw main routine)
org $809B61
write_reserve_main:
	bra .write_mid_reserve_row
org $809B6F
.write_mid_reserve_row:

;;; skip top row of auto reserve to have more room (pause screen manual/auto switch)
org $82AF08
write_reserve_pause_enable:
	bra .write_mid_reserve_row
org $82AF16
.write_mid_reserve_row:

org $82AF36
write_reserve_pause_disable:
	bra .write_mid_reserve_row
org $82AF3E
.write_mid_reserve_row:


;;; the following code will overwrite the normal etank drawing code,
;;; no extra space required, just turn the 2 lines of 14 etank into
;;; 1 lines of combined 14 etanks
org $809B99
	STA $4204
	SEP #$20
	LDA #$64
	STA $4206 
	REP #$30
	LDA #$0000
	STA $14
	LDY #$0007
	TAX
	LDA $4216
	STA $12
	-
	LDA $14 : CLC : ADC #$0064 : STA $14
	ADC #$02BC : STA $16
	INX : INX 
	LDA $09C4
	CMP $14 : BCS +;check if empty
	LDA #$2C0F
	BRA ++
	+
	LDA $09C2
	CMP $16 : BCC +
	LDA #$2C31
	BRA ++
	+
	CMP $14 : BCC +
	LDA #$2831
	BRA ++
	+
	LDA #$3430
	++
	STA $7EC648,x
	DEY
	BNE -
	NOP 
;end of etank row combine

org $80d130
draw_info:
	phx
	phy
	php

	;; check if an objective has recently been completed
	;; if so, !hud_special will be set with a special value
	jsl check_objectives
	;; determine if we should show some special state
	lda !hud_special
	bne .special

	;; normal display
.normal:
	;; check if we should show scav loc/index or area/items
	lda !scav_idx
	asl : tax
	lda.l scav_order,x
	cmp #$ffff : bne .draw_next_scav
	jmp .draw_area

	;; special values by priority :
.special:
	;; - "PRESS X-Y" prompt in scavenger
	bmi .draw_press_xy
	;; - all objectives completed notification
	bit #!all_objectives_hud_mask : bne .draw_all_objectives_ok
	;; - individual objective completed notification
	bit #!objective_hud_mask : bne .draw_objective
	;; unknown
	bra .normal
.draw_press_xy:
	ldy #press_xy-hud_text
	jsr draw_text
	bra .game_state_check
.draw_objective:
	ldy #objective_completed-hud_text
	jsr draw_text
	;; draw objective index
	lda !hud_special : and #$00ff : inc : jsr draw_one
	jmp .end
.draw_all_objectives_ok:
	ldy #all_objectives_completed-hud_text
	jsr draw_text
	jmp .end

	;; Display scavenger hunt status
.draw_next_scav:
	and #$00ff
	cmp !previous : beq .scav_setup_next
	sta !previous
	asl : asl : asl : asl
	clc : adc #scav_names-hud_text
	tay
	jsr draw_text
.draw_scav_index:
	;; don't show index if showing special stuff
	lda !previous : cmp.w !hunt_over_hud : beq .scav_setup_next
	;; show current index in required scav list
	lda #$2C0F : sta !split_locs_hud-2 ; blank before numbers for cleanup
	lda !scav_idx : inc : jsr draw_two
.scav_setup_next:
	lda !previous : cmp.w !hunt_over_hud : bne .game_state_check
	jmp .end

	;; Scavenger pause:
	;; when pausing, we allow the user to press X/Y to
	;; cycle through the remaining items.
	;; during this phase, scav_tmp is used to store
	;; maj_index backup in its low byte, and current
	;; increment due to button pressed its high byte
	;; scav_tmp is set to ffff when not in pause
.game_state_check:
	lda !game_state
	cmp #$000f : beq .pause_start_check
	cmp #$0010 : beq .pause_end
	jmp .end
.pause_start_check:
	lda !scav_tmp
	cmp #$ffff : beq .pause_init
	bra .pause
.pause_init:
	sep #$20
	lda !scav_idx : sta !scav_tmp
	lda #$00 : sta !scav_tmp+1	; current increment=0
	rep #$20
	;; show "PRESS X-Y" next frame
	lda #!press_xy_hud_mask : ora !hud_special : sta !hud_special
	;; reset previous value to trigger redraw
	lda #$ffff : sta !previous
	jmp .end
.pause_end:
	lda !scav_tmp
	cmp #$ffff : bne .pause_deinit
	jmp .end
.pause_deinit:
	lda !scav_tmp : and #$00ff : sta !scav_idx
	lda #$ffff : sta !scav_tmp
	;; clear press X-Y flag
	lda !hud_special : and #~!press_xy_hud_mask : sta !hud_special
	jmp .end
.pause:
	sep #$20
	xba
	bne .pause_next_scav
	;; no action registered, check if we must register one
	rep #$20
	lda $8f			; newly pressed input
	bit #$0040 : bne .pause_x_was_pressed
	bit #$4000 : bne .pause_y_was_pressed
	jmp .end
.pause_x_was_pressed:
	lda #$0001
	bra .pause_store_action
.pause_y_was_pressed:
	lda #$ffff
.pause_store_action:
	sep #$20 : sta !scav_tmp+1 : rep #$20
	jmp .end
.pause_next_scav:
	;; action required: user pressed X or Y last frame
	;; first, save our action increment and check if we're
	;; just displaying the first item (works with either button)
	pha
	rep #$20
	lda !hud_special : bmi .pause_first_scav
	sep #$20
	pla
	;; add action increment (1 or -1) to scav_idx	
	clc : adc !scav_idx : sta !scav_idx
	cmp !scav_tmp : bmi .pause_first_scav_store
	asl : tax
	lda.l scav_order,x
	cmp.b !hunt_over_hud : beq .pause_end_list
	bra .pause_next_scav_end
.pause_end_list:
	lda !scav_idx : dec : sta !scav_idx
	bra .pause_next_scav_end
.pause_first_scav:
	;; clear press X-Y flag
	and #~!press_xy_hud_mask : sta !hud_special
	sep #$20
	pla
.pause_first_scav_store:
	lda !scav_tmp : sta !scav_idx
	lda #$00 : sta !scav_idx+1
.pause_next_scav_end:
	;; reset action
	lda #$00 : sta !scav_tmp+1
	rep #$20
	jmp .end

	;; Draw current area name and remaining items in it
.draw_area:
	;; determine current graph area
	ldx $07bb
	sep #$20
	lda $8f0010,x
	;; check if we must draw it
	cmp !previous
	beq .items
	sta !previous
	rep #$20
	;; get text address
	and #$00ff
	asl : asl : asl : asl
	clc : adc #area_names-hud_text
	tay
	;; draw text
	jsr draw_text
	lda #$2C0F : sta !split_locs_hud-2 ; blank before numbers for cleanup
.items:
	;; check if we must draw remaining items counter
	sep #$20
	lda !n_items : cmp !previous+1
	beq .end
	sta !previous+1
	lda !seed_type
	rep #$20
	and #$00ff
	cmp #$005a		; 'Z'
	beq .draw_chozo
	cmp #$004d		; 'M'
	beq .draw_major
	;; default to full split: draw remaining item count on 2 digits
	lda !n_items : jsr draw_two
	bra .end
.draw_chozo:
	lda #$0CF9 : sta !split_locs_hud ; blue 'Z'
	bra .draw_items
.draw_major:
	lda #$0CEC : sta !split_locs_hud ; blue 'M'
.draw_items:
	lda !n_items : jsr draw_one

.end:
	plp
	ply
	plx
	lda $09C2 ;original code that was hijacked
	rts

; A=remaining items (2 digits)
draw_two:
	sta $4204
	sep #$20
	lda #$0a
	sta $4206
	pha : pla : pha : pla : rep #$20
	lda $4214 : asl : tay
	lda NumberGFXTable, y
	sta !split_locs_hud
	lda $4216
draw_one:			; A=remaining items (1 digit)
	asl : tay
	lda NumberGFXTable, y
	sta !split_locs_hud+2
	rts

;; Normal numbers (like energy/ammo)
NumberGFXTable:
	DW #$0C09,#$0C00,#$0C01,#$0C02,#$0C03,#$0C04,#$0C05,#$0C06,#$0C07,#$0C08

;;; Y ptr to string, relative to hud_text
draw_text:
	ldx !hudposition
.loop:
	lda hud_text,y
	beq .end
	sta $7ec602,x
	iny : iny
	inx : inx
	bra .loop
.end:
	rts

;; ;; Inverse video numbers
;; NumberGFXTable:
;; 	DW #$0C45,#$0C3C,#$0C3D,#$0C3E,#$0C3F,#$0C40,#$0C41,#$0C42,#$0C43,#$0C44

table "tables/hud_chars.txt"
hud_text:
area_names:
	dw " CERES "
	dw $0000
	dw " CRATER"
	dw $0000
	dw "GR BRIN"
	dw $0000
	dw "RED BRI"
	dw $0000
	dw " W SHIP"
	dw $0000
	dw " KRAID "
	dw $0000
	dw "UP NORF"
	dw $0000
	dw " CROC  "
	dw $0000
	dw "LO NORF"
	dw $0000
	dw "W MARID"
	dw $0000
	dw "E MARID"
	dw $0000
	dw "TOURIAN"
	dw $0000

scav_names:
	dw " MORPH "
	dw $0000
	dw " BOMB  "
	dw $0000
	dw " CHARGE"
	dw $0000
	dw " SPAZER"
	dw $0000
	dw " VARIA "
	dw $0000
	dw "HI-JUMP"
	dw $0000
	dw "  ICE  "
	dw $0000
	dw " SPEED "
	dw $0000
	dw "  WAVE "
	dw $0000
	dw "GRAPPLE"
	dw $0000
	dw " X-RAY "
	dw $0000
	dw "GRAVITY"
	dw $0000
	dw " SPACE "
	dw $0000
	dw " SPRING"
	dw $0000
	dw " PLASMA"
	dw $0000
	dw " SCREW "
	dw $0000
	dw " RIDLEY"
	dw $0000
	dw "HUNT OVER "
	dw $0000

;; special values
press_xy:
	dw "PRESS X-Y "
	dw $0000

objective_completed:
	dw " OBJ OK!  "
	dw $0000

all_objectives_completed:
	dw " OBJS OK! "
	dw $0000

cleartable

print "b80 end: ", pc

warnpc $80d5ff

org $a1f550

incsrc "locs_by_areas.asm"

;;; used only in scavenger hunt mode, written to by rando
;;; have a word for each location of required order in scavenger mode:
;;; hi byte: location ID as in item bit array (same IDs used in locs_by_areas)
;;; lo byte: item/location index in scav_names list for HUD display
;;; #$ffff=scav list terminator
scav_order:
	fillbyte $ff : fill 38	; (17 max scav locs+"HUNT OVER"+terminator)*2

;;; ROM option for auto escape trigger when objectives are completed (see objectives.asm)
print "escape_option: ", pc
escape_option:
	skip 2			; value written in objectives.asm

load_state:
	lda #$ffff
	sta !previous
	sta !scav_tmp
	jsr compute_n_items
	;; hijacked code
	LDX $07BB
	LDA $0003,x
	jml $82DEFD		; resume routine

;;; return
;;; - carry set if in scav mode, clear if not
;;; - X set to index in scav_order
;;; - A scav_order entry
scav_mode_check:
	lda !scav_idx : asl : tax
	lda.l scav_order,x
	cmp #$ffff : beq .not_scav ; not in scavenger mode
.scav:
	sec
	bra .end
.not_scav:
	clc
.end:
	rtl

;;; X : index in scav list
;;; !scav_tmp: next scav loc ID
;;; Y : loc ID of current pickup
;;;
;;; returns carry set if pickup allowed, clear if not.
;;; !scav_tmp contains !scav_next_found if the location
;;; found is the next scav loc, otherwise garbage
scav_list_check:
	tya : cmp !scav_tmp : beq .found_next_scav
	;; now checks if the item we found is in the remaining list
.scav_list_check_loop:
	inx : inx
	lda.l scav_order,x
	cmp #$ffff : beq .allow
	and #$ff00 : xba : sta !scav_tmp
	tya : cmp !scav_tmp : beq .deny
	bra .scav_list_check_loop
.found_next_scav:
	lda !scav_next_found : sta !scav_tmp
.allow:
	sec
	bra .end
.deny:
	clc
.end:
	rts

found_next_scav:
	lda !scav_idx : inc : sta !scav_idx
	asl : tax
	lda.l scav_order,x : and #$00ff
	cmp.w !hunt_over_hud : bne .end
	;; last item pickup : set scav hunt event
	lda !hunt_over_event : jsl !mark_event
	bra .end
.end:
	lda #$ffff : sta !scav_tmp
	rts

scav_ridley_check:
	phx : phy
	dec !ridley_timer
	bne .continue
	;; here, Ridley is supposed to show up
	lda !area_index : cmp !norfair : bne .show ; don't check Ceres Ridley
	jsl scav_mode_check
	bcc .show				   ; not in scav mode
	;; scav_tmp = loc ID to check against
	and #$ff00 : xba : sta !scav_tmp
	ldy !ridley_id
	jsr scav_list_check
	lda #$ffff : sta !scav_tmp
	bcs .show
	inc !ridley_timer
.continue:
	ply : plx
	jml ridley_initial_wait_continue
.show:
	ply : plx
	jml ridley_initial_wait_show

scav_ridley_dead:
	dec !ridley_timer
	bpl .not_dead
	;; dead: see if it was the scav location, and advance
	phx
	jsl scav_mode_check
	bcc .dead
	and #$ff00 : xba
	cmp !ridley_id : bne .dead
	;; Ridley was indeed the next scav location
	jsr found_next_scav
	bra .dead
.not_dead:
	jml ridley_still_dying
.dead:
	lda !ridley_event : jsl !mark_event
	plx
	jml ridley_dead

item_pickup:
	phy
	phx
	;; check if loc ID is the next required scav
	jsl scav_mode_check
	bcc .pickup_end_return ; not in scavenger mode
	;; scav_tmp = loc ID to check against
	and #$ff00 : xba : sta !scav_tmp
	;; checks if picked up loc is the next scav loc
	;; Room PLM arg, which gives us our loc ID, has been pushed at the start
	;; of the hijacked routine. Get it back in Y, and save it back to the stack
	ply : phy
	lda $1dc7,y : tay
	jsr scav_list_check
	bcc .nopickup_end
.pickup_end:
	lda !scav_tmp : cmp !scav_next_found : beq .found_next_scav
	lda #$ffff : sta !scav_tmp
	bra .pickup_end_return
.found_next_scav:
	jsr found_next_scav
.pickup_end_return:
	plx
	ply
	phx			; stack balance, X will be pulled at the end of hijacked routine
	LDA $1DC7,x		; remaining part hijacked code
	jml item_resume_pickup
.nopickup_end:			; routine end when we prevent item pick up (forbidden item)
	lda #$ffff : sta !scav_tmp
	plx
	ply
	rep 6 : dey		; move back PLM instruction pointer to "goto draw"
	jml item_abort_pickup	; jump to hijacked routine exit

item_post_collect:
	jsr compute_n_items
	LDA #$0168 : JSL $82E118 ;} Play room music track after 6 seconds
.end:
	rtl

compute_n_items:
	phx
	phy
	lda #$0000 : sta !n_items ; temporarily used to count collected items in current area
	ldy #$0000		; Y will be used to store number of items in current area
	;; go through loc id list for current area, counting collected items
	;; determine current graph area
	ldx $07bb : lda $8f0010,x
	;; get loc id list index in bank A1 in X
	asl : tax : lda.l locs_by_areas,x : tax
.count_loop:
	lda $a10000,x : and #$00ff
	cmp #$00ff : beq .end
	phx
	jsl !bit_index
	lda !item_bit_array,x : and $05e7
	beq .next
	lda !n_items : inc : sta !n_items
.next:
	plx
	iny
	inx
	bra .count_loop
.end:
	;; here, n_items contain collected items, and Y number of items
	;; make it so, n_items contains remaining items:
	;; n_items = max(0, Y - n_items) ; handle < 0 for some restricted locs cases
	tya : sec : sbc !n_items
        bpl .store
        lda #$0000
.store:
        sta !n_items
	bne .ret
	;; 0 items left, trigger appropriate event : current graph area idx+area_clear_event_base
	ldx $07bb : lda $8f0010,x
	clc : adc !area_clear_event_base
	jsl !mark_event
.ret:
	ply
	plx
	rts

;;; checks if the HUD shall draw/stop drawing objective notifications,
;;; updates !hud_special
print "check_objectives: ", pc
check_objectives:
	;; check if we're drawing stuff
	lda !hud_special
	;; press x-y should be drawn, do nothing
	bmi .ret
	bit #!objective_global_mask : beq .check
	;; draw objective notification:
	;; when in pause, cancel
	lda !game_state : cmp #$000f : beq .stop_draw
	;; handle timer
	lda !hud_special_timer : dec : sta !hud_special_timer
	beq .stop_draw
.ret:
	rtl
.stop_draw:
	;; clear both draw flags, as "all objectives" has priority
	lda #~!objective_global_mask : and !hud_special : sta !hud_special
	;; reset previous value to trigger redraw
	lda #$ffff : sta !previous
	lda !objectives_completed_event : jsl !check_event : bcs .all_notified
	;; it was an individual objective, get index and set notification event
	lda !hud_special : and #$00ff : asl : tax
	lda.l objective_notified_events,x : jsl !mark_event
	bra .end
.all_notified:
	lda !objectives_completed_event_notified : jsl !mark_event
	bra .end
	;; check objectives
.check:
	;; when in pause, don't check anything
	lda !game_state : cmp #$000f : beq .end
	;; align check prequency with objectives (check one frame later)
	lda !timer : and !obj_check_period-1
	bne .end
.check_all:
	;; check if all objectives are completed and if we should notify
	lda !objectives_completed_event_notified : jsl !check_event : bcs .end
	lda !objectives_completed_event : jsl !check_event : bcc .check_indiv
	;; notify all objectives completed
	lda #!all_objectives_hud_mask : ora !hud_special : sta !hud_special
	bra .notify
	;; check individual objectives
.check_indiv:
	ldx.w #!max_objectives*2
.loop:
	dex : dex
	bmi .end
	lda.l objective_notified_events,x : jsl !check_event
	bcs .loop
	;; objective not notified, check completion
	lda.l objective_completed_events,x : jsl !check_event
	bcc .loop
	;; notify objective completed but not displayed yet
	lda #$ff00 : and !hud_special : sta !hud_special
	txa : lsr : ora !hud_special
	;; display mask in hi byte, objective number in low byte
	ora #!objective_hud_mask : sta !hud_special
.notify:
	lda !notification_display_frames : sta !hud_special_timer
.end:
	rtl

objective_completed_events:
%objectivesCompletedEventArray()

objective_notified_events:
%objectivesNotifiedEventArray()

print "a1 end: ", pc
warnpc $a1f8ff
