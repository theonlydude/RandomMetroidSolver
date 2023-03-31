
;---------------------------------------------------------------------------------------------------
;|x|                                    MAPTILE GLOW                                             |x|
;---------------------------------------------------------------------------------------------------
{
ORG !Freespace_MaptileGlow
;Palettes for maptile glow: organized by area to account for additional colors

!Glow_Crateria = $35e9,$31c8,$2da7,$2986,$2565,$2986,$2da7,$31c8
!Glow_GreenPinkBrinstar = $06e1,$02c0,$02a0,$0280,$0260,$0280,$02a0,$02c0
!Glow_RedBrinstar = $04f5,$00d4,$00d3,$00d2,$00b1,$00d2,$00d3,$00d4
!Glow_WreckedShip = $3ad6,$36b5,$2e94,$2a73,$2652,$2a73,$2e94,$36b5
!Glow_Kraid = $19c0,$19a0,$1980,$1560,$1540,$1560,$1980,$19a0
!Glow_Norfair = $023f,$021e,$021d,$01fc,$01fb,$01fc,$021d,$021e
!Glow_Crocomire = $2497,$2076,$1c55,$1c34,$1813,$1c34,$1c55,$2076
!Glow_LowerNorfair = $00df,$00be,$00bd,$00bc,$00bb,$00bc,$00bd,$00be
!Glow_WestMaridia = $7e20,$7a20,$7600,$7200,$6de0,$7200,$7600,$7a20
!Glow_EastMaridia = $6e3c,$6a1b,$65da,$61b9,$5d98,$61b9,$65da,$6a1b
!Glow_Tourian = $5297,$4e76,$4635,$4214,$39d3,$4214,$4635,$4e76
!Glow_Undefined = !AreaColor_Undefined,!AreaColor_Undefined,!AreaColor_Undefined,!AreaColor_Undefined,!AreaColor_Undefined,!AreaColor_Undefined,!AreaColor_Undefined,!AreaColor_Undefined

;;; consistent with order defined in pause_palettes
Glow:
.Crateria:
..Palette7:
        DW !Glow_Crateria
..Palette6:
        DW !Glow_WreckedShip
..Palette5:
        DW !Glow_Tourian
..Palette4:
        DW !Glow_EastMaridia

.Brinstar:
..Palette7:
        DW !Glow_GreenPinkBrinstar
..Palette6:
        DW !Glow_RedBrinstar
..Palette5:
        DW !Glow_Crateria
..Palette4:
        DW !Glow_Kraid

.Norfair:
..Palette7:
        DW !Glow_Norfair
..Palette6:
        DW !Glow_LowerNorfair
..Palette5:
        DW !Glow_Crocomire
..Palette4:
        DW !Glow_Undefined

.WreckedShip:
..Palette7:
        DW !Glow_WreckedShip
..Palette6:
        DW !Glow_Undefined
..Palette5:
        DW !Glow_Undefined
..Palette4:
        DW !Glow_Undefined

.Maridia:
..Palette7:
        DW !Glow_RedBrinstar
..Palette6:
        DW !Glow_WestMaridia
..Palette5:
        DW !Glow_EastMaridia
..Palette4:
        DW !Glow_Undefined

.Tourian:
..Palette7:
        DW !Glow_Tourian
..Palette6:
        DW !Glow_Undefined
..Palette5:
        DW !Glow_Undefined
..Palette4:
        DW !Glow_Undefined

;Time in frames for one color (amount of values get set in the config under "TimerAmount")
MaptileGlow_GlobalTimer:
	DB $40, $08, $04, $08, $0C, $08, $04, $08

;Pointers to these maptile glow palettes (amount of values get set in the config under "PaletteAmount")
; the pointers are now organized by area
MaptileGlow_PalettePointer:
	dw Glow_Crateria_Palette7
        dw Glow_Crateria_Palette6
        dw Glow_Crateria_Palette5
        dw Glow_Crateria_Palette4

;Position of palette for maptile glow [<palette position> * 2] (amount of values same as above)
MaptileGlow_PaletteOffset:
	DW  $00E2, $00C2, $00A2, $0082
}
warnpc $8effff
