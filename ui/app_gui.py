
import sys
import os
import tkinter as tk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Asegúrate de que el directorio 'ui' está en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
import tkinter as tk
from tkinter import messagebox

class GraphAppGUI:
    def __init__(self, master, app):
        self.master = master
        self.app = app

        # Título de la ventana
        self.master.title("Selecciona tu Ruta")

        # Instrucción
        self.instruccion = tk.Label(master, text="Selecciona el nodo de inicio y destino")
        self.instruccion.grid(row=0, column=0, columnspan=2)

        # Opciones de nodos
        self.nodos = list(range(len(self.app.coordenadas)))  # Nodos disponibles para seleccionar
        self.nodo_inicio_var = tk.StringVar()
        self.nodo_inicio_var.set(str(self.nodos[0]))  # Nodo inicial por defecto
        self.nodo_destino_var = tk.StringVar()
        self.nodo_destino_var.set(str(self.nodos[1]))  # Nodo destino por defecto

        # Crear los menús desplegables
        self.nodo_inicio_menu = tk.OptionMenu(master, self.nodo_inicio_var, *self.nodos)
        self.nodo_inicio_menu.grid(row=1, column=0)

        self.nodo_destino_menu = tk.OptionMenu(master, self.nodo_destino_var, *self.nodos)
        self.nodo_destino_menu.grid(row=1, column=1)

        # Botón para calcular el camino más corto
        self.calcular_btn = tk.Button(master, text="Calcular Camino Más Corto", command=self.calcular_camino)
        self.calcular_btn.grid(row=2, column=0, columnspan=2)

        # Botón para mostrar el grafo
        self.mostrar_grafo_btn = tk.Button(master, text="Mostrar Grafo", command=self.mostrar_grafo)
        self.mostrar_grafo_btn.grid(row=3, column=0, columnspan=2)

    def calcular_camino(self):
        try:
            nodo_inicio = int(self.nodo_inicio_var.get())
            nodo_destino = int(self.nodo_destino_var.get())
            camino_mas_corto, distancia_total = self.app.obtener_camino_mas_corto(nodo_inicio, nodo_destino)

            if camino_mas_corto:
                mensaje = f"Camino más corto: {camino_mas_corto}\nDistancia total: {distancia_total:.2f} metros"
                messagebox.showinfo("Resultado", mensaje)
                self.app.visualizar_grafo(camino_mas_corto)
            else:
                messagebox.showerror("Error", "No existe un camino entre los nodos seleccionados.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, selecciona nodos válidos.")

    def mostrar_grafo(self):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_title("Visualización del Grafo")

        # Aquí dibujas el grafo usando los datos de tu aplicación
        self.app.dibujar_grafo(ax)  # Esto debe ser implementado en tu clase GraphApp

        # Mostrar el gráfico en la interfaz Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

        # Actualizar el layout para que el botón y el grafo se ajusten en la pantalla
        self.master.update()
