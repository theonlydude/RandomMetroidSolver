
;---------------------------------------------------------------------------------------------------
;|x|                                    NO HEX MAP                                               |x|
;---------------------------------------------------------------------------------------------------

;Patch to jump directly into gameplay when selecting "start game" in file select
;and delete anything related to the hex map.

;--------------------------------------- BANK $81 --------------------------------------------------

ORG $819E3E : PADBYTE $FF : PAD $819E92		;delete main file select map
ORG $81A32A : PADBYTE $FF : PAD $81B2CB		;delete all file select map routines
ORG $81B71A : PADBYTE $FF : PAD $81EF1A		;clear area select tilemaps


;--------------------------------------- BANK $82 --------------------------------------------------

ORG $82898B : DW $8000						;if game state is 5: go to "load game data" anyway
ORG $8289EA : FILLBYTE $FF : FILL $5
ORG $82D9B8 : PADBYTE $FF : PAD $82DA02		;delete gradual colour change for hex map


;--------------------------------------- BANK $A2 --------------------------------------------------

ORG $A2A9A0 : LDA #$0006					;save "load game state" to 6 when leaving the gunship for the first time
