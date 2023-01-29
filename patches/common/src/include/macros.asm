;;; VARIA shared macros

include

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
