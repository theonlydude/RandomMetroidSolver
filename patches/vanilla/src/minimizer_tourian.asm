;;; Tourian speedup for minimizer :
;;; - use specific addresses for rom flavor
;;;
;;; Compiles with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

incsrc "sym/minimizer_tourian_common.asm"

;;; Replace door hit instruction with alternative one for
;;; all left facing gadoras
org $84d887
	dw minimizer_tourian_common_alt_door_hit

;;; overwrite setup/main asm ptrs for all room states
;;; (not sure if it's necessary, at least one state seems
;;;  useless)
org $8fdd80
	dw minimizer_tourian_common_mb_room_main

org $8fdd86
	dw minimizer_tourian_common_mb_room_setup

org $8fdd9a
	dw minimizer_tourian_common_mb_room_main

org $8fdda0
	dw minimizer_tourian_common_mb_room_setup

org $8fddb4
	dw minimizer_tourian_common_mb_room_main

org $8fddba
	dw minimizer_tourian_common_mb_room_setup
