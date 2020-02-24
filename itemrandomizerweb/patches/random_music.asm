;;; Randomize music
;;;
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; HIJACKS
org $808FD8
	;; use a jml to avoid touching the stack
	jml music_queue

org $809006
	jsl music_queue_timer

org $82E102
	jml load_new_music

org $a98810
	rep 4 : nop		; disables MB2 "no music" before fight, as cutscene is sped up

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
	dw $ff1e	; Tourian

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
	db $01	; Tourian

;;; check that music in A is in musics_list table.
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
	jml $808fdc		; called with jml
	
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

load_new_music:
;;; $82:E102 C5 14       CMP $14    [$7E:0014]
;;; $82:E104 F0 0A       BEQ $0A    [$E110]
	;; if new music, load it
	;; if same music, check if the new one is a random one, if it is, load it anyway
	cmp $14 		; original code
	beq .same_music
	jml $82E106		; go back to music changing code
.same_music:
	pha			; save A
	lda $07F3 : ora #$FF00	; set music xx in A: 0xFFxx
	jsr is_music_to_randomize
	pla			; restore A
	bcc .notrandom
	jml $82E106		; go to the part of the hijacked function which load the new music
.notrandom:
	jml $82E110		; go to the end of the hijacked function

randomize_music_and_track:
	;; pla has set the n flag in calling functions.
	;; music data has its first byte as 0xFF (negative)
	phx
	bmi .check_music
	bra .check_track
.check_music:
	jsr is_music_to_randomize
	bcc .end
.randomize_music:
	;; call RNG, result in A
	jsl $808111
	;; A = A % 16
	and #$000F
	;; X = A*2
	asl : tax
	;; load in A value of musics_list[x]
	lda.l musics_list,x
	bra .end
.check_track:
	pha
	lda $063d     ; load current music
	jsr is_music_to_randomize
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
	cmp #$0001 : bne .randomize_track
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
	clc : adc #$0005
.end:
	plx
	rts

warnpc $a1f3ff
