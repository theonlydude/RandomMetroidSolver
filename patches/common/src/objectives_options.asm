;;; Objectives options: need to be read by several patches

lorom
arch 65816

incsrc "macros.asm"

org $a1f550
;;; if non-zero trigger escape as soon as objectives are completed
%export(escape_flag)
	db $00
;;; low bit (0): with nothing objective, trigger escape only in crateria
;;; high bit (7): play sfx on objective completion (don't use for vanilla objectives)
;;; bit 1: if set, objectives will be hidden in pause menu until a room is visited (usually G4)
;;; VARIA tweaks BT options:
;;; bit 2: don't wake up BT on item collection. set to 1 if nothing item and no "trigger chozo bots" objective
%export(settings_flags)
	db %00000001
