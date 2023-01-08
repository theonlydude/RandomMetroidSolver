;;; compile with thedopefish asar
;;; fix snails in aqueduct orientation and X position for mirror

arch 65816
lorom

org $A1D357
; Room $D5A7, state $D5B4: Enemy population
;;; inverse orientation
;;; 01: ?
;;; 02: ?
;;; 03: down
;;; 04: left  ceiling
;;; 05: right ceiling
;;; 06: left  ground
;;; 07: right ground

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
dw $DBBF,$00BC,$01D8,$0006,$A800,$0000,$0004,$0000
dw $DBBF,$03E0,$0294,$0007,$A800,$0000,$0003,$0000
dw $DBBF,$01E0,$0264,$0003,$A800,$0000,$0005,$0000
dw $DBBF,$0425,$0130,$0004,$A800,$0000,$0007,$0000
dw $DBBF,$00b0,$02B8,$0003,$A000,$0000,$0002,$0000
dw $FFFF : db $05
