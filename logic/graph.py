import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.node import Node
from logic.edge import Edge

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, name):
        node = Node(name)
        self.nodes[name] = node
        return node
    
    def add_edge(self, source, target, weight=1):
        if source not in self.nodes:
            self.nodes[source] = Node(source)
        if target not in self.nodes:
            self.nodes[target] = Node(target)
        
        edge = Edge(self.nodes[source], self.nodes[target], weight)
        edge2= Edge(self.nodes[target], self.nodes[source], weight)
        
        self.nodes[source].add_edge(edge)
        self.nodes[target].add_edge(edge2)
        self.edges.append(edge)
        self.edges.append(edge2)
        
    def get_node(self, name):
        return self.nodes[name]
    
    def get_edge(self, source, target):
        for edge in self.edges:
            if edge.source.name == source and edge.target.name == target:
                return edge
        return None
    
    def get_nodes(self):
        return self.nodes.values()
    
    def get_neighbors(self, node):
        return [edge.target for edge in node.edges]
    

    def __str__(self):
        graph_str = ""
        for node in self.nodes.values():
            graph_str += f"Node {node.name}: "
            edges = [f"{edge.target.name} (weight {edge.weight})" for edge in node.edges]
            graph_str += ", ".join(edges) if edges else "No edges"
            graph_str += "\n"
        return graph_str
    
    def get_edge_weight(self, source, target):
        for edge in self.edges:
            if edge.source.name == source and edge.target.name == target:
                return edge.weight
        return None
