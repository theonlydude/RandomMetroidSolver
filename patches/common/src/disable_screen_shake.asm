;;; Disables excessive screen shaking
;;; compile with asar

arch snes.cpu
lorom

;;; disable earthquake in various escape setup/main asm (also covers random escape)
org $8f919c
        rts

org $8f91bd
        rts

org $8FC127
        rts
        
org $8FC926
        rts

org $8FC933
        rts

org $8FC946
        rts

org $8FC95B
        rts

org $8FE57C
        rts

org $8FE5A4
esc_room_4_main:
        bra .skip
org $8FE5CE
.skip:

org $ADF40B
mb3_end:
        bra .skip
org $ADF417   
.skip:

org $a9b289
esc_start:
        bra .skip
org $A9B295
.skip:

;;; lava/acid rising earthquake disable
org $88B36A
fx_rising_wait:
        bra .skip
org $88B376
.skip:
  
org $88B385
fx_rising:
        bra .skip
org $88B391
.skip:
