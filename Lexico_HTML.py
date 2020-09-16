import os
import platform
import re
class lex_HTML():
    
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
        "html","head","title","body","h1","h2","h3","h4","h5","h6",
        "p", "br","img","a","href","ol","ul","li","table","th","tr","td",
        "caption","colgroup","col","thead","tbody","tfoot"]

        self.signs = {
        "PUNTOCOMA":'\;', "COMA":'\,', "LLAVEA":'\{', "LLAVEC":'\}', 
        "PARA":'\(', "PARC":'\)', "DIV":'\/', "PUNTO":'\.',"DPUNTO":'\:',
        "TAGA":'\<',"TAGCI":'\>',"IGUAL":"\="}

    def initial_state(self,text):
        self.line = 1
        self.column = 1
        self.listaTokens = []

        while self.counter < len(text):
            if re.search(r"[A-Za-z\_\-]", text[self.counter]): #IDENTIFICADOR
                self.listaTokens.append(self.identifier_state(self.line,self.column,text, text[self.counter]))
            elif re.search(r"[0-9]", text[self.counter]): #NUMERO
                self.listaTokens.append(self.number_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\']", text[self.counter]): #CADENA
                self.listaTokens.append(self.simple_string_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\"]", text[self.counter]): #CADENA
                self.listaTokens.append(self.double_string_state(self.line, self.column, text, text[self.counter]))          
            elif re.search(r"[\>]", text[self.counter]): #TAG DE CIERRE
                self.listaTokens.append([self.line, self.column,"operador",">"])
                self.listaTokens.append(self.tag_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\<]", text[self.counter]): #TAG DE CIERRE
                self.listaTokens.append(self.comment_state(self.line, self.column, text, text[self.counter]))
            elif re.search(r"[\/]", text[self.counter]): #DIVISION
                self.listaTokens.append(self.div_state(self.line, self.column, text, text[self.counter]))
                
            elif re.search(r"[\n]", text[self.counter]):#SALTO DE LINEA
                self.counter += 1
                self.line += 1
                self.column = 1
                self.listaTokens.append([self.line, self.column, "salto", "\n"])
            elif re.search(r"[ \t]", text[self.counter]):#ESPACIOS Y TABULACIONES
                self.counter += 1
                self.column += 1
                self.listaTokens.append([self.line, self.column, "espacio", " \t"])
            elif re.search(r"[\r]", text[self.counter]):#ESPACIOS Y TABULACIONES
                self.counter += 1
                self.column += 1  
            else:
            #SIGNOS
                isSign = False
                for clave in self.signs:
                    valor = self.signs[clave]
                    if re.search(valor, text[self.counter]):
                        self.listaTokens.append([self.line, self.column, "operador", valor.replace('\\','')])
                        self.counter += 1
                        self.column += 1
                        isSign = True
                        break
                if not isSign:
                    self.column += 1
                    self.errors.append([self.line, self.column, text[self.counter]])
                    self.counter += 1
        return self.listaTokens
#----------------------------------------------------------------------------------------------------------------------------
    def identifier_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9\_]", text[self.counter]):#IDENTIFICADOR
                return self.identifier_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'identificador', word]
        else:
            return [linea, columna, 'identificador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def tag_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)*[^\<]", text[self.counter]):
                if re.search(r"[\n]",text[self.counter]):
                    self.line+=1
                return self.tag_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[\<]", text[self.counter]):
                return self.final_final_state(linea, columna, text, word + text[self.counter])
                    
            else:
                return [None,None,None,None]
        else:
            return [None,None,None,None]

    def final_final_state (self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\/]", text[self.counter]):
                return self.final_final_final_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[\<]", text[self.counter]):
                return self.final_final_final_state(linea, columna, text, word + text[self.counter])
                    
            else:
                self.listaTokens.append([linea,columna,"TAG",word[1:-1]])
                return [linea, columna, 'operador',  "<"]
        else:
            return [linea, columna, 'operador',  word[2]]

    def final_final_final_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            self.listaTokens.append([linea,columna,"TAG",word[1:-2]])         
            return [linea, columna, 'operador',  "</"]
#----------------------------------------------------------------------------------------------------------------------------
    def identifier_state(self,linea, columna, text, word):

        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9\_]", text[self.counter]):#IDENTIFICADOR
                return self.identifier_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'identificador', word]
        else:
            return [linea, columna, 'identificador', word]
#----------------------------------------------------------------------------------------------------------------------------
    def comment_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\!]", text[self.counter]):
                return self.Ca_state(linea, columna, text, word + text[self.counter])                   
            else:
                return [linea, columna, 'operador',  word]
        else:
            return [linea, columna, 'operador',  word]

    def Ca_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\-]", text[self.counter]):
                return self.Caa_state(linea, columna, text, word + text[self.counter])
                    
            else:
                return [linea, columna, 'operador',  word]
        else:
            return [linea, columna, 'operador',  word]


    def Caa_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\-]", text[self.counter]):
                return self.Cb_state(linea, columna, text, word + text[self.counter])
                    
            else:
                return [linea, columna, 'operador',  word]
        else:
            return [linea, columna, 'operador',  word]


    def Cb_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"(.|\s)", text[self.counter]):
                if re.search(r"[\-]", text[self.counter]):
                    return self.Cc_state(linea, columna, text, word + text[self.counter])
                return self.Cb_state(linea, columna, text, word + text[self.counter])
                    
            else:
                return [linea, columna, 'identificadorb',  word]
        else:
            return [linea, columna, 'identificadorb',  word]

    def Cc_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\-]", text[self.counter]):
                return self.Cd_state(linea, columna, text, word + text[self.counter])
                    
            else:
                return self.Cc_state(linea, columna, text, word + text[self.counter])
        else:
            return [linea, columna, 'identificadorc',  word]

    def Cd_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\>]", text[self.counter]):
                return self.Ce_state(linea, columna, text, word + text[self.counter])
                    
            else:
                return self.Cd_state(linea, columna, text, word + text[self.counter])
        else:
            return [linea, columna, 'identificadord', word]

    def Ce_state (self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):       
            return [linea, columna, 'comentario',  word]
#----------------------------------------------------------------------------------------------------------------------------
    def div_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\/]", text[self.counter]):
                return self.uniline_state(linea, columna, text, word + text[self.counter])
            else:
                return [linea, columna, 'operador', word]
        else:
            return [linea, columna, 'operador', word]

    def uniline_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
        if self.counter < len(text):
            if re.search(r"[\S]", text[self.counter]):
                return self.uniline_state(linea, columna, text, word + text[self.counter])
            elif re.search(r"[ \t]", text[self.counter]):
                
                return self.uniline_state(linea, columna, text, word + text[self.counter])

            else:

                return [linea, columna, 'comentario', word]
        else:
            return [linea, columna, 'comentario', word]
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
        else:
            return [linea, columna, 'integer', word]

    def decimal_state(self,linea, columna, text, word):
        self.counter += 1
        self.column += 1
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
                self.clean+=str(token[3])
        for error in self.errors:
            counter+=1          
            self.error_output.append(error)          
            self.error_list[len(self.error_output)] = {'count':str(counter), 'column':str(error[1]) ,"line":str(error[0]),'Descripcion':str(error[2])}
#----------------------------------------------------------------------------------------------------------------------------

        


        
