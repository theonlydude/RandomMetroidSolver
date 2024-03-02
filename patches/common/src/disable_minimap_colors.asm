;;; Disables minimap colors IRQ trick, as it can cause glitches on certain real hardware configurations

arch 65816
lorom

incsrc "sym/map.asm"

!vcounter_target = $1F
!hcounter_target = $98

org $809616
vanilla_irq:
org $80987C
.table:
        dw vanilla_irq
org $8096E8
.transition_start:
        db $0A
org $8096EB
        db !vcounter_target
org $8096EE
        db !hcounter_target
.draygon:
org $80972A
        db $0E
org $80972D
        db !vcounter_target
org $809730
        db !hcounter_target
.vertical:
org $809768
        db $12
org $80976B
        db !vcounter_target
org $80976E
        db !hcounter_target
.horizontal:
org $8097D1
        db $18
org $8097D4
        db !vcounter_target
org $8097D7
        db !hcounter_target


org map_get_room_minimap_table
get_room_minimap_table:
        lda #map_MinimapTilePaletteTable
        rtl
