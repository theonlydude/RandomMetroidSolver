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
!_tile_offset #= 2*(<y>*$20+<x>)
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
