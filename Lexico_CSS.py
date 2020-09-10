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
        self.states = []
        self.token_output = []
        self.error_output = []
        self.state_output = []
        self.error_list={}
        self.state_list={}
        self.reserved = [
        "color","background-color","background-image","border","opacity","background",
        "text-align","font-family","font-style", "font-weight","font-size","font",
        "padding-left","padding-right","padding-bottom","padding-top","padding","display",
        "line-height","widht","height","margin-top","magin-right","margin-bottom",
        "margin-left","margin","border-style","display","position","bottom",
        "top","right","left","float","clear","max-width",
        "min-width","max-height","min-height","content","url","rgba",
        "inline-block","relative","absolute","solid","inherit",
        "px","em","vh","vw","in","cm","mm","pt","pc"]

        self.signs = {
        "PUNTOCOMA":'\;', "COMA":'\,', "LLAVEA":'\{', "LLAVEC":'\}', 
        "PARA":'\(',"POR":'\*', "PARC":'\)', "PUNTO":'\.',"DPUNTO":'\:',"PORCENTAJE":'\%'}

    def initial_state(self,text):

        self.line = 1
        self.column = 1
        listaTokens = []

        while self.counter < len(text):
            
            if re.search(r"[A-Za-z\-\_]", text[self.counter]): #IDENTIFICADOR
                self.states.append(["id_inicio",text[self.counter]])
                listaTokens.append(self.identifier_state(self.line,self.column,text, text[self.counter]))

            elif re.search(r"\#", text[self.counter]): #HEXADECIMAL
                self.states.append(["numeral_inicio",text[self.counter]])
                listaTokens.append(self.numeral_state(self.line, self.column, text, text[self.counter])) 

            elif re.search(r"[0-9]", text[self.counter]): #NUMERO
                self.states.append(["numero_inicio",text[self.counter]])
                listaTokens.append(self.number_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[\']", text[self.counter]): #CHAR
                self.states.append(["char_inicio",text[self.counter]])
                listaTokens.append(self.simple_string_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[\"]", text[self.counter]): #STRING
                self.states.append(["string_inicio",text[self.counter]])
                listaTokens.append(self.double_string_state(self.line, self.column, text, text[self.counter]))          

            elif re.search(r"[\/]", text[self.counter]): #DIVISION
                self.states.append(["division_inicio",text[self.counter]])
                listaTokens.append(self.div_state(self.line, self.column, text, text[self.counter]))

            elif re.search(r"[\n]", text[self.counter]):#SALTO DE LINEA
                self.counter += 1
                self.line += 1
                self.column = 1
                self.states.append(["salto","\n"])
                listaTokens.append([self.line, self.column, "salto", "\n"])

            elif re.search(r"[ \t]", text[self.counter]):#ESPACIOS Y TABULACIONES
                self.counter += 1
                self.column += 1
                listaTokens.append([self.line, self.column, "espacio", "\t"])

            elif re.search(r"[\r]", text[self.counter]):#ESPACIOS Y TABULACIONES
                self.counter += 1
                self.column += 1  
            else:
            #SIGNOS
                isSign = False
                for clave in self.signs:
                    valor = self.signs[clave]
                    if re.search(valor, text[self.counter]):
                        self.states.append(["operador_aceptacion",text[self.counter]])
                        listaTokens.append([self.line, self.column, "operador", valor.replace('\\','')])
                        self.counter += 1
                        self.column += 1
                        isSign = True
                        break
                if not isSign:
                    self.column += 1
                    self.states.append(["estado_error",text[self.counter]])
                    self.errors.append([self.line, self.column, text[self.counter]])
                    self.counter += 1
        return listaTokens
#----------------------------------------------------------------------------------------------------------------------------
    def identifier_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9\-\_]", text[self.counter]):#IDENTIFICADOR
                self.states.append(["id",str(text[self.counter])])
                return self.identifier_state(linea, columna, text, word + text[self.counter])

            else:
                self.states.append(["id_aceptacion",word])
                return [linea, columna, 'identificador', word]
        else:
            self.states.append(["id_aceptacion",word])
            return [linea, columna, 'identificador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def numeral_state(self,linea, columna, text, word):
        contador = 0
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-fA-F_0-9]", text[self.counter]):#NUMERAL
                self.states.append(["hexadecimal",text[self.counter]])                                  
                return self.hexadecimal_state(linea, columna, text, word + text[self.counter])

            else:
                self.states.append(["numeral_aceptacion",word])
                return [linea, columna, 'operador', word]
        else:
            self.states.append(["numeral_aceptacion",word])
            return [linea, columna, 'operador', word]

    def hexadecimal_state(self,linea, columna, text, word):
        contador = 0
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-fA-F_0-9]", text[self.counter]):#HEXADECIMAL
                self.states.append(["hexadecimal",text[self.counter]])                                  
                return self.hexadecimal_state(linea, columna, text, word + text[self.counter])

            else:
                self.states.append(["hexadecimal_aceptacion",word])
                return [linea, columna, 'hexadecimal', word]
        else:
            self.states.append(["hexadecimal_aceptacion",word])
            return [linea, columna, 'hexadecimal', word]
#----------------------------------------------------------------------------------------------------------------------------
    def div_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\*]", text[self.counter]):#COMENTARIO
                self.states.append(["comentario_inicio",text[self.counter]])
                return self.C_state(linea, columna, text, word + text[self.counter])

            else:
                self.states.append(["division_aceptacion",word])
                return [linea, columna, 'operador', word]
        else:
            self.states.append(["division_aceptacion",word])
            return [linea, columna, 'operador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def B_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\*]", text[self.counter]):
                self.states.append(["comentario",text[self.counter]])
                return self.C_state(linea, columna, text, word + text[self.counter])

            else:
                if re.search(r"[\n]", text[self.counter]):                    
                    self.line+=1
                self.states.append(["comentario",text[self.counter]])
                return self.C_state(linea, columna, text, word + text[self.counter])
        else:
            self.states.append(["comentario",text[self.counter]])
            return self.C_state(linea, columna, text, word + text[self.counter])

    def C_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)", text[self.counter]):
                self.states.append(["comentario",text[self.counter]])
                if re.search(r"[\n]", text[self.counter]):                    
                    self.line+=1
                return self.D_state(linea, columna, text, word + text[self.counter])

            else:
                if re.search(r"[\n]", text[self.counter]):                    
                    self.line+=1
                return [linea, columna, 'operador25', word]
        else:
            return [linea, columna, 'operador25b', word]

    def D_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)*", text[self.counter]):
                self.states.append(["comentario",text[self.counter]])
                if re.search(r"[\n]", text[self.counter]):                    
                    self.line+=1

                elif re.search(r"[\*]", text[self.counter]):
                    self.states.append(["comentario",text[self.counter]])
                    return self.E_state(linea, columna, text, word + text[self.counter])

                return self.D_state(linea, columna, text, word + text[self.counter])
            else:
                if re.search(r"[\n]", text[self.counter]):                    
                    self.line+=1
                return [linea, columna, 'operador35', word]
        else:
            self.errors.append([self.line, self.column, word])
            return [None,None,None,None]

    def E_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\/]", text[self.counter]):
                if re.search(r"[a-zA-Z_0-9_._\=_^\/]", text[self.counter+1]):
                    self.states.append(["comentario",text[self.counter]])
                    return self.E_state(linea, columna, text, word + text[self.counter])
                self.states.append(["comentario",text[self.counter]])
                return self.F_state(linea, columna, text, word + text[self.counter])
            else:
                if re.search(r"[\n]", text[self.counter]):                    
                    self.line+=1
                self.states.append(["comentario",text[self.counter]])
                return self.E_state(linea, columna, text, word + text[self.counter])
        else:
            self.states.append(["comentario_Error",word])         
            self.errors.append([self.line, self.column, word])
            return [None,None,None,None]

    def F_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            self.states.append(["comentario_aceptacion",word])
            return [linea, columna, 'comentario',  word]
#----------------------------------------------------------------------------------------------------------------------------
    def number_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#ENTERO
                self.states.append(["entero",str(text[self.counter])])
                return self.number_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"\.", text[self.counter]):#DECIMAL
                self.states.append(["decimal",str(text[self.counter])])
                return self.decimal_state(linea, columna, text, word + text[self.counter])

            else:
                self.states.append(["entero_aceptacion",word])
                return [linea, columna, 'integer', word]
        else:
            self.states.append(["entero_aceptacion",word])
            return [linea, columna, 'integer', word]

    def decimal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#DECIMAL
                self.states.append(["decimal",str(text[self.counter])])
                return self.decimal_state(linea, columna, text, word + text[self.counter])

            else:
                self.states.append(["decimal_aceptacion",word])
                return [linea, columna, 'decimal', word]
        else:
            self.states.append(["decimal_aceptacion",word])
            return [linea, columna, 'decimal', word]
#----------------------------------------------------------------------------------------------------------------------------
    def simple_string_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)*[^\']", text[self.counter]):
                if re.search(r"[\n]", text[self.counter]):
                    self.states.append(["estadoError_char",text[self.counter]])
                    self.errors.append([self.line, self.column, word])
                    return [None,None,None,None]
                self.states.append(["char",text[self.counter]])
                return self.simple_string_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"[ \t]", text[self.counter]):
                self.states.append(["char",text[self.counter]])
                return self.simple_string_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"[\']", text[self.counter]):
                self.states.append(["char",text[self.counter]])
                return self.simple_string_final_state(linea, columna, text, word + text[self.counter])

            else:
                return [linea, columna, 'cadena simple con error', word]
        else:
            return [linea, columna, 'cadena simple con error', word]

    def simple_string_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            self.states.append(["char_aceptacion",word])
            return [linea, columna, 'string',  word]
#----------------------------------------------------------------------------------------------------------------------------
    def double_string_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1

        if self.counter < len(text):
            if re.search(r"(.|\s)*[^\"]", text[self.counter]):
                if re.search(r"[\n]", text[self.counter]):
                    self.states.append(["estadoError_string",text[self.counter]])
                    self.errors.append([self.line, self.column, word])
                    return [None,None,None,None]
                self.states.append(["string",text[self.counter]])
                return self.double_string_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"[ \t]", text[self.counter]):
                self.states.append(["string",text[self.counter]])
                return self.double_string_state(linea, columna, text, word + text[self.counter])

            elif re.search(r"[\"]", text[self.counter]):
                self.states.append(["string",text[self.counter]])
                return self.double_string_final_state(linea, columna, text, word + text[self.counter])

            else:
                return [linea, columna, 'cadena doble con error', word]
        else:
            return [linea, columna, 'cadena doble con error', word]

    def double_string_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            self.states.append(["string_aceptacion",word])
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
        state_counter = 0
        for token in tokens:
            self.token_output.append(token)
            if(token[0]!=None):
                self.clean+=str(token[3])
        for error in self.errors:
            counter+=1          
            self.error_output.append(error)          
            self.error_list[len(self.error_output)] = {'count':str(counter), 'column':str(error[1]) ,"line":str(error[0]),'Descripcion':str(error[2])}
        for state in self.states:
            state_counter+=1
            self.state_output.append(state)                 
            self.state_list[len(self.state_output)] = {'count':str(state_counter), 'estado':str(state[0]) ,"token":str(state[1])}
#----------------------------------------------------------------------------------------------------------------------------

        


        
