;;; Changes how the end percentage in calculated. Original patch by Sadiztyk Fish.
;;; Display item percent in inventory pause menu
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)
;;; or a variant of xkas that supports arch directive

lorom
arch 65816

incsrc "sym/endingtotals.asm"

org $828F6B
        JSR display_item_count_menu

; Free space at end of bank 82 (0x40 bytes)
org $82FFBF
display_item_count_menu:
        jsl endingtotals_compute_percent
        jsr display_menu
        JSR $8F70               ;//vanilla
        rts

display_menu:
        phx
        LDX #$0000
        LDA #$0C4A              ; decimal icon
        STA $7E39CE
        LDA #$0C02              ; percent icon
        STA $7E39D2
        LDA $12 : JSR draw_digit_menu
        LDA $14 : JSR draw_digit_menu
        LDA $16 : JSR draw_digit_menu
        INX : INX
        LDA $18 : JSR draw_digit_menu
        plx
        rts

draw_digit_menu:
        CLC : ADC #$0804
        STA $7E39C8,x
        INX : INX
        rts

print "End of items percent: ", pc
warnpc $82ffff

;;; ['items' box] in inventory menu
org $B6E980
        dw $0000,$1D5C,$3941,$3942,$3943,$0C1C,$0C1D,$0C1E,$7943,$3942,$3942,$7941
org $B6E9C0
        dw $0000,$1D5C,$3940,$2801,$2801,$2801,$2801,$2801,$2801,$2801,$2801,$7940
org $B6EA00
        dw $0000,$1D5C,$B941,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$B942,$F941

;;; new tiles for 'items' text
org $b68380
        db $77,$0,$22,$0,$22,$0,$22,$0,$22,$0,$72,$0,$0,$0,$0,$0,$ff,$77,$ff,$22,$ff,$22,$ff,$22,$ff,$22,$ff,$72,$ff,$0,$ff,$0
org $b683a0
        db $7a,$0,$43,$0,$73,$0,$42,$0,$42,$0,$7a,$0,$0,$0,$0,$0,$ff,$7a,$ff,$43,$ff,$73,$ff,$42,$ff,$42,$ff,$7a,$ff,$0,$ff,$0
org $b683c0
        db $27,$0,$68,$0,$ef,$0,$a1,$0,$21,$0,$2e,$0,$0,$0,$0,$0,$ff,$27,$ff,$68,$ff,$ef,$ff,$a1,$ff,$21,$ff,$2e,$ff,$0,$ff,$0




