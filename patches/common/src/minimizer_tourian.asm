;;; Tourian speedup for minimizer :
;;; - connects G4 door to Tourian Eye Door Room
;;; - transforms Gadora into a Tourian Guardian (invincible until you
;;;   beat all Golden Four)
;;; - add door ASM for Gadora's door: refill+kill the zebs and MB
;;;   glass
;;; - skips MB3 fight and baby cutscene: MB dies at the end of MB2,
;;;   and you get hyper+refill for the escape
;;;
;;; Compiles with asar

arch snes.cpu
lorom

!full_refill = $f700    ; short ptr in bank 8F (see area_rando_doors.asm)
!bit_index   = $80818e  ; returns X=byte index, $05e7=bitmask
!refill_f    = $7fff36	; health refill during hyper beam acquisition
!hyper_animation_2frames = #$9d	; nb of frames of hyper animation/2 (because divisor has to be 8-bits)
!samus_health          = $09c2
!samus_max_health      = $09c4
!samus_reserve         = $09d6
!samus_max_reserve     = $09d4
!current_room          = $079b
!tourian_eye_door_room = #$ddc4

incsrc "event_list.asm"

;;; connect Statues Hallway to Tourian Eye Door Room...
org $8fa616
	dw $aa5c
;;; update door bit flag
org $83aa5e
	db $40
;;; ...and back
org $8fddeb
	dw $9216
;;; update door bit flag
org $839218
	db $40


org $848a59                     ; unused instruction
;;; alternative door hit instruction that skips hit counter check
alt_door_hit:
        ;; test if current room is Tourian Door Room
        lda !current_room
        cmp !tourian_eye_door_room
        bne .vanilla_door_hit
	clc
	bra .skip_check		; resume original routine

warnpc $848a72

org $848a91
.vanilla_door_hit:

org $848aa3
.skip_check:

;;; Replace door hit instruction with alternative one for
;;; all left facing gadoras
org $84d887
	dw alt_door_hit

;;; door asm ptr for Tourian eye door
org $83aaae
	dw tourian_door

;;; door asm ptr for door leading to Tourian eye door
org $83aa66
	dw pre_tourian_door
	;; dw $f76e


;;; overwrite setup/main asm ptrs for all room states
;;; (not sure if it's necessary, at least one state seems
;;;  useless)
org $8fdd80
	dw mb_room_main

org $8fdd86
	dw mb_room_setup

org $8fdd9a
	dw mb_room_main

org $8fdda0
	dw mb_room_setup

org $8fddb4
	dw mb_room_main

org $8fddba
	dw mb_room_setup

org $91ffee
enable_hyper:
	jsr $e5f0
	rtl

warnpc $91ffff

org $8ff730
;;; gadora door asm
tourian_door:
	;; remove MB glass and kill zebetites
	lda #$0002 : jsl !mark_event
	lda #$0003 : jsl !mark_event
	lda #$0004 : jsl !mark_event
	lda #$0005 : jsl !mark_event
	;; free ship refill here instead of Tourian elevator
	jsr !full_refill
	rts

;;; statues door asm leading to gadora room
pre_tourian_door:
	;; check if objectives are completed
	lda !objectives_completed_event : jsl !check_event
        bcc .end
	;; if they are completed, set door open for gadora
print "test pre_tourian_door: ", pc
	phx
	lda #$00a8 : jsl !bit_index
	lda $7ED8B0,x : ora $05E7 : sta $7ED8B0,x
	plx
.end:
	rts

;;; MB room setup/main asm: refill samus health during hyper beam animation
mb_room_setup:
	lda #$0000 : sta !refill_f
	rts

mb_room_main:
	lda !refill_f
	beq .end
	clc : adc !samus_health
	cmp !samus_max_health : bmi .add
	bcs .max
	bra .end
.max:
	lda !samus_max_health
.add:
	sta !samus_health
.end:
	rts

warnpc $8ff7ef

;;; change MB2 main AI script pointer to MB3 death instead
;;; of triggering rainbow beam, baby cutscene etc
org $a9b90e
	dw $c1cf

;;; hijack final MB death cutscene start (head on the floor)
;;; and start hyper acquisition animation
;;; carefully chosen because it runs only once, not every frame
org $a9b17f
	jsr hyper_start

;;; hijack escape start and stop hyper acquisition animation
;;; carefully chosen because it runs only once, not every frame
org $a9b1be
	jsr hyper_end

;;; skips MB invicibility palette handling to avoid flashing bug
;;; during death animation
org $a9cfdb
	bra $1f

org $a9fc00
hyper_start:
        ;; clear current charging beam to avoid vanilla bug related to flares
        STZ $0CD0
        STZ $0CD6
        STZ $0CD8
        STZ $0CDA
        STZ $0CDC
        STZ $0CDE
        STZ $0CE0
        ;; set rainbow samus
	lda #$8000 : sta $0a4a
	jsl enable_hyper
	;; compute health increase per frame: health to refill/nb frames
	lda !samus_max_health
	sec : sbc !samus_health
	sta $4204
	sep #$20
	lda !hyper_animation_2frames : sta $4206
	pha : pla : xba : xba
	rep #$20
	lda $4214
	;; divide by 2, because divisor is halved as well (we lose 1 bit of precision)
	lsr
	bne .store_refill
	lda #$0001 		; still one if 0 to animate something
.store_refill:
	sta !refill_f
	lda #$b189	; hijacked code
	rts

hyper_end:
	;; unrainbow samus
	stz $0a4a
	jsr reset_samus_palette
	;; load samus suit palette
	jsl $91deba
	;; stop health refill and cap health to max
	lda #$0000 : sta !refill_f
	lda !samus_max_health  : sta !samus_health
	lda !samus_max_reserve : sta !samus_reserve
	lda #$b1d5	  ; hijacked code
	rts

reset_samus_palette:
	;; reset various samus palette stuff
	stz $0ace
	stz $0ad0
	stz $0b62
	rts

warnpc $a9fc7f
