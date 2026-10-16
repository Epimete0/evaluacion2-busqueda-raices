# Informe: búsqueda de raíces

Se usó tolerancia `1e-6` y máximo 100 iteraciones. La raíz de referencia se calculó por bisección con tolerancia `1e-12`, excepto la raíz doble, que es exactamente 2.

## Ambiente

| Función | Intervalo | x0 | x1 | f(a) | f(b) | Cambio de signo |
|---|---:|---:|---:|---:|---:|---|
| x³ − x − 2 | [1, 2] | 1.5 | 1.6 | -2 | 4 | sí |
| (x − 2)² | — | 1.2 | 1.3 | — | — | no; f(2)=0, f'(2)=0, f(x)≥0 |
| ln(x) + x − 4 | [2, 3] | 2.5 | 2.6 | -1.306853 | 0.098612 | sí |
| exp(−x) − x | [0, 1] | 0.5 | 0.6 | 1 | -0.632121 | sí |
| cos(x) − x | [0, 1] | 0.5 | 0.6 | 1 | -0.459698 | sí |
| √x − cos(x) | [0.1, 1] | 0.5 | 0.6 | -0.678776 | 0.459698 | sí |

## Iteraciones

| Función | Bisección | Falsa posición | Punto fijo | Secante | Newton | Newton mejorado |
|---|---:|---:|---:|---:|---:|---:|
| x³ − x − 2 | 20 | 12 | 7 | 3 | 2 | 2 |
| (x − 2)² | N/A | N/A | 10 | 14 | 10 | 1 |
| ln(x) + x − 4 | 19 | 4 | 13 | 3 | 3 | 3 |
| exp(−x) − x | 20 | 7 | 21 | 3 | 2 | 2 |
| cos(x) − x | 20 | 5 | 33 | 3 | 3 | 3 |
| √x − cos(x) | 20 | 4 | 13 | 3 | 2 | 2 |

`N/A`: el método no aplica por falta de intervalo con cambio de signo. Los errores finales por método y función son:

| Función | Bisección | Falsa posición | Punto fijo | Secante | Newton | Newton mejorado |
|---|---:|---:|---:|---:|---:|---:|
| x³ − x − 2 | 7.17695e-7 | 2.45014e-7 | 2.75331e-8 | 6.96131e-8 | 9.91603e-8 | 9.73089e-8 |
| (x − 2)² | N/A | N/A | 7.81250e-4 | 7.44779e-4 | 7.81250e-4 | 0 |
| ln(x) + x − 4 | 3.76155e-7 | 4.19379e-7 | 3.91587e-7 | 3.23433e-8 | 5.77316e-13 | 1.48059e-12 |
| exp(−x) − x | 1.49837e-7 | 8.56248e-8 | 4.61008e-7 | 1.72990e-10 | 1.25374e-7 | 1.36984e-7 |
| cos(x) − x | 6.42340e-8 | 3.50766e-7 | 4.60654e-7 | 5.74902e-7 | 7.06049e-10 | 1.04938e-9 |
| √x − cos(x) | 1.12992e-8 | 5.31698e-7 | 6.82749e-7 | 2.95272e-10 | 4.95920e-7 | 1.14620e-7 |

El detalle de raíces, errores y estados está en [resumen_convergencia.csv](src/data/resumen_convergencia.csv); el orden observado está en [orden_convergencia.csv](src/data/orden_convergencia.csv) y las pruebas de inicios están en [sensibilidad.csv](src/data/sensibilidad.csv).

## Gráficos

| Función | Curva y raíz | Error por iteración |
|---|---|---|
| x³ − x − 2 | ![](src/assets/funcion_1.png) | ![](src/assets/error_1.png) |
| (x − 2)² | ![](src/assets/funcion_2.png) | ![](src/assets/error_2.png) |
| ln(x) + x − 4 | ![](src/assets/funcion_3.png) | ![](src/assets/error_3.png) |
| exp(−x) − x | ![](src/assets/funcion_4.png) | ![](src/assets/error_4.png) |
| cos(x) − x | ![](src/assets/funcion_5.png) | ![](src/assets/error_5.png) |
| √x − cos(x) | ![](src/assets/funcion_6.png) | ![](src/assets/error_6.png) |

Comparación de iteraciones:

![](src/assets/iteraciones_metodos.png)

## Respuestas

1. **Método con menos iteraciones:** Newton mejorado necesitó una iteración en la raíz doble y dos en tres funciones. Para las otras, Newton o Newton mejorado usaron entre dos y tres iteraciones. Aprovechan las derivadas y avanzan rápido cerca de la raíz.
2. **Orden de convergencia:** bisección reduce el intervalo de forma lineal; secante suele mostrar convergencia superlineal; Newton cuadrática para raíces simples, y Newton mejorado acelera especialmente raíces múltiples. En las gráficas se ve como una bajada más rápida del error, aunque los puntos dejan de distinguirse cerca de la tolerancia.
3. **Cambio de signo:** bisección y falsa posición lo necesitan. En la raíz doble no hay cambio de signo, así que no aplican.
4. **Raíz doble:** la curva toca el eje en 2 sin cruzarlo. Newton clásico y punto fijo tardaron 10 iteraciones, secante 14 y Newton mejorado llegó a 2 en una iteración.
5. **Intervalo e inicio:** en sensibilidad, bisección del cúbico convergió en 20 iteraciones con [1,2], pero [0,1] no aplica. Newton convergió en 2 a 30 iteraciones según el inicio. Para exp(−x)−x, Newton usó 3 iteraciones desde 0 y 4 desde 2.
6. **Recomendación:** usar bisección si se busca un método seguro y hay cambio de signo; falsa posición reduce iteraciones en varios casos (4 para logaritmo y raíz cuadrada); Newton si se conoce la derivada y el inicio es razonable; Newton mejorado para raíces múltiples. Punto fijo depende mucho de la función g: para √x−cos(x) no convergió en 100 iteraciones.

## Conclusión

Newton y Newton mejorado fueron los más rápidos en cinco funciones, con 2–3 iteraciones; para la raíz doble, Newton mejorado necesitó 1. En cambio, el punto fijo de √x−cos(x) no convergió en 100. Los datos muestran que el método y el inicio sí cambian el resultado.
