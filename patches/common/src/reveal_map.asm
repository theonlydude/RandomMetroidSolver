lorom

incsrc "sym/map.asm"

incsrc "macros.asm"

org $8FE893
        jsr setup_asm_hook

%freespaceStart($8FE9B8)
setup_asm_hook:
        jsr map_set_collected_map
        ldx $07bb               ; vanilla code
        rts
print "bank 8f end: ", pc
%freespaceStart($8FE9BF)
