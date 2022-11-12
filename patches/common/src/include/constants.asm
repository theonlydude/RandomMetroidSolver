;;; VARIA shared constants

include

;; shared ROM options addresses
!disabled_tourian_escape_flag = $a1f5fe

;; shared constants
!obj_check_period = #$0020	; unit:frames, works only in powers of 2

;;; IGT vanilla RAM
!igt_frames = $7E09DA
!igt_seconds = $7E09DC
!igt_minutes = $7E09DE
!igt_hours = $7E09E0

;; RTA timer RAM updated during NMI
!timer1 = $05b8
!timer2 = $05ba

;; stats RAM
!_stats_ram = fc00
!stats_ram = $7f!_stats_ram
!stats_timer = !stats_ram

;; tracked stats (see tracking.txt)
!stat_nb_door_transitions = #$0002
!stat_rta_door_transitions = #$0003
!stat_rta_door_align = #$0005
!stat_rta_regions = #$0007
!stat_uncharged_shots = #$001f
!stat_charged_shots = #$0020
!stat_SBAs = #$0021
!stat_missiles = #$0022
!stat_supers = #$0023
!stat_PBs = #$0024
!stat_bombs = #$0025
!stat_rta_menu = #$0026
!stat_deaths = #$0028
!stat_resets = #$0029
