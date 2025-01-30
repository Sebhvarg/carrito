import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.app import GraphApp  # Asegúrate de importar la clase correcta

# Crear la ventana de Tkinter
root = tk.Tk()
root.title("Test de GraphApp")

# Instanciar la aplicación
app = GraphApp(root)

# Iniciar el bucle de eventos de Tkinter
root.mainloop()
