lorom

;An Attempt to fix the scrolling sky issue with code, not just by placing dummy graphics into vram.
;this works for every door you enter a room that has scrolling sky, but iirc it messed up sometimes when loading from a save
;basically a certain value needs to be set in order to load the correct graphics to vram, so the sky does not mess up
;it works fine for the landing site, but I made this so long ago that I don't know if it worked for rooms with ocean sky too, so be sure to try it on a backup
;before applying it to your hack!

;8FB7AE:	bg_data room 793FE
;Landing site: FX2: C116, BG_data: B76A

;0E 00 FE 88 80 B1 8A 00 48 00 08	when landing with the ship, Y screen 0
;0E 00 B2 89 80 B9 8A 00 4C 00 08	top right door, Y screen 1, note 4C
;0E 00 46 89 80 C1 8A 00 48 00 08	top left door, Y screen 2
;0E 00 6A 89 80 D1 8A 00 48 00 08	bottom left door, Y screen 4
;0E 00 C6 8A 80 D1 8A 00 48 00 08	bottom right door, Y screen 4
;0E 00 0A 89 80 C1 8A 00 48 00 08	when loading from a save, Y screen 4, but WHY THE HELL C1 ?!??!?!!?!

;Scrolling sky with land: 88AD9C
;Scrolling sky with water: 88ADA6

;Byte B1: Screen Y 00
;Byte B9: Screen Y 01
;Byte C1: Screen Y 02
;Byte C9: Screen Y 03
;Byte D1: Screen Y 04
;Byte D9: Screen Y 05



org $82E5D9

JMP SKYFIX
BACK:

org $82F713
SKYFIX:
	PHY
	PHB
	PEA $8300
	PLB
	PLB
	LDY $078D		;current DDB pointer in bank $83
	LDA $0007,y		;target Y screen
	AND #$00FF
	PHA
	CMP #$0004
	BNE SKIP
	LDA $07DF
	CMP #$C11B
	BNE SKIP
	PLA
	ASL
	ASL
	ASL
	CLC
	ADC #$00B9
	BRA STORE
	
SKIP:	
	PLA
	ASL
	ASL
	ASL
	CLC
	ADC #$00B1		;determine screen
STORE:
	STA $12
	PLB
	PLY
	INY
	INY
	LDA $07DF
	LDA $0003,y
	STA $05BE
	LDA $0000,y
	STA $05C0
	LDA $0001,y
	AND #$FF00
	CLC
	ADC $12
	STA $05C1
	LDA $0005,y
	STA $05C3
	LDA #$8000
	TSB $05BC
	WAIT:
	BIT $05BC
	BMI WAIT
	SEC
	RTS
