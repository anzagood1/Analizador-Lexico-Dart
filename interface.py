import tkinter as tk
from tkinter import scrolledtext

#FUNCIONES PARA CADA BOTON (SE DEBEN REEMPLAZAR CON LA INTERACCION CON EL ANALIZADOR)

def evaluate_code():
    code = input_text.get("1.0", tk.END)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Entrada evaluada:\n{code}")
    output_text.config(state="disabled")

def reset_code():
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, "Inserta tu código aquí...")
    output_text.delete("1.0", tk.END)

#CONFIGURACION BASE DE LA VENTANA

root = tk.Tk()
root.title("Dart Playground") #titulo
root.geometry("960x540") #dimensiones

icon = tk.PhotoImage(file='assets/dart.png')
root.iconphoto(False, icon) #icono

#ENTRADA DE TEXTO

input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=6, font=("Helvetica", 14))
input_text.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=36, pady=(36,12))
input_text.insert(tk.END, "Inserta tu código Dart aquí...")

#BOTONES

buttons_frame = tk.Frame(root)
buttons_frame.grid(row=2, column=0, sticky="ns", padx=(36,0),pady=(0,36))

# espaciador para centrar los botones
top_spacer = tk.Frame(buttons_frame)
top_spacer.pack(side="top", expand=True, fill='y')

eval_button = tk.Button(buttons_frame, text="Evaluar código", width=21, command=evaluate_code,font=("Helvetica", 14),bg="#4398e8", activebackground="#006fd6")
eval_button.pack(pady=(0,10))


reset_button = tk.Button(buttons_frame, text="Resetear Código", width=21, command=reset_code, font=("Helvetica", 14))
reset_button.pack()

# espaciador para centrar los botones
bottom_spacer = tk.Frame(buttons_frame)
bottom_spacer.pack(side="top", expand=True, fill='y')

#SALIDA EN PANTALLA

output_label = tk.Label(root, text="Live Preview", font=("Helvetica", 14))
output_label.grid(row=1, column=2, sticky="w", padx=36)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=9, width=40, font=("Helvetica", 14), state="disabled")
output_text.grid(row=2, column=2, sticky="nsew", padx=36, pady=(0,36))


#responsividad de las areas del grid (1 para expandibles, 0 para fijas)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)

root.mainloop()