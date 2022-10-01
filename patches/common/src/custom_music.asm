;;; allow music customizer to change various songs that are changed by
;;; game code instead of room state header
;;; data is laid out as in room state header, so the addresses can be
;;; added to pc_addresses entry in vanilla JSON track metadata
;;;
;;; compile with asar

lorom
arch snes.cpu

!song_routine = $808fc1

;;; max out the SPC communication timeout 
org $80805d
	dw #$ffff

;;; end of custom music data table. accounted for by MusicPatcher
org $8fe86b
	dw $caca		; identifier that we have custom music
print "title_screen_intro: ", pc
title_screen_intro:
	db $03, $05
print "menu: ", pc
menu:
	db $03, $06
print "escape: ", pc
escape:
	db $24, $07
print "credits: ", pc
credits:
	db $3c, $05
print "mb3: ", pc
mb3:
	db $48, $05
print "mb2: ", pc
mb2:
	db $21, $05

org $8b9b6c
	jsr load_title_screen_music_data

org $8b9b7f
	jsr load_title_screen_music_track

org $8b9a94
	jsr load_menu_music

org $8bdbac
	jsr load_credits_music_data

org $8bdbb3
	jsr load_credits_music_track

org $a9b1fe
	jsr load_escape_music_data

org $a9b282
	jsr load_escape_music_track

org $A6C0B6
	jsl ceres_escape

org $a9cc65
	jsr load_mb3_music_data

org $a9cc6c
	jsr load_mb3_music_track

org $a98859
	jsr load_mb2_music_data

org $a98e17
	jsr load_mb2_music_track

macro loadMusicData(data)
	lda.l <data>
	ora #$ff00
	rts
endmacro

macro loadMusicTrack(data)
	lda.l <data>+1
	and #$00ff
	rts
endmacro

org $8bf890
load_title_screen_music_data:
	%loadMusicData(title_screen_intro)

load_title_screen_music_track:
	%loadMusicTrack(title_screen_intro)

load_menu_music:
	lda #$0000 : jsl !song_routine
	lda.l menu
	ora #$ff00
	jsl !song_routine
	%loadMusicTrack(menu)

load_credits_music_data:
	%loadMusicData(credits)

load_credits_music_track:
	%loadMusicTrack(credits)

warnpc $8bf8ff

org $a9fc80
load_escape_music_data:
	%loadMusicData(escape)

load_escape_music_track:
	%loadMusicTrack(escape)

load_mb3_music_data:
	%loadMusicData(mb3)

load_mb3_music_track:
	%loadMusicTrack(mb3)

load_mb2_music_data:
	%loadMusicData(mb2)

load_mb2_music_track:
	%loadMusicTrack(mb2)

ceres_escape:
	lda #$0000 : jsl !song_routine
	lda.l escape
	ora #$ff00
	jsl !song_routine
	lda.l escape+1
	and #$00ff
	jsl !song_routine
	rtl
