lorom
arch 65816

incsrc "macros.asm"

org $b58000

%export(brinstar)
incbin "map/brinstar.bin"
%export(crateria)
incbin "map/crateria.bin"
%export(norfair)
incbin "map/norfair.bin"
%export(wrecked_ship)
incbin "map/wrecked_ship.bin"
%export(maridia)
incbin "map/maridia.bin"
%export(tourian)
incbin "map/tourian.bin"
%export(ceres)
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
