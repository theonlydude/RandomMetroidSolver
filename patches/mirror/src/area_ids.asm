lorom
arch 65816

incsrc "sym/bank_8f.asm"

incsrc "area_ids_base.asm"

;;; MB room
;;; TODO add minimap room types
org bank_8f_Room_DD58_state_DD6E_Header+16
	print "pc1: ", pc
        db $0b
org bank_8f_Room_DD58_state_DD88_Header+16
	print "pc1: ", pc
        db $0b
org bank_8f_Room_DD58_state_DDA2_Header+16
	print "pc1: ", pc
        db $0b
