namespace environmental

;org $8DE37C		;//heated damage suit check
	;AND #$0020		;//and #$0021
	
;org $8DE385		;//speed of health loss in heated room no varia
	;JSR Envi		;//adc #$4000

;; ;//[FREE SPACE]
;; ;--------------
;; org $8DFFF0		;//[06FFF0] ($0E bytes)
;; Envi:
;; 	LDA $7ED808		;//difficulty stored in sram
;; 	BEQ +			;//branch if normal mode
;; 	ADC #$4800		;//higher numbers drain faster
;; 	RTS
;; +
;; 	ADC #$4000		;//vanilla
;; 	RTS

;//org $909E8B			;//speed of health loss in lava
;//org $909E8F			;//speed of health loss in acid

org $9081FE		;//lava
	JSR Hotstuff		;//sta $0A4E
org $908240		;//acid
	JSR Hotstuff		;//sta $0A4E		

;//[FREE SPACE]
;--------------
org $90FF00		;//[087F00] ($12 bytes)
Hotstuff:
	PHA
	LDA $7ED808
	BEQ +			;//branch if normal mode
	PLA
	ASL A
	STA $0A4E
	RTS
+
	PLA
	STA $0A4E		;//deal damage to Samus (1/65536th)
	RTS

namespace off

