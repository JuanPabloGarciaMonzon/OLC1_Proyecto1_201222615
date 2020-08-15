import re
import tkinter as tk
from interfaz import Interfaz
from copy import copy

class regularExpressions():


### Hay que corregir los binarios y hexadecimales
    categoriasTokens = {
    "comentarios": r"\(\*(.|\s)*\*\)|\/\/\/.*",
    "numeros": r"0b[0-1]+|0[0-7]+|0x([0-9]|[a-f]|[A-F])+|(?!0)\d{1,}|0",
    "palabrasReservadas": r"_if|_while|_main"
    }
    categoriasNumeros ={
    "decimal": r"(?!0)\d{1,}|0(\s|$)",
    "binario": r"0b[0-1]+",
    "octal": r"0[0-7]+",
    "hexadecimal": r"0x([0-9]|[a-f]|[A-F])+"
    }

    def clasificarTokens(self,tokensEncontrados):
        Tokens = []
        for token in tokensEncontrados:

            cadena = token.group()
            if (self.esComentario(cadena)):
                Tokens.append( ("comentario", cadena))
            else:
                Tokens.append(("simbolo", cadena))
        return Tokens

    def esComentario (self,cadena):
        return re.match(self.categoriasTokens["comentarios"],cadena)

    def result(self):

        res = tk.Tk()
        displayclass = Interfaz(res)
        entrada = displayclass.text.get(1.0, tk.END)       
        regexTokens = r"\(\*(.|\s)*\*\)|\/\/\/.*|0b[0-1]+|0[0-7]+|0x([0-9]|[a-f]|[A-F])+|(?!0)\d{1,}|0|_if|_while|_main|[A-z]{1}(\d|\w)*"
    #f = open("C:/Users/juanpi/Downloads/analizadorLexico-master/entrada.txt",'r')
    #entrada = f.read()
        tokensEncontrados = re.finditer(regexTokens,entrada)
        Tokens = self.clasificarTokens(tokensEncontrados)

        Tabla = """\
    +---------------------------------------------+
    | Tipo                 |                 Valor|
    |---------------------------------------------|
    {}
    +---------------------------------------------+\
    """
        Tabla = (Tabla.format('\n'.join("| {:<20} | {:>20} |".format(*fila)
         for fila in Tokens)))

        displayclass.terminal.insert(tk.INSERT,Tabla)
