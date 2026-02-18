import tkinter as tk
from tkinter import ttk
import validateDuplicateds as vd
import threading

# 1. Definir la función que se ejecutará al presionar el botón
def button_handled():
    progress_bar(True)
    hilo = threading.Thread(target=call_back)
    hilo.start()

def call_back():
    root.after(0, lambda: label_root.config(text=""))
    try:
       duplicate_quantity = vd.get_duplicateds()
       
       if duplicate_quantity == 0:
            root.after(0, lambda: show_message("No se han encontrado clientes con duplicados"))
       elif isinstance(duplicate_quantity, str):
             root.after(0, lambda: label_root.config(text="Error: revise el archivo de exportación"))
             root.after(0, lambda: show_message(f"{duplicate_quantity}"))
       else:
             root.after(0, lambda: show_message(f"Se han encontrado {duplicate_quantity} duplicados"))            
    finally:
     # 3. IMPORTANTE: Cuando el proceso termina, quitamos la carga
        root.after(0, lambda: progress_bar(False))

def show_message(message):
    # 1. Crear una ventana flotante (Toplevel)
    toast = tk.Toplevel()
    toast.overrideredirect(True) # Quita los bordes y botones de cerrar
    toast.attributes("-topmost", True) # Asegura que esté por encima de todo
    
    # 2. Diseño del Toast
    label = tk.Label(toast, text=message, bg="#333333", fg="white", 
                     padx=20, pady=10, font=("Arial", 10, "bold"))
    label.pack()

    # 3. Posicionamiento (abajo al centro)
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (toast.winfo_width() // 2)
    y = root.winfo_screenheight() - 150
    toast.geometry(f"+{x}+{y}")

    # 4. Auto-destrucción después de N milisegundos
    toast.after(10000, toast.destroy)

def center_window(window, width, height):
    # 1. Obtener el ancho y alto de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 2. Calcular las coordenadas X e Y para centrar
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # 3. Aplicar la geometría: "ancho x alto + posicion_x + posicion_y"
    window.geometry(f"{width}x{height}+{x}+{y}")


def progress_bar(state:bool):
    # 1. Mostrar la barra y empezar la animación
    if state:
        barra.pack(pady=10)
        barra.start(10)   
    else:
        barra.stop()
        barra.pack_forget()

# 2. Crear la window principal
root = tk.Tk()
root.title("Duplicados")
root.geometry("300x100")
root.attributes('-topmost',True)
center_window(root, 300, 90)

# 3. Crear una etiqueta (Label)
label_root = tk.Label(root, text="")
label_root.pack(pady=1) # 'pack' coloca el elemento en la window


# Widget de carga
# mode='indeterminate' hace que la barra rebote de lado a lado
barra = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
# 4. Crear el botón y asociar el evento con 'command'
# Nota: Pasamos el nombre de la función sin paréntesis
boton = tk.Button(root, text="Generar Duplicados.xlsx", command=button_handled)
boton.pack()

# 5. Iniciar el bucle de la aplicación
root.mainloop()