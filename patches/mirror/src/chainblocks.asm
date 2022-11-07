;****************************************
;Fusion/ZM style chain block PLM
;By: Black Falcon
;Version: 1.00

;This PLM defines the starting block of a chain of blocks to break
;Place it on a breakable block of any sort. Destroying that one block triggers the breaking of the chain.

;NOTE: it will NOT be triggered if any other block of the chain you defined gets destroyed!
;NOTE2: it will destroy ANY PLM within its path, except for this PLM itself, which will be triggered in this case.
;NOTE3: The broken chain will return after re-entering the room.

;So be careful when laying out the chain's path so it doesn't destroy items 'n stuff!
;You can trigger multiple chains by putting another chainblock PLM within the current chain's path
;this way you can make the chain branch off into different directions

;further instructions are given in the PLM's text file
;----------------------------------------

lorom	

!blockindex = $1D77,x

;;; old PLM address, relocate after endingtotals
; org $84F060
org $84fC1F

print "PLM: ", pc
PLM:
        DW INIT : DW INST       ; header

print "INST: ", pc
INST:
        DW MAIN                 ; instruction pointer

print "INIT: ", pc
INIT:
        PHX
        LDA $1C87,Y : LSR : STA $1D77,Y
        TYX
        LDA #$0001 : STA $7EDE1C,X ; PLM frame delay, always needed - 0 = wait 65365 frames...
        PLX
        RTS

print "MAIN: ", pc
MAIN:
	PHY : PHX
	JSR RUN
	PLX : PLY : PLA
	RTS

print "RUN: ", pc
RUN:
	TXY                     ; X contains the PLM's index
	LDA #INST : STA $1D27,X ; Store at Next PLM instruction
	PHX
	LDX $1C87,Y                                  ; current block index x2
	LDA $7F0002,X : PLX : CMP #$FF00 : BEQ BREAK ; breaks if air
        ;; does NOT break if:
	AND #$F000 : CMP #$4000 : BEQ IDLE ; shootable air
	CMP #$7000 : BEQ IDLE   ; bombable air
	CMP #$8000 : BEQ IDLE   ; solid
	CMP #$B000 : BEQ IDLE   ; crumble
	CMP #$C000 : BEQ IDLE   ; shot
	CMP #$F000 : BEQ IDLE   ; bomb
	CMP #$A000 : BEQ IDLE   ; Spike (enemy breakable block)
	BRA BREAK               ; else break

IDLE:                           ; SET = do nothing
        LDA #$0001 : STA $7EDE1C,X ; PLM frame delay, idling
        RTS

BREAK:
	LDA $1DC7,X : AND #$00FF : BEQ END
	TAY
	LDA !blockindex : STA $0DC4
	LDA #$D074 : JSL $8484E7 ; this routine creates PLMs at the desired spot
	DEY : TYA : STA $12
	LDA $1DC7,X : AND #$FF00 : CLC : ADC $12 : STA $1DC7,X ; store it to the argument without overwriting High
	LDA #$0004 : STA $7EDE1C,X ; 4 frames (almost the same speed as in Fusion/ZM) PLM frame delay
	LDA $1DC7,X : AND #$0F00 : BEQ END
	XBA : CMP #$0005 : BCS END
	CMP #$0001 : BEQ RIGHT
	CMP #$0002 : BEQ LEFT
	CMP #$0003 : BEQ UP
	CMP #$0004 : BEQ DOWN
END:
        LDA #$DFA9 : STA $1D27,X
        LDA #$0001 : STA $7EDE1C,X ; PLM frame delay
        RTS

RIGHT:
        INC !blockindex : BRA DIRECTION
LEFT:
        DEC !blockindex : BRA DIRECTION
UP:
        LDA !blockindex : SEC : SBC $07A5 : STA !blockindex : BRA DIRECTION ; subtract current rooms width in blocks
DOWN:
        LDA !blockindex : CLC : ADC $07A5 : STA !blockindex ; add current rooms width in blocks
DIRECTION:
	PHX
	LDA !blockindex : TAX
	LDA $7F6402,X : AND #$00FF : BEQ ARETEES ; check BTS map, if 00, continue
	CMP #$0005 : BCS ARETEES ; same with 5
	XBA : PLX : STA $12
	LDA $1DC7,X : AND #$00FF : CLC : ADC $12 : STA $1DC7,X ; store it to the argument without overwriting Lo
	RTS
ARETEES:
        PLX
        RTS

print "the end: ", pc
warnpc $84FD28
