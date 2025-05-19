import numpy as np

class DecisionModel:
    def __init__(self):
        self.matrix = None

    def generate_matrix(self, n, m):
        return np.random.randint(0, 101, size=(n, m))

    def set_matrix(self, matrix):
        self.matrix = matrix

    def laplace(self):
        return np.mean(self.matrix, axis=1)

    def hurwicz(self, alpha):
        return alpha * np.max(self.matrix, axis=1) + (1 - alpha) * np.min(self.matrix, axis=1)

    def optimistic(self):
        return np.max(self.matrix, axis=1)

    def pessimistic(self):
        return np.min(self.matrix, axis=1)

    def savage(self):
        max_in_columns = np.max(self.matrix, axis=0)
        regret_matrix = max_in_columns - self.matrix
        return np.max(regret_matrix, axis=1)
