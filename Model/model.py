import numpy as np  # Importa la biblioteca numpy para operaciones matriciales

class DecisionModel:
    def __init__(self):
        # Inicializa el modelo de decisión con una matriz vacía
        self.matrix = None

    def generate_matrix(self, n, m):
        # Genera una matriz aleatoria de tamaño n x m con valores entre 0 y 100
        return np.random.randint(0, 101, size=(n, m))

    def set_matrix(self, matrix):
        # Establece la matriz actual para el modelo
        self.matrix = matrix

    def laplace(self):
        # Calcula el promedio de cada fila de la matriz (criterio de Laplace)
        return np.mean(self.matrix, axis=1)

    def hurwicz(self, alpha):
        # Calcula el criterio de Hurwicz combinando el valor máximo y mínimo de cada fila
        # α es el coeficiente de optimismo (0 <= α <= 1)
        return alpha * np.max(self.matrix, axis=1) + (1 - alpha) * np.min(self.matrix, axis=1)

    def optimistic(self):
        # Calcula el criterio optimista seleccionando el valor máximo de cada fila
        return np.max(self.matrix, axis=1)

    def pessimistic(self):
        # Calcula el criterio pesimista seleccionando el valor mínimo de cada fila
        return np.min(self.matrix, axis=1)

    def savage(self):
        # Calcula el criterio de Savage basado en la matriz de arrepentimientos
        # Obtiene el valor máximo de cada columna
        max_in_columns = np.max(self.matrix, axis=0)
        # Calcula la matriz de arrepentimientos restando los valores de la matriz original
        regret_matrix = max_in_columns - self.matrix
        # Selecciona el valor máximo de cada fila de la matriz de arrepentimientos
        return np.max(regret_matrix, axis=1)
