# Importación de las clases necesarias
from View.first_window import FirstWindow
from View.second_window import SecondWindow
from Model.model import DecisionModel

class MainController:
    def __init__(self):
        self.model = DecisionModel()  # Modelo para los cálculos
        self.first_window = FirstWindow(self.start_application)  # Ventana inicial
        self.second_window = None  # Ventana secundaria

    def start_application(self, n, m, alpha):
        # Inicia la aplicación con los valores ingresados
        self.first_window.destroy()  # Cierra la ventana inicial
        self.model.set_matrix(self.model.generate_matrix(n, m))  # Genera y establece la matriz
        self.second_window = SecondWindow(
            parent=None,
            model=self.model,
            n=n,
            m=m,
            alpha=alpha,
            show_matrix_flag=True,
            on_generate_zero_matrix=self._generate_zero_matrix
        )

    def _generate_zero_matrix(self):
        # Genera una matriz de ceros y la establece en el modelo
        n, m = self.model.matrix.shape
        self.model.set_matrix(np.zeros((n, m)))
        self.second_window.update_matrix_and_results(0, 0, self.second_window.alpha)

    def run(self):
        # Ejecuta la ventana inicial
        self.first_window.mainloop()