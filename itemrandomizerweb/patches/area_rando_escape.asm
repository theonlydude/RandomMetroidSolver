;;; Randomized escape sequence
;;;
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; HIJACKS
org $82df38
    jml music_and_enemies

org $848c91
    jmp map_station
    
org $848cf3
    jmp save_station
    
org $84c556
    jsr super_check             ; green gate left
    
org $84c575
    jsr super_check             ; green gate right

org $84cee8
    jsr pb_check                ; bomb block PB reaction

org $84cf3c
    jsr pb_check                ; PB block

org $84cf75
    jsr super_check             ; super block

org $8fe896
    jsr room_setup

org $8fe8bd
    jsr room_main

;;; CODE in bank 84 (PLM)
org $84f070

;;; Disables "ammo locked" elements b/c of no ammo in escape :
;;; makes them react to hyper beam shots
    
;;; returns zero flag set if in the escape and projectile is hyper beam
escape_hyper_check:    
    jsl check_ext_escape : bcc .nohit
    lda $0c18,x
    bit #$0008                  ; check for plasma (hyper = wave+plasma)
    beq .nohit
    lda #$0000                  ; set zero flag
    bra .end
.nohit:
    lda #$0001                  ; reset zero flag
.end:
    rts

super_check:
    cmp #$0200                  ; vanilla check for supers
    beq .end
    jsr escape_hyper_check
.end:
    rts

pb_check:
    cmp #$0300                  ; vanilla check for PBs
    beq .end
    jsr escape_hyper_check
.end:
    rts

;;; make all map stations reveal all the map
;;; we do this because only crateria map station
;;; will be opened.
map_station:
    ;; activate map stations for all regions
    lda #$ffff
    ldx #$0000
-
    sta $7ed908,x
    inx : inx
    cpx #$0008
    bcc -
    ;; resume original routine
    jmp $8c9f

;;; Disables save stations during the escape
save_station:
    jsl check_ext_escape : bcc .resume
    ;; disable save
    jmp $8d32
.resume:
    ;; resume original routine
    lda #$0017
    jmp $8cf6



;;; CODE (in a tiny bit of bank 8F free space)
org $8fe9a0
    ;; test door ASM
    lda #$0000 : jsl $8081fa    ; wake zebes
    lda #$000e : jsl $8081fa    ; set escape flag
    ;; door ASM for MB escape door
escape_setup:
    ;; open all doors
    lda #$ffff
    ldx #$0000
-
    sta $7ed8b0,x
    inx : inx
    cpx #$0020
    bcc -
    ;; kill all bosses
    ldx #$0000
-
    sta $7ed828,x
    inx : inx
    cpx #$0008
    bcc -
    rts

room_setup:
    jsl check_ext_escape : bcc .end
    phb                         ; do vanilla setup to call room asm
    phk
    plb
    jsr $919c                   ; sets up room shaking
    plb
.end:
    ;; goes back to vanilla setup asm call
    lda $0018,x
    rts

room_main:
    jsl check_ext_escape : bcc .end
    phb                         ; do vanilla setup to call room asm
    phk
    plb
    jsr $c124                   ; explosions etc
    plb
.end:
    ;; goes back to vanilla room asm call
    ldx $07df
    rts

warnpc $8fe9ff

   
;;; DATA (bank A1 free space)
org $a1f000  
;;; custom enemy populations for some rooms

;;; room ID, enemy population in bank a1, enemy GFX in bank b4 
enemy_table:
    dw $a7de,one_elev_list_1,$8aed  ; business center
    dw $a6a1,$98e4,$8529            ; warehouse (vanilla data)
    dw $a98d,$bb0e,$8b11            ; croc room (vanilla "croc dead" data)
    dw $962a,$89DF,$81F3            ; red brin elevator (vanilla data)
    dw $a322,one_elev_list_1,$863F  ; red tower top
    dw $94cc,$8B74,$8255            ; forgotten hiway elevator (vanilla data)
    dw $d30b,one_elev_list_2,$8d85  ; forgotten hiway
    dw $9e9f,one_elev_list_3,$83b5  ; morph room
    dw $97b5,$8b61,$824b            ; blue brin elevator (vanilla data)
    dw $9ad9,one_elev_list_1,$8541  ; green brin shaft
    dw $9938,$8573,$80d3            ; green brin elevator (vanilla data)
    dw $af3f,$a544,$873d            ; LN elevator (vanilla data)
    dw $b236,one_elev_list_4,$893d  ; LN main hall
    ;; table terminator
    dw $ffff

one_elev_list_1:
    dw $D73F,$0080,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

one_elev_list_2:
    dw $D73F,$0080,$02C0,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

one_elev_list_3:
    dw $D73F,$0580,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

one_elev_list_4:
    dw $D73F,$0480,$02A2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00


;;; CODE (in bank A1 free space)

;;; checks the need for "extended escape" setup
;;; return carry set if setup is needed, carry clear if not
check_ext_escape:
    lda #$000e : jsl $808233
    bcc .end
    ;; filter out Tourian area and Crateria escape rooms
    ;; (already handled by the game)
    lda $079f                  ; current area
    cmp #$0005 : beq .filtered ; filter out Tourian
    cmp #$0000 : bne .needed   ; if not crateria, we have to do extended escape
    lda $079b                  ; current room (in crateria)
    ;; few rooms, so do a nasty "if/elseif" instead of iterating through a table
    cmp #$91f8 : beq .filtered ; Landing site
    cmp #$92fd : beq .filtered ; parlor
    cmp #$9879 : beq .filtered ; BT hallway
    cmp #$9804 : beq .filtered ; BT
    cmp #$96ba : beq .filtered ; climb
.needed:
    sec
    bra .end
.filtered:
    clc
.end:
    rtl

music_and_enemies:
    lda $0006,x                 ; common vanilla fx load
    sta $07CD
    jsl check_ext_escape : bcs .escape
    ;; vanilla 
    lda $0004,x ;\
    and #$00ff  ;} Music data index = [[X] + 4]
    sta $07CB   ;/
    lda $0005,x ;\
    and #$00FF  ;} Music track index = [[X] + 5]
    sta $07C9   ;/
    lda $0008,x ;\
    sta $07CF   ;} Enemy population pointer = [[X] + 8]
    lda $000A,x ;\
    sta $07D1   ;} Enemy set pointer = [[X] + Ah]
    bra .end
.escape:
    stz $07CB   ;} Music data index = 0
    stz $07C9   ;} Music track index = 0
    
    ;; check room ID against list of custom enemy populations (elevators etc.)
    phb : phk : plb             ; data bank=program bank
    ldy #$0000
.loop:
    lda enemy_table,y
    cmp #$ffff
    beq .empty_list
    lda $079B
    cmp enemy_table,y
    beq .load
    rep 6 : iny
    bra .loop
.load:
    iny : iny
    lda enemy_table,y
    sta $07CF
    iny : iny
    lda enemy_table,y
    sta $07D1
    plb
    bra .end
.empty_list:
    plb
    lda #$85a9  ;\
    sta $07CF   ;} Enemy population pointer = empty list
    lda #$80eb  ;\
    sta $07D1   ;} Enemy set pointer = empty list
.end:
    jml $82df5c

warnpc $a1ffff

;;; TEST
org $83AB34
    ;; escape door header => norfair map station
    dw $A7DE
    db $00,$04,$01,$46,$00,$04
    dw $8000
    dw $E9A0                    ; sets escape flag and triggers escape setup asm
;;; END TEST
