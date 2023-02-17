;;; compile with thedopefish asar
;;; fix kraid camera

arch 65816
lorom

;;; vanilla kraid ;;;

;;; $A959: Initialisation AI - enemy $E2BF (Kraid) ;;;
; $A7:A9E4 A9 02 00    LDA #$0002             ;\
; $A7:A9E7 8D 41 09    STA $0941  [$7E:0941]  ;} Camera distance index = 2 (keeps Samus to the left side of the screen)

;;; $C537: Kraid death - Kraid sinks through floor ;;;
; $A7C594 9C 41 09    STZ $0941  [$7E:0941]  ; Camera distance index = 0 (normal)

; $0941: Camera distance index
; {
;     0: Normal (camera is 60h pixels behind Samus)
;     2: Kraid/Crocomire (camera is 40h/50h pixels to the left of Samus when she's facing right/left)
;     4: Camera is 20h pixels to the left of Samus. There's Crocomire code that sets this, but I think it's unused
;     6: Camera is E0h pixels to the left of Samus
; }


;;; mirror kraid ;;;
; $A7:A9E4 A9 02 00    LDA #$0006

;;; $C0A1: Kraid function - Kraid gets big - release camera ;;;
;;; can't change camera 2 as crocomire is not mirrored, so use camera 4 which is unused
org $A7C0A1
        bra kraid_camera_hijack : nop
kraid_camera_hijack_comeback:

;;; unused code [a7c0bd - a7c167]
;;; $C0BD: Unused. Crumble first section of Kraid's spike floor ;;;
; $A7:C167 60          RTS
org $A7C0BD
kraid_camera_hijack:
	;; set camera to mirrored kraid mode
	lda #$0004
	sta $0941

	;; vanilla code
        lda #$AC4D
        bra kraid_camera_hijack_comeback

warnpc $A7C0C8

; ; Target distance camera is to the left of Samus
; $90:963F             dw 0060, 0040, 0020, 00E0 ; When Samus is facing right
; $90:9647             dw 00A0, 0050, 0020, 00E0 ; When Samus is facing left
org $909643
        dw $00B0
org $90964B
        dw $00C0
