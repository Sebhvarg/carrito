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

graph.add_edge(graph.get_node("FIEC"), graph.get_node("FCV"), 1) 
graph.add_edge(graph.get_node("FCV"), graph.get_node("FIMCP"), 1)
graph.add_edge(graph.get_node("FIMCP"), graph.get_node("FADCOM"), 1)
graph.add_edge(graph.get_node("FADCOM"), graph.get_node("FCNM"), 1)
graph.add_edge(graph.get_node("FCNM"), graph.get_node("FIEC"), 1)



