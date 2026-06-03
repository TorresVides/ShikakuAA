# rectangulo.py
class Rectangulo:
    def __init__(self, fila, col, alto, base):
        self.fila = fila
        self.col = col
        self.alto = alto
        self.base = base

    def area(self):
        area = self.alto*self.base
        return area

    def ocupadas(self):
        ocupadas = []

        for f in range(self.fila, self.fila + self.alto):
            for c in range(self.col, self.col + self.base):
                ocupadas.append((f,c))
        return ocupadas

    def contiene(self, fila, col):
        contenidas = self.ocupadas()

        if (fila, col) in contenidas:
            return True

        return False

    def solapados(self, otro):
        ocupadas1 = self.ocupadas()
        ocupadas2 = otro.ocupadas()

        for celda in ocupadas1:
            if celda in ocupadas2:
                return True

        return False  


