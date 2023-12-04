lorom
arch 65816

;;; [Crab Maze to Elevator]
org $8f95c5
	db $04, $17
;;; [Elevator to Maridia]
org $8f94e9
	db $04, $17
;;; [Elevator to Red Brinstar]
org $8f9647
	db $01, $19
;;; [Elevator to Green Brinstar]
org $8f9955
	db $01, $19
;;; Statues Hallway
org $8fa60a
	db $01, $1a
;;; Statues Room
org $8fa687
	db $01, $1a
;;; Warehouse Entrance
org $8fa6be
	db $03, $01
;;; Lava Dive Room
org $8faf31
	db $06, $0b
;;; [Elevator to Lower Norfair]
org $8faf5c
	db $06, $0c
;;; [Elevator Save Room]
org $8fb1d8
	db $06, $0c
