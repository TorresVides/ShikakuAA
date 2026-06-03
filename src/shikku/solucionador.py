# solucionador.py

class SolucionadorShikaku:
    def __init__(self, tablero):
        self.tablero = tablero
        self.candidatos = tablero.candidatos_todas_pistas()
        self.solucion = []
        self.llamadas_recursivas = 0
        self.rectangulos_probados = 0

    def resolver(self):
        self.solucion = []

        if self._backtracking(0, []):
            return self.solucion

        return None

    def _backtracking(self, indice, seleccionados):
        self.llamadas_recursivas += 1

        if indice == len(self.candidatos):
            if self.cubre_todo_tablero(seleccionados):
                self.solucion = list(seleccionados)
                return True

            return False

        fila, col, valor, candidatos = self.candidatos[indice]

        for rectangulo in candidatos:
            self.rectangulos_probados += 1

            if self.no_solapa(rectangulo, seleccionados):
                seleccionados.append(rectangulo)

                if self._backtracking(indice + 1, seleccionados):
                    return True

                seleccionados.pop()

        return False

    def no_solapa(self, rectangulo, seleccionados):
        for otro in seleccionados:
            if rectangulo.solapados(otro):
                return False

        return True

    def cubre_todo_tablero(self, seleccionados):
        celdas_ocupadas = set()

        for rectangulo in seleccionados:
            for celda in rectangulo.ocupadas():
                celdas_ocupadas.add(celda)

        total_celdas = self.tablero.filas * self.tablero.cols

        return len(celdas_ocupadas) == total_celdas
