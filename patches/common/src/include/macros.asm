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
;;; result in !_tile_offset
macro tileOffset(x, y)
!_tile_offset #= 2*((<y>*$20)+<x>)
endmacro

;;; ldx the result of %tileOffset
macro ldx_tileOffset(x, y)
%tileOffset(<x>, <y>)
        ldx.w #!_tile_offset
endmacro

;; BG tile format
;; vhopppcc cccccccc
;; v/h        = Vertical/Horizontal flip this tile.
;; o          = Tile priority.
;; ppp        = Tile palette. The number of entries in the palette depends on the Mode and the BG.
;; cccccccccc = Tile number.
macro BGtile(index, palette, prio, hflip, vflip)
!_tile #= (<index>&$3FF)|((<palette>&$7)<<10)|((<prio>&$1)<<13)|((<hflip>&$1)<<14)|((<vflip>&$1)<<15)
endmacro

macro dw_BGtile(index, palette, prio, hflip, vflip)
%BGtile(<index>, <palette>, <prio>, <hflip>, <vflip>)
        dw !_tile
endmacro

;;; simple helper to instant DMA gfx from a static source address to VRAM
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
