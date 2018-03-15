arch snes.cpu
lorom

org $8ba592
  db $a9
  db $2f
  db $b7
    
// Hijack init routine to autosave and set door flags
org $828067
    jsl introskip_doorflags

org $80ff00
introskip_doorflags:
    // Set construction zone and red tower elevator doors to blue
    lda $7ed8b6
    ora.w #$0004
    sta $7ed8b6    
    lda $7ed8b2
    ora.w #$0001
    sta $7ed8b2

    lda #$0000
    rtl
