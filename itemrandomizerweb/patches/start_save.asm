arch snes.cpu
lorom

;; org $82805b
;;     jsl start_save

;; org $a1ffe0
;; start_save:    
;;     lda #$0000 : jsl $8081fa    ; wake zebes
;;     lda #$0001 : sta $079f      ; area
;;     lda #$0000 : sta $078b      ; save index
;;     jsl $80c437                 ; actually load
;;     rtl

;;; FIXME : completely tmp mess
    
org $82e8d5
    jsl additional_plms

org $82eb8b
    jsl additional_plms

org $8fffd0
additional_plms:
    lda $079B
    cmp #$99bd
    bne .end
    ldx #save_plm
    jsl $84846a
.end:
    ;; vanilla code (call door asm)
    jsl $8fe8a3
    rtl

print pc
save_plm:
    dw $B76F
    db $0B, $09
    dw $0007

org $80c527
crateria_load:
    dw $99BD, $8B1A, $0000, $0000, $0000, $0078, $0040
