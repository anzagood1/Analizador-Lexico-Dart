import tkinter as tk
from tkinter import scrolledtext


class WindowElements(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Entrada de texto
        self.input_text = scrolledtext.ScrolledText(self.parent, wrap=tk.WORD, height=6, font=("Helvetica", 14))
        self.input_text.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=36, pady=(36, 12))
        self.input_text.insert(tk.END, "Inserta tu código Dart aquí...")

        # Frame para botones
        self.buttons_frame = tk.Frame(self.parent)
        self.buttons_frame.grid(row=2, column=0, sticky="ns", padx=(36, 0), pady=(0, 36))

        # Espaciador para centrar botones
        self.top_spacer = tk.Frame(self.buttons_frame)
        self.top_spacer.pack(side="top", expand=True, fill='y')

        #botones
        self.eval_button = tk.Button(self.buttons_frame, text="Evaluar código", width=21,
                                     command=self.evaluate_code,
                                     font=("Helvetica", 14), bg="#4398e8", activebackground="#006fd6")
        self.eval_button.pack(pady=(0, 10))

        self.reset_button = tk.Button(self.buttons_frame, text="Resetear Código", width=21,
                                      command=self.reset_code,
                                      font=("Helvetica", 14))
        self.reset_button.pack()

        # Espaciador para centrar botones
        self.bottom_spacer = tk.Frame(self.buttons_frame)
        self.bottom_spacer.pack(side="top", expand=True, fill='y')

        # Salida en pantalla
        self.output_label = tk.Label(self.parent, text="Live Preview", font=("Helvetica", 14))
        self.output_label.grid(row=1, column=2, sticky="w", padx=36)

        self.output_text = scrolledtext.ScrolledText(self.parent, wrap=tk.WORD, height=9, width=40,
                                                    font=("Helvetica", 14), state="disabled")
        self.output_text.grid(row=2, column=2, sticky="nsew", padx=36, pady=(0, 36))

        # Responsividad
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_rowconfigure(2, weight=0)
        self.parent.grid_columnconfigure(0, weight=0)
        self.parent.grid_columnconfigure(1, weight=0)
        self.parent.grid_columnconfigure(2, weight=1)

    #funciones (EDITAR CON LA FUNCION RESPECTIVA DE ANALISIS)

    def evaluate_code(self):
        code = self.input_text.get("1.0", tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Entrada evaluada:\n{code}")
        self.output_text.config(state="disabled")

    def reset_code(self):
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, "Inserta tu código aquí...")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")


def create_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Dart Playground")
    WindowElements(new_window)


# Configuración base de la ventana principal
root = tk.Tk()
root.title("Dart Playground")
icon = tk.PhotoImage(file="assets/dart.png")
root.iconphoto(False, icon)

# Barra de menú
menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)
file_menu.add_command(label="Reset", command=lambda: app.reset_code())
file_menu.add_command(label="New Window", command=create_new_window)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Evaluation Results")
help_menu.add_command(label="Documentation")
help_menu.add_command(label="Feedback")

app = WindowElements(root)

root.mainloop()
