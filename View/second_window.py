import tkinter as tk
from tkinter import ttk, messagebox
import math

class SecondWindow(tk.Toplevel):
    def __init__(self, parent, n, m, alpha, matrix, model, show_matrix, on_update_results, on_update_matrix, on_generate_zero_matrix, mode):
        super().__init__(parent)
        self.n = n
        self.m = m
        self.alpha = alpha
        self.matrix = matrix
        self.model = model
        self.show_matrix_flag = show_matrix
        self.on_update_results = on_update_results
        self.on_update_matrix = on_update_matrix
        self.on_generate_zero_matrix = on_generate_zero_matrix
        self.mode = mode
        self.title("Resultados y matriz")
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.geometry("1200x700")
        self.attributes('-fullscreen', True)
        self._build_gui()
        self.grab_set()

    def _build_gui(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        if self.show_matrix_flag:
            ttk.Label(frm, text="Fila inicial a mostrar:").grid(row=0, column=0, sticky="w")
            self.start_row_entry = ttk.Entry(frm, width=10)
            self.start_row_entry.grid(row=0, column=1)
            self.start_row_entry.insert(0, "1")

            ttk.Label(frm, text="Columna inicial a mostrar:").grid(row=0, column=2, sticky="w")
            self.start_col_entry = ttk.Entry(frm, width=10)
            self.start_col_entry.grid(row=0, column=3)
            self.start_col_entry.insert(0, "1")

        ttk.Label(frm, text="Valor de α (0 <= α <= 1):").grid(row=0, column=4, sticky="w")
        self.alpha_entry = ttk.Entry(frm, width=10)
        self.alpha_entry.grid(row=0, column=5)
        self.alpha_entry.insert(0, str(self.alpha))

        ttk.Button(frm, text="Actualizar resultados", command=self._update_results).grid(row=0, column=6, padx=5)

        if self.show_matrix_flag:
            ttk.Button(frm, text="Redibujar matriz", command=self._update_matrix).grid(row=0, column=7, padx=5)
        ttk.Button(frm, text="Generar matriz desde cero", command=self._generate_zero_matrix).grid(row=0, column=8, padx=5)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(main_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky="ns")
        hbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        hbar.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.matrix_frame = ttk.Frame(self.scrollable_frame)
        self.matrix_frame.pack(side=tk.TOP, anchor="w", padx=10, pady=(0,0))
        self.results_frame = ttk.Frame(self.scrollable_frame)
        self.results_frame.pack(side=tk.TOP, anchor="w", padx=10, pady=(0,0))

        self._show_matrix_and_results()

    def _show_matrix_and_results(self):
        if not self.show_matrix_flag:
            self._show_results(float(self.alpha_entry.get() or self.alpha))
            return

        try:
            start_row = int(self.start_row_entry.get() or 1)
            start_col = int(self.start_col_entry.get() or 1)
            alpha = float(self.alpha_entry.get() or self.alpha)
        except:
            messagebox.showerror("Error", "Campos de fila, columna o α inválidos.")
            return

        if not (1 <= start_row <= self.n) or not (1 <= start_col <= self.m):
            messagebox.showerror("Error", "Fila o columna de inicio fuera de rango")
            return

        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self._show_matrix(start_row-1, start_col-1)
        self._show_results(alpha)

    def _show_matrix(self, start_row, start_col, max_size=30):
        n, m = self.n, self.m
        end_row = min(start_row + max_size, n)
        end_col = min(start_col + max_size, m)

        for j in range(start_col, end_col):
            tk.Label(self.matrix_frame, text=f"C{j+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=0, column=j - start_col + 1)

        for i in range(start_row, end_row):
            tk.Label(self.matrix_frame, text=f"F{i+1}", bg="#d9ead3", borderwidth=1, relief="solid", width=10).grid(row=i - start_row + 1, column=0)
            for j in range(start_col, end_col):
                tk.Label(self.matrix_frame, text=str(self.matrix[i][j]), borderwidth=1, relief="solid", width=10).grid(row=i - start_row + 1, column=j - start_col + 1)

        if n > max_size or m > max_size:
            aviso = ttk.Label(self.matrix_frame, text=f"Mostrando desde Fila {start_row+1}, Columna {start_col+1} hasta Fila {end_row}, Columna {end_col}", foreground="red")
            aviso.grid(row=(end_row - start_row + 2), column=0, columnspan=(end_col - start_col + 2), pady=10)

    def _show_results(self, alpha):
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
            highlight_value = min(res) if method_name == "Savage" else max(res)
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

            for value in res:
                color = "dark green" if value == highlight_value else "black"
                results_text.insert(tk.END, f"{value}\n", (color,))

            results_text.tag_configure("dark green", foreground="dark green")
            results_text.tag_configure("black", foreground="black")
            results_text.config(state=tk.DISABLED)

    def _update_results(self):
        alpha = float(self.alpha_entry.get() or self.alpha)
        if math.isclose(alpha, self.alpha):
            messagebox.showinfo("Sin cambios", "El valor de α no ha cambiado.")
            return
        self.alpha = alpha
        self._show_matrix_and_results()

    def _update_matrix(self):
        if not self.show_matrix_flag:
            return
        try:
            start_row = int(self.start_row_entry.get() or 1)
            start_col = int(self.start_col_entry.get() or 1)
            self._show_matrix_and_results()
        except:
            messagebox.showerror("Error", "Campos de fila o columna inválidos.")

    def _generate_zero_matrix(self):
        self.on_generate_zero_matrix()

    def update_results(self, start_row, start_col, alpha):
        self.alpha = alpha
        self._show_matrix_and_results()

    def update_matrix_and_results(self, start_row, start_col, alpha):
        self.alpha = alpha
        self._show_matrix_and_results()

    def close(self):
        self.destroy()
