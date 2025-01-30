import requests  # Asegúrate de tener esta librería instalada con 'pip install requests'
import math
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import time
import tkinter as tk
from tkinter import ttk, messagebox
from logic.graph import Graph
from logic.pathfinding import shortest_path
import threading

class GraphApp:
    def __init__(self, master, arduino=None, flask_url="http://localhost:5000/nodos"):
        self.master = master
        self.arduino = arduino
        self.graph = Graph()  # Crear el grafo
        self.flask_url = flask_url  # URL del servidor Flask
        self.server_running = False  # Estado del servidor
        self.server_ip = "http://192.168.3.12:5000/coordenadas"  # IP del servidor Flask
        
        # Crear widgets de la interfaz
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

        # Botones para iniciar/detener servidor
        self.start_server_button = ttk.Button(self.master, text="Iniciar Servidor", command=self.start_server)
        self.start_server_button.grid(row=4, column=0, pady=10)

        self.stop_server_button = ttk.Button(self.master, text="Detener Servidor", command=self.stop_server, state="disabled")
        self.stop_server_button.grid(row=4, column=1, pady=10)

        # Aquí iría el resto de la interfaz de la app, como el grafo, las entradas, etc.
        self.start_button = ttk.Button(self.master, text="Buscar Camino Más Corto", command=self.find_shortest_path)
        self.start_button.grid(row=5, column=0, columnspan=2, pady=10)

    def start_server(self):
        if not self.server_running:
            self.start_flask_server()  # Usar self para llamar a la función interna
            self.server_running = True
            self.start_server_button.config(state="disabled")
            self.stop_server_button.config(state="normal")
            print("Servidor Flask iniciado.")
        else:
            messagebox.showinfo("Información", "El servidor ya está corriendo.")

    def start_flask_server(self):
        def run_flask():
            from flask import Flask
            app = Flask(__name__)

            @app.route('/coordenadas', methods=['GET'])
            def recibir_coordenadas():
                lat = request.args.get('lat')
                lon = request.args.get('lon')

                if lat and lon:
                    print(f"📍 Coordenadas recibidas: Latitud = {lat}, Longitud = {lon}")
                    nodos[cantidad] = {"latitud": lat, "longitud": lon}
                    cantidad += 1        
                    return {"status": "OK", "latitud": lat, "longitud": lon}, 200
                else:
                    return {"error": "Faltan parámetros lat y lon"}, 400
                
            app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

        threading.Thread(target=run_flask).start()

    def stop_server(self):
        if self.server_running:
            stop_flask_server()  # Detener el servidor (esto es solo un placeholder, necesitarás lógica extra)
            self.server_running = False
            self.start_server_button.config(state="normal")
            self.stop_server_button.config(state="disabled")
            print("Servidor Flask detenido.")
            self.save_graph()  # Guardar el grafo cuando se detiene el servidor
        else:
            messagebox.showinfo("Información", "El servidor no está corriendo.")

    def save_graph(self):
        # Guardar el grafo a un archivo
        print("Guardando el grafo...")
        # Aquí puedes guardar el grafo, por ejemplo, como un archivo JSON
        with open("grafo.json", "w") as file:
            file.write(str(self.graph))  # Puedes convertir el grafo a JSON si es necesario
        print("Grafo guardado.")
        
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

        for edge in self.graph.get_edges():  # Utiliza el método get_edges
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

    def send_coordinates_to_server(self, lat, lon):
        try:
            response = requests.get(self.server_ip, params={'lat': lat, 'lon': lon})
            if response.status_code == 200:
                print(f"📤 Coordenadas enviadas: Lat = {lat}, Lon = {lon}")
            else:
                print(f"❌ Error al enviar coordenadas: {response.status_code}")
        except Exception as e:
            print(f"❌ Error al enviar coordenadas: {e}")