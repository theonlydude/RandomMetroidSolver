;;; compile with thedopefish asar
;;; fix crab direction in mt everest (required for suitless climb with ice)

arch 65816
lorom
	
;;; fix direction for last crab
org $a1cf22
        dw $2001
