
;;; rough gadoras disasm from sm rotation
	
arch snes.cpu
lorom	

;;; BANK 84
org $84C4B1
   InstrList_Closed_L: dw $8AF1                             ;84C4B1|        |      ; vanilla routine is "Instruction list - closed blue door facing left", but this is used for up doors?? // PLM BTS = 42h, vanilla is 40h
                       db $42                               ;84C4B3|        |      ;  
                       dw $8724                             ;84C4B4|        |      ; go to a custom PLM instruction
                       dw Custom_InstrList_1                    ;84C4B6|        |00F050;  
                       dw $86BC                             ;84C4B8|        |      ;  

org $84C4E2
   InstrList_Closed_R: dw $8AF1                             ;84C4E2|        |      ; vanilla routine is "Instruction list - closed blue door facing right", but this is used for down doors??
                       db $41                               ;84C4E4|        |      ;  
                       dw $0001                             ;84C4E5|        |      ; go to a custom PLM instruction
                       dw Custom_InstrList_R_3                    ;84C4E7|        |00F1C0;  
                       dw $86BC                             ;84C4E9|        |      ; delete
	
org $84d77a
            Eye_Shoot: LDA.W $0000,Y                        ;84D77A|B90000  |000000; vanilla
                       PHY                                  ;84D77D|5A      |      ;  
                       LDY.W #$B743                         ;84D77E|A043B7  |      ;  
                       JSL.L $868097                 ;84D781|22978086|868097;  
                       LDA.W #$004C                         ;84D785|A94C00  |      ;  
                       JSL.L $8090CB                 ;84D788|22CB9080|8090CB;  
                       PLY                                  ;84D78C|7A      |      ;  
                       INY                                  ;84D78D|C8      |      ;  
                       INY                                  ;84D78E|C8      |      ;  
                       RTS                                  ;84D78F|60      |      ;  
                                                            ;      |        |      ;  
                                                            ;      |        |      ;  
            Eye_Sweat: LDA.W $0000,Y                        ;84D790|B90000  |000000; vanilla
                       PHY                                  ;84D793|5A      |      ;  
                       LDY.W #$B751                         ;84D794|A051B7  |      ;  
                       JSL.L $868097                 ;84D797|22978086|868097;  
                       PLY                                  ;84D79B|7A      |      ;  
                       INY                                  ;84D79C|C8      |      ;  
                       INY                                  ;84D79D|C8      |      ;  
                       RTS                                  ;84D79E|60      |      ;  
                                                            ;      |        |      ;  
                                                            ;      |        |      ;  
     Eye_Double_Smoke: PHY                                  ;84D79F|5A      |      ; vanilla
                       LDA.W #$030A                         ;84D7A0|A90A03  |      ;  
                       LDY.W #$E517                         ;84D7A3|A017E5  |      ;  
                       JSL.L $868097                 ;84D7A6|22978086|868097;  
                       LDA.W #$030A                         ;84D7AA|A90A03  |      ;  
                       LDY.W #$E517                         ;84D7AD|A017E5  |      ;  
                       JSL.L $868097                 ;84D7B0|22978086|868097;  
                       PLY                                  ;84D7B4|7A      |      ;  
                       RTS                                  ;84D7B5|60      |      ;  
                                                            ;      |        |      ;  
                                                            ;      |        |      ;  
            Eye_Smoke: PHY                                  ;84D7B6|5A      |      ; vanilla
                       LDA.W #$000B                         ;84D7B7|A90B00  |      ;  
                       LDY.W #$E517                         ;84D7BA|A017E5  |      ;  
                       JSL.L $868097                 ;84D7BD|22978086|868097;  
                       PLY                                  ;84D7C1|7A      |      ;  
                       RTS                                  ;84D7C2|60      |      ;  
                                                            ;      |        |      ;  
                                                            ;      |        |      ;  
          Door_Make_R: PHX                                  ;84D7C3|DA      |      ; vanilla is: "Instruction - move PLM up one row and make a blue door facing right"
                       LDA.W $1C87,X                        ;84D7C4|BD871C  |001C87;  
                       SEC                                  ;84D7C7|38      |      ;  
                       SBC.W $07A5                          ;84D7C8|EDA507  |0007A5;  
                       SBC.W $07A5                          ;84D7CB|EDA507  |0007A5;  
                       STA.W $1C87,X                        ;84D7CE|9D871C  |001C87;  
                       TAX                                  ;84D7D1|AA      |      ;  
                       LDA.W #$C043                         ;84D7D2|A943C0  |      ; vanilla is #$C041
                       JSR.W $82B4                 ;84D7D5|20B482  |8482B4;  
                       BRA Create_3_block_ext               ;84D7D8|8015    |84D7EF;  
                                                            ;      |        |      ;  
                                                            ;      |        |      ;  
          Door_Make_L: PHX                                  ;84D7DA|DA      |      ; vanilla: "Instruction - move PLM up one row and make a blue door facing left"
                       LDA.W $1C87,X                        ;84D7DB|BD871C  |001C87;  
                       SEC                                  ;84D7DE|38      |      ; vanilla "A -= 2*$07A5" becomes "A -= 2"
                       DEC A                                ;84D7DF|3A      |      ;  
                       DEC A                                ;84D7E0|3A      |      ;  
                       NOP                                  ;84D7E1|EA      |      ;  
                       NOP                                  ;84D7E2|EA      |      ;  
                       NOP                                  ;84D7E3|EA      |      ;  
                       NOP                                  ;84D7E4|EA      |      ;  
                       STA.W $1C87,X                        ;84D7E5|9D871C  |001C87;  
                       TAX                                  ;84D7E8|AA      |      ;  
                       LDA.W #$C042                         ;84D7E9|A942C0  |      ; vanilla is #$C040
                       JSR.W $82B4                 ;84D7EC|20B482  |8482B4;  
                                                            ;      |        |      ;  
   Create_3_block_ext: TXA                                  ;84D7EF|8A      |      ; vanilla: "Create 3 block vertical extension"
                       CLC                                  ;84D7F0|18      |      ; vanilla "A += 2*$07A5" becomes "A += 2"
                       INC A                                ;84D7F1|1A      |      ;  
                       INC A                                ;84D7F2|1A      |      ;  
                       NOP                                  ;84D7F3|EA      |      ;  
                       NOP                                  ;84D7F4|EA      |      ;  
                       NOP                                  ;84D7F5|EA      |      ;  
                       NOP                                  ;84D7F6|EA      |      ;  
                       TAX                                  ;84D7F7|AA      |      ;  
                       LDA.W #$50FF                         ;84D7F8|A9FF50  |      ; vanilla is #$D0FF
                       JSR.W $82B4                 ;84D7FB|20B482  |8482B4;  
                       TXA                                  ;84D7FE|8A      |      ;  
                       CLC                                  ;84D7FF|18      |      ; vanilla "A += 2*$07A5" becomes "A += 2"
                       INC A                                ;84D800|1A      |      ;  
                       INC A                                ;84D801|1A      |      ;  
                       NOP                                  ;84D802|EA      |      ;  
                       NOP                                  ;84D803|EA      |      ;  
                       NOP                                  ;84D804|EA      |      ;  
                       NOP                                  ;84D805|EA      |      ;  
                       TAX                                  ;84D806|AA      |      ;  
                       LDA.W #$50FE                         ;84D807|A9FE50  |      ; vanilla is #$D0FE
                       JSR.W $82B4                 ;84D80A|20B482  |8482B4;  
                       TXA                                  ;84D80D|8A      |      ;  
                       CLC                                  ;84D80E|18      |      ; vanilla "A += 2*$07A5" becomes "A += 2"
                       INC A                                ;84D80F|1A      |      ;  
                       INC A                                ;84D810|1A      |      ;  
                       NOP                                  ;84D811|EA      |      ;  
                       NOP                                  ;84D812|EA      |      ;  
                       NOP                                  ;84D813|EA      |      ;  
                       NOP                                  ;84D814|EA      |      ;  
                       TAX                                  ;84D815|AA      |      ;  
                       LDA.W #$50FD                         ;84D816|A9FD50  |      ; vanilla is #$D0FD
                       JSR.W $82B4                 ;84D819|20B482  |8482B4;  
                       PLX                                  ;84D81C|FA      |      ;  
                       RTS                                  ;84D81D|60      |      ;  
                                                            ;      |        |      ;  
                                                            ;      |        |      ;  
      InstrList_Eye_L: dw $8A72                             ;84D81E|        |      ; Go to $D8E3 if the room argument door is set
                       dw PTR16_84D8E3                      ;84D820|        |84D8E3;  
        DATA16_84D822: dw $0004,$9C03,$8D41                 ;84D822|        |      ; Daw instr
                       db $06,$04                           ;84D828|        |      ;  
                       dw DATA16_84D830                     ;84D82A|        |84D830;  
                       dw $8724                             ;84D82C|        |      ; Go to $D822
                       dw DATA16_84D822                     ;84D82E|        |84D822;  
        DATA16_84D830: dw $8A24                             ;84D830|        |      ; Link instruction = $D880
                       dw DATA16_84D880                     ;84D832|        |84D880;  
                       dw $86C1,$BD50,$0008,$9C0B           ;84D834|        |      ; Pre-instruction = go to link instruction if shot with a (super) missile
        DATA16_84D83C: dw $8D41                             ;84D83C|        |      ; Go to $D878 if Samus is within 01h columns and 04h rows of PLM
                       db $01,$04                           ;84D83E|        |      ;  
                       dw DATA16_84D878                     ;84D840|        |84D878;  
                       dw $0040,$9C13                       ;84D842|        |      ; Draw instr
                       dw Custom_Instr_Eye_U_1              ;84D846|        |84F4D0; Shoot *custom* eye door projectile with enemy projectile argument 0000h
                       dw $0000,$0020,$9C13                 ;84D848|        |      ;  
                       dw Custom_Instr_Eye_U_1              ;84D84E|        |84F4D0; Shoot *custom* eye door projectile with enemy projectile argument 0000h
                       dw $0000,$0020,$9C13                 ;84D850|        |      ;  
                       dw Custom_Instr_Eye_U_1              ;84D856|        |84F4D0; Shoot *custom* eye door projectile with enemy projectile argument 0000h
                       dw $0000,$0040,$9C13,$0006           ;84D858|        |      ;  
                       dw $9C0B,$0030,$9C03,$0030           ;84D860|        |      ;  
                       dw $9C03,$0006,$9C0B,$8D41           ;84D868|        |      ;  
                       db $06,$04                           ;84D870|        |      ;  
                       dw DATA16_84D83C                     ;84D872|        |84D83C;  
                       dw $8724                             ;84D874|        |      ; Go to $D822
                       dw DATA16_84D822                     ;84D876|        |84D822;  
        DATA16_84D878: dw $0004,$9C03,$8724                 ;84D878|        |      ;  
                       dw DATA16_84D83C                     ;84D87E|        |84D83C;  
        DATA16_84D880: dw $8C10                             ;84D880|        |      ; Queue sound 9, sound library 2, max queued sounds allowed = 6
                       db $09                               ;84D882|        |      ;  
                       dw Eye_Double_Smoke                  ;84D883|        |84D79F; Spawn two eye door smoke enemy projectiles
                       dw Eye_Double_Smoke                  ;84D885|        |84D79F;  
                       dw $8A91                             ;84D887|        |      ; Increment door hit counter; Set room argument door and go to $D8C4 if [door hit counter] >= 03h
                       db $03                               ;84D889|        |      ;  
                       dw DATA16_84D8C4                     ;84D88A|        |84D8C4;  
                       dw $0002,$9C1B,$0002,$9C23           ;84D88C|        |      ; Draw instructions
                       dw Eye_Double_Smoke                  ;84D894|        |84D79F; Spawn two eye door smoke enemy projectiles
                       dw $0002,$9C1B,$0002,$9C23           ;84D896|        |      ; Draw instructions
                       dw $0002,$9C1B                       ;84D89E|        |      ;  
                       dw Eye_Double_Smoke                  ;84D8A2|        |84D79F; Spawn two eye door smoke enemy projectiles
                       dw $0002,$9C23,$0004,$9C0B           ;84D8A4|        |      ; Draw instructions
                       dw $0008,$9C03                       ;84D8AC|        |      ;  
                       dw Eye_Sweat                         ;84D8B0|        |84D790; Spawn eye door sweat enemy projectile with argument 0000h
                       dw $0000,$0038,$9C03,$0004           ;84D8B2|        |      ; Draw instructions
                       dw $9C0B,$0004,$9C23,$8724           ;84D8BA|        |      ;  
                       dw DATA16_84D83C                     ;84D8C2|        |84D83C;  
        DATA16_84D8C4: dw $86CA                             ;84D8C4|        |      ; Clear pre-instruction
                       dw Eye_Smoke                         ;84D8C6|        |84D7B6; Spawn projectiles
                       dw Eye_Smoke                         ;84D8C8|        |84D7B6;  
                       dw Eye_Double_Smoke                  ;84D8CA|        |84D79F;  
                       dw Eye_Double_Smoke                  ;84D8CC|        |84D79F;  
                       dw Door_Make_L                       ;84D8CE|        |84D7DA; make door
                       dw $874E                             ;84D8D0|        |      ; Timer = 0Ah
                       db $0A                               ;84D8D2|        |      ;  
        DATA16_84D8D3: dw $0003,$9BF7,$0004,$A9A7           ;84D8D3|        |      ; Draw instructions
                       dw $873F                             ;84D8DB|        |      ; Decrement timer and go to $D8D3 if non-zero
                       dw DATA16_84D8D3                     ;84D8DD|        |84D8D3;  
                       dw $8724                             ;84D8DF|        |      ; Go to $C4B1
                       dw InstrList_Closed_L                ;84D8E1|        |84C4B1;  
         PTR16_84D8E3: dw Door_Make_L                       ;84D8E3|        |84D7DA; make door
                       dw $8724                             ;84D8E5|        |      ; Go to $C4B1
                       dw InstrList_Closed_L                ;84D8E7|        |84C4B1;  
                                                            ;      |        |      ;  
     InstrList_Door_L: dw $8A72                             ;84D8E9|        |      ; Go to $D91D if the room argument door is set
                       dw DATA16_84D91D                     ;84D8EB|        |84D91D;  
        DATA16_84D8ED: dw $8D41                             ;84D8ED|        |      ; Go to $D8FB if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84D8EF|        |      ;  
                       dw DATA16_84D8FB                     ;84D8F1|        |84D8FB;  
                       dw $0008,$9C2B,$8724                 ;84D8F3|        |      ; Draw instructions
                       dw DATA16_84D8ED                     ;84D8F9|        |84D8ED;  
        DATA16_84D8FB: dw $8A24                             ;84D8FB|        |      ; Link instruction = $D91D
                       dw DATA16_84D91D                     ;84D8FD|        |84D91D;  
                       dw $86C1,$D753                       ;84D8FF|        |      ; Pre-instruction = wake PLM if room argument door is set
        DATA16_84D903: dw $0008,$9C2B,$0008,$9C31           ;84D903|        |      ; Draw instructions
                       dw $0008,$9C37,$0008,$9C31           ;84D90B|        |      ;  
                       dw $8D41                             ;84D913|        |      ; Go to $D903 if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84D915|        |      ;  
                       dw DATA16_84D903                     ;84D917|        |84D903;  
                       dw $8724                             ;84D919|        |      ; Go to $D8ED
                       dw DATA16_84D8ED                     ;84D91B|        |84D8ED;  
        DATA16_84D91D: dw $86BC                             ;84D91D|        |      ; Delete
                                                            ;      |        |      ;  
  InstrList_DoorBot_L: dw $8A72                             ;84D91F|        |      ; Go to $D953 if the room argument door is set
                       dw DATA16_84D953                     ;84D921|        |84D953;  
        DATA16_84D923: dw $8D41                             ;84D923|        |      ; Go to $D931 if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84D925|        |      ;  
                       dw DATA16_84D931                     ;84D927|        |84D931;  
                       dw $0008,$9C3D,$8724                 ;84D929|        |      ; Draw instructions
                       dw DATA16_84D923                     ;84D92F|        |84D923;  
        DATA16_84D931: dw $8A24                             ;84D931|        |      ; Link instruction = $D953
                       dw DATA16_84D953                     ;84D933|        |84D953;  
                       dw $86C1,$D753                       ;84D935|        |      ; Pre-instruction = wake PLM if room argument door is set
        DATA16_84D939: dw $0008,$9C3D,$0008,$9C43           ;84D939|        |      ; Draw instructions
                       dw $0008,$9C49,$0008,$9C43           ;84D941|        |      ;  
                       dw $8D41                             ;84D949|        |      ; Go to $D939 if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84D94B|        |      ;  
                       dw DATA16_84D939                     ;84D94D|        |84D939;  
                       dw $8724                             ;84D94F|        |      ; Go to $D923
                       dw DATA16_84D923                     ;84D951|        |84D923;  
        DATA16_84D953: dw $86BC                             ;84D953|        |      ; Delete
                                                            ;      |        |      ;  
      InstrList_Eye_R: dw $8A72                             ;84D955|        |      ; Go to $F180 (vanilla is $DA1A) if the room argument door is set
                       dw Custom_InstrList_R_1              ;84D957|        |84F180;  
        DATA16_84D959: dw $0004,$9C5B,$8D41                 ;84D959|        |      ; Draw instructions
                       db $06,$04                           ;84D95F|        |      ;  
                       dw DATA16_84D967                     ;84D961|        |84D967;  
                       dw $8724                             ;84D963|        |      ; Go to $D959
                       dw DATA16_84D959                     ;84D965|        |84D959;  
        DATA16_84D967: dw $8A24                             ;84D967|        |      ; Link instruction = $D9B7
                       dw DATA16_84D9B7                     ;84D969|        |84D9B7;  
                       dw $86C1,$BD50,$0008,$9C63           ;84D96B|        |      ; Pre-instruction = go to link instruction if shot with a (super) missile
        DATA16_84D973: dw $8D41                             ;84D973|        |      ; Go to $D9AF if Samus is within 01h columns and 04h rows of PLM
                       db $01,$04                           ;84D975|        |      ;  
                       dw DATA16_84D9AF                     ;84D977|        |84D9AF;  
                       dw $0040,$9C6B                       ;84D979|        |      ; Draw instructions, then shoot eye door projectile with enemy projectile argument 0014h (3 times)
                       dw Eye_Shoot                         ;84D97D|        |84D77A;  
                       dw $0014,$0020,$9C6B                 ;84D97F|        |      ;  
                       dw Eye_Shoot                         ;84D985|        |84D77A;  
                       dw $0014,$0020,$9C6B                 ;84D987|        |      ;  
                       dw Eye_Shoot                         ;84D98D|        |84D77A;  
                       dw $0014,$0040,$9C6B,$0006           ;84D98F|        |      ;  
                       dw $9C63,$0030,$9C5B,$0030           ;84D997|        |      ;  
                       dw $9C5B,$0006,$9C63,$8D41           ;84D99F|        |      ;  
                       db $06,$04                           ;84D9A7|        |      ;  
                       dw DATA16_84D973                     ;84D9A9|        |84D973;  
                       dw $8724                             ;84D9AB|        |      ; Go to $D959
                       dw DATA16_84D959                     ;84D9AD|        |84D959;  
        DATA16_84D9AF: dw $0004,$9C5B,$8724                 ;84D9AF|        |      ; Draw instructions
                       dw DATA16_84D973                     ;84D9B5|        |84D973;  
        DATA16_84D9B7: dw $8C10                             ;84D9B7|        |      ; Queue sound 9, sound library 2, max queued sounds allowed = 6
                       db $09                               ;84D9B9|        |      ;  
                       dw Eye_Double_Smoke                  ;84D9BA|        |84D79F; Spawn two eye door smoke enemy projectiles
                       dw Eye_Double_Smoke                  ;84D9BC|        |84D79F; Spawn two eye door smoke enemy projectiles
                       dw $8A91                             ;84D9BE|        |      ; Increment door hit counter; Set room argument door and go to $D9FB if [door hit counter] >= 03h
                       db $03                               ;84D9C0|        |      ;  
                       dw DATA16_84D9FB                     ;84D9C1|        |84D9FB;  
                       dw $0002,$9C73,$0002,$9C7B           ;84D9C3|        |      ; Draw instructions + spawn two proj x2
                       dw Eye_Double_Smoke                  ;84D9CB|        |84D79F;  
                       dw $0002,$9C73,$0002,$9C7B           ;84D9CD|        |      ;  
                       dw $0002,$9C73                       ;84D9D5|        |      ;  
                       dw Eye_Double_Smoke                  ;84D9D9|        |84D79F;  
                       dw $0002,$9C7B,$0004,$9C63           ;84D9DB|        |      ;  
                       dw $0008,$9C5B                       ;84D9E3|        |      ;  
                       dw Eye_Sweat                         ;84D9E7|        |84D790; Spawn eye door sweat enemy projectile with argument 0004h, then draw
                       dw $0004,$0038,$9C5B,$0004           ;84D9E9|        |      ;  
                       dw $9C63,$0004,$9C7B,$8724           ;84D9F1|        |      ;  
                       dw DATA16_84D973                     ;84D9F9|        |84D973;  
        DATA16_84D9FB: dw $86CA                             ;84D9FB|        |      ; Clear pre-instruction
                       dw Eye_Smoke                         ;84D9FD|        |84D7B6; Spawn eye door smoke projectile
                       dw Eye_Smoke                         ;84D9FF|        |84D7B6; Spawn eye door smoke projectile
                       dw CODE_84F16C                       ;84DA01|        |84F16C; Spawn two eye door smoke enemy projectiles *** custom *** ...RTS?
                       dw CODE_84F16C                       ;84DA03|        |84F16C; Spawn two eye door smoke enemy projectiles *** custom *** ...RTS?
                       dw Custom_Instr_R_1                  ;84DA05|        |84F160; vanilla: "Move PLM up one row and make a blue door facing right". here custom
                       dw $874E                             ;84DA07|        |      ; Timer = 0Ah
                       db $0A                               ;84DA09|        |      ;  
        DATA16_84DA0A: dw $0003                             ;84DA0A|        |      ; Draw instructions? custom
                       dw Custom_InstrList_3                ;84DA0C|        |84F080;  
                       dw $0004                             ;84DA0E|        |      ;  
                       dw Custom_InstrList_4                ;84DA10|        |84F090;  
                       dw $873F                             ;84DA12|        |      ; Decrement timer and go to $DA0A if non-zero
                       dw DATA16_84DA0A                     ;84DA14|        |84DA0A;  
                       dw $8724                             ;84DA16|        |      ; Go to $F180 (vanilla is $C4E2)
                       dw Custom_InstrList_R_1              ;84DA18|        |84F180;  
                                                            ;      |        |      ;  
                       dw Door_Make_R                       ;84DA1A|        |84D7C3; Move PLM up one row and make a blue door facing right
                       dw $8724                             ;84DA1C|        |      ; Go to $C4E2
                       dw InstrList_Closed_R                ;84DA1E|        |84C4E2;  
                                                            ;      |        |      ;  
     InstrList_Door_R: dw $8A72                             ;84DA20|        |      ; Go to $DA54 if the room argument door is set
                       dw DATA16_84DA54                     ;84DA22|        |84DA54;  
        DATA16_84DA24: dw $8D41                             ;84DA24|        |      ; Go to $DA32 if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84DA26|        |      ;  
                       dw DATA16_84DA32                     ;84DA28|        |84DA32;  
                       dw $0008,$9C83,$8724                 ;84DA2A|        |      ; Draw
                       dw DATA16_84DA24                     ;84DA30|        |84DA24;  
        DATA16_84DA32: dw $8A24                             ;84DA32|        |      ; Link instruction = $DA54
                       dw DATA16_84DA54                     ;84DA34|        |84DA54;  
                       dw $86C1,$D753                       ;84DA36|        |      ; Pre-instruction = wake PLM if room argument door is set
        DATA16_84DA3A: dw $0006,$9C83,$0006,$9C89           ;84DA3A|        |      ; Draw
                       dw $0006,$9C8F,$0006,$9C89           ;84DA42|        |      ;  
                       dw $8D41                             ;84DA4A|        |      ; Go to $DA3A if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84DA4C|        |      ;  
                       dw DATA16_84DA3A                     ;84DA4E|        |84DA3A;  
                       dw $8724                             ;84DA50|        |      ; Go to $DA24
                       dw DATA16_84DA24                     ;84DA52|        |84DA24;  
        DATA16_84DA54: dw $86BC                             ;84DA54|        |      ; Delete
                                                            ;      |        |      ;  
  InstrList_DoorBot_R: dw $8A72                             ;84DA56|        |      ; Go to $DA8A if the room argument door is set
                       dw DATA16_84DA8A                     ;84DA58|        |84DA8A;  
        DATA16_84DA5A: dw $8D41                             ;84DA5A|        |      ; Go to $DA68 if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84DA5C|        |      ;  
                       dw DATA16_84DA68                     ;84DA5E|        |84DA68;  
                       dw $0008,$9C95,$8724                 ;84DA60|        |      ; Draw
                       dw DATA16_84DA5A                     ;84DA66|        |84DA5A;  
        DATA16_84DA68: dw $8A24                             ;84DA68|        |      ; Link instruction = $DA8A
                       dw DATA16_84DA8A                     ;84DA6A|        |84DA8A;  
                       dw $86C1,$D753                       ;84DA6C|        |      ; Pre-instruction = wake PLM if room argument door is set
        DATA16_84DA70: dw $0006,$9C95,$0006,$9C9B           ;84DA70|        |      ; Draw
                       dw $0006,$9CA1,$0006,$9C9B           ;84DA78|        |      ;  
                       dw $8D41                             ;84DA80|        |      ; Go to $DA70 if Samus is within 06h columns and 10h rows of PLM
                       db $06,$10                           ;84DA82|        |      ;  
                       dw DATA16_84DA70                     ;84DA84|        |84DA70;  
                       dw $8724                             ;84DA86|        |      ; Go to $DA5A
                       dw DATA16_84DA5A                     ;84DA88|        |84DA5A;  
        DATA16_84DA8A: dw $86BC                             ;84DA8A|        |      ; Delete
                                                            ;      |        |      ;  
    Setup_Eye_DoorBot: PHY                                  ;84DA8C|5A      |      ;  
                       LDA.W $1DC7,Y                        ;84DA8D|B9C71D  |841DC7;  
                       JSL.L $80818E                 ;84DA90|228E8180|80818E;  
                       LDA.L $7ED8B0,X                      ;84DA94|BFB0D87E|7ED8B0;  
                       PLY                                  ;84DA98|7A      |      ;  
                       AND.W $05E7                          ;84DA99|2DE705  |8405E7;  
                       BNE CODE_84DAB8                      ;84DA9C|D01A    |84DAB8;  
                       LDX.W $1C87,Y                        ;84DA9E|BE871C  |841C87;  
                       LDA.W #$C044                         ;84DAA1|A944C0  |      ;  
                       JSR.W $82B4                 ;84DAA4|20B482  |8482B4;  
                       LDA.W $1C87,Y                        ;84DAA7|B9871C  |841C87;  
                       CLC                                  ;84DAAA|18      |      ;  
                       INC A                                ;84DAAB|1A      |      ; vanilla A += 2*$07A5 becomes A += 2
                       INC A                                ;84DAAC|1A      |      ;  
                       NOP                                  ;84DAAD|EA      |      ;  
                       NOP                                  ;84DAAE|EA      |      ;  
                       NOP                                  ;84DAAF|EA      |      ;  
                       NOP                                  ;84DAB0|EA      |      ;  
                       TAX                                  ;84DAB1|AA      |      ;  
                       LDA.W #$50FF                         ;84DAB2|A9FF50  |      ; vanilla: #$D0FF
                       JSR.W $82B4                 ;84DAB5|20B482  |8482B4;  
          CODE_84DAB8: RTS                                  ;84DAB8|60      |      ;  
                                                            ;      |        |      ;  
                                                            ;      |        |      ;  
           Setup_Door: PHY                                  ;84DAB9|5A      |      ; whole routine unchanged
                       LDA.W $1DC7,Y                        ;84DABA|B9C71D  |841DC7;  
                       JSL.L $80818E                 ;84DABD|228E8180|80818E;  
                       LDA.L $7ED8B0,X                      ;84DAC1|BFB0D87E|7ED8B0;  
                       PLY                                  ;84DAC5|7A      |      ;  
                       AND.W $05E7                          ;84DAC6|2DE705  |8405E7;  
                       BNE CODE_84DAD4                      ;84DAC9|D009    |84DAD4;  
                       LDX.W $1C87,Y                        ;84DACB|BE871C  |841C87;  
                       LDA.W #$A000                         ;84DACE|A900A0  |      ;  
                       JSR.W $82B4                 ;84DAD1|20B482  |8482B4;  
          CODE_84DAD4: RTS                                  ;84DAD4|60      |      ;  
                                                            ;      |        |      ;  
org $84DB48
           Ptrs_Eye_R: dw Setup_Eye_DoorBot                 ;84DB48|        |84DA8C;  
                       dw InstrList_Eye_R                   ;84DB4A|        |84D955;  
                                                            ;      |        |      ;  
          Ptrs_Door_R: dw Setup_Door                        ;84DB4C|        |84DAB9;  
                       dw InstrList_Door_R                  ;84DB4E|        |84DA20;  
                       dw $AAE3                    ;84DB50|        |84AAE3;  
                                                            ;      |        |      ;  
       Ptrs_DoorBot_R: dw Setup_Door                        ;84DB52|        |84DAB9;  
                       dw InstrList_DoorBot_R               ;84DB54|        |84DA56;  
                                                            ;      |        |      ;  
           Ptrs_Eye_L: dw Setup_Eye_DoorBot                 ;84DB56|        |84DA8C;  
                       dw InstrList_Eye_L                   ;84DB58|        |84D81E;  
                                                            ;      |        |      ;  
          Ptrs_Door_L: dw Setup_Door                        ;84DB5A|        |84DAB9;  
                       dw InstrList_Door_L                  ;84DB5C|        |84D8E9;  
                       dw $AAE3                    ;84DB5E|        |84AAE3;  
                                                            ;      |        |      ;  
       Ptrs_DoorBot_L: dw Setup_Door                        ;84DB60|        |84DAB9;  
                       dw InstrList_DoorBot_L               ;84DB62|        |84D91F;  

org $84F050
   Custom_InstrList_1: dw $8AF1                             ;84F050|        |      ;  
                       db $42                               ;84F052|        |      ;  
                       dw $0001                             ;84F053|        |      ; another custom instr??
                       dw Custom_InstrList_2                ;84F055|        |84F060;  
                       dw $86BC                             ;84F057|        |      ;  

org $84F060
   Custom_InstrList_2: dw $0004,$C41D,$541C,$501C           ;84F060|        |      ;  
                       dw $501D,$0000                       ;84F068|        |      ;  
                       ;; db $FF,$FF,$FF,$FF,$04,$00,$1D,$CC   ;84F06C|        |FFFFFF;  
                       ;; db $1C,$5C,$1C,$58,$1D,$58,$00,$00   ;84F074|        |841C5C;  
                       ;; db $FF,$FF,$FF,$FF                   ;84F07C|        |FFFFFF;  

org $84F080
   Custom_InstrList_3: dw $0004,$8C1D,$8C1C,$881C           ;84F080|        |      ;  
                       dw $881D,$0000                       ;84F088|        |      ;  

org $84F090
   Custom_InstrList_4: dw $0004,$84AA,$84CA,$80CA           ;84F090|        |      ;  
                       dw $80AA,$0000                       ;84F098|        |      ;  

org $84F160
     Custom_Instr_R_1: PHX                                  ;84F160|DA      |      ;  
                       PHP                                  ;84F161|08      |      ;  
                       REP #$30                             ;84F162|C230    |      ;  
                       LDX.W $1C27                          ;84F164|AE271C  |841C27;  
                       DEC.W $1C87,X                        ;84F167|DE871C  |841C87;  
                       PLP                                  ;84F16A|28      |      ;  
                       PLX                                  ;84F16B|FA      |      ;  
          CODE_84F16C: RTS                                  ;84F16C|60      |      ;  

org $84F170
 Custom_InstrList_R_2: dw $0004,$CC1D,$5C1C,$581C           ;84F170|        |      ;  
                       dw $581D,$0000                       ;84F178|        |      ;  

org $84F180
 Custom_InstrList_R_1: dw Custom_Instr_R_1                  ;84F180|        |84F160;  
                       dw $8AF1,$0143                       ;84F182|        |      ;  
                       db $00                               ;84F186|        |      ;  
                       dw Custom_InstrList_R_2              ;84F187|        |84F170;  
                       dw $86BC                             ;84F189|        |      ;  
                       ;; db $FF,$FF,$FF,$FF,$FF,$60,$F1,$F1   ;84F18B|        |FFFFFF;  
                       ;; db $8A,$43,$B0,$F1,$F1,$8A,$FF,$B0   ;84F193|        |      ;  
                       ;; db $F1,$F1,$8A,$FE,$B0,$F1,$F1,$8A   ;84F19B|        |0000F1;  
                       ;; db $FD,$60,$F1,$60,$F1,$60,$F1,$01   ;84F1A3|        |84F160;  
                       ;; db $00,$70,$F1,$BC,$86,$DA,$08,$C2   ;84F1AB|        |      ;  
                       ;; db $30,$AE,$27,$1C,$FE,$87,$1C,$28   ;84F1B3|        |84F163;  
                       ;; db $FA,$60,$FF,$FF,$FF               ;84F1BB|        |      ;  

org $84F1C0
 Custom_InstrList_R_3: dw $8004,$C40C,$D42C,$DC2C           ;84F1C0|        |      ;  
                       dw $DC0C,$0000                       ;84F1C8|        |      ;  

org $84F4D0
 Custom_Instr_Eye_U_1: LDA.W $0000,Y                        ;84F4D0|B90000  |840000;  
                       PHY                                  ;84F4D3|5A      |      ;  
                       LDY.W #$F4D0                         ;84F4D4|A0D0F4  |      ; Y is enemy projectile ID..apparently Smiley took the same address in $86 for custom projectile?
                       JSL.L $868097                 ;84F4D7|22978086|868097;  
                       LDA.W #$004C                         ;84F4DB|A94C00  |      ;  
                       JSL.L $8090CB                 ;84F4DE|22CB9080|8090CB; Queue sound, sound library 2, max queued sounds allowed = 6
                       PLY                                  ;84F4E2|7A      |      ;  
                       INY                                  ;84F4E3|C8      |      ;  
                       INY                                  ;84F4E4|C8      |      ;  
                       RTS                                  ;84F4E5|60      |      ;  

;;; BANK 86
org $86F4C0
    nmyprj1_routine_1: ADC.W #$FFFF                         ;86F4C0|69FFFF  |      ;  
                       STA.W $1A93,Y                        ;86F4C3|99931A  |001A93;  
                       RTS                                  ;86F4C6|60      |      ;  
org $86F4D0
      Custom_nmyprj_1: dw Custom_nmyprj_1_init              ;86F4D0|        |86F4E0;  
                       dw $84FB,$B5D9                       ;86F4D2|        |      ;  
                       db $08,$08                           ;86F4D6|        |      ;  
                       dw $8004,$0000,$B603                 ;86F4D8|        |      ;  
org $86F4E0	
 Custom_nmyprj_1_init: LDX.W $1C27                          ;86F4E0|AE271C  |861C27;  
                       LDA.W $1DC7,X                        ;86F4E3|BDC71D  |861DC7;  
                       STA.W $1B23,Y                        ;86F4E6|99231B  |861B23;  
                       JSL.L $848290                 ;86F4E9|22908284|848290;  
                       LDX.W $1993                          ;86F4ED|AE9319  |861993;  
                       LDA.W $1C29                          ;86F4F0|AD291C  |861C29;  
                       SEC                                  ;86F4F3|38      |      ;  
                       ASL A                                ;86F4F4|0A      |      ;  
                       ASL A                                ;86F4F5|0A      |      ;  
                       ASL A                                ;86F4F6|0A      |      ;  
                       ASL A                                ;86F4F7|0A      |      ;  
                       CLC                                  ;86F4F8|18      |      ;  
                       ADC.W $B65B,X               ;86F4F9|7D5BB6  |86B65B;  
                       STA.W $1A4B,Y                        ;86F4FC|994B1A  |861A4B;  
                       LDA.W $1C2B                          ;86F4FF|AD2B1C  |861C2B;  
                       ASL A                                ;86F502|0A      |      ;  
                       ASL A                                ;86F503|0A      |      ;  
                       ASL A                                ;86F504|0A      |      ;  
                       ASL A                                ;86F505|0A      |      ;  
                       CLC                                  ;86F506|18      |      ;  
                       ADC.W $B65D,X               ;86F507|7D5DB6  |86B65D;  
                       JSR.W nmyprj1_routine_1              ;86F50A|20C0F4  |86F4C0;  
                       RTS                                  ;86F50D|60      |      ;  
