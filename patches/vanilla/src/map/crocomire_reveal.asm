include

;Mark boss room as explored offsets
ORG $90A840 : DW CrocomireMarkMaptileOffset	;pointer to offsets for Crocomire
ORG $90A844 : DW PhantoonMarkMaptileOffset	;pointer to offsets for Phantoon
ORG $90A848 : DW $A852		;Draygon shares pointer with Kraid, as there room size are similar

ORG $90A864
PhantoonMarkMaptileOffset:
	DW $0000, $0000, $FFFF
CrocomireMarkMaptileOffset:	;this covers from the spike wall all the way to the freestanding item
	DW $0200, $0000, $0300, $0000, $0400, $0000, $0500, $0000, $0600, $0000, $0700, $0000, $FFFF
;6 bytes left
