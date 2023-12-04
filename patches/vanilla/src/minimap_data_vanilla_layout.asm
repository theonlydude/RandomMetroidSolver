lorom
arch 65816

incsrc "sym/map.asm"
incsrc "area_colors.asm"

org map_MinimapTilePaletteTables+0
palette_triplet_0:
	dw $2000
	dw $2400
	dw $2800
	dw $2c00
	dw $3000
	dw $2800
	dw $2000
	dw $3800
org map_MinimapTilePaletteTables+16
palette_triplet_1:
	dw $2000
	dw $2400
	dw $2800
	dw $2800
	dw $2000
	dw $3400
	dw $3800
	dw $3800
org map_MinimapTilePaletteTables+32
palette_triplet_2:
	dw $2000
	dw $2400
	dw $2800
	dw $2800
	dw $3000
	dw $2000
	dw $3800
	dw $3800
org map_MinimapTilePaletteTables+48
palette_triplet_3:
	dw $2000
	dw $2400
	dw $2800
	dw $2c00
	dw $2800
	dw $3400
	dw $2000
	dw $3c00

warnpc map_MinimapTilePaletteTables_limit

org map_minimap_color_data
minimap_room_type_0:
	dw palette_triplet_0
	dw !AreaColor_GreenPinkBrinstar
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_1:
	dw palette_triplet_0
	dw !AreaColor_Crateria
	dw !AreaColor_GreenPinkBrinstar
	dw !vanilla_etank_color
minimap_room_type_2:
	dw palette_triplet_0
	dw !AreaColor_RedBrinstar
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_3:
	dw palette_triplet_0
	dw !AreaColor_GreenPinkBrinstar
	dw !AreaColor_RedBrinstar
	dw !vanilla_etank_color
minimap_room_type_4:
	dw palette_triplet_0
	dw !AreaColor_Crateria
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_5:
	dw palette_triplet_0
	dw !AreaColor_Crateria
	dw !AreaColor_RedBrinstar
	dw !vanilla_etank_color
minimap_room_type_6:
	dw palette_triplet_0
	dw !AreaColor_Crateria
	dw !AreaColor_GreenPinkBrinstar
	dw !AreaColor_RedBrinstar
minimap_room_type_7:
	dw palette_triplet_1
	dw !AreaColor_Kraid
	dw !AreaColor_Norfair
	dw !vanilla_etank_color
minimap_room_type_8:
	dw palette_triplet_1
	dw !AreaColor_Kraid
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_9:
	dw palette_triplet_0
	dw !AreaColor_Norfair
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_10:
	dw palette_triplet_0
	dw !AreaColor_Crocomire
	dw !AreaColor_Norfair
	dw !vanilla_etank_color
minimap_room_type_11:
	dw palette_triplet_0
	dw !AreaColor_Crocomire
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_12:
	dw palette_triplet_0
	dw !AreaColor_Crocomire
	dw !AreaColor_LowerNorfair
	dw !vanilla_etank_color
minimap_room_type_13:
	dw palette_triplet_0
	dw !AreaColor_Crocomire
	dw !AreaColor_LowerNorfair
	dw !AreaColor_Norfair
minimap_room_type_14:
	dw palette_triplet_0
	dw !AreaColor_LowerNorfair
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_15:
	dw palette_triplet_0
	dw !AreaColor_LowerNorfair
	dw !AreaColor_Norfair
	dw !vanilla_etank_color
minimap_room_type_16:
	dw palette_triplet_0
	dw !AreaColor_RedBrinstar
	dw !AreaColor_WestMaridia
	dw !vanilla_etank_color
minimap_room_type_17:
	dw palette_triplet_0
	dw !AreaColor_WestMaridia
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_18:
	dw palette_triplet_0
	dw !AreaColor_EastMaridia
	dw !AreaColor_WestMaridia
	dw !vanilla_etank_color
minimap_room_type_19:
	dw palette_triplet_0
	dw !AreaColor_EastMaridia
	dw !AreaColor_RedBrinstar
	dw !AreaColor_WestMaridia
minimap_room_type_20:
	dw palette_triplet_0
	dw !AreaColor_EastMaridia
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_21:
	dw palette_triplet_1
	dw !AreaColor_Crateria
	dw !AreaColor_GreenPinkBrinstar
	dw !vanilla_etank_color
minimap_room_type_22:
	dw palette_triplet_2
	dw !AreaColor_Crateria
	dw !AreaColor_GreenPinkBrinstar
	dw !AreaColor_Tourian
minimap_room_type_23:
	dw palette_triplet_0
	dw !AreaColor_Crateria
	dw !AreaColor_Tourian
	dw !vanilla_etank_color
minimap_room_type_24:
	dw palette_triplet_0
	dw !AreaColor_Crateria
	dw !AreaColor_WreckedShip
	dw !vanilla_etank_color
minimap_room_type_25:
	dw palette_triplet_0
	dw !AreaColor_WreckedShip
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_26:
	dw palette_triplet_3
	dw !AreaColor_EastMaridia
	dw !AreaColor_WreckedShip
	dw !vanilla_etank_color
minimap_room_type_27:
	dw palette_triplet_0
	dw !AreaColor_Tourian
	dw !vanilla_etank_color
	dw !vanilla_etank_color
minimap_room_type_28:
	dw palette_triplet_1
	dw !AreaColor_Ceres
	dw !vanilla_etank_color
	dw !vanilla_etank_color

warnpc map_minimap_color_data_limit
