
;;; Fast doors patch diasm/tweak
;;; Original patch by Rakki

;; ['$82de55 - 26']

arch snes.cpu
lorom

;;; Door transition - right

org $80ae9c
	ADC #$0008	;} Layer 1 X position += 8 (original is += 4)

org $80aea6
	ADC #$0008	;} Layer 2 X position += 8 (original is += 4)

org $80aeb5
	CPX #$0020	;} If [door transition frame counter] = 20h (original is 40)

;;; Door transition - left

org $80aee0
	SBC #$0008	;} Layer 1 X position -= 8 (original is -= 4)

org $80aeea
	SBC #$0008	;} Layer 1 X position -= 8 (original is -= 4)

org $80aef9
	CPX #$0020	;} If [door transition frame counter] = 20h (original is 40)

;;; Door transition - down

org $80af63
	ADC #$0008	;} Layer 1 Y position += 8 (original is += 4)

org $80af6d
	ADC #$0008	;} Layer 1 Y position += 8 (original is += 4)

org $80af7c
	CPX #$001D	; If number of times screen has scrolled >= 1Dh: (original is 39h)


;;; Door transition - up

org $80afe5
	SBC #$0008	;} Layer 1 Y position -= 8 (original is -= 4)

org $80afef
	SBC #$0008	;} Layer 1 Y position -= 8 (original is -= 4)

org $80aff5
	CPX #$0003	; If number of times screen has scrolled < 3 (original is 5)

org $80b029
	CPX #$001D	; If number of times screen has scrolled == 1Dh: (original is 39h)

;;; General change
org $82d961
	LDA #$0006	; Set Palette change denominator to 6h (original is Ch)

org $82de50
	BPL door_rw_mult

org $82de55
door_rewrite:
	ROR A
        ROR A
        BCS doors_rw_2
        LDA.W #$00C8
        BRA door_rw_mult
doors_rw_2:
	LDA.W #$0180
door_rw_mult:
	ASL A
	STA.B $13
	LDA.B $12
	STA.W $092B
	LDA.B $14
	STA.W $092D
	RTS

org $82e3f1
	CMP #$0003  ; If door direction is 3 (up)  (orig is 2=down)

org $82e498
	CMP #$0003  ; If door direction is 3 (up)  (orig is 3 as well...WTF is that about?)
