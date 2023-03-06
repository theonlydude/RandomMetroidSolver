
;---------------------------------------------------------------------------------------------------
;|x|                                    MAPTILE GLOW                                             |x|
;---------------------------------------------------------------------------------------------------
{
ORG !Freespace_MaptileGlow
;Palettes for maptile glow:

;"pink" tilemap palette:
Explored_MapGlow: DW $48FB, $44DA, $40B9, $3C98, $3877, $3C98, $40B9, $44DA

;"green" tilemap palette:
Secret_MapGlow: DW $1EA9, $1A88, $1667, $1246, $0E25, $1246, $1667, $1A88

;"yellow" tilemap palette:
Important_MapGlow: DW $02DF, $02BE, $029D, $027C, $025B, $027C, $029D, $02BE

;"orange" tilemap palette:
Heated_MapGlow: DW $0E3F, $0A1E, $05FD, $01DC, $01BB, $01DC, $05FD, $0A1E


;Time in frames for one color (amount of values get set in the config under "TimerAmount")
MaptileGlow_GlobalTimer:
	DB $40, $08, $04, $08, $0C, $08, $04, $08

;Pointers to these maptile glow palettes (amount of values get set in the config under "PaletteAmount")
MaptileGlow_PalettePointer:
	DW Explored_MapGlow, Secret_MapGlow, Important_MapGlow, Heated_MapGlow

;Position of palette for maptile glow [<palette position> * 2] (amount of values same as above)
MaptileGlow_PaletteOffset:
	DW $0062, $0082, $00A2, $00C2
}
