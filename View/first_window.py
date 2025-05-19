# Importación de las bibliotecas necesarias
import tkinter as tk
from tkinter import ttk

class FirstWindow(tk.Tk):
    def __init__(self, on_start):
        super().__init__()
        self.on_start = on_start  # Callback para iniciar la aplicación

        # Configuración de la ventana principal
        self.title("Primera Ventana")
        self.geometry("400x300")

        # Etiqueta para el título
        title_label = ttk.Label(self, text="Configuración Inicial", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Entrada para el número de filas
        self.rows_entry = ttk.Entry(self)
        self.rows_entry.pack(pady=5)
        self.rows_entry.insert(0, "Número de filas")

        # Entrada para el número de columnas
        self.cols_entry = ttk.Entry(self)
        self.cols_entry.pack(pady=5)
        self.cols_entry.insert(0, "Número de columnas")

        # Entrada para el valor de α
        self.alpha_entry = ttk.Entry(self)
        self.alpha_entry.pack(pady=5)
        self.alpha_entry.insert(0, "Valor de α (0-1)")

        # Botón para iniciar
        start_button = ttk.Button(self, text="Iniciar", command=self._start)
        start_button.pack(pady=20)

    def _start(self):
        # Obtiene los valores ingresados y llama al callback
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            alpha = float(self.alpha_entry.get())
            if not (0 <= alpha <= 1):
                raise ValueError("El valor de α debe estar entre 0 y 1.")
            self.on_start(rows, cols, alpha)
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Entrada inválida: {e}")