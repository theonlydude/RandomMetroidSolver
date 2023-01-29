include

%export(locs_by_areas)
	dw locs_Ceres,locs_Crateria,locs_GreenPinkBrinstar,locs_RedBrinstar,locs_WreckedShip,locs_Kraid,locs_Norfair,locs_Crocomire,locs_LowerNorfair,locs_WestMaridia,locs_EastMaridia,locs_Tourian
%export(locs_start)
%export(locs_Ceres)
	db $ff
%export(locs_Crateria)
	db $05,$07,$08,$1a,$1d,$00,$04,$06,$09,$0a,$0b,$0c,$1b,$1c,$22,$24,$25,$ff
%export(locs_GreenPinkBrinstar)
	db $11,$17,$1e,$21,$23,$0d,$0e,$0f,$10,$12,$13,$15,$16,$18,$19,$1f,$ff
%export(locs_RedBrinstar)
	db $26,$2a,$27,$28,$29,$ff
%export(locs_WreckedShip)
	db $81,$84,$86,$87,$01,$02,$03,$80,$82,$83,$85,$ff
%export(locs_Kraid)
	db $2b,$30,$2c,$ff
%export(locs_Norfair)
	db $32,$35,$3d,$42,$44,$31,$33,$36,$37,$38,$3e,$3f,$40,$41,$43,$ff
%export(locs_Crocomire)
	db $34,$3c,$39,$3a,$3b,$ff
%export(locs_LowerNorfair)
	db $4e,$4f,$50,$46,$47,$49,$4a,$4b,$4c,$4d,$ff
%export(locs_WestMaridia)
	db $8a,$88,$89,$8b,$8c,$8d,$8e,$ff
%export(locs_EastMaridia)
	db $8f,$91,$96,$98,$9a,$90,$92,$93,$94,$95,$97,$ff
%export(locs_Tourian)
	db $ff
%export(locs_end)
