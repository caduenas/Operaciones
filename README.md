# Métodos de Decisión

Este proyecto implementa una aplicación gráfica para trabajar con matrices y métodos de decisión. La interfaz gráfica está desarrollada en Python utilizando la biblioteca `tkinter`.

## Estructura del Proyecto

El proyecto está organizado en los siguientes directorios:

- `Main/`: Contiene el archivo principal para ejecutar la aplicación.
- `Controller/`: Contiene la lógica de control de la aplicación, que conecta la interfaz gráfica con los cálculos y datos.
- `View/`: Contiene la interfaz gráfica de usuario (GUI), diseñada para la interacción con el usuario.
- `Model/`: Contiene la lógica relacionada con los datos y los cálculos de los métodos de decisión.

## Requisitos

- Python 3.8 o superior
- Bibliotecas estándar de Python (`tkinter`, `math`)

## Instalación

1. Clona este repositorio:
    ```
    git clone https://github.com/cadenas/Operaciones
    cd Operaciones
    ```

2. Asegúrate de tener Python instalado. Puedes verificarlo ejecutando:
    ```
    python --version
    ```
    No se requieren dependencias adicionales, ya que tkinter viene incluido con Python.

## Ejecución

Para iniciar la aplicación, ejecuta el archivo principal desde el directorio Main:

    cd Main
    python main.py


## Uso

1. **Formulario de entrada**: Ingresa el número de filas y columnas de la matriz, selecciona el modo de llenado (manual o automático) y proporciona el valor de α (entre 0 y 1).
2. **Generar matriz**: Haz clic en el botón "Generar Matriz" para crear la matriz.
3. **Resultados**: Los resultados de los métodos de decisión se mostrarán en la sección de resultados.

## Funcionalidades

- **Interfaz gráfica intuitiva**: Permite ingresar datos y visualizar resultados de manera clara.
- **Llenado de matriz**: Soporta llenado manual o automático de matrices.
- **Visualización de resultados**: Los resultados de los métodos de decisión se presentan de forma estructurada y alineada.
- **Métodos de decisión implementados**:
    - Pesimista
    - Optimista
    - Savage
    - Laplace
    - Hurwicz (con un valor ajustable de α)

## Métodos de Decisión

Cada método de decisión implementado en el proyecto tiene su propia lógica en el modelo. Los resultados se calculan y se muestran en la interfaz gráfica, destacando los valores óptimos.

## Estructura de Archivos

    metodos-decision/
    ├── Main/
    │ ├── main.py
    │ └── main_controller.py
    ├── Controller/
    ├── View/
    │ ├── gui_view.py
    │ └── second_window.py
    ├── Model/
    │ └── decision_methods.py
    └── README.md


## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad (`git checkout -b nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -m "Añadir nueva funcionalidad"`).
4. Sube tus cambios a tu rama (`git push origin nueva-funcionalidad`).
5. Abre un Pull Request.