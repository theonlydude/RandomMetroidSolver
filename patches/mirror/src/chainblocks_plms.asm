;;; compile with asar

arch snes.cpu
lorom

;;; replace plm with rellocated one, apply after mirrortroid main patch
;;; before: F060
;;; new: FC1F

!blockchain_plm = #$FC1F

org $8fecea
        dw !blockchain_plm
org $8fecf0
        dw !blockchain_plm
org $8fecf6
        dw !blockchain_plm
org $8fecfc
        dw !blockchain_plm
org $8fed02
        dw !blockchain_plm
