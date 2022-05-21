;;; Patches to apply when specific tracks are customized, disable certain sound effects that rely on vanilla music.
;;; 
;;; compile with asar
;;; 
;;; Define desired vanilla song(s) on the command line with -D

arch snes.cpu
lorom


if defined("Upper_Norfair")
;;; disables lava sounds to avoid weird noises in Norfair
org $88B446
    rep 4 : nop
endif


if defined("Red_Brinstar")
;;; TODO tube opening (mid prio)
endif


if defined("Lower_Norfair")
;;; TODO desgeegas, namihe flames (low prio)
endif


if defined("East_Maridia")
;;; TODO mochtroids (mid prio)
endif


if defined("Tourian_Bubbles")
;;; disables MB2 "no music" before fight (special music data), as cutscene is sped up in VARIA seeds
org $A98810
	rep 4 : nop
;;; TODO MB1 glass and hurt sound (mid prio)
endif


org $A99B0F
mb_goto:
if defined("Mother_Brain_2")
;;; patch instruction lists to skip sound effects
org $A99B91
mb2_cry:	
	dw mb_goto,.skip1
.skip1:
org $A99D47
	dw mb_goto,.skip5
.skip5:	
org $A99DFF
	bra .skip7
org $A99E0D
.skip7:
org $A99EE2
	dw mb_goto,.skip8
.skip8:
;; FIXME missing cry after 1st rainbow, cry during baby drain and refill

baby_cry:
org $A9C7BB
	bra .skip_cry
org $A9C7CB
.skip_cry:
org $A9CB13
	bra .release_skip_cry
org $A9CB1A
.release_skip_cry:
org $A9F75D
	bra .drain_skip_cry
org $A9F786
.drain_skip_cry:

endif


if defined("Mother_Brain_3")

org $A99BC5
mb3_cry:
	dw mb_goto,.skip2
.skip2:
org $A99BF7
	dw mb_goto,.skip3
.skip3:
org $A99C43
	dw mb_goto,.skip4
.skip4:
org $A99F16
	dw mb_goto,.skip9
.skip9:

endif


if defined("Wrecked_Ship_-_Power_on")
;;; TODO walking robots (low prio)
endif


if defined("Boss_fight_-_Ridley")
;;; TODO Ridley cries (hi prio)
endif


if defined("Boss_fight_-_Kraid")
;;; TODO Kraid cries (especially death, hi prio)
endif


if defined("Boss_fight_-_Phantoon")
;;; TODO Phantoon cries (hi prio)
endif


if defined("Boss_fight_-_Crocomire")
;;; TODO croc cries (especially death, hi prio)
endif


if defined("Boss_fight_-_Spore_Spawn")
;;; TODO spospo opening sounds (hi prio)
endif
