import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.graph import Graph
from logic.pathfinding import shortest_path


graph = Graph()
graph.add_node("FIEC")
graph.add_node("FCV")
graph.add_node("FIMCP")
graph.add_node("FADCOM")
graph.add_node("FCNM")

graph.add_edge("FIEC", "FIMCP", 8)
graph.add_edge("FIEC", "FCNM", 67)
graph.add_edge("FIMCP", "FCV", 5)
graph.add_edge("FCV", "FCNM", 2)
graph.add_edge("FIMCP", "FCNM", 4)

path = shortest_path(graph, graph.get_node("FIEC"), graph.get_node("FCV"))

print(path)