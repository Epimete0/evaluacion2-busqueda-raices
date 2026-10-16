import numpy as np


def funciones():
    # g elegidas en el mismo orden: cbrt(x+2), (x+2)/2, 4-ln(x), exp(-x), cos(x), cos²(x).
    return [
        {
            "nombre": "x^3 - x - 2",
            "funcion": lambda x: x**3 - x - 2,
            "derivada": lambda x: 3*x**2 - 1,
            "segunda_derivada": lambda x: 6*x,
            "punto_fijo": lambda x: np.cbrt(x + 2),
            "a": 1, "b": 2, "x_inicial": 1.5, "segundo_inicio": 1.6,
        },
        {
            "nombre": "(x - 2)^2",
            "funcion": lambda x: (x - 2)**2,
            "derivada": lambda x: 2*(x - 2),
            "segunda_derivada": lambda x: 2,
            "punto_fijo": lambda x: (x + 2)/2,
            "a": None, "b": None, "x_inicial": 1.2, "segundo_inicio": 1.3,
        },
        {
            "nombre": "ln(x) + x - 4",
            "funcion": lambda x: np.log(x) + x - 4,
            "derivada": lambda x: 1/x + 1,
            "segunda_derivada": lambda x: -1/x**2,
            "punto_fijo": lambda x: 4 - np.log(x),
            "a": 2, "b": 3, "x_inicial": 2.5, "segundo_inicio": 2.6,
        },
        {
            "nombre": "exp(-x) - x",
            "funcion": lambda x: np.exp(-x) - x,
            "derivada": lambda x: -np.exp(-x) - 1,
            "segunda_derivada": lambda x: np.exp(-x),
            "punto_fijo": lambda x: np.exp(-x),
            "a": 0, "b": 1, "x_inicial": 0.5, "segundo_inicio": 0.6,
        },
        {
            "nombre": "cos(x) - x",
            "funcion": lambda x: np.cos(x) - x,
            "derivada": lambda x: -np.sin(x) - 1,
            "segunda_derivada": lambda x: -np.cos(x),
            "punto_fijo": lambda x: np.cos(x),
            "a": 0, "b": 1, "x_inicial": 0.5, "segundo_inicio": 0.6,
        },
        {
            "nombre": "sqrt(x) - cos(x)",
            "funcion": lambda x: np.sqrt(x) - np.cos(x),
            "derivada": lambda x: 1/(2*np.sqrt(x)) + np.sin(x),
            "segunda_derivada": lambda x: -1/(4*x**1.5) + np.cos(x),
            "punto_fijo": lambda x: np.cos(x)**2,
            "a": 0.1, "b": 1, "x_inicial": 0.5, "segundo_inicio": 0.6,
        },
    ]
