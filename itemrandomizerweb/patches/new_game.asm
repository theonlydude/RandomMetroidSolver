;;; VARIA new game hook: skips intro and customizes starting point
;;; 
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

arch snes.cpu
lorom

;;; CONSTANTS
!GameStartState = $7ED914


;;; HIJACKS (bank 82 init routines)

org $82801d
    jsl startup

org $828067
    jsl gameplay_start

;;; This skips the intro : game state 1F instead of 1E
org $82eeda
    db $1f

;;; DATA in bank A1

org $a1f200
print "start_location: ", pc
start_location:
    ;; start location: $0000=Zebes, $0001=Ceres,
    ;; otherwise hi byte is area and low is save index
    dw $0000

;;; CODE in bank A1

;;; zero flag set if we're starting a new game
    ;; TODO call this from credits_varia.asm, or move start hooks from credits to here
check_new_game:
    ;; Make sure game mode is 1f
    lda $7e0998
    cmp #$001f : bne .end
    ;; check that Game time and frames is equal zero for new game
    ;; (Thanks Smiley and P.JBoy from metconst)
    lda $09DA
    ora $09DC
    ora $09DE
    ora $09E0
.end:
    rtl

startup:
    jsl check_new_game      : bne .end
    lda.l start_location    : beq .zebes
    cmp #$0001              : beq .ceres
    ;; custom start point on Zebes
    pha
    and #$ff00 : xba : sta $079f ; hi byte is area
    pla
    and #$00ff : sta $078b      ; low byte is save index
    lda #$0000 : jsl $8081fa    ; wake zebes
.zebes:
    lda #$0005 : bra .store_state
.ceres:
    lda #$001f
.store_state:
    sta !GameStartState
.end:
    ;; run hijacked code and return
    lda !GameStartState
    rtl

gameplay_start:
    jsl check_new_game  : bne .end
    ;; Set construction zone and red tower elevator doors to blue
    lda $7ed8b6 : ora.w #$0004 : sta $7ed8b6
    lda $7ed8b2 : ora.w #$0001 : sta $7ed8b2

    ;; Call the save code to create a new file
    lda $7e0952 : jsl $818000
.end:
    rtl

warnpc $a1ffff

;; org $80c527
;; crateria_load:
;;     dw $99BD, $8B1A, $0000, $0000, $0000, $0078, $0040
