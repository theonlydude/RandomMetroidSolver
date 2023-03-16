lorom

incsrc "sym/map.asm"

org $8FE893
        jsr setup_asm_hook

org $8FE9B8
setup_asm_hook:
        jsr map_set_collected_map
        ldx $07bb               ; vanilla code
        rts
print "bank 8f end: ", pc
