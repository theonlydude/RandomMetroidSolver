
;---------------------------------------------------------------------------------------------------
;|x|                                    BANK $90        Minimap                                  |x|
;---------------------------------------------------------------------------------------------------
{
ORG $90A7EE : LDA.w #!BossfightMinimapCovertile		;tile used to cover minimap during bossfights


;Change tiles in active map when entering a boss room ;update minimap
ORG $90A8C2 : TAX
ORG $90A8DF : TAY : SEP #$20 : LDA $07F7,y
ORG $90A8E5 : JSR UpdateActiveMapWithExplored : STZ !SamusMapPositionMirror


ORG $90A8EF
MinimapASM:
	PHP : STZ $12 : STZ $16 : SEP #$20
	LDA $05F7 : BNE .return				;minimap disabled
	LDA $0AF7 : CMP $07A9 : BCS +++
	LDA $0AFB : CMP $07AB : BCS +++		;is samus still in room
	LDA $0AF7 : CLC : ADC $07A1 : STA $12	;$12: samus X map coord
	LDA $0AFB : CLC : ADC $07A3 : INC	;$16: samus Y map coord
	STA $16 : CMP.w !SamusMapPositionMirror+1 : BNE ++
	LDA $12 : CMP.w !SamusMapPositionMirror : BEQ +++		;check if samus map coord has changed
	STA.w !SamusMapPositionMirror : BRA +				;save mirror and update minimap
++ : STA.w !SamusMapPositionMirror+1
+
        JSR UpdateMinimapTileset
+++ : LDA $7EC681 : AND #$E3 : TAX					;filter out palette from samus minimap position
	LDA $05B5 : BIT.b #$01<<!SamusMinimapPositionTimer : BNE +	;check global time for palette change
	AND.b #$01<<!SamusMinimapPositionTimer-1 : BNE .return		;check if palette has to be reverted back to origin
	TXA : ORA !MinimapIndicatorPalette : BRA ++		;set palette back to origin
+ : TXA : ORA.b #!SamusMinimapPositionPalette<<2	;set palette to position indicator palette
++ : STA $7EC681 : .return : PLP : RTL				;save palette ;return

UpdateMinimapTileset:
	PHP : REP #$30
	LDA $12 : AND #$0020 : STA $22	;$22 = map page
	LDA $12 : AND #$001F : STA $12 : AND #$0007 : TAX			;[X] bit index for explored bit
	LDA $12 : LSR #3 : STA $14
	LDA $16 : CLC : ADC $22 : ASL : ASL : CLC : ADC $14 : TAY	;[Y] index for explored bit
	SEP #$20 : LDA $07F7,y : JSR UpdateActiveMapWithExplored : REP #$30

	LDA $16 : CLC : ADC $22 : XBA : LSR #3 : CLC : ADC $12 : STA $14	;$14 = maptile index
	LDA $22 : BEQ + : LDA $12 : CMP #$0002 : BPL +	;is samus in right mappage and X = 0/1
	LDA $14 : SEC : SBC #$0402 : BRA ++		;adjust index to topleft corner of minimap and left mappage
+ : LDA $14 : SEC : SBC #$0022				;adjust index to topleft corner of minimap
++ : ASL : TAY

	LDA #$007E : STA $02 : STA $05 : STA $08	;set pointer of active RAM map for each row in minimap
	LDA.w #!RAM_ActiveMap : STA $00
	LDA.w #!RAM_ActiveMap+$40 : STA $03
	LDA.w #!RAM_ActiveMap+$80 : STA $06
	LDA #$0005 : STA $12 : STZ $14

;Row 0
- : LDA [$00],y : CMP.w #!EmptyTile : BNE +						;check if current tile is empty tile
	ORA.w #!MinimapPaletteEmptyTile<<10|$2000 : BRA ++			;set palette and priority bit
+ : AND #$1C00 : LSR : XBA : TAX								;gather palette from maptile and create index of palette for minimap
	LDA [$00],y : AND #$E3FF : ORA.w MinimapTilePaletteTable,x	;set minimap palette
++ : LDX $14 : STA $7EC63C,x
;Row 1
	LDA [$03],y : CMP.w #!EmptyTile : BNE +
	ORA.w #!MinimapPaletteEmptyTile<<10|$2000 : BRA ++
+ : AND #$1C00 : LSR : XBA : TAX
	LDA [$03],y : AND #$E3FF : ORA.w MinimapTilePaletteTable,x
++ : LDX $14 : STA $7EC67C,x
;Row 2
	LDA [$06],y : CMP.w #!EmptyTile : BNE +
	ORA.w #!MinimapPaletteEmptyTile<<10|$2000 : BRA ++
+ : AND #$1C00 : LSR : XBA : TAX
	LDA [$06],y : AND #$E3FF : ORA.w MinimapTilePaletteTable,x
++ : LDX $14 : STA $7EC6BC,x

	INC $14 : INC $14 : INY #2
	TYA : BIT #$003F : BNE +	;check for map wrap
	CLC : ADC #$07C0 : TAY		;set offset to right page
+ : DEC $12 : BNE - : BRA ApplyTileGFXtoRAM	;setting minimap tiles done?

;;; A = explored bits of samus current position
;;; Y = byte offset in current area map
UpdateActiveMapWithExplored:
	BIT $AC04,x : BNE ++		;check if tilebit has been set already
	ORA $AC04,x : STA $07F7,y	;save bit
	STX $20 : REP #$30
	JSL LoadSourceMapData		;[$00] = long pointer to current area map data
	TYA : ASL #3 : CLC : ADC $20 : ASL : TAX : TAY	;offset of maptile
	LDA [$00],y : STA !RAM_ActiveMap,x				;save origin tile to RAM minimap
        jsr update_area_tilecount
++ : RTS

ApplyTileGFXtoRAM:
	PHB : PEA $7E00 : PLB : PLB						;bank $7E
	STZ $12 : LDA $12 : LDY.w #!RAM_Minimap_GFX		;prepare loop ;[Y] maptile GFX transfer target

- : TAX : LDA $C63C,x : PHA : AND #$00FF : STA $14				;$14 = maptile index
	PLA : AND #$FC00 : ORA.l HUD_MapTileOffset,x : STA $C63C,x	;save HUD tile with palette and mirror
	LDA $14 : ASL #4 : ADC.w #!Freespace_MinimapTiles : TAX		;set source for transfer
	LDA #$000F : MVN.w !Freespace_MinimapTiles>>8&$FF00+$7E		;transfer maptile GFX to RAM
	LDA $12 : BIT #$0008 : BNE + : INC : INC : STA $12 : BRA -	;finish row check
+ : CLC : ADC #$0038 : STA $12 : CMP #$0090 : BMI -				;set index to next row

	INC !Update_Minimap_VRAM_Flag				;set bit for transfer to VRAM
	PLB : PLP
	LDA $7EC681 : AND #$1C : STA !MinimapIndicatorPalette	;set origin palette for samus position indicator
	RTS

;;; VARIA addition: maintain a RAM table of explored map tile count 
;;; A: exlored tile
update_area_tilecount:
        and #$03FF : cmp.w #!EmptyTile : bne .count ; don't count empty tiles you could reach with X-Ray climb etc.
        rts
.count:
        phx
        php
        %a8()
	;; determine current graph area in special byte in room state header
	ldx $07bb
	lda $8f0010,x : tax
        ;; if total tile count for this area is 0, don't count the tiles
        lda area_tiles, x : beq .end
        ;; we can afford counting tiles on a single byte (max is 177, upper norfair in area rando)
        lda.l !map_tilecounts_table, x : inc : sta.l !map_tilecounts_table, x
        %a16()
        lda.l !map_total_tilecount : inc : sta.l !map_total_tilecount
.end:
        plp
	plx
        rts

;;; quantities of tiles, per graph area. to be filled by randomizer based on flavor
%export(area_tiles)
        fillbyte 0 : fill !nb_areas

;;; total number of map tiles in the seed, to be filled by randomizer based on present areas
%export(total_tiles)
        dw 0

print "main minimap end: ", pc
warnpc $90AC04

ORG $90AC0C
MinimapTilePaletteTable:
	DW !MinimapPalette0<<10|$2000, !MinimapPalette1<<10|$2000, !MinimapPalette2<<10|$2000, !MinimapPalette3<<10|$2000
	DW !MinimapPalette4<<10|$2000, !MinimapPalette5<<10|$2000, !MinimapPalette6<<10|$2000, !MinimapPalette7<<10|$2000


ORG $90E734 : JSL MinimapASM
ORG $90E801 : JSL MinimapASM
ORG $90E873 : JSL MinimapASM
ORG $90E8E5 : JSL MinimapASM
ORG $90E8F8 : JSL MinimapASM


;;; VARIA addition: display custom area colors in minimap

;; hook some palettes management
org $82E4A2
        jsl load_target_palette : nop : nop

org $82e75a
        jsl door_transition

org $82E7C9
        jsl load_tileset_palette : nop : nop : nop


;; change "end HUD drawing" IRQ handlers to skip registers update so we
;; can do it ourselves
org $80961c     ; main gameplay
        dw $96c1
org $809620     ; start of door transition
        dw $9708
org $809624     ; draygon's room
        dw $9746
org $809628     ; vertical transition
        dw end_hud_irq_vertical_transition
org $80962e     ; horizontal transition
        dw end_hud_irq_horizontal_transition

;; Hook into begin/end HUD drawing IRQs to switch colors
!vcounter_target = $1e          ; since we raise the HUD, trigger IRQ 1 line early
!hcounter_target = 220          ; change IRQ fire in scanline to restore display at the proper time
!hud_draw_offset = 1

org $8096A2
        ldy.w #!vcounter_target
        jmp begin_hud
org $8096CF
        jmp end_hud_main_gameplay
org $8096EA
        ldy.w #!vcounter_target
        jmp begin_hud
org $809716
        jmp end_hud_transition_start
org $80972C
        ldy.w #!vcounter_target
        jmp begin_hud
org $809754
        jmp end_hud_draygon
org $80976A
        ldy.w #!vcounter_target
        jmp begin_hud
org $8097D3
        ldy.w #!vcounter_target
        jmp begin_hud

;; raise HUD one pixel to have an extra scanline to change colors
org $888338
        jsl raise_hud

org $82E304
        jsl raise_hud_door_transition : nop
org $88838B
        nop : nop

org $808764
        jsr enable_hcounter

;; normal explored color
!pal2_idx = 9
;; normal unexplored color
!pal3_idx = 13
;; palette 6 (used for color math)
!pal6_idx = 25
;; palette 0 (acid)
!pal0_idx = 1
;; palette 7 red flashing color
!pal7_idx = 30

;; CGRAM access registers
!CGADD = $2121
!CGDATA = $2122

;; explored colors definitions
!explored_0_index = !pal2_idx
!explored_0 = $0362
!explored_0_backup #= !explored_0_index*2+!palettes_ram

!explored_1_index = !pal0_idx
!explored_1 = $0364
!explored_1_backup #= !explored_1_index*2+!palettes_ram

!explored_2_index = !pal6_idx
!explored_2 = $0366
!explored_2_backup #= !explored_2_index*2+!palettes_ram

;; to raise HUD during door transitions and message boxes
!NMI_BG3_scroll = $bb
!BG3VOFS = $2112

;; F-Blank management
!NMI_INIDISP = $51
!INIDISP = $2100
!OPHCT = $213C
!STAT78 = $213F
!WRIO = $4201
!hcounter_begin_hud = $0368

macro setNextColor(addr)
        lda <addr> : sta.w !CGDATA
        lda <addr>+1 : sta.w !CGDATA
endmacro

macro setColor(index, addr)
        lda.b #<index> : sta.w !CGADD
        %setNextColor(<addr>)
endmacro

macro addWhite()
        lda.b #$ff : sta.w !CGDATA : sta.w !CGDATA
endmacro

macro beginFBlank()
        lda.b !NMI_INIDISP : ora.b #$80 : sta.w !INIDISP
endmacro

macro endFBlank()
        lda.b !NMI_INIDISP : sta.w !INIDISP
endmacro


org $80d600
begin_hud:
        pha
        %a8()
        %beginFBlank()
        %setColor(!explored_0_index, !explored_0)
        %setColor(!explored_1_index, !explored_1)
        %addWhite()
        %setColor(!explored_2_index, !explored_2)
        %addWhite()
        ;; save hcounter (beam position) to determine next IRQ hcounter target
        ;; indeed, depending on active HDMA the time taken by the IRQ handler varies
        ;; see https://problemkaputt.de/fullsnes.htm#snespictureprocessingunitppu
        ;; section "SNES PPU Timers and Status" for details
        stz.w !WRIO : lda.b #$80 : sta.w !WRIO
        lda.w !OPHCT : sta.w !hcounter_begin_hud
        lda.w !OPHCT : and.b #$01 : sta.w !hcounter_begin_hud+1
        lda.w !STAT78
        %a16()
        ;; some heuristics based on hcounter value
        ;; whatever works, we can't afford fancy calculations in an IRQ handler
        lda.w !hcounter_begin_hud
        cmp.w #165 : bcc .low
        cmp.w #180 : bcc .high
        ldx.w #!hcounter_target
        bra .end
.high:
        ldx.w #!hcounter_target-20
        bra .end
.low:
        ldx.w #!hcounter_target+20
.end:
        %a8()
        %endFBlank()
        %a16()
        pla
        rts

macro endHudColors()
        %beginFBlank()
        %setColor(!explored_2_index, !explored_2_backup)
        %setNextColor(!explored_2_backup+2)
        %setColor(!explored_1_index, !explored_1_backup)
        %setNextColor(!explored_1_backup+2)
        %setColor(!explored_0_index, !explored_0_backup)
endmacro

macro mainGameplayStart()
	LDA.b $70;| 8096AB | 80 | \
	STA.w $2130                      ;| 8096AD | 80 | } Colour math control register A = [gameplay colour math control register A]
	LDA.b $73;| 8096B0 | 80 | \
	STA.w $2131                      ;| 8096B2 | 80 | } Colour math control register B = [gameplay colour math control register B]
	LDA.b $5b;| 8096B5 | 80 | \
	STA.w $2109                      ;| 8096B7 | 80 | } BG3 tilemap base address and size = [gameplay BG3 tilemap base address and size]
endmacro

end_hud_main_gameplay:
        ldx.w #$0098              ; hijacked code
        pha
        %a8()
        %endHudColors()
        ;; vanilla code
        %mainGameplayStart()
	LDA.b $6a      ;| 8096BA | 80 | \
	STA.w $212C                      ;| 8096BC | 80 | } Main screen layers = [gameplay main screen layers]
.end:
        %endFBlank()
        %a16()
        pla
        rts

end_hud_transition_start:
        ldx.w #$0098              ; hijacked code
        pha
        %a8()
        %endHudColors()
        ;; vanilla code
        LDA.w $07b3                         ;| 8096F3 | 80 | \
        ORA.w $07b1                 ;| 8096F6 | 80 | |
        BIT.b #$01                              ;| 8096F9 | 80 | } If ([CRE bitset] | [previous CRE bitset]) & 1 != 0:
        BEQ .BRA_809701                          ;| 8096FB | 80 | /
        LDA.b #$10                              ;| 8096FD | 80 | \
        BRA .BRA_809703                          ;| 8096FF | 80 | } Main screen layers = sprites
; Else (([CRE bitset] | [previous CRE bitset]) & 1 = 0):
.BRA_809701:
        LDA.b #$11                              ;| 809701 | 80 |  Main screen layers = BG1/sprites
.BRA_809703:
        STA.w $212C                      ;| 809703 | 80 | 
.end:
        %endFBlank()
        %a16()
        pla
        rts

end_hud_draygon:
        ldx.w #$0098              ; hijacked code
        pha
        %a8()
        %endHudColors()
        %mainGameplayStart()
        %endFBlank()
.end:
        %a16()
        pla
        rts

end_hud_irq_vertical_transition:
        %a8()
        %endHudColors()
        ;; vanilla code
        LDA.w $07b3                         ;| 8096F3 | 80 | \
        ORA.w $07b1                 ;| 8096F6 | 80 | |
        BIT.b #$01                              ;| 8096F9 | 80 | } If ([CRE bitset] | [previous CRE bitset]) & 1 != 0:
        BEQ .BRA_809781                          ;| 80977B | 80 | /
        LDA.b #$10                              ;| 80977D | 80 | \
        BRA .BRA_809783                          ;| 80977F | 80 | } Main screen layers = sprites
; Else (([CRE bitset] | [previous CRE bitset]) & 1 = 0):
.BRA_809781:
        LDA.b #$11                              ;| 809781 | 80 |  Main screen layers = BG1/sprites
.BRA_809783:
        STA.w $212C                      ;| 809783 | 80 | 
        STZ.w $2130                      ;| 809786 | 80 | \
        STZ.w $2131                      ;| 809789 | 80 | } Disable colour math
        REP.b #$20                              ;| 80978C | 80 | 
        LDX.w $05bc      ;| 80978E | 80 | \
        BPL .BRA_809796                          ;| 809791 | 80 | } If door transition VRAM update:
        JSR.w $9632   ;| 809793 | 80 |  Execute door transition VRAM update
.BRA_809796:
        LDA.w $0931                       ;| 809796 | 80 | \
        BMI .BRA_80979F                          ;| 809799 | 80 | } If door transition has not finished scrolling:
        JSL.l $80AE4E              ;| 80979B | 80 |  Follow door transition
.BRA_80979F:
        LDY.w #$00D8                            ;| 8097A2 | 80 |  IRQ v-counter target = D8h
        ldx.w #$0098
        %a8()
        %endFBlank()
        %a16()
        LDA.w #$0014                            ;| 80979F | 80 |  Interrupt command = 14h
.end:
        rts

end_hud_irq_horizontal_transition:
        %a8()
        %endHudColors()
        ;; vanilla code
        LDA.w $07b3                         ;| 8096F3 | 80 | \
        ORA.w $07b1                 ;| 8096F6 | 80 | |
        BIT.b #$01                              ;| 8096F9 | 80 | } If ([CRE bitset] | [previous CRE bitset]) & 1 != 0:
        BEQ .BRA_8097EA                          ;| 8097E4 | 80 | /
        LDA.b #$10                              ;| 8097E6 | 80 | \
        BRA .BRA_8097EC                          ;| 8097E8 | 80 | } Main screen layers = sprites
; Else (([CRE bitset] | [previous CRE bitset]) & 1 = 0):
.BRA_8097EA:
        LDA.b #$11                              ;| 8097EA | 80 |  Main screen layers = BG1/sprites
.BRA_8097EC:
        STA.w $212C                      ;| 8097EC | 80 | 
        STZ.w $2130                      ;| 8097EF | 80 | \
        STZ.w $2131                      ;| 8097F2 | 80 | } Disable colour math
        REP.b #$20                              ;| 8097F5 | 80 | 
        LDA.w $0931                       ;| 8097F7 | 80 | \
        BMI .BRA_809800                          ;| 8097FA | 80 | } If door transition has not finished scrolling:
        JSL.l $80AE4E              ;| 8097FC | 80 |  Follow door transition
.BRA_809800:
        LDY.w #$00A0                            ;| 809803 | 80 |  IRQ v-counter target = A0h (bottom of door)
        ldx.w #$0098
        %a8()
        %endFBlank()
        %a16()
        LDA.w #$001A                            ;| 809800 | 80 |  Interrupt command = 1Ah
.end:
        rts

load_target_palette:
        ;; Prevent HUD map colors from gradually changing (e.g. to blue/pink) during door transition
        jsr target_pal
        ;; hijacked code
        LDA #$E4A9
        STA $099C
        rtl

target_pal:
        lda 2*!pal3_idx+!palettes_ram : sta 2*!pal3_idx+!palettes_ram+$200
        lda 2*!pal7_idx+!palettes_ram : sta 2*!pal7_idx+!palettes_ram+$200
        rts

door_transition:
        JSL $848270             ; hijacked code
        jsr set_hud_map_colors
        rtl

load_tileset_palette:
        ;; vanilla code: Decompress [tileset palette pointer] to $7E:C200
        JSL $80B0FF
        dl $7EC200
        jsr set_hud_map_colors
        jsr target_pal
        rtl

set_hud_map_colors:
        lda #!unexplored_gray : sta 2*!pal3_idx+!palettes_ram
        lda #!vanilla_etank_color : sta 2*!pal7_idx+!palettes_ram
        ;; FIXME hardcode for now
        lda #!AreaColor_Crateria : sta !explored_0
        lda #!AreaColor_WreckedShip : sta !explored_1
        lda #!AreaColor_Tourian : sta !explored_2
        rts

;; affects the BG3 scroll HDMA object, active during main gameplay
raise_hud:
        lda.w #!hud_draw_offset : sta $7ECADA
        lda.w #0
        rtl

;; as BG3 scroll HDMA object is inactive during door transitions,
;; we set it via the NMI routine
raise_hud_door_transition:
        lda.w #!hud_draw_offset : sta.b !NMI_BG3_scroll
        ;; hijacked code
        LDA #$0008
        STA $A7
        rtl

enable_hcounter:
        lda.b #$80 : sta.w !WRIO
        rts

org $858199
;; replace BG3 Y scroll value at the top of the screen in HDMA RAM table
raise_hud_msg_boxes:
        lda.b #!hud_draw_offset
        sta.w !BG3VOFS
        nop
org $8581A7
        lda.w #!hud_draw_offset
org $8582D7
        lda.w #!hud_draw_offset
}
