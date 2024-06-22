
;---------------------------------------------------------------------------------------------------
;|x|                                    MAPTILE GLOW                                             |x|
;---------------------------------------------------------------------------------------------------
{
%freespaceStart(!Freespace_MaptileGlow)
;Palettes for maptile glow: organized by area to account for additional colors
!AreaColor_Undefined = $0802
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
print "8e end: ", pc
%freespaceEnd($8ee7ff)
