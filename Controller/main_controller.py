import random
from Model.model import DecisionModel
from View.gui_view import GUIView

class MainController:
    def __init__(self):
        self.model = DecisionModel()
        self.matrix = None
        self.n = None
        self.m = None
        self.alpha = None
        self.view = GUIView(
            self.process_input,
            self.process_results,
            self.show_viewport,
            self.create_zero_matrix
        )

    def process_input(self, n, m, mode, alpha, start_row=0, start_col=0):
        try:
            if mode == "manual":
                matrix = self.view.get_matrix_input(n, m)
            else:
                matrix = [[round(random.uniform(0, 100), 2) for _ in range(m)] for _ in range(n)]
            self.model.set_matrix(matrix)
            self.matrix = matrix
            self.n = n
            self.m = m
            self.alpha = alpha
            self.view.show_matrix(matrix, start_row, start_col)
            results = [
                ("Pesimista", self.model.pessimistic()),
                ("Optimista", self.model.optimistic()),
                ("Savage", self.model.savage()),
                ("Laplace", self.model.laplace()),
                ("Hurwicz", self.model.hurwicz(alpha)),
            ]
            self.view.show_results(results)
        except ValueError as e:
            self.view.show_error(str(e))

    def process_results(self, n, m, mode, alpha, start_row=0, start_col=0):
        try:
            if self.matrix:
                matrix = self.matrix
            else:
                if mode == "manual":
                    matrix = self.view.get_matrix_input(n, m)
                else:
                    matrix = [[round(random.uniform(0, 100), 2) for _ in range(m)] for _ in range(n)]
                self.model.set_matrix(matrix)
                self.matrix = matrix
                self.n = n
                self.m = m
            self.alpha = alpha
            self.view.show_matrix(matrix, start_row, start_col)
            results = [
                ("Pesimista", self.model.pessimistic()),
                ("Optimista", self.model.optimistic()),
                ("Savage", self.model.savage()),
                ("Laplace", self.model.laplace()),
                ("Hurwicz", self.model.hurwicz(alpha)),
            ]
            self.view.show_results(results)
        except ValueError as e:
            self.view.show_error(str(e))

    def show_viewport(self, start_row, start_col):
        if self.matrix:
            self.view.show_matrix(self.matrix, start_row, start_col)
        else:
            self.view.show_error("Primero debe generar una matriz.")

    def create_zero_matrix(self, n, m):
        matrix = [[0 for _ in range(m)] for _ in range(n)]
        self.model.set_matrix(matrix)
        self.matrix = matrix
        self.n = n
        self.m = m
        self.alpha = 0.5  # Valor por defecto para alpha
        self.view.show_matrix(matrix, 0, 0)
        self.view.show_results([
            ("Pesimista", self.model.pessimistic()),
            ("Optimista", self.model.optimistic()),
            ("Savage", self.model.savage()),
            ("Laplace", self.model.laplace()),
            ("Hurwicz", self.model.hurwicz(self.alpha)),
        ])

    def run(self):
        self.view.root.mainloop()
