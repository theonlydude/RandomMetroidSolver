;;; Tourian speedup for minimizer :
;;; - connects G4 door to Tourian Eye Door Room
;;; - transforms Gadora into a Tourian Guardian (invincible until you
;;;   beat all Golden Four)
;;; - add door ASM for Gadora's door: refill+kill the zebs and MB
;;;   glass
;;;
;;; Compiles with asar

arch snes.cpu
lorom

!full_refill = $f700    ; short ptr in bank 8F (see area_rando_doors.asm)
!mark_event  = $8081fa
!bit_index   = $80818e  ; returns X=byte index, $05e7=bitmask
	
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
	;; check if all G4 are dead (g4 check borrowed from g4_skip patch)
	lda $7ed828
	bit.w #$0100
	beq .end
	lda $7ed82c
	bit.w #$0001
	beq .end
	lda $7ed82a
	and.w #$0101
	cmp.w #$0101
	bne .end
	;; if they are dead, set door open for gadora
print "test pre_tourian_door: ", pc
	phx
	lda #$00a8 : jsl !bit_index
	lda $7ED8B0,x : ora $05E7 : sta $7ED8B0,x
	plx
.end:
	rts

warnpc $8ff7ef

;;; connect Statues Hallway to Tourian Eye Door Room...
org $8fa616
	dw $aa5c
;;; ...and back
org $8fddeb
	dw $9216

;;; alternative door hit instruction that skips hit counter check
org $848a6d ; end of some unused instruction
alt_door_hit:
	clc
	bra .skip_check		; resume original routine
org $848aa3
.skip_check:

;;; Replace door hit instruction with alternative one for
;;; all left facing gadoras (it's ok since other gadoras are
;;; removed in minimizer mode)
org $84d887
	dw alt_door_hit

;;; door asm ptr for Tourian eye door
org $83aaae
	dw tourian_door

;;; door asm ptr for door leading to Tourian eye door
org $83aa66
	dw pre_tourian_door
	;; dw $f76e

org $91ffee
enable_hyper:
	jsr $e5f0
	rtl

warnpc $91ffff

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
	lda #$8000
	sta $0a4a	; set rainbow samus
	jsl enable_hyper
.end:
	lda #$b189	; hijacked code
	rts

hyper_end:
	stz $0a4a		; unrainbow samus
	;; reset various samus palette stuff
	stz $0ace
	stz $0ad0
	stz $0b62
	;; load samus suit palette
	jsl $91deba
	lda #$b1d5	  ; hijacked code
	rts
