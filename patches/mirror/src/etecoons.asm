;;; compile with thedopefish asar
;;; fix etecoons wall jumping

arch 65816
lorom

;;; see doc/etecoons_ai.asm for more details

;;; fix etecoons X position
org $A199FA+2
        dw $01A1
org $A199FA+2+16
        dw $0191
org $A199FA+2+32
        dw $0181

;;; fix etecoon 2 properties (modified by mistake in mirrortroid, revert to vanilla value)
org $A199FA+8+16
        dw $0C00

;;; exchange run to the right and run to the left instruction lists
;;; as they are set by incrementing Y from previous ones
org $A7E824
        dw $0001,$F1C0
        dw $0005,$F089
        dw $0005,$F09A
        dw $0005,$F0A6
        dw $0005,$F09A

org $A7E87C
        dw $0001,$F024
        dw $0005,$EEED
        dw $0005,$EEFE
        dw $0005,$EF0A
        dw $0005,$EEFE

;;; replace looking right and looking left
org $A7E8F6
        dw $0020,$F1E5
        dw $0020,$F19B

;;; exchange etecoons X offsets when going right and left
org $a7e908
	dw $FFFE
org $a7e908+4
	dw $0002

;;; invert distance in pixel to check against the wall
org $a7eb2c
        lda.w #$ffe0

;;; exchange instruction list when walljumping against a wall
org $A7EBDC
        lda.w #$E83C
org $A7EBF0
        lda.w #$E894

;;; update hardcoded X position used to switch to next AI function
org $A7EC9D
        CMP.w #$01e7
        BMI $18

;;; update hardcoded X position, first tile on the cliff
org $A7ECC1
        CMP.w #$01a8
        BPL $18
org $A7ECE5
        CMP.w #$01a8
        BPL $1E

;;; update hardcoded X position when jumping into tunnel
org $A7ED12
        CMP.w #$0158
        BPL $12

;;; update hardcoded X position when walking in the tunnel
org $A7ED30
        CMP.w #$00b8
	BPL $1E

;;; update hardcoded X position, first tile on the cliff
org $A7EEA0
        CMP.w #$01a8
        BPL $12
