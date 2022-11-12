;;; door asm of bt/animal room during escape
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)


arch 65816
lorom

incsrc "sym/tracking.asm"
incsrc "sym/credits_varia.asm"

org $838BCC
    db $20, $ff

!timer1 = $05b8
!timer2 = $05ba
!stats_timer = $7ffc00

org $8FFF20
gameend:
        LDA $7ED820 ; loads event flags
        BIT #$4000  ; checks for escape flag set
        BEQ .quit
        LDA #$0026
        STA $7E0998 ; stores gamestate as game end trigger

        ;; update region time
        jsl tracking_update_and_store_region_time
        ;; save timer in stats
        lda !timer1
        sta !stats_timer
        lda !timer2
        sta !stats_timer+2

        ;; save stats to SRAM
        lda #$0001
        jsl credits_varia_save_stats
.quit:
        RTS
