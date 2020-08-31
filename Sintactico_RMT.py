import os
import re
from Lexico_RMT import lex_RMT

    #' E-> T EP
    #' EP-> + T EP
    #'    | - T EP
    #'    | EPSILON
    #' T->F TP
    #' TP-> * F TP
    #'    | / F TP
    #'    | EPSILON
    #' F->  (E)
    #'    | NUMERO

class syn_RMT():

    def E(self):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9]", text[self.counter]):#IDENTIFICADOR
                return self.identifier_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'identificador', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'identificador', word]

    def EP(self):
        print("EP")
        for i in self.list:
            if(i[3]==self.signs.signs.get("MAS")):
                #EP-> + T EP
                print(re.match(rmt.signs.get("MAS"),"+"))
                self.T()
                self.EP()
            elif (i[3]==self.signs.signs.get("MENOS")):
                #EP-> - T EP
                print(re.match(rmt.signs.get("MENOS"),"-"))
                self.T()
                self.EP()
            #EP-> EPSILON
            #Para esta producción de EP en epsilon (cadena vacía), simplemente no se hace nada.
            
    def T(self):
        print("T")
        self.F()
        self.TP()

    def TP(self):
        print("TP")
        for i in self.list:
            if(i[3]==self.signs.signs.get("POR")):
                #TP-> * F TP
                if(re.match(rmt.signs.get("POR"),"*")):
                    self.F()
                    self.TP()
                else:
                    print("ERROR EN MULTIPLICACION")
                    
            elif (i[3]==self.signs.signs.get("DIV")):
                #TP-> / F TP
                if(re.match(rmt.signs.get("DIV"),"/")):
                    self.F()
                    self.TP()
                else:
                    print("ERROR EN DIVISION")
            #EP-> EPSILON
            #Para esta producción de EP en epsilon (cadena vacía), simplemente no se hace nada.

    def F(self):
        print("F")
        for i in self.list:
            if(i[3]==self.signs.signs.get("PARA")):
                #TF->  (E)
                if(re.match(rmt.signs.get("PARA"),"(")):
                    self.E()
                else:
                    print("ERROR EN PARENTESIS ABIERTO")
                
                if(re.match(rmt.signs.get("PARC"),")")):
                    print("CORRECTO PARENTESIS CIERRA")
                else:
                    print("ERROR EN PARENTESIS CERRADO")
            else:
                if(re.match(r'[0-9]+',i[3])):
                    print("NUMERO")
                    self.F()
                else:
                    print("A SABER")

    def __init__(self,lista):
    #print(re.match(rmt.signs.get("PARA"),"("))
    #Variable que se usa como índice para recorrer la lista de Tokens
        self.numPreanalisis = 0
    #Lista de Tokens que el parser recibe del analizador léxico
        self.signs = lex_RMT()
        self.list = lista
        self.receive_input()