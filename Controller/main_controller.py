import math
from tkinter import simpledialog, messagebox
from View.first_window import FirstWindow
from View.second_window import SecondWindow
from Model.model import DecisionModel

class MainController:
    def __init__(self):
        self.model = DecisionModel()
        self.matrix = None
        self.n = None
        self.m = None
        self.alpha = None
        self.first_window = None
        self.second_window = None
        self.show_first_window()

    def show_first_window(self):
        self.first_window = FirstWindow(
            on_matrix_and_results=self.on_matrix_and_results,
            on_only_results=self.on_only_results
        )

    def on_matrix_and_results(self, n, m, alpha, mode):
        self.n, self.m, self.alpha = n, m, alpha
        self.matrix = None
        self.first_window.close()
        if mode == "manual":
            self.matrix = self.get_manual_matrix(n, m)
        else:
            self.matrix = self.model.generate_matrix(n, m)
        self.model.set_matrix(self.matrix)
        self.show_second_window(show_matrix=True, mode=mode)

    def on_only_results(self, n, m, alpha, mode):
        self.n, self.m, self.alpha = n, m, alpha
        self.matrix = None
        self.first_window.close()
        if mode == "manual":
            self.matrix = self.get_manual_matrix(n, m)
        else:
            self.matrix = self.model.generate_matrix(n, m)
        self.model.set_matrix(self.matrix)
        self.show_second_window(show_matrix=False, mode=mode)

    def show_second_window(self, show_matrix, mode):
        self.second_window = SecondWindow(
            parent=self.first_window.root,
            n=self.n,
            m=self.m,
            alpha=self.alpha,
            matrix=self.matrix,
            model=self.model,
            show_matrix=show_matrix,
            on_update_results=self.on_update_results,
            on_update_matrix=self.on_update_matrix,
            on_generate_zero_matrix=self.on_generate_zero_matrix,
            mode=mode
        )

    def on_update_results(self, start_row, start_col, alpha):
        if not math.isclose(alpha, self.alpha):
            self.alpha = alpha
            self.second_window.update_results(start_row, start_col, alpha)
        else:
            messagebox.showinfo("Sin cambios", "El valor de α no ha cambiado.")

    def on_update_matrix(self, start_row, start_col, alpha):
        self.second_window.update_matrix_and_results(start_row, start_col, alpha)

    def on_generate_zero_matrix(self):
        self.second_window.close()
        self.first_window.show()  # Vuelve a mostrar la ventana principal

    def get_manual_matrix(self, n, m):
        matrix = []
        for i in range(n):
            row = []
            for j in range(m):
                value = simpledialog.askfloat(
                    "Entrada de Matriz",
                    f"Ingrese el valor para la posición ({i + 1}, {j + 1}):"
                )
                if value is None:
                    raise ValueError("Se canceló la entrada de la matriz.")
                row.append(value)
            matrix.append(row)
        return matrix

    def run(self):
        self.first_window.run()
