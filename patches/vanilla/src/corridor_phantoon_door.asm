lorom
arch 65816

org $8fcd1c
        dw phantoon_room_doors

org $8ff79c
phantoon_room_doors:
        dw $a2c4, phantoon_back_door

org $83ae34
phantoon_back_door:
        ;; placeholder: wraps back in room (copy of $a2ac)
        dw $CD13
        db $00,$04,$01,$06,$00,$00
        dw $8000,$0000
