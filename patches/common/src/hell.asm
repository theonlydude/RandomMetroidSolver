;;; permanent hell run
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

lorom
arch 65816

incsrc "macros.asm"

org $8fe89d
	jsr add_heat_fx		; setup asm call

%freespaceStart($8ff410)
add_heat_fx:
        JSR ($0018,x)           ; hijacked code
	phy
	ldy #$f761 : jsl $8dc4e9 ; spawn heat dmg fx
	ply
	rts

print "8f end: ", pc
%freespaceEnd($8ff41f)
