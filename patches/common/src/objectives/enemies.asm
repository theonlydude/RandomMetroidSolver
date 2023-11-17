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

org $a18508
        dw $2080
org $a18518
        dw $2081
org $a18528
        dw $2082
org $a18538
        dw $2083
org $a18548
        dw $2084

pullpc

namespace off
