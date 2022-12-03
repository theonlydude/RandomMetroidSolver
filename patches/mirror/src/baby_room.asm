;;; change baby init AI to allow you to come back in his room
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

org $A9EF6F
        ;; original check is awfully weird: it loads the 'active baby' AI pointer ($EFE6, which is now in A),
        ;; and AND it (using BIT to preserve value), with layer 1 X position, and it will actually set it as AI
        ;; if the result is positive. This works in vanilla, as layer 1 X is FF70 when coming from the left.
        ;; We change the check to a one against explored map tiles. 
        ;; Side effect, the baby won't ever load if you have seen it once
        bit $08B9               ; this is 0 when entering from the left, otherwise the value works when AND with $EFE6
        beq $0C
