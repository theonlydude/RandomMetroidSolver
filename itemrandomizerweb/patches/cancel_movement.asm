;;; This patch brings a 'cancel movement' routine in $0fea00 that will be used for the
;;; area randomizer for incompatbile 'teleport' door transitions
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

!spark_flag = $0741 ; free ram (used from pause screen stuff) to store global shinespark cancel flag
!MAGIC = #$caca	    ; magic value for spark flag check

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
	lda $09c2		; load samus health
	rts
+
	lda #$0010		; if cancel spark flag is set, fill A with fake health, and clear flag
	stz !spark_flag
	rts

org $0fea00
cancel_movement:
	;cancel samus movement:
	stz $0b2c ; VY subpix
	stz $0b2e ; VY pix
	stz $0b42 ; VX pix
	stz $0b44 ; VX subpix
	stz $0b46 ; momentum pix
	stz $0b48 ; momentum subpix
	;;samus "elevator pose"
	stz $0a1c
	stz $0a96
	;; set cancel spark flag if a spark is active
	lda $0A6E
	cmp #$0002
	beq .sparking
	rts
.sparking:
	lda !MAGIC
	sta !spark_flag
	rts
