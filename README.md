# Proyecto Shikaku - Análisis de Algoritmos

## Descripción general

Este proyecto implementa un solucionador para el rompecabezas lógico **Shikaku**. El sistema permite cargar tableros desde archivos de texto, visualizar el tablero, jugar manualmente desde una interfaz por consola y ejecutar un solucionador sintético.

El proyecto fue desarrollado para el curso **Análisis de Algoritmos**. Su objetivo principal es diseñar e implementar una solución computacional para resolver instancias de Shikaku, aplicando conceptos de búsqueda exhaustiva, generación de candidatos, validación de restricciones, heurísticas, programación dinámica con memoización y análisis experimental de recursos.

## Reglas del problema

En Shikaku se tiene un tablero rectangular dividido en celdas. Algunas celdas contienen números llamados pistas. El objetivo es dividir todo el tablero en rectángulos de tal forma que:

1. Cada rectángulo contenga exactamente una pista.
2. El área de cada rectángulo sea igual al valor de la pista que contiene.
3. Los rectángulos no se solapen.
4. Todos los rectángulos cubran completamente el tablero.

## Estructura del proyecto

```text
Shikaku/
├── src/
│   └── shikku/
│       ├── __init__.py
│       ├── rectangulo.py
│       ├── tablero.py
│       ├── solucionador.py
│       └── interfaz.py
├── tests/
│   ├── test_rectangulo.py
│   ├── test_tablero.py
│   └── test_solucionador.py
├── puzzles/
│   ├── puzzle_4x4.txt
│   ├── puzzle_5x5.txt
│   ├── puzzle_6x6.txt
│   ├── puzzle_7x7.txt
│   ├── puzzle_8x8.txt
│   ├── puzzle_9x9.txt
│   ├── puzzle_10x10.txt
│   └── puzzle_sin_solucion.txt
├── resultados/
│   ├── resultados_experimentos.csv
│   └── resultados_experimentos_YYYYMMDD_HHMMSS.csv
├── main.py
├── experimentos.py
├── README.md
├── requirements.txt
└── pytest.ini
```

## Componentes principales

### `Rectangulo`

La clase `Rectangulo` representa una región rectangular del tablero. Sus responsabilidades principales son:

* Calcular el área del rectángulo.
* Listar las celdas ocupadas.
* Verificar si una celda pertenece al rectángulo.
* Verificar si dos rectángulos se solapan.

### `TableroShikaku`

La clase `TableroShikaku` representa el tablero completo del rompecabezas. Sus responsabilidades principales son:

* Guardar la matriz de celdas.
* Identificar las pistas del tablero.
* Verificar si una celda está dentro del tablero.
* Validar si un rectángulo es correcto para una pista.
* Generar candidatos válidos para cada pista.
* Ordenar las pistas según la cantidad de candidatos.
* Mostrar el tablero inicial, el avance manual y la solución.

### `SolucionadorShikaku`

La clase `SolucionadorShikaku` implementa el solucionador automático. El algoritmo genera candidatos válidos para cada pista y luego aplica búsqueda con retroceso para seleccionar un conjunto de rectángulos que cubra completamente el tablero sin solapamientos.

El solucionador fue optimizado mediante:

* Heurística de ordenamiento por menor número de candidatos.
* Máscaras binarias para representar celdas ocupadas.
* Memoización de estados fallidos.
* Contadores de llamadas recursivas, rectángulos probados, estados memoizados y podas por memoización.

La memoización permite evitar repetir estados del tipo `(índice de pista, máscara de celdas ocupadas)` que ya fueron explorados y demostraron no conducir a una solución.

### `Interfaz`

La clase `Interfaz` implementa una interfaz sencilla por consola. Permite:

* Mostrar el tablero cargado.
* Cargar puzzles desde la carpeta `puzzles`.
* Jugar manualmente.
* Resolver automáticamente.
* Visualizar el avance del tablero en modo manual.
* Visualizar la solución generada por el solucionador sintético.
* Mostrar métricas de ejecución del solucionador.

## Formato de los puzzles

Los tableros se guardan como archivos `.txt` dentro de la carpeta `puzzles`.

Cada archivo representa una matriz. El valor `0` indica una celda vacía y cualquier número diferente de cero indica una pista.

Ejemplo:

```text
4 0 0 4
0 0 0 0
4 0 0 0
0 0 0 4
```

Este tablero corresponde a una instancia de tamaño `4x4`.

## Ejecución del programa

Desde la raíz del proyecto, ejecutar:

```bash
python main.py
```

La interfaz mostrará un menú similar al siguiente:

```text
===== SHIKAKU =====
1. Mostrar tablero
2. Jugar manualmente
3. Resolver automáticamente
4. Cargar puzzle
5. Salir
```

Antes de jugar o resolver automáticamente, se puede cargar un puzzle desde la carpeta `puzzles`. Si no hay tablero cargado, la interfaz solicita seleccionar uno.

## Jugar manualmente

En el modo manual, el sistema recorre las pistas del tablero y solicita al usuario ingresar un rectángulo para cada una.

Para cada rectángulo se deben ingresar:

* Fila inicial.
* Columna inicial.
* Alto.
* Base.

Las filas y columnas se manejan desde índice `0`.

Después de ingresar un rectángulo válido, el programa muestra el tablero parcial actualizado. Si el rectángulo no cumple las restricciones del Shikaku o se solapa con otro rectángulo ya ingresado, el sistema lo rechaza y solicita otro.

## Resolver automáticamente

El modo automático ejecuta el solucionador sintético. El procedimiento general es:

1. Obtener todas las pistas del tablero.
2. Generar rectángulos candidatos para cada pista.
3. Filtrar candidatos que no cumplan las restricciones básicas.
4. Ordenar las pistas de acuerdo con la cantidad de candidatos.
5. Aplicar backtracking con memoización.
6. Rechazar ramas donde haya solapamientos.
7. Guardar estados fallidos para no repetir exploraciones.
8. Verificar que la solución cubra todo el tablero.

El ordenamiento por menor número de candidatos funciona como una heurística de restricción. La idea es procesar primero las pistas con menos opciones, ya que estas reducen más rápidamente el espacio de búsqueda.

## Algoritmo usado

El solucionador se basa en búsqueda con retroceso sobre candidatos válidos y memoización de estados fallidos.

Primero, para cada pista `(fila, columna, valor)`, se generan todos los rectángulos posibles cuya área sea igual al valor de la pista. Cada candidato se valida verificando que:

* Esté dentro del tablero.
* Contenga la pista correspondiente.
* Tenga área igual al valor de la pista.
* Contenga exactamente una pista.

Después, el algoritmo intenta construir una solución escogiendo un candidato por cada pista. Si el candidato no se solapa con los rectángulos ya seleccionados, se agrega temporalmente a la solución y se avanza a la siguiente pista. Si no se logra completar el tablero, el algoritmo retrocede y prueba otro candidato.

La memoización almacena estados fallidos de la forma:

```text
(indice, mascara_ocupada)
```

donde `indice` representa la pista que se está procesando y `mascara_ocupada` representa las celdas ya cubiertas. Si el algoritmo vuelve a llegar a un estado que ya falló, evita repetir esa rama.

## Complejidad general

Sea `k` la cantidad de pistas del tablero y sea `c_i` la cantidad de candidatos válidos generados para la pista `i`.

En el peor caso, sin memoización, el algoritmo puede explorar una cantidad de combinaciones proporcional a:

```text
O(c_1 · c_2 · ... · c_k)
```

Si se asume que cada pista tiene a lo sumo `c` candidatos, el peor caso puede escribirse como:

```text
O(c^k)
```

Con memoización, los estados se identifican por una pareja `(i, M)`, donde `i` es el índice de la pista actual y `M` es una máscara de ocupación. En el peor caso teórico, el número de máscaras posibles sobre un tablero de `A` celdas es `2^A`, por lo que el número máximo de estados posibles está acotado por:

```text
O(k · 2^A)
```

En la práctica, el número real de estados explorados es mucho menor debido a la generación previa de candidatos válidos, el rechazo de solapamientos y el ordenamiento heurístico de las pistas.

## Divide y vencerás

Se analizó la estrategia de divide y vencerás, pero no se adoptó como estrategia principal porque Shikaku no se descompone naturalmente en subproblemas independientes. Si se divide el tablero de forma arbitraria, se pueden cortar rectángulos válidos que cruzan la frontera entre subtableros.

Por esta razón, el algoritmo principal usa búsqueda exacta con backtracking, heurística y memoización. Esta decisión preserva las restricciones globales del problema: cada rectángulo debe contener exactamente una pista, no debe solaparse y la solución completa debe cubrir todo el tablero.

## Teorema maestro

El teorema maestro no se aplica directamente al algoritmo implementado, porque la recurrencia del solucionador no tiene la forma clásica:

```text
T(n) = aT(n/b) + f(n)
```

El algoritmo no divide el tablero en subproblemas de tamaño uniforme. En cambio, explora un árbol de decisiones definido por los candidatos de cada pista. Por tanto, el análisis se realiza por inspección del espacio de búsqueda y por medición experimental.

## Pruebas unitarias

El proyecto usa `pytest` para validar el funcionamiento de sus componentes principales.

Para ejecutar las pruebas:

```bash
python -m pytest
```

Las pruebas verifican:

* Cálculo del área de un rectángulo.
* Celdas ocupadas por un rectángulo.
* Pertenencia de una celda a un rectángulo.
* Detección de solapamientos.
* Identificación de pistas en el tablero.
* Validación de rectángulos dentro del tablero.
* Conteo de pistas dentro de un rectángulo.
* Generación de candidatos válidos.
* Funcionamiento del solucionador automático.
* Cobertura completa del tablero en una solución encontrada.

Resultado actual de pruebas:

```text
10 passed
```

## Experimentos de rendimiento

El archivo `experimentos.py` permite medir experimentalmente el comportamiento del solucionador sobre distintos puzzles.

Para ejecutar los experimentos:

```bash
python experimentos.py
```

El script evalúa todos los archivos `.txt` ubicados en la carpeta `puzzles` y guarda los resultados en la carpeta `resultados`.

Las métricas recolectadas son:

* Archivo evaluado.
* Número de filas.
* Número de columnas.
* Cantidad de pistas.
* Total de candidatos generados.
* Llamadas recursivas.
* Rectángulos probados.
* Estados memoizados.
* Podas por memoización.
* Tiempo promedio de ejecución.
* Tiempo mínimo.
* Tiempo máximo.
* Memoria pico promedio.
* Indicación de si se encontró solución.

## Resultados experimentales recientes

| Puzzle                  | Tamaño | Pistas | Candidatos | Llamadas | Probados | Memoizados | Podas | Tiempo promedio (s) | Memoria pico (KB) | Solución |
| ----------------------- | -----: | -----: | ---------: | -------: | -------: | ---------: | ----: | ------------------: | ----------------: | -------- |
| puzzle_4x4.txt          |    4x4 |      4 |          7 |        5 |        4 |          0 |     0 |            0.000098 |          0.664062 | Sí       |
| puzzle_5x5.txt          |    5x5 |      5 |         13 |        6 |        9 |          0 |     0 |            0.000227 |          0.867188 | Sí       |
| puzzle_6x6.txt          |    6x6 |      8 |         28 |       11 |       28 |          2 |     0 |            0.001054 |          1.320312 | Sí       |
| puzzle_7x7.txt          |    7x7 |      9 |         47 |       53 |      259 |         37 |     6 |            0.007054 |          4.609375 | Sí       |
| puzzle_8x8.txt          |    8x8 |     11 |         69 |      204 |     1846 |        190 |     2 |            0.053495 |         16.367188 | Sí       |
| puzzle_9x9.txt          |    9x9 |     12 |         82 |      137 |     1037 |        124 |     0 |            0.028637 |         14.238281 | Sí       |
| puzzle_10x10.txt        |  10x10 |     15 |        112 |      325 |     2410 |        309 |     0 |            0.066770 |         60.637500 | Sí       |
| puzzle_sin_solucion.txt |    3x3 |      2 |          2 |        1 |        0 |          1 |     0 |            0.000009 |          0.257812 | No       |

## Interpretación de los experimentos

Los experimentos permiten observar que el costo computacional no depende únicamente del tamaño del tablero. También depende de:

* La cantidad de pistas.
* La cantidad de candidatos generados por pista.
* La distribución espacial de las pistas.
* El número de retrocesos necesarios durante la búsqueda.

Por esta razón, un tablero más grande no necesariamente es siempre más costoso que uno más pequeño. Por ejemplo, el tablero `9x9` tuvo menor tiempo promedio que el tablero `8x8`, aunque tiene mayor tamaño. Esto se explica porque la distribución de pistas del `9x9` genera una búsqueda más favorable.

El caso `10x10` presentó el mayor tiempo promedio y la mayor memoria pico. Esto es coherente con su mayor cantidad de celdas, pistas, candidatos y estados memoizados.

## Instalación de dependencias

El proyecto requiere Python 3 y `pytest`.

Para instalar dependencias:

```bash
pip install -r requirements.txt
```

Como `requirements.txt` solo contiene `pytest`, también puede instalarse manualmente:

```bash
pip install pytest
```

## Ejecución recomendada

Secuencia recomendada para validar el proyecto:

```bash
python -m pytest
python main.py
python experimentos.py
```

## Estado actual del proyecto

El proyecto cuenta con:

* Separación de clases.
* Interfaz por consola.
* Carga de puzzles desde archivo.
* Modo manual.
* Solucionador automático.
* Backtracking.
* Heurística de ordenamiento.
* Memoización de estados fallidos.
* Visualización de solución.
* Pruebas unitarias.
* Script de experimentos.
* Resultados experimentales en CSV.

Como mejora futura, se podría agregar una interfaz gráfica y un solucionador por componentes independientes cuando el grafo de conflictos del tablero permita una descomposición segura.
