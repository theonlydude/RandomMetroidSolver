;;; Adds beam doors to the game. This file contains only the patch for the PLM bank,
;;; graphics have to be applied from a separate patch: beam_doors_gfx.ips
;;; Disassembled from the IPS patch by Mettyk25jigsaw using DiztinGUIsh
;;; Factorized code and added extra check for spazer/plasma doors to avoid beam switching

arch 65816
lorom

incsrc "macros.asm"
incsrc "doors_plms_common.asm"

;;; Free space after itemsounds.asm
%freespaceStart($84F037)
;;; Common functions to set doors open
set_open_left:
	dw $8A91
	db $01
	dw open_left
set_open_right:
	dw $8A91
	db $01
	dw open_right
set_open_top:
	dw $8A91
	db $01
	dw open_top
set_open_bottom:
	dw $8A91
	db $01
	dw open_bottom

;;; Beam Doors: disassembled and simplified from original patch
;;; Foregoes all the copy pasted door open stuff from missile doors and just
;;; point to open blue door instead (no specific opening graphics).
;;; Also removed the copy-pasted "blink when shot" loop, useless as only one shot is
;;; needed to open doors.

   close_list_wave_left: dw $0008,$A677,$0002,$A90B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A8FF,$0002,$A8F3,$0001     ;  
                       dw draw_wave_left                    ; ptr to draw instructions
                                                            ;  
  main_list_wave_left: dw $8A72,$C4B1,$8A24                 ;  
			dw set_open_left
                       dw $86C1                             ;  
                       dw check_wave                        ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_wave_left                    ; ptr to draw instructions
        DATA16_84F05E: dw $86B4                             ;  
                                ;

   close_list_wave_right: dw $0008,$A683,$0002,$A93B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A92F,$0002,$A923,$0001     ;  
                       dw draw_wave_right                    ; ptr to draw instructions
                                                            ;  
  main_list_wave_right: dw $8A72,$C4E2,$8A24                 ;  
			dw set_open_right
                       dw $86C1                             ;  
                       dw check_wave                        ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_wave_right                    ; ptr to draw instructions
        DATA16_84F0C0: dw $86B4                             ;  
                                                            ;  
   close_list_wave_top: dw $0002,$A68F,$0002,$A96B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A95F,$0002,$A953,$0001     ;  
                       dw draw_wave_top                    ; ptr to draw instructions
                                                            ;  
  main_list_wave_top: dw $8A72,$C513,$8A24                 ;  
			dw set_open_top
                       dw $86C1                             ;  
                       dw check_wave                        ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_wave_top                    ; ptr to draw instructions
        DATA16_84F122: dw $86B4                             ;  
                                                            ;  
   close_list_wave_bottom: dw $0008,$A69B,$0002,$A99B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A98F,$0002,$A983,$0001     ;  
                       dw draw_wave_bottom                    ; ptr to draw instructions
                                                            ;  
  main_list_wave_bottom: dw $8A72,$C544,$8A24                 ;  
			dw set_open_bottom
                       dw $86C1                             ;  
                       dw check_wave                        ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_wave_bottom                    ; ptr to draw instructions
        DATA16_84F184: dw $86B4                             ;  
                                                            ;  
    close_list_ice_left: dw $0008,$A677,$0002,$A90B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A8FF,$0002,$A8F3,$0001     ;  
                       dw draw_ice_left                     ; ptr to draw instructions
                                                            ;  
   main_list_ice_left: dw $8A72,$C4B1,$8A24                 ;  
			dw set_open_left
                       dw $86C1                             ;  
                       dw check_ice                         ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_ice_left                     ; ptr to draw instructions
        DATA16_84F1E6: dw $86B4                             ;  
                                                            ;  
    close_list_ice_right: dw $0008,$A683,$0002,$A93B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A92F,$0002,$A923,$0001     ;  
                       dw draw_ice_right                     ; ptr to draw instructions
                                                            ;  
   main_list_ice_right: dw $8A72,$C4E2,$8A24                 ;  
			dw set_open_right
                       dw $86C1                             ;  
                       dw check_ice                         ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_ice_right                     ; ptr to draw instructions
        DATA16_84F248: dw $86B4                             ;  
                                                            ;  
    close_list_ice_top: dw $0002,$A68F,$0002,$A96B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A95F,$0002,$A953,$0001     ;  
                       dw draw_ice_top                     ; ptr to draw instructions
                                                            ;  
   main_list_ice_top: dw $8A72,$C513,$8A24                 ;  
			dw set_open_top
                       dw $86C1                             ;  
                       dw check_ice                         ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_ice_top                     ; ptr to draw instructions
        DATA16_84F2AA: dw $86B4                             ;  
                                                            ;  
    close_list_ice_bottom: dw $0008,$A69B,$0002,$A99B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A98F,$0002,$A983,$0001     ;  
                       dw draw_ice_bottom                     ; ptr to draw instructions
                                                            ;  
   main_list_ice_bottom: dw $8A72,$C544,$8A24                 ;  
			dw set_open_bottom
                       dw $86C1                             ;  
                       dw check_ice                         ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_ice_bottom                     ; ptr to draw instructions
        DATA16_84F30C: dw $86B4                             ;  
                                                            ;  
   close_list_spazer_left: dw $0008,$A677,$0002,$A90B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A8FF,$0002,$A8F3,$0001     ;  
                       dw draw_spazer_left                    ; ptr to draw instructions
                                                            ;  
  main_list_spazer_left: dw $8A72,$C4B1,$8A24                 ;  
			dw set_open_left
                       dw $86C1                             ;  
                       dw check_spazer                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_spazer_left                    ; ptr to draw instructions
        DATA16_84F36E: dw $86B4                             ;  
                                                            ;  
   close_list_spazer_right: dw $0008,$A683,$0002,$A93B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A92F,$0002,$A923,$0001     ;  
                       dw draw_spazer_right                    ; ptr to draw instructions
                                                            ;  
  main_list_spazer_right: dw $8A72,$C4E2,$8A24                 ;  
			dw set_open_right
                       dw $86C1                             ;  
                       dw check_spazer                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_spazer_right                    ; ptr to draw instructions
        DATA16_84F3D0: dw $86B4                             ;  
                                                            ;  
   close_list_spazer_top: dw $0002,$A68F,$0002,$A96B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A95F,$0002,$A953,$0001     ;  
                       dw draw_spazer_top                    ; ptr to draw instructions
                                                            ;  
  main_list_spazer_top: dw $8A72,$C513,$8A24                 ;  
			dw set_open_top
                       dw $86C1                             ;  
                       dw check_spazer                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_spazer_top                    ; ptr to draw instructions
        DATA16_84F432: dw $86B4                             ;  
                                                            ;  
   close_list_spazer_bottom: dw $0008,$A69B,$0002,$A99B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A98F,$0002,$A983,$0001     ;  
                       dw draw_spazer_bottom                    ; ptr to draw instructions
                                                            ;  
  main_list_spazer_bottom: dw $8A72,$C544,$8A24                 ;  
			dw set_open_bottom
                       dw $86C1                             ;  
                       dw check_spazer                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_spazer_bottom                    ; ptr to draw instructions
        DATA16_84F494: dw $86B4                             ;  
                                                            ;  
   close_list_plasma_left: dw $0008,$A677,$0002,$A90B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A8FF,$0002,$A8F3,$0001     ;  
                       dw draw_plasma_left                    ; ptr to draw instructions
                                                            ;  
  main_list_plasma_left: dw $8A72,$C4B1,$8A24                 ;  
			dw set_open_left
                       dw $86C1                             ;  
                       dw check_plasma                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_plasma_left                    ; ptr to draw instructions
        DATA16_84F4F6: dw $86B4                             ;  
                                                            ;  
   close_list_plasma_right: dw $0008,$A683,$0002,$A93B,$8C19     ;  
                       db $15                               ;  
                       dw $0002,$A92F,$0002,$A923,$0001     ;  
                       dw draw_plasma_right                    ; ptr to draw instructions
                                                            ;  
  main_list_plasma_right: dw $8A72,$C4E2,$8A24                 ;  
			dw set_open_right
                       dw $86C1                             ;  
                       dw check_plasma                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_plasma_right                    ; ptr to draw instructions
        DATA16_84F558: dw $86B4                             ;  
                                                            ;  
   close_list_plasma_top: dw $0002,$A68F,$0002,$A96B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A95F,$0002,$A953,$0001     ;  
                       dw draw_plasma_top                    ; ptr to draw instructions
                                                            ;  
  main_list_plasma_top: dw $8A72,$C513,$8A24                 ;  
			dw set_open_top
                       dw $86C1                             ;  
                       dw check_plasma                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_plasma_top                    ; ptr to draw instructions
        DATA16_84F5BA: dw $86B4                             ;  
                                                            ;  
   close_list_plasma_bottom: dw $0008,$A69B,$0002,$A99B,$8C19     ;  
                       db $08                               ;  
                       dw $0002,$A98F,$0002,$A983,$0001     ;  
                       dw draw_plasma_bottom                    ; ptr to draw instructions
                                                            ;  
  main_list_plasma_bottom: dw $8A72,$C544,$8A24                 ;  
			dw set_open_bottom
                       dw $86C1                             ;  
                       dw check_plasma                      ; ptr to hit check code
                       dw $0001                             ;  
                       dw draw_plasma_bottom                    ; ptr to draw instructions
        DATA16_84F61C: dw $86B4                             ;  

;; Beam Doors checker functions, disassembled and factorized from original patch.
;; Added extra check for spazer/plasma doors to avoid beam switching
           check_wave: jsr check_beam : beq no_hit
                       LDA.W $1D77,X                        ;  
                       bit #$0001                         ;  
                       bne open_door
                       bra no_hit
                                                            ;  
            check_ice: jsr check_beam : beq no_hit
                       LDA.W $1D77,X                        ;  
                       bit #$0002                         ;  
                       bne open_door
                       bra no_hit
                                                            ;  
         check_spazer: jsr check_beam : beq no_hit
                       LDA.W $1D77,X                        ;
                       bit #$0004                         ;
                       bne open_door
			;; if plasma and spazer are collected, check for plasma hit
	               lda $09a8 : and #$000c : cmp #$000c : bne no_hit
                       LDA.W $1D77,X                        ;  
                       bit #$0008                         ;  
                       bne open_door
                       bra no_hit
                                                            ;  
         check_plasma: jsr check_beam : beq no_hit
                       LDA.W $1D77,X                        ;  
                       bit #$0008                         ;  
                       bne open_door
			;; if plasma and spazer are collected, check for spazer hit
	               lda $09a8 : and #$000c : cmp #$000c : bne no_hit
                       LDA.W $1D77,X                        ;  
                       bit #$0004                         ;  
                       bne open_door
no_hit:
                       STZ.W $1D77,X                        ;  
                       RTS                                  ;  
open_door:
	               STZ.W $1D77,X                        ;  
                       LDA.L $7EDEBC,X                      ;  
                       STA.W $1D27,X                        ;  
                       LDA.W #$0001                         ;  
                       STA.L $7EDE1C,X                      ;  
                       RTS                                  ;  

check_beam:
		       LDA.W $1D77,X                        ;  
                       AND.W #$0F00                         ;  
                       CMP.W #$0500                         ;  
		       rts

;;; Define instructions lists and PLMs for beam door indicators
%defineIndicator(wave,left)
%defineIndicator(wave,right)
%defineIndicator(wave,top)
%defineIndicator(wave,bottom)
%defineIndicator(plasma,left)
%defineIndicator(plasma,right)
%defineIndicator(plasma,top)
%defineIndicator(plasma,bottom)
%defineIndicator(spazer,left)
%defineIndicator(spazer,right)
%defineIndicator(spazer,top)
%defineIndicator(spazer,bottom)
%defineIndicator(ice,left)
%defineIndicator(ice,right)
%defineIndicator(ice,top)
%defineIndicator(ice,bottom)

%defineIndicatorPLM(wave,left)
%defineIndicatorPLM(wave,right)
%defineIndicatorPLM(wave,top)
%defineIndicatorPLM(wave,bottom)
%defineIndicatorPLM(plasma,left)
%defineIndicatorPLM(plasma,right)
%defineIndicatorPLM(plasma,top)
%defineIndicatorPLM(plasma,bottom)
%defineIndicatorPLM(spazer,left)
%defineIndicatorPLM(spazer,right)
%defineIndicatorPLM(spazer,top)
%defineIndicatorPLM(spazer,bottom)
%defineIndicatorPLM(ice,left)
%defineIndicatorPLM(ice,right)
%defineIndicatorPLM(ice,top)
%defineIndicatorPLM(ice,bottom)

print "Instruction lists end: ", pc
warnpc $84f70e

org $84f70f                                ;  
        plm_wave_top: dw $C7B1                             ;  
                       dw main_list_wave_top               ;  
                       dw close_list_wave_top                ;  
                                                            ;  
        plm_wave_bottom: dw $C7B1                             ;  
                       dw main_list_wave_bottom               ;  
                       dw close_list_wave_bottom                ;  
                                                            ;  
         plm_ice_left: dw $C7B1                             ;  
                       dw main_list_ice_left                ;  
                       dw close_list_ice_left                 ;  
                                                            ;  
         plm_ice_right: dw $C7B1                             ;  
                       dw main_list_ice_right                ;  
                       dw close_list_ice_right                 ;  
                                                            ;  
         plm_ice_top: dw $C7B1                             ;  
                       dw main_list_ice_top                ;  
                       dw close_list_ice_top                 ;  
                                                            ;  
         plm_ice_bottom: dw $C7B1                             ;  
                       dw main_list_ice_bottom                ;  
                       dw close_list_ice_bottom                 ;  
                                                            ;  
      plm_spazer_left: dw $C7B1                             ;  
                       dw main_list_spazer_left               ;  
                       dw close_list_spazer_left                ;  
                                                            ;  
      plm_spazer_right: dw $C7B1                             ;  
                       dw main_list_spazer_right               ;  
                       dw close_list_spazer_right                ;  
                                                            ;  
      plm_spazer_top: dw $C7B1                             ;  
                       dw main_list_spazer_top               ;  
                       dw close_list_spazer_top                ;  
                                                            ;  
      plm_spazer_bottom: dw $C7B1                             ;  
                       dw main_list_spazer_bottom               ;  
                       dw close_list_spazer_bottom                ;  
                                                            ;  
      plm_plasma_left: dw $C7B1                             ;  
                       dw main_list_plasma_left               ;  
                       dw close_list_plasma_left                ;  
                                                            ;  
      plm_plasma_right: dw $C7B1                             ;  
                       dw main_list_plasma_right               ;  
                       dw close_list_plasma_right                ;  
                                                            ;  
      plm_plasma_top: dw $C7B1                             ;  
                       dw main_list_plasma_top               ;  
                       dw close_list_plasma_top                ;  
                                                            ;  
      plm_plasma_bottom: dw $C7B1                             ;  
                       dw main_list_plasma_bottom               ;  
                       dw close_list_plasma_bottom                ;  
                                                            ;  
        plm_wave_left: dw $C7B1                             ;  
                       dw main_list_wave_left               ;  
                       dw close_list_wave_left                ;  
                                                            ;  
        plm_wave_right: dw $C7B1                             ;  
                       dw main_list_wave_right               ;  
                       dw close_list_wave_right                ;  
                                                            ;  
       draw_wave_left: dw $8004,$C0E0,$D0E1,$D8E1,$D8E0,$0000;  
                                                            ;  
       draw_wave_right: dw $8004,$C4E0,$D4E1,$DCE1,$DCE0,$0000;  
                                                            ;  
       draw_wave_top: dw $0004,$C4E9,$54E8,$50E8,$50E9,$0000;  
                                                            ;  
       draw_wave_bottom: dw $0004,$CCE9,$5CE8,$58E8,$58E9,$0000;  
                                                            ;  
        draw_ice_left: dw $8004,$C0E2,$D0E3,$D8E3,$D8E2,$0000;  
                                                            ;  
        draw_ice_right: dw $8004,$C4E2,$D4E3,$DCE3,$DCE2,$0000;  
                                                            ;  
        draw_ice_top: dw $0004,$C4EB,$54EA,$50EA,$50EB,$0000;  
                                                            ;  
        draw_ice_bottom: dw $0004,$CCEB,$5CEA,$58EA,$58EB,$0000;  
                                                            ;  
       draw_spazer_left: dw $8004,$C0E4,$D0E5,$D8E5,$D8E4,$0000;  
                                                            ;  
       draw_spazer_right: dw $8004,$C4E4,$D4E5,$DCE5,$DCE4,$0000;  
                                                            ;  
       draw_spazer_top: dw $0004,$C4ED,$54EC,$50EC,$50ED,$0000;  
                                                            ;  
       draw_spazer_bottom: dw $0004,$CCED,$5CEC,$58EC,$58ED,$0000;  
                                                            ;  
       draw_plasma_left: dw $8004,$C0E6,$D0E7,$D8E7,$D8E6,$0000;  
                                                            ;  
       draw_plasma_right: dw $8004,$C4E6,$D4E7,$DCE7,$DCE6,$0000;  
                                                            ;  
       draw_plasma_top: dw $0004,$C4EF,$54EE,$50EE,$50EF,$0000;  
                                                            ;  
       draw_plasma_bottom: dw $0004,$CCEF,$5CEE,$58EE,$58EF,$0000;  

%freespaceEnd($84F82F)			; start of endingtotals.asm

;;; alterations to vanilla door open/close animations (blue door open for all)
org $84a6b5
        db $0d
org $84a6b7
        db $2d
org $84a6b9
        db $2d
org $84a6bb
        db $0d
org $84a6c1
        db $0e
org $84a6c3
        db $2e
org $84a6c5
        db $2e
org $84a6c7
        db $0e
org $84a6cd
        db $0f
org $84a6cf
        db $2f
org $84a6d1
        db $2f
org $84a6d3
        db $0f
org $84a6e5
        db $0d
org $84a6e7
        db $2d
org $84a6e9
        db $2d
org $84a6eb
        db $0d
org $84a6f1
        db $0e
org $84a6f3
        db $2e
org $84a6f5
        db $2e
org $84a6f7
        db $0e
org $84a6fd
        db $0f
org $84a6ff
        db $2f
org $84a701
        db $2f
org $84a703
        db $0f
org $84a715
        db $3d
org $84a717
        db $3c
org $84a719
        db $3c
org $84a71b
        db $3d
org $84a721
        db $1f
org $84a723
        db $1e
org $84a725
        db $1e
org $84a727
        db $1f
org $84a72d
        db $3f
org $84a72f
        db $3e
org $84a731
        db $3e
org $84a733
        db $3f
org $84a745
        db $3d
org $84a747
        db $3c
org $84a749
        db $3c
org $84a74b
        db $3d
org $84a751
        db $1f
org $84a753
        db $1e
org $84a755
        db $1e
org $84a757
        db $1f
org $84a75d
        db $3f
org $84a75f
        db $3e
org $84a761
        db $3e
org $84a763
        db $3f
org $84a775
        db $0d
org $84a777
        db $2d
org $84a779
        db $2d
org $84a77b
        db $0d
org $84a781
        db $0e
org $84a783
        db $2e
org $84a785
        db $2e
org $84a787
        db $0e
org $84a78d
        db $0f
org $84a78f
        db $2f
org $84a791
        db $2f
org $84a793
        db $0f
org $84a7a5
        db $0d
org $84a7a7
        db $2d
org $84a7a9
        db $2d
org $84a7ab
        db $0d
org $84a7b1
        db $0e
org $84a7b3
        db $2e
org $84a7b5
        db $2e
org $84a7b7
        db $0e
org $84a7bd
        db $0f
org $84a7bf
        db $2f
org $84a7c1
        db $2f
org $84a7c3
        db $0f
org $84a7d5
        db $3d
org $84a7d7
        db $3c
org $84a7d9
        db $3c
org $84a7db
        db $3d
org $84a7e1
        db $1f
org $84a7e3
        db $1e
org $84a7e5
        db $1e
org $84a7e7
        db $1f
org $84a7ed
        db $3f
org $84a7ef
        db $3e
org $84a7f1
        db $3e
org $84a7f3
        db $3f
org $84a805
        db $3d
org $84a807
        db $3c
org $84a809
        db $3c
org $84a80b
        db $3d
org $84a811
        db $1f
org $84a813
        db $1e
org $84a815
        db $1e
org $84a817
        db $1f
org $84a81d
        db $3f
org $84a81f
        db $3e
org $84a821
        db $3e
org $84a823
        db $3f
org $84a835
        db $0d
org $84a837
        db $2d
org $84a839
        db $2d
org $84a83b
        db $0d
org $84a841
        db $0e
org $84a843
        db $2e
org $84a845
        db $2e
org $84a847
        db $0e
org $84a84d
        db $0f
org $84a84f
        db $2f
org $84a851
        db $2f
org $84a853
        db $0f
org $84a865
        db $0d
org $84a867
        db $2d
org $84a869
        db $2d
org $84a86b
        db $0d
org $84a871
        db $0e
org $84a873
        db $2e
org $84a875
        db $2e
org $84a877
        db $0e
org $84a87d
        db $0f
org $84a87f
        db $2f
org $84a881
        db $2f
org $84a883
        db $0f
org $84a895
        db $3d
org $84a897
        db $3c
org $84a899
        db $3c
org $84a89b
        db $3d
org $84a8a1
        db $1f
org $84a8a3
        db $1e
org $84a8a5
        db $1e
org $84a8a7
        db $1f
org $84a8ad
        db $3f
org $84a8af
        db $3e
org $84a8b1
        db $3e
org $84a8b3
        db $3f
org $84a8c5
        db $3d
org $84a8c7
        db $3c
org $84a8c9
        db $3c
org $84a8cb
        db $3d
org $84a8d1
        db $1f
org $84a8d3
        db $1e
org $84a8d5
        db $1e
org $84a8d7
        db $1f
org $84a8dd
        db $3f
org $84a8df
        db $3e
org $84a8e1
        db $3e
org $84a8e3
        db $3f
org $84a8f5
        db $0d
org $84a8f7
        db $2d
org $84a8f9
        db $2d
org $84a8fb
        db $0d
org $84a901
        db $0e
org $84a903
        db $2e
org $84a905
        db $2e
org $84a907
        db $0e
org $84a90d
        db $0f
org $84a90f
        db $2f
org $84a911
        db $2f
org $84a913
        db $0f
org $84a925
        db $0d
org $84a927
        db $2d
org $84a929
        db $2d
org $84a92b
        db $0d
org $84a931
        db $0e
org $84a933
        db $2e
org $84a935
        db $2e
org $84a937
        db $0e
org $84a93d
        db $0f
org $84a93f
        db $2f
org $84a941
        db $2f
org $84a943
        db $0f
org $84a955
        db $3d
org $84a957
        db $3c
org $84a959
        db $3c
org $84a95b
        db $3d
org $84a961
        db $1f
org $84a963
        db $1e
org $84a965
        db $1e
org $84a967
        db $1f
org $84a96d
        db $3f
org $84a96f
        db $3e
org $84a971
        db $3e
org $84a973
        db $3f
org $84a985
        db $3d
org $84a987
        db $3c
org $84a989
        db $3c
org $84a98b
        db $3d
org $84a991
        db $1f
org $84a993
        db $1e
org $84a995
        db $1e
org $84a997
        db $1f
org $84a99d
        db $3f
org $84a99f
        db $3e
org $84a9a1
        db $3e
org $84a9a3
        db $3f
