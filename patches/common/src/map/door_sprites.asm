include

red_Left:
	    dw $01ff : db $ff : dw $2ad0
green_Left:
	    dw $01ff : db $ff : dw $2ad1
yellow_Left:
	    dw $01ff : db $ff : dw $2ad2
grey_Left:
	    dw $01ff : db $ff : dw $2ad3
wave_Left:
	    dw $01ff : db $ff : dw $2ad4
plasma_Left:
	    dw $01ff : db $ff : dw $2ad5
spazer_Left:
	    dw $01ff : db $ff : dw $2ad6
ice_Left:
	    dw $01ff : db $ff : dw $2ad7
red_Top:
	    dw $0000 : db $01 : dw $2ad8
green_Top:
	    dw $0000 : db $01 : dw $2ad9
yellow_Top:
	    dw $0000 : db $01 : dw $2ada
grey_Top:
	    dw $0000 : db $01 : dw $2adb
wave_Top:
	    dw $0000 : db $01 : dw $2adc
plasma_Top:
	    dw $0000 : db $01 : dw $2add
spazer_Top:
	    dw $0000 : db $01 : dw $2ade
ice_Top:
	    dw $0000 : db $01 : dw $2adf
red_Right:
	    dw $0001 : db $ff : dw $6ad0
green_Right:
	    dw $0001 : db $ff : dw $6ad1
yellow_Right:
	    dw $0001 : db $ff : dw $6ad2
grey_Right:
	    dw $0001 : db $ff : dw $6ad3
wave_Right:
	    dw $0001 : db $ff : dw $6ad4
plasma_Right:
	    dw $0001 : db $ff : dw $6ad5
spazer_Right:
	    dw $0001 : db $ff : dw $6ad6
ice_Right:
	    dw $0001 : db $ff : dw $6ad7
red_Bottom:
	    dw $0000 : db $ff : dw $aad8
green_Bottom:
	    dw $0000 : db $ff : dw $aad9
yellow_Bottom:
	    dw $0000 : db $ff : dw $aada
grey_Bottom:
	    dw $0000 : db $ff : dw $aadb
wave_Bottom:
	    dw $0000 : db $ff : dw $aadc
plasma_Bottom:
	    dw $0000 : db $ff : dw $aadd
spazer_Bottom:
	    dw $0000 : db $ff : dw $aade
ice_Bottom:
	    dw $0000 : db $ff : dw $aadf

doors_mapicons_sprite_table:
	dw red_Left,green_Left,yellow_Left,grey_Left,wave_Left,plasma_Left,spazer_Left,ice_Left,red_Top,green_Top,yellow_Top,grey_Top,wave_Top,plasma_Top,spazer_Top,ice_Top,red_Right,green_Right,yellow_Right,grey_Right,wave_Right,plasma_Right,spazer_Right,ice_Right,red_Bottom,green_Bottom,yellow_Bottom,grey_Bottom,wave_Bottom,plasma_Bottom,spazer_Bottom,ice_Bottom
