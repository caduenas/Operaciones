import random

class DecisionModel:
    def __init__(self):
        self.matrix = []

    def generate_matrix(self, n, m):
        self.matrix = [[random.randint(0, 100) for _ in range(m)] for _ in range(n)]

    def set_matrix(self, matrix):
        self.matrix = matrix

    def laplace(self):
        return [sum(row)/len(row) for row in self.matrix]

    def hurwicz(self, alpha):
        return [alpha * max(row) + (1 - alpha) * min(row) for row in self.matrix]

    def optimistic(self):
        return [max(row) for row in self.matrix]

    def pessimistic(self):
        return [min(row) for row in self.matrix]

    def savage(self):
        max_in_columns = [max(col) for col in zip(*self.matrix)]
        regret_matrix = [[max_in_columns[j] - self.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))]
        return [max(row) for row in regret_matrix]
