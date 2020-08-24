import os
import platform
import re
import tkinter as tk
#import interfaz
#To display pdfs
import webbrowser
import re
class lex_JS():
    
    def __init__(self): 
        self.cadena = " "
        self.clean = " "
        self.line = 0 
        self.column = 0
        self.counter = 0
        self.errors = []
        self.token_output = []
        self.error_output = []
        self.reserved = [
        #Var
        "var",
        #Control Sentences
        "if","else","for","while","do",
        "continue","break","return",
        "class", "function","constructor"]

        self.signs = {
        "PUNTOCOMA":';', 
        "COMA":',', 
        "LLAVEA":'{', 
        "LLAVEC":'}', 
        "PARA":'\(',
        "POR":'\*', 
        "PARC":'\)', 
        "PUNTO":'\.',
        "DPUNTO":':'}

    def initial_state(self,text):

        self.line = 1
        self.column = 1
        listaTokens = []

        while self.counter < len(text):
            if re.search(r"[A-Za-z]", text[self.counter]): #IDENTIFICADOR
                listaTokens.append(self.identifier_state(self.line,self.column,text, text[self.counter]))
            elif re.search(r"[0-9]", text[self.counter]): #NUMERO
                listaTokens.append(self.number_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\']", text[self.counter]): #CADENA
                listaTokens.append(self.simple_string_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\"]", text[self.counter]): #CADENA
                listaTokens.append(self.double_string_state(self.line, self.column, text, text[self.counter]))          
            elif re.search(r"[<]", text[self.counter]): #MENOR  O MENOR IGUAL QUE
                listaTokens.append(self.below_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[>]", text[self.counter]): #MAYOR  O MAYOR IGUAL QUE
                listaTokens.append(self.above_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[=]", text[self.counter]): #IGUAL o IGUALDAD
                listaTokens.append(self.equal_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[!]", text[self.counter]): #NOT o DIFERENCIA
                listaTokens.append(self.not_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[+]", text[self.counter]): #MAS O INCREMENTO
                listaTokens.append(self.plus_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[-]", text[self.counter]): #MENOS O DECREMENTO
                listaTokens.append(self.substracion_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[&]", text[self.counter]): #CONJUNCION
                listaTokens.append(self.conjuction_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[|]", text[self.counter]): #DISYUNCION
                listaTokens.append(self.disyunction_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[/]", text[self.counter]): #DIVISION
                listaTokens.append(self.div_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[\n]", text[self.counter]):#SALTO DE LINEA
                self.counter += 1
                self.line += 1
                self.column = 1 
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
                        listaTokens.append([self.line, self.column, clave, valor.replace('\\','')])
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

    def below_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#MENOR O IGUAL QUE
                
                return self.below_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'menorQue', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'menorQue', word]

    def below_equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):##MENOR O IGUAL QUE
                return self.below_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'menorIgualQue', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'menorIgualQue', word]
#----------------------------------------------------------------------------------------------------------------------------

    def conjuction_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[&]", text[self.counter]):#CONJUNCION
                
                return self.conjuction_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'conjuncion', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'conjuncion', word]
#----------------------------------------------------------------------------------------------------------------------------

    def disyunction_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[|]", text[self.counter]):#DISYUNCION
                
                return self.disyunction_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'disyuncion', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'disyuncion', word]
#----------------------------------------------------------------------------------------------------------------------------  
    def plus_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[+]", text[self.counter]):#MENOR O IGUAL QUE                
                return self.increment_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'mas', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'mas', word]

    def increment_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'incremento', word]
#----------------------------------------------------------------------------------------------------------------------------
    def substracion_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[-]", text[self.counter]):#MENOR O IGUAL QUE               
                return self.decrement_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'menos', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'menos', word]

    def decrement_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'decremento', word]
#----------------------------------------------------------------------------------------------------------------------------
    def above_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#MENOR O IGUAL QUE
                return self.above_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'mayorQue', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'mayorQue', word]

    def above_equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):##MENOR O IGUAL QUE
                return self.above_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'mayorIgualQue', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'mayorIgualQue', word]
#----------------------------------------------------------------------------------------------------------------------------

    def equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#MENOR O IGUAL QUE
                return self.equal_equal_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[>]", text[self.counter]):#IMPLEMENTACION
                return self.implementation_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'igual', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'igual', word]

    def equal_equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'igualdad', word]

    def implementation_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'implementacion', word]
#----------------------------------------------------------------------------------------------------------------------------

    def div_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\/]", text[self.counter]):
                return self.uniline_state(linea, columna, text, word + text[self.counter])
            if re.search(r"[\*]", text[self.counter]):
                return self.multiline_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'division', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'division', word]


    def uniline_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\S]", text[self.counter]):
                return self.uniline_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[ \t]", text[self.counter]):
                
                return self.uniline_state(linea, columna, text, word + text[self.counter])

            else:

                return [linea, columna, 'comentario unilinea', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'comentario unilinea', word]
#----------------------------------------------------------------------------------------------------------------------------
    def multiline_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1

        if self.counter < len(text):
            if re.search(r"(.|\s)*[^\*]", text[self.counter]):
                if re.search(r"[\n]", text[self.counter]):
                    self.line+=1
                    return self.multiline_state(linea, columna, text, word + text[self.counter])
                return self.multiline_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"[ \t]", text[self.counter]):
                return self.multiline_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[\*]", text[self.counter]):
                return self.final_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'nada', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'nada', word]

    def final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        
        if self.counter < len(text):
            if re.search(r"[\/]", text[self.counter]):
                return self.final_final_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'nadaA', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'nada', word]

    def final_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'comentario multilinea',  word]
#----------------------------------------------------------------------------------------------------------------------------

    def not_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#NOT
                return self.difference_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'not', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'not', word]

    def difference_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#DIFERENCIA
                return self.above_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'diferencia', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'diferencia', word]  
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
    def simple_string_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)*[^\']", text[self.counter]):
                if re.search(r"[\n]", text[self.counter]):
                    self.errors.append([self.line, self.column, word])
                    return [None,None,None,None]
                return self.simple_string_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[ \t]", text[self.counter]):
                return self.simple_string_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[\']", text[self.counter]):
                return self.simple_string_final_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'cadena simple con error', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'cadena simple con error', word]

    def simple_string_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'cadena simple',  word]
#----------------------------------------------------------------------------------------------------------------------------
    def double_string_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1

        if self.counter < len(text):
            if re.search(r"(.|\s)*[^\"]", text[self.counter]):
                if re.search(r"[\n]", text[self.counter]):
                    self.errors.append([self.line, self.column, word])
                    return [None,None,None,None]
                return self.double_string_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"[ \t]", text[self.counter]):
                return self.double_string_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[\"]", text[self.counter]):
                return self.double_string_final_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'cadena doble con error', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'cadena doble con error', word]

    def double_string_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'cadena doble',  word]

    def double_string_error_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'identificador', word]   
#----------------------------------------------------------------------------------------------------------------------------

    def verification_reserved(self,TokenList):
        for token in TokenList:
            if token[2] == 'identificador':
                for reservada in self.reserved:
                    palabra = r"^" + reservada + "$"
                    if re.match(palabra, token[3], re.IGNORECASE):
                        token[2] = 'reservada'
                        break

    def receive_input(self):
        tokens = self.initial_state(self.cadena)
        self.verification_reserved(tokens)
        for token in tokens:
            self.token_output.append(token)
        for error in self.errors:
            self.error_output.append(error)
            self.clean = re.sub(error[2], '', self.cadena)
