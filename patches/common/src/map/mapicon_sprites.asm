include

door_red_Left:
	    dw $01ff : db $ff : dw $2acb
door_green_Left:
	    dw $01ff : db $ff : dw $2acc
door_yellow_Left:
	    dw $01ff : db $ff : dw $2acd
door_grey_Left:
	    dw $01ff : db $ff : dw $2ace
door_wave_Left:
	    dw $01ff : db $ff : dw $2acf
door_plasma_Left:
	    dw $01ff : db $ff : dw $2ad0
door_spazer_Left:
	    dw $01ff : db $ff : dw $2ad1
door_ice_Left:
	    dw $01ff : db $ff : dw $2ad2
door_red_Bottom:
	    dw $0000 : db $01 : dw $2ad3
door_green_Bottom:
	    dw $0000 : db $01 : dw $2ad4
door_yellow_Bottom:
	    dw $0000 : db $01 : dw $2ad5
door_grey_Bottom:
	    dw $0000 : db $01 : dw $2ad6
door_wave_Bottom:
	    dw $0000 : db $01 : dw $2ad7
door_plasma_Bottom:
	    dw $0000 : db $01 : dw $2ad8
door_spazer_Bottom:
	    dw $0000 : db $01 : dw $2ad9
door_ice_Bottom:
	    dw $0000 : db $01 : dw $2ada
door_red_Right:
	    dw $0001 : db $ff : dw $6acb
door_green_Right:
	    dw $0001 : db $ff : dw $6acc
door_yellow_Right:
	    dw $0001 : db $ff : dw $6acd
door_grey_Right:
	    dw $0001 : db $ff : dw $6ace
door_wave_Right:
	    dw $0001 : db $ff : dw $6acf
door_plasma_Right:
	    dw $0001 : db $ff : dw $6ad0
door_spazer_Right:
	    dw $0001 : db $ff : dw $6ad1
door_ice_Right:
	    dw $0001 : db $ff : dw $6ad2
door_red_Top:
	    dw $0000 : db $ff : dw $aad3
door_green_Top:
	    dw $0000 : db $ff : dw $aad4
door_yellow_Top:
	    dw $0000 : db $ff : dw $aad5
door_grey_Top:
	    dw $0000 : db $ff : dw $aad6
door_wave_Top:
	    dw $0000 : db $ff : dw $aad7
door_plasma_Top:
	    dw $0000 : db $ff : dw $aad8
door_spazer_Top:
	    dw $0000 : db $ff : dw $aad9
door_ice_Top:
	    dw $0000 : db $ff : dw $aada

doors_mapicons_sprite_table:
	dw door_red_Left,door_green_Left,door_yellow_Left,door_grey_Left,door_wave_Left,door_plasma_Left,door_spazer_Left,door_ice_Left,door_red_Bottom,door_green_Bottom,door_yellow_Bottom,door_grey_Bottom,door_wave_Bottom,door_plasma_Bottom,door_spazer_Bottom,door_ice_Bottom,door_red_Right,door_green_Right,door_yellow_Right,door_grey_Right,door_wave_Right,door_plasma_Right,door_spazer_Right,door_ice_Right,door_red_Top,door_green_Top,door_yellow_Top,door_grey_Top,door_wave_Top,door_plasma_Top,door_spazer_Top,door_ice_Top

portal_Crateria:
	    dw $0000 : db $ff : dw $28db
portal_GreenPinkBrinstar:
	    dw $0000 : db $ff : dw $28dc
portal_RedBrinstar:
	    dw $0000 : db $ff : dw $28dd
portal_WreckedShip:
	    dw $0000 : db $ff : dw $28de
portal_Kraid:
	    dw $0000 : db $ff : dw $28df
portal_Norfair:
	    dw $0000 : db $ff : dw $28e0
portal_Crocomire:
	    dw $0000 : db $ff : dw $28e1
portal_LowerNorfair:
	    dw $0000 : db $ff : dw $28e2
portal_WestMaridia:
	    dw $0000 : db $ff : dw $28e3
portal_EastMaridia:
	    dw $0000 : db $ff : dw $28e4
portal_Tourian:
	    dw $0000 : db $ff : dw $28e5
portal_KraidBoss:
	    dw $0000 : db $ff : dw $28f8
portal_PhantoonBoss:
	    dw $0000 : db $ff : dw $28f9
portal_DraygonBoss:
	    dw $0000 : db $ff : dw $28fa
portal_RidleyBoss:
	    dw $0000 : db $ff : dw $28fb

portals_mapicons_sprite_table:
	dw portal_Crateria,portal_GreenPinkBrinstar,portal_RedBrinstar,portal_WreckedShip,portal_Kraid,portal_Norfair,portal_Crocomire,portal_LowerNorfair,portal_WestMaridia,portal_EastMaridia,portal_Tourian,portal_KraidBoss,portal_PhantoonBoss,portal_DraygonBoss,portal_RidleyBoss

objective_1:
	    dw $0001 : db $ff : dw $2ee6
objective_2:
	    dw $0001 : db $ff : dw $2ee7
objective_3:
	    dw $0001 : db $ff : dw $2ee8
objective_4:
	    dw $0001 : db $ff : dw $2ee9
objective_5:
	    dw $0001 : db $ff : dw $2eea
objective_6:
	    dw $0001 : db $ff : dw $2eeb
objective_7:
	    dw $0001 : db $ff : dw $2eec
objective_8:
	    dw $0001 : db $ff : dw $2eed
objective_9:
	    dw $0001 : db $ff : dw $2eee
objective_10:
	    dw $0001 : db $ff : dw $2eef
objective_11:
	    dw $0001 : db $ff : dw $2ef0
objective_12:
	    dw $0001 : db $ff : dw $2ef1
objective_13:
	    dw $0001 : db $ff : dw $2ef2
objective_14:
	    dw $0001 : db $ff : dw $2ef3
objective_15:
	    dw $0001 : db $ff : dw $2ef4
objective_16:
	    dw $0001 : db $ff : dw $2ef5
objective_17:
	    dw $0001 : db $ff : dw $2ef6
objective_18:
	    dw $0001 : db $ff : dw $2ef7

objectives_mapicons_sprite_table:
	dw objective_1,objective_2,objective_3,objective_4,objective_5,objective_6,objective_7,objective_8,objective_9,objective_10,objective_11,objective_12,objective_13,objective_14,objective_15,objective_16,objective_17,objective_18

