;;; allow music customizer to change various songs that are changed by
;;; game code instead of room state header
;;; data is laid out as in room state header, so the addresses can be
;;; added to pc_addresses entry in vanilla JSON track metadata
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

lorom
arch 65816

incsrc "macros.asm"

!song_routine = $808fc1

;;; max out the SPC communication timeout 
org $80805d
	dw #$ffff

;;; disable data load in some elevator rooms (custom music will change
;;; tracks in rooms around them instead)

;;; [Elevator to Maridia]
org $8f94dd
        db $00
;;; [Elevator to Green Brinstar]
org $8f9949
        db $00
;;; Warehouse Entrance
org $8fa6b2
        db $00
;;; Bowling Alley
org $8fc9be
        db $00
org $8fc9a4
        db $00

;;; end of custom music data table. accounted for by MusicPatcher
org $8fe86b
marker:
	dw $caca		; identifier that we have custom music

;;; load custom music in special places
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

%freespaceStart($8bf890)
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

%freespaceEnd($8bf8ff)

%freespaceStart($a9fc80)
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

print "a9 end: ", pc
%freespaceEnd($a9fcff)

; SPC Engine Echo Improvements
; By H A M
; The echo on a channel when a sound is finished gets re-activated, and the echo never applies to a sound.
; Use asar 1.90.
; I actually made this while i was porting songs from "Zelda no Densetsu - Kamigami no Triforce".
; Version 1.02: save more bytes in SPC RAM
; Version 1.01: save 1 byte each in ROM and SPC RAM

!SPCFreespace = $04BE ; put it in somewhere that mITroid's key off patches never touch

org $808459 : JML SPC_Engine_Upload ; hijack

%freespaceStart($81ff80)
SPC_Engine_Upload:
        LDA $80845D : STA $00 : LDA $80845E : STA $01 : JSL $808024 ; upload SPC engine to APU (gets repointed by SMART)
        TDC : - : DEC : BNE - ; wait for SPC to be available for upload
        JSL $80800A : dl Patch ; upload patch
        JML $808482 ; back to normal code
Patch:
arch spc700
spcblock $1A4B nspc ; echo enable command
	mov $4F,a ; store to unused ram
endspcblock
spcblock $15FE nspc
	call ResumeEchoAfterHandlingMusicTrack
endspcblock
spcblock !SPCFreespace nspc
ResumeEchoAfterHandlingMusicTrack:
	call $1793
	mov a,$1A ; Echo enable flags = [$4F] AND NOT [enabled sound voices]
	eor a,#$FF
	and a,$4F
	mov $4A,a
	ret
endspcblock
;; execute $1500
        dw $0000, $1500
