;;; compile with thedopefish asar
;;; vanilla boulders ai commented

arch 65816
lorom

; org $A19505
; ; Room $A1AD, state $A1BA: Enemy population; billy may
; 
; ; Enemy population format is:
; ;    ____________________________________ Enemy ID
; ;   |      _______________________________ X position
; ;   |     |      __________________________ Y position
; ;   |     |     |      _____________________ Initialisation parameter (orientation in SMILE)
; ;   |     |     |     |      ________________ Properties (special in SMILE)
; ;   |     |     |     |     |      ___________ Extra properties (special graphics bitset in SMILE)
; ;   |     |     |     |     |     |      ______ Parameter 1 (speed in SMILE)
; ;   |     |     |     |     |     |     |      _ Parameter 2 (speed2 in SMILE)
; ;   |     |     |     |     |     |     |     |
; ;   iiii  xxxx  yyyy  oooo  pppp  gggg  aaaa  bbbb
; dw $DFBF,$00B0,$00C0,$0080,$2000,$0000,$0200,$A050
; dw $DFBF,$0110,$00C0,$0080,$2000,$0000,$0200,$A050
; dw $DFBF,$0174,$00C0,$0080,$2000,$0000,$0200,$A050
; dw $FFFF : db $00
	
;; Room $B6EE, state $B6FB: Enemy population; firefleas
;$A1:AB80
;      DFBF,0150,0130,0050,2000,0000,0000,0080, 
;      DFBF,01B8,01D0,0050,2800,0000,0100,0080, 
;      DFBF,0128,0260,0050,2800,0000,0000,0080, 


;; Room $D51E, state $D52B: Enemy population; sand pit
;$A1:DF63
;     DFBF,0190,00A0,0072,2800,0000,0200,7204, 
;     DFBF,0150,00C0,0098,2800,0000,0200,A204, 
;     DFBF,00D0,00D0,00C0,2800,0000,0200,A204, 
;
;; Room $D4EF, state $D4FC: Enemy population; sand pit
;$A1:DF96
;     DFBF,01D0,0090,0050,2800,0000,0200,6204, 
;     DFBF,00B0,0140,0080,2800,0000,0200,A004, 
;     DFBF,00F0,0160,00F0,2800,0000,0200,F004, 
;     DFBF,0030,0090,0040,2800,0000,0200,5204, 

ASamusYPositionMinusEnemyYPosition = $A0AEDD
ASamusXPositionMinusEnemyXPosition = $A0AEE5

EnemyIndex = $7E0E54

X_position = $7E0F7A
Y_position = $7E0F7E
Y_subposition = $7E0F80
Init_param = $7E0F92            ; low: y radius
Instruction_list = $7E0F92      ; for drawing


AI_variable_0 = $7E0FA8
AI_variable_1 = $7E0FAA
AI_variable_2 = $7E0FAC
AI_variable_3 = $7E0FAE
AI_variable_4 = $7E0FB0         ; boulder direction
Boulder_direction_P1H = $7E0FB0         ; boulder direction (high byte of param 1)
AI_variable_5 = $7E0FB2

Param1 = $7E0FB4
Param1_high = $7E0FB5           ; direction (high byte)
Param2 = $7E0FB6                ; x radius (low byte)
Param2_high = $7E0FB7           ; if == 0 then store 1 in Extra_RAM_flag

Extra_RAM_neg_X_radius_P2L = $7E7800
Extra_RAM_unknown_P1L = $7E7802
Extra_RAM_Y_subposition = $7E7804
Extra_RAM_Y_position1 = $7E7806
Extra_RAM_X_position = $7E7808
Extra_RAM_Y_position2_P2H = $7E780A
Extra_RAM_Y_radius_PIL = $7E780C
Extra_RAM_flag = $7E780E

org $a686F5
;;; $86F5: Initialisation AI - enemy $DFBF (boulder) ;;;
{
InitialisationAiEnemyDfbfBoulder:
    LDX.w EnemyIndex                        ; 
    STZ.w AI_variable_2,X                    ; zero in ai2
    LDA.w #$0000                            ; 
    STA.w AI_variable_1,X                    ; zero in ai1
    LDA.w #$0002                            ; 
    STA.w AI_variable_3,X                ; 2 in ai3
    LDA.w #$879A                            ; 
    STA.w AI_variable_0,X                    ; pointer to boulder main ai
    LDA.w X_position,X                    ; 
    STA.l Extra_RAM_X_position,X             ; x pos in extra ram x pos
    LDA.w Y_position,X                ; 
    STA.l Extra_RAM_Y_position2_P2H,X                     ; y pos in extra ram y pos
    STA.l Extra_RAM_Y_position1,X                     ; 
    LDA.w Y_subposition,X                    ; 
    STA.l Extra_RAM_Y_subposition,X                     ; 
    LDA.w Param2_high,X                  ; param 2 high byte
    AND.w #$00FF                            ; keep only byte
    BNE BRA_A68735                          ; if != 0 continue
    LDA.w #$0001                            ; store 1 in extra ram param flag (for horizontal boulders in firefleas)
    STA.l Extra_RAM_flag,X                     ; 

BRA_A68735:
    EOR.w #$FFFF                            ; get negative value of param2 high byte (or 1 for firefleas boulders)
    INC                                     ; 
    CLC                                     ; 
    ADC.l Extra_RAM_Y_position2_P2H,X           ; add negative value of param2 high byte to Y pos
    STA.w Y_position,X                      ; update Y position of boulder
    LDA.w Param2,X                          ; load param2
    AND.w #$00FF                            ; keep low byte
    EOR.w #$FFFF                            ; get negative value
    INC                                     ; 
    STA.l Extra_RAM_neg_X_radius_P2L,X            ; store in extra ram
    LDA.w Init_param,X                    ; load init param low byte
    AND.w #$00FF                            ; 
    STA.l Extra_RAM_Y_radius_PIL,X            ; store in extra ram
    LDA.w #$86A7                            ; load instruction list in init param (rolling left)
    STA.w Instruction_list,X                    ; 
    LDA.w Param1_high,X                  ; load high byte of param1
    AND.w #$00FF                            ; 
    STA.w Boulder_direction_P1H,X                    ; 2 for falling boulders, 0 or 1 for right/left boulders
    BNE BRA_A6877C                          ; 
    LDA.l Extra_RAM_neg_X_radius_P2L,X            ; right boulder, negate again radius
    EOR.w #$FFFF                            ; 
    INC                                     ; 
    STA.l Extra_RAM_neg_X_radius_P2L,X       ; 
    LDA.w #$86CB                            ; load instruction list in init param (rolling right)
    STA.w Instruction_list,X                    ; 

BRA_A6877C:
    LDA.w #$0002                            ; 
    STA.l Extra_RAM_unknown_P1L,X               ; store 2 in unknown extra ram param if low byte of param 1 is == 0
    LDA.w Param1,X                          ; get low byte of parameter 1
    AND.w #$00FF                            ; 
    BEQ .end
    LDA.w #$0005                            ; store 5 in unknown extra ram param if low byte of param 1 is != 0
    STA.l Extra_RAM_unknown_P1L,X               ; 

.end:
    RTL                                     ;
}


;;; $8793: Main AI - enemy $DFBF (boulder) ;;;
{
MainAiEnemyDfbfBoulder:
    LDX.w EnemyIndex                        ; 
    JSR.w (AI_variable_0,X)                  ; 
    RTL                                     ; 
}


org $A6879A
FirstBoulderAiFunction:
;;; $879A:  ;;;
{
    LDX.w EnemyIndex                        ; 
    JSL.l ASamusYPositionMinusEnemyYPosition     ; > 0 if samus is under boulder, < 0 is above boulder
    BMI .end                          ; samus above boulder
    CMP.l Extra_RAM_Y_radius_PIL,X                     ; check if samus is inside Y radius
    BPL .end                          ; samus not inside Y radius
    LDA.w Boulder_direction_P1H,X                    ; 0: right, 1: left, 2: down
    BNE .BRA_A687CE                          ; 
    JSL.l ASamusXPositionMinusEnemyXPosition     ; boulder direction right
    BMI .end                          ; samus on left of boulder -> end ; $A6:87B2
    CMP.l Extra_RAM_neg_X_radius_P2L,X       ; samus on right of boulder, check if in X radius
    BPL .end                          ; if not en
    LDA.w #$87ED                            ; load new AI pointer
    STA.w AI_variable_0,X                    ; 
    LDA.l Extra_RAM_flag,X                     ; set to 1 if param 2 high byte == 0 (only in firefleas)
    BEQ .end                          ; 
    LDA.w #$8942                            ; for boulder with direction right and param high byte != 0, should not happen
    STA.w AI_variable_0,X                    ; 
    BRA .end                          ; 

.BRA_A687CE                                  ; boulder direction left or down
    JSL.l ASamusXPositionMinusEnemyXPosition     ; if > 0 samus on the right side of the boulder, if < 0 samus on the left side of the boulder
    BPL .end                          ; on the right side, do nothing
    CMP.l Extra_RAM_neg_X_radius_P2L,X       ; on the left side, check X radius
    BMI .end                          ; not in radius, end
    LDA.w #$87ED                            ; load new ai pointer
    STA.w AI_variable_0,X                    ; 
    LDA.l Extra_RAM_flag,X                     ; set to 1 if param 2 high byte == 0 (only in firefleas)
    BEQ .end                          ; 
    LDA.w #$8942                            ; load new ai pointer for firefleas rolling boulders
    STA.w AI_variable_0,X                    ; 

.end
    RTS                                     ;
}
