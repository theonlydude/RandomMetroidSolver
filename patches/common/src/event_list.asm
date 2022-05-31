include

math pri on

;;; event routines
!mark_event = $8081FA
!check_event = $808233

;;; vanilla main events
!tourian_open_event = #$000a
!escape_event = #$000e
!maridia_tube_open = #$000b
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

;;; VARIA events
!VARIA_event_base = #$0080
!cur_VARIA_event = !VARIA_event_base

macro defineVARIAevent(event_name)
!<event_name> = !cur_VARIA_event
;; this leads to pretty inefficient "math" by text-replacing +1+1+1 etc,
;; but it is necessary to keep proper hex 16 bits formattings and avoid
;; suffixing instructions manipulating event constants with .w like we would
;; have to do if actual asar math were used
!cur_VARIA_event := !cur_VARIA_event+1
endmacro

;; scavenger hunt completion
%defineVARIAevent(hunt_over_event)

;; objectives events : a global objectives completed event for endgame
;; and individual events for each objective :
;; - is it completed?
;; - if completed, was the user notified in the HUD?
;;   (can never be set if HUD is disabled)
!objectives_completed_event = !tourian_open_event ; reuse tourian entrance event
%defineVARIAevent(objectives_completed_event_notified)

%defineVARIAevent(fish_tickled_event)

;;; Keep these macros at the end as they depend on cur_VARIA_event, which depends on custom events definitions above:
!max_objectives = 5
!objectives_event_base = !cur_VARIA_event

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
