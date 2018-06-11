;;; This patch handles area rando door transitions:
;;; - for incompatible transitions, cancel samus movement
;;; - changes song if needed
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; Constants :
;;; For spark hijack
!spark_flag = $0741 ; free ram (used from pause screen stuff) to store global shinespark cancel flag
!MAGIC = #$caca	    ; magic value for spark flag check
!samus_health = $09c2
;;; For movement cancel
!current_pose = $0a1c
!contact_dmg_idx = $0a6e
!iframes = $18a8
;;; For song change
!song_routine = $808fc1

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

org $0fea00
cancel_movement:
	;; cancel samus movement:
	stz $0b2c ; VY subpix
	stz $0b2e ; VY pix
	stz $0b42 ; VX pix
	stz $0b44 ; VX subpix
	stz $0b46 ; momentum pix
	stz $0b48 ; momentum subpix
	;; samus "elevator pose" to avoid taking into account transition direction
	;; only if samus is not unmorphing to avoid game crash
	lda #$003d 		; check for unmorph right pose
	cmp !current_pose
	beq .end_cancel	        ; you can't shinespark and unmorph at the same time, so skip to the end
	lda #$003e 		; check for unmorph left pose	
	cmp !current_pose
	beq .end_cancel	        ; you can't shinespark and unmorph at the same time, so skip to the end
	stz !current_pose	; set elevator pose (0)
	stz $0a96		; reset animation timer
	;; set cancel spark flag if a spark is active
	lda !contact_dmg_idx
	cmp #$0002		; contact damage is 2 if samus is sparking
	bne .end_cancel
	lda !MAGIC
	sta !spark_flag
.end_cancel:
	;; gives 128 I-frames to samus to handle disorientation
	lda #$0080
	sta !iframes
	rts

;;; changes current song: shall be #$ff<song> in A
change_song:
	pha			; save song to load
	lda #$0000		; stops current song
	jsl !song_routine
	pla			; retrieve song to load
	jsl !song_routine   	; change song
	lda #$0005         	; load song track 5 (First track from song data)
	jsl !song_routine
	rts
