;;; door asm of bt/animal room during escape
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

arch snes.cpu
lorom

org $838BCC
    db $20, $ff

!update_and_store_region_time = $A1EC00
!timer1 = $05b8
!timer2 = $05ba
!stats_timer = $7ffc00
!save_stats = $dfd7bf

org $8FFF20
gameend:
        LDA $7ED820 ; loads event flags
        BIT #$4000  ; checks for escape flag set
        BEQ .quit
        LDA #$0026
        STA $7E0998 ; stores gamestate as game end trigger

        ;; update region time
        jsl !update_and_store_region_time
        ;; save timer in stats
        lda !timer1
        sta !stats_timer
        lda !timer2
        sta !stats_timer+2

        ;; save stats to SRAM
        lda #$0001
        jsl !save_stats

.quit
        RTS
