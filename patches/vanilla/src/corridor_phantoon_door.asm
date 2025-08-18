lorom
arch 65816

incsrc "macros.asm"

org $8fcd1c
        dw phantoon_room_doors

%freespaceStart($8ff79c)
phantoon_room_doors:
        dw $a2c4, phantoon_back_door
%freespaceEnd($8ff79c+4)

%freespaceStart($83ae34)
%export(phantoon_back_door)
        ;; placeholder: wraps back in room (copy of $a2ac)
        dw $CD13
        db $00,$04,$01,$06,$00,$00
        dw $8000,$0000
%freespaceEnd($83ae34+12)
