;;; Randomize music in game
;;;
;;; Music will change only if music requested by the game is different from last
;;; requested music.
;;;
;;; Uses RNG routine but does not alter current RNG number.
;;; Uses tracking patch RTA timer to seed RNG.
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; CONSTANTS
!tracks_tbl_sz	= #$0018
!nb_tracks_8b	= #$0c
!last_music_rq	= $7fff30	; RAM address to store music requests by the game
!last_music_rnd = $7fff32	; RAM address to store our random music
!room_music	= $07cb
!room_track	= $07c9
!current_music	= $07f3
!current_track	= $07f5
!RNG		= $808111	; RNG function
!RNG_seed	= $05e5
!RTA_timer	= $05b8		; see tracking.asm

;;; HIJACKS
org $82DF3E
	;; hijack room state header load to replace music/track
	;; area escape rando hijacks before and returns control after,
	;; so it has to call a function here
	jml load_room_music_no_escape_rando

org $a98810
	rep 4 : nop		; disables MB2 "no music" before fight, as cutscene is sped up

org $A1F300
musics_list:
	;; music set index
	;; hi: music data index
	;; lo: music track index
	dw $0905	; Lower Crateria
	dw $0c05	; Upper Crateria PBs
	dw $0f05	; Green Brinstar
	dw $1205	; Red Brinstar
	dw $1505	; Upper Norfair
	dw $1b05	; Maridia 1
	dw $1b06	; Maridia 2
	dw $3005	; Wrecked Ship 1
	dw $3006	; Wrecked Ship 2
	dw $1805	; Lower Norfair
	dw $3605	; Intro
	dw $1e05	; Tourian

;;; check that music in A is in musics_list table.
;;; set carry flag if true.
;;; if carry flag is set, X holds index in musics_list
;;; doesn't touch A
is_music_to_randomize:
	;; set X to 0
	ldx #$0000
.loop:
	;; compare A with value in table at position X
	cmp.l musics_list,x
	beq .music_is_random
	inx : inx
	cpx !tracks_tbl_sz : beq .music_is_not_random : bra .loop
.music_is_not_random:
	;; clear carry flag
	clc
	bra .endloop
.music_is_random:
	;; set carry flag
	sec
.endloop:
	rts

;;; single use random function that leaves game rng untouched
rand:
	lda !RNG_seed : pha
	eor !RTA_timer : sta !RNG_seed
	jsl !RNG : pha
	pla : sta !RNG_seed
	pla
	rts

;;; gets a random data/track couple from table, and store it in last_music_rnd (and A)
get_random_music:
	;; call RNG, result in A
	jsr rand
	;; A = A % nb_tracks
	sta $4204
	;; switch to 8-bit mode for divisor
	sep #$20
	lda !nb_tracks_8b : sta $4206
	pha : pla : xba : xba 	; wait for division
	;; back to 16-bit mode
	rep #$20
	lda $4216		; get remainder to have modulo
	;; load random data/track couple in A
	asl : tax : lda.l musics_list,x
	sta !last_music_rnd
	rts

;;; hijacks room music loading. the music data and track index in room header
;;; will be randomized if:
;;; - new music is actually requested
;;; - this new music is different from the last new music we tried to load
;;; xxtt with tt 05 or 06 and xx not 0 => if music combination is to be randomized,
;;; 		                          randomize and use it.
;;; 					  if not store as asked.
;;; 					  in all cases, store asked music
;;; xxtt with tt not 05 or 06 => if xx is 0, store it as asked.
;;;                              if not, check if xx05 or xx06 matches last asked music.
;;;                              if it does not, randomize music but just store it
;;;                              in last random music.
;;; 				 if it does, store as asked
;;; 0005/0006 => if last asked song was randomized, restore random music
;;; 		 if not, restore last asked music
load_room_music:
	phx
	;; at this point, A contains music data index in lo byte, 0 in hi
	;; X contains room header index in bank 8F (DB=8F)
	xba
	sep #$20
	lda $0005,x
	;; A now contains music data in hi byte and track in lo byte
	;; (from room header)
	cmp #$05	: beq .track_ok
	cmp #$06	: beq .track_ok
	rep #$20
	bit #$ff00	: beq .store_music	; vanilla load if 00xx
	;; here, music data is != 0, but track is neither 05 nor 06
	;; check if data|05 or data|06 matches last music request
	pha
	and #$ff00 : ora #$0005
	cmp !last_music_rq : beq .restore_music
	and #$ff00 : ora #$0006
	cmp !last_music_rq : beq .restore_music
	;; randomize music but don't use it, just store it in last_music_rnd
	jsr get_random_music
	pla : pha
	and #$ff00 : ora #$0005
	sta !last_music_rq	; store data|05 as last requested
.restore_music:
	pla
	bra .store_music
.track_ok:
	;; if music data = 0 but track is 5 or 6, load last music (randomized or not)
	xba : beq .dont_change	; still in 8 bits mode here
	xba
	;; check if music/track couple is to be randomized
	rep #$20
	jsr is_music_to_randomize : bcc .dont_randomize
	cmp !last_music_rq	  : bne .randomize
	;; we're here when new music is asked but it's the same
	;; as the last asked new music.
.dont_change:
	;; restore last randomized music if last asked music was randomized
	;; if not, restore last asked music
	rep #$20
	lda !last_music_rq
	jsr is_music_to_randomize : bcc .store_music
	lda !last_music_rnd	  : bra .store_music
.dont_randomize:
	sta !last_music_rq
	bra .store_music
.randomize:
	sta !last_music_rq
	jsr get_random_music
.store_music:
	;; stores A word as defined in musics_list is RAM room header
	sep #$20
	sta !room_track
	xba
	sta !room_music
	rep #$20
.end:
	plx
	rts

load_room_music_no_escape_rando:
	jsr load_room_music
	jml $82DF4A

warnpc $a1f3ef

org $a1f3f0		 ; fixed position used in area_rando_escape
load_room_music_escape_rando:
	lda $0004,x : and #$00ff ; reload music data index (needed by load_room_music)
	jsr load_room_music
	rtl

warnpc $a1f3ff
