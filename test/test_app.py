# archivo: main.py

import sys
import os
import tkinter as tk

# Asegúrate de que el directorio 'ui' está en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui")))

from app import GraphApp  # Importar la clase GraphApp
from app_gui import GraphAppGUI  # Importar la clase GraphAppGUI

def main():
    root = tk.Tk()
    archivo = 'C:\\Users\\Lenovo\\Desktop\\carrito\\server\\coordenadas.txt'
    app = GraphApp(archivo)
    gui = GraphAppGUI(root, app)
    root.mainloop()

if __name__ == "__main__":
    main()
