;;; Randomize music
;;;
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; hijack les deux routines de chargement de la musique
;;; table avec les 16 id de musique qu'on veut randomizer
;;; on appele la fonction RNG puis on la modulo 16
;;; le format de la musique c'est 0xFFxx (musique data) ou 0x00xx (musique track)
;;; on randomize que le music data (que tu crois)
;;; 
;;; on hijack ici:
;;; $80:8FD8 68          PLA                
;;; $80:8FD9 EC 3B 06    CPX $063B  [$7E:063B]
	
;;; et la:
;;; $80:9006 9D 19 06    STA $0619,x[$7E:0619]
;;; $80:9009 98          TYA

;;; HIJACKS
org $808FD8
	jsl music_queue

org $809006
	jsl music_queue_timer

org $A1F300
musics_list:
	;; do not change order below, the second table is dependent on it
	;; music set index
	dw $ff09	; Lower Crateria
	dw $ff0c	; Upper Crateria PBs
	dw $ff0f	; Green Brinstar
	dw $ff12	; Red Brinstar
	dw $ff15	; Upper Norfair
	dw $ff1b	; Maridia 1
	dw $ff1b	; Maridia 2
	dw $ff30	; Wrecked Ship 1
	dw $ff30	; Wrecked Ship 2
	dw $ff18	; Lower Norfair
	dw $ff36	; Intro
	dw $ff1b	; Maridia 2
	dw $ff18	; Lower Norfair
	dw $ff12	; Red Brinstar
	dw $ff0f	; Green Brinstar
	dw $ff36	; Intro

number_tracks:
	;; number of possible music tracks
	db $01	; Lower Crateria
	db $01	; Upper Crateria PBs
	db $01	; Green Brinstar
	db $01	; Red Brinstar
	db $01	; Upper Norfair
	db $02	; Maridia 1
	db $02	; Maridia 2
	db $02	; Wrecked Ship 1
	db $02	; Wrecked Ship 2
	db $01	; Lower Norfair
	db $01	; Intro
	db $02	; Maridia 2
	db $01	; Lower Norfair
	db $01	; Red Brinstar
	db $01	; Green Brinstar
	db $01	; Intro

;;; check that musique in A is in musics_list table.
;;; set carry flag if true.
is_music_to_randomize:
	;; set X to 0
	ldx #$0000
.loop:
	;; compare A with value in table at position X
	cmp.l musics_list,x
	beq .music_is_random
	inx : inx
	cpx #$0020 : beq .music_is_not_random : bra .loop
.music_is_not_random:
	;; clear carry flag
	clc
	bra .endloop
.music_is_random:
	;; set carry flag
	sec
.endloop:	
	rts

music_queue:
;;; $80:8FD8 68          PLA                
;;; $80:8FD9 EC 3B 06    CPX $063B  [$7E:063B]
	pla			; original code
	jsr randomize_music_and_track
	cpx $063b		; original code
	rtl
	
music_queue_timer:
;;; $80:9006 9D 19 06    STA $0619,x[$7E:0619]
;;; $80:9009 98          TYA
	phy			; save Y
	cmp #$0000		; sets cpu flags wrt A value
	jsr randomize_music_and_track
	ply			; restore Y
	sta $0619,x		; original code
	tya			; original code
	rtl

randomize_music_and_track:
	;; pla has set the n flag in calling functions.
	;; music data has its first byte as 0xFF (negative)
	phx
	bmi .check_music
	bra .check_track
.check_music:
	jsl is_music_to_randomize
	bcc .end
.randomize_music:
	;; call RNG, result in A
	jsl $808111
	;; A = A % 16
	and #$000F
	;; X = A*2
	asl
	;; load in A value of musics_list[x]
	lda.l musics_list,x
	bra .end
.check_track:
	pha
	lda $063d     ; load current music
	jsl is_music_to_randomize
	pla			; pla doesn't change the carry flag
	bcc .end
	;; check if track is 0x05 or 0x06 (track1 or track2)
	cmp #$0005 : beq .track_ok
	cmp #$0006 : beq .track_ok
	bra .end
.track_ok:
	;; load number of tracks using X/2 (X was set in is_music_to_randomize)
	txa : lsr : tax
	lda.l number_tracks,x
	and #$00ff
	cmp $#0001 : bne .randomize_track
	;;  if only one track, use it (track1 = 0x05)
	lda #$0005
	bra .end
.randomize_track:
	;; two tracks, randomize between them (track1=0x05, track2=0x06)
	;; call RNG, result in A
	jsl $808111
	;; A = A % 2
	and #$0001
	;; A = A + 0x05
	clc : adc #$05
.end:
	plx
	rts

warnpc $a1f3ff
