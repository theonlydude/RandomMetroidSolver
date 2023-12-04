lorom
arch 65816

;;; [Crab Maze to Elevator]
org $8f95c5
	db $04, $1a
;;; [Elevator to Maridia]
org $8f94e9
	db $04, $1a
;;; [Elevator to Red Brinstar]
org $8f9647
	db $01, $15
;;; [Elevator to Green Brinstar]
org $8f9955
	db $01, $15
;;; Statues Hallway
org $8fa60a
	db $01, $17
;;; Statues Room
org $8fa687
	db $01, $17
;;; Warehouse Entrance
org $8fa6be
	db $03, $07
;;; Lava Dive Room
org $8faf31
	db $06, $0f
;;; [Elevator to Lower Norfair]
org $8faf5c
	db $06, $0d
;;; [Elevator Save Room]
org $8fb1d8
	db $06, $0d
