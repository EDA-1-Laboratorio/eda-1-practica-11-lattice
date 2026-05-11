"""
Práctica: Diseño de algoritmos recursivos
Módulo  : Búsqueda binaria recursiva

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.

Recuerda identificar en tus comentarios:
    # PASO BASE
    # HIPÓTESIS INDUCTIVA (como comentario en prosa)
    # PASO RECURSIVO
"""

import time
import random


# ---------------------------------------------------------------------------
# Problema A – Búsqueda binaria recursiva
# ---------------------------------------------------------------------------

def busqueda_binaria(arr: list[int], objetivo: int,
                     lo: int = 0, hi: int = None) -> int:
    """
    Busca 'objetivo' en arr[lo..hi] usando búsqueda binaria recursiva.

    Precondición:
        arr está ordenado de menor a mayor.

    Retorna:
        El índice de 'objetivo' si existe, o -1 si no está.
    """

    if hi is None:
        hi = len(arr) - 1

    # Paso base: el subarreglo está vacío
    if lo > hi:
        return -1

    # Punto medio
    mid = (lo + hi) // 2

    # Caso encontrado
    if arr[mid] == objetivo:
        return mid

    # Buscar en la mitad izquierda
    if objetivo < arr[mid]:
        return busqueda_binaria(arr, objetivo, lo, mid - 1)

    # Buscar en la mitad derecha
    return busqueda_binaria(arr, objetivo, mid + 1, hi)


# =========================
# Pruebas mínimas
# =========================

A = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]

assert busqueda_binaria(A, 23) == 5
assert busqueda_binaria(A, 16) == 4
assert busqueda_binaria(A, 2) == 0
assert busqueda_binaria(A, 91) == 10
assert busqueda_binaria(A, 99) == -1
assert busqueda_binaria(A, 1) == -1
assert busqueda_binaria([], 5) == -1

print("Todas las pruebas pasaron.")

# ---------------------------------------------------------------------------
# Problema B – Versión instrumentada con contador de comparaciones
# ---------------------------------------------------------------------------
def busqueda_binaria(arr: list[int], objetivo: int,
                     lo: int = 0, hi: int = None) -> int:
    """
    Busca 'objetivo' en arr[lo..hi] usando búsqueda binaria recursiva.

    Precondición:
        arr está ordenado de menor a mayor.

    Retorna:
        El índice de 'objetivo' si existe, o -1 si no está.
    """

    if hi is None:
        hi = len(arr) - 1

    # Paso base: el subarreglo está vacío
    if lo > hi:
        return -1

    # Cálculo del punto medio
    mid = (lo + hi) // 2

    # Si encontramos el objetivo
    if arr[mid] == objetivo:
        return mid

    # Buscar en la mitad izquierda
    if objetivo < arr[mid]:
        return busqueda_binaria(arr, objetivo, lo, mid - 1)

    # Buscar en la mitad derecha
    else:
        return busqueda_binaria(arr, objetivo, mid + 1, hi)


# =========================
# Pruebas mínimas
# =========================

A = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]

assert busqueda_binaria(A, 23) == 5
assert busqueda_binaria(A, 16) == 4
assert busqueda_binaria(A, 2) == 0
assert busqueda_binaria(A, 91) == 10
assert busqueda_binaria(A, 99) == -1
assert busqueda_binaria(A, 1) == -1
assert busqueda_binaria([], 5) == -1

print("Todas las pruebas pasaron.")

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def busqueda_lineal(arr: list[int], objetivo: int) -> int:
    """Búsqueda lineal O(n) — referencia para comparar tiempos."""
    for i, v in enumerate(arr):
        if v == objetivo:
            return i
    return -1


# ---------------------------------------------------------------------------
# Pruebas automáticas
# ---------------------------------------------------------------------------

def _pruebas_correctitud():
    A = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]

    assert busqueda_binaria(A, 23) == 5,  "Falla: 23 no encontrado en índice 5"
    assert busqueda_binaria(A, 16) == 4,  "Falla: 16 no encontrado en índice 4"
    assert busqueda_binaria(A, 2)  == 0,  "Falla: 2 no encontrado en índice 0"
    assert busqueda_binaria(A, 91) == 10, "Falla: 91 no encontrado en índice 10"
    assert busqueda_binaria(A, 99) == -1, "Falla: 99 debería devolver -1"
    assert busqueda_binaria(A, 1)  == -1, "Falla: 1 debería devolver -1"
    assert busqueda_binaria([], 5) == -1, "Falla: arreglo vacío debería devolver -1"

    print("✓ Pruebas de correctitud: todas pasaron.")


def _pruebas_conteo():
    """Verifica que las comparaciones crecen logarítmicamente."""
    for exp in range(3, 21):
        n = 2 ** exp
        arr = list(range(n))
        conteo = [0]
        busqueda_binaria_conteo(arr, -1, 0, n - 1, conteo)   # peor caso
        print(f"  n = {n:>8}, comparaciones peor caso = {conteo[0]:>3}, "
              f"log2(n)+1 = {exp + 1}")


def _experimento_tiempo():
    """Mide el tiempo de búsqueda binaria vs. lineal."""
    REPETICIONES = 10_000
    encabezado = f"{'n':>12} {'T_lineal (µs)':>16} {'T_binaria (ns)':>16} {'Factor':>10}"
    print(encabezado)
    print("-" * len(encabezado))

    for n in [1_000, 10_000, 100_000, 1_000_000]:
        arr = list(range(n))
        objetivo = -1           # peor caso: no está

        # Búsqueda lineal
        t0 = time.perf_counter()
        for _ in range(REPETICIONES):
            busqueda_lineal(arr, objetivo)
        t_lineal = (time.perf_counter() - t0) / REPETICIONES * 1e6  # µs

        # Búsqueda binaria
        t0 = time.perf_counter()
        for _ in range(REPETICIONES):
            busqueda_binaria(arr, objetivo)
        t_binaria = (time.perf_counter() - t0) / REPETICIONES * 1e9  # ns

        factor = t_lineal * 1e3 / t_binaria if t_binaria > 0 else float('inf')
        print(f"{n:>12,} {t_lineal:>16.2f} {t_binaria:>16.1f} {factor:>10.0f}x")


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    print("=" * 60)
    print("Búsqueda binaria recursiva")
    print("=" * 60)

    print("\n[1] Pruebas de correctitud")
    _pruebas_correctitud()

    print("\n[2] Comparaciones por tamaño (problema B)")
    _pruebas_conteo()

    print("\n[3] Experimento de tiempo (problema C)")
    _experimento_tiempo()
