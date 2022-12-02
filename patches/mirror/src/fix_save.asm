;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

arch 65816
lorom

;;; fix red tower top save x/y on map
org $82c8cd
    dw $00c8
    dw $0047
