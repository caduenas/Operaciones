# Importación de la biblioteca numpy para cálculos matriciales
import numpy as np

class DecisionModel:
    def __init__(self):
        self.matrix = None  # Matriz utilizada en los cálculos

    def generate_matrix(self, n, m):
        # Genera una matriz aleatoria de tamaño n x m con valores entre 0 y 100
        return np.random.randint(0, 101, size=(n, m))

    def set_matrix(self, matrix):
        # Establece la matriz actual
        self.matrix = matrix

    def laplace(self):
        # Calcula el promedio de cada fila (criterio de Laplace)
        return np.mean(self.matrix, axis=1)

    def hurwicz(self, alpha):
        # Calcula el criterio de Hurwicz con el valor de α
        return alpha * np.max(self.matrix, axis=1) + (1 - alpha) * np.min(self.matrix, axis=1)

    def optimistic(self):
        # Calcula el criterio optimista (máximo de cada fila)
        return np.max(self.matrix, axis=1)

    def pessimistic(self):
        # Calcula el criterio pesimista (mínimo de cada fila)
        return np.min(self.matrix, axis=1)

    def savage(self):
        # Calcula el criterio de Savage (máximo de la matriz de arrepentimientos)
        max_in_columns = np.max(self.matrix, axis=0)
        regret_matrix = max_in_columns - self.matrix
        return np.max(regret_matrix, axis=1)