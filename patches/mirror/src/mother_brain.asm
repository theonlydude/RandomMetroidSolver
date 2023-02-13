;;; compile with thedopefish asar
;;; fix mother brain screen

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

;;; $C5C2: Move Mother Brain's bomb ;;;
; $86:C5CC BD 4B 1A    LDA $1A4B,x[$7E:1A6B]  ;\
; $86:C5CF C9 F0 00    CMP #$00F0             ;} If [enemy projectile X position] >= F0h:
; $86:C5D2 30 0A       BMI $0A    [$C5DE]     ;/
;;; one more tile on the left as the right wall is doubled
org $86C5CF
        CMP #$03E0

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
        lda #$033b
	
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
        lda #$033b

;;; $8DEC: Mother Brain's body function - fake death - ascent - start music and earthquake ;;;
; $A9:8E01 A9 3B 00    LDA #$003B             ;\
; $A9:8E04 8D 7A 0F    STA $0F7A  [$7E:0F7A]  ;} Mother Brain's body X position = 3Bh
org $A98E01
	lda #$033b

;;; $8F46: Spawn dust clouds for Mother Brain's ascent ;;;
; $A9:8F7F             dw 003D, 0054, 0020, 0035, 005A, 0043, 0067, 0029
org $A98F7F
	dw $033D, $0354, $0320, $0335, $035A, $0343, $0367, $0329

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

;;; $AEE1: Mother Brain's body function - third phase - death sequence - move to back of room ;;;
; $A9:AEFD A9 28 00    LDA #$0028             ;} Make Mother Brain walk backwards medium towards X position 28h
; $A9:AF00 20 47 C6    JSR $C647  [$A9:C647]  ;/
org $A9AEFD
       LDA #$0328 

;;; $AF21: Mother Brain's body function - third phase - death sequence - stumble to middle of room and drool ;;;
; $A9:AF27 A9 60 00    LDA #$0060             ;} Make Mother Brain walk forwards really fast towards X position 60h
; $A9:AF2A 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9AF27
	LDA #$0360

;;; $B32A: Mother Brain's body function - third phase - death sequence - blow up escape door ;;;
; $A9:B333 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A9:B337             dx  00, 06, B677       ;} Spawn Mother Brain's room escape door
org $A9B337
        db $3f

;;; $B88F: Mother Brain second phase - firing death beam - back up ;;;
; $A9:B892 A9 28 00    LDA #$0028             ;} Make Mother Brain walk backwards slow towards X position 28h
; $A9:B895 20 47 C6    JSR $C647  [$A9:C647]  ;/
org $A9B892
        LDA #$0328

;;; $B781: Mother Brain's body function - firing bomb - decide on walking ;;;
; $A9:B781 AD E5 05    LDA $05E5  [$7E:05E5]  ;\
; $A9:B784 C9 80 FF    CMP #$FF80             ;} If [random number] >= FF80h: go to decide on crouching
; $A9:B787 B0 2E       BCS $2E    [$B7B7]     ;/
; $A9:B789 A2 40 00    LDX #$0040             ; X = 40h (target X position)
; $A9:B78C C9 00 60    CMP #$6000             ;\
; $A9:B78F B0 03       BCS $03    [$B794]     ;} If [random number] < 6000h:
; $A9:B791 A2 60 00    LDX #$0060             ; X = 60h (target X position)
org $A9B789
        LDX #$0340
org $A9B791
        LDX #$0360

;;; $BC3F: Move Samus horizontally towards wall ;;;
;;     Carry: Set if reached wall (X position EBh), clear otherwise
; $A9:BC59 C9 EB 00    CMP #$00EB
org $A9BC59
	CMP #$03DB
; $A9:BC65 A9 EB 00    LDA #$00EB
org $A9BC65
	LDA #$03DB

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
        dw $0480

;;; $BF41: Mother Brain's body function - drained by Shitroid - move to back of room ;;;
; $A9:BF41 A9 28 00    LDA #$0028             ;\
; $A9:BF44 20 47 C6    JSR $C647  [$A9:C647]  ;} Make Mother Brain walk backwards towards X position 28h with animation delay [Y]
org $A9BF41
       LDA #$0328 

;;; $BFD0: Mother Brain painful walking function - walk forwards  ;;;
; $A9:BFD5 A9 48 00    LDA #$0048             ;} Make Mother Brain walk forwards towards X position 48h with animation delay [$7E:784E]
; $A9:BFD8 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9BFD5
        LDA #$0348

;;; $C004: Mother Brain painful walking function - walk backwards ;;;
; $A9:C009 A9 28 00    LDA #$0028             ;} Make Mother Brain walk backwards towards X position 28h with animation delay [$7E:784E]
; $A9:C00C 20 47 C6    JSR $C647  [$A9:C647]  ;/
org $A9C009
        LDA #$0328

;;; $C0FB: Mother Brain's body function - second phase - revive self - walk up to Shitroid ;;;
; $A9:C103 A9 50 00    LDA #$0050             ;} Make Mother Brain walk forwards fast towards X position 50h
; $A9:C106 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9C103
        LDA #$0350

;;; $C147: Mother Brain's body function - second phase - revive self - finish preparing for Shitroid murder ;;;
; $A9:C156 A9 50 00    LDA #$0050             ;} Make Mother Brain walk forwards really slow towards X position 50h
; $A9:C159 20 01 C6    JSR $C601  [$A9:C601]  ;/
org $A9C156
        LDA #$0350

;;; $C18E: Mother Brain's body function - second phase - prepare for final Shitroid attack ;;;
; $A9:C194 A9 40 00    LDA #$0040             ;} Make Mother Brain walk backwards fast towards X position 40h
; $A9:C197 4C 47 C6    JMP $C647  [$A9:C647]  ;/
org $A9C194
        LDA #$0340

;;; $C601: Make Mother Brain walk forwards ;;;
; $A9:C60F C9 80 00    CMP #$0080             ;} If [Mother Brain's body X position] >= 80h: return carry set
; $A9:C612 10 08       BPL $08    [$C61C]     ;/
org $A9C60F
        CMP #$0380

;;; $C647: Make Mother Brain walk backwards ;;;
; $A9:C655 C9 30 00    CMP #$0030             ;} If [Mother Brain's body X position] < 30h: return carry set
; $A9:C658 30 08       BMI $08    [$C662]     ;/
org $A9C655
        CMP #$0330

;;; $C647: Make Mother Brain walk backwards ;;;
;; Parameters:
;;     A: Target X position. Minimum of 2Fh
;;     Y: Speed (actually animation delay)
;; Returns:
;;     Carry: Set if reached target, clear otherwise
; $A9:C647 CD 7A 0F    CMP $0F7A  [$7E:0F7A]  ;\
; $A9:C64A 10 16       BPL $16    [$C662]     ;} If [Mother Brain's body X position] <= [A]: return carry set
; $A9:C64C AF 04 78 7E LDA $7E7804[$7E:7804]  ;\
; $A9:C650 D0 0E       BNE $0E    [$C660]     ;} If [Mother Brain's pose] != standing: return return carry clear
; $A9:C652 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C655 C9 30 00    CMP #$0030             ;} If [Mother Brain's body X position] < 30h: return carry set
org $A9C655
        CMP #$0330

;;; $C6B8: Handle Mother Brain walking ;;;
; $A9:C6D9 AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C6DC C9 80 00    CMP #$0080             ;} If [Mother Brain's body X position] >= 80h: return
org $A9C6DC
	CMP #$0380
; $A9:C6EE AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C6F1 C9 30 00    CMP #$0030             ;} If [Mother Brain's body X position] < 30h: go to BRANCH_MAYBE_WALK_FORWARDS
org $A9C6F1
        CMP #$0330
; $A9:C6FC AD 7A 0F    LDA $0F7A  [$7E:0F7A]  ;\
; $A9:C6FF C9 30 00    CMP #$0030             ;} If [Mother Brain's body X position] >= 30h: return
org $A9C6FF
        CMP #$0330

;;; $C710: Initialisation AI - enemy $ECBF (Shitroid in cutscene) ;;;
; $A9:C741 A9 40 01    LDA #$0140             ;\
; $A9:C744 9D 7A 0F    STA $0F7A,x[$7E:0FFA]  ;} Enemy X position = 140h
org $A9C741
	LDA #$0440 

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
        dw $03A0
org $A9CA24+8
        dw $0430
org $A9CA24+16
        dw $03B0
org $A9CA24+24
        dw $03B0
org $A9CA24+32
        dw $03D0
org $A9CA24+40
        dw $03BD
org $A9CA24+48
        dw $03BC
org $A9CA24+56
        dw $03BB

;;; $CB56: Shitroid function - fly off-screen ;;;
; $A9:CB56 A9 10 01    LDA #$0110             ;\
; $A9:CB59 85 12       STA $12    [$7E:0012]  ;} $12 = 110h
org $A9CB56
	LDA #$0410

;;; $CB7B: Shitroid function - move to final charge start position ;;;
; $A9:CB7B A9 31 01    LDA #$0131             ;\
; $A9:CB7E 85 12       STA $12    [$7E:0012]  ;} $12 = 131h
org $A9CB7B
	LDA #$0431

;;; $CBB3: Shitroid function - initiate final charge ;;;
; $A9:CBB3 A9 22 01    LDA #$0122             ;\
; $A9:CBB6 85 12       STA $12    [$7E:0012]  ;} $12 = 122h
org $A9CBB3
        LDA #$0422

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

;;; $FB72: Initialisation AI - enemy $E27F (zebetites) ;;;
; $A6:FC1B             dw 0338,0278,01B8,00F8 ; X position
org $A6FC1B
        dw $00c8, $0188, $0248, $0308

; Room $DD58, state $DD6E: Enemy population
; Room $DD58, state $DD88: Enemy population
; $A1:E321             dx EC7F,0081,006F,0000,2800,0004,0000,0000, EC3F,0081,006F,0000,2800,0004,0000,0000, E27F,0000,0000,0000,2000,0000,0000,0000, D23F,0337,0036,0000,6000,0000,0001,0000, D23F,0337,00A6,0000,6000,0000,0002,0000, D23F,0277,001C,0000,6000,0000,0003,0000, FFFF, 00
org $A1E323
        dw $0081
org $A1E333
        dw $0381

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
        jmp handle_samus_X_displacement

org $A9B4DE
        nop : nop : nop
        nop : nop : nop

;;; unused space in A9: [$C2E5 -> $C313[
;;; $C2E5: Unused. Mother Brain walking function - crouch ;;;
;;; $C2F9: Unused. Mother Brain walking function - crouching ;;;
;;; $C30B: Unused. Mother Brain walking function - stand up ;;;
org $A9C2E5
handle_samus_X_displacement:
	pha
	;; mb current phase
        lda $7E7800
	beq .phase_1

	;; phase two and three, push samus to the right
	lda #$0001
        sta $0A54
	pla
        bra .end

.phase_1
	;; first phase, push samus to the left
	stz $0A54
	pla
	;; negate X displacement
        EOR #$FFFF
        INC A

.end
        ;; go back to vanilla
	sta $0B58
        jmp $B4C6

warnpc $A9C303
