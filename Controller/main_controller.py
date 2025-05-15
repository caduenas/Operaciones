# Archivo: Controller/main_controller.py
import random
from Model.model import DecisionModel
from View.gui_view import GUIView

class MainController:
    def __init__(self):
        self.model = DecisionModel()
        self.view = GUIView(self.process_input, self.process_results)

    def process_input(self, n, m, mode, alpha):
        try:
            if mode == "manual":
                matrix = self.view.get_matrix_input(n, m)
            else:
                matrix = [[round(random.uniform(0, 100), 2) for _ in range(m)] for _ in range(n)]

            self.model.set_matrix(matrix)
            self.view.show_matrix(matrix)

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

    def process_results(self, n, m, mode, alpha):
        try:
            if mode == "manual":
                matrix = self.view.get_matrix_input(n, m)
            else:
                matrix = [[round(random.uniform(0, 100), 2) for _ in range(m)] for _ in range(n)]

            self.model.set_matrix(matrix)

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

    def run(self):
        self.view.root.mainloop()