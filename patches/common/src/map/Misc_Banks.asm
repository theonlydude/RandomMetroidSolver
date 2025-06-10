
;---------------------------------------------------------------------------------------------------
;|x|                                    BANK $80        VRAM                                     |x|
;---------------------------------------------------------------------------------------------------
{
;Required tiles for HUD get fittingly transfer to RAM and then transfered to VRAM here.
ORG $8095A7 : JSR NMI_MinimapHijack

ORG $8098FF
HUD_MapTileOffset: 
;; DW $005B, $005C, $005D, $005E, $005F	;row 0 of HUD map
;; ORG $80993F : DW $006B, $006C, $006D, $006E, $006F		;row 1 of HUD map
;; ORG $80997F : DW $007B, $007C, $007D, $007E, $007F		;row 2 of HUD map

ORG $809AF3 : STZ !SamusMapPositionMirror : NOP		;remove broken minimap update during start game
ORG $80A153 : JSL RevertAreaNumber

ORG !FreespaceBank80_VRAM
NMI_MinimapHijack:
	LDA !Update_Minimap_VRAM_Flag : BEQ .end	;check if update minimap flag is set
        ;; actually update gfx
	PHP : SEP #$30
;row 0 tiles to VRAM
	LDA #$80 : STA $2115		;set video port control (only need to do once)
	LDA #$D8 : STA $2116		;set low byte of target in VRAM
        LDA $5E : ASL #4 : CLC : ADC #$02 : PHA		;determine high byte of target and save it to stack
	STA $2117		;set high byte of target in VRAM
	JSL $8091A9					;set up DMA transfer (channel, transfer mode, destination address : source : size)
	DB $01, $01, $18 : DL !RAM_Minimap_GFX : DW $0050
	LDA #$02 : STA $420B		;activate DMA transfer
;row 1 tiles to VRAM
	LDA #$58 : STA $2116
	PLA : INC : PHA : STA $2117
	JSL $8091A9
	DB $01, $01, $18 : DL !RAM_Minimap_GFX+$50 : DW $0050
	LDA #$02 : STA $420B
;row 2 tiles to VRAM
	LDA #$D8 : STA $2116
        PLA : STA $2117
	JSL $8091A9
	DB $01, $01, $18 : DL !RAM_Minimap_GFX+$A0 : DW $0050
	LDA #$02 : STA $420B
	
	PLP : STZ !Update_Minimap_VRAM_Flag	;zero flag to not update minimap every frame
.end : JMP $91EE							;jump to "update IO registers"


;Force update minimap to prevent showing garbage when unpausing or during room transition
ForceUpdateHUDMapInKraid:
	LDA #$02 : BRA $02		;set tile address of BG 3
ForceUpdateHUDMapOutKraid:
	LDA #$04 : STA $5E : STA !Update_Minimap_VRAM_Flag : RTL


;Return area number and mapstation flag to original values when unpausing
RevertAreaNumber:
	LDA !OriginAreaIndex : STA $079F : TAX		;area number
	LDA $7ED908,x : AND #$00FF : STA $0789	 	;map station flag
	JMP $835D		;return
print "bank 80 end: ", pc

warnpc $80CE3F
}
;---------------------------------------------------------------------------------------------------
;|x|                                    BANK $81        Planet Zebes Map                         |x|
;---------------------------------------------------------------------------------------------------
{
;Remove routine offset, where palette gets overwriten when going back from map to graph again
ORG $819E6D
	DW $A546, $A578, $A5B3, $AFF6, $B0BB, $9E7B, $FFFF


ORG $81A3C4 : JSR PlanetZebesGraphMapPaletteHijack


ORG $81A3D6 : LDA.w PlanetZebesGPIOColored,x	;for area graph colored
ORG $81A3DF : LDA.w PlanetZebesGPIOGrayed,x		;for area graph grayed out

ORG $81A3E3 : LDA.w PlanetZebesGPI,y	;area graph palette instruction
ORG $81A3ED : LDA.w PlanetZebesGPI+2,y	; " +2
ORG $81A3F2 : LDA #$0004	;amount of colors changed

ORG $81A40E
	;colored
	DW $7FE0, $7EA0, $7D40, $7C00	;Wrecked Ship	(light blue)
	DW $01DB, $0196, $0150, $00EB	;Crateria		(orange)
	DW $033B, $0296, $01F0, $014B	;Crateria		(yellow)
	;18
	DW $6400, $4C00, $3400, $1C00	;Maridia		(blue)
	DW $0013, $000F, $000A, $0006	;Norfair		(red)
	DW $0BB1, $0B0D, $0669, $05A4	;Brinstar		(green)
	;30
	DW $7FE0, $7EA0, $7D40, $7C00	;Wrecked Ship	(light blue)
	DW $6417, $4C12, $380D, $2007	;Tourian		(pink)
	DW $5280, $4620, $39C0, $2940	;Wrecked Ship	(cyan)
	;gray
	;48
	DW $35AD, $2D6B, $2529, $18C6	;Wrecked Ship
	DW $4A52, $3DEF, $318C, $2108	;Crateria
	DW $56B5, $4A52, $39CE, $2D6B	;Crateria
	;60
	DW $18C6, $14A5, $1084, $0842	;Maridia
	DW $1084, $0C63, $0842, $0421	;Norfair
	DW $2108, $1CE7, $14A5, $1084	;Brinstar
	;78
	DW $35AD, $2D6B, $2529, $18C6	;Wrecked Ship
	DW $294A, $2108, $1CE7, $14A5	;Tourian
	DW $4A52, $3DEF, $318C, $2108	;Wrecked Ship

;Instruction offset
PlanetZebesGPIOColored:	;PlanetZebesGraphPaletteInstructionOffsetColored
	DW PZGPICrateriaColored-PlanetZebesGPI, PZGPIBrinstarColored-PlanetZebesGPI, PZGPINorfairColored-PlanetZebesGPI, PZGPIWreckedShipColored-PlanetZebesGPI, PZGPIMaridiaColored-PlanetZebesGPI, PZGPITourianColored-PlanetZebesGPI
PlanetZebesGPIOGrayed:	;PlanetZebesGraphPaletteInstructionOffsetGrayed
	DW PZGPICrateriaGrayed-PlanetZebesGPI, PZGPIBrinstarGrayed-PlanetZebesGPI, PZGPINorfairGrayed-PlanetZebesGPI, PZGPIWreckedShipGrayed-PlanetZebesGPI, PZGPIMaridiaGrayed-PlanetZebesGPI, PZGPITourianGrayed-PlanetZebesGPI

;Instruction
PlanetZebesGPI:	;PlanetZebesGraphPaletteInstruction
	;$(color offset), $(palette position), $FFFF(terminator)
PZGPICrateriaColored:
	DW $0008, $00B0
	DW $0010, $00B8, $FFFF
PZGPIBrinstarColored:
	DW $0028, $00D8, $FFFF
PZGPINorfairColored:
	DW $0020, $00D0, $FFFF
PZGPIWreckedShipColored:
	DW $0000, $00A8
	DW $0030, $00E8
	DW $0040, $00F8, $FFFF
PZGPIMaridiaColored:
	DW $0018, $00C8, $FFFF
PZGPITourianColored:
	DW $0038, $00F0, $FFFF

PZGPICrateriaGrayed:
	DW $0050, $00B0
	DW $0058, $00B8, $FFFF
PZGPIBrinstarGrayed:
	DW $0070, $00D8, $FFFF
PZGPINorfairGrayed:
	DW $0068, $00D0, $FFFF
PZGPIWreckedShipGrayed:
	DW $0048, $00A8
	DW $0078, $00E8
	DW $0088, $00F8, $FFFF
PZGPIMaridiaGrayed:
	DW $0060, $00C8, $FFFF
PZGPITourianGrayed:
	DW $0080, $00F0, $FFFF


MaptilePaletteOverwriteOffset:
	DW $0002, $0022, $0042, $0062
	DW $0082, $00A2, $00C2, $00E2
;$20 bytes left


ORG $81A79F : LDA.l !PauseScreen_Map_Tilemap_Pointer,x

;Switch RAM locations for constructing map border after hex map ($7E4000) and map tilemap ($7E3000)
ORG $81A7A3 : STA $7E3000,x
ORG $81A7B1 : STA $7E3000,x
ORG $81A7BC : LDA #$3154
ORG $81A7D3 : STA $7E3000,x
ORG $81A7E5 : LDA #$3000
ORG $81AB00 : LDA #$3000


ORG $81A823 : LDA #$0015		;new "return to file select" index value

ORG $81AD1D : JSL LoadMapFromGameMenuBeforeStart
ORG $81AD56 : LDA $B3 : CLC : ADC #$0018 : STA $B3 : NOP #2		;adjust screen Y position for different mapframe position

;Map screen border offset
ORG $81AED4 : SBC.w #!Left_MapFrameOffset+!Left_MapBorderOffset<<3
ORG $81AEE6 : ADC.w #!Right_MapFrameOffset+!Right_MapBorderOffset<<3-1
ORG $81AEFC : SBC.w #!Top_MapFrameOffset+!Top_MapBorderOffset-3<<3
ORG $81AF0E : SBC.w #$1D-!Bottom_MapFrameOffset-!Bottom_MapBorderOffset<<3+1

ORG $81AFD3						;freespace from removed "refresh palette" routine
PlanetZebesGraphMapPaletteHijack:
	LDY #$000E
-- : LDX.w MaptilePaletteOverwriteOffset,y	;load offset 
	LDA #$0003 : STA $12					;color overwrite amount
- : LDA.l !PauseScreen_Palette_Pointer,x : STA.l $7EC000,x		;take from pause screen palette and apply to current one
	INX : INX : DEC $12 : BNE -
	DEY : DEY : BPL --
	INC $0727 : RTS
;2 bytes left
}
;---------------------------------------------------------------------------------------------------
;|x|                                    BANK $??        Misc.                                    |x|
;---------------------------------------------------------------------------------------------------
{
;---------------------------------------BANK $??----------------------------------------------------

ORG $90DF7F : BRA $01 : NOP	;remove STZ $0B2A
ORG $91F1D9 : BRA $01 : NOP	;remove STZ $0B2A
ORG $9BCA00 : BRA $01 : NOP	;remove STZ $0B2A

;;; copy the whole HUD tile sheet in Kraid unpause hook when Kraid is dead
;;; instead of just half
org $A7C244
        dw $1000

;---------------------------------------BANK $84----------------------------------------------------
ORG $848CA6
	INC $0789 : STZ $0727	;set mapstation loaded bit ;set pause screen index to "map"
	JMP $8747				;reconstruct active map for loaded tiles

ORG $848747
	JSL ConstructMap					;load area map to RAM map after mapstation activation
	PLY : PLX : RTS

ORG $8488AA : JSL ChangeTileFromPLM		;change RAM map after item bit is set


;---------------------------------------BANK $88----------------------------------------------------
ORG $8883D2 : JSL ForceUpdateHUDMapOutKraid		;triggered every room transition


;---------------------------------------BANK $8E----------------------------------------------------
;File select menu palette overwrite (doesn't influence anything, just visual indication)
ORG $8EE4A2 : DW $02DF, $7FF4, $001F, $7FE0, $7EA0, $7D40, $7C00, $01DB, $0196, $0150, $00EB, $033B, $0296, $01F0, $014B
ORG $8EE4C2 : DW $0E3F, $7FF4, $001F, $6400, $4C00, $3400, $1C00, $0013, $000F, $000A, $0006, $0BB1, $0B0D, $0669, $05A4
ORG $8EE4E2 : DW $4631, $7FF4, $001F, $7FE0, $7EA0, $7D40, $7C00, $6417, $4C12, $380D, $2007, $5280, $4620, $39C0, $2940	


;---------------------------------------BANK $8F----------------------------------------------------
;Custom setup ASM (set collected map on current area)
ORG $8F0000+!SetCollectedAreaCodePosition
set_collected_map:
	REP #$30
	LDX !area_index : LDA !map_station_ram,x
	BIT #$0001 : BNE +							;check if map station bit has been set for this area
	ORA #$0001 : STA !map_station_ram,x : STA $0789		;set map station bit for this area
	JSL ConstructMap							;reload active map
+ : RTS
print "bank 8F end ", pc
}
