arch 65816
lorom
bank $90

;;; Remove the checks for 10/10/10 ammo
;;; by comparing to 0 instead of 10
;;; we could save space and make this more effecient
;;; by removing these checks entirely,
;;; but that's probably not worth the overall effort.

org $90D5D5
	CMP #$0000
org $90D5DD
	CMP #$0000
org $90D5E5
	CMP #$0000

;;; Set total to decrement to 30 (was 10 each)
org $90D64B
	LDA #$001E

!Ammo_Type       = $0DEA
!CF_Count        = $0DEC
!Missile_Count   = $09C6
!Super_Count     = $09CA
!Powerbomb_Count = $09CE

;;; $D6CE: Samus movement handler - crystal flash - main (decrement ammo) ;;;
org $90D6CE
SamusMovementHandler:
{
	LDA !CF_Count  ; if crystal flash ammo decrementing timer is < 1, we're done
	CMP #$0001
	BMI .cf_done
	;; If missiles, supers, and PBs are all 0, we're done
	;; We do this by checking each one to see if the ammo is strictly
	;; less than 1.
	LDA !Missile_Count      ; check missiles
	CMP #$0001
	BPL .cf_step
	LDA !Super_Count        ; check supers
	CMP #$0001
	BPL .cf_step
	LDA !Powerbomb_Count    ; check powerbombs
	CMP #$0001
	BPL .cf_step
; Clean up and exit CF state
.cf_done:
	LDA #$D75B ;             ;\
	STA $0A58  ; [$7E:0A58]  ;} Samus movement handler = $D75B (crystal flash - finish)
	LDA #$EB52 ;             ;\
	STA $0A5C  ; [$7E:0A5C]  ;} $0A5C = default
	LDA #$0003 ;             ;\
	STA $0A94  ; [$7E:0A94]  ;} Samus animation frame timer = 3
	LDA #$000C ;             ;\
	STA $0A96  ; [$7E:0A96]  ;} Samus animation frame = 12
	BRA .return
; Do an iteration of crystal flash, decrement ammo and grant health
.cf_step:
	JSR DecrementAmmo ; decrements ammo according to Ammo_Type
	STZ $18A8  ; [$7E:18A8]  ; Samus invincibility timer = 0
	STZ $18AA  ; [$7E:18AA]  ; Samus knock back timer = 0
.return:
	RTS
}

;;; $D6E3: Crystal flash - decrement missiles ;;;
DecrementAmmo:
{
	LDA $05B6  ; [$7E:05B6]  ;\
	BIT #$0007 ;             ;} If frame counter not a multiple of 8: return
	BNE .return; [$D705]     ;/
	;; The logic here is a little complicated, but works as the following:
	;; we move to the next ammo type. If it's < 1, then we move to the next
	;; ammo type and try again. If it's >= 1, then we decrement the ammo, the CF
	;; counter, and give samus 50 hp, then exit. If we get here with 0/0/0 ammo,
	;; this would loop forever. However, the caller checks that we have at least one
	;; ammo of some type. So the loop should always terminate.
.check_count:
	INC !Ammo_Type
	LDA !Ammo_Type
	CMP #$0003
	BMI .continue
	;; The ammo type counter has to be 0 to 2, so we
	;; need to reset it to 0 aka missiles. Additionally,
	;; we want to keep A equal to the ammo type, so we clear both
	STZ !Ammo_Type
	LDA #$0000
.continue:
	;; Multiply ammo type by 4
	ASL A      ; why 4? Because that's the difference between addresses
	ASL A      ; for missiles/supers/pbs
	TAX
	LDA !Missile_Count, x
	CMP #$0001
	BMI .check_count ; if out of this ammo type, go to the next
	DEC !Missile_Count, x      ; [$7E:09C6]  ; Decrement Samus ammo
	LDA #$0032 ;             ;\
	JSL $91DF12; [$91:DF12]  ;} Give Samus 50 health
	DEC !CF_Count  ; [$7E:0DEC]  ; Decrement crystal flash ammo decrementing timer
.return:
	RTS
}
