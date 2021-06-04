;;; VARIA HUD to display current area (in the area randomizer sense),
;;; the split type (M for major, or Z for chozo), and the remaining
;;; number of items of the chozen split in the current area (1 digit
;;; for M/Z, 2 digits in full - no split indicator, and more items)
;;;
;;; It also handles Scavenger mode HUD. If the rando writes a list
;;; of required majors (see address format specified at majors_order),
;;; it will :
;;; - display the next major to collect in the HUD, and its index in the
;;;   majors list
;;; - cycle through remaining required majors (the route) during pause
;;; - prevent the player to pick up out of order majors by triggering
;;;   a game over if they do
;;; - prevent the player to go through G4 if all required majors have
;;;   not been collected. For this, it replaces g4_skip asm, so don't
;;;   apply g4_skip when this patch is applied.
;;; When all required majors have been collected, Tourian access is
;;; unlocked, and the HUD falls back to remaining items mode.

;;; Includes etank bar combine by lioran

;;; Compile with "asar" (https://github.com/RPGHacker/asar/releases)

!hudposition = #$0006
;;; RAM used to store previous values to see whether we must draw
;;; area/item counter or next major display
!previous = $7fff3c		; hi: area/00, lo: remaining items/next major
;;; RAM for remaining items in current area
!n_items = $7fff3e
;;; RAM for current index in major list order
!major_idx = $7ed86a		; saved to SRAM automatically
!major_tmp  = $7fff40
;;; item split written by randomizer
!seed_type = $82fb6c
;;; vanilla bit array to keep track of collected items
!item_bit_array = $7ed870
;;; bit index to byte index/bitmask routine
!bit_index = $80818e
;;; RAM area to write to for split/locs in HUD
!split_locs_hud = $7ec618

!game_state = $0998
!major_timer = #$80
!mark_event = $8081FA
!hunt_over_hud = #$0010

lorom

;;; hijack the start of health handling in the HUD to draw area or
;;; remaining items if necessary
org $809B8B
	JSR draw_info

;;; hijack load room state, to init remaining items counter
org $82def7
	jml load_state

;;; yet another item pickup hijack, different from the ones in endingtotals and bomb_torizo
;;; this one is used to count remaining items in current area
org $848899
	jml item_pickup


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

	;; first, determine if we should show next major item or area/items
	lda !major_idx : asl : tax
	lda.l majors_order,x
	cmp #$ffff : bne .draw_next_major
	jmp .draw_area
.draw_next_major:
	and #$00ff
	cmp !previous : beq .major_setup_next
	sta !previous
	asl : asl : asl : asl
	tay
	;; draw text
	ldx !hudposition
.draw_major_loop:
	lda majors_names,y
	beq .maj_index
	sta $7ec602,x
	iny : iny
	inx : inx
	bra .draw_major_loop
.maj_index:
	;; don't show index if hunt is over
	lda !previous : cmp !hunt_over_hud : beq .major_setup_next
	;; show current index in required major list
	lda !major_idx : inc : jsr draw_two
.major_setup_next:
	;; when pausing, we cycle through the remaining items.
	;; during this phase, major_tmp is used to store
	;; maj_index backup in its low byte, and frames
	;; remaining until next item in its high byte
	;; major_tmp is set to ffff when not in pause
	lda !game_state
	cmp #$000c : beq .pause_start
	cmp #$0010 : beq .pause_end
	bra .pause_check
.pause_start:
	lda !major_tmp
	cmp #$ffff : beq .pause_init
	jmp .end
.pause_init:
	sep #$20
	lda !major_idx : sta !major_tmp
	lda !major_timer : lsr : sta !major_tmp+1 ; half timer for the first we already know
	rep #$20
	jmp .end
.pause_end:
	lda !major_tmp
	cmp #$ffff : bne .pause_deinit
	jmp .end
.pause_deinit:
	lda !major_tmp : and #$00ff : sta !major_idx
	lda #$ffff : sta !major_tmp
	jmp .end
.pause_check:
	lda !major_tmp
	cmp #$ffff : bne .pause
	jmp .end
.pause:
	sep #$20
	xba
	dec
	beq .pause_next_major
	sta !major_tmp+1
	rep #$20
	jmp .end
.pause_next_major:
	lda !major_timer : sta !major_tmp+1
	lda !major_idx : inc : sta !major_idx
	rep #$20
	;; cycle through if we reach the end of the route
	and #$00ff : asl : tax
	lda.l majors_order,x : and #$00ff
	cmp !hunt_over_hud : beq .cycle_major
	jmp .end
.cycle_major:
	lda !major_tmp : and #$00ff : sta !major_idx
	jmp .end
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
	tay
	;; draw text
	ldx !hudposition
.draw_area_loop:
	lda area_names,y
	beq .items
	sta $7ec602,x
	iny : iny
	inx : inx
	bra .draw_area_loop
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

;; ;; Inverse video numbers
;; NumberGFXTable:
;; 	DW #$0C45,#$0C3C,#$0C3D,#$0C3E,#$0C3F,#$0C40,#$0C41,#$0C42,#$0C43,#$0C44

table "tables/hud_chars.txt"

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

majors_names:
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
	dw "HUNT OVER "
	dw $0000

cleartable

print "b80 end: ", pc

warnpc $80d4ff

org $a1f550

incsrc "locs_by_areas.asm"

;;; used only in scavenger hunt mode, written to by rando
;;; have a word for each major of required order in scavenger mode:
;;; hi byte: location ID as in item bit array (same IDs used in locs_by_areas)
;;; lo byte: item/location index in majors_names list for HUD display
;;; #$ffff=major list terminator
majors_order:
	fillbyte $ff : fill 36	; (16 max majors+"HUNT OVER"+terminator)*2

load_state:
	lda #$ffff
	sta !previous
	sta !major_tmp
	jsr compute_n_items
	;; hijacked code
	LDX $07BB
	LDA $0003,x
	jml $82DEFD		; resume routine

item_pickup:
	phy
	phx
	jsr compute_n_items
	;; check if loc ID is the next required major
	lda !major_idx : asl : tax
	lda.l majors_order,x
	cmp #$ffff : beq .pickup_end ; not in scavenger mode, or all required majors collected
	;; major_tmp = loc ID to check against
	and #$ff00 : xba : sta !major_tmp
	;; checks if picked up loc is the next major.
	;; Room PLM arg, which gives us our loc ID, has been pushed at the start
	;; of the hijacked routine. Get it back in Y, and save it back to the stack
	ply : phy
	lda $1dc7,y : cmp !major_tmp : beq .found_next_major
	;; now checks if the item we found is in the remaining list
.major_check_loop:
	inx : inx
	lda.l majors_order,x
	cmp #$ffff : beq .pickup_end
	and #$ff00 : xba : sta !major_tmp
	lda $1dc7,y : cmp !major_tmp : beq .nopickup_end
	bra .major_check_loop
.found_next_major:
	lda !major_idx : inc : sta !major_idx
	asl : tax
	lda.l majors_order,x
	cmp #$ffff : bne .pickup_end
	;; we picked up last major, reset previous for HUD drawing to switch back to area
	sta !previous
.pickup_end:			; routine end when we pick up the item
	lda #$ffff : sta !major_tmp
	plx
	ply
	LDA $1DC7,x		; remaining part hijacked code
	phx			; stack balance, X will be pulled at the end of hijacked routine
	jml $84889D		; resume pickup
.nopickup_end:			; routine end when we prevent item pick up (forbidden item)
	lda #$ffff : sta !major_tmp
	plx
	ply
	rep 6 : dey		; move back PLM instruction pointer to "goto draw"
	jml $8488AF		; jump to hijacked routine exit

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
	;; n_items = Y - n_items
	tya : sec : sbc !n_items : sta !n_items
	ply
	plx
	rts

print "a1 end: ", pc
warnpc $a1f6ff

;;; make golden statues instructions check for majors collection
;;; in scavenger mode :
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
;;; set event in argument only if not in scavenger mode, or all majors collected
alt_set_event:
	phx
	;; skip check if not in scavenger mode:
	lda !major_idx : asl : tax
	lda.l majors_order,x : cmp #$ffff : beq .set_event
	;; in scavenger mode, check if the hunt is over
	and #$00ff : cmp !hunt_over_hud : bne .end
.set_event:
	lda $0000,y : jsl !mark_event
.end:
	iny : iny
	plx
	rts

org $838c5c
	dw alt_g4_skip

;;; same place as g4_skip patch door asm
org $8ffe00
alt_g4_skip:
    ;; skip check if not in scavenger mode:
    lda !major_idx : asl : tax
    lda.l majors_order,x : cmp #$ffff : beq .g4_skip
    ;; in scavenger mode, check if the hunt is over
    and #$00ff : cmp !hunt_over_hud : bne +
.g4_skip:
    ;; original g4_skip code:
    lda $7ed828
    bit.w #$0100
    beq +
    lda $7ed82c
    bit.w #$0001
    beq +
    lda $7ed82a
    and.w #$0101
    cmp.w #$0101
    bne +
    lda $7ed820
    ora.w #$0400
    sta $7ed820
+
    rts
