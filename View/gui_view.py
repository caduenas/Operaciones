# Archivo: View/gui_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class GUIView:
    def __init__(self, process_input_callback):
        self.root = tk.Tk()
        self.root.title("Métodos de Decisión")
        self.root.geometry("1280x720")
        self.root.attributes("-fullscreen", True)  # Abrir en pantalla completa
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))  # Salir de pantalla completa
        self.process_input_callback = process_input_callback

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

        self.generate_button = ttk.Button(self.form_frame, text="Generar Matriz", command=self.on_generate_matrix)
        self.generate_button.grid(row=4, column=0, columnspan=3, pady=10)

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

    def on_generate_matrix(self):
        try:
            n = int(self.rows_entry.get())
            m = int(self.cols_entry.get())
            mode = self.fill_mode.get()
            alpha = float(self.alpha_entry.get())

            # Validar que α esté entre 0 y 1
            if not (0 <= alpha <= 1):
                raise ValueError("El valor de α debe estar entre 0 y 1.")

            self.process_input_callback(n, m, mode, alpha)
        except ValueError as e:
            self.show_error(str(e))

    def get_matrix_input(self, n, m):
        # Solicita al usuario ingresar los valores de la matriz manualmente
        matrix = []
        for i in range(n):
            row = []
            for j in range(m):
                value = simpledialog.askfloat(
                    "Entrada de Matriz",
                    f"Ingrese el valor para la posición ({i + 1}, {j + 1}):",
                    parent=self.root  # Asegura que el diálogo esté asociado a la ventana principal
                )
                if value is None:
                    raise ValueError("Se canceló la entrada de la matriz.")
                row.append(value)
            matrix.append(row)
        return matrix

    def show_matrix(self, matrix):
        if self.matrix_table:
            self.matrix_table.destroy()

        self.matrix_table = ttk.Frame(self.matrix_frame)
        self.matrix_table.pack(pady=10)

        for j in range(len(matrix[0])):
            tk.Label(self.matrix_table, text=f"C{j+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=0, column=j+1)

        for i, row in enumerate(matrix):
            tk.Label(self.matrix_table, text=f"F{i+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=i+1, column=0)
            for j, value in enumerate(row):
                tk.Label(self.matrix_table, text=str(value), borderwidth=1, relief="solid", width=10).grid(row=i+1, column=j+1)

    def show_results(self, methods_results):
        # Limpiar resultados anteriores
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Crear un contenedor en forma de grilla
        columns = 3
        row_idx = 0
        col_idx = 0

        for method_name, results in methods_results:
            container = ttk.Frame(self.results_frame, padding=10, borderwidth=2, relief="ridge")
            container.grid(row=row_idx, column=col_idx, padx=10, pady=10, sticky="nsew")

            # Etiqueta del método
            method_label = ttk.Label(container, text=f"Método: {method_name}", font=("Arial", 10, "bold"))
            method_label.pack(anchor="w", pady=5)

            # Caja de texto desplazable para los resultados
            text_frame = ttk.Frame(container)
            text_frame.pack(fill=tk.BOTH, expand=True)

            text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
            text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            results_text = tk.Text(text_frame, wrap=tk.WORD, height=5, yscrollcommand=text_scrollbar.set, width=50)
            results_text.pack(fill=tk.BOTH, expand=True)
            text_scrollbar.config(command=results_text.yview)

            # Insertar resultados en la caja de texto
            results_text.insert(tk.END, ", ".join(map(str, results)))
            results_text.config(state=tk.DISABLED)

            # Actualizar índices de fila y columna
            col_idx += 1
            if col_idx >= columns:
                col_idx = 0
                row_idx += 1

    def show_error(self, message):
        messagebox.showerror("Error", message)