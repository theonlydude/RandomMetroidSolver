lorom
arch 65816

incsrc "sym/bank_8f.asm"

incsrc "area_ids_base.asm"

;;; MB room
org bank_8f_Room_DD58_state_DD6E_Header+16
	print "pc1: ", pc
        db $0b, $1d
org bank_8f_Room_DD58_state_DD88_Header+16
	print "pc1: ", pc
        db $0b, $1d
org bank_8f_Room_DD58_state_DDA2_Header+16
	print "pc1: ", pc
        db $0b, $1d
