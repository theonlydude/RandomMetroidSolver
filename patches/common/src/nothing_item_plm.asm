;;; plm used for nothing items
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)


lorom
arch 65816

incsrc "macros.asm"

;;; set nothing item collected as soon as samus enters its screen, for in-game tracker to behave
;;; like auto-tracker. That way nothing items will still appear on the map and disappear as soon as
;;; Samus is in the same screen

!plm_x_block = $1C29
!plm_y_block = $1C2B
!samus_x = $0af6
!samus_y = $0afa

org $848290
calc_plm_coords:

org $8486B4
instr_sleep:

org $8486C1
instr_set_preinstr:

org $8486CA
instr_clear_preinstr:

org $848724
instr_goto:

org $84887C
instr_check_item:

org $848899
instr_set_item:

org $848A2E
instr_call:

org $84DFA9
instr_list_empty_item:

org $84E007
instr_list_item_shot_block:

org $84E032
instr_list_item_shot_block_reconcealing:

;;; use some free space for pre-instruction "wake PLM if samus is in same screen as PLM"
org $8486D1
preinstr_check_screen:
        jsl calc_plm_coords
        ;; $12 = PLM X screen
        lda !plm_x_block : lsr #4 : sta $12
        ;; if X screen is different, return
        lda !samus_x : lsr #8 : cmp $12 : bne .ret
        ;; $12 = PLM Y screen
        lda !plm_y_block : lsr #4 : sta $12
        ;; if Y screen is different, return
        lda !samus_y : lsr #8 : cmp $12 : bne .ret
        jmp wake_plm
.ret:
        rts

warnpc $84870B

;;; use some more freespace
org $84BAD1
;;; nothing PLM entries ;;;
%export(visible)
        dw $EE86, instr_list_visible_block ; Nothing, visible/chozo block
%export(hidden)
        dw $EE86, instr_list_shot_block    ; Nothing, shot block

;;; Instruction list for visible/chozo nothing
instr_list_visible_block:
.start:
        dw instr_check_item, .end
        dw instr_set_preinstr, preinstr_check_screen
        dw instr_sleep
.collect:
        dw instr_set_item
.end:
        dw instr_goto, instr_list_empty_item

;;; Wake PLM and clear pre-instruction
wake_plm:
        ;; PLM timer = 1
        lda.w #1 : sta $7EDE1C,x
        jmp wake_plm_end

;;; end of free space
warnpc $84BAF3

;;; other freespace
org $848a40
;;; instruction list for nothing shot block
instr_list_shot_block:
.start:                         ; don't behave as a shot block yet if tile is unexplored for simpler implementation
        dw instr_check_item, .shot_block
        dw instr_set_preinstr, preinstr_check_screen
        dw instr_sleep
.collect:
        dw instr_set_item
.shot_block:
        dw instr_call, instr_list_item_shot_block
        dw instr_goto, .end
.end:
        dw instr_call, instr_list_item_shot_block_reconcealing
        dw instr_goto, .shot_block

wake_plm_end:
        ;; PLM instruction list pointer += 2
        INC $1D27,x
        INC $1D27,x
        ;; clear pre-instruction
        jmp instr_clear_preinstr

;;; end of free space is used by minimizer patch
warnpc $848a67
