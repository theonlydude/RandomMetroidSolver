;;; add new grey door opening conditions with G4 bosses
;;;
;;; requires also the G4 blinking roomout patches.
;;; addresses to update to enforce boss order (vanilla value: 0x00, minimizer value: 0x8c):
;;; kraid: 0x78A1F
;;; phantoon: 0x7C2A2
;;; draygon: 0x7C740
;;; ridley: 0x78EAB
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; use this 58 bytes unused plms space: (patch length: 50 bytes)
;;; $86D1: Unused. Instruction - call function [[Y]] ;;;
;;; $86EB: Unused. Instruction - call function [[Y]] with A = [[Y] + 3] ;;;

;;; vanilla code
;;; $BE3F: Instruction - set grey door pre-instruction ;;;
; $84:BE40 BC 17 1E    LDY $1E17,x[$7E:1E55] ; get door type from plm variable
; $84:BE43 B9 4B BE    LDA $BE4B,y[$84:BE53] ; load instruction from vanilla DoorUnlockTable
; $84:BE46 9D D7 1C    STA $1CD7,x[$7E:1D15] ; copy instruction in plm variable

;;; update instruction table pointer loading
org $84BE44
        dw DoorUnlockTable

;;; in unused plm code
org $8486D1
BossOrder:
	;; store the required order in ROM for the solver. ex: KPDR
        db $00,$00,$00,$00

;;; plm high byte parameter for door opening condition (index in DoorUnlockTable):
; 00: area main boss dead
; 04: area mini boss dead
; 08: area torizo dead
; 0C: enemies dead matches enemies needed
; 10: always closed
; 14: delay in tourian gate room
; 18: etecoons/dachora saved
; 
; new conditions:
; 1C: kraid dead
; 20: phantoon dead
; 24: draygon dead
; 28: ridley dead
DoorUnlockTable:
        ;; vanilla table
        dw $BDD4,$BDE3,$BDF2,$BE01,$BE1C,$BE1F,$BE30
        ;; new plm instructions in table for bosses conditions
        dw Kraid,Phantoon,Draygon,Ridley


;;; $BE30: Pre-instruction - go to link instruction if critters escaped else play dud sound ;;;
; $84:BE30 A9 0F 00    LDA #$000F
; $84:BE33 22 33 82 80 JSL $808233[$80:8233] ; check if event in A is done, if yes set carry
; $84:BE37 90 03       BCC $03    [$BE3C]    ; if carry clear go to end
; $84:BE39 4C B2 BD    JMP $BDB2  [$84:BDB2] ; go to link instruction
; $84:BE3C 4C C4 BD    JMP $BDC4  [$84:BDC4] ; play dud sound
        ;; new plm instructions
        ;; load boss dead event to check in A then hijack into critters check:
Kraid:
        lda #$0048
        jmp $BE33
Phantoon:
        lda #$0058
        jmp $BE33
Draygon:
        lda #$0060
        jmp $BE33
Ridley:
        lda #$0050
        jmp $BE33

;;; end of patch
warnpc $848703
