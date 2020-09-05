import os
import re
from Lexico_RMT import lex_RMT

#     #  S->E
#     #' E-> T EP
#     #' EP-> + T EP
#     #'    | - T EP
#     #'    | EPSILON
#     #' T->F TP
#     #' TP-> * F TP
#     #'    | / F TP
#     #'    | EPSILON
#     #' F->  (E) SL 
#     #'    | NUMERO SL
#     #     | ID SL 
#     # SL->\n
#     #    |EPSILON 

class syn_RMT():

#     def S(self):
#         #Mandar a llamar a E

#     def E(self):
#         #Mandar a llamar a T 
#         #Mandar a llamar a EP

#     def EP(self):
#         #Miro mi token actual
#         #if(tokenActual == +):
#             #tokenA = token_output[self.contadorT]
#             #match(+)
#             #T
#             #EP
#         #elif (tokenActual == -)
#             #tokenA = token_output[self.contadorT]
#             #match(-)
#             #T
#             #EP
#         else:
#             pass 
            
#     def T(self):
#             #F
#             #TP

#     def TP(self):
#         #Miro mi token actual
#         #if(tokenActual == *):
#             #tokenA = token_output[self.contadorT]
#             #match(*)
#             #T
#             #EP
#         #elif (tokenActual == /)
#             #tokenA = token_output[self.contadorT]
#             #match(/)
#             #T
#             #EP
#         #else:
#             #pass 
            

#     def F(self):
#         #Miro mi token actual
#         #if(tokenActual == ( ):
#             #tokenA = token_output[self.contadorT]
#             #match(PARA)
#             #E
#             #tokenA = token_output[self.contadorT]
#             #match(PARC)
#             #SL
#         #elif (tokenActual == Numero)
#             #tokenA = token_output[self.contadorT]
#             #match(Numero)
#             #SL
#         #elif (tokenActual == ID)
#             #tokenA = token_output[self.contadorT]
#             #match(ID)
#             #SL


#     def SL(self):
#         #if(tokenA = \n):
#         #tokenA = token_output[self.contadorT]
#         #match(\n)
#         #if(Flag):
#             #Error
#         #else:
#             #limpia
#         #flag = False
#         #else:
#         #pass

#     def match(self,tokenA,simboloE,MensajeErr):
#         #if(tokenA == simboloE):
#             #nextToken
#             #print(Correcto)
#         #else:
#             #errorsyn=linea,columna,mensajeErr,lexema,tipoE
#             #errorSin.append(errorSyn)
#             #panic

#     def nextToken(self):
#             #if(contadorT!=len(token_output)):
#                 #contadorT++
#             #return token_output[self.contadorT]

#     def panic(self):
#             #flag = True
#             #tokenA = token_output[self.contadorT]
#             #while(tokenA!=\n):
#                 #tokenA = netToken()
#                 #if(contadorA==len(token_out)):
#                     #break
#                 #else:
#                     #pass




    def __init__(self,lista):
    #print(re.match(rmt.signs.get("PARA"),"("))
    #Variable que se usa como índice para recorrer la lista de Tokens
        self.numPreanalisis = 0
    #Lista de Tokens que el parser recibe del analizador léxico
        self.signs = lex_RMT()
        self.list = lista
        self.receive_input()
        self.contadorT = 0
        self.flag = False