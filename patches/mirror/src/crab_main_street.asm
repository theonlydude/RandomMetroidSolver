;;; compile with thedopefish asar
;;; fix crab position in main street (required for suitless climb with ice)

arch 65816
lorom
	
;;; fix x/y position
org $a1dedd+2
        dw $0207, $0487
