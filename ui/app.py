import math
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import time
import tkinter as tk
from tkinter import ttk, messagebox
from logic.graph import Graph
from logic.pathfinding import shortest_path


class GraphApp:
    def __init__(self, master, arduino=None):
        self.master = master
        self.arduino = arduino
        self.graph = Graph()  # Crear el grafo

        # Agregar nodos y aristas iniciales
        self.graph.add_edge("FIEC", "FCNM", 5)
        self.graph.add_edge("FCNM", "FICT", 1)
        self.graph.add_edge("FIEC", "FICT", 7)
        self.graph.add_edge("FCNM", "FADCOM", 1)
        self.graph.add_edge("ADMISION", "ADMISION", 0)

        self.create_widgets()

    def create_widgets(self):
        # Variables de selección
        self.start_node_var = tk.StringVar()
        self.end_node_var = tk.StringVar()
        self.weight_var = tk.StringVar()  # Para capturar el nuevo peso de las aristas
        self.result_var = tk.StringVar()

        # Etiquetas
        ttk.Label(self.master, text="Seleccione el lugar de inicio:").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.master, text="Seleccione el lugar de destino:").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(self.master, text="Nuevo peso de la arista:").grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(self.master, textvariable=self.result_var, foreground="blue").grid(row=3, column=1, padx=10, pady=10)

        # Menús desplegables
        nodes = list(self.graph.get_nodes())
        self.start_dropdown = ttk.Combobox(self.master, textvariable=self.start_node_var, values=nodes, state="readonly")
        self.start_dropdown.grid(row=0, column=2, padx=10, pady=5)

        self.end_dropdown = ttk.Combobox(self.master, textvariable=self.end_node_var, values=nodes, state="readonly")
        self.end_dropdown.grid(row=1, column=2, padx=10, pady=5)

        # Entrada de texto para el nuevo peso
        self.weight_entry = ttk.Entry(self.master, textvariable=self.weight_var)
        self.weight_entry.grid(row=2, column=2, padx=10, pady=5)

        # Botones
        self.update_weight_button = ttk.Button(self.master, text="Actualizar Peso", command=self.update_edge_weight)
        self.update_weight_button.grid(row=4, column=1, columnspan=2, pady=10)

        self.find_button = ttk.Button(self.master, text="Buscar Camino Más Corto", command=self.find_shortest_path)
        self.find_button.grid(row=5, column=1, columnspan=2, pady=10)

        # Crear el lienzo para mostrar el grafo
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, rowspan=4)

        # Dibujar el grafo inicial
        self.draw_graph()

    def draw_graph(self):
        self.canvas.delete("all")  # Limpiar el lienzo antes de redibujar
        node_radius = 20
        node_positions = {}

        # Posicionar nodos en el lienzo
        width, height = 400, 400
        angle_gap = 360 / len(self.graph.get_nodes()) if self.graph.get_nodes() else 0
        for i, node in enumerate(self.graph.get_nodes()):
            angle = i * angle_gap
            x = width // 2 + 150 * math.cos(math.radians(angle))
            y = height // 2 + 150 * math.sin(math.radians(angle))
            node_positions[node.name] = (x, y)
            self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=node.name, font=("Arial", 12, "bold"))

        # Dibujar las aristas (edges)
        for edge in self.graph.edges:
            start = edge.source.name
            end = edge.target.name
            weight = edge.weight
            start_x, start_y = node_positions[start]
            end_x, end_y = node_positions[end]
            self.canvas.create_line(start_x, start_y, end_x, end_y, width=2, fill="black")

            # Calcular el punto medio de la arista
            midpoint_x = (start_x + end_x) / 2
            midpoint_y = (start_y + end_y) / 2

            # Crear un fondo de color para resaltar el texto (rectángulo)
            text_width = 30  # Ajuste de ancho del texto para mayor legibilidad
            text_height = 20
            self.canvas.create_rectangle(midpoint_x - text_width / 2, midpoint_y - text_height / 2,
                                         midpoint_x + text_width / 2, midpoint_y + text_height / 2,
                                         fill="yellow", outline="black")

            # Dibujar el peso de la arista con texto más grande
            self.canvas.create_text(midpoint_x, midpoint_y,
                                    text=str(weight),
                                    font=("Arial", 14, "bold"),  # Tamaño de fuente mayor
                                    fill="black")  # Texto en color negro

    def update_edge_weight(self):
        source = self.start_node_var.get()
        target = self.end_node_var.get()
        new_weight = self.weight_var.get()

        if not source or not target or not new_weight:
            messagebox.showerror("Error", "Por favor, seleccione los nodos y proporcione un peso.")
            return

        try:
            new_weight = int(new_weight)
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número entero.")
            return

        # Verificar si la arista existe
        edge = self.graph.get_edge(source, target)
        if edge:
            # Si la arista existe, actualizar el peso
            edge.weight = new_weight
            self.graph.get_edge(target, source).weight = new_weight  # Actualizar la arista inversa también
            self.draw_graph()  # Redibujar el grafo con el nuevo peso
        else:
            # Si no existe la arista, mostrar un mensaje de error
            messagebox.showerror("Error", f"No existe una arista entre {source} y {target}. No se puede actualizar el peso.")

    def animate_shortest_path(self, path):
        node_positions = {}
        width, height = 400, 400
        angle_gap = 360 / len(self.graph.get_nodes()) if self.graph.get_nodes() else 0
        node_radius = 20

        # Posicionamos los nodos
        for i, node in enumerate(self.graph.get_nodes()):
            angle = i * angle_gap
            x = width // 2 + 150 * math.cos(math.radians(angle))
            y = height // 2 + 150 * math.sin(math.radians(angle))
            node_positions[node.name] = (x, y)

        def draw_step(i, progress):
            if i < len(path) - 1:
                start = path[i]
                end = path[i + 1]
                start_x, start_y = node_positions[start]
                end_x, end_y = node_positions[end]

                # Calcular el progreso de la línea en función del porcentaje de avance
                line_x = start_x + (end_x - start_x) * progress
                line_y = start_y + (end_y - start_y) * progress

                # Dibujar la línea parcialmente
                self.canvas.create_line(start_x, start_y, line_x, line_y, width=8, fill="blue", dash=(4, 2))
                self.canvas.update()

                if progress < 1:
                    # Si no ha llegado al final, aumentamos el progreso
                    self.master.after(100, draw_step, i, progress + 0.05)  # Aumentar el progreso gradualmente
                else:
                    # Una vez que la línea ha llegado a su destino, ir al siguiente paso
                    self.master.after(600, draw_step, i + 1, 0)  # Comenzar con el siguiente segmento

        # Empezar la animación desde el primer segmento del camino
        draw_step(0, 0)

    def find_shortest_path(self):
        start = self.start_node_var.get()
        end = self.end_node_var.get()

        if not start or not end:
            messagebox.showerror("Error", "Seleccione los nodos de inicio y destino.")
            return

        path = self.shortest_path(self.graph, start, end)
        if path:
            self.result_var.set(f"Camino más corto: {' -> '.join(path)}")
            self.animate_shortest_path(path)  # Llamar a la función de animación
        else:
            self.result_var.set("No se encontró un camino.")

        # Redibujar el grafo con los nuevos datos
        self.draw_graph()

    def shortest_path(self, graph, start, end):
        # Aquí se implementa el algoritmo de camino más corto (Dijkstra, A*, etc.)
        # Suponiendo que la función ya existe y devuelve el camino más corto
        pass

    def send_route_to_arduino(self, path):
        if self.arduino:
            for node in path:
                # Envía cada nodo al Arduino
                data = f"{node}\n"
                self.arduino.write(data.encode())  # Enviar el nodo como comando al Arduino
                print(f"Enviando nodo {node} al arduino")
                time.sleep(1)  # Simula el movimiento del carro (reemplazar por comandos de movimiento reales)
           
