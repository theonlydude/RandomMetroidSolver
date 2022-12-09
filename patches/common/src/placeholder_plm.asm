;;; Compile with asar
;;; place holder for dynamic PLMs to detect collision with other patches

lorom
arch 65816
	
incsrc "sym/plm_spawn.asm"

org plm_spawn_plm_lists
        padbyte $CA : pad plm_spawn_room_plms_upwards

