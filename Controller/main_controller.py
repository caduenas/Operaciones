from Model.model import DecisionModel
from View.console_view import ConsoleView

class MainController:
    def __init__(self):
        self.model = DecisionModel()
        self.view = ConsoleView()

    def run(self):
        n = int(input("Ingrese número de filas (n): "))
        m = int(input("Ingrese número de columnas (m): "))
        modo = input("¿Desea llenar la matriz manualmente (M) o automáticamente (A)? ").lower()

        if modo == "m":
            matrix = self.view.get_matrix_input(n, m)
        else:
            self.model.generate_matrix(n, m)
            matrix = self.model.matrix

        self.model.set_matrix(matrix)
        self.view.show_matrix(matrix)

        self.view.show_results("Laplace", self.model.laplace())

        alpha = float(input("Ingrese el valor de alfa (0 <= α <= 1) para Hurwicz: "))
        self.view.show_results("Hurwicz", self.model.hurwicz(alpha))

        self.view.show_results("Optimista (Maximax)", self.model.optimistic())
        self.view.show_results("Pesimista (Maximin)", self.model.pessimistic())
        self.view.show_results("Savage (Arrepentimiento)", self.model.savage())
