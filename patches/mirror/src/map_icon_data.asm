;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)
;;; fix some map icons

arch 65816
lorom

org $82c83b
;;; $C83B: Crateria map icon data ;;;
; Boss icons
;       dw FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFF
        dw $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $ffff
; (Missile stations)
;       dw FFFF
        dw $ffff
; (Energy station)
;       dw FFFF
        dw $ffff
; Map stations
;       dw 00B8,0040,   FFFF
        dw $0138,$0040, $ffff
; Save points
;       dw 00D8,0028,   0090,0038,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $0118,$0026, $015f,$0037, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe
; Debug elevator markers
;       dw 01A0,0058,   0110,0040,   00B8,0090,   0030,0048,   0088,0050,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $01a0,$0058, $0110,$0040, $00b8,$0090, $0030,$0048, $0088,$0050, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe
; Debug save points
;       dw 00D8,0028,   0188,0028,   FFFF
        dw $00d8,$0028, $0188,$0028, $ffff

;;; $C89D: Brinstar map icon data ;;;
; Boss icons
;       dw 01BC,009C,   FFFF
        dw $003c,$009b, $ffff
; Missile stations
;       dw 0028,0040, FFFF
        dw $01d0,$003f, $ffff
; Energy stations
;       dw 0048,0068,   0100,0098,   01B0,0098,   FFFF
        dw $01ae,$0068, $00f7,$0097, $0048,$0098, $ffff
; Map stations
;       dw 0028,0028,   FFFF
        dw $01d0,$0027, $ffff
; Save points
;       dw 0078,0028,   0040,0030,   0028,0060,   0188,0098,   0130,0048,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $017e,$0027, $01b7,$002f, $01cf,$0060, $006e,$0097, $00c8,$0047, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe
; Debug elevator markers
;       dw 0048,0018,   00D0,0058,   0128,0038,   0148,0098,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $0048,$0018, $00d0,$0058, $0128,$0038, $0148,$0098, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe
; Debug save points
;       dw 0048,0018,   01B8,00A0,   0090,0020,   FFFF
        dw $0048,$0018, $01b8,$00a0, $0090,$0020, $ffff

;;; $C90B: Norfair map icon data ;;;
; Boss icons
;       dw 00B8,0090,   FFFF
        dw $0137,$0091, $ffff
; (Missile stations)
;       dw FFFF
        dw $ffff
; Energy stations
;       dw 00A0,0050,   00A8,0080,   FFFF
        dw $014f,$004e, $0146,$0080, $ffff
; Map stations
;       dw 0048,0028,   FFFF
        dw $01a8,$0028, $ffff
; Save points
;       dw 0060,0060,   00A8,0020,   0058,0030,   0080,0048,   00A0,0058,   0120,0068,   FFFE,FFFE,   FFFE,FFFE
        dw $0197,$005f, $0147,$0020, $0196,$002f, $016e,$0046, $014e,$0058, $00ce,$0067, $fffe,$fffe, $fffe,$fffe
; Debug elevator markers
;       dw 0050,0018,   00A8,0058,   00A8,0070,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $0050,$0018, $00A8,$0058, $00A8,$0070, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE
; Debug save points
;       dw 0050,0010,   0078,0050,   00B0,0088,   0050,0058,   00A8,0070,   00A0,0080,   0010,0008,   FFFF
        dw $0050,$0010, $0078,$0050, $00B0,$0088, $0050,$0058, $00A8,$0070, $00A0,$0080, $0010,$0008, $FFFF

;;; $C981: Wrecked Ship map icon data ;;;
; Boss icons
;       dw 0098,00A0,   FFFF
        dw $0115,$009f, $ffff
; (Missile stations)
;       dw FFFF
        dw $ffff
; (Energy station)
;       dw FFFF
        dw $ffff
; Map stations
;       dw 0068,00A0,   FFFF
        dw $0148,$009f, $ffff
; Save points
;       dw 0088,0078,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $0127,$0077, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe
; Debug elevator markers
;       dw FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE
; Debug save points
;       dw 0050,0078,   0090,00A0,   FFFF
        dw $0050,$0078, $0090,$00A0, $FFFF

;;; $C9DB: Maridia map icon data ;;;
; Boss icons
;       dw 013C,0054,   FFFF
        dw $00d3,$0053, $ffff
; Missile stations
;       dw 0130,0048,   FFFF
        dw $00e0,$0047, $ffff
; Energy station
;       dw 0150,0038,   FFFF
        dw $00bf,$0037, $ffff
; Map stations
;       dw 0088,0090,   FFFF
        dw $0188,$0090, $ffff
; Save points
;       dw 0060,00A0,   0118,0028,   0098,0060,   0148,0038,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $01af,$009f, $00f7,$0028, $0177,$005f, $00c7,$0037, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe
; Debug elevator markers
;       dw 0110,0018,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $0110,$0018, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE
; Debug save points
;       dw 0090,0028,   0148,0050,   00B8,0048,   00B0,0088,   FFFF
        dw $0090,$0028, $0148,$0050, $00B8,$0048, $00B0,$0088, $FFFF

;;; $CA49: Tourian map icon data ;;;
; (Boss icons)
;       dw FFFF
        dw $ffff
; (Missile stations)
;       dw FFFF
        dw $ffff
; Energy station
;       dw 0058,0088,   FFFF
        dw $010f,$0088, $ffff
; Map stations
;       dw FFFF
        dw $ffff
; Save points
;       dw 0080,0090,   00A8,0068,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $0136,$008f, $014e,$0067, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe, $fffe,$fffe
; Debug elevator markers
;       dw 00A0,0060,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $00A0,$0060, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE
; Debug save points
;       dw 0088,0050,   0068,00C0,   FFFF
        dw $0088,$0050, $0068,$00C0, $FFFF

;;; $CA9B: Ceres map icon data ;;;
; Boss icons
;       dw 00A0,0088,   FFFF
        dw $00A0,$0088, $FFFF
; (Missile stations)
;       dw FFFF
        dw $FFFF
; (Energy station)
;       dw FFFF
        dw $FFFF
; (Map stations)
;       dw FFFF
        dw $FFFF
; (Save points)
;       dw FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE
; (Debug elevator markers)
;       dw FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE,   FFFE,FFFE
        dw $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE, $FFFE,$FFFE
; (Debug save points)
;       dw FFFF
        dw $FFFF
