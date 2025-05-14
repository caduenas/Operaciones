# Métodos de Decisión

Este proyecto implementa una aplicación gráfica para trabajar con matrices y métodos de decisión. La interfaz gráfica está desarrollada en Python utilizando la biblioteca `tkinter`.

## Estructura del Proyecto

El proyecto está organizado en los siguientes directorios:

- `Main/`: Contiene el archivo principal para ejecutar la aplicación.
- `Controller/`: Contiene la lógica de control de la aplicación.
- `View/`: Contiene la interfaz gráfica de usuario (GUI).
- `Model/`: Contiene la lógica relacionada con los datos y cálculos.

## Requisitos

- Python 3.8 o superior
- Bibliotecas estándar de Python (`tkinter`)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/caduenas/Operaciones
   cd Operaciones
   
2. Asegúrate de tener Python instalado. Puedes verificarlo ejecutando:
   ```bash
   python --version
   
3. No se requieren dependencias adicionales, ya que `tkinter` viene incluido con Python.

## Ejecución

Para iniciar la aplicación, ejecuta el archivo principal:
   ```bash
    cd Main
    python Main/main.py
   ```
    
## Uso

1. `Formulario de entrada:` Ingresa el número de filas y columnas de la matriz, selecciona el modo de llenado (manual o automático) y proporciona el valor de α (entre 0 y 1). 
2. `Generar matriz:` Haz clic en el botón "Generar Matriz" para crear la matriz. 
3. `Resultados:` Los resultados de los métodos de decisión se mostrarán en la sección de resultados.

## Funcionalidades

El proyecto está organizado en los siguientes directorios:

- `Interfaz gráfica:` Una GUI intuitiva para ingresar datos y visualizar resultados. 
- `Llenado de matriz:` Permite el llenado manual o automático de matrices. 
- `Resultados organizados:` Los resultados se presentan de manera estructurada y alineada a la izquierda.

## Estructura de Archivos

    metodos-decision/
    ├── Main/
    │   └── main.py
    ├── Controller/
    │   └── main_controller.py
    ├── View/
    │   └── gui_view.py
    ├── Model/
    │   └── decision_methods.py
    └── README.md