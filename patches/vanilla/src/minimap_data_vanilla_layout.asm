lorom
arch 65816

incsrc "sym/map.asm"
incsrc "area_colors.asm"

org map_MinimapTilePaletteTables+0
;;; [5, 6, 7]
palette_triplet_0:
	dw $2000 ; pal 0: 0
	dw $2400 ; pal 1: 1
	dw $2c00 ; pal 2: 3
	dw $2c00 ; pal 3: 3
	dw $3000 ; pal 4: 4
	dw $2800 ; pal 5: 2
	dw $2000 ; pal 6: 0
	dw $3800 ; pal 7: 6
org map_MinimapTilePaletteTables+16
;;; [3, 4, 6]
palette_triplet_1:
	dw $2000 ; pal 0: 0
	dw $2400 ; pal 1: 1
	dw $2c00 ; pal 2: 3
	dw $2800 ; pal 3: 2
	dw $2000 ; pal 4: 0
	dw $3400 ; pal 5: 5
	dw $3800 ; pal 6: 6
	dw $3c00 ; pal 7: 7

warnpc map_MinimapTilePaletteTables_limit

org map_minimap_color_data
;;; ['Brinstar Map Room', '[Green Brinstar Missile Station]', 'Etecoon Super Room', '[Etecoon Save Room]', 'Brinstar Pre-Map Room', 'Green Brinstar Fireflea Room', 'Etecoon Energy Tank Room', '[Green Brinstar Main Shaft Save Room]', 'Green Brinstar Beetom Room', 'Waterway Energy Tank Room', 'Green Brinstar Main Shaft [etecoon room]', '[Dachora Room Energy Charge Station]', 'Early Supers Room', 'Dachora Room', 'Brinstar Reserve Tank Room', '[Spore Spawn Save Room]', 'Pink Brinstar Power Bomb Room', 'Big Pink', 'Spore Spawn Keyhunter Room', 'Pink Brinstar Hopper Room', 'Green Hill Zone', 'Spore Spawn Farming Room', 'Hopper Energy Tank Room', 'Morph Ball Room', 'Spore Spawn Room', 'Spore Spawn Super Room', 'X-Ray Scope Room', 'Red Brinstar Fireflea Room', 'Noob Bridge', 'First Missile Room', 'Blue Brinstar Double Missile Room', 'Construction Zone', 'Blue Brinstar Boulder Room', 'Blue Brinstar Energy Tank Room', '[Red Tower Energy Charge Station]', 'Red Tower', 'Hellway', 'Alpha Power Bomb Room', 'Bat Room', 'Beta Power Bomb Room', 'Below Spazer', 'Caterpillar Room', '[Caterpillar Save Room]', 'Spazer Room']
minimap_room_type_0:
	dw palette_triplet_0
	dw !AreaColor_Crateria
	dw !AreaColor_RedBrinstar
	dw !AreaColor_GreenPinkBrinstar
;;; ['Warehouse Entrance', 'Warehouse Energy Tank Room', 'Warehouse Zeela Room', 'Warehouse Keyhunter Room', 'Baby Kraid Room', '[Kraid Save Room]', 'Kraid Eye Door Room', '[Kraid Recharge Station]', 'Kraid Room', 'Varia Suit Room']
minimap_room_type_1:
	dw palette_triplet_1
	dw !AreaColor_Norfair
	dw !AreaColor_Kraid
	dw !AreaColor_RedBrinstar
;;; ['Crumble Shaft', 'Ice Beam Snake Room', 'Ice Beam Gate Room', 'Crocomire Speedway', 'Grapple Beam Room', 'Ice Beam Tutorial Room', 'Ice Beam Acid Room', 'Grapple Tutorial Room 1', 'Post Crocomire Jump Room', 'Ice Beam Room', 'Grapple Tutorial Room 2', 'Hi Jump Boots Room', 'Grapple Tutorial Room 3', 'Hi Jump Energy Tank Room', 'Norfair Map Room', 'Post Crocomire Power Bomb Room', 'Business Center', 'Post Crocomire Farming Room', 'Post Crocomire Shaft', 'Cathedral Entrance', '[Business Center Save Room]', 'Crocomire Escape', 'Post Crocomire Missile Room', 'Frog Speedway', "Crocomire's Room", '[Post Crocomire Save Room]', 'Cathedral', 'Acid Statue Room', '[Crocomire Save Room]', 'Acid Snakes Tunnel', 'Rising Tide', 'Main Hall', 'Norfair Reserve Tank Room', "Golden Torizo's Room", 'Red Pirate Shaft', 'Green Bubbles Missile Room', 'Upper Norfair Farming Room', '[Crocomire Recharge Room]', '[Elevator Save Room]', 'Screw Attack Room', '[Bubble Mountain Save Room]', 'Spiky Acid Snakes Tunnel', '[Elevator to Lower Norfair]', 'Fast Ripper Room', '[Screw Attack Energy Charge Room]', 'Bubble Mountain', 'Purple Shaft', 'Lava Dive Room', 'Ridley Tank Room', 'Purple Farming Room', 'Magdollite Tunnel', "Ridley's Room", 'Bat Cave', 'Single Chamber', 'Lower Norfair Farming Room', 'Speed Booster Hall', 'Double Chamber', 'Spiky Platforms Tunnel', 'Fast Pillars Setup Room', 'Kronic Boost Room', 'Mickey Mouse Room', 'Pillar Room', 'Volcano Room', 'Plowerhouse Room', 'Wave Beam Room', "Three Muskateers' Room", 'The Worst Room In The Game', 'Metal Pirates Room', 'Amphitheatre', 'Wasteland', 'Lower Norfair Spring Ball Maze Room', 'Lower Norfair Fireflea Room', 'Red Keyhunter Shaft', '[Red Keyhunter Shaft Save Room]', 'Speed Booster Room', 'Lower Norfair Escape Power Bomb Room']
minimap_room_type_2:
	dw palette_triplet_0
	dw !AreaColor_Crocomire
	dw !AreaColor_LowerNorfair
	dw !AreaColor_Norfair
;;; ['Main Street', 'West Tunnel', 'Glass Tunnel', 'Watering Hole', 'Red Fish Room', 'Mt. Everest', 'Crab Tunnel', 'East Tunnel', '[Glass Tunnel Save Room]', 'Fish Tank', 'Northwest Maridia Bug Room', 'Crab Hole', 'Mama Turtle Room', '[Tunnel to West Sand Hall]', 'Maridia Map Room', 'Pseudo Plasma Spark Room', 'Crab Shaft', 'West Sand Hall', '[Aqueduct Save Room]', 'Botwoon Hallway', 'Aqueduct', 'West Sand Hole', '[West Sand Fall]', 'Plasma Spark Room', '[Vertical Tube]', 'Oasis', '[East Sand Fall]', 'East Sand Hole', 'East Sand Hall', "Botwoon's Room", 'Plasma Climb', 'Plasma Tutorial Room', 'Bug Sand Hole', '[Bug Sand Fall]', 'Butterfly Room', 'Botwoon Energy Tank Room', 'Below Botwoon Energy Tank', 'Pants Room', 'Plasma Room', 'Thread The Needle Room', 'Cactus Alley [West]', '[Pants Room West half]', 'Cactus Alley [East]', '[Botwoon Sand Fall]', 'Shaktool Room', 'Spring Ball Room', 'Halfie Climb Room', 'Maridia Elevator Room', 'Colosseum', '[Maridia Elevator Save Room]', '[Halfie Climb Missile Station]', 'Space Jump Room', "Draygon's Room", '[Colosseum Save Room]', 'The Precious Room', '[Colosseum Energy Charge Room]']
minimap_room_type_3:
	dw palette_triplet_0
	dw !AreaColor_EastMaridia
	dw !AreaColor_WestMaridia
	dw !AreaColor_RedBrinstar
;;; ['[Elevator to Green Brinstar]', 'Lower Mushrooms', 'Green Pirates Shaft', 'Gauntlet Energy Tank Room', 'Terminator Room', 'Statues Hallway', 'The Final Missile', 'Final Missile Bombway', 'Statues Room', 'Gauntlet Entrance', 'Parlor and Alcatraz', '[Parlor Save Room]', 'Climb', 'Pre-Map Flyway', 'Pit Room [Old Mother Brain Room]', 'Crateria Super Room', 'Flyway', 'Landing Site', 'Crateria Map Room', '[Elevator to Blue Brinstar]', 'Bomb Torizo Room', 'Crateria Power Bomb Room', 'Crateria Tube', 'Crateria Keyhunter Room', '[Elevator to Red Brinstar]', 'The Moat', 'West Ocean', 'Bowling Alley Path', '[West Ocean Geemer Corridor]', 'East Ocean', '[Crab Maze to Elevator]', '[Elevator to Maridia]', 'Crab Maze', 'Forgotten Highway Kago Room']
minimap_room_type_4:
	dw palette_triplet_0
	dw !AreaColor_Tourian
	dw !AreaColor_WreckedShip
	dw !AreaColor_Crateria
;;; ['Bowling Alley', 'Gravity Suit Room', 'Attic', 'Wrecked Ship Entrance', 'Wrecked Ship Main Shaft', 'Wrecked Ship Map Room', 'Basement', 'Wrecked Ship West Super Room', '[Wrecked Ship Save Room]', 'Sponge Bath', 'Wrecked Ship Energy Tank Room', 'Wrecked Ship East Super Room', 'Wrecked Ship East Missile Room', 'Spiky Death Room', "Phantoon's Room", 'Electric Death Room']
minimap_room_type_5:
	dw palette_triplet_0
	dw !vanilla_etank_color
	dw !vanilla_etank_color
	dw !AreaColor_WreckedShip
;;; ['Tourian Recharge Room', 'Tourian Escape Room 1', 'Tourian Escape Room 2', 'Seaweed Room', 'Tourian Escape Room 3', 'Metroid Room 2', 'Big Boy Room', 'Tourian Eye Door Room', 'Mother Brain Room', 'Metroid Room 1', 'Metroid Room 3', '[Mother Brain Save Room]', 'Dust Torizo Room', 'Rinka Shaft', 'Tourian Escape Room 4', 'Blue Hopper Room', 'Tourian First Room', 'Metroid Room 4', '[Tourian First Save Room]']
minimap_room_type_6:
	dw palette_triplet_0
	dw !vanilla_etank_color
	dw !vanilla_etank_color
	dw !AreaColor_Tourian
;;; ['[Ceres Elevator Room]', '[Ceres Jump Tutorial Room]', '[Ceres Staircase Room]', '[Ceres Dead Scientists Room]', '[Ceres Last Corridor]', '[Ceres Ridley Room]']
minimap_room_type_7:
	dw palette_triplet_1
	dw !AreaColor_Ceres
	dw !vanilla_etank_color
	dw !vanilla_etank_color

warnpc map_minimap_color_data_limit
