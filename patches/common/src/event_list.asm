include

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
!objectives_completed_event = !tourian_open_event ; reuse tourian entrance event
!hunt_over_event = #$0080
