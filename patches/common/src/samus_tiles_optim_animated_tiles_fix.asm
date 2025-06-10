;;; Transfer Samus tiles optimization + animated tiles fix v1.1 by H A M
;;; 
;;; included mainly for the 1st feature, as it saves a lot of cycles in NMI routine,
;;; and compensate for the time lost there by RTA timer and map gfx transfer
;;; 
;;; VARIA adaptation:
;;; The original patch is compatible with SpriteSomething, but applying a custom sprite
;;; after this patch crashes the game, since SpriteSomething overwrites vanilla code 
;;; in the same place. So instead of rewriting in place the "transfer samus tiles" routine,
;;; we put the new version in free space and call it there.

arch 65816
lorom

org $8095A1
        jsr transfer_samus_tiles ; overwrite call to original transfer tiles routine to our own

org $80A0D9 : JSL ResetStuff
org $82895A : LDA #$8000 : TRB $071F : TRB $0721 ; Clear Samus tiles transfer flags
org $829392 : JSL UnpauseAnimatedTiles

org $928040
        TAX : EOR $071F : ASL : BEQ + ; If [A] != [Samus top half tiles definition]:
        NOP : NOP
        STX $071F ; Samus top half tiles definition = [A], flag transfer for Samus top half tiles to VRAM
+

org $92807E
        TAX : EOR $0721 : ASL : BEQ + ; If [A] != [Samus bottom half tiles definition]:
        NOP : NOP
        STX $0721 ; Samus bottom half tiles definition = [A], flag transfer for Samus bottom half tiles to VRAM
+

org $82936A : BRA $01 ; skip clearing samus/beam tiles when unpausing

org $809416
process_animated_tiles:
	LDA $1EF1 : BPL + ; If animated tiles objects are disabled: return
	LDY #$87 : STY $4314 ; DMA 1 source address bank = $87
	LDX #$0A ; X = Ah (animated tiles object index)
	LDY #$02 ; Y = 2
-
	LDA $1EF5,x : BEQ ++ ; If [animated tiles object ID] != 0:
	LDA $1F25,x : BPL ++ ; If animated tiles object tiles flagged for transfer:
	STA $4312 ; DMA 1 source address = $87:0000 + [animated tiles object source address]
	; DMA 1 control / target = 16-bit VRAM write (set by $809376)
	LDA $1F31,x : STA $4315 ; DMA 1 size = [animated tiles object size]
	LDA $1F3D,x : STA $2116 ; VRAM write address = [animated tiles object VRAM address]
	; VRAM address increment mode = 16-bit access (set by $809376)
	STY $420B ; Enable DMA 1
	LDA $1F25,x : AND #$7FFF : STA $1F25,x ; Unflag animated tiles object tiles for transfer
++
	DEX : DEX ; X -= 2 (next animated tiles object index)
	BPL - ; If [X] >= 0: loop
+
        RTS

org $80db00
transfer_samus_tiles:
	LDX #$92 : STX $3E ; $3E low = $92
	LDX #$80 : STX $2115 ; VRAM address increment mode = 16-bit access
	LDA #$1801 : STA $4310 ; DMA 1 control / target = 16-bit VRAM data write
	LDX #$02 ; X = 2
	LDA $0721 : BPL ++ ; If Samus bottom half tiles flagged for transfer:
	STA $3C ; $3C = [Samus bottom half tiles definition]
	LDA #$6080 : STA $2116 ; VRAM address = $6080
	LDA [$3C] : STA $4312 ; DMA 1 source address = [[$3C]]
	TXY : LDA [$3C],y : STA $4314
	INY : LDA [$3C],y : STA $4315 ; DMA 1 size = [[$3C] + 3]
	STX $420B ; Enable DMA 1
	INY : INY : LDA [$3C],y : BEQ ++ ; If [[$3C] + 5] != 0:
	STA $4315 ; DMA 1 size = [[$3C] + 5]
	LDA #$6180 : STA $2116 ; VRAM address = $6180
	STX $420B ; Enable DMA 1
++
	LDA $071F : BPL + ; If Samus top half tiles flagged for transfer:
	STA $3C ; $3C = [Samus top half tiles definition]
	LDA #$6000 : STA $2116 ; VRAM address = $6000
	LDA [$3C] : STA $4312 ; DMA 1 source address = [[$3C]]
	TXY : LDA [$3C],y : STA $4314
	INY : LDA [$3C],y : STA $4315 ; DMA 1 size = [[$3C] + 3]
	STX $420B ; Enable DMA 1
	INY : INY : LDA [$3C],y : BEQ + ; If [[$3C] + 5] != 0:
	STA $4315 ; DMA 1 size = [[$3C] + 5]
	LDA #$6100 : STA $2116 ; VRAM address = $6100
	STX $420B ; Enable DMA 1
+
	RTS

ResetStuff:
        STZ $071F : STZ $0721 : RTL ; Samus tiles definitions = 0, clear Samus tiles transfer flags

UnpauseAnimatedTiles:
	LDX #$000A ; X = Ah (animated tiles object index)
-
	LDA $1EF5,x : BEQ + : LDA $1F25,x : BEQ + ; If [animated tiles object ID and src addr] != 0:
	ORA #$8000 : STA $1F25,x ; Flag animated tiles object tiles for transfer
+
	DEX : DEX ; X -= 2 (next animated tiles object index)
	BPL - ; If [X] >= 0: loop
	LDA #$8000 : TSB $1EF1 ; Enable animated tiles objects
	RTL

print "b80 end: ", pc
warnpc $80dbff
