arch snes.cpu
lorom

org $82805b
    jsl start_save

org $a1ffe0
start_save:
    lda #$0000 : jsl $8081fa    ; wake zebes
    lda #$0001 : sta $079f      ; area
    lda #$0000 : sta $078b      ; save index
    jsl $80c437                 ; actually load
    rtl
