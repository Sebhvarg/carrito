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
    
    def add_edge(self, source, target, weight = 1):
        if source not in self.nodes:
            self.nodes[source] = Node(source)
        if target not in self.nodes:
            self.nodes[target] = Node(target)
        
        edge = Edge(self.nodes[source], self.nodes[target], weight)
        
        self.nodes[source].add_edge(edge)
        self.edges.append(edge)
        
    def get_node(self, name):
        return self.nodes[name]
    
    def get_edge(self, source, target):
        for edge in self.edges:
            if edge.source.name == source and edge.target.name == target:
                return edge
        return None
    
    def get_nodes(self):
        return self.nodes.values()
    
    