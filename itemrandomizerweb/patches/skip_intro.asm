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
    // Do some checks to see that we're actually starting a new game

    // Make sure game mode is 1f
    lda $7e0998
    cmp.w #$001f
    bne .ret

    // check that Game time and frames is equal zero for new game
    // (Thanks Smiley and P.JBoy from metconst)
    LDA $09DA
    ORA $09DC
    ORA $09DE
    ORA $09E0
    bne .ret

    // Set construction zone and red tower elevator doors to blue
    lda $7ed8b6
    ora.w #$0004
    sta $7ed8b6
    lda $7ed8b2
    ora.w #$0001
    sta $7ed8b2

    // Call the save code to create a new file
    //lda $7e0952
    //jsl $818000

.ret:   
    lda #$0000
    rtl
