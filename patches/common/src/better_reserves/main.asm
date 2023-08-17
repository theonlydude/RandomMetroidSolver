include

;;; Reserve Tanks bugfixes By NoDever2 (https://metroidconstruction.com/resource.php?id=418)

;This patch does a few things:
;* Prevents the loss of invincibility frames when auto reserves activate (no more getting hit twice!)
;* Prevents heat damage when auto reserves activate
;* Prevents a crash when pausing while auto reserves are active.
;* Makes reserve tanks come filled up.
;* Makes reserve tanks not empty if samus is fully healed when they are used in auto or manual mode.
;* Fix jank where deselecting and reselecting refill button during manual refill causes it to resume.
;  Can also press A during manual refill at any time to stop refilling.
;If you think of other ways reserves can be fixed, let me know! This patch has been updated a few times to tweak some things and continue to make reserves less sucky.

;Patch written by Nodever2 on 1-6-2020. Another bugfix added by Benox50, see update log below.
;Please let me know if there are any problems, I am still learning.
;No freespace is used.

;UPDATE HISTORY
;{
;1-11-2020
;Prevented heat damage from being dealt while reserves are refilling.
;Delete everything below the first "BRA $18" to undo this.

;3-17-2020
;Made it so that the game no longer crashes if paused at the same time that auto reserves activate.
;This was accomplished by adding org $82DB73
;Credit to Benox50 for this fix!!

;5-17-2022
;Made it so that reserve tanks come full when picked up.
;Made reserve tanks preserve remaining energy when used if not emptied.
;Also fixed jank in the pause screen where if you're manually refilling, deselect and reselect the refill button,
;refill continues.
;}

!ReserveHealthMode = $09C0
!SamusHealthRam = $09C2
!SamusMaxHealthRam = $09C4
!SamusReserveHealthRam = $09D6
!SamusMaxReserveHealthRam = $09D4
!FrameCounter = $05B6 
!SamusiFrameRam = $18A8
!PeriodicSubDamageRam = $0A4E
!PeriodicDamageRam = $0A50

!ManualReserveDelayCounter = $0757
!EQScreenCategoryIndex = $0755
!EQScreenItemIndex = $0756

;--------------------------------------
;Hijacks and such:
org $84897F;point this at any "JSL $858080 : INY : INY : RTS" in $84. Hint: there are a lot.
DisplayMsgAndReturn:

org $82AC52 : JSR CheckIfReservesSelected;HIJACK

;--------------------------------------
;Reserve tanks come full	
org $848986
;Instruction - collect [[Y]] health reserve tank
	LDA !SamusMaxReserveHealthRam
	CLC : ADC $0000,y
	STA !SamusMaxReserveHealthRam
	STA !SamusReserveHealthRam      ;makes reserves come full
	LDA !ReserveHealthMode : BNE + : INC !ReserveHealthMode
+	LDA #$0168 : JSL $82E118
	LDA #$0019 : JMP DisplayMsgAndReturn

warnpc $8489AA

;--------------------------------------
;Prevents heat damage while reserves are refilling, and prevents loss of invincibility frames too
;Also prevents auto reserves from being emptied if not all of their energy was used to heal samus
org $82DC31
AutoReserveRoutine:
;prevent heat damage and loss of i-frames
	STZ !PeriodicSubDamageRam
	INC !SamusiFrameRam

;play SFX every few frames
	LDA !FrameCounter : BIT #$0007 : BNE MainReserveRoutine
	LDA #$002D : JSL $809139;play incremental health SFX

;flow into main reserve routine

MainReserveRoutine:
	LDA !SamusReserveHealthRam : BEQ .retend

;increment samus health
	LDA !SamusHealthRam : INC : CMP !SamusMaxHealthRam
	BEQ +
	BPL .retend ; if positive, samus's health would now be greater than max, so we return without any changes
+	STA !SamusHealthRam

;decrement reserve health
	DEC !SamusReserveHealthRam

.retcont
	CLC : RTS
.retend
	SEC : RTS

;--------------------------------------
;new: if reserves not selected, reset manual reserve delay counter
;note: the below load loads category and item index, both are 1 byte
CheckIfReservesSelected:
	LDA !EQScreenCategoryIndex : CMP #$0100 : BEQ ++ ; if not selected reserve tank:
	STZ !ManualReserveDelayCounter					 ; cancel refilling
++	RTS;(vanilla code was LDA !EQScreenCategoryIndex)

;--------------------------------------
;prevents manual reserves from being emptied if not all of their energy was used to heal samus
org $82AF4F
ManualReserveRoutine:
	PHP : REP #$30

	LDA !ManualReserveDelayCounter : BEQ +++ ;if not already refilling, goto init
	LDA $8F : BIT #$0080 : BEQ ++			 ;if not newly pressed A, continue as normal
	STZ !EQScreenCategoryIndex				 ;\
	STZ !ManualReserveDelayCounter : BRA +	 ;) else, end refill and return

+++	;init (check for starting to refill):
	LDA $8F : BIT #$0080 : BEQ +	;if not newly pressed A, return
	LDA !SamusReserveHealthRam		;\
	CLC : ADC #$0007 : AND #$FFF8	;) else, set delay counter for refilling
	STA !ManualReserveDelayCounter	;/

++	;play SFX every few frames
	DEC !ManualReserveDelayCounter
	LDA !ManualReserveDelayCounter
	AND #$0007 : CMP #$0007 : BNE ++
	LDA #$002D : JSL $80914D		;play incremental health SFX

++	JSR MainReserveRoutine
	BCC +
	STZ !ManualReserveDelayCounter	;\
	JSR $AE46						;) Normal manual reserve cleanup
	STZ !EQScreenCategoryIndex		;/   except the part where we STZ !SamusReserveHealthRam
	;note that this also STZ's EQScreenItemIndex, both are 1 byte
+	PLP : RTS

;vvv---------------------------vvv Below Code by Benox50 vvv--------------------------vvv
;Game no longer crashes if pausing during reserves

org $82DB73;occurs when samus runs out of hp
;Check GameState, Crash safe 
    LDA $0998
    CMP #$0008 : BEQ +
;Getout 
    PLP : RTS
+
;Multi Checks if we do auto reserve or kill
    LDA $09C0
    BIT #$0001 : BEQ SamusNoHpContinueA ;if reserve auto
    LDA $09D6 : BEQ SamusNoHpContinueA ;if reserve 0 

;Trigger Auto Reserves
    LDA #$8000 : STA $0A78
    LDA #$001B : STA $0998
    JSL $90F084    
    BRA SamusNoHpContinueB

;Resume vanilla routine
org $82DB9F
SamusNoHpContinueA: ;Kill Samus (Game state = 13h)

org $82DBB2
SamusNoHpContinueB: ;TICK_GAME_TIME

;^^^---------------------------^^^-----------------------^^^--------------------------^^^
