LoRom

;==============================================================
;//SPRITE REPLACEMENTS
;==============================================================
org $978DF4		;//[0B8DF4-0B8FCC]
	incbin options.bin
org $978FCD		;//[0B8FCD-0B91C3]
	incbin controller.bin
org $97938D		;//[0B938D-0B9539]
	incbin difficulty.bin
;--------------------------------------------------------------

;==============================================================
;//REFILL VALUES
;==============================================================
org $86F0BE	
	JSR Energy			;//jsl $91DF12
	NOP
org $86F0CD
	JSR Energy			;//jsl $91DF12
	NOP
org $86F0DC	;//will drop zero value if hard mode & vanilla drops just one
	;JSR PowerBombs			;//jsl $91DFF0
	;NOP
	JSL $91DFF0
org $86F0EB
	JSR Missiles			;//jsl $91DF80
	NOP
org $86F0FA	;//will drop zero value if hard mode & vanilla drops just one
	;JSR SuperMissiles		;//jsl $91DFD3
	;NOP
	JSL $91DFD3

;//FREE SPACE
;------------
org $86F5A0		;//[0375A0] ($1F bytes)
Energy:
	JSR Values
	JSL $91DF12
	RTS
;PowerBombs:
;	JSR Values
;	JSL $91DFF0
;	RTS
Missiles:
	JSR Values
	JSL $91DF80
	RTS
;SuperMissiles:
;	JSR Values
;	JSL $91DFD3
;	RTS
Values:
	PHA				
	LDA $7ED808			;//difficulty flag
	CMP #$0000			;//normal mode
	BEQ +				;//skip division if normal mode
	PLA
	LSR A				;//division
	PHA
+
	PLA
	RTS				;//return	
;--------------------------------------------------------------

;==============================================================
;//STOP ITEM CANCEL WHEN HARD MODE (AUTO) IS SELECTED
;==============================================================
org $90AD6B		;//item cancel ($0B bytes)
	LDA $09EA			;//vanilla
	BEQ $06				;//vanilla
	NOP : NOP : NOP			;//skip stz $09D2
	NOP : NOP : NOP			;//skip stz $0A04
;--------------------------------------------------------------


;==============================================================
;//SAMUS ARMOR & DAMAGE REDUCTION (ENEMIES)
;==============================================================
org $A0A6E4		;//projectile damage array
	JSR DamageReduction

;//FREE SPACE
;------------
org $A0FED0		;//[107ED0] ($20 bytes + $0E bytes HardMode:)
DamageReduction:	;//checks for hard mode
	LDA $0C2C,x 			;//projectile damage array
	PHA				;//get out the way
	LDA $7ED808			;//difficulty flag
	CMP #$0000			;//if normal mode
	BEQ +				;//branch
	PLA				;//damage array
	LSR A				;//some division
	STA $7EFFFE			;//UNUSED RAM
	LDA $0C2C,x
	SEC
	SBC $7EFFFE			;//damage reduction
	PHA
+
	PLA				;//damage array
	RTS				;//return
HardMode:		;//checks for hard mode ($0E bytes)
	LDA $7ED808			;//item cancel (difficulty)
	CMP #$0000
	BEQ +				;//branch if normal
	ASL $12			;//multiply
+
	LDA $09A2			;//equipped items
	RTS				;//return

org $A0A45E		;//suit damage division ($19 bytes)
	STA $12
	JSR HardMode
;; ;//COMMENT REST OF ROUTINE FOR VANILLA DIVISOR
;; 	BIT #$0001			;//checks for varia, branches if NOT equipped
;; 	BEQ +
;; 	LSR $12				;//varia equipped, divide damage by 2
;; +
;; 	BIT #$0020			;//checks for gravity, branches if NOT equipped
;; 	BEQ ++		
;; 	LSR $12				;//gravity equipped, divide damage by 2
;; ++
;; 	LDA $12				;//loads the resulting damage to A and returns
;; 	RTL				;//return
;; 	NOP : NOP : NOP			;//nice
;--------------------------------------------------------------

;==============================================================
;//DISPLAY DIFFICULTY ON FILE SELECT SCREEN
;==============================================================
org $81A149
	JSR DisplayDifficulty
	NOP

;//FREE SPACE
;------------
org $81FA0A 		;//[00FA00] ($42 bytes)
DisplayDifficulty:
	STA $7E3642,x	;[$7E:379E]	;//moved (x=#$015C)
	PHX
	PHY
	LDA $09EA
	ASL A				;//this shows hard mode
	TAY
	LDA DifficultySprites,y
    	TAY
- 
	LDA $0000,y
	BMI +				;//this shows all sprites instead of first letter
	STA $7E366A,x
	INX : INX
	INY : INY
	BRA -
+ 
	PLY
	PLX
	RTS

DifficultySprites:
	DW NormalSprites,HardSprites
NormalSprites:				;//mode:nff
	DW $2076,$2078,$206D,$206E,$208C,$2077,$FFFF
HardSprites:				;//mode:hff
	DW $2076,$2078,$206D,$206E,$208C,$2071,$FFFF

	NOP				;//to know where the data ends

;--------------------------------------------------------------

;==============================================================
;//Save & Load (for everything not starting at ceres elevator)
;==============================================================
org $A2A9B5		;//part of samus arrival routine
	JSR SaveMode			;//lda $0952

org $8283E0		;//part of the ceres routine
	NOP : NOP : NOP			;//lda $0952

;//FREE SPACE
;------------
org $A2FFE0		;//[117FE0] ($16 bytes) End of bank
SaveMode:
	LDA $7E09EA
	;CMP #$0000
	BNE +
	LDA #$0000
	BRA ++
+
	LDA #$0001
++
	STA $7ED808
	LDA $0952			;//moved
	RTS

org $80858F
	JSR LoadMode

;//FREE SPACE
;------------
org $80FFA0		;//[007FA0] ($16 bytes) End of bank b4 rom info
LoadMode:
	LDA $7ED808
	;CMP #$0000			;//check normal flag
	BNE +				;//if not normal
	LDA #$0000			;//else normal mode
	BRA ++
+
	LDA #$0001			;//hard
++
	STA $7E09EA
	LDA $079F			;//moved
	RTS
;--------------------------------------------------------------

org $8DFFF0
        db $ff
