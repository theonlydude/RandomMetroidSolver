;;; compile with thedopefish asar
;;; fix etecoons wall jumping

arch 65816
lorom


org $A199FA
; Room $9AD9, state $9AE6: Enemy population
; Enemy population format is:
;    ____________________________________ Enemy ID
;   |      _______________________________ X position
;   |     |      __________________________ Y position
;   |     |     |      _____________________ Initialisation parameter (orientation in SMILE)
;   |     |     |     |      ________________ Properties (special in SMILE)
;   |     |     |     |     |      ___________ Extra properties (special graphics bitset in SMILE)
;   |     |     |     |     |     |      ______ Parameter 1 (speed in SMILE)
;   |     |     |     |     |     |     |      _ Parameter 2 (speed2 in SMILE)
;   |     |     |     |     |     |     |     |
;   iiii  xxxx  yyyy  oooo  pppp  gggg  aaaa  bbbb
dw $E5BF,$01a1,$0B98,$0000,$0C00,$0000,$0000,$0000
dw $E5BF,$0191,$0B98,$0000,$0C00,$0000,$0000,$0001
dw $E5BF,$0181,$0B98,$0000,$0C00,$0000,$0000,$0002

; $A1:997A             dx 
; D73F,0080,02C2,0000,2C00,0000,0001,0018, 
; DC7F,00DA,02CB,0001,2803,0000,0001,0002, 
; DC7F,0070,0398,0003,2001,0000,0001,0002, 
; D43F,006C,03F6,0000,2000,0000,0018,0001, 
; DC7F,0079,06E8,0003,2000,0000,0001,0002, 
; D43F,0043,0548,0000,2000,0000,0018,0001, 
; DC7F,007B,05F8,0001,2002,0000,0001,0002, 
; DC7F,0027,03CC,0000,2003,0000,0001,0002, 
; E5BF,025F,0B98,0000,0C00,0000,0000,0000, 
; E5BF,026F,0B98,0000,0C00,0000,0000,0001, 
; E5BF,027F,0B98,0000,0C00,0000,0000,0002, FFFF, 07

;;; etecoon0:
;;; ai: e9af il: e8d6 facing camera, arms up and down, when samus enters the room
;;; ai: ea00 il: e854 facing camera, on the ground, before jump
;;; ai: ea37 il: e84a facing camera, first jump
;;; ai: eab5 il: e81e on the ground, looking left
;;; 
;;; 
;;; 
;;; 
;;; 
;;; etecoon1:
;;; ai: e9af il: e8d6 facing camera, arms up and down, when samus enters the room
;;; ai: ea00 il: e854 facing camera, on the ground, before jump
;;; ai: ea37 il: e84a facing camera, first jump
;;; ai: eab5 il: e81e on the ground, looking left
;;; 
;;; 
;;; 
;;; 
;;; 
;;; etecoon2:
;;; ai: e9af il: e8d6 facing camera, arms up and down, when samus enters the room
;;; ai: ea00 il: e854 facing camera, on the ground, before jump
;;; ai: ea37 il: e84a facing camera, first jump
;;; ai: ea00 il: e854 facing camera, on the ground, before jump
;;; 
;;; 
;;; 
;;; 
;;; 

;;; functions
org $A0C6AB
CommonHorizontalMovementRoutineMovesBy1412200: ; $C6AB: Move enemy right by [$14].[$12], ignore slopes

org $A0C786
CommonVerticalMovementRoutineMovesBy1412200: ; $C786: Move enemy down by [$14].[$12] ;

org $A0AEED
IsSamusWithinAPixelRowsOfEnemy: ; $AEED: Is Samus within [A] pixel rows of enemy ;

org $8090A3
QueueSoundSoundLibrary2MaxQueuedSoundsAllowed15: ; $90A3: Queue sound, sound library 2, max queued sounds allowed = 15 ;

org $8090CB
QueueSoundSoundLibrary2MaxQueuedSoundsAllowed6: ; $90CB: Queue sound, sound library 2, max queued sounds allowed = 6 ;

org $A0AF0B
IsSamusWithinAPixelColumnsOfEnemy: ; $AF0B: Is Samus within [A] pixel columns of enemy ;

org $A0AE29
DetermineDirectionOfSamusFromEnemy: ; $AE29: Determine direction of Samus from enemy ;

; Lots of enemy boundary calculations
; (seems to be trying to find it's location in room, possibly calculating x distance movement).
org $A0BBBF
SUBL_A0BBBF:

;;; variables
Samus_X_position = $7E0AF6

EarthquakeTimer = $7E1840
EnemyIndex = $7E0E54

X_position = $7E0F7A
Y_position = $7E0F7E
Y_subposition = $7E0F80
Properties = $7E0F86
Spritemap_pointer = $7E0F8E
Timer = $7E0F90
Init_param = $7E0F92
Instruction_list = $7E0F92      ; for drawing
Instruction_timer = $7E0F94


AI_variable_0 = $7E0FA8
AI_variable_1 = $7E0FAA
AI_variable_2 = $7E0FAC
AI_variable_3 = $7E0FAE
AI_variable_4 = $7E0FB0
AI_variable_5 = $7E0FB2         ; AI pointer

Param1 = $7E0FB4
Param1_high = $7E0FB5           ; direction (high byte)
Param2 = $7E0FB6                ; x radius (low byte)
Param2_high = $7E0FB7           ; if == 0 then store 1 in Extra_RAM_flag

DoorTransitionFlag = $7E0797

	
org $A7E81E
;;; $E81E: Instruction list - on the ground, looking left ;;;
{
    dw $0005,$EFFF
    dw $812F ; | A7E822 | Sleep
}

;;; run to the left
;;; $E824: Instruction list - yyyy ;;;
run_to_the_left:
{
;    dw $0001,$F024
;    dw $0005,$EEED
;    dw $0005,$EEFE
;    dw $0005,$EF0A
;    dw $0005,$EEFE
    dw $0001,$F1C0
    dw $0005,$F089
    dw $0005,$F09A
    dw $0005,$F0A6
    dw $0005,$F09A
    dw $80ED,$E828 ; | A7E838 | Go to $E828
}


;;; $E83C: Instruction list - yyyy ;;;
{
    dw $0008,$EF5A
    dw $0003,$EF16
    dw $0003,$EF27
    dw $0003,$EF38
    dw $0003,$EF49
    dw $80ED,$E840 ; | A7E850 | Go to $E840
}


;;; $E854: Instruction list - facing camera, on the ground, before jump ;;;
{
    dw $0001,$EF6B
    dw $812F ; | A7E858 | Sleep
}


;;; $E85A: Instruction list - facing camera, first jump ;;;
{
    dw $000C,$EF90
    dw $000C,$EFB5
    dw $0006,$EFDA
    dw $000C,$EFB5
    dw $000C,$EF90
    dw $812F ; | A7E86E | Sleep
}


;;; $E870: Instruction list - yyyy ;;;
{
    dw $0001,$F06E
    dw $812F ; | A7E874 | Sleep
}

;;; goes from this il to the next by increasing Y
;;; $E876: Instruction list - yyyy ;;;
{
    dw $0005,$F1E5
    dw $812F ; | A7E87A | Sleep
}

;;; run on the right
;;; $E87C: Instruction list - yyyy ;;;
run_to_the_right:
{
;    dw $0001,$F1C0
;    dw $0005,$F089
;    dw $0005,$F09A
;    dw $0005,$F0A6
;    dw $0005,$F09A
    dw $0001,$F024
    dw $0005,$EEED
    dw $0005,$EEFE
    dw $0005,$EF0A
    dw $0005,$EEFE
    dw $80ED,$E880 ; | A7E890 | Go to $E880
}


;;; $E894: Instruction list - yyyy ;;;
{
    dw $0008,$F0F6
    dw $0003,$F0B2
    dw $0003,$F0C3
    dw $0003,$F0D4
    dw $0003,$F0E5
    dw $80ED,$E898 ; | A7E8A8 | Go to $E898
}


;;; $E8AC: Instruction list - yyyy ;;;
{
    dw $0001,$F107
    dw $812F ; | A7E8B0 | Sleep
}


;;; $E8B2: Instruction list - yyyy ;;;
{
    dw $000C,$F12C
    dw $000C,$F151
    dw $0006,$F176
    dw $000C,$F151
    dw $000C,$F12C
    dw $812F ; | A7E8C6 | Sleep
}


;;; $E8C8: Instruction list - yyyy ;;;
{
    dw $0001,$F20A
    dw $812F ; | A7E8CC | Sleep
}


;;; $E8CE: Instruction list - yyyy ;;;
{
    dw $0008,$F107
    dw $80ED,$E8CE ; | A7E8D2 | Go to $E8CE
}


;;; $E8D6: Instruction list - facing camera, arms up and down, when samus enters the room ;;;
IL_facing_camera_jumping_up_and_down:
{
    dw $8123,$0004 ; | A7E8D6 | Timer = 0004h
    dw $0008,$F107
    dw $0008,$F12C
    dw $0008,$F151
    dw $0008,$F176
    dw $0008,$F151
    dw $0008,$F12C
    dw $8110,$E8DA ; | A7E8F2 | Decrement timer and go to $E8DA if non-zero
;    dw $0020,$F19B ; looking right (when the music stops)
    dw $0020,$F1E5 ; looking left (when the music stops)
;    dw $0020,$F1E5 ; looking left
    dw $0020,$F19B ; looking right
    dw $812F ; | A7E8FE | Sleep
}


DAT_A7E900:
    dw $FFFD
DAT_A7E902:
    dw $0000
DAT_A7E904:
    dw $FFFC
DAT_A7E906:
    dw $0000
Etecoon_X_offset_to_the_right:                     ; etecoon X offset to move by: to the right
;    dw $0002
        dw $FFFE
Etecoon_X_suboffset_to_the_right:                     ; etecoon X suboffset to move by
    dw $0000
Etecoon_X_offset_to_the_left:                     ; etecoon X offset to move by: to the left
;    dw $FFFE
	dw $0002
Etecoon_X_suboffset_to_the_left:                     ; etecoon X suboffset to move by
    dw $0000
DAT_A7E910:
    dw $0040


;;; $E912: Initialisation AI - enemy $E5BF (etecoon) ;;;
{
InitialisationAiEnemyE5BfEtecoon:
    LDX.w EnemyIndex                        ;| A7E912 | A7 | 
    LDA.w Properties,X                    ;| A7E915 | A7 | 
    ORA.w #$2000                            ;| A7E918 | A7 | 
    STA.w Properties,X                    ;| A7E91B | A7 | 
    LDA.w #$804D                            ;| A7E91E | A7 | 
    STA.w Spritemap_pointer,X                    ;| A7E921 | A7 | 
    LDA.w #$0001                            ;| A7E924 | A7 | 
    STA.w Instruction_timer,X                    ;| A7E927 | A7 | 
    STZ.w Timer,X                    ;| A7E92A | A7 | 
    LDA.w #$E8CE                            ;| A7E92D | A7 | 
    STA.w Instruction_list,X                    ;| A7E930 | A7 | 
    LDA.w #$E9AF                            ;| A7E933 | A7 | 
    STA.w AI_variable_5,X                    ;| A7E936 | A7 | 
    LDA.w #$FFFF                            ;| A7E939 | A7 | 
    STA.w AI_variable_4,X                    ;| A7E93C | A7 | 
    RTL                                     ;| A7E93F | A7 | 
}


;;; $E940: Main AI - enemy $E5BF (etecoon) ;;;
{
MainAiEnemyE5BfEtecoon:
    LDX.w EnemyIndex                        ;| A7E940 | A7 | 
    LDA.w Param2,X                    ;| A7E943 | A7 | 
    BIT.w #$FF00                            ;| A7E946 | A7 | 
    BEQ BRA_A7E954                          ;| A7E949 | A7 | 
    SEC                                     ;| A7E94B | A7 | 
    SBC.w #$0100                            ;| A7E94C | A7 | 
    STA.w Param2,X                    ;| A7E94F | A7 | 
    BRA BRA_A7E957                          ;| A7E952 | A7 | 

BRA_A7E954:
    JMP.w (AI_variable_5,X)                  ;| A7E954 | A7 | 

BRA_A7E957:
    RTL                                     ;| A7E957 | A7 | 
}

;;; $E958:  ;;;
{
SUB_A7E958:
    LDA.w EarthquakeTimer                   ;| A7E958 | A7 | 
    BEQ BRA_A7E973                          ;| A7E95B | A7 | 
    LDA.w Param2,X                    ;| A7E95D | A7 | 
    AND.w #$00FF                            ;| A7E960 | A7 | 
    ORA.w #$8000                            ;| A7E963 | A7 | 
    STA.w Param2,X                    ;| A7E966 | A7 | 
    LDA.w Instruction_timer,X                    ;| A7E969 | A7 | 
    CLC                                     ;| A7E96C | A7 | 
    ADC.w #$0080                            ;| A7E96D | A7 | 
    STA.w Instruction_timer,X                    ;| A7E970 | A7 | 

BRA_A7E973:
    RTS                                     ;| A7E973 | A7 | 
}

;;; move etecoon, Move enemy right by [AI_2].[AI_3], ignore slopes
;; Parameters:
;;     X: Enemy index
;;     $12: X suboffset to move by
;;     $14: X offset to move by
;; Returns:
;;     Carry: Set if collided with wall
;;; $E974:  ;;;
{
MoveEtecoonToTheRight:
    LDA.w AI_variable_2,X                    ;| A7E974 | A7 | \
    STA.b $14                               ;| A7E977 | A7 | |
    LDA.w AI_variable_3,X                ;| A7E979 | A7 | } Move enemy right by [enemy X velocity]
    STA.b $12                               ;| A7E97C | A7 | |
    JSL.l CommonHorizontalMovementRoutineMovesBy1412200;| A7E97E | A0 | /
    RTS                                     ;| A7E982 | A7 | 
}


;;; $E983:  ;;;
{
SUB_A7E983:
    LDA.w AI_variable_0,X                    ;| A7E983 | A7 | \
    STA.b $14                               ;| A7E986 | A7 | |
    LDA.w AI_variable_1,X                    ;| A7E988 | A7 | } $14.$12 = [enemy Y velocity]
    STA.b $12                               ;| A7E98B | A7 | /
    LDA.w AI_variable_0,X                    ;| A7E98D | A7 | 
    CMP.w #$0005                            ;| A7E990 | A7 | 
    BPL BRA_A7E9AA                          ;| A7E993 | A7 | 
    LDA.w AI_variable_1,X                    ;| A7E995 | A7 | 
    CLC                                     ;| A7E998 | A7 | 
    ADC.l $000B32                           ;| A7E999 | A7 | 
    STA.w AI_variable_1,X                    ;| A7E99D | A7 | 
    LDA.w AI_variable_0,X                    ;| A7E9A0 | A7 | 
    ADC.l $000B34                           ;| A7E9A3 | A7 | 
    STA.w AI_variable_0,X                    ;| A7E9A7 | A7 | 

BRA_A7E9AA:
    JSL.l CommonVerticalMovementRoutineMovesBy1412200;| A7E9AA | A0 |  Move enemy down by [$14].[$12]
    RTS                                     ;| A7E9AE | A7 | 
}

;;; wait for door transition to end, then to samus to be close on Y axis to etecoons, then load etecoons theme
;;; $E9AF:  ;;;
{
    LDA.w DoorTransitionFlag                ; set to 0001 if door transition is in progress, 0000 otherwise
    BEQ BRA_A7E9B5                          ;| A7E9B2 | A7 | 
    RTL                                     ;| A7E9B4 | A7 | 

BRA_A7E9B5:
    LDA.w AI_variable_4,X                    ;| A7E9B5 | A7 | 
    BPL BRA_A7E9E6                          ;| A7E9B8 | A7 | 
    LDA.w #$0080                            ;| A7E9BA | A7 | 
    JSL.l IsSamusWithinAPixelRowsOfEnemy    ;| A7E9BD | A0 | 
    TAY                                     ;| A7E9C1 | A7 | 
    BEQ BRA_A7E9FF                          ;| A7E9C2 | A7 | 
    LDA.w Param2,X                    ;| A7E9C4 | A7 | 
    BIT.w #$0003                            ;| A7E9C7 | A7 | 
    BNE BRA_A7E9D3                          ;| A7E9CA | A7 | 
    LDA.w #$0035                            ;| A7E9CC | A7 | \
    JSL.l QueueSoundSoundLibrary2MaxQueuedSoundsAllowed15;| A7E9CF | 80 | } Queue sound 35h, sound library 2, max queued sounds allowed = 15 (etecoon's theme)

BRA_A7E9D3:
    LDA.w #$0001                            ;| A7E9D3 | A7 | 
    STA.w Instruction_timer,X                    ;| A7E9D6 | A7 | 
    LDA.w #IL_facing_camera_jumping_up_and_down
    STA.w Instruction_list,X                    ;| A7E9DC | A7 | 
    LDA.w #$0100                            ;| A7E9DF | A7 | 
    STA.w AI_variable_4,X                    ;| A7E9E2 | A7 | 
    RTL                                     ;| A7E9E5 | A7 | 

BRA_A7E9E6:
    DEC.w AI_variable_4,X                    ;| A7E9E6 | A7 | 
    BEQ BRA_A7E9ED                          ;| A7E9E9 | A7 | 
    BPL BRA_A7E9FF                          ;| A7E9EB | A7 | 

BRA_A7E9ED:
    LDA.w #$E854                            ;| A7E9ED | A7 | 
    STA.w Instruction_list,X                    ;| A7E9F0 | A7 | 
    LDA.w #AI_Facing_camera_standing_on_the_ground
    STA.w AI_variable_5,X                    ;| A7E9F6 | A7 | 
    LDA.w #$000B                            ;| A7E9F9 | A7 | 
    STA.w AI_variable_4,X                    ;| A7E9FC | A7 | 

BRA_A7E9FF:
    RTL                                     ;| A7E9FF | A7 | 
}

;;; facing camera, standing on the ground, arms down for a few frames
;;; $EA00:  ;;;
AI_Facing_camera_standing_on_the_ground:
{
    DEC.w AI_variable_4,X                    ;| A7EA00 | A7 | 
    BEQ BRA_A7EA07                          ;| A7EA03 | A7 | 
    BPL BRA_A7EA36                          ;| A7EA05 | A7 | 

BRA_A7EA07:
    LDA.w DAT_A7E900                        ;| A7EA07 | A7 | 
    STA.w AI_variable_0,X                    ;| A7EA0A | A7 | 
    LDA.w DAT_A7E902                        ;| A7EA0D | A7 | 
    STA.w AI_variable_1,X                    ;| A7EA10 | A7 | 
    LDA.w Instruction_list,X                    ;| A7EA13 | A7 | 
    INC                                     ;| A7EA16 | A7 | 
    INC                                     ;| A7EA17 | A7 | 
    STA.w Instruction_list,X                    ;| A7EA18 | A7 | 
    LDA.w #$0001                            ;| A7EA1B | A7 | 
    STA.w Instruction_timer,X                    ;| A7EA1E | A7 | 
    LDA.w #AI_Facing_Camera_Jumping_Vertically  ;| A7EA21 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EA24 | A7 | 
    LDA.w Samus_X_position                      ;| A7EA27 | A7 | 
    CMP.w #$0100                            ;| A7EA2A | A7 | 
    BMI BRA_A7EA36                          ;| A7EA2D | A7 | 
    LDA.w #$0033                            ;| A7EA2F | A7 | \
    JSL.l QueueSoundSoundLibrary2MaxQueuedSoundsAllowed6;| A7EA32 | 80 | } Queue sound 33h, sound library 2, max queued sounds allowed = 6 (etecoon cry)

BRA_A7EA36:
    RTL                                     ;| A7EA36 | A7 | 
}

;;; facing camera, jumping vertically
;;; AI_variable_0: stores Y step, < 0 when jumping, > 0 when falling
;;; $EA37:  ;;;
AI_Facing_Camera_Jumping_Vertically:
{
    JSR.w SUB_A7E983                        ;| A7EA37 | A7 | 
    BCS BRA_A7EA3D                          ;| A7EA3A | A7 | 
    RTL                                     ;| A7EA3C | A7 | 

BRA_A7EA3D:
    LDA.w AI_variable_0,X                    ;| A7EA3D | A7 | 
    BPL BRA_A7EA55                          ;| A7EA40 | A7 | 
    STZ.w AI_variable_0,X                    ;| A7EA42 | A7 | 
    STZ.w AI_variable_1,X                    ;| A7EA45 | A7 | 
    LDA.w #$0003                            ;| A7EA48 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EA4B | A7 | 
    LDA.w #$E862                            ;| A7EA4E | A7 | 
    STA.w Instruction_list,X                    ;| A7EA51 | A7 | 
    RTL                                     ;| A7EA54 | A7 | 

BRA_A7EA55:
    LDA.w #$0040                            ;| A7EA55 | A7 | 
    JSL.l IsSamusWithinAPixelRowsOfEnemy    ;| A7EA58 | A0 | 
    TAY                                     ;| A7EA5C | A7 | 
    BEQ BRA_A7EA9C                          ;| A7EA5D | A7 | 
    LDA.w DAT_A7E910                        ;| A7EA5F | A7 | 
    JSL.l IsSamusWithinAPixelColumnsOfEnemy ;| A7EA62 | A0 | 
    TAY                                     ;| A7EA66 | A7 | 
    BEQ BRA_A7EA9C                          ;| A7EA67 | A7 | 
    JSL.l DetermineDirectionOfSamusFromEnemy;| A7EA69 | A0 | 
    CMP.w #$0005                            ;| A7EA6D | A7 | 
    BPL BRA_A7EA7D                          ;| A7EA70 | A7 | 
    LDA.w #$E81E                            ;| A7EA72 | A7 | 
    STA.w Instruction_list,X                    ;| A7EA75 | A7 | 
    STZ.w Param1,X                    ;| A7EA78 | A7 | 
    BRA BRA_A7EA89                          ;| A7EA7B | A7 | 

BRA_A7EA7D:
    LDA.w #$E876                            ;| A7EA7D | A7 | 
    STA.w Instruction_list,X                    ;| A7EA80 | A7 | 
    LDA.w #$0001                            ;| A7EA83 | A7 | 
    STA.w Param1,X                    ;| A7EA86 | A7 | 

BRA_A7EA89:
    LDA.w #$0020                            ;| A7EA89 | A7 | 
    STA.w AI_variable_4,X                    ;| A7EA8C | A7 | 
    LDA.w #$0001                            ;| A7EA8F | A7 | 
    STA.w Instruction_timer,X                    ;| A7EA92 | A7 | 
    LDA.w #$EAB5                            ;| A7EA95 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EA98 | A7 | 
    RTL                                     ;| A7EA9B | A7 | 

BRA_A7EA9C:
    LDA.w #$000B                            ;| A7EA9C | A7 | 
    STA.w AI_variable_4,X                    ;| A7EA9F | A7 | 
    LDA.w #AI_Facing_camera_standing_on_the_ground
    STA.w AI_variable_5,X                    ;| A7EAA5 | A7 | 
    LDA.w #$0001                            ;| A7EAA8 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EAAB | A7 | 
    LDA.w #$E854                            ;| A7EAAE | A7 | 
    STA.w Instruction_list,X                    ;| A7EAB1 | A7 | 
    RTL                                     ;| A7EAB4 | A7 | 
}

;;; looks left, setup behaviour
;;; $EAB5:  ;;;
etecoon_first_time_action_4:
{
    DEC.w AI_variable_4,X                    ;| A7EAB5 | A7 | 
    BEQ .end_timer                          ;| A7EAB8 | A7 | 
    BPL .end                          ;| A7EABA | A7 | 

.end_timer
    LDA.w Instruction_list,X                    ;| A7EABC | A7 | 
    INC                                     ;| A7EABF | A7 | 
    INC                                     ;| A7EAC0 | A7 | 
    STA.w Instruction_list,X                    ;| A7EAC1 | A7 | 
    LDA.w #$0001                            ;| A7EAC4 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EAC7 | A7 | 
    LDA.w Param1,X                    ;| A7EACA | A7 | 
    BEQ .BRA_A7EAE3                          ;| A7EACD | A7 | 

    LDA.w Etecoon_X_offset_to_the_right                        ; etecoon 200 with param1 == 1
    STA.w AI_variable_2,X                    ;| A7EAD2 | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_right                        ;| A7EAD5 | A7 | 
    STA.w AI_variable_3,X                ;| A7EAD8 | A7 | 
    LDA.w #$EB2C                            ;| A7EADB | A7 | 
    STA.w AI_variable_5,X                    ;| A7EADE | A7 | 
    BRA .BRA_A7EAF5                          ;| A7EAE1 | A7 | 

.BRA_A7EAE3
    LDA.w Etecoon_X_offset_to_the_left                        ; etecoon X offset to move by
    STA.w AI_variable_2,X
    LDA.w Etecoon_X_suboffset_to_the_left                        ; etecoon X suboffset to move by
    STA.w AI_variable_3,X
    LDA.w #$EB02                            ; next AI
    STA.w AI_variable_5,X

.BRA_A7EAF5
    LDA.w DAT_A7E900                        ;| A7EAF5 | A7 | 
    STA.w AI_variable_0,X                    ;| A7EAF8 | A7 | 
    LDA.w DAT_A7E902                        ;| A7EAFB | A7 | 
    STA.w AI_variable_1,X                    ;| A7EAFE | A7 | 

.end
    RTL                                     ;| A7EB01 | A7 | 
}

;;; move etecoon to the right by [AI_2].[AI_3] until collision with wall
;;; then setup etecoon behaviour 
;;; $EB02:  ;;;
{
    JSR.w MoveEtecoonToTheRight                        ;| A7EB02 | A7 | 
    BCC BRA_A7EB2B                          ;| A7EB05 | A7 | 
    LDA.w Etecoon_X_offset_to_the_right                        ;| A7EB07 | A7 | 
    STA.w AI_variable_2,X                    ;| A7EB0A | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_right                        ;| A7EB0D | A7 | 
    STA.w AI_variable_3,X                ;| A7EB10 | A7 | 
    LDA.w #$EB2C                            ;| A7EB13 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EB16 | A7 | 
    LDA.w #$0001                            ;| A7EB19 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EB1C | A7 | 
    LDA.w #$E880                            ;| A7EB1F | A7 | 
    STA.w Instruction_list,X                    ;| A7EB22 | A7 | 
    LDA.w #$0001                            ;| A7EB25 | A7 | 
    STA.w Param1,X                    ;| A7EB28 | A7 | 

BRA_A7EB2B:
    RTL                                     ;| A7EB2B | A7 | 
}


;;; $EB2C:  ;;;
{
;    LDA.w #$0020                            ; distance in pixel to check against the wall, from the left
    LDA.w #$ffe0                            ; distance in pixel to check against the wall, from the left
    STA.b $14                               ; distance in pixel
    STZ.b $12                               ; distance in subpixel
    JSL.l SUBL_A0BBBF                       ; call routine to check if etecoon is 2 tiles from wall
    BCC BRA_A7EB4C                          ;| A7EB37 | A7 | 
    LDA.w #$0001                            ;| A7EB39 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EB3C | A7 | 
    LDA.w #$E898                            ;| A7EB3F | A7 | 
    STA.w Instruction_list,X                    ;| A7EB42 | A7 | 
    LDA.w #$EB50                            ; next ai to start spin jumping toward the wall
    STA.w AI_variable_5,X                    ;| A7EB48 | A7 | 
    RTL                                     ;| A7EB4B | A7 | 

BRA_A7EB4C:
    JSR.w MoveEtecoonToTheRight                        ; not at 2 tiles from wall, move etecoon to the right
    RTL
}

;;; spin jump toward the wall
;;; $EB50:  ;;;
{
    JSR.w SUB_A7E958                        ;| A7EB50 | A7 | 
    JSR.w MoveEtecoonToTheRight                        ;| A7EB53 | A7 | 
    BCC BRA_A7EB96                          ;| A7EB56 | A7 | 
    LDA.w Param1,X                    ;| A7EB58 | A7 | 
    BNE BRA_A7EB6B                          ;| A7EB5B | A7 | 
    LDA.w #$E8C8                            ;| A7EB5D | A7 | 
    STA.w Instruction_list,X                    ;| A7EB60 | A7 | 
    LDA.w #$0001                            ;| A7EB63 | A7 | 
    STA.w Param1,X                    ;| A7EB66 | A7 | 
    BRA BRA_A7EB74                          ;| A7EB69 | A7 | 

BRA_A7EB6B:
    LDA.w #$E870                            ;| A7EB6B | A7 | 
    STA.w Instruction_list,X                    ;| A7EB6E | A7 | 
    STZ.w Param1,X                    ;| A7EB71 | A7 | 

BRA_A7EB74:
    LDA.w #$0001                            ;| A7EB74 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EB77 | A7 | 
    LDA.w #$EBCD                            ;| A7EB7A | A7 | 
    STA.w AI_variable_5,X                    ;| A7EB7D | A7 | 
    LDA.w #$0008                            ;| A7EB80 | A7 | 
    STA.w AI_variable_4,X                    ;| A7EB83 | A7 | 
    LDA.w Samus_X_position                      ;| A7EB86 | A7 | 
    CMP.w #$0100                            ;| A7EB89 | A7 | 
    BMI BRA_A7EB95                          ;| A7EB8C | A7 | 
    LDA.w #$0032                            ;| A7EB8E | A7 | \
    JSL.l QueueSoundSoundLibrary2MaxQueuedSoundsAllowed6;| A7EB91 | 80 | } Queue sound 32h, sound library 2, max queued sounds allowed = 6 (etecoon wall-jump)

BRA_A7EB95:
    RTL                                     ;| A7EB95 | A7 | 

BRA_A7EB96:
    JSR.w SUB_A7E983                        ;| A7EB96 | A7 | 
    BCC BRA_A7EBCC                          ;| A7EB99 | A7 | 
    LDA.w Param1,X                    ;| A7EB9B | A7 | 
    BNE BRA_A7EBA8                          ;| A7EB9E | A7 | 
    LDA.w #$E8AC                            ;| A7EBA0 | A7 | 
    STA.w Instruction_list,X                    ;| A7EBA3 | A7 | 
    BRA BRA_A7EBAE                          ;| A7EBA6 | A7 | 

BRA_A7EBA8:
    LDA.w #$E854                            ;| A7EBA8 | A7 | 
    STA.w Instruction_list,X                    ;| A7EBAB | A7 | 

BRA_A7EBAE:
    LDA.w #$0001                            ;| A7EBAE | A7 | 
    STA.w Instruction_timer,X                    ;| A7EBB1 | A7 | 
    LDA.w #$000B                            ;| A7EBB4 | A7 | 
    STA.w AI_variable_4,X                    ;| A7EBB7 | A7 | 
    LDA.w #$EC1B                            ;| A7EBBA | A7 | 
    STA.w AI_variable_5,X                    ;| A7EBBD | A7 | 
    LDA.w DAT_A7E900                        ;| A7EBC0 | A7 | 
    STA.w AI_variable_0,X                    ;| A7EBC3 | A7 | 
    LDA.w DAT_A7E902                        ;| A7EBC6 | A7 | 
    STA.w AI_variable_1,X                    ;| A7EBC9 | A7 | 

BRA_A7EBCC:
    RTL                                     ;| A7EBCC | A7 | 
}

;;; contact with the wall, change direction, jump, next ai when away 1 tile from the wall
;;; $EBCD:  ;;;
{
    JSR.w SUB_A7E958                        ;| A7EBCD | A7 | 
    DEC.w AI_variable_4,X                    ;| A7EBD0 | A7 | 
    BEQ BRA_A7EBD7                          ;| A7EBD3 | A7 | 
    BPL BRA_A7EC1A                          ;| A7EBD5 | A7 | 

BRA_A7EBD7:
    LDA.w Param1,X                    ;| A7EBD7 | A7 | 
    BEQ BRA_A7EBF0                          ;| A7EBDA | A7 | 
;    LDA.w #$E894                            ;| A7EBDC | A7 | 
    LDA.w #$E83C                            ;| A7EBF0 | A7 | 
    STA.w Instruction_list,X                    ;| A7EBDF | A7 | 
    LDA.w Etecoon_X_offset_to_the_right                        ;| A7EBE2 | A7 | 
    STA.w AI_variable_2,X                    ;| A7EBE5 | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_right                        ;| A7EBE8 | A7 | 
    STA.w AI_variable_3,X                ;| A7EBEB | A7 | 
    BRA BRA_A7EC02                          ;| A7EBEE | A7 | 

BRA_A7EBF0:
;    LDA.w #$E83C                            ;| A7EBF0 | A7 | 
    LDA.w #$E894                            ;| A7EBDC | A7 | 
    STA.w Instruction_list,X                    ;| A7EBF3 | A7 | 
    LDA.w Etecoon_X_offset_to_the_left                        ;| A7EBF6 | A7 | 
    STA.w AI_variable_2,X                    ;| A7EBF9 | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_left                        ;| A7EBFC | A7 | 
    STA.w AI_variable_3,X                ;| A7EBFF | A7 | 

BRA_A7EC02:
    LDA.w #$0001                            ;| A7EC02 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EC05 | A7 | 
    LDA.w #$EB50                            ;| A7EC08 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EC0B | A7 | 
    LDA.w DAT_A7E900                        ;| A7EC0E | A7 | 
    STA.w AI_variable_0,X                    ;| A7EC11 | A7 | 
    LDA.w DAT_A7E902                        ;| A7EC14 | A7 | 
    STA.w AI_variable_1,X                    ;| A7EC17 | A7 | 

BRA_A7EC1A:
    RTL                                     ;| A7EC1A | A7 | 
}

;;; landed on the floor on top after walljumping
;;; $EC1B:  ;;;
{
    DEC.w AI_variable_4,X                    ;| A7EC1B | A7 | 
    BEQ BRA_A7EC22                          ;| A7EC1E | A7 | 
    BPL BRA_A7EC40                          ;| A7EC20 | A7 | 

BRA_A7EC22:
    LDA.w DAT_A7E900                        ;| A7EC22 | A7 | 
    STA.w AI_variable_0,X                    ;| A7EC25 | A7 | 
    LDA.w DAT_A7E902                        ;| A7EC28 | A7 | 
    STA.w AI_variable_1,X                    ;| A7EC2B | A7 | 
    TXY                                     ;| A7EC2E | A7 | 
    LDA.w Param2,X                    ;| A7EC2F | A7 | 
    AND.w #$00FF                            ;| A7EC32 | A7 | 
    ASL                                     ;| A7EC35 | A7 | 
    TAX                                     ;| A7EC36 | A7 | 
    JSR.w ($EC41,X)                         ;| A7EC37 | A7 | 
    LDA.w #$0001                            ;| A7EC3A | A7 | 
    STA.w Instruction_timer,X                    ;| A7EC3D | A7 | 

BRA_A7EC40:
    RTL                                     ;| A7EC40 | A7 | 

    dw $EC47,$EC61,$EC7B
}


;;; $EC47:  ;;;
{
    TYX                                     ;| A7EC47 | A7 | 
    LDA.w #$EC97                            ;| A7EC48 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EC4B | A7 | 
    LDA.w #$E828                            ;| A7EC4E | A7 | 
    STA.w Instruction_list,X                    ;| A7EC51 | A7 | 
    LDA.w Etecoon_X_offset_to_the_left                        ;| A7EC54 | A7 | 
    STA.w AI_variable_2,X                    ;| A7EC57 | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_left                        ;| A7EC5A | A7 | 
    STA.w AI_variable_3,X                ;| A7EC5D | A7 | 
    RTS                                     ;| A7EC60 | A7 | 
}


;;; $EC61:  ;;;
{
    TYX                                     ;| A7EC61 | A7 | 
    LDA.w #$ECBB                            ;| A7EC62 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EC65 | A7 | 
    LDA.w #$E880                            ;| A7EC68 | A7 | 
    STA.w Instruction_list,X                    ;| A7EC6B | A7 | 
    LDA.w Etecoon_X_offset_to_the_right                        ;| A7EC6E | A7 | 
    STA.w AI_variable_2,X                    ;| A7EC71 | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_right                        ;| A7EC74 | A7 | 
    STA.w AI_variable_3,X                ;| A7EC77 | A7 | 
    RTS                                     ;| A7EC7A | A7 | 
}


;;; $EC7B:  ;;;
{
    TYX                                     ;| A7EC7B | A7 | 
    LDA.w #$ED75                            ;| A7EC7C | A7 | 
    STA.w AI_variable_5,X                    ;| A7EC7F | A7 | 
    LDA.w Instruction_list,X                    ;| A7EC82 | A7 | 
    INC                                     ;| A7EC85 | A7 | 
    INC                                     ;| A7EC86 | A7 | 
    STA.w Instruction_list,X                    ;| A7EC87 | A7 | 
    LDA.w Etecoon_X_offset_to_the_right                        ;| A7EC8A | A7 | 
    STA.w AI_variable_2,X                    ;| A7EC8D | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_right                        ;| A7EC90 | A7 | 
    STA.w AI_variable_3,X                ;| A7EC93 | A7 | 
    RTS                                     ;| A7EC96 | A7 | 
}


;;; $EC97:  ;;;
{
    JSR.w MoveEtecoonToTheRight
    LDA.w X_position,X
;    CMP.w #$0219                            ; hardcoded x position to switch to next ai
    CMP.w #$01e7                            ; hardcoded x position to switch to next ai
;    BPL BRA_A7ECBA                          ;| A7ECA0 | A7 | 
    BMI BRA_A7ECBA                          ;| A7ECA0 | A7 | 
    LDA.w #$000B                            ;| A7ECA2 | A7 | 
    STA.w AI_variable_4,X                    ;| A7ECA5 | A7 | 
    LDA.w #$EDC7                            ;| A7ECA8 | A7 | 
    STA.w AI_variable_5,X                    ;| A7ECAB | A7 | 
    LDA.w #$0001                            ;| A7ECAE | A7 | 
    STA.w Instruction_timer,X                    ;| A7ECB1 | A7 | 
    LDA.w #$E854                            ;| A7ECB4 | A7 | 
    STA.w Instruction_list,X                    ;| A7ECB7 | A7 | 

BRA_A7ECBA:
    RTL                                     ;| A7ECBA | A7 | 
}


;;; $ECBB:  ;;;
{
    JSR.w MoveEtecoonToTheRight
    LDA.w X_position,X
;    CMP.w #$0258                            ; hard coded X position, first tile on the cliff
    CMP.w #$01a8                            ; hard coded X position, first tile on the cliff
;    BMI BRA_A7ECDE
    BPL BRA_A7ECDE
    LDA.w #$000B                            ;| A7ECC6 | A7 | 
    STA.w AI_variable_4,X                    ;| A7ECC9 | A7 | 
    LDA.w #$EDC7                            ;| A7ECCC | A7 | 
    STA.w AI_variable_5,X                    ;| A7ECCF | A7 | 
    LDA.w #$0001                            ;| A7ECD2 | A7 | 
    STA.w Instruction_timer,X                    ;| A7ECD5 | A7 | 
    LDA.w #$E854                            ;| A7ECD8 | A7 | 
    STA.w Instruction_list,X                    ;| A7ECDB | A7 | 

BRA_A7ECDE:
    RTL                                     ;| A7ECDE | A7 | 
}

;;; run to the right to the cliff
;;; $ECDF:  ;;;
{
    JSR.w MoveEtecoonToTheRight                        ;| A7ECDF | A7 | 
    LDA.w X_position,X                    ;| A7ECE2 | A7 | 
;    CMP.w #$0258                            ; hard coded X position, first tile on the cliff
    CMP.w #$01a8                            ;| A7ECE5 | A7 | 
;    BMI BRA_A7ED08                          ;| A7ECE8 | A7 | 
    BPL BRA_A7ED08                          ;| A7ECE8 | A7 | 
    LDA.w #$ED09                            ;| A7ECEA | A7 | 
    STA.w AI_variable_5,X                    ;| A7ECED | A7 | 
    LDA.w DAT_A7E904                        ;| A7ECF0 | A7 | 
    STA.w AI_variable_0,X                    ;| A7ECF3 | A7 | 
    LDA.w DAT_A7E906                        ;| A7ECF6 | A7 | 
    STA.w AI_variable_1,X                    ;| A7ECF9 | A7 | 
    LDA.w #$0001                            ;| A7ECFC | A7 | 
    STA.w Instruction_timer,X                    ;| A7ECFF | A7 | 
    LDA.w #$E898                            ;| A7ED02 | A7 | 
    STA.w Instruction_list,X                    ;| A7ED05 | A7 | 

BRA_A7ED08:
    RTL                                     ;| A7ED08 | A7 | 
}

;;; jump to the right into the tunnel (etecoon 280)
;;; $ED09:  ;;;
{
    JSR.w MoveEtecoonToTheRight                        ;| A7ED09 | A7 | 
    JSR.w SUB_A7E983                        ;| A7ED0C | A7 | 
    LDA.w X_position,X                    ;| A7ED0F | A7 | 
;    CMP.w #$02A8                            ;| A7ED12 | A7 | 
    CMP.w #$0158                            ;| A7ED12 | A7 | 
;    BMI BRA_A7ED29                          ;| A7ED15 | A7 | 
    BPL BRA_A7ED29                          ;| A7ED15 | A7 | 
    LDA.w #$0001                            ;| A7ED17 | A7 | 
    STA.w Instruction_timer,X                    ;| A7ED1A | A7 | 
    LDA.w #$E880                            ;| A7ED1D | A7 | 
    STA.w Instruction_list,X                    ;| A7ED20 | A7 | 
    LDA.w #$ED2A                            ;| A7ED23 | A7 | 
    STA.w AI_variable_5,X                    ;| A7ED26 | A7 | 

BRA_A7ED29:
    RTL                                     ;| A7ED29 | A7 | 
}

;;; walk right into the tunnel (etecoon 280)
;;; $ED2A:  ;;;
{
    JSR.w MoveEtecoonToTheRight                        ;| A7ED2A | A7 | 
    LDA.w X_position,X                    ;| A7ED2D | A7 | 
;    CMP.w #$0348                            ;| A7ED30 | A7 | 
    CMP.w #$00b8                            ;| A7ED30 | A7 | 
;    BMI BRA_A7ED53                          ;| A7ED33 | A7 | 
    BPL BRA_A7ED53                          ;| A7ED33 | A7 | 
    LDA.w #$0001                            ;| A7ED35 | A7 | 
    STA.w Instruction_timer,X                    ;| A7ED38 | A7 | 
    LDA.w #$E898                            ;| A7ED3B | A7 | 
    STA.w Instruction_list,X                    ;| A7ED3E | A7 | 
    LDA.w #$ED54                            ;| A7ED41 | A7 | 
    STA.w AI_variable_5,X                    ;| A7ED44 | A7 | 
    LDA.w #$FFFF                            ;| A7ED47 | A7 | 
    STA.w AI_variable_0,X                    ;| A7ED4A | A7 | 
    LDA.w DAT_A7E906                        ;| A7ED4D | A7 | 
    STA.w AI_variable_1,X                    ;| A7ED50 | A7 | 

BRA_A7ED53:
    RTL                                     ;| A7ED53 | A7 | 
}

;;; spin jump to final spot (etecoon 280)
;;; $ED54:  ;;;
{
    JSR.w MoveEtecoonToTheRight                        ;| A7ED54 | A7 | 
    JSR.w SUB_A7E983                        ;| A7ED57 | A7 | 
    BCC BRA_A7ED74                          ;| A7ED5A | A7 | 
    LDA.w #$000B                            ;| A7ED5C | A7 | 
    STA.w AI_variable_4,X                    ;| A7ED5F | A7 | 
    LDA.w #$0001                            ;| A7ED62 | A7 | 
    STA.w Instruction_timer,X                    ;| A7ED65 | A7 | 
    LDA.w #$E854                            ;| A7ED68 | A7 | 
    STA.w Instruction_list,X                    ;| A7ED6B | A7 | 
    LDA.w #$EDC7                            ;| A7ED6E | A7 | 
    STA.w AI_variable_5,X                    ;| A7ED71 | A7 | 

BRA_A7ED74:
    RTL                                     ;| A7ED74 | A7 | 
}


;;; $ED75:  ;;;
{
    JSR.w SUB_A7E958                        ;| A7ED75 | A7 | 
    JSR.w SUB_A7E983                        ;| A7ED78 | A7 | 
    BCS BRA_A7ED7E                          ;| A7ED7B | A7 | 
    RTL                                     ;| A7ED7D | A7 | 

BRA_A7ED7E:
    LDA.w AI_variable_0,X                    ;| A7ED7E | A7 | 
    BPL BRA_A7ED96                          ;| A7ED81 | A7 | 
    STZ.w AI_variable_0,X                    ;| A7ED83 | A7 | 
    STZ.w AI_variable_1,X                    ;| A7ED86 | A7 | 
    LDA.w #$0003                            ;| A7ED89 | A7 | 
    STA.w Instruction_timer,X                    ;| A7ED8C | A7 | 
    LDA.w #$E862                            ;| A7ED8F | A7 | 
    STA.w Instruction_list,X                    ;| A7ED92 | A7 | 
    RTL                                     ;| A7ED95 | A7 | 

BRA_A7ED96:
    LDA.w #$000B                            ;| A7ED96 | A7 | 
    STA.w AI_variable_4,X                    ;| A7ED99 | A7 | 
    LDA.w #$0001                            ;| A7ED9C | A7 | 
    STA.w Instruction_timer,X                    ;| A7ED9F | A7 | 
    LDA.w #$E854                            ;| A7EDA2 | A7 | 
    STA.w Instruction_list,X                    ;| A7EDA5 | A7 | 
    LDA.w Param2,X                    ;| A7EDA8 | A7 | 
    BIT.w #$0002                            ;| A7EDAB | A7 | 
    BNE BRA_A7EDB8                          ;| A7EDAE | A7 | 

BRA_A7EDB0:
    LDA.w #$EDC7                            ;| A7EDB0 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EDB3 | A7 | 
    BRA BRA_A7EDC6                          ;| A7EDB6 | A7 | 

BRA_A7EDB8:
    LDA.w X_position,X                    ;| A7EDB8 | A7 | 
    CMP.w #$0340                            ;| A7EDBB | A7 | 
    BPL BRA_A7EDB0                          ;| A7EDBE | A7 | 
    LDA.w #$EE3E                            ;| A7EDC0 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EDC3 | A7 | 

BRA_A7EDC6:
    RTL                                     ;| A7EDC6 | A7 | 
}


;;; $EDC7:  ;;;
{
    JSR.w SUB_A7E958                        ;| A7EDC7 | A7 | 
    DEC.w AI_variable_4,X                    ;| A7EDCA | A7 | 
    BEQ BRA_A7EDD1                          ;| A7EDCD | A7 | 
    BPL BRA_A7EE3D                          ;| A7EDCF | A7 | 

BRA_A7EDD1:
    LDA.w Param1,X                    ;| A7EDD1 | A7 | 
    CLC                                     ;| A7EDD4 | A7 | 
    ADC.w #$0100                            ;| A7EDD5 | A7 | 
    STA.w Param1,X                    ;| A7EDD8 | A7 | 
    AND.w #$FF00                            ;| A7EDDB | A7 | 
    CMP.w #$0400                            ;| A7EDDE | A7 | 
    BMI BRA_A7EE0E                          ;| A7EDE1 | A7 | 
    LDA.w Param1,X                    ;| A7EDE3 | A7 | 
    AND.w #$00FF                            ;| A7EDE6 | A7 | 
    STA.w Param1,X                    ;| A7EDE9 | A7 | 
    LDA.w Param2,X                    ;| A7EDEC | A7 | 
    BIT.w #$0002                            ;| A7EDEF | A7 | 
    BNE BRA_A7EE0E                          ;| A7EDF2 | A7 | 
    LDA.w #$EE9A                            ;| A7EDF4 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EDF7 | A7 | 
    LDA.w #$E880                            ;| A7EDFA | A7 | 
    STA.w Instruction_list,X                    ;| A7EDFD | A7 | 
    LDA.w Etecoon_X_offset_to_the_right                        ;| A7EE00 | A7 | 
    STA.w AI_variable_2,X                    ;| A7EE03 | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_right                        ;| A7EE06 | A7 | 
    STA.w AI_variable_3,X                ;| A7EE09 | A7 | 
    BRA BRA_A7EE1C                          ;| A7EE0C | A7 | 

BRA_A7EE0E:
    LDA.w #$ED75                            ;| A7EE0E | A7 | 
    STA.w AI_variable_5,X                    ;| A7EE11 | A7 | 
    LDA.w Instruction_list,X                    ;| A7EE14 | A7 | 
    INC                                     ;| A7EE17 | A7 | 
    INC                                     ;| A7EE18 | A7 | 
    STA.w Instruction_list,X                    ;| A7EE19 | A7 | 

BRA_A7EE1C:
    LDA.w DAT_A7E900                        ;| A7EE1C | A7 | 
    STA.w AI_variable_0,X                    ;| A7EE1F | A7 | 
    LDA.w DAT_A7E902                        ;| A7EE22 | A7 | 
    STA.w AI_variable_1,X                    ;| A7EE25 | A7 | 
    LDA.w #$0001                            ;| A7EE28 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EE2B | A7 | 
    LDA.w Samus_X_position                      ;| A7EE2E | A7 | 
    CMP.w #$0100                            ;| A7EE31 | A7 | 
    BMI BRA_A7EE3D                          ;| A7EE34 | A7 | 
    LDA.w #$0033                            ;| A7EE36 | A7 | \
    JSL.l QueueSoundSoundLibrary2MaxQueuedSoundsAllowed6;| A7EE39 | 80 | } Queue sound 33h, sound library 2, max queued sounds allowed = 6 (etecoon cry)

BRA_A7EE3D:
    RTL                                     ;| A7EE3D | A7 | 
}


;;; $EE3E:  ;;;
{
    JSR.w SUB_A7E958                        ;| A7EE3E | A7 | 
    DEC.w AI_variable_4,X                    ;| A7EE41 | A7 | 
    BEQ BRA_A7EE48                          ;| A7EE44 | A7 | 
    BPL BRA_A7EE99                          ;| A7EE46 | A7 | 

BRA_A7EE48:
    LDA.w #$0040                            ;| A7EE48 | A7 | 
    JSL.l IsSamusWithinAPixelRowsOfEnemy    ;| A7EE4B | A0 | 
    TAY                                     ;| A7EE4F | A7 | 
    BEQ BRA_A7EE6A                          ;| A7EE50 | A7 | 
    LDA.w #$0030                            ;| A7EE52 | A7 | 
    JSL.l IsSamusWithinAPixelColumnsOfEnemy ;| A7EE55 | A0 | 
    TAY                                     ;| A7EE59 | A7 | 
    BEQ BRA_A7EE6A                          ;| A7EE5A | A7 | 
    LDA.w #$E880                            ;| A7EE5C | A7 | 
    STA.w Instruction_list,X                    ;| A7EE5F | A7 | 
    LDA.w #$ECDF                            ;| A7EE62 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EE65 | A7 | 
    BRA BRA_A7EE93                          ;| A7EE68 | A7 | 

BRA_A7EE6A:
    LDA.w DAT_A7E900                        ;| A7EE6A | A7 | 
    STA.w AI_variable_0,X                    ;| A7EE6D | A7 | 
    LDA.w DAT_A7E902                        ;| A7EE70 | A7 | 
    STA.w AI_variable_1,X                    ;| A7EE73 | A7 | 
    LDA.w Instruction_list,X                    ;| A7EE76 | A7 | 
    INC                                     ;| A7EE79 | A7 | 
    INC                                     ;| A7EE7A | A7 | 
    STA.w Instruction_list,X                    ;| A7EE7B | A7 | 
    LDA.w #$ED75                            ;| A7EE7E | A7 | 
    STA.w AI_variable_5,X                    ;| A7EE81 | A7 | 
    LDA.w Samus_X_position                      ;| A7EE84 | A7 | 
    CMP.w #$0100                            ;| A7EE87 | A7 | 
    BMI BRA_A7EE93                          ;| A7EE8A | A7 | 
    LDA.w #$0033                            ;| A7EE8C | A7 | \
    JSL.l QueueSoundSoundLibrary2MaxQueuedSoundsAllowed6;| A7EE8F | 80 | } Queue sound 33h, sound library 2, max queued sounds allowed = 6 (etecoon cry)

BRA_A7EE93:
    LDA.w #$0001                            ;| A7EE93 | A7 | 
    STA.w Instruction_timer,X                    ;| A7EE96 | A7 | 

BRA_A7EE99:
    RTL                                     ;| A7EE99 | A7 | 
}


;;; $EE9A:  ;;;
{
    JSR.w MoveEtecoonToTheRight
    LDA.w X_position,X
;    CMP.w #$0258                            ; hardcoded x position to switch to next ai
    CMP.w #$01a8                            ; hardcoded x position to switch to next ai
;    BMI BRA_A7EEB7                          ;| A7EEA3 | A7 | 
    BPL BRA_A7EEB7                          ;| A7EEA3 | A7 | 
    LDA.w #$EEB8                            ;| A7EEA5 | A7 | 
    STA.w AI_variable_5,X                    ;| A7EEA8 | A7 | 
    LDA.w #$0001                            ;| A7EEAB | A7 | 
    STA.w Instruction_timer,X                    ;| A7EEAE | A7 | 
    LDA.w #$E898                            ;| A7EEB1 | A7 | 
    STA.w Instruction_list,X                    ;| A7EEB4 | A7 | 

BRA_A7EEB7:
    RTL                                     ;| A7EEB7 | A7 | 
}


;;; $EEB8:  ;;;
{
    JSR.w MoveEtecoonToTheRight                        ;| A7EEB8 | A7 | 
    JSR.w SUB_A7E983                        ;| A7EEBB | A7 | 
    BCC BRA_A7EEEA                          ;| A7EEBE | A7 | 
    LDA.w Etecoon_X_offset_to_the_left                        ;| A7EEC0 | A7 | 
    STA.w AI_variable_2,X                    ;| A7EEC3 | A7 | 
    LDA.w Etecoon_X_suboffset_to_the_left                        ;| A7EEC6 | A7 | 
    STA.w AI_variable_3,X                ;| A7EEC9 | A7 | 
    LDA.w #$EB02                            ;| A7EECC | A7 | 
    STA.w AI_variable_5,X                    ;| A7EECF | A7 | 
    LDA.w DAT_A7E900                        ;| A7EED2 | A7 | 
    STA.w AI_variable_0,X                    ;| A7EED5 | A7 | 
    LDA.w DAT_A7E902                        ;| A7EED8 | A7 | 
    STA.w AI_variable_1,X                    ;| A7EEDB | A7 | 
    LDA.w #$0001                            ;| A7EEDE | A7 | 
    STA.w Instruction_timer,X                    ;| A7EEE1 | A7 | 
    LDA.w #$E828                            ;| A7EEE4 | A7 | 
    STA.w Instruction_list,X                    ;| A7EEE7 | A7 | 

BRA_A7EEEA:
    RTL                                     ;| A7EEEA | A7 | 
}


;;; $EEEB: RTL ;;;
{
Rtl_EEEB:
    RTL                                     ;| A7EEEB | A7 | 
}


;;; $EEEC: RTL ;;;
{
Rtl_EEEC:
    RTL                                     ;| A7EEEC | A7 | 
}


;;; $EEED: Spritemaps ;;;
{
    dw $0003,$01F2 : db $FF : dw $3329,$C3F5 : db $EF : dw $3300,$C3FA : db $F7 : dw $3302
    dw $0002,$C3F5 : db $F0 : dw $3300,$C3FA : db $F8 : dw $3304
    dw $0002,$C3F5 : db $F1 : dw $3300,$C3FA : db $F9 : dw $3306
    dw $0003,$0000 : db $06 : dw $3326,$01F8 : db $06 : dw $3325,$C3F8 : db $F6 : dw $3308
    dw $0003,$0006 : db $F8 : dw $3327,$0006 : db $00 : dw $3328,$C3F6 : db $F8 : dw $330A
    dw $0003,$0000 : db $F2 : dw $B326,$01F8 : db $F2 : dw $B325,$C3F8 : db $FA : dw $F308
    dw $0003,$01F2 : db $F8 : dw $7327,$01F2 : db $00 : dw $7328,$C3FA : db $F8 : dw $F30A
    dw $0003,$0008 : db $02 : dw $332E,$C3F3 : db $F3 : dw $3300,$C3F8 : db $FA : dw $330E
    dw $0007,$0001 : db $FE : dw $7322,$01F8 : db $FE : dw $3322,$C3F8 : db $F2 : dw $730C,$01F9 : db $01 : dw $3324,$0000 : db $01 : dw $7324,$01F9 : db $FA : dw $3320,$0000 : db $FA : dw $7320
    dw $0007,$01F7 : db $FC : dw $3322,$0002 : db $FC : dw $7322,$C3F8 : db $F1 : dw $730C,$01F9 : db $01 : dw $3323,$0000 : db $01 : dw $7323,$01F9 : db $FA : dw $3320,$0000 : db $FA : dw $7320
    dw $0007,$01F9 : db $01 : dw $3323,$0000 : db $01 : dw $7323,$C3F8 : db $EF : dw $730C,$01F9 : db $F9 : dw $3320,$0000 : db $F9 : dw $7320,$01F5 : db $F9 : dw $3321,$0004 : db $F9 : dw $7321
    dw $0007,$01F9 : db $01 : dw $3323,$0000 : db $01 : dw $7323,$C3F8 : db $EF : dw $730C,$01F9 : db $F9 : dw $3320,$0000 : db $F9 : dw $7320,$01F5 : db $F7 : dw $3321,$0004 : db $F7 : dw $7321
    dw $0007,$C3F8 : db $F0 : dw $3300,$0002 : db $FC : dw $7322,$01F7 : db $FC : dw $3322,$01F9 : db $02 : dw $3324,$0000 : db $02 : dw $7324,$01F9 : db $FA : dw $3320,$0000 : db $FA : dw $7320
    dw $0007,$0002 : db $FC : dw $7322,$01F7 : db $FC : dw $3322,$C3F8 : db $F0 : dw $730C,$01F9 : db $02 : dw $3324,$0000 : db $02 : dw $7324,$01F9 : db $FA : dw $3320,$0000 : db $FA : dw $7320
    dw $0007,$C3F8 : db $F0 : dw $7300,$0002 : db $FC : dw $7322,$01F7 : db $FC : dw $3322,$01F9 : db $02 : dw $3324,$0000 : db $02 : dw $7324,$01F9 : db $FA : dw $3320,$0000 : db $FA : dw $7320
    dw $0005,$C3F6 : db $F2 : dw $3300,$0000 : db $00 : dw $332D,$01F8 : db $00 : dw $332C,$0000 : db $F8 : dw $332B,$01F8 : db $F8 : dw $332A
    dw $0003,$0006 : db $FF : dw $7329,$C3FB : db $EF : dw $7300,$C3F6 : db $F7 : dw $7302
    dw $0002,$C3FB : db $F0 : dw $7300,$C3F6 : db $F8 : dw $7304
    dw $0002,$C3FB : db $F1 : dw $7300,$C3F6 : db $F9 : dw $7306
    dw $0003,$01F8 : db $06 : dw $7326,$0000 : db $06 : dw $7325,$C3F8 : db $F6 : dw $7308
    dw $0003,$01F2 : db $F8 : dw $7327,$01F2 : db $00 : dw $7328,$C3FA : db $F8 : dw $730A
    dw $0003,$01F8 : db $F2 : dw $F326,$0000 : db $F2 : dw $F325,$C3F8 : db $FA : dw $B308
    dw $0003,$0006 : db $F8 : dw $3327,$0006 : db $00 : dw $3328,$C3F6 : db $F8 : dw $B30A
    dw $0003,$01F0 : db $02 : dw $732E,$C3FD : db $F3 : dw $7300,$C3F8 : db $FA : dw $730E
    dw $0007,$01F7 : db $FE : dw $3322,$0000 : db $FE : dw $7322,$C3F8 : db $F2 : dw $330C,$01FF : db $01 : dw $7324,$01F8 : db $01 : dw $3324,$01FF : db $FA : dw $7320,$01F8 : db $FA : dw $3320
    dw $0007,$0001 : db $FC : dw $7322,$01F6 : db $FC : dw $3322,$C3F8 : db $F1 : dw $330C,$01FF : db $01 : dw $7323,$01F8 : db $01 : dw $3323,$01FF : db $FA : dw $7320,$01F8 : db $FA : dw $3320
    dw $0007,$01FF : db $01 : dw $7323,$01F8 : db $01 : dw $3323,$C3F8 : db $EF : dw $330C,$01FF : db $F9 : dw $7320,$01F8 : db $F9 : dw $3320,$0003 : db $F9 : dw $7321,$01F4 : db $F9 : dw $3321
    dw $0007,$01FF : db $01 : dw $7323,$01F8 : db $01 : dw $3323,$C3F8 : db $EF : dw $330C,$01FF : db $F9 : dw $7320,$01F8 : db $F9 : dw $3320,$0003 : db $F7 : dw $7321,$01F4 : db $F7 : dw $3321
    dw $0007,$C3F8 : db $F0 : dw $7300,$01F6 : db $FC : dw $3322,$0001 : db $FC : dw $7322,$01FF : db $02 : dw $7324,$01F8 : db $02 : dw $3324,$01FF : db $FA : dw $7320,$01F8 : db $FA : dw $3320
    dw $0007,$01F6 : db $FC : dw $3322,$0001 : db $FC : dw $7322,$C3F8 : db $F0 : dw $330C,$01FF : db $02 : dw $7324,$01F8 : db $02 : dw $3324,$01FF : db $FA : dw $7320,$01F8 : db $FA : dw $3320
    dw $0007,$C3F8 : db $F0 : dw $3300,$01F6 : db $FC : dw $3322,$0001 : db $FC : dw $7322,$01FF : db $02 : dw $7324,$01F8 : db $02 : dw $3324,$01FF : db $FA : dw $7320,$01F8 : db $FA : dw $3320
    dw $0005,$C3FA : db $F2 : dw $7300,$01F8 : db $00 : dw $732D,$0000 : db $00 : dw $732C,$01F8 : db $F8 : dw $732B,$0000 : db $F8 : dw $732A
}
}


