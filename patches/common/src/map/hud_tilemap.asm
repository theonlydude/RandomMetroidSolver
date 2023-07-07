
include

%BGtile($1E, 3, 1, 1, 0)
!vert_bar_left #= !_tile
%BGtile($1E, 3, 1, 0, 0)
!vert_bar_right #= !_tile
%BGtile($1D, 3, 1, 0, 0)
!horiz_bar_bottom #= !_tile
%BGtile($1C, 3, 1, 1, 0)
!corner_top_left #= !_tile
%BGtile($1C, 3, 1, 0, 0)
!corner_top_right #= !_tile

org $80988b
	dw $2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,!horiz_bar_bottom,!horiz_bar_bottom,!horiz_bar_bottom,!horiz_bar_bottom,!horiz_bar_bottom,!corner_top_right
org $8098cb
	dw $2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$005b,$005c,$005d,$005e,$005f,!vert_bar_right
org $80990b
	dw $2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$006b,$006c,$006d,$006e,$006f,!vert_bar_right
org $80994b
	dw $2c0f,$2c0b,$2c0c,$2c0d,$2c32,$2c0f,$2c09,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$2c0f,$007b,$007c,$007d,$007e,$007f,!vert_bar_right
