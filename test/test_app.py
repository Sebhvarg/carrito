# archivo: main.py

import sys
import os
import tkinter as tk

# Asegúrate de que el directorio 'ui' está en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "ui")))

from app import GraphApp
from app_gui import GraphAppGUI  # Importar la clase GraphAppGUI

def main():
    root = tk.Tk()
    archivo = 'coordenadas.txt'  # Nombre del archivo con las coordenadas
    app = GraphApp(archivo)
    gui = GraphAppGUI(root, app)
    root.mainloop()

if __name__ == "__main__":
    main()
