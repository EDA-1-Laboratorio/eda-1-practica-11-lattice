[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/u-RYJRjY)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23859605&assignment_repo_type=AssignmentRepo)
# Guía práctica: Diseño de algoritmos recursivos

## Objetivo general

Diseñar e implementar algoritmos recursivos correctos, identificando explícitamente sus
tres componentes: **paso base**, **hipótesis inductiva** y **paso recursivo**. Analizar su
complejidad temporal mediante relaciones de recurrencia.

## Conexión con la clase

En sesiones anteriores el grupo dedujo la **versión recursiva de insertion sort** y estudió
**merge sort** como ejemplo canónico de divide y vencerás. Para ambos algoritmos se planteó
la relación de recurrencia que describe su tiempo de ejecución. Esta práctica extiende ese
aprendizaje a dos nuevos algoritmos: **búsqueda binaria** y **quick sort**.

## Requisitos técnicos

- Python 3.10 o superior.
- Bibliotecas: `time`, `random`, `sys`.
- Entorno sugerido: VS Code.

## Entregables

- Código fuente con las funciones implementadas.
- Reporte técnico con análisis matemático y resultados experimentales.

---

## Parte 0. Anatomía de una función recursiva

Antes de escribir cualquier código, el equipo debe interiorizar la estructura de toda
función recursiva correcta. Usaremos como **referencia** la versión recursiva de
insertion sort que ya conocen.

### 0.1 Los tres componentes

Toda función recursiva bien construida tiene exactamente tres piezas:

| Componente | ¿Qué hace? | Pregunta clave |
|:---|:---|:---|
| **Paso base** | Resuelve el caso más pequeño sin recurrir. | ¿Cuándo la entrada es tan sencilla que la respuesta es inmediata? |
| **Hipótesis inductiva** | Supongan (sin demostrar) que la llamada recursiva resolverá correctamente el subproblema más pequeño. | ¿Qué le pedimos a la llamada recursiva y qué promete que devolverá? |
| **Paso recursivo** | Reducir el problema al subproblema más pequeño y combinar el resultado. | ¿Cómo usamos la hipótesis para resolver el problema completo? |

> **Nota:** La hipótesis inductiva no se "verifica" dentro del código; se asume verdadera.
> La corrección total del algoritmo se prueba por inducción matemática sobre el tamaño de
> la entrada. En esta práctica basta con enunciarla claramente en el reporte.

### 0.2 Referencia: insertion sort recursivo

Revisa el siguiente pseudocódigo antes de responder las preguntas:

```
insertion_sort_rec(arr, n):
    # Paso base
    if n <= 1:
        return

    # Hipótesis inductiva: insertion_sort_rec(arr, n-1) ordena
    # correctamente los primeros n-1 elementos de arr.
    insertion_sort_rec(arr, n - 1)

    # Paso recursivo: insertar arr[n-1] en la posición correcta
    # dentro del segmento ya ordenado arr[0..n-2].
    llave = arr[n - 1]
    j = n - 2
    while j >= 0 and arr[j] > llave:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = llave
```

### 0.3 Preguntas de comprensión (responder en el reporte)

Antes de continuar, discutan en equipo:

1. ¿Por qué el caso `n <= 1` es el paso base? ¿Qué pasa si se omite?
2. Enunciar la hipótesis inductiva con sus propias palabras: *"Supongamos que
   `insertion_sort_rec(arr, n-1)` …"*
3. ¿Por qué basta con insertar `arr[n-1]` en su lugar correcto después de la llamada
   recursiva?
4. Plantear la relación de recurrencia para el peor caso de este algoritmo:

$$
T(n) = T(n-1) + \,?, \quad T(1) = 1
$$

   ¿Cuánto vale el término `?` y qué valor exacto tiene $T(n)$ al resolver la recurrencia?

---

## Parte 1. Búsqueda binaria

### 1.1 Marco conceptual

La búsqueda lineal recorre el arreglo elemento a elemento: en el peor caso realiza $n$
comparaciones. Si el arreglo está **ordenado**, podemos hacer algo más inteligente:
comparar con el elemento del **medio** y descartar la mitad donde el objetivo no puede
estar.

### 1.2 Descubrimiento guiado

Trabaja estos escenarios **antes de implementar**:

1. Tienes el arreglo ordenado $A = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]$
   (índices 0 al 10) y buscas el valor $23$.
   - El elemento del medio es $A[5] = 23$. ¿Lo encontraste? ¿Cuántas comparaciones
     necesitaste?

2. Repite para buscar $16$ en el mismo arreglo:
   - Primer paso: compara con $A[5] = 23$. Como $16 < 23$, ¿en qué mitad continúas?
   - Segundo paso: el nuevo subarreglo es $A[0..4] = [2, 5, 8, 12, 16]$, el elemento
     del medio es $A[2] = 8$. Como $16 > 8$, ¿en qué mitad continúas?
   - Tercer paso: el subarreglo es $A[3..4] = [12, 16]$, el elemento del medio es
     $A[3] = 12$. Como $16 > 12$, ¿en qué mitad continúas?
   - Cuarto paso: el subarreglo es $A[4..4] = [16]$. ¿Lo encontraste?
   - ¿Cuántas comparaciones realizaste en total?

3. Busca el valor $99$ (que **no** está en el arreglo). ¿Cómo sabes que no está cuando el
   subarreglo queda vacío?

4. Completa la traza de la búsqueda de $16$ en la siguiente tabla:

   | Paso | `lo` | `hi` | `mid` | `A[mid]` | Decisión |
   |:---:|:---:|:---:|:---:|:---:|:---|
   | 1 | 0 | 10 | 5 | 23 | buscar en mitad izquierda |
   | 2 | 0 | 4 | 2 | 8 | |
   | 3 | | | | | |
   | 4 | | | | | |

5. ¿En cuántos pasos como máximo puedes buscar en un arreglo de $n = 1\,000\,000$ de
   elementos? *(Pista: ¿cuántas veces puedes dividir $n$ entre 2 antes de llegar a 1?)*

### 1.3 Diseño del algoritmo

Antes de programar, **describe el algoritmo** respondiendo las tres preguntas del
esquema recursivo:

**Paso base:**  
¿Cuándo es el subarreglo tan pequeño que la respuesta es inmediata? ¿Qué devuelves
en ese caso?

> Escribe aquí tu respuesta: *"El paso base se da cuando `lo > hi`, lo que significa que
> el subarreglo está vacío. En ese caso devolvemos …"*

**Hipótesis inductiva:**  
Supón que `busqueda_binaria(arr, objetivo, lo, mid-1)` devuelve correctamente el índice
del objetivo dentro del subarreglo `arr[lo..mid-1]`, o `-1` si no existe.

> Completa: *"Supongo que `busqueda_binaria(arr, objetivo, mid+1, hi)` devuelve …"*

**Paso recursivo:**  
¿Cómo reduces el problema al subarreglo correcto y combinas la respuesta?

> Escribe aquí tu descripción en prosa antes de pasar al código.

### 1.4 Problema A — Implementación

Implementa la búsqueda binaria en la firma indicada. **Deja comentarios explícitos**
que identifiquen el paso base, la hipótesis y el paso recursivo:

```python
def busqueda_binaria(arr: list[int], objetivo: int,
                     lo: int = 0, hi: int = None) -> int:
    """
    Busca 'objetivo' en arr[lo..hi] (extremos inclusivos).

    Precondición: arr está ordenado de menor a mayor.
    Retorna el índice de 'objetivo' si existe, o -1 si no está.
    """
    if hi is None:
        hi = len(arr) - 1

    # TODO – Paso base

    # TODO – Cálculo del punto medio (usa (lo + hi) // 2)

    # TODO – Si arr[mid] == objetivo, ¿qué devuelves?

    # TODO – Paso recursivo: decide en qué mitad buscar y
    #         devuelve el resultado de la llamada recursiva.
```

**Restricciones:**
- La función debe ser estrictamente recursiva (sin ciclos).
- No uses la función `bisect` de la biblioteca estándar.

**Pruebas mínimas:**

```python
A = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
assert busqueda_binaria(A, 23)  == 5
assert busqueda_binaria(A, 16)  == 4
assert busqueda_binaria(A, 2)   == 0
assert busqueda_binaria(A, 91)  == 10
assert busqueda_binaria(A, 99)  == -1
assert busqueda_binaria(A, 1)   == -1
assert busqueda_binaria([], 5)  == -1
print("Todas las pruebas pasaron.")
```

### 1.5 Problema B — Contador de comparaciones

Modifica (o implementa por separado) una versión instrumentada:

```python
def busqueda_binaria_conteo(arr: list[int], objetivo: int,
                             lo: int, hi: int,
                             conteo: list[int]) -> int:
    """
    Igual que busqueda_binaria, pero incrementa conteo[0]
    en cada comparación con arr[mid].
    """
```

Usa esta versión para completar la siguiente tabla con arreglos de tamaño $n$:

| n | Comparaciones (mejor caso) | Comparaciones (peor caso) | $\lfloor\log_2 n\rfloor + 1$ |
|---:|:---:|:---:|:---:|
| 8 | | | 4 |
| 16 | | | 5 |
| 32 | | | 6 |
| 64 | | | 7 |
| 1 024 | | | 11 |
| 1 048 576 | | | 21 |

El **mejor caso** ocurre cuando el objetivo es exactamente el elemento del medio del
arreglo completo (una sola comparación). El **peor caso** ocurre cuando el objetivo no
está en el arreglo o está en uno de los extremos.

### 1.6 Problema C — Análisis de complejidad

**C.1 — Relación de recurrencia**

Cada llamada recursiva realiza un número **constante** de operaciones (calcular `mid`,
una comparación con `arr[mid]`) y luego llama a la búsqueda en una mitad del arreglo.
Sea $T(n)$ el número de comparaciones en el peor caso para un arreglo de tamaño $n$:

$$
T(n) = T\!\left(\frac{n}{2}\right) + 1, \qquad T(1) = 1
$$

1. Expande la recurrencia para $n = 8$ paso a paso:

$$
T(8) = T(4) + 1 = \bigl(T(2) + 1\bigr) + 1 = \cdots
$$

   ¿Cuántos pasos de expansión necesitas hasta llegar al caso base?

2. Generaliza: demuestra que $T(n) = \lfloor\log_2 n\rfloor + 1$.  
   *(Pista: después de $k$ expansiones el problema tiene tamaño $n/2^k$; el caso base se
   alcanza cuando $n/2^k = 1$, es decir $k = \log_2 n$.)*

3. Por lo tanto:

$$
T_{\text{peor}}(n) = O(\log n)
$$

**C.2 — Test de doblamiento**

Mide el tiempo de `busqueda_binaria` en el **peor caso** (elemento no presente) para
arreglos de tamaño creciente. Para obtener mediciones estables, repite cada experimento
al menos 10 000 veces y usa el tiempo promedio:

| n | T_peor (ns) promedio | Razón $T(2n) / T(n)$ |
|---:|---:|:---:|
| 1 000 | | — |
| 2 000 | | |
| 4 000 | | |
| 8 000 | | |
| 16 000 | | |
| 1 000 000 | | |

¿La razón es cercana a 1? ¿Qué sugiere eso sobre la complejidad?

> **Reflexión:** A diferencia de insertion sort (donde duplicar $n$ cuadruplicaba el
> tiempo), aquí duplicar $n$ apenas suma una comparación. ¿Por qué esto hace a la
> búsqueda binaria tan poderosa para colecciones grandes?

**C.3 — Comparación con búsqueda lineal**

Implementa también una búsqueda lineal:

```python
def busqueda_lineal(arr: list[int], objetivo: int) -> int:
    for i, v in enumerate(arr):
        if v == objetivo:
            return i
    return -1
```

Compara el tiempo de ambos algoritmos en el peor caso:

| n | T_lineal (µs) | T_binaria (ns) | Factor de mejora |
|---:|---:|---:|---:|
| 1 000 | | | |
| 100 000 | | | |
| 1 000 000 | | | |

¿A partir de qué valor de $n$ la diferencia se vuelve notable?

---

## Parte 2. Quick sort

### 2.1 Marco conceptual

Merge sort divide el arreglo en dos mitades **iguales**, ordena cada mitad y luego
**combina** (merge) en $O(n)$. Quick sort hace lo contrario: primero **particiona** el
arreglo en torno a un pivote (operación $O(n)$) y luego ordena cada parte. La
"combinación" es trivial (concatenación) porque la partición ya garantiza que los
elementos de la parte izquierda son menores o iguales que los de la derecha.

### 2.2 Descubrimiento guiado: la partición

Considera el arreglo $A = [3, 6, 8, 10, 1, 2, 1]$ y elige como pivote el **último
elemento** ($p = 1$).

El objetivo de la partición es reorganizar $A$ de modo que:
- todos los elementos $\leq p$ queden a la izquierda del pivote,
- todos los elementos $> p$ queden a la derecha.

**Algoritmo de partición de Lomuto** (el más sencillo de entender):

```
particiona(arr, lo, hi):
    pivot = arr[hi]          # último elemento como pivote
    i = lo - 1               # índice del último elemento ≤ pivot encontrado
    para j de lo hasta hi-1:
        si arr[j] <= pivot:
            i += 1
            intercambia arr[i] y arr[j]
    intercambia arr[i+1] y arr[hi]  # coloca el pivote en su lugar definitivo
    devuelve i + 1           # índice final del pivote
```

1. Aplica el algoritmo de Lomuto a mano sobre $A = [3, 6, 8, 10, 1, 2, 1]$, con
   $\text{lo}=0$ y $\text{hi}=6$. Llena la tabla:

   | j | arr[j] | ¿arr[j] ≤ pivot? | i tras el paso | Estado del arreglo |
   |:---:|:---:|:---:|:---:|:---|
   | 0 | 3 | No (3 > 1) | −1 | [3, 6, 8, 10, 1, 2, **1**] |
   | 1 | 6 | | | |
   | 2 | 8 | | | |
   | 3 | 10 | | | |
   | 4 | 1 | | | |
   | 5 | 2 | | | |
   | — | intercambio final | — | | |

   ¿En qué índice quedó el pivote? ¿Todos los elementos a su izquierda son ≤ 1? ¿Y los
   de la derecha son ≥ 1?

2. Después de la partición, ¿necesitas mover el pivote de nuevo para ordenar el arreglo
   completo? ¿Por qué?

3. Si el arreglo ya estuviera ordenado $[1, 2, 3, 4, 5]$ y eliges siempre el último
   elemento como pivote, ¿cuántos elementos quedan en la parte izquierda y cuántos en la
   derecha después de cada partición? ¿Qué forma tiene el árbol de llamadas recursivas?

### 2.3 Diseño del algoritmo

Responde las tres preguntas antes de programar:

**Paso base:**  
¿Cuándo un subarreglo ya está ordenado sin hacer nada?

> *"El paso base ocurre cuando `lo >= hi`, es decir, cuando el subarreglo tiene …
> elementos. En ese caso …"*

**Hipótesis inductiva:**  
Supón que `quicksort(arr, lo, p-1)` ordena correctamente `arr[lo..p-1]` y que
`quicksort(arr, p+1, hi)` ordena correctamente `arr[p+1..hi]`.

> Completa: *"Supongo que ambas llamadas recursivas ordenan correctamente sus
> subarreglos respectivos. Entonces, después de `particiona`, el pivote en `arr[p]`
> ya está en su posición definitiva porque …"*

**Paso recursivo:**  
¿Qué operación realiza el nivel actual (no recursivo) y cómo combina los resultados?

> *"En el paso recursivo: (1) particionamos `arr[lo..hi]` en torno al pivote,
> obteniendo su posición `p`; (2) …"*

### 2.4 Problema A — Implementación de la partición

```python
def particiona(arr: list, lo: int, hi: int) -> int:
    """
    Reorganiza arr[lo..hi] (Lomuto) en torno al pivote arr[hi].

    Postcondición:
        - arr[p] == pivote, donde p es el índice devuelto.
        - arr[lo..p-1] <= arr[p] <= arr[p+1..hi].

    Retorna el índice final del pivote.
    """
    pivot = arr[hi]
    i = lo - 1

    # TODO: recorre j de lo hasta hi-1 (inclusive).
    #       Si arr[j] <= pivot, incrementa i e intercambia arr[i] con arr[j].

    # TODO: coloca el pivote en su posición definitiva (intercambia arr[i+1] con arr[hi])
    # TODO: devuelve i + 1

```

**Pruebas mínimas de la partición:**

```python
A = [3, 6, 8, 10, 1, 2, 1]
p = particiona(A, 0, 6)
assert A[p] == 1
assert all(v <= 1 for v in A[:p])
assert all(v >= 1 for v in A[p+1:])
print(f"Partición correcta: {A}, pivote en índice {p}")
```

### 2.5 Problema B — Implementación de quick sort

```python
def quicksort(arr: list, lo: int = 0, hi: int = None) -> None:
    """
    Ordena arr[lo..hi] en su lugar usando quick sort (Lomuto).

    Modifica arr directamente (in-place). No devuelve nada.
    """
    if hi is None:
        hi = len(arr) - 1

    # TODO – Paso base: si lo >= hi, el subarreglo ya está ordenado; retorna.

    # TODO – Paso recursivo:
    #   1. Llama a particiona(arr, lo, hi) y guarda el índice del pivote en p.
    #   2. Llama recursivamente a quicksort para la mitad izquierda (lo..p-1).
    #   3. Llama recursivamente a quicksort para la mitad derecha (p+1..hi).
```

**Pruebas mínimas:**

```python
import random

def verificar_ordenamiento(n: int, semilla: int = 42) -> bool:
    random.seed(semilla)
    arr = [random.randint(-1000, 1000) for _ in range(n)]
    referencia = sorted(arr)
    quicksort(arr)
    return arr == referencia

assert verificar_ordenamiento(0)
assert verificar_ordenamiento(1)
assert verificar_ordenamiento(2)
assert verificar_ordenamiento(100)
assert verificar_ordenamiento(10_000)
print("Quick sort correcto en todos los casos.")
```

### 2.6 Problema C — Elección del pivote y peor caso

El pivote elegido determina la calidad de la partición:

1. **Peor caso — pivote siempre mínimo o máximo.** Ocurre cuando el arreglo está
   ordenado (o inversamente ordenado) y siempre se elige el último elemento como pivote.
   En ese caso, una de las dos partes siempre tiene 0 elementos:

$$
T(n) = T(0) + T(n-1) + cn = T(n-1) + cn
$$

   Resuelve esta recurrencia por expansión:

$$
T(n) = cn + c(n-1) + c(n-2) + \cdots + c \cdot 1 = c\,\frac{n(n+1)}{2} \implies T_{\text{peor}}(n) = O(n^2)
$$

2. **Mejor caso — pivote siempre en la mediana.** Cada partición divide el arreglo en
   dos mitades exactamente iguales:

$$
T(n) = 2\,T\!\left(\frac{n}{2}\right) + cn
$$

   ¿Reconoces esta recurrencia? ¿A qué algoritmo visto en clase corresponde?
   Aplica el **teorema maestro** (o el árbol de recursión) para demostrar que
   $T_{\text{mejor}}(n) = O(n \log n)$.

3. Implementa la mejora del **pivote aleatorio** para evitar el peor caso en entradas
   ordenadas:

```python
def particiona_aleatoria(arr: list, lo: int, hi: int) -> int:
    """
    Igual que particiona, pero primero intercambia arr[hi] con un
    elemento aleatorio de arr[lo..hi].
    """
    import random
    idx = random.randint(lo, hi)
    arr[idx], arr[hi] = arr[hi], arr[idx]
    return particiona(arr, lo, hi)
```

   ¿Por qué esta pequeña modificación cambia radicalmente el comportamiento en entradas
   ordenadas?

### 2.7 Problema D — Análisis experimental

**D.1 — Instrumentación**

Añade un contador de comparaciones a tu implementación de quick sort. El único lugar
donde se compara elementos es dentro del ciclo de la partición.

```python
def quicksort_conteo(arr: list, lo: int, hi: int, conteo: list) -> None:
    """Igual que quicksort, pero incrementa conteo[0] por cada comparación."""
```

**D.2 — Experimento de doblamiento**

Usa `quicksort_conteo` en tres escenarios para arreglos de tamaño $n$:

| n | Comparaciones (aleatorio) | Comparaciones (ordenado, sin pivote aleatorio) | Comparaciones (ordenado, con pivote aleatorio) |
|---:|---:|---:|---:|
| 100 | | | |
| 1 000 | | | |
| 2 000 | | | |
| 4 000 | | | |
| 8 000 | | | |

Calcula el **test de doblamiento** para el escenario de arreglo aleatorio:

| n | Comparaciones | Razón |
|---:|---:|:---:|
| 1 000 | | — |
| 2 000 | | |
| 4 000 | | |
| 8 000 | | |

¿La razón converge a ≈ 2? ¿Qué clase de crecimiento sugiere eso?

**D.3 — Deducción matemática del caso promedio**

Para quick sort con pivote aleatorio, puede demostrarse que el número esperado de
comparaciones satisface:

$$
T(n) = 2\,T\!\left(\frac{n}{2}\right) + O(n) \implies T_{\text{promedio}}(n) = O(n \log n)
$$

El factor de 2 frente al $n \log n$ de merge sort es la constante oculta. En la
práctica, quick sort suele ser **más rápido en memoria caché** porque accede al arreglo
de forma más localizada.

**D.4 — Comparación con merge sort (o sorted de Python)**

Mide el tiempo de ejecución de tu `quicksort` y de `sorted()` para arreglos aleatorios
de tamaño creciente:

| n | T_quicksort (ms) | T_sorted (ms) | Razón |
|---:|---:|---:|---:|
| 1 000 | | | |
| 10 000 | | | |
| 100 000 | | | |

¿A partir de qué tamaño empieza a notarse la diferencia? ¿Qué optimizaciones incorpora
`sorted()` que tu implementación no tiene?

---

## Parte 3. Síntesis y comparación

### 3.1 Cuadro comparativo de algoritmos recursivos

Completa el cuadro con los resultados de las Partes 1 y 2, y agrega los algoritmos
vistos en clase:

| Algoritmo | Estrategia | Recurrencia (peor caso) | $T(n)$ peor caso | $T(n)$ mejor caso |
|:---|:---|:---:|:---:|:---:|
| Insertion sort recursivo | Incremental | $T(n) = T(n-1) + O(n)$ | $O(n^2)$ | $O(n)$ |
| Merge sort | Divide y vencerás | $T(n) = 2T(n/2) + O(n)$ | $O(n \log n)$ | $O(n \log n)$ |
| Búsqueda binaria | Divide y vencerás | $T(n) = T(n/2) + O(1)$ | $O(\log n)$ | $O(1)$ |
| Quick sort (pivote fijo) | Divide y vencerás | $T(n) = T(n-1) + O(n)$ | $O(n^2)$ | $O(n \log n)$ |
| Quick sort (pivote aleatorio) | Divide y vencerás | — | $O(n^2)$ (improbable) | $O(n \log n)$ esperado |

### 3.2 Preguntas de reflexión final (responder en el reporte)

1. **Paso base compartido.** Tanto la búsqueda binaria como quick sort tienen el mismo
   paso base estructural. ¿Cuál es? ¿Por qué tiene sentido que sea el mismo?

2. **Rol de la hipótesis inductiva.** En la búsqueda binaria, la hipótesis dice que la
   llamada recursiva "encontrará el objetivo en la mitad correcta si existe". En quick
   sort, la hipótesis dice que "cada llamada recursiva ordenará correctamente su
   subarreglo". ¿Cómo justifica la partición que esas hipótesis son suficientes para
   ordenar el arreglo completo?

3. **Peor caso de quick sort vs. merge sort.** Ambos son $O(n \log n)$ en el caso
   promedio, pero quick sort puede degradarse a $O(n^2)$. Sin embargo, en la práctica
   quick sort suele ser más rápido. ¿Cómo se explica esa paradoja?

4. **Búsqueda binaria y datos ordenados.** ¿Por qué la búsqueda binaria **requiere**
   que el arreglo esté ordenado? Si tuvieras una colección de $10^9$ elementos que se
   consulta muchas veces pero rara vez se modifica, ¿valdría la pena ordenarla una sola
   vez para después usar búsqueda binaria? Justifica con complejidades.

5. **Límites de la recursión en Python.** Python tiene un límite por defecto de
   ~1 000 llamadas recursivas anidadas (`sys.getrecursionlimit()`). ¿Para qué tamaño
   de arreglo ordenado podría fallar tu implementación recursiva de búsqueda binaria
   sin modificar ese límite? ¿Y quick sort en el peor caso?

### 3.3 Actividad de cierre: diseña tu propio algoritmo recursivo

El equipo elige **uno** de los siguientes problemas y lo diseña siguiendo
**explícitamente** el esquema: paso base → hipótesis inductiva → paso recursivo.
No es obligatorio implementarlo, pero sí enunciarlo con claridad y escribir su
relación de recurrencia.

**Opción A — Potencia rápida:**  
Calcula $x^n$ en $O(\log n)$ usando la identidad $x^n = (x^{n/2})^2$ si $n$ es par.

**Opción B — Máximo en un arreglo:**  
Encuentra el máximo de `arr[lo..hi]` de forma recursiva. ¿Cuál es la relación de
recurrencia? ¿Es mejor o igual que el algoritmo iterativo?

**Opción C — Palíndromo recursivo:**  
Determina si una cadena es palíndromo sin ciclos. ¿Cuándo es el paso base? ¿Cómo
reduces el problema?

---

## Apéndice: implementación de referencia para la partición de Lomuto

El siguiente pseudocódigo es la referencia canónica. No lo copies directamente;
úsalo sólo para verificar tu razonamiento si te atascas:

```
particiona(arr, lo, hi):
    pivot ← arr[hi]
    i ← lo − 1
    para j ← lo hasta hi − 1:
        si arr[j] ≤ pivot:
            i ← i + 1
            intercambia(arr[i], arr[j])
    intercambia(arr[i + 1], arr[hi])
    devuelve i + 1
```

La invariante del ciclo es: en todo momento, `arr[lo..i] ≤ pivot` y
`arr[i+1..j-1] > pivot`. Verifica que tu implementación mantiene esta invariante
en cada iteración del ciclo.
