# interfaz.py
import os
import time
import tracemalloc
from src.shikku.rectangulo import Rectangulo
from src.shikku.solucionador import SolucionadorShikaku
from src.shikku.tablero import TableroShikaku


class InterfazShikaku:
    def __init__(self, tablero=None):
        self.tablero = tablero

    def iniciar(self):
        while True:
            print("\n===== SHIKAKU =====")
            print("1. Mostrar tablero")
            print("2. Jugar manualmente")
            print("3. Resolver automáticamente")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.mostrar_tablero()

            elif opcion == "2":
                self.jugar_manual()

            elif opcion == "3":
                self.resolver_automaticamente()

            elif opcion == "4":
                print("Saliendo del programa...")
                break

            else:
                print("Opción inválida.")

    def mostrar_tablero(self):
        print("\nTablero:")
        self.tablero.mostrar_tablero()

    def resolver_automaticamente(self):
        self.preguntar_cambiar_puzzle()

        if not self.asegurar_tablero():
            return

        print("\nResolviendo automáticamente...")

        solucionador = SolucionadorShikaku(self.tablero)

        tracemalloc.start()
        inicio = time.perf_counter()

        solucion = solucionador.resolver()

        fin = time.perf_counter()
        memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tiempo = fin - inicio

        if solucion is None:
            print("No se encontró solución.")
        else:
            print("Solución encontrada:")
            self.tablero.mostrar_solucion(solucion)

        print("Tiempo de ejecución:", round(tiempo, 6), "segundos")
        print("Llamadas recursivas:", solucionador.llamadas_recursivas)
        print("Rectángulos probados:", solucionador.rectangulos_probados)
        print("Memoria pico:", round(memoria_pico / 1024, 4), "KB")

    def jugar_manual(self):

        self.preguntar_cambiar_puzzle()

        if not self.asegurar_tablero():
            return

        print("\nPuzzle a resolver:")
        self.tablero.mostrar_tablero()


        seleccionados = []

        print("\nModo manual")
        print("Ingrese los rectángulos para cada pista.")
        print("Recuerde que las filas y columnas empiezan en 0.")

        seleccionados = []

        for fila_pista, col_pista, valor_pista in self.tablero.pistas():
            print("\nPista actual:")
            print("Fila:", fila_pista)
            print("Columna:", col_pista)
            print("Valor:", valor_pista)

            while True:
                try:
                    fila = int(input("Fila inicial del rectángulo: "))
                    col = int(input("Columna inicial del rectángulo: "))
                    alto = int(input("Alto del rectángulo: "))
                    base = int(input("Base del rectángulo: "))
                except ValueError:
                    print("Debe ingresar números enteros.")
                    continue

                rectangulo = Rectangulo(fila, col, alto, base)

                if not self.tablero.rectValidoP(rectangulo, fila_pista, col_pista, valor_pista):
                    print("Rectángulo inválido para esta pista.")
                    continue

                if not self.no_solapa(rectangulo, seleccionados):
                    print("Rectángulo inválido: se solapa con otro rectángulo.")
                    continue

                seleccionados.append(rectangulo)
                print("Rectángulo agregado correctamente.")

                print("\nTablero actual:")
                self.tablero.mostrar_solucion(seleccionados)

                break

        print("\nResultado ingresado:")
        self.tablero.mostrar_solucion(seleccionados)

        if self.cubre_todo_tablero(seleccionados):
            print("El tablero fue completado correctamente.")
        else:
            print("El tablero no quedó completamente cubierto.")

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

    def cargar_tablero(self, ruta):
        celdas = []

        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                valores = linea.strip().split()

                if len(valores) == 0:
                    continue

                fila = []

                for valor in valores:
                    fila.append(int(valor))

                celdas.append(fila)

        return TableroShikaku(celdas)


    def cargar_puzzle(self):
        carpeta = "puzzles"

        if not os.path.exists(carpeta):
            print("No existe la carpeta puzzles.")
            return

        archivos = []

        for nombre in os.listdir(carpeta):
            if nombre.endswith(".txt"):
                archivos.append(nombre)

        archivos.sort()

        if len(archivos) == 0:
            print("No hay archivos .txt en la carpeta puzzles.")
            return

        print("\nPuzzles disponibles:")

        for i in range(len(archivos)):
            print(str(i + 1) + ". " + archivos[i])

        try:
            opcion = int(input("Seleccione el número del puzzle: "))
        except ValueError:
            print("Debe ingresar un número.")
            return

        if opcion < 1 or opcion > len(archivos):
            print("Opción inválida.")
            return

        nombre_archivo = archivos[opcion - 1]
        ruta = os.path.join(carpeta, nombre_archivo)

        self.tablero = self.cargar_tablero(ruta)

        print("\nPuzzle cargado correctamente:")
        self.tablero.mostrar_tablero()


    def asegurar_tablero(self):
        if self.tablero is None:
            print("\nNo hay ningún puzzle cargado.")
            self.cargar_puzzle()

        return self.tablero is not None


    def preguntar_cambiar_puzzle(self):
        respuesta = input("¿Desea escoger o cambiar el puzzle antes de continuar? (s/n): ")
        respuesta = respuesta.strip().lower()

        if respuesta == "s":
            self.cargar_puzzle()