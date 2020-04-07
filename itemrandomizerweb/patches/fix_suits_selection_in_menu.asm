;;; In inventory menu, when having only a beam and a suit you have to press right+up to go from beam to suit,
;;; it's not natural, so fix it to only require right.
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

org $82B000
        ;; test of return of $B4B7 compare A and #$0000, when no item found A==#$ffff, which set the carry
        ;; so when carry is clear it means that an item was found in misc.
        ;; if no item was found in misc, we check in boots then in suits, so if an item is found in both
        ;; boots and suits, as suits is tested last the selection will be set on suits.
        bcc $64
