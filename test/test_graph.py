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

graph.add_edge("FIEC", "FIMCP", 1)
graph.add_edge("FIEC", "FCNM", 1)
graph.add_edge("FIMCP", "FCV", 1)
graph.add_edge("FCV", "FCNM", 1)
graph.add_edge("FIMCP", "FCNM", 1)

print(graph)
