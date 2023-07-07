
namespace spikes

org $948EAF		;//bts "spike"
	LDA $0A50
	ADC #$003C	;//vanilla spike damage (0A0EAF)
	JSR Spikes

org $948EEA		;//bts 01
	LDA $0A50
	ADC #$0010	;//vanilla spike damage (0A0EEE)
	JSR Spikes

org $949886		;//bts 02
	LDA $0A50
	ADC #$0010	;//vanilla spike damage	(0A188A)
	JSR Spikes

org $948F25		;//bts 03
	LDA $0A50	
	ADC #$0010	;//vanilla spike damage	(0A0F29)
	JSR Spikes

;//FREE SPACE
;------------
org $94B1A0		;//[0A31A0] ($0F bytes)
Spikes:
	PHA
	LDA $7ED808			;//difficulty flag
	BEQ +				;//branch if normal mode
	PLA
	ASL A				;//double damage
	PHA
+
	PLA
	STA $0A50			;//damage to samus (suit divisor)
	RTS

namespace off
