arch 65816
lorom

;;; patch pit and climb room states
org $8fe652
;;; pit room: in vanilla, checks for morph+missiles collection
morph_missile_check:
    ;; check that zebes is awake instead: works with both standard
    ;; start wake zebes door asm, and non standard start with wake
    ;; zebes forced from the start.
    lda #$0000 : jsl $808233
    bcc .not_awake
    bra .awake
org $8fe65f
.awake:
org $8fe666
.not_awake:

;;; Enemies gray doors set zebes awake when unlocking.
;;; Disable that, as the event is set in blue brin by
;;; wake zebes door asm (or right away if random start),
;;; and we don't want it to be set if we encounter
;;; Climb flashing portal door (enemy door set at 0)
org $84BE0B
skip_wake_zebes:
	bra .skip
org $84BE12
.skip:

;;; Door ASM pointer (Door into small corridor before construction zone)
org $838eb4
    dw wake_zebes

;;; Door ASM to force Zebes awake event.
;;; With the new nothing item plm we can really have no item collected at morph ball location,
;;; so always wake zebes when we traverse the door.
org $8fff00
wake_zebes:
    lda $7ed820                 ; load Event bit array.
    ora.w #$0001                ; 1:   Event 0 - Zebes is awake
    sta $7ed820                 ; update RAM
    rts
