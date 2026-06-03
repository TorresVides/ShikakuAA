# solucionador.py

class SolucionadorShikaku:
    def __init__(self, tablero):
        self.tablero = tablero
        self.candidatos = tablero.candidatos_todas_pistas()
        self.solucion = []

        self.llamadas_recursivas = 0
        self.rectangulos_probados = 0

        self.estados_fallidos = set()
        self.estados_memoizados = 0
        self.podas_memoizacion = 0

        self.mascara_total = (1 << (self.tablero.filas * self.tablero.cols)) - 1

    def resolver(self):
        self.solucion = []

        self.llamadas_recursivas = 0
        self.rectangulos_probados = 0
        self.estados_fallidos = set()
        self.estados_memoizados = 0
        self.podas_memoizacion = 0

        if self._backtracking(0, [], 0):
            return self.solucion

        return None

    def _backtracking(self, indice, seleccionados, mascara_ocupada):
        self.llamadas_recursivas += 1

        estado = (indice, mascara_ocupada)

        if estado in self.estados_fallidos:
            self.podas_memoizacion += 1
            return False

        if indice == len(self.candidatos):
            if mascara_ocupada == self.mascara_total:
                self.solucion = list(seleccionados)
                return True

            self.estados_fallidos.add(estado)
            self.estados_memoizados = len(self.estados_fallidos)
            return False

        fila, col, valor, candidatos = self.candidatos[indice]

        for rectangulo in candidatos:
            self.rectangulos_probados += 1

            mascara_rectangulo = self.obtener_mascara_rectangulo(rectangulo)

            if mascara_ocupada & mascara_rectangulo == 0:
                seleccionados.append(rectangulo)

                nueva_mascara = mascara_ocupada | mascara_rectangulo

                if self._backtracking(indice + 1, seleccionados, nueva_mascara):
                    return True

                seleccionados.pop()

        self.estados_fallidos.add(estado)
        self.estados_memoizados = len(self.estados_fallidos)

        return False

    def obtener_mascara_rectangulo(self, rectangulo):
        mascara = 0

        for fila, col in rectangulo.ocupadas():
            indice = fila * self.tablero.cols + col
            mascara = mascara | (1 << indice)

        return mascara

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
