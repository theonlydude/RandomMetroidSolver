;;; Patches to apply when specific tracks are customized, disable certain sound effects that rely on vanilla music.
;;; 
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)
;;; 
;;; Define desired vanilla song(s) on the command line with -D

arch 65816
lorom

!SPC_Engine_Base = $CF6C08

macro orgSPC(addr)
org !SPC_Engine_Base+<addr>
endmacro	

macro silence(addr)
%orgSPC(<addr>)
	db $ff
endmacro	


if defined("Green_Brinstar")
print "Green_Brinstar"
;;; Etecoon wall-jump
%silence($3F84)
;;; Etecoon cry
%silence($3F8C)
;;; Etecoons theme
%silence($3FA1)

endif	

if defined("Upper_Norfair")
print "Upper_Norfair"
;;; Lava bubbling
%silence($3BC3)
%silence($3BE9)
%silence($3C0A)
;;; Fune/Namihe spits
%silence($3D9D)

endif


if defined("Red_Brinstar")
print "Red_Brinstar"
;;; mini-Kraid: disable here as red brin song plays when bosses are randomized
;;; (if kraid is vanilla, the vanilla song will play, so no need for this patch,
;;; but we don't know that here)
%silence($3C3D)
;;; tube
%silence($3D03)
%silence($3D36)
endif


if defined("Lower_Norfair")
print "Lower_Norfair"
;;; Desgeega shot (also Croc destroys wall, so that'll get disabled as well...)
%silence($3F60)
;;; Fune/Namihe spits
%silence($3D9D)

endif


if defined("East_Maridia")
print "East_Maridia"	
;;; Toilet (vanilla is already silence, that might not be the case with custom music)
%silence($3C35)
;;; Evirs
%silence($4145)
;;; Mochtroids (also some metroid cry)
%silence($429E)
%silence($42A4)
;;; snails
%silence($4491)

endif


if defined("Tourian_Bubbles")
print "Tourian_Bubbles"	
;;; disables MB2 "no music" before fight (special music data), as cutscene is sped up in VARIA seeds
org $A98810
	rep 4 : nop
;;; Metroid
%silence($41DD)
%silence($41E3)
;;; More metroid (also mochtroid)
%silence($429E)
%silence($42A4)
;;; even more metroid
%silence($42C3)
%silence($42C9)
;;; shot MB in glass
%silence($4473)
%silence($4479)
;;; glass shattering
%silence($52F5)
%silence($52FB)

endif

if defined("Mother_Brain_2")
print "Mother_Brain_2"
;;; Rainbow Beam
%silence($30E7)
%silence($3118)
%silence($3121)
;;; Ketchup
%silence($4356)
%silence($438E)
;;; MB low pitch cry
%silence($4483)
%silence($4489)
;;; baby cry
%silence($44A8)
%silence($44AE)
;;; baby drain
%silence($461C)
%silence($4622)
;;; MB high pitch cry (also phantoon dying cry)
%silence($4688)
;;; MB charging the rainbow
%silence($4692)
%silence($46C8)
;;; baby dies
%silence($517C)
%silence($5182)
endif


if defined("Mother_Brain_3")
print "Mother_Brain_3"
;;; MB low pitch cry
%silence($4483)
%silence($4489)
;;; MB high pitch cry (also phantoon dying cry)
%silence($4688)

endif

if defined("Wrecked_Ship___Power_off")
print "Wrecked_Ship___Power_off"
;;; Ghost
%silence($41F2)
%silence($4207)

endif

if defined("Wrecked_Ship___Power_on")
;;; Robot
%silence($4424)
endif


if defined("Boss_fight___Ridley")
print "Boss_fight___Ridley"
;;; Ridley's roar
%silence($42B3)
%silence($42B9)

endif


if defined("Boss_fight___Kraid")
print "Boss_fight___Kraid"
;;; Kraid's roar (also Croc dying cry, so that'll get disabled as well...)
%silence($3F1A)
;;; Kraid dying cry
%silence($3F24)
%silence($3F34)
endif


if defined("Boss_fight___Phantoon")
print "Boss_fight___Phantoon"
;;; Phantoon cry
%silence($44BD)
%silence($44C3)
;;; Phantoon appears 1
%silence($4631)
%silence($4637)
;;; Phantoon appears 2
%silence($4646)
%silence($464C)
;;; Phantoon appears 3
%silence($465B)
%silence($4661)
;;; Phantoon dying cry (also MB high pitch cry)
%silence($4688)

endif


if defined("Boss_fight___Crocomire")
print "Boss_fight___Crocomire"
;;; Croc dying cry (also kraid's roar, so that'll get disabled as well...)
%silence($3F1A)
;;; Croc destroys wall (also desgeega shot, so that'll get disabled as well...)
%silence($3F60)
;;; Croc cry
%silence($44D2)
%silence($44D8)
;;; Croc melting
%silence($459E)
%silence($45D1)

endif


if defined("Boss_fight___Spore_Spawn")
print "Boss_fight___Spore_Spawn"
;;; spospo opens
%silence($3F07)
%silence($3F0D)
	
endif

if defined("Boss_fight___Botwoon")
print "Boss_fight___Botwoon"	
;;; Botwoon spit
%silence($466E)

endif

if defined("Boss_fight___Draygon")
print "Boss_fight___Draygon"
;;; Draygon dies
%silence($518F)
%silence($519F)

endif
