import heapq as hq

def shortest_path(graph, inicio, fin):
    ### Algoritmo de Dijkstra para encontrar el camino más corto entre dos nodos

    distancias = {node: float('infinity') for node in graph.get_nodes()}
    distancias[inicio] = 0

    # Cola de prioridad

    cola = [0, inicio]
    hq.heapify(cola)

    nodos_anteriores = { node: None for node in graph.get_nodes() }

    while len(cola) > 0:
        distancia, nodo = hq.heappop(cola)

        if nodo == fin:
            break

        for vecino in graph.get_neighbors(nodo):
            nueva_distancia = distancia + graph.get_edge(nodo, vecino).weight

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                hq.heappush(cola, (nueva_distancia, vecino))
                nodos_anteriores[vecino] = nodo
    
    #camino
    camino = []
    nodo_actual = fin   
    while nodo_actual is not None:
        camino.insert(0, nodo_actual)
        nodo_actual = nodos_anteriores[nodo_actual]

    if distancias[fin] == float('infinity'):
        return None
    
    camino.insert(0, inicio)
    return camino, distancias[fin]
        
