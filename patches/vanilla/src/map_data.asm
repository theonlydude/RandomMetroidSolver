lorom

incrsrc "macros.asm"

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

%export(crateria_screens)
incbin "map/crateria_data.bin"
%export(brinstar_screens)
incbin "map/brinstar_data.bin"
%export(norfair_screens)
incbin "map/norfair_data.bin"
%export(wrecked_ship_screens)
incbin "map/wrecked_ship_data.bin"
%export(maridia_screens)
incbin "map/maridia_data.bin"
%export(tourian_screens)
incbin "map/tourian_data.bin"
%export(ceres_screens)
incbin "map/ceres_data.bin"
