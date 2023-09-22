;;; VARIA shared macros

include

math pri on

;;; used to export labels towards the python side :
;;; %export(my_label)
;;;     <code...>
macro export(label)
export__<label>:
<label>:
endmacro

macro a8()
        sep #$20
endmacro

macro a16()
	rep #$20
endmacro

macro i8()
	rep #$10
endmacro

macro ai8()
	sep #$30
endmacro

macro ai16()
	rep #$30
endmacro

macro i16()
	rep #$10
endmacro

;;; compute absolute tile offset from coords
function tileOffset(x, y) = 2*((y*$20)+x)

;; BG tile format
;; vhopppcc cccccccc
;; v/h        = Vertical/Horizontal flip this tile.
;; o          = Tile priority.
;; ppp        = Tile palette. The number of entries in the palette depends on the Mode and the BG.
;; cccccccccc = Tile number.
function BGtile(index, palette, prio, hflip, vflip) = (index&$3FF)|((palette&$7)<<10)|((prio&$1)<<13)|((hflip&$1)<<14)|((vflip&$1)<<15)

;; an oam entry is made of five bytes: (s000000 x xxxxxxxx) (yyyyyyyy) (YXppPPPt tttttttt)
;;  s = size bit
;;      0: 8x8
;;      1: 16x16
;;  x = X offset of sprite from centre
;;  y = Y offset of sprite from centre
;;  Y = Y flip
;;  X = X flip
;;  p = priority (relative to background)
;;  t = tile number
macro sprite(index, x, y, hflip, vflip, prio, large)
        dw (<large><<15)|(<x>&$1ff) : db <y>
        dw (<vflip><<15)|(<hflip><<14)|(<prio><<13)|<index>
endmacro

;;; simple helper to instant DMA gfx from a static long source address to VRAM
;;; usable during blank screen only
macro gfxDMA(src, dstVRAM, size)
        php
        %ai8()
        lda.b #(<dstVRAM>&$ff) : sta $2116  ;| VRAM Address Registers (Low)
        lda.b #(<dstVRAM>>>8) : sta $2117   ;| VRAM Address Registers (High)
        LDA.b #$80 : STA $2115    ;} Video Port Control Register - Set VRAM transfer mode to word-access, increment by 1.
                                  ;    0x80 == 0b10000000 => i---ffrr => i=1 (increment when $2119 is accessed),
                                  ;    ff=0 (full graphic ??), rr=0 (increment by 2 bytes)
        JSL $8091A9 ; Set up a DMA transfer
        db $01,$01          ; hard-coded channel 1, options = $01
        db $18              ; DMA target = VRAM
        dl <src>
        dw <size>
        LDA.b #$02 : STA $420B   ; start transfer
        plp
endmacro

;;; helper to DMA load from static long address (*not RAM*) to static long address (RAM)
macro loadRamDMA(src, dstRAMl, size)
        php
        %ai8()
        ;; write RAM address to proper registers
        LDA.b #(<dstRAMl>&$ff) : STA $2181
        LDA.b #((<dstRAMl>&$ff00)>>8) : STA $2182
        LDA.b #(<dstRAMl>>>16) : STA $2183
        ;; set up DMA transfer
        JSL $8091A9
        db $01,$00          ; hard-coded channel 1, options = $00
        db $80              ; DMA target = WRAM
        dl <src>
        dw <size>
        LDA #$02 : STA $420B   ; start transfer
        plp
endmacro

;;; simple helper to queue DMA gfx from a static long source address to VRAM
;;; usable at any time, uses X
macro queueGfxDMA(src, dstVRAM, size)
        LDX $0330
        LDA.w #<size> : STA.b $D0,x
        INX : INX
        LDA.W #(<src>&$ffff) : STA.b $D0,x
        INX : INX
        %a8()
        LDA.b #(<src>>>16) : STA.b $D0,x
        %a16()
        INX
        LDA.w #<dstVRAM> : STA.b $D0,x
        INX : INX
        STX $0330
endmacro
