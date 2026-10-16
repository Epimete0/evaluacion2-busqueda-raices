def biseccion(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) >= 0:
        print("Bisección no aplica: no hay cambio de signo")
        return []
    historial = []
    anterior = None
    for i in range(max_iter):
        x = (a + b) / 2
        historial.append((i + 1, x, f(x)))
        if abs(f(x)) < tol or (anterior is not None and abs(x - anterior) < tol):
            return historial
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        anterior = x
    print("Bisección no converge")
    return historial


def falsa_posicion(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) >= 0:
        print("Falsa posición no aplica: no hay cambio de signo")
        return []
    historial = []
    anterior = None
    for i in range(max_iter):
        x = (a*f(b) - b*f(a)) / (f(b) - f(a))
        historial.append((i + 1, x, f(x)))
        if abs(f(x)) < tol or (anterior is not None and abs(x - anterior) < tol):
            return historial
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        anterior = x
    print("Falsa posición no converge")
    return historial


def punto_fijo(g, f, x0, tol=1e-6, max_iter=100):
    historial = []
    anterior = x0
    for i in range(max_iter):
        x = g(anterior)
        historial.append((i + 1, x, f(x)))
        if abs(f(x)) < tol or abs(x - anterior) < tol:
            return historial
        anterior = x
    print("Punto fijo no converge")
    return historial


def secante(f, x0, x1, tol=1e-6, max_iter=100):
    historial = []
    for i in range(max_iter):
        if f(x1) == f(x0):
            print("Secante no converge: división por cero")
            return historial
        x = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0))
        historial.append((i + 1, x, f(x)))
        if abs(f(x)) < tol or abs(x - x1) < tol:
            return historial
        x0, x1 = x1, x
    print("Secante no converge")
    return historial


def newton(f, df, x0, tol=1e-6, max_iter=100):
    historial = []
    x = x0
    for i in range(max_iter):
        if df(x) == 0:
            print("Newton no converge: derivada cero")
            return historial
        nuevo = x - f(x)/df(x)
        historial.append((i + 1, nuevo, f(nuevo)))
        if abs(f(nuevo)) < tol or abs(nuevo - x) < tol:
            return historial
        x = nuevo
    print("Newton no converge")
    return historial


def newton_mejorado(f, df, d2f, x0, tol=1e-6, max_iter=100):
    historial = []
    x = x0
    for i in range(max_iter):
        divisor = df(x)**2 - f(x)*d2f(x)
        if divisor == 0:
            print("Newton mejorado no converge: división por cero")
            return historial
        nuevo = x - f(x)*df(x)/divisor
        historial.append((i + 1, nuevo, f(nuevo)))
        if abs(f(nuevo)) < tol or abs(nuevo - x) < tol:
            return historial
        x = nuevo
    print("Newton mejorado no converge")
    return historial
