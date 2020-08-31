import os
import platform
import re
class lex_CSS():
    
    def __init__(self): 
        self.cadena = " "
        self.clean = " "
        self.line = 0 
        self.column = 0
        self.counter = 0
        self.errors = []
        self.token_output = []
        self.error_output = []
        self.error_list={}
        self.reserved = [
        #Control Sentences
        "color","background-color","background-image",
        "border","opacity","background",
        "text-align","font-family","font-style", 
        "font-weight","font-size","font",
        "padding-left","padding-right","padding-bottom",
        "padding-top","padding","display",
        "line-height","widht","height",
        "margin-top","magin-right","margin-bottom",
        "margin-left","margin","border-style",
        "display","position","bottom",
        "top","right","left",
        "float","clear","max-width",
        "min-width","max-height","min-height",
        "content","url","rgba",
        "inline-block","relative","absolute",
        "solid","inherit",
        "px","em","vh",
        "vw","in","cm",
        "mm","pt","pc"]

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
            elif re.search(r"\#", text[self.counter]): #NUMERO
                listaTokens.append(self.numeral_state(self.line, self.column, text, text[self.counter]))                
            elif re.search(r"[0-9]", text[self.counter]): #NUMERO
                listaTokens.append(self.number_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\']", text[self.counter]): #CADENA
                listaTokens.append(self.simple_string_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\"]", text[self.counter]): #CADENA
                listaTokens.append(self.double_string_state(self.line, self.column, text, text[self.counter]))          

            elif re.search(r"[=]", text[self.counter]): #IGUAL o IGUALDAD
                listaTokens.append(self.equal_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[+]", text[self.counter]): #MAS O INCREMENTO
                listaTokens.append(self.plus_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[-]", text[self.counter]): #MENOS O DECREMENTO
                listaTokens.append(self.substracion_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[/]", text[self.counter]): #DIVISION
                listaTokens.append(self.div_state(self.line, self.column, text, text[self.counter]))

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
            if re.search(r"[a-zA-Z_0-9\-]", text[self.counter]):#IDENTIFICADOR
                return self.identifier_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'identificador', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'identificador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def numeral_state(self,linea, columna, text, word):
        contador = 0
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-F_0-9]", text[self.counter]):#IDENTIFICADOR                                  
                return self.hexadecimal_state(linea, columna, text, word + text[self.counter])
            else:
                self.errors.append([self.line, self.column, word])
                return [None,None,None,None]
                #agregar automata de identificador en el arbol, con el valor
        else:
            self.errors.append([self.line, self.column, word])
            return [None,None,None,None]

    def hexadecimal_state(self,linea, columna, text, word):
        contador = 0
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-F_0-9\-]", text[self.counter]):#IDENTIFICADOR                                  
                return self.hexadecimal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'identificador', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'identificador', word]
#----------------------------------------------------------------------------------------------------------------------------  
    def plus_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[+]", text[self.counter]):#MENOR O IGUAL QUE                
                return self.increment_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'operador', word]

    def increment_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'operador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def substracion_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[-]", text[self.counter]):#MENOR O IGUAL QUE               
                return self.decrement_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'operador', word]

    def decrement_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'operador', word]
#----------------------------------------------------------------------------------------------------------------------------

    def equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'operador', word]
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
                return [linea, columna, 'operador', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [linea, columna, 'operador', word]
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
                return self.multiline_state(linea, columna, text, word + text[self.counter])
                #agregar automata de identificador en el arbol, con el valor
        else:
            self.errors.append([self.line, self.column, "/*"])
            return [None,None,None,None]

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
            return [linea, columna, 'comentario',  word]
#----------------------------------------------------------------------------------------------------------------------------

    def number_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#ENTERO
                return self.number_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"\.", text[self.counter]):#DECIMAL
                return self.decimal_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"\%", text[self.counter]):#DECIMAL
                return self.percent_state(linea, columna, text, word + text[self.counter])
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
            elif re.search(r"\%", text[self.counter]):#DECIMAL
                return self.percent_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'decimal', word]
                #agregar automata de decimal en el arbol, con el valor
        else:
            return [linea, columna, 'decimal', word]

    def percent_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'porcentaje', word]

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
            return [linea, columna, 'string',  word]
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
            return [linea, columna, 'string',  word]
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
        counter = 0
        for token in tokens:
            self.token_output.append(token)
            if(token[0]!=None):
                self.clean+=" "+str(token[3])
            # self.clean+=str(token[3])
        for error in self.errors:
            counter+=1          
            self.error_output.append(error)          
            self.error_list[len(self.error_output)] = {'count':str(counter), 'column':str(error[1]) ,"line":str(error[0]),'Descripcion':str(error[2])}
#----------------------------------------------------------------------------------------------------------------------------

        


        
