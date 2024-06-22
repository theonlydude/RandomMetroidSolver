;;; Some vanilla bugfixes included in all VARIA seeds
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

incsrc "macros.asm"

;;; Fix the crash that occurs when you kill an eye door whilst a eye door projectile is alive
;;; See the comments in the bank logs for $86:B6B9 for details on the bug
;;; The fix here is setting the X register to the enemy projectile index,
;;; which can be done without free space due to an unnecessary RTS in the original code
org $86B704
fix_gadora_crash:
	BEQ .ret
	TYX
org $86B713
.ret:

;;; skips suits acquisition animation
org $848717
	rep 4 : nop

;;; fix to speed echoes bug when hell running
org $91b629
	db $01

;;; disable GT code
org $aac91c
	bra $3f

;;; Pause menu fixes :

;;; disable spacetime beam select in pause menu
org $82b174
	ldx #$0001
;;; fix screw attack select in pause menu
org $82b4c4
	cpx #$000c
;;; In inventory menu, when having only a beam and a suit you have
;;; to press right+up to go from beam to suit.
;;; It's not natural, so fix it to only require right.
org $82b000
	;; test of return of $B4B7 compare A and #$0000,
	;; when no item found A==#$ffff, which sets the carry,
	;; so when carry is clear it means that an item was found in misc.
	;; if no item was found in misc, we check in boots then in suits,
	;; so if an item is found in both boots and suits, as suits is
	;; tested last the selection will be set on suits.
	bcc $64

;;; Spring ball menu crash fix by strotlog.
;;; Fix obscure vanilla bug where: turning off spring ball while bouncing, can crash in $91:EA07,
;;; or exactly the same way as well in $91:F1FC:
;;; Fix buffer overrun. Overwrite nearby unreachable code at $91:fc4a (due to pose 0x65
;;; not existing) as our "free space". Translate RAM $0B20 values:
;;; #$0601 (spring ball specific value) --> #$0001
;;; #$0602 (spring ball specific value) --> #$0002
;;; thus loading a valid jump table array index for these two buggy functions.
org $91ea07
	jsr fix_spring_ball_crash
org $91f1fc
	jsr fix_spring_ball_crash
org $91fc4a
fix_spring_ball_crash:
	lda $0B20    ; $0B20: Used for bouncing as a ball when you land
	and #$00ff
	rts
warnpc $91fc54 ; ensure we don't write past the point where vanilla-accessible code resumes


;;; fix morph ball in hidden chozo PLM
org $84e8ce
	db $04
org $84ee02
	db $04

;;; To allow area transition blinking doors in rooms with no enemies,
;;; fixes enemies loading so that when there are no enemies, some values
;;; are still reset
org $a08ae5
	;; hijack enemy list empty check
	jsr check_empty
%freespaceStart($a0f820)
check_empty:
	cmp #$ffff		; original empty enemy list check
	bne .end		; it not empty: return
	stz $0e4e		; nb of enemies in the room = 0
	stz $0e52		; nb of enemies needed to clear the room = 0
.end:
	rts

%freespaceEnd($a0f830)

;;; Fixes for the extra save stations in area rando/random start :

;;; allow all possible save slots (needed for area rando extra stations)
org $848d0c
	and #$001f

;;; Save station PLM code has a bug where it can spawn two detection PLMs
;;; instead of one. These PLMs are supposed to precisely detect
;;; when Samus is standing on the save. When Samus does, it looks
;;; for a PLM at the same coordinates as itself, which is normally
;;; the actual save station PLM.
;;; But when two detection blocks are spawn, it can detect the other detection
;;; block as being the save, and the save station doesn't work.
;;; That can happen when there are item PLMs in the room with PLM index
;;; lower than the one of the save station. The detection PLMs are then spawned
;;; before the save itself in the PLM list.
;;; Therefore, we add an extra check on PLM type to double check it has
;;; actually found the save station PLM.

;;; hijack in detection block PLM code when samus is
;;; positioned correctly
org $84b5d4
search_loop_start:
	jmp save_station_check
org $84b5d9
search_loop_cont:
org $84b5df
search_loop_found:
;;; some unused bank 84 space
org $84858c
save_station_check:
	cmp $1c87,x		; original block coord check
	beq .coords_ok
	jmp search_loop_cont
.coords_ok:
	pha
	lda $1c37,x : cmp #$b76f ; check if PLM ID is save station
	beq .save_ok
	pla
	jmp search_loop_cont
.save_ok:
	pla
	jmp search_loop_found

;;; end of unused space
warnpc $8485b2

;;; Kraid vomit fix by PJBoy. Avoids garbage tiles in Kraid room when
;;; he's dead and fast doors are enabled.

;;; During horizontal door transitions, the "ready for NMI" flag is set by
;;; IRQ at the bottom of the door as an optimisation,
;;; but the PLM drawing routine hasn't necessarily finished processing
;;; yet.
;;; The Kraid quick kill vomit happens because NMI actually interrupts the
;;; PLM drawing routine for the PLM that clears the spike floor,
;;; *whilst* it's in the middle of writing entries to the $D0 table, which
;;; the NMI processes.
;;; This fix simply clears this NMI-ready flag for the duration of the PLM
;;; drawinging routine.

;;; other unused bank 84 space
org $848258
drawPlmSafe:
	lda.w $05B4 : pha ; Back up NMI ready flag
	stz.w $05B4 ; Not ready for NMI
	jsr $8DAA   ; Draw PLM
	pla : sta.w $05B4 ; Restore NMI ready flag
	rts

;;; end of unused space
warnpc $848270

; Patch calls to draw PLM
org $84861a ; End of PLM processing. Probably the only particularly important one to patch
	jsr drawPlmSafe

; org $848b50 ; End of block respawn instruction. Shouldn't need patching
; 	jsr drawPlmSafe

org $84e094 ; End of animated PLM drawing instruction. Could theoretically happen...
	jsr drawPlmSafe

; Fixes the water row at the bottom of the hud not rendering correctly (by H A M)
org $88C57E
        JMP SetXScroll

org $88EE32
SetXScroll:
        ADC #$005E : STA $12 : LDA ($12) : TAX : LDA $7E9C00,x : STA $7ECADC : PLY : PLX : PLB : RTL

; Graphical fix for loading to start location with camera not aligned to screen boundary, by strotlog:
; (See discussion in Metconst: https://discord.com/channels/127475613073145858/371734116955193354/1010003248981225572)
org $80C473
	stz $091d

org $80C47C
	stz $091f

; Graphical fix for going through door transition with camera not aligned to screen boundary, by PJBoy
!layer1PositionX = $0911
!layer1PositionY = $0915
!bg1ScrollX = $B1
!bg1ScrollY = $B3
!bg2ScrollX = $B5
!bg2ScrollY = $B7

org $80AE29
	jsr fix_camera_alignment

%freespaceStart($80dc00)
fix_camera_alignment:
	SEP #$20
	LDA !layer1PositionX : STA !bg1ScrollX : STA !bg2ScrollX
	LDA !layer1PositionY : STA !bg1ScrollY : STA !bg2ScrollY
	REP #$20

	LDA $B1 : SEC
	RTS
pushpc

; Fix water physics animation bug when transitioning to a dry room, by Benox (via dagit and moehr)

org $82E659
    JSL handle_door_transition

pullpc
handle_door_transition:
    ; Lets fix the entering from water to no water animation bug 
    STZ $0A9C
    JSL $878064 ; run hi-jacked instruction
    RTL

print "b80 end: ", pc
%freespaceEnd($80dc1f)
