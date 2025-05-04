class ConsoleView:
    def get_matrix_input(self, n, m):
        matrix = []
        print(f"Ingrese los {n}x{m} valores de la matriz:")
        for i in range(n):
            row = []
            for j in range(m):
                while True:
                    try:
                        val = float(input(f"Elemento [{i+1}][{j+1}]: "))
                        row.append(val)
                        break
                    except ValueError:
                        print("Entrada inválida. Intente de nuevo.")
            matrix.append(row)
        return matrix

    def show_matrix(self, matrix):
        print("\nMatriz ingresada:")
        for row in matrix:
            print(row)

    def show_results(self, name, results):
        print(f"\nResultado del método {name}:")
        for i, val in enumerate(results):
            print(f"Alternativa {i+1}: {val}")
