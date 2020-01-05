;;; VARIA new game hook: skips intro and customizes starting point
;;; 
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

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

;; org $80c527
;; crateria_load:
;;     dw $99BD, $8B1A, $0000, $0000, $0000, $0078, $0040
