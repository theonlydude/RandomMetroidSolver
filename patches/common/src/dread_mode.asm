;;; Dread mode : one-hit KO from everything
;;; - removes low health beep
;;; - disables rainbow beam damage
;;; - tweak drop system to prevent systematic health drops
;;;
;;; Additional setup needed :
;;; - set starting energy to 1 in start
;;; - remove all health tanks from seed

lorom
arch 65816

;;; disable low health beep
org $90EA7F
low_health_check:
    rts
org $90F331
    bra +
org $90F340
+
org $91E6CF
    bra +
org $91E6DE
+

;;; disables rainbow beam damage
org $A9BA2D
rainbow_loop_count:
    lda.w #1
org $A9C57D
rainbow_drain:
    clc
    rtl

;;; disables low health drop chance (only energy)
org $86F151
    STZ $0E1A                   ; replace STY with STZ to zero out health drop bias flag
