;;; patches by NoDever2 to imprive reserve behavior. see included files in better_reserves/ for details.
;;;
;;; adapted for dynamic VARIA HUD compatibility. Still has to be applied *after* VARIA HUD!
;;; 
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

incsrc "sym/varia_hud.asm"

;;; z flag set if VARIA HUD patch is present
macro hasVARIAhud()
        ;; detect hijack
        lda.l varia_hud_hijack_health_draw  : and #$00ff : cmp #$0020 ; JSR opcode
endmacro

incsrc "better_reserves/main.asm"
incsrc "better_reserves/hud.asm"
