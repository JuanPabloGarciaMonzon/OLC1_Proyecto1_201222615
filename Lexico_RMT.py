import os
import platform
import re
class lex_RMT():
    
    def __init__(self): 
        self.cadena = " "
        self.line = 0 
        self.column = 0
        self.counter = 0
        self.errors = []
        self.token_output = []
        self.error_output = []
        self.error_list={}

        self.signs = {
        "PARA":'\(', 
        "PARC":'\)', 
        "POR":'\*',
        "DIV":'\/',
        "MAS":'\+',
        "MENOS":'\-'}
        
    def initial_state(self,text):

        self.line = 1
        self.column = 1
        listaTokens = []

        while self.counter < len(text):
            if re.search(r"[A-Za-z]", text[self.counter]): #IDENTIFICADOR
                listaTokens.append(self.identifier_state(self.line,self.column,text, text[self.counter]))
            elif re.search(r"[0-9]", text[self.counter]): #NUMERO
                listaTokens.append(self.number_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[\n]", text[self.counter]):#SALTO DE LINEA
                self.counter += 1
                self.line += 1
                self.column = 1
                listaTokens.append([self.line, self.column, "salto", "\n"])
            elif re.search(r"[ \t]", text[self.counter]):#ESPACIOS Y TABULACIONES
                self.counter += 1
                self.column += 1
            elif re.search(r"[\r]", text[self.counter]):#ESPACIOS Y TABULACIONES
                self.counter += 1
                self.column += 1  
            else:
            #SIGNOS
                isSign = False
                for clave in self.signs:
                    valor = self.signs[clave]
                    if re.search(valor, text[self.counter]):
                        listaTokens.append([self.line, self.column, "operador", valor.replace('\\','')])
                        self.counter += 1
                        self.column += 1
                        isSign = True
                        break
                if not isSign:
                    self.column += 1
                    self.errors.append([self.line, self.column, text[self.counter]])
                    self.counter += 1
        return listaTokens
#----------------------------------------------------------------------------------------------------------------------------

    def identifier_state(self,linea, columna, text, word):
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
#----------------------------------------------------------------------------------------------------------------------------

    def number_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#ENTERO
                return self.number_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"\.", text[self.counter]):#DECIMAL
                return self.decimal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'integer', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [linea, columna, 'integer', word]

    def decimal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#DECIMAL
                return self.decimal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'decimal', word]
                #agregar automata de decimal en el arbol, con el valor
        else:
            return [linea, columna, 'decimal', word]
#----------------------------------------------------------------------------------------------------------------------------
    def receive_input(self):
        tokens = self.initial_state(self.cadena)
        counter = 0
        for token in tokens:
            self.token_output.append(token)
        for error in self.errors:
            counter+=1          
            self.error_output.append(error)          
            self.error_list[len(self.error_output)] = {'count':str(counter), 'column':str(error[1]) ,"line":str(error[0]),'Descripcion':str(error[2])}
#----------------------------------------------------------------------------------------------------------------------------

        


        
