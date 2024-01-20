include

;;; palettes from map overhaul example patch
org $b6f000
	dw $0000, $02df, $01d7, $00ac, $5ebb, $3db3, $292e, $1486, $6318, $48fb, $7fff, $0000, $6318, !unexplored_gray, $7fff, $0000
org $b6f020
	dw $2003, $0bb1, $1ea9, $0145, $0000, $3db3, $292e, $1486, $6318, $5ef7, $0000, $0000, $6318, $02df, !vanilla_etank_color, $7fff
org $b6f040
        ;; modified "unexplored" palette to be less dark
        dw $2003, !unexplored_gray, $6b5a, $4e73, $0000, $7fff, $0156, $001f, $2413, $559d, $0000, $02df, $4408, $7fff, $5ef7, $318c
org $b6f060
	dw $0000, $48fb, $7fff, $7392, $0000, $4a52, $318c, $5ef7, $1ce7, $2870, $1ce7, $4a52, $4408, $7fff, $5ef7, $318c
org $b6f080
	dw $0000, $1ea9, $7fff, $7392, $0000, $7fff, $4a52, $6318, $6318, $6318, $48fb, $6318, $6318, $0000, $7fff, $6318
org $b6f0a0
	dw $0000, $02df, $7fff, $7392, $6318, $6318, $6318, $6318, $6318, $6318, $2884, $6318, $7000, $0000, $7fff, $6318
org $b6f0c0
	dw $0000, $0e3f, $7fff, $7392, $0000, $739c, $0156, $6e7a, $0000, $0000, $0000, $039e, $4408, $7fff, $5ef7, $318c
org $b6f0e0
	dw $0000, $4631, $7fff, $7392, $0000, $739c, $318c, $739c, $739c, $739c, $0000, $4a52, $4408, $7fff, $6318, $6318
org $b6f100
	dw $3800, $7fff, $4bff, $13ff, $129f, $111f, $0cb5, $046a, $0000, $3db3, $292e, $48fb, $1849, $44e5, $7fff, $0000
org $b6f120
	dw $3800, $7fff, $4bff, $13ff, $129f, $111f, $0cb5, $046a, $0000, $1085, $0c64, $1447, $0823, $1442, $2108, $0000
org $b6f140
	dw $3800, $200d, $000a, $2c02, $4e73, $7fff, $039f, $001f, $0000, $559d, $001d, $039f, $7fff, $0000, $0000, $023f
org $b6f160
	dw $3800, $200d, $000a, $2c02, $4e73, $7fff, $039f, $001f, $0000, $559d, $001d, $039f, $7fff, $0000, $0000, $023f
org $b6f180
	;; custom VARIA palette for area map icons
	dw $3800
        dw !AreaColor_GreenPinkBrinstar
        dw !AreaColor_RedBrinstar
        dw !AreaColor_WreckedShip
        dw !AreaColor_Kraid
        dw !AreaColor_Norfair
        dw !AreaColor_Crocomire
        dw !AreaColor_LowerNorfair
        dw !AreaColor_WestMaridia
        dw !AreaColor_EastMaridia
        dw !AreaColor_Tourian
        dw !AreaColor_Undefined
        dw $38e0
        dw !AreaColor_Crateria
        dw $0000, $0000
org $b6f1a0
	;; custom VARIA palette for door map icons
	dw $3800, $6e7b, $44b9, $02be, $01b6, $0790, $1a88, $3992, $250d, $4d03, $71c7, $0000, $0000, $1ce7, $0000, $0000
org $b6f1c0
	dw $3800, $0ce0, $08a0, $0040, $18c5, $1062, $0c41, $0421, $0ce7, $0887, $0027, $0025, $0023, $0001, $1ce7, $0000
org $b6f1e0
	dw $3800, $2fe0, $1a80, $0120, $6b37, $4588, $2d05, $1062, $37ff, $1e3f, $047f, $0456, $004c, $0023, $7fff, $0000

;;; additional colors by area to be able to draw graph areas with a consistent palette
org !PauseScreen_AreaPalettes_Pointer
;;; replace 2nd color of palette lines $03 to $07, indexed by area
area_palettes:
        ;; pointers to color lists
        dw .Crateria, .Brinstar, .Norfair, .WreckedShip, .Maridia, .Tourian
        ;; color lists in reverse order (palette index 7 to 3)
.Crateria:
        dw !AreaColor_Crateria
        dw !AreaColor_WreckedShip
        dw !AreaColor_Tourian
        dw !AreaColor_EastMaridia
        dw !AreaColor_Undefined ; used for one tile of GreenPinkBrinstar and one of RedBrinstar (area rando only)
.Brinstar:
        dw !AreaColor_GreenPinkBrinstar
        dw !AreaColor_RedBrinstar
        dw !AreaColor_Crateria
        dw !AreaColor_Kraid
        dw !AreaColor_Norfair
.Norfair:
        dw !AreaColor_Norfair
        dw !AreaColor_LowerNorfair
        dw !AreaColor_Crocomire
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined
.WreckedShip:
        dw !AreaColor_WreckedShip
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined
.Maridia:
        dw !AreaColor_RedBrinstar
        dw !AreaColor_WestMaridia
        dw !AreaColor_EastMaridia
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined
.Tourian:
        dw !AreaColor_Tourian
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined
        dw !AreaColor_Undefined

print "B6 end: ", pc

warnpc $b6ffff
