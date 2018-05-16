lorom

;An Attempt to fix the scrolling sky issue with code, not just by placing dummy graphics into vram.
;this works for every door you enter a room that has scrolling sky, but iirc it messed up sometimes when loading from a save
;basically a certain value needs to be set in order to load the correct graphics to vram, so the sky does not mess up
;it works fine for the landing site, but I made this so long ago that I don't know if it worked for rooms with ocean sky too, so be sure to try it on a backup
;before applying it to your hack!

;Landing site (791F8): FX: 8380C0, FX2: 8FC116, BG_data: 8FB76A
;West Ocean (793FE): FX: 838112, FX2: 8FC11B, BG_data: 8FB7AE
;Small room with two doors (7968F): FX: 83818C, FX2: 8FC11B, BG_data: 8FB80A, Y screen 0 only
;East Ocean (794FD): FX: 838144, FX2: 8FC11B, BG_data: 8FB7F2

;;; FLO: This seems to be the original BG tables...landing site only???
;0E 00 FE 88 80 B1 8A 00 48 00 08	when landing with the ship, Y screen 0
;0E 00 B2 89 80 B9 8A 00 4C 00 08	top right door, Y screen 1, note 4C ; FLO : this one does not work, what is this "note 4C"??
;0E 00 46 89 80 C1 8A 00 48 00 08	top left door, Y screen 2
;0E 00 6A 89 80 D1 8A 00 48 00 08	bottom left door, Y screen 4
;0E 00 C6 8A 80 D1 8A 00 48 00 08	bottom right door, Y screen 4
;0E 00 0A 89 80 C1 8A 00 48 00 08	when loading from a save, Y screen 4, but WHY THE HELL C1 ?!??!?!!?!

;Scrolling sky with land: 88AD9C
;Scrolling sky with water: 88ADA6

;;; $88:AD9C             dx B180, B980, C180, C980, D180
;;; $88:ADA6             dx B180, B980, C180, C980, D980, E180 ; No D1 here

;;; West Ocean :
;;; Left+bottom right doors, Y screen 4 (works)
;;; Gravity Exit door : Y screen 3 (does not work)
;;; Bowling alley Reserve tank check exit door: Y screen 1 (does not work)
;;; Attic exit door : Y screen 0 (works)
;;; Bowling alley path exit : Y screen 2 (works)

;;; Small room wth 2 doors (fakely part of West Ocean):
;;; Bowling alley path exit : Y screen 0 (works)

;;; East Ocean:
;;; both doors: Y screen 4 (works)

;;; Landin site
;Byte B1: Screen Y 00
;Byte B9: Screen Y 01
;Byte C1: Screen Y 02
;Byte C9: Screen Y 03
;Byte D1: Screen Y 04
;Byte D9: Screen Y 05

org $82E5D9			; hijack original BG code
JMP SKYFIX			; with SKYFIX routine
BACK:

org $82F713 			; free space in bank $82
SKYFIX:
	PHY			; saves current Y (index) and B (data bank) registers
	PHB			;
	PEA $8300		; switches data bank to $83 (two PLB calls because B is 8 bits and a 16-bits value has been pushed)
	PLB			;
	PLB			; 
	LDY $078D		; Door Data Bytes pointer in bank $83 for current room transition
	LDA $0007,y		; target Y screen (DDB ptr + 7)
	AND #$00FF		; clear high byte, since Y screen is on one byte
	PHA			; saves target Y screen on the stack
	CMP #$0004		; checks if Y screen is 04
	BNE SKIP		; if not, goto SKIP
	LDA $07DF		; loads ptr to "room FX2"
	CMP #$C11B		; checks if it is C11B: Ocean. Y=4+Ocean BG: this check is for both Oceans bottom doors (I suspect East Ocean has 4 screens of useless rock at the top just for the doors to be at the same coords as west ocean ones...)
	BNE SKIP		; it not, goto SKIP
	PLA			; retrieve Y screen from stack
	ASL			; shift left Y screen 3 times (multiply by 8)
	ASL			;
	ASL			;
	CLC			; clear carry
	ADC #$00B9		; add B9 to Y with carry => D9 (since Y is 4)
	BRA STORE		; goto STORE
SKIP:	
	PLA			; retrieve Y screen from stack
	ASL			; shift left Y screen 3 times (multiply by 8)
	ASL			;
	ASL			;
	CLC			; clear carry
	ADC #$00B1		; add B1 to Y with carry: "determine screen" (original comment)
STORE:
	STA $12			; store processed screen Y position to $7e0012 : "Commmon horizontal subpixel value or X coordinate"
	PLB			; retrieve original data bank from stack
	PLY			; retrieve original Y index from stack
	INY			; IY += 2
	INY			;
	LDA $07DF		; loads ptr to "room FX2"...seems useless since A is overwritten the next instruction
	LDA $0003,y		; gets what's at IY + 3
	STA $05BE		; stores it at $7e05be : "Offset for VRAM. Used by 80:9632, when you enter a door"
	LDA $0000,y		; gets what's at IY 
	STA $05C0		; stores it at $7e05C0 : Source for VRAM update, including bank byte. Used by 80:9632, when you enter a door
	LDA $0001,y		; gets what's at IY + 1
	AND #$FF00		; clears low byte
	CLC			; add A to previously processed screen Y position 
	ADC $12			; 
	STA $05C1		; store it to $7e05C1 : same as C0. Done in two passes because 24-bits address.
	LDA $0005,y		; gets what's at IY+5
	STA $05C3		; store it to $7e05C3 : "Size of VRAM update.  Used by 80:9632, when you enter a door"
	LDA #$8000		; set highest bit to 1 at $7e05bc : write to VRAM flag 
	TSB $05BC		; 
WAIT:			
	BIT $05BC		; loops until highest bit of $7e05bc is cleared : waits for VRAM to be written 
	BMI WAIT
	SEC			; Set Carry flag for BG data code to properly detect the last BG data routine (this one) has been executed
	RTS			; return
