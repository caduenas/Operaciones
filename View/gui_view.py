import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class GUIView:
    def __init__(
        self,
        process_input_callback,
        process_results_callback,
        show_viewport_callback,
        create_zero_matrix_callback
    ):
        self.root = tk.Tk()
        self.root.title("Métodos de Decisión")
        self.root.geometry("1280x720")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        self.process_input_callback = process_input_callback
        self.process_results_callback = process_results_callback
        self.show_viewport_callback = show_viewport_callback
        self.create_zero_matrix_callback = create_zero_matrix_callback

        # Formulario
        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Número de filas (n):").grid(row=0, column=0, sticky="w", pady=5)
        self.rows_entry = ttk.Entry(self.form_frame, width=10)
        self.rows_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.form_frame, text="Número de columnas (m):").grid(row=1, column=0, sticky="w", pady=5)
        self.cols_entry = ttk.Entry(self.form_frame, width=10)
        self.cols_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.form_frame, text="Modo de llenado:").grid(row=2, column=0, sticky="w", pady=5)
        self.fill_mode = tk.StringVar(value="manual")
        ttk.Radiobutton(self.form_frame, text="Manual", variable=self.fill_mode, value="manual").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(self.form_frame, text="Automático", variable=self.fill_mode, value="auto").grid(row=2, column=2, sticky="w")

        ttk.Label(self.form_frame, text="Valor de α (0 <= α <= 1):").grid(row=3, column=0, sticky="w", pady=5)
        self.alpha_entry = ttk.Entry(self.form_frame, width=10)
        self.alpha_entry.grid(row=3, column=1, pady=5)

        # Viewport controls
        ttk.Label(self.form_frame, text="Fila inicial a mostrar:").grid(row=4, column=0, sticky="w", pady=5)
        self.start_row_entry = ttk.Entry(self.form_frame, width=10)
        self.start_row_entry.grid(row=4, column=1, pady=5)
        self.start_row_entry.insert(0, "1")  # Valor predeterminado 1

        ttk.Label(self.form_frame, text="Columna inicial a mostrar:").grid(row=5, column=0, sticky="w", pady=5)
        self.start_col_entry = ttk.Entry(self.form_frame, width=10)
        self.start_col_entry.grid(row=5, column=1, pady=5)
        self.start_col_entry.insert(0, "1")  # Valor predeterminado 1

        # Botones de acción
        self.generate_button_matrix_results = ttk.Button(
            self.form_frame,
            text="Generar NUEVA matriz y resultados",
            command=self.on_generate_matrix_and_results
        )
        self.generate_button_matrix_results.grid(row=6, column=0, columnspan=2, pady=10)

        self.generate_button_results = ttk.Button(
            self.form_frame,
            text="Actualizar resultados para la matriz actual",
            command=self.on_generate_results
        )
        self.generate_button_results.grid(row=6, column=2, columnspan=2, pady=10)

        self.show_viewport_button = ttk.Button(
            self.form_frame,
            text="Mostrar otra parte de la matriz actual",
            command=self.on_show_viewport
        )
        self.show_viewport_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.create_zero_matrix_button = ttk.Button(
            self.form_frame,
            text="Crear MATRIZ DE CEROS (borra la actual)",
            command=self.on_create_zero_matrix
        )
        self.create_zero_matrix_button.grid(row=7, column=2, columnspan=2, pady=10)

        # Contenedor con scroll para la matriz y resultados
        self.canvas = tk.Canvas(self.root)
        self.scrollbar_y = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Contenedor para la matriz
        self.matrix_frame = ttk.Frame(self.scrollable_frame)
        self.matrix_frame.pack(side=tk.TOP, anchor="w", padx=10, pady=10)

        # Contenedor para los resultados
        self.results_frame = ttk.Frame(self.scrollable_frame)
        self.results_frame.pack(side=tk.TOP, anchor="w", padx=10, pady=10)

        self.matrix_table = None

    def on_generate_matrix_and_results(self):
        try:
            n = int(self.rows_entry.get())
            m = int(self.cols_entry.get())
            mode = self.fill_mode.get()
            alpha = float(self.alpha_entry.get())
            start_row = int(self.start_row_entry.get() or 1) - 1  # Ajuste a índice Python
            start_col = int(self.start_col_entry.get() or 1) - 1  # Ajuste a índice Python
            if not (0 <= alpha <= 1):
                raise ValueError("El valor de α debe estar entre 0 y 1.")
            self.process_input_callback(n, m, mode, alpha, start_row, start_col)
        except ValueError as e:
            self.show_error(str(e))

    def on_generate_results(self):
        try:
            n = int(self.rows_entry.get())
            m = int(self.cols_entry.get())
            mode = self.fill_mode.get()
            alpha = float(self.alpha_entry.get())
            start_row = int(self.start_row_entry.get() or 1) - 1
            start_col = int(self.start_col_entry.get() or 1) - 1
            if not (0 <= alpha <= 1):
                raise ValueError("El valor de α debe estar entre 0 y 1.")
            self.process_results_callback(n, m, mode, alpha, start_row, start_col)
        except ValueError as e:
            self.show_error(str(e))

    def on_show_viewport(self):
        try:
            start_row = int(self.start_row_entry.get() or 1) - 1
            start_col = int(self.start_col_entry.get() or 1) - 1
            self.show_viewport_callback(start_row, start_col)
        except ValueError as e:
            self.show_error(str(e))

    def on_create_zero_matrix(self):
        try:
            n = int(self.rows_entry.get())
            m = int(self.cols_entry.get())
            self.create_zero_matrix_callback(n, m)
        except ValueError as e:
            self.show_error(str(e))

    def get_matrix_input(self, n, m):
        matrix = []
        for i in range(n):
            row = []
            for j in range(m):
                value = simpledialog.askfloat(
                    "Entrada de Matriz",
                    f"Ingrese el valor para la posición ({i + 1}, {j + 1}):",
                    parent=self.root
                )
                if value is None:
                    raise ValueError("Se canceló la entrada de la matriz.")
                row.append(value)
            matrix.append(row)
        return matrix

    def show_matrix(self, matrix, start_row=0, start_col=0, max_size=90):
        if self.matrix_table:
            self.matrix_table.destroy()

        self.matrix_table = ttk.Frame(self.matrix_frame)
        self.matrix_table.pack(pady=10)

        n = len(matrix)
        m = len(matrix[0])
        end_row = min(start_row + max_size, n)
        end_col = min(start_col + max_size, m)

        # Encabezados de columna
        for j in range(start_col, end_col):
            tk.Label(self.matrix_table, text=f"C{j+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=0, column=j - start_col + 1)

        for i in range(start_row, end_row):
            tk.Label(self.matrix_table, text=f"F{i+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=i - start_row + 1, column=0)
            for j in range(start_col, end_col):
                tk.Label(self.matrix_table, text=str(matrix[i][j]), borderwidth=1, relief="solid", width=10).grid(row=i - start_row + 1, column=j - start_col + 1)

        # Aviso si solo se muestra una parte
        if n > max_size or m > max_size:
            aviso = ttk.Label(self.matrix_table, text=f"Mostrando desde Fila {start_row+1}, Columna {start_col+1} hasta Fila {end_row}, Columna {end_col}", foreground="red")
            aviso.grid(row=(end_row - start_row + 2), column=0, columnspan=(end_col - start_col + 2), pady=10)

    def show_results(self, methods_results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for idx, (method_name, results) in enumerate(methods_results):
            if method_name == "Savage":
                highlight_value = min(results)
            else:
                highlight_value = max(results)
            optimal_label = ttk.Label(
                self.results_frame,
                text=f"El resultado óptimo para este ejercicio resuelto por medio del método de decisión de {method_name} es: {highlight_value}",
                font=("Arial", 10, "bold"),
            )
            optimal_label.grid(row=idx * 2, column=0, padx=10, pady=5, sticky="w")

            container = ttk.Frame(self.results_frame, padding=10, borderwidth=2, relief="ridge")
            container.grid(row=idx * 2 + 1, column=0, padx=10, pady=15, sticky="nsew")
            method_label = ttk.Label(container, text=f"Resultados completos para el método: {method_name}", font=("Arial", 10, "bold"))
            method_label.pack(anchor="w", pady=5)
            text_frame = ttk.Frame(container)
            text_frame.pack(fill=tk.BOTH, expand=True)
            text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
            text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            results_text = tk.Text(text_frame, wrap=tk.WORD, height=5, yscrollcommand=text_scrollbar.set, width=50)
            results_text.pack(fill=tk.BOTH, expand=True)
            text_scrollbar.config(command=results_text.yview)
            for value in results:
                color = "dark green" if value == highlight_value else "black"
                results_text.insert(tk.END, f"{value}\n", (color,))
            results_text.tag_configure("dark green", foreground="dark green")
            results_text.tag_configure("black", foreground="black")
            results_text.config(state=tk.DISABLED)

    def show_error(self, message):
        messagebox.showerror("Error", message)
