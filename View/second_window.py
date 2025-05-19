# Importación de las bibliotecas necesarias
import tkinter as tk
from tkinter import ttk, messagebox
import math

class SecondWindow(tk.Toplevel):
    def __init__(self, parent, model, n, m, alpha, show_matrix_flag, on_generate_zero_matrix):
        super().__init__(parent)
        self.model = model  # Modelo que contiene los métodos de decisión
        self.n = n  # Número de filas de la matriz
        self.m = m  # Número de columnas de la matriz
        self.alpha = alpha  # Valor inicial de α
        self.show_matrix_flag = show_matrix_flag  # Bandera para mostrar la matriz
        self.on_generate_zero_matrix = on_generate_zero_matrix  # Callback para generar una matriz de ceros

        # Configuración de la ventana principal
        self.title("Segunda Ventana")
        self.geometry("800x600")

        # Creación del marco principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Creación del lienzo para manejar el desplazamiento
        self.canvas = tk.Canvas(main_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Barras de desplazamiento vertical y horizontal
        vbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky="ns")
        hbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        hbar.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        # Marco desplazable dentro del lienzo
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Marcos para la matriz y los resultados
        self.matrix_frame = ttk.Frame(self.scrollable_frame)
        self.matrix_frame.pack(side=tk.TOP, anchor="w", padx=10, pady=(0, 0))
        self.results_frame = ttk.Frame(self.scrollable_frame)
        self.results_frame.pack(side=tk.TOP, anchor="w", padx=10, pady=(0, 0))

        # Mostrar la matriz y los resultados iniciales
        self._show_matrix_and_results()

    def _show_matrix_and_results(self):
        # Muestra la matriz y los resultados según la configuración actual
        if not self.show_matrix_flag:
            self._show_results(float(self.alpha_entry.get() or self.alpha))
            return

        try:
            # Obtiene los valores de fila, columna y α desde las entradas
            start_row = int(self.start_row_entry.get() or 1)
            start_col = int(self.start_col_entry.get() or 1)
            alpha = float(self.alpha_entry.get() or self.alpha)
        except:
            # Muestra un error si los valores son inválidos
            messagebox.showerror("Error", "Campos de fila, columna o α inválidos.")
            return

        # Verifica que las filas y columnas estén dentro del rango permitido
        if not (1 <= start_row <= self.n) or not (1 <= start_col <= self.m):
            messagebox.showerror("Error", "Fila o columna de inicio fuera de rango")
            return

        # Limpia el marco de la matriz y muestra la nueva matriz
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self._show_matrix(start_row - 1, start_col - 1)
        self._show_results(alpha)

    def _show_matrix(self, start_row, start_col, max_size=30):
        # Muestra una porción de la matriz en el marco
        n, m = self.n, self.m
        end_row = min(start_row + max_size, n)
        end_col = min(start_col + max_size, m)

        # Encabezados de las columnas
        for j in range(start_col, end_col):
            tk.Label(self.matrix_frame, text=f"C{j+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=0, column=j - start_col + 1)

        # Encabezados de las filas y valores de la matriz
        for i in range(start_row, end_row):
            tk.Label(self.matrix_frame, text=f"F{i+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=i - start_row + 1, column=0)
            for j in range(start_col, end_col):
                tk.Label(self.matrix_frame, text=str(self.matrix[i][j]), borderwidth=1, relief="solid", width=10).grid(row=i - start_row + 1, column=j - start_col + 1)

        # Muestra un aviso si la matriz es demasiado grande
        if n > max_size or m > max_size:
            aviso = ttk.Label(self.matrix_frame, text=f"Mostrando desde Fila {start_row+1}, Columna {start_col+1} hasta Fila {end_row}, Columna {end_col}", foreground="red")
            aviso.grid(row=(end_row - start_row + 2), column=0, columnspan=(end_col - start_col + 2), pady=10)

    def _show_results(self, alpha):
        # Muestra los resultados de los métodos de decisión
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        results = [
            ("Pesimista", self.model.pessimistic()),
            ("Optimista", self.model.optimistic()),
            ("Savage", self.model.savage()),
            ("Laplace", self.model.laplace()),
            ("Hurwicz", self.model.hurwicz(alpha)),
        ]
        for idx, (method_name, res) in enumerate(results):
            # Resalta el valor óptimo según el método
            highlight_value = min(res) if method_name == "Savage" else max(res)
            optimal_label = ttk.Label(
                self.results_frame,
                text=f"El resultado óptimo para este ejercicio resuelto por medio del método de decisión de {method_name} es: {highlight_value}",
                font=("Arial", 10, "bold"),
            )
            optimal_label.grid(row=idx * 2, column=0, padx=10, pady=5, sticky="w")

            # Contenedor para los resultados completos
            container = ttk.Frame(self.results_frame, padding=10, borderwidth=2, relief="ridge")
            container.grid(row=idx * 2 + 1, column=0, padx=10, pady=15, sticky="nsew")

            method_label = ttk.Label(container, text=f"Resultados completos para el método: {method_name}", font=("Arial", 10, "bold"))
            method_label.pack(anchor="w", pady=5)

            # Marco para el texto desplazable
            text_frame = ttk.Frame(container)
            text_frame.pack(fill=tk.BOTH, expand=True)

            text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
            text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            results_text = tk.Text(text_frame, wrap=tk.WORD, height=5, yscrollcommand=text_scrollbar.set, width=50)
            results_text.pack(fill=tk.BOTH, expand=True)
            text_scrollbar.config(command=results_text.yview)

            # Inserta los valores en el cuadro de texto
            for value in res:
                color = "dark green" if value == highlight_value else "black"
                results_text.insert(tk.END, f"{value}\n", (color,))

            # Configura los estilos de texto
            results_text.tag_configure("dark green", foreground="dark green")
            results_text.tag_configure("black", foreground="black")
            results_text.config(state=tk.DISABLED)

    def _update_results(self):
        # Actualiza los resultados si el valor de α cambia
        alpha = float(self.alpha_entry.get() or self.alpha)
        if math.isclose(alpha, self.alpha):
            messagebox.showinfo("Sin cambios", "El valor de α no ha cambiado.")
            return
        self.alpha = alpha
        self._show_matrix_and_results()

    def _update_matrix(self):
        # Actualiza la matriz si la bandera está activa
        if not self.show_matrix_flag:
            return
        try:
            start_row = int(self.start_row_entry.get() or 1)
            start_col = int(self.start_col_entry.get() or 1)
            self._show_matrix_and_results()
        except:
            messagebox.showerror("Error", "Campos de fila o columna inválidos.")

    def _generate_zero_matrix(self):
        # Genera una matriz de ceros
        self.on_generate_zero_matrix()

    def update_results(self, start_row, start_col, alpha):
        # Actualiza los resultados con nuevos valores
        self.alpha = alpha
        self._show_matrix_and_results()

    def update_matrix_and_results(self, start_row, start_col, alpha):
        # Actualiza la matriz y los resultados con nuevos valores
        self.alpha = alpha
        self._show_matrix_and_results()

    def close(self):
        # Cierra la ventana
        self.destroy()