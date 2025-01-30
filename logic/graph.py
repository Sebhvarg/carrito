import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from logic.graph import Graph  # Importa la clase Graph
from math import radians, sin, cos, sqrt, atan2

# URL del servidor Flask
url_servidor = "http://192.168.3.12:5000/nodos"

# Obtener los nodos del servidor Flask
def obtener_nodos():
    try:
        response = requests.get(url_servidor)
        
        if response.status_code == 200:
            nodos = response.json()
            print("🌐 Nodos obtenidos:", nodos)
            return nodos
        else:
            print(f"❌ Error al obtener nodos: {response.status_code}")
            return {}
    except Exception as e:
        print(f"⚠️ Error en la solicitud: {e}")
        return {}

# Función para calcular la distancia entre dos puntos usando la fórmula de Haversine
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radio de la Tierra en kilómetros
    
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c  # Distancia en kilómetros

# Crear un grafo utilizando los nodos
def crear_grafo(nodos):
    grafo = Graph()

    # Agregar los nodos al grafo
    for nodo_id, nodo in nodos.items():
        lat = float(nodo["latitud"])
        lon = float(nodo["longitud"])
        # Usar el nodo_id como nombre del nodo
        grafo.add_node(nodo_id)
    
    # Agregar los bordes (edges) entre los nodos
    nodos_list = list(nodos.items())
    for i in range(len(nodos_list)):
        for j in range(i + 1, len(nodos_list)):
            nodo1_id, nodo1 = nodos_list[i]
            nodo2_id, nodo2 = nodos_list[j]
            
            lat1, lon1 = float(nodo1["latitud"]), float(nodo1["longitud"])
            lat2, lon2 = float(nodo2["latitud"]), float(nodo2["longitud"])
            
            # Calcular la distancia entre los dos nodos
            distancia = calcular_distancia(lat1, lon1, lat2, lon2)
            
            # Agregar un borde entre los dos nodos con la distancia como peso
            grafo.add_edge(nodo1_id, nodo2_id, distancia)
    
    print("🗺️ Grafo creado:", grafo)
    return grafo

if __name__ == "__main__":
    nodos = obtener_nodos()
    if nodos:
        grafo = crear_grafo(nodos)
