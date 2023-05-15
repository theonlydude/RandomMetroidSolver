;;; VARIA shared constants

include

;; shared ROM options addresses
!disabled_tourian_escape_flag = $a1f550

;; shared constants
;; RAM to store current obj check index
!obj_check_index = $7fff46
;;; RAM for remaining items in current area
!n_items = $7fff3e
;;; vanilla bit array to keep track of collected items
!item_bit_array = $7ed870
;;; bit index to byte index/bitmask routine
!bit_index = $80818e

;;; IGT vanilla RAM
!igt_frames = $7E09DA
!igt_seconds = $7E09DC
!igt_minutes = $7E09DE
!igt_hours = $7E09E0

;; game state
!game_state = $0998

;; RTA timer RAM updated during NMI
!timer1 = $05b8
!timer2 = $05ba
;; lag counter helpers
!skip_lag_count_flag = $033c
!timer_lag = $033a

;; stats RAM
!_stats_ram = fc00
!stats_ram = $7f!_stats_ram
!stats_timer = !stats_ram


;;; collected items
!CollectedItems  = $7ED86E
!collected_beams_mask = $09A8
!collected_items_mask = $09A4

;;; collected map tiles (11 bytes)
!map_tilecounts_table = $7fff50
!map_total_tilecount = $7fff5b

;; bitfields
; arg: A=bit index. returns: X=byte index, !bitindex_mask=bitmask
!bitindex_routine = $80818e
!bitindex_mask = $05e7
!doors_bitfield = $7ED8B0

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
!stat_rta_lag = $2A
!stat_rta_lag_ram #= !stats_ram+(2*!stat_rta_lag)

;; vanilla area check
!area_index = $079f
!brinstar = $0001
!norfair = $0002

!palettes_ram = $7EC000
!palette_size = 32              ; usual size of a palette is 16 colors (1 word per color)

;;; pause state
!pause_index = $0727

;;; pause index values
!pause_index_map_screen = #$0000
!pause_index_equipment_screen = #$0001
!pause_index_map2equip_fading_out = #$0002
!pause_index_map2equip_load_equip = #$0003
!pause_index_map2equip_fading_in = #$0004
!pause_index_equip2map_fading_out = #$0005
!pause_index_equip2map_load_map = #$0006
!pause_index_equip2map_fading_in = #$0007
