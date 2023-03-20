lorom
arch 65816

incsrc "macros.asm"

org $b58000

%export(Brinstar)
incbin "map/brinstar.bin"
%export(Crateria)
incbin "map/crateria.bin"
%export(Norfair)
incbin "map/norfair.bin"
%export(WreckedShip)
incbin "map/wrecked_ship.bin"
%export(Maridia)
incbin "map/maridia.bin"
%export(Tourian)
incbin "map/tourian.bin"
%export(Ceres)
incbin "map/ceres.bin"

org $829727

screens:
incbin "map/crateria_data.bin"
incbin "map/brinstar_data.bin"
incbin "map/norfair_data.bin"
incbin "map/wrecked_ship_data.bin"
incbin "map/maridia_data.bin"
incbin "map/tourian_data.bin"
incbin "map/ceres_data.bin"
