import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from funciones import funciones
from metodos import biseccion, falsa_posicion, punto_fijo, secante, newton, newton_mejorado

CARPETA_SRC = os.path.dirname(os.path.dirname(__file__))
CARPETA_DATOS = os.path.join(CARPETA_SRC, "data")
CARPETA_GRAFICOS = os.path.join(CARPETA_SRC, "assets")
TOLERANCIA = 1e-6
MAX_ITERACIONES = 100
METODOS = ["biseccion", "falsa_posicion", "punto_fijo", "secante", "newton", "newton_mejorado"]


def raiz_real(funcion):
    calcular = funcion["funcion"]
    if funcion["nombre"] == "(x - 2)^2":
        return 2.0
    a, b = funcion["a"], funcion["b"]
    for iteracion in range(1000):
        medio = (a + b) / 2
        if abs(calcular(medio)) < 1e-12 or abs(b - a) < 1e-12:
            return medio
        if calcular(a) * calcular(medio) < 0:
            b = medio
        else:
            a = medio
    return medio


def ejecutar_metodo(metodo, datos_funcion, a=None, b=None, inicio=None, segundo_inicio=None,
                    tolerancia=TOLERANCIA, max_iteraciones=MAX_ITERACIONES):
    calcular = datos_funcion["funcion"]
    if metodo == "biseccion":
        if a is None or b is None:
            print("Bisección no aplica: función sin intervalo")
            return []
        return biseccion(calcular, a, b, tolerancia, max_iteraciones)
    if metodo == "falsa_posicion":
        if a is None or b is None:
            print("Falsa posición no aplica: función sin intervalo")
            return []
        return falsa_posicion(calcular, a, b, tolerancia, max_iteraciones)
    if metodo == "punto_fijo":
        return punto_fijo(datos_funcion["punto_fijo"], calcular, inicio, tolerancia, max_iteraciones)
    if metodo == "secante":
        return secante(calcular, inicio, segundo_inicio, tolerancia, max_iteraciones)
    if metodo == "newton":
        return newton(calcular, datos_funcion["derivada"], inicio, tolerancia, max_iteraciones)
    return newton_mejorado(calcular, datos_funcion["derivada"], datos_funcion["segunda_derivada"], inicio, tolerancia, max_iteraciones)


def estimar_orden(historial, raiz):
    errores = [abs(punto[1] - raiz) for punto in historial if abs(punto[1] - raiz) > 1e-13]
    if len(errores) < 3:
        return ""
    e_anterior, e_actual, e_siguiente = errores[-3:]
    return np.log(e_siguiente / e_actual) / np.log(e_actual / e_anterior)


def estado_historial(historial):
    if not historial:
        return "no aplica"
    if abs(historial[-1][2]) < TOLERANCIA or (len(historial) > 1 and abs(historial[-1][1] - historial[-2][1]) < TOLERANCIA):
        return "convergió"
    return "no convergió"


def guardar_curva(funcion, raiz, indice):
    calcular = funcion["funcion"]
    if funcion["a"] is None:
        valores_x = np.linspace(0.5, 3.5, 200)
    else:
        valores_x = np.linspace(funcion["a"], funcion["b"], 200)
    valores_y = [calcular(x) for x in valores_x]
    with open(os.path.join(CARPETA_DATOS, "funcion_" + str(indice + 1) + ".csv"), "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["x", "f(x)"])
        for x, valor_y in zip(valores_x, valores_y):
            escritor.writerow([x, valor_y])
    plt.figure()
    plt.plot(valores_x, valores_y, label="f(x)")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.scatter([raiz], [calcular(raiz)], color="red", label="raíz")
    plt.title(funcion["nombre"])
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "funcion_" + str(indice + 1) + ".png"))
    plt.close()


def main():
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    lista_funciones = funciones()
    resumen = []
    historiales = {}
    raices = {}
    for indice, funcion in enumerate(lista_funciones):
        raiz = raiz_real(funcion)
        raices[funcion["nombre"]] = raiz
        print("\n", funcion["nombre"], "tolerancia=", TOLERANCIA)
        if funcion["a"] is None:
            print("inicio=", funcion["x_inicial"], "f(2)=", funcion["funcion"](2), "f'(2)=", funcion["derivada"](2), "f(x)>=0: sí")
        else:
            a, b = funcion["a"], funcion["b"]
            print("intervalo=", (a, b), "f(a)=", funcion["funcion"](a), "f(b)=", funcion["funcion"](b), "f(a)*f(b)<0:", funcion["funcion"](a)*funcion["funcion"](b) < 0)
        guardar_curva(funcion, raiz, indice)
        for metodo in METODOS:
            historial = ejecutar_metodo(metodo, funcion, funcion["a"], funcion["b"], funcion["x_inicial"], funcion["segundo_inicio"])
            estado = estado_historial(historial)
            x = historial[-1][1] if historial else ""
            error = abs(x - raiz) if historial else ""
            resumen.append([funcion["nombre"], metodo, len(historial), x, error, estado])
            historiales[(funcion["nombre"], metodo)] = historial
    with open(os.path.join(CARPETA_DATOS, "resumen_convergencia.csv"), "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["funcion", "metodo", "iteraciones", "raiz", "error_final", "estado"])
        escritor.writerows(resumen)

    # Corrida separada a tolerancia estricta, solo para estimar el orden.
    ordenes = []
    for funcion in lista_funciones:
        raiz = raices[funcion["nombre"]]
        for metodo in METODOS:
            historial = ejecutar_metodo(metodo, funcion, funcion["a"], funcion["b"],
                                        funcion["x_inicial"], funcion["segundo_inicio"],
                                        tolerancia=1e-12, max_iteraciones=100)
            ordenes.append([funcion["nombre"], metodo, estimar_orden(historial, raiz)])
    with open(os.path.join(CARPETA_DATOS, "orden_convergencia.csv"), "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["funcion", "metodo", "orden_observado"])
        escritor.writerows(ordenes)

    for indice, funcion in enumerate(lista_funciones):
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
        plt.savefig(os.path.join(CARPETA_GRAFICOS, "error_" + str(indice + 1) + ".png"))
        plt.close()

    plt.figure(figsize=(12, 6))
    posiciones = np.arange(len(lista_funciones))
    ancho = 0.13
    for indice, metodo in enumerate(METODOS):
        iteraciones_grafico = [fila[2] for fila in resumen if fila[1] == metodo]
        plt.bar(posiciones + indice*ancho, iteraciones_grafico, ancho, label=metodo)
    plt.xticks(posiciones + ancho*2.5, [funcion["nombre"] for funcion in lista_funciones], rotation=20, ha="right")
    plt.title("Iteraciones por método y función")
    plt.xlabel("Función")
    plt.ylabel("Iteraciones")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "iteraciones_metodos.png"))
    plt.close()

    sensibilidad = []
    casos = [(lista_funciones[0], [(1, 2), (0, 1), (1.5, 2)]), (lista_funciones[3], [(0, 1), (2, 3), (-1, 1)]), (lista_funciones[1], [(1.2, 1.2), (2.5, 2.5), (5, 5)])]
    for funcion, pruebas in casos:
        for inicio, segundo_inicio in pruebas:
            for metodo in ["biseccion", "newton"]:
                historial = ejecutar_metodo(metodo, funcion, inicio, segundo_inicio, inicio, segundo_inicio + 0.1)
                estado = estado_historial(historial)
                sensibilidad.append([funcion["nombre"], metodo, inicio, segundo_inicio, len(historial), estado])
    with open(os.path.join(CARPETA_DATOS, "sensibilidad.csv"), "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["funcion", "metodo", "inicio_a_x0", "fin_x1", "iteraciones", "estado"])
        escritor.writerows(sensibilidad)
    print("\nArchivos generados en src/data y src/assets")


if __name__ == "__main__":
    main()
