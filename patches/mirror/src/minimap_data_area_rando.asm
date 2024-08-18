lorom
arch 65816

incsrc "sym/map.asm"
incsrc "area_colors.asm"

org map_MinimapTilePaletteTables+0
;;; [3, 4, 6]
palette_triplet_0:
	dw $2000 ; pal 0: 0
	dw $2400 ; pal 1: 1
	dw $2c00 ; pal 2: 3
	dw $2800 ; pal 3: 2
	dw $2000 ; pal 4: 0
	dw $3400 ; pal 5: 5
	dw $3800 ; pal 6: 6
	dw $3c00 ; pal 7: 7
org map_MinimapTilePaletteTables+16
;;; [5, 6, 7]
palette_triplet_1:
	dw $2000 ; pal 0: 0
	dw $2400 ; pal 1: 1
	dw $2c00 ; pal 2: 3
	dw $2c00 ; pal 3: 3
	dw $3000 ; pal 4: 4
	dw $2800 ; pal 5: 2
	dw $2000 ; pal 6: 0
	dw $3800 ; pal 7: 6
org map_MinimapTilePaletteTables+32
;;; [3, 5, 7]
palette_triplet_2:
	dw $2000 ; pal 0: 0
	dw $2400 ; pal 1: 1
	dw $2c00 ; pal 2: 3
	dw $2800 ; pal 3: 2
	dw $3000 ; pal 4: 4
	dw $2000 ; pal 5: 0
	dw $3800 ; pal 6: 6
	dw $3800 ; pal 7: 6

warnpc map_MinimapTilePaletteTables_limit

org map_minimap_color_data
;;; ['Varia Suit Room', 'Kraid Room', '[Kraid Recharge Station]', 'Kraid Eye Door Room', 'Baby Kraid Room', '[Kraid Save Room]', 'Warehouse Keyhunter Room', 'Warehouse Zeela Room', 'Warehouse Entrance', 'Warehouse Energy Tank Room', 'Caterpillar Room', '[Caterpillar Save Room]', 'Spazer Room', 'Below Spazer', 'Beta Power Bomb Room', 'Bat Room', 'Red Brinstar Fireflea Room', '[Red Tower Energy Charge Station]', 'X-Ray Scope Room']
minimap_room_type_0:
	dw palette_triplet_0
	dw !AreaColor_Norfair
	dw !AreaColor_Kraid
	dw !AreaColor_RedBrinstar
;;; ['Hellway', 'Alpha Power Bomb Room', 'Red Tower', 'Blue Brinstar Energy Tank Room', 'Noob Bridge', 'Blue Brinstar Boulder Room', 'Blue Brinstar Double Missile Room', 'Construction Zone', 'Morph Ball Room', 'First Missile Room', 'Green Hill Zone', 'Spore Spawn Super Room', 'Spore Spawn Room', 'Spore Spawn Keyhunter Room', 'Spore Spawn Farming Room', 'Hopper Energy Tank Room', 'Pink Brinstar Hopper Room', 'Big Pink', 'Dachora Room', 'Pink Brinstar Power Bomb Room', '[Spore Spawn Save Room]', 'Brinstar Reserve Tank Room', 'Waterway Energy Tank Room', 'Early Supers Room', 'Green Brinstar Main Shaft [etecoon room]', 'Etecoon Energy Tank Room', '[Dachora Room Energy Charge Station]', 'Brinstar Pre-Map Room', '[Green Brinstar Main Shaft Save Room]', 'Green Brinstar Fireflea Room', 'Green Brinstar Beetom Room', 'Brinstar Map Room', '[Green Brinstar Missile Station]', 'Etecoon Super Room', '[Etecoon Save Room]']
minimap_room_type_1:
	dw palette_triplet_1
	dw !AreaColor_Crateria
	dw !AreaColor_RedBrinstar
	dw !AreaColor_GreenPinkBrinstar
;;; ['Speed Booster Room', 'Speed Booster Hall', "Three Muskateers' Room", 'The Worst Room In The Game', 'Single Chamber', 'Wave Beam Room', 'Volcano Room', 'Mickey Mouse Room', 'Double Chamber', 'Spiky Platforms Tunnel', 'Kronic Boost Room', 'Magdollite Tunnel', 'Spiky Acid Snakes Tunnel', 'Lava Dive Room', 'Bat Cave', 'Main Hall', 'Bubble Mountain', 'Purple Farming Room', 'Purple Shaft', 'Green Bubbles Missile Room', '[Bubble Mountain Save Room]', 'Rising Tide', 'Upper Norfair Farming Room', '[Elevator to Lower Norfair]', '[Crocomire Recharge Room]', '[Elevator Save Room]', 'Norfair Reserve Tank Room', 'Frog Speedway', 'Red Pirate Shaft', 'Acid Snakes Tunnel', "Crocomire's Room", 'Acid Statue Room', 'Cathedral', '[Crocomire Save Room]', 'Crocomire Speedway', 'Crocomire Escape', 'Post Crocomire Missile Room', 'Cathedral Entrance', '[Post Crocomire Save Room]', '[Business Center Save Room]', 'Post Crocomire Farming Room', 'Post Crocomire Jump Room', 'Business Center', 'Post Crocomire Shaft', 'Ice Beam Gate Room', 'Norfair Map Room', 'Hi Jump Energy Tank Room', 'Post Crocomire Power Bomb Room', 'Grapple Tutorial Room 3', 'Hi Jump Boots Room', 'Grapple Tutorial Room 2', 'Ice Beam Tutorial Room', 'Ice Beam Room', 'Ice Beam Acid Room', 'Grapple Tutorial Room 1', 'Ice Beam Snake Room', 'Grapple Beam Room', 'Crumble Shaft']
minimap_room_type_2:
	dw palette_triplet_1
	dw !AreaColor_Crocomire
	dw !AreaColor_LowerNorfair
	dw !AreaColor_Norfair
;;; ['Lower Norfair Spring Ball Maze Room', 'Lower Norfair Escape Power Bomb Room', 'Lower Norfair Fireflea Room', 'Red Keyhunter Shaft', 'Wasteland', '[Red Keyhunter Shaft Save Room]', 'Amphitheatre', 'Metal Pirates Room', 'Pillar Room', 'Plowerhouse Room', 'Lower Norfair Farming Room', 'Fast Pillars Setup Room', 'Fast Ripper Room', "Ridley's Room", 'Ridley Tank Room', '[Screw Attack Energy Charge Room]', 'Screw Attack Room', "Golden Torizo's Room"]
minimap_room_type_3:
	dw palette_triplet_0
	dw !vanilla_etank_color
	dw !vanilla_etank_color
	dw !AreaColor_LowerNorfair
;;; ['[Colosseum Energy Charge Room]', 'The Precious Room', '[Colosseum Save Room]', 'Colosseum', "Draygon's Room", '[Halfie Climb Missile Station]', 'Space Jump Room', 'Halfie Climb Room', '[Maridia Elevator Save Room]', 'Maridia Elevator Room', 'Thread The Needle Room', 'Spring Ball Room', 'Cactus Alley [East]', 'Botwoon Energy Tank Room', 'Shaktool Room', '[Botwoon Sand Fall]', 'Below Botwoon Energy Tank', 'Plasma Room', 'Cactus Alley [West]', 'Pants Room', '[Pants Room West half]', 'Plasma Tutorial Room', 'Bug Sand Hole', '[Bug Sand Fall]', 'Butterfly Room', 'Plasma Climb', 'Plasma Spark Room', "Botwoon's Room", 'Aqueduct', 'East Sand Hall', 'West Sand Hall', 'East Sand Hole', 'Botwoon Hallway', '[East Sand Fall]', '[Vertical Tube]', 'Oasis', 'Pseudo Plasma Spark Room', '[West Sand Fall]', 'West Sand Hole', 'Crab Shaft', '[Aqueduct Save Room]', 'Mama Turtle Room', 'Mt. Everest', '[Tunnel to West Sand Hall]', 'Maridia Map Room', 'Fish Tank', 'Crab Hole', 'Crab Tunnel', 'East Tunnel', 'Main Street', '[Glass Tunnel Save Room]', 'Glass Tunnel', 'West Tunnel']
minimap_room_type_4:
	dw palette_triplet_1
	dw !AreaColor_EastMaridia
	dw !AreaColor_WestMaridia
	dw !AreaColor_RedBrinstar
;;; ['Northwest Maridia Bug Room', 'Red Fish Room', 'Watering Hole']
minimap_room_type_5:
	dw palette_triplet_0
	dw !vanilla_etank_color
	dw !vanilla_etank_color
	dw !AreaColor_WestMaridia
;;; ['Forgotten Highway Kago Room', 'Crab Maze', 'East Ocean', '[Crab Maze to Elevator]', '[Elevator to Maridia]', '[West Ocean Geemer Corridor]', 'Bowling Alley Path']
minimap_room_type_6:
	dw palette_triplet_0
	dw !AreaColor_GreenPinkBrinstar
	dw !AreaColor_EastMaridia
	dw !AreaColor_WreckedShip
;;; ['West Ocean', 'The Moat', 'Crateria Power Bomb Room', 'Crateria Tube', 'Landing Site', 'Bomb Torizo Room', 'Flyway', 'Crateria Super Room', 'Crateria Map Room', '[Elevator to Blue Brinstar]', 'Gauntlet Entrance', 'Parlor and Alcatraz', 'Pre-Map Flyway', 'Pit Room [Old Mother Brain Room]', 'Climb', '[Parlor Save Room]', 'Final Missile Bombway', 'Gauntlet Energy Tank Room', 'Terminator Room', 'Statues Room', 'The Final Missile', 'Statues Hallway', 'Green Pirates Shaft']
minimap_room_type_7:
	dw palette_triplet_1
	dw !AreaColor_Tourian
	dw !AreaColor_WreckedShip
	dw !AreaColor_Crateria
;;; ['Crateria Keyhunter Room', '[Elevator to Red Brinstar]']
minimap_room_type_8:
	dw palette_triplet_2
	dw !AreaColor_RedBrinstar
	dw !AreaColor_Tourian
	dw !AreaColor_Crateria
;;; ['Lower Mushrooms', '[Elevator to Green Brinstar]']
minimap_room_type_9:
	dw palette_triplet_2
	dw !AreaColor_GreenPinkBrinstar
	dw !AreaColor_Tourian
	dw !AreaColor_Crateria
;;; ['Wrecked Ship East Missile Room', 'Electric Death Room', 'Wrecked Ship East Super Room', 'Wrecked Ship Energy Tank Room', 'Spiky Death Room', "Phantoon's Room", 'Attic', 'Sponge Bath', 'Basement', '[Wrecked Ship Save Room]', 'Wrecked Ship Main Shaft', 'Bowling Alley', 'Wrecked Ship Entrance', 'Wrecked Ship West Super Room', 'Wrecked Ship Map Room', 'Gravity Suit Room']
minimap_room_type_10:
	dw palette_triplet_1
	dw !vanilla_etank_color
	dw !vanilla_etank_color
	dw !AreaColor_WreckedShip
;;; ['[Tourian First Save Room]', 'Tourian First Room', 'Metroid Room 4', 'Blue Hopper Room', 'Tourian Escape Room 4', 'Metroid Room 1', 'Metroid Room 3', 'Dust Torizo Room', 'Rinka Shaft', 'Tourian Escape Room 3', 'Big Boy Room', 'Tourian Eye Door Room', '[Mother Brain Save Room]', 'Mother Brain Room', 'Metroid Room 2', 'Seaweed Room', 'Tourian Escape Room 1', 'Tourian Recharge Room', 'Tourian Escape Room 2']
minimap_room_type_11:
	dw palette_triplet_1
	dw !vanilla_etank_color
	dw !vanilla_etank_color
	dw !AreaColor_Tourian
;;; ['[Ceres Ridley Room]', '[Ceres Last Corridor]', '[Ceres Dead Scientists Room]', '[Ceres Staircase Room]', '[Ceres Jump Tutorial Room]', '[Ceres Elevator Room]']
minimap_room_type_12:
	dw palette_triplet_0
	dw !AreaColor_Ceres
	dw !vanilla_etank_color
	dw !vanilla_etank_color

warnpc map_minimap_color_data_limit
