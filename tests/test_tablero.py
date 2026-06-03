#
from src.shikku.rectangulo import Rectangulo
from src.shikku.tablero import TableroShikaku


def crear_tablero():
    celdas = [
        [4, 0, 0, 4],
        [0, 0, 0, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 4]
    ]

    return TableroShikaku(celdas)


def test_esta_dentro():
    tablero = crear_tablero()

    assert tablero.esta_dentro(0, 0) == True
    assert tablero.esta_dentro(3, 3) == True
    assert tablero.esta_dentro(4, 0) == False
    assert tablero.esta_dentro(0, 4) == False
    assert tablero.esta_dentro(-1, 0) == False


def test_pistas():
    tablero = crear_tablero()

    esperado = [
        (0, 0, 4),
        (0, 3, 4),
        (2, 0, 4),
        (3, 3, 4)
    ]

    assert tablero.pistas() == esperado


def test_contar_pistas_rectangulo():
    tablero = crear_tablero()

    r1 = Rectangulo(0, 0, 2, 2)
    r2 = Rectangulo(0, 0, 1, 4)

    assert tablero.contarPistasR(r1) == 1
    assert tablero.contarPistasR(r2) == 2


def test_rectangulo_valido_para_pista():
    tablero = crear_tablero()

    r1 = Rectangulo(0, 0, 2, 2)
    r2 = Rectangulo(0, 0, 1, 4)
    r3 = Rectangulo(3, 3, 2, 2)
    r4 = Rectangulo(0, 1, 2, 2)

    assert tablero.rectValidoP(r1, 0, 0, 4) == True
    assert tablero.rectValidoP(r2, 0, 0, 4) == False
    assert tablero.rectValidoP(r3, 3, 3, 4) == False
    assert tablero.rectValidoP(r4, 0, 0, 4) == False


def test_candidatos_pista():
    tablero = crear_tablero()

    candidatos = tablero.candidatos_pista(0, 0, 4)

    assert len(candidatos) > 0

    for rectangulo in candidatos:
        assert tablero.rectValidoP(rectangulo, 0, 0, 4) == True