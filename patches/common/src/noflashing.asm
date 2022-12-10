;;; Avoids flashing in-game
;;; Author: kara

arch 65816
lorom

incsrc "noflash/power_bomb.asm"
incsrc "noflash/escape.asm"
incsrc "noflash/bosses.asm"

; remove Initial Landing Site Lightning
org $8DEB43
        dw $00F0, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $C648 : db $02
        dw $0002, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0002, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $C639, $EB5A
        dw $00F0, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $C648 : db $01
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0001, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $0002, $2D6C, $294B, $252A, $2109, $1CE8, $18C7, $14A6, $1085, $C595
        dw $C639, $EC01
        dw $C61E, $EB43
        
warnpc $8DEC59
