import os
import re
from enum import Enum
class Token():

    def Tipo (Enum):
        INTEGER
        DECIMAL
        MAS
        MENOS
        POR
        DIV
        PARA
        PARC
        ID
        
    def __init__(self,tipo,valor):
        self.tipoT = self.Tipo()

        self.tipoT = tipo
        self.valor = valor

    def getTipo(self):
        return self.tipoT

    def getValor(self):
        return self.valor

    def getTipoEnString(self):
        
        if self.tipoT == "NUMERO":
            return "Numero"
        elif self.tipoT == "MAS":
            return "Mas"
        elif self.tipoT == "MENOS":
            return "Menos"
        elif self.tipoT == "POR":
            return "Por"
        elif self.tipoT == "DIV":
            return "Division"
        elif self.tipoT == "PARA":
            return "Para"
        elif self.tipoT == "PARC":
            return "Parc"
        elif self.tipoT == "ID":
            return "Id"
        else:
            return None
