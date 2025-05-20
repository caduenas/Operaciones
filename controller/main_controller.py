import math
from tkinter import simpledialog, messagebox
from view.first_window import FirstWindow
from view.second_window import SecondWindow
from model.model import DecisionModel

class MainController:
    def __init__(self):
        # Inicializa el modelo y variables principales
        self.model = DecisionModel()  # Modelo de decisiones
        self.matrix = None            # Matriz de datos
        self.n = None                 # Número de filas
        self.m = None                 # Número de columnas
        self.alpha = None             # Valor de α
        self.first_window = None      # Ventana principal (ingreso de datos)
        self.second_window = None     # Ventana secundaria (resultados/matriz)
        self.show_first_window()      # Muestra la ventana principal al iniciar

    def show_first_window(self):
        # Crea e inicializa la ventana principal (FirstWindow)
        self.first_window = FirstWindow(
            on_matrix_and_results=self.on_matrix_and_results,  # Callback para matriz y resultados
            on_only_results=self.on_only_results               # Callback para solo resultados
        )

    def on_matrix_and_results(self, n, m, alpha, mode):
        # Maneja la acción cuando el usuario quiere ver matriz y resultados
        self.n, self.m, self.alpha = n, m, alpha
        self.matrix = None
        self.first_window.close()  # Oculta la ventana principal
        if mode == "manual":
            # Si el modo es manual, solicita la matriz al usuario
            self.matrix = self.get_manual_matrix(n, m)
            if self.matrix is None:
                # El usuario canceló, no continuar
                return
        else:
            # Si el modo es automático, genera la matriz aleatoriamente
            self.matrix = self.model.generate_matrix(n, m)
        self.model.set_matrix(self.matrix)  # Establece la matriz en el modelo
        self.show_second_window(show_matrix=True, mode=mode)  # Muestra la ventana de resultados con la matriz

    def on_only_results(self, n, m, alpha, mode):
        # Maneja la acción cuando el usuario quiere ver solo los resultados
        self.n, self.m, self.alpha = n, m, alpha
        self.matrix = None
        self.first_window.close()  # Oculta la ventana principal
        if mode == "manual":
            # Si el modo es manual, solicita la matriz al usuario
            self.matrix = self.get_manual_matrix(n, m)
            if self.matrix is None:
                # El usuario canceló, no continuar
                return
        else:
            # Si el modo es automático, genera la matriz aleatoriamente
            self.matrix = self.model.generate_matrix(n, m)
        self.model.set_matrix(self.matrix)  # Establece la matriz en el modelo
        self.show_second_window(show_matrix=False, mode=mode)  # Muestra la ventana de resultados sin la matriz

    def show_second_window(self, show_matrix, mode):
        # Crea y muestra la ventana secundaria (SecondWindow) con los datos y callbacks necesarios
        self.second_window = SecondWindow(
            parent=self.first_window.root,
            n=self.n,
            m=self.m,
            alpha=self.alpha,
            matrix=self.matrix,
            model=self.model,
            show_matrix=show_matrix,
            on_update_results=self.on_update_results,           # Callback para actualizar resultados
            on_update_matrix=self.on_update_matrix,             # Callback para actualizar matriz
            on_generate_zero_matrix=self.on_generate_zero_matrix,  # Callback para volver a ventana principal
            mode=mode
        )

    def on_update_results(self, start_row, start_col, alpha):
        # Actualiza los resultados si el valor de α cambió
        if not math.isclose(alpha, self.alpha):
            self.alpha = alpha
            self.second_window.update_results(start_row, start_col, alpha)
        else:
            # Informa si no hubo cambios en α
            messagebox.showinfo("Sin cambios", "El valor de α no ha cambiado.")

    def on_update_matrix(self, start_row, start_col, alpha):
        # Actualiza la matriz y los resultados en la ventana secundaria
        self.second_window.update_matrix_and_results(start_row, start_col, alpha)

    def on_generate_zero_matrix(self):
        # Cierra la ventana secundaria y vuelve a mostrar la ventana principal para reiniciar el proceso
        self.second_window.close()
        self.first_window.show()  # Vuelve a mostrar la ventana principal

    def get_manual_matrix(self, n, m):
        # Solicita al usuario que ingrese manualmente los valores de la matriz
        matrix = []
        for i in range(n):
            row = []
            for j in range(m):
                while True:
                    try:
                        # Solicita un valor numérico al usuario
                        value = simpledialog.askfloat(
                            "Entrada de Matriz",
                            f"Ingrese un valor numérico mayor a 0 para la posición ({i + 1}, {j + 1}):"
                        )
                        if value is None:
                            # Si se presiona "Cancelar", regresa al formulario anterior
                            messagebox.showinfo("Cancelado", "Regresando al formulario anterior.")
                            self.first_window.show()  # Vuelve a mostrar la ventana principal
                            return None  # Detiene el proceso
                        if value <= 0:
                            # Verifica que el valor sea mayor a 0
                            raise ValueError("El valor debe ser mayor a 0.")
                        row.append(value)
                        break  # Sale del bucle si el valor es válido
                    except ValueError:
                        # Muestra un mensaje de error si el valor no es válido
                        messagebox.showerror("Error", f"Por favor ingrese un valor numérico mayor a 0.")
            matrix.append(row)
        return matrix

    def run(self):
        # Inicia el bucle principal de la interfaz gráfica
        self.first_window.run()
