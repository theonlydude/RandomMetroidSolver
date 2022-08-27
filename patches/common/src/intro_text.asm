;;; Shows a single page of text and start the game

lorom
arch snes.cpu

org $8ba592
	lda #$a66f 		; cinematic function = setup intro text page 1 (skips "the last metroid...")

;;; cinematic object definition : page 1 text
org $8cc383
	;; skip vanilla japanese text handling
	;; vanilla 1 frame delay, probably necessary
	dw $0001
	db $01
	db $01
	dw $D683
print "page1_text: ", pc
	;; format :
	;;  dw frame_delay    ; vanilla is $0005
	;;  db $xx,$yy	; letter coordinates. x++ to go right ($01-$1E, 00 and 1F possible as last resort)
	;;                                    y+=2 for next line ($02-$18, 00 possible as last resort also possible to +1)
	;;  dw charCode
	;; numbers:
	;; ; 0->9, D721->D757 (step=6)
	;; special chars:
	;;  =D67D
	;; .=D75D
	;; !=D77B
	;; '=D76F
	;; letters:
	;; ; A->Z, D685->D71B (step=6)
!char_speed = $0002
macro printChar(x,y,charCode)
	dw !char_speed
	db <x>,<y>
	dw <charCode>
endmacro
	;; some random garbage to test the limits of the screen draw
	%printChar($01, $03, $d721)
	%printChar($1f, $02, $d721)
	%printChar($02, $04, $d721)
	%printChar($03, $04, $d721)
	%printChar($04, $04, $d721)
	%printChar($05, $04, $d721)
	%printChar($06, $04, $d721)
	%printChar($07, $04, $d721)
	%printChar($08, $04, $d721)
	%printChar($09, $04, $d721)
	%printChar($0a, $04, $d721)
	%printChar($0b, $04, $d721)
	%printChar($0c, $04, $d721)
	%printChar($0d, $04, $d721)
	%printChar($0e, $04, $d721)
	%printChar($0f, $04, $d721)
	%printChar($11, $04, $d721)
	%printChar($12, $04, $d721)
	%printChar($13, $04, $d721)
	%printChar($14, $04, $d721)
	%printChar($15, $04, $d721)
	%printChar($16, $04, $d721)
	%printChar($17, $04, $d721)
	%printChar($18, $04, $d721)
	%printChar($19, $04, $d721)
	%printChar($1a, $04, $d721)
	%printChar($1b, $04, $d721)
	%printChar($1c, $04, $d721)
	%printChar($00, $17, $d75d)
	%printChar($1f, $17, $d75d)
	;; custom text END: put this at the end of the text to end the script
        dw $ae5b 		; tweaked end of page 1 routine start
        dw $9698 ; Delete


;;; tweaked page 1 end, spills a bit into page 2 stuff, not a problem here
org $8bae61
introtxt_end:
	bra .skip			; ignore japanese text handling
org $8BAE72
.skip:
	lda #input_check : sta $1f51	; cinematic function=input check
.end:
	rts

print "input_check: ", pc
input_check:
	lda $8f : beq .end	; if button newly pressed:
	lda #$B240 : sta $1f51  ; 	cinematic function=start game
.end:
	rts

org $8bb763
skip_space_colony:
	lda #$C100 : sta $1F51	; start gameplay
        jsr reset_time
        rts
warnpc $8bb772

;;; now unused space (page 2+ instructions)
org $8bb336
reset_time:
        ;; reset IGT to 0
	stz $09DA
	stz $09DC
	stz $09DE
	stz $09E0
        ;; reset RTA to 0
	stz $05b8
	stz $05ba
	rts

;;; since we don't show the intro with samus gameplay, skip
;;; stuff that will impact actual gameplay
org $8ba3b0
skip_samus_900_missiles:
	bra .skip
org $8BA3B9
.skip:

org $8BA3C2
skip_restore_default_controls:
	nop #3
