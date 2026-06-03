# experimentos.py
import os
import csv
import time
import tracemalloc
from datetime import datetime

from src.shikku.tablero import TableroShikaku
from src.shikku.solucionador import SolucionadorShikaku


def cargar_tablero_desde_archivo(ruta):
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


def medir_puzzle(ruta, repeticiones=5):
    tiempos = []
    memorias = []

    ultima_solucion = None
    ultimo_solucionador = None
    ultimo_tablero = None

    for _ in range(repeticiones):
        tablero = cargar_tablero_desde_archivo(ruta)
        solucionador = SolucionadorShikaku(tablero)

        tracemalloc.start()
        inicio = time.perf_counter()

        solucion = solucionador.resolver()

        fin = time.perf_counter()
        memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tiempos.append(fin - inicio)
        memorias.append(memoria_pico / 1024)

        ultima_solucion = solucion
        ultimo_solucionador = solucionador
        ultimo_tablero = tablero

    total_candidatos = 0

    for fila, col, valor, candidatos in ultimo_solucionador.candidatos:
        total_candidatos += len(candidatos)

    return {
        "archivo": ruta,
        "filas": ultimo_tablero.filas,
        "columnas": ultimo_tablero.cols,
        "pistas": len(ultimo_tablero.pistas()),
        "total_candidatos": total_candidatos,
        "llamadas_recursivas": ultimo_solucionador.llamadas_recursivas,
        "rectangulos_probados": ultimo_solucionador.rectangulos_probados,
        "tiempo_promedio": sum(tiempos) / len(tiempos),
        "tiempo_minimo": min(tiempos),
        "tiempo_maximo": max(tiempos),
        "memoria_pico_promedio_kb": sum(memorias) / len(memorias),
        "encontro_solucion": ultima_solucion is not None
    }


def main():
    carpeta_puzzles = "puzzles"
    carpeta_resultados = "resultados"

    if not os.path.exists(carpeta_resultados):
        os.mkdir(carpeta_resultados)

    archivos = []

    for nombre in os.listdir(carpeta_puzzles):
        if nombre.endswith(".txt"):
            ruta = os.path.join(carpeta_puzzles, nombre)
            archivos.append(ruta)

    archivos.sort()

    resultados = []

    for ruta in archivos:
        print("Midiendo:", ruta)
        resultado = medir_puzzle(ruta, repeticiones=5)
        resultados.append(resultado)

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = "resultados_experimentos_" + fecha + ".csv"
    ruta_salida = os.path.join(carpeta_resultados, nombre_archivo)

    columnas = [
        "archivo",
        "filas",
        "columnas",
        "pistas",
        "total_candidatos",
        "llamadas_recursivas",
        "rectangulos_probados",
        "tiempo_promedio",
        "tiempo_minimo",
        "tiempo_maximo",
        "memoria_pico_promedio_kb",
        "encontro_solucion"
    ]

    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escritor.writeheader()

        for resultado in resultados:
            escritor.writerow(resultado)

    print("\nResultados guardados en:", ruta_salida)


if __name__ == "__main__":
    main()