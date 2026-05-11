"""
Práctica: Diseño de algoritmos recursivos
Módulo  : Quick sort recursivo

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
# Problema A – Partición de Lomuto
# ---------------------------------------------------------------------------

def particiona(arr: list, lo: int, hi: int) -> int:
    pivot = arr[hi]
    i = lo - 1

    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # colocar pivote en su posición final
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]

    return i + 1


def particiona_aleatoria(arr: list, lo: int, hi: int) -> int:
    idx = random.randint(lo, hi)
    arr[idx], arr[hi] = arr[hi], arr[idx]
    return particiona(arr, lo, hi)


# ---------------------------------------------------------------------------
# Problema B – Quick sort recursivo
# ---------------------------------------------------------------------------

def quicksort(arr: list, lo: int = 0, hi: int = None) -> None:
    if hi is None:
        hi = len(arr) - 1

    # PASO BASE
    if lo >= hi:
        return

    # PASO RECURSIVO
    p = particiona(arr, lo, hi)

    quicksort(arr, lo, p - 1)
    quicksort(arr, p + 1, hi)

def quicksort_aleatorio(arr: list, lo: int = 0, hi: int = None) -> None:
    if hi is None:
        hi = len(arr) - 1

    # PASO BASE
    if lo >= hi:
        return

    # PASO RECURSIVO con pivote aleatorio
    p = particiona_aleatoria(arr, lo, hi)

    quicksort_aleatorio(arr, lo, p - 1)
    quicksort_aleatorio(arr, p + 1, hi)


# ---------------------------------------------------------------------------
# Problema D – Versión instrumentada con contador de comparaciones
# ---------------------------------------------------------------------------

def _particiona_conteo(arr: list, lo: int, hi: int, conteo: list) -> int:
    pivote = arr[hi]
    i = lo - 1
    
    for j in range(lo, hi):
        conteo[0] += 1 
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1

def quicksort_conteo(arr: list, lo: int, hi: int, conteo: list) -> None:

    if lo >= hi:
        return

    p = _particiona_conteo(arr, lo, hi, conteo)
    
    quicksort_conteo(arr, lo, p - 1, conteo)
    quicksort_conteo(arr, p + 1, hi, conteo)



# ---------------------------------------------------------------------------
# Utilidades de verificación y generación de datos
# ---------------------------------------------------------------------------

def verificar_ordenamiento(arr_original: list) -> bool:
    """Verifica que quicksort produce el mismo resultado que sorted()."""
    arr = arr_original.copy()
    referencia = sorted(arr)
    quicksort(arr)
    return arr == referencia


def generar_arreglo(n: int, escenario: str, semilla: int = 42) -> list:
    """
    Genera un arreglo de tamaño n según el escenario:
        'aleatorio'  → permutación aleatoria
        'ordenado'   → ya ordenado (mejor caso para búsqueda binaria,
                        peor caso para quicksort con pivote fijo)
        'inverso'    → orden descendente (peor caso para quicksort)
    """
    random.seed(semilla)
    if escenario == 'aleatorio':
        arr = list(range(n))
        random.shuffle(arr)
    elif escenario == 'ordenado':
        arr = list(range(n))
    elif escenario == 'inverso':
        arr = list(range(n - 1, -1, -1))
    else:
        raise ValueError(f"Escenario desconocido: {escenario}")
    return arr


# ---------------------------------------------------------------------------
# Pruebas automáticas
# ---------------------------------------------------------------------------

def _pruebas_particion():
    A = [3, 6, 8, 10, 1, 2, 1]
    p = particiona(A, 0, 6)
    assert A[p] == 1, f"Pivote incorrecto: A[{p}] = {A[p]}, esperado 1"
    assert all(v <= 1 for v in A[:p]),   f"Hay elementos > pivot a la izquierda: {A}"
    assert all(v >= 1 for v in A[p+1:]), f"Hay elementos < pivot a la derecha: {A}"
    print(f"✓ Partición correcta: {A}, pivote en índice {p}")


def _pruebas_quicksort():
    casos = [
        [],
        [1],
        [2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        list(range(100, 0, -1)),    # inverso
        list(range(100)),           # ya ordenado
    ]
    for arr in casos:
        assert verificar_ordenamiento(arr), f"Falla en: {arr[:10]}..."
    print("✓ Quick sort correcto en todos los casos de prueba.")


def _experimento_comparaciones():
    """Compara las comparaciones en los tres escenarios."""
    import sys
    sys.setrecursionlimit(100_000)

    print(f"\n{'n':>8} {'aleatorio':>12} {'ordenado (fijo)':>17} {'ordenado (random)':>19}")
    print("-" * 62)

    for n in [100, 500, 1_000, 2_000, 4_000]:
        # Aleatorio
        arr = generar_arreglo(n, 'aleatorio')
        c_al = [0]
        quicksort_conteo(arr, 0, n - 1, c_al)

        # Ordenado, pivote fijo (peor caso)
        arr = generar_arreglo(n, 'ordenado')
        c_ord = [0]
        quicksort_conteo(arr, 0, n - 1, c_ord)

        # Ordenado, pivote aleatorio (esperado O(n log n))
        arr = generar_arreglo(n, 'ordenado')
        c_rand = [0]
        # Para instrumentar quicksort_aleatorio necesitaríamos otra versión;
        # aquí usamos quicksort_conteo sólo para el pivote fijo.
        # (Actividad: extiende quicksort_conteo para usar pivote aleatorio.)

        print(f"{n:>8,} {c_al[0]:>12,} {c_ord[0]:>17,} {'(ver actividad)':>19}")


def _experimento_tiempo():
    """Mide el tiempo de quicksort vs. sorted() en arreglos aleatorios."""
    import sys
    sys.setrecursionlimit(1_000_000)

    print(f"\n{'n':>10} {'T_quicksort (ms)':>18} {'T_sorted (ms)':>15} {'Razón':>8}")
    print("-" * 56)

    for n in [1_000, 10_000, 100_000]:
        arr_orig = generar_arreglo(n, 'aleatorio')

        arr = arr_orig.copy()
        t0 = time.perf_counter()
        quicksort(arr)
        t_qs = (time.perf_counter() - t0) * 1e3

        arr = arr_orig.copy()
        t0 = time.perf_counter()
        sorted(arr)
        t_so = (time.perf_counter() - t0) * 1e3

        razon = t_qs / t_so if t_so > 0 else float('inf')
        print(f"{n:>10,} {t_qs:>18.3f} {t_so:>15.3f} {razon:>8.2f}x")


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(200_000)

    print("=" * 60)
    print("Quick sort recursivo")
    print("=" * 60)

    print("\n[1] Pruebas de la partición (problema A)")
    _pruebas_particion()

    print("\n[2] Pruebas de correctitud de quick sort (problema B)")
    _pruebas_quicksort()

    print("\n[3] Comparaciones por escenario (problema D)")
    _experimento_comparaciones()

    print("\n[4] Tiempo de ejecución vs. sorted() (problema D.4)")
    _experimento_tiempo()
