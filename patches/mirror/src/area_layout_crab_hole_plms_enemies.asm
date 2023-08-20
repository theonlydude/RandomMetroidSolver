lorom
arch 65816
	
; Room $D21C, state $D229: PLM
; vanilla:
;     dx B703,08,0E,D24D,
;     dx B703,08,11,D24D

org $8fc53b
; room D21C: Crab Hole
    ; Scroll PLM
    dw $b703 : db $07 : db $0d : dw $d24d 
    ; Scroll PLM
    dw $b703 : db $08 : db $12 : dw $d24d 


; Enemy population format is:
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

; Room $D21C, state $D229: Enemy population
org $A1DE47
    dw $D77F,$006f,$0162,$0003,$2800,$0000,$0002,$0000 


