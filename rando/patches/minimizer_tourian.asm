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

;;; change MB2 main AI script pointer to MB3 death instead
;;; of triggering baby cutscene
org $a9b90e
	dw $c1cf
