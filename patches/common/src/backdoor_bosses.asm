;; from map rando (patch.rs), adapted for VARIA
;; to include when miniboss randomization is active

arch 65816
lorom

incsrc "sym/door_transition.asm" ; will be active as well in miniboss rando

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

;;; In Kraid's room, no longer restrict Samus X position to left screen:
org $A7C9EE
        rts

;;; exiting kraid room to the right is not handled by transitions exit
;;; asm because it is not an area/boss transition, add it as door asm
org $8391da+10
        dw door_transition_kraid_exit_fix

;;; likewise, add draygon exit fix for door to space jump room
org $83a978+10
        dw door_transition_boss_exit_fix

;;; and for crocomire back door
org $8393de+10
        dw door_transition_boss_exit_fix
