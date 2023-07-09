;;; Display item percent in inventory pause menu, uses endingtotals by Scyzer for that
;;; Also displays RTA timer in the inventory menu
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)


lorom
arch 65816

incsrc "sym/base.asm"
incsrc "sym/endingtotals.asm"

incsrc "macros.asm"
incsrc "constants.asm"

!BG1_tilemap = $7E3800
!decimal_point = $0C4A
%BGtile($150, 2, 0, 0, 0)
!percent #= !_tile
%BGtile($160, 2, 0, 0, 0)
!digit_0 #= !_tile

!semicolon = $08A3

;; skip load of base tilemap when loading pause menu, do it when switching to equipment screen only.
;; this enables reusing the RAM tilemap for other purposes in other map screens
org $828F1D
load_eqt_screen_base_tilemap:
        bra .skip
.hijack_end:
        ;; completely skip useless dummy samus wireframe tilemap copy to the wrong place to make some free space
org $828F6E
.skip:

;;; hijack load equipment screen to load base tilemap there
org $8291B1
        jsr load_eqt_screen_base_tilemap_rewrite

;;; reuse free space above to load equipment screen base tilemap
org load_eqt_screen_base_tilemap_hijack_end
load_eqt_screen_base_tilemap_rewrite:
        ;; load base tilemap
        %loadRamDMA($B6E800, $7E3800, $800)
        JSR $B20C       ; Write Samus wireframe tilemap
        JSR $8F70       ; Load equipment screen reserve health tilemap
        jsr $A12B       ; refresh equipment tilemap
        ;; write items and time as soon as the tilemap is setup to avoid weird effect when fading in
        jsr display_item_count_menu
        jsr display_RTA_time
        JSR $AB47               ; hijacked code
        rts

warnpc load_eqt_screen_base_tilemap_skip


org $8290F6
        jsr display_time : nop

; Free space at end of bank 82 after objectives
org $82FEC0
display_time:
        JSL $809B44             ; vanilla code
        jsr display_RTA_time_frame
        rts

display_item_count_menu:
        jsl endingtotals_compute_percent
        jsr display_percent
        rts

display_RTA_time_frame:
        lda !pause_index
        cmp !pause_index_equipment_screen : beq .time
        cmp !pause_index_map2equip_load_equip : beq .time
        cmp !pause_index_map2equip_fading_in : beq .time
        bra .end
.time:
        jsr display_RTA_time
.end:
        rts

display_RTA_time:
        phx
        lda !timer1 : sta !stats_timer
        lda !timer2 : sta !stats_timer+2
        jsl base_update_igt
        %ldx_tileOffset(21, 7)
        ;; don't display leading 0s for hours
        lda !igt_hours : cmp.w #10 : bmi .sub10
        jsr draw_two_digits
        bra .minutes
.sub10:
        inx : inx
        jsr draw_digit_menu
.minutes:
        inx : inx
        lda #!semicolon : sta !BG1_tilemap, x
        inx : inx
        lda !igt_minutes : jsr draw_two_digits
        inx : inx
        lda #!semicolon : sta !BG1_tilemap, x
        inx : inx
        lda !igt_seconds : jsr draw_two_digits
.end:
        plx
        rts

display_percent:
        phx
        LDX #$0000
        %tileOffset(7, 7)
        LDA #!decimal_point : STA !BG1_tilemap+!_tile_offset
        %tileOffset(9, 7)
        LDA #!percent : STA !BG1_tilemap+!_tile_offset
        ;; don't draw leading 0s for hundreds and tenths
.hundred:
        %ldx_tileOffset(4, 7)
        LDA $12 : beq .tenth
        JSR draw_digit_menu
.tenth:
        inx : inx
        LDA $14 : bne .draw
        ;; don't draw tenth 0 if < 100%
        lda $12 : beq .units
        lda $14
.draw:
        JSR draw_digit_menu
.units:
        inx : inx
        LDA $16 : JSR draw_digit_menu
        %ldx_tileOffset(8, 7)
        LDA $18 : JSR draw_digit_menu
        plx
        rts

draw_two_digits:
        sta $4204
        %a8()
        lda.b #10
        sta $4206
        pha : pla :  pha : pla
        %a16()
        lda $4214
        jsr draw_digit_menu
        inx : inx
        lda $4216
        jsr draw_digit_menu
        rts

draw_digit_menu:
        CLC : ADC #!digit_0
        STA !BG1_tilemap,x
        rts

print "End of items percent: ", pc
warnpc $82ffff

;;; needed additional tiles are in pause screen gfx included by map patch

;;; BG1 tilemap alterations for equipment screen

;;; ['items' box] in inventory menu
org $B6E980+4
        dw $3941,$3942,$3943
        %dw_BGtile($151, 3, 0, 0, 0)
        %dw_BGtile($152, 3, 0, 0, 0)
        %dw_BGtile($153, 3, 0, 0, 0)
        dw $7943,$3942,$3942,$7941
org $B6E9C0+4
        dw $3940,$2801,$2801,$2801,$2801,$2801,$2801,$2801,$2801,$7940
org $B6EA00+4
        dw $B941,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$F941

;;; ['time' box] in inventory menu (TIME tiles already exist oO, put back in the original spot in map patch)
org $B6E980+40
        dw $3941,$3942,$3942,$3943,$0C93,$0C94,$0CA4,$7943,$3942,$3942,$7941
org $B6E9C0+40
        dw $3940,$2801,$2801,$2801,$2801,$2801,$2801,$2801,$2801,$2801,$7940
org $B6EA00+40
        dw $B941,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$F941

;;; redraw reserve arrow since tile indices are changed in map patch
org $B6E902
        %dw_BGtile($14a, 7, 1, 0, 0)
org $B6E942
        %dw_BGtile($15a, 7, 1, 0, 0)
org $B6E982
        %dw_BGtile($15a, 7, 0, 0, 0)
org $B6E9C2
        %dw_BGtile($15a, 7, 0, 0, 0)
org $B6EA02
        %dw_BGtile($15a, 7, 0, 0, 0)
org $B6EA42
        %dw_BGtile($15a, 7, 0, 0, 0)
org $B6EA82
        %dw_BGtile($15a, 7, 0, 0, 0)
org $B6EAC2
        %dw_BGtile($15a, 7, 0, 0, 0)
org $B6EB02
        %dw_BGtile($16a, 7, 0, 0, 0)
        %dw_BGtile($16b, 7, 1, 0, 0)

;;; move equipment boxes on the right down one tile
org $B6EA68
        dw $3941,$3942,$3942,$3943,$28F6,$28F7,$28F8,$7943,$3942,$3942,$7941
org $B6EAA8
        dw $7954,$0CFF,$0D00,$0D01,$0D02,$0D03,$0D04,$0D05,$0CD4,$0CD4,$7940
org $B6EAE8
        dw $3940,$0CFF,$0CD0,$0CD1,$0CD2,$0CD3,$0D03,$0D04,$0D05,$0CD4,$7940
org $B6EB28
        dw $B941,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$F941
org $B6EB68
        dw $3941,$3942,$3942,$3943,$29B0,$29B1,$29B2,$7943,$3942,$3942,$7941
org $B6EBA8
        dw $7954,$08FF,$0920,$0921,$0922,$0923,$0917,$0918,$090F,$091F,$7940
org $B6EBE8
        dw $3940,$08FF,$08D5,$08D6,$08D7,$08D4,$08D4,$08D4,$08D4,$08D4,$7940
org $B6EC28
        dw $3940,$08FF,$0910,$0911,$0912,$0913,$0914,$0915,$0916,$08D4,$7940
org $B6EC68
        dw $3940,$08FF,$08E0,$08E1,$08E2,$08E3,$08E4,$08E5,$08E6,$08D4,$7940
org $B6ECA8
        dw $B941,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$F941
org $B6ECE8
        dw $3941,$3942,$3942,$3943,$2CA0,$2CA1,$2CA2,$7943,$3942,$3942,$7941
org $B6ED28
        dw $3940,$0CFF,$0D30,$0D31,$0D32,$0D33,$0D34,$0D35,$0D36,$0CD4,$7940
org $B6ED68
        dw $F954,$0CFF,$0CF0,$0CF1,$0CF2,$0CF3,$0CF4,$0CF5,$0CD4,$0CD4,$7940
org $B6EDA8
        dw $3940,$0CFF,$0D24,$0D25,$0D26,$0D27,$0D28,$0D29,$0D2A,$0D2B,$7940
org $B6EDE8
        dw $B941,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$F941

;;; fix reserve digit tile IDs
org $828fb7
        %dw_BGtile($160, 2, 0, 0, 0)
org $828fc2
        %dw_BGtile($160, 2, 0, 0, 0)
org $828fcc
        %dw_BGtile($160, 2, 0, 0, 0)
org $82b3bc
        %dw_BGtile($160, 2, 0, 0, 0)
org $82b3c7
        %dw_BGtile($160, 2, 0, 0, 0)
org $82b3d1
        %dw_BGtile($160, 2, 0, 0, 0)

;;; fix RAM tilemap offsets for equipment we moved
org $82C076
        dw $3AAA ; Suit/misc - varia suit
        dw $3AEA ; Suit/misc - gravity suit
        dw $3BAA ; Suit/misc - morph ball
        dw $3BEA ; Suit/misc - bombs
        dw $3C2A ; Suit/misc - spring ball
        dw $3C6A  ; Suit/misc - screw attack
org $82C082
        dw $3D2A ; Boots - hi-jump boots
        dw $3D6A ; Boots - space jump
        dw $3DAA  ; Boots - speed booster

;;; fix equipment selector positions
org $82C1B2
        dw $00CC,$004C+8 ; Suit/misc - varia suit
        dw $00CC,$0054+8 ; Suit/misc - gravity suit
        dw $00CC,$006C+8 ; Suit/misc - morph ball
        dw $00CC,$0074+8 ; Suit/misc - bombs
        dw $00CC,$007C+8 ; Suit/misc - spring ball
        dw $00CC,$0084+8 ; Suit/misc - screw attack
org $82C1CA
        dw $00CC,$009C+8 ; Boots - hi-jump boots
        dw $00CC,$00A4+8 ; Boots - space jump
        dw $00CC,$00AC+8 ; Boots - speed booster
