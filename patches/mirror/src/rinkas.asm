;;; compile with thedopefish asar
;;; fix rinka spawn in mother brain room

arch 65816
lorom

; ; Room $DD58, vanilla rinkas
; $A1:E351             
; D23F,0337,0036,0000,6000,0000,0001,0000, ; enemy 03, spawn mode 1
; D23F,0337,00A6,0000,6000,0000,0002,0000, ; enemy 04, spawn mode 2
; D23F,0277,001C,0000,6000,0000,0003,0000, ; enemy 05, spawn mode 3
; 	
; ; Room $DD58, mirror rinkas
; $A1:E351             
; D23F,01c9,0036,0000,6000,0000,0001,0000, ; enemy 03, spawn mode 1
; D23F,01c9,00A6,0000,6000,0000,0000,0000, ; enemy 04, spawn mode 0
; D23F,0289,001C,0000,6000,0000,0003,0000, ; enemy 05, spawn mode 3

;;; set back 2nd rinka spawn mode to 2
org $a1e36d
        dw $0002
