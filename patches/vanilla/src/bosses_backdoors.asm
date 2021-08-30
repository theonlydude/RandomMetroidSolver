;;; Tweaks to be able to backdoor some bosses/minibosses without glitching.
;;; Required for miniboss rando to be able to turn any boss/miniboss into either a corridor
;;; or a dead-end (depending on which boss it replaces)
;;; 
;;; Spore Spawn: if alive, spawn in its screen when backdooring, otherwise act normal
;;; Crocomire: if alive, spawn before spikes when backdooring, otherwise act normal
;;; Kraid: ???
;;; Botwoon: if alive, spawn in its screen when backdooring, otherwise act normal
;;;
;;; compile with asar

;;; CONSTANTS
!incompatible_doors  = $F600
!door_list_ptr       = $07B5
!SamusX		     = $0AF6
!SamusY		     = $0AFA

;;; DATA

;;; alternate doors in bank 83

;;; Spore Spawn Super Room alternate door to spospo room to use when it's alive
org $83ae10
spospo_backdoor:
	dw $9DC7
	db $00,$01,$0E,$06,$00,$02 ; screen Y=2
	dw $0000,spospo_back_enter  ; distance to spawn=0, set door ASM

;;; setup ASM ptrs overwrites in bank 8F

org $8f9b80
	dw spospo_back_setup

;;; alternate door lists in bank 8F

org $8ff060
spospo_alt_doorlist:
	dw $8D1E,spospo_backdoor

;;; CODE

;;; macros

;;; z set if boss alive
macro isMiniBossDead()
	LDX $079F
	LDA $7ED828,x
	AND #$0002
endmacro

;;; setup/door ASMs
spospo_back_setup:
	%isMiniBossDead() : bne .end
	lda #spospo_alt_doorlist : sta !door_list_ptr
.end:
	rts

spospo_back_enter:
	lda #$0049 : sta !SamusX
	lda #$02c8 : sta !SamusY
	jsr !incompatible_doors
.end:
	rts
