;;; compile with thedopefish asar
;;; fix boulders reaction to samus

arch 65816
lorom


Boulder_direction_P1H = $7E0FB0         ; boulder direction (high byte of param 1)

!Boulder_direction_right = #$0000
!Boulder_direction_left = #$0001
!Boulder_direction_down = #$0002


;;; vanilla code
; $A6:8765 9D B0 0F    STA $0FB0,x[$7E:0FB0]
org $a68765
        jsr boulder_direction_set_overide

; $A6:87A9 BD B0 0F    LDA $0FB0,x[$7E:0FB0]
org $a687A9
        jsr boulder_direction_load_overide

;;; in A6 freespace
org $A6FEBC
boulder_direction_load_overide:
	;; in vanilla, direction:
        ;;  0: the boulder goes right, samus X position is tested on the right of the boulder
        ;;  1: the boulder goes left,  samus X position is tested on the left  of the boulder
        ;;  2: the boulder goes down,  samus X position is tested on the left  of the boulder
        ;; in mirror we want:
        ;;  0: the boulder goes right, samus X position is tested on the right of the boulder
        ;;  1: the boulder goes left,  samus X position is tested on the left  of the boulder
        ;;  2: the boulder goes down,  samus X position is tested on the right of the boulder
        ;; the only change is the samus X position test for boulders going down

        ;; load boulder direction
        LDA.w Boulder_direction_P1H,X
	;; set z flag to 1 if direction 2 (down), same as if direction is 0 (right)
	cmp !Boulder_direction_down
        beq .end

        ;; reload value to set flags for direction 0 right / 1 left
        LDA.w Boulder_direction_P1H,X

.end
        rts


boulder_direction_set_overide:
        ;; vanilla
        STA.w Boulder_direction_P1H,X
        jsr boulder_direction_load_overide
        rts

warnpc $A6FFFF
