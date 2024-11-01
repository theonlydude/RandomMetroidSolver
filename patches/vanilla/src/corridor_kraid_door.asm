lorom
arch 65816

incsrc "macros.asm"

org $8fa6eb
        dw varia_suit_room_doors

org $8ff72c
varia_suit_room_doors:
        dw $9252, varia_suit_back_door

org $83ae1c
%export(varia_suit_back_door)
        ;; placeholder: wraps back in room (copy of $91DA)
        dw $A6E2
        db $00,$04,$01,$06,$00,$00
        dw $8000,$0000
