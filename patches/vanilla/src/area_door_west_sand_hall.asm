;;; This patch handles the specifics for area rando door;;; 
;;; - maridia sand warp
;;;
;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

lorom
arch 65816

;; update left sand hall left door to lead to it
org $83a63c
	dw $D6FD
	db $00,$05,$3E,$06,$03,$00
	dw $8000,$0000
