def biseccion(funcion, a, b, tolerancia=1e-6, max_iteraciones=100):
    if funcion(a) * funcion(b) >= 0:
        print("Bisección no aplica: no hay cambio de signo")
        return []
    historial = []
    anterior = None
    for iteracion in range(max_iteraciones):
        x = (a + b) / 2
        historial.append((iteracion + 1, x, funcion(x)))
        if abs(funcion(x)) < tolerancia or (anterior is not None and abs(x - anterior) < tolerancia):
            return historial
        if funcion(a) * funcion(x) < 0:
            b = x
        else:
            a = x
        anterior = x
    print("Bisección no converge")
    return historial


def falsa_posicion(funcion, a, b, tolerancia=1e-6, max_iteraciones=100):
    if funcion(a) * funcion(b) >= 0:
        print("Falsa posición no aplica: no hay cambio de signo")
        return []
    historial = []
    anterior = None
    for iteracion in range(max_iteraciones):
        x = (a*funcion(b) - b*funcion(a)) / (funcion(b) - funcion(a))
        historial.append((iteracion + 1, x, funcion(x)))
        if abs(funcion(x)) < tolerancia or (anterior is not None and abs(x - anterior) < tolerancia):
            return historial
        if funcion(a) * funcion(x) < 0:
            b = x
        else:
            a = x
        anterior = x
    print("Falsa posición no converge")
    return historial


def punto_fijo(funcion_iterativa, funcion, inicio, tolerancia=1e-6, max_iteraciones=100):
    historial = []
    anterior = inicio
    for iteracion in range(max_iteraciones):
        x = funcion_iterativa(anterior)
        historial.append((iteracion + 1, x, funcion(x)))
        if abs(funcion(x)) < tolerancia or abs(x - anterior) < tolerancia:
            return historial
        anterior = x
    print("Punto fijo no converge")
    return historial


def secante(funcion, inicio, segundo_inicio, tolerancia=1e-6, max_iteraciones=100):
    historial = []
    for iteracion in range(max_iteraciones):
        if funcion(segundo_inicio) == funcion(inicio):
            print("Secante no converge: división por cero")
            return historial
        x = segundo_inicio - funcion(segundo_inicio)*(segundo_inicio - inicio)/(funcion(segundo_inicio) - funcion(inicio))
        historial.append((iteracion + 1, x, funcion(x)))
        if abs(funcion(x)) < tolerancia or abs(x - segundo_inicio) < tolerancia:
            return historial
        inicio, segundo_inicio = segundo_inicio, x
    print("Secante no converge")
    return historial


def newton(funcion, derivada, inicio, tolerancia=1e-6, max_iteraciones=100):
    historial = []
    x = inicio
    for iteracion in range(max_iteraciones):
        if derivada(x) == 0:
            print("Newton no converge: derivada cero")
            return historial
        siguiente = x - funcion(x)/derivada(x)
        historial.append((iteracion + 1, siguiente, funcion(siguiente)))
        if abs(funcion(siguiente)) < tolerancia or abs(siguiente - x) < tolerancia:
            return historial
        x = siguiente
    print("Newton no converge")
    return historial


def newton_mejorado(funcion, derivada, segunda_derivada, inicio, tolerancia=1e-6, max_iteraciones=100):
    historial = []
    x = inicio
    for iteracion in range(max_iteraciones):
        divisor = derivada(x)**2 - funcion(x)*segunda_derivada(x)
        if divisor == 0:
            print("Newton mejorado no converge: división por cero")
            return historial
        siguiente = x - funcion(x)*derivada(x)/divisor
        historial.append((iteracion + 1, siguiente, funcion(siguiente)))
        if abs(funcion(siguiente)) < tolerancia or abs(siguiente - x) < tolerancia:
            return historial
        x = siguiente
    print("Newton mejorado no converge")
    return historial
