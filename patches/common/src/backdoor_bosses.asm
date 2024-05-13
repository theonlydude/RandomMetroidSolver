arch 65816
lorom

;; from map rando

;; In Crocomire's initialization, skip setting the leftmost screens to red scroll. Even in the vanilla game there
;; is no purpose to this, as they are already red. But it important to skip here in the rando, because when entering
;; from the left door with Crocomire still alive, these scrolls are set to blue by the door ASM, and if they
;; were overridden with red it would break the graphics.
org $A48A92
croc_backdoor:
        bra .skip
org $A48A96
.skip:

;; Release Spore Spawn camera so it won't be glitched when entering from the right:
org $A5EADA
spospo_backdoor:
        bra .skip
org $A5EADD
.skip:

;; Likewise release Kraid camera so it won't be as glitched when entering from the right:
org $A7A9F4
kraid_backdoor:
        bra .skip
org $A7A9F8
.skip:
