;;; Common definitions for doors patches

include

;;; Define some vanilla instructions and instruction lists

org $84BD0F
check_shot:

;; Borrow open instruction sequences from blue doors
org $84C489
open_left:
org $84C4BA
open_right:
org $84C4EB
open_top:
org $84C51C
open_bottom:

org $84C4B1
closed_blue_door_left:
org $84A9B3
draw_closed_blue_door_left:
org $84C4E2
closed_blue_door_right:
org $84A9EF
draw_closed_blue_door_right:
org $84C513
closed_blue_door_top:
org $84AA2B
draw_closed_blue_door_top:
org $84C544
closed_blue_door_bottom:
org $84AA67
draw_closed_blue_door_bottom:

org $84A767
draw_PB_left:
org $84A797
draw_PB_right:
org $84A7C7
draw_PB_top:
org $84A7F7
draw_PB_bottom:
org $84A827
draw_super_left:
org $84A857
draw_super_right:
org $84A887
draw_super_top:
org $84A8B7
draw_super_bottom:
org $84A8E7
draw_missile_left:
org $84A917
draw_missile_right:
org $84A947
draw_missile_top:
org $84A977
draw_missile_bottom:
org $84A6A7
draw_none_left:
org $84A6D7
draw_none_right:
org $84A707
draw_none_top:
org $84A737
draw_none_bottom:

;;; Colored doors indicators: new door PLM that acts like a blue door,
;;; but blinks a door color while the matching door on the other side
;;; is closed (using equal PLM room argument for both doors).
!blink_frames_blue = 9
!blink_frames_colored = !blink_frames_blue

macro closeListIndicator_left()
;; $C49E: Instruction list - door $C8A2 (shot/bombed/grappled reaction, shootable, BTS 40h. Blue door facing left) ;;;
	dw $0002,$A677,$0002,$A9D7,$8C19
	db $08        ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002,$A9CB,$0002,$A9BF
endmacro

macro closeListIndicator_right()
;;; $C4CF: Instruction list - door $C8A8 (shot/bombed/grappled reaction, shootable, BTS 41h. Blue door facing right) ;;;
	dw $0002,$A683,$0002,$AA13,$8C19
	db $08        ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
        dw $0002,$AA07,$0002,$A9FB
endmacro

macro closeListIndicator_top()
;;; $C500: Instruction list - door $C8AE (shot/bombed/grappled reaction, shootable, BTS 42h. Blue door facing up) ;;;
	dw $0002,$A68F,$0002,$AA4F,$8C19
	db $08        ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
	dw $0002,$AA43,$0002,$AA37
endmacro

macro closeListIndicator_bottom()
;;; $C531: Instruction list - door $C8B4 (shot/bombed/grappled reaction, shootable, BTS 43h. Blue door facing down) ;;;
	dw $0002,$A69B,$0002,$AA8B,$8C19
	db $08        ; Queue sound 8, sound library 3, max queued sounds allowed = 6 (door closed)
	dw $0002,$AA7F,$0002,$AA73
endmacro

macro defineIndicator(req,direction)
close_list_indicator_<req>_<direction>:
	;; paste vanilla closing blue door instruction list
	%closeListIndicator_<direction>()
main_list_indicator_<req>_<direction>:
	;; set to blue door if PLM room arg is set (ie matching door is open)
	dw $8A72,closed_blue_door_<direction>
	;; link instruction=open door (don't set flags)
	dw $8A24,open_<direction>
	;; pre-instruction=go to link instruction if shot
        dw $86C1,check_shot
.blink_loop:
	dw !blink_frames_blue,draw_closed_blue_door_<direction>
	dw !blink_frames_colored,draw_<req>_<direction>
	dw $8724,.blink_loop
endmacro

macro defineIndicatorPLM(req,direction)
%export(plm_indicator_<req>_<direction>)
	dw $C7B1
	dw main_list_indicator_<req>_<direction>
	dw close_list_indicator_<req>_<direction>
endmacro
