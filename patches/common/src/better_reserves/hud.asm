include

;;; Full Reserve Tank HUD Indicator By NoDever2 (https://metroidconstruction.com/resource.php?id=418)
;;; 
;;; * VARIA notes:
;;; Used compatibility version, with code commented out/modified for VARIA HUD compatibilty.
;;; Modifications for full HUD in better_reserves_full_hud patch.

;This code adds a new feature to the game where when reserve tanks are full on auto mode, the HUD icon
;turns pink (or more accurately, to the same color as full etanks).

;Warning, the Auto Reserve and Empty Auto Reserve tilemaps at $80998B are now unused and replaced with some custom code.
;The Empty Auto Reserve one has also been repointed (See "Data").

;Thanks to PJBoy's bank logs as always. Also tilemap format is as follows:
;tilemap format is yxpPPPtttttttttt
;where PPP are the palette bits

org $809B4E
	LDA $09C0 : DEC : BNE BRANCH_NOT_AUTO_RESERVES ;small optimization of vanilla code
HandleAutoReserveTilemap:
; First things first, check if reserves are Full, Empty, or neither.
; The way this works is that we are storing a value in $14 with palette bits set that will later be XOR'ed with the reserve tilemap
; tiles loaded from ROM. We are doing this to manipulate the tiles' palette bits on load.

	LDA $09D6 : BNE .NotEmpty
	LDA #$0000 : BRA + ; Reserves are empty, display blue icon (don't modify any bits)
	
.NotEmpty
	CMP $09D4 : BEQ .Full
	LDA #$1000 : BRA + ; Reserves are not empty nor full, display yellow icon.

.Full
	LDA #$0400 ; Reserves are full, display pink icon.
+	STA $14 : LDA #$0000 : TAY : TAX
.write
	JSL WriteTilemap_half
	BRA BRANCH_NOT_AUTO_RESERVES

; Empty Auto Reserve Tilemap
Data:
	;; DW $2C33, $2C46
	DW $2C47, $2C48
	DW $AC33, $AC46

;print "main routine overwrite end: ", pc, " (vanilla code resumes at $809B8B)" ; DEBUG
warnpc $809B8C

org $809B8B ; vanilla branch destination
BRANCH_NOT_AUTO_RESERVES:	

org $81fad0

WriteTilemap:
;print "freespace usage start: ", pc ; DEBUG
	; Y is index into reserve tilemap in ROM to transfer
	; X is index into reserve tilemap destination in RAM
.full:
	JSL TransferNextVal					; stores to 7EC618
	JSL TransferNextVal					; stores to 7EC61A
	JSL NextRowX
.half:
	JSL TransferNextVal					; stores to 7EC658
	JSL TransferNextVal					; stores to 7EC65A
	JSL NextRowX
	JSL TransferNextVal					; stores to 7EC698
	JSL TransferNextVal					; stores to 7EC69A
	RTL

warnpc $81faff
;print "freespace usage end:   ", pc ; DEBUG

org $80998B ; overwrite now-unused vanilla reserve HUD tilemaps
            ; Transfers one word from ROM,y to RAM,x.
            ; This is where the XOR operation happens.
TransferNextVal: ; Also increments X and Y
	LDA Data,y : EOR $14
.store:
        STA $7EC658,x
	INY : INY : INX : INX : RTL

; Adjust X (register) for writing to next vertical line on HUD
NextRowX:
	TXA : CLC : ADC #$003C : TAX : RTL

;print "auto reserve tilemap overwrite end: ", pc, " (vanilla data resumes at $8099A3)" ; DEBUG
warnpc $8099A4
