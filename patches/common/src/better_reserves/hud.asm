include

;;; Full Reserve Tank HUD Indicator By NoDever2 (https://metroidconstruction.com/resource.php?id=418)

;This code adds a new feature to the game where when reserve tanks are full on auto mode, the HUD icon
;turns pink (or more accurately, to the same color as full etanks).

;Warning, the Auto Reserve and Empty Auto Reserve tilemaps at $80998B are now unused and replaced with some custom code.
;The Empty Auto Reserve one has also been repointed (See "Data").

;Thanks to PJBoy's bank logs as always. Also tilemap format is as follows:
;tilemap format is yxpPPPtttttttttt
;where PPP are the palette bits

;;; VARIA edits: we can't use pink because of minimap palette modifications,
;;; add specific tiles and use modified palette 7 (also used for new etank tile)

org $809B4E
; First things first, check if reserves are Full, Empty, or neither.
; The way this works is that we are storing a value in $14 with palette bits set that will later be XOR'ed with the reserve tilemap
; tiles loaded from ROM. We are doing this to manipulate the tiles' palette bits on load.
	LDA $09C0 : CMP.w #1         ; keep vanilla code here to stay compatible with multitroid hijack
        BNE BRANCH_NOT_AUTO_RESERVES
HandleAutoReserveTilemap:
	LDA $09D6 : BNE .NotEmpty
	stz $14 : BRA + ; Reserves are empty, display blue icon (don't modify any bits)

.NotEmpty:
	CMP $09D4 : BEQ .Full
	LDA #$1000 : sta $14 : BRA + ; Reserves are not empty nor full, display yellow icon.

.Full:
        lda #$2000 : sta $14    ; use special value to load full tiles and not modify palette (VARIA)
+       tdc : TAY : TAX
.write:
	JSL WriteTilemap
	BRA BRANCH_NOT_AUTO_RESERVES

full_tiles:
.top:
        dw BGtile($ca, 7, 1, 0, 0)
        dw BGtile($d9, 7, 1, 0, 0)
.bottom:
        dw BGtile($da, 7, 1, 0, 0)
        dw BGtile($db, 7, 1, 0, 0)
        dw BGtile($ca, 7, 1, 0, 1)
        dw BGtile($d9, 7, 1, 0, 1)

;print "main routine overwrite end: ", pc, " (vanilla code resumes at $809B8B)" ; DEBUG
warnpc $809B8B

org $809B8B ; vanilla branch destination
BRANCH_NOT_AUTO_RESERVES:	

org $81fb80

macro nextRowX()
        TXA : CLC : ADC #$003C : TAX
endmacro

WriteTilemap:
        lda $14 : cmp #$2000 : bne .not_full
        ;; full special case
        stz $14
        lda #full_tiles : sta $16
        bra +
.not_full:
        lda #not_full_tiles : sta $16
+
;print "freespace usage start: ", pc ; DEBUG
	; Y is index into reserve tilemap in ROM to transfer
	; X is index into reserve tilemap destination in RAM
        %hasVARIAhud() : bne .top
        ;; set up half draw: X+=$40, Y+=4
        iny #4
        txa : clc : adc #$0040 : tax
        bra .bottom
.top:
	JSL TransferNextVal					; stores to 7EC618
	JSL TransferNextVal					; stores to 7EC61A
        %nextRowX()
.bottom:
	JSL TransferNextVal					; stores to 7EC658
	JSL TransferNextVal					; stores to 7EC65A
        %nextRowX()
	JSL TransferNextVal					; stores to 7EC698
	JSL TransferNextVal					; stores to 7EC69A
	RTL

warnpc $81fbff
;print "freespace usage end:   ", pc ; DEBUG

org $80998B ; overwrite now-unused vanilla reserve HUD tilemaps
            ; Transfers one word from ROM,y to RAM,x.
            ; This is where the XOR operation happens.
TransferNextVal: ; Also increments X and Y
	LDA ($16),y : eor $14
.store:
        STA $7EC618,x
	INY : INY : INX : INX : RTL

not_full_tiles:
.top:
	DW $2C33, $2C46
.bottom:
	DW $2C47, $2C48
	DW $AC33, $AC46

;print "auto reserve tilemap overwrite end: ", pc, " (vanilla data resumes at $8099A3)" ; DEBUG
warnpc $8099A4
