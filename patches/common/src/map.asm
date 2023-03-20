LOROM

;---------------------------------------------------------------------------------------------------
;|x|                                      MAP OVERHAUL v1.2                                      |x|
;|x|                                       Made by MFreak                                        |x|
;---------------------------------------------------------------------------------------------------

;;; See map/README.txt for original patch documentation
;;;
;;; VARIA adaptations :
;;; * change path to external files
;;; * include gfx, tilemaps, palettes, and other small modifications to match map overhaul example ips,
;;;   except for
;;;     - pause screen BG base tile (put back grid)
;;;     - eqt screen tilemap (handled in equipment_screen patch)
;;; * include gfx for ITEMS, TIME, OBJ
;;; * behaviour changes :
;;;     - removed pause screen status restore
;;; * adapted freespace values to step around other patches

incsrc "macros.asm"

;---------------------------------------------------------------------------------------------------
;|x|                                    CONFIG                                                   |x|
;---------------------------------------------------------------------------------------------------

{;-------------------------------------- GENERAL ---------------------------------------------------

;Location of map construction code for anything which require a map (minimap, pause screen, file select)
;Can be moved anywhere (size: $236)
	!Freespace_MapConstruction = $85C000

;Location for maptile GFX for minimap (size: $1000)
	!Freespace_MinimapTiles = $9AC200
        !Vanilla_MinimapTiles = $9AB200
;Location of code to transfer tile graphics from RAM to VRAM (restricted to bank $80) (size: $97)
	!FreespaceBank80_VRAM = $80CD8E


;RAM addresses:
	!SamusMapPositionMirror = $0B28     ;used to not update minimap every frame
	!Update_Minimap_VRAM_Flag = $0B2A   ;flag for updating minimap GFX to VRAM
	!RAM_ActiveMap = $7EDF5C            ;map layout for minimap, originally storage for BG 2 tilemap during pause (size: $1000)
	!RAM_Minimap_GFX = $7EFE00          ;space to transfer tile graphics to then put it fittingly to VRAM later (size: $F0)
;RAM addresses for select switch area:
	!MinimapIndicatorPalette = $7EFEF0	;only used for minimap to load origin palette for samus position indicator
	!ExploredAreaBits = $7EFEF1         ;only used during pause screen, set bit of areas which have explored bits set
	!OriginAreaIndex = $7EFEF2          ;only used during pause screen, copy of $079F when loading pause screen


;Empty tile used for unexplored sections of the map (vanilla: $1F)
	!EmptyTile = $1F
;Tile in HUD graphic used to cover up the minimap during a bossfight (vanilla: $1F)
	!BossfightMinimapCovertile = $1F


;Set position for setup ASM. Similar to $C90A (set collected map for current area) seen in tourian entrance room (setup ASM)
;with the addition that it will be updated on the minimap too.
;Must be in bank $8F for it to work. Duo to SMART you have to change the setup asm pointers yourself.
;Custom setup asm for setting map station bit (size: $1D)
	!SetCollectedAreaCodePosition = $E99B
}

{;-------------------------------------- COVER TILES -----------------------------------------------
;Array of tiledata to cover with if maptile is loaded but unexplored (size: $100)
	!Freespace_CoverTiles = $89C700
}

{;-------------------------------------- ITEMBIT TILECHANGE ----------------------------------------
;Array of tiledata to change specific tiles in depending areas if the itembit is set (size: $400)
	!Freespace_ItembitTilechange = $89C800
}

{;-------------------------------------- MAP DECORATION --------------------------------------------

;Location of map decoration data (original size: $C8)
	!Freespace_MapDecoration = $89C600

;Map deco tiles only appears when map station is activated (default: !AlwaysActive)
	!MapDecorationAppearence = !AlwaysActive
;!AlwaysActive    : map decoration always appears in pause map screen
;!MapStationActive: map decoration only appears in pause map screen when mapstation has been activated


;Should map decoration be considered for setting up map screen boundaries? (default: !Involve)
	!InvolveMapDecorationForBoundary = !Ignore
;!Involve: map decoration contribute in map screen boundaries
;!Ignore : map decoration get ignored when setting map screen boundaries
}

{;-------------------------------------- MAPTILE GLOW ----------------------------------------------

;Location of palette data for maptiles to change color (original size: $C8)
	!Freespace_MaptileGlow = $8EE600

;RAM address for maptile glow timer and index (default: $0759)
	!MaptileGlowRAM = $0759


;How many color steps should maptile glow have, before it repeat? (default: $08)
	!MaptileGlow_TimerAmount = $08

;How many palettes should have maptile glow? (default: $06)
	!MaptileGlow_PaletteAmount = $06
}

{;-------------------------------------- MINIMAP ---------------------------------------------------

;Sets palettes for tiles in minimap depending on the initial palette of the tile in the map (range: $00 - $07)
	!MinimapPalette0 = $00
	!MinimapPalette1 = $04
	!MinimapPalette2 = $03
	!MinimapPalette3 = $02
	!MinimapPalette4 = $03
	!MinimapPalette5 = $02
	!MinimapPalette6 = $03
	!MinimapPalette7 = $02

;Which minimap palette should empty tiles have? (vanilla: $03) (range: $00 - $07)
	!MinimapPaletteEmptyTile = $03

;Set palette for samus position indication in minimap (vanilla: $07) (range: $00 - $07)
	!SamusMinimapPositionPalette = $07

;Adjust blinking timer for samus position indication. Formula is 2^n in frames.
;At 8 and above the indicator will not blink at all (default $03) (range $00 - $08)
	!SamusMinimapPositionTimer = $03
}

{;-------------------------------------- PAUSE SCREEN MAP SCROLL BOUNDARY --------------------------

;Map scroll boundaries are values where the screen stops at a certain position.
;This value is defined by the outest exposed tile in the area map.
;An additional offset is used to extend the map scroll boundary to a certain extent,
;so the entire map cannot and will not be obscured by the pause screen frame.

;How many empty tiles beyond the outest exposed tile before screen boundary hits
;(Offset values are defined in tiles) (vanilla offset is $02 in all directions)
	!Left_MapBorderOffset = $02
	!Right_MapBorderOffset = $02
	!Top_MapBorderOffset = $02
	!Bottom_MapBorderOffset = $02


;Defined offset for the frame in the pause screen tilemap (offset values are defined in tiles)
;(This should not be changed unless you edited the size of the frame from the pause screen tilemap)
	!Left_MapFrameOffset = $01
	!Right_MapFrameOffset = $01
	!Top_MapFrameOffset = $06
	!Bottom_MapFrameOffset = $08
}

{;-------------------------------------- PAUSE SCREEN TILEMAP/PALETTE POINTERS ---------------------

;Here you can change the pointers to the tilemap data and palette of the pause screen.
;Only the reference point gets changed. The actual data does not get moved.
;(When moving pause screen related data, some patches related to this may break!)
        !PauseScreen_Tiles_Pointer = $B68000       ;(vanilla: $B68000 (PC: $1B0000) ;size: $6000)
	!PauseScreen_Map_Tilemap_Pointer = $B6E000       ;(vanilla: $B6E000 (PC: $1B6000) ;size: $800)
	!PauseScreen_Equipment_Tilemap_Pointer = $B6E800 ;(vanilla: $B6E800 (PC: $1B6800) ;size: $800)
	!PauseScreen_Palette_Pointer = $B6F000           ;(vanilla: $B6F000 (PC: $1B7000) ;size: $200)
}

{;-------------------------------------- SELECT SWITCH AREA ----------------------------------------

;Allows you to switch to other area maps by pressing SELECT on the pause screen.
;Set how many areas should be shown with SELECT switch. (default: $06 / range: $01 - $08)
	!AccessableAreaNumber = $06
}

{;-------------------------------------- SMOOTH MAP SCREEN CONTROLS --------------------------------

;Allows you to freely control the map screen in all 8 directions.
;Map screen scroll speed cap (default: $02)
	!MapScrollSpeedCap = $02
}

{;-------------------------------------- UNEXPLORED TILE PALETTE -----------------------------------

;Changes the palette of loaded unexplored tiles.
;If the original tile isn't explored yet, the palette get changed to the defined palette here
;(range: $00 - $07) (default: all $02 "vanilla unexplored blue")
	!UnexploredTilePalette0 = $02
	!UnexploredTilePalette1 = $02
	!UnexploredTilePalette2 = $02
	!UnexploredTilePalette3 = $02
	!UnexploredTilePalette4 = $02
	!UnexploredTilePalette5 = $02
	!UnexploredTilePalette6 = $02
	!UnexploredTilePalette7 = $02
}

{;-------------------------------------- VERTICAL AREA MAP -----------------------------------------

;You can control which area should display the area map vertically instead of horizontally.
;The right page of the map will be moved below the left page of the map.
;Rooms and icons of that area must be adjusted for vertical area (see README for more info).

;Set to 1 for this area to be displayed vertically.
;Sorted in this order: (Debug), (Ceres), (Tourian), (Maridia), (WShip), (Norfair), (Brinstar), (Crateria)
	!VerticalAreaMapBits = %00000000
}

;---------------------------------------------------------------------------------------------------
;|x|                                    MAIN                                                     |x|
;---------------------------------------------------------------------------------------------------
{
;Config files
INCSRC "map/config/CoverTileList.asm"
INCSRC "map/config/ItembitTilechangeList.asm"
INCSRC "map/config/MaptileGlow.asm"
INCSRC "map/config/MapDecoration.asm"

;Clean up
ORG $82925D : PADBYTE $FF : PAD $829324		;delete original map scrolling code ($C7)
ORG $82943D : PADBYTE $FF : PAD $829628		;delete original map construction code ($1EB)
ORG $829E27 : PADBYTE $FF : PAD $82A09A		;delete redundant map scroll setup/original scroll boundary set routines ($273)

ORG $90A8EF : PADBYTE $FF : PAD $90AC04		;delete original minimap code ($315)

;Code files
INCSRC "map/Misc_Banks.asm"
INCSRC "map/PauseScreenRoutines.asm"
INCSRC "map/MapConstruction.asm"
INCSRC "map/Minimap.asm"

; Hex map disable
incsrc "map/NoHexMap.asm"

org $81b14b
incbin "map/start_tilemap.bin"

; Minimap GFX
org !Vanilla_MinimapTiles
incbin "map/minimap.gfx"
ORG !Freespace_MinimapTiles
incbin "map/minimap_extra.gfx"

org $80988B
incbin "map/hud_tilemap.bin"

; Pause GFX
org !PauseScreen_Tiles_Pointer
incbin "map/pause.gfx"
org !PauseScreen_Palette_Pointer
incbin "map/pause_palettes.bin"
org !PauseScreen_Palette_Pointer+26
        ;; put back vanilla HUD blue color when in pause
        dw $44e5

; Pause tilemaps
org !PauseScreen_Map_Tilemap_Pointer
incbin "map/pause_map_tilemap.bin"

}
