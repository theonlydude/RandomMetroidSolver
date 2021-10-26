;;; Add a new menu in pause to display objectives to finish the seed
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; pause state
!pause_index = $0727

;;; pause index values
!pause_index_map_screen = #$0000
!pause_index_equipment_screen = #$0001
!pause_index_map2equip_fading_out = #$0002
!pause_index_map2equip_load_equip = #$0003
!pause_index_map2equip_fading_in = #$0004
!pause_index_equip2map_fading_out = #$0005
!pause_index_equip2map_load_map = #$0006
!pause_index_equip2map_fading_in = #$0007
;;; new screen:
!pause_index_objective_screen = #$0008
!pause_index_map2obj_fading_out = #$0009
!pause_index_map2obj_load_obj = #$000A
!pause_index_map2obj_fading_in = #$000B
!pause_index_obj2map_fading_out = #$000C
!pause_index_obj2map_load_map = #$000D
!pause_index_obj2map_fading_in = #$000E


;;; pause screen button label mode
!pause_screen_button_mode = $0753
!pause_screen_button_map = #$0000     ; Map screen (SAMUS on the right, OBJ on the left)
!pause_screen_button_nothing = #$0001 ; Unpausing (nothing)
!pause_screen_button_equip = #$0002   ; Equipment screen (MAP on the left)
;;; new button mode:
!pause_screen_button_obj = #$0003     ; Objective screen (MAP on the right)


;;; Pause screen mode
!pause_screen_mode = $0763

;;; pause screen mode values
!pause_screen_mode_map = #$0000
!pause_screen_mode_equip = #$0001
;;; new mode:
!pause_screen_mode_obj = #$0002


;;; replace pause mode code pointers list
org $82910A
        jsr (new_pause_actions_func_list,x)

;;; new function to check for L/R button pressed
org $82A505
        jsr check_l_r_pressed

;;; replace pause screen button label palettes functions
org $82A61D
        jsr (new_pause_palettes_func_list,x)

;;; vanilla function to check an event
org $808233
check_event:

;;; scavenger hunt order in ROM
org $A1F5D8
scav_order:


;;; free space after tracking.ips and seed_display.ips
org $82f983

;;; seed objectives checker functions pointers, max 5, list ends with $0000
print "objectives checker functions: ", pc
first_objective_func:
        dw kraid_is_dead
second_objective_func:
        dw phantoon_is_dead
third_objective_func:
        dw draygon_is_dead
fourth_objective_func:
        dw ridley_is_dead
fith_objective_func:
        dw $0000
        dw $0000

;;; objectives checker functions, set carry if objective is completed
print ""

;;; load boss dead event to check in A
print "Kraid is dead: ", pc
kraid_is_dead:
        lda #$0048
        jsl check_event
        rts

print "Phantoon is dead: ", pc
phantoon_is_dead:
        lda #$0058
        jsl check_event
        rts

print "Draygon is dead: ", pc
draygon_is_dead:
        lda #$0060
        jsl check_event
        rts

print "Ridley is dead: ", pc
ridley_is_dead:
        lda #$0050
        jsl check_event
        rts

print "All bosses dead: ", pc
all_g4_dead:
        jsr kraid_is_dead
        bcc .no
        jsr phantoon_is_dead
        bcc .no
        jsr draygon_is_dead
        bcc .no
        jsr ridley_is_dead
        bcc .no
        sec
.no
        rts

; $7E:D828..2F: Boss bits. Indexed by area
;     1: Area boss (Kraid, Phantoon, Draygon, both Ridleys)
;     2: Area mini-boss (Spore Spawn, Botwoon, Crocomire, Mother Brain)
;     4: Area torizo (Bomb Torizo, Golden Torizo)
; 
; $079F: Area index
;     0: Crateria
;     1: Brinstar
;     2: Norfair
;     3: Wrecked Ship
;     4: Maridia
;     5: Tourian
;     6: Ceres
;     7: Debug

; event bytes start at $7ED820
; event code is: (byte index << 3) + ln(boss bit), with byte index == area index + 8

print "Spore Spawn is dead: ", pc
spore_spawn_dead:
        lda #$0049
        jsl check_event
        rts

print "Botwoon is dead: ", pc
botwoon_dead:
        lda #$0061
        jsl check_event
        rts

print "Crocomire is dead: ", pc
crocomire_dead:
        lda #$0051
        jsl check_event
        rts

print "Bomb Torizo is dead: ", pc
bomb_torizo_dead:
        lda #$0042
        jsl check_event
        rts

print "Golden Torizo is dead: ", pc
golden_torizo_dead:
        lda #$0052
        jsl check_event
        rts

print "All mini bosses dead: ", pc
all_mini_bosses_dead:
        jsr spore_spawn_dead
        bcc .no
        jsr botwoon_dead
        bcc .no
        jsr crocomire_dead
        bcc .no
        jsr bomb_torizo_dead
        bcc .no
        jsr golden_torizo_dead
        bcc .no
        sec
.no
        rts

print "Shaktool cleared the path: ", pc
shaktool_cleared_path:
        lda #$000D
        jsl check_event
        rts

!scav_idx = $7ed86a
!hunt_over_hud = #$0011
print "Scavenger hunt completed: ", pc
scavenger_hunt_completed:
        ;; TODO::to be replaced with an event
        lda !scav_idx : asl : tax
        lda.l scav_order,x
        and #$00ff
        cmp !hunt_over_hud
        bne .scav_not_completed
        sec
        bra .end
.scav_not_completed
        clc
.end
	rts

print ""

;;; new pointers list
new_pause_actions_func_list:
        dw $9120                ; map
        dw $9142                ; equipment
        dw $9156, $91AB, $9231  ; map2equip
        dw $9186, $91D7, $9200  ; equip2map
        dw func_objective_screen
        dw func_map2obj_fading_out, func_map2obj_load_obj, func_map2obj_fading_in
        dw func_obj2map_fading_out, $91D7, $9200

new_pause_palettes_func_list:
        dw $A796, $A6DF, $A628, update_palette_objective_screen

update_palette_objective_screen:
        PHP
        REP #$30
        jsr set_bg2_objective_screen
        LDY #$000A
        LDX #$0000
.loop_top
        LDA $7E364A,x
        AND #$E3FF
        ORA #$1400
        STA $7E364A,x ;} Set tilemap palette indices at $7E:364A..53 to 5 (top of MAP)
        INX : INX
        DEY : DEY
        BNE .loop_top

        LDY #$000A
        LDX #$0000
.loop_bottom
        LDA $7E368A,x
        AND #$E3FF
        ORA #$1400
        STA $7E368A,x ;} Set tilemap palette indices at $7E:368A..93 to 5 (bottom of MAP)
        INX : INX
        DEY : DEY
        BNE .loop_bottom
        PLP
        RTS

func_objective_screen:
        STZ $B1      ; BG1 X scroll = 0
        STZ $B3      ; BG1 Y scroll = 0
        JSR draw_completed_objectives_sprites
        JSR $A505    ; Checks for L or R input during pause screens
        JSR $A5B7    ; Checks for start input during pause screen
        LDA !pause_screen_mode_obj ;\
        STA !pause_screen_mode     ;} Pause screen mode = objective screen
        RTS

func_map2obj_fading_out:
        JSL $82BB30  ; Display map elevator destinations
        JSR $B9C8    ; Map screen - draw Samus position indicator
        JSL $82B672  ; Draw map icons
        JSR $A56D    ; Updates the flashing buttons when you change pause screens
        JSL $808924  ; Handle fading out
        SEP #$20
        LDA $51      ;\
        CMP #$80     ;} If not finished fading out: return
        BNE .end     ;/
        JSL $80834B  ; Enable NMI
        REP #$20
        STZ $0723    ; Screen fade delay = 0
        STZ $0725    ; Screen fade counter = 0
        INC !pause_index    ; Pause index = 6 (equipment screen to map screen - load map screen)
.end
        RTS

func_map2obj_load_obj:
        REP #$30
        ;; backup map's scroll
        LDA $B1
        STA $BD  ;} BG4 X scroll = [BG1 X scroll]
        LDA $B3
        STA $BF  ;} BG4 Y scroll = [BG1 Y scroll]
        ;; no scroll
        STZ $B1      ; BG1 X scroll = 0
        STZ $B3      ; BG1 Y scroll = 0
        JSR transfert_objective_bg1  ; objective screen - transfer BG1 tilemap
        JSR draw_completed_objectives_sprites
        LDA !pause_screen_mode_obj   ;\
        STA !pause_screen_mode       ;} Pause screen mode = objective screen
        JSR $A615    ; Set pause screen button label palettes
        STZ $073F    ; $073F = 0
        LDA $C10C    ;\
        STA $072B    ;} $072B = Fh
        LDA #$0001   ;\
        STA $0723    ;} Screen fade delay = 1
        STA $0725    ; Screen fade counter = 1
        INC !pause_index    ; Pause index = B (map screen to objective screen - fading in)
        RTS

func_map2obj_fading_in:
        JSR draw_completed_objectives_sprites
        LDA !pause_screen_mode_obj   ;\
        STA !pause_screen_mode       ;} Pause screen mode = objective screen
        JSL $80894D  ; Handle fading in
        SEP #$20
        LDA $51      ;\
        CMP #$0F     ;} If not finished fading in: return
        BNE .end     ;/
        REP #$20
        STZ $0723    ; Screen fade delay = 0
        STZ $0725    ; Screen fade counter = 0
        LDA !pause_screen_button_obj
        STA !pause_screen_button_mode
        LDA !pause_index_objective_screen ; index = objective
        STA !pause_index    ;/
.end
        RTS

func_obj2map_fading_out:
        ;; fade out to map
        JSR draw_completed_objectives_sprites
        JSR $A56D    ; Updates the flashing buttons when you change pause screens
        JSL $808924  ; Handle fading out
        SEP #$20
        LDA $51      ;\
        CMP #$80     ;} If not finished fading out: return
        BNE .end     ;/
        JSL $80834B  ; Enable NMI
        REP #$20
        STZ $0723    ; Screen fade delay = 0
        STZ $0725    ; Screen fade counter = 0
        INC !pause_index    ; Pause index = D (obj screen to map screen - load map screen)
.end
        RTS

;;; seed display patch start
print "Before seed display ($82fb6c): ", pc
warnpc $82fb6c

;;; continue after InfoStr in seed_display.asm
org $82FB6D

;;; don't move, used by other patches: g4_skip, minimizer_tourian.
;;; returns carry set if all objectives are completed, carry clear if not
objectives_completed:
        phx
        sec                     ; in case no objective function has been set
        ldx $#0000
.loop
        lda first_objective_func, x
        beq .end                ; function not set
        jsr (first_objective_func, x)
        bcc .end                ; objective not completed
        inx : inx
        cpx $#000a              ; max five objective functions to check
        bne .loop
.end
        plx
        rtl

!held_buttons = $05E1
!l_button = #$0020
!r_button = #$0010
!light_up_no_button = #$0000
!light_up_l_button  = #$0001
!light_up_r_button  = #$0002

;;; check for L or R input and update pause_index && pause_screen_button_mode
check_l_r_pressed:
        PHP
        REP #$30
        LDA !held_buttons
        BIT !l_button
        BNE .press_L
        BIT !r_button
        BNE .press_R
        BRA .end

.press_R
        LDA !pause_screen_button_mode
        CMP !pause_screen_button_equip  ; if already equipment screen => end
        BEQ .end
        ;; common actions
        LDA $C10A   ; $82:C10A             db 05,00
        STA $0729   ; Frames to flash L/R/Start button on pause screen
        LDA !light_up_r_button
        STA $0751   ; $0751: Which button lights up for $0729 frames when changing screens from pause screen 

        LDA !pause_screen_button_mode
        CMP !pause_screen_button_obj
        BEQ .move_to_map_from_obj

.move_to_equip_from_map
        LDA !pause_index_map2equip_fading_out
        STA !pause_index
        LDA !pause_screen_button_equip
        STA !pause_screen_button_mode
        BRA .play_sound

.move_to_map_from_obj
        LDA !pause_index_obj2map_fading_out
        STA !pause_index
        LDA !pause_screen_button_map
        STA !pause_screen_button_mode   ; pause_screen_button_mode set to pause_screen_button_equip
        BRA .play_sound

.press_L
        LDA !pause_screen_button_mode  ; pause_screen_button_mode, 00 == map screen
        CMP !pause_screen_button_obj
        BEQ .end                ; if already on objective screen => end
        ;; common actions
        LDA $C10A  ; $82:C10A             db 05,00
        STA $0729  ; frames to flash L/R/Start button on pause screen
        LDA !light_up_l_button
        STA $0751

        LDA !pause_screen_button_mode
        CMP !pause_screen_button_map
        BEQ .move_to_obj_from_map   ; if on map screen and L pressed => objective screen

.move_to_map_from_equip
        LDA !pause_index_equip2map_fading_out
        STA !pause_index
        STZ !pause_screen_button_mode  ; pause_screen_button_mode set to pause_screen_button_map
        BRA .play_sound

.move_to_obj_from_map
        LDA !pause_index_map2obj_fading_out
        STA !pause_index
        LDA !pause_screen_button_obj
        STA !pause_screen_button_mode
        
.play_sound
        JSR $A615   ; $A615: Set pause screen buttons label palettes to show/hide them
        LDA #$0038  ;\
        JSL $809049 ;} Queue sound 38h, sound library 1, max queued sounds allowed = 6 (menu option selected)

.end
        PLP
        RTS

;;; load from ROM $B6F200 to VRAM $F200
load_objective_bg1:
        STA $420B                ; vanilla code

        LDA #$00
        STA $2181   ; WRAM Address Registers, low
        LDA #$F2
        STA $2182   ; middle
        LDA #$7E
        STA $2183   ; high => 7EF200
        JSL $8091A9 ; Set up a DMA transfer
         ;; DMA option 00: Write 1 byte, B0->$21xx
         ;; DMA target 80: write to $2180: WRAM Data Register
        db $01,$00,$80
        dl $B6F200
        dw $0800
        LDA #$02
        STA $420B   ; start transfert

        RTS

;;; transfert from VRAM $F200 to BG1 in VRAM $3000
transfert_objective_bg1:
        PHP
        PHB
        PHK
        PLB
        SEP #$30
        LDA #$00     ;\
        STA $2116    ;| VRAM Address Registers (Low) - This sets the address for $2118/9
        LDA #$30     ;|
        STA $2117    ;| VRAM Address Registers (High) - This sets the address for $2118/9 => $3000
        LDA #$80     ;|
        STA $2115    ;} Video Port Control Register - Set VRAM transfer mode to word-access, increment by 1.
                     ;    0x80 == 0b10000000 => i---ffrr => i=1 (increment when $2119 is accessed),
                     ;    ff=0 (full graphic ??), rr=0 (increment by 2 bytes)
        JSL $8091A9  ;| Set up a DMA transfer
         ;; DMA options: AB0CDEEE A: transfert direction 0 == CPU -> PPU, B HDMA addressing mode 0 == absolute, C CPU addr Auto inc/dec selection 0 == Increment, D CPU addr Auto inc/dec enable 0 == Enable, EEE DMA Transfer Word Select 1 == Write 2 bytes, B0->$21xx B1->$21XX+1
        ;; DMA target: PPU register selection
        ;;  The byte written here is ORed with $2100 to form the destination address for the DMA transfer. This is the "$21XX" in the description of the DMA Transfer Word Select for $43x0.
        ;;  here write to $2118: VRAM Data Write Registers (Low) (and $2119 as we write words)
         ;; DMA channel, DMA options, DMA target, Source address, Size (in bytes)
        db         $01,         $01,        $18,  $00, $F2, $7E,        $00, $08
        LDA #$02     ;\
        STA $420B    ;/ DMA Enable Register, start transfert on channel 1: 76543210 => 7/6/5/4/3/2/1/0

        STZ $B3      ;\
        STZ $B4      ;} BG1 Y scroll = 0
        PLB
        PLP
        RTS

;;; unpause
display_unpause:
        LDA !pause_screen_mode
        CMP !pause_screen_mode_equip
        BEQ .equip
        CMP !pause_screen_mode_obj
        BEQ .objective
.map
        JSL $82BB30  ; Display map elevator destinations
        JSL $82B672  ; Draw map icons
        JMP $B9C8    ; Map screen - draw Samus position indicator
.equip
        JSR $B267    ; Draw item selector
        JSR $B2A2    ; Display reserve tank amount
.objective
        JMP $A56D    ; Updates the flashing buttons when you change pause screens

;;; buttons addresses in BG2
!left_button_top     = $7E364A
!left_button_bottom  = $7E368A
!right_button_top    = $7E366C
!right_button_bottom = $7E36AC

;;; replace 'MAP' with 'OBJ' in left BG2, put back 'SAMUS' in right BG2
set_bg2_map_screen:
        LDY #$000A
        LDX #$0000
.left_loop_top
        LDA obj_top,x
        STA !left_button_top,x
        INX : INX
        DEY : DEY
        BNE .left_loop_top

        LDY #$000A
        LDX #$0000
.left_loop_bottom
        LDA obj_bottom,x
        STA !left_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .left_loop_bottom

        LDY #$000A
        LDX #$0000
.right_loop_top
        LDA samus_top,x
        STA !right_button_top,x
        INX : INX
        DEY : DEY
        BNE .right_loop_top

        LDY #$000A
        LDX #$0000
.right_loop_bottom
        LDA samus_bottom,x
        STA !right_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .right_loop_bottom
        LDY #$000A              ; vanilla code
        RTS


;;; put back 'MAP' in BG2 left
set_bg2_equipment_screen:
        LDY #$000A
        LDX #$0000
.loop_top
        LDA map_top,x
        STA !left_button_top,x
        INX : INX
        DEY : DEY
        BNE .loop_top

        LDY #$000A
        LDX #$0000
.loop_bottom
        LDA map_bottom,x
        STA !left_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .loop_bottom
        LDY #$000A              ; vanilla code
        RTS

;;; replace 'SAMUS' with 'MAP' in BG2 right
set_bg2_objective_screen:
        LDY #$000A
        LDX #$0000
.loop_top
        LDA map_top,x
        STA !right_button_top,x
        INX : INX
        DEY : DEY
        BNE .loop_top

        LDY #$000A
        LDX #$0000
.loop_bottom
        LDA map_bottom,x
        STA !right_button_bottom,x
        INX : INX
        DEY : DEY
        BNE .loop_bottom
        RTS

;;; obj:   left: grey (obj), right: MAP
;;; map:   left: OBJ,        right: samus
;;; equip: left: map,        right: grey (samus)

;;; obj/map/samus buttons tiles
obj_top:
        dw $2899, $2888, $289E, $289F, $289D

obj_bottom:
        dw $28A9, $2898, $28AE, $28AF, $28AD

map_top:
        dw $2899, $289A, $289B, $289C, $289D

map_bottom:
        dw $28A9, $28AA, $28AB, $28AC, $28AD

samus_top:
        dw $2879, $287A, $287B, $287C, $287D

samus_bottom:
        dw $2889, $288A, $288B, $288C, $288D

;;; glowing sprites around L/R
glowing_LR_animation:
        dw $002A, $002A, $002A, $002A

;;; sprites for completed objectives.
;;; an oam entry is made of five bytes: (s000000 xxxxxxxxx) (yyyyyyyy) (YXppPPPt tttttttt)
print "completed spritemaps: ", pc
first_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
second_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
third_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
fourth_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C
fith_spritemap:
        dw $0001, $0000 : db $00 : dw $3E8C

draw_completed_objectives_sprites:
        lda first_objective_func
        beq .end
        ldx #$0000 : jsr (first_objective_func, x)
        bcc .second_objective
        ldy #first_spritemap
        jsr draw_spritemap

.second_objective
        lda second_objective_func
        beq .end
        ldx #$0000 : jsr (second_objective_func, x)
        bcc .third_objective
        ldy #second_spritemap
        jsr draw_spritemap

.third_objective
        lda third_objective_func
        beq .end
        ldx #$0000 : jsr (third_objective_func, x)
        bcc .fourth_objective
        ldy #third_spritemap
        jsr draw_spritemap

.fourth_objective
        lda fourth_objective_func
        beq .end
        ldx #$0000 : jsr (fourth_objective_func, x)
        bcc .fith_objective
        ldy #fourth_spritemap
        jsr draw_spritemap

.fith_objective
        lda fith_objective_func
        beq .end
        ldx #$0000 : jsr (fith_objective_func, x)
        bcc .end
        ldy #fith_spritemap
        jsr draw_spritemap

.end
        rts

draw_spritemap:
        ;; Y: spritemap addr
        PHP
        REP #$30
        PHB

        PEA $8200
        PLB
        PLB
        LDA #$1E00
        STA $16                 ; palette * 200h
        lda #$0008
        STA $14                 ; X
	lda #$0080
        STA $12                 ; Y at screen center
        JSL $81879F ; Add spritemap to OAM

        PLB
        PLP
        RTS

print ""
print "The end: ", pc

;;; end of bank
warnpc $82ffff

;;; keep 'MAP' left button visible on map screen by keeping palette 2 instead of palette 5 (grey one)
org $82A820
        ORA #$0800
org $82A83E
        ORA #$0800

;;; update BG2 buttons
org $82A79B
        JSR set_bg2_map_screen
org $82A62D
        JSR set_bg2_equipment_screen

;;; load objective screen BG1 from ROM
org $828F3A
        JSR load_objective_bg1

;;; display correct sprites when unpausing
org $82932B
        JSR display_unpause

;;; update glowing sprite around L/R pointer
org $82C1E6
        dw glowing_LR_animation

;;; new tiles for 'OBJ' button in unused tiles
org $B69100
        db $00,$ff,$00,$00,$ff,$ff,$ff,$ff,$f8,$f8,$f0,$f0,$f2,$f2,$f2,$f2,$ff,$ff,$ff,$ff,$00,$ff,$00,$ff,$07,$f8,$0f,$f0,$0d,$f2,$0d,$f2
org $B69300
        db $f2,$f2,$f2,$f2,$f0,$f0,$f8,$f8,$ff,$ff,$00,$ff,$00,$00,$00,$ff,$0d,$f2,$0d,$f2,$0f,$f0,$07,$f8,$00,$ff,$ff,$00,$ff,$ff,$ff,$ff
org $B693C0
        db $00,$ff,$00,$00,$ff,$ff,$ff,$ff,$c1,$c1,$4c,$4c,$4c,$4c,$41,$41,$ff,$ff,$ff,$ff,$00,$ff,$00,$ff,$3e,$c1,$b3,$4c,$b3,$4c,$be,$41
org $B693E0
        db $00,$ff,$00,$00,$ff,$ff,$ff,$ff,$f3,$f3,$f3,$f3,$f3,$f3,$f3,$f3,$ff,$ff,$ff,$ff,$00,$ff,$00,$ff,$0c,$f3,$0c,$f3,$0c,$f3,$0c,$f3
org $B695C0
        db $41,$41,$4c,$4c,$4c,$4c,$c1,$c1,$ff,$ff,$00,$ff,$00,$00,$00,$ff,$be,$41,$b3,$4c,$b3,$4c,$3e,$c1,$00,$ff,$ff,$00,$ff,$ff,$ff,$ff
org $B695E0
        db $93,$93,$93,$93,$83,$83,$c7,$c7,$ff,$ff,$00,$ff,$00,$00,$00,$ff,$6c,$93,$6c,$93,$7c,$83,$38,$c7,$00,$ff,$ff,$00,$ff,$ff,$ff,$ff

;;; blank objective screen from B6F200 to B6FA00
org $B6F200
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        ;;                                                 ===== ::          O     B     J     E     C     T     I     V     E     S           ::    =====
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$68BD,$2801,$383E,$3831,$3839,$3834,$3832,$3843,$3838,$3845,$3834,$3842,$2801,$68BD,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
        dw $0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000,$0000
