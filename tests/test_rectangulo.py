#
from src.shikku.rectangulo import Rectangulo


def test_area_rectangulo():
    r = Rectangulo(0, 0, 2, 3)
    assert r.area() == 6


def test_ocupadas_rectangulo():
    r = Rectangulo(0, 0, 2, 2)

    esperado = [
        (0, 0), (0, 1),
        (1, 0), (1, 1)
    ]

    assert r.ocupadas() == esperado


def test_contiene_celda():
    r = Rectangulo(0, 0, 2, 2)

    assert r.contiene(1, 1) == True
    assert r.contiene(3, 3) == False


def test_solapados():
    r1 = Rectangulo(0, 0, 2, 2)
    r2 = Rectangulo(1, 1, 2, 2)
    r3 = Rectangulo(2, 2, 2, 2)

    assert r1.solapados(r2) == True
    assert r1.solapados(r3) == False