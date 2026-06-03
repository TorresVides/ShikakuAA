# tablero.py
from src.shikku.rectangulo import Rectangulo

class TableroShikaku:
    def __init__(self, celdas):
        
        self.celdas = celdas
        self.filas = len(celdas)
        self.cols = len(celdas[0])

    def mostrar_tablero(self):
        for f in range(self.filas):
            fila_texto = ""

            for c in range(self.cols):
                valor = self.celdas[f][c]

                if valor == 0:
                    fila_texto += ". "
                else:
                    fila_texto += str(valor) + " "

            print(fila_texto)

    def esta_dentro(self, fila, col):
        if 0 <= fila < self.filas and 0 <= col < self.cols:
            return True

        return False

    def pistas(self):
        pistas = []
        for f in range(self.filas):
            for c in range(self.cols):
                valor = self.celdas[f][c]
                if  valor != 0:
                    pistas.append((f, c, valor))
        
        return pistas
        
    def rectanguloDentro(self, otro):
        for fila, col in otro.ocupadas():
            if not self.esta_dentro(fila, col):
                return False
     
        return True
    
    def contarPistasR(self, otro):
        n_pistas = 0

        for f, c in otro.ocupadas():
            if self.esta_dentro(f, c):
                valor = self.celdas[f][c]

                if valor != 0:
                    n_pistas += 1

        return n_pistas


    def rectValidoP(self, rectangulo, fila_pista, col_pista, valor_pista):

        if not self.rectanguloDentro(rectangulo):
            return False

        if not rectangulo.contiene(fila_pista, col_pista):
            return False

        if rectangulo.area() != valor_pista:
            return False

        if self.contarPistasR(rectangulo) != 1:
            return False


        return True

    def candidatos_pista(self, fila_pista, col_pista, valor_pista):
        candidatos = []

        for alto in range(1, valor_pista + 1):
            if valor_pista % alto == 0:
                base = valor_pista // alto

                for fila_inicio in range(fila_pista - alto + 1, fila_pista + 1):
                    for col_inicio in range(col_pista - base + 1, col_pista + 1):

                        rectangulo = Rectangulo(fila_inicio, col_inicio, alto, base)

                        if self.rectValidoP(rectangulo, fila_pista, col_pista, valor_pista):
                            candidatos.append(rectangulo)

        return candidatos

    def candidatos_todas_pistas(self):
        todos = []

        for fila, col, valor in self.pistas():
            candidatos = self.candidatos_pista(fila, col, valor)
            todos.append((fila, col, valor, candidatos))

            todos.sort(key=lambda elemento: len(elemento[3]))   

        return todos

    def mostrar_solucion(self, solucion):
        tablero_salida = []

        for f in range(self.filas):
            fila = []
            for c in range(self.cols):
                fila.append(".")
            tablero_salida.append(fila)

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for i in range(len(solucion)):
            rectangulo = solucion[i]

            if i < len(letras):
                etiqueta = letras[i]
            else:
                etiqueta = str(i)

            for f, c in rectangulo.ocupadas():
                tablero_salida[f][c] = etiqueta

        for fila in tablero_salida:
            print(" ".join(fila))



