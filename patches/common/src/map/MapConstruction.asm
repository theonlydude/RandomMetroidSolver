
;---------------------------------------------------------------------------------------------------
;|x|                                    BANK $??        Map Construction                         |x|
;---------------------------------------------------------------------------------------------------
{

!AlwaysActive = ""
!MapStationActive = "LDA $0789 : BNE + : LDA #$0300 : STA $2E"	;check if mapstation is active in current area

!AreaPalettes_RAM = !palettes_ram+(!AreaPalettes_BaseIndex*!palette_size)+(2*!AreaPalettes_ExploredColorIndex)

ORG !Freespace_MapConstruction
LoadMapFromPause:
	PHP : REP #$30 : STZ $2E

        ;; overwrite explored tile color in palettes based on area
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

	!MapDecorationAppearence		;config: draw map deco depending on mapstation setting
+ : LDA #$4000 : JSR MainMapConstruction		;construct map in this RAM location
	INC !Update_Minimap_VRAM_Flag	;set bit for transfer to VRAM
	PLP : RTL


ConstructMapFromAreaTransition:
	JSL $80858C		;transfer explored bits of next area
ConstructMap:
	LDA $079F : STA !OriginAreaIndex
	LDA #$0300 : STA $2E
	LDA.w #!RAM_ActiveMap : JSR MainMapConstruction : RTL


;[A] = address in bank $7E (RAM)
MainMapConstruction:
	PHB : STA $04					;save address
	LDA #$007E : STA $06 : STA $0E	;set bank of target address to 7E

	LDA.w #!EmptyTile : STA [$04]	;set defining tile as empty maptile
	LDX $04 : TXY : INY : INY		;set source and target
	LDA #$0FFD : MVN $7E7E			;clear up entire map with empty maptiles
	PHK : PLB

	JSR MapDecoration
	JSL LoadSourceMapData			;[$00] = long pointer to current area map data
;map station loaded maptiles pointer
	LDA $079F : ASL A : TAX : LDA #$0082 : STA $0A
	LDA $829717,x : STA $08
;prepare first 16 bits of loaded tiles
	LDA [$08] : XBA : STA $26 : INC $08 : INC $08
;prepare first 16 bits of explored tiles
	LDA $079F : CMP !OriginAreaIndex : BEQ +	;check if in current area
	XBA : CLC : ADC #$CD52 : BRA ++				;use different explored area bit array
+ : LDA #$07F7 : ++ : STA $0C					;else use current area explored bit array
	LDA [$0C] : XBA : STA $28 : INC $0C : INC $0C
	LDY #$0000

.tile : LDA [$00],y : ASL $28 : BCC +	;is tile explored?
	ASL $26 : BRA .save		;yes! go to save directly
+ : ASL $26 : BCC .skip		;no! Skip if tile is not loaded
	LDX $0789 : BEQ .skip	;skip if map station is not activated in this area
;If tile loaded and map station active: load tile with different tile and palette
++ : PHY : SEP #$30
	TAX : LDA.l CoverTileList,x					;load cover tile
	XBA : TAY : AND #$1C : LSR : LSR : TAX		;unexplored palette index
	TYA : AND #$E3 : ORA.w UnexploredPalette,x	;set palette
	XBA : REP #$30 : PLY
.save : STA [$04],y							;save tile
.skip : INY : INY : CPY #$1000 : BPL ++		;branch if all tiles asigned
	TYA : BIT #$001F : BNE .tile
	LDA [$08] : XBA : STA $26 : INC $08 : INC $08	;load next 16 bits of loaded tiles
	LDA [$0C] : XBA : STA $28 : INC $0C : INC $0C	;load next 16 bits of explored tiles
	BRA .tile : ++

;check for any itembits who change tiles in this region
	LDX #$0000 : TXY						;set [X] and [Y] to 0
-- : TYX : LDA $7ED870,x : BEQ .empty		;check if 16 bits of itembits are 0
	STA $14 : LDX #$0000

.loop : LSR $14 : BCS +	;if shifted a item bit out
	BEQ .empty			;if no item bits left
- : INX : BRA .loop		;set counter to next item bit

;bit has been found
+ : STX $10 : TYA : ASL #3 : CLC : ADC $10	;offset of itembit checklist from itembits
	JSR ChangeTileWithItembit
	LDX $10 : BRA -

.empty : INY : INY : CPY #$0040 : BCC --	;loop
	STZ !SamusMapPositionMirror				;zero minimap mirror upon map construction
	PLB : RTS


;change palette of unexplored tile
UnexploredPalette:
	DB !UnexploredTilePalette0<<2, !UnexploredTilePalette1<<2, !UnexploredTilePalette2<<2, !UnexploredTilePalette3<<2
	DB !UnexploredTilePalette4<<2, !UnexploredTilePalette3<<2, !UnexploredTilePalette5<<2, !UnexploredTilePalette7<<2


; [A] = Itembit
; $04 = Map (destination)
; $20 = Item tilecheck bitmask
; $22 = Maptile from map
ChangeTileWithItembit:
	ASL : TAX : LDA.l ItemTileCheckList,x	;load from list
	STA $20 : BEQ +++						;if entry is empty
	AND #$3800 : LSR #3 : XBA : CMP $079F : BNE +++		;check if in current area
	TYX : LDA $20 : AND #$07FF : ASL : TAY : LDA [$04],y : STA $22	;load tile from position of tilecheck
	LDA $20 : ASL : BCS +						;MSB set: <tile> +, else <tile> -
	DEC $22 : ASL : BCC ++ : DEC $22 : BRA ++	;if next bit is set: additional <tile> -
+ : INC $22 : ASL : BCC ++ : INC $22			;if next bit is set: additional <tile> +
++ : LDA $22 : STA [$04],y : TXY
+++ : RTS


ChangeTileFromPLM:		;used in bank $84
	STA $7ED870,x		;save itembit
	LDA.w #!RAM_ActiveMap : STA $04		;save destination of loaded map to DirectPage
	LDA #$007E : STA $06
	LDA $04,s : TAX : LDA $1DC7,x		;gather item index
	JSR ChangeTileWithItembit
	STZ !SamusMapPositionMirror : RTL	;zero minimap mirror upon item collection


; $04 = Map (destination)
MapDecoration:
	PHB : PEA.w !Freespace_MapDecoration>>8 : PLB : PLB		;set bank to decoration data
	LDA $079F : ASL : TAX : LDA.w MapDecoration_AreaPointer,x : TAX : BRA +	;pointer to decoration data of current area

--- : LDX $12 : INX #4					;next deco tilegroup
+ : STX $12 : LDA $0000,x : BPL +++		;if not a pointer (terminator) -> return
	STA $14 : SEP #$20					;$14 = pointer of current deco tilegroup
	LDA $0003,x : XBA : LDA $0002,x : ASL #3 : REP #$20 : LSR #2 : TAY	;tilegroup offset from X and Y coords
	LDA $0002,x : BIT #$0020 : BEQ +				;check if deco tilegroup X position is >= $20 (right map page)
	TYA : ORA #$0800 : TAY : + : LDX $14			;adjust offset to right page
-- : STY $16										;$16 = starting offset of starting/next row
	LDA $0000,x : AND #$00FF : BIT #$00C0 : BNE ---	;set tile amount of row, terminator is >= $40 (over max map size)
	STA $14 : INX									;$14 = tile amount
;Draw row of deco tilegroup
- : DEC $14 : BMI .nextrow							;branch if row done
	LDA $0000,x : BEQ + : BIT $2E : BNE + : STA [$04],y		;save tile, skip if $0000
+ : INX #2 : INY #2 : TYA : BIT #$003F : BNE -		;check if reaching map page border
	CLC : ADC #$07C0 : CMP #$1000 : BPL .failsave	;adjust to map page border, goto failsave if offset over map size
	TAY : BRA -
.nextrow : LDA $16 : CLC : ADC #$0040 : CMP #$1000 : BPL --- : TAY : BRA --	;adjust offset to next row, skip current deco tilegroup if over map size
.failsave : INX #2 : DEC $14 : BNE .failsave : BRA .nextrow					;skip current row tile drawing and proceed to next row
+++ : PLB : RTS


;Code from $829517 (top and bottom code are the same as original, but the big middle part is nearly, if not identical as $82943D)
;Used as map loading after hex map
LoadMapFromGameMenuBeforeStart:
;set background data
	SEP #$30
	LDA #$33 : STA $5D
	LDA #$13 : STA $69
	REP #$30
	LDA $079F : STA !OriginAreaIndex
	LDA #$0300 : STA $2E
	LDA #$4000 : JSR MainMapConstruction
;transfer to VRAM
	LDX $0330
	LDA #$1000 : STA $D0,x								;size
	LDA #$4000 : STA $D2,x : LDA #$007E : STA $D4,x		;source
	LDA $58 : AND #$00FC : XBA : STA $D5,x				;destination
	TXA : CLC : ADC #$0007 : STA $0330
	RTL
}
