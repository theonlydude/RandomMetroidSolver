lorom
arch 65816

org $8fb6a1
        dw ridley_tank_room_doors

org $8ff798
ridley_tank_room_doors:
        dw $9a62, ridley_tank_back_door

org $83ae28
ridley_tank_back_door:
        ;; placeholder: wraps back in room (copy of $98b2)
        dw $B698
        db $00,$05,$0E,$06,$00,$00
        dw $8000,$0000