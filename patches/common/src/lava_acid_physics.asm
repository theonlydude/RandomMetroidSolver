lorom

;;; changes air physics to lava/acid physics

;;; re-route function pointers to end of lava/acid physics routine, except water
org $908e26
	dw set_lava_acid_physics ; air
	dw set_lava_acid_physics ; lava
	dw set_lava_acid_physics ; acid
	skip 2			 ; water
	dw set_lava_acid_physics ; spores
	dw set_lava_acid_physics ; rain
	dw set_lava_acid_physics ; fog
	dw set_lava_acid_physics ; ?

org $908e43
set_lava_acid_physics:

;; tweak water physics function to change "air physics" cases to "lava/acid physics"
org $908e4d
	bmi set_lava_acid_physics
org $908e53
	bra set_lava_acid_physics
org $908e5b
	bne set_lava_acid_physics


;;; change animate samus ptr table for FX
org $908067
	dw samus_submerged_lava_acid ; FX=None
	skip 6			     ; keep lava/acid/water ptrs vanilla
	dw samus_submerged_lava_acid ; spores
	dw samus_submerged_lava_acid ; rain
	dw samus_submerged_lava_acid ; fog
	dw samus_submerged_lava_acid ; ?

;; "Samus is submerged in lava/acid"
org $90824c
samus_submerged_lava_acid:
org $90825D
	;; disable graphic effects to avoid them spawning all the time
	;; when tere is actually lava/acid
	bra .fully_submerged
org $9082C3
.fully_submerged:

;;; tweak animate samus FX-dependent functions to change "air physics without gravity" cases to "lava/acid physics"

;; lava FX 
org $90820C
	jmp samus_submerged_lava_acid

;; reuse 3 bytes in now unused normal function to work around branching distance 
;; problems
org $908088
local_samus_submerged_lava_acid:
	jmp samus_submerged_lava_acid

;; water FX
org $9080bb
	bmi local_samus_submerged_lava_acid
org $9080C1
	bra local_samus_submerged_lava_acid
org $9080C9
	bne local_samus_submerged_lava_acid

;; wall jump management
org $908429
	bra wall_jump_branch_submerged
org $908452
wall_jump_branch_submerged:

;; run speed management
org $90974D
	bra run_speed_branch_submerged
org $90976E
run_speed_branch_submerged:

;; jump management
org $9098D7
	bra jump_lava_acid_branch
	bra jump_lava_acid_branch
org $9098F4
jump_lava_acid_branch:

org $909964
	bra wall_jump_lava_acid_branch
	bra wall_jump_lava_acid_branch
org $909981
wall_jump_lava_acid_branch:

;; knockback management
org $9099F1
	bra knockback_lava_acid_branch
	bra knockback_lava_acid_branch
org $909A0E
knockback_lava_acid_branch:

;; bomb jump management
org $909A44
	bra bomb_jump_lava_acid_branch
	bra bomb_jump_lava_acid_branch
org $909A61
bomb_jump_lava_acid_branch:

;; X speed table lookup
org $909BE9
	bra x_speed_lava_acid_branch
	bra x_speed_lava_acid_branch
org $909C06
x_speed_lava_acid_branch:

;; grapple X speed
org $909C39
	bra grapple_x_speed_lava_acid_branch
	bra grapple_x_speed_lava_acid_branch
org $909C56
grapple_x_speed_lava_acid_branch:

;; Y acceleration
org $909C70
	bra y_accel_lava_acid_branch
	bra y_accel_lava_acid_branch
org $909C9F
y_accel_lava_acid_branch:

;; spin jump management
org $90A445
	bra spin_jump_liquid_branch
org $90A461
spin_jump_liquid_branch:

;;; screw attack palette management
org $91D9BE
	bra screw_palette_liquid_branch
org $91D9F5
screw_palette_liquid_branch:

;;; misc physics stuff
org $91F696
	bra misc_physics_1_liquid_branch
org $91F6C4
misc_physics_1_liquid_branch:

org $91F6F7
	bra misc_physics_2_liquid_branch
org $91F725
misc_physics_2_liquid_branch:

org $91FA7A
	bra misc_physics_3_liquid_branch
org $91FAC8
misc_physics_3_liquid_branch:

;;; animation frame management
org $91FB34
	bra animation_frame_lava_acid_branch
	bra animation_frame_lava_acid_branch
org $91FB56
animation_frame_lava_acid_branch:
