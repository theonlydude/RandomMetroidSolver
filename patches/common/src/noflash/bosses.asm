; Kraid damage flashing
org $A7B394
        LDY.w #$0020

; Crocomire damage flashing
org $A48CDD
        LDA.w #$0814
; this doesn't stop his legs from flashing but it's a start?

; Phantoon damage flashing
org $A7DD7F
        LDA.w #$092B
; make phantoon flash brown instead of bright white

; Draygon damage flashing
org $A5955B
        LDY.w #$A257
org $A595AA
        LDY.w #$A257
; not ideal but it works I guess? Draygon's stomach still flashes a bit when hurt, which is probably ok?

; Mother Brain jar death flashing
org $A9CFFD
        LDA.w #$0000
        STA $7E781C
        LDA.w #$0001
        STA $7E781E
