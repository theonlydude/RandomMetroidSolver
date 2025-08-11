;;; Dread mode : one-hit KO from everything
;;; - forces starting and max health to 01
;;; - removes low health beep
;;; - disables rainbow beam damage

lorom
arch 65816

;;; set Samus health/max health to 01
org $81B2CD
health_init:
    lda.w #1

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
