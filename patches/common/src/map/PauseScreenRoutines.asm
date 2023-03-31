
;---------------------------------------------------------------------------------------------------
;|x|                                    BANK $82        Pause Screen Routines                    |x|
;---------------------------------------------------------------------------------------------------
{
;---------------------------------------------------------------------------------------------------
;|x|                                    GENERAL                                                  |x|
;---------------------------------------------------------------------------------------------------
{
{;-------------------------------------- HIJACKS ---------------------------------------------------

ORG $828067 : JSL ConstructMap	;on game start up

;Routine during pause transition, originally used $7EDF5C for storage of BG 2 tilemap, now $7E6000 gets used instead
;$7E6000 - $7E6FFF gets used for x-ray, door transitions and non-gameplay routines so it should be safe.
ORG $828D6A	: LDA #$00			;low byte of: transfer tilemap of BG 2 to RAM
ORG $828D6F : LDA #$60			;high byte of: transfer tilemap of BG 2 to RAM
ORG $828DB1 : DL $7E6000		;source of: transfer tilemap of BG 2 from RAM back to VRAM

ORG $828EB1 : DW $3C00			;increase size for equipment screen tiles
ORG $828ED1 : DW $1000			;half size of HUD graphic tiles loading
ORG $828EE2 : LDA #$50			;change position for map border
ORG $828EF3 : DL !PauseScreen_Map_Tilemap_Pointer
ORG $828F13 : DL !PauseScreen_Map_Tilemap_Pointer+$400
ORG $828F33 : DL !PauseScreen_Equipment_Tilemap_Pointer
ORG $828FF8 : LDA.l !PauseScreen_Palette_Pointer,x
ORG $82902B : JSR SetMapScrollBoundaries

ORG $8293D8 : LDA #$48			;change position for tilemap "map"
ORG $8293E2 : JSR LoadMapHijack
ORG $8293FB : LDA #$50			;change position for area name text
ORG $82A0B6 : LDA #$49			;change BA (Background Address) of BG 1 (map/equipment screen)
ORG $82A0BD : LDA #$50			;change BA of BG 2 (border)
ORG $82AC2D : LDA #$48			;change position for equipment screen
ORG $82B200 : LDA #$4880		;change position for samus wireframe

ORG $82B6D7 : JSL CheckIconVerticalPosition		;samus's gunship (pausescreen map)
ORG $82B747 : JSL CheckIconVerticalPosition		;samus icon
ORG $82B74E : JSL CheckIconVerticalPosition		;samus position indicator
ORG $82B792 : JSL CheckIconVerticalPosition		;samus's gunship

ORG $82B849 : JSL CheckIconVerticalPosition		;map icons (energy/missile/map/save station)
ORG $82B8DC : JSL CheckIconVerticalPosition		;boss icon
ORG $82B8FE : JSL CheckIconVerticalPosition		;boss dead icon (cross out)
;Map screen border offset
ORG $82B942 : SBC.w #!Left_MapFrameOffset+!Left_MapBorderOffset<<3
ORG $82B954 : ADC.w #!Right_MapFrameOffset+!Right_MapBorderOffset<<3-1
ORG $82B96A : SBC.w #!Top_MapFrameOffset+!Top_MapBorderOffset<<3
ORG $82B97C : SBC.w #$20-!Bottom_MapFrameOffset-!Bottom_MapBorderOffset<<3+1

ORG $82B9F7 : JSL CheckIconVerticalPosition		;samus position indicator
ORG $82BB67 : JSL CheckIconVerticalPosition		;elevator destination
ORG $82DFC2 : JSL ConstructMapFromAreaTransition
ORG $82E488 : BRA $08 : NOP #8	;skip operation "overwrite BG3 tiles" in special graphics bit rooms
ORG $82E643 : JSL ForceUpdateHUDMapInKraid		;part of background routine, triggered during kraid room transition
ORG $82EA6B : JSL ForceUpdateHUDMapInKraid		;part of background routine, triggered when unpausing in kraid's room
}

{;--------------------------------------- VARIOUS OPTIONS ------------------------------------------
ORG $82943D
LoadMapHijack: JSL LoadMapFromPause : RTS

;829442
VerticalAreaMapBit: DB !VerticalAreaMapBits


ORG $829446
LoadSourceMapData:
	PHB : PHK : PLB
	LDA $079F : ASL A : CLC : ADC $079F : TAX
	LDA $964A,x : STA $00 : LDA $964C,x : STA $02
	PLB : RTL
}
}
;---------------------------------------------------------------------------------------------------
;|x|                                    MAP SCREEN BOUNDARIES                                    |x|
;---------------------------------------------------------------------------------------------------
{
;ORG continues from above!
;---------------------------------------- SET MAP SCREEN BOUNDARY ----------------------------------
;Uses different methode to define boundaries: checks for non-empty tiles after map construction
;instead of using explored/loaded map bits.
SetMapScrollBoundaries:
	PHP
	LDA #$007E : STA $02 : STA $05	;bank pointer in direct page (7E: RAM)
	LDA #$4000 : STA $00			;$00 = left map page pointer
	LDA #$4800 : STA $03			;$03 = right map page pointer
;Check if vertical area map bit is set for current area
	SEP #$30 : LDY #$00 : LDX $079F : LDA.l VerticalAreaMapBit
	AND $82B7C9,x : BNE VerticalMapBoundary	;$82B7C9 = selective bit index
	JMP HorizontalMapBoundary

VerticalMapBoundary:
	LDA $58 : AND #$FC : ORA #$02 : STA $58 : REP #$30	;set BG 1 screen size to vertical
;Top border
	;LDY #$0000
- : JSR MainPageBorderCheck : BNE ++
	INY : INY : CPY #$1000 : BMI -
	LDY #$0040								;fix border value if map completely empty
++ : TYA : AND #$FFC0 : STA $05B0
;Bottom border
	LDY #$0FFE
- : JSR MainPageBorderCheck : BNE ++
	DEY : DEY : BPL -
	LDY #$02C0								;fix border value if map completely empty
++ : TYA : ORA #$003F : INC : STA $05B2
;Left border
	LDX #$0000
-- : TXA : AND #$003F : CLC : ADC $05B0 : TAY			;maptile offset
- : JSR MainPageBorderCheck : BNE ++
	TYA : CLC : ADC #$0040 : TAY : CMP $05B2 : BMI -	;next tile in column
	INX : INX : CPX #$0080 : BMI --
	LDX #$003E								;fix border value if map completely empty
++ : TXA : ASL : ASL : STA $05AC
;Right border
	LDX #$003E
-- : TXA : AND #$003F : CLC : ADC $05B0 : TAY			;maptile offset
- : JSR MainPageBorderCheck : BNE ++
	TYA : CLC : ADC #$0040 : TAY : CMP $05B2 : BMI -	;next tile in column
	DEX : DEX : BPL --
	LDX #$0042								;fix border value if map completely empty
++ : JMP FinalAdjustmentBoundary
	;TXA : INC : INC : ASL : ASL : STA $05AE

!Involve = "AND #$00FF"	;filter out map deco tiles, so boundary considers decotiles
!Ignore = "AND #$03FF"	;only tile data, if decotile gets detected -> skip tile

FullPageBorderCheck:
	LDA [$03],y : !InvolveMapDecorationForBoundary : BIT #$0300 : BNE +	;check if tile is deco tile in right mappage
	CMP.w #!EmptyTile : BEQ + : RTS		;check if tile is empty tile
+ : MainPageBorderCheck:
	LDA [$00],y : !InvolveMapDecorationForBoundary : BIT #$0300 : BNE +	;check if tile is deco tile in left mappage
	CMP.w #!EmptyTile : RTS
+ : LDA #$0000 : RTS					;continue boundary search
;2 bytes left


ORG $829547
HorizontalMapBoundary:
	LDA $58 : AND #$FC : ORA #$01 : STA $58				;set BG 1 screen size to horizontal
	REP #$30
;Top border
	;LDY #$0000
- : JSR FullPageBorderCheck : BNE ++
	INY : INY : CPY #$0800 : BMI -
	LDY #$0040								;fix border value if map completely empty
++ : TYA : AND #$FFC0 : STA $05B0
;Bottom border
	LDY #$07FE
- : JSR FullPageBorderCheck : BNE ++
	DEY : DEY : BPL -
	LDY #$02C0								;fix border value if map completely empty
++ : TYA : ORA #$003F : INC : STA $05B2
;Left border
	LDX #$0000
-- : TXA : AND #$003F : CLC : ADC $05B0 : TAY			;maptile offset
- : JSR MainPageBorderCheck : BNE ++
	TYA : CLC : ADC #$0040 : TAY : CMP $05B2 : BMI -	;next tile in column
	INX : INX : CPX #$0080 : BPL +
	CPX #$0040 : BNE --						;if map page border reached
	LDA $03 : STA $00 : BRA --				;left page completely empty -> set pointer to right map page
+ : LDX #$0034								;fix border value if map completely empty
++ : TXA : ASL : ASL : STA $05AC
;Right border
	LDX #$007E
-- : TXA : AND #$003F : CLC : ADC $05B0 : TAY			;maptile offset
- : LDA [$03],y : !InvolveMapDecorationForBoundary : BIT #$0300 : BNE +
	CMP.w #!EmptyTile : BNE ++
+ : TYA : CLC : ADC #$0040 : TAY : CMP $05B2 : BMI -	;next tile in column
	DEX : DEX : BMI +
	CPX #$0040 : BNE --						;if map page border reached
	LDA $00 : STA $03 : BRA --				;right page completely empty -> set pointer to left map page
+ : LDX #$0038								;fix border value if map completely empty
++ : FinalAdjustmentBoundary:
	TXA : INC : INC : ASL : ASL : STA $05AE
;Adjust top/bottom borders
	LDA $05B0 : LSR #3 : STA $05B0
	LDA $05B2 : LSR #3 : STA $05B2
	PLP : RTS
;$1F byte left


;---------------------------------------- SET PAUSE SCREEN STARTING POSITION -----------------------

!LeftScreenOffset = "!Left_MapFrameOffset+!Left_MapBorderOffset<<3"
!RightScreenOffset = "$20-!Right_MapFrameOffset-!Right_MapBorderOffset-1<<3"
!TopScreenOffset = "!Top_MapFrameOffset+!Top_MapBorderOffset<<3"
!BottomScreenOffset = "$20-!Bottom_MapFrameOffset-!Bottom_MapBorderOffset-1<<3"

ORG $82902E
;Determine the X midpoint of the map
	LDA $05AE : SEC : SBC $05AC : LSR : CLC : ADC $05AC
	SEC : SBC.w #$20-!Left_MapFrameOffset-!Right_MapFrameOffset>>1+!Left_MapFrameOffset<<3 : STA $B1
;Determine the Y midpoint of the map
	LDA $05B2 : SEC : SBC $05B0 : LSR : CLC : ADC $05B0
	SEC : SBC.w #$20-!Top_MapFrameOffset-!Bottom_MapFrameOffset>>1+!Top_MapFrameOffset<<3 : STA $B3

	LDA !OriginAreaIndex : CMP $079F : BEQ + : RTL	;check if in current area for samus cursor
+ : LDA $0AF7 : AND #$00FF : CLC : ADC $07A1 : ASL #3 : STA $12 : SEC : SBC $B1	;$12 = samus X position from map
	CMP.w #!LeftScreenOffset : BMI +				;branch if samus is to far left from map midpoint
	CMP.w #!RightScreenOffset : BPL ++ : BRA +++	;branch if samus is to far right from map midpoint
+ : LDA $12 : SEC : SBC.w #!LeftScreenOffset : STA $B1 : BRA +++	;adjust screen for cursor position
++ : LDA $12 : SEC : SBC.w #!RightScreenOffset : STA $B1			;adjust screen for cursor position
+++ : LDA $0AFB : AND #$00FF : CLC : ADC $07A3 : INC : ASL #3 : STA $12 : SEC : SBC $B3	;same for Y position
	CMP.w #!TopScreenOffset : BMI +
	CMP.w #!BottomScreenOffset : BPL ++ : RTL
+ : LDA $12 : SEC : SBC.w #!TopScreenOffset : STA $B3 : RTL
++ : LDA $12 : SEC : SBC.w #!BottomScreenOffset : STA $B3 : RTL
;$C byte left
}
;---------------------------------------------------------------------------------------------------
;|x|                                    MAPTILE GLOW                                             |x|
;---------------------------------------------------------------------------------------------------
{
;Hijacks
ORG $8290FA : JSR MaptileGlowRoutine
ORG $82B6E2 : JSR MaptileGlowRoutine


!MaptileGlowTimer = !MaptileGlowRAM
!MaptileGlowIndex = !MaptileGlowRAM+1

ORG $82925D
MaptileGlowRoutine:
	JSR $A92B			;pause screen animation
	PHP : SEP #$30
	LDA.w !MaptileGlowTimer : BEQ ++				;draw mapglow palette on first frame of mapscreen
	DEC !MaptileGlowTimer : BNE +					;decrease timer
	INC !MaptileGlowIndex : LDA.w !MaptileGlowIndex	;next index
	CMP.b #!MaptileGlow_TimerAmount : BCC +			;check if end of index reached
	STZ !MaptileGlowIndex : + : PLP : RTS			;reset index ;return
++ : PHB : PEA.w !Freespace_MaptileGlow>>8 : PLB : PLB			;set bank to where maptile glow data is
	LDX !MaptileGlowIndex : LDA.w MaptileGlow_GlobalTimer,x		;load timer data by next index
	INC : STA.w !MaptileGlowTimer : LDY #$00 : REP #$30			;set timer, prepare loop
;[X] = pointer of current maptile glow data + index*2 + area index*glow table size
        lda !area_index : asl #6 : sta $12 ; works because !MaptileGlow_TimerAmount is 8, so glow table size is 64
-
        LDA.w !MaptileGlowIndex : AND #$00FF : ASL : CLC : ADC.w MaptileGlow_PalettePointer,y : adc $12 : TAX
	LDA $0000,x : LDX.w MaptileGlow_PaletteOffset,y : STA $7EC000,x		;set palette
+ : INY #2 : CPY.w #!MaptileGlow_PaletteAmount<<1 : BCC -
	PLB : PLP : RTS

warnpc $8292BD

;---------------------------------------------------------------------------------------------------
;;; area-specific map palettes
;---------------------------------------------------------------------------------------------------

org $828D25
        ;; invert the two vanilla calls to "load map" and "backup palettes", since we change palettes when loading the map
        JSR $8FD4
        JSL $8293C3

org !Freespace_AreaPalettes
!AreaPalettes_RAM = !palettes_ram+(!AreaPalettes_BaseIndex*!palette_size)+(2*!AreaPalettes_ExploredColorIndex)
load_area_palettes:
        ;; overwrite explored tile color in palettes based on area
        phx
        phy
        phb
        pea.w !PauseScreen_AreaPalettes_Pointer>>8 : plb : plb
        lda !area_index : asl : tax
        ldy.w !PauseScreen_AreaPalettes_Pointer, x
        lda.w #!AreaPalettes_Amount-1 : sta $12
-
        lda $12 : asl #5 : tax  ; multiply by palette_size (32) with 5 ASL
        lda $0000, y
        sta.l !AreaPalettes_RAM, x
        iny : iny
        dec $12 : bpl -
        plb
        ply
        plx
        rtl


}
;---------------------------------------------------------------------------------------------------
;|x|                                    SELECT SWITCH AREA                                       |x|
;---------------------------------------------------------------------------------------------------
{
;--------------------------------------- HIJACKS ---------------------------------------------------

ORG $828D1A : JSR PrepareAreaIndex
ORG $828D38 : STZ $074D				;undo hijack
ORG $82910A : JSR (PauseRoutineIndex,x)
ORG $829125 : JSR CheckForSelectPress
ORG $829130 : JSR DrawIndicatorIfInCurrentArea
ORG $829156 : JSR DrawSelectButtonSprite : NOP
ORG $82915A : JSR DrawIndicatorIfInCurrentArea
ORG $829200 : JSR DrawIndicatorIfInCurrentArea
ORG $82935B : JMP DrawIndicatorIfInCurrentArea

ORG $82B881 : JSR CheckToDrawMapIcons
ORG $82C581 : DW SelectButtonSprite, $C22B, $C22B, $C22B	;changed sprite data pointer ($0C - $0F)
ORG $82C599 : DW $C22B										;changed sprite data pointer ($18)
ORG $82C3AF						;overwrite (garbage?) sprite data
SelectButtonSprite: DW $0008	;how many OAM tiles to draw
					DW $0008 : DB $00 : DW $34CA : DW $0000 : DB $00 : DW $34BA : DW $01F8 : DB $00 : DW $34C3 : DW $01F0 : DB $00 : DW $34C2
					DW $0008 : DB $F8 : DW $74B4 : DW $0000 : DB $F8 : DW $34B6 : DW $01F8 : DB $F8 : DW $34B5 : DW $01F0 : DB $F8 : DW $34B4
					;[X offset] : [Y offset] : [tile details] : repeat...


;--------------------------------------- FREESPACE -------------------------------------------------

ORG $8292BD

CheckForSelectPress:
	JSR $A5B7							;check for START press
	LDA $0998 : CMP #$000F : BNE +		;check if still in game state "paused"
	LDA $05E1 : BIT #$2000 : BEQ +		;check for SELECT press
	JSR NextAvailableAreaFinder : BCC +	;check if next area is valid to be loaded
	LDA #$0037 : JSL $809049			;play sound "move cursor"
	LDA #$0001 : STA $0723 : STA $0725	;set fading flag
	STZ $0751					;zero shoulder button pressed highlight
	LDA #$0016 : STA $0729		;set sprite timer
	LDA #$0008 : STA $0727		;set pause index to 8: show next area - fading out
+ : RTS


DrawSelectButtonSprite:
	LDA $0727 : CMP #$0008 : BNE +		;check if currently in "switch map area - fading out"
	LDA $0729 : BEQ +					;draw sprite timer zero?
	DEC $0729 : STZ $03
	LDY #$00D0 : LDX #$0070 : LDA #$000C : JSL $81891F	;draw sprite; [A] = sprite index; [X] = sprite X position; [Y] = sprite Y position
+ : JSL $82BB30 : RTS					;draw map elevator destination

warnpc $829324

ORG $829533
DrawIndicatorIfInCurrentArea:
	LDA !OriginAreaIndex : CMP $079F : BNE +		;check if area shown is the same area as samus
	JSR $B9C8 : + : RTS



ORG $829F4C
PrepareAreaIndex:
	JSR $8DBD : LDA $079F : STA !OriginAreaIndex
	PHP : SEP #$20 : TAX : XBA : LDA.w $B7C9,x		;$B7C9 = selective bit index
	REP #$30 : STA !ExploredAreaBits : LDA #$0000	;set bit from origin area
;check every area for explored bits
.arealoop : PHA : XBA : TAX : LDY #$0080	;setup
;check this area for explored bits, if none: go to next area.
- : LDA $7ECD52,x : BNE + : INX #2 : DEY : BNE - : BRA ++
;if area has a explored bit: set bit in !ExploredAreaBits for this area and go to the next one
+ : SEP #$30 : LDA $01,s : TAX
	LDA !ExploredAreaBits : ORA.w $B7C9,x : STA !ExploredAreaBits : REP #$30
++ : PLA : INC : CMP.w #!AccessableAreaNumber : BCC .arealoop	;check as many areas as set
	PLP : RTS


;Construct next explored map during switch routine
MapSwitchConstruct:
	REP #$30
	JSL $82BB30		;display map elevator destinations
	JSR NextAvailableAreaFinder : STX $079F	;save next area number
	LDA $7ED908,x : AND #$00FF : STA $0789	;set flag of map station for next area
	JSL $8293C3		;update area label and construct new area map
	JSL $829028		;set map scroll boundaries and screen starting position
++ : STZ $073F : LDA $C10C : STA $072B		;set L/R highlight animation data
	LDA #$0001 : STA $0723 : STA $0725
	STZ $0763 : INC $0727 : RTS


;Get offset of current explored area bit or different area
;for where and which icons should be drawn
CheckToDrawMapIcons:
	LDA $079F : CMP !OriginAreaIndex : BEQ +		;check if in current area
	PHP : REP #$20 : PHX
	XBA : CLC : ADC #$CD52 : ADC $12 : TAX : LDA $7E0000,x	;load explored bit of different area
	PLX : PLP : RTS
+ : LDA $07F7,y : RTS						;load explored bit of current area


;Returns value of next area (X), carry set if next area is valid, otherwise carry clear
NextAvailableAreaFinder:
	PHP : SEP #$30
	LDA !ExploredAreaBits : LDX $079F : INX	;search for next explored area bit
- : BIT $B7C9,x : BNE +						;branch if area bit is set ;$B7C9 = selective bit index
.continue
	INX : CPX #$08 : BCC - : LDX #$00 : BRA -
;if another area is available
+ : CPX $079F : BEQ .return							;check if it is the same area as active currently
	CPX.b #!AccessableAreaNumber : BCS .continue	;continue search if not the signed range
	PLP : SEC : RTS				;valid area to switch to, set carry, return
.return : PLP : CLC : RTS		;no valid areas available, clear carry, return


CheckIconVerticalPosition:	;draw icon depending on vertical position
	STA $22 : TYA : AND #$FF00 : BNE +
	LDA $22 : JSL $81891F	;if onscreen position: draw sprite
+ : RTL						;else return

PauseRoutineIndex:
	DW $9120, $9142, $9156, $91AB, $9231, $9186, $91D7, $9200	;same as $9110
	DW $9156, MapSwitchConstruct, $9200		;fade out / map construction / fade in
.objectives:
        ;; reserve space for objectives function list
        skip 14

warnpc $82A09A

}
;---------------------------------------------------------------------------------------------------
;|x|                                    SMOOTH MAP SCREEN CONTROLS                               |x|
;---------------------------------------------------------------------------------------------------
{
;New definition in RAM
;$05FB = map screen available direction
;$05FD = left scroll speed
;$05FE = right scroll speed
;$05FF = up scroll speed
;$0600 = down scroll speed


;--------------------------------------- BANK $81 --------------------------------------------------

ORG $81AD88 : JSL MapScrollMain
ORG $81AF13 : BMI $07
ORG $81AF1F : PADBYTE $FF : PAD $81AF32


;--------------------------------------- BANK $82 --------------------------------------------------

ORG $82912C : JSL MapScrollMain
ORG $82B91F : LDA $05FB : ORA $0006,x : STA $05FB : RTL

pause_loading_end:
        jsl load_area_palettes : PLP : RTS
;3 bytes left


ORG $82B981 : BMI $07
ORG $82B98D : PADBYTE $FF : PAD $82B9A0


;--------------------------------------- FREESPACE -------------------------------------------------

ORG $829E27
MapScrollMain:
	PHP : SEP #$30
	LDA $05FC : ASL : AND #$06 : TAX : JSR (HorizontalScreenMovementTable,x)	;move screen in horizontal axes
	LDA $05FC : LSR : AND #$06 : TAX : JSR (VerticalScreenMovementTable,x)		;move screen in vertical axes
	LDA $05B6 : BIT #$01 : BNE +												;set scroll speed every 2nd frame
	LDA $8C : AND $05FC : ASL : AND #$06 : TAX : JSR (HorizontalScreenSpeedTable,x)	;set horizontal scroll speed depending on controller input
	LDA $8C : AND $05FC : LSR : AND #$06 : TAX : JSR (VerticalScreenSpeedTable,x)	;set vertical scroll speed depending on controller input
+ : PLP : STZ $05FB : RTL														;zero available directions and return


HorizontalScreenMovementTable:
	DW NoMovement, ScreenMovement_OnlyRight, ScreenMovement_OnlyLeft, ScreenMovement_Horizontal
VerticalScreenMovementTable:
	DW NoMovement, ScreenMovement_OnlyDown, ScreenMovement_OnlyUp, ScreenMovement_Vertical

HorizontalScreenSpeedTable:
	DW PauseScreen_HorizontalNeutral, PauseScreen_MoveRight, PauseScreen_MoveLeft
VerticalScreenSpeedTable:
	DW PauseScreen_VerticalNeutral, PauseScreen_MoveDown, PauseScreen_MoveUp


NoMovement: RTS


ScreenMovement_OnlyRight:				;if screen bumps on left boundary of map screen
	LDA $05FD : BEQ +					;check if still momentum
	STZ $05FD : LDA #$36 : JSL $80903F	;zero speed and play sound (scrolling map) in library 1 (max queue: 6)
+ : BRA ScreenMovement_Right			;goto right map scroll

ScreenMovement_OnlyLeft:				;if screen bumps on right boundary of map screen
	LDA $05FE : BEQ +
	STZ $05FE : LDA #$36 : JSL $80903F
+

ScreenMovement_Left:
	LDA $B1 : SEC : SBC $05FD : STA $B1 : BCS +	;move BG1 left by n pixel
	DEC $B2 : + : RTS							;if underflow: decrement screen page
ScreenMovement_Horizontal:
	JSR ScreenMovement_Left
ScreenMovement_Right:
	LDA $B1 : CLC : ADC $05FE : STA $B1 : BCC +	;move BG1 right by n pixel
	INC $B2 : + : RTS							;if overflow: increment screen page


ScreenMovement_OnlyDown:				;if screen bumps on up boundary of map screen
	LDA $05FF : BEQ +
	STZ $05FF : LDA #$36 : JSL $80903F
+ : BRA ScreenMovement_Down

ScreenMovement_OnlyUp:					;if screen bumps on down boundary of map screen		
	LDA $0600 : BEQ +
	STZ $0600 : LDA #$36 : JSL $80903F
+

ScreenMovement_Up:
	LDA $B3 : SEC : SBC $05FF : STA $B3 : BCS +	;move BG1 up by n pixel
	DEC $B4 : + : RTS
ScreenMovement_Vertical:
	JSR ScreenMovement_Up
ScreenMovement_Down:
	LDA $B3 : CLC : ADC $0600 : STA $B3 : BCC +	;move BG1 down by n pixel
	INC $B4 : + : RTS


PauseScreen_MoveUp:
	LDA $05FF : CMP.b #!MapScrollSpeedCap : BPL + : INC $05FF : + : BRA PauseScreen_Decelerate_Down		;increase up scroll speed and jump to decrease down scroll speed
PauseScreen_MoveDown:
	LDA $0600 : CMP.b #!MapScrollSpeedCap : BPL + : INC $0600 : +	;increase down scroll speed

PauseScreen_Decelerate_Up:
	LDA $05FF : BEQ + : DEC $05FF : + : RTS			;decrease up scroll speed
PauseScreen_VerticalNeutral:
	JSR PauseScreen_Decelerate_Up
PauseScreen_Decelerate_Down:
	LDA $0600 : BEQ + : DEC $0600 : + : RTS			;decrease down scroll speed


PauseScreen_MoveLeft:
	LDA $05FD : CMP.b #!MapScrollSpeedCap : BPL + : INC $05FD : + : BRA PauseScreen_Decelerate_Right	;increase left scroll speed and jump to decrease right scroll speed
PauseScreen_MoveRight:
	LDA $05FE : CMP.b #!MapScrollSpeedCap : BPL + : INC $05FE : +	;increase right scroll speed

PauseScreen_Decelerate_Left:
	LDA $05FD : BEQ + : DEC $05FD : + : RTS			;decrease left scroll speed
PauseScreen_HorizontalNeutral:
	JSR PauseScreen_Decelerate_Left
PauseScreen_Decelerate_Right:
	LDA $05FE : BEQ + : DEC $05FE : + : RTS			;decrease right scroll speed
}
;---------------------------------------------------------------------------------------------------
;|x|                                    PRESERVE SCREEN INDEX                                    |x|
;---------------------------------------------------------------------------------------------------
{
ORG $829009		;during pause screen loading
	PHP
	JSR $A09A	;set up PPU for pause menu
	JSR $A12B	;load equipment screen tilemaps
	JSR $A615	;load button palette
	JSR $A84D	;update pause menu buttons
	JSL $829028	;set up general map scrolling (pause menu animation reset ; map scroll limit/position)
	LDA $0727 : BEQ +	;return if in map screen
	JSR $AB47	;set screen position for equipment section
	JSR $B1E0	;equipment screen VRAM transfer
+
        jmp pause_loading_end
;0 byte left!


;;; commented out for VARIA to restore vanilla pause menu behavior
;; ORG $82A106 : BRA $01 : NOP		;delete zero $0753	(button label index)
;; ORG $82A383 : BRA $01 : NOP		;delete zero $0727	(screen index)
;; ORG $82A3BF : BRA $01 : NOP		;delete zero $0753	(button label index)
;; ORG $82A3C2 : BRA $01 : NOP		;delete zero $0755	(equipment cursor index)


ORG $82A512		;make priority button check (so pause menu index doesn't get screwed if L/R + start button get pressed together)
	BIT #$1000 : BNE $54	;return if start is pressed
	BIT #$0020 : BNE $2B	;check for L button (same as vanilla)
	BIT #$0010 : BNE $04	;check for R button
	BRA $48					;return


ORG $82AB56					;optimized code of "set up reserve mode" + additions
	LDA $09C0 : BEQ ++				;check if reserve activated (in auto/manual mode)
	LDX #$0082 : STX $02
	LDX #$BF2A : CMP #$0001 : BEQ +	;AUTO tile offset
	LDX #$BF22 : + : STX $00		;load MANUAL offset instead if in manual mode
	LDX #$0006 : TXY
- : LDA $7E3A8E,x : AND #$FC00 : ORA [$00],y : STA $7E3A8E,x	;tile transfer
	DEX : DEX : TXY : BPL -			;loop
++ : STZ $0741 : STZ $0743				;\
	LDA $C10C : AND #$00FF : STA $072D	;animation resets
	LDA $C165 : AND #$00FF : STA $072F	;/

	LDA $0A76 : BNE +						;check if hyper beam active
	LDA $0755 : BNE ReturnNewCursorIndex	;check for new cursor position if not set/in reserve section
	LDA $09D4 : BEQ FindNewCursorIndex		;continue if no reserve
	STZ $0755 : BRA ReturnNewCursorIndex
;look for new cursor position if cursor still is in beam section after hyper beam activation, else return
+ : LDA $0755 : AND #$000F : DEC : BNE ReturnNewCursorIndex : BRA FindHyperBeamCursorReplacement
;5 bytes left


ORG $82ABBF : FindNewCursorIndex:
ORG $82ABDE : FindHyperBeamCursorReplacement:
ORG $82AC15 : ReturnNewCursorIndex:
}
}
