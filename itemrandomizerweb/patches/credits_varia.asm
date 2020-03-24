// custom credits
arch snes.cpu
lorom

// Defines for the script and credits data
define speed $f770
define set $9a17
define delay $9a0d
define draw $0000
define end $f6fe, $99fe
define blank $1fc0
define row $0040
define pink "table tables/pink.tbl"
define yellow "table tables/yellow.tbl"
define cyan "table tables/cyan.tbl"
define blue "table tables/blue.tbl"
define green "table tables/green.tbl"
define orange "table tables/orange.tbl"
define purple "table tables/purple.tbl"
define big "table tables/big.tbl"
// store last save slot in unused SRAM
define last_saveslot $7016fe
// backup RAM for timer to avoid it to get cleared at boot
define timer_backup1 $7fffe2
define timer_backup2 {timer_backup1}+2
define softreset $7fffe6
define scroll_speed $7fffe8
// RTA timer RAM updated during NMI
define timer1 $05b8
define timer2 $05ba
// routine in new_game.asm
define check_new_game   $A1F210

define stats_sram_sz_b  #$0080
define stats_sram_sz_w  #$0040
define tmp_area_sz      #$00df

define _stats_ram        fc00
define stats_ram         $7f{_stats_ram}
define stats_timer       {stats_ram}

define _stats_sram_slot0      1400
define _stats_sram_slot1      1700
define _stats_sram_slot2      1a00
define stats_sram_slot0       $70{_stats_sram_slot0}
define stats_sram_slot1       $70{_stats_sram_slot1}
define stats_sram_slot2       $70{_stats_sram_slot2}

define last_stats_save_ok_off  #$02fc
define last_stats_save_ok_flag #$caca

// Patch boot to init our stuff
org $80844B
    jml boot1
org $808490
    jml boot2

// Patch loading and saving routines
org $81807f
    jmp patch_save

org $8180f7
    jmp patch_load

// Hijack loading new game to reset stats
org $828063
    jsl clear_values

// Hijack the original credits code to read the script from bank $DF
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

// Hijack when samus is in the ship and ready to leave the planet
org $a2ab13
    jsl game_end

// Patch NMI to skip resetting 05ba and instead use that as an extra time counter
org $8095e5
nmi:
    ldx #$00
    stx $05b4
    ldx $05b5
    inx
    stx $05b5
    inc $05b6
.inc:
    rep #$30
    inc $05b8
    bne +
    inc $05ba
+
    bra .end

org $809602
    bra .inc
.end:
    ply
    plx
    pla
    pld
    plb
    rti

// Patch boot to init stuff
org $80fe00
boot1:
    lda #$0000
    sta {timer_backup1}
    sta {timer_backup2}
    jsl is_save_slot
    beq .save
    bra .cont   // don't restore anything if no game was ever saved
.save:
    // check if "soft reset" and restore RAM timer
    // if not, restore last SRAM timer (console power cycle)
    lda {softreset} // Check if we're softresetting
    cmp #$babe
    bne .power
    lda {timer1}
    sta {timer_backup1}
    lda {timer2}
    sta {timer_backup2}
    bra .cont
.power:
    // load timer from SRAM, last stats if possible
    lda #$0000
    jsl save_index
    lda $70000,x
    sta {timer_backup1}
    lda $70002,x
    sta {timer_backup2}
.cont:
    // vanilla init stuff
    ldx #$1ffe
    lda #$0000
-
    stz $0000, x
    dex
    dex
    bpl -
    // place marker for resets
    lda #$babe
    sta {softreset}
    // resume
    jml $808455

boot2:
    ldx #$1ffe
-
    stz $0000,x
    stz $2000,x
    stz $4000,x
    stz $6000,x
    stz $8000,x
    stz $a000,x
    stz $c000,x
    stz $e000,x
    dex
    dex
    bpl -

    ldx {tmp_area_sz}          // clear temp variables
    lda #$0000
-
    sta $7fff00, x
    dex
    dex
    bpl -

    jml $8084af

//// save related routines
// zero flag set if value in last_saveslot is valid
is_save_slot:
    // check for the 3 possible valid values
    lda {last_saveslot}
    cmp #$0010
    beq .end
    cmp #$0011
    beq .end
    cmp #$0012
    beq .end
.end:
    rtl

// assuming a valid save slot is in last_saveslot,
// stores in X the bank $70 index to stats area
// arg A: if 0 we want last stats, otherwise standard stats
save_index:
    pha
    lda {last_saveslot}
    cmp #$0010
    beq .slot0
    cmp #$0011
    beq .slot1
.slot2:
    ldx #${_stats_sram_slot2}
    bra .last
.slot0:
    ldx #${_stats_sram_slot0}
    bra .last
.slot1:
    ldx #${_stats_sram_slot1}
.last:
    pla
    bne .end
    txa
    clc
    adc {stats_sram_sz_b}
    tax
.end:
    rtl

warnpc $80ffbf

// Patch load and save routines
// a save will always be performed when starting a new game (see new_game.asm)
org $81ef20
patch_save:
    lda {timer1}
    sta {stats_timer}
    lda {timer2}
    sta {stats_timer}+2
    lda #$0001
    jsl save_stats
    ply
    plx
    clc
    plb
    plp
    rtl

patch_load:
    lda $7e0952
    clc
    adc #$0010
    cmp {last_saveslot}     // we're loading the same save that's played last
    bne .load
    lda {softreset}
    cmp #$babe
    // discard time spent in menus by restoring boot time timer
    // TODO add menu time to pause stat and make it a general menus stat?
    lda {timer_backup1}
    sta {timer1}
    lda {timer_backup2}
    sta {timer2}
    beq .end                   // use stats from RAM
.load:
    // load stats from SRAM
    jsl load_stats
    // update live timer
    lda {stats_timer}
    sta {timer1}
    lda {stats_timer}+2
    sta {timer2}
.end:
    ply
    plx
    clc
    plb
    rtl

////////////////////////// CREDITS /////////////////////////////

// Hijack after decompression of regular credits tilemaps
org $8be0d1
    jsl copy

// Load credits script data from bank $df instead of $8c
org $8bf770
set_scroll:
    rep #$30
    phb; pea $df00; plb; plb
    lda $0000, y
    sta {scroll_speed}
    iny
    iny
    plb
    rts

scroll:
    inc $1995
    lda $1995
    cmp {scroll_speed}
    beq +
    lda $1997
    jml $8b9989
+
    stz $1995
    inc $1997
    lda $1997
    jml $8b9989


patch1:
    phb; pea $df00; plb; plb
    lda $0000, y
    bpl +
    plb
    jml $8b99a0
+
    plb
    jml $8b99aa

patch2:
    sta $0014
    phb; pea $df00; plb; plb
    lda $0002, y
    plb
    jml $8b99eb

patch3:
    phb; pea $df00; plb; plb
    lda $0000, y
    tay
    plb
    jml $8b9a0c

patch4:
    phb; pea $df00; plb; plb
    lda $0000, y
    plb
    sta $19fb
    jml $8b9a1f

// Copy custom credits tilemap data from $ceb240,x to $7f2000,x
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
    cmp #$0000
    beq +
    sta $7fa000, x
    inx
    inx
    jmp -
+

    jsl write_stats
    lda #$0002
    sta {scroll_speed}
    plx
    pla
    jsl $8b95ce
    rtl

clear_values:
    php
    rep #$30
    jsl {check_new_game}
    bne .ret

    ldx #$0000
    lda #$0000
-
    jsl store_stat
    inx
    cpx {stats_sram_sz_w}
    bne -

    // Clear RTA Timer
    lda #$0000
    sta {timer1}
    sta {timer2}

.ret:
    plp
    jsl $809a79
    rtl

// Game has ended, save RTA timer to RAM and copy all stats to SRAM a final time
game_end:
    lda {timer1}
    sta {stats_timer}
    lda {timer2}
    sta {stats_timer}+2

    // Subtract frames from pressing down at ship to this code running
    lda {stats_timer}
    sec
    sbc #$013d
    sta {stats_timer}
    lda #$0000  // if carry clear this will subtract one from the high byte of timer
    sbc {stats_timer}+2

    lda #$0001
    jsl save_stats
    lda #$000a
    jsl $90f084
    rtl

org $dfd4f0
// Draw full time as hh:mm:ss:ff
// Pointer to first byte of RAM in A
draw_full_time:
    phx
    phb
    pea $7f7f; plb; plb
    tax
    lda $0000, x
    sta $16
    lda $0002, x
    sta $14
    lda #$003c
    sta $12
    lda #$ffff
    sta $1a
    jsr div32 // frames in $14, rest in $16
    iny; iny; iny; iny; iny; iny // Increment Y three positions forward to write the last value
    lda $14
    jsr draw_two
    tya
    sec
    sbc #$0010
    tay     // Skip back 8 characters to draw the top three things
    lda $16
    jsr draw_time
    plb
    plx
    rts

// Draw time as xx:yy:zz
draw_time:
    phx
    phb
    dey; dey; dey; dey; dey; dey // Decrement Y by 3 characters so the time count fits
    pea $7f7f; plb; plb
    sta $004204
    sep #$20
    lda #$ff
    sta $1a
    lda #$3c
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004216 // Seconds or Frames
    sta $12
    lda $004214 // First two groups (hours/minutes or minutes/seconds)
    sta $004204
    sep #$20
    lda #$3c
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004216
    sta $14
    lda $004214 // First group (hours or minutes)
    jsr draw_two
    iny; iny // Skip past separator
    lda $14 // Second group (minutes or seconds)
    jsr draw_two
    iny; iny
    lda $12 // Last group (seconds or frames)
    jsr draw_two
    plb
    plx
    rts

// Draw 5-digit value to credits tilemap
// A = number to draw, Y = row address
draw_value:
    phx
    phb
    pea $7f7f; plb; plb
    sta $004204
    lda #$0000
    sta $1a     // Leading zeroes flag
    sep #$20
    lda #$64
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004216 // Last two digits
    sta $12
    lda $004214 // Top three digits
    jsr draw_three
    lda $12
    jsr draw_two
    plb
    plx
    rts

draw_three:
    sta $004204
    sep #$20
    lda #$64
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004214 // Hundreds
    asl
    tax
    cmp $1a
    beq +
    lda numbers_top, x
    sta $0034, y
    lda numbers_bot, x
    sta $0074, y
    dec $1a
+
    iny; iny // Next number
    lda $004216

draw_two:
    sta $004204
    sep #$20
    lda #$0a
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004214
    asl
    tax
    cmp $1a
    beq +
    lda numbers_top, x
    sta $0034, y
    lda numbers_bot, x
    sta $0074, y
    dec $1a
+
    lda $004216
    asl
    tax
    cmp $1a
    beq +
    lda numbers_top, x
    sta $0036, y
    lda numbers_bot, x
    sta $0076, y
    dec $1a
+
    iny; iny; iny; iny
    rts

// Loop through stat table and update RAM with numbers representing those stats
write_stats:
    phy
    phb
    php
    pea $dfdf; plb; plb
    rep #$30
    jsl load_stats      // Copy stats back from SRAM
    ldx #$0000
    ldy #$0000

.loop:
    // Get pointer to table
    tya
    asl; asl; asl;
    tax

    // Load stat type
    lda stats+4, x
    beq .end
    cmp #$0001
    beq .number
    cmp #$0002
    beq .time
    cmp #$0003
    beq .fulltime
    jmp .continue

.number:
    // Load statistic
    lda stats, x
    jsl load_stat
    pha

    // Load row address
    lda stats+2, x
    tyx
    tay
    pla
    jsr draw_value
    txy
    jmp .continue

.time:
    // Load statistic
    lda stats, x
    jsl load_stat
    pha

    // Load row address
    lda stats+2, x
    tyx
    tay
    pla
    jsr draw_time
    txy
    jmp .continue

.fulltime:
    lda stats, x        // Get stat id
    asl
    clc
    adc #$fc00          // Get pointer to value instead of actual value
    pha

    // Load row address
    lda stats+2, x
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

// 32-bit by 16-bit division routine I found somewhere
div32:
    phy
    phx
    php
    rep #$30
    sep #$10
    sec
    lda $14
    sbc $12
    bcs uoflo
    ldx #$11
    rep #$10

ushftl:
    rol $16
    dex
    beq umend
    rol $14
    lda #$0000
    rol
    sta $18
    sec
    lda $14
    sbc $12
    tay
    lda $18
    sbc #$0000
    bcc ushftl
    sty $14
    bra ushftl
uoflo:
    lda #$ffff
    sta $16
    sta $14
umend:
    plp
    plx
    ply
    rts

numbers_top:
    dw $0060, $0061, $0062, $0063, $0064, $0065, $0066, $0067, $0068, $0069, $006a, $006b, $006c, $006d, $006e, $006f
numbers_bot:
    dw $0070, $0071, $0072, $0073, $0074, $0075, $0076, $0077, $0078, $0079, $007a, $007b, $007c, $007d, $007e, $007f

load_stats:
    phx
    phy
    lda $7e0952
    clc
    adc #$0010
    sta {last_saveslot}
    jsl save_index
    // X = start of standard stats
    // tries to load from last stats
    jsr is_last_save_flag_ok
    bne .notok
    lda #$0000
    jsl save_index
.notok:
    jsr load_stats_at
    ply
    plx
    rtl

// arg X = index of where to load stats from in bank $70
load_stats_at:
    phx
    phy
    ldy #${_stats_ram}
    // 1 excess byte will be copied but since we restricted
    // stats area size there is still plenty of room, so not a concern
    lda {stats_sram_sz_b}
    phb
    mvn $70,$7f
    plb
    ply
    plx
    rts

// args: X = stats area start in $70
// return zero flag set is flag ok
is_last_save_flag_ok:
    txa
    clc
    adc {last_stats_save_ok_off}
    tax
    lda {last_stats_save_ok_flag}
    cmp $700000,x
    rts

// args: X = stats area start in $70
//       A = value to store
// X and A untouched
set_last_save_ok_flag:
    phx
    pha
    txa
    clc
    adc {last_stats_save_ok_off}
    tax
    pla
    sta $700000,x
    plx
    rts

// arg X = index of where to save stats in bank $70
save_stats_at:
    phx
    phy
    txy
    ldx #${_stats_ram}
    // 1 excess byte will be copied but since we restricted
    // stats area size there is still plenty of room, so not a concern
    lda {stats_sram_sz_b}
    phb
    mvn $7f,$70
    plb
    ply
    plx
    rts

// save stats both in standard and last areas
// arg: A = 0 if we just want to save last stats
save_stats:
    phx
    phy
    pha
    lda $7e0952
    clc
    adc #$0010
    sta {last_saveslot}
    pla
    beq .last   // skip standard start save if A=0
    jsl save_index // A is not 0, so we ask for standard stats index
    jsr save_stats_at
    lda #$0000
.last:
    jsl save_index // A is 0, so we ask for last stats index
    lda #$0000
    jsr set_last_save_ok_flag
    jsr save_stats_at
    lda {last_stats_save_ok_flag}
    jsr set_last_save_ok_flag
    ply
    plx
    rtl

print "stats end : ", org

warnpc $dfd800
// Increment Statistic (in A)
org $dfd800
inc_stat:
    phx
    asl
    tax
    lda {stats_ram}, x
    inc
    sta {stats_ram}, x
    plx
    rtl

warnpc $dfd83f
// Decrement Statistic (in A)
org $dfd840
dec_stat:
    phx
    asl
    tax
    lda {stats_ram}, x
    dec
    sta {stats_ram}, x
    plx
    rtl

warnpc $dfd87f
// Store Statistic (value in A, stat in X)
org $dfd880
store_stat:
    phx
    pha
    txa
    asl
    tax
    pla
    sta {stats_ram}, x
    plx
    rtl

warnpc $dfd8af
// Load Statistic (stat in A, returns value in A)
org $dfd8b0
load_stat:
    phx
    asl
    tax
    lda {stats_ram}, x
    plx
    rtl

warnpc $dfd91a
// New credits script in free space of bank $DF
org $dfd91b
script:
    dw {set}, $0002; -
    dw {draw}, {blank}
    dw {delay}, -

    // Show a compact version of the original credits so we get time to add more
    dw {draw}, {row}*0      // SUPER METROID STAFF
    dw {draw}, {blank}
    dw {draw}, {row}*4      // PRODUCER
    dw {draw}, {blank}
    dw {draw}, {row}*7      // MAKOTO KANOH
    dw {draw}, {row}*8
    dw {draw}, {blank}
    dw {draw}, {row}*9      // DIRECTOR
    dw {draw}, {blank}
    dw {draw}, {row}*10     // YOSHI SAKAMOTO
    dw {draw}, {row}*11
    dw {draw}, {blank}
    dw {draw}, {row}*12     // BACK GROUND DESIGNERS
    dw {draw}, {blank}
    dw {draw}, {row}*13     // HIROFUMI MATSUOKA
    dw {draw}, {row}*14
    dw {draw}, {blank}
    dw {draw}, {row}*15     // MASAHIKO MASHIMO
    dw {draw}, {row}*16
    dw {draw}, {blank}
    dw {draw}, {row}*17     // HIROYUKI KIMURA
    dw {draw}, {row}*18
    dw {draw}, {blank}
    dw {draw}, {row}*19     // OBJECT DESIGNERS
    dw {draw}, {blank}
    dw {draw}, {row}*20     // TOHRU OHSAWA
    dw {draw}, {row}*21
    dw {draw}, {blank}
    dw {draw}, {row}*22     // TOMOYOSHI YAMANE
    dw {draw}, {row}*23
    dw {draw}, {blank}
    dw {draw}, {row}*24     // SAMUS ORIGINAL DESIGNERS
    dw {draw}, {blank}
    dw {draw}, {row}*25     // HIROJI KIYOTAKE
    dw {draw}, {row}*26
    dw {draw}, {blank}
    dw {draw}, {row}*27     // SAMUS DESIGNER
    dw {draw}, {blank}
    dw {draw}, {row}*28     // TOMOMI YAMANE
    dw {draw}, {row}*29
    dw {draw}, {blank}
    dw {draw}, {row}*83     // SOUND PROGRAM
    dw {draw}, {row}*107    // AND SOUND EFFECTS
    dw {draw}, {blank}
    dw {draw}, {row}*84     // KENJI YAMAMOTO
    dw {draw}, {row}*85
    dw {draw}, {blank}
    dw {draw}, {row}*86     // MUSIC COMPOSERS
    dw {draw}, {blank}
    dw {draw}, {row}*84     // KENJI YAMAMOTO
    dw {draw}, {row}*85
    dw {draw}, {blank}
    dw {draw}, {row}*87     // MINAKO HAMANO
    dw {draw}, {row}*88
    dw {draw}, {blank}
    dw {draw}, {row}*30     // PROGRAM DIRECTOR
    dw {draw}, {blank}
    dw {draw}, {row}*31     // KENJI IMAI
    dw {draw}, {row}*64
    dw {draw}, {blank}
    dw {draw}, {row}*65     // SYSTEM COORDINATOR
    dw {draw}, {blank}
    dw {draw}, {row}*66     // KENJI NAKAJIMA
    dw {draw}, {row}*67
    dw {draw}, {blank}
    dw {draw}, {row}*68     // SYSTEM PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*69     // YOSHIKAZU MORI
    dw {draw}, {row}*70
    dw {draw}, {blank}
    dw {draw}, {row}*71     // SAMUS PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*72     // ISAMU KUBOTA
    dw {draw}, {row}*73
    dw {draw}, {blank}
    dw {draw}, {row}*74     // EVENT PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*75     // MUTSURU MATSUMOTO
    dw {draw}, {row}*76
    dw {draw}, {blank}
    dw {draw}, {row}*77     // ENEMY PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*78     // YASUHIKO FUJI
    dw {draw}, {row}*79
    dw {draw}, {blank}
    dw {draw}, {row}*80     // MAP PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*81     // MOTOMU CHIKARAISHI
    dw {draw}, {row}*82
    dw {draw}, {blank}
    dw {draw}, {row}*101    // ASSISTANT PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*102    // KOUICHI ABE
    dw {draw}, {row}*103
    dw {draw}, {blank}
    dw {draw}, {row}*104    // COORDINATORS
    dw {draw}, {blank}
    dw {draw}, {row}*105    // KATSUYA YAMANO
    dw {draw}, {row}*106
    dw {draw}, {blank}
    dw {draw}, {row}*63     // TSUTOMU KANESHIGE
    dw {draw}, {row}*96
    dw {draw}, {blank}
    dw {draw}, {row}*89    // PRINTED ART WORK
    dw {draw}, {blank}
    dw {draw}, {row}*90    // MASAFUMI SAKASHITA
    dw {draw}, {row}*91
    dw {draw}, {blank}
    dw {draw}, {row}*92    // YASUO INOUE
    dw {draw}, {row}*93
    dw {draw}, {blank}
    dw {draw}, {row}*94    // MARY COCOMA
    dw {draw}, {row}*95
    dw {draw}, {blank}
    dw {draw}, {row}*99    // YUSUKE NAKANO
    dw {draw}, {row}*100
    dw {draw}, {blank}
    dw {draw}, {row}*108   // SHINYA SANO
    dw {draw}, {row}*109
    dw {draw}, {blank}
    dw {draw}, {row}*110   // NORIYUKI SATO
    dw {draw}, {row}*111
    dw {draw}, {blank}
    dw {draw}, {row}*32    // SPECIAL THANKS TO
    dw {draw}, {blank}
    dw {draw}, {row}*33    // DAN OWSEN
    dw {draw}, {row}*34
    dw {draw}, {blank}
    dw {draw}, {row}*35    // GEORGE SINFIELD
    dw {draw}, {row}*36
    dw {draw}, {blank}
    dw {draw}, {row}*39    // MASARU OKADA
    dw {draw}, {row}*40
    dw {draw}, {blank}
    dw {draw}, {row}*43    // TAKAHIRO HARADA
    dw {draw}, {row}*44
    dw {draw}, {blank}
    dw {draw}, {row}*47    // KOHTA FUKUI
    dw {draw}, {row}*48
    dw {draw}, {blank}
    dw {draw}, {row}*49    // KEISUKE TERASAKI
    dw {draw}, {row}*50
    dw {draw}, {blank}
    dw {draw}, {row}*51    // MASARU YAMANAKA
    dw {draw}, {row}*52
    dw {draw}, {blank}
    dw {draw}, {row}*53    // HITOSHI YAMAGAMI
    dw {draw}, {row}*54
    dw {draw}, {blank}
    dw {draw}, {row}*57    // NOBUHIRO OZAKI
    dw {draw}, {row}*58
    dw {draw}, {blank}
    dw {draw}, {row}*59    // KENICHI NAKAMURA
    dw {draw}, {row}*60
    dw {draw}, {blank}
    dw {draw}, {row}*61    // TAKEHIKO HOSOKAWA
    dw {draw}, {row}*62
    dw {draw}, {blank}
    dw {draw}, {row}*97    // SATOSHI MATSUMURA
    dw {draw}, {row}*98
    dw {draw}, {blank}
    dw {draw}, {row}*122   // TAKESHI NAGAREDA
    dw {draw}, {row}*123
    dw {draw}, {blank}
    dw {draw}, {row}*124   // MASAHIRO KAWANO
    dw {draw}, {row}*125
    dw {draw}, {blank}
    dw {draw}, {row}*45    // HIRO YAMADA
    dw {draw}, {row}*46
    dw {draw}, {blank}
    dw {draw}, {row}*112   // AND ALL OF R&D1 STAFFS
    dw {draw}, {row}*113
    dw {draw}, {blank}
    dw {draw}, {row}*114   // GENERAL MANAGER
    dw {draw}, {blank}
    dw {draw}, {row}*5     // GUMPEI YOKOI
    dw {draw}, {row}*6
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}

    // Custom item randomizer credits text : max 248 dw {draw} statements
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*128 // VARIA RANDOMIZER STAFF
    dw {draw}, {blank}
    dw {draw}, {row}*129
    dw {draw}, {row}*130
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*131 // ORIGINAL ITEM RANDOMIZERS
    dw {draw}, {blank}
    dw {draw}, {row}*132
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*133 // SNES CODE
    dw {draw}, {blank}
    dw {draw}, {row}*134
    dw {draw}, {blank}
    dw {draw}, {row}*135
    dw {draw}, {blank}
    dw {draw}, {row}*136
    dw {draw}, {blank}
    dw {draw}, {row}*137
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*142 // PALETTE RANDOMIZER
    dw {draw}, {blank}
    dw {draw}, {row}*143
    dw {draw}, {row}*144
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*138 // SPECIAL THANKS TO
    dw {draw}, {blank}
    dw {draw}, {row}*139 // METROID CONSTRUCTION
    dw {draw}, {blank}
    dw {draw}, {row}*140
    dw {draw}, {row}*141
    dw {draw}, {blank}
    dw {draw}, {row}*165 // SUPER METROID DISASSEMBLY
    dw {draw}, {blank}
    dw {draw}, {row}*166
    dw {draw}, {row}*167
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*145 // RANDOMIZER PARAMETERS
    dw {draw}, {blank}
    dw {draw}, {row}*155 // PROG SPEED
    dw {draw}, {blank}
    dw {draw}, {row}*156 // PROG DIFF
    dw {draw}, {blank}
    dw {draw}, {row}*158 // SUITS RESTRICTION
    dw {draw}, {blank}
    dw {draw}, {row}*159 // MORPH PLACEMENT
    dw {draw}, {blank}

    // change scroll speed
    dw {speed}, $0003

    dw {draw}, {row}*160 // SUPER FUN COMBAT
    dw {draw}, {blank}
    dw {draw}, {row}*161 // SUPER FUN MOVEMENT
    dw {draw}, {blank}
    dw {draw}, {row}*162 // SUPER FUN SUITS
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*157 // ITEMS DISTRIBUTION
    dw {draw}, {blank}
    dw {draw}, {row}*168 // AVAILABLE
    dw {draw}, {row}*169
    dw {draw}, {blank}
    dw {draw}, {row}*152 // ENERGY
    dw {draw}, {row}*153
    dw {draw}, {blank}
    dw {draw}, {row}*146 // MISSILES
    dw {draw}, {row}*147
    dw {draw}, {blank}
    dw {draw}, {row}*148 // SUPERS
    dw {draw}, {row}*149
    dw {draw}, {blank}
    dw {draw}, {row}*150 // PBs
    dw {draw}, {row}*151
    dw {draw}, {blank}
    dw {draw}, {row}*163 // AMMO DISTRIBUTION
    dw {draw}, {row}*164
    dw {draw}, {blank}

    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*223 // PLAY THIS RANDOMIZER AT
    dw {draw}, {blank}
    dw {draw}, {row}*179
    dw {draw}, {row}*180
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*181
    dw {draw}, {blank}
    dw {draw}, {row}*182
    dw {draw}, {blank}
    dw {draw}, {blank}

    dw {draw}, {row}*183 // GAMEPLAY STATS
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*184 // SPEEDRUNNING STATS
    dw {draw}, {blank}

    // Set scroll speed to 3 frames per pixel
//    dw {speed}, $0003
    dw {draw}, {row}*185 // DOOR TRANSITIONS
    dw {draw}, {row}*186
    dw {draw}, {blank}
    dw {draw}, {row}*187 // TIME IN DOORS
    dw {draw}, {row}*188
    dw {draw}, {blank}
    dw {draw}, {row}*189 // TIME ADJUSTING DOOR
    dw {draw}, {row}*190
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*191 // TIME SPENT
    dw {draw}, {blank}
    dw {draw}, {row}*192 // CRATERIA
    dw {draw}, {row}*193
    dw {draw}, {blank}
    dw {draw}, {row}*194 // BRINSTAR
    dw {draw}, {row}*195
    dw {draw}, {blank}
    dw {draw}, {row}*196 // NORFAIR
    dw {draw}, {row}*197
    dw {draw}, {blank}
    dw {draw}, {row}*198 // WS
    dw {draw}, {row}*199
    dw {draw}, {blank}
    dw {draw}, {row}*200 // MARIDIA
    dw {draw}, {row}*201
    dw {draw}, {blank}
    dw {draw}, {row}*202 // TOURIAN
    dw {draw}, {row}*203
    dw {draw}, {blank}
    dw {draw}, {row}*221 // PAUSE MENU
    dw {draw}, {row}*222
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*204 // SHOTS AND AMMO
    dw {draw}, {blank}
    dw {draw}, {row}*170 // UNCHARGED
    dw {draw}, {row}*171
    dw {draw}, {blank}
    dw {draw}, {row}*205 // CHARGED
    dw {draw}, {row}*206
    dw {draw}, {blank}
    dw {draw}, {row}*207 // SBA
    dw {draw}, {row}*208
    dw {draw}, {blank}
    dw {draw}, {row}*209 // MISSILES
    dw {draw}, {row}*210
    dw {draw}, {blank}
    dw {draw}, {row}*211 // SUPERS
    dw {draw}, {row}*212
    dw {draw}, {blank}
    dw {draw}, {row}*213 // PBs
    dw {draw}, {row}*214
    dw {draw}, {blank}
    dw {draw}, {row}*215 // BOMBS
    dw {draw}, {row}*216


    // Draw item locations
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*640
    dw {draw}, {blank}
    dw {draw}, {blank}

    dw {draw}, {row}*641
    dw {draw}, {row}*642
    dw {draw}, {blank}
    dw {draw}, {row}*643
    dw {draw}, {row}*644
    dw {draw}, {blank}
    dw {draw}, {row}*645
    dw {draw}, {row}*646
    dw {draw}, {blank}
    dw {draw}, {row}*647
    dw {draw}, {row}*648
    dw {draw}, {blank}
    dw {draw}, {row}*649
    dw {draw}, {row}*650
    dw {draw}, {blank}
    dw {draw}, {row}*651
    dw {draw}, {row}*652
    dw {draw}, {blank}
    dw {draw}, {row}*653
    dw {draw}, {row}*654
    dw {draw}, {blank}
    dw {draw}, {row}*655
    dw {draw}, {row}*656
    dw {draw}, {blank}
    dw {draw}, {row}*657
    dw {draw}, {row}*658
    dw {draw}, {blank}
    dw {draw}, {row}*659
    dw {draw}, {row}*660
    dw {draw}, {blank}
    dw {draw}, {row}*661
    dw {draw}, {row}*662
    dw {draw}, {blank}
    dw {draw}, {row}*663
    dw {draw}, {row}*664
    dw {draw}, {blank}
    dw {draw}, {row}*665
    dw {draw}, {row}*666
    dw {draw}, {blank}
    dw {draw}, {row}*667
    dw {draw}, {row}*668
    dw {draw}, {blank}
    dw {draw}, {row}*669
    dw {draw}, {row}*670
    dw {draw}, {blank}
    dw {draw}, {row}*671
    dw {draw}, {row}*672
    dw {draw}, {blank}
    dw {draw}, {row}*673
    dw {draw}, {row}*674
    dw {draw}, {blank}
    dw {draw}, {row}*675
    dw {draw}, {row}*676
    dw {draw}, {blank}
    dw {draw}, {row}*677
    dw {draw}, {row}*678
    dw {draw}, {blank}

    // Last info
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*217 // Final Time
    dw {draw}, {row}*218
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*219 // Thanks
    dw {draw}, {row}*220
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}

    // Set scroll speed to 4 frames per pixel
    dw {speed}, $0004

    // Scroll all text off and end credits
    dw {set}, $0017; -
    dw {draw}, {blank}
    dw {delay}, -
    dw {end}

stats:
    // STAT ID, ADDRESS,    TYPE (1 = Number, 2 = Time, 3 = Full time), UNUSED
    dw 0,       {row}*217,  3, 0    // Full RTA Time
    dw 2,       {row}*185,  1, 0    // Door transitions
    dw 3,       {row}*187,  3, 0    // Time in doors
    dw 5,       {row}*189,  2, 0    // Time adjusting doors
    dw 7,       {row}*192,  3, 0    // Crateria
    dw 9,       {row}*194,  3, 0    // Brinstar
    dw 11,      {row}*196,  3, 0    // Norfair
    dw 13,      {row}*198,  3, 0    // Wrecked Ship
    dw 15,      {row}*200,  3, 0    // Maridia
    dw 17,      {row}*202,  3, 0    // Tourian
    dw 19,      {row}*170,  1, 0    // Uncharged Shots
    dw 20,      {row}*205,  1, 0    // Charged Shots
    dw 21,      {row}*207,  1, 0    // Special Beam Attacks
    dw 22,      {row}*209,  1, 0    // Missiles
    dw 23,      {row}*211,  1, 0    // Super Missiles
    dw 24,      {row}*213,  1, 0    // Power Bombs
    dw 26,      {row}*215,  1, 0    // Bombs
    dw 27,      {row}*221,  3, 0    // Time in pause
//  dw 29,      {row}*224,  2, 0    // time saved arm pumping
    dw 0,               0,  0, 0    // end of table

print "credits end : ", org

warnpc $dfffff

// Relocated credits tilemap to free space in bank CE
org $ceb240
credits:
    // When using big text, it has to be repeated twice, first in UPPERCASE and then in lowercase since it's split into two parts
    // Numbers are mapped in a special way as described below:
    // 0123456789%& '´
    // }!@#$%&/()>~.

    // This is not exactly in display order
    {pink}
    dw "     VARIA RANDOMIZER STAFF     " // 128
    {big}
    dw "          DUDE AND FLO          " // 129
    dw "          dude and flo          " // 130
    {purple}
    dw "    ORIGINAL ITEM RANDOMIZERS   " // 131
    {yellow}
    dw "       TOTAL   DESSYREQT        " // 132
    {purple}
    dw "            SNES CODE           " // 133
    {yellow}
    dw "   TOTAL      FOOSDA      FLO   " // 134
    dw "   DARKSHOCK   RAKKI   SCYZER   " // 135
    dw "   KEJARDON   SMILEY   LIORAN   " // 136
    dw "      PERSONITIS    LEODOX      " // 137
    {cyan}
    dw "       SPECIAL THANKS TO        " // 138
    {yellow}
    dw "      METROID CONSTRUCTION      " // 139
    {big}
    dw "     METROIDCONSTRUCTION COM    " // 140
    dw "     metroidconstruction.com    " // 141
    {purple}
    dw "       PALETTE RANDOMIZER       " // 142
    {big}
    dw "             RAND 0             " // 143
    dw "             rand }             " // 144
    {purple}
    // params title
    dw "     RANDOMIZER PARAMETERS      " // 145
    {big}
    // item distribution data start
    dw " MISSILE PACKS               XX " // 146
    dw " missile packs ............. xx " // 147
    dw " SUPER PACKS                 XX " // 148
    dw " super packs ............... xx " // 149
    dw " POWER BOMB PACKS            XX " // 150
    dw " power bomb packs .......... xx " // 151
    dw " HEALTH TANKS                XX " // 152
    dw " health tanks .............. xx " // 153
    dw "                                " // 154  : reusable
    // params data start
    {yellow}
    dw " PROGRESSION SPEED .... XXXXXXX " // 155
    dw " PROGRESSION DIFFICULTY XXXXXXX " // 156
    // item distrib title
    {purple}
    dw "       ITEMS DISTRIBUTION       " // 157
    // params data end
    {yellow}
    dw " SUITS RESTRICTION ........ XXX " // 158
    dw " MORPH PLACEMENT ....... XXXXXX " // 159
    dw " SUPER FUN COMBAT ......... XXX " // 160
    dw " SUPER FUN MOVEMENT ....... XXX " // 161
    dw " SUPER FUN SUITS .......... XXX " // 162
    // item distrib data end
    {big}
    dw " AMMO DISTRIBUTION  X X X X X X " // 163
    dw " ammo distribution  x.x x.x x.x " // 164
    // credits continued
    {yellow}
    dw "   SUPER METROID DISASSEMBLY    " // 165
    {big}
    dw "     PJBOY        KEJARDON      " // 166
    dw "     pjboy        kejardon      " // 167
// stats continued
    dw " AVAILABLE AMMO XXX% ENERGY XXX%" // 168
    dw " available ammo xxx> energy xxx>" // 169
    dw " UNCHARGED SHOTS                " // 170
    dw " uncharged shots                " // 171
// --- this space is reusable
    dw "                                " // 172
    dw "                                " // 173
    dw "                                " // 174
    dw "                                " // 175
    dw "                                " // 176
    dw "                                " // 177
    dw "                                " // 178
// End of reusable space
    {big}
    dw "            VARIA RUN           " // 179
    dw "            varia.run           " // 180
    {orange}
    dw "         BETA.VARIA.RUN         " // 181
    dw "        DISCORD.VARIA.RUN       " // 182
    {purple}
    dw "      GAMEPLAY STATISTICS       " // 183
    {blue}
    dw "      SPEEDRUNNING STATS        " // 184
    {big}
    dw " DOOR TRANSITIONS               " // 185
    dw " door transitions               " // 186
    dw " TIME IN DOORS      00'00'00^00 " // 187
    dw " time in doors                  " // 188
    dw " TIME ALIGNING DOORS   00'00^00 " // 189
    dw " time aligning doors            " // 190
    {blue}
    dw "         TIME SPENT IN          " // 191
    {big}
    dw " CRATERIA           00'00'00^00 " // 192
    dw " crateria                       " // 193
    dw " BRINSTAR           00'00'00^00 " // 194
    dw " brinstar                       " // 195
    dw " NORFAIR            00'00'00^00 " // 196
    dw " norfair                        " // 197
    dw " WRECKED SHIP       00'00'00^00 " // 198
    dw " wrecked ship                   " // 199
    dw " MARIDIA            00'00'00^00 " // 200
    dw " maridia                        " // 201
    dw " TOURIAN            00'00'00^00 " // 202
    dw " tourian                        " // 203
    {green}
    dw "      SHOTS AND AMMO FIRED      " // 204
    {big}
    dw " CHARGED SHOTS                  " // 205
    dw " charged shots                  " // 206
    dw " SPECIAL BEAM ATTACKS           " // 207
    dw " special beam attacks           " // 208
    dw " MISSILES                       " // 209
    dw " missiles                       " // 210
    dw " SUPER MISSILES                 " // 211
    dw " super missiles                 " // 212
    dw " POWER BOMBS                    " // 213
    dw " power bombs                    " // 214
    dw " BOMBS                          " // 215
    dw " bombs                          " // 216
    dw " FINAL TIME         00'00'00^00 " // 217
    dw " final time                     " // 218
    dw "       THANKS FOR PLAYING       " // 219
    dw "       thanks for playing       " // 220
    dw " PAUSE MENU         00'00'00^00 " // 221
    dw " pause menu                     " // 222
    {cyan}
    dw "     PLAY THIS RANDOMIZER AT    " // 223
    {big}
    //dw " ARM PUMPING GAIN      00'00^00 " // 224
    //dw " arm pumping gain               " // 225
    dw $0000                              // End of credits tilemap

warnpc $ceffff

// Placeholder label for item locations inserted by the randomizer
org $ded200
itemlocations:
    {pink}
    dw "         ITEM LOCATIONS         " // 640
