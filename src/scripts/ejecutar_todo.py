import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from funciones import funciones
from metodos import biseccion, falsa_posicion, punto_fijo, secante, newton, newton_mejorado

BASE = os.path.dirname(os.path.dirname(__file__))
DATOS = os.path.join(BASE, "data")
IMAGENES = os.path.join(BASE, "assets")
TOL = 1e-6
MAX_ITER = 100
METODOS = ["biseccion", "falsa_posicion", "punto_fijo", "secante", "newton", "newton_mejorado"]


def raiz_real(funcion):
    f = funcion["f"]
    if funcion["nombre"] == "(x - 2)^2":
        return 2.0
    a, b = funcion["a"], funcion["b"]
    for i in range(1000):
        medio = (a + b) / 2
        if abs(f(medio)) < 1e-12 or abs(b - a) < 1e-12:
            return medio
        if f(a) * f(medio) < 0:
            b = medio
        else:
            a = medio
    return medio


def ejecutar_metodo(metodo, funcion, a=None, b=None, x0=None, x1=None):
    f = funcion["f"]
    if metodo == "biseccion":
        if a is None or b is None:
            print("Bisección no aplica: función sin intervalo")
            return []
        return biseccion(f, a, b, TOL, MAX_ITER)
    if metodo == "falsa_posicion":
        if a is None or b is None:
            print("Falsa posición no aplica: función sin intervalo")
            return []
        return falsa_posicion(f, a, b, TOL, MAX_ITER)
    if metodo == "punto_fijo":
        return punto_fijo(funcion["g"], f, x0, TOL, MAX_ITER)
    if metodo == "secante":
        return secante(f, x0, x1, TOL, MAX_ITER)
    if metodo == "newton":
        return newton(f, funcion["df"], x0, TOL, MAX_ITER)
    return newton_mejorado(f, funcion["df"], funcion["d2f"], x0, TOL, MAX_ITER)


def estado_historial(historial):
    if not historial:
        return "no aplica"
    if abs(historial[-1][2]) < TOL or (len(historial) > 1 and abs(historial[-1][1] - historial[-2][1]) < TOL):
        return "convergió"
    return "no convergió"


def guardar_curva(funcion, raiz, indice):
    f = funcion["f"]
    if funcion["a"] is None:
        xs = np.linspace(0.5, 3.5, 200)
    else:
        xs = np.linspace(funcion["a"], funcion["b"], 200)
    ys = [f(x) for x in xs]
    with open(os.path.join(DATOS, "funcion_" + str(indice + 1) + ".csv"), "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["x", "f(x)"])
        for x, y in zip(xs, ys):
            escritor.writerow([x, y])
    plt.figure()
    plt.plot(xs, ys, label="f(x)")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.scatter([raiz], [f(raiz)], color="red", label="raíz")
    plt.title(funcion["nombre"])
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(IMAGENES, "funcion_" + str(indice + 1) + ".png"))
    plt.close()


def main():
    os.makedirs(DATOS, exist_ok=True)
    os.makedirs(IMAGENES, exist_ok=True)
    lista = funciones()
    resumen = []
    historiales = {}
    raices = {}
    for j, funcion in enumerate(lista):
        raiz = raiz_real(funcion)
        raices[funcion["nombre"]] = raiz
        print("\n", funcion["nombre"], "tol=", TOL)
        if funcion["a"] is None:
            print("x0=", funcion["x0"], "f(2)=", funcion["f"](2), "f'(2)=", funcion["df"](2), "f(x)>=0: sí")
        else:
            a, b = funcion["a"], funcion["b"]
            print("intervalo=", (a, b), "f(a)=", funcion["f"](a), "f(b)=", funcion["f"](b), "f(a)*f(b)<0:", funcion["f"](a)*funcion["f"](b) < 0)
        guardar_curva(funcion, raiz, j)
        for metodo in METODOS:
            historial = ejecutar_metodo(metodo, funcion, funcion["a"], funcion["b"], funcion["x0"], funcion["x1"])
            estado = estado_historial(historial)
            x = historial[-1][1] if historial else ""
            error = abs(x - raiz) if historial else ""
            resumen.append([funcion["nombre"], metodo, len(historial), x, error, estado])
            historiales[(funcion["nombre"], metodo)] = historial
    with open(os.path.join(DATOS, "resumen_convergencia.csv"), "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["funcion", "metodo", "iteraciones", "raiz", "error", "estado"])
        escritor.writerows(resumen)

    for i, funcion in enumerate(lista):
        plt.figure()
        for metodo in METODOS:
            historial = historiales[(funcion["nombre"], metodo)]
            if historial:
                errores = [max(abs(punto[1] - raices[funcion["nombre"]]), 1e-16) for punto in historial]
                plt.plot(range(1, len(errores) + 1), errores, marker=".", label=metodo)
        plt.yscale("log")
        plt.title("Error por iteración: " + funcion["nombre"])
        plt.xlabel("Iteración")
        plt.ylabel("|error|")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(IMAGENES, "error_" + str(i + 1) + ".png"))
        plt.close()

    plt.figure(figsize=(12, 6))
    posiciones = np.arange(len(lista))
    ancho = 0.13
    for k, metodo in enumerate(METODOS):
        valores = [next((fila[2] for fila in resumen if fila[0] == f["nombre"] and fila[1] == metodo), 0) for f in lista]
        plt.bar(posiciones + k*ancho, valores, ancho, label=metodo)
    plt.xticks(posiciones + ancho*2.5, [f["nombre"] for f in lista], rotation=20, ha="right")
    plt.title("Iteraciones por método y función")
    plt.xlabel("Función")
    plt.ylabel("Iteraciones")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGENES, "iteraciones_metodos.png"))
    plt.close()

    sensibilidad = []
    casos = [(lista[0], [(1, 2), (0, 1), (1.5, 2)]), (lista[3], [(0, 1), (2, 3), (-1, 1)]), (lista[1], [(1.2, 1.2), (2.5, 2.5), (5, 5)])]
    for funcion, pruebas in casos:
        for p, q in pruebas:
            for metodo in ["biseccion", "newton"]:
                h = ejecutar_metodo(metodo, funcion, p, q, p, q + 0.1)
                estado = estado_historial(h)
                sensibilidad.append([funcion["nombre"], metodo, p, q, len(h), estado])
    with open(os.path.join(DATOS, "sensibilidad.csv"), "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["funcion", "metodo", "inicio_a_x0", "fin_x1", "iteraciones", "estado"])
        escritor.writerows(sensibilidad)
    print("\nArchivos generados en src/data y src/assets")


if __name__ == "__main__":
    main()
