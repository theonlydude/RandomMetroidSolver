;;; This patch handles area rando door transitions:
;;; - for incompatible transitions, cancel samus movement
;;; - changes song if needed
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; Constants :
;;; For spark hijack
!spark_flag            = $0741  ; free ram (used from pause screen stuff) to store global shinespark cancel flag
!MAGIC                 = #$caca ; magic value for spark flag check
!samus_health          = $09c2
;;; For movement cancel
!current_pose          = $0a1c
!poses_transitions     = $0a2a	
!contact_dmg_idx       = $0a6e
!iframes               = $18a8
;;; For refill
!samus_max_health      = $09c4
!samus_reserve         = $09d6
!samus_max_reserve     = $09d4
!samus_missiles        = $09c6
!samus_max_missiles    = $09c8
!samus_supers          = $09ca
!samus_max_supers      = $09cc
!samus_pbs             = $09ce
!samus_max_pbs         = $09d0
!samus_reserve         = $09d6
!samus_max_reserve     = $09d4

;;; hijack shinespark end check to avoid teleport transition spark bug
org $90d2ba
	;; do a jsr to overwrite the lda
	jsr shinespark_end
org $90f700
shinespark_end:
	;; at this point A should contain samus health and is
	;; about to be compared to 30 so when we return from this,
	;; A shall contain either samus health or a < 30 value to
	;; cancel spark
	lda !spark_flag
	cmp !MAGIC
	beq +
	lda !samus_health	; load samus health
	rts
+
	lda #$0010		; if cancel spark flag is set, fill A with fake health, and clear flag
	stz !spark_flag
	rts

org $8fea30
print "incompatible_doors:"
print pc
;;; routine called from door ASM when connecting two incompatible doors
;;; stops samus, forces her in elevator pose and gives iframes
incompatible_doors:
	;; cancel samus movement:
	stz $0b2c ; VY subpix
	stz $0b2e ; VY pix
	stz $0b42 ; VX pix
	stz $0b44 ; VX subpix
	stz $0b46 ; momentum pix
	stz $0b48 ; momentum subpix
	;; force samus "elevator pose" to avoid taking into account transition direction
	;; for this, reflect "stable elevator pose" state :
	;; - set 12 bytes of pose-handling stuff to zero
	ldx #$0000
-
	stz !current_pose,x
	inx : inx
	cpx #$000c
	bne -
	;; - set 6 bytes pose transition stuff to FF
	lda #$ffff
	ldx #$0000
--
	sta !poses_transitions,x
	inx : inx
	cpx #$0006
	bne --
	;; - reset animation timer
	stz $0a96
	;; set cancel spark flag if a spark is active
	lda !contact_dmg_idx
	cmp #$0002		; contact damage is 2 if samus is sparking
	bne .end
	lda !MAGIC
	sta !spark_flag
.end:
print "giveiframes:"
print pc
;;; gives 128 I-frames to samus
;;; also called from door ASM when connecting compatible doors
giveiframes:
	lda #$0080
	sta !iframes
	rts

;;; "ship refill" for tourian elevator
full_refill:
	;; check that we're in area rando (this patch is also applied in boss rando)
	lda $c5d564 : and #$00ff : cmp #$00f2 : bne .end
	;; actual refill
	lda !samus_max_health
	sta !samus_health
	lda !samus_max_reserve
	sta !samus_reserve
	lda !samus_max_missiles
	sta !samus_missiles
	lda !samus_max_supers
	sta !samus_supers
	lda !samus_max_pbs
	sta !samus_pbs
.end:
	rts

;;; stop before generated door asm routines start
warnpc $8feaff

org $83922c                     ; Tourian Elevator door ASM ptr
    dw full_refill
