;;; Completes HUD drawing of better_reserves. Apply when VARIA HUD is off.
;;; 
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

incsrc "sym/better_reserves.asm"

org better_reserves_Data
	DW $2C33, $2C46
	DW $2C47, $2C48
	DW $AC33, $AC46

org better_reserves_HandleAutoReserveTilemap_write
        JSL better_reserves_WriteTilemap_full

org better_reserves_TransferNextVal_store
        STA $7EC618,x
