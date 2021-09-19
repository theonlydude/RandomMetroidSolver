; Fix the crash that occurs when you kill an eye door whilst a eye door projectile is alive
; See the comments in the bank logs for $86:B6B9 for details on the bug

; The fix here is setting the X register to the enemy projectile index,
; which can be done without free space due to an unnecessary RTS in the original code

lorom

org $86B704
BEQ ret
TYX

org $86B713
ret:
