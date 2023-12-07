lorom
arch 65816

;;; [Crab Maze to Elevator]
org $8f95c5
	db $04, $08
;;; [Elevator to Maridia]
org $8f94e9
	db $04, $08
;;; [Elevator to Red Brinstar]
org $8f9647
	db $01, $07
;;; [Elevator to Green Brinstar]
org $8f9955
	db $01, $04
;;; Statues Hallway
org $8fa60a
	db $01, $06
;;; Statues Room
org $8fa687
	db $01, $06
;;; Warehouse Entrance
org $8fa6be
	db $03, $01
;;; Lava Dive Room
org $8faf31
	db $06, $02
;;; [Elevator to Lower Norfair]
org $8faf5c
	db $06, $02
;;; [Elevator Save Room]
org $8fb1d8
	db $06, $02
