import numpy as np

class DecisionModel:
    def __init__(self):
        # Inicializa la matriz vacía
        self.matrix = np.array([])

    def generate_matrix(self, n, m):
        # Genera una matriz aleatoria de tamaño n x m
        self.matrix = np.random.randint(0, 101, size=(n, m))

    def set_matrix(self, matrix):
        # Establece la matriz ingresada por el usuario
        self.matrix = np.array(matrix)

    def laplace(self):
        # Calcula el método de Laplace en lote
        return np.mean(self.matrix.toarray(), axis=1)

    def hurwicz(self, alpha):
        # Calcula el método de Hurwicz
        return alpha * np.max(self.matrix, axis=1) + (1 - alpha) * np.min(self.matrix, axis=1)

    def optimistic(self):
        # Calcula el método Optimista (Maximax)
        return np.max(self.matrix, axis=1)

    def pessimistic(self):
        # Calcula el método Pesimista (Maximin)
        return np.min(self.matrix, axis=1)

    def savage(self):
        # Calcula el método de Savage (Arrepentimiento)
        max_in_columns = np.max(self.matrix, axis=0)
        regret_matrix = max_in_columns - self.matrix
        return np.max(regret_matrix, axis=1)