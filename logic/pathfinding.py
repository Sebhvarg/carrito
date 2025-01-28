import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import heapq as hq
from logic.graph import Graph, Node


def shortest_path(graph, start, end):
    # Si recibimos objetos Node, trabajamos con sus nombres
    if isinstance(start, Node):
        start = start.name
    if isinstance(end, Node):
        end = end.name
    
    queue = []
    hq.heappush(queue, (0, start))  # (costo, nombre_nodo)
    visited = set()
    # Almacenamos tuplas de (costo_total, nodo_anterior)
    distances = {start: (0, None)}
    
    while queue:
        current_cost, current_node_name = hq.heappop(queue)
        
        if current_node_name == end:
            break
            
        if current_node_name in visited:
            continue
            
        visited.add(current_node_name)
        
        # Obtener el nodo actual y sus aristas
        current_node = graph.get_node(current_node_name)
        for edge in current_node.edges:
            next_node_name = edge.target.name
            if next_node_name in visited:
                continue
                
            new_cost = current_cost + edge.weight
            
            if next_node_name not in distances or new_cost < distances[next_node_name][0]:
                distances[next_node_name] = (new_cost, current_node_name)
                hq.heappush(queue, (new_cost, next_node_name))
    
    # Si no encontramos el destino
    if end not in distances:
        return None
        
    # Reconstruir el camino
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = distances[current][1]
    
    return path[::-1]

# Función de prueba
def test_path():
    graph = Graph()
    
    # Agregar las aristas
    graph.add_edge("FIEC", "FCNM", 5)
    graph.add_edge("FCNM", "FICT", 3)
    graph.add_edge("FIEC", "FICT", 7)
    
    def print_path_details(path):
        if not path:
            print("No se encontró un camino")
            return
            
        print("Camino encontrado:")
        total_cost = 0
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            edge = graph.get_edge(current, next_node)
            cost = edge.weight
            total_cost += cost
            print(f"  {current} --({cost})--> {next_node}")
        print(f"Costo total: {total_cost}")
    
    try:
        # Probar con nodos
        path1 = shortest_path(graph, graph.get_node("FIEC"), graph.get_node("FCNM"))
        print("\nPrueba 1: FIEC a FCNM")
        print_path_details(path1)
        
        # Probar con strings
        path2 = shortest_path(graph, "FIEC", "FICT")
        print("\nPrueba 2: FIEC a FICT")
        print_path_details(path2)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_path()