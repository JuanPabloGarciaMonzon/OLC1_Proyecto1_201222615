from consArbol import consArbol
from tranTabla import tranTabla
import json
import sigTabla


class principal:

    def __init__(self, ER):
        # METODO DEL ARBOL

        '''
        Pasos del metodo del arbol:
            1. Aumentar la ER con el simbolo de aceptacion #
            2. Construir el arbol
            3. Numerar cada hoja
            4. Encontrar los anulables
            5. Tabla de primeros y ultimos
            6. Tabla de siguientes
            7. Tabla de transiciones y diagrama de estados
        '''

        # La ER estara en prefijo
        # a . b -> . a b 
        # se aceptara el . | *

        ER = ER + "#"

        ca = consArbol(ER)
        raiz = ca.getRaiz()

        raiz.getNodo()
        raiz.siguientes()
        print("==============================TABLA SEGUIENTES==============================")
        sigTabla.impTabla()
        tran = tranTabla(raiz)
        print("=============================TABLA TRANSICIONES=============================")
        tran.impTabla()
        tran.grafo()
    #END
#END


if __name__ == "__main__":
    #ER = "....ab*b*|ab"
    #String 
    ER = "..."+"\""+"*|"+"°"+"S"+"\""
    #Identificador
    #ER = "..D*D"
    #Unilinea
    #ER= "...." + "//" + "*°" +"n"
    #Multilinea
    #ER = "...../°*|°S°/"
    p = principal(ER)
