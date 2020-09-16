
import os

#     #  S->E R
      #  R-> E R
      #    |EPSILON
#     #' E-> T EP
#     #' EP-> + T EP
#     #'    | - T EP
#     #'    | EPSILON
#     #' T->F TP
#     #' TP-> * F TP
#     #'    | / F TP
#     #'    | EPSILON
#     #' F->  (E) 
#     #'    | NUMERO 
#     #     | ID  


class syn_RMT():

    def S(self):
        #Mandar a llamar a E
        self.E()
        self.R()

    def R(self):
        self.tokenAt = self.list[self.contadorT]
        if(self.contadorT != len(self.list)-1):            
            if(self.tokenAt[2]=="salto" and self.flag == True):
                self.line.append([self.string,"incorrecto",self.tokenAt[0]-1])
                self.string=""
                self.tokenAt = self.nextToken()                
                self.flag = False
                self.E()
                self.R()

            elif(self.tokenAt[2] =="salto" and self.flag == False):
                self.line.append([self.string,"correcto",self.tokenAt[0]-1,self.tokenAt[1]])
                self.string=""
                self.match(self.tokenAt,"salto","SE ESPERABA SALTO")                
                self.E()
                self.R()

            elif(self.tokenAt[2] =="MAS" or self.tokenAt[2] =="MENOS" or self.tokenAt[2] =="POR" or self.tokenAt[2] =="DIV"):
                self.E()
                self.R()
                
            else:
                self.match(self.tokenAt,"MAS","SE ESPERABA SIMBOLO OPERADOR")
                self.E()
                self.R()
        else:
            pass



    def E(self):
        #Mandar a llamar a T
        self.tokenAt = self.list[self.contadorT]       
        if(self.tokenAt[2] == "integer" or self.tokenAt[2] == "identificador"  or self.tokenAt[2] == "decimal" or self.tokenAt[2]=="PARA"):
            self.T()
            self.EP()
        else:
            self.match(self.tokenAt,"integer","SE ESPERABA NUMERO O PARA")



    def EP(self):
        #Miro mi token actual
        self.tokenAt = self.list[self.contadorT]    
        if(self.tokenAt[2] == "MAS"):
            self.match(self.tokenAt,"MAS","SE ESPERABA MAS")
            self.T()
            self.EP()
        elif(self.tokenAt[2] =="MENOS"):
            self.match(self.tokenAt,"MENOS","SE ESPERABA MENOS")
            self.T()
            self.EP()
        else:
            pass 
            
    def T(self):
        #' T->F TP
        #Mandar a llamar a F
        self.F()
        #Mandar a llamar a TP
        self.TP()

    def TP(self):
        #Miro mi token actual
        self.tokenAt= self.list[self.contadorT]
        if(self.tokenAt[2] == "POR"):
            self.match(self.tokenAt,"POR","SE ESPERABA POR")
            self.T()
            self.EP()
        elif (self.tokenAt[2] == "DIV"):
            self.match(self.tokenAt,"DIV","SE ESPERABA DIV")
            self.T()
            self.EP()
        else:
            pass 
            

    def F(self):
        #Miro mi token actual
        self.tokenAt = self.list[self.contadorT]
        if(self.tokenAt[2] == "PARA"):
            self.match(self.tokenAt,"PARA","SE ESPERABA PARA")
            self.E()
            self.match(self.tokenAt,"PARC","SE ESPERABA PARC")
            
        elif (self.tokenAt[2] == "integer"):
            self.match(self.tokenAt,"integer","SE ESPERABA NUMERO")
            
        elif (self.tokenAt[2] == "decimal"):
            self.match(self.tokenAt,"decimal","SE ESPERABA NUMERO")
            
        elif (self.tokenAt[2]== "identificador"):
            self.match(self.tokenAt,"identificador","SE ESPERABA ID")
            
        else:
            self.match(self.tokenAt,"integer","SE ESPERABA NUMERO O PARA")   


    def match(self,tokenAt,simboloE,MensajeErr):
        if(tokenAt[2] == simboloE):
            self.nextToken()
        else:                   
            self.error.append([tokenAt[0],tokenAt[1],MensajeErr,tokenAt[2],tokenAt[3]])
            self.panic()

    def nextToken(self):
            tokenAt2 = self.list[self.contadorT]
            if(tokenAt2[2]!="salto"):
                self.string = self.string + tokenAt2[3]
            if(self.contadorT != len(self.list)-1):
                self.contadorT=self.contadorT + 1
                self.tokenAt = self.list[self.contadorT]
                return self.tokenAt

    def panic(self):
            self.flag = True
            self.tokenAt = self.list[self.contadorT]
            while(self.tokenAt[2]!="salto"):
                self.tokenAt = self.nextToken()
                if(self.contadorT==len(self.list)-1):
                    break




    def __init__(self,lista):
    #Lista de Tokens que el parser recibe del analizador léxico
        self.list = lista
        self.contadorT = 0
        self.contador = 0
        self.flag = False
        self.error = []
        self.line = []
        self.aux = []
        self.errorList = {}
        self.tokenAt = ""
        self.string = ""
        self.S()
        for l in self.line:
            self.contador+=1
            self.aux.append(l)                 
            self.errorList[len(self.aux)] = {'count':str(self.contador), 'L':str(l[2]), 'linea':str(l[0]) ,"resultado":str(l[1])}
