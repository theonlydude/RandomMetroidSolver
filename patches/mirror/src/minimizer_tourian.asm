;;; Tourian speedup for minimizer :
;;; - use specific addresses for rom flavor
;;;
;;; Compiles with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

incsrc "sym/minimizer_tourian_common.asm"
incsrc "sym/bank_8f.asm"

;;; Replace door hit instruction with alternative one for
;;; all right facing gadoras
org $84d9be
	dw minimizer_tourian_common_alt_door_hit

;;; overwrite setup/main asm ptrs for all room states
;;; (not sure if it's necessary, at least one state seems
;;;  useless)
org bank_8f_Room_FD40_state_FD56_Header+18
	dw minimizer_tourian_common_mb_room_main

org bank_8f_Room_FD40_state_FD56_Header+24
	dw minimizer_tourian_common_mb_room_setup

org bank_8f_Room_FD40_state_FD70_Header+18
	dw minimizer_tourian_common_mb_room_main

org bank_8f_Room_FD40_state_FD70_Header+24
	dw minimizer_tourian_common_mb_room_setup

org bank_8f_Room_FD40_state_FD8A_Header+18
	dw minimizer_tourian_common_mb_room_main

org bank_8f_Room_FD40_state_FD8A_Header+24
	dw minimizer_tourian_common_mb_room_setup
