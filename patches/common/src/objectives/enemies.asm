include

namespace enemies

table:
        dw !space_pirates_green_pirates_shaft_0_event, space_pirates, green_pirates_shaft, 0
        dw !space_pirates_green_pirates_shaft_1_event, space_pirates, green_pirates_shaft, 0
        dw !space_pirates_green_pirates_shaft_2_event, space_pirates, green_pirates_shaft, 0
        dw !space_pirates_green_pirates_shaft_3_event, space_pirates, green_pirates_shaft, 0
        dw !space_pirates_green_pirates_shaft_4_event, space_pirates, green_pirates_shaft, 0

space_pirates:
        db $05
        dw $02
        dw !space_pirates_all_event

green_pirates_shaft:
        dw 12

        dw !space_pirates_green_pirates_shaft_0_event
        dw !space_pirates_green_pirates_shaft_1_event
        dw !space_pirates_green_pirates_shaft_2_event
        dw !space_pirates_green_pirates_shaft_3_event
        dw !space_pirates_green_pirates_shaft_4_event

        dw !space_pirates_green_pirates_shaft_all_event

pushpc

org $a1850a
        dw $4004
org $a1851a
        dw $400c
org $a1852a
        dw $4014
org $a1853a
        dw $401c
org $a1854a
        dw $4024

pullpc

namespace off
