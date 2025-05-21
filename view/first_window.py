import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import psutil

class FirstWindow:
    def __init__(self, on_matrix_and_results, on_only_results):
        # Inicializa la ventana principal de Tkinter
        self.root = tk.Tk()
        self.root.title("Ingreso de datos")
        window_width = 400
        window_height = 250

        # Centrar la ventana en pantalla
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Guarda las funciones callback para los botones
        self.on_matrix_and_results = on_matrix_and_results
        self.on_only_results = on_only_results

        # Crea el frame principal con padding
        frm = ttk.Frame(self.root, padding=20)
        frm.pack(expand=True)

        # Campo para el número de filas (n)
        ttk.Label(frm, text="Filas (n):").grid(row=0, column=0, sticky="w")
        self.n_entry = ttk.Entry(frm, width=10)
        self.n_entry.grid(row=0, column=1, pady=5)

        # Campo para el número de columnas (m)
        ttk.Label(frm, text="Columnas (m):").grid(row=1, column=0, sticky="w")
        self.m_entry = ttk.Entry(frm, width=10)
        self.m_entry.grid(row=1, column=1, pady=5)

        # Selección del modo de llenado (manual o automático)
        ttk.Label(frm, text="Modo de llenado:").grid(row=2, column=0, sticky="w")
        self.fill_mode = tk.StringVar(value="manual")
        ttk.Radiobutton(frm, text="Manual", variable=self.fill_mode, value="manual").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(frm, text="Automático", variable=self.fill_mode, value="auto").grid(row=2, column=2, sticky="w")

        # Campo para el valor de alfa (α)
        ttk.Label(frm, text="Valor de α (0 <= α <= 1):").grid(row=3, column=0, sticky="w")
        self.alpha_entry = ttk.Entry(frm, width=10)
        self.alpha_entry.grid(row=3, column=1, pady=5)

        # Botón para mostrar matriz y resultados
        btn1 = ttk.Button(frm, text="Matriz y resultados", command=self._matrix_and_results)
        btn1.grid(row=4, column=0, pady=20)
        # Botón para mostrar solo resultados
        btn2 = ttk.Button(frm, text="Solo resultados", command=self._only_results)
        btn2.grid(row=4, column=1, pady=20)

    def _check_memory(self, n, m, dtype=np.int32):
        # Calcula la memoria necesaria para una matriz de tamaño n x m y el tipo de dato especificado
        bytes_per_element = np.dtype(dtype).itemsize
        total_elements = n * m
        total_bytes = total_elements * bytes_per_element
        total_gib = total_bytes / (1024 ** 3)  # Convierte a GiB
        ram_gib = psutil.virtual_memory().available / (1024 ** 3)  # RAM disponible en GiB
        return total_gib, ram_gib

    def _matrix_and_results(self):
        # Maneja el evento del botón "Matriz y resultados"
        try:
            n_str = self.n_entry.get()
            m_str = self.m_entry.get()
            alpha_str = self.alpha_entry.get()
            # Verifica que todos los campos estén completos
            if not n_str or not m_str or not alpha_str:
                raise ValueError("Todos los campos son obligatorios.")
            n = int(n_str)
            m = int(m_str)
            alpha = float(alpha_str)
            # Verifica que alfa esté en el rango permitido
            if not (0 <= alpha <= 1):
                raise ValueError("El valor de α debe estar entre 0 y 1.")

            # Verifica que haya suficiente memoria RAM para la matriz
            total_gib, ram_gib = self._check_memory(n, m)
            if total_gib > ram_gib * 0.8:  # Solo permite si hay al menos 20% de RAM libre
                messagebox.showerror(
                    "Error de memoria",
                    f"No es posible crear una matriz de {n:,} x {m:,}: requiere aproximadamente {total_gib:.2f} GB de memoria RAM, "
                    f"pero solo hay {ram_gib:.2f} GB disponibles.\n"
                    "Reduce el tamaño de la matriz para poder realizar la operación."
                )
                return

            # Llama a la función callback con los datos ingresados
            self.on_matrix_and_results(n, m, alpha, self.fill_mode.get())
        except Exception as e:
            # Muestra un mensaje de error si los datos no son válidos
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def _only_results(self):
        # Maneja el evento del botón "Solo resultados"
        try:
            n_str = self.n_entry.get()
            m_str = self.m_entry.get()
            alpha_str = self.alpha_entry.get()
            # Verifica que todos los campos estén completos
            if not n_str or not m_str or not alpha_str:
                raise ValueError("Todos los campos son obligatorios.")
            n = int(n_str)
            m = int(m_str)
            alpha = float(alpha_str)
            # Verifica que alfa esté en el rango permitido
            if not (0 <= alpha <= 1):
                raise ValueError("El valor de α debe estar entre 0 y 1.")

            # Verifica que haya suficiente memoria RAM para la matriz
            total_gib, ram_gib = self._check_memory(n, m)
            if total_gib > ram_gib * 0.8:
                messagebox.showerror(
                    "Error de memoria",
                    f"No es posible crear una matriz de {n:,} x {m:,}: requiere aproximadamente {total_gib:.2f} GB de memoria RAM, "
                    f"pero solo hay {ram_gib:.2f} GB disponibles.\n"
                    "Reduce el tamaño de la matriz para poder realizar la operación."
                )
                return

            # Llama a la función callback con los datos ingresados
            self.on_only_results(n, m, alpha, self.fill_mode.get())
        except Exception as e:
            # Muestra un mensaje de error si los datos no son válidos
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def close(self):
        # Oculta la ventana principal sin destruirla
        self.root.withdraw()

    def show(self):
        # Muestra nuevamente la ventana principal si estaba oculta
        self.root.deiconify()

    def run(self):
        # Inicia el bucle principal de la aplicación Tkinter
        self.root.mainloop()
