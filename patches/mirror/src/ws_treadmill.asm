;;; compile with thedopefish asar
;;; mirror treadmill direction

arch 65816
lorom

;;; $B971: Door ASM: start Wrecked Ship treadmill west entrance ;;;
; Room $93FE, door list index 1: Door
; $8F:B971 A0 75 82    LDY #$8275
; $8F:B974 22 27 80 87 JSL $878027[$87:8027]
; $8F:B978 22 D7 83 84 JSL $8483D7[$84:83D7]
; $8F:B97C             dx 04, 09, B64B
; $8F:B980 60          RTS
org $8FB97E
	dw $B64F

;;; $E1D8: Door ASM: start Wrecked Ship treadmill east entrance ;;;
; Room $CAF6, door list index 0: Door
; $8F:E1D8 A0 7B 82    LDY #$827B
; $8F:E1DB 22 27 80 87 JSL $878027[$87:8027]
; $8F:E1DF 22 D7 83 84 JSL $8483D7[$84:83D7]
; $8F:E1E3             dx 04, 09, B64F
; $8F:E1E7 60          RTS
org $8FE1E5
        dw $B64B
