;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

;; custom credits
arch 65816
lorom

incsrc "sym/utils.asm"
incsrc "sym/base.asm"

;;; -------------------------------
;;; CONSTANTS ;;;
;;; -------------------------------

incsrc "constants.asm"

;; Defines for the script and credits data
!speed = set_scroll
!set = $9a17
!delay = $9a0d
!draw = $0000
!end = $f6fe, $99fe
!blank = $1fc0
!row = $0040
!pink = "table tables/pink.tbl,rtl"
!yellow = "table tables/yellow.tbl,rtl"
!cyan = "table tables/cyan.tbl,rtl"
!blue = "table tables/blue.tbl,rtl"
!green = "table tables/green.tbl,rtl"
!orange = "table tables/orange.tbl,rtl"
!purple = "table tables/purple.tbl,rtl"
!big = "table tables/big.tbl,rtl"
;; tmp RAM for credits scroll speed
!scroll_speed = $7fffe8

;; RAM and constants for IGT display on end screen
!end_seconds_1 = $0DF8
!end_seconds_2 = $0DFA
!sprite_colon_x = #$00B4
!sprite_second_1x = #$00BC
!sprite_second_2x = #$00C4

;;; -------------------------------
;; HIJACKS
;;; -------------------------------

;; Hijack the original credits code to read the script from bank $DF
org $8b9976
    jml scroll

org $8b999b
    jml patch1

org $8b99e5
    jml patch2

org $8b9a08
    jml patch3

org $8b9a19
    jml patch4

;; Hijack after decompression of regular credits tilemaps
org $8be0d1
    jsl copy

;; hijacks for samus ending animations
org $8BE00D
	jsr check_samus_good_time
org $8BE1E3
	jsr check_samus_good_time
org $8BE1E8
	jsr check_samus_avg_time
org $8BE279
	jsr check_samus_good_time
org $8BE2E7
	jsr check_samus_good_time
org $8BE2EC
	jsr check_samus_avg_time
org $8BE328
	jsr check_samus_good_time
org $8BE36F
	jsr check_samus_good_time
org $8BE374
	jsr check_samus_avg_time
org $8BF558
	jsr check_samus_avg_time
org $8BF59A
	jsr check_samus_avg_time
org $8BF5BD
	jsr check_samus_avg_time

;;; -------------------------------
;;; CODE
;;; -------------------------------

;; Load credits script data from bank $df instead of $8c
org $8bf770
;; set scroll speed routine (!speed instruction in credits script)
set_scroll:
    rep #$30
    phb : pea $df00 : plb : plb
    lda $0000, y
    sta !scroll_speed
    iny
    iny
    plb
    rts

scroll:
    inc $1995
    lda $1995
    cmp !scroll_speed
    beq +
    lda $1997
    jml $8b9989
+
    stz $1995
    inc $1997
    lda $1997
    jml $8b9989


patch1:
    phb : pea $df00 : plb : plb
    lda $0000, y
    bpl +
    plb
    jml $8b99a0
+
    plb
    jml $8b99aa

patch2:
    sta $0014
    phb : pea $df00 : plb : plb
    lda $0002, y
    plb
    jml $8b99eb

patch3:
    phb : pea $df00 : plb : plb
    lda $0000, y
    tay
    plb
    jml $8b9a0c

patch4:
    phb : pea $df00 : plb : plb
    lda $0000, y
    plb
    sta $19fb
    jml $8b9a1f

;; Copy custom credits tilemap data from $ceb240,x to $7f2000,x
copy:
    pha
    phx
    ldx #$0000
-
    lda.l credits, x
    cmp #$0000
    beq +
    sta $7f2000, x
    inx
    inx
    jmp -
+

    ldx #$0000
-
    lda.l itemlocations, x
    rep 4 : nop
    cmp #$0000
    beq +
    sta $7fa000, x
    inx
    inx
    jmp -
+

    jsl write_stats
    lda #$0002
    sta !scroll_speed
    plx
    pla
    jsl $8b95ce
    rtl

warnpc $8bf88f

;; configurable hh:mm values for samus animations at the end
org $8bf900
samus_times:
;; "good time" limit: 1h30m
samus_good_time_h:
	dw $0001
samus_good_time_m:
	dw $001e
;; "average time" limit: 3h
samus_avg_time_h:
	dw $0003
samus_avg_time_m:
	dw $0000

check_samus_good_time:
	lda !igt_hours
	cmp.l samus_good_time_h
	bne .end
	lda !igt_minutes
	cmp.l samus_good_time_m
.end:
	rts

check_samus_avg_time:
	lda !igt_hours
	cmp.l samus_avg_time_h
	bne .end
	lda !igt_minutes
	cmp.l samus_avg_time_m
.end:
	rts

warnpc $8bf92f

org $dfd6f0
;; Draw full time as hh:mm:ss:ff
;; Pointer to first byte of RAM in A
draw_full_time:
    phx
    phb
    pea $7f7f : plb : plb
    tax
    lda $0000, x
    sta $16
    lda $0002, x
    sta $14
    lda #$003c
    sta $12
    lda #$ffff
    sta $1a
    jsl utils_div32 ;; frames in $14, rest in $16
    rep 6 : iny ;; Increment Y three positions forward to write the last value
    lda $14
    jsr draw_two
    tya
    sec
    sbc #$0010
    tay     ;; Skip back 8 characters to draw the top three things
    lda $16
    jsr draw_time
    plb
    plx
    rts

;; Draw time as xx:yy:zz
draw_time:
    phx
    phb
    rep 6 : dey ;; Decrement Y by 3 characters so the time count fits
    pea $7f7f : plb : plb
    sta $004204
    sep #$20
    lda #$ff
    sta $1a
    lda #$3c
    sta $004206
    pha : pla :  pha : pla : rep #$20
    lda $004216 ;; Seconds or Frames
    sta $12
    lda $004214 ;; First two groups (hours/minutes or minutes/seconds)
    sta $004204
    sep #$20
    lda #$3c
    sta $004206
    pha : pla :  pha : pla : rep #$20
    lda $004216
    sta $14
    lda $004214 ;; First group (hours or minutes)
    jsr draw_two
    iny : iny ;; Skip past separator
    lda $14 ;; Second group (minutes or seconds)
    jsr draw_two
    iny : iny
    lda $12 ;; Last group (seconds or frames)
    jsr draw_two
    plb
    plx
    rts

;; Draw 5-digit value to credits tilemap
;; A = number to draw, Y = row address
draw_value:
    phx
    phb
    pea $7f7f : plb : plb
    sta $004204
    lda #$0000
    sta $1a     ;; Leading zeroes flag
    sep #$20
    lda #$64
    sta $004206
    pha : pla :  pha : pla : rep #$20
    lda $004216 ;; Last two digits
    sta $12
    lda $004214 ;; Top three digits
    jsr draw_three
    lda $12
    jsr draw_two
.end:
    plb
    plx
    rts

draw_three:
    sta $004204
    sep #$20
    lda #$64
    sta $004206
    pha : pla :  pha : pla : rep #$20
    lda $004214 ;; Hundreds
    asl
    tax
    cmp $1a
    beq +
    lda.l numbers_top, x
    sta $0034, y
    lda.l numbers_bot, x
    sta $0074, y
    dec $1a
+
    iny : iny ;; Next number
    lda $004216

draw_two:
    sta $004204
    sep #$20
    lda #$0a
    sta $004206
    pha : pla :  pha : pla : rep #$20
    lda $004214
    asl
    tax
    cmp $1a
    beq +
    lda.l numbers_top, x
    sta $0034, y
    lda.l numbers_bot, x
    sta $0074, y
    dec $1a
+
    lda $004216
    asl
    tax
    cmp $1a
    beq +
    lda.l numbers_top, x
    sta $0036, y
    lda.l numbers_bot, x
    sta $0076, y
    dec $1a
+
    rep 4 : iny
    rts

;; Loop through stat table and update RAM with numbers representing those stats
write_stats:
    phy
    phb
    php
    pea $dfdf : plb : plb
    rep #$30
    jsl base_load_stats      ;; Copy stats back from SRAM
    ldx #$0000
    ldy #$0000

.loop:
    ;; Get pointer to table
    tya
    asl : asl : asl
    tax

    ;; Load stat type
    lda.l stats+4, x
    beq .end
    cmp #$0001
    beq .number
    cmp #$0002
    beq .time
    cmp #$0003
    beq .fulltime
    jmp .continue

.number:
    ;; Load statistic
    lda.l stats, x
    jsl base_load_stat
    pha

    ;; Load row address
    lda.l stats+2, x
    tyx
    tay
    pla
    jsr draw_value
    txy
    jmp .continue

.time:
    ;; Load statistic
    lda.l stats, x
    jsl base_load_stat
    pha

    ;; Load row address
    lda.l stats+2, x
    tyx
    tay
    pla
    jsr draw_time
    txy
    jmp .continue

.fulltime:
    lda.l stats, x        ;; Get stat id
    asl
    clc
    adc #$!_stats_ram          ;; Get pointer to value instead of actual value
    pha

    ;; Load row address
    lda.l stats+2, x
    tyx
    tay
    pla
    jsr draw_full_time
    txy
    jmp .continue

.continue:
    iny
    jmp .loop

.end:
    plp
    plb
    ply
    rtl

numbers_top:
    dw $0060, $0061, $0062, $0063, $0064, $0065, $0066, $0067, $0068, $0069, $006a, $006b, $006c, $006d, $006e, $006f
numbers_bot:
    dw $0070, $0071, $0072, $0073, $0074, $0075, $0076, $0077, $0078, $0079, $007a, $007b, $007c, $007d, $007e, $007f

print "DF code end: ", pc
warnpc $dfd91a
;; New credits script in free space of bank $DF
org $dfd91b
script:
    dw !set, $0002
-
    dw !draw, !blank
    dw !delay, -

    ;; Show a compact and sped up version of the original credits so we get time to add more
    ;; change scroll speed to 1 pixel per frame

    ;; NOTE: when adding new stuff to the credits, remove blanks from
    ;;	     "Last info" section, as this credits script is in sync with credits music

    dw !speed, $0001

    dw !draw, !row*0      ;; SUPER METROID STAFF
    dw !draw, !blank
    dw !draw, !row*4      ;; PRODUCER
    dw !draw, !blank
    dw !draw, !row*7      ;; MAKOTO KANOH
    dw !draw, !row*8
    dw !draw, !blank
    dw !draw, !row*9      ;; DIRECTOR
    dw !draw, !blank
    dw !draw, !row*10     ;; YOSHI SAKAMOTO
    dw !draw, !row*11
    dw !draw, !blank
    dw !draw, !row*12     ;; BACK GROUND DESIGNERS
    dw !draw, !blank
    dw !draw, !row*13     ;; HIROFUMI MATSUOKA
    dw !draw, !row*14
    dw !draw, !blank
    dw !draw, !row*15     ;; MASAHIKO MASHIMO
    dw !draw, !row*16
    dw !draw, !blank
    dw !draw, !row*17     ;; HIROYUKI KIMURA
    dw !draw, !row*18
    dw !draw, !blank
    dw !draw, !row*19     ;; OBJECT DESIGNERS
    dw !draw, !blank
    dw !draw, !row*20     ;; TOHRU OHSAWA
    dw !draw, !row*21
    dw !draw, !blank
    dw !draw, !row*22     ;; TOMOYOSHI YAMANE
    dw !draw, !row*23
    dw !draw, !blank
    dw !draw, !row*24     ;; SAMUS ORIGINAL DESIGNERS
    dw !draw, !blank
    dw !draw, !row*25     ;; HIROJI KIYOTAKE
    dw !draw, !row*26
    dw !draw, !blank
    dw !draw, !row*27     ;; SAMUS DESIGNER
    dw !draw, !blank
    dw !draw, !row*28     ;; TOMOMI YAMANE
    dw !draw, !row*29
    dw !draw, !blank
    dw !draw, !row*83     ;; SOUND PROGRAM
    dw !draw, !row*107    ;; AND SOUND EFFECTS
    dw !draw, !blank
    dw !draw, !row*84     ;; KENJI YAMAMOTO
    dw !draw, !row*85
    dw !draw, !blank
    dw !draw, !row*86     ;; MUSIC COMPOSERS
    dw !draw, !blank
    dw !draw, !row*84     ;; KENJI YAMAMOTO
    dw !draw, !row*85
    dw !draw, !blank
    dw !draw, !row*87     ;; MINAKO HAMANO
    dw !draw, !row*88
    dw !draw, !blank
    dw !draw, !row*30     ;; PROGRAM DIRECTOR
    dw !draw, !blank
    dw !draw, !row*31     ;; KENJI IMAI
    dw !draw, !row*64
    dw !draw, !blank
    dw !draw, !row*65     ;; SYSTEM COORDINATOR
    dw !draw, !blank
    dw !draw, !row*66     ;; KENJI NAKAJIMA
    dw !draw, !row*67
    dw !draw, !blank
    dw !draw, !row*68     ;; SYSTEM PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*69     ;; YOSHIKAZU MORI
    dw !draw, !row*70
    dw !draw, !blank
    dw !draw, !row*71     ;; SAMUS PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*72     ;; ISAMU KUBOTA
    dw !draw, !row*73
    dw !draw, !blank
    dw !draw, !row*74     ;; EVENT PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*75     ;; MUTSURU MATSUMOTO
    dw !draw, !row*76
    dw !draw, !blank
    dw !draw, !row*77     ;; ENEMY PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*78     ;; YASUHIKO FUJI
    dw !draw, !row*79
    dw !draw, !blank
    dw !draw, !row*80     ;; MAP PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*81     ;; MOTOMU CHIKARAISHI
    dw !draw, !row*82
    dw !draw, !blank
    dw !draw, !row*101    ;; ASSISTANT PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*102    ;; KOUICHI ABE
    dw !draw, !row*103
    dw !draw, !blank
    dw !draw, !row*104    ;; COORDINATORS
    dw !draw, !blank
    dw !draw, !row*105    ;; KATSUYA YAMANO
    dw !draw, !row*106
    dw !draw, !blank
    dw !draw, !row*63     ;; TSUTOMU KANESHIGE
    dw !draw, !row*96
    dw !draw, !blank
    dw !draw, !row*89    ;; PRINTED ART WORK
    dw !draw, !blank
    dw !draw, !row*90    ;; MASAFUMI SAKASHITA
    dw !draw, !row*91
    dw !draw, !blank
    dw !draw, !row*92    ;; YASUO INOUE
    dw !draw, !row*93
    dw !draw, !blank
    dw !draw, !row*94    ;; MARY COCOMA
    dw !draw, !row*95
    dw !draw, !blank
    dw !draw, !row*99    ;; YUSUKE NAKANO
    dw !draw, !row*100
    dw !draw, !blank
    dw !draw, !row*108   ;; SHINYA SANO
    dw !draw, !row*109
    dw !draw, !blank
    dw !draw, !row*110   ;; NORIYUKI SATO
    dw !draw, !row*111
    dw !draw, !blank
    dw !draw, !row*32    ;; SPECIAL THANKS TO
    dw !draw, !blank
    dw !draw, !row*33    ;; DAN OWSEN
    dw !draw, !row*34
    dw !draw, !blank
    dw !draw, !row*35    ;; GEORGE SINFIELD
    dw !draw, !row*36
    dw !draw, !blank
    dw !draw, !row*39    ;; MASARU OKADA
    dw !draw, !row*40
    dw !draw, !blank
    dw !draw, !row*43    ;; TAKAHIRO HARADA
    dw !draw, !row*44
    dw !draw, !blank
    dw !draw, !row*47    ;; KOHTA FUKUI
    dw !draw, !row*48
    dw !draw, !blank
    dw !draw, !row*49    ;; KEISUKE TERASAKI
    dw !draw, !row*50
    dw !draw, !blank
    dw !draw, !row*51    ;; MASARU YAMANAKA
    dw !draw, !row*52
    dw !draw, !blank
    dw !draw, !row*53    ;; HITOSHI YAMAGAMI
    dw !draw, !row*54
    dw !draw, !blank
    dw !draw, !row*57    ;; NOBUHIRO OZAKI
    dw !draw, !row*58
    dw !draw, !blank
    dw !draw, !row*59    ;; KENICHI NAKAMURA
    dw !draw, !row*60
    dw !draw, !blank
    dw !draw, !row*61    ;; TAKEHIKO HOSOKAWA
    dw !draw, !row*62
    dw !draw, !blank
    dw !draw, !row*97    ;; SATOSHI MATSUMURA
    dw !draw, !row*98
    dw !draw, !blank
    dw !draw, !row*122   ;; TAKESHI NAGAREDA
    dw !draw, !row*123
    dw !draw, !blank
    dw !draw, !row*124   ;; MASAHIRO KAWANO
    dw !draw, !row*125
    dw !draw, !blank
    dw !draw, !row*45    ;; HIRO YAMADA
    dw !draw, !row*46
    dw !draw, !blank
    dw !draw, !row*112   ;; AND ALL OF R&D1 STAFFS
    dw !draw, !row*113
    dw !draw, !blank
    dw !draw, !row*114   ;; GENERAL MANAGER
    dw !draw, !blank
    dw !draw, !row*5     ;; GUMPEI YOKOI
    dw !draw, !row*6
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    ;; change scroll speed to 2 pixels per frame
    dw !speed, $0002
    ;; Custom item randomizer credits text
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*128 ;; VARIA RANDOMIZER STAFF
    dw !draw, !blank
    dw !draw, !row*129
    dw !draw, !row*130
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*131 ;; ORIGINAL ITEM RANDOMIZERS
    dw !draw, !blank
    dw !draw, !row*132
    dw !draw, !row*133
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*134 ;; CONTRIBUTORS
    dw !draw, !blank
    dw !draw, !row*135
    dw !draw, !row*136
    dw !draw, !blank
    dw !draw, !row*137
    dw !draw, !row*138
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*139 ;; SPECIAL THANKS TO
    dw !draw, !blank
    dw !draw, !row*140 ;; SMILEY SUKU
    dw !draw, !row*141
    dw !draw, !blank
    dw !draw, !row*154 ;; hackers
    dw !draw, !row*176
    dw !draw, !blank
    dw !draw, !row*177 ;; donators
    dw !draw, !row*178
    dw !draw, !blank
    dw !draw, !row*142 ;; METROID CONSTRUCTION
    dw !draw, !blank
    dw !draw, !row*143
    dw !draw, !row*144
    dw !draw, !blank
    dw !draw, !row*165 ;; SUPER METROID DISASSEMBLY
    dw !draw, !blank
    dw !draw, !row*166
    dw !draw, !row*167
    dw !draw, !blank
    dw !draw, !row*184 ;; SpriteSomething
    dw !draw, !blank
    dw !draw, !row*224
    dw !draw, !row*225
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*145 ;; RANDOMIZER PARAMETERS
    dw !draw, !blank
    dw !draw, !row*155 ;; PROG SPEED
    dw !draw, !blank
    dw !draw, !row*156 ;; PROG DIFF
    dw !draw, !blank
    dw !draw, !row*158 ;; SUITS RESTRICTION
    dw !draw, !blank
    dw !draw, !row*159 ;; MORPH PLACEMENT
    dw !draw, !blank

    ;; change scroll speed to 3 px/frame
    dw !speed, $0003

    dw !draw, !row*160 ;; SUPER FUN COMBAT
    dw !draw, !blank
    dw !draw, !row*161 ;; SUPER FUN MOVEMENT
    dw !draw, !blank
    dw !draw, !row*162 ;; SUPER FUN SUITS
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*157 ;; ITEMS DISTRIBUTION
    dw !draw, !blank
    dw !draw, !row*146 ;; LOCATIONS
    dw !draw, !row*147
    dw !draw, !blank
    dw !draw, !row*148 ;; LOCS DETAIL
    dw !draw, !row*149
    dw !draw, !blank
    dw !draw, !row*168 ;; AVAILABLE
    dw !draw, !row*169
    dw !draw, !blank
    dw !draw, !row*152 ;; ENERGY DETAIL
    dw !draw, !row*153
    dw !draw, !blank
    dw !draw, !row*150 ;; AMMO DETAIL
    dw !draw, !row*151
    dw !draw, !blank
    dw !draw, !row*163 ;; AMMO DISTRIBUTION
    dw !draw, !row*164
    dw !draw, !blank

    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*223 ;; PLAY THIS RANDOMIZER AT
    dw !draw, !blank
    dw !draw, !row*179
    dw !draw, !row*180
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*181
    dw !draw, !blank
    dw !draw, !row*182
    dw !draw, !blank
    dw !draw, !blank

    dw !draw, !row*183 ;; GAMEPLAY STATS
    dw !draw, !blank
    dw !draw, !row*172 ;; DEATHS
    dw !draw, !row*173
    dw !draw, !blank
    dw !draw, !row*174 ;; RESETS
    dw !draw, !row*175
    dw !draw, !blank
    dw !draw, !row*185 ;; DOOR TRANSITIONS
    dw !draw, !row*186
    dw !draw, !blank
    dw !draw, !row*187 ;; TIME IN DOORS
    dw !draw, !row*188
    dw !draw, !blank
    dw !draw, !row*189 ;; TIME ADJUSTING DOOR
    dw !draw, !row*190
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*191 ;; TIME SPENT
    dw !draw, !blank
    dw !draw, !row*192 ;; CERES
    dw !draw, !row*193
    dw !draw, !blank
    dw !draw, !row*194 ;; CRATERIA
    dw !draw, !row*195
    dw !draw, !blank
    dw !draw, !row*196 ;; GREEN BRINSTAR
    dw !draw, !row*197
    dw !draw, !blank
    dw !draw, !row*198 ;; RED BRINSTAR
    dw !draw, !row*199
    dw !draw, !blank
    dw !draw, !row*200 ;; WRECKED SHIP
    dw !draw, !row*201
    dw !draw, !blank
    dw !draw, !row*202 ;; KRAID
    dw !draw, !row*203
    dw !draw, !blank
    dw !draw, !row*226 ;; UPPER NORFAIR
    dw !draw, !row*227
    dw !draw, !blank
    dw !draw, !row*228 ;; CROC
    dw !draw, !row*229
    dw !draw, !blank
    dw !draw, !row*230 ;; LOWER NORFAIR
    dw !draw, !row*231
    dw !draw, !blank
    dw !draw, !row*232 ;; WEST MARIDIA
    dw !draw, !row*233
    dw !draw, !blank
    dw !draw, !row*234 ;; EAST MARIDIA
    dw !draw, !row*235
    dw !draw, !blank
    dw !draw, !row*236 ;; TOURIAN
    dw !draw, !row*237
    dw !draw, !blank
    dw !draw, !row*221 ;; PAUSE MENU
    dw !draw, !row*222
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*204 ;; SHOTS AND AMMO
    dw !draw, !blank
    dw !draw, !row*170 ;; UNCHARGED
    dw !draw, !row*171
    dw !draw, !blank
    dw !draw, !row*205 ;; CHARGED
    dw !draw, !row*206
    dw !draw, !blank
    dw !draw, !row*207 ;; SBA
    dw !draw, !row*208
    dw !draw, !blank
    dw !draw, !row*209 ;; MISSILES
    dw !draw, !row*210
    dw !draw, !blank
    dw !draw, !row*211 ;; SUPERS
    dw !draw, !row*212
    dw !draw, !blank
    dw !draw, !row*213 ;; PBs
    dw !draw, !row*214
    dw !draw, !blank
    dw !draw, !row*215 ;; BOMBS
    dw !draw, !row*216


    ;; Draw item locations
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*640
    dw !draw, !blank
    dw !draw, !blank

    dw !draw, !row*641
    dw !draw, !row*642
    dw !draw, !blank
    dw !draw, !row*643
    dw !draw, !row*644
    dw !draw, !blank
    dw !draw, !row*645
    dw !draw, !row*646
    dw !draw, !blank
    dw !draw, !row*647
    dw !draw, !row*648
    dw !draw, !blank
    dw !draw, !row*649
    dw !draw, !row*650
    dw !draw, !blank
    dw !draw, !row*651
    dw !draw, !row*652
    dw !draw, !blank
    dw !draw, !row*653
    dw !draw, !row*654
    dw !draw, !blank
    dw !draw, !row*655
    dw !draw, !row*656
    dw !draw, !blank
    dw !draw, !row*657
    dw !draw, !row*658
    dw !draw, !blank
    dw !draw, !row*659
    dw !draw, !row*660
    dw !draw, !blank
    dw !draw, !row*661
    dw !draw, !row*662
    dw !draw, !blank
    dw !draw, !row*663
    dw !draw, !row*664
    dw !draw, !blank
    dw !draw, !row*665
    dw !draw, !row*666
    dw !draw, !blank
    dw !draw, !row*667
    dw !draw, !row*668
    dw !draw, !blank
    dw !draw, !row*669
    dw !draw, !row*670
    dw !draw, !blank
    dw !draw, !row*671
    dw !draw, !row*672
    dw !draw, !blank
    dw !draw, !row*673
    dw !draw, !row*674
    dw !draw, !blank
    dw !draw, !row*675
    dw !draw, !row*676
    dw !draw, !blank
    dw !draw, !row*677
    dw !draw, !row*678
    dw !draw, !blank

    ;; Last info.
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank

    dw !draw, !row*217 ;; Final Time
    dw !draw, !row*218

    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank

    dw !draw, !row*219 ;; Thanks
    dw !draw, !row*220

    ;; don't touch those blanks
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank

    ;; Set scroll speed to 4 frames per pixel
    dw !speed, $0004

    ;; Scroll all text off and end credits
    dw !set, $0017
-
    dw !draw, !blank
    dw !delay, -
    dw !end

stats:
    ;; STAT ID, ADDRESS,    TYPE (1 = Number, 2 = Time, 3 = Full time), UNUSED
    dw 0,       !row*217,  3, 0    ;; Full RTA Time
    dw 2,       !row*185,  1, 0    ;; Door transitions
    dw 3,       !row*187,  3, 0    ;; Time in doors
    dw 5,       !row*189,  2, 0    ;; Time adjusting doors
    dw 7,       !row*192,  3, 0    ;; Ceres
    dw 9,       !row*194,  3, 0    ;; Crateria/Blue brin
    dw 11,      !row*196,  3, 0    ;; Green/Pink brin
    dw 13,      !row*198,  3, 0    ;; Red Brin
    dw 15,      !row*200,  3, 0    ;; WS
    dw 17,      !row*202,  3, 0    ;; Kraid
    dw 19,      !row*226,  3, 0    ;; Upper Norfair
    dw 21,      !row*228,  3, 0    ;; Croc
    dw 23,      !row*230,  3, 0    ;; Lower Norfair
    dw 25,      !row*232,  3, 0    ;; West Maridia
    dw 27,      !row*234,  3, 0    ;; East Maridia
    dw 29,      !row*236,  3, 0    ;; Tourian
    dw 31,      !row*170,  1, 0    ;; Uncharged Shots
    dw 32,      !row*205,  1, 0    ;; Charged Shots
    dw 33,      !row*207,  1, 0    ;; Special Beam Attacks
    dw 34,      !row*209,  1, 0    ;; Missiles
    dw 35,      !row*211,  1, 0    ;; Super Missiles
    dw 36,      !row*213,  1, 0    ;; Power Bombs
    dw 37,      !row*215,  1, 0    ;; Bombs
    dw 38,      !row*221,  3, 0    ;; Time in pause
    dw 40,      !row*172,  1, 0    ;; deaths
    dw 41,      !row*174,  1, 0    ;; resets
    dw 0,               0,  0, 0    ;; end of table

print "bank DF end : ", pc

;; palette rando stores its relocated palette there
warnpc $dfe1ff

;; Relocated credits tilemap to free space in bank CE
org $ceb240
credits:
    ;; When using big text, it has to be repeated twice, first in UPPERCASE and then in lowercase since it's split into two parts
    ;; Numbers are mapped in a special way as described below:
    ;; 0123456789%& '´
    ;; }!@#$%&/()>~.

    ;; This is not in display order
    !pink
    dw "     VARIA RANDOMIZER STAFF     " ;; 128
    !big
    dw "          DUDE AND FLO          " ;; 129
    dw "          dude and flo          " ;; 130
    !purple
    dw "    ORIGINAL ITEM RANDOMIZERS   " ;; 131
    !big
    dw "       TOTAL   DESSYREQT        " ;; 132
    dw "       total   dessyreqt        " ;; 133
    !purple
    dw "          CONTRIBUTORS          " ;; 134
    !big
    dw "    RAND 0   COUT   CHRISC      " ;; 135
    dw "    rand }   cout   chrisc      " ;; 136
    dw "        DJLO   PRANKARD         " ;; 137
    dw "        djlo   prankard         " ;; 138
    !cyan
    dw "       SPECIAL THANKS TO        " ;; 139
    !big
    dw "         SMILEY   SUKU          " ;; 140
    dw "         smiley   suku          " ;; 141
    !yellow
    dw "      METROID CONSTRUCTION      " ;; 142
    !big
    dw "     METROIDCONSTRUCTION COM    " ;; 143
    dw "     metroidconstruction.com    " ;; 144
    !purple
    ;; params title
    dw "     RANDOMIZER PARAMETERS      " ;; 145
    !big
    ;; item distribution data start
.items_distrib:
    dw " ITEM LOCATIONS              XX " ;; 146
    dw " item locations............. xx " ;; 147
    dw "  MAJ XX EN XX AMMO XX BLANK XX " ;; 148
    dw "  maj xx en xx ammo XX blank XX " ;; 149
    dw " AMMO PACKS  MI XX SUP XX PB XX " ;; 150
    dw " ammo packs  mi XX sup XX pb XX " ;; 151
    dw " HEALTH TANKS         E XX R XX " ;; 152
    dw " health tanks ......  e.xx.r xx " ;; 153
    dw "   ALL SUPER METROID HACKERS    " ;; 154 : credits
    ;; params data start
    !yellow
    dw " PROGRESSION SPEED .... XXXXXXX " ;; 155
    dw " PROGRESSION DIFFICULTY XXXXXXX " ;; 156
    ;; item distrib title
    !purple
    dw "       ITEMS DISTRIBUTION       " ;; 157
    ;; params data end
    !yellow
    dw " SUITS RESTRICTION ........ XXX " ;; 158
    dw " MORPH PLACEMENT ....... XXXXXX " ;; 159
    dw " SUPER FUN COMBAT ......... XXX " ;; 160
    dw " SUPER FUN MOVEMENT ....... XXX " ;; 161
    dw " SUPER FUN SUITS .......... XXX " ;; 162
    ;; item distrib data end
    !big
    dw " AMMO DISTRIBUTION  X X X X X X " ;; 163
    dw " ammo distribution  x.x x.x x.x " ;; 164
    ;; credits continued
    !yellow
    dw "   SUPER METROID DISASSEMBLY    " ;; 165
    !big
    dw "        PJBOY    KEJARDON       " ;; 166
    dw "        pjboy    kejardon       " ;; 167
.items_distrib_continued:
;; stats continued
    dw " AVAILABLE AMMO XXX% ENERGY XXX%" ;; 168
    dw " available ammo xxx> energy xxx>" ;; 169
    dw " UNCHARGED SHOTS              0 " ;; 170
    dw " uncharged shots              } " ;; 171
    dw " DEATHS                       0 " ;; 172
    dw " deaths                       } " ;; 173
    dw " RESETS                       0 " ;; 174
    dw " resets                       } " ;; 175
;; some more credits
    dw "   all super metroid hackers    " ;; 176
    dw "     OUR GENEROUS DONATORS      " ;; 177
    dw "     our generous donators      " ;; 178
;; varia URLs
    !big
    dw "            VARIA RUN           " ;; 179
    dw "            varia.run           " ;; 180
    !orange
    dw "         BETA.VARIA.RUN         " ;; 181
    dw "        DISCORD.VARIA.RUN       " ;; 182
    !purple
    dw "      GAMEPLAY STATISTICS       " ;; 183
    !yellow
    dw "        SPRITESOMETHING         " ;; 184  : credits
    !big
    dw " DOOR TRANSITIONS             0 " ;; 185
    dw " door transitions             } " ;; 186
    dw " TIME IN DOORS      00'00'00^00 " ;; 187
    dw " time in doors      }} }} }} }} " ;; 188
    dw " TIME ALIGNING DOORS   00'00^00 " ;; 189
    dw " time aligning doors   }} }} }} " ;; 190
    !blue
    dw "         TIME SPENT IN          " ;; 191
    !big
    dw " CERES              00'00'00^00 " ;; 192
    dw " ceres              }} }} }} }} " ;; 193
    dw " CRATERIA           00'00'00^00 " ;; 194
    dw " crateria           }} }} }} }} " ;; 195
    dw " GREEN BRINSTAR     00'00'00^00 " ;; 196
    dw " green brinstar     }} }} }} }} " ;; 197
    dw " RED BRINSTAR       00'00'00^00 " ;; 198
    dw " red brinstar       }} }} }} }} " ;; 199
    dw " WRECKED SHIP       00'00'00^00 " ;; 200
    dw " wrecked ship       }} }} }} }} " ;; 201
    dw " KRAID'S LAIR       00'00'00^00 " ;; 202
    dw " kraid s lair       }} }} }} }} " ;; 203
    !green
    dw "      SHOTS AND AMMO FIRED      " ;; 204
    !big
    dw " CHARGED SHOTS                0 " ;; 205
    dw " charged shots                } " ;; 206
    dw " SPECIAL BEAM ATTACKS         0 " ;; 207
    dw " special beam attacks         } " ;; 208
    dw " MISSILES                     0 " ;; 209
    dw " missiles                     } " ;; 210
    dw " SUPER MISSILES               0 " ;; 211
    dw " super missiles               } " ;; 212
    dw " POWER BOMBS                  0 " ;; 213
    dw " power bombs                  } " ;; 214
    dw " BOMBS                        0 " ;; 215
    dw " bombs                        } " ;; 216
    dw " FINAL TIME         00'00'00^00 " ;; 217
    dw " final time         }} }} }} }} " ;; 218
    dw "       THANKS FOR PLAYING       " ;; 219
    dw "       thanks for playing       " ;; 220
    dw " PAUSE MENU         00'00'00^00 " ;; 221
    dw " pause menu         }} }} }} }} " ;; 222
    !cyan
    dw "     PLAY THIS RANDOMIZER AT    " ;; 223
    !big
    ;; how about some more credits
    dw "    ARTHEAU   MIKE TRETHEWEY    " ;; 224
    dw "    artheau   mike trethewey    " ;; 225
    ;; now some more stats
    dw " UPPER NORFAIR      00'00'00^00 " ;; 226
    dw " upper norfair      }} }} }} }} " ;; 227
    dw " CROCOMIRE          00'00'00^00 " ;; 228
    dw " crocomire          }} }} }} }} " ;; 229
    dw " LOWER NORFAIR      00'00'00^00 " ;; 230
    dw " lower norfair      }} }} }} }} " ;; 231
    dw " WEST MARIDIA       00'00'00^00 " ;; 232
    dw " west maridia       }} }} }} }} " ;; 233
    dw " EAST MARIDIA       00'00'00^00 " ;; 234
    dw " east maridia       }} }} }} }} " ;; 235
    dw " TOURIAN            00'00'00^00 " ;; 236
    dw " tourian            }} }} }} }} " ;; 237

    dw $0000                              ;; End of credits tilemap

warnpc $ceffff

;; Placeholder label for item locations inserted by the randomizer
org $ded200
itemlocations:
    !pink
    dw "         ITEM LOCATIONS         " ;; 640
.start:
;; pad with spaces to mark space as used + to apply the patch on a vanilla ROM
!counter = 0
while !counter < 1239
        dw $007F
        !counter #= !counter+1
endif
        dw $0000

;; update 'clear time' to display 'real  time'
org $8cb49b
;; 'R'
        dw $0002
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB4A7
;; 'RE'
        dw $0004
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB4BD
;; 'REA'
        dw $0006
        dw $01C8 : db $00 : dw $3130
        dw $01C8 : db $F8 : dw $3120
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB4DD
;; 'REAL'
        dw $0008
        dw $01D0 : db $00 : dw $313B
        dw $01D0 : db $F8 : dw $312B
        dw $01C8 : db $00 : dw $3130
        dw $01C8 : db $F8 : dw $3120
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB507
;; 'REAL'
        dw $0008
        dw $01D0 : db $00 : dw $313B
        dw $01D0 : db $F8 : dw $312B
        dw $01C8 : db $00 : dw $3130
        dw $01C8 : db $F8 : dw $3120
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB53B
;; 'REAL T'
        dw $000A
        dw $01E0 : db $00 : dw $3153
        dw $01E0 : db $F8 : dw $3143
        dw $01D0 : db $00 : dw $313B
        dw $01D0 : db $F8 : dw $312B
        dw $01C8 : db $00 : dw $3130
        dw $01C8 : db $F8 : dw $3120
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB579
;; 'REAL TI'
        dw $000C
        dw $01E8 : db $00 : dw $3138
        dw $01E8 : db $F8 : dw $3128
        dw $01E0 : db $00 : dw $3153
        dw $01E0 : db $F8 : dw $3143
        dw $01D0 : db $00 : dw $313B
        dw $01D0 : db $F8 : dw $312B
        dw $01C8 : db $00 : dw $3130
        dw $01C8 : db $F8 : dw $3120
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB5C1
;; 'REAL TIM'
        dw $000E
        dw $01F0 : db $00 : dw $313C
        dw $01F0 : db $F8 : dw $312C
        dw $01E8 : db $00 : dw $3138
        dw $01E8 : db $F8 : dw $3128
        dw $01E0 : db $00 : dw $3153
        dw $01E0 : db $F8 : dw $3143
        dw $01D0 : db $00 : dw $313B
        dw $01D0 : db $F8 : dw $312B
        dw $01C8 : db $00 : dw $3130
        dw $01C8 : db $F8 : dw $3120
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141

org $8CB613
;; 'REAL TIME'
        dw $0010
        dw $01F8 : db $00 : dw $3134
        dw $01F8 : db $F8 : dw $3124
        dw $01F0 : db $00 : dw $313C
        dw $01F0 : db $F8 : dw $312C
        dw $01E8 : db $00 : dw $3138
        dw $01E8 : db $F8 : dw $3128
        dw $01E0 : db $00 : dw $3153
        dw $01E0 : db $F8 : dw $3143
        dw $01D0 : db $00 : dw $313B
        dw $01D0 : db $F8 : dw $312B
        dw $01C8 : db $00 : dw $3130
        dw $01C8 : db $F8 : dw $3120
        dw $01C0 : db $00 : dw $3134
        dw $01C0 : db $F8 : dw $3124
        dw $01B8 : db $00 : dw $3151
        dw $01B8 : db $F8 : dw $3141


;; draw RTA seconds at ship end
org $8beefd+4
        dw instruction_list_time

org $8bf416
        jsr hijack_push_rta

;; update X pos for hour1 hour2 : min1 min2
org $8bF065
        dw $008C
org $8bF074
        dw $0094
org $8bF07D
        dw $009C
org $8bF08C
        dw $00A4
org $8bF09B
        dw $00AC

org $8bf930
hijack_push_rta:
	;; vanilla
        STA $0DF2

	;; load RTA seconds
        LDA !igt_seconds
        STA $4204
        SEP #$20
        LDA #$0A
        STA $4206
        NOP
        NOP
        NOP
        NOP
        NOP
        NOP
        NOP
        REP #$20
        LDA $4214
	;; use unused RAM to store seconds next to hours/minutes
        STA !end_seconds_1
        LDA $4216
        STA !end_seconds_2
	RTS

;; add :xx at the end of displayed time to display seconds
instruction_list_time:
        dw $0008, $B49B
        dw $0008, $B4A7
        dw $0008, $B4BD
        dw $0008, $B4DD
        dw $000F, $B507
        dw $0008, $B53B
        dw $0008, $B579
        dw $0008, $B5C1
	;; hour
        dw $000F, $B613, $F41B
        dw $0008, $B613, $F424
	;; :
        dw $0008, $B613, $F42D
	;; minute
        dw $0008, $B613, $F436
        dw $0008, $B613, $F43F
	;; :
        dw $0008, $B613, display_second_colon
	;; second
        dw $0008, $B613, display_second_1
        dw $0008, $B613, display_second_2

        dw $0080, $B613, $F448
loop:
        dw $000F, $B613
	;; goto loop
        dw $94BC, loop

display_second_colon:
        PHY
        LDY #sprite_colon
        JSR $938A ;; Spawn cinematic sprite object
        PLY
        RTS

display_second_1:
        PHY
        LDY #sprite_second_1
        JSR $938A ;; Spawn cinematic sprite object
        PLY
        RTS

display_second_2:
        PHY
        LDY #sprite_second_2
        JSR $938A ;; Spawn cinematic sprite object
        PLY
        RTS

;;          _____________ Initialisation function
;;         |                      ________ Pre-instruction
;;         |                     |       ___ Instruction list
;;         |                     |      |
sprite_colon:
        dw init_sprite_colon,    $F3B9, $ECD1
sprite_second_1:
        dw init_sprite_second_1, $F3B9, $EC81
sprite_second_2:
        dw init_sprite_second_2, $F3B9, $EC81

init_sprite_colon:
        LDA !sprite_colon_x
        STA $1A7D,y
        JMP $F051

init_sprite_second_1:
        LDA !end_seconds_1
        JSR $F0A3
        LDA !sprite_second_1x
        STA $1A7D,y
        JMP $F051

init_sprite_second_2:
        LDA !end_seconds_2
        JSR $F0A3
        LDA !sprite_second_2x
        STA $1A7D,y
        JMP $F051

print "bank 8B end : ", pc
warnpc $8bfa0f
