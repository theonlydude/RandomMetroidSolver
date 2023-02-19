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
