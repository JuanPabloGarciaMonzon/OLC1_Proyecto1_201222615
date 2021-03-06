import os
import platform
import re
import Grafo

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
        self.error_list={}
        self.reserved = [
        #Control Sentences
        "if","else","for","while","do",
        "continue","break","return",
        "class", "function","constructor"]

        self.signs = {
        "PUNTOCOMA":'\;', "COMA":'\,', "LLAVEA":'\{', "LLAVEC":'\}', 
        "PARA":'\(',"POR":'\*', "PARC":'\)', "PUNTO":'\.',"DPUNTO":'\:',"MAS":'\+',"MENOS":'\-'}

    def initial_state(self,text):
        self.line = 1
        self.column = 1
        self.flag_id = False
        self.flag_comment = False
        self.flag_multicomment = False
        self.flag_string = False
        self.flag_decimal = False
        self.flag_number = False
        self.flag_char = False
        listaTokens = []

        while self.counter < len(text):
            if re.search(r"[A-Za-z\_]", text[self.counter]): #IDENTIFICADOR
                listaTokens.append(self.identifier_state(self.line,self.column,text, text[self.counter]))

            elif re.search(r"[0-9]", text[self.counter]): #NUMERO
                listaTokens.append(self.number_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[\']", text[self.counter]): #CHAR
                listaTokens.append(self.simple_string_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[\"]", text[self.counter]): #STRING
                listaTokens.append(self.double_string_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[<]", text[self.counter]): #MENOR  O MENOR IGUAL QUE
                listaTokens.append(self.below_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[>]", text[self.counter]): #MAYOR  O MAYOR IGUAL QUE
                listaTokens.append(self.above_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[=]", text[self.counter]): #IGUAL o IGUALDAD
                listaTokens.append(self.equal_state(self.line, self.column, text, text[self.counter]))
            
            elif re.search(r"[!]", text[self.counter]): #NOT o DIFERENCIA
                listaTokens.append(self.not_state(self.line, self.column, text, text[self.counter]))
            
            elif re.search(r"[&]", text[self.counter]): #CONJUNCION
                listaTokens.append(self.amperson_state(self.line, self.column, text, text[self.counter]))
            
            elif re.search(r"[|]", text[self.counter]): #DISYUNCION
                listaTokens.append(self.pipe_state(self.line, self.column, text, text[self.counter]))
            
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
                listaTokens.append([self.line, self.column, "espacio", "\t"])
            elif re.search(r"[\r]", text[self.counter]):#CARREO
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
        IDr = Grafo.grafica()
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9\_]", text[self.counter]):#IDENTIFICADOR
                return self.identifier_state(linea, columna, text, word + text[self.counter])
            else:
                if(self.flag_id==False):
                    IDr.grafoID()
                    self.flag_id=True                    
                return [linea, columna, 'identificador', word]
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
                return [linea, columna, 'operador', word]
                
        else:
            return [linea, columna, 'operador', word]

    def below_equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):##MENOR O IGUAL QUE
                return self.below_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
                
        else:
            return [linea, columna, 'operador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def amperson_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[&]", text[self.counter]):#CONJUNCION               
                return self.conjuction_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
        else:
            return [linea, columna, 'operador', word]

    def conjuction_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'operador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def pipe_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[|]", text[self.counter]):#CONJUNCION                
                return self.disyunction_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
        else:
            return [linea, columna, 'operador', word]

    def disyunction_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'operador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def above_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#MENOR O IGUAL QUE
                return self.above_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
        else:
            return [linea, columna, 'operador', word]

    def above_equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):##MENOR O IGUAL QUE
                return self.above_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
        else:
            return [linea, columna, 'operador', word]
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
                return [linea, columna, 'operador', word]
        else:
            return [linea, columna, 'operador', word]

    def equal_equal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            return [linea, columna, 'operador', word]

    def implementation_state(self,linea, columna, text, word):
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

            elif re.search(r"[\*]", text[self.counter]):
                return self.B_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
        else:
            return [linea, columna, 'operador', word]

    def uniline_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        Uni = Grafo.grafica()
        if self.counter < len(text):
            if re.search(r"(.)", text[self.counter]):
                return self.uniline_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"[\n]", text[self.counter]):
                if(self.flag_comment==False):
                    Uni.grafoUniComment()
                    self.flag_comment=True                
                return [linea, columna, 'comentario', word]

        else:
            return [linea, columna, 'comentario', word]
#----------------------------------------------------------------------------------------------------------------------------
    def B_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\*]", text[self.counter]):
                return self.C_state(linea, columna, text, word + text[self.counter])

            else:
                return self.C_state(linea, columna, text, word + text[self.counter])
        else:
            return self.C_state(linea, columna, text, word + text[self.counter])

    def C_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)", text[self.counter]):
                return self.D_state(linea, columna, text, word + text[self.counter])

            else:
                return [linea, columna, 'operador2', word]
        else:
            return [linea, columna, 'operador', word]

    def D_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)", text[self.counter]):
                if re.search(r"[\*]", text[self.counter]):
                    return self.E_state(linea, columna, text, word + text[self.counter])
                return self.D_state(linea, columna, text, word + text[self.counter])

            else:
                return [linea, columna, 'operador3', word]
        else:
            self.errors.append([self.line, self.column, word])
            return [None,None,None,None]

    def E_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\/]", text[self.counter]):
                if re.search(r"[a-zA-Z_0-9_._\=_^\/]", text[self.counter+1]):
                    return self.E_state(linea, columna, text, word + text[self.counter])
                return self.F_state(linea, columna, text, word + text[self.counter])

            else:
                if re.search(r"[\n]", text[self.counter]):                    
                    self.line+=1 
                return self.E_state(linea, columna, text, word + text[self.counter])                
        else:         
            return [linea, columna, 'operador', word]

    def F_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        Multi = Grafo.grafica()
        if self.counter < len(text):
            if(self.flag_multicomment==False):
                Multi.grafoMultiComment()
                self.flag_multicomment=True

            return [linea, columna, 'comentario',  word]
#----------------------------------------------------------------------------------------------------------------------------
    def not_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#NOT
                return self.difference_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
                
        else:
            return [linea, columna, 'operador', word]

    def difference_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[=]", text[self.counter]):#DIFERENCIA
                return self.above_equal_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
                
        else:
            return [linea, columna, 'operador', word]  
#----------------------------------------------------------------------------------------------------------------------------
    def number_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        Nmber = Grafo.grafica()
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#ENTERO
                return self.number_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"\.", text[self.counter]):#DECIMAL
                return self.decimal_state(linea, columna, text, word + text[self.counter])

            else:
                if(self.flag_number==False):
                    Nmber.grafoNumber()
                    self.flag_number=True

                return [linea, columna, 'integer', word]
        else:
            return [linea, columna, 'integer', word]

    def decimal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        Deci = Grafo.grafica()
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#DECIMAL
                return self.decimal_final_state(linea, columna, text, word + text[self.counter])
            else:
                self.errors.append([self.line, self.column, word])
                return [None,None,None,None]
        else:
            self.errors.append([self.line, self.column, word])
            return [None,None,None,None]

    def decimal_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        Deci = Grafo.grafica()
        if self.counter < len(text):
            if(self.flag_decimal==False):
                Deci.grafoDecimal()
                self.flag_decimal=True
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
                
        else:
            return [linea, columna, 'cadena simple con error', word]

    def simple_string_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        Char = Grafo.grafica()
        if self.counter < len(text):
            if(self.flag_char==False):
                Char.grafoChar()
                self.flag_char=True
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
                
        else:
            return [linea, columna, 'cadena doble con error', word]

    def double_string_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        doublestring = Grafo.grafica()
        if self.counter < len(text):

            if(self.flag_string==False):
                doublestring.grafoString()
                self.flag_string=True

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
                self.clean+=str(token[3])
        for error in self.errors:
            counter+=1          
            self.error_output.append(error)          
            self.error_list[len(self.error_output)] = {'count':str(counter), 'column':str(error[1]) ,"line":str(error[0]),'Descripcion':str(error[2])}
#----------------------------------------------------------------------------------------------------------------------------

        


        
