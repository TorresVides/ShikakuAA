#
from src.shikku.tablero import TableroShikaku
from src.shikku.solucionador import SolucionadorShikaku


def test_solucionador_encuentra_solucion():
    celdas = [
        [4, 0, 0, 4],
        [0, 0, 0, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 4]
    ]

    tablero = TableroShikaku(celdas)
    solucionador = SolucionadorShikaku(tablero)

    solucion = solucionador.resolver()

    assert solucion is not None
    assert len(solucion) == len(tablero.pistas())

    celdas_ocupadas = set()

    for rectangulo in solucion:
        for celda in rectangulo.ocupadas():
            celdas_ocupadas.add(celda)

    total_celdas = tablero.filas * tablero.cols

    assert len(celdas_ocupadas) == total_celdas