
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
        ;; $18 = minimap tile palette table addr
        jsl get_room_minimap_table : sta $18

;Row 0
- : LDA [$00],y : CMP.w #!EmptyTile : BNE +						;check if current tile is empty tile
	ORA.w #!MinimapPaletteEmptyTile<<10|$2000 : BRA ++			;set palette and priority bit
+ : PHY : AND #$1C00 : LSR : XBA : PHA								;gather palette from maptile and create index of palette for minimap
	LDA [$00],y : AND #$E3FF : PLY : ORA ($18), y : PLY	;set minimap palette
++ : LDX $14 : STA $7EC63C,x
;Row 1
	LDA [$03],y : CMP.w #!EmptyTile : BNE +
	ORA.w #!MinimapPaletteEmptyTile<<10|$2000 : BRA ++
+ : PHY : AND #$1C00 : LSR : XBA : PHA
	LDA [$03],y : AND #$E3FF : PLY : ORA ($18), y : PLY
++ : LDX $14 : STA $7EC67C,x
;Row 2
	LDA [$06],y : CMP.w #!EmptyTile : BNE +
	ORA.w #!MinimapPaletteEmptyTile<<10|$2000 : BRA ++
+ : PHY : AND #$1C00 : LSR : XBA : PHA
	LDA [$06],y : AND #$E3FF : PLY : ORA ($18), y : PLY
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
        and #$03FF : cmp.w #!EmptyTile : beq ++ ; don't count empty tiles you could reach with X-Ray climb etc.
        lda !VARIA_area_id : jsl update_area_tilecount
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
;;; A: VARIA area id
update_area_tilecount:
        phx
        php
        %ai8()
	tax
        ;; if total tile count for this area is 0, don't count the tiles
        lda area_tiles, x : beq .end
        ;; we can afford counting tiles on a single byte (max is 177, upper norfair in area rando)
        lda.l !map_tilecounts_table, x : inc : sta.l !map_tilecounts_table, x
        %a16()
        lda.l !map_total_tilecount : inc : sta.l !map_total_tilecount
.end:
        plp
	plx
        rtl

;;; quantities of tiles, per graph area. to be filled by randomizer based on flavor
%export(area_tiles)
        fillbyte 0 : fill !nb_areas

;;; total number of map tiles in the seed, to be filled by randomizer based on present areas
%export(total_tiles)
        dw 0

;; actual data depends on flavor and is provided in separate patch
MinimapTilePaletteTables:

print "main minimap end: ", pc
org $90AC04
.limit:

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

org $82E21B
        jsl preserve_etank_color : nop : nop

;;; add some new IRQ commands to handle colors, so create a new table
org $80987C
        dw new_irq_table

;; raise HUD to have extra scanlines to restore colors
!hud_draw_offset #= 2

;; IRQ parameters
!vcounter_target_begin = 2
!vcounter_target_colors #= 31-!hud_draw_offset
!vcounter_target_end = 31
!hcounter_target = 178
!hcounter_end_hud_door_transitions_offset #= 0

;; direct page flag to offset hcounter when HUD HDMA is not active and main gameplay IRQ is used (pause/message boxe)
!no_hud_hdma_flag = $ce
!no_hud_hdma_offset #= !hcounter_end_hud_door_transitions_offset ; value to offset when no_hud_hdma_offset is non-zero


org $888338
        jsl raise_hud

org $82E304
        jsl raise_hud_door_transition : nop
org $88838B
        nop : nop

org $828DF7
        jsl raise_hud_pause : nop
org $82A104
        nop : nop

org $82809C
        jsl raise_hud_loading

;;; in main gameplay, reset no hud hdma flag
org $828B4B
        jsl reset_no_hud_hdma_flag

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
;; long writes to INIDISP mitigates early read glitch (https://undisbeliever.net/snesdev/registers/inidisp.html#early-read-glitch)
!INIDISP_begin_fblank #= $800000+!INIDISP
!INIDISP_end_fblank #= $0f0000+!INIDISP

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

macro clearFBlank()
        ;; disables F-blank, but turn beam black to avoid glitches
        lda.b #0 : sta.l !INIDISP_end_fblank
endmacro

macro beginFBlank()
        lda.b #$80 : sta.l !INIDISP_begin_fblank
print "begin fblank ", pc
endmacro

macro endFBlank()
        lda.b !NMI_INIDISP : sta.l !INIDISP_end_fblank
print "end fblank ", pc
endmacro


;; IRQ handlers logic: vanilla "begin HUD" IRQ now points to a new one that will, on scanline 0
;; - enable F-Blank (needed to access CGRAM)
;; - swap colors
;; - run vanilla IRQ handler
;; - setup the next IRQ (new) late on scanline 2
;; This new "end begin HUD" IRQ will :
;; - disable F-blank
;; - setup "end HUD" IRQ (new) on scanline 28
;; This new "end HUD" IRQ will :
;; - enable F-blank
;; - restore colors
;; - run most of vanilla IRQ handler
;; - setup "end HUD end" IRQ late on scanline 31 (vanilla end HUD IRQ)
;; "end HUD end" IRQ will :
;; - disable F-blank
;; - run extended vanilla IRQ handler
;;
;; What is run and when is the result of various experiments, notably regarding door transitions. IRQ trigger time and
;; exec duration vary, and are dependant on stuff like the amount of running HDMA, which makes adjusting timings
;; for them to work in all cases very difficult.
;;
;; Actual SNES hardware is where most glitches appear, Mesen being the emulator that shows the most, followed by bsnes-accuracy.
;; Other tested emulators (snes9x, normal bsnes, SNES Classic canoe) are way less finnicky and probably don't require
;; half of the shenanigans below.

;; change next IRQ commands and vtarget in "begin HUD" original handlers:
;; door transition start
org $8096E8
        db $22
org $8096EB
        db !vcounter_target_colors
org $8096EE
        db !hcounter_target+!hcounter_end_hud_door_transitions_offset

;; draygon room
org $80972A
        db $26
org $80972D
        db !vcounter_target_colors
org $809730
        db !hcounter_target

;; vertical transition
org $809768
        db $2a
org $80976B
        db !vcounter_target_colors
org $80976E
        db !hcounter_target+!hcounter_end_hud_door_transitions_offset

;; horizontal transition
org $8097D1
        db $2e
org $8097D4
        db !vcounter_target_colors
org $8097D7
        db !hcounter_target+!hcounter_end_hud_door_transitions_offset


;; replace etank tile with a custom one using palette 7,
;; so etanks don't change color with minimap
org $809BDC
        ldx.w etank_tile

org $80d600
etank_tile:                     ; put this in ROM to be able to disable the minimap HUD colors
        dw BGtile($4f, 7, 1, 0, 0)

new_irq_table:
        dw $966E, $9680
        dw irq_colors_begin_hud_main_gameplay    ; IRQ cmd $04: main gameplay begin hud drawing
        dw irq_colors_end_hud_main_gameplay_end  ; IRQ cmd $06: main gameplay end hud drawing
        dw irq_colors_begin_hud_start_transition ; IRQ cmd $08: start of door transition begin hud drawing
        dw irq_colors_end_hud_start_transition_end  ; IRQ cmd $0A: start of door transition end hud drawing
        dw irq_colors_begin_hud_draygon          ; IRQ cmd $0C: draygon room begin hud drawing
        dw irq_colors_end_hud_draygon_end        ; IRQ cmd $0E: draygon room end hud drawing
        dw irq_colors_begin_hud_vertical_transition  ; IRQ cmd $10: vertical transition begin hud drawing
        dw irq_colors_end_hud_vertical_transition_end ; IRQ cmd $12: vertical transition end hud drawing
        dw $97A9
        dw irq_colors_begin_hud_horizontal_transition ; IRQ cmd $16: horizontal transition begin hud drawing
        dw irq_colors_end_hud_horizontal_transition_end  ; IRQ cmd $18: horizontal transition end hud drawing
        dw $980A
        ;; new entries:
        dw irq_colors_begin_hud_main_gameplay_end     ; IRQ cmd $1C: original main gameplay begin hud drawing + end FBlank
        dw irq_colors_end_hud_main_gameplay           ; IRQ cmd $1E
        dw irq_colors_begin_hud_start_transition_end  ; IRQ cmd $20: original start of door transition begin hud drawing + end FBlank
        dw irq_colors_end_hud_start_transition ; IRQ cmd $22
        dw irq_colors_begin_hud_draygon_end          ; IRQ cmd $24: original draygon room begin hud drawing
        dw irq_colors_end_hud_draygon       ; IRQ cmd $26
        dw irq_colors_begin_hud_vertical_transition_end ; IRQ cmd $28: original vertical transition begin hud drawing
        dw irq_colors_end_hud_vertical_transition ; IRQ cmd $2A
        dw irq_colors_begin_hud_horizontal_transition_end ; IRQ cmd $2C: original horizontal transition begin hud drawing
        dw irq_colors_end_hud_horizontal_transition ; IRQ cmd $2E

begin_hud:
        %beginFBlank()
        %setColor(!explored_0_index, !explored_0)
        %setColor(!explored_1_index, !explored_1)
        %addWhite()
        %setColor(!explored_2_index, !explored_2)
        %addWhite()
        lda.b #!pal7_idx+1 : sta.w !CGADD
        %addWhite()
        rts

end_hud:
        %setColor(!pal7_idx+1, 2*(!pal7_idx+1)+!palettes_ram)
        %setColor(!explored_2_index, !explored_2_backup)
        %setNextColor(!explored_2_backup+2)
        %setColor(!explored_1_index, !explored_1_backup)
        %setNextColor(!explored_1_backup+2)
        %setColor(!explored_0_index, !explored_0_backup)
        rts

irq_colors_begin_hud_main_gameplay:
        %a8()
        jsr begin_hud
        LDA.b #$5A : STA.w $2109
        STZ.w $2130 : STZ.w $2131
        LDA.b #$04 : STA.w $212C
        %a16()
        lda.w #$1C
        ldy.w #!vcounter_target_begin
        ldx.w #!hcounter_target
        rts

irq_colors_begin_hud_main_gameplay_end:
        %a8()
        %endFBlank()
        %a16()
        LDX.w #!hcounter_target
        lda !no_hud_hdma_flag : beq +
        ldx.w #!hcounter_target+!no_hud_hdma_offset
+
        LDA.w #$001E
        LDY.w #!vcounter_target_colors
        rts

irq_colors_end_hud_main_gameplay:
        %a8()
        %beginFBlank()
        LDA.b $70;| 8096AB | 80 | \
        STA.w $2130                      ;| 8096AD | 80 | } Colour math control register A = [gameplay colour math control register A]
        LDA.b $73;| 8096B0 | 80 | \
        STA.w $2131                      ;| 8096B2 | 80 | } Colour math control register B = [gameplay colour math control register B]
        LDA.b $5b;| 8096B5 | 80 | \
        STA.w $2109                      ;| 8096B7 | 80 | } BG3 tilemap base address and size = [gameplay BG3 tilemap base address and size]
        LDA.b $6a      ;| 8096BA | 80 | \
        STA.w $212C                      ;| 8096BC | 80 | } Main screen layers = [gameplay main screen layers]
        jsr end_hud
        %clearFBlank()
        %a16()
        ldx.w #!hcounter_target
        lda !no_hud_hdma_flag : beq +
        ldx.w #!hcounter_target+!no_hud_hdma_offset
+
        lda.w #$06
        ldy.w #!vcounter_target_end
        rts

irq_colors_end_hud_main_gameplay_end:
        %a8()        
        %endFBlank()
        jmp $96BF

irq_colors_begin_hud_start_transition:
        %a8()
        jsr begin_hud
        LDA.b #$5A                              ;| 8096D5 | 80 | \
        STA.w $2109                      ;| 8096D7 | 80 | } BG3 tilemap base address = $5800, size = 32x64
        LDA.b #$04                              ;| 8096DA | 80 | \
        STA.w $212C                      ;| 8096DC | 80 | } Main screen layers = BG3
        STZ.w $2130                      ;| 8096DF | 80 | \
        STZ.w $2131                      ;| 8096E2 | 80 | } Disable colour math
        %a16()
        lda.w #$20
        ldy.w #!vcounter_target_begin
        ldx.w #!hcounter_target
        rts

irq_colors_begin_hud_start_transition_end:
        %a8()
        %endFBlank()
        jmp $96e5

irq_colors_end_hud_start_transition:
        %a8()
        %beginFBlank()
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
        jsr end_hud
        %clearFBlank()
        %a16()
        lda.w #$0a
        ldy.w #!vcounter_target_end
        ldx.w #!hcounter_target
        rts

irq_colors_end_hud_start_transition_end:
        %a8()
        %endFBlank()
        jmp $9706

irq_colors_begin_hud_draygon:
        %a8()
        jsr begin_hud
        LDA.b #$04                              ;| 80971C | 80 | \
        STA.w $212C                      ;| 80971E | 80 | } Main screen layers = BG3
        STZ.w $2130                      ;| 809721 | 80 | \
        STZ.w $2131                      ;| 809724 | 80 | } Disable colour math
        %a16()
        lda.w #$24
        ldy.w #!vcounter_target_begin
        ldx.w #!hcounter_target
        rts

irq_colors_begin_hud_draygon_end:
        %a8()
        %endFBlank()
        jmp $9727

irq_colors_end_hud_draygon:
        %a8()
        %beginFBlank()
        LDA.b $5b;| 809735 | 80 | \
        STA.w $2109                      ;| 809737 | 80 | } BG3 tilemap base address and size = [gameplay BG3 tilemap base address and size]
        LDA.b $70;| 80973A | 80 | \
        STA.w $2130                      ;| 80973C | 80 | } Colour math control register A = [gameplay colour math control register A]
        LDA.b $73;| 80973F | 80 | \
        STA.w $2131                      ;| 809741 | 80 | } Colour math control register B = [gameplay colour math control register B]
        jsr end_hud
        %clearFBlank()
        %a16()
        lda.w #$0E
        ldy.w #!vcounter_target_end
        ldx.w #!hcounter_target
        rts

irq_colors_end_hud_draygon_end:
        %a8()
        %endFBlank()
        jmp $9744

irq_colors_begin_hud_vertical_transition:
        %a8()
        jsr begin_hud
        LDA.b #$04                              ;| 80975A | 80 | \
        STA.w $212C                      ;| 80975C | 80 | } Main screen layers = BG3
        STZ.w $2130                      ;| 80975F | 80 | \
        STZ.w $2131                      ;| 809762 | 80 | } Disable colour math
        %a16()
        lda.w #$28
        ldy.w #!vcounter_target_begin
        ldx.w #!hcounter_target+!hcounter_end_hud_door_transitions_offset
        rts

irq_colors_begin_hud_vertical_transition_end:
        %a8()
        %endFBlank()
        jmp $9765

irq_colors_end_hud_vertical_transition:
        %a8()
        %beginFBlank()
        LDA.w $07b3                         ;| 809773 | 80 | \
        ORA.w $07b1                 ;| 809776 | 80 | |
        BIT.b #$01                              ;| 809779 | 80 | } If ([CRE bitset] | [previous CRE bitset]) & 1 != 0:
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
        jsr end_hud
        %clearFBlank()
        %a16()
        lda.w #$12
        ldy.w #!vcounter_target_end
        ldx.w #!hcounter_target+!hcounter_end_hud_door_transitions_offset
        rts

irq_colors_end_hud_vertical_transition_end:
        %a8()
        %endFBlank()
        jmp $978c

irq_colors_begin_hud_horizontal_transition:
        %a8()
        jsr begin_hud
        LDA.b #$04                              ;| 8097C3 | 80 | \
        STA.w $212C                      ;| 8097C5 | 80 | } Main screen layers = BG3
        STZ.w $2130                      ;| 8097C8 | 80 | \
        STZ.w $2131                      ;| 8097CB | 80 | } Disable colour math
        %a16()
        lda.w #$2C
        ldy.w #!vcounter_target_begin
        ldx.w #!hcounter_target+!hcounter_end_hud_door_transitions_offset
        rts

irq_colors_begin_hud_horizontal_transition_end:
        %a8()
        %endFBlank()
        jmp $97CE

irq_colors_end_hud_horizontal_transition:
        %a8()
        %beginFBlank()
        LDA.w $07b3                         ;| 8097DC | 80 | \
        ORA.w $07b1                 ;| 8097DF | 80 | |
        BIT.b #$01                              ;| 8097E2 | 80 | } If ([CRE bitset] | [previous CRE bitset]) & 1 != 0:
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
        jsr end_hud
        %clearFBlank()
        %a16()
        lda.w #$18
        ldy.w #!vcounter_target_end
        ldx.w #!hcounter_target+!hcounter_end_hud_door_transitions_offset
        rts

irq_colors_end_hud_horizontal_transition_end:
        %a8()
        %endFBlank()
        jmp $97F5

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
        phx
        lda #!unexplored_gray : sta 2*!pal3_idx+!palettes_ram
        lda #!vanilla_etank_color : sta 2*!pal7_idx+!palettes_ram
        ;; get explored colors from table
        lda !VARIA_minimap_room_type : and #$00ff : asl : asl : asl : tax
        lda.l minimap_color_data+2, x  : sta !explored_0
        lda.l minimap_color_data+4, x  : sta !explored_1
        lda.l minimap_color_data+6, x  : sta !explored_2
        plx
        rts

preserve_etank_color:
        LDA $C03A : STA $C23A   ; hijacked code
        LDA $C03C : STA $C23C
        rtl

;;; returns in A the ptr to minimap palette table in bank 90
get_room_minimap_table:
        lda !VARIA_minimap_room_type : and #$00ff : asl : asl : asl : tax
        lda.l minimap_color_data, x
        rtl

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

raise_hud_pause:
        lda.b !NMI_BG3_scroll : sta.w $0770 ; hijacked code
        lda.b #1 : sta.b !no_hud_hdma_flag
        lda.b #!hud_draw_offset : sta.b !NMI_BG3_scroll
        rtl

raise_hud_loading:
        JSL $888288     ; hijacked code: Enable HDMA objects
        JSL $88D865     ; Spawn HUD BG3 scroll HDMA object
        rtl

reset_no_hud_hdma_flag:
        stz.b !no_hud_hdma_flag
        lda.w #0
        rtl

print "b80 end: ", pc
;; table indexed by room type containing 8 byte entries of the form:
;; minimap_palettes_ptr_bank90, explored_0, explored_1, explored_2
;; actual data depends on flavor etc so it will be applied in separate patch
minimap_color_data:
org $80e000
.limit:


;; message boxes

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

;; prevent the game from manipulating palette 6 (useless because overwritten by IRQ handler)
org $858152
skip_msgbox_colors:
        ;; set no hud hdma flag when setting up msg boxes
        lda.b #$01 : sta.b !no_hud_hdma_flag
        bra .skip
org $858169
.skip:

;; change button letters palettes, face buttons in pink, shoulders in gray
org $858426
        dw BGtile($e0, 2, 1, 0, 0) ; pink A
        dw BGtile($e1, 2, 1, 0, 0) ; pink B
        dw BGtile($f7, 2, 1, 0, 0) ; pink X
        dw BGtile($f8, 2, 1, 0, 0) ; pink Y
        dw BGtile($d0, 2, 1, 0, 0) ; white select
        dw BGtile($eb, 3, 1, 0, 0) ; gray L
        dw BGtile($f1, 3, 1, 0, 0) ; gray R

;;; adjust Bomb Message
org $8590c9
        dw BGtile($dc, 7, 1, 0, 0)
org $85914d
        dw BGtile($cd, 7, 1, 0, 0)

;; change save dialog arrow color to pink
org $85948F
        dw BGtile($cc, 2, 1, 0, 0)
        dw BGtile($cd, 2, 1, 0, 0)
org $8595D1
        dw BGtile($cc, 2, 1, 0, 0)
        dw BGtile($cd, 2, 1, 0, 0)
org $859623
        dw BGtile($cc, 2, 1, 0, 0)
        dw BGtile($cd, 2, 1, 0, 0)

;; replace unexplored+map selection/etank colors in Phantoon WS power on palettes
org $A7CA61+(2*!pal3_idx)
        dw !unexplored_gray
org $A7CA61+(2*!pal7_idx)
        dw !vanilla_etank_color
}
