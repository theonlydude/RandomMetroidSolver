;;; Common routines used by other patches
;;; 
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

!RNG		= $808111	; RNG function
!RNG_seed	= $05e5
!RTA_timer	= $05b8		; see tracking.asm


org $a1f2a0
;;; single use (will give the same result if called several times in the same frame)
;;; random function that leaves game rng untouched
;;; result in A
rand:
    phy
    lda !RNG_seed : pha             ; save current rand seed
    eor !RTA_timer : sta !RNG_seed  ; alter seed with frame counter
    jsl !RNG : tay                  ; call RNG and save result to Y
    pla : sta !RNG_seed             ; restore current rand seed
    tya                             ; get RNG result in A
    ply
    rtl

;;; courtesy of Smiley
fix_timer_gfx:
    PHX
    LDX $0330						;get index for the table
    LDA #$0400 : STA $D0,x  				;Size
    INX : INX						;inc X for next entry (twice because 2 bytes)
    LDA #$C000 : STA $D0,x					;source address
    INX : INX						;inc again
    SEP #$20 : LDA #$B0 : STA $D0,x : REP #$20  		;Source bank $B0
    INX							;inc once, because the bank is stored in one byte only
    ;; VRAM destination (in word addresses, basically take the byte
    ;; address from the RAM map and and devide them by 2)
    LDA #$7E00	: STA $D0,x
    INX : INX : STX $0330 					;storing index
    PLX
    RTL							;done. return

;; 32-bit by 16-bit division routine total found somewhere
;; ($14$16)/$12 : result in $16, remainder in $14
div32:
    phy
    phx
    php
    rep #$30
    sep #$10
    sec
    lda $14
    sbc $12
    bcs .uoflo
    ldx #$11
    rep #$10
.ushftl:
    rol $16
    dex
    beq .umend
    rol $14
    lda #$0000
    rol
    sta $18
    sec
    lda $14
    sbc $12
    tay
    lda $18
    sbc #$0000
    bcc .ushftl
    sty $14
    bra .ushftl
.uoflo:
    lda #$ffff
    sta $16
    sta $14
.umend:
    plp
    plx
    ply
    rtl
