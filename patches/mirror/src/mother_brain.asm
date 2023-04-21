;;; compile with thedopefish asar
;;; fix mother brain screen and mirror it

arch 65816
lorom

;;; vanilla samus detection to trigger MB2
; $A9:87F1 AD F6 0A    LDA $0AF6  [$7E:0AF6]  ;\
; $A9:87F4 C9 EC 00    CMP #$00EC             ;} If [Samus X position] < ECh:
; $A9:87F7 10 1F       BPL $1F    [$8818]     ;/
org $a987f4
        cmp #$0314
        bmi $1F

;;; set mb screen scroll to red
; $A9:8836 AF 20 CD 7E LDA $7ECD20[$7E:CD20]  ;\
; $A9:883A 29 FF 00    AND #$00FF             ;} Scroll 1 = red
; $A9:883D 8F 20 CD 7E STA $7ECD20[$7E:CD20]  ;/
org $a98836
        lda $7ECD22
        and #$FF00
        sta $7ECD22

;;; fake death explosions
; $A9:8929             dw 0088,0074,
;                         0078,0084,
;                         007C,005A,
;                         008A,0092,
;                         0078,0034,
;                         007C,00AA,
;                         008A,0048,
;                         0078,00CE
org $a98929
        dw $0378,$0074
        dw $0388,$0084
        dw $0384,$005A
        dw $0376,$0092
        dw $0388,$0034
        dw $0384,$00AA
        dw $0376,$0048
        dw $0388,$00CE

;;; $896E: Mother brain body subfunction - clear bottom-left tube ;;;
; $A9:896E 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:8972             dx 05,09,B6C3          ;} Spawn PLM to clear Mother Brain's bottom-left tube
org $A98972
        db $35

;;; $8A22: Mother brain body subfunction - clear bottom-middle-left tube ;;;
; $A9:8A22 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:8A26             dx 06,0A,B6BB          ;} Spawn PLM to clear Mother Brain's bottom-middle-side tube
org $A98A26
        db $36

;;; $8AAE: Mother brain body subfunction - clear bottom-middle-right tube ;;;
; $A9:8AAE 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:8AB2             dx 09,0A,B6BB          ;} Spawn PLM to clear Mother Brain's bottom-middle-side tube
org $A98AB2
	db $39

;;; $8AD6: Mother brain body subfunction - clear bottom-middle tubes ;;;
; $A9:8AD6 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:8ADA             dx 07,07,B6BF          ;} Spawn PLM to clear Mother Brain's bottom-middle tubes
org $A98ADA
	db $37

;;; $89FA: Mother brain body subfunction - clear bottom-right tube ;;;
; $A9:89FA 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:89FE             dx 0A,09,B6C7          ;} Spawn PLM to clear Mother Brain's bottom-right tube
org $A989FE
	db $3a

;;; $89D2: Mother brain body subfunction - clear ceiling block column 6 ;;;
; $A9:89D2 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:89D6             dx 06,02,B6B3          ;} Spawn PLM to clear ceiling block
org $A989D6
        db $36

;;; $8A54: Mother brain body subfunction - clear ceiling tube column 7 ;;;
; $A9:8A54 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:8A58             dx 07,02,B6B7          ;} Spawn PLM to clear ceiling tube
org $A98A58
        db $38

;;; $8A86: Mother brain body subfunction - clear ceiling tube column 8 ;;;
; $A9:8A86 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:8A8A             dx 08,02,B6B7          ;} Spawn PLM to clear ceiling tube
org $A98A8A
        db $37

;;; $89A0: Mother brain body subfunction - clear ceiling block column 9 ;;;
; $A9:89A0 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:89A4             dx 09,02,B6B3          ;} Spawn PLM to clear ceiling block
org $A989A4
	db $39

;;; $8884: Mother Brain body function - fake death - descent - begin screen flashing and lower acid ;;;
; $A9:88A9 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:88AD             dx 0E,02,B6B3          ;} Spawn PLM to clear ceiling block
org $A988AD
        db $31

;;; $CC5B: Enemy projectiles - Mother Brain's top tube falling ;;;
; ;                        __________________________________ Initialisation AI
; ;                       |     _____________________________ Pre-instruction
; ;                       |    |     ________________________ Instruction list
; ;                       |    |    |     ___________________ X radius
; ;                       |    |    |    |   ________________ Y radius
; ;                       |    |    |    |  |   _____________ Properties
; ;                       |    |    |    |  |  |     ________ Hit instruction list
; ;                       |    |    |    |  |  |    |     ___ Shot instruction list
; ;                       |    |    |    |  |  |    |    |
; $86:CC5B             dx CBC9,CBE7,CC43,08,10,5000,0000,84FC ; Mother Brain's top-right tube falling
; $86:CC69             dx CBC9,CBE7,CC49,08,10,5000,0000,84FC ; Mother Brain's top-left tube falling
; $86:CC77             dx CBC9,CBE7,CC4F,08,18,5000,0000,84FC ; Mother Brain's top-middle-left tube falling
; $86:CC85             dx CBC9,CBE7,CC55,08,18,5000,0000,84FC ; Mother Brain's top-middle-right tube falling

;;; $C684: Initialisation AI - enemy projectile $CB75 (Mother Brain's death beam - fired) ;;;
; $86:C70E BD 4B 1A    LDA $1A4B,x[$7E:1A59]  ;\
; $86:C711 C9 02 00    CMP #$0002             ;|
; $86:C714 30 1C       BMI $1C    [$C732]     ;} If 2 <= [enemy projectile X position] < EEh:
; $86:C716 C9 EE 00    CMP #$00EE             ;|
; $86:C719 10 17       BPL $17    [$C732]     ;/
org $86C711
        CMP #$0302
org $86C716
        CMP #$03EE

;;; $C84D: Pre-instruction - enemy projectile $CB91/$CB9F (Mother Brain's drool) ;;;
; X/Y position offsets
; $86:C86E             dw 0006,0014,
;                         000E,0012,
;                         0008,0017,
;                         000A,0013,
;                         000B,0019,
;                         000C,0012
org $86C86E
        dw $FFFA,$0014
        dw $FFF2,$0012
        dw $FFF8,$0017
        dw $FFF6,$0013
        dw $FFF5,$0019
        dw $FFF4,$0012

;;; $8983: Mother brain body subfunction - spawn top-right tube falling enemy projectile ;;;
; $A9:8988 A9 98 00    LDA #$0098             ;\
; $A9:898B 85 12       STA $12    [$7E:0012]  ;} $12 = 98h
; $A9:898D A9 2F 00    LDA #$002F             ;\
; $A9:8990 85 14       STA $14    [$7E:0014]  ;} $14 = 2Fh
; $A9:8992 A0 5B CC    LDY #$CC5B             ;\
; $A9:8995 22 97 80 86 JSL $868097[$86:8097]  ;} Spawn Mother Brain's top-right tube falling enemy projectile
org $A98988
        lda #$0398

;;; $89B5: Mother brain body subfunction - spawn top-left tube falling enemy projectile ;;;
; $A9:89BA A9 68 00    LDA #$0068             ;\
; $A9:89BD 85 12       STA $12    [$7E:0012]  ;} $12 = 68h
; $A9:89BF A9 2F 00    LDA #$002F             ;\
; $A9:89C2 85 14       STA $14    [$7E:0014]  ;} $14 = 2Fh
; $A9:89C4 A0 69 CC    LDY #$CC69             ;\
; $A9:89C7 22 97 80 86 JSL $868097[$86:8097]  ;} Spawn Mother Brain's top-left tube falling enemy projectile
org $A989BA
        lda #$0368

;;; $8A37: Mother brain body subfunction - spawn top-middle-left tube falling enemy projectile ;;;
; $A9:8A3C A9 78 00    LDA #$0078             ;\
; $A9:8A3F 85 12       STA $12    [$7E:0012]  ;} $12 = 78h
; $A9:8A41 A9 3B 00    LDA #$003B             ;\
; $A9:8A44 85 14       STA $14    [$7E:0014]  ;} $14 = 3Bh
; $A9:8A46 A0 77 CC    LDY #$CC77             ;\
; $A9:8A49 22 97 80 86 JSL $868097[$86:8097]  ;} Spawn Mother Brain's top-middle-left tube falling enemy projectile
org $A98A3C
        lda #$0388

;;; $8A69: Mother brain body subfunction - spawn top-middle-right tube falling enemy projectile ;;;
; $A9:8A6E A9 88 00    LDA #$0088             ;\
; $A9:8A71 85 12       STA $12    [$7E:0012]  ;} $12 = 88h
; $A9:8A73 A9 3B 00    LDA #$003B             ;\
; $A9:8A76 85 14       STA $14    [$7E:0014]  ;} $14 = 3Bh
; $A9:8A78 A0 85 CC    LDY #$CC85             ;\
; $A9:8A7B 22 97 80 86 JSL $868097[$86:8097]  ;} Spawn Mother Brain's top-middle-right tube falling enemy projectile
org $A98A6E
        lda #$0378

;;; mb tubes falling
;;; $8AE5: Mother Brain's tubes falling enemy population entries ;;;
; ;                        ____________________________________ Enemy ID
; ;                       |     _______________________________ X position
; ;                       |    |     __________________________ Y position
; ;                       |    |    |     _____________________ Initialisation list pointer
; ;                       |    |    |    |     ________________ Properties
; ;                       |    |    |    |    |     ___________ Extra properties
; ;                       |    |    |    |    |    |     ______ Parameter 1
; ;                       |    |    |    |    |    |    |     _ Parameter 2
; ;                       |    |    |    |    |    |    |    |
; $A9:8AE5             dw ECFF,0060,00B3,8C69,A000,0000,0000,0000 ; Bottom left
; $A9:8AF5             dw ECFF,00A0,00B3,8C6F,A000,0000,0002,0000 ; Bottom right
; $A9:8B05             dw ECFF,0068,00BB,8C75,A000,0000,0004,0000 ; Bottom-middle-left
; $A9:8B15             dw ECFF,0098,00BB,8C7B,A000,0000,0006,0000 ; Bottom-middle-right
; $A9:8B25             dw ECFF,0080,00A7,8C81,A800,0000,0008,0020 ; Main tube
org $a98ae5+2
        dw $0360
org $a98af5+2
        dw $03a0
org $a98b05+2
        dw $0368
org $a98b1+2
        dw $0398
org $a98b25+2
        dw $0380

;;; $8BD6: Mother Brain's tubes falling function - main tube - falling ;;;
; $A9:8C1B A9 3B 00    LDA #$003B             ;\
; $A9:8C1E 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;} Mother Brain's body X position = 3Bh
org $a98c1b
        lda #$03c5
	
;;; $8C87: Mother Brain's body function - fake death - ascent - draw room background on BG1 - rows 2/3 ;;;
org $A98C8B
        db $31
org $A98C93
        db $31
org $A98Ca2
        db $31
org $A98Caa
        db $31
org $A98Cb9
        db $31
org $A98Cc1
        db $31
org $A98Cd0
        db $31
org $A98Cd8
        db $31
org $A98Ce7
        db $31
org $A98Cef
        db $31
org $A98Cfe
        db $31
org $A98d06
        db $31

;;; $8DC3: Mother Brain's body function - fake death - ascent - continue pausing for suspense ;;;
; $A9:8DC8 A9 3B 00    LDA #$003B             ;\
; $A9:8DCB 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;} Mother Brain's body X position = 3Bh
org $A98DC8
        lda #$03c5
; $A9:8DD4 A9 E5 FF    LDA #$FFE5             ;\
; $A9:8DD7 85 B5       STA $B5    [$7E:00B5]  ;} BG2 X scroll = -1Bh
org $A98DD4                     ; first called before rising
        lda #$ff98

;;; $8DEC: Mother Brain's body function - fake death - ascent - start music and earthquake ;;;
; $A9:8E01 A9 3B 00    LDA #$003B             ;\
; $A9:8E04 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;} Mother Brain's body X position = 3Bh
org $A98E01
	lda #$03c5
; $A9:8E0D A9 E5 FF    LDA #$FFE5             ;\
; $A9:8E10 85 B5       STA $B5    [$7E:00B5]  ;} BG2 X scroll = -1Bh
org $A98E0D
        lda #$ff98              ; 2nd called before rising

;;; $8F46: Spawn dust clouds for Mother Brain's ascent ;;;
; $A9:8F7F             dw 003D, 0054, 0020, 0035, 005A, 0043, 0067, 0029
org $A98F7F
	dw $03C3, $03AC, $03E0, $03CB, $03A6, $03BD, $0399, $03D7

;;; $91B8: Handle Mother Brain's neck ;;;
; $A9:91B8 A9 B0 FF    LDA #$FFB0             ;\
; $A9:91BB 18          CLC                    ;|
; $A9:91BC 6D 7A 0F    ADC $0F7A  [$7E:0F7A]  ;} $7E:7814 = [Mother Brain's body X position] - 50h
org $A991B8
        lda #$0050
; $A9:91E3 AF 48 80 7E LDA $7E8048[$7E:8048]  ;\
; $A9:91E7 22 60 C4 A9 JSL $A9C460[$A9:C460]  ;|
org $A991E7
        jsl compute_neg_sinus
; $A9:91EC 6F 14 78 7E ADC $7E7814[$7E:7814]  ;} Mother Brain's neck segment 0 X position = [$7E:7814] + 70h + ±[Mother Brain's neck segment 0 distance] * sin([$12] * pi / 80h)
; $A9:91F0 18          CLC                    ;|
; $A9:91F1 69 70 00    ADC #$0070             ;|
org $A991F1
        adc #$ff90
; $A9:920D AF 4E 80 7E LDA $7E804E[$7E:804E]  ;\
; $A9:9211 22 60 C4 A9 JSL $A9C460[$A9:C460]  ;|
org $A99211
        jsl compute_neg_sinus
; $A9:9216 6F 14 78 7E ADC $7E7814[$7E:7814]  ;} Mother Brain's neck segment 1 X position = [$7E:7814] + 70h + ±[Mother Brain's neck segment 1 distance] * sin([$12] * pi / 80h)
; $A9:921A 18          CLC                    ;|
; $A9:921B 69 70 00    ADC #$0070             ;|
org $A9921B
        adc #$ff90
; $A9:9237 AF 54 80 7E LDA $7E8054[$7E:8054]  ;\
; $A9:923B 22 60 C4 A9 JSL $A9C460[$A9:C460]  ;|
org $A9923B
        jsl compute_neg_sinus
; $A9:9240 6F 14 78 7E ADC $7E7814[$7E:7814]  ;} Mother Brain's neck segment 2 X position = [$7E:7814] + 70h + ±[Mother Brain's neck segment 2 distance] * sin([$12] * pi / 80h)
; $A9:9244 18          CLC                    ;|
; $A9:9245 69 70 00    ADC #$0070             ;|
org $A99245
        adc #$ff90
; $A9:926A AF 5A 80 7E LDA $7E805A[$7E:805A]  ;\
; $A9:926E 22 60 C4 A9 JSL $A9C460[$A9:C460]  ;|
; $A9:9272 18          CLC                    ;} Mother Brain's neck segment 3 X position = [Mother Brain's neck segment 2 X position] + ±[Mother Brain's neck segment 3 distance] * sin([$12] * pi / 80h)
org $A9926E
        jsl compute_neg_sinus
; $A9:928C AF 60 80 7E LDA $7E8060[$7E:8060]  ;\
; $A9:9290 22 60 C4 A9 JSL $A9C460[$A9:C460]  ;|
; $A9:9294 18          CLC                    ;} Mother Brain's neck segment 4 X position = [Mother Brain's neck segment 2 X position] + ±[Mother Brain's neck segment 4 distance] * sin([$12] * pi / 80h)
org $A99290
	jsl compute_neg_sinus

;;; $9357: Draw Mother Brain's brain ;;;
; $A9:9397 29 06 00    AND #$0006             ;\
; $A9:939A AA          TAX                    ;} X = [A] & 6
; $A9:939B BD BB 93    LDA $93BB,x[$A9:93BB]  ;\
; $A9:939E 18          CLC                    ;|
; $A9:939F 6D BA 0F    ADC $0FBA  [$7E:0FBA]  ;} $12 = [Mother Brain brain X position] + [$93BB + [X]] (shake X offset)
; $A9:93A2 85 12       STA $12    [$7E:0012]  ;/
; $A9:93A4 18          CLC                    ;\
; $A9:93A5 69 20 00    ADC #$0020             ;|
; $A9:93A8 38          SEC                    ;} If [$12] + 20h - [layer 1 X position] < 0: return
; $A9:93A9 ED 11 09    SBC $0911  [$7E:0911]  ;|
; $A9:93AC 30 0C       BMI $0C    [$93BA]     ;/
;;; substract 1 screen (0x100) and half mb lenght (0x20)
org $A993A5
        ADC #$fee0
org $A993AC
        BPL $0C

;;; $9552: Move Mother Brain's body down by [A], scroll it left by [X] ;;;
; $A9:9566 69 22 00    ADC #$0022             ;|
; $A9:9569 85 14       STA $14    [$7E:0014]  ;|
; $A9:956B AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;|
; $A9:956E 49 FF FF    EOR #$FFFF             ;} BG2 X scroll = 22h - [Mother Brain's body X position] + [X]
; $A9:9571 1A          INC A                  ;|
; $A9:9572 18          CLC                    ;|
; $A9:9573 65 14       ADC $14    [$7E:0014]  ;|
; $A9:9575 85 B5       STA $B5    [$7E:00B5]  ;/
;;; 3rd called after rising
org $A99566
        ADC #$0060

;;; $9579: Move Mother Brain's body down by [A] ;;;
; $A9:958B A9 00 00    LDA #$0000             ;\
; $A9:958E 38          SEC                    ;|
; $A9:958F ED 7A 0F    SBC $0F7A  [$7E:0F7A]  ;|
; $A9:9592 18          CLC                    ;} BG2 X scroll = 22h - [Mother Brain's body X position]
; $A9:9593 69 22 00    ADC #$0022             ;|
;;; 4th called after rising
org $A99593
        ADC #$0060

;;; $95B6: Instruction - move Mother Brain's body up by 10px, scroll it left by 4px ;;;
; $A9:95B7 A2 04 00    LDX #$0004
org $A995B7
        ldx #$fffc

;;; $95C0: Instruction - move Mother Brain's body up by 16px, scroll it left by 4px ;;;
; $A9:95C1 A2 04 00    LDX #$0004
org $A995C1
        ldx #$fffc

;;; $95CA: Instruction - move Mother Brain's body up by 12px, scroll it right by 2px ;;;
; $A9:95CB A2 FE FF    LDX #$FFFE
org $A995CB
	ldx #$0002

;;; $95D4: Unused. Instruction - scroll Mother Brain's body right by 2px ;;;
; $A9:95D5 A2 FE FF    LDX #$FFFE
org $A995D5
	ldx #$0002

;;; $95DE: Instruction - move Mother Brain's body down by 12px, scroll it left by 4px ;;;
; $A9:95DF A2 04 00    LDX #$0004
org $A995DF
        ldx #$fffc

;;; $95E8: Instruction - move Mother Brain's body down by 16px, scroll it right by 2px ;;;
; $A9:95E9 A2 FE FF    LDX #$FFFE
org $A995E9
        ldx #$0002

;;; $95F2: Instruction - move Mother Brain's body down by 10px, scroll it right by 2px ;;;
; $A9:95F3 A2 FE FF    LDX #$FFFE
org $A995F3
        ldx #$0002

;;; $95FC: Instruction - move Mother Brain's body up by 2px and right by 1px ;;;
; $A9:95FC AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:95FF 18          CLC                    ;|
; $A9:9600 69 01 00    ADC #$0001             ;} Mother Brain's body X position += 1
; $A9:9603 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A99600
        ADC #$ffff

;;; $960C: Instruction - move Mother Brain's body right by 2px ;;;
; $A9:960C AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:960F 18          CLC                    ;|
; $A9:9610 69 02 00    ADC #$0002             ;} Mother Brain's body X position += 2
; $A9:9613 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A99610
        ADC #$fffe

;;; $9622: Instruction - move Mother Brain's body up by 1px and right by 3px, do footstep effect ;;;
; $A9:9628 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:962B 18          CLC                    ;|
; $A9:962C 69 03 00    ADC #$0003             ;} Mother Brain's body X position += 3
; $A9:962F 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A9962C
        ADC #$fffd

;;; $9638: Instruction - move Mother Brain's body down by 2px and right by 15px ;;;
; $A9:9638 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:963B 18          CLC                    ;|
; $A9:963C 69 0F 00    ADC #$000F             ;} Mother Brain's body X position += 15
; $A9:963F 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A9963C
        ADC #$fff1

;;; $9648: Instruction - move Mother Brain's body down by 4px and right by 6px ;;;
; $A9:9648 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:964B 18          CLC                    ;|
; $A9:964C 69 06 00    ADC #$0006             ;} Mother Brain's body X position += 6
; $A9:964F 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A9964C
        ADC #$fffa

;;; $9658: Instruction - move Mother Brain's body up by 4px and left by 2px ;;;
; $A9:9658 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:965B 18          CLC                    ;|
; $A9:965C 69 FE FF    ADC #$FFFE             ;} Mother Brain's body X position -= 2
; $A9:965F 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A9965C
        ADC #$0002

;;; $9668: Instruction - move Mother Brain's body up by 2px and left by 1px, do footstep effect ;;;
; $A9:966E AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:9671 18          CLC                    ;|
; $A9:9672 69 FF FF    ADC #$FFFF             ;} Mother Brain's body X position -= 1
; $A9:9675 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A99672
        ADC #$0001

;;; $967E: Instruction - move Mother Brain's body up by 2px and left by 1px, do footstep effect ;;;
; $A9:9684 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:9687 38          SEC                    ;|
; $A9:9688 E9 01 00    SBC #$0001             ;} Mother Brain's body X position -= 1
; $A9:968B 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A99688
        SBC #$ffff

;;; $9694: Instruction - move Mother Brain's body left by 2px ;;;
; $A9:9694 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:9697 38          SEC                    ;|
; $A9:9698 E9 02 00    SBC #$0002             ;} Mother Brain's body X position -= 2
; $A9:969B 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A99698
        SBC #$fffe

;;; $96AA: Instruction - move Mother Brain's body down by 1px and left by 3px ;;;
; $A9:96AA AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:96AD 38          SEC                    ;|
; $A9:96AE E9 03 00    SBC #$0003             ;} Mother Brain's body X position -= 3
; $A9:96B1 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A996AE
        SBC #$fffd

;;; $96BA: Instruction - move Mother Brain's body up by 2px and left by 15px, do footstep effect ;;;
; $A9:96C0 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:96C3 38          SEC                    ;|
; $A9:96C4 E9 0F 00    SBC #$000F             ;} Mother Brain's body X position -= 15
; $A9:96C7 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A996C4
	SBC #$fff1

;;; $96D0: Instruction - move Mother Brain's body up by 4px and left by 6px ;;;
; $A9:96D0 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:96D3 38          SEC                    ;|
; $A9:96D4 E9 06 00    SBC #$0006             ;} Mother Brain's body X position -= 6
; $A9:96D7 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A996D4
        SBC #$fffa

;;; $96E0: Instruction - move Mother Brain's body down by 4px and right by 2px ;;;
; $A9:96E0 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:96E3 38          SEC                    ;|
; $A9:96E4 E9 FE FF    SBC #$FFFE             ;} Mother Brain's body X position += 2
; $A9:96E7 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A996E4
        SBC #$0002

;;; $96F0: Instruction - move Mother Brain's body down by 2px and right by 1px ;;;
; $A9:96F0 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:96F3 38          SEC                    ;|
; $A9:96F4 E9 FF FF    SBC #$FFFF             ;} Mother Brain's body X position += 1
; $A9:96F7 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;/
org $A996F4
        SBC #$0001

;;; $9A42: Instruction list - Mother Brain's body - death beam mode ;;;
; $A9:9A42             dx 9720,                   ; Mother Brain's pose = death beam mode
;                         0001,9FA0,
;                         0001,A384,
;                         0001,A3CE,
;                         9AC8,0024,FFD8,0001,    ; Spawn enemy projectile $E509 to offset (24h, FFD8h) with parameter 1
;                         0001,A3CE,
;                         9AC8,0022,FFD6,0002,    ; Spawn enemy projectile $E509 to offset (22h, FFD6h) with parameter 2
;                         0001,A3CE,
;                         9AC8,0024,FFD8,0001,    ; Spawn enemy projectile $E509 to offset (24h, FFD8h) with parameter 1
;                         0001,A3CE,
;                         9AC8,0022,FFD6,0002,    ; Spawn enemy projectile $E509 to offset (22h, FFD6h) with parameter 2
;                         0001,A3CE,
;                         9AC8,0024,FFD8,0001,    ; Spawn enemy projectile $E509 to offset (24h, FFD8h) with parameter 1
;                         0001,A3CE,
;                         9AC8,0022,FFD6,0002,    ; Spawn enemy projectile $E509 to offset (22h, FFD6h) with parameter 2
;                         0001,A3CE,
;                         9AC8,0024,FFD8,0001,    ; Spawn enemy projectile $E509 to offset (24h, FFD8h) with parameter 1
;                         0001,A3CE,
;                         9AC8,0022,FFD6,0002,    ; Spawn enemy projectile $E509 to offset (22h, FFD6h) with parameter 2
;;; the charging small explosion on mb body when firing death beam
org $A99A52
        dw $ffdc
org $A99A5E
        dw $ffde
org $A99A6A
        dw $ffdc
org $A99A76
        dw $ffde
org $A99A82
        dw $ffdc
org $A99A8E
        dw $ffde
org $A99A9A
        dw $ffdc
org $A99AA6
        dw $ffde

;;; $9E37: Instruction - aim Mother Brain blue rings at Shitroid ;;;
; $A9:9E3E BD 7A 0F    LDA $0F7A,x[$7E:0FFA]  ;\
; $A9:9E41 38          SEC                    ;|
; $A9:9E42 ED BA 0F    SBC $0FBA  [$7E:0FBA]  ;|
; $A9:9E45 38          SEC                    ;} $12 = [Shitroid X position] - Ah - [Mother Brain's brain X position]
; $A9:9E46 E9 0A 00    SBC #$000A             ;|
org $A99E3E
        lda $0FBA
org $A99E42
	sbc $0F7A,x

;;; $9E5B: Instruction - aim Mother Brain blue rings at Samus ;;;
; $A9:9E5D AD F6 0A    LDA $0AF6  [$7E:0AF6]  ;\
; $A9:9E60 38          SEC                    ;|
; $A9:9E61 ED BA 0F    SBC $0FBA  [$7E:0FBA]  ;|
; $A9:9E64 38          SEC                    ;} $12 = [Samus X position] - Ah - [Mother Brain's brain X position]
; $A9:9E65 E9 0A 00    SBC #$000A             ;|
; $A9:9E68 85 12       STA $12    [$7E:0012]  ;/
org $A99E5D
        lda $0FBA
org $A99E61
        sbc $0AF6

;;; $9F46: Instruction - spawn Mother Brain laser enemy projectile ;;;
; $A9:9F4E AD BA 0F    LDA $0FBA  [$7E:0FBA]  ;\
; $A9:9F51 18          CLC                    ;|
; $A9:9F52 69 10 00    ADC #$0010             ;} $12 = [Mother Brain's brain X position] + 10h
; $A9:9F55 85 12       STA $12    [$7E:0012]  ;/
org $A99F52
	ADC #$fff0
; $A9:9F60 A9 01 00    LDA #$0001
;;; value in A is not used by function called to spawn laser (JSL $868097), it reads $16 for laser direction
;;; Direction in $16: 0 = left, otherwise right
org $A99F60
	stz $16 : nop

;;; $AEE1: Mother Brain's body function - third phase - death sequence - move to back of room ;;;
; $A9:AEFD A9 28 00    LDA #$0028             ;} Make Mother Brain walk backwards medium towards X position 28h
; $A9:AF00 20 47 C6    JSR $C647  [$A9:C647]  ;/
org $A9AEFD
       LDA #$03d8

;;; $AF21: Mother Brain's body function - third phase - death sequence - stumble to middle of room and drool ;;;
; $A9:AF27 A9 60 00    LDA #$0060             ;} Make Mother Brain walk forwards really fast towards X position 60h
; $A9:AF2A 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9AF27
	LDA #$03a0

;;; $B32A: Mother Brain's body function - third phase - death sequence - blow up escape door ;;;
; $A9:B333 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:B337             dx  00, 06, B677       ;} Spawn Mother Brain's room escape door
org $A9B337
        db $3f

;;; $B88F: Mother Brain second phase - firing death beam - back up ;;;
; $A9:B892 A9 28 00    LDA #$0028             ;} Make Mother Brain walk backwards slow towards X position 28h
; $A9:B895 20 47 C6    JSR $C647  [$A9:C647]  ;/
org $A9B892
        LDA #$03d8

;;; $B781: Mother Brain's body function - firing bomb - decide on walking ;;;
; $A9:B781 AD E5 05    LDA $05E5  [$7E:05E5]  ;\
; $A9:B784 C9 80 FF    CMP #$FF80             ;} If [random number] >= FF80h: go to decide on crouching
; $A9:B787 B0 2E       BCS $2E    [$B7B7]     ;/
; $A9:B789 A2 40 00    LDX #$0040             ; X = 40h (target X position)
; $A9:B78C C9 00 60    CMP #$6000             ;\
; $A9:B78F B0 03       BCS $03    [$B794]     ;} If [random number] < 6000h:
; $A9:B791 A2 60 00    LDX #$0060             ; X = 60h (target X position)
org $A9B789
        LDX #$03c0
org $A9B791
        LDX #$03a0
; $A9:B794 8A          TXA                    ;\
; $A9:B795 CD 7A 0F    CMP $0F7A  [$7E:0F7A]  ;} If [Mother Brain's body X position] <= [X]: go to decide on crouching
; $A9:B798 10 1D       BPL $1D    [$B7B7]     ;/
; $A9:B79A 8D B2 0F    STA $0FB2  [$7E:0FB2]  ; $0FB2 = [X]
org $A9B798
        bmi $1D

;;; $DE00: Calculate Mother Brain rainbow beam HDMA tables ;;;
; $AD:DE23 18          CLC                    ;|
; $AD:DE24 69 00 0E    ADC #$0E00             ;} Mother Brain rainbow beam right edge origin X position = ([Mother Brain's brain X position] + Eh) * 100h
org $ADDE24
        adc #$f200

;;; $BA5E: Mother Brain's body function - second phase - firing rainbow beam - finish firing rainbow beam ;;;
; $A9:BA82 A9 00 FF    LDA #$FF00             ;\
; $A9:BA85 8D B4 0F    STA $0FB4  [$7E:0FB4]  ;} Custom Samus X velocity = -100h
;;; samus x velocity when falling from wall after rainbow beam
org $A9BA82
        lda #$0100

;;; $BB82: Aim Mother Brain rainbow beam ;;;
; $A9:BB82 AD F6 0A    LDA $0AF6  [$7E:0AF6]  ;\
; $A9:BB85 38          SEC                    ;|
; $A9:BB86 ED BA 0F    SBC $0FBA  [$7E:0FBA]  ;|
; $A9:BB89 38          SEC                    ;} $12 = [Samus X position] - [Mother Brain's brain X position] - 10h
; $A9:BB8A E9 10 00    SBC #$0010             ;|
; $A9:BB8D 85 12       STA $12    [$7E:0012]  ;/
; $A9:BB8F AD FA 0A    LDA $0AFA  [$7E:0AFA]  ;\
; $A9:BB92 38          SEC                    ;|
; $A9:BB93 ED BE 0F    SBC $0FBE  [$7E:0FBE]  ;|
; $A9:BB96 38          SEC                    ;} $14 = [Samus Y position] - [Mother Brain's brain Y position] - 4
; $A9:BB97 E9 04 00    SBC #$0004             ;|
; $A9:BB9A 85 14       STA $14    [$7E:0014]  ;/
; $A9:BB9C 22 AE C0 A0 JSL $A0C0AE[$A0:C0AE]  ; A = angle of ([$12], [$14]) offset
; $A9:BBA0 38          SEC                    ;\
; $A9:BBA1 E9 80 00    SBC #$0080             ;|
; $A9:BBA4 49 FF FF    EOR #$FFFF             ;|
; $A9:BBA7 1A          INC A                  ;} Mother Brain rainbow beam angle = 80h - [A] & FFh (Y flip)
; $A9:BBA8 29 FF 00    AND #$00FF             ;|
; $A9:BBAB 8F 22 80 7E STA $7E8022[$7E:8022]  ;/
org $A9BB89
        clc
        adc #$0010

;;; $BBE1: Move Samus for falling after rainbow beam ;;;
;; Returns:
;;     Carry: Set if reached floor (not in Y position range 30h..BFh), clear otherwise
; $A9:BBE1 AD B4 0F    LDA $0FB4  [$7E:0FB4]  ;\
; $A9:BBE4 18          CLC                    ;|
; $A9:BBE5 69 02 00    ADC #$0002             ;|
; $A9:BBE8 30 03       BMI $03    [$BBED]     ;} Custom Samus X velocity = min(0, [custom Samus X velocity] + 2)
; $A9:BBEA A9 00 00    LDA #$0000             ;|
;                                             ;|
; $A9:BBED 8D B4 0F    STA $0FB4  [$7E:0FB4]  ;/
; $A9:BBF0 20 3F BC    JSR $BC3F  [$A9:BC3F]  ; Move Samus [custom Samus X velocity] / 100h px horizontally towards wall
;;; vanilla x velocity is -0x100, we've put 0x100, do inverse its decrease
org $A9BBE4
        SEC
        SBC #$0002
        BPL $03

;;; $BC3F: Move Samus horizontally towards wall ;;;
;;     Carry: Set if reached wall (X position EBh), clear otherwise
; $A9:BC51 10 03       BPL $03    [$BC56]
; $A9:BC53 09 00 FF    ORA #$FF00
; $A9:BC56 6D F6 0A    ADC $0AF6  [$7E:0AF6]
; $A9:BC59 C9 EB 00    CMP #$00EB
; $A9:BC5C 10 07       BPL $07    [$BC65]
org $A9BC51
        ;; invert x delta to apply to samus X position
        eor #$ffff
        inc A
        adc $0AF6
        CMP #$0315
        bmi samus_hits_the_wall
        ;; cmp will set the carry if samus position is bigger than left wall at 0x0315 so we have to clear it as it's used as return from this function
        clc
; $A9:BC65 A9 EB 00    LDA #$00EB
org $A9BC65
samus_hits_the_wall:
	LDA #$0315

;;; $BE1B: Spawn Shitroid in cutscene ;;;
; ;                        ____________________________________ Enemy ID
; ;                       |     _______________________________ X position
; ;                       |    |     __________________________ Y position
; ;                       |    |    |     _____________________ Initialisation parameter
; ;                       |    |    |    |     ________________ Properties
; ;                       |    |    |    |    |     ___________ Extra properties
; ;                       |    |    |    |    |    |     ______ Parameter 1
; ;                       |    |    |    |    |    |    |     _ Parameter 2
; ;                       |    |    |    |    |    |    |    |
; $A9:BE28             dw ECBF,0180,0040,CFA2,2800,0000,0000,0000
; $A0:ECBF             dx 0000, F8E6, 0C80, 0028, 0024, 0024, A9, 00, 0000, 0000, C710, 0001, 0000, C779, 800F, 804C, 8041, 0000, 0000, 00000000, 0000, 0000, 00000000, CF03, 804C, 0000, B18400, 02, F4A0, EC1C, 0000
org $A9BE28+2
        dw $0280

;;; $BF41: Mother Brain's body function - drained by Shitroid - move to back of room ;;;
; $A9:BF41 A9 28 00    LDA #$0028             ;\
; $A9:BF44 20 47 C6    JSR $C647  [$A9:C647]  ;} Make Mother Brain walk backwards towards X position 28h with animation delay [Y]
org $A9BF41
       LDA #$03d8

;;; $BFD0: Mother Brain painful walking function - walk forwards  ;;;
; $A9:BFD5 A9 48 00    LDA #$0048             ;} Make Mother Brain walk forwards towards X position 48h with animation delay [$7E:784E]
; $A9:BFD8 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9BFD5
        LDA #$03b8

;;; $C004: Mother Brain painful walking function - walk backwards ;;;
; $A9:C009 A9 28 00    LDA #$0028             ;} Make Mother Brain walk backwards towards X position 28h with animation delay [$7E:784E]
; $A9:C00C 20 47 C6    JSR $C647  [$A9:C647]  ;/
org $A9C009
        LDA #$03d8

;;; $C0FB: Mother Brain's body function - second phase - revive self - walk up to Shitroid ;;;
; $A9:C103 A9 50 00    LDA #$0050             ;} Make Mother Brain walk forwards fast towards X position 50h
; $A9:C106 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9C103
        LDA #$03b0

;;; $C147: Mother Brain's body function - second phase - revive self - finish preparing for Shitroid murder ;;;
; $A9:C156 A9 50 00    LDA #$0050             ;} Make Mother Brain walk forwards really slow towards X position 50h
; $A9:C159 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9C156
        LDA #$03b0

;;; $C18E: Mother Brain's body function - second phase - prepare for final Shitroid attack ;;;
; $A9:C194 A9 40 00    LDA #$0040             ;} Make Mother Brain walk backwards fast towards X position 40h
; $A9:C197 4C 47 C6    JMP $C647  [$A9:C647]  ;/
org $A9C194
        LDA #$03c0

;;; $C26A: Mother Brain walking function - try to inch forward ;;;
; $A9:C27D AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C280 1A          INC A                  ;} Mother Brain target X position = [Mother Brain's body X position] + 1
; $A9:C281 8F 76 78 7E STA $7E7876[$7E:7876]  ;/
org $A9C280
        dec A
; BRANCH_WALK_LEFT
; $A9:C2A1 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C2A4 38          SEC                    ;|
; $A9:C2A5 E9 0E 00    SBC #$000E             ;} Mother Brain target X position = [Mother Brain's body X position] - Eh
; $A9:C2A8 8F 76 78 7E STA $7E7876[$7E:7876]  ;/
org $A9C2A5
        SBC #$fff2

;;; $C2B3: Mother Brain walking function - retreat quickly ;;;
; $A9:C2BF AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C2C2 38          SEC                    ;|
; $A9:C2C3 E9 0E 00    SBC #$000E             ;} Mother Brain target X position = [Mother Brain's body X position] - Eh
; $A9:C2C6 8F 76 78 7E STA $7E7876[$7E:7876]  ;/
org $A9C2C3
        sbc #$fff2

;;; $C313: Set Mother Brain walking function to try to inch forward ;;;
; $A9:C31E AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C321 1A          INC A                  ;} Mother Brain target X position = [Mother Brain's body X position] + 1 (gets ignored)
; $A9:C322 8F 76 78 7E STA $7E7876[$7E:7876]  ;/
org $A9C321
        dec A



org $A9C46C
compute_sinus:

;;; $C48E: Unused. Enemy X position += [A] / 100h ;;;
org $A9C48E
compute_neg_sinus:
        ;; compute -sin(x), using sin(x+pi)
        TAY
        LDA $12
        CLC
        ADC #$0080              ; pi
        bra compute_sinus
warnpc $A9C4A8

;;; $C601: Make Mother Brain walk forwards ;;;
;; Parameters:
;;     A: Target X position. Maximum of 7Fh
;;     Y: Animation delay
;; Returns:
;;     Carry: Set if reached target, clear otherwise
; $A9:C601 CD 7A 0F    CMP $0F7A  [$7E:0F7A]  ;\
; $A9:C604 30 16       BMI $16    [$C61C]     ;} If [Mother Brain's body X position] > [A]: return carry set
org $A9C604
        bpl $16
; $A9:C606 AF 04 78 7E LDA $7E7804[$7E:7804]  ;\
; $A9:C60A D0 0E       BNE $0E    [$C61A]     ;} If [Mother Brain's pose] != standing: return return carry clear
; $A9:C60C AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C60F C9 80 00    CMP #$0080             ;} If [Mother Brain's body X position] >= 80h: return carry set
; $A9:C612 10 08       BPL $08    [$C61C]     ;/
org $A9C60F
        CMP #$0380
        bmi $08

;;; $C647: Make Mother Brain walk backwards ;;;
;; Parameters:
;;     A: Target X position. Minimum of 2Fh
;;     Y: Speed (actually animation delay)
;; Returns:
;;     Carry: Set if reached target, clear otherwise
; $A9:C647 CD 7A 0F    CMP $0F7A  [$7E:0F7A]  ;\
; $A9:C64A 10 16       BPL $16    [$C662]     ;} If [Mother Brain's body X position] <= [A]: return carry set
org $A9C64A
        bmi $16
; $A9:C64C AF 04 78 7E LDA $7E7804[$7E:7804]  ;\
; $A9:C650 D0 0E       BNE $0E    [$C660]     ;} If [Mother Brain's pose] != standing: return return carry clear
; $A9:C652 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C655 C9 30 00    CMP #$0030             ;} If [Mother Brain's body X position] < 30h: return carry set
; $A9:C658 30 08       BMI $08    [$C662]     ;/
org $A9C655
        CMP #$03D0
        BPL $08

;;; $C6B8: Handle Mother Brain walking ;;;
; $A9:C6D9 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C6DC C9 80 00    CMP #$0080             ;} If [Mother Brain's body X position] >= 80h: return
; $A9:C6DF 10 2E       BPL $2E    [$C70F]     ;/
org $A9C6DC
	CMP #$0380
        bmi $2E
; $A9:C6EE AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C6F1 C9 30 00    CMP #$0030             ;} If [Mother Brain's body X position] < 30h: go to BRANCH_MAYBE_WALK_FORWARDS
; $A9:C6F4 30 0E       BMI $0E    [$C704]     ;/
org $A9C6F1
        CMP #$03d0
        bpl $0E
; $A9:C6FC AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C6FF C9 30 00    CMP #$0030             ;} If [Mother Brain's body X position] >= 30h: return
; $A9:C702 10 0B       BPL $0B    [$C70F]     ;/
org $A9C6FF
        CMP #$03d0
        bmi $0B

;;; $C710: Initialisation AI - enemy $ECBF (Shitroid in cutscene) ;;;
; $A9:C741 A9 40 01    LDA #$0140             ;\
; $A9:C744 9D 7A 0F    STA $0F7A,x[$7E:0FFA]  ;} Enemy X position = 140h
org $A9C741
	LDA #$02c0 

;;; update baby path when dashing toward mb head
;;; $C7CC: Shitroid function - dash onto screen ;;;
; $A9:C7D2 A9 00 D8    LDA #$D800             ;\
; $A9:C7D5 9F 14 78 7E STA $7E7814,x[$7E:7894];} Enemy angle = -2800h : -40
; $A9:C7D9 A9 00 0A    LDA #$0A00             ;\
; $A9:C7DC 9F 16 78 7E STA $7E7816,x[$7E:7896];} Enemy speed = A00h
; $A9:C7E0 A9 EC C7    LDA #$C7EC             ;\
; $A9:C7E3 9D A8 0F    STA $0FA8,x[$7E:1028]  ;} Enemy function = $C7EC
org $A9C7D2
	lda #$2800

;;; $C7EC: Shitroid function - curve towards Mother Brain's brain ;;;
; $A9:C7EC A9 80 FE    LDA #$FE80             ;\
; $A9:C7EF 85 12       STA $12    [$7E:0012]  ;} $12 = -180h (angle delta) : -1.5
; $A9:C7F1 A9 00 B0    LDA #$B000             ;\
; $A9:C7F4 85 14       STA $14    [$7E:0014]  ;} $14 = -5000h (target angle) : -80
; $A9:C7F6 A9 00 0A    LDA #$0A00             ;\
; $A9:C7F9 85 16       STA $16    [$7E:0016]  ;} $16 = A00h (target speed)
; $A9:C7FB 20 31 CF    JSR $CF31  [$A9:CF31]  ; Update Shitroid speed and angle
org $A9C7EC
        lda #$0180
org $A9C7F1
        lda #$5000

;;; $C811: Shitroid function - get right up in Mother Brain's face ;;;
; $A9:C811 A9 00 FA    LDA #$FA00             ;\
; $A9:C814 85 12       STA $12    [$7E:0012]  ;} $12 = -500h (angle delta) : -5
; $A9:C816 A9 00 82    LDA #$8200             ;\
; $A9:C819 85 14       STA $14    [$7E:0014]  ;} $14 = -7800h (target angle) : -120
; $A9:C81B A9 00 0E    LDA #$0E00             ;\
; $A9:C81E 85 16       STA $16    [$7E:0016]  ;} $16 = E00h (target speed)
; $A9:C820 20 31 CF    JSR $CF31  [$A9:CF31]  ; Update Shitroid speed and angle
org $A9C811
        lda #$0500
org $A9C816
        lda #$7800

;;; $CA24: Shitroid movement table - ceiling -> Samus ;;;
; ; $F45F: Gradually accelerate towards point - $1A = 8
; ; $F466: Gradually accelerate towards point - $1A = 10h (faster off-screen movement)
; 
; ;                        __________________ Target X position (or next enemy function if $8000+)
; ;                       |     _____________ Target Y position
; ;                       |    |     ________ Acceleration divisor table index (0 is slowest acceleration)
; ;                       |    |    |     ___ Acceleration function
; ;                       |    |    |    |
; $A9:CA24             dw 00A0,0078,0000,F466,
;                         0130,007A,0000,F466,
;                         00C0,0040,0000,F466,
;                         00C0,0070,0000,F466,
;                         00E0,0080,0000,F466,
;                         00CD,0090,0000,F45F,
;                         00CC,00A0,0000,F45F,
;                         00CB,00B0,0000,F45F,
;                         CA66
org $A9CA24
        dw $0360
org $A9CA24+8
        dw $02d0
org $A9CA24+16
        dw $0340
org $A9CA24+24
        dw $0340
org $A9CA24+32
        dw $0320
org $A9CA24+40
        dw $0333
org $A9CA24+48
        dw $0334
org $A9CA24+56
        dw $0335

;;; $CB56: Shitroid function - fly off-screen ;;;
; $A9:CB56 A9 10 01    LDA #$0110             ;\
; $A9:CB59 85 12       STA $12    [$7E:0012]  ;} $12 = 110h
org $A9CB56
	LDA #$02f0

;;; $CB7B: Shitroid function - move to final charge start position ;;;
; $A9:CB7B A9 31 01    LDA #$0131             ;\
; $A9:CB7E 85 12       STA $12    [$7E:0012]  ;} $12 = 131h
org $A9CB7B
	LDA #$02cf

;;; $CBB3: Shitroid function - initiate final charge ;;;
; $A9:CBB3 A9 22 01    LDA #$0122             ;\
; $A9:CBB6 85 12       STA $12    [$7E:0012]  ;} $12 = 122h
org $A9CBB3
        LDA #$02de

;;; plm closing the wall
; $AD:E3BE 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $AD:E3C2             dx  0F, 04, B673       ;} Spawn PLM to fill Mother Brain's wall at block (Fh, 4)
; $AD:E3C6 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $AD:E3CA             dx  0F, 09, B673       ;} Spawn PLM to fill Mother Brain's wall at block (Fh, 9)
org $ADE3C2
        db $30
org $ADE3CA
        db $30

;;; $BE4F..C1B7: Mother Brain's room turrets ;;;
; X positions
; $86:BE89             dw 0398, 0348, 0328, 02D8, 0288, 0268, 0218, 01C8, 01A8, 0158, 0108, 00E8
org $86BE89
        dw $0068, $00b8, $00d8, $0128, $0178, $0198, $01e8, $0238, $0258, $02a8, $02f8, $0318

;;; $CA6A..F5: Mother Brain's purple breath ;;;
; $86:CA71 18          CLC                    ;|
; $86:CA72 69 06 00    ADC #$0006             ;} Enemy projectile X position = [Mother Brain's brain X position] + 6
; $86:CA75 9D 4B 1A    STA $1A4B,x[$7E:1A6B]  ;/
org $86CA71
        SEC
        SBC #$0006
; $86:CA87 AD BA 0F    LDA $0FBA  [$7E:0FBA]  ;\
; $86:CA8A 18          CLC                    ;|
; $86:CA8B 69 06 00    ADC #$0006             ;} Enemy projectile X position = [Mother Brain's brain X position] + 6
; $86:CA8E 9D 4B 1A    STA $1A4B,x[$7E:1A6D]  ;/
org $86CA8A
        SEC
        SBC #$0006

;;; $C2F3..C481: Mother Brain's blue ring lasers ;;;

;;; $C2F3: Initialisation AI - enemy projectile $CB4B (Mother Brain's blue ring lasers) ;;;
; $86:C308 A9 50 04    LDA #$0450             ;\
; $86:C30B DA          PHX                    ;|
; $86:C30C 22 6C C2 86 JSL $86C26C[$86:C26C]  ;} Enemy projectile X velocity = 450h * sin([$12] * pi / 80h)
; $86:C310 FA          PLX                    ;|
; $86:C311 9D B7 1A    STA $1AB7,x[$7E:1AD5]  ;/
org $86C311
        jsr negate_blue_ring_x_velocity

;;; $C75D: Unused. ;;;
org $86C75D
negate_blue_ring_x_velocity:
	eor #$FFFF
        inc A
	;; vanilla
        STA $1AB7,x
        rts
warnpc $86C76C

;;; $C320: Move to blue ring spawn position ;;;
; $86:C320 AD BA 0F    LDA $0FBA  [$7E:0FBA]  ;\
; $86:C323 18          CLC                    ;|
; $86:C324 69 0A 00    ADC #$000A             ;} Enemy projectile X position = [Mother Brain's brain X position] + Ah
; $86:C327 9D 4B 1A    STA $1A4B,x[$7E:1A69]  ;/
org $86C324
        ADC #$fff6

;;; $C482..C604: Mother Brain's bomb ;;;

;;; $C482: Initialisation AI - enemy projectile $CB59 (Mother Brain's bomb) ;;;
; $86:C492 A9 E0 00    LDA #$00E0             ;\
; $86:C495 99 B7 1A    STA $1AB7,y[$7E:1AD7]  ;} Enemy projectile X velocity = E0h
; $86:C498 AD BA 0F    LDA $0FBA  [$7E:0FBA]  ;\
; $86:C49B 18          CLC                    ;|
; $86:C49C 69 0C 00    ADC #$000C             ;} Enemy projectile X position = [Mother Brain's brain X position] + Ch
; $86:C49F 99 4B 1A    STA $1A4B,y[$7E:1A6B]  ;/
org $86C492
        lda #$ff20
org $86C49C
        adc #$fff4

;;; $C5C2: Move Mother Brain's bomb ;;;
; $86:C5CC BD 4B 1A    LDA $1A4B,x[$7E:1A6B]  ;\
; $86:C5CF C9 F0 00    CMP #$00F0             ;} If [enemy projectile X position] >= F0h:
; $86:C5D2 30 0A       BMI $0A    [$C5DE]     ;/
org $86C5CF
        CMP #$0310
        bpl $0A

;;; $C605..C76D: Mother Brain's death beam ;;;

;;; $C605: Initialisation AI - enemy projectile $CB67 (Mother Brain's death beam - charging) ;;;
; $86:C628 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $86:C62B 18          CLC                    ;|
; $86:C62C 69 40 00    ADC #$0040             ;} Enemy projectile X position = [Mother Brain's body X position] + 40h
; $86:C62F 99 4B 1A    STA $1A4B,y[$7E:1A5B]  ;/
org $86C62C
        ADC #$ffc0

;;; $C684: Initialisation AI - enemy projectile $CB75 (Mother Brain's death beam - fired) ;;;
; $86:C70E BD 4B 1A    LDA $1A4B,x[$7E:1A59]  ;\
; $86:C711 C9 02 00    CMP #$0002             ;|
; $86:C714 30 1C       BMI $1C    [$C732]     ;} If 2 <= [enemy projectile X position] < EEh:
; $86:C716 C9 EE 00    CMP #$00EE             ;|
; $86:C719 10 17       BPL $17    [$C732]     ;/
;;; spawn death beam big explosion when touching a wall
org $86C711
        cmp #$0312
org $86C716
        cmp #$03fe

;;; $C961..CA69: Mother Brain's exploded escape door particles ;;;
; $86:C96B B9 92 C9    LDA $C992,y[$86:C992]  ;\
; $86:C96E 18          CLC                    ;|
; $86:C96F 69 10 00    ADC #$0010             ;} Enemy projectile X position = 10h + [$C992 + [Y]]
; $86:C972 9D 4B 1A    STA $1A4B,x[$7E:1A61]  ;/
org $86C96F
        adc #$fff0
; ; X/Y offsets
; $86:C992             dw 0000,FFE0, 0000,FFE8, 0000,FFF0, 0000,FFF8, 0000,0000, 0000,0008, 0000,0010, 0000,0018
org $86C992
        dw $0400,$ffe0, $0400,$ffe8, $0400,$fff0, $0400,$fff8, $0400,$0000, $0400,$0008, $0400,$0010, $0400,$0018
; ; X/Y velocities
; $86:C9B2             dw 0500,FE00, 0500,FF00, 0500,FF00, 0500,FF80, 0500,FF80, 0500,0080, 0500,FF00, 0500,0200
org $86C9B2
	dw $fb00,$FE00, $fb00,$FF00, $fb00,$FF00, $fb00,$FF80, $fb00,$FF80, $fb00,$0080, $fb00,$FF00, $fb00,$0200

;;; $E09B: Handle letting Samus up from being drained ;;;
; $90:E09B AD 1C 0A    LDA $0A1C  [$7E:0A1C]  ;\
; $90:E09E C9 E9 00    CMP #$00E9             ;} If [Samus pose] != E9h (facing left - Samus drained - crouching): return
org $90E09E
        cmp #$00E8              ; facing right

;;; $E0C5: Handle letting Samus fail to stand up from being drained ;;;
;;; the pose when samus fails to stand up is not available when facing right, so disable the possibility to try to stand
org $90E0C5
        rts

;;; $F394: Set up Samus for being drained ;;;
; $90:F394 A9 54 00    LDA #$0054             ;\
; $90:F397 8D 1C 0A    STA $0A1C  [$7E:0A1C]  ;} Samus pose = facing left - knockback
org $90F394
        lda #$0053              ; samus pose: facing right - knockback

;;; $F3FB: $F084 - A = 19h: freeze drained Samus animation ;;;
; $90:F3FB A9 01 00    LDA #$0001             ;\
; $90:F3FE 8D 94 0A    STA $0A94  [$7E:0A94]  ;} Samus animation frame timer = 1
; $90:F401 A9 1C 00    LDA #$001C             ;\
; $90:F404 8D 96 0A    STA $0A96  [$7E:0A96]  ;} Samus animation frame = 1Ch
; $90:F407 38          SEC                    ;\
; $90:F408 60          RTS                    ;} Return carry set
;;; the animation frame 0x1C is too far for drained samus facing right,
;;; there's 15 animations when facing right
;;; there's 32 animations when facing left
;;; so reuse the same animation as when before
org $90F401
        lda #$0008

;;; $DEBA:  ;;;
; $90:DEBA AD 1C 0A    LDA $0A1C  [$7E:0A1C]
; $90:DEBD C9 E8 00    CMP #$00E8
; $90:DEC0 F0 07       BEQ $07    [$DEC9]
; $90:DEC2 C9 E9 00    CMP #$00E9
; $90:DEC5 F0 02       BEQ $02    [$DEC9]
; $90:DEC7 80 0C       BRA $0C    [$DED5]
; 
; $90:DEC9 A9 11 00    LDA #$0011
; $90:DECC 8D 94 0A    STA $0A94  [$7E:0A94]
; $90:DECF A9 1A 00    LDA #$001A               ; this animation frame doesn't exist with samus facing left
; $90:DED2 8D 96 0A    STA $0A96  [$7E:0A96]
; 
; $90:DED5 9C 30 0A    STZ $0A30  [$7E:0A30]  ; $0A30 = 0
; $90:DED8 9C 52 0A    STZ $0A52  [$7E:0A52]
; $90:DEDB 18          CLC
; $90:DEDC 60          RTS
;;; fix issue when samus is hit while drained before final rainbow beam
org $90DECF
	lda #$0008

;;; in bank 92 in the spritemap table the entry for the bottom of samus sprite with movement type 0x1B
;;; and pose E8 (Facing right - Samus drained - crouching/falling) point to 0000.
;;; with spritesomething custom sprites the table is rewritten and don't have the 0000 issue.
; ; Bottom half - E8: Facing right - Samus drained - crouching
;                         0000 ; 06D5
;                         0000 ; 06D6
;                         0000 ; 06D7 <- this one
;                         B0AF ; 06D8
;                         B0AF ; 06D9
;                         B0AF ; 06DA
org $928e3b
        dw $B0AF

;;; $FB72: Initialisation AI - enemy $E27F (zebetites) ;;;
; $A6:FC1B             dw 0338,0278,01B8,00F8 ; X position
org $A6FC1B
        dw $00c8, $0188, $0248, $0308

; Room $DD58, state $DD6E: Enemy population
; Room $DD58, state $DD88: Enemy population
; $A1:E321             dx EC7F,0081,006F,0000,2800,0004,0000,0000, EC3F,0081,006F,0000,2800,0004,0000,0000, E27F,0000,0000,0000,2000,0000,0000,0000, D23F,0337,0036,0000,6000,0000,0001,0000, D23F,0337,00A6,0000,6000,0000,0002,0000, D23F,0277,001C,0000,6000,0000,0003,0000, FFFF, 00
org $A1E323
        dw $037F
org $A1E333
        dw $037F

;;; $B75B: Mother Brain's room rinka spawn data ;;;
; ;                        _____________ X position
; ;                       |     ________ Y position
; ;                       |    |     ___ Index into $7E:8800 table (+ 2)
; ;                       |    |    |
; $A2:B75B             dw 03E7,0026,0002,
;                         03E7,00A6,0004,
;                         0337,0036,0006,
;                         0337,00A6,0008,
;                         0277,001C,000A,
;                         0277,00B6,000C,
;                         01B7,0036,000E,
;                         01B7,00A6,0010,
;                         00F7,001C,0012,
;                         00F7,00B6,0014,
;                         0080,00A8,0016
org $A2B75B
        dw $0019, $0026, $0002
        dw $0019, $00A6, $0004
        dw $00c9, $0036, $0006
        dw $00c9, $00A6, $0008
        dw $0189, $001C, $000A
        dw $0189, $00B6, $000C
        dw $0249, $0036, $000E
        dw $0249, $00A6, $0010
        dw $0309, $001C, $0012
        dw $0309, $00B6, $0014
        dw $0380, $00A8, $0016

;;; $B455: Mother Brain part / Samus collision detection ;;;
; ; BRANCH_HIT
; $A9:B4BB C9 04 00    CMP #$0004             ;\
; $A9:B4BE 10 03       BPL $03    [$B4C3]     ;|
; $A9:B4C0 A9 04 00    LDA #$0004             ;} Extra Samus X displacement = max(4, [A])
;                                             ;|
; $A9:B4C3 8D 58 0B    STA $0B58  [$7E:0B58]  ;/
; $A9:B4C6 A9 04 00    LDA #$0004             ;\
; $A9:B4C9 8D 5C 0B    STA $0B5C  [$7E:0B5C]  ;} Extra Samus Y displacement = 4
; $A9:B4CC 9C 56 0B    STZ $0B56  [$7E:0B56]  ; Extra Samus X subdisplacement = 0
; $A9:B4CF 9C 5A 0B    STZ $0B5A  [$7E:0B5A]  ; Extra Samus Y subdisplacement = 0
; $A9:B4D2 A9 60 00    LDA #$0060             ;\
; $A9:B4D5 8D A8 18    STA $18A8  [$7E:18A8]  ;} Samus invincibility timer = 60h
; $A9:B4D8 A9 05 00    LDA #$0005             ;\
; $A9:B4DB 8D AA 18    STA $18AA  [$7E:18AA]  ;} Samus knockback timer = 5
; $A9:B4DE A9 01 00    LDA #$0001             ;\
; $A9:B4E1 8D 54 0A    STA $0A54  [$7E:0A54]  ;} Knockback X direction = right
org $A9B4C3
        jsr invert_samus_X_displacement

org $A9B4DE
        lda #$0000              ; knockback x direction left

; $A9:B4F2 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:B4F5 18          CLC                    ;|
; $A9:B4F6 69 18 00    ADC #$0018             ;} If [Mother Brain body X position] + 18h < [Samus X position]:
; $A9:B4F9 CD F6 0A    CMP $0AF6  [$7E:0AF6]  ;|
; $A9:B4FC 10 03       BPL $03    [$B501]     ;/
; $A9:B4FE 20 E1 B5    JSR $B5E1  [$A9:B5E1]  ; Hurt Samus
org $A9B4F6
	adc #$ffe8
org $A9B4FC
        bmi $03

;;; unused space in A9: [$C2E5 -> $C313[
;;; $C2E5: Unused. Mother Brain walking function - crouch ;;;
;;; $C2F9: Unused. Mother Brain walking function - crouching ;;;
;;; $C30B: Unused. Mother Brain walking function - stand up ;;;
org $A9C2E5
invert_samus_X_displacement:
	eor #$ffff
        inc A
        ;; vanilla
        sta $0B58
	rts
warnpc $A9C302

;;; fix rainbow beam when aiming up left
;;; $E124: Calculate Mother Brain rainbow beam HDMA data table - beam is aimed upwards - beam is aimed up-left ;;;
; $AD:E191 C9 FF FF    CMP #$FFFF             ;\
; $AD:E194 D0 03       BNE $03    [$E199]     ;} If [[X]] = FFh, FFh:
; $AD:E196 A9 FF 00    LDA #$00FF             ; [X] = FFh, 00h
org $ADE191
	;; we need to put the filler if (0, 0), not (ff, ff) as the beam is aiming left
	nop : nop : nop

;;; add function to handle when rainbow beam is aiming left
org $ADDE5F+22
        dw compute_mb_rainbow_beam_hdma_table_aimed_left

;;; compute missing compute of mother brain rainbow beam hdma tables when beam is aimed left
;;; freespace
org $ADF444
compute_mb_rainbow_beam_hdma_table_aimed_left:
    ;; reuse the aimed right function ($DE7F) but change the call to the subroutine which fill the hdma table
    LDA.l $7E8038                           ; \
    STA.b $16                               ; } $16 = [Mother Brain rainbow beam right edge origin X position]
    LDA.l $7E803C                           ; \
    STA.b $18                               ; } $18 = [Mother Brain rainbow beam left edge origin X position]
    JSR.w compute_mb_rainbow_beam_hdma_table_data_aimed_left
    LDA.w #$0010                            ; \
    STA.l $7E9C00                           ; |
    LDA.w #$9C00                            ; |
    STA.l $7E9C01                           ; |
    LDA.w #$0010                            ; |
    STA.l $7E9C03                           ; |
    LDA.w #$9C03                            ; |
    STA.l $7E9C04                           ; |
    LDA.w #$00F0                            ; |
    STA.l $7E9C06                           ; } $7E:9C00..0D = 10h,$9C00, 10h,$9C03, F0h,$9D04, F4h,$9DEC, 00h,00h
    LDA.w #$9D04                            ; |
    STA.l $7E9C07                           ; |
    LDA.w #$00F4                            ; |
    STA.l $7E9C09                           ; |
    LDA.w #$9DEC                            ; |
    STA.l $7E9C0A                           ; |
    LDA.w #$0000                            ; |
    STA.l $7E9C0C                           ; /
    RTS                                     ; 

compute_mb_rainbow_beam_hdma_table_data_aimed_left:
;; Parameters:
;;     $16: [$7E:8038] (right edge origin X position)
;;     $18: [$7E:803C] (left edge origin X position)
    PHB
    PEA $7E7E              ;\
    PLB                    ;} DB = $7E
    PLB                    ;/
    LDA #$00FF             ;\
    STA $9D00              ;} $9D00 = FFh, 00h
    STA $9D02              ; $9D02 = FFh, 00h
    LDA $8034              ;\
    EOR #$FFFF
    INC A
    AND #$00FF             ;|
    ASL A                  ;|
    TAX                    ;} $12 = |tan(-[Mother Brain rainbow beam right edge angle] * pi / 80h)| * 100h (right edge gradient)
    LDA $91C9D4,x          ;|
    STA $12                ;/
    LDA $8036              ;\
    EOR #$FFFF
    INC A
    AND #$00FF             ;|
    ASL A                  ;|
    TAX                    ;} $14 = |tan(-[Mother Brain rainbow beam left edge angle] * pi / 80h)| * 100h (left edge gradient)
    LDA $91C9D4,x          ;|
    STA $14                ;/
    LDA $803E              ;\
    TAY                    ;} Y = [Mother Brain rainbow beam origin Y position]
    SEC                    ;\
    SBC #$0020             ;|
    ASL A                  ;|
    CLC                    ;} X = $9D02 + ([Y] - 20h) * 2
    ADC #$9D02             ;|
    TAX                    ;/
    LDA #$0000             ;\
    STA $0002,x            ;} [X] + 2 = 00h, 00h
    STA $0004,x            ; [X] + 4 = 00h, 00h
    PHX                    ; Push X

.LOOP_RIGHT_EDGE
    LDA $16                ;\
    SEC                    ;|
    SBC $12                ;} $16 = max(0, [$16] - [$12])
    BCS .POSITIVE_RIGHT    ;/
    LDA #$0000
.POSITIVE_RIGHT
    STA $16                ; $16 -= [$12]
    AND #$FF00
    BNE .NOT_FILLER_RIGHT
    LDA #$00FF               ; filler
.NOT_FILLER_RIGHT          ;} [X] = [$16] / 100h, 00h
    STA $0000,x            ;/
    DEX
    DEX
    DEY
    CPY #$0020
    BNE .LOOP_RIGHT_EDGE

    PLX                    ;\
    INX                    ;} X = $9D04 + ([Mother Brain rainbow beam origin Y position] - 20h) * 2
    INX                    ;/
    LDA $803E              ;\
    TAY                    ;} Y = [Mother Brain rainbow beam origin Y position]

.LOOP_LEFT_EDGE
    LDA $18                ;\
    SEC                    ;|
    SBC $14                ;} $18 = max(0, [$18] - [$14])
    BCS .POSITIVE_LEFT     ;/
    LDA #$0000
.POSITIVE_LEFT
    STA $18                ; $18 -= [$14]
    AND #$FF00             ;|
    BNE .NOT_FILLER_LEFT
    LDA #$00FF
.NOT_FILLER_LEFT           ;} [X] = 00h, [$18] / 100h
    STA $0000,x            ;/
    INX
    INX
    INY
    CPY #$00E8
    BNE .LOOP_LEFT_EDGE
    PLB
    RTS

warnpc $ADFFFF


;;; spritemaps, extended spritemaps, tilemaps, hitboxes
org $a99fa2
        dw $ffee
org $a99faa
        dw $ffe2
org $a99fb2
        dw $ffe7
org $a99fd2
        dw $000a
org $a99fda
        dw $fff9
org $a99fe2
        dw $fffe
org $a99fec
        dw $ffe4
org $a99ff4
        dw $ffda
org $a99ffc
        dw $ffdf
org $a9a01c
        dw $000b
org $a9a024
        dw $fffa
org $a9a02c
        dw $ffff
org $a9a034
        dw $0019
org $a9a03e
        dw $ffd8
org $a9a046
        dw $ffda
org $a9a04e
        dw $ffdd
org $a9a06e
        dw $000d
org $a9a076
        dw $fffb
org $a9a07e
        dw $0001
org $a9a086
        dw $001a
org $a9a090
        dw $ffd8
org $a9a098
        dw $ffda
org $a9a0a0
        dw $ffdd
org $a9a0a8
        dw $0001
org $a9a0c0
        dw $000d
org $a9a0c8
        dw $fffb
org $a9a0d0
        dw $0001
org $a9a0d8
        dw $001a
org $a9a0e2
        dw $ffdc
org $a9a0ea
        dw $ffdf
org $a9a0f2
        dw $ffe1
org $a9a0fa
        dw $ffff
org $a9a112
        dw $0010
org $a9a11a
        dw $fffd
org $a9a122
        dw $0004
org $a9a12c
        dw $ffeb
org $a9a134
        dw $ffe3
org $a9a13c
        dw $ffe5
org $a9a144
        dw $0002
org $a9a15c
        dw $0010
org $a9a16c
        dw $0005
org $a9a176
        dw $fff1
org $a9a17e
        dw $ffe2
org $a9a186
        dw $ffe6
org $a9a18e
        dw $0002
org $a9a1a6
        dw $000a
org $a9a1ae
        dw $fffc
org $a9a1b6
        dw $0001
org $a9a1c0
        dw $ffef
org $a9a1c8
        dw $ffe2
org $a9a1d0
        dw $ffe8
org $a9a1d8
        dw $0001
org $a9a1f0
        dw $0008
org $a9a1f8
        dw $fff9
org $a9a200
        dw $fffd
org $a9a20a
        dw $ffee
org $a9a212
        dw $ffe1
org $a9a21a
        dw $ffe7
org $a9a222
        dw $0001
org $a9a23a
        dw $000a
org $a9a242
        dw $fff9
org $a9a24a
        dw $fffe
org $a9a254
        dw $ffee
org $a9a25c
        dw $ffde
org $a9a264
        dw $ffe1
org $a9a26c
        dw $0005
org $a9a27c
        dw $fffc
org $a9a284
        dw $000a
org $a9a28e
        dw $ffee
org $a9a296
        dw $ffdc
org $a9a29e
        dw $ffe1
org $a9a2a6
        dw $0005
org $a9a2b6
        dw $0002
org $a9a2be
        dw $000a
org $a9a2c6
        dw $fff9
org $a9a2ce
        dw $fffe
org $a9a2d8
        dw $ffee
org $a9a2e0
        dw $ffe1
org $a9a2e8
        dw $ffe6
org $a9a2f0
        dw $0005
org $a9a300
        dw $0002
org $a9a308
        dw $000a
org $a9a310
        dw $fff9
org $a9a318
        dw $fffe
org $a9a386
        dw $ffee
org $a9a38e
        dw $ffe2
org $a9a396
        dw $ffe7
org $a9a3b6
        dw $000a
org $a9a3be
        dw $fff9
org $a9a3c6
        dw $fffe
org $a9a3d0
        dw $ffee
org $a9a3d8
        dw $ffe2
org $a9a3e0
        dw $ffe7
org $a9a400
        dw $000a
org $a9a408
        dw $fff9
org $a9a410
        dw $fffe
org $a9a41a
        dw $ffee
org $a9a422
        dw $ffe2
org $a9a42a
        dw $ffe7
org $a9a44a
        dw $000a
org $a9a452
        dw $fff9
org $a9a45a
        dw $fffe
org $a9a464
        dw $ffee
org $a9a46c
        dw $ffe2
org $a9a474
        dw $ffe7
org $a9a494
        dw $000a
org $a9a49c
        dw $fff9
org $a9a4a4
        dw $fffe
org $a9a4ae
        dw $fff0,$ffeb,$0014,$0017
org $a9a4bc
        dw $ffed,$ffeb,$0014,$0017
org $a9a4cc
        dw $ffe9,$ffff,$0017,$0007
org $a9a4dc
        dw $ffe9,$fffe,$0017,$0007
org $a9a4ea
        dw $ffec,$ffe8,$0020,$0034
org $a9a4f6
        dw $fff3,$ffd6,$0018,$ffe7
org $a9a506
        dw $ffe4,$ffc5,$fffc,$ffe8
org $a9a512
        dw $ffc7,$ffd7,$ffe4,$ffe2
org $a9a520
        dw $ffe4,$ffc5,$fffc,$ffe8
org $a9a52c
        dw $ffca,$ffd7,$ffe4,$ffe2
org $a9a53a
        dw $ffe4,$ffc5,$fffc,$ffe8
org $a9a546
        dw $ffd3,$ffd5,$ffe3,$ffe8
org $a9a554
        dw $ffe4,$ffc5,$fffc,$ffe8
org $a9a560
        dw $ffbc,$ffd0,$ffe3,$ffd8
org $a9a56e
        dw $ffe4,$ffc5,$fffc,$ffe8
org $a9a57a
        dw $ffc6,$ffd7,$ffe4,$ffe1
org $a9a586
    dw $000b : dw $01ec : db $01 : dw $6133 : dw $81ee : db $09 : dw $6100 : dw $8008 : db $04 : dw $6108 : dw $81f8 : db $04 : dw $6102 : dw $81f8 : db $f4 : dw $6120 : dw $81e8 : db $00 : dw $6104 : dw $81e8 : db $f0 : dw $611e : dw $81e8 : db $e8 : dw $610e : dw $81f8 : db $e4 : dw $610a : dw $0008 : db $ec : dw $6122 : dw $8008 : db $f4 : dw $6106

org $a9a5bf
    dw $000b : dw $01ec : db $01 : dw $6132 : dw $81ee : db $09 : dw $6100 : dw $8008 : db $04 : dw $6108 : dw $81f8 : db $04 : dw $6102 : dw $81f8 : db $f4 : dw $6120 : dw $81e8 : db $00 : dw $6104 : dw $81e8 : db $f0 : dw $611e : dw $81e8 : db $e8 : dw $610e : dw $81f8 : db $e4 : dw $610a : dw $0008 : db $ec : dw $6122 : dw $8008 : db $f4 : dw $6106

org $a9a5f8
    dw $000a : dw $81ee : db $09 : dw $6100 : dw $8008 : db $04 : dw $6108 : dw $81f8 : db $04 : dw $6102 : dw $81f8 : db $f4 : dw $6120 : dw $81e8 : db $00 : dw $6104 : dw $81e8 : db $f0 : dw $611e : dw $81e8 : db $e8 : dw $610e : dw $81f8 : db $e4 : dw $610a : dw $0008 : db $ec : dw $6122 : dw $8008 : db $f4 : dw $6106

org $a9a62c
    dw $000a : dw $81f1 : db $0e : dw $6124 : dw $8008 : db $04 : dw $6108 : dw $81f8 : db $04 : dw $6102 : dw $81f8 : db $f4 : dw $6120 : dw $81e8 : db $00 : dw $6104 : dw $81e8 : db $f0 : dw $611e : dw $81e8 : db $e8 : dw $610e : dw $81f8 : db $e4 : dw $610a : dw $0008 : db $ec : dw $6122 : dw $8008 : db $f4 : dw $6106

org $a9a660
    dw $000a : dw $81f4 : db $10 : dw $6126 : dw $8008 : db $04 : dw $6108 : dw $81f8 : db $04 : dw $6102 : dw $81f8 : db $f4 : dw $6120 : dw $81e8 : db $00 : dw $6104 : dw $81e8 : db $f0 : dw $611e : dw $81e8 : db $e8 : dw $610e : dw $81f8 : db $e4 : dw $610a : dw $0008 : db $ec : dw $6122 : dw $8008 : db $f4 : dw $6106

org $a9a694
    dw $0001 : dw $81f8 : db $f8 : dw $612a

org $a9a69b
    dw $000c : dw $01ec : db $01 : dw $6133 : dw $81ee : db $09 : dw $6100 : dw $81e8 : db $00 : dw $6104 : dw $01f0 : db $e8 : dw $6123 : dw $81e8 : db $f0 : dw $613e : dw $81f8 : db $e4 : dw $613c : dw $81f8 : db $f4 : dw $6128 : dw $81f8 : db $04 : dw $6102 : dw $0008 : db $0c : dw $614b : dw $0008 : db $ec : dw $614a : dw $8008 : db $f4 : dw $610c : dw $8008 : db $fc : dw $611c

org $a9a6d9
    dw $000c : dw $01ec : db $01 : dw $6132 : dw $81ee : db $09 : dw $6100 : dw $81e8 : db $00 : dw $6104 : dw $01f0 : db $e8 : dw $6123 : dw $81e8 : db $f0 : dw $613e : dw $81f8 : db $e4 : dw $613c : dw $81f8 : db $f4 : dw $6128 : dw $81f8 : db $04 : dw $6102 : dw $0008 : db $0c : dw $614b : dw $0008 : db $ec : dw $614a : dw $8008 : db $f4 : dw $610c : dw $8008 : db $fc : dw $611c

org $a9a717
    dw $000b : dw $81ee : db $09 : dw $6100 : dw $81e8 : db $00 : dw $6104 : dw $01f0 : db $e8 : dw $6123 : dw $81e8 : db $f0 : dw $613e : dw $81f8 : db $e4 : dw $613c : dw $81f8 : db $f4 : dw $6128 : dw $81f8 : db $04 : dw $6102 : dw $0008 : db $0c : dw $614b : dw $0008 : db $ec : dw $614a : dw $8008 : db $f4 : dw $610c : dw $8008 : db $fc : dw $611c

org $a9a750
    dw $000b : dw $81f1 : db $0e : dw $6124 : dw $81e8 : db $00 : dw $6104 : dw $01f0 : db $e8 : dw $6123 : dw $81e8 : db $f0 : dw $613e : dw $81f8 : db $e4 : dw $613c : dw $81f8 : db $f4 : dw $6128 : dw $81f8 : db $04 : dw $6102 : dw $0008 : db $0c : dw $614b : dw $0008 : db $ec : dw $614a : dw $8008 : db $f4 : dw $610c : dw $8008 : db $fc : dw $611c

org $a9a789
    dw $000b : dw $81f4 : db $10 : dw $6126 : dw $81e8 : db $00 : dw $6104 : dw $01f0 : db $e8 : dw $6123 : dw $81e8 : db $f0 : dw $613e : dw $81f8 : db $e4 : dw $613c : dw $81f8 : db $f4 : dw $6128 : dw $81f8 : db $04 : dw $6102 : dw $0008 : db $0c : dw $614b : dw $0008 : db $ec : dw $614a : dw $8008 : db $f4 : dw $610c : dw $8008 : db $fc : dw $611c

org $a9a7c2
    dw $0009 : dw $01dc : db $1c : dw $737b : dw $81dc : db $0c : dw $735a : dw $81e4 : db $14 : dw $7369 : dw $01ec : db $0c : dw $7366 : dw $01e4 : db $04 : dw $b378 : dw $01f4 : db $14 : dw $7378 : dw $01fc : db $fc : dw $7347 : dw $81f4 : db $04 : dw $7357 : dw $81ec : db $fc : dw $7348

org $a9a7f1
    dw $0006 : dw $81d3 : db $03 : dw $735e : dw $81d3 : db $0b : dw $736e : dw $81e3 : db $0b : dw $7362 : dw $81e3 : db $fb : dw $7360 : dw $81f3 : db $03 : dw $736c : dw $81f3 : db $fb : dw $735c

org $a9a811
    dw $0008 : dw $01d0 : db $00 : dw $f377 : dw $01d0 : db $f8 : dw $7377 : dw $81d8 : db $00 : dw $f343 : dw $81d8 : db $f0 : dw $7343 : dw $81e0 : db $00 : dw $f342 : dw $81f0 : db $00 : dw $f340 : dw $81e0 : db $f0 : dw $7342 : dw $81f0 : db $f0 : dw $7340

org $a9a83b
    dw $0006 : dw $81d3 : db $ed : dw $f35e : dw $81d3 : db $e5 : dw $f36e : dw $81e3 : db $e5 : dw $f362 : dw $81e3 : db $f5 : dw $f360 : dw $81f3 : db $ed : dw $f36c : dw $81f3 : db $f5 : dw $f35c

org $a9a85b
    dw $0001 : dw $81f8 : db $f8 : dw $7364

org $a9a862
    dw $0002 : dw $81f8 : db $10 : dw $7388 : dw $81f8 : db $00 : dw $7345

org $a9a86e
    dw $0002 : dw $81fd : db $10 : dw $738a : dw $81f9 : db $00 : dw $7381

org $a9a87a
    dw $0004 : dw $01fd : db $0e : dw $7376 : dw $8005 : db $0e : dw $7386 : dw $81f5 : db $fe : dw $7384 : dw $81fd : db $fe : dw $7383

org $a9a890
    dw $0004 : dw $01e8 : db $00 : dw $7390 : dw $01f0 : db $00 : dw $7380 : dw $81f8 : db $f8 : dw $738e : dw $8008 : db $f8 : dw $738c

org $a9a8a6
    dw $0009 : dw $01dc : db $1c : dw $677b : dw $81dc : db $0c : dw $675a : dw $81e4 : db $14 : dw $6769 : dw $01ec : db $0c : dw $6766 : dw $01e4 : db $04 : dw $a778 : dw $01f4 : db $14 : dw $6778 : dw $01fc : db $fc : dw $6747 : dw $81f4 : db $04 : dw $6757 : dw $81ec : db $fc : dw $6748

org $a9a8d5
    dw $0006 : dw $81d3 : db $03 : dw $675e : dw $81d3 : db $0b : dw $676e : dw $81e3 : db $0b : dw $6762 : dw $81e3 : db $fb : dw $6760 : dw $81f3 : db $03 : dw $676c : dw $81f3 : db $fb : dw $675c

org $a9a8f5
    dw $0008 : dw $01d0 : db $00 : dw $e777 : dw $01d0 : db $f8 : dw $6777 : dw $81d8 : db $00 : dw $e743 : dw $81d8 : db $f0 : dw $6743 : dw $81e0 : db $00 : dw $e742 : dw $81f0 : db $00 : dw $e740 : dw $81e0 : db $f0 : dw $6742 : dw $81f0 : db $f0 : dw $6740

org $a9a91f
    dw $0006 : dw $81d3 : db $ed : dw $e75e : dw $81d3 : db $e5 : dw $e76e : dw $81e3 : db $e5 : dw $e762 : dw $81e3 : db $f5 : dw $e760 : dw $81f3 : db $ed : dw $e76c : dw $81f3 : db $f5 : dw $e75c

org $a9a93f
    dw $0001 : dw $81f8 : db $f8 : dw $6764

org $a9a946
    dw $0002 : dw $81f8 : db $10 : dw $6788 : dw $81f8 : db $00 : dw $6745

org $a9a952
    dw $0002 : dw $81fd : db $10 : dw $678a : dw $81f9 : db $00 : dw $6781

org $a9a95e
    dw $0004 : dw $01fd : db $0e : dw $6776 : dw $8005 : db $0e : dw $6786 : dw $81f5 : db $fe : dw $6784 : dw $81fd : db $fe : dw $6783

org $a9a974
    dw $0004 : dw $01e8 : db $00 : dw $6790 : dw $01f0 : db $00 : dw $6780 : dw $81f8 : db $f8 : dw $678e : dw $8008 : db $f8 : dw $678c

org $a9a98a
    dw $FFFE
    dw $2098,$0004, $71b8,$71b7,$6338,$6338
    dw $20d8,$0004, $71bb,$71ba,$71b9,$6338
    dw $2118,$0004, $71be,$71bd,$71bc,$6338
    dw $214c,$000a, $71c8,$71c7,$71c6,$71c5,$71c4,$71c3,$71c2,$71c1,$71c0,$71bf
    dw $218c,$000a, $6338,$6338,$6338,$71d0,$71cf,$71ce,$71cd,$71cc,$71cb,$71ca
    dw $21cc,$000a, $6338,$6338,$71d8,$71d7,$71d6,$71d5,$71d4,$71d3,$71d2,$71d1
    dw $220c,$000a, $6338,$6338,$71e0,$71df,$71de,$71dd,$71dc,$71db,$71da,$71d9
    dw $224c,$000a, $6338,$6338,$6338,$71e7,$71e6,$71e5,$71e4,$71e3,$71e2,$71e1
    dw $228c,$000a, $6338,$6338,$6338,$71ed,$71ec,$71eb,$71ea,$71e9,$71e8,$6338
    dw $22d8,$0004, $71ef,$71ee,$6338,$6338
    dw $FFFF

org $a9aa4e
    dw $FFFE
    dw $2098,$0002, $6338,$6338
    dw $20d8,$0003, $6338,$6338,$6338
    dw $2118,$0003, $6338,$6338,$6338
    dw $214c,$000a, $6338,$6338,$6338,$6338,$6338,$6338,$6338,$6338,$6338,$6338
    dw $2192,$0007, $6338,$6338,$6338,$6338,$6338,$6338,$6338
    dw $21d0,$0008, $6338,$6338,$6338,$6338,$6338,$6338,$6338,$6338
    dw $2210,$0008, $6338,$6338,$6338,$6338,$6338,$6338,$6338,$6338
    dw $2252,$0007, $6338,$6338,$6338,$6338,$6338,$6338,$6338
    dw $2292,$0006, $6338,$6338,$6338,$6338,$6338,$6338
    dw $22d8,$0002, $6338,$6338
    dw $FFFF

org $a9aaea
    dw $FFFE
    dw $2004,$000b, $6338,$6338,$6338,$6338,$6338,$6338,$7169,$7168,$7167,$6338,$6338
    dw $2044,$000b, $6338,$6338,$6338,$6338,$6338,$716e,$716d,$716c,$716b,$716a,$6338
    dw $2084,$000b, $6338,$6338,$7187,$7186,$7174,$7173,$7172,$7171,$7170,$716f,$71b8
    dw $20c4,$000b, $6338,$6338,$7189,$7188,$717c,$717b,$717a,$7179,$7178,$7177,$71bb
    dw $2104,$000b, $6338,$6338,$6338,$7185,$7184,$7183,$7182,$7181,$7180,$717f,$71be
    dw $FFFF

org $a9ab70
    dw $FFFE
    dw $2004,$000b, $6338,$6338,$6338,$6338,$6338,$6338,$7169,$7168,$7167,$6338,$6338
    dw $2044,$000b, $6338,$6338,$6338,$6338,$6338,$716e,$716d,$716c,$716b,$716a,$6338
    dw $2084,$000b, $6338,$6338,$7176,$7175,$7174,$7173,$7172,$7171,$7170,$716f,$71b8
    dw $20c4,$000b, $6338,$6338,$717e,$717d,$717c,$717b,$717a,$7179,$7178,$7177,$71bb
    dw $2104,$000b, $6338,$6338,$6338,$7185,$7184,$7183,$7182,$7181,$7180,$717f,$71be
    dw $FFFF

org $a9abf6
    dw $FFFE
    dw $2018,$0001, $6338
    dw $2012,$0002, $718b,$718a
    dw $2004,$0002, $6338,$6338
    dw $2058,$0001, $6338
    dw $2050,$0003, $718e,$718d,$718c
    dw $2044,$0002, $6338,$6338
    dw $2084,$000b, $6338,$6338,$6338,$6338,$7194,$7193,$7192,$7191,$7190,$718f,$71b8
    dw $20c4,$000b, $6338,$6338,$6338,$719b,$719a,$7199,$7198,$7197,$7196,$7195,$71bb
    dw $2118,$0001, $71be
    dw $210c,$0004, $719f,$719e,$719d,$719c
    dw $2104,$0002, $6338,$6338
    dw $FFFF

org $a9ac76
    dw $FFFE
    dw $2010,$0003, $71a1,$71a0,$7167
    dw $2058,$0001, $71b6
    dw $204e,$0004, $71a5,$71a4,$71a3,$71a2
    dw $2044,$0003, $71a8,$71a7,$71a6
    dw $2084,$000a, $71b1,$71b0,$71af,$71ae,$71ad,$71ac,$71ab,$71aa,$71a9,$716f
    dw $20ca,$0007, $71b5,$71b4,$71b3,$71b2,$7178,$7178,$7177
    dw $2118,$0001, $71be
    dw $210c,$0004, $719f,$719e,$719d,$719c
    dw $2104,$0002, $6338,$6338
    dw $FFFF

org $a9ace4
    dw $FFFE
    dw $2010,$0002, $7169,$7168
    dw $2058,$0001, $6338
    dw $204e,$0004, $716e,$716d,$716c,$716b
    dw $2044,$0003, $6338,$6338,$6338
    dw $2084,$0009, $6338,$6338,$7187,$7186,$7174,$7173,$7172,$7171,$7170
    dw $20c8,$0006, $7189,$7188,$717c,$717b,$717a,$7179
    dw $210c,$0004, $7184,$7183,$7182,$7181
    dw $FFFF

org $a9ad3e
    dw $0009 : dw $81e8 : db $08 : dw $61e4 : dw $81f8 : db $08 : dw $61e2 : dw $8008 : db $08 : dw $61e0 : dw $81e8 : db $f8 : dw $61c4 : dw $81f8 : db $f8 : dw $61c2 : dw $8008 : db $f8 : dw $61c0 : dw $81e8 : db $e8 : dw $61a4 : dw $81f8 : db $e8 : dw $61a2 : dw $8008 : db $e8 : dw $61a0

org $a9ad6d
    dw $000a : dw $81dc : db $08 : dw $61ec : dw $81ec : db $08 : dw $61ea : dw $81fc : db $08 : dw $61e8 : dw $800c : db $08 : dw $61e6 : dw $81ec : db $f8 : dw $61ca : dw $81fc : db $f8 : dw $61c8 : dw $800c : db $f8 : dw $61c6 : dw $81ec : db $e8 : dw $61aa : dw $81fc : db $e8 : dw $61a8 : dw $800c : db $e8 : dw $61a6

org $a9b429
        dw $ffd6,$ffe8,$0020,$0038
org $a9b431
        dw $ffe4,$ffd6,$0018,$ffe7
org $a9b43b
        dw $ffea,$ffea,$0018,$0000
org $a9b443
        dw $fff0,$0001,$0016,$0014
org $a9b44d
        dw $fff8,$fff8,$0008,$0008

;;; mother brain's projectiles
org $8d93db
    dw $000b : dw $01fc : db $e5 : dw $7aed : dw $01ea : db $ef : dw $7afc : dw $000e : db $ef : dw $3afc : dw $01d3 : db $f8 : dw $7aec : dw $01de : db $d6 : dw $7aec : dw $0019 : db $d6 : dw $7aec : dw $0025 : db $f8 : dw $7aec : dw $000b : db $f8 : dw $7aeb : dw $01ec : db $f8 : dw $7aeb : dw $01f4 : db $ed : dw $7aeb : dw $0003 : db $ed : dw $7aeb

org $8d9414
    dw $0007 : dw $01fc : db $e1 : dw $7aee : dw $01e7 : db $ed : dw $7afd : dw $0011 : db $ed : dw $3afd : dw $0008 : db $e8 : dw $3afc : dw $0010 : db $f8 : dw $3add : dw $01e8 : db $f8 : dw $7add : dw $01f0 : db $e8 : dw $7afc

org $8d9439
    dw $0007 : dw $01fc : db $de : dw $7aef : dw $01e0 : db $e8 : dw $7afe : dw $0018 : db $e8 : dw $3afe : dw $0013 : db $f8 : dw $3ade : dw $01e4 : db $f8 : dw $7ade : dw $01ee : db $e6 : dw $7afd : dw $000a : db $e6 : dw $3afd

org $8d945e
    dw $0007 : dw $01fc : db $da : dw $7aff : dw $01db : db $e6 : dw $7aff : dw $001c : db $e6 : dw $3aff : dw $001a : db $f8 : dw $3adf : dw $01dd : db $f8 : dw $7adf : dw $01e8 : db $e0 : dw $7afe : dw $0010 : db $e0 : dw $3afe

org $8d9483
    dw $000a : dw $01ee : db $f3 : dw $7aea : dw $01fc : db $ec : dw $7aea : dw $01fc : db $d4 : dw $7aec : dw $01d8 : db $e4 : dw $7aec : dw $0008 : db $f3 : dw $7aea : dw $001e : db $e4 : dw $7aec : dw $0020 : db $f8 : dw $3aff : dw $01d8 : db $f8 : dw $7aff : dw $01e4 : db $dc : dw $7aff : dw $0014 : db $dc : dw $3aff

org $8d94b7
    dw $000e : dw $01fc : db $ea : dw $7aeb : dw $01d6 : db $e3 : dw $7aec : dw $01ee : db $f3 : dw $7aeb : dw $0009 : db $f3 : dw $7aeb : dw $0020 : db $e3 : dw $7aec : dw $0017 : db $d8 : dw $7aec : dw $000c : db $f8 : dw $7aea : dw $0004 : db $ec : dw $7aea : dw $01f3 : db $ec : dw $7aea : dw $01ec : db $f8 : dw $7aea : dw $01d5 : db $f8 : dw $7aec : dw $01e0 : db $d8 : dw $7aec : dw $01fc : db $d1 : dw $7aec : dw $0023 : db $f8 : dw $7aec

org $8d94ff
    dw $0001 : dw $01fc : db $fa : dw $7af0

org $8d9506
    dw $0001 : dw $01fc : db $fb : dw $7af1

org $8d950d
    dw $0001 : dw $01fc : db $fc : dw $7af2

org $8d9514
    dw $0001 : dw $01fc : db $fc : dw $7af3

org $8d951b
    dw $0001 : dw $01fc : db $fc : dw $7af4

org $8d9522
    dw $0001 : dw $01fc : db $fc : dw $7af5

org $8d9529
    dw $0001 : dw $01fc : db $fc : dw $7af6

org $8d9530
    dw $0001 : dw $01fc : db $fc : dw $7ada

org $8d9537
    dw $0002 : dw $01fc : db $00 : dw $7adc : dw $01fc : db $fc : dw $7adb

org $8d9543
    dw $0002 : dw $01fc : db $04 : dw $7adc : dw $01fc : db $fc : dw $7adb

org $8d954f
    dw $0002 : dw $000a : db $f2 : dw $7af7 : dw $c3f8 : db $f8 : dw $7ad0

org $8d955b
    dw $0004 : dw $000c : db $ee : dw $7af7 : dw $000a : db $f1 : dw $7af8 : dw $c3f0 : db $00 : dw $3ad0 : dw $c3f8 : db $f7 : dw $7ad2

org $8d9571
    dw $0007 : dw $0010 : db $e8 : dw $7af9 : dw $000a : db $ea : dw $7af7 : dw $000c : db $ed : dw $7af8 : dw $000a : db $f0 : dw $7af9 : dw $c3e8 : db $08 : dw $bad0 : dw $c3f0 : db $01 : dw $7ad2 : dw $c3f8 : db $f6 : dw $7ad4

org $8d9596
    dw $0008 : dw $0010 : db $e6 : dw $7af7 : dw $000a : db $e9 : dw $7af8 : dw $000c : db $ec : dw $7af9 : dw $000a : db $ef : dw $7afa : dw $c3e0 : db $0e : dw $3ad0 : dw $c3e8 : db $07 : dw $7ad2 : dw $c3f0 : db $00 : dw $7ad4 : dw $c3f8 : db $f4 : dw $7ad6

org $8d95c0
    dw $0007 : dw $0010 : db $e5 : dw $7af8 : dw $000a : db $e8 : dw $7af9 : dw $000c : db $eb : dw $7afa : dw $c3dd : db $0d : dw $7ad2 : dw $c3e8 : db $06 : dw $7ad4 : dw $c3f0 : db $fe : dw $7ad6 : dw $c3f8 : db $f1 : dw $7ad8

org $8d95e5
    dw $0006 : dw $0010 : db $e4 : dw $7af9 : dw $0009 : db $e7 : dw $7afa : dw $000c : db $ea : dw $7afb : dw $c3de : db $0c : dw $7ad4 : dw $c3e8 : db $02 : dw $7ad6 : dw $c3f0 : db $fb : dw $7ad8

org $8d9605
    dw $0004 : dw $0010 : db $e3 : dw $7afa : dw $0008 : db $e6 : dw $7afb : dw $c3de : db $0a : dw $7ad6 : dw $c3e8 : db $ff : dw $7ad8

org $8d961b
    dw $0002 : dw $0010 : db $e3 : dw $7afb : dw $c3de : db $07 : dw $7ad8

org $8d9627
    dw $0001 : dw $01fc : db $f8 : dw $7af7

org $8d962e
    dw $0002 : dw $01fe : db $f4 : dw $7af7 : dw $01fc : db $f7 : dw $7af8

org $8d963a
    dw $0004 : dw $0002 : db $ee : dw $7af9 : dw $01fc : db $f0 : dw $7af7 : dw $01fe : db $f3 : dw $7af8 : dw $01fc : db $f6 : dw $7af9

org $8d9650
    dw $0004 : dw $0002 : db $ec : dw $7af7 : dw $01fc : db $ef : dw $7af8 : dw $01fe : db $f2 : dw $7af9 : dw $01fc : db $f5 : dw $7afa

org $8d9666
    dw $0003 : dw $0002 : db $eb : dw $7af8 : dw $01fc : db $ee : dw $7af9 : dw $01fe : db $f1 : dw $7afa

org $8d9677
    dw $0003 : dw $0002 : db $ea : dw $7af9 : dw $01fb : db $ed : dw $7afa : dw $01fe : db $f0 : dw $7afb

org $8d9688
    dw $0002 : dw $0002 : db $e9 : dw $7afa : dw $01fa : db $ec : dw $7afb

org $8d9694
    dw $0001 : dw $0002 : db $e9 : dw $7afb

org $8d969b
    dw $0001 : dw $01fc : db $fc : dw $7302

org $8d96a2
    dw $0001 : dw $c3f8 : db $f8 : dw $7303

org $8d96a9
    dw $0001 : dw $01fc : db $fc : dw $7312

org $8d96b0
    dw $0001 : dw $c3f8 : db $f8 : dw $7305

org $8d96b7
    dw $0001 : dw $01fc : db $fc : dw $7307

org $8d96be
    dw $0001 : dw $c3f8 : db $f8 : dw $7308

org $8d96c5
    dw $0001 : dw $01fc : db $fc : dw $7317

org $8d96cc
    dw $0001 : dw $c3f8 : db $f8 : dw $730a
