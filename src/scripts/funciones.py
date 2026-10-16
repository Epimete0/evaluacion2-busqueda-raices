import numpy as np


def funciones():
    return [
        {"nombre": "x^3 - x - 2", "f": lambda x: x**3 - x - 2, "df": lambda x: 3*x**2 - 1, "d2f": lambda x: 6*x, "g": lambda x: np.cbrt(x + 2), "a": 1, "b": 2, "x0": 1.5, "x1": 1.6},
        {"nombre": "(x - 2)^2", "f": lambda x: (x - 2)**2, "df": lambda x: 2*(x - 2), "d2f": lambda x: 2, "g": lambda x: (x + 2)/2, "a": None, "b": None, "x0": 1.2, "x1": 1.3},
        {"nombre": "ln(x) + x - 4", "f": lambda x: np.log(x) + x - 4, "df": lambda x: 1/x + 1, "d2f": lambda x: -1/x**2, "g": lambda x: 4 - np.log(x), "a": 2, "b": 3, "x0": 2.5, "x1": 2.6},
        {"nombre": "exp(-x) - x", "f": lambda x: np.exp(-x) - x, "df": lambda x: -np.exp(-x) - 1, "d2f": lambda x: np.exp(-x), "g": lambda x: np.exp(-x), "a": 0, "b": 1, "x0": 0.5, "x1": 0.6},
        {"nombre": "cos(x) - x", "f": lambda x: np.cos(x) - x, "df": lambda x: -np.sin(x) - 1, "d2f": lambda x: -np.cos(x), "g": lambda x: np.cos(x), "a": 0, "b": 1, "x0": 0.5, "x1": 0.6},
        {"nombre": "sqrt(x) - cos(x)", "f": lambda x: np.sqrt(x) - np.cos(x), "df": lambda x: 1/(2*np.sqrt(x)) + np.sin(x), "d2f": lambda x: -1/(4*x**1.5) + np.cos(x), "g": lambda x: np.cos(x)**2, "a": 0.1, "b": 1, "x0": 0.5, "x1": 0.6},
    ]
