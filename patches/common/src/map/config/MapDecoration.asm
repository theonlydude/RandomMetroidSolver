
;---------------------------------------------------------------------------------------------------
;|x|                                    MAP DECORATION                                           |x|
;---------------------------------------------------------------------------------------------------
{
ORG !Freespace_MapDecoration

;Pointer to deco tilegroups for each area
MapDecoration_AreaPointer:
;; 	DW MapDecoration_NoDecoration, MapDecoration_NoDecoration, MapDecoration_NoDecoration, MapDecoration_NoDecoration
;; 	DW MapDecoration_NoDecoration, MapDecoration_NoDecoration, MapDecoration_NoDecoration, MapDecoration_NoDecoration

;; ;Tilegroup: draw no deco tiles
;; MapDecoration_NoDecoration:
        DW $0000


;Example of one deco tilegroup instruction
;This will draw "YOU CAN DO IT" on crateria landing site.


;MapDecoration_List_Crateria:
;	DW Deco_Example : DB $18, $03
;	DW $0000

;Deco_Example:
;	DB $07 : DW $0682, $0678, $067E, $0000, $066C, $066A, $0677
;	DB $06 : DW $0000, $066D, $0678, $0000, $0672, $067D
;	DB $FF
}
