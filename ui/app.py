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
        self.start_node_var = tk.StringVar()
        self.end_node_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.result_var = tk.StringVar()

        ttk.Label(self.master, text="Seleccione el lugar de inicio:").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.master, text="Seleccione el lugar de destino:").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(self.master, text="Nuevo peso de la arista:").grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(self.master, textvariable=self.result_var, foreground="blue").grid(row=3, column=1, padx=10, pady=10)

        nodes = list(self.graph.get_nodes())
        self.start_dropdown = ttk.Combobox(self.master, textvariable=self.start_node_var, values=nodes, state="readonly")
        self.start_dropdown.grid(row=0, column=2, padx=10, pady=5)

        self.end_dropdown = ttk.Combobox(self.master, textvariable=self.end_node_var, values=nodes, state="readonly")
        self.end_dropdown.grid(row=1, column=2, padx=10, pady=5)

        self.weight_entry = ttk.Entry(self.master, textvariable=self.weight_var)
        self.weight_entry.grid(row=2, column=2, padx=10, pady=5)

        self.update_weight_button = ttk.Button(self.master, text="Actualizar Peso", command=self.update_edge_weight)
        self.update_weight_button.grid(row=4, column=1, columnspan=2, pady=10)

        self.find_button = ttk.Button(self.master, text="Buscar Camino Más Corto", command=self.find_shortest_path)
        self.find_button.grid(row=5, column=1, columnspan=2, pady=10)

        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, rowspan=4)

        self.draw_graph()

    def draw_graph(self):
        self.canvas.delete("all")
        node_radius = 20
        node_positions = {}

        width, height = 400, 400
        angle_gap = 360 / len(self.graph.get_nodes()) if self.graph.get_nodes() else 0
        for i, node in enumerate(self.graph.get_nodes()):
            angle = i * angle_gap
            x = width // 2 + 150 * math.cos(math.radians(angle))
            y = height // 2 + 150 * math.sin(math.radians(angle))
            node_positions[node.name] = (x, y)
            self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=node.name, font=("Arial", 12, "bold"))

        for edge in self.graph.edges:
            start = edge.source.name
            end = edge.target.name
            weight = edge.weight
            start_x, start_y = node_positions[start]
            end_x, end_y = node_positions[end]
            self.canvas.create_line(start_x, start_y, end_x, end_y, width=2, fill="black")
            midpoint_x = (start_x + end_x) / 2
            midpoint_y = (start_y + end_y) / 2
            self.canvas.create_rectangle(midpoint_x - 15, midpoint_y - 10, midpoint_x + 15, midpoint_y + 10, fill="yellow", outline="black")
            self.canvas.create_text(midpoint_x, midpoint_y, text=str(weight), font=("Arial", 14, "bold"), fill="black")

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

        edge = self.graph.get_edge(source, target)
        if edge:
            edge.weight = new_weight
            self.graph.get_edge(target, source).weight = new_weight
            self.draw_graph()
        else:
            messagebox.showerror("Error", f"No existe una arista entre {source} y {target}.")

    def find_shortest_path(self):
        start = self.start_node_var.get()
        end = self.end_node_var.get()

        if not start or not end:
            messagebox.showerror("Error", "Por favor, seleccione los nodos de inicio y destino.")
            return

        path = shortest_path(self.graph, start, end)

        if path is None:
            self.result_var.set("No hay camino disponible.")
        else:
            self.result_var.set(" → ".join(path))
            self.animate_shortest_path(path)
            self.send_route_to_arduino(path)

    def animate_shortest_path(self, path):
        print(f"Animando ruta: {' → '.join(path)}")
        # Aquí puedes agregar lógica para visualizar el camino

    def send_route_to_arduino(self, path):
        if self.arduino:
            for node in path:
                self.arduino.write(f"{node}\n".encode())
                print(f"Enviando nodo {node} al arduino")
                time.sleep(1)
