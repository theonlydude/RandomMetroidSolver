;;; compile with thedopefish asar
;;; mirror crocomire

arch 65816
lorom

;;; crocomire

;  ____________________________________ Enemy ID
; |     _______________________________ X position
; |    |     __________________________ Y position
; |    |    |     _____________________ Initialisation parameter (orientation in SMILE)
; |    |    |    |     ________________ Properties (special in SMILE)
; |    |    |    |    |     ___________ Extra properties (special graphics bitset in SMILE)
; |    |    |    |    |    |     ______ Parameter 1 (speed in SMILE)
; |    |    |    |    |    |    |     _ Parameter 2 (speed2 in SMILE)
; |    |    |    |    |    |    |    |
; iiii xxxx yyyy oooo pppp gggg aaaa bbbb
; Room $A98D, state $A9B9: Enemy population
; $A1:BB0E             dx DDBF,0480,0078,BD2A,A800,0004,0000,0000,
;                         DDFF,0480,0078,BD2A,A800,0004,0000,0000, FFFF, 00
org $A1BB0E+2                   ; croc
        dw $0380
org $A1BB1E+2                   ; tongue
        dw $0380

;;; $8692: Crocomire constants ;;;
; $A4:86A2             dw 0300
; $A4:86A4             dw 0640
org $A486A2
        dw $0500                 ; compared to croc X position
org $A486A4
        dw $01B0                ; compared to croc x position before falling in acid

;;; croc PLMs
; $84:B747             dw B3C1,AFCA   ; Clear Crocomire's bridge
; $84:B74B             dw B3C1,AFD0   ; Crumble a block of Crocomire's bridge
; $84:B74F             dw B3C1,AFD6   ; Clear a block of Crocomire's bridge
; $84:B753             dw B3C1,AFDC   ; Clear Crocomire invisible wall - clears 8 blocks in a column for 3 columns
; $84:B757             dw B3C1,AFE2   ; Create Crocomire invisible wall - clears 8 blocks in a column for 3 columns

;;; when croc is already dead
; $A4:8AF6 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:8AFA             dx 20,03,B753          ;} Spawn PLM to clear Crocomire invisible wall at (20h, 3)
org $A48AFA
        db $5D
; $A4:8AFE 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:8B02             dx 1E,03,B753          ;} Spawn PLM to clear Crocomire invisible wall at (1Eh, 3)
org $A48B02
        db $5F
; $A4:8B06 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:8B0A             dx 61,0B,B747          ;} Spawn PLM to clear Crocomire's bridge
org $A48B0A
        db $15

;;; when croc dies
; $A4:90D0 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:90D4             dx 4E,03,B753
org $A490D4
        db $2F

; $A4:996A 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:996E             dx 20,03,B753          ;} Spawn PLM to clear Crocomire invisible wall at (20h, 3)
org $A4996E
        db $5D
; $A4:9972 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:9976             dx 1E,03,B757          ;} Spawn PLM to clear Crocomire invisible wall at (1Eh, 3)
org $A49976 
        db $5F
; $A4:997A 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:997E             dx 70,0B,B747          ;} Spawn PLM to clear Crocomire's bridge at (70h, Bh) <-- ok but the bridge is Fh blocks to the left... so this does nothing
org $A4997E
        db $15

; $A4:9B3A 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:9B3E             dx 30,03,B753
org $A49B3E
        db $4D
; $A4:9B70 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:9B74             dx 1E,03,B753
org $A49B74
        db $5F
; $A4:8E9F 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8EA3             dx 4E,03,B757
org $A48EA3
        db $2F
; $A4:97EB 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:97EF             dx 30,03,B757
org $A497EF
        db $4D

; $A4:8AF6 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:8AFA             dx 20,03,B753          ;} Spawn PLM to clear Crocomire invisible wall at (20h, 3)
org $A48AFA
        db $5D
; $A4:8AFE 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:8B02             dx 1E,03,B753          ;} Spawn PLM to clear Crocomire invisible wall at (1Eh, 3)
org $A48B02
        db $5F
; $A4:8B06 22 D7 83 84 JSL $8483D7[$84:83D7]  ;\
; $A4:8B0A             dx 61,0B,B747          ;} Spawn PLM to clear Crocomire's bridge
org $A48B0A
	db $15

;;; Crumble a block of Crocomire's bridge
; $A4:8DBE 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8DC2             dx 61,0B,B74B
org $A48DC2
        db $1E
; $A4:8E07 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8E0B             dx 62,0B,B74B
; $A4:8E0F 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8E13             dx 63,0B,B74B
org $A48E0B
        db $1D
org $A48E13
        db $1C

;;; Clear a block of Crocomire's bridge
; $A4:8EE5 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8EE9             dx 61,0B,B74F
; $A4:8EED 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8EF1             dx 62,0B,B74F
; $A4:8EF5 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8EF9             dx 63,0B,B74F
; $A4:8EFD 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8F01             dx 64,0B,B74F
; $A4:8F05 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8F09             dx 65,0B,B74F
; $A4:8F0D 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8F11             dx 66,0B,B74F
; $A4:8F15 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8F19             dx 67,0B,B74F
; $A4:8F1D 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8F21             dx 68,0B,B74F
; $A4:8F25 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8F29             dx 69,0B,B74F
; $A4:8F2D 22 D7 83 84 JSL $8483D7[$84:83D7]
; $A4:8F31             dx 6A,0B,B74F
org $A48EE9
	db $1E
org $A48EF1
	db $1D
org $A48EF9
	db $1C
org $A48F01
	db $1B
org $A48F09
	db $1A
org $A48F11
	db $19
org $A48F19
	db $18
org $A48F21
	db $17
org $A48F29
	db $16
org $A48F31
	db $15


;;; scrolls updates
; $A4:8ADC A9 01 01    LDA #$0101
; $A4:8ADF 8F 20 CD 7E STA $7ECD20[$7E:CD20]
; $A4:8AE3 8F 22 CD 7E STA $7ECD22[$7E:CD22]
org $A48ADF
        STA $7ECD26
        STA $7ECD24
; $A4:8C72 A9 01 01    LDA #$0101
; $A4:8C75 8F 24 CD 7E STA $7ECD24[$7E:CD24]
org $A48C75
        STA $7ECD22
; $A4:8C79 AD F6 0A    LDA $0AF6  [$7E:0AF6]
; $A4:8C7C C9 20 05    CMP #$0520
; $A4:8C7F 30 07       BMI $07    [$8C88]
; $A4:8C81 A9 00 01    LDA #$0100
; $A4:8C84 8F 24 CD 7E STA $7ECD24[$7E:CD24]
org $A48C7C
        CMP #$02e0
        BPL $07
        LDA #$0001
        STA $7ECD22
; $A4:90BD A9 01 01    LDA #$0101
; $A4:90C0 8F 24 CD 7E STA $7ECD24[$7E:CD24]
org $A490C0
        STA $7ECD22
; $A4:97E4 A9 00 01    LDA #$0100
; $A4:97E7 8F 23 CD 7E STA $7ECD23[$7E:CD23]
org $A497E4
        LDA #$0001
; $A4:9B65 A9 01 01    LDA #$0101
; $A4:9B68 8F 20 CD 7E STA $7ECD20[$7E:CD20]
; $A4:9B6C 8F 22 CD 7E STA $7ECD22[$7E:CD22]
org $A49B68
        STA $7ECD26
        STA $7ECD24

;;; $8717:  ;;;
; $A4:8737 AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:873A CD A2 86    CMP $86A2  [$A4:86A2]
; $A4:873D 30 09       BMI $09    [$8748]
;;; compare croc x to constant before moving toward samus
org $A4873D
	BPL $09

;;; $87E9:  ;;;
; $A4:87E9 AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:87EC CD A2 86    CMP $86A2  [$A4:86A2]
; $A4:87EF 30 09       BMI $09    [$87FA]
;;; compare croc x to constant before moving toward samus
org $A487EF
	BPL $09

;;; $895E:  ;;;
; $A4:895E AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:8961 C9 A0 02    CMP #$02A0
; $A4:8964 10 13       BPL $13    [$8979]
org $A48961
        CMP #$560
        BMI $13

;;; $8A5A: Initialisation AI - enemy $DDBF (Crocomire) ;;;
; $A4:8A8F A9 00 00    LDA #$0000
; $A4:8A92 8F 20 CD 7E STA $7ECD20[$7E:CD20]
;;; update scroll
org $A48A92
        sta $7ECD26
;;; camera distance index to 2, use camera 4 that we created for Kraid
; $A4:8ABA A9 02 00    LDA #$0002
; $A4:8ABD 8D 41 09    STA $0941  [$7E:0941]
org $A48ABA
	LDA #$0004
; $A4:8B20 A9 40 02    LDA #$0240
; $A4:8B23 8D 7A 0F    STA $0F7A  [$7E:0F7A]
org $A48B20
        LDA #$05C0

;;; $8B5B:  ;;;
; $A4:8BC8 AD 11 09    LDA $0911  [$7E:0911]  ;\
; $A4:8BCB 38          SEC                    ;|
; $A4:8BCC FD 7A 0F    SBC $0F7A,x[$7E:0F7A]  ;|
; $A4:8BCF 18          CLC                    ;|
; $A4:8BD0 69 33 00    ADC #$0033             ;} BG2 X scroll = |[layer 1 X position] + 33h - [enemy X position]|
; $A4:8BD3 48          PHA                    ;|
; $A4:8BD4 10 04       BPL $04    [$8BDA]     ;|
; $A4:8BD6 49 FF FF    EOR #$FFFF             ;|
; $A4:8BD9 1A          INC A                  ;/
; 
; $A4:8BDA C9 1C 01    CMP #$011C             ;\
; $A4:8BDD 30 05       BMI $05    [$8BE4]     ;} If [BG2 X scroll] >= 11Ch:
; $A4:8BDF 68          PLA                    ;\
; $A4:8BE0 A9 00 01    LDA #$0100             ;} BG2 X scroll = 100h
; $A4:8BE3 48          PHA                    ;/
;;; fix layer2 scroll to display mirrored croc body
org $A48BCF
        CLC
        ADC #$004d

;;; $8C95:  ;;;
; $A4:8C95 AD A8 0F    LDA $0FA8  [$7E:0FA8]
; $A4:8C98 D0 30       BNE $30    [$8CCA]
; $A4:8C9A AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:8C9D 38          SEC
; $A4:8C9E ED 82 0F    SBC $0F82  [$7E:0F82]
; $A4:8CA1 ED FE 0A    SBC $0AFE  [$7E:0AFE]
; $A4:8CA4 ED F6 0A    SBC $0AF6  [$7E:0AF6]
; $A4:8CA7 10 21       BPL $21    [$8CCA]
; $A4:8CA9 22 77 A4 A0 JSL $A0A477[$A0:A477]
; $A4:8CAD AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:8CB0 38          SEC
; $A4:8CB1 ED 82 0F    SBC $0F82  [$7E:0F82]
; $A4:8CB4 38          SEC
; $A4:8CB5 ED FE 0A    SBC $0AFE  [$7E:0AFE]
; $A4:8CB8 8D F6 0A    STA $0AF6  [$7E:0AF6]
; $A4:8CBB 8D 10 0B    STA $0B10  [$7E:0B10]
; $A4:8CBE A9 FC FF    LDA #$FFFC             ;\
; $A4:8CC1 8D 58 0B    STA $0B58  [$7E:0B58]  ;} Extra Samus X displacement = -4
; $A4:8CC4 A9 FF FF    LDA #$FFFF             ;\
; $A4:8CC7 8D 5C 0B    STA $0B5C  [$7E:0B5C]  ;} Extra Samus Y displacement = -1
; 
; $A4:8CCA 60          RTS
org $A48CA7
        bmi $21
org $A48CB0
        clc
        adc $0F82               ; enemy x radius
        clc
        adc $0AFE               ; samus x radius
org $A48CBE
        lda #$0004              ; inverse x displacement

;;; $8D5E:  ;;;
; $A4:8D5F AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:8D62 C9 00 06    CMP #$0600
; $A4:8D65 30 28       BMI $28    [$8D8F]
; $A4:8D67 C9 10 06    CMP #$0610
; $A4:8D6A 10 38       BPL $38    [$8DA4]
org $A48D62
        CMP #$0200
        BPL $28
        CMP #$01F0
        BMI $38
; $A4:8DA4 AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:8DA7 C9 10 06    CMP #$0610
; $A4:8DAA 30 30       BMI $30    [$8DDC]
; $A4:8DAC C9 20 06    CMP #$0620
; $A4:8DAF 10 3C       BPL $3C    [$8DED]
org $A48DA7
        CMP #$01F0
        BPL $30
        CMP #$01E0
        BMI $3C
; $A4:8DC6 A9 20 06    LDA #$0620
;;; spawn dust cloud
org $A48DC6
        LDA #$01E0
; $A4:8DED AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:8DF0 C9 20 06    CMP #$0620
; $A4:8DF3 30 38       BMI $38    [$8E2D]
; $A4:8DF5 C9 30 06    CMP #$0630
; $A4:8DF8 10 40       BPL $40    [$8E3A]
org $A48DF0
	CMP #$01E0
        BPL $38
        CMP #$01C0              ; 0x10 more pixel on the left for croc mouth to not touch the floor
        BMI $40

;;; $8FDF:  ;;;
; $A4:8FEE A9 FC FF    LDA #$FFFC             ;|
; $A4:8FF1 85 14       STA $14    [$7E:0014]  ;} Move enemy left by 4.0
; $A4:8FF3 22 AB C6 A0 JSL $A0C6AB[$A0:C6AB]  ;/
org $A48FEE
        LDA #$0004

;;; $905B:  ;;;
; $A4:9062 A9 04 00    LDA #$0004            ; movement length
; $A4:9065 85 14       STA $14    [$7E:0014]
; $A4:9067 AD 7A 0F    LDA $0F7A  [$7E:0F7A] ; x position
; $A4:906A 38          SEC
; $A4:906B ED 82 0F    SBC $0F82  [$7E:0F82] ; x radius
; $A4:906E E9 00 01    SBC #$0100            ; screen x size
; $A4:9071 E5 14       SBC $14    [$7E:0014]
; $A4:9073 CD 11 09    CMP $0911  [$7E:0911] ; layer x position
; $A4:9076 10 04       BPL $04    [$907C]
; $A4:9078 22 AB C6 A0 JSL $A0C6AB[$A0:C6AB] ; Move enemy right by [$14].[$12]
org $A49062
        LDA #$FFFC

;;; $907F: Move enemy right by 4.0 ;;;
; $A4:9083 A9 04 00    LDA #$0004
; $A4:9086 85 14       STA $14    [$7E:0014]
org $A49083
	LDA #$FFFC

;;; $9108:  ;;;
; $A4:9156             dw 0780, 0730, 0790, 0740, 07B0, 0760, 07A0, 0770, 0710, 0750, 0720
;;; croc bridge crumbling enemy projectile x positions
;;; displayed outside of the screen in vanilla, so don't display them either
;org $A49156
;        dw $0180,$01d0,$0170,$01c0,$0150,$01a0,$0160,$0190,$01f0,$01b0,$01e0

;;; $916C:  ;;;


;;; $97D3:  ;;;
; $A4:97D5 AD F6 0A    LDA $0AF6  [$7E:0AF6]
; $A4:97D8 C9 80 02    CMP #$0280
; $A4:97DB 10 52       BPL $52    [$982F]
org $A497D8
        cmp #$580
	bmi $52

;;; $9830:  ;;;
; $A4:9830 AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:9833 38          SEC
; $A4:9834 E9 02 00    SBC #$0002
; $A4:9837 8D 7A 0F    STA $0F7A  [$7E:0F7A]
; $A4:983A C9 E0 01    CMP #$01E0
; $A4:983D 30 07       BMI $07    [$9846]
; $A4:983F A9 DC 00    LDA #$00DC
; $A4:9842 8D 7E 0F    STA $0F7E  [$7E:0F7E]
; $A4:9845 60          RTS
; 
; $A4:9846 A9 E0 01    LDA #$01E0
; $A4:9849 8D 7A 0F    STA $0F7A  [$7E:0F7A]
; $A4:984C A9 36 00    LDA #$0036
; $A4:984F 8D 7E 0F    STA $0F7E  [$7E:0F7E]
; $A4:9852 A9 3E 00    LDA #$003E
; $A4:9855 8D A8 0F    STA $0FA8  [$7E:0FA8]
; $A4:9858 60          RTS
org $A49833
	CLC
        ADC #$002
org $A4983A
        CMP #$0620
        BPL $07
org $A49846
        LDA #$0620

;;; $990A:  ;;;
; $A4:9952 A9 E0 01    LDA #$01E0
; $A4:9955 8D 7A 0F    STA $0F7A  [$7E:0F7A]
org $A49952
	LDA #$0620

;;; $99E5:  ;;;
;;; before croc breaks the spike wall
; $A4:99E5 AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:99E8 C9 E0 00    CMP #$00E0
; $A4:99EB 10 2E       BPL $2E    [$9A1B]
org $A499E8
        CMP #$0720
        BMI $2E
; $A4:99F7 AD B2 0F    LDA $0FB2  [$7E:0FB2]
; $A4:99FA 69 00 00    ADC #$0000
; $A4:99FD C9 02 00    CMP #$0002
; $A4:9A00 30 03       BMI $03    [$9A05]
; $A4:9A02 A9 02 00    LDA #$0002
org $A499FD
        CMP #$FFFE
        BPL $03
        LDA #$FFFE

;;; $9A38:  ;;;
; $A4:9A42 AD B2 0F    LDA $0FB2  [$7E:0FB2]
; $A4:9A45 69 00 00    ADC #$0000
; $A4:9A48 C9 05 00    CMP #$0005
; $A4:9A4B 30 03       BMI $03    [$9A50]
; $A4:9A4D A9 05 00    LDA #$0005
org $A49A48
        CMP #$FFFB
        BPL $03
        LDA #$FFFB
;;; croc skeleton moves after breaking the spike wall
; $A4:9A69 18          CLC
; $A4:9A6A 6D B0 0F    ADC $0FB0  [$7E:0FB0]
; $A4:9A6D 8D 7C 0F    STA $0F7C  [$7E:0F7C]
; $A4:9A70 AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:9A73 6D B2 0F    ADC $0FB2  [$7E:0FB2]
; $A4:9A76 8D 7A 0F    STA $0F7A  [$7E:0F7A]
org $A49A69
        SEC
        SBC $0FB0
org $A49A73
        SBC $0FB2
; $A4:9A76 8D 7A 0F    STA $0F7A  [$7E:0F7A]
; $A4:9A79 C9 40 02    CMP #$0240
; $A4:9A7C 30 1C       BMI $1C    [$9A9A]
org $A49A79
        CMP #$05C0
        BPL $1C

;;; $9ADA:  ;;;
;;; spawn dust clouds when croc skeleton collapses
org $A49A9B
        LDA #$0020
org $A49AA5
        LDA #$0020
org $A49AAA
        LDA #$FFF0
org $A49AB4
        LDA #$FFF8
org $A49AB9
        LDA #$FFF0
org $A49ABE
        LDA #$FFE8
org $A49AC3
        LDA #$FFE0
org $A49AC8
        LDA #$FFD8
org $A49ACD
        LDA #$FFD0
org $A49AD2
        LDA #$FFC8
org $A49AD7
        LDA #$FFC0

;;; $9B06:  ;;;
; $A4:9B1A AD 7A 0F    LDA $0F7A  [$7E:0F7A]
; $A4:9B1D 18          CLC
; $A4:9B1E 69 40 00    ADC #$0040
; $A4:9B21 8D 7A 0F    STA $0F7A  [$7E:0F7A]
org $A49B1E
        ADC #$FFC0

;;; $B93D:  ;;;
;;; when samus touches croc, inverse X displacement
; $A4:B94A A9 FC FF    LDA #$FFFC             ;\
; $A4:B94D 8D 58 0B    STA $0B58  [$7E:0B58]  ;} Extra Samus X displacement = -4
org $A4B94A
        lda #$0004

;;; $F67A: Initialisation AI - enemy $DDFF (Crocomire's tongue) ;;;
; $A4:F69E A9 17 00    LDA #$0017
; $A4:F6A1 9D A8 0F    STA $0FA8,x[$7E:0FE8]
;;; tongue x added to croc position
org $A4F69E
        LDA #$FFE9

;;; $B9D8: Crocomire death item drop routine ;;;
; $A0:B9E9 69 40 02    ADC #$0240
org $A0B9E9
        ADC #$0540

;;; croc spite
; $86:9026 A9 00 FE    LDA #$FE00
; $86:9029 99 B7 1A    STA $1AB7,y[$7E:1AD5]
; $86:902C A9 01 00    LDA #$0001
; $86:902F 99 DB 1A    STA $1ADB,y[$7E:1AF9]
; $86:9032 BD 7A 0F    LDA $0F7A,x[$7E:0F7A]
; $86:9035 38          SEC
; $86:9036 E9 20 00    SBC #$0020
; $86:9039 99 4B 1A    STA $1A4B,y[$7E:1A69]
org $869026
	lda #$0200              ; x velocity
org $869035
        CLC
        ADC #$0020              ; x position
;;; x velocity
; $86:909D 99 B7 1A    STA $1AB7,y[$7E:1AD5]
org $86909D
	jsr inverse_spite_x_velocity

;;; croc spike wall pieces
; $86:90DD A9 10 02    LDA #$0210
; $86:90E0 99 4B 1A    STA $1A4B,y[$7E:1A6D]
org $8690DD
	lda #$05F0

;;; move croc spike wall pieces on X axis
; $86:914A BD B7 1A    LDA $1AB7,x[$7E:1AD9]
; $86:914D 18          CLC
; $86:914E 7D 28 1A    ADC $1A28,x[$7E:1A4A]
; $86:9151 9D 28 1A    STA $1A28,x[$7E:1A4A]
; $86:9154 BD B8 1A    LDA $1AB8,x[$7E:1ADA]
; $86:9157 7D 4B 1A    ADC $1A4B,x[$7E:1A6D]
; $86:915A 9D 4B 1A    STA $1A4B,x[$7E:1A6D]
; $86:915D BD 4C 1A    LDA $1A4C,x[$7E:1A6E]
; $86:9160 69 00       ADC #$00
; $86:9162 9D 4C 1A    STA $1A4C,x[$7E:1A6E]
org $86914A
	jmp update_spike_wall_x_pos
org $869165
return_from_spike_wall_update:

;;; use freespace in unused proc [$86922F -> $86926F]
org $86922F
update_spike_wall_x_pos:
    LDA $7E1A27+1,X             ; x speed
    SEC
    SBC $7E1AB7,X               ; x accel
    STA $7E1A27+1,X             ; x speed
    LDA $7E1A4B,X               ; x position low
    SBC $7E1AB7+1,X             ; x diff
    STA $7E1A4B,X               ; x position low
    LDA $7E1A4B+1,X             ; x position high
    SBC #$00                    ; propagate carry if exists
    STA $7E1A4B+1,X             ; x position high
    JMP return_from_spike_wall_update

inverse_spite_x_velocity:
        eor #$FFFF
        inc a
        ;; vanilla
        STA $1AB7,y
        RTS
warnpc $86926F


; Enemy projectile $8F9D (Crocomire bridge crumbling)
org $8d8109
    dw $0001 : dw $c3f4 : db $fc : dw $61cc
; Enemy projectile $90C1 (Crocomire spike wall pieces)
org $8d8110
    dw $0002 : dw $c3e8 : db $f8 : dw $67ee : dw $c3f8 : db $f8 : dw $25cc

;;; croc melting bg2
org $a49c79
    dw $0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$7c01,$7c50,$7c40,$7c30,$7c20,$7c00
org $a49cb9
    dw $0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$7c51,$7c41,$7c23,$7c43,$7c33,$7c04,$7c11,$7c10
org $a49cf9
    dw $0338,$0338,$0338,$0338,$0338,$0338,$7c22,$7c12,$7c34,$7c24,$7c54,$7c44,$7c05,$7c14,$7c02,$0338
org $a49d39
    dw $0338,$0338,$0338,$0338,$0338,$7c52,$7c13,$7c46,$7c36,$7c26,$7c16,$7c06,$7c15,$7c53,$0338,$0338
org $a49d79
    dw $0338,$0338,$0338,$0338,$0338,$7c03,$7c47,$7c37,$7c27,$7c17,$7c07,$7c56,$7c25,$0338,$0338,$0338
org $a49db9
    dw $0338,$0338,$0338,$0338,$0338,$7c35,$7c48,$7c38,$7c28,$7c18,$7c08,$7c57,$0338,$0338,$0338,$0338
org $a49df9
    dw $0338,$0338,$0338,$0338,$0338,$7c59,$7c49,$7c29,$7c29,$7c19,$7c09,$7c58,$7c45,$7c21,$7c32,$0338
org $a49e39
    dw $0338,$0338,$0338,$0338,$0338,$7c0b,$7c5a,$7c4a,$7c3a,$7c2a,$7c1a,$7c0a,$7c55,$7c31,$7c42,$0338
org $a49e7b
    dw $0338,$0338,$0338,$0338,$0338,$0338,$7c00,$0338,$0338,$0338,$0338,$0338,$7c30,$7c20,$7c10,$7c00
org $a49ebb
    dw $0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$0338,$7c23,$7c50,$7c21,$7c11,$7c40
org $a49efb
    dw $0338,$0338,$0338,$0338,$0338,$7c53,$7c01,$7c33,$0338,$0338,$7c03,$7c54,$7c04,$7c42,$7c32,$0338
org $a49f3b
    dw $0338,$0338,$0338,$0338,$0338,$7c22,$7c12,$7c02,$7c14,$7c24,$7c05,$7c44,$7c34,$0338,$0338,$0338
org $a49f7b
    dw $0338,$0338,$0338,$0338,$7c3a,$7c36,$7c26,$7c16,$7c06,$7c55,$7c45,$7c35,$0338,$0338,$0338,$0338
org $a49fbb
    dw $0338,$0338,$0338,$0338,$7c47,$7c37,$7c27,$7c17,$7c07,$7c56,$7c46,$0338,$0338,$0338,$0338,$0338
org $a49ffb
    dw $0338,$0338,$0338,$0338,$7c09,$7c58,$7c48,$7c38,$7c28,$7c18,$7c08,$7c57,$7c51,$7c41,$7c31,$0338
org $a4a03b
    dw $0338,$0338,$0338,$0338,$7c3a,$7c2a,$7c1a,$7c0a,$7c59,$7c49,$7c39,$7c13,$7c19,$7c52,$7c43,$0338

;;; extended spritemaps
org $a4bfc6
    dw $fffd
org $a4bfd6
    dw $001d
org $a4bff8
    dw $ffff
org $a4c008
    dw $001d
org $a4c03a
    dw $001d
org $a4c05c
    dw $ffff
org $a4c06c
    dw $001d
org $a4c08e
    dw $ffff
org $a4c09e
    dw $001d
org $a4c0c0
    dw $ffff
org $a4c0d0
    dw $001d
org $a4c0f2
    dw $ffff
org $a4c102
    dw $001d
org $a4c124
    dw $ffff
org $a4c134
    dw $001d
org $a4c156
    dw $ffff
org $a4c166
    dw $001d
org $a4c188
    dw $ffff
org $a4c198
    dw $001d
org $a4c1ba
    dw $ffff
org $a4c1ca
    dw $001d
org $a4c1ec
    dw $ffff
org $a4c1fc
    dw $001d
org $a4c21e
    dw $ffff
org $a4c22e
    dw $001d
org $a4c250
    dw $ffff
org $a4c260
    dw $001d
org $a4c282
    dw $ffff
org $a4c292
    dw $001d
org $a4c2bc
    dw $0003
org $a4c2cc
    dw $001d
org $a4c2f6
    dw $0003
org $a4c306
    dw $001d
org $a4c330
    dw $0003
org $a4c340
    dw $001d
org $a4c36a
    dw $0003
org $a4c37a
    dw $001d
org $a4c3a4
    dw $0003
org $a4c3b4
    dw $001d
org $a4c3de
    dw $0003
org $a4c3ee
    dw $001d
org $a4c418
    dw $0003
org $a4c428
    dw $001d
org $a4c45a
    dw $001d
org $a4c47c
    dw $ffff
org $a4c48c
    dw $001d
org $a4c4be
    dw $001d
org $a4c4e0
    dw $ffff
org $a4c4f0
    dw $001d
org $a4c522
    dw $001d
org $a4c544
    dw $ffff
org $a4c554
    dw $001d
org $a4c576
    dw $ffff
org $a4c586
    dw $001d
org $a4c5b0
    dw $ffff
org $a4c5c0
    dw $001d
org $a4c5ea
    dw $ffff
org $a4c5fa
    dw $001d
org $a4c660
    dw $0020
org $a4c66a
    dw $0020
org $a4c674
    dw $0020
org $a4c67e
    dw $0020
org $a4c6a6
    dw $fffd
org $a4c6b6
    dw $001d
org $a4c6e0
    dw $ffff
org $a4c6f0
    dw $001d
org $a4c72a
    dw $001d
org $a4c754
    dw $ffff
org $a4c764
    dw $001d
org $a4c78e
    dw $ffff
org $a4c79e
    dw $001d
org $a4c7c8
    dw $ffff
org $a4c7d8
    dw $001d
org $a4c802
    dw $ffff
org $a4c812
    dw $001d
org $a4c83c
    dw $ffff
org $a4c84c
    dw $001d
org $a4c876
    dw $ffff
org $a4c886
    dw $001d
org $a4c8b0
    dw $ffff
org $a4c8c0
    dw $001d
org $a4c8ea
    dw $ffff
org $a4c8fa
    dw $001d
org $a4c924
    dw $ffff
org $a4c934
    dw $001d
org $a4c95e
    dw $ffff
org $a4c96e
    dw $001d
org $a4c9a8
    dw $001d
org $a4c9d2
    dw $ffff
org $a4c9e2
    dw $001d
org $a4ca1c
    dw $001d
org $a4ca46
    dw $ffff
org $a4ca56
    dw $001d
org $a4cad0
    dw $ffff
org $a4cae4
    dw $ffff
org $a4caf8
    dw $ffff

;;; hitboxes
org $a4cb09
    dw $0010,$0020,$004e,$002b
org $a4cb17
    dw $0010,$000b,$005f,$000b
org $a4cb25
    dw $0010,$001f,$0045,$002c
org $a4cb33
    dw $0010,$0012,$003c,$0020
org $a4cb41
    dw $0010,$000d,$0050,$001b
org $a4cb51
    dw $0010,$fffa,$005f,$001b
org $a4cb61
    dw $0010,$fff7,$003b,$0005
org $a4cb6f
    dw $001e,$ffdc,$005d,$fff3
org $a4cb7d
    dw $fffc,$fffb,$0005,$0004
org $a4cb8b
    dw $fffb,$fff9,$0006,$0006
org $a4cb99
    dw $fff9,$fff8,$0008,$0007
org $a4cba7
    dw $fff8,$fff8,$0009,$0007
org $a4cbb7
    dw $fff8,$fff7,$0009,$0007
org $a4cbc7
    dw $ffd8,$ffdb,$0032,$fff0
org $a4cbd3
    dw $ffd6,$ffc6,$0034,$ffda
org $a4cbdf
    dw $ffd8,$fff3,$0020,$0000
org $a4cbed
    dw $fff3,$ffcb,$002e,$fff0
org $a4cbf9
    dw $fff0,$ffb6,$0029,$ffc7
org $a4cc05
    dw $fff0,$fff0,$0025,$fffd
org $a4cc13
    dw $ffda,$ffce,$0025,$fffc
org $a4cc21
    dw $ffdb,$ffd0,$0026,$0034
org $a4cc2f
    dw $ffd6,$fffc,$0026,$0034

;;; sprite maps
org $a4cc3d
    dw $0011 : dw $0014 : db $18 : dw $71a6 : dw $0004 : db $18 : dw $71bf : dw $000c : db $18 : dw $71af : dw $81d4 : db $10 : dw $71ca : dw $81e4 : db $10 : dw $71c8 : dw $81f4 : db $10 : dw $71c6 : dw $81d4 : db $00 : dw $71c4 : dw $81e4 : db $00 : dw $71c2 : dw $81f4 : db $00 : dw $71c0 : dw $01ec : db $e8 : dw $71b6 : dw $81d4 : db $f0 : dw $71ad : dw $81e4 : db $f0 : dw $71ab : dw $81f4 : db $f0 : dw $71a9 : dw $8004 : db $f0 : dw $71a7 : dw $81f4 : db $e0 : dw $71a4 : dw $8004 : db $e0 : dw $71a2 : dw $8014 : db $e0 : dw $71a0

org $a4cc94
    dw $0011 : dw $01e4 : db $18 : dw $31a6 : dw $01f4 : db $18 : dw $31bf : dw $01ec : db $18 : dw $31af : dw $801c : db $10 : dw $31ca : dw $800c : db $10 : dw $31c8 : dw $81fc : db $10 : dw $31c6 : dw $801c : db $00 : dw $31c4 : dw $800c : db $00 : dw $31c2 : dw $81fc : db $00 : dw $31c0 : dw $000c : db $e8 : dw $31b6 : dw $801c : db $f0 : dw $31ad : dw $800c : db $f0 : dw $31ab : dw $81fc : db $f0 : dw $31a9 : dw $81ec : db $f0 : dw $31a7 : dw $81fc : db $e0 : dw $31a4 : dw $81ec : db $e0 : dw $31a2 : dw $81dc : db $e0 : dw $31a0

org $a4cceb
    dw $000a : dw $01e0 : db $0c : dw $716b : dw $01e8 : db $0c : dw $716a : dw $81e0 : db $fc : dw $7168 : dw $81e0 : db $ec : dw $7166 : dw $81f0 : db $00 : dw $7164 : dw $8000 : db $00 : dw $7162 : dw $81f0 : db $f0 : dw $7164 : dw $8000 : db $f0 : dw $7162 : dw $8010 : db $fc : dw $7180 : dw $8010 : db $ec : dw $7160

org $a4cd1f
    dw $000a : dw $0018 : db $0c : dw $316b : dw $0010 : db $0c : dw $316a : dw $8010 : db $fc : dw $3168 : dw $8010 : db $ec : dw $3166 : dw $8000 : db $00 : dw $3164 : dw $81f0 : db $00 : dw $3162 : dw $8000 : db $f0 : dw $3164 : dw $81f0 : db $f0 : dw $3162 : dw $81e0 : db $fc : dw $3180 : dw $81e0 : db $ec : dw $3160

org $a4cd53
    dw $000f : dw $81d0 : db $10 : dw $718e : dw $81f0 : db $10 : dw $718a : dw $81e0 : db $10 : dw $718c : dw $0000 : db $18 : dw $717b : dw $0008 : db $10 : dw $710f : dw $0000 : db $10 : dw $711f : dw $0011 : db $18 : dw $317a : dw $0018 : db $18 : dw $717a : dw $0028 : db $10 : dw $7188 : dw $0020 : db $10 : dw $7189 : dw $0018 : db $10 : dw $7198 : dw $0010 : db $10 : dw $7199 : dw $8000 : db $00 : dw $7186 : dw $8010 : db $00 : dw $7184 : dw $8020 : db $00 : dw $7182

org $a4cda0
    dw $000f : dw $8020 : db $10 : dw $318e : dw $8000 : db $10 : dw $318a : dw $8010 : db $10 : dw $318c : dw $01f8 : db $18 : dw $317b : dw $01f0 : db $10 : dw $310f : dw $01f8 : db $10 : dw $311f : dw $01e7 : db $18 : dw $717a : dw $01e0 : db $18 : dw $317a : dw $01d0 : db $10 : dw $3188 : dw $01d8 : db $10 : dw $3189 : dw $01e0 : db $10 : dw $3198 : dw $01e8 : db $10 : dw $3199 : dw $81f0 : db $00 : dw $3186 : dw $81e0 : db $00 : dw $3184 : dw $81d0 : db $00 : dw $3182

org $a4cded
    dw $0002 : dw $81f0 : db $f8 : dw $716e : dw $8000 : db $f8 : dw $716c

org $a4cdf9
    dw $0002 : dw $8000 : db $f8 : dw $316e : dw $81f0 : db $f8 : dw $316c

org $a4ce05
    dw $0001 : dw $81f8 : db $f8 : dw $3160

org $a4ce0c
    dw $0001 : dw $81f8 : db $f8 : dw $3180

org $a4ce13
    dw $0001 : dw $81f8 : db $f8 : dw $3162

org $a4ce1a
    dw $0001 : dw $81f8 : db $f8 : dw $3164

org $a4ce21
    dw $0001 : dw $81f8 : db $f8 : dw $3166

org $a4ce28
    dw $0001 : dw $81f8 : db $f8 : dw $3168

org $a4ce2f
    dw $0002 : dw $0000 : db $fc : dw $316b : dw $01f8 : db $fc : dw $316a

org $a4ce3b
    dw $0003 : dw $01f8 : db $04 : dw $3188 : dw $0000 : db $04 : dw $3189 : dw $81f8 : db $f4 : dw $3182

org $a4ce4c
    dw $0005 : dw $01ff : db $08 : dw $717a : dw $01f8 : db $08 : dw $317a : dw $01f8 : db $00 : dw $3198 : dw $0000 : db $00 : dw $3199 : dw $81f8 : db $f0 : dw $3184

org $a4ce67
    dw $0004 : dw $01f8 : db $05 : dw $310f : dw $0000 : db $0d : dw $317b : dw $0000 : db $05 : dw $311f : dw $81f8 : db $f5 : dw $3186

org $a4ce7d
    dw $0001 : dw $81f8 : db $f8 : dw $318a

org $a4ce84
    dw $0001 : dw $81f8 : db $f8 : dw $318c

org $a4ce8b
    dw $0001 : dw $81f8 : db $f8 : dw $318e

org $a4ce92
    dw $0009 : dw $802d : db $1a : dw $70e4 : dw $803d : db $1e : dw $7100 : dw $01f8 : db $07 : dw $7108 : dw $0008 : db $ff : dw $70f6 : dw $8000 : db $07 : dw $7106 : dw $81f8 : db $f7 : dw $70e7 : dw $8004 : db $0b : dw $70e0 : dw $8012 : db $12 : dw $70e0 : dw $8020 : db $19 : dw $70e0

org $a4cec1
    dw $0009 : dw $803f : db $13 : dw $70e4 : dw $804f : db $13 : dw $7100 : dw $0000 : db $09 : dw $70ff : dw $0008 : db $f9 : dw $70ef : dw $8008 : db $01 : dw $70ed : dw $81f8 : db $f9 : dw $710d : dw $8012 : db $05 : dw $7102 : dw $8022 : db $0f : dw $7104 : dw $8030 : db $0f : dw $7102

org $a4cef0
    dw $0007 : dw $8024 : db $1c : dw $70e4 : dw $8034 : db $1e : dw $7100 : dw $81f8 : db $08 : dw $7109 : dw $81f8 : db $f8 : dw $70e9 : dw $81fa : db $0d : dw $70e0 : dw $8008 : db $14 : dw $70e0 : dw $8016 : db $1b : dw $70e0

org $a4cf15
    dw $0009 : dw $01f8 : db $08 : dw $30ff : dw $01f0 : db $f8 : dw $30ef : dw $81e8 : db $00 : dw $30ed : dw $81f8 : db $f8 : dw $310d : dw $801b : db $11 : dw $70e4 : dw $802b : db $11 : dw $7100 : dw $81ee : db $03 : dw $7102 : dw $81fe : db $0d : dw $7104 : dw $800c : db $0d : dw $7102

org $a4cf44
    dw $0007 : dw $8030 : db $0c : dw $70e4 : dw $8040 : db $0c : dw $7100 : dw $81f8 : db $08 : dw $7109 : dw $81f8 : db $f8 : dw $70e9 : dw $8000 : db $0c : dw $70e2 : dw $8010 : db $0c : dw $70e2 : dw $8020 : db $0c : dw $70e2

org $a4cf69
    dw $0008 : dw $01f6 : db $09 : dw $70df : dw $01fe : db $09 : dw $70de : dw $0006 : db $09 : dw $70dd : dw $000e : db $09 : dw $70dc : dw $0016 : db $09 : dw $70db : dw $81fe : db $f9 : dw $712d : dw $81fa : db $f9 : dw $714b : dw $81ef : db $f9 : dw $712b

org $a4cf93
    dw $0008 : dw $01f3 : db $09 : dw $70df : dw $01fb : db $09 : dw $70de : dw $0003 : db $09 : dw $70dd : dw $000b : db $09 : dw $70dc : dw $0013 : db $09 : dw $70db : dw $81fb : db $f9 : dw $712d : dw $81f9 : db $f9 : dw $714b : dw $81ef : db $f9 : dw $712b

org $a4cfbd
    dw $0008 : dw $01f0 : db $09 : dw $70df : dw $01f8 : db $09 : dw $70de : dw $0000 : db $09 : dw $70dd : dw $0008 : db $09 : dw $70dc : dw $0010 : db $09 : dw $70db : dw $81f8 : db $f9 : dw $712d : dw $81f7 : db $f9 : dw $714b : dw $81f0 : db $f9 : dw $712b

org $a4cfe7
    dw $0008 : dw $01ec : db $09 : dw $70df : dw $01f4 : db $09 : dw $70de : dw $01fc : db $09 : dw $70dd : dw $0004 : db $09 : dw $70dc : dw $000c : db $09 : dw $70db : dw $81f4 : db $f9 : dw $712d : dw $81f4 : db $f9 : dw $714b : dw $81f0 : db $f9 : dw $712b

org $a4d011
    dw $0008 : dw $81ed : db $f9 : dw $712d : dw $81ee : db $f9 : dw $314b : dw $01e7 : db $09 : dw $70df : dw $01ef : db $09 : dw $70de : dw $01f7 : db $09 : dw $70dd : dw $01ff : db $09 : dw $70dc : dw $0007 : db $09 : dw $70db : dw $81ef : db $f9 : dw $312b

org $a4d03b
    dw $0008 : dw $81e7 : db $f9 : dw $712d : dw $81ea : db $f9 : dw $314b : dw $01e0 : db $09 : dw $70df : dw $01e8 : db $09 : dw $70de : dw $01f0 : db $09 : dw $70dd : dw $01f8 : db $09 : dw $70dc : dw $0000 : db $09 : dw $70db : dw $81ef : db $f9 : dw $312b

org $a4d065
    dw $0008 : dw $81e0 : db $f9 : dw $712d : dw $81e5 : db $f9 : dw $314b : dw $01d8 : db $09 : dw $70df : dw $01e0 : db $09 : dw $70de : dw $01e8 : db $09 : dw $70dd : dw $01f0 : db $09 : dw $70dc : dw $01f8 : db $09 : dw $70db : dw $81ed : db $f9 : dw $312b

org $a4d08f
    dw $0008 : dw $81e7 : db $f8 : dw $712d : dw $81ea : db $f8 : dw $314b : dw $01e0 : db $09 : dw $70df : dw $01e8 : db $08 : dw $70de : dw $01f0 : db $08 : dw $70dd : dw $01f8 : db $09 : dw $70dc : dw $0000 : db $09 : dw $70db : dw $81ef : db $f9 : dw $312b

org $a4d0b9
    dw $0008 : dw $81ed : db $f5 : dw $712d : dw $81ee : db $f5 : dw $314b : dw $01e7 : db $06 : dw $70df : dw $01ef : db $05 : dw $70de : dw $01f7 : db $05 : dw $70dd : dw $01ff : db $07 : dw $70dc : dw $0007 : db $07 : dw $70db : dw $81ef : db $f9 : dw $312b

org $a4d0e3
    dw $0008 : dw $01ec : db $06 : dw $70df : dw $01f4 : db $05 : dw $70de : dw $01fc : db $05 : dw $70dd : dw $0004 : db $07 : dw $70dc : dw $000c : db $07 : dw $70db : dw $81f4 : db $f5 : dw $712d : dw $81f4 : db $f5 : dw $714b : dw $81f0 : db $f9 : dw $712b

org $a4d10d
    dw $0008 : dw $01f0 : db $06 : dw $70df : dw $01f8 : db $05 : dw $70de : dw $0000 : db $05 : dw $70dd : dw $0008 : db $07 : dw $70dc : dw $0010 : db $07 : dw $70db : dw $81f8 : db $f5 : dw $712d : dw $81f7 : db $f5 : dw $714b : dw $81f0 : db $f9 : dw $712b

org $a4d137
    dw $0008 : dw $01f3 : db $07 : dw $70df : dw $01fb : db $06 : dw $70de : dw $0003 : db $06 : dw $70dd : dw $000b : db $08 : dw $70dc : dw $0013 : db $08 : dw $70db : dw $81fb : db $f6 : dw $712d : dw $81f9 : db $f6 : dw $714b : dw $81ef : db $f9 : dw $712b

org $a4d161
    dw $0008 : dw $01f6 : db $08 : dw $70df : dw $01fe : db $07 : dw $70de : dw $0006 : db $07 : dw $70dd : dw $000e : db $08 : dw $70dc : dw $0016 : db $08 : dw $70db : dw $81fe : db $f7 : dw $712d : dw $81fa : db $f7 : dw $714b : dw $81ef : db $f9 : dw $712b

org $a4d18b
    dw $0008 : dw $01ec : db $04 : dw $70df : dw $01f4 : db $05 : dw $70de : dw $01fc : db $05 : dw $70dd : dw $0004 : db $05 : dw $70dc : dw $000c : db $05 : dw $70db : dw $81f4 : db $f5 : dw $712d : dw $81f4 : db $f5 : dw $714b : dw $81f0 : db $f9 : dw $712b

org $a4d1b5
    dw $0008 : dw $01ec : db $04 : dw $70df : dw $01f4 : db $05 : dw $70de : dw $01fc : db $05 : dw $70dd : dw $0004 : db $05 : dw $70dc : dw $000c : db $05 : dw $70db : dw $81f4 : db $f5 : dw $712d : dw $81f4 : db $f3 : dw $714b : dw $81f0 : db $f5 : dw $712b

org $a4d1df
    dw $0008 : dw $01ec : db $04 : dw $70df : dw $01f4 : db $05 : dw $70de : dw $01fc : db $05 : dw $70dd : dw $0004 : db $05 : dw $70dc : dw $000c : db $05 : dw $70db : dw $81f4 : db $f5 : dw $712d : dw $81f4 : db $f1 : dw $714b : dw $81f0 : db $f1 : dw $712b

org $a4d209
    dw $0009 : dw $81c3 : db $1a : dw $30e4 : dw $81b3 : db $1e : dw $3100 : dw $0000 : db $07 : dw $3108 : dw $01f0 : db $ff : dw $30f6 : dw $81f0 : db $07 : dw $3106 : dw $81f8 : db $f7 : dw $30e7 : dw $81ec : db $0b : dw $30e0 : dw $81de : db $12 : dw $30e0 : dw $81d0 : db $19 : dw $30e0

org $a4d238
    dw $0009 : dw $81b1 : db $13 : dw $30e4 : dw $81a1 : db $13 : dw $3100 : dw $01f8 : db $09 : dw $30ff : dw $01f0 : db $f9 : dw $30ef : dw $81e8 : db $01 : dw $30ed : dw $81f8 : db $f9 : dw $310d : dw $81de : db $05 : dw $3102 : dw $81ce : db $0f : dw $3104 : dw $81c0 : db $0f : dw $3102

org $a4d267
    dw $0007 : dw $81cc : db $1c : dw $30e4 : dw $81bc : db $1e : dw $3100 : dw $81f8 : db $08 : dw $3109 : dw $81f8 : db $f8 : dw $30e9 : dw $81f6 : db $0d : dw $30e0 : dw $81e8 : db $14 : dw $30e0 : dw $81da : db $1b : dw $30e0

org $a4d28c
    dw $0009 : dw $0000 : db $08 : dw $70ff : dw $0008 : db $f8 : dw $70ef : dw $8008 : db $00 : dw $70ed : dw $81f8 : db $f8 : dw $710d : dw $81d5 : db $11 : dw $30e4 : dw $81c5 : db $11 : dw $3100 : dw $8002 : db $03 : dw $3102 : dw $81f2 : db $0d : dw $3104 : dw $81e4 : db $0d : dw $3102

org $a4d2bb
    dw $0007 : dw $800a : db $fa : dw $70eb : dw $81fa : db $fa : dw $710b : dw $8043 : db $fa : dw $70e4 : dw $8053 : db $fa : dw $7100 : dw $8013 : db $fa : dw $70e2 : dw $8023 : db $fa : dw $70e2 : dw $8033 : db $fa : dw $70e2

org $a4d2e0
    dw $0009 : dw $01f8 : db $f0 : dw $b0ff : dw $01f0 : db $00 : dw $b0ef : dw $81e8 : db $f0 : dw $b0ed : dw $81f8 : db $f8 : dw $b10d : dw $81b3 : db $db : dw $30e4 : dw $81a3 : db $db : dw $3100 : dw $81e0 : db $ec : dw $b102 : dw $81d0 : db $e2 : dw $b104 : dw $81c2 : db $e2 : dw $b102

org $a4d30f
    dw $0007 : dw $81e6 : db $fa : dw $30eb : dw $81f6 : db $fa : dw $310b : dw $81ad : db $fa : dw $30e4 : dw $819d : db $fa : dw $3100 : dw $81dd : db $fa : dw $30e2 : dw $81cd : db $fa : dw $30e2 : dw $81bd : db $fa : dw $30e2

org $a4d334
    dw $0009 : dw $0000 : db $08 : dw $70ff : dw $0008 : db $f8 : dw $70ef : dw $8008 : db $00 : dw $70ed : dw $81f8 : db $f8 : dw $710d : dw $81d5 : db $f6 : dw $30e4 : dw $81c5 : db $f6 : dw $3100 : dw $8002 : db $07 : dw $b102 : dw $81f2 : db $fd : dw $b104 : dw $81e4 : db $fd : dw $b102

org $a4d363
    dw $0007 : dw $81f8 : db $08 : dw $3109 : dw $81f8 : db $f8 : dw $30e9 : dw $81c6 : db $fa : dw $30e4 : dw $81b6 : db $fa : dw $3100 : dw $81f3 : db $0b : dw $b102 : dw $81e3 : db $01 : dw $b104 : dw $81d5 : db $01 : dw $b102

org $a4d388
    dw $0009 : dw $01f8 : db $08 : dw $30ff : dw $01f0 : db $f8 : dw $30ef : dw $81e8 : db $00 : dw $30ed : dw $81f8 : db $f8 : dw $310d : dw $801b : db $f6 : dw $70e4 : dw $802b : db $f6 : dw $7100 : dw $81ee : db $07 : dw $f102 : dw $81fe : db $fd : dw $f104 : dw $800c : db $fd : dw $f102

org $a4d3b7
    dw $0009 : dw $0000 : db $f0 : dw $f0ff : dw $0008 : db $00 : dw $f0ef : dw $8008 : db $f0 : dw $f0ed : dw $81f8 : db $f8 : dw $f10d : dw $803d : db $db : dw $70e4 : dw $804d : db $db : dw $7100 : dw $8010 : db $ec : dw $f102 : dw $8020 : db $e2 : dw $f104 : dw $802e : db $e2 : dw $f102

org $a4d3e6
    dw $0004 : dw $01f8 : db $f8 : dw $30d0 : dw $01f8 : db $00 : dw $b0d0 : dw $0000 : db $00 : dw $f0d0 : dw $0000 : db $f8 : dw $70d0

org $a4d3fc
    dw $0004 : dw $01f8 : db $f8 : dw $30d1 : dw $01f8 : db $00 : dw $b0d1 : dw $0000 : db $00 : dw $f0d1 : dw $0000 : db $f8 : dw $70d1

org $a4d412
    dw $0004 : dw $01f8 : db $00 : dw $b0d2 : dw $01f8 : db $f8 : dw $30d2 : dw $0000 : db $00 : dw $f0d2 : dw $0000 : db $f8 : dw $70d2

org $a4d428
    dw $0004 : dw $01f8 : db $00 : dw $b0d3 : dw $01f8 : db $f8 : dw $30d3 : dw $0000 : db $00 : dw $f0d3 : dw $0000 : db $f8 : dw $70d3

org $a4d43e
    dw $0004 : dw $01f0 : db $00 : dw $60d7 : dw $01f8 : db $00 : dw $60d6 : dw $0000 : db $00 : dw $60d5 : dw $0000 : db $f8 : dw $60d4

org $a4d454
    dw $0003 : dw $01f0 : db $00 : dw $60da : dw $01f8 : db $00 : dw $60d9 : dw $0000 : db $00 : dw $60d8

org $a4d465
    dw $0004 : dw $01f0 : db $f8 : dw $e0d7 : dw $01f8 : db $f8 : dw $e0d6 : dw $0000 : db $f8 : dw $e0d5 : dw $0000 : db $00 : dw $e0d4

org $a4d47b
    dw $0003 : dw $01f0 : db $f8 : dw $e0da : dw $01f8 : db $f8 : dw $e0d9 : dw $0000 : db $f8 : dw $e0d8

org $a4d48c
    dw $0001 : dw $81f8 : db $f8 : dw $71cc

org $a4d493
    dw $0006 : dw $0018 : db $00 : dw $71de : dw $0018 : db $f8 : dw $71ce : dw $0010 : db $00 : dw $715d : dw $0010 : db $f8 : dw $714d : dw $8000 : db $f0 : dw $71e6 : dw $81f0 : db $f0 : dw $71e0

org $a4d4b3
    dw $0006 : dw $0018 : db $00 : dw $71df : dw $0018 : db $f8 : dw $71cf : dw $0010 : db $00 : dw $715d : dw $0010 : db $f8 : dw $714d : dw $8000 : db $f0 : dw $71e6 : dw $81f0 : db $f0 : dw $71e0

org $a4d4d3
    dw $0006 : dw $0010 : db $00 : dw $715e : dw $0010 : db $f8 : dw $714e : dw $0018 : db $00 : dw $713f : dw $0018 : db $f8 : dw $712f : dw $8000 : db $f0 : dw $71e6 : dw $81f0 : db $f0 : dw $71e0

org $a4d4f3
    dw $0004 : dw $81f0 : db $f0 : dw $71e0 : dw $8000 : db $f0 : dw $71e8 : dw $0010 : db $00 : dw $715f : dw $0010 : db $f8 : dw $714f

org $a4d509
    dw $0002 : dw $81f0 : db $f0 : dw $71e2 : dw $8000 : db $f0 : dw $71ea

org $a4d515
    dw $0001 : dw $81f0 : db $f0 : dw $71e4

;;; tilemaps
org $a4d51c
    dw $FFFE
    dw $2008,$000c, $4338,$4338,$4338,$4338,$4338,$4338,$4338,$4338,$4338,$4338,$4338,$4338
    dw $2048,$000c, $4338,$7caa,$7ca9,$7ca8,$7ca7,$7ca6,$7ca5,$7ca4,$7ca3,$7ca2,$4338,$4338
    dw $2088,$000c, $7cbb,$7cba,$7cb9,$7cb8,$7cb7,$7cb6,$7cb5,$7cb4,$7cb3,$7cb2,$7cb1,$7cb0
    dw $20c8,$000c, $7cc7,$7cc6,$7cc5,$7cc4,$7cc3,$7cc2,$7cc1,$7cc0,$7caf,$7cae,$7cad,$7cac
    dw $2108,$000c, $7cd7,$7cd6,$7cd5,$7cd4,$7cd3,$7cd2,$7cd1,$7cd0,$7cbf,$7cbe,$7cbd,$7cbc
    dw $2148,$000c, $7c8c,$7c8b,$7ccf,$7cce,$7ccd,$7ccc,$7ccb,$7cca,$4338,$4338,$4338,$4338
    dw $2188,$000c, $7c9c,$7c9b,$7cdf,$7cde,$7cdd,$7cdc,$7cdb,$7cda,$7cd9,$7cd8,$4338,$4338
    dw $21c8,$000c, $7c9f,$7c9e,$7c9d,$7c8f,$7c8e,$7c8d,$7c46,$7c45,$7c44,$7c43,$4338,$4338
    dw $FFFF

org $a4d600
    dw $FFFE
    dw $2010,$0008, $7ce6,$7ce5,$7ce4,$7ce3,$7ce2,$7ce1,$7ce0,$4338
    dw $204a,$000b, $4338,$7cf8,$7cf7,$7cf6,$7cf5,$7cf4,$7cf3,$7cf2,$7cf1,$7cf0,$4338
    dw $2088,$000c, $4338,$7d01,$7d00,$7cef,$7cee,$7ced,$7cec,$7ceb,$7cea,$7ce9,$4338,$4338
    dw $20c8,$000c, $7d12,$7d11,$7d10,$7cff,$7cfe,$7cfd,$7cfc,$7cfb,$7cfa,$4338,$4338,$4338
    dw $2108,$000c, $7d0a,$7d09,$7d08,$7d07,$7d06,$7d05,$7d04,$7d03,$4338,$4338,$4338,$4338
    dw $2148,$000c, $7d1a,$7d19,$7d18,$7d17,$7d16,$7d15,$7d14,$4338,$4338,$4338,$4338,$4338
    dw $2188,$000c, $7d25,$7d24,$7d23,$7d22,$7d21,$7d20,$7d0f,$7d0e,$7d0d,$7d0c,$4338,$4338
    dw $21c8,$000c, $7d35,$7d34,$7d33,$7d32,$7d31,$7d30,$7d1f,$7d1e,$7d1d,$7d1c,$4338,$4338
    dw $FFFF

org $a4d6da
    dw $FFFE
    dw $2010,$0008, $4338,$4338,$4338,$4338,$4338,$4338,$4338,$4338
    dw $204a,$000b, $7c07,$7c06,$7c05,$7c04,$7c03,$7c02,$4338,$4338,$4338,$4338,$4338
    dw $2088,$000c, $7c18,$7c17,$7c16,$7c15,$7c14,$7c13,$7c12,$7c11,$7c10,$4338,$4338,$4338
    dw $20c8,$000c, $7c24,$7c23,$7c22,$7c21,$7c20,$7c0f,$7c0e,$7c0d,$7c0c,$7c0b,$7c0a,$4338
    dw $2108,$000c, $7c34,$7c33,$7c32,$7c31,$7c30,$7c1f,$7c1e,$7c1d,$7c1c,$7c1b,$7c1a,$7c19
    dw $2148,$000c, $7c40,$7c2f,$7c2e,$7c2d,$7c2c,$7c2b,$7c2a,$7c29,$7c28,$7c27,$7c26,$7c25
    dw $2188,$000c, $7c50,$7c3f,$7c3e,$7c3d,$7c3c,$7c3b,$7c3a,$7c39,$7c38,$7c37,$7c36,$7c35
    dw $21de,$0001, $7c00
    dw $21c8,$000a, $7c4c,$7c4b,$7c4a,$7c49,$7c48,$7c47,$7c46,$7c45,$7c44,$7c43
    dw $FFFF

org $a4d7b6
    dw $FFFE
    dw $2252,$0004, $7c62,$7c61,$7c60,$7c4f
    dw $2292,$0004, $7c72,$7c71,$7c70,$7c5f
    dw $22d2,$0004, $7c6d,$7c6c,$7c6b,$7c6a
    dw $2312,$0004, $7c7d,$7c7c,$7c7b,$7c7a
    dw $FFFF

org $a4d7ea
    dw $FFFE
    dw $2252,$0004, $7d49,$7d48,$7d47,$7d46
    dw $2292,$0004, $7d59,$7d58,$7d57,$7d56
    dw $22d2,$0004, $7d4d,$7d4c,$7d4b,$7d4a
    dw $2312,$0004, $7d5d,$7d5c,$7d5b,$7d5a
    dw $FFFF

org $a4d81e
    dw $FFFE
    dw $2252,$0004, $7d0b,$7d02,$7d4f,$7d4e
    dw $2292,$0004, $7c51,$7c42,$7d1b,$7d13
    dw $22d2,$0004, $7cf9,$7cab,$7ca1,$7ca0
    dw $2312,$0004, $7c41,$7c09,$7c08,$7c01
    dw $FFFF

org $a4d852
    dw $FFFE
    dw $2340,$0006, $7d45,$7d44,$7d43,$7d42,$7d41,$7d40
    dw $2380,$0006, $7d55,$7d54,$7d53,$7d52,$7d51,$7d50
    dw $FFFF

org $a4d876
    dw $FFFE
    dw $2340,$0006, $7d2b,$7d2a,$7d29,$7d28,$7d27,$7d26
    dw $2380,$0006, $7d3b,$7d3a,$7d39,$7d38,$7d37,$7d36
    dw $FFFF

org $a4d89a
    dw $FFFE
    dw $2340,$0006, $7cc9,$7cc8,$7d2f,$7d2e,$7d2d,$7d2c
    dw $2380,$0006, $7ce8,$7ce7,$7d3f,$7d3e,$7d3d,$7d3c
    dw $FFFF

org $a4d8be
    dw $FFFE
    dw $2048,$000c, $4338,$7c07,$7c06,$7c05,$7c04,$7c03,$7c02,$4338,$4338,$4338,$4338,$4338
    dw $2088,$000c, $7c18,$7c17,$7c16,$7c15,$7c14,$7c13,$7c12,$7c11,$7c10,$4338,$4338,$4338
    dw $20c8,$000c, $7c24,$7c23,$7c22,$7c21,$7c20,$7c0f,$7c0e,$7c0d,$7c0c,$7c0b,$7c0a,$4338
    dw $2108,$000c, $7c34,$7c33,$7c32,$7c31,$7c30,$7c1f,$7c1e,$7c1d,$7c1c,$7c1b,$7c1a,$7c19
    dw $2148,$000c, $7c40,$7c2f,$7c2e,$7c2d,$7c2c,$7c2b,$7c2a,$7c29,$7c28,$7c27,$7c26,$7c25
    dw $2188,$000c, $7c50,$7c3f,$7c3e,$7c3d,$7c3c,$7c3b,$7c3a,$7c39,$7c38,$7c37,$7c36,$7c35
    dw $21c8,$000c, $7c4c,$7c4b,$7c4a,$7c49,$7c48,$7c47,$7c46,$7c45,$7c44,$7c43,$4338,$7c00
    dw $2208,$000c, $7c5c,$7c5b,$7c5a,$7c59,$7c58,$7c57,$7c56,$7c55,$7c54,$7c53,$4338,$4338
    dw $2248,$000c, $7c67,$7c66,$7c65,$7c64,$7c63,$7c62,$7c61,$7c60,$7c4f,$7c4e,$7c4d,$4338
    dw $2288,$000c, $7c77,$7c76,$7c75,$7c74,$7c73,$7c72,$7c71,$7c70,$7c5f,$7c5e,$7c5d,$4338
    dw $22c8,$000c, $4338,$7c81,$7c80,$7c6f,$7c6e,$7c6d,$7c6c,$7c6b,$7c6a,$7c69,$7c68,$4338
    dw $2308,$000c, $4338,$7c91,$7c90,$7c7f,$7c7e,$7c7d,$7c7c,$7c7b,$7c7a,$7c79,$7c78,$4338
    dw $2348,$000c, $7d41,$7d40,$7c8a,$7c89,$7c88,$7c87,$7c86,$7c85,$7c84,$7c83,$7c82,$4338
    dw $2388,$000c, $7d51,$7d50,$7c9a,$7c99,$7c98,$7c97,$7c96,$7c95,$7c94,$7c93,$4338,$4338
    dw $FFFF

org $a4da4a
    dw $FFFE
    dw $2208,$000b, $7c5c,$7c5b,$7c5a,$7c59,$7c58,$7c57,$7c56,$7c55,$7c54,$7c53,$4338
    dw $2248,$000b, $7c67,$7c66,$7c65,$7c64,$7c63,$7c62,$7c61,$7c60,$7c4f,$7c4e,$7c4d
    dw $2288,$000b, $7c77,$7c76,$7c75,$7c74,$7c73,$7c72,$7c71,$7c70,$7c5f,$7c5e,$7c5d
    dw $22c8,$000b, $4338,$7c81,$7c80,$7c6f,$7c6e,$7c6d,$7c6c,$7c6b,$7c6a,$7c69,$7c68
    dw $2308,$000b, $4338,$7c91,$7c90,$7c7f,$7c7e,$7c7d,$7c7c,$7c7b,$7c7a,$7c79,$7c78
    dw $2348,$000b, $7d41,$7d40,$7c8a,$7c89,$7c88,$7c87,$7c86,$7c85,$7c84,$7c83,$7c82
    dw $2388,$000b, $7d51,$7d50,$7c9a,$7c99,$7c98,$7c97,$7c96,$7c95,$7c94,$7c93,$4338
    dw $FFFF

;;; croc in acid spritemaps
org $a4db04
    dw $0017 : dw $0020 : db $d8 : dw $6f77 : dw $0010 : db $e8 : dw $6f66 : dw $0008 : db $e8 : dw $6f65 : dw $01f8 : db $d0 : dw $6f76 : dw $0000 : db $d0 : dw $6f75 : dw $0008 : db $d0 : dw $6f74 : dw $0008 : db $c8 : dw $6f64 : dw $c210 : db $c8 : dw $6f62 : dw $c220 : db $c8 : dw $6f60 : dw $c208 : db $d8 : dw $6f68 : dw $0018 : db $e0 : dw $6f77 : dw $0018 : db $d8 : dw $6f67 : dw $c3d8 : db $d8 : dw $6f6e : dw $c3e8 : db $d8 : dw $6f6c : dw $c3f8 : db $d8 : dw $6f6a : dw $c3d8 : db $e8 : dw $6f84 : dw $c3e8 : db $e8 : dw $6f82 : dw $c3f8 : db $e8 : dw $6f80 : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $c208 : db $f8 : dw $6f88 : dw $c218 : db $f8 : dw $6f86

org $a4db79
    dw $0022 : dw $0020 : db $d8 : dw $6f77 : dw $0010 : db $e8 : dw $6f66 : dw $0008 : db $e8 : dw $6f65 : dw $01f8 : db $d0 : dw $6f76 : dw $0000 : db $d0 : dw $6f75 : dw $0008 : db $d0 : dw $6f74 : dw $0008 : db $c8 : dw $6f64 : dw $c210 : db $c8 : dw $6f62 : dw $c220 : db $c8 : dw $6f60 : dw $c208 : db $d8 : dw $6f68 : dw $0018 : db $e0 : dw $6f77 : dw $0018 : db $d8 : dw $6f67 : dw $c3d8 : db $d8 : dw $6f6e : dw $c3e8 : db $d8 : dw $6f6c : dw $c3f8 : db $d8 : dw $6f6a : dw $c3d8 : db $e8 : dw $6f84 : dw $c3e8 : db $e8 : dw $6f82 : dw $c3f8 : db $e8 : dw $6f80 : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $c208 : db $f8 : dw $6f88 : dw $c218 : db $f8 : dw $6f86 : dw $01d8 : db $08 : dw $6f3a : dw $01e0 : db $08 : dw $6f39 : dw $01e8 : db $08 : dw $6f38 : dw $01f0 : db $08 : dw $6f37 : dw $01f8 : db $08 : dw $6f36 : dw $0000 : db $08 : dw $6f35 : dw $0008 : db $08 : dw $6f34 : dw $0010 : db $08 : dw $6f33 : dw $0018 : db $08 : dw $6f32 : dw $0020 : db $08 : dw $6f31 : dw $0028 : db $08 : dw $6f30

org $a4dc25
    dw $002d : dw $0020 : db $d8 : dw $6f77 : dw $0010 : db $e8 : dw $6f66 : dw $0008 : db $e8 : dw $6f65 : dw $01f8 : db $d0 : dw $6f76 : dw $0000 : db $d0 : dw $6f75 : dw $0008 : db $d0 : dw $6f74 : dw $0008 : db $c8 : dw $6f64 : dw $c210 : db $c8 : dw $6f62 : dw $c220 : db $c8 : dw $6f60 : dw $c208 : db $d8 : dw $6f68 : dw $0018 : db $e0 : dw $6f77 : dw $0018 : db $d8 : dw $6f67 : dw $c3d8 : db $d8 : dw $6f6e : dw $c3e8 : db $d8 : dw $6f6c : dw $c3f8 : db $d8 : dw $6f6a : dw $c3d8 : db $e8 : dw $6f84 : dw $c3e8 : db $e8 : dw $6f82 : dw $c3f8 : db $e8 : dw $6f80 : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $c208 : db $f8 : dw $6f88 : dw $c218 : db $f8 : dw $6f86 : dw $01d8 : db $10 : dw $6f4a : dw $01e0 : db $10 : dw $6f49 : dw $01e8 : db $10 : dw $6f48 : dw $01f0 : db $10 : dw $6f47 : dw $01f8 : db $10 : dw $6f46 : dw $0000 : db $10 : dw $6f45 : dw $0008 : db $10 : dw $6f44 : dw $0010 : db $10 : dw $6f43 : dw $0018 : db $10 : dw $6f42 : dw $0020 : db $10 : dw $6f41 : dw $0028 : db $10 : dw $6f40 : dw $01d8 : db $08 : dw $6f3a : dw $01e0 : db $08 : dw $6f39 : dw $01e8 : db $08 : dw $6f38 : dw $01f0 : db $08 : dw $6f37 : dw $01f8 : db $08 : dw $6f36 : dw $0000 : db $08 : dw $6f35 : dw $0008 : db $08 : dw $6f34 : dw $0010 : db $08 : dw $6f33 : dw $0018 : db $08 : dw $6f32 : dw $0020 : db $08 : dw $6f31 : dw $0028 : db $08 : dw $6f30

org $a4dd08
    dw $0037 : dw $0020 : db $d8 : dw $6f77 : dw $0010 : db $e8 : dw $6f66 : dw $0008 : db $e8 : dw $6f65 : dw $01f8 : db $d0 : dw $6f76 : dw $0000 : db $d0 : dw $6f75 : dw $0008 : db $d0 : dw $6f74 : dw $0008 : db $c8 : dw $6f64 : dw $c210 : db $c8 : dw $6f62 : dw $c220 : db $c8 : dw $6f60 : dw $c208 : db $d8 : dw $6f68 : dw $0018 : db $e0 : dw $6f77 : dw $0018 : db $d8 : dw $6f67 : dw $c3d8 : db $d8 : dw $6f6e : dw $c3e8 : db $d8 : dw $6f6c : dw $c3f8 : db $d8 : dw $6f6a : dw $c3d8 : db $e8 : dw $6f84 : dw $c3e8 : db $e8 : dw $6f82 : dw $c3f8 : db $e8 : dw $6f80 : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $c208 : db $f8 : dw $6f88 : dw $c218 : db $f8 : dw $6f86 : dw $01e0 : db $18 : dw $6f59 : dw $01e8 : db $18 : dw $6f58 : dw $01f0 : db $18 : dw $6f57 : dw $01f8 : db $18 : dw $6f56 : dw $0000 : db $18 : dw $6f55 : dw $0008 : db $18 : dw $6f54 : dw $0010 : db $18 : dw $6f53 : dw $0018 : db $18 : dw $6f52 : dw $0020 : db $18 : dw $6f51 : dw $0028 : db $18 : dw $6f50 : dw $01d8 : db $10 : dw $6f4a : dw $01e0 : db $10 : dw $6f49 : dw $01e8 : db $10 : dw $6f48 : dw $01f0 : db $10 : dw $6f47 : dw $01f8 : db $10 : dw $6f46 : dw $0000 : db $10 : dw $6f45 : dw $0008 : db $10 : dw $6f44 : dw $0010 : db $10 : dw $6f43 : dw $0018 : db $10 : dw $6f42 : dw $0020 : db $10 : dw $6f41 : dw $0028 : db $10 : dw $6f40 : dw $01d8 : db $08 : dw $6f3a : dw $01e0 : db $08 : dw $6f39 : dw $01e8 : db $08 : dw $6f38 : dw $01f0 : db $08 : dw $6f37 : dw $01f8 : db $08 : dw $6f36 : dw $0000 : db $08 : dw $6f35 : dw $0008 : db $08 : dw $6f34 : dw $0010 : db $08 : dw $6f33 : dw $0018 : db $08 : dw $6f32 : dw $0020 : db $08 : dw $6f31 : dw $0028 : db $08 : dw $6f30

org $a4de1d
    dw $0018 : dw $01e8 : db $f0 : dw $6fed : dw $01f0 : db $f0 : dw $6fec : dw $01d8 : db $f0 : dw $6ffd : dw $01e0 : db $f0 : dw $6ffc : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $01f7 : db $d0 : dw $6fb6 : dw $001f : db $00 : dw $6fa6 : dw $0017 : db $00 : dw $6faf : dw $000f : db $00 : dw $6fbf : dw $c3df : db $f8 : dw $6fca : dw $c3ef : db $f8 : dw $6fc8 : dw $c3ff : db $f8 : dw $6fc6 : dw $c3df : db $e8 : dw $6fc4 : dw $c3ef : db $e8 : dw $6fc2 : dw $c3ff : db $e8 : dw $6fc0 : dw $c3df : db $d8 : dw $6fad : dw $c3ef : db $d8 : dw $6fab : dw $c3ff : db $d8 : dw $6fa9 : dw $c20f : db $d8 : dw $6fa7 : dw $c3ff : db $c8 : dw $6fa4 : dw $c20f : db $c8 : dw $6fa2 : dw $c21f : db $c8 : dw $6fa0

org $a4de97
    dw $0023 : dw $01e8 : db $f0 : dw $6fed : dw $01f0 : db $f0 : dw $6fec : dw $01d8 : db $f0 : dw $6ffd : dw $01e0 : db $f0 : dw $6ffc : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $01f7 : db $d0 : dw $6fb6 : dw $001f : db $00 : dw $6fa6 : dw $0017 : db $00 : dw $6faf : dw $000f : db $00 : dw $6fbf : dw $c3df : db $f8 : dw $6fca : dw $c3ef : db $f8 : dw $6fc8 : dw $c3ff : db $f8 : dw $6fc6 : dw $c3df : db $e8 : dw $6fc4 : dw $c3ef : db $e8 : dw $6fc2 : dw $c3ff : db $e8 : dw $6fc0 : dw $c3df : db $d8 : dw $6fad : dw $c3ef : db $d8 : dw $6fab : dw $c3ff : db $d8 : dw $6fa9 : dw $c20f : db $d8 : dw $6fa7 : dw $c3ff : db $c8 : dw $6fa4 : dw $c20f : db $c8 : dw $6fa2 : dw $c21f : db $c8 : dw $6fa0 : dw $01d8 : db $08 : dw $6f3a : dw $01e0 : db $08 : dw $6f39 : dw $01e8 : db $08 : dw $6f38 : dw $01f0 : db $08 : dw $6f37 : dw $01f8 : db $08 : dw $6f36 : dw $0000 : db $08 : dw $6f35 : dw $0008 : db $08 : dw $6f34 : dw $0010 : db $08 : dw $6f33 : dw $0018 : db $08 : dw $6f32 : dw $0020 : db $08 : dw $6f31 : dw $0028 : db $08 : dw $6f30

org $a4df48
    dw $002e : dw $01e8 : db $f0 : dw $6fed : dw $01f0 : db $f0 : dw $6fec : dw $01d8 : db $f0 : dw $6ffd : dw $01e0 : db $f0 : dw $6ffc : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $01f7 : db $d0 : dw $6fb6 : dw $001f : db $00 : dw $6fa6 : dw $0017 : db $00 : dw $6faf : dw $000f : db $00 : dw $6fbf : dw $c3df : db $f8 : dw $6fca : dw $c3ef : db $f8 : dw $6fc8 : dw $c3ff : db $f8 : dw $6fc6 : dw $c3df : db $e8 : dw $6fc4 : dw $c3ef : db $e8 : dw $6fc2 : dw $c3ff : db $e8 : dw $6fc0 : dw $c3df : db $d8 : dw $6fad : dw $c3ef : db $d8 : dw $6fab : dw $c3ff : db $d8 : dw $6fa9 : dw $c20f : db $d8 : dw $6fa7 : dw $c3ff : db $c8 : dw $6fa4 : dw $c20f : db $c8 : dw $6fa2 : dw $c21f : db $c8 : dw $6fa0 : dw $01d8 : db $10 : dw $6f4a : dw $01e0 : db $10 : dw $6f49 : dw $01e8 : db $10 : dw $6f48 : dw $01f0 : db $10 : dw $6f47 : dw $01f8 : db $10 : dw $6f46 : dw $0000 : db $10 : dw $6f45 : dw $0008 : db $10 : dw $6f44 : dw $0010 : db $10 : dw $6f43 : dw $0018 : db $10 : dw $6f42 : dw $0020 : db $10 : dw $6f41 : dw $0028 : db $10 : dw $6f40 : dw $01d8 : db $08 : dw $6f3a : dw $01e0 : db $08 : dw $6f39 : dw $01e8 : db $08 : dw $6f38 : dw $01f0 : db $08 : dw $6f37 : dw $01f8 : db $08 : dw $6f36 : dw $0000 : db $08 : dw $6f35 : dw $0008 : db $08 : dw $6f34 : dw $0010 : db $08 : dw $6f33 : dw $0018 : db $08 : dw $6f32 : dw $0020 : db $08 : dw $6f31 : dw $0028 : db $08 : dw $6f30

org $a4e030
    dw $0038 : dw $01e8 : db $f0 : dw $6fed : dw $01f0 : db $f0 : dw $6fec : dw $01d8 : db $f0 : dw $6ffd : dw $01e0 : db $f0 : dw $6ffc : dw $c3d8 : db $f8 : dw $6f8e : dw $c3e8 : db $f8 : dw $6f8c : dw $c3f8 : db $f8 : dw $6f8a : dw $01f7 : db $d0 : dw $6fb6 : dw $001f : db $00 : dw $6fa6 : dw $0017 : db $00 : dw $6faf : dw $000f : db $00 : dw $6fbf : dw $c3df : db $f8 : dw $6fca : dw $c3ef : db $f8 : dw $6fc8 : dw $c3ff : db $f8 : dw $6fc6 : dw $c3df : db $e8 : dw $6fc4 : dw $c3ef : db $e8 : dw $6fc2 : dw $c3ff : db $e8 : dw $6fc0 : dw $c3df : db $d8 : dw $6fad : dw $c3ef : db $d8 : dw $6fab : dw $c3ff : db $d8 : dw $6fa9 : dw $c20f : db $d8 : dw $6fa7 : dw $c3ff : db $c8 : dw $6fa4 : dw $c20f : db $c8 : dw $6fa2 : dw $c21f : db $c8 : dw $6fa0 : dw $01e0 : db $18 : dw $6f59 : dw $01e8 : db $18 : dw $6f58 : dw $01f0 : db $18 : dw $6f57 : dw $01f8 : db $18 : dw $6f56 : dw $0000 : db $18 : dw $6f55 : dw $0008 : db $18 : dw $6f54 : dw $0010 : db $18 : dw $6f53 : dw $0018 : db $18 : dw $6f52 : dw $0020 : db $18 : dw $6f51 : dw $0028 : db $18 : dw $6f50 : dw $01d8 : db $10 : dw $6f4a : dw $01e0 : db $10 : dw $6f49 : dw $01e8 : db $10 : dw $6f48 : dw $01f0 : db $10 : dw $6f47 : dw $01f8 : db $10 : dw $6f46 : dw $0000 : db $10 : dw $6f45 : dw $0008 : db $10 : dw $6f44 : dw $0010 : db $10 : dw $6f43 : dw $0018 : db $10 : dw $6f42 : dw $0020 : db $10 : dw $6f41 : dw $0028 : db $10 : dw $6f40 : dw $01d8 : db $08 : dw $6f3a : dw $01e0 : db $08 : dw $6f39 : dw $01e8 : db $08 : dw $6f38 : dw $01f0 : db $08 : dw $6f37 : dw $01f8 : db $08 : dw $6f36 : dw $0000 : db $08 : dw $6f35 : dw $0008 : db $08 : dw $6f34 : dw $0010 : db $08 : dw $6f33 : dw $0018 : db $08 : dw $6f32 : dw $0020 : db $08 : dw $6f31 : dw $0028 : db $08 : dw $6f30

;;; croc dying extended spritemaps, spritemaps, tilemaps, hitboxes

;;; extended spritemaps
org $a4e200
        dw $0010
org $a4e208
        dw $0004
org $a4e210
        dw $0019
org $a4e218
        dw $0001
org $a4e220
        dw $001c
org $a4e22a
        dw $0010
org $a4e232
        dw $0003
org $a4e23a
        dw $0019
org $a4e242
        dw $0001
org $a4e24a
        dw $001e
org $a4e254
        dw $000b
org $a4e25c
        dw $0001
org $a4e264
        dw $0019
org $a4e26c
        dw $0001
org $a4e274
        dw $001f
org $a4e27e
        dw $0010
org $a4e28e
        dw $0019
org $a4e296
        dw $0001
org $a4e29e
        dw $0020
org $a4e2a8
        dw $000c
org $a4e2b0
        dw $fffe
org $a4e2b8
        dw $0019
org $a4e2c0
        dw $0001
org $a4e2c8
        dw $0021
org $a4e2d2
        dw $000c
org $a4e2da
        dw $fffe
org $a4e2e2
        dw $0019
org $a4e2ea
        dw $0001
org $a4e2f2
        dw $0022
org $a4e2fc
        dw $000b
org $a4e304
        dw $fffd
org $a4e30c
        dw $0019
org $a4e314
        dw $0001
org $a4e31c
        dw $0022
org $a4e326
        dw $000c
org $a4e32e
        dw $fffe
org $a4e336
        dw $0019
org $a4e33e
        dw $0001
org $a4e346
        dw $0023
org $a4e350
        dw $0010
org $a4e358
        dw $fff7
org $a4e360
        dw $0019
org $a4e368
        dw $ffff
org $a4e370
        dw $0026
org $a4e37a
        dw $0015
org $a4e382
        dw $fff0
org $a4e38a
        dw $0019
org $a4e392
        dw $fffb
org $a4e39a
        dw $0026
org $a4e3a4
        dw $0016
org $a4e3ac
        dw $ffeb
org $a4e3b4
        dw $001a
org $a4e3bc
        dw $fff9
org $a4e3c4
        dw $0026
org $a4e3ce
        dw $0016
org $a4e3d6
        dw $ffe1
org $a4e3de
        dw $0019
org $a4e3e6
        dw $fff6
org $a4e3ee
        dw $0026
org $a4e3f8
        dw $0016
org $a4e400
        dw $ffdc
org $a4e408
        dw $0019
org $a4e410
        dw $fff6
org $a4e418
        dw $0026
org $a4e422
        dw $ffd2
org $a4e42a
        dw $0019
org $a4e432
        dw $fff4
org $a4e43a
        dw $ffff
org $a4e442
        dw $0015
org $a4e44a
        dw $0028
org $a4e452
        dw $003a
org $a4e45a
        dw $004a
org $a4e462
        dw $005d
org $a4e46c
        dw $ffc9
org $a4e474
        dw $ffd7
org $a4e47c
        dw $0007
org $a4e484
        dw $ffe7
org $a4e48c
        dw $ffe7
org $a4e494
        dw $0008
org $a4e49c
        dw $fff8
org $a4e4a4
        dw $fff7
org $a4e4ac
        dw $0009
org $a4e4b4
        dw $0018
org $a4e4bc
        dw $002d
org $a4e4c4
        dw $003d
org $a4e4cc
        dw $004c
org $a4e4d6
        dw $ffc4
org $a4e4de
        dw $ffd7
org $a4e4e6
        dw $0007
org $a4e4ee
        dw $ffe4
org $a4e4f6
        dw $ffe6
org $a4e4fe
        dw $0003
org $a4e506
        dw $fff7
org $a4e50e
        dw $fff3
org $a4e516
        dw $0008
org $a4e51e
        dw $0017
org $a4e526
        dw $0030
org $a4e52e
        dw $003e
org $a4e536
        dw $0052
org $a4e540
        dw $ffc2
org $a4e548
        dw $ffd7
org $a4e550
        dw $0008
org $a4e558
        dw $ffe4
org $a4e560
        dw $ffe8
org $a4e568
        dw $0002
org $a4e570
        dw $fff7
org $a4e578
        dw $fff1
org $a4e580
        dw $000a
org $a4e588
        dw $0018
org $a4e590
        dw $0032
org $a4e598
        dw $0040
org $a4e5a0
        dw $0054
org $a4e5aa
        dw $ffc0
org $a4e5b2
        dw $ffd7
org $a4e5ba
        dw $0009
org $a4e5c2
        dw $ffe4
org $a4e5ca
        dw $ffea
org $a4e5d2
        dw $fffe
org $a4e5da
        dw $fff4
org $a4e5e2
        dw $fff1
org $a4e5ea
        dw $000a
org $a4e5f2
        dw $0017
org $a4e5fa
        dw $002e
org $a4e602
        dw $0042
org $a4e60c
        dw $ffc0
org $a4e614
        dw $ffd7
org $a4e61c
        dw $000a
org $a4e624
        dw $ffe4
org $a4e62c
        dw $ffea
org $a4e634
        dw $fffe
org $a4e63c
        dw $fff4
org $a4e644
        dw $fff1
org $a4e64c
        dw $0016
org $a4e654
        dw $002e
org $a4e65e
        dw $ffc0
org $a4e666
        dw $000d
org $a4e66e
        dw $ffe3
org $a4e676
        dw $ffec
org $a4e67e
        dw $fffe
org $a4e686
        dw $fff4
org $a4e690
        dw $ffc0
org $a4e698
        dw $000d
org $a4e6a0
        dw $fff2
org $a4e6aa
        dw $ffc0
org $a4e718
        dw $ffe0

;;; hitboxes
org $a4e722
        dw $ffda,$ffe2,$001a,$001d
org $a4e730
        dw $0000,$fff0,$0026,$001f
org $a4e73c
        dw $ffe6,$ffe3,$0000,$001c

;;; spritemaps
org $a4e74a
    dw $0011 : dw $0014 : db $18 : dw $6fa6 : dw $0004 : db $18 : dw $6fbf : dw $000c : db $18 : dw $6faf : dw $81d4 : db $10 : dw $6fca : dw $81e4 : db $10 : dw $6fc8 : dw $81f4 : db $10 : dw $6fc6 : dw $81d4 : db $00 : dw $6fc4 : dw $81e4 : db $00 : dw $6fc2 : dw $81f4 : db $00 : dw $6fc0 : dw $01ec : db $e8 : dw $6fb6 : dw $81d4 : db $f0 : dw $6fad : dw $81e4 : db $f0 : dw $6fab : dw $81f4 : db $f0 : dw $6fa9 : dw $8004 : db $f0 : dw $6fa7 : dw $81f4 : db $e0 : dw $6fa4 : dw $8004 : db $e0 : dw $6fa2 : dw $8014 : db $e0 : dw $6fa0

org $a4e7a1
    dw $0011 : dw $01e4 : db $18 : dw $2fa6 : dw $01f4 : db $18 : dw $2fbf : dw $01ec : db $18 : dw $2faf : dw $801c : db $10 : dw $2fca : dw $800c : db $10 : dw $2fc8 : dw $81fc : db $10 : dw $2fc6 : dw $801c : db $00 : dw $2fc4 : dw $800c : db $00 : dw $2fc2 : dw $81fc : db $00 : dw $2fc0 : dw $000c : db $e8 : dw $2fb6 : dw $801c : db $f0 : dw $2fad : dw $800c : db $f0 : dw $2fab : dw $81fc : db $f0 : dw $2fa9 : dw $81ec : db $f0 : dw $2fa7 : dw $81fc : db $e0 : dw $2fa4 : dw $81ec : db $e0 : dw $2fa2 : dw $81dc : db $e0 : dw $2fa0

org $a4e7f8
    dw $000a : dw $01e0 : db $0c : dw $6f6b : dw $01e8 : db $0c : dw $6f6a : dw $81e0 : db $fc : dw $6f68 : dw $81e0 : db $ec : dw $6f66 : dw $81f0 : db $00 : dw $6f64 : dw $8000 : db $00 : dw $6f62 : dw $81f0 : db $f0 : dw $6f64 : dw $8000 : db $f0 : dw $6f62 : dw $8010 : db $fc : dw $6f80 : dw $8010 : db $ec : dw $6f60

org $a4e82c
    dw $000a : dw $0018 : db $0c : dw $2f6b : dw $0010 : db $0c : dw $2f6a : dw $8010 : db $fc : dw $2f68 : dw $8010 : db $ec : dw $2f66 : dw $8000 : db $00 : dw $2f64 : dw $81f0 : db $00 : dw $2f62 : dw $8000 : db $f0 : dw $2f64 : dw $81f0 : db $f0 : dw $2f62 : dw $81e0 : db $fc : dw $2f80 : dw $81e0 : db $ec : dw $2f60

org $a4e860
    dw $000f : dw $81d0 : db $10 : dw $6f8e : dw $81f0 : db $10 : dw $6f8a : dw $81e0 : db $10 : dw $6f8c : dw $0000 : db $18 : dw $6f7b : dw $0008 : db $10 : dw $6f0f : dw $0000 : db $10 : dw $6f1f : dw $0011 : db $18 : dw $2f7a : dw $0018 : db $18 : dw $6f7a : dw $0028 : db $10 : dw $6f88 : dw $0020 : db $10 : dw $6f89 : dw $0018 : db $10 : dw $6f98 : dw $0010 : db $10 : dw $6f99 : dw $8000 : db $00 : dw $6f86 : dw $8010 : db $00 : dw $6f84 : dw $8020 : db $00 : dw $6f82

org $a4e8ad
    dw $000f : dw $8020 : db $10 : dw $2f8e : dw $8000 : db $10 : dw $2f8a : dw $8010 : db $10 : dw $2f8c : dw $01f8 : db $18 : dw $2f7b : dw $01f0 : db $10 : dw $2f0f : dw $01f8 : db $10 : dw $2f1f : dw $01e7 : db $18 : dw $6f7a : dw $01e0 : db $18 : dw $2f7a : dw $01d0 : db $10 : dw $2f88 : dw $01d8 : db $10 : dw $2f89 : dw $01e0 : db $10 : dw $2f98 : dw $01e8 : db $10 : dw $2f99 : dw $81f0 : db $00 : dw $2f86 : dw $81e0 : db $00 : dw $2f84 : dw $81d0 : db $00 : dw $2f82

org $a4e8fa
    dw $0002 : dw $81f0 : db $f8 : dw $6f6e : dw $8000 : db $f8 : dw $6f6c

org $a4e906
    dw $0002 : dw $8000 : db $f8 : dw $2f6e : dw $81f0 : db $f8 : dw $2f6c

org $a4e912
    dw $0001 : dw $81f8 : db $f8 : dw $2f60

org $a4e919
    dw $0001 : dw $81f8 : db $f8 : dw $2f80

org $a4e920
    dw $0001 : dw $81f8 : db $f8 : dw $2f62

org $a4e927
    dw $0001 : dw $81f8 : db $f8 : dw $2f64

org $a4e92e
    dw $0001 : dw $81f8 : db $f8 : dw $2f66

org $a4e935
    dw $0001 : dw $81f8 : db $f8 : dw $2f68

org $a4e93c
    dw $0002 : dw $0000 : db $fc : dw $2f6b : dw $01f8 : db $fc : dw $2f6a

org $a4e948
    dw $0003 : dw $01f8 : db $04 : dw $2f88 : dw $0000 : db $04 : dw $2f89 : dw $81f8 : db $f4 : dw $2f82

org $a4e959
    dw $0005 : dw $01ff : db $08 : dw $6f7a : dw $01f8 : db $08 : dw $2f7a : dw $01f8 : db $00 : dw $2f98 : dw $0000 : db $00 : dw $2f99 : dw $81f8 : db $f0 : dw $2f84

org $a4e974
    dw $0004 : dw $01f8 : db $05 : dw $2f0f : dw $0000 : db $0d : dw $2f7b : dw $0000 : db $05 : dw $2f1f : dw $81f8 : db $f5 : dw $2f86

org $a4e98a
    dw $0001 : dw $81f8 : db $f8 : dw $2f8a

org $a4e991
    dw $0001 : dw $81f8 : db $f8 : dw $2f8c

org $a4e998
    dw $0001 : dw $81f8 : db $f8 : dw $2f8e

org $a4e99f
    dw $0009 : dw $802d : db $1a : dw $60e4 : dw $803d : db $1e : dw $6100 : dw $01f8 : db $07 : dw $6108 : dw $0008 : db $ff : dw $60f6 : dw $8000 : db $07 : dw $6106 : dw $81f8 : db $f7 : dw $60e7 : dw $8004 : db $0b : dw $60e0 : dw $8012 : db $12 : dw $60e0 : dw $8020 : db $19 : dw $60e0

org $a4e9ce
    dw $0009 : dw $803f : db $13 : dw $60e4 : dw $804f : db $13 : dw $6100 : dw $0000 : db $09 : dw $60ff : dw $0008 : db $f9 : dw $60ef : dw $8008 : db $01 : dw $60ed : dw $81f8 : db $f9 : dw $610d : dw $8012 : db $05 : dw $6102 : dw $8022 : db $0f : dw $6104 : dw $8030 : db $0f : dw $6102

org $a4e9fd
    dw $0007 : dw $8024 : db $1c : dw $60e4 : dw $8034 : db $1e : dw $6100 : dw $81f8 : db $08 : dw $6109 : dw $81f8 : db $f8 : dw $60e9 : dw $81fa : db $0d : dw $60e0 : dw $8008 : db $14 : dw $60e0 : dw $8016 : db $1b : dw $60e0

org $a4ea22
    dw $0009 : dw $01f8 : db $08 : dw $20ff : dw $01f0 : db $f8 : dw $20ef : dw $81e8 : db $00 : dw $20ed : dw $81f8 : db $f8 : dw $210d : dw $801b : db $11 : dw $60e4 : dw $802b : db $11 : dw $6100 : dw $81ee : db $03 : dw $6102 : dw $81fe : db $0d : dw $6104 : dw $800c : db $0d : dw $6102

org $a4ea51
    dw $0007 : dw $8030 : db $0c : dw $60e4 : dw $8040 : db $0c : dw $6100 : dw $81f8 : db $08 : dw $6109 : dw $81f8 : db $f8 : dw $60e9 : dw $8000 : db $0c : dw $60e2 : dw $8010 : db $0c : dw $60e2 : dw $8020 : db $0c : dw $60e2

org $a4ea76
    dw $0008 : dw $01f6 : db $09 : dw $60df : dw $01fe : db $09 : dw $60de : dw $0006 : db $09 : dw $60dd : dw $000e : db $09 : dw $60dc : dw $0016 : db $09 : dw $60db : dw $81fe : db $f9 : dw $612d : dw $81fa : db $f9 : dw $614b : dw $81ef : db $f9 : dw $612b

org $a4eaa0
    dw $0008 : dw $01f3 : db $09 : dw $60df : dw $01fb : db $09 : dw $60de : dw $0003 : db $09 : dw $60dd : dw $000b : db $09 : dw $60dc : dw $0013 : db $09 : dw $60db : dw $81fb : db $f9 : dw $612d : dw $81f9 : db $f9 : dw $614b : dw $81ef : db $f9 : dw $612b

org $a4eaca
    dw $0008 : dw $01f0 : db $09 : dw $60df : dw $01f8 : db $09 : dw $60de : dw $0000 : db $09 : dw $60dd : dw $0008 : db $09 : dw $60dc : dw $0010 : db $09 : dw $60db : dw $81f8 : db $f9 : dw $612d : dw $81f7 : db $f9 : dw $614b : dw $81f0 : db $f9 : dw $612b

org $a4eaf4
    dw $0008 : dw $01ec : db $09 : dw $60df : dw $01f4 : db $09 : dw $60de : dw $01fc : db $09 : dw $60dd : dw $0004 : db $09 : dw $60dc : dw $000c : db $09 : dw $60db : dw $81f4 : db $f9 : dw $612d : dw $81f4 : db $f9 : dw $614b : dw $81f0 : db $f9 : dw $612b

org $a4eb1e
    dw $0008 : dw $81ed : db $f9 : dw $612d : dw $81ee : db $f9 : dw $214b : dw $01e7 : db $09 : dw $60df : dw $01ef : db $09 : dw $60de : dw $01f7 : db $09 : dw $60dd : dw $01ff : db $09 : dw $60dc : dw $0007 : db $09 : dw $60db : dw $81ef : db $f9 : dw $212b

org $a4eb48
    dw $0008 : dw $81e7 : db $f9 : dw $612d : dw $81ea : db $f9 : dw $214b : dw $01e0 : db $09 : dw $60df : dw $01e8 : db $09 : dw $60de : dw $01f0 : db $09 : dw $60dd : dw $01f8 : db $09 : dw $60dc : dw $0000 : db $09 : dw $60db : dw $81ef : db $f9 : dw $212b

org $a4eb72
    dw $0008 : dw $81e0 : db $f9 : dw $612d : dw $81e5 : db $f9 : dw $214b : dw $01d8 : db $09 : dw $60df : dw $01e0 : db $09 : dw $60de : dw $01e8 : db $09 : dw $60dd : dw $01f0 : db $09 : dw $60dc : dw $01f8 : db $09 : dw $60db : dw $81ed : db $f9 : dw $212b

org $a4eb9c
    dw $0008 : dw $81e7 : db $f8 : dw $612d : dw $81ea : db $f8 : dw $214b : dw $01e0 : db $09 : dw $60df : dw $01e8 : db $08 : dw $60de : dw $01f0 : db $08 : dw $60dd : dw $01f8 : db $09 : dw $60dc : dw $0000 : db $09 : dw $60db : dw $81ef : db $f9 : dw $212b

org $a4ebc6
    dw $0008 : dw $81ed : db $f5 : dw $612d : dw $81ee : db $f5 : dw $214b : dw $01e7 : db $06 : dw $60df : dw $01ef : db $05 : dw $60de : dw $01f7 : db $05 : dw $60dd : dw $01ff : db $07 : dw $60dc : dw $0007 : db $07 : dw $60db : dw $81ef : db $f9 : dw $212b

org $a4ebf0
    dw $0008 : dw $01ec : db $06 : dw $60df : dw $01f4 : db $05 : dw $60de : dw $01fc : db $05 : dw $60dd : dw $0004 : db $07 : dw $60dc : dw $000c : db $07 : dw $60db : dw $81f4 : db $f5 : dw $612d : dw $81f4 : db $f5 : dw $614b : dw $81f0 : db $f9 : dw $612b

org $a4ec1a
    dw $0008 : dw $01f0 : db $06 : dw $60df : dw $01f8 : db $05 : dw $60de : dw $0000 : db $05 : dw $60dd : dw $0008 : db $07 : dw $60dc : dw $0010 : db $07 : dw $60db : dw $81f8 : db $f5 : dw $612d : dw $81f7 : db $f5 : dw $614b : dw $81f0 : db $f9 : dw $612b

org $a4ec44
    dw $0008 : dw $01f3 : db $07 : dw $60df : dw $01fb : db $06 : dw $60de : dw $0003 : db $06 : dw $60dd : dw $000b : db $08 : dw $60dc : dw $0013 : db $08 : dw $60db : dw $81fb : db $f6 : dw $612d : dw $81f9 : db $f6 : dw $614b : dw $81ef : db $f9 : dw $612b

org $a4ec6e
    dw $0008 : dw $01f6 : db $08 : dw $60df : dw $01fe : db $07 : dw $60de : dw $0006 : db $07 : dw $60dd : dw $000e : db $08 : dw $60dc : dw $0016 : db $08 : dw $60db : dw $81fe : db $f7 : dw $612d : dw $81fa : db $f7 : dw $614b : dw $81ef : db $f9 : dw $612b

org $a4ec98
    dw $0008 : dw $01ec : db $04 : dw $60df : dw $01f4 : db $05 : dw $60de : dw $01fc : db $05 : dw $60dd : dw $0004 : db $05 : dw $60dc : dw $000c : db $05 : dw $60db : dw $81f4 : db $f5 : dw $612d : dw $81f4 : db $f5 : dw $614b : dw $81f0 : db $f9 : dw $612b

org $a4ecc2
    dw $0008 : dw $01ec : db $04 : dw $60df : dw $01f4 : db $05 : dw $60de : dw $01fc : db $05 : dw $60dd : dw $0004 : db $05 : dw $60dc : dw $000c : db $05 : dw $60db : dw $81f4 : db $f5 : dw $612d : dw $81f4 : db $f3 : dw $614b : dw $81f0 : db $f5 : dw $612b

org $a4ecec
    dw $0008 : dw $01ec : db $04 : dw $60df : dw $01f4 : db $05 : dw $60de : dw $01fc : db $05 : dw $60dd : dw $0004 : db $05 : dw $60dc : dw $000c : db $05 : dw $60db : dw $81f4 : db $f5 : dw $612d : dw $81f4 : db $f1 : dw $614b : dw $81f0 : db $f1 : dw $612b

org $a4ed16
    dw $0009 : dw $81c3 : db $1a : dw $22e4 : dw $81b3 : db $1e : dw $2300 : dw $0000 : db $07 : dw $2308 : dw $01f0 : db $ff : dw $22f6 : dw $81f0 : db $07 : dw $2306 : dw $81f8 : db $f7 : dw $22e7 : dw $81ec : db $0b : dw $22e0 : dw $81de : db $12 : dw $22e0 : dw $81d0 : db $19 : dw $22e0

org $a4ed45
    dw $0009 : dw $81b1 : db $13 : dw $22e4 : dw $81a1 : db $13 : dw $2300 : dw $01f8 : db $09 : dw $22ff : dw $01f0 : db $f9 : dw $22ef : dw $81e8 : db $01 : dw $22ed : dw $81f8 : db $f9 : dw $230d : dw $81de : db $05 : dw $2302 : dw $81ce : db $0f : dw $2304 : dw $81c0 : db $0f : dw $2302

org $a4ed74
    dw $0007 : dw $81cc : db $1c : dw $22e4 : dw $81bc : db $1e : dw $2300 : dw $81f8 : db $08 : dw $2309 : dw $81f8 : db $f8 : dw $22e9 : dw $81f6 : db $0d : dw $22e0 : dw $81e8 : db $14 : dw $22e0 : dw $81da : db $1b : dw $22e0

org $a4ed99
    dw $0009 : dw $0000 : db $08 : dw $62ff : dw $0008 : db $f8 : dw $62ef : dw $8008 : db $00 : dw $62ed : dw $81f8 : db $f8 : dw $630d : dw $81d5 : db $11 : dw $22e4 : dw $81c5 : db $11 : dw $2300 : dw $8002 : db $03 : dw $2302 : dw $81f2 : db $0d : dw $2304 : dw $81e4 : db $0d : dw $2302

org $a4edc8
    dw $0007 : dw $800a : db $fa : dw $60eb : dw $81fa : db $fa : dw $610b : dw $8043 : db $fa : dw $60e4 : dw $8053 : db $fa : dw $6100 : dw $8013 : db $fa : dw $60e2 : dw $8023 : db $fa : dw $60e2 : dw $8033 : db $fa : dw $60e2

org $a4eded
    dw $0009 : dw $01f8 : db $f0 : dw $a2ff : dw $01f0 : db $00 : dw $a2ef : dw $81e8 : db $f0 : dw $a2ed : dw $81f8 : db $f8 : dw $a30d : dw $81b3 : db $db : dw $22e4 : dw $81a3 : db $db : dw $2300 : dw $81e0 : db $ec : dw $a302 : dw $81d0 : db $e2 : dw $a304 : dw $81c2 : db $e2 : dw $a302

org $a4ee1c
    dw $0007 : dw $81e6 : db $fa : dw $22eb : dw $81f6 : db $fa : dw $230b : dw $81ad : db $fa : dw $22e4 : dw $819d : db $fa : dw $2300 : dw $81dd : db $fa : dw $22e2 : dw $81cd : db $fa : dw $22e2 : dw $81bd : db $fa : dw $22e2

org $a4ee41
    dw $0009 : dw $0000 : db $08 : dw $62ff : dw $0008 : db $f8 : dw $62ef : dw $8008 : db $00 : dw $62ed : dw $81f8 : db $f8 : dw $630d : dw $81d5 : db $f6 : dw $22e4 : dw $81c5 : db $f6 : dw $2300 : dw $8002 : db $07 : dw $a302 : dw $81f2 : db $fd : dw $a304 : dw $81e4 : db $fd : dw $a302

org $a4ee70
    dw $0007 : dw $81f8 : db $08 : dw $2309 : dw $81f8 : db $f8 : dw $22e9 : dw $81c6 : db $fa : dw $22e4 : dw $81b6 : db $fa : dw $2300 : dw $81f3 : db $0b : dw $a302 : dw $81e3 : db $01 : dw $a304 : dw $81d5 : db $01 : dw $a302

org $a4ee95
    dw $0009 : dw $01f8 : db $08 : dw $20ff : dw $01f0 : db $f8 : dw $20ef : dw $81e8 : db $00 : dw $20ed : dw $81f8 : db $f8 : dw $210d : dw $801b : db $f6 : dw $60e4 : dw $802b : db $f6 : dw $6100 : dw $81ee : db $07 : dw $e102 : dw $81fe : db $fd : dw $e104 : dw $800c : db $fd : dw $e102

org $a4eec4
    dw $0009 : dw $0000 : db $f0 : dw $e0ff : dw $0008 : db $00 : dw $e0ef : dw $8008 : db $f0 : dw $e0ed : dw $81f8 : db $f8 : dw $e10d : dw $803d : db $db : dw $60e4 : dw $804d : db $db : dw $6100 : dw $8010 : db $ec : dw $e102 : dw $8020 : db $e2 : dw $e104 : dw $802e : db $e2 : dw $e102

org $a4eef3
    dw $0004 : dw $01f8 : db $f8 : dw $20d0 : dw $01f8 : db $00 : dw $a0d0 : dw $0000 : db $00 : dw $e0d0 : dw $0000 : db $f8 : dw $60d0

org $a4ef09
    dw $0004 : dw $01f8 : db $f8 : dw $20d1 : dw $01f8 : db $00 : dw $a0d1 : dw $0000 : db $00 : dw $e0d1 : dw $0000 : db $f8 : dw $60d1

org $a4ef1f
    dw $0004 : dw $01f8 : db $00 : dw $a0d2 : dw $01f8 : db $f8 : dw $20d2 : dw $0000 : db $00 : dw $e0d2 : dw $0000 : db $f8 : dw $60d2

org $a4ef35
    dw $0004 : dw $01f8 : db $00 : dw $a0d3 : dw $01f8 : db $f8 : dw $20d3 : dw $0000 : db $00 : dw $e0d3 : dw $0000 : db $f8 : dw $60d3

org $a4ef4b
    dw $0004 : dw $01f0 : db $00 : dw $60d7 : dw $01f8 : db $00 : dw $60d6 : dw $0000 : db $00 : dw $60d5 : dw $0000 : db $f8 : dw $60d4

org $a4ef61
    dw $0003 : dw $01f0 : db $00 : dw $60da : dw $01f8 : db $00 : dw $60d9 : dw $0000 : db $00 : dw $60d8

org $a4ef72
    dw $0004 : dw $01f0 : db $f8 : dw $e0d7 : dw $01f8 : db $f8 : dw $e0d6 : dw $0000 : db $f8 : dw $e0d5 : dw $0000 : db $00 : dw $e0d4

org $a4ef88
    dw $0003 : dw $01f0 : db $f8 : dw $e0da : dw $01f8 : db $f8 : dw $e0d9 : dw $0000 : db $f8 : dw $e0d8

org $a4ef99
    dw $0001 : dw $81f8 : db $f8 : dw $61cc

org $a4efa0
    dw $0006 : dw $0018 : db $00 : dw $61de : dw $0018 : db $f8 : dw $61ce : dw $0010 : db $00 : dw $615d : dw $0010 : db $f8 : dw $614d : dw $8000 : db $f0 : dw $61e6 : dw $81f0 : db $f0 : dw $61e0

org $a4efc0
    dw $0006 : dw $0018 : db $00 : dw $61df : dw $0018 : db $f8 : dw $61cf : dw $0010 : db $00 : dw $615d : dw $0010 : db $f8 : dw $614d : dw $8000 : db $f0 : dw $61e6 : dw $81f0 : db $f0 : dw $61e0

org $a4efe0
    dw $0006 : dw $0010 : db $00 : dw $615e : dw $0010 : db $f8 : dw $614e : dw $0018 : db $00 : dw $613f : dw $0018 : db $f8 : dw $612f : dw $8000 : db $f0 : dw $61e6 : dw $81f0 : db $f0 : dw $61e0

org $a4f000
    dw $0004 : dw $81f0 : db $f0 : dw $61e0 : dw $8000 : db $f0 : dw $61e8 : dw $0010 : db $00 : dw $615f : dw $0010 : db $f8 : dw $614f

org $a4f016
    dw $0002 : dw $81f0 : db $f0 : dw $61e2 : dw $8000 : db $f0 : dw $61ea

org $a4f022
    dw $0001 : dw $81f0 : db $f0 : dw $61e4

;;; tilemaps
org $a4f029
    dw $FFFE
    dw $2008,$000c, $41ff,$41ff,$41ff,$41ff,$41ff,$41ff,$41ff,$41ff,$41ff,$41ff,$41ff,$41ff
    dw $2048,$000c, $41ff,$5caa,$5ca9,$5ca8,$5ca7,$5ca6,$5ca5,$5ca4,$5ca3,$5ca2,$41ff,$41ff
    dw $2088,$000c, $5cbb,$5cba,$5cb9,$5cb8,$5cb7,$5cb6,$5cb5,$5cb4,$5cb3,$5cb2,$5cb1,$5cb0
    dw $20c8,$000c, $5cc7,$5cc6,$5cc5,$5cc4,$5cc3,$5cc2,$5cc1,$5cc0,$5caf,$5cae,$5cad,$5cac
    dw $2108,$000c, $5cd7,$5cd6,$5cd5,$5cd4,$5cd3,$5cd2,$5cd1,$5cd0,$5cbf,$5cbe,$5cbd,$5cbc
    dw $2148,$000c, $5c8c,$5c8b,$5ccf,$5cce,$5ccd,$5ccc,$5ccb,$5cca,$41ff,$41ff,$41ff,$41ff
    dw $2188,$000c, $5c9c,$5c9b,$5cdf,$5cde,$5cdd,$5cdc,$5cdb,$5cda,$5cd9,$5cd8,$41ff,$41ff
    dw $21c8,$000c, $5c9f,$5c9e,$5c9d,$5c8f,$5c8e,$5c8d,$5c46,$5c45,$5c44,$5c43,$41ff,$41ff
    dw $FFFF

org $a4f10d
    dw $FFFE
    dw $2010,$0007, $5ce6,$5ce5,$5ce4,$5ce3,$5ce2,$5ce1,$5ce0
    dw $204a,$000a, $41ff,$5cf8,$5cf7,$5cf6,$5cf5,$5cf4,$5cf3,$5cf2,$5cf1,$5cf0
    dw $2088,$000c, $41ff,$5d01,$5d00,$5cef,$5cee,$5ced,$5cec,$5ceb,$5cea,$5ce9,$41ff,$41ff
    dw $20c8,$000c, $5d12,$5d11,$5d10,$5cff,$5cfe,$5cfd,$5cfc,$5cfb,$5cfa,$41ff,$41ff,$41ff
    dw $2108,$000c, $5d0a,$5d09,$5d08,$5d07,$5d06,$5d05,$5d04,$5d03,$41ff,$41ff,$41ff,$41ff
    dw $2148,$0008, $5d1a,$5d19,$5d18,$5d17,$5d16,$5d15,$5d14,$41ff
    dw $2188,$000a, $5d25,$5d24,$5d23,$5d22,$5d21,$5d20,$5d0f,$5d0e,$5d0d,$5d0c
    dw $21c8,$000a, $5d35,$5d34,$5d33,$5d32,$5d31,$5d30,$5d1f,$5d1e,$5d1d,$5d1c
    dw $FFFF

org $a4f1d3
    dw $FFFE
    dw $2010,$0007, $41ff,$41ff,$41ff,$41ff,$41ff,$41ff,$41ff
    dw $204a,$000a, $5c07,$5c06,$5c05,$5c04,$5c03,$5c02,$41ff,$41ff,$41ff,$41ff
    dw $2088,$000a, $5c18,$5c17,$5c16,$5c15,$5c14,$5c13,$5c12,$5c11,$5c10,$41ff
    dw $20c8,$000b, $5c24,$5c23,$5c22,$5c21,$5c20,$5c0f,$5c0e,$5c0d,$5c0c,$5c0b,$5c0a
    dw $2108,$000c, $5c34,$5c33,$5c32,$5c31,$5c30,$5c1f,$5c1e,$5c1d,$5c1c,$5c1b,$5c1a,$5c19
    dw $2148,$000c, $5c40,$5c2f,$5c2e,$5c2d,$5c2c,$5c2b,$5c2a,$5c29,$5c28,$5c27,$5c26,$5c25
    dw $2188,$000c, $5c50,$5c3f,$5c3e,$5c3d,$5c3c,$5c3b,$5c3a,$5c39,$5c38,$5c37,$5c36,$5c35
    dw $21de,$0001, $5c00
    dw $21c8,$000a, $5c4c,$5c4b,$5c4a,$5c49,$5c48,$5c47,$5c46,$5c45,$5c44,$5c43
    dw $FFFF

org $a4f2a5
    dw $FFFE
    dw $2252,$0004, $5c62,$5c61,$5c60,$5c4f
    dw $2292,$0004, $5c72,$5c71,$5c70,$5c5f
    dw $22d2,$0004, $5c6d,$5c6c,$5c6b,$5c6a
    dw $2312,$0004, $5c7d,$5c7c,$5c7b,$5c7a
    dw $FFFF

org $a4f2d9
    dw $FFFE
    dw $2252,$0004, $5d49,$5d48,$5d47,$5d46
    dw $2292,$0004, $5d59,$5d58,$5d57,$5d56
    dw $22d2,$0004, $5d4d,$5d4c,$5d4b,$5d4a
    dw $2312,$0004, $5d5d,$5d5c,$5d5b,$5d5a
    dw $FFFF

org $a4f30d
    dw $FFFE
    dw $2252,$0004, $5d0b,$5d02,$5d4f,$5d4e
    dw $2292,$0004, $5c51,$5c42,$5d1b,$5d13
    dw $22d2,$0004, $5cf9,$5cab,$5ca1,$5ca0
    dw $2312,$0004, $5c41,$5c09,$5c08,$5c01
    dw $FFFF

org $a4f341
    dw $FFFE
    dw $2340,$0006, $5d45,$5d44,$5d43,$5d42,$5d41,$5d40
    dw $2380,$0006, $5d55,$5d54,$5d53,$5d52,$5d51,$5d50
    dw $FFFF

org $a4f365
    dw $FFFE
    dw $2340,$0006, $5d2b,$5d2a,$5d29,$5d28,$5d27,$5d26
    dw $2380,$0006, $5d3b,$5d3a,$5d39,$5d38,$5d37,$5d36
    dw $FFFF

org $a4f389
    dw $FFFE
    dw $2340,$0006, $5cc9,$5cc8,$5d2f,$5d2e,$5d2d,$5d2c
    dw $2380,$0006, $5ce8,$5ce7,$5d3f,$5d3e,$5d3d,$5d3c
    dw $FFFF

org $a4f3ad
    dw $FFFE
    dw $2048,$000c, $41ff,$5c07,$5c06,$5c05,$5c04,$5c03,$5c02,$41ff,$41ff,$41ff,$41ff,$41ff
    dw $2088,$000c, $5c18,$5c17,$5c16,$5c15,$5c14,$5c13,$5c12,$5c11,$5c10,$41ff,$41ff,$41ff
    dw $20c8,$000c, $5c24,$5c23,$5c22,$5c21,$5c20,$5c0f,$5c0e,$5c0d,$5c0c,$5c0b,$5c0a,$41ff
    dw $2108,$000c, $5c34,$5c33,$5c32,$5c31,$5c30,$5c1f,$5c1e,$5c1d,$5c1c,$5c1b,$5c1a,$5c19
    dw $2148,$000c, $5c40,$5c2f,$5c2e,$5c2d,$5c2c,$5c2b,$5c2a,$5c29,$5c28,$5c27,$5c26,$5c25
    dw $2188,$000c, $5c50,$5c3f,$5c3e,$5c3d,$5c3c,$5c3b,$5c3a,$5c39,$5c38,$5c37,$5c36,$5c35
    dw $21c8,$000c, $5c4c,$5c4b,$5c4a,$5c49,$5c48,$5c47,$5c46,$5c45,$5c44,$5c43,$41ff,$5c00
    dw $2208,$000c, $5c5c,$5c5b,$5c5a,$5c59,$5c58,$5c57,$5c56,$5c55,$5c54,$5c53,$41ff,$41ff
    dw $2248,$000c, $5c67,$5c66,$5c65,$5c64,$5c63,$5c62,$5c61,$5c60,$5c4f,$5c4e,$5c4d,$41ff
    dw $2288,$000c, $5c77,$5c76,$5c75,$5c74,$5c73,$5c72,$5c71,$5c70,$5c5f,$5c5e,$5c5d,$41ff
    dw $22c8,$000c, $41ff,$5c81,$5c80,$5c6f,$5c6e,$5c6d,$5c6c,$5c6b,$5c6a,$5c69,$5c68,$41ff
    dw $2308,$000c, $41ff,$5c91,$5c90,$5c7f,$5c7e,$5c7d,$5c7c,$5c7b,$5c7a,$5c79,$5c78,$41ff
    dw $2348,$000c, $4141,$4140,$5c8a,$5c89,$5c88,$5c87,$5c86,$5c85,$5c84,$5c83,$5c82,$41ff
    dw $2388,$000c, $4151,$4150,$5c9a,$5c99,$5c98,$5c97,$5c96,$5c95,$5c94,$5c93,$41ff,$41ff
    dw $FFFF

org $a4f539
    dw $FFFE
    dw $2208,$000b, $5c5c,$5c5b,$5c5a,$5c59,$5c58,$5c57,$5c56,$5c55,$5c54,$5c53,$41ff
    dw $2248,$000b, $5c67,$5c66,$5c65,$5c64,$5c63,$5c62,$5c61,$5c60,$5c4f,$5c4e,$5c4d
    dw $2288,$000b, $5c77,$5c76,$5c75,$5c74,$5c73,$5c72,$5c71,$5c70,$5c5f,$5c5e,$5c5d
    dw $22c8,$000b, $41ff,$5c81,$5c80,$5c6f,$5c6e,$5c6d,$5c6c,$5c6b,$5c6a,$5c69,$5c68
    dw $2308,$000b, $41ff,$5c91,$5c90,$5c7f,$5c7e,$5c7d,$5c7c,$5c7b,$5c7a,$5c79,$5c78
    dw $2348,$000b, $4141,$4140,$5c8a,$5c89,$5c88,$5c87,$5c86,$5c85,$5c84,$5c83,$5c82
    dw $2388,$000b, $4151,$4150,$5c9a,$5c99,$5c98,$5c97,$5c96,$5c95,$5c94,$5c93,$41ff
    dw $FFFF

;;; spritemaps
org $a4f5f3
    dw $0001 : dw $01fc : db $fc : dw $7a25

org $a4f5fa
    dw $0003 : dw $01f8 : db $f8 : dw $7a25 : dw $01fe : db $f6 : dw $7a25 : dw $01fc : db $fb : dw $7a25

org $a4f60b
    dw $0003 : dw $01f7 : db $f7 : dw $7a25 : dw $01ff : db $f4 : dw $7a25 : dw $01fd : db $fa : dw $7a25

org $a4f61c
    dw $0003 : dw $01f7 : db $f5 : dw $7a43 : dw $01fc : db $f8 : dw $7a43 : dw $01fe : db $f1 : dw $7a43

org $a4f62d
    dw $0003 : dw $01f7 : db $f3 : dw $7a43 : dw $01fc : db $f5 : dw $7a43 : dw $01fe : db $ee : dw $7a43

org $a4f63e
    dw $0003 : dw $01f8 : db $f0 : dw $7a40 : dw $01fc : db $f4 : dw $7a40 : dw $01fe : db $ed : dw $7a40

org $a4f64f
    dw $0003 : dw $01f8 : db $ee : dw $7a40 : dw $01fc : db $f2 : dw $7a40 : dw $01fe : db $ec : dw $7a40

org $a4f660
    dw $0002 : dw $01f8 : db $ec : dw $7a40 : dw $01fc : db $f0 : dw $7a40

org $a4f66c
    dw $0001 : dw $01fc : db $ee : dw $7a40

org $a4f673
    dw $0001 : dw $01fc : db $ee : dw $4a40
