;;; Spawns additional PLMs into rooms without needing to repoint anything
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)


arch 65816
lorom

;;; HIJACKS (room load routines in bank 82)
org $82e8d5
    jsl add_plms

org $82eb8b
    jsl add_plms

;;; DATA in bank 8F free space
org $8fe9a0
;;; additional zero-terminated PLM lists go here (written at ROM generation)
print "downwards plm_lists table start: ", pc
plm_lists:

;;; TEST
    ;; dw $B76F
    ;; db $0B, $09
    ;; dw $0007
;;; 
    dw  $0000                   ; PLM 1 ID
    dw  $00,$00                 ; PLM 1 X, PLM 1 Y
    dw  $0000                   ; PLM 1 argument
    ;; ...
    dw  $0000                   ; PLM n ID
    dw  $00,$00                 ; PLM n X, PLM n Y
    dw  $0000                   ; PLM n argument
    
    dw  $0000                   ; PLM list 1 terminator
    ;; ...

;;; *** Non-overlap in this space has to be handled at ROM generation ***

org $8feff8

;;; Additional PLM definitions for rooms *going upwards* (written a t ROM generation)
;;; 
;;; PLM lists are indexed by (Room ptr, Room State ptr, Entry Door ptr) and terminated by $0000
;;;
;;; Only Room is mandatory, if any other is $0000 it will be ignored.
;;; 
;;; List terminated by room ID $0000
room_plms:
    ;;  Room   State  Door   PLM list address
    dw  $0000, $0000, $0000, $0000
;;; TEST
;; room_plms:
;;     dw  $99bd, $99ca, $8b1a, plm_lists
;;; 
room_plms_upwards:

;;; CODE in bank 8F
org $8ff300

add_plms:
    phx
    ;; iterate through room table
    ;; we use only X as index register because of no "LDA bbaaaa,Y" instruction
    ldx #room_plms
.room_loop:
    lda $8f0000,x   : beq .end
    cmp $079b       : beq .room_ok
    bra .next_entry
.room_ok:
    lda $8f0002,x   : beq .state_ok
    cmp $07bb       : beq .state_ok
    bra .next_entry
.state_ok:
    lda $8f0004,x   : beq .load
    cmp $078d       : beq .load
    bra .next_entry
.load:
    phx                         ; save our room table iterator
    lda $8f0006,x : tax         ; put PLM list address in X
.plm_loop:
    lda $8f0000,x   : beq .load_end
    jsl $84846a                 ; spawn room PLM. argument is X : PLM offset in bank 8F
    rep 6 : inx                 ; X += 6
    bra .plm_loop
.load_end:
    plx                         ; restore room table iterator
.next_entry:
    txa : sec : sbc #$0008 : tax ; X -= 8
    bra .room_loop
.end:
    plx
    ;; vanilla code (call door asm)
    jsl $8fe8a3
    rtl

warnpc $8ff3ff
