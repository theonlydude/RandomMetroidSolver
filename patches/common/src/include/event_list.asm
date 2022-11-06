include

math pri on

;;; event routines
!mark_event = $8081FA
!check_event = $808233

;;; vanilla main events
!tourian_open_event = #$000a
!escape_event = #$000e
!maridia_tube_open = #$000b
!LN_chozo_lowered_acid_event = #$000c
!shaktool_cleared_path = $000d

;;; vanilla boss events
; $7E:D828..2F: Boss bits. Indexed by area
;     1: Area boss (Kraid, Phantoon, Draygon, both Ridleys)
;     2: Area mini-boss (Spore Spawn, Botwoon, Crocomire, Mother Brain)
;     4: Area torizo (Bomb Torizo, Golden Torizo)
;
; $079F: Area index
;     0: Crateria
;     1: Brinstar
;     2: Norfair
;     3: Wrecked Ship
;     4: Maridia
;     5: Tourian
;     6: Ceres
;     7: Debug

; event bytes start at $7ED820
; event code is: (byte index << 3) + ln(boss bit), with byte index == area index + 8
!kraid_event = #$0048
!phantoon_event = #$0058
!draygon_event = #$0060
!ridley_event = #$0050
!spospo_event = #$0049
!botwoon_event = #$0061
!croc_event = #$0051
!GT_event = #$0052
!BT_event = #$0042

;;; VARIA events
!VARIA_event_base = #$0080

;; objectives events : a global objectives completed event for endgame
;; and individual events for each objective :
;; - is it completed?
;; - if completed, was the user notified in the HUD?
;;   (can never be set if HUD is disabled)
!objectives_completed_event = !tourian_open_event ; reuse tourian entrance event
!objectives_completed_event_notified = !VARIA_event_base+0

;; scavenger hunt completion
!hunt_over_event = !VARIA_event_base+1

;; clear area events : events based on area index, from 1 (crateria) to 10 (east maridia),
!area_clear_event_base = !VARIA_event_base+4 ; has to be unused, will be set as ceres cleared if ceres start
!crateria_cleared_event = !VARIA_event_base+5
!green_brin_cleared_event = !VARIA_event_base+6
!red_brin_cleared_event = !VARIA_event_base+7
!ws_cleared_event = !VARIA_event_base+8
!kraid_cleared_event = !VARIA_event_base+9
!upper_norfair_cleared_event = !VARIA_event_base+10
!croc_cleared_event = !VARIA_event_base+11
!lower_norfair_cleared_event = !VARIA_event_base+12
!west_maridia_cleared_event = !VARIA_event_base+13
!east_maridia_cleared_event = !VARIA_event_base+14
!tourian_cleared_event = !VARIA_event_base+15 ; not useful, here as a placeholder bc it will be set entering tourian

;; memes
!fish_tickled_event = !VARIA_event_base+2
!orange_geemer_event = !VARIA_event_base+3
!shak_dead_event = !VARIA_event_base+16
!bowling_chozo_event = !VARIA_event_base+17
!visited_dachora_event = !VARIA_event_base+18
!visited_etecoons_event = !VARIA_event_base+19
!king_cac_event = !VARIA_event_base+20

;;; Keep these macros at the end as they depend on current event index:
!max_objectives = 5
!objectives_event_base = !VARIA_event_base+21

;; declare an array with all the "objective completed" events
macro objectivesCompletedEventArray()
!obj_idx = 0
while !obj_idx < !max_objectives
	dw !objectives_event_base+2*!obj_idx
	!obj_idx #= !obj_idx+1
endif
endmacro

;; declare an array with all the "objective notified" events
macro objectivesNotifiedEventArray()
!obj_idx = 0
while !obj_idx < !max_objectives
	dw !objectives_event_base+2*!obj_idx+1
	!obj_idx #= !obj_idx+1
endif
endmacro
