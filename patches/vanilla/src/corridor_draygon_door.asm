lorom
arch 65816

incsrc "macros.asm"

org $8fd9b3
        dw space_jump_room_doors

%freespaceStart($8ff728)
space_jump_room_doors:
        dw $A924, space_jump_back_door
%freespaceEnd($8ff728+4)

%freespaceStart($83ae10)
%export(space_jump_back_door)
        ;; placeholder: wraps back in room (copy of $a978)
        dw $D9AA
        db $00,$05,$0E,$06,$00,$00
        dw $8000,$0000
%freespaceEnd($83ae10+12)
