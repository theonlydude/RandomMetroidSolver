;;; Super Metroid save/load routine expansion v1.0
;;; Made by Scyzer, patched for VARIA integration
;;;
;;; This patch/asm file will modify the saving and loading routine of Super Metroid for the SNES.
;;; The most basic function is that is will change how maps are stored and loaded, meaning you will be able to use the ENTIRE map for all areas.
;;; Debug is still not supported due to space limitations, but there is no map for this area anyway, so...
;;; 
;;; KejMap is made completely redundant by this patch, so dont bother applying it (it won't do anything if you already have)
;;; 
;;; VARIA : extra SRAM features are removed, save/load hooks are removed, now an include file instead of a standalone patch

include

CheckSumAdd: CLC : ADC $14 : INC A : STA $14 : RTS

SaveGame: PHP : REP #$30 : PHB : PHX : PHY
	PEA $7E7E : PLB : PLB : PHA
        jsr patch_save          ; call VARIA pre-save hook
        STZ $14 : PLA : AND #$0003 : ASL A : STA $12
	LDA $079F : INC A : XBA : TAX : LDY #$00FE
SaveMap: LDA $07F7,Y : STA $CD50,X : DEX : DEX : DEY : DEY : BPL SaveMap		;Saves the current map
	LDY #$005E
SaveItems: LDA $09A2,Y : STA $D7C0,Y : DEY : DEY : BPL SaveItems				;Saves current equipment	
	LDA $078B : STA $D916		;Current save for the area
	LDA $079F : STA $D918		;Current Area
	LDX $12 : LDA.l slots_sram_offsets,X : TAX : LDY #$0000		;Where to save for items and event bits
SaveSRAMItems: LDA $D7C0,Y : STA $700000,X : JSR CheckSumAdd : INX : INX : INY : INY : CPY #$0160 : BNE SaveSRAMItems	
	LDY #$06FE		;How much data to save for maps
SaveSRAMMaps: LDA $CD52,Y : STA $700000,X : INX : INX : DEY : DEY : BPL SaveSRAMMaps
SaveChecksum: LDX $12 : LDA $14 : STA $700000,X : STA $701FF0,X : EOR #$FFFF : STA $700008,X : STA $701FF8,X
EndSaveGame: PLY : PLX : PLB : PLP : RTL

;;; this hijacks regular load, VARIA hijacks menu load
LoadGame: PHP : REP #$30 : PHB : PHX : PHY
	PEA $7E7E : PLB : PLB : STZ $14 : AND #$0003 : ASL A : STA $12
	TAX : LDA.l slots_sram_offsets,X : STA $16 : TAX : LDY #$0000		;How much data to load for items and event bits
LoadSRAMItems: LDA $700000,X : STA $D7C0,Y : JSR CheckSumAdd : INX : INX : INY : INY : CPY #$0160 : BNE LoadSRAMItems
	LDY #$06FE		;How much data to load for maps
LoadSRAMMaps: LDA $700000,X : STA $CD52,Y : INX : INX : DEY : DEY : BPL LoadSRAMMaps
LoadCheckSum: LDX $12 : LDA $700000,X : CMP $14 : BNE $0B : EOR #$FFFF : CMP $14 : BNE $02 : BRA LoadSRAM
	LDA $14 : CMP $701FF0,X : BNE SetupClearSRAM : EOR #$FFFF : CMP $701FF8,X : BNE SetupClearSRAM : BRA LoadSRAM
LoadSRAM: LDY #$005E
LoadItems: LDA $D7C0,Y : STA $09A2,Y : DEY : DEY : BPL LoadItems		;Loads current equipment
	LDA $D916 : STA $078B		;Current save for the area
	LDA $D918 : STA $079F		;Current Area
	PLY : PLX : PLB : PLP : CLC : RTL
SetupClearSRAM: LDX $16 : LDY #!regular_save_size-2 : LDA #$0000
ClearSRAM: STA $700000,X : INX : INX : DEY : DEY : BPL ClearSRAM
	PLY : PLX : PLB : PLP : SEC : RTL
