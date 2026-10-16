# Búsqueda de raíces

Proyecto de laboratorio de métodos numéricos. Compara seis métodos para seis funciones y guarda tablas y gráficos.

## Preparar el entorno

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar desde la carpeta principal:

```bash
python src/scripts/ejecutar_todo.py
```

- `metodos.py`: implementa los seis métodos de búsqueda.
- `funciones.py`: define las funciones, derivadas y estimaciones iniciales.
- `ejecutar_todo.py`: calcula las raíces y crea los CSV y gráficos.
