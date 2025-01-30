# archivo: ui/app.py
# archivo: main.py

import sys
import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Asegúrate de que el directorio 'ui' está en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

class GraphApp:
    def __init__(self, archivo):
        # Cargar coordenadas desde el archivo
        self.coordenadas = self.cargar_coordenadas(archivo)
        # Crear el grafo
        self.G = self.crear_grafo()

    def cargar_coordenadas(self, archivo):
        coordenadas = []
        try:
            with open(archivo, 'r') as f:
                for linea in f:
                    lat, lon = map(float, linea.strip().split(','))
                    coordenadas.append((lat, lon))
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
        return coordenadas

    def crear_grafo(self):
        G = nx.Graph()
        for idx, coord in enumerate(self.coordenadas):
            G.add_node(idx, lat=coord[0], lon=coord[1])

        for i in range(len(self.coordenadas) - 1):
            coord1, coord2 = self.coordenadas[i], self.coordenadas[i + 1]
            distancia = geodesic(coord1, coord2).meters
            ponderacion = 1 if distancia < 1 else 2
            G.add_edge(i, i + 1, weight=distancia, ponderacion=ponderacion)

        coord1, coord2 = self.coordenadas[-1], self.coordenadas[0]
        distancia = geodesic(coord1, coord2).meters
        ponderacion = 1 if distancia < 1 else 2
        G.add_edge(len(self.coordenadas) - 1, 0, weight=distancia, ponderacion=ponderacion)

        return G

    def obtener_camino_mas_corto(self, nodo_inicio, nodo_destino):
        try:
            camino_mas_corto = nx.shortest_path(self.G, source=nodo_inicio, target=nodo_destino, weight='weight')
            distancia_total = nx.shortest_path_length(self.G, source=nodo_inicio, target=nodo_destino, weight='weight')
            return camino_mas_corto, distancia_total
        except nx.NetworkXNoPath:
            return None, None

    def visualizar_grafo(self, camino_mas_corto=None):
        pos = {i: (self.G.nodes[i]['lon'], self.G.nodes[i]['lat']) for i in self.G.nodes}

        plt.figure(figsize=(8, 6))
        nx.draw(self.G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10)

        if camino_mas_corto:
            edge_list = list(zip(camino_mas_corto, camino_mas_corto[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=edge_list, edge_color='red', width=2)

        plt.title("Ruta más corta con Dijkstra")
        plt.show()

    def dibujar_grafo(self, ax):
        ax.clear()  # Limpia el gráfico antes de dibujar
        pos = {i: (self.G.nodes[i]['lon'], self.G.nodes[i]['lat']) for i in self.G.nodes}

        nx.draw(self.G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, ax=ax)
    
        ax.set_title("Grafo de Coordenadas")  # Usar 'ax.set_title()' en vez de 'plt.axes.set_title()'
