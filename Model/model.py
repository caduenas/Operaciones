# Archivo: Model/model.py
import random

class DecisionModel:
    def __init__(self):
        # Inicializa la matriz vacía
        self.matrix = []

    def generate_matrix(self, n, m):
        # Genera una matriz aleatoria de tamaño n x m
        self.matrix = [[random.randint(0, 100) for _ in range(m)] for _ in range(n)]

    def set_matrix(self, matrix):
        # Establece la matriz ingresada por el usuario
        self.matrix = matrix

    def laplace(self):
        # Calcula el método de Laplace
        return [sum(row) / len(row) for row in self.matrix]

    def hurwicz(self, alpha):
        # Calcula el método de Hurwicz
        return [alpha * max(row) + (1 - alpha) * min(row) for row in self.matrix]

    def optimistic(self):
        # Calcula el método Optimista (Maximax)
        return [max(row) for row in self.matrix]

    def pessimistic(self):
        # Calcula el método Pesimista (Maximin)
        return [min(row) for row in self.matrix]

    def savage(self):
        # Calcula el método de Savage (Arrepentimiento)
        max_in_columns = [max(col) for col in zip(*self.matrix)]
        regret_matrix = [[max_in_columns[j] - self.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))]
        return [max(row) for row in regret_matrix]