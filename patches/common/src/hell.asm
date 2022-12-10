;;; permanent hell run
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

lorom
arch 65816

org $8fe893
	jsr add_heat_fx		; setup asm call

org $8ff410
add_heat_fx:
	phy
	ldy #$f761 : jsl $8dc4e9 ; spawn heat dmg fx
	ply
	ldx $07bb		; hijacked code
	rts
