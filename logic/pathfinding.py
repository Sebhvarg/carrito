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

